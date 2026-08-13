# Research log: regular minimal product at `R_hyb`

All times are America/Los_Angeles.  No external communication or broad graph
search was used.

## 2026-08-13 -- exact reduction and first-level obstruction

- Proved that on a regular module the Bd dual law is
  `pi_B(A)=(r-1)^|A|/(r^s-1)`, hence its singleton atom is
  `u=(r-1)/(r^s-1)` and `rho_B-p=u/r`.
- Since regularity makes the two physical portal laws identical, MP for all
  portals is exactly the vertexwise dB inequality
  `pi_D({i}) >= r^2[rho_D-p]_+`.
- Rewrote the target using the exact dB hole identity as singleton entrance
  versus the deterministic one-hole deficit plus stationary two-hole
  collision budget.
- Retained the exact singleton/doubleton entrance balance.  It is symmetric
  on regular kernels but does not control ranks at least three.
- Exactified that logical obstruction: scaling all genuine complete-kernel
  singleton/doubleton atoms by `epsilon` and putting the residual mass on a
  rank-three state preserves every singleton equation while violating the
  vertexwise target for small `epsilon` on order eight throughout the
  isolating interval containing `R_hyb`.
- Conclusion: the universal regular target remains open; a proof must use a
  rank-two/rank-three return equation or an equivalent full Green/tree
  identity.  No broad graph or coefficient search was performed.

## 2026-08-13 -- finite-depth return and root-loss obstruction

- Used the one-step support fact that the dB dual can lower rank by at most
  one.  Scaling a genuine law on every rank at most `m+1` and putting the
  residual mass at rank `m+2` preserves every coordinate stationarity
  equation through rank `m`.
- For `m=2`, this preserves the full doubleton equation and its scaled
  triple-to-doubleton entrance current.  On order eight the limiting
  pseudo-density is `1/2>p(R_hyb)` while every singleton atom vanishes, so
  the rank-two/rank-three row alone cannot prove VDR.
- The same construction at order `2(m+2)` refutes every fixed finite-rank
  closure as a universal proof route.  It is not a graph counterexample;
  the first omitted rank equation fails.
- Wrote the honest stopped-chain identity rootwise as
  `v_i=sum_C eta(C)G^-(C,{i})`.  Its scalar rank shadow retains only the sum
  over `i`.
- Exactified failure of the canonical root-average bridge on one connected
  regular six-vertex equitable kernel with class sizes two and four.  A
  symbolic 13-state orbit solve proves the two singleton classes differ for
  every `r>1`.
- Conclusion: a surviving proof must use a full high-excursion Green/tree
  invariant and keep the named root.  No such invariant emerged, so the
  rank-prefix route was stopped without graph enumeration.
