# Research log: rank-dependent quadratic fitness-two potential

## 2026-08-08 — exact dual and conductance storage

- Derived the exact LP dual.  Its nonnegative weights are state occupation
  pseudoflows conserving, rank by rank, mass and all one- and two-vertex
  marked moments.  The dual objective is the full-boundary flux `z`; proving
  the certificate requires an upper bound on every feasible `z`.
- Derived the complete mass, one-mark, and pair-mark recurrence systems.
- Found the reversible quadratic storage
  `H(S)=pi(S)+sum_({i,j} subset S) pi_i P_ij`.  At fitness two its drift is
  exactly the stationary conductance cut of `S`.
- Obtained the endpoint identity
  `1/n + sum_S y_S cut(S) = 3z/2` and its exact adjacent-rank refinement.
- Identified the same object in the determinant branch as a two-labelled
  request/cache-cut alignment.  No endpoint sign has been inferred from
  this identification.
- Hostile floating quotient searches with four through six equitable
  classes, including multiscale and sparse supports, found no rank-pair LP
  violation.  This remains discovery evidence only.
- Derived an exact row-stochastic tangent decomposition of the complete
  radial optional drift.  Its nonlinear remainder is a positive sum of
  squares; the only linear terms are the column-temperature defect and
  `Z_k=k(k-1)/(n-1)-sum_(i,j in S)P_ij`.  This exactly isolates the
  compressed vertex-plus-one-pair certificate now under study.
- Hostile tests on genuinely directed row-stochastic kernels (arbitrary
  kernels on `n=5,6,7`, 10,000 direct fixation trials at `n=5`, and directed
  three/four-class quotients) also approached the complete value only from
  below.  This is numerical evidence, not an extension theorem.
- Rewrote the optional Farkas system as a signed current on hypercube edges.
  Rank-pair balance transports every degree-two current moment by a factor
  two between adjacent ranks.  Derived the exact top/bottom ratio which is
  necessary and sufficient for the base sign, including the separate
  singleton injection defect.
- Combined the edge current with reversible conductance storage.  The exact
  weighted cut-production identity survives, but positivity of the cut
  terms yields only the reverse (lower) endpoint estimate.  The unresolved
  sign is now sharply an upper bound on this weighted cut production using
  the remaining individual marked-current balances.
- Observed that the geometrically weighted cut is exactly
  `mathcal A(2^(k-N-1) H)`.  This converts the endpoint theorem into a
  boundary-extension problem.  The fixed geometric conductance profile
  leaves precisely the old additive obstruction; the live compressed
  theorem requires an additional zero-boundary conductance profile plus the
  arbitrary rank-labelled vertex corrector.
- Proved that geometric optional reweighting is an exact conjugacy, not only
  a scalar cut identity.  If `eta` is an optional full rank-pair Farkas ray,
  then `mu_S=2^(|S|-n+1) eta_S`, normalized by
  `I=A_(n-1)+2^(2-n)R_1`, is exactly a nonnegative degree-two Green
  pseudoflow with uniform singleton source and fixation flux `A_(n-1)/I`.
  The optional endpoint ratio is algebraically identical to the original
  complete-baseline bound.
- Wrote all one- and two-mark balances as one matrix carré-du-champ identity
  `sum mu [s d^T+d s^T+Diag((1-2s)d)]=z 11^T-I/n`.  Its restriction to the
  zero-sum label space is the fixed negative form `-I/n`; this is the exact
  degree-two collision/variance budget which the determinant/common-pin
  formulation must reproduce.
- Isolated the stationary selection gain
  `Q=L pi(S)=sum_v pi_v x_v(1-x_v)/(1+x_v)` and proved the sharp statewise
  conditional-Jensen inequality
  `Q/C <= (1-M-C)/(1-M+C)+(M-C)/(2M-C)`.  Equality means that the mutant
  posterior is constant separately on the two sides of the cut, and holds
  on every complete-graph rank.
- Reduced the universal endpoint sign exactly to the summed all-rank bound
  `sum mu Q <= kappa_n sum mu C`, where
  `kappa_n=2((n-3)2^n+4)/((3n-7)2^n+8)`.  The local Jensen bound alone is
  insufficient near a vanishing cut, so the remaining issue is genuinely a
  two-marked flow/collision inequality rather than a per-rank cut ceiling.
- Factored `Q` as the quadratic form of the state-dependent PSD matrix
  `K_S=sum_v pi_v (Diag(P_v)-P_v^T P_v)/(1+x_v)`.  The exact reversible
  square
  `2 L_pi-(Pi-P^T Pi P)=(I-P)^T Pi(I-P)` gives
  `K_S <= Pi-P^T Pi P <= 2L_pi`.  For binary state vectors this yields the
  stronger exact collision decomposition
  `2C-Q=sum_v pi_v[(s_v-x_v)^2+x_v^2(1-x_v)/(1+x_v)]`.
  This supplies a graph-independent positive square identity, but its
  factor-two bound is still weaker than the required all-rank constant.
- [EXACT ROUTE REFUTATION] Tested the corrected smallest compressed ansatz:
  arbitrary rank constants, arbitrary rank-labelled vertex fields, and one
  global coefficient of stationary internal conductance in the original
  fixation potential.  The exact 17-vertex `(2,5,10)` additive-witness graph
  refutes it.  Within the 196-state symmetry quotient the function space has
  dimension 50; a 49-state strictly positive rational dual ray and an exact
  matching primal give restricted optimum
  `0.4767015236181397039926...`, strictly above the `K_17` baseline
  `524288/1114095` by an exact 719/721-digit rational.  Every labelled to
  quotient row and every primal inequality is replayed independently.
- Consequently a single fixed conductance contraction of the matrix budget
  cannot prove the endpoint theorem.  The full rank-pair system, or at least
  a genuinely rank-dependent conductance profile, remains the live route.

### Active sign

For every feasible two-moment pseudoflow, prove

`sum_S y_S cut_pi(S) <= (3/2) rho_dB(K_n,2) - 1/n`.

The next analytic attempt is to combine the rank-cut recurrence with the
arbitrary one-mark recurrence using a rank-dependent solution of a
reversible Poisson equation.  The smaller space containing only rank
constants, stationary mass, and internal conductance is exactly unsuitable
as a universal route according to direct LP counterexamples, so the full
vertex corrector must be retained.
