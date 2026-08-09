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
- [EXACT ROUTE REFUTATION] The full rank-dependent conductance space is now
  refuted, not merely its global-coefficient subspace.  A connected
  complete-support nine-vertex integer-weight graph with equitable class
  sizes `(1,1,2,2,3)` has a 142-state quotient and a 47-dimensional
  rank-constant + rank-vertex + rank-conductance potential space.  An exact
  46-state strictly positive rational Farkas ray and independently
  reconstructed matching rational primal give restricted optimum
  `0.4463122484779187239833287...`, above the `K_9` baseline `1024/2295` by
  the exact positive rational identified by SHA-256
  `54157ebc0d0153a2d86dc928f47495f688d2104b3971ff5cf0127e838ccb9f76`.
  Every quotient drift and its labelled realization are checked exactly.
- This refutation concerns only the certificate space; preliminary true-chain
  computation is suppressing and is not used as an exact claim.  Rank-`H`
  alone is closed as a proof route.  The live compressed route must combine
  rank-dependent `H` and `K_0`, equivalently two independent reversible
  quadratic directions per rank, with the full pair matrix as fallback.
- [EXACT TWO-CHANNEL REDUCTION] Used the arbitrary vertex fields to gauge
  away quadratic diagonals.  The `L_pi` pair direction is then `-2E_1`,
  where `E_1` is internal target--request conductance, and the `K_0` pair
  direction is `-2E_2`, where `E_2` is internal conductance for two
  independent requests from a common stationary target.  Their upward-edge
  increments are exactly `pi_v(Ps)_v` and `pi_v(P^2s)_v`.
- Wrote the combined restricted primal/dual without redundancy.  Its slice
  space is exactly `span{1,s_i,E_1,E_2}`; its dual consists exactly of
  nonnegative pseudoflow plus rank mass, every one-mark balance, and the two
  storage recurrences.  The surviving universal implication is therefore a
  concrete finite system, not an informal PSD heuristic.
- Split both channels into nonnegative creation/debt currents and derived the
  exact two-component rank recurrence, including top boundary
  `z(1,1-chi)/2`.  The all-rank totals give the sharp universal collision
  deficit
  `sum(P_2-N_2) <= (n-2)/(n-1) sum(P_1-N_1)`, whose exact slack is
  `z/2 sum_v pi_v sum_(i!=v)(P_vi-1/(n-1))^2`.  Equality is exactly the
  complete kernel.  This is new graph-independent information but does not
  alone control the first-channel debt rankwise.
- Factored `K(theta)=L_pi+theta K_0` spectrally.  It is a graph Laplacian
  with effective conductances `c+theta q` for `theta>=0`, and is PSD for
  every reversible kernel for the sharp universal range `theta>=-1/2`.
  The corresponding rank-profile identity is the canonical two-channel
  M-matrix/Schur starting point; the remaining sign is precisely a rankwise
  second-channel transport bound coupled to all one-marks.
- [EXACT MINIMAL SCHUR MODE] Split off the complete-aligned collision
  channel by setting `E_perp=E_2-(1-chi)E_1` and
  `K_perp=K_0-(1-chi)L_pi`.  This storage vanishes at empty, every singleton,
  and full; `K_perp` has row sums and trace zero, so whenever nonzero it is
  necessarily indefinite.  Its rank recurrence has no source at either
  endpoint and zero total drift.  Therefore the new combined information is
  exactly a signed redistribution between ranks, not a positive fixed-matrix
  budget.
- With `R=Diag((P^2)_(vv))` and
  `B=P^2-R-(I-R)P`, proved `B1=0` and the local forcing formula
  `L E_perp=sum_v pi_v d_v[(chi-r_v)x_v+(Bs)_v]`.  This vanishes pointwise
  on the complete kernel but has no general local sign.  The remaining
  obligation is now minimal: couple this zero-boundary rank Schur mode to
  every one-mark balance strongly enough to control first-channel
  destruction debt.
- Factored the neutral mode further as
  `K_perp=L_pi(P+chi I)`.  Its reversible spectral multiplier is
  `(1-lambda)(lambda+chi)`, with the exact difference-of-squares form
  `(1+chi)^2 ||f||_pi^2/4-||(P-(1-chi)I/2)f||_pi^2` and sharp cone
  `-(1-chi)L_pi <= K_perp <= (1+chi)L_pi`.  Complete-graph nonconstant
  modes sit exactly at the sign-change `lambda=-chi`.  This proves that the
  required gain cannot come from a fixed PSD comparison; it must use
  rank-dependent transport across the positive and negative spectral parts.

### Active sign

For every feasible two-moment pseudoflow, prove

`sum_S y_S cut_pi(S) <= (3/2) rho_dB(K_n,2) - 1/n`.

The live route is now the full rank-pair matrix balance `(68)`.  The
rank-`H,K_0` Schur pencil and each of its one-channel restrictions have all
been exactly refuted as universal certificate spaces.  Any smaller new
candidate must add at least one genuinely independent pair direction and
must be hostile-tested before analytic investment.

- [EXACT ROUTE REFUTATION] Rank-dependent `K_0` plus all rank-labelled
  one-marks is now also exactly refuted.  A complete-support nine-vertex
  equitable graph with class sizes `(1,1,2,2,3)` has a 142-state quotient
  and a 47-dimensional rank-constant + rank-vertex + rank-`K_0` potential
  space.  An exact 46-state strictly positive rational Farkas dual and
  independently reconstructed matching primal give restricted optimum
  `0.4539329228798728451964329...`, above the `K_9` baseline `1024/2295` by
  `0.007745559045450187244363190...`.  The exact gap is identified by
  SHA-256
  `49230606abeb30eafdf1dbe7bfd96b7e35f80bdff7eb7b15efbd759706c4534c`.
  All 142 quotient drifts agree exactly with a separately labelled chain.
- This refutes only the `K_0`-only certificate, not the fixation theorem.
  Together with the earlier exact rank-`H` refutation, it identified the
  two-channel rank-`H,K_0` space as the next candidate; that candidate is
  refuted below.
- [EXACT COMBINED-ROUTE REFUTATION] The full two-channel compressed space
  with rank constants, every rank-labelled one-mark, and independent
  rank-`H` and rank-`K_0` coefficients on every rank is exactly refuted.  A
  complete-support twelve-vertex graph with class sizes `(1,1,2,3,5)` has
  a 286-state quotient and 74-dimensional `W_12` space.  A 73-state
  strictly positive rational Farkas dual and independently reconstructed
  matching primal give restricted optimum
  `0.4600442069423893447745517...`, above the `K_12` baseline `2816/6141`
  by the exact positive rational
  `0.001486968707574168093229390...`, SHA-256
  `0cc5256b94a446ce0a8d2f8174e8cc081f5c3a0b25ea683d977808f044f94a22`.
  All 286 quotient rows match a separately labelled chain.
- [EXACT NON-CONFLATION] An independent exact harmonic solve gives true
  fixation `0.4215620895939539989012090...`, strictly below the complete
  baseline by `0.03699514864086117778011324...` (exact-margin SHA-256
  `15fdf227d4184ee288596e3d92f7ea65be17c0e0e87b9d60a01ecd1d8d190ae1`).
  Thus this is solely a proof-space counterexample.
- The full rank-pair matrix is now the smallest live quadratic certificate.
  The next task is to contract the complete matrix balance without reducing
  it to the refuted `H,K_0` span, and to hostile-test the full pair LP on
  this exact witness.
- [EXACT THIRD PAIR DIRECTION] Contracting the full matrix balance with
  `pi pi^T` adds stationary mutant mass squared `M^2`.  If
  `V=M(1-M)` and `D=2C-R0`, the covariance matrix of the stationary target
  indicator and its request probability is
  `[[V,V-C],[V-C,V-R0]]>=0`; hence the sharp statewise square
  `C^2<=VD`.  Equality holds exactly when `x` is constant on each side of
  the cut, including every complete-graph rank.
- The exact current law is
  `L M^2=2MQ+sum_v pi_v^2 t_v`.  Resolving additions/removals gives
  nonnegative third-channel creation/debt and a rank recurrence with source
  `||pi||_2^2/n`, sink `z`, and total net
  `z-||pi||_2^2/n`.  The exact verifier checks the PSD determinant, equality
  class, generator identity, every rank equation, and the total boundary
  law.
- [NUMERICAL ONLY] Adding rank-dependent `M^2` to `W_12` repairs the exact
  twelve-vertex refuter with margin about `0.02988`; initial 728-evaluation
  five-class and 540-evaluation six-class multiscale hostile cycles found no
  failure.  The live intermediate conjecture is `W_123`; the next analytic
  target is a `2 by 2` rank Schur/Riccati bound using `C^2<=M(1-M)D`.
- [HOSTILE SCREEN, NUMERICAL ONLY] `W_123` also closes every stored exact
  refuter: the rank-`H` and rank-`K_0` nine-vertex graphs, the combined
  twelve-vertex graph, and the original seventeen-vertex additive witness.
  New optimized multiscale cycles found no violation: 567 seven-class
  evaluations on sizes `(1,1,1,1,2,3,5)` with best gap `-0.0486952`, 504
  five-class evaluations on `(1,2,3,5,8)` with best gap `-0.0185538`, and
  360 six-class evaluations on `(1,1,2,3,4,6)` with best gap `-0.0574056`.
  The weight ratios spanned up to about `exp(40)`.  These screens do not
  establish universal feasibility.
- [EXACT RANK SCHUR REDUCTION] Summing the target/request covariance matrix
  on each rank gives `C_k^2<=V_k D_k`, equivalently the full tangent family
  `D_k-2 theta_k C_k+theta_k^2 V_k>=0`.  Subtracting the `M^2` recurrence
  from the rank-labelled `M` recurrence gives the boundary-zero variance
  transport for `V=M(1-M)`, with signed adjacent-rank responses
  `B^+=P^M-P^3` and `B^-=N^3-N^M`.  The verifier checks the state generator,
  every endpoint, every rank recurrence, and nonconstant exact tangents.
- [EXACT STATIC-SCHUR REFUTATION] The strongest contraction which discards
  that signed transport and optimizes every rank tangent independently is
  insufficient on the exact twelve-vertex graph.  Its exact Green residual
  is `-0.2524901456099282956184879...`, SHA-256
  `56d33de896c8e6c7d23dfb1712acbbb972647529cbbcec94d12cd5c61832a2e9`,
  while the true target residual is the exact positive rational
  `0.002549972027336616301296108...`, SHA-256
  `e9921c44de22a2f1d274edfe7e95672a803a3e32541b9f1aa5a260a9fe2f2782`.
  This refutes only the static PSD tangent route, not `W_123`; any proof of
  the latter must use the signed variance-current recurrence essentially.
- [EXACT PURE-PAIR GAUGE] Using the available one-mark
  `J=sum_i pi_i^2 s_i`, replaced `M^2` by the equivalent internal pair flow
  `E_3=(M^2-J)/2=sum_(i<j)pi_i pi_j s_i s_j`.  Its addition and removal
  increments are `pi_v M` and `pi_v(M-pi_v)`, so both creation and debt are
  nonnegative.  The exact rank recurrence has zero singleton source, top
  sink `z(1-||pi||_2^2)/2`, and total net equal to that sink.
- This third channel supplies a second sharp total deficit:
  `sum(P_3-N_3)<=(n-1)/n sum(P_1-N_1)`, with exact gap
  `z(||pi||_2^2-1/n)/2`.  Together with the row-collision deficit of channel
  two, equality forces both uniform stationary mass and uniform loopless
  rows, hence the complete kernel.
- [EXACT OPERATOR SQUARE] With `L_3=Pi-pi pi^T`,
  `D_0=2L_pi-K_0`, and `B=I-1 pi^T`, proved for every real `theta`
  `D_0-2 theta L_pi+theta^2 L_3=((I-P)-theta B)^T Pi
  ((I-P)-theta B)>=0`.  Its binary specialization is the rank covariance
  tangent.  Matrix equality plus looplessness uniquely forces
  `pi=1/n`, `theta=n/(n-1)`, and `P_ij=1/(n-1)`.  Thus `W_123` is exactly a
  three-channel nonnegative-flow/Schur system with the right equality class;
  the remaining gap is dynamic rank transport, not identification of a
  positive square.
- [EXACT MIXED-CURRENT CONE] At the complete slope `theta=n/(n-1)`, wrote
  the first/third creation and debt discrepancies as oriented averages of
  the same Schur error `e_v=s_v-x_v-theta(s_v-M)`.  Weighted
  Cauchy--Schwarz gives exact statewise and rankwise second-order-cone
  bounds.  The removal identity has one correction
  `sum_in ell_v pi_v(pi_v-1/n)`, which is retained exactly by the
  rank-labelled one-mark with coefficients `pi_v(pi_v-1/n)`.  The verifier
  checks both oriented identities and both rank-aggregated squares over the
  rationals.  This is the smallest current-level Riccati cone found so far;
  an explicit rank profile coupling its two orientations is still open.
