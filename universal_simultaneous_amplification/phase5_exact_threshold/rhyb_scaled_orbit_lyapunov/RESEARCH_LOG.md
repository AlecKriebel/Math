# Research log: scaled-orbit Lyapunov audit

## 2026-08-13 — exact theorem and two-cycle obstruction

- Derived a universal relative-coordinate representation of the dB map.
  The fixed-point Doob transform turns one update into Markov averaging of
  `y/s`, followed coordinatewise by a motion along the segment toward one.
- Consequently every convex function minimized at one gives a
  nonincreasing average under the reversible Doob measure
  `nu_i=m_i s_i^2/[r(1-s_i)]`.  This is an exact nonlinear Lyapunov family
  for all `r>1`.
- The Lyapunov is unsigned and uses a different measure from the signed
  target `E_p(y-s)`.  It therefore does not settle endpoint-versus-first.
- Derived the exact orbit identity

  ```text
  E_p(y-F_r(y))
    = (1/r) E_p[F_r(y){rF_r(y)-(r-1)}/(1-F_r(y))].
  ```

  Its convex integrand changes sign, so it is not an iterative sign
  certificate.
- Without searching kernels, analyzed the deterministic reversible
  two-cycle at arbitrary mass ratio.  For every imbalance and every
  `3/2 <= r <= 151/100`, the scaled Bd-started orbit has
  `E_p y_2 > E_p y_1`.  Thus raw-average monotonicity already fails on the
  first post-certificate step throughout the `R_hyb` band.
- On the same entire class, proved the desired strict comparison
  `E_p y_1 > E_p s` (indeed for every `r>=3/2`).  The two-cycle is a route
  obstruction, not a counterexample to the endpoint conjecture.
- Best-guess completion: **100% for the requested Lyapunov/two-cycle audit;
  roughly 55% for the diffuse-support branch.**  The general signed endpoint
  gap remains open and no further orbit exploration is warranted without a
  new mechanism retaining the coupled endpoint grounds.
