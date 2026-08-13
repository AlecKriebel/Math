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
- Reduced the whole seven-arm endpoint-weight family to ten pair orbits and
  solved over `Q(x)`.  Simultaneous weak amplification occurs exactly on the
  nonempty interval `(alpha_B,alpha_D)`, with `alpha_B` the unique positive
  root of an explicit degree-seven polynomial and `alpha_D` an explicit
  quadratic radical.  The rational witness `103/500` is strictly interior.
- Updated the packet-cone target: an unrestricted weak paired cone already
  enters the positive quadrant.  Any useful scale induction must be
  fitness-resolved and show where a positive weak atom loses a coordinate.
- Built the exact `13,728`-orbit full-fitness quotient for the seven-arm
  theta graph.  At fixed `x=103/500`, dB remains positive through roughly
  `r=1.006` and changes sign before `1.0065`; the weak interval therefore
  does not collapse immediately but is narrow.
- Extracted the exact first Taylor coefficients as rational functions of
  `x` and proved, by the analytic implicit-function theorem at the two
  simple weak roots, that the Bd/dB overlap persists for a positive
  finite-fitness wedge.
- Proved an explicit finite-fitness checkpoint at `r=1001/1000`.  Two
  rational Bellman subsolutions on the full quotient have positive exact
  uniform-start gaps for both rules.  Float solves are proposal-only; every
  final inequality is over `QQ`.
- At `R_hyb`, the theta atom has `a+b approximately 0.90086<1`, so the BDM
  Hellinger target is zero and all positive portal laws pass strictly.  This
  is a targeted float diagnostic, not an exact promotion.
- Scope warning: `K_r>=0` remains open and is asserted nowhere.  The exact
  square is a diffuse-adjoint theorem, not a universal finite-graph affine
  separator.
