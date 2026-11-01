# Technical notes

This is the technical companion to the [README](README.md). It covers the original papers, the data, the
method, every test statistic and how to reproduce them. All tables are reprinted in
[results/FINDINGS.md](results/FINDINGS.md).

## The original study

A. Michael Spence, "Product Selection, Fixed Costs, and Monopolistic Competition," *Review of Economic Studies*
43(2), 1976, pp. 217–235. Avinash K. Dixit and Joseph E. Stiglitz, "Monopolistic Competition and Optimum Product
Diversity," *American Economic Review* 67(3), 1977, pp. 297–308.

Both papers are theory and report no data. In the Dixit–Stiglitz constant-elasticity case, with group utility
$`V = (\sum_i x_i^{\rho})^{1/\rho}`$ and $`0 < \rho < 1`$, the elasticity of substitution between varieties is
$`1/(1-\rho)`$ (their equation 14) and every active firm charges $`p_e = c/\rho`$ (equation 15). The market
equilibrium coincides with the optimum constrained by zero profits (equation 22), and the unconstrained optimum has
more firms of the same size (equation 30). Their Section II lets the elasticity vary with output, giving
$`p_e = c[1 + \beta(x_e)]`$ (equation 36), a markup that is no longer constant. The testable property taken here
is the constant markup, which implies complete pass-through of any cost change to price:

```math
p = \frac{\sigma}{\sigma - 1}\,c \quad\Longrightarrow\quad \frac{d\ln p^{\$}}{d\ln E} = \frac{d\ln p^{\$}}{d\ln c^{*}} = 1 .
```

## Headline results

| Test (pooled, 7 origins, 2004–2026) | Estimate | SE | Constant markup predicts | p for that prediction |
|---|---|---|---|---|
| Exchange-rate pass-through, 12 months | 0.175 | 0.024 | 1 | < 0.001 |
| Exchange-rate pass-through, 24 months | 0.221 | 0.019 | 1 | < 0.001 |
| Exchange-rate pass-through, 36 months | 0.225 | 0.022 | 1 | < 0.001 |
| Same, 24 months, with month effects | 0.157 | 0.023 | 1 | < 0.001 |
| Weight on US manufacturing PPI, 24 months | 0.326 | 0.028 | 0 | < 0.001 |
| Pass-through plus PPI weight, 24 months | 0.483 | 0.032 | 1 under variable markups | < 0.001 |

The implied markup elasticity at 24 months is $`\hat\Gamma = (1-\hat\beta)/\hat\beta = 3.53`$.

## Data

All files are in `data/raw/` and are re-downloaded by `src/passthrough.py` if deleted.

| File | Source | Content |
|---|---|---|
| `fred_JPNTOT.csv`, `fred_GERTOT.csv`, `fred_FRNTOT.csv`, `fred_UKTOT.csv`, `fred_CHNTOT.csv` | BLS import price indexes by locality of origin, via FRED | All commodities; Germany, France, UK and China from Dec 2003, Japan from Dec 1990 (index bases differ; only log changes are used) |
| `fred_CANMANU.csv`, `fred_MEXMANU.csv`, `fred_EECMANU.csv` | Same | Manufactured goods from Canada, Mexico (from Dec 2008) and the European Union |
| `fred_EXJPUS.csv`, `fred_EXUSEU.csv`, `fred_EXUSUK.csv`, `fred_EXCAUS.csv`, `fred_EXMXUS.csv`, `fred_EXCHUS.csv` | Federal Reserve H.10, via FRED | Monthly average exchange rates |
| `bis_WS_LONG_CPI_csv_flat.zip` | Bank for International Settlements, long CPI series | Monthly consumer price indexes, 2010 = 100 |
| `bls_ppi.csv` | BLS public data API, version 1 | PPI for manufacturing industries (`PCUOMFG--OMFG--`) and industrial commodities less fuels (`WPU03THRU15`) |
| `census_country_trade.xlsx` | US Census Bureau, foreign trade, `country.xlsx` | Annual goods imports by partner, used only for the 2025 import values |

All files were downloaded on 1 November 2026. The import price indexes measure US dollar prices at the border,
before tariffs and domestic distribution.

## Method

Rules fixed before the first run:

- **Sample.** January 2004 to September 2026. Mexico enters in December 2008, when its manufactured-goods index
  begins. October 2025, the month of the federal government shutdown, is missing from every BLS import index, so each country has 272 months (Mexico 213) and long differences that start or end in that month are dropped. The pooled panel uses Japan, Germany, France, the United Kingdom, Canada, Mexico and China. The European
  Union is estimated on its own, because it contains Germany and France.
- **Prices.** All-commodities indexes where BLS publishes them for the origin; manufactured goods for Canada and
  Mexico, whose all-commodities indexes are dominated by dollar-priced crude oil.
- **Exchange rate.** $`E`$ is US dollars per unit of foreign currency, so the constant-markup prediction is a
  coefficient of +1.
- **Cost proxy.** Home-country consumer price index from the BIS. No public source gives exporters' marginal cost in
  their own currency.
- **Horizons.** Long differences of 1, 3, 6, 12, 24 and 36 months.
- **Estimating equation.**

```math
\Delta_h \ln p_{c,t} = \alpha_c + \beta_h\,\Delta_h \ln E_{c,t} + \gamma_h\,\Delta_h \ln P^{*}_{c,t} + \varepsilon_{c,t}
```

- **Errors.** Pooled: Driscoll–Kraay with $`h+2`$ lags (statsmodels `hac-groupsum`, grouped by month).
  Time is indexed chronologically. Per country: Newey–West with $`h+2`$ lags. Tests use the normal distribution.
- **Second specification.** Adds a dummy for every month, so $`\beta_h`$ is identified only by cross-country
  differences in currency moves.
- **Episodes.** For each origin, the 24-month window with the largest absolute change in $`\ln E`$; the
  constant-markup prediction is $`\Delta\ln E + \Delta\ln P^{*}`$. A separate row covers the yen from its strongest
  month in 2020–22 (January 2021) to its weakest in 2023–25 (June 2024).
- **Extension** (Amiti, Itskhoki and Konings 2019). Adds $`\delta_h\,\Delta_h \ln P^{US}_t`$, the change in the US PPI
  for manufacturing industries, with the same country intercepts and errors. Constant markups imply
  $`\delta_h = 0`$; the variable-markup decomposition implies $`\beta_h + \delta_h = 1`$.

Added after the first run, as robustness checks: the pooled estimate without China, the split into 2004–2014 and
2015–2026, and the second US price index (`WPU03THRU15`).

## Full test statistics

Pooled pass-through, $`\hat\beta_h`$ (Driscoll–Kraay SE):

| Horizon | Country intercepts | SE | 95% CI | Month effects | SE | N |
|---|---|---|---|---|---|---|
| 1 | 0.067 | 0.018 | [0.031, 0.103] | 0.047 | 0.024 | 1,831 |
| 3 | 0.125 | 0.028 | [0.069, 0.180] | 0.103 | 0.040 | 1,817 |
| 6 | 0.159 | 0.030 | [0.100, 0.218] | 0.132 | 0.045 | 1,796 |
| 12 | 0.175 | 0.024 | [0.129, 0.222] | 0.132 | 0.035 | 1,761 |
| 24 | 0.221 | 0.019 | [0.184, 0.257] | 0.157 | 0.023 | 1,677 |
| 36 | 0.225 | 0.022 | [0.182, 0.268] | 0.154 | 0.022 | 1,593 |

At 24 months the coefficient on home consumer prices is 0.825 with country intercepts and 0.399 with month effects.
Without China, 24-month pass-through is 0.228 (0.017). By sub-period it is 0.244 (0.019) for 2004–2014 and 0.185
(0.044) for 2015–2026.

Country by country, 24 months (Newey–West SE): Canada 0.571 (0.099), United Kingdom 0.304 (0.056), China 0.183
(0.063), European Union 0.177 (0.022), France 0.147 (0.049), Germany 0.137 (0.033), Japan 0.106 (0.041), Mexico
0.085 (0.038). Every one rejects a coefficient of one with $`p < 0.001`$.

Extension at 24 months, PPI for manufacturing: $`\hat\beta = 0.156\ (0.013)`$, $`\hat\gamma = 0.356\ (0.056)`$,
$`\hat\delta = 0.326\ (0.028)`$, $`\hat\beta + \hat\delta = 0.483\ (0.032)`$. With industrial commodities less
fuels: $`\hat\delta = 0.240\ (0.023)`$, $`\hat\beta + \hat\delta = 0.394\ (0.023)`$. Both restrictions are rejected
at every horizon with both indexes ($`p < 0.001`$). Per country, $`\hat\delta`$ is 1.33 for Canada, 0.66 for the
United Kingdom (where $`\beta + \delta = 1`$ is not rejected, $`p = 0.20`$), 0.21 to 0.32 for Japan, Germany,
China and the European Union, and insignificant for France ($`p = 0.73`$) and Mexico ($`p = 0.21`$).

## Reproducing the results

```bash
pip install -r requirements.txt
python src/passthrough.py
python src/competitor_prices.py
```

Python 3.12 or later. The first script writes the pass-through tables, the episodes table and both figures; the
second writes the two `competitor_prices_*.csv` files. Deleting `data/raw/` makes the first script download
everything again (FRED, BIS, Census and three calls to the BLS API).

## References

- Amiti, M., Itskhoki, O. & Konings, J. (2019). International shocks, variable markups, and domestic prices.
  *Review of Economic Studies* 86(6), 2356–2402.
- Atkeson, A. & Burstein, A. (2008). Pricing-to-market, trade costs, and international relative prices. *American
  Economic Review* 98(5), 1998–2031.
- Dixit, A. K. & Stiglitz, J. E. (1977). Monopolistic competition and optimum product diversity. *American Economic
  Review* 67(3), 297–308.
- Driscoll, J. C. & Kraay, A. C. (1998). Consistent covariance matrix estimation with spatially dependent panel
  data. *Review of Economics and Statistics* 80(4), 549–560.
- Gopinath, G., Itskhoki, O. & Rigobon, R. (2010). Currency choice and exchange rate pass-through. *American
  Economic Review* 100(1), 304–336.
- Kimball, M. S. (1995). The quantitative analytics of the basic neomonetarist model. *Journal of Money, Credit and
  Banking* 27(4), 1241.
- Krugman, P. (1979). Increasing returns, monopolistic competition, and international trade. *Journal of
  International Economics* 9(4), 469–479.
- Spence, A. M. (1976). Product selection, fixed costs, and monopolistic competition. *Review of Economic Studies*
  43(2), 217–235.
