"""Extension: do foreign sellers price off their American rivals?

Under the Spence-Dixit-Stiglitz constant-elasticity demand, a seller's markup does not depend on what
its competitors charge, so the dollar price of an import moves with the exporter's own costs and the
exchange rate and not at all with American producer prices. Under the variable-markup demand systems
that replaced it in international economics (Kimball 1995; Atkeson and Burstein 2008; the empirical
decomposition of Amiti, Itskhoki and Konings 2019), a seller with markup elasticity Gamma sets

    dlog p$ = 1/(1+Gamma) * (dlog c* + dlog E) + Gamma/(1+Gamma) * dlog P_US,

so the weight on its own costs and the weight on rivals' prices add up to one.

This script adds the US producer price index for manufacturing industries (BLS PPI series
PCUOMFG--OMFG--) to the pooled pass-through regression of src/passthrough.py and tests both
restrictions: delta = 0 (constant markup) and beta + delta = 1 (variable markup). A second US index,
industrial commodities less fuels (WPU03THRU15), is a robustness check.

Run from the repository root, after src/passthrough.py (which downloads the raw files):
    python src/competitor_prices.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))  # so the shared loaders import under python -I
import passthrough as pt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results"
MAIN_PPI = "PCUOMFG--OMFG--"


def us_ppi(series):
    df = pd.read_csv(ROOT / "data" / "raw" / "bls_ppi.csv", parse_dates=["date"])
    s = df[df["series"] == series].set_index("date")["value"]
    print(f"  BLS {series}: {len(s)} months, {s.index.min():%Y-%m} to {s.index.max():%Y-%m}")
    return np.log(s)


def add_ppi_diffs(ld, lppi, h):
    dppi = (lppi - lppi.shift(h)).rename("dppi")
    out = ld.merge(dppi, left_on="date", right_index=True, how="left")
    dropped = out["dppi"].isna().sum()
    if dropped:
        print(f"    h={h}: dropped {dropped} rows with no PPI change")
    return out.dropna(subset=["dppi"])


def fit(ld, h):
    X = ld[["de", "dcpi", "dppi"]].join(pd.get_dummies(ld["country"], dtype=float))
    codes = pd.factorize(ld["date"], sort=True)[0]  # chronological time index
    return sm.OLS(ld["dp"], X).fit(cov_type="hac-groupsum", cov_kwds={"time": codes, "maxlags": h + 2})


def summarize(m, **extra):
    b, d = m.params["de"], m.params["dppi"]
    V = m.cov_params()
    se_b, se_d = np.sqrt(V.loc["de", "de"]), np.sqrt(V.loc["dppi", "dppi"])
    se_sum = np.sqrt(V.loc["de", "de"] + V.loc["dppi", "dppi"] + 2 * V.loc["de", "dppi"])
    p_d0 = 2 * stats.norm.sf(abs(d / se_d))
    p_sum1 = 2 * stats.norm.sf(abs((b + d - 1) / se_sum))
    p_b1 = 2 * stats.norm.sf(abs((b - 1) / se_b))
    return {**extra, "beta_fx": b, "se_fx": se_b, "p_beta_eq_1": p_b1,
            "gamma_home_cpi": m.params["dcpi"], "se_home_cpi": m.bse["dcpi"],
            "delta_us_ppi": d, "se_us_ppi": se_d, "p_delta_eq_0": p_d0,
            "beta_plus_delta": b + d, "se_sum": se_sum, "p_sum_eq_1": p_sum1,
            "implied_markup_elasticity": (1 - b) / b, "nobs": int(m.nobs)}


def per_country_24(panel, lppi):
    rows = []
    ld = add_ppi_diffs(pt.long_diffs(panel, 24), lppi, 24)
    for name, d in ld.groupby("country"):
        m = sm.OLS(d["dp"], sm.add_constant(d[["de", "dcpi", "dppi"]])).fit(
            cov_type="HAC", cov_kwds={"maxlags": 26})
        b, dl = m.params["de"], m.params["dppi"]
        V = m.cov_params()
        se_sum = np.sqrt(V.loc["de", "de"] + V.loc["dppi", "dppi"] + 2 * V.loc["de", "dppi"])
        rows.append({"country": name, "horizon": 24, "beta_fx": b, "se_fx": m.bse["de"],
                     "delta_us_ppi": dl, "se_us_ppi": m.bse["dppi"],
                     "p_delta_eq_0": 2 * stats.norm.sf(abs(dl / m.bse["dppi"])),
                     "beta_plus_delta": b + dl,
                     "p_sum_eq_1": 2 * stats.norm.sf(abs((b + dl - 1) / se_sum)), "nobs": int(m.nobs)})
    return pd.DataFrame(rows)


def main():
    print("Loading panel from data/raw")
    panel = pt.build_panel()
    core = panel[panel["country"].isin(pt.COUNTRIES)]
    rows = []
    for series in [MAIN_PPI, "WPU03THRU15"]:
        lppi = us_ppi(series)
        for h in pt.HORIZONS:
            ld = add_ppi_diffs(pt.long_diffs(core, h), lppi, h)
            rows.append(summarize(fit(ld, h), us_index=series, horizon=h))
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "competitor_prices_pooled.csv", index=False, float_format="%.5f")
    print(res[["us_index", "horizon", "beta_fx", "se_fx", "delta_us_ppi", "se_us_ppi", "p_delta_eq_0",
               "beta_plus_delta", "p_sum_eq_1", "nobs"]].to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    print("Country by country, 24-month changes, PPI for manufacturing industries")
    pc = per_country_24(panel, us_ppi(MAIN_PPI))
    pc.to_csv(OUT / "competitor_prices_by_country.csv", index=False, float_format="%.4f")
    print(pc.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    print("Wrote results/competitor_prices_pooled.csv and results/competitor_prices_by_country.csv")


if __name__ == "__main__":
    main()
