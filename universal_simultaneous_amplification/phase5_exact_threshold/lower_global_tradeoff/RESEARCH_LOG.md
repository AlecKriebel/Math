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
- Proved the exact pair-chain Schur decomposition for an arbitrary module
  partition and either update rule.  It splits each weak coefficient into a
  killed local occupation plus a nonnegative effective boundary load on the
  trace pair chain.  The local blocks are exactly module-diagonal.
- Derived the sharp uniformity parameter for module collapse:
  `escape scale x killed Green norm`.  If it does not vanish, the module is
  metastable and must be promoted to the next trace scale.
- Exact replay on the frozen five-path shows that its dB local occupation is
  zero while its entire dB coefficient, including the positive weak excess,
  is carried by the boundary trace.  This proves portal coupling is
  essential in any atomic compactness theorem.
- Exactified the 23-vertex, seven-arm theta graph with endpoint weights
  `103/500`.  Direct rational pair-chain solves prove both weak excesses are
  positive.  This is an exact finite strict simultaneous weak amplifier and
  settles the formerly open finite weak-selection question.
- Refuted the natural reversible-power midpoint inequality
  `N(1)+N(-1)<=2N(0)=2n` exactly on the same graph.  The common symmetrized
  pair hopping and common boundary vector are insufficient because the
  diagonal holding rates and pair source co-vary with the power parameter.
- Updated the packet-cone target: an unrestricted weak paired cone already
  enters the positive quadrant.  Any useful scale induction must be
  fitness-resolved and show where a positive weak atom loses a coordinate.
- Scope warning: `K_r>=0` remains open and is asserted nowhere.  The exact
  square is a diffuse-adjoint theorem, not a universal finite-graph affine
  separator.
