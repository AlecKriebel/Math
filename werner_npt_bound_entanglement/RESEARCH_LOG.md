# Research log

All timestamps use America/Los_Angeles.

## 2026-07-28

- Initialized the program in a dedicated folder.
- Adopted two independent layers: exploratory computation under `discovery/`
  and exact proof/certificate checking under `verification/`.
- Repository coordination note: the primary checkout was on another branch,
  while `main` was already checked out at `/Users/alec/Documents/Math-kissing5`.
  Work is therefore being conducted in this dedicated folder in that existing
  `main` worktree, leaving all unrelated untracked files untouched.
- First checkpoint targets:
  1. derive the exact coefficient-matrix contraction formula;
  2. prove the sharp one-copy endpoint bound;
  3. search independently for a tensorization invariant and for exact
     finite-copy witnesses.
- Derived and proved the exact formula
  \[
  Q_{\alpha,d,n}(C)=\sum_{S\subseteq[n]}\alpha^{|S|}
  \|\operatorname{Tr}_S C\|_F^2.
  \]
  In particular, at the endpoint all explicit factors of \(d\) cancel.
- Proved the sharp one-copy inequality
  \(|\operatorname{Tr}C|^2\le2\|C\|_F^2\) for rank-at-most-two \(C\), including
  its equality classification.
- Re-expressed cross terms between rank-one coefficient matrices as matrix
  elements of the positive kernel
  \(R_{d,n}=(I-\tfrac12F)^{\otimes n}\).
- Proved a useful exact obstruction: no two-term witness can work when all
  four Schmidt-side vectors factor copy by copy.  A genuine witness, if one
  exists, must use cross-copy entanglement inside at least one Schmidt-side
  vector.
- Proved all-copy parameter monotonicity: if the endpoint
  \(\alpha=-\tfrac12\) is two-block-positive for every tensor power at a
  fixed \(d\), then every \(\alpha\in[-\tfrac12,0]\) is as well.  The proof
  expands toward the identity and uses that every coefficient submatrix of a
  rank-two matrix still has rank at most two.
- Isolated the sharp quantitative all-copy conjecture
  \(Q_n(C)\ge2^{-n}(s_1-s_2)^2\), proved its sharpness at every \(n\), and
  reduced it to a coupled crossed-kernel inequality.  This remains unproved.
- Independently checked an exact reduction of the full \(d=3,n=2\) problem
  to a Ky--Fan two-singular-value inequality for
  \(D=I\otimes A+B\otimes I+zI/\sqrt6\), with traceless \(3\times3\)
  matrices \(A,B\).  The resulting finite inequality remains unproved.
- Discovery-only projected-gradient searches at \(d=3,n=2,3\) reached zero
  to floating-point precision but found no reliable negative value.
- Verified two further exact boundary facts:
  1. diagonal rank-two matrices built from strings at odd Hamming distance
     have exactly zero endpoint expectation for every \(n\);
  2. every normal rank-at-most-two coefficient matrix is nonnegative for
     two copies.
- Localized the sign in an auxiliary-qubit replica formula: all physical
  factors form a positive kernel, while the sole negative auxiliary sector
  is the one-dimensional antisymmetric subspace.  This is an exact
  reformulation, not yet a closing inequality.
- Proved that any \(d=3\) endpoint witness embeds unchanged in every
  \(d\ge3\).
- Proved a tensor-stable local-support theorem: if, at every copy, at least
  one side of the vector is supported on a subspace of dimension at most
  two, the local compression of \(X_{\alpha,d}\) is positive and so is the
  tensor product.  Hence a \(d=3\) witness needs a common site where both
  Schmidt-side planes have full local support.
- Classified equality in the local-support theorem and proved two-copy
  nonnegativity for every coefficient matrix that is phase-equivalent to a
  positive semidefinite rank-two matrix.
- Validated the exact local-compression checker independently
  (\(2^nQ=31262\) by both contractions); all accompanying C++ discovery
  sources pass syntax-only compilation.
- Proved an exact copy-doubling reduction: any negative rank-two witness at
  \(n\) copies produces an equal-singular-value witness at \(2n\) copies by
  antisymmetrizing its two SVD terms.  The doubled expectation is
  \(2\det H<0\).  Therefore all-copy positivity is equivalent to positivity
  on rank-two partial isometries at every copy number.
- Exactly disproved a tempting stronger compression inequality at \(n=2\):
  for explicit two-planes \(U,V\), the compression of
  \(R_2=(I-\tfrac12F)^{\otimes2}\) has trace \(11/4\) and top eigenvalue
  \((7+\sqrt{17})/8>11/8\).
- Isolated the correct weaker compression target.  Only maximally entangled
  vectors between the two code planes must be controlled:
  \(2\omega_{\rm ME}(K)\le\operatorname{Tr}K\).  In Pauli coordinates this
  is the exact \(3\times3\) inequality
  \(s_1(M)+s_2(M)-\operatorname{sgn}(\det M)s_3(M)\le\operatorname{Tr}K\).
  The explicit counterexample to the operator-norm strengthening saturates,
  rather than violates, this live inequality.
- Derived an adjoint-mixed copy-doubling construction.  A tempting block
  swap makes the resulting coefficient matrix normal, but it also changes
  the \(A_i:B_i\) copy pairing; an exact example reverses the expectation
  from \(-2\) to \(+2\).  Thus negativity cannot be transferred to the
  normal subclass by that relabeling.
- Proved the sharp two-copy quantitative identity for every
  \(H\succeq0\):
  \[
  Q_2(H)-\tfrac12\bigl(\operatorname{Tr}H^2
  -\tfrac12(\operatorname{Tr}H)^2\bigr)
  =2\operatorname{Tr}[(H\otimes H)\Pi_1^-\Pi_2^-]\ge0.
  \]
  For positive rank two this gives
  \(Q_2(H)\ge(\lambda_1-\lambda_2)^2/4\).
- Proved all-copy positivity, for arbitrary matrix rank, when the coefficient
  matrix is supported on a common tensor product of local subspaces of
  dimension at most two.  On that support the endpoint form is exactly the
  squared norm of the component traceless on every two-dimensional site.
- Derived the \(d=3\) Levi--Civita representation
  \(\operatorname{Tr}(M)I-M=\sum_kA_kM^TA_k^\dagger\).  Its partial
  tensor expansion is not termwise positive; a sparse exact \(n=3\)
  certificate saturates the resulting copositivity obstruction.
- Proved the projection-reduction theorem.  For every
  \(-1<\alpha<0\), any finite-copy negative rank-two witness first doubles
  to an equal-singular-value partial isometry \(D\), then finitely many
  orthogonal product flags turn it into a negative orthogonal rank-two
  projection.  The exact flagged expectation is
  \[
  2Q(D)+(1+\alpha)^m\{Q(P_R)+Q(P_L)\}
  +2\alpha^m\operatorname{Re}\mathcal B(P_R,P_L).
  \]
  The nuisance terms vanish while \(2Q(D)<0\) remains fixed.  Hence the
  complete all-copy endpoint question is equivalent to nonnegativity on
  two-dimensional code projectors at every copy number.
- At the \(d=3\) endpoint, obtained the explicit finite flag bound:
  if \(q=Q_n(D)<0\), any \(m\) with \(2^{-m}<-q/4\) makes the flagged
  rank-two projection negative.
- Developed the complete scalar and logical-Pauli swap enumerators of a
  two-dimensional code.  For \(n=3\), projector positivity is exactly the
  Pauli broadcast monogamy inequality
  \[
  Q_3(P)=\tfrac32-\tfrac14\sum_{i=1}^3
  \sum_{a=1}^3\|\mathcal N_i(\sigma_a)\|_2^2\ge0,
  \]
  equivalently \(E_2\ge3p_{\{1,2,3\}}\) in local swap sectors.
- Constructed exact negative pseudo-enumerators satisfying sector
  positivity, every complement/Lorentz/Pauli-Gram identity, the full
  logical sector-POVM relaxation, and natural nesting bounds.  They are
  rigorously nonrealizable.  Thus any proof must use nonlinear common-code
  (Plücker/tensor-square) compatibility, not only linear enumerator data.
- Proved the full \(d=3,n=2\) dual Ky--Fan inequality when either one of
  the two \(3\times3\) summands is normal, with the other arbitrary and
  with the scalar term present.  Also proved all embedded traceless
  \(2\times2\) simultaneous-nonnormal cores and identified broad exact
  equality families.  The genuinely three-dimensional simultaneous
  nonnormal case remains open.
- Derived the exact even-reduction identity
  \[
  {\cal L}^{\otimes n}-2^{1-n}{\cal L}_{\rm grouped}
  =2^{1-n}\sum_{\substack{|S|\ {\rm even}\\|S|\ge2}}{\cal R}_S.
  \]
  For positive rank-two matrices, the grouped quadratic form is exactly
  \(2^{-n}(\lambda_1-\lambda_2)^2\).  Thus the sharp positive-matrix
  conjecture is equivalent to nonnegativity of one cyclic sum of even
  partial reductions.  At two copies it is the proved double-reduction
  sum of squares; at three copies its individual terms can be negative, so
  the cyclic sum cannot be split cut by cut.
- Added a discovery-only optimizer for real permutation-symmetric qutrit
  codes.  It uses the exact hypergeometric decomposition of normalized
  occupation states, so all \(2^n\) partial traces collapse to \(n+1\)
  reduced matrices.  Searches through \(n=14\) found no negative value:
  odd copy counts approached boundary values and the sampled even copy
  counts remained positive.  These floating-point observations are not
  used as mathematical evidence.
- Completed an exact projector-induction audit.  The full parity formula is
  \[
  Q_n(P)=2^{-n}\sum_{j\ge1}(3^{2j}-1)
  (e_{2j}-3o_{2j+1}),
  \]
  but its individual brackets can be negative even for two product
  codewords.  The common-isometry block recursion retains the projection
  identities \(\sum_kP_{ik}P_{kj}=P_{ij}\); scalar rank induction loses
  precisely these relations.  The exact code
  \(P=Q_1\otimes|\Phi_2\rangle\langle\Phi_2|_{23}\) has even-reduction
  contributions \((-1,-1,2)\), proving that only the cyclic sum can be
  controlled.
- Reduced the full three-copy projector problem to the exact crossed-purity
  inequality
  \[
  \sum_i(2y_i-x_i)\le\frac{e(u)+e(v)}2.
  \]
  An orthogonal four-term pair gives cross-sector deficit \(-3/8\), while
  the two diagonal terms compensate exactly and the code has \(Q_3=0\).
  A separate rational sparse pair disproves a proposed holomorphic
  concurrence bridge.  These are exact obstructions, not numerical
  evidence.
- Proved the sharp positive-rank-two inequality for a non-product
  two-parameter parity family at every copy number.  At odd \(n\) its
  defect is an explicit sum of two squares; at even \(n\) the remaining
  \(2\times2\) copositivity determinant is positive by a quadratic with
  negative discriminant.  This family includes a rational example where a
  mixed subprojection derivative is negative although the full strong
  determinant is positive.
- Proved the strong three-copy inequality on common local qubit supports
  via six covers by nine pairwise anticommuting observables.  Averaging
  qutrit-to-qubit compressions reaches sector coefficient \(2\), whereas
  the qutrit target needs \(3\); the exact factor loss rules out that
  isotropic compression argument.

## 2026-07-28 12:17--12:42 PDT — full three-copy theorem and recursion audit

- Proved, without a local-dimension restriction, the sharp strong
  three-copy theorem
  \[
  Q_3(H)\geq\frac18\left(2\operatorname{Tr}H^2
  -(\operatorname{Tr}H)^2\right)
  \qquad(H\succeq0,\ \operatorname{rank}H\leq2).
  \]
  In particular every rank-two code projection has \(Q_3(P)\geq0\).
  The proof purifies \(H\) with a logical qubit, assigns the three logical
  Pauli directions bijectively to the three physical sites, and chooses
  the sign of each reduced encoded Pauli as the physical observable.
  The resulting observables anticommute.  The two elementary estimates
  \[
  \sum_j\langle O_j\rangle^2\leq1,\qquad
  2\|X\|_2^2\leq\|X\|_1^2+(\operatorname{Tr}X)^2
  \]
  give the theorem after averaging the six assignments.  All normalization
  identities were independently rederived from complementary purities.
- Extended the same sign-frame argument to arbitrary mixed states with a
  maximally mixed logical-qubit marginal.  This proves the exact
  fixed-marginal support-function bound and explains why the earlier
  unrestricted operator-norm relaxation lost the sharp constant.
- Extracted all-\(n\) consequences by grouping sites into three blocks and
  by positive rank-one conditioning.  These consequences do not close:
  exact rational formal sector tables at \(n=4\) and \(n=5\) satisfy every
  grouped one-, two-, and three-block inequality, sector positivity, and
  the logical even/odd trace identities, yet have negative singleton
  endpoint functionals.  The tables are nonrealizability obstructions,
  not physical witnesses.
- Completed the sequential-sector audit.  The exact Abel-tail formula is
  \[
  D(3)=8\sum_{j\geq1}9^{j-1}T_j.
  \]
  Product equality codes make every fixed-depth initial window negative
  when their Hamming distance is sufficiently large.  Scalar prefix
  masses therefore cannot furnish a bounded-memory induction; the first
  closed recursion state is matrix-valued and retains the common-isometry
  relations.
- Completed the reduction-map algebra audit.  Although
  \({\cal R}^2={\cal R}+2I\) and
  \({\cal R}^{-1}=({\cal R}-I)/2\), the natural inverse-image cone,
  complement-pair inequalities, and orbit-moment cone are all refuted by
  exact rank-two equality codes.  These failures locate the missing
  information in the tensor-square/Plücker structure rather than the
  reduction algebra alone.
- Ran a discovery-only real optimization over the asymmetric parity family
  \[
  u=a_0|1^n\rangle+\sum_i a_i|e_i\rangle,\qquad
  v=b_0|0^n\rangle+\sum_i b_i|\overline e_i\rangle
  \]
  for \(3\leq n\leq12\).  No reliable negative value appeared.  Values
  near zero were treated as boundary/roundoff observations and are not
  mathematical evidence.

## 2026-07-28 12:42--14:20 PDT — four-copy frontier and nonlinear obstructions

- Reduced the rank-two projector problem at four sites to
  \[
  Q_4(P)=\tfrac12(e_2-3o_3+10e_4).
  \]
  Isolated the sharper, sharp-coefficient conjecture
  \(e_2+6e_4\ge3o_3\), which would imply
  \(Q_4(P)\ge2e_4\).  Its equivalent purification form is
  \[
  6\operatorname{Tr}\rho_K^2+
  \sum_{i<j}\operatorname{Tr}\rho_{ij}^2
  -3\sum_i\operatorname{Tr}\rho_{Ki}^2\ge0.
  \]
- Proved that this four-copy candidate is exactly the difference between
  the sum of six grouped strong three-copy defects and the sum of four
  Haar-conditioned strong three-copy defects.  Exact formal sector models
  show that separate nonnegativity of all currently known grouped,
  conditioned, and Pauli-shadow inequalities does not prove the required
  comparison.
- Recorded exact counterfamilies to naive three-copy-defect tensorization,
  pairwise sector sharing, scalar/Pauli decoupling, and orbitwise Hodge
  injection.  These failures consistently show that the missing estimate
  must retain global common-code compatibility.
- Lifted the four-copy purity functional to three replicas.  Removing the
  global alternating \(S_3\) sector, as forced by the rank-two condition,
  is not by itself a positive certificate: the local representation type
  (sign, sign, trivial, standard) gives the exact negative block \(-4I\)
  while carrying no global sign representation.
- Derived exact qutrit Hodge--Walsh orbit formulas and the pointwise
  Pluecker identity tying the logical symmetric and exterior amplitudes.
  An exact equality code has a strictly negative individual Hodge orbit,
  proving that compensation must mix distinct unordered-pair orbits.
- Proved a nonproduct all-copy flagged-GHZ subclass formula
  \[
  Q_{m+1}(P)=|a\bar b-c\bar d|^2+
  2^{-m}(1-(-1)^m)(|a|^2-|c|^2)^2.
  \]
- Derived the exact Grassmann Euler equation
  \([P,\Phi_n(P)]=0\) and full Hessian.  A nonfactor five-site equality
  code supported on local qubit planes has a completely explicit
  positive-semidefinite dyadic Hessian.  Thus a factor-only critical-point
  classification is false, while the enlarged alternative “pure factor
  or common local qubit supports” remains viable.
- The proposed cumulative hierarchy
  \[
  \sum_{\ell\ge j}\binom{2\ell}{2j}e_{2\ell}
  \ge3o_{2j+1}
  \]
  is false.  The exact five-site cyclic code has layer masses
  \((9/8,15/16,15/8,0,0,1/16)\), hence its \(j=2\) expression is
  \(-3/16\).  Pure spectator sites extend this obstruction to every
  \(n\ge5\).
- Completed an exact qutrit graph-code reduction: every arbitrary logical
  two-plane in a graph-state orbit reduces to four logical Weyl eigenplanes.
  Exhaustive integer enumeration of all 58,320 four-site graph/syndrome
  cases gives nonnegative endpoint values; connected cases obey the sharp
  bound \(Q_4\ge1/4\).  This is a large exact subclass, not a general
  four-copy proof.
- Proved all-copy positivity for every arbitrary two-plane in the
  three-string qutrit repetition subspace.  If
  \(P=I-|z\rangle\langle z|\) there and
  \(s=\sum_a|z_a|^4\), then
  \[
  Q_n(P)=
  \begin{cases}
  (1-s)(1-2^{1-n}),&n\text{ odd},\\
  1-s+2^{2-n},&n\text{ even}.
  \end{cases}
  \]
  Thus coherent repetition does not activate the negative three-point
  Gram direction of the local endpoint kernel.

## 2026-07-28 14:20--15:35 PDT — exact rank cutoff at the four-copy frontier

- The Clifford-frame audit proved a sharp commuting/anticommuting
  covariance lemma but also an unavoidable additive gap in the natural
  normalized-Pauli proof.  An exact qutrit code saturates the obstructing
  constant.  The simple three-replica lift likewise has an admissible
  invariant block of value \(-4\).
- A refined tensor-cube calculation showed that this bad block is genuinely
  populated by an exact qutrit code.  A second, larger negative
  three-standard block is populated simultaneously; positive Young
  sectors compensate in the full value.  Thus removing one bad
  representation sector cannot prove the inequality.
- Derived the exact homogeneous four-copy target
  \[
  {\cal B}(H)=6\operatorname{Tr}H^2+
  \sum_{|S|=2}\|\operatorname{Tr}_S H\|_2^2
  -3\sum_{|S|=1}\|\operatorname{Tr}_S H\|_2^2\ge0
  \]
  for positive \(H\) of rank at most two.  Its purification is the
  qubit-reference inequality already isolated above.
- Proved that the rank cutoff is essential: for
  \(|\Phi_3\rangle_{K4}\otimes|GHZ_3\rangle_{123}\), the reference has
  dimension three, the physical marginal has rank three, and the exact
  value is \(-2/3\).
- Reduced the missing rank-two assertion to a \(2\times2\) copositivity
  inequality after diagonalizing \(H\).  Its two diagonal entries are
  nonnegative by a direct sum of six linear-entropy subadditivity squares;
  only the lower bound on the off-diagonal entry remains.
- Direct homogeneous searches with qubit reference and physical dimensions
  two through four again approached zero without a resolved negative.  The
  qutrit zero points had numerically rank-deficient one-site marginals,
  consistent with the common-local-qubit equality boundary.  This is
  discovery information only.
- Derived a Gram-corrected transfer-matrix formula for translation-invariant
  two-dimensional MPS codes.  It gives an exact constant-coefficient
  recurrence of order at most \(D^8\).  Proved all-copy positivity for
  physical-rank-two tensors, every commuting \(D=2\) tensor (including its
  Jordan case), and orthogonal diagonal \(D=3\) tensors.  No negative MPS
  family was found.
- Proved an additional all-copy graph-code theorem.  For the qutrit complete
  graph at every length, every rank-two plane in every three-dimensional
  graph orbit is endpoint-nonnegative.  The proof reduces the signed coset
  sums to a 27-term character formula and handles the one-, two-, and
  three-syndrome-value strata uniformly.  The only cancellation occurs for
  a constant nonzero syndrome at odd length, where the value is exactly
  zero.  A nine-state integer transfer independently audited the formulas.

## 2026-07-28 15:05--15:20 PDT — global Gram frontier and a second graph theorem

- Polarized the four-party homogeneous functional completely.  For
  \(H=\lambda|u\rangle\langle u|+\mu|v\rangle\langle v|\), its two
  diagonal coefficients are sums of six double-antisymmetrizer squares.
  The remaining assertion is exactly the one-sided \(2\times2\)
  copositivity bound on the cross coefficient.
- Rewrote that cross bound as the single direct-sum Pluecker inequality
  \[
  \|r(u,v)\|^2\leq
  \|s(u,v)\|^2+\|q(u)\|\,\|q(v)\|,
  \]
  where all six physical pairs are retained in one norm.  Proved it when
  one eigenvector is fully product, for every one-site logical-flag code,
  and whenever the operator has a common pure physical factor.  Exact
  examples disprove both pairwise Cauchy--Schwarz and positivity of the
  full spectral Gram matrix, so the six pairs cannot be separated.
- Derived the full local-filter Euler and Hessian conditions at a putative
  negative four-party minimum.  A Haar rank-two qutrit filter gives the
  exact average \((5c+T_\ell)/12\), quantifying the remaining
  dimension-reduction obstruction.  The resulting linear swap constraints
  are still compatible with a negative formal sector table.
- In the all-qubit specialization, reduced the homogeneous target exactly
  to \(B_2+6B_0\geq3A_1\) in Pauli weights.  Subset-resolved complement and
  spin-shadow constraints admit an exact rational negative formal model,
  proving that nonlinear pure-state information is still essential.
- Found an exact qutrit equality state
  \(|GHZ_3\rangle_{123}\otimes|\Phi_2\rangle_{K4}\) whose first three
  one-site marginals are full rank.  Hence no positive lower bound by a
  sum of local marginal determinants can prove the four-party inequality.
- Independently audited the complete-graph all-copy proof from its defining
  character sum; no gap was found.
- Proved a second structured all-copy theorem: for every qutrit cycle
  graph with constant nonzero syndrome, every logical rank-two plane is
  endpoint-nonnegative at every length \(n\geq3\), with equality only at
  \(n=3\).  The proof uses exact nine-state transfers, degree-five
  characteristic polynomials, rational root-modulus certificates, and
  finitely many exact base cases.  The standard-library verifier replayed
  every finite certificate.
