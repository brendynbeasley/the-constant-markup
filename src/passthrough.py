"""Does a constant markup survive contact with the exchange rate?

The Spence (1976) and Dixit-Stiglitz (1977) model of monopolistic competition gives every seller a
constant-elasticity demand curve, so every seller charges the same fixed multiple of marginal cost,
p = c * sigma / (sigma - 1). A foreign exporter whose costs are in yen, euros or pesos and who sells in
the United States therefore charges a dollar price p$ = mu * c* * E, where E is dollars per unit of its
currency. With mu constant, a 10% rise in E raises the dollar price by 10%: pass-through equals one.

This script tests that prediction on the Bureau of Labor Statistics import price indexes by country
of origin (via FRED), monthly exchange rates (FRED, Federal Reserve H.10) and exporter-country consumer
prices (BIS) for 2004-2026. It estimates cumulative pass-through at horizons of 1 to 36 months,
country by country and pooled, tests it against one, finds the biggest currency swing for each
country, and draws two figures.

Run from the repository root:
    python src/passthrough.py
Raw inputs are read from data/raw/ and downloaded there first if missing.
"""
import io
import json
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import statsmodels.api as sm
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

# Country -> (BLS import price index on FRED, FRED exchange rate, True if quoted as foreign units per
# dollar, BIS consumer price area code). Canada and Mexico use the manufactured-goods index so that
# crude oil, priced in dollars worldwide, does not dominate; the others are all-commodities indexes,
# which BLS publishes for these origins (imports from them are overwhelmingly manufactured goods).
COUNTRIES = {
    "Japan": ("JPNTOT", "EXJPUS", True, "JP"),
    "Germany": ("GERTOT", "EXUSEU", False, "DE"),
    "France": ("FRNTOT", "EXUSEU", False, "FR"),
    "United Kingdom": ("UKTOT", "EXUSUK", False, "GB"),
    "Canada": ("CANMANU", "EXCAUS", True, "CA"),
    "Mexico": ("MEXMANU", "EXMXUS", True, "MX"),
    "China": ("CHNTOT", "EXCHUS", True, "CN"),
}
# Reported country by country but left out of the pooled panel, since it contains Germany and France.
EXTRA = {"European Union": ("EECMANU", "EXUSEU", False, "XM")}
# Census country names in the annual trade file, for import values in the named table.
CENSUS_NAMES = {"Japan": "Japan", "Germany": "Germany", "France": "France",
                "United Kingdom": "United Kingdom", "Canada": "Canada", "Mexico": "Mexico",
                "China": "China", "European Union": "European Union"}
SAMPLE_START = "2004-01-01"   # the China, Germany, France and UK indexes begin December 2003
HORIZONS = [1, 3, 6, 12, 24, 36]
EPISODE_MONTHS = 24           # window length for each country's largest currency swing
YEN_HIGH_WINDOW = ("2020-01-01", "2022-12-01")  # search window for the yen's post-2020 peak against the dollar
YEN_LOW_WINDOW = ("2023-01-01", "2025-12-01")   # search window for its later trough
SUBPERIODS = [("2004-01-01", "2014-12-01"), ("2015-01-01", "2026-12-01")]
US_PPI = ["PCUOMFG--OMFG--", "WPU03THRU15"]  # BLS PPI: manufacturing industries; industrial commodities less fuels
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="
BIS_CPI = "https://data.bis.org/static/bulk/WS_LONG_CPI_csv_flat.zip"
CENSUS_TRADE = "https://www.census.gov/foreign-trade/balance/country.xlsx"
BLS_API = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
UA = {"User-Agent": "Brendyn Beasley research 83249437+brendynbeasley@users.noreply.github.com"}


def fetch(url, dest, **kw):
    if dest.exists():
        return
    print(f"  downloading {url}")
    r = requests.get(url, headers=UA, timeout=120, **kw)
    r.raise_for_status()
    tmp = dest.with_suffix(dest.suffix + ".part")
    tmp.write_bytes(r.content)
    tmp.rename(dest)


def fetch_bls_ppi(dest):
    """BLS public API, version 1 (no key; at most 10 years per request)."""
    if dest.exists():
        return
    rows = []
    for start, end in [(2003, 2012), (2013, 2022), (2023, 2026)]:
        print(f"  downloading BLS PPI {start}-{end}")
        body = {"seriesid": US_PPI, "startyear": str(start), "endyear": str(end)}
        r = requests.post(BLS_API, json=body, headers=UA, timeout=120)
        r.raise_for_status()
        for s in r.json()["Results"]["series"]:
            for d in s["data"]:
                if d["period"].startswith("M") and d["period"] != "M13":
                    rows.append((s["seriesID"], f"{d['year']}-{d['period'][1:]}-01", float(d["value"])))
    df = pd.DataFrame(rows, columns=["series", "date", "value"]).sort_values(["series", "date"])
    df.to_csv(dest, index=False)


def get_raw():
    RAW.mkdir(parents=True, exist_ok=True)
    ids = sorted({v[0] for v in {**COUNTRIES, **EXTRA}.values()} |
                 {v[1] for v in {**COUNTRIES, **EXTRA}.values()})
    for i in ids:
        fetch(FRED + i, RAW / f"fred_{i}.csv")
    fetch(BIS_CPI, RAW / "bis_WS_LONG_CPI_csv_flat.zip")
    fetch(CENSUS_TRADE, RAW / "census_country_trade.xlsx")
    fetch_bls_ppi(RAW / "bls_ppi.csv")


def fred(series_id):
    df = pd.read_csv(RAW / f"fred_{series_id}.csv", na_values=["."])
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"])
    return df.dropna().set_index("date")["value"]


def bis_cpi():
    with zipfile.ZipFile(RAW / "bis_WS_LONG_CPI_csv_flat.zip") as z:
        name = [n for n in z.namelist() if n.endswith(".csv")][0]
        df = pd.read_csv(io.BytesIO(z.read(name)))
    df.columns = [c.split(":")[0] for c in df.columns]
    df = df[df["FREQ"].str.startswith("M") & df["UNIT_MEASURE"].str.startswith("628")]
    df["area"] = df["REF_AREA"].str.split(":").str[0]
    df["date"] = pd.to_datetime(df["TIME_PERIOD"] + "-01")
    return df.pivot_table(index="date", columns="area", values="OBS_VALUE")


def build_panel():
    cpi = bis_cpi()
    frames = []
    for name, (imp, fx, inverted, area) in {**COUNTRIES, **EXTRA}.items():
        p = fred(imp)
        e = fred(fx)
        e = 1.0 / e if inverted else e       # E = US dollars per unit of foreign currency
        merged = pd.DataFrame({"p": np.log(p), "e": np.log(e), "cpi": np.log(cpi[area])})
        both = merged.dropna()
        d = both[both.index >= SAMPLE_START].copy()
        d["country"] = name
        frames.append(d)
        print(f"  {name:15s} {imp:8s} {fx:7s} kept {len(d):3d} months "
              f"{d.index.min():%Y-%m} to {d.index.max():%Y-%m}; dropped {len(merged) - len(both)} months "
              f"outside the overlap of price, exchange-rate and CPI series and {len(both) - len(d)} before {SAMPLE_START[:7]}")
    panel = pd.concat(frames).reset_index().rename(columns={"index": "date"})
    return panel


def long_diffs(panel, h):
    out = []
    for name, d in panel.groupby("country"):
        d = d.sort_values("date").set_index("date")
        full = pd.date_range(d.index.min(), d.index.max(), freq="MS")
        d = d.reindex(full)
        dd = pd.DataFrame({"dp": d["p"] - d["p"].shift(h), "de": d["e"] - d["e"].shift(h),
                           "dcpi": d["cpi"] - d["cpi"].shift(h)}, index=full).dropna()
        dd["country"] = name
        out.append(dd)
    res = pd.concat(out)
    res.index.name = "date"
    return res.reset_index()


def ols_hac(y, X, lags):
    return sm.OLS(y, sm.add_constant(X)).fit(cov_type="HAC", cov_kwds={"maxlags": lags})


def ols_dk(y, X, time_codes, lags):
    """Driscoll-Kraay errors: robust to correlation across countries in the same month and to the
    serial correlation that overlapping long differences create."""
    return sm.OLS(y, X).fit(cov_type="hac-groupsum", cov_kwds={"time": time_codes, "maxlags": lags})


def row(model, var, **extra):
    b, se = model.params[var], model.bse[var]
    t1 = (b - 1.0) / se
    return {**extra, "beta": b, "se": se, "ci_low": b - 1.96 * se, "ci_high": b + 1.96 * se,
            "p_beta_eq_0": 2 * stats.norm.sf(abs(b / se)), "p_beta_eq_1": 2 * stats.norm.sf(abs(t1)),
            "implied_markup_elasticity": (1.0 - b) / b, "nobs": int(model.nobs), "r2": model.rsquared}


def per_country(panel):
    rows = []
    for h in HORIZONS:
        ld = long_diffs(panel, h)
        for name, d in ld.groupby("country"):
            m = ols_hac(d["dp"], d[["de", "dcpi"]], lags=h + 2)
            rows.append(row(m, "de", country=name, horizon=h, cpi_coef=m.params["dcpi"],
                            start=d["date"].min().strftime("%Y-%m"), end=d["date"].max().strftime("%Y-%m")))
    return pd.DataFrame(rows)


def pooled(panel, spec):
    """spec: 'country_fe' (country intercepts, Driscoll-Kraay errors) or 'month_fe' (adds a dummy for
    every month, so pass-through is identified only from currencies moving against each other)."""
    rows = []
    core = panel[panel["country"].isin(COUNTRIES)]
    for h in HORIZONS:
        ld = long_diffs(core, h)
        X = ld[["de", "dcpi"]].copy()
        X = X.join(pd.get_dummies(ld["country"], drop_first=False, dtype=float))
        if spec == "month_fe":
            X = X.join(pd.get_dummies(ld["date"].dt.strftime("%Y-%m"), prefix="m", drop_first=True, dtype=float))
        codes = pd.factorize(ld["date"], sort=True)[0]  # chronological time index
        m = ols_dk(ld["dp"], X, codes, lags=h + 2)
        rows.append(row(m, "de", spec=spec, horizon=h, cpi_coef=m.params["dcpi"],
                        countries=ld["country"].nunique(), months=ld["date"].nunique()))
    return pd.DataFrame(rows)


def episodes(panel):
    """For each country, the 24-month window with the largest move in its currency against the dollar."""
    imports = census_imports()
    rows = []
    for name, d in panel.groupby("country"):
        d = d.sort_values("date").set_index("date")
        de = d["e"] - d["e"].shift(EPISODE_MONTHS)
        end = de.abs().idxmax()
        start = end - pd.DateOffset(months=EPISODE_MONTHS)
        rows.append(episode_row(d, name, start, end, imports.get(name, np.nan)))
    out = pd.DataFrame(rows).sort_values("us_imports_2025_bn", ascending=False)
    # The most recent yen swing, from its strongest month in 2020-22 to its weakest in 2023-25.
    d = panel[panel["country"] == "Japan"].sort_values("date").set_index("date")
    hi = d.loc[YEN_HIGH_WINDOW[0]:YEN_HIGH_WINDOW[1], "e"].idxmax()
    lo = d.loc[YEN_LOW_WINDOW[0]:YEN_LOW_WINDOW[1], "e"].idxmin()
    recent = episode_row(d, "Japan (recent yen slide)", hi, lo, imports.get("Japan", np.nan))
    recent["yen_per_dollar_start"] = float(np.exp(-d.loc[hi, "e"]))
    recent["yen_per_dollar_end"] = float(np.exp(-d.loc[lo, "e"]))
    recent["dollars_per_million_yen_start"] = 1e6 * float(np.exp(d.loc[hi, "e"]))
    recent["dollars_per_million_yen_end"] = 1e6 * float(np.exp(d.loc[lo, "e"]))
    return pd.concat([out, pd.DataFrame([recent])], ignore_index=True)


def episode_row(d, name, start, end, imports_bn):
    a, b = d.loc[start], d.loc[end]
    pred = (b["e"] - a["e"]) + (b["cpi"] - a["cpi"])
    act = b["p"] - a["p"]
    return {"country": name, "start": f"{start:%Y-%m}", "end": f"{end:%Y-%m}",
            "currency_change_pct": 100 * (np.exp(b["e"] - a["e"]) - 1),
            "home_cpi_change_pct": 100 * (np.exp(b["cpi"] - a["cpi"]) - 1),
            "ces_predicted_dollar_price_change_pct": 100 * (np.exp(pred) - 1),
            "actual_dollar_price_change_pct": 100 * (np.exp(act) - 1),
            "share_of_predicted_log_change": act / pred,
            "implied_markup_change_pct": 100 * (np.exp(act - pred) - 1),
            "us_imports_2025_bn": imports_bn}


def census_imports():
    """Annual US goods imports by partner from the Census country file, 2025, in billions of dollars."""
    raw = pd.read_excel(RAW / "census_country_trade.xlsx", engine="openpyxl")
    raw.columns = [str(c).strip() for c in raw.columns]
    year_col = [c for c in raw.columns if c.lower() == "year"][0]
    name_col = [c for c in raw.columns if c.lower() == "ctyname"][0]
    imp_col = [c for c in raw.columns if c.upper() == "IYR"][0]
    sub = raw[raw[year_col] == 2025]
    out = {}
    for k, v in CENSUS_NAMES.items():
        hit = sub[sub[name_col].str.strip() == v]
        if len(hit):
            out[k] = hit[imp_col].iloc[0] / 1000.0
    print(f"  Census country file: {len(sub)} partner rows for 2025, matched {len(out)} of {len(CENSUS_NAMES)}")
    return out


def figure_horizons(pc, mf):
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.axhline(1, color="#888", ls="--", lw=1)
    ax.text(0.6, 1.03, "constant markup (CES) predicts 1", va="bottom", fontsize=9, color="#555")
    ax.axhline(0, color="#bbb", lw=0.8)
    for df, lab, col, off in [(pc, "country intercepts", "#1f5a96", -0.35), (mf, "plus month effects", "#c0612b", 0.35)]:
        x = np.array(df["horizon"]) + off
        ax.errorbar(x, df["beta"], yerr=1.96 * df["se"], fmt="o-", color=col, capsize=3, label=lab)
    ax.set_xticks(HORIZONS)
    ax.set_xlabel("months after the exchange-rate change")
    ax.set_ylabel("share of the currency move in the dollar price")
    ax.set_xlim(0, 38)
    ax.set_ylim(-0.1, 1.15)
    ax.set_title("Exchange-rate pass-through into US import prices, 7 countries, 2004-2026", fontsize=10)
    ax.legend(loc="center right", frameon=False, fontsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "passthrough_by_horizon.png", dpi=150)
    plt.close(fig)


def figure_japan(panel):
    d = panel[panel["country"] == "Japan"].set_index("date").sort_index()
    base = d.index[0]
    actual = 100 * np.exp(d["p"] - d.loc[base, "p"])
    ces = 100 * np.exp((d["e"] + d["cpi"]) - (d.loc[base, "e"] + d.loc[base, "cpi"]))
    pd.DataFrame({"actual_index": actual, "ces_constant_markup_index": ces}).to_csv(OUT / "japan_paths.csv")
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.plot(actual.index, actual, color="#1f5a96", lw=2, label="dollar prices of goods from Japan (BLS)")
    ax.plot(ces.index, ces, color="#c0612b", lw=1.5, ls="--",
            label="path with a constant markup over Japanese consumer prices")
    ax.set_ylabel(f"index, {base:%B %Y} = 100")
    ax.set_title("Japanese exporters held dollar prices steady while the yen swung", fontsize=10)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "japan_yen_vs_prices.png", dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    print("Loading raw data")
    get_raw()
    panel = build_panel()
    print(f"Panel: {len(panel)} country-months; pooled panel uses {len(COUNTRIES)} countries "
          f"(European Union reported separately)")
    panel.to_csv(OUT / "panel_levels.csv", index=False, float_format="%.6f")

    print("Country-by-country pass-through")
    pcountry = per_country(panel)
    pcountry.to_csv(OUT / "passthrough_by_country.csv", index=False, float_format="%.5f")
    print(pcountry[pcountry["horizon"].isin([12, 24])][["country", "horizon", "beta", "se", "p_beta_eq_1", "nobs"]]
          .to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    print("Pooled pass-through")
    pc = pooled(panel, "country_fe")
    mf = pooled(panel, "month_fe")
    pooled_all = pd.concat([pc, mf])
    pooled_all.to_csv(OUT / "passthrough_pooled.csv", index=False, float_format="%.5f")
    print(pooled_all[["spec", "horizon", "beta", "se", "p_beta_eq_1", "nobs"]]
          .to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    print("Pooled pass-through without China (managed exchange rate)")
    no_cn = pooled(panel[panel["country"] != "China"], "country_fe")
    no_cn["spec"] = "country_fe_excl_china"
    no_cn.to_csv(OUT / "passthrough_pooled_excl_china.csv", index=False, float_format="%.5f")
    print(no_cn[["horizon", "beta", "se"]].to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    print("Pooled pass-through by sub-period (country intercepts)")
    subs = []
    for a, b in SUBPERIODS:
        sub = panel[(panel["date"] >= a) & (panel["date"] <= b)]
        r = pooled(sub, "country_fe")
        r["period"] = f"{a[:4]}-{min(b[:4], str(panel['date'].max().year))}"
        subs.append(r)
    subs = pd.concat(subs)
    subs.to_csv(OUT / "passthrough_pooled_subperiods.csv", index=False, float_format="%.5f")
    print(subs[["period", "horizon", "beta", "se", "nobs"]].to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    print("Largest currency swing per country")
    ep = episodes(panel)
    ep.to_csv(OUT / "episodes.csv", index=False, float_format="%.2f")
    print(ep.to_string(index=False, float_format=lambda v: f"{v:.2f}"))

    figure_horizons(pc, mf)
    figure_japan(panel)
    print("Wrote results/passthrough_by_country.csv, passthrough_pooled.csv, passthrough_pooled_excl_china.csv, "
          "passthrough_pooled_subperiods.csv, episodes.csv, japan_paths.csv, panel_levels.csv and two figures")


if __name__ == "__main__":
    main()
