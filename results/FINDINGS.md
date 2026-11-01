# Findings

## Plain English

- A fixed markup over cost, the pricing rule of Spence (1976) and Dixit and Stiglitz (1977), predicts that a 10% rise
  in a foreign currency raises the dollar price of that country's goods by 10%. Across imports from Japan, Germany,
  France, the United Kingdom, Canada, Mexico and China in 2004–2026, the rise was about 2.2% after two years, and a
  third year added almost nothing.
- When the yen slid from 103.79 to 157.86 per dollar between January 2021 and June 2024, a fixed markup over yen
  costs called for dollar prices of goods from Japan (Toyota, Honda, Subaru, Mazda) to fall 28.8%. They rose 3.6%,
  a markup about 45% wider measured against Japanese consumer prices.
- Every country falls short of full pass-through. Mexico (0.09) and Japan (0.11) are furthest away; Canada (0.57),
  whose manufacturing trade runs through cross-border supply chains, is closest.
- Import prices move with American producer prices even when exchange rates and foreign costs do not, a weight of
  0.33 at two years. The constant-markup model says that weight should be zero.

## Key to the labels

| Label | Meaning |
|---|---|
| `spec` | `country_fe`: country intercepts; `month_fe`: country intercepts plus a dummy for every month; `country_fe_excl_china`: China dropped |
| `horizon` | length $`h`$ of the long difference, in months |
| `beta`, `beta_fx` | pass-through, coefficient on $`\Delta_h \ln E`$ (US dollars per unit of foreign currency); constant markup predicts 1 |
| `se`, `se_fx` | Driscoll–Kraay (pooled) or Newey–West (single country) standard error, $`h+2`$ lags |
| `ci_low`, `ci_high` | 95% confidence interval |
| `p_beta_eq_0`, `p_beta_eq_1` | two-sided p-values for $`\beta = 0`$ and $`\beta = 1`$ |
| `cpi_coef`, `gamma_home_cpi` | coefficient on the change in the exporting country's log consumer price index |
| `implied_markup_elasticity` | $`(1-\beta)/\beta`$, the markup elasticity $`\Gamma`$ consistent with the estimated pass-through |
| `delta_us_ppi` | coefficient on the change in the log US producer price index (`us_index`); constant markup predicts 0 |
| `beta_plus_delta`, `se_sum`, `p_sum_eq_1` | sum of the two weights, its standard error and the p-value for a sum of 1 (variable-markup prediction) |
| `currency_change_pct` | change in the dollar value of the country's currency over the window |
| `ces_predicted_dollar_price_change_pct` | change in dollar price with a fixed markup: currency change plus home CPI change, in logs |
| `share_of_predicted_log_change` | actual log price change divided by the predicted one |
| `implied_markup_change_pct` | change in price relative to home-currency cost, $`\exp(\Delta\ln p - \Delta\ln E - \Delta\ln P^{*}) - 1`$ |
| `us_imports_2025_bn` | US goods imports from the partner in 2025, billions of dollars (Census) |

`results/panel_levels.csv` holds the monthly log levels behind every regression, and `results/japan_paths.csv` the
two series in `japan_yen_vs_prices.png` (actual dollar price index for goods from Japan and the fixed-markup path,
January 2004 = 100). The figure `passthrough_by_horizon.png` plots the pooled estimates below with 95% intervals.

## Tables

### passthrough_pooled.csv

| spec | horizon | beta | se | ci_low | ci_high | p_beta_eq_0 | p_beta_eq_1 | cpi_coef | implied_markup_elasticity | months | nobs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| country_fe | 1 | 0.067 | 0.018 | 0.031 | 0.103 | < 0.001 | < 0.001 | 0.223 | 13.903 | 270 | 1831 |
| country_fe | 3 | 0.125 | 0.028 | 0.069 | 0.180 | < 0.001 | < 0.001 | 0.506 | 7.032 | 268 | 1817 |
| country_fe | 6 | 0.159 | 0.030 | 0.100 | 0.218 | < 0.001 | < 0.001 | 0.719 | 5.297 | 265 | 1796 |
| country_fe | 12 | 0.175 | 0.024 | 0.129 | 0.222 | < 0.001 | < 0.001 | 0.819 | 4.702 | 260 | 1761 |
| country_fe | 24 | 0.221 | 0.019 | 0.184 | 0.257 | < 0.001 | < 0.001 | 0.825 | 3.531 | 248 | 1677 |
| country_fe | 36 | 0.225 | 0.022 | 0.182 | 0.268 | < 0.001 | < 0.001 | 0.839 | 3.445 | 236 | 1593 |
| month_fe | 1 | 0.047 | 0.024 | 0.000 | 0.094 | 0.048 | < 0.001 | -0.044 | 20.198 | 270 | 1831 |
| month_fe | 3 | 0.103 | 0.040 | 0.024 | 0.182 | 0.011 | < 0.001 | 0.094 | 8.727 | 268 | 1817 |
| month_fe | 6 | 0.132 | 0.045 | 0.043 | 0.222 | 0.004 | < 0.001 | 0.215 | 6.556 | 265 | 1796 |
| month_fe | 12 | 0.132 | 0.035 | 0.064 | 0.201 | < 0.001 | < 0.001 | 0.272 | 6.563 | 260 | 1761 |
| month_fe | 24 | 0.157 | 0.023 | 0.111 | 0.203 | < 0.001 | < 0.001 | 0.399 | 5.369 | 248 | 1677 |
| month_fe | 36 | 0.154 | 0.022 | 0.111 | 0.196 | < 0.001 | < 0.001 | 0.389 | 5.510 | 236 | 1593 |

### passthrough_pooled_excl_china.csv

| spec | horizon | beta | se | ci_low | ci_high | p_beta_eq_1 | cpi_coef | nobs |
|---|---|---|---|---|---|---|---|---|
| country_fe_excl_china | 1 | 0.068 | 0.019 | 0.031 | 0.104 | < 0.001 | 0.293 | 1561 |
| country_fe_excl_china | 3 | 0.126 | 0.028 | 0.071 | 0.182 | < 0.001 | 0.654 | 1549 |
| country_fe_excl_china | 6 | 0.161 | 0.029 | 0.103 | 0.218 | < 0.001 | 0.870 | 1531 |
| country_fe_excl_china | 12 | 0.177 | 0.023 | 0.133 | 0.222 | < 0.001 | 0.912 | 1501 |
| country_fe_excl_china | 24 | 0.228 | 0.017 | 0.195 | 0.262 | < 0.001 | 0.912 | 1429 |
| country_fe_excl_china | 36 | 0.238 | 0.020 | 0.200 | 0.277 | < 0.001 | 0.941 | 1357 |

### passthrough_pooled_subperiods.csv

| period | horizon | beta | se | ci_low | ci_high | p_beta_eq_1 | cpi_coef | nobs |
|---|---|---|---|---|---|---|---|---|
| 2004-2014 | 1 | 0.090 | 0.029 | 0.032 | 0.147 | < 0.001 | 0.135 | 858 |
| 2004-2014 | 3 | 0.163 | 0.044 | 0.076 | 0.250 | < 0.001 | 0.448 | 844 |
| 2004-2014 | 6 | 0.201 | 0.043 | 0.116 | 0.286 | < 0.001 | 0.646 | 823 |
| 2004-2014 | 12 | 0.213 | 0.028 | 0.158 | 0.269 | < 0.001 | 0.781 | 781 |
| 2004-2014 | 24 | 0.244 | 0.019 | 0.207 | 0.281 | < 0.001 | 0.796 | 697 |
| 2004-2014 | 36 | 0.250 | 0.028 | 0.196 | 0.305 | < 0.001 | 0.533 | 613 |
| 2015-2026 | 1 | 0.041 | 0.015 | 0.012 | 0.070 | < 0.001 | 0.249 | 966 |
| 2015-2026 | 3 | 0.077 | 0.019 | 0.039 | 0.115 | < 0.001 | 0.486 | 952 |
| 2015-2026 | 6 | 0.103 | 0.030 | 0.045 | 0.162 | < 0.001 | 0.704 | 931 |
| 2015-2026 | 12 | 0.128 | 0.046 | 0.038 | 0.219 | < 0.001 | 0.780 | 896 |
| 2015-2026 | 24 | 0.185 | 0.044 | 0.098 | 0.272 | < 0.001 | 0.829 | 812 |
| 2015-2026 | 36 | 0.138 | 0.013 | 0.112 | 0.164 | < 0.001 | 0.792 | 728 |

### passthrough_by_country.csv

| country | horizon | beta | se | ci_low | ci_high | p_beta_eq_0 | p_beta_eq_1 | cpi_coef | start | nobs |
|---|---|---|---|---|---|---|---|---|---|---|
| Canada | 1 | 0.141 | 0.040 | 0.064 | 0.219 | < 0.001 | < 0.001 | 1.022 | 2004-02 | 270 |
| China | 1 | 0.048 | 0.023 | 0.003 | 0.094 | 0.035 | < 0.001 | 0.032 | 2004-02 | 270 |
| European Union | 1 | 0.063 | 0.021 | 0.023 | 0.104 | 0.002 | < 0.001 | 0.101 | 2004-02 | 270 |
| France | 1 | 0.053 | 0.020 | 0.013 | 0.093 | 0.009 | < 0.001 | 0.071 | 2004-02 | 270 |
| Germany | 1 | 0.031 | 0.018 | -0.003 | 0.066 | 0.078 | < 0.001 | 0.152 | 2004-02 | 270 |
| Japan | 1 | 0.008 | 0.007 | -0.005 | 0.021 | 0.238 | < 0.001 | -0.022 | 2004-02 | 270 |
| Mexico | 1 | 0.023 | 0.016 | -0.009 | 0.055 | 0.161 | < 0.001 | -0.065 | 2009-01 | 211 |
| United Kingdom | 1 | 0.174 | 0.073 | 0.030 | 0.318 | 0.018 | < 0.001 | 0.271 | 2004-02 | 270 |
| Canada | 3 | 0.242 | 0.050 | 0.143 | 0.340 | < 0.001 | < 0.001 | 1.516 | 2004-04 | 268 |
| China | 3 | 0.088 | 0.032 | 0.025 | 0.151 | 0.006 | < 0.001 | 0.096 | 2004-04 | 268 |
| European Union | 3 | 0.121 | 0.026 | 0.070 | 0.172 | < 0.001 | < 0.001 | 0.441 | 2004-04 | 268 |
| France | 3 | 0.084 | 0.026 | 0.033 | 0.134 | 0.001 | < 0.001 | 0.524 | 2004-04 | 268 |
| Germany | 3 | 0.092 | 0.019 | 0.055 | 0.130 | < 0.001 | < 0.001 | 0.458 | 2004-04 | 268 |
| Japan | 3 | 0.029 | 0.009 | 0.010 | 0.047 | 0.002 | < 0.001 | 0.003 | 2004-04 | 268 |
| Mexico | 3 | 0.039 | 0.024 | -0.007 | 0.085 | 0.100 | < 0.001 | 0.015 | 2009-03 | 209 |
| United Kingdom | 3 | 0.286 | 0.094 | 0.101 | 0.470 | 0.002 | < 0.001 | 0.789 | 2004-04 | 268 |
| Canada | 6 | 0.327 | 0.067 | 0.195 | 0.459 | < 0.001 | < 0.001 | 1.781 | 2004-07 | 265 |
| China | 6 | 0.144 | 0.045 | 0.056 | 0.232 | 0.001 | < 0.001 | 0.211 | 2004-07 | 265 |
| European Union | 6 | 0.146 | 0.028 | 0.092 | 0.200 | < 0.001 | < 0.001 | 0.864 | 2004-07 | 265 |
| France | 6 | 0.100 | 0.031 | 0.039 | 0.160 | 0.001 | < 0.001 | 0.843 | 2004-07 | 265 |
| Germany | 6 | 0.110 | 0.021 | 0.069 | 0.150 | < 0.001 | < 0.001 | 0.629 | 2004-07 | 265 |
| Japan | 6 | 0.042 | 0.016 | 0.011 | 0.072 | 0.007 | < 0.001 | 0.008 | 2004-07 | 265 |
| Mexico | 6 | 0.053 | 0.031 | -0.006 | 0.113 | 0.080 | < 0.001 | 0.230 | 2009-06 | 206 |
| United Kingdom | 6 | 0.331 | 0.090 | 0.155 | 0.507 | < 0.001 | < 0.001 | 1.041 | 2004-07 | 265 |
| Canada | 12 | 0.432 | 0.093 | 0.250 | 0.614 | < 0.001 | < 0.001 | 1.982 | 2005-01 | 260 |
| China | 12 | 0.187 | 0.063 | 0.063 | 0.311 | 0.003 | < 0.001 | 0.440 | 2005-01 | 260 |
| European Union | 12 | 0.156 | 0.024 | 0.110 | 0.202 | < 0.001 | < 0.001 | 0.856 | 2005-01 | 260 |
| France | 12 | 0.102 | 0.035 | 0.034 | 0.171 | 0.003 | < 0.001 | 1.041 | 2005-01 | 260 |
| Germany | 12 | 0.119 | 0.027 | 0.066 | 0.172 | < 0.001 | < 0.001 | 0.722 | 2005-01 | 260 |
| Japan | 12 | 0.076 | 0.026 | 0.024 | 0.128 | 0.004 | < 0.001 | 0.072 | 2005-01 | 260 |
| Mexico | 12 | 0.039 | 0.032 | -0.023 | 0.102 | 0.218 | < 0.001 | 1.020 | 2009-12 | 201 |
| United Kingdom | 12 | 0.295 | 0.072 | 0.154 | 0.437 | < 0.001 | < 0.001 | 0.849 | 2005-01 | 260 |
| Canada | 24 | 0.571 | 0.099 | 0.377 | 0.766 | < 0.001 | < 0.001 | 1.595 | 2006-01 | 248 |
| China | 24 | 0.183 | 0.063 | 0.059 | 0.307 | 0.004 | < 0.001 | 0.394 | 2006-01 | 248 |
| European Union | 24 | 0.177 | 0.022 | 0.133 | 0.220 | < 0.001 | < 0.001 | 0.780 | 2006-01 | 248 |
| France | 24 | 0.147 | 0.049 | 0.050 | 0.244 | 0.003 | < 0.001 | 1.192 | 2006-01 | 248 |
| Germany | 24 | 0.137 | 0.033 | 0.072 | 0.202 | < 0.001 | < 0.001 | 0.650 | 2006-01 | 248 |
| Japan | 24 | 0.106 | 0.041 | 0.025 | 0.187 | 0.010 | < 0.001 | 0.219 | 2006-01 | 248 |
| Mexico | 24 | 0.085 | 0.038 | 0.012 | 0.159 | 0.023 | < 0.001 | 1.131 | 2010-12 | 189 |
| United Kingdom | 24 | 0.304 | 0.056 | 0.194 | 0.415 | < 0.001 | < 0.001 | 0.812 | 2006-01 | 248 |
| Canada | 36 | 0.552 | 0.078 | 0.399 | 0.704 | < 0.001 | < 0.001 | 1.355 | 2007-01 | 236 |
| China | 36 | 0.183 | 0.092 | 0.002 | 0.364 | 0.047 | < 0.001 | 0.234 | 2007-01 | 236 |
| European Union | 36 | 0.174 | 0.042 | 0.092 | 0.256 | < 0.001 | < 0.001 | 0.767 | 2007-01 | 236 |
| France | 36 | 0.184 | 0.076 | 0.034 | 0.334 | 0.016 | < 0.001 | 1.305 | 2007-01 | 236 |
| Germany | 36 | 0.110 | 0.041 | 0.029 | 0.192 | 0.008 | < 0.001 | 0.654 | 2007-01 | 236 |
| Japan | 36 | 0.122 | 0.042 | 0.040 | 0.203 | 0.003 | < 0.001 | 0.331 | 2007-01 | 236 |
| Mexico | 36 | 0.104 | 0.052 | 0.003 | 0.206 | 0.045 | < 0.001 | 1.451 | 2011-12 | 177 |
| United Kingdom | 36 | 0.294 | 0.105 | 0.089 | 0.500 | 0.005 | < 0.001 | 0.802 | 2007-01 | 236 |

### episodes.csv

| country | start | end | currency_change_pct | home_cpi_change_pct | ces_predicted_dollar_price_change_pct | actual_dollar_price_change_pct | share_of_predicted_log_change | implied_markup_change_pct | us_imports_2025_bn | yen_per_dollar_start | yen_per_dollar_end | dollars_per_million_yen_start | dollars_per_million_yen_end |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| European Union | 2006-03 | 2008-03 | 29.03 | 5.59 | 36.25 | 9.05 | 0.28 | -19.96 | 632.90 |  |  |  |  |
| Mexico | 2014-11 | 2016-11 | -31.96 | 5.59 | -28.15 | -6.28 | 0.20 | 30.44 | 534.31 |  |  |  |  |
| Canada | 2014-01 | 2016-01 | -23.00 | 3.01 | -20.69 | -11.45 | 0.52 | 11.65 | 381.92 |  |  |  |  |
| China | 2006-07 | 2008-07 | 16.89 | 12.31 | 31.28 | 6.26 | 0.22 | -19.06 | 308.65 |  |  |  |  |
| Germany | 2006-03 | 2008-03 | 29.03 | 5.10 | 35.61 | 9.20 | 0.29 | -19.48 | 155.83 |  |  |  |  |
| Japan | 2012-11 | 2014-11 | -30.33 | 4.05 | -27.51 | -4.37 | 0.14 | 31.91 | 145.84 |  |  |  |  |
| France | 2006-03 | 2008-03 | 29.03 | 4.41 | 34.72 | 12.46 | 0.39 | -16.52 | 68.07 |  |  |  |  |
| United Kingdom | 2007-03 | 2009-03 | -27.24 | 5.41 | -23.30 | 0.60 | -0.02 | 31.16 | 64.78 |  |  |  |  |
| Japan (recent yen slide) | 2021-01 | 2024-06 | -34.25 | 8.30 | -28.80 | 3.59 | -0.10 | 45.49 | 145.84 | 103.79 | 157.86 | 9635.00 | 6334.73 |

### competitor_prices_pooled.csv

| us_index | horizon | beta_fx | se_fx | gamma_home_cpi | se_home_cpi | delta_us_ppi | se_us_ppi | p_delta_eq_0 | beta_plus_delta | se_sum | p_sum_eq_1 | nobs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PCUOMFG--OMFG-- | 1 | 0.049 | 0.015 | 0.005 | 0.040 | 0.262 | 0.027 | < 0.001 | 0.311 | 0.035 | < 0.001 | 1831 |
| PCUOMFG--OMFG-- | 3 | 0.093 | 0.023 | 0.125 | 0.057 | 0.304 | 0.026 | < 0.001 | 0.397 | 0.039 | < 0.001 | 1817 |
| PCUOMFG--OMFG-- | 6 | 0.116 | 0.023 | 0.236 | 0.066 | 0.337 | 0.024 | < 0.001 | 0.453 | 0.034 | < 0.001 | 1796 |
| PCUOMFG--OMFG-- | 12 | 0.125 | 0.017 | 0.254 | 0.059 | 0.353 | 0.025 | < 0.001 | 0.477 | 0.034 | < 0.001 | 1761 |
| PCUOMFG--OMFG-- | 24 | 0.156 | 0.013 | 0.356 | 0.056 | 0.326 | 0.028 | < 0.001 | 0.483 | 0.032 | < 0.001 | 1677 |
| PCUOMFG--OMFG-- | 36 | 0.154 | 0.013 | 0.372 | 0.065 | 0.361 | 0.026 | < 0.001 | 0.514 | 0.031 | < 0.001 | 1593 |
| WPU03THRU15 | 1 | 0.040 | 0.014 | 0.034 | 0.044 | 0.215 | 0.019 | < 0.001 | 0.255 | 0.026 | < 0.001 | 1831 |
| WPU03THRU15 | 3 | 0.087 | 0.022 | 0.173 | 0.065 | 0.234 | 0.017 | < 0.001 | 0.321 | 0.027 | < 0.001 | 1817 |
| WPU03THRU15 | 6 | 0.111 | 0.022 | 0.310 | 0.080 | 0.245 | 0.017 | < 0.001 | 0.356 | 0.023 | < 0.001 | 1796 |
| WPU03THRU15 | 12 | 0.119 | 0.017 | 0.372 | 0.060 | 0.247 | 0.015 | < 0.001 | 0.366 | 0.021 | < 0.001 | 1761 |
| WPU03THRU15 | 24 | 0.154 | 0.013 | 0.450 | 0.045 | 0.240 | 0.023 | < 0.001 | 0.394 | 0.023 | < 0.001 | 1677 |
| WPU03THRU15 | 36 | 0.155 | 0.013 | 0.449 | 0.054 | 0.274 | 0.020 | < 0.001 | 0.429 | 0.018 | < 0.001 | 1593 |

### competitor_prices_by_country.csv

| country | beta_fx | se_fx | delta_us_ppi | se_us_ppi | p_delta_eq_0 | beta_plus_delta | p_sum_eq_1 | nobs |
|---|---|---|---|---|---|---|---|---|
| Canada | 0.077 | 0.053 | 1.328 | 0.163 | < 0.001 | 1.405 | 0.003 | 248 |
| China | 0.101 | 0.047 | 0.221 | 0.056 | < 0.001 | 0.322 | < 0.001 | 248 |
| European Union | 0.112 | 0.020 | 0.324 | 0.042 | < 0.001 | 0.437 | < 0.001 | 248 |
| France | 0.156 | 0.055 | -0.046 | 0.134 | 0.730 | 0.109 | < 0.001 | 248 |
| Germany | 0.086 | 0.032 | 0.248 | 0.036 | < 0.001 | 0.333 | < 0.001 | 248 |
| Japan | 0.118 | 0.020 | 0.206 | 0.039 | < 0.001 | 0.324 | < 0.001 | 248 |
| Mexico | 0.067 | 0.042 | 0.095 | 0.076 | 0.208 | 0.162 | < 0.001 | 189 |
| United Kingdom | 0.181 | 0.046 | 0.656 | 0.150 | < 0.001 | 0.837 | 0.195 | 248 |

