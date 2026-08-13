# Research log: `R_hyb` compactness reduction

- Separated the minimal one-module gate theorem from its convex closure.
  Direct solution of the two gate inequalities gives exactly
  `q_B q_D >= r^3 [rho_Bd-p]_+ [rho_dB-p]_+`, the portal-general form of
  the old stationary singleton-product inequality (65).  This is strictly
  weaker than BDM.  Nevertheless BDM is necessary for the separated
  response cone: any strict positive `D+(r-1)B` score can be mixed with
  either the ordinary leaf ray or the tangent strong-`K_2` ray to enter the
  open positive quadrant.  Exact symbolic replay verifies both reductions.

All times are America/Los_Angeles.  No external communication or graph
optimization was used.

## 2026-08-13 -- exact bounded dual-moment frontier

- Corrected the endpoint sequence criterion: `liminf min(X,Y)<=1` does not
  exclude strict dilute gains approaching zero.  A matching upper theorem
  must forbid eventual membership in the open positive quadrant and retain
  the actual first nonzero response scale.
- Proved that exceptional `o(n)` vertex sets cannot simply be deleted from
  the dynamics.  Their initializations are negligible only at scale
  `|E|/(n epsilon)=o(1)`; their dynamical effect must remain in the exact
  Schur trace.
- Formulated precise bulk/dilute response-scale compactness alternatives and
  identified the two missing uniformities: trace error relative to the
  actual gain, and tightness of growing-module trace data.
- Rewrote every invariant of a bounded separated module using the two exact
  stationary OR-dual laws: mean ranks `m_B,m_D` and portal-weighted singleton
  atoms `q_B,q_D`.
- Reduced the universal module separator to the sharp inequality

  ```text
  q_B q_D >= r(r-1)^2
      [sqrt(a b)-sqrt((1-a)(1-b))]_+^2,
  a=rho_dB/(r-1), b=rho_Bd,
  ```

  together with `a<=1`.
- Derived the exact degree-coupled portal formulation as copositivity of a
  rank-four symmetric matrix.  Pointwise singleton products are necessary
  but do not by themselves control mixed portals.
- Derived the exact singleton-state stationarity balances for both duals and
  an exact three-copy product-chain LP certificate formulation.  The missing
  step is a cross-rule stationary inequality; marginal profiling alone does
  not close it.
- Proved first-level balance is decisively insufficient: scale every
  rank-one/rank-two mass by `lambda` and put the residual probability on
  rank three.  On eight vertices the limiting means satisfy `a<1<a+b`, while
  `q_B q_D=O(lambda^2)`, violating the Hellinger bound.  This is a pseudo-law
  obstruction to the relaxed proof space, not a graph counterexample; it
  proves that higher-rank stationary flow is unavoidable.
- Isolated `a<=1` as the separate density theorem
  `rho_dB(H,R_hyb)<=R_hyb-1`.  The open complementary-level conjecture would
  imply the stronger half-density bound, whereas first-level balance cannot.
- Verified that `K_2` has discriminant exactly `r^2 P(r)`, so equality at
  `R_hyb` is precisely the known hybrid tangency.
- Proved BDM for every complete module `K_s` and arbitrary portal loads.  A
  closed all-order estimate gives `a_s+b_s<1` for `s>=7`; exact Sturm signs
  discharge the forced boundary orders `3<=s<=6`.  The separator is strict
  for every `s>=3`, while `K_2` has the unique double-root equality at the
  hybrid gate scale.
- Best-guess completion of the exact-threshold program: **73%**.  The local
  matching-upper question is now one exact stationary inequality, while the
  global trace compactness and positive-density bulk alternatives remain
  open.
