# Research log: weighted `P_3` BDM at `R_hyb`

## 2026-08-13 -- exact arbitrary-portal theorem

- Normalized every positively weighted path to edge weights `(1,t)` and used
  reflection to reduce to `0<t<=1`.
- Rebuilt the two labelled six-state fixation chains and their reciprocal
  fitness versions.  This produced exact mean ranks and all six singleton
  atoms of the Bd and dB OR duals.
- Found a portal-extremal inequality: the degree-coupled product
  `q_B q_D` is always at least the singleton product at the leaf incident to
  the heavier edge.  The corresponding copositivity matrix is in fact
  entrywise nonnegative.  Three nontrivial entries have positive degree-four
  Bernstein coefficients for every `r>=3/2`; the other two have direct
  one-line signs.
- Reduced BDM to a scalar inequality in `(r,t)`.  At `R_hyb`, the small-edge
  regime has `K_0(a+b-1)<1`; the remaining regime satisfies the stronger
  rationalized Hellinger bound
  `4k_0(1-a)(1-b)>r(r-1)^2(a+b-1)^2`.
- Certified both signs exactly and uniformly over the rational isolating
  interval of `R_hyb` by tensor-Bernstein coefficients.  The fixed
  subdivision has one small rectangle and seven remaining `t` intervals.
  No graph enumeration or numerical sign decision is used.
- **PROVED:** every positively weighted `P_3`, with every nonzero
  nonnegative portal vector, satisfies strict BDM at `R_hyb` and hence
  `D+(R_hyb-1)B<0` at every positive gate scale.
- **OPEN:** universal BDM for bounded modules of order at least four.
