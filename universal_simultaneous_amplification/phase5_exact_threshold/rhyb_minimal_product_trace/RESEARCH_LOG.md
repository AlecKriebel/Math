# Research log: minimal stationary product trace

All times are America/Los_Angeles.  No external communication or new graph
search was used; explicitly identified stored witnesses may be replayed as
exact audits.

## 2026-08-13 15:50 PDT -- full-excursion repayment normalization

- Rewrote the root Green repayment bound in the honest alternating
  rank-`<=2`/rank-`>=3` excursion coordinates.  If
  `h_U=nu_U^-G_U^-`, `H_U=sum_i h_U({i})`, and
  `X_U=M_U/s-pT_U`, then exactly
  `lambda=h_1/H`, `eta=h_2/H`, and `bar(phi)=X/H`.
- Rescaled the doubleton rebate before applying `(I-L)^(-1)`.  Every
  singleton and crossing-current normalizer cancels.  The resulting clean
  sufficient target is `(x.y)^2 >= r^3[X_B]_+[X_D]_+(x.1)(x.e)`, with
  `y=(I-L)^(-1)hat(beta)`.  Its all-portal form again has a sharp pairwise
  copositivity criterion.
- Proved a route obstruction: the rank-three pseudo-law scaling leaves
  `lambda`, normalized doubletons, `L`, and the normalized root Green bound
  fixed, while `bar(phi)_B bar(phi)_D` grows as `epsilon^-2`.  Thus no proof
  using normalized low data plus singleton balances alone can control the
  full reward.  The doubleton/rank-three return equation is indispensable.
- Schur-traced the full normalized reward to the base-edge doubleton boundary:
  `bar(phi)_U=sum_D eta_D Psi_U(D)`, where `Psi_U` is the signed reward of a
  full killed excursion away from that boundary.  This aligns the reward
  with the doubleton atoms in the rebate, but the killed-Green coefficient
  cannot be discarded or localized by immediate rank drift.
- Proved this localization failure exactly on the unit Bd star with `L`
  leaves.  The positive reward divided by total normalized edge-doubleton
  mass grows as
  `r^(2L-1)/[(r-1)(r+1)^2 exp(r-1/r)]`.  Hence no constant or
  polynomial-in-order *separate per-rule* coefficient can replace the full
  Green reward.  This does not refute a paired bound: the large-star dB
  excess is nonpositive, so cross-rule compensation remains available.
- Added the exact boundary-trace replay on the named hostile weighted `P4`.
- Universal `(FER)`, `(RHR)`, `(SRR)`, and the minimal stationary product
  remain open.  The exact residual problem is a paired comparison between
  the two full boundary-excursion coefficients and the nonlinear doubleton
  rebate propagated by the base-path Green kernel.

## 2026-08-13 15:13 PDT -- root-Hellinger hostile audit and Green repayment

- Hostile-audited `(RHR)` only on named, previously stored modules.  At the
  numerical algebraic value `R_hyb`, it survives unweighted and `1:17`
  weighted `P3`, two weighted `P4` modules, triangles with weights `(2,3,5)`
  and `(1,1,100)`, and several weighted `K4/C4` witnesses.  The smallest
  observed nontrivial gap was about `0.00235` on the extreme triangle; this
  is evidence only, not a finite-search argument.
- Exactified the portal reduction.  All-portal `(RHR)` is equivalent to the
  diagonal conditions `h_i>=Q_0` and one sharp two-by-two copositivity
  inequality for each root pair.  Recorded all endpoint and interior
  equality cases.
- Derived the exact singleton balance pair
  `rt_i u_Bi=sum_j P_ij(u_Bj+b^B_ij)` and
  `u_Di=sum_j g_r(P_ji)(u_Dj+b^D_ij)`.
- Multiplying those balances and applying Cauchy gives a root-Hellinger
  superharmonic inequality with an explicit positive doubleton rebate.
  In physical coordinates it is `a>=La+beta`, where `L` is an explicit
  cross-rule base-path kernel.
- Proved `rho(L)<1` for every connected module of order at least two and
  `r>1`, hence the exact Green lower bound
  `a>=(I-L)^(-1) beta=sum_m L^m beta`.  This is the first rigorous path/Green
  comparison between the two singleton trace laws and exposes the
  higher-rank term that a first-level proof necessarily misses.
- The remaining universal gap is now exact: compare this doubleton-fed
  Green lower bound with the product of the two full signed excursion
  rewards `Q_0=r^3[bar(phi)_B]_+[bar(phi)_D]_+`.
- Added and passed `verify_singleton_root_schur.py`: direct/two-stage Schur
  associativity, normalization and reward identities, SRR cancellation,
  singleton balances, exact unweighted-`P3` RHR, and two named hostile
  order-four coefficient audits.
- Hostile audit of the separate minimal-product-to-BDM lift found no fatal
  circularity or limit-order flaw.  Its leaf-bundle domination should be
  stated as a finite-state `tau -> 0` continuity/coupling bound, not as an
  exact common-clock identity for unequal core loads.
- Best-guess completion toward the universal minimal-product theorem: 45%.
  The proof target is now a single Green-reward comparison, but its sign is
  not yet established.

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
