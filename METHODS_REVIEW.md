# Methods review

- **Paper:** Avinash K. Dixit and Joseph E. Stiglitz, "Monopolistic Competition and Optimum Product Diversity,"
  *American Economic Review* 67(3), June 1977, pp. 297–308; read together with A. Michael Spence, "Product
  Selection, Fixed Costs, and Monopolistic Competition," *Review of Economic Studies* 43(2), June 1976,
  pp. 217–235.
- **Statistical focus:** the constant-elasticity pricing rule $`p_e = c/\rho`$ (Dixit and Stiglitz, equation 15)
  and the welfare comparison that equilibrium and constrained-optimal prices and numbers of firms coincide
  (equation 22), with the unconstrained optimum having more firms (equation 30).
- **Review standard:** internal consistency of the formal results, explicitness of assumptions, and the
  testability of the predictions.
- **What was read:** the full text of Dixit and Stiglitz (1977) from the American Economic Association's free
  copy of its "Top 20" articles (aeaweb.org/aer/top20/67.3.297-308.pdf). For Spence (1976) I read only the
  bibliographic record (Crossref, DOI 10.2307/2297319) and Dixit and Stiglitz's description of it; the
  extraction below therefore covers Dixit and Stiglitz, and nothing is claimed about Spence's text beyond that
  description.

## Methods summary

### Research design

A theoretical welfare analysis. A representative consumer has separable utility $`u = U(x_0, V(x_1, x_2, \ldots))`$
over a numeraire good and a group of differentiated products, each with a fixed cost $`a`$ and constant marginal
cost $`c`$. Section I takes $`V`$ to be constant elasticity of substitution with arbitrary $`U`$; Section II takes
$`U`$ to be Cobb–Douglas with a more general additive $`V`$; Section III treats asymmetric demand and cost. In each
case the paper compares the Chamberlinian free-entry equilibrium with a constrained optimum (each firm must break
even) and an unconstrained optimum (lump-sum transfers allowed).

### Sampling strategy, sample size, inclusion and exclusion criteria

Not applicable. The paper uses no data. Its "population" is the set of potential products, assumed symmetric in
Sections I and II, with $`n`$ large enough that each firm's price has a negligible effect on the group price index
(the large-group assumption, stated after equation 8).

### Independent and dependent variables

The primitives are the substitution parameter $`\rho`$ (with $`0 < \rho < 1`$), the fixed and marginal costs
$`a`$ and $`c`$, income, and the intersector elasticity of substitution $`\sigma(q)`$. The outcomes are the price
per variety, output per firm, the number of firms and the budget share of the group.

### Statistical methods

Not applicable in the econometric sense. The methods are first-order conditions, two-stage budgeting under
homotheticity, and comparative statics. Several derivations are omitted "to save space" and referred to the
authors' 1975 Warwick working paper (footnote 5), and the proof that active firms should have equal outputs and
prices in the constrained optimum is omitted ("We omit the proof").

### Reported effect sizes, confidence intervals, p-values

There are no estimates, intervals or p-values. The formal results in the table below play the role of the
paper's statistics.

### Missing data treatment

Not applicable.

### Stated limitations

The authors note that symmetry is restrictive, since real products often differ in how close substitutes they are
(Section I introduction); that income distribution is neglected, so $`U`$ is read as a social indifference map;
that uniqueness conditions in Section II are "rather involved and opaque" and are omitted; and that in the
variable-elasticity case the direction of the welfare bias "could go either way."

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Elasticity of substitution within the group | $`1/(1-\rho)`$, unitless | Eq. 14, p. 299 | How easily consumers switch between any two varieties under CES | Any empirical value of $`\rho`$ for a real industry |
| Elasticity of each firm's demand (dd curve) | $`(1+\beta)/\beta`$ with $`\beta = (1-\rho)/\rho`$ | Eq. 9 and text before eq. 15, p. 299 | Own-price elasticity facing one seller, holding the group price index fixed | That real sellers face constant elasticities |
| Equilibrium price | $`p_e = c(1+\beta) = c/\rho`$, a multiple of marginal cost | Eq. 15, p. 299 | Profit-maximizing markup under CES; constant across firms and costs | That markups stay fixed when costs or exchange rates change in practice |
| Constrained-optimum price | $`p_c = c(1+\beta)`$, equal to $`p_e`$ | Eq. 22, p. 301 | Equilibrium coincides with the zero-profit-constrained optimum under CES | Optimality under any non-CES preferences |
| Unconstrained-optimum price | $`p_u = c`$ | Eq. 26, p. 301 | Marginal-cost pricing with lump-sum transfers | Feasibility of such transfers |
| Firm output, equilibrium vs. unconstrained optimum | Equal | Eq. 27 and text, p. 301 | Equilibrium does not leave scale economies unexploited relative to the first best | Any measured excess capacity |
| Number of firms | $`n_u > n_c = n_e`$ | Eq. 30, p. 302 | The first best has more variety than the market | The size of the shortfall |
| Variable-elasticity equilibrium price | $`p_e = c[1 + \beta(x_e)]`$ | Eq. 36, p. 303 | Markup that varies with output when elasticity varies | Which direction markups move empirically |
| Direction of output bias, Section II | $`x_c \gtrless x_e`$ as $`\rho'(x) \lessgtr 0`$ | Eq. 41, p. 303 | Bias depends on how the elasticity of utility changes | An empirical sign |
| Asymmetric case | Market biased against goods with inelastic demand and high cost ("opera relative to football matches") | Section III, pp. 306–307; concluding remarks, p. 308 | Which goods the market under-provides | Magnitudes; distributional judgments are set aside |

## Interpretation notes

- The constant markup in equation 15 follows from two assumptions jointly, CES preferences and the large-group
  approximation that each firm ignores its effect on the price index. Neither is tested in the paper, and the
  authors present them as simplifications chosen for tractability.
- The headline welfare result (equilibrium equals constrained optimum) is specific to Section I. Section II shows
  that with variable elasticities the comparison turns on the elasticity of utility, not of demand, and can go
  either way. Readers who cite the paper for "the market provides the right variety" are citing only the CES case.
- The concluding remarks say there is "some presumption" of too few firms; this is a judgment drawn from the
  Section II cases, not a theorem.
- Equation 6 restricts $`\theta(q) < 1`$; the paper notes $`\theta`$ can be negative when the intersector elasticity
  exceeds one, and the uniqueness condition (17) is assumed rather than derived from primitives.

## Unanswered questions

- How large are the welfare gaps between equilibrium and the unconstrained optimum for plausible parameter values?
  The paper signs them but does not size them.
- How do the results change when firms are few enough to affect the group price index? The large-group
  approximation is assumed throughout Section I.
- Which empirical moments would distinguish the CES case from the variable-elasticity case of Section II? The
  paper does not propose a test. Later work used cost pass-through and market-size effects for this purpose.
- Spence's partial-equilibrium version is described by Dixit and Stiglitz as giving very similar results; a
  side-by-side check of where the two differ would need Spence's text, which was not read for this review.

## Items requiring expert verification

- The extraction of equations 6, 9, 16 and 36 relies on a scanned copy whose text layer garbles some symbols; the
  equation numbers and their meaning were checked against the surrounding prose, but exact typography should be
  confirmed against the printed page.
- Whether the omitted proofs (equal outputs in the constrained optimum; uniqueness in Section II) hold under the
  stated assumptions is not verified here; they are referred to the 1975 working paper, which was not read.
- No published correction or comment documenting an analytical error in the paper was found or consulted; the
  later literature (for example Kimball 1995; Atkeson and Burstein 2008) relaxes its assumptions rather than
  disputing its derivations.

This repository does not reproduce the paper, which has no data to reproduce. It takes the paper's constant-markup
rule, which implies one-for-one pass-through of cost changes to price, and confronts it with US import prices
for 2004–2026, where pass-through of exchange-rate changes is about 0.22 after two years.
