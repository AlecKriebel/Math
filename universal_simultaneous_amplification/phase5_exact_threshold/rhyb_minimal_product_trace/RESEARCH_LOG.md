# Research log: minimal stationary product trace

All times are America/Los_Angeles.  No external communication or new graph
search was used; explicitly identified stored witnesses may be replayed as
exact audits.

## 2026-08-13 15:00 PDT -- singleton-root Schur and sharp Cauchy split

- Schur-compressed the exact duals from singleton/doubleton states all the
  way to singleton roots.  The resulting trace law `lambda_U` and Green
  excess reward `phi_U` retain every higher rank.
- Proved exact cancellation of both total singleton masses.  The minimal
  stationary product is equivalent to the singleton-root repayment
  inequality `(gamma.lambda_B)(alpha.lambda_D) >=
  r^3 bar(phi_B) bar(phi_D)` on the active branch.
- Derived the sharp Lagrange/Cauchy split into a nonnegative orientation
  square and one root-Hellinger remainder.  Proved that the all-portal
  root-Hellinger certificate needs only pair-supported portals.
- Exactly refuted the tempting common-conductance Picone route on unweighted
  `P3`: its Bd singleton trace has a positive leaf-to-leaf skip, while the dB
  reverse trace edge is zero.  Positive clocks and diagonal similarities
  cannot repair this support mismatch.
- Proved the root-Hellinger certificate for every portal on unweighted `P3`.
  The exact leaf--centre quadratic has minimum `193/42` after positive
  scaling.
- Audited the stronger entrywise portal inequality at the rational
  diagnostic fitness `r=3/2` on two stored hostile order-four rational
  graphs.  Both pass strictly; these are finite checks only, not a theorem
  at `R_hyb` or in arbitrary order.
- Identified the optional-stopping obstruction: the same-state cut-odds
  product is at most `r^3`, but a P3 cross-state pair has product
  `3*(5/2)>r^3`.  Any path-reversal proof must synchronize the two histories
  or retain a compensating likelihood current.
- Strongest new proved result: exact singleton-root/Cauchy reduction and a
  genuine all-portal theorem for `P3`.  Remaining universal gap: compare
  the two rule-specific root trace laws and Green excursion excesses.
- Best-guess completion toward the universal minimal-product theorem: 35%.
  The operator target is substantially smaller, but its cross-rule sign is
  still open.

## 2026-08-13 -- exact two-copy reduction

- Stopped the separate dB-density route after deriving its exact hole
  identity; the universal density theorem was not near closure and is not
  needed for the minimal gate disjunction.
- Proved `rho_dB-p=(s/r-sigma-EW)/s`, where
  `sigma=sum_i(1+sum_v h_r(P_vi))^(-1)`.  Thus the minimal product is
  automatic whenever `sigma>=s/r`, with the exact gap retained.
- Homogenized the minimal stationary product in alternating-excursion
  coordinates.  On its active branch it is exactly MPER,
  `S_B S_D >= r^3 X_B X_D/s^2`, with `X_U=M_U-spT_U`.
- Schur-traced the forcing to a two-copy product of singleton/doubleton
  spaces.  The signed reward is
  `f_gamma*f_alpha-r^3(κ_B/s-pτ_B)(κ_D/s-pτ_D)`.
- Proved that first-level singleton balances cannot establish even this
  weaker theorem: a rank-three pseudo-law on eight vertices has both mean
  densities tending to `3/8>p` while the singleton product is
  `O(lambda^2)`.
- The remaining sign is a genuine cross-rule comparison of the two killed
  Green corrections and their common rank-three boundary, not a finite
  graph or portal search.
