# Research log: cross-fitness forest interpolation

## 2026-08-13 18:11 PDT

- Started from the proposed full-interval disjunction using the two weak
  derivatives at `r=1` and the leaf-annihilating endpoint score at
  `R_hyb`.  No graph search was performed.
- Derived the exact two-root directed-forest ratio for Bd and dB fixation on
  every finite weighted graph.
- Differentiated the forest law to obtain the exact covariance score.  The
  neutral Bd score counts upward forest edges; the neutral dB score of a
  target change is `indicator(up)-W_j(A)/d_j`.
- Cleared the normalized endpoint support to one signed product of the Bd
  and dB forest determinants and their root-marked numerators.
- Audited the quantifier order against the already proved dilute pair--leaf
  diagonal.  Its scaled Bd response has the exact pole
  `lambda_*/(r-1)`, while every finite scaled response is analytic and zero
  at neutrality.  This proves that no uniform first-order control from
  `r=1` survives the diagonal.
- Stopped the derivative-at-neutrality route at this conceptual
  obstruction.  The finite-graph disjunction itself is neither proved nor
  refuted.  The remaining plausible cross-fitness formulation must use a
  fixed `r_0>1` or retain the collapsing neutral layer as an explicit scale.
- Added a symbolic weighted-three-path replay for the determinant,
  derivative, endpoint-clearing, root-isolation, and pole identities.  It
  performs no graph or forest enumeration.
