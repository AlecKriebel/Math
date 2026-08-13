# Research log: fitness-dependent global tradeoff

## 2026-08-13

- Created this dedicated folder after the exact five-ground endpoint-orbit
  reduction was frozen in `lower_global_diagonal`.
- Derived the arbitrary-fitness endpoint deficits `B_r,D_r`, the
  cross-energy formula, and the exact support square (1) in
  `R_DEPENDENT_DIFFUSE_SUPPORT_IDENTITY.md`.
- Checked that the identity specializes exactly to the `r=2`
  ground-energy decomposition and factorizes positively on the
  deterministic two-cycle.
- Matched the diffuse support to the leaf-annihilating pair score and the
  known square-minus-sextic completion defining `R_hyb`.
- Derived the complete three-moment form of a fitness-integrated pair
  charge.  A nonzero nonnegative weight below `R_hyb` cannot be tangent to
  the known equality pair: `F_r(sigma_*)<0` at every interior fitness.
  Thus cancellation requires a signed weight, a nonlinear coordinate-wise
  penalty, or a boundary/derivative observable.
- Derived the exact neutral Lyapunov--Schmidt coefficients.  In particular,
  the diffuse dB weak-gain derivative is
  `1/E_pi(1/a)-1<=0`, strictly negative off the isothermal mode, and
  `T_r/(r-1)->1-1/E_pi(1/a)`.  This proves that a non-isothermal diffuse
  branch cannot supply the near-neutral part of a simultaneous amplifier.
- Made the neutral expansion rigorous by analytic Lyapunov--Schmidt
  reduction.  The `O((r-1)^2)` remainder is uniform for a fixed finite type
  law, and uniformly so on compact fixed-dimensional families with
  nondegenerate temperatures and Perron gaps.  Degenerating gaps/type laws
  are explicitly excluded and identify the possible boundary-layer route.
- Refuted the stronger scalar atomic hypothesis using the frozen exact
  five-path `5,1,1,5`, whose dB weak coefficient exceeds the complete value
  by `1/9310`.  Any scale induction must retain paired Bd/dB atom vectors
  and their coupled portal trace, not a dB sign alone.
- Scope warning: `K_r>=0` remains open and is asserted nowhere.  The exact
  square is a diffuse-adjoint theorem, not a universal finite-graph affine
  separator.
