# Research log: universal `r=2` dB-dual mean ceiling

All timestamps use America/Los_Angeles.

## 2026-08-02

- 04:02 -- [NUMERICALLY OBSERVED] No violation of the candidate
  chi-square target-information bound `I2<=2` in extreme random weighted
  tests through seven vertices.  Complete graphs give equality.
- 04:11 -- [PROVED REDUCTION] Derived
  `I2 >= n E[1/(n-|A|)] >= n/(n-E|A|)` and the exact decomposition
  `I2=1+E|A|/n+(1/n)E sum e_v^2`.  Thus `I2<=2` would prove the universal
  half-density ceiling.  The contraction itself remains open.
- 04:19 -- [PROVED] Found an explicit graph-dependent linear Poisson
  certificate whenever
  `sum_i 1/(1+sum_v 2P_vi/(1+P_vi)) >= n/2`.  This proves the exact
  `r=2` half-density ceiling throughout that heterogeneous-temperature
  regime.  The complementary dense/near-regular regime remains open.
- 04:19 -- [PROVED FORMULA / NUMERICAL ROUTE] Derived the degree-three hole
  Mobius expansion of a general quadratic certificate.  Nonnegative pair
  coefficients in the potential force nonnegative cubic slack.  Broad LP
  screens support universal feasibility, but no all-graph formula or
  existence proof is claimed.

