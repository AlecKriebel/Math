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
- Contracted the exact degree-two matrix balance with the two fixed
  reversible PSD matrices.  The `L_pi` contraction is identically
  `L cut=3Q-2 cut`, hence is only a linear combination of the already known
  mass/storage boundary laws.  The `K_0=Pi-P^T Pi P` contraction has source
  `1-chi`, where `chi=sum_(v,i) pi_v P_vi^2 >=1/(n-1)`, but its two-step
  response `J_2` changes sign even on the exact four-cycle.  Therefore no
  sign follows from either fixed contraction alone.
- Derived the exact arbitrary-rank multiplier formula for `s^T K s` and
  its rank-current recurrence.  PSD controls only the diagonal
  carre-du-champ for a constant multiplier; rank variation introduces
  signed adjacent-rank mixed currents which must be coupled to the
  one-mark balances.  This is the minimal unresolved term in the matrix
  contraction route.
- Wrote the exact compressed dual for rank constants, arbitrary
  rank-labelled vertices, and one conductance coefficient per rank.  It is
  precisely nonnegative pseudoflow plus the rank-mass equations, all
  one-mark equations, and one `H`-storage recurrence per rank.
- [EXACT FINITE REPAIR] On the same 17-vertex graph which refutes one global
  conductance coefficient, the rank-dependent conductance space has exact
  dimension 63.  A 62-state strictly positive rational dual and matching
  rational primal give optimum
  `0.463075851135221216402749...`, below the `K_17` baseline by
  `0.00751956487508311132513730...`; all 196 quotient drifts are exact.
- [EXACT FINITE REPAIR] Replacing rank-dependent conductance by the
  rank-dependent two-request covariance `s^T K_0 s` also repairs the same
  witness.  Its exact optimum is `0.439476931794796785748626...`, below
  baseline by `0.0311184842155075419792610...`.
- The naive scalar use of `Q<=s^T K_0s` cannot prove the sharp constant:
  on the exact four-vertex verifier graph the integrated ratio
  `(sum mu s^T K_0s)/(sum mu cut)` is
  `3763047422347/5888649661090 > kappa_4=5/11`.  The live `K_0` route must
  retain rank transport and the positive remainder
  `sum pi x^2(1-x)/(1+x)`.
- Split the `L_pi` response into the two oriented selection currents
  `Q_k^+` and `Q_k^-`.  The exact addition/removal responses are respectively
  `(C+Q^+,Q^--C)` for stationary mass and
  `(3Q^+-C,3Q^--C)` for the conductance cut.  This gives a closed pair of
  rank-current recurrences before the fixed contraction collapses them to
  `L C=3Q-2C`.
- [EXACT POSITIVE REFORMULATION] Combining rank-`H` and rank-`K_0`, set
  `D=2C-R0=sum pi(s-x)^2` and
  `W=sum pi x^2(1-x)/(1+x)`.  Then `2C-Q=D+W` pointwise, so the sharp theorem
  is exactly the integrated coercivity
  `(2-kappa_n) sum mu C <= sum mu(D+W)`.  The combined certificate tracks
  `C` and `D` on every rank; `W` is an additional nonnegative fitness-two
  remainder.  This is the cleanest surviving positive target.
- The scalar cone obtained by retaining only the oriented total currents
  and the bounds `0<=Q^+<=C`, `0<=Q^-<=C/2` is insufficient; individual
  rank-labelled vertex recurrences remain essential.  Any M-matrix or
  continued-fraction proof must therefore be vertex marked rather than a
  one-dimensional rank argument.
- [EXACT RELAXATION REFUTATION] Added every natural scalar event-moment bound
  (`X^C<=X^M,A-X^M`, and the analogous down-current inequalities) and the
  exact singleton/top identities.  At `n=3` this enlarged scalar system
  still has a rational point with flux `z=5/9`, above the complete baseline
  `4/9`.  The exact verifier explicitly warns that this is not a graph or
  pseudoflow; it isolates the loss caused by forgetting the individual
  vertex currents.
- Found the simplest rank-`H` storage form: internal conductance `E=H-M`
  obeys `LE=C-Q`.  Oriented additions create
  `P=C-Q^+=sum_out 2 pi x^2/(1+x)>=0`, while removals destroy
  `N=Q^-`.  Its rank recurrence has zero singleton source and top boundary
  `z/2`, so `sum(P-N)=z/2`.  The sharp theorem is exactly
  `(1-kappa_n)sum mu C <= sum(P-N)`.  This isolates the missing statement as
  transport of vertex-marked destruction debt across an entire excursion,
  not a pointwise or prefix inequality.

### Active sign

For every feasible two-moment pseudoflow, prove

`sum_S y_S cut_pi(S) <= (3/2) rho_dB(K_n,2) - 1/n`.

The next analytic attempt is to combine the rank-cut recurrence with the
arbitrary one-mark recurrence using a rank-dependent solution of a
reversible Poisson equation.  The smaller space containing only rank
constants, stationary mass, and internal conductance is exactly unsuitable
as a universal route according to direct LP counterexamples, so the full
vertex corrector must be retained.

The sharpest surviving compressed conjecture is now the exact implication
from rank mass + every rank one-mark balance + the rank-`H` recurrence to
`z<=rho_dB(K_n,2)`.  A parallel augmentation uses the rank-`K_0` recurrence.
Neither fixed-matrix PSD nor `Q<=s^T K_0s` closes the sign; the unresolved
object is the signed adjacent-rank mixed current after one-mark elimination.
