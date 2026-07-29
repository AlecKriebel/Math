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

## 2026-07-28 16:24--18:24 PDT — correct filtering and nonlinear local kernels

- Corrected the nonunitary-filter calculation for the genuine endpoint
  form.  The filtered value is quadratic in the local effect, whereas the
  projection-eliminated sector polynomial is not preserved by filtering.
  The exact Haar identity is
  \[
  Q_4(H)=3\mathbb E_x\!\left[Q_4(H_{I-Q_x})-Q_4(H_{Q_x})\right].
  \]
- Proved that three traceless Hermitian qutrit matrices have a common pure
  zero.  Consequently every rank-two code admits, at each physical site,
  a line whose logical compression is scalar.  This gives exact
  projection-preserving line/plane interpolation formulas at every
  critical code.
- Refuted the stronger balanced-orthonormal-basis conjecture by an exact
  triple of qutrit observables and realized that triple as a genuine
  rank-two code compression.  Thus a single balanced line cannot in
  general be completed by an orthogonal balanced line.
- Organized a hypothetical negative projection by the least number of
  full qutrit supports.  At a minimal negative projection \(P\), every
  full site has a real kernel
  \[
  {\cal K}_\ell=\{A=A^\dagger:U^\dagger A_\ell U=0\},
  \qquad \dim{\cal K}_\ell\ge5,
  \]
  on which the exact local effect Hessian must satisfy
  \[
  {\cal N}_\ell(A)\ge -Q_4(P)\|A\|_{\rm op}^2.
  \]
  Hence one nonpositive kernel direction would give an exact
  support-descending contradiction.
- Derived basis-free pseudoinverse and bordered-determinant formulas for
  the restricted Hessian.  Exact sparse codes refute universal signs for
  its trace, its determinant, the proposed bound
  \(\operatorname{tr}{\cal N}|_{\cal K}\le Q_4(P)/8\), and the full
  nine-dimensional positive index.  A new standard-library rational
  verifier checks these obstructions entry by entry.
- Classified the rank-deficient local compression stratum: if the
  compression rank is at most three, a complete orthonormal qutrit basis
  of balanced lines exists.  For full compression rank, the complexified
  five-dimensional kernel necessarily contains a rank-one matrix
  \(Z=|x\rangle\langle y|\).  Its Hermitian quadratures lie in the real
  kernel and have an exact paired Hessian formula with
  \(V_x^\dagger V_y=0\).  The surviving four-copy target is to prove that
  at least one common rank-one kernel point supplies a nonpositive paired
  direction; individual points can have either sign.

## 2026-07-28 18:05--19:45 PDT — coefficient-10 SOS and crossed-kernel obstructions

- Isolated the actual four-copy projection target
  \[
  {\cal Q}=e_2-3e_3+10e_4\geq0
  \]
  as one global coefficient-\(10\) Pluecker norm inequality.  The extra
  compensation over the homogeneous target is exactly \(8e_4\).
- Proved that no local Hodge-orbit argument can establish this target:
  an exact zero code contains an individual decomposable orbit of value
  \(-1/2\), repaired only by cross-orbit compensation.
- Proved a representation-theoretic no-go theorem for fixed quadratic
  Gram/SOS certificates.  The quadratic covariant sectors are
  multiplicity-free under \(U(3)^4\times U(2)\), while an exact rational
  affine-rank computation shows that the only affine sector identities
  on rank-two qutrit codes are the logical even/odd parity sums.  Those
  identities are incompatible with a nonnegative Gram representation of
  the coefficient vector \((0,0,1,-3,10)\).
- At a hypothetical negative minimizer, the local-effect Hessian
  \({\cal N}_\ell\) must be positive definite on the at-least
  five-dimensional kernel of
  \({\cal C}_\ell(A)=U^\dagger A_\ell U\).  Exact sparse examples refuted
  three simpler replacements for this crossed-kernel assertion:
  unrestricted positive inertia can be six; the kernel trace can be
  positive and can exceed \(F(P)/8\); and the kernel determinant can be
  positive with two negative directions.
- The smallest determinant-sign obstruction uses only five basis terms:
  \[
  u=(-i|1212\rangle+|0010\rangle)/\sqrt2,\quad
  v=(i|2212\rangle+(-1+i)|0111\rangle+(1-i)|1111\rangle)/\sqrt5.
  \]
  Its kernel spectrum is exactly
  \((-7/160,-59/2400,1/400,1/400,3/160)\).
- Despite these no-go results, every dense and sparse search still finds
  at least one nonpositive crossed-kernel direction.  The direct assertion
  \({\cal N}_\ell|_{\ker{\cal C}_\ell}\not\succ0\) remains a sharp,
  finite-dimensional sufficient condition for the four-copy theorem.
  A new possible route uses the six generic rank-one points in the
  projective intersection
  \(\mathbb P(\ker{\cal C}_\ell)\cap(\mathbb P^2\times\mathbb P^2)\);
  no sign theorem for their common-code Hessian values is yet proved.

## 2026-07-28 17:50--18:26 PDT — complement-balance spectral reduction

- Under the four-site complement-balance hypothesis, reduced the proposed
  sharp bound \(p_{1234}\geq1/8\) to a \(3\times3\) Pauli-Gram problem.
  With
  \[
  D=\sum_{|T|=2}G_T-2\sum_{|T|=1}G_T,\qquad t=\operatorname{tr}D,
  \]
  the exact identities are
  \[
  16c_{1234}(x)=1+\frac{t-x^tDx}{4},\qquad
  \operatorname{Re}E_{1234}
  =\left(\frac18+\frac t{32}\right)I-\frac D{32},\qquad
  p_{1234}=\frac{6+t}{16}.
  \]
  Hence \(\lambda_{\min}(D)\leq\operatorname{tr}D\), in particular
  negative inertia at most one, would prove the sharp bound.
- Proved the sharp bound on the boundary stratum where some antipodal
  logical basis has orthogonal reductions at one physical site.
- Applied the strong three-block theorem to every positive logical
  filter and, independently, after conditioning each physical qutrit
  on a Haar-random line.  This yields two exact families of Lorentz-cone
  quadratic inequalities.
- The formal symmetric target with isotropic Gram matrices satisfies all
  those inequalities strictly while giving
  \(D=-(26/15)I_3\).  Therefore quadratic Pauli-Gram consequences of
  grouped and conditioned strong \(Q_3\) cannot establish the needed
  inertia bound; a nonlinear common-isometry compatibility inequality is
  essential.

## 2026-07-28 18:52--19:11 PDT — exact Hodge-determinant obstruction

- Refuted the proposed complement-balanced identity
  \(\sum_k|\det S_k|=1\) with an exact four-qutrit graph code.  Its
  proper nonempty swap moments are all \(4/3\), so it is
  complement-balanced, while
  \[
  p_{1234}=\frac5{24},\qquad
  \sum_k|\det S_k|=\frac{\sqrt{21}}3.
  \]
- More decisively, applying a qutrit Fourier transform on one physical
  site preserves every \(A_T\) but changes the determinant sum to
  \[
  \sum_k|\det S_k|=\frac13.
  \]
  Hence even the proof-relevant lower bound
  \(\sum_k|\det S_k|\ge1\) is false on the complement-balanced slice.
- Gave sparse exact formulas for the rotated code.  Of the 81
  determinants, 54 vanish and the other 27 have modulus \(1/81\).
  A standard-library Eisenstein-integer verifier checks orthonormality,
  all moments, \(p_{1234}=5/24\), and both determinant sums.
- The exact swap-sector split is especially diagnostic:
  \(d_{R,k}=\det S_k/8\) for every odd \(R\) and every \(k\).
  Thus the eight sector contributions align phasewise, but each has
  determinant \(\ell^1\) norm \(1/24\) despite sector mass \(1/8\).
  The proposed sectorwise lower bound fails by exactly a factor of three.
- The failure is caused by local-basis dependence: complement balance
  and \(\sum_k\|S_k\|_F^2=16p_{1234}\) are local-unitary invariant, but
  the fixed-coordinate determinant \(\ell^1\) norm is not.  Any surviving
  Hodge-determinant proof must optimize over local frames or use an
  invariant replacement.

## 2026-07-28 19:06--19:18 PDT — universal odd-sector Pluecker identity

- Proved a pointwise, basis-covariant nonlinear realizability identity
  for the eight odd Hodge quadratics of every decomposable four-party
  bivector:
  \[
  q_{\bar i}=\frac13q_i+h
  \quad\text{for all four singleton masks }i,
  \]
  with one common scalar \(h\).  Equivalently,
  \[
  q_{11}-q_7=\frac{q_4-q_8}{3},\quad
  q_{13}-q_7=\frac{q_2-q_8}{3},\quad
  q_{14}-q_7=\frac{q_1-q_8}{3}.
  \]
- The proof reduces Walsh inversion to
  \(2(m_i-m_j)=m_{ik}+m_{il}\).  Double antisymmetrization factors its
  coefficient as a four-form; it annihilates
  \(\omega\otimes\omega\) exactly because the common rank-two Pluecker
  vector is decomposable and \(\omega\wedge\omega=0\).
- This reduces the eight pointwise sector polynomials to five, but the
  Fourier-rotated exact code proves that the missing magnitude estimate
  does not follow: every odd sector has Hermitian mass \(1/8\) and Hodge
  \(\ell^1\)-mass \(1/24\).
- The strictly smaller surviving determinant lemma is therefore the
  local-frame-optimized bound
  \[
  \sup_{g_1,\ldots,g_4\in U(3)}
  \sum_k\left|\det\!\left[
  U^T\bigotimes_i(g_i^TL_{k_i}g_i)U\right]\right|\ge1
  \]
  on the complement-balanced slice.  It remains conjectural.
- A dependency-free exact verifier replays the epsilon factorization,
  its alternating transformation laws, and all Walsh identities.
- Two independent hostile audits checked the moment identity for all site
  choices on exact random integer decomposable bivectors, verified every
  sign and normalization in the Walsh reduction, and confirmed that the
  identity fails for a generic nondecomposable antisymmetric tensor.

## 2026-07-28 20:35--21:48 PDT — unrestricted three-copy audit

- Implemented an unrestricted fully complex rank-two search
  \(C=U\operatorname{diag}(s_1,s_2)V^\dagger\) with independent complex
  Stiefel frames.  In discovery arithmetic only, 1,000 general and 540
  normal three-qutrit starts found no negative \(Q_3\).  At nine fixed
  singular-value ratios, the minima matched
  \(2^{-3}(s_1-s_2)^2\).  Zero minimizers collapsed to common local
  two-dimensional supports.  These observations are not proof evidence.
- Exactly refuted the proposed sufficient cyclic inequality
  \[
  E(C)=3\|C\|_2^2-2\sum_i\|\operatorname{Tr}_iC\|_2^2
       +\sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2\geq0.
  \]
  For
  \[
  C=\operatorname{diag}(1,1,0)\otimes|0\rangle\langle1|
    \otimes|0\rangle\langle0|,
  \]
  the rank is two, the partial-trace norm layers are
  \(2;(4,0,2);(0,4,0);0\), and \(E(C)=-2\).
  Nevertheless \(Q_3(C)=0\), so the witness saturates rather than refutes
  the sharp three-copy conjecture.
- Isolated the exact repaired identity
  \[
  8Q_3(C)=2\|C\|_2^2-|\operatorname{Tr}C|^2+2E(C).
  \]
  Thus the sharp singular-value target is
  \[
  2E(C)+(s_1+s_2)^2-|\operatorname{Tr}C|^2\geq0.
  \]
- Put \(N=\bigotimes_i(2I-F_i)=8Y\), \(M=N-I\succeq0\).  For an SVD and
  \(x_{ab}=u_a\otimes v_b\), the repaired theorem is exactly the
  two-plane shifted minor
  \[
  |h|\leq1+\sqrt{g_1g_2},\qquad
  g_a=\langle x_{aa},Mx_{aa}\rangle,\quad
  h=\langle x_{12},Nx_{21}\rangle.
  \]
- Exactly ruled out routing this through the ordinary matched Gram entry
  \(d=\langle x_{11},Nx_{22}\rangle\).  The basis grid
  \(u_1=000,u_2=001,v_1=110,v_2=111\) has
  \((g_1,g_2,h,d)=(3,3,-4,0)\): the live inequality is saturated, but
  \(|h|\leq1+|d|\) fails maximally.
- Added a dependency-free exact verifier and a detailed proof-layer note:
  `verification/verify_n3_even_reduction_obstruction.py` and
  `notes/agent_n3_shifted_minor_audit.md`.

## 2026-07-28 20:40--22:05 PDT — exact-weight-three Lorentz determinant reduction

- Expanded the four encoded logical Pauli operators in a local
  identity/traceless Hilbert--Schmidt basis and introduced their
  exact-support \(4\times4\) Gram matrices \(Z_R\).
- Proved, using only the four singleton/triple balances, that
  \[
  \widehat\Gamma
  =2I_4+63Z_0-\frac92Z_3,\qquad
  Z_0=\frac4{81}E_{00}.
  \]
  Consequently
  \[
  18(\widehat\Gamma+2\eta)=128E_{00}-81Z_3.
  \]
- Thus the conjectural fixed Lorentz eigenvalue \(-2\) is exactly
  equivalent to the single nonlinear common-code assertion
  \[
  \det(128E_{00}-81Z_3)=0.
  \]
  Its stronger spatial form is
  \(\operatorname{rank}W_3\le2\), where \(W_3\) is the exact-weight-three
  Gram of the encoded traceless Pauli operators.
- Audited the hypotheses carefully: the determinant reduction uses only
  the four singleton/triple equalities.  Uniformity of all eight odd
  bivector sectors uses the stronger seven complement equalities, unless
  one first proves the still-missing sharp nonlinear defect theorem.
- Numerically restored balanced frames consistently have
  \(\operatorname{rank}W_3\le2\).  Stronger seven-balanced frames also
  show rank-three \(6\times27\) stacked flattenings at every site and
  vanishing complementary cubic-moment defects.  These are recorded only
  as discovery targets; no equality classification proving them is known.
- The exact four-copy stopping point is therefore the determinant above.
  It is a smaller explicit Plücker-realizability lemma, but it remains
  unproved; no four-copy theorem or counterexample is claimed.

## 2026-07-28 21:25--21:41 PDT — the uncorrected \(n=3\) even-reduction conjecture is false

- Found the exact rank-two integer matrix
  \[
  C=|0\rangle\langle1|\otimes|0\rangle\langle1|
    \otimes(|0\rangle\langle0|+|1\rangle\langle1|).
  \]
  Its three cyclic even-reduction terms are exactly
  \[
  (2,-2,-2),
  \]
  so \(E(C)=-2\).  This disproves \(E(C)\ge0\) for arbitrary rank-two
  coefficient matrices.
- The witness has singular values \((1,1)\), trace zero, and
  \(Q_3(C)=0\).  It is therefore an exact equality case of the desired
  sharp endpoint bound, not a distillation witness.
- Isolated the correct residual inequality:
  \[
  E(C)+\frac12\bigl((s_1+s_2)^2-|\operatorname{Tr}C|^2\bigr)\ge0.
  \]
  By the even-reduction identity this is exactly equivalent to
  \(Q_3(C)\ge\frac18(s_1-s_2)^2\).
- Extended the witness to the tensor family
  \(C=A_1\otimes A_2\otimes H\), where the \(A_i\) are normalized
  traceless rank-one matrices and \(\operatorname{rank}H\le2\), and
  proved the corrected inequality exactly on that family.  Equality
  requires equal singular values of \(H\) and saturation of its trace
  norm bound.
- Added a dependency-free exact integer verifier for rank, all three
  reduction terms, the corrected defect, and \(Q_3\).

## 2026-07-28 21:54--21:58 PDT — exact phase obstruction for the corrected \(n=3\) Gram route

- Recast the surviving sharp target in the shifted-minor variables
  \(g_1,g_2,h\).  A seemingly natural stronger certificate,
  \[
  |h+1|^2\le g_1g_2,
  \]
  is impossible because it is not covariant under the independent
  phase of the second right singular flag.
- The exact basis grid
  \(u_1=000,u_2=001,v_1=110,v_2=111\) has
  \((g_1,g_2,h)=(3,3,-4)\).  Replacing \(v_2\) by \(-v_2\)
  leaves the diagonals fixed and gives \(h=4\), hence
  \[
  |h+1|^2=25>9=g_1g_2.
  \]
- The same grid saturates both phase-invariant live boundaries:
  \[
  |h|=1+\sqrt{g_1g_2}=4,\qquad
  |h|^2=(1+g_1)(1+g_2)=16.
  \]
  Therefore a valid exterior Gram must either prove the weaker
  determinant minor with diagonals \(1+g_a\), sufficient for
  \(Q_3\ge0\), or supply a phase-covariant exterior vector of norm at
  most one for the sharp shifted radius.  A fixed scalar correction
  cannot work.
- Added the exact audit to
  `verification/verify_n3_even_reduction_obstruction.py` and the proof
  discussion to `notes/agent_n3_shifted_minor_audit.md`.

## 2026-07-28 21:22--21:42 PDT — unrestricted \(n=3\): exact self-adjoint and normal frontier

- Proved, in arbitrary finite local dimensions, the sharp bound
  \[
  Q_3(H)\ge\frac18(s_1(H)-s_2(H))^2
  \]
  for every self-adjoint rank-at-most-two \(H\).  The indefinite case
  follows from the exact orthogonal-pure-state identity
  \[
  \frac18-\mathcal B_3(P_u,P_v)
  =2\left\|\prod_i\frac{I-F_i}{2}(u\otimes v)\right\|^2
   +\frac14\sum_i\operatorname{Tr}(\rho_{\bar i}^u\rho_{\bar i}^v).
  \]
- Extended the same sharp singular-value bound to every normal rank-two
  matrix.  More generally, \(Q_3(C)\ge0\) whenever the left and right
  singular planes coincide, even if \(C\) is not normal.
- Classified the remaining nonnormal locus by the principal geometry of
  its left and right two-planes.  A one-dimensional intersection gives a
  three-dimensional cubic normal form; transverse planes give
  \[
  C=A(I+iJ),\qquad J^\dagger A=AJ,\qquad J^2=-I,
  \]
  and reduce the target exactly to \(Q_3(A)+Q_3(AJ)\ge0\).
- Eliminated the singular-value optimization at fixed planes.  For
  \[
  K(U,V)=(U^\dagger\otimes V^\dagger)
  \bigotimes_i(I-\tfrac12F_i)(U\otimes V),
  \]
  unrestricted positivity is equivalent to the single invariant
  determinant inequality
  \[
  \det K(U,V)^{\Gamma_2}\ge0.
  \]
  The equivalence is exact because a strictly block-positive two-qubit
  Hermitian operator has at most one negative eigenvalue and cannot have
  a negative and a zero eigenvalue simultaneously.
- This reaches the requested “normal theorem plus precise remaining
  nonnormal locus” checkpoint.  It does not settle the transverse
  determinant inequality, so unrestricted three-copy positivity remains
  open internally and no paper/site publication is authorized yet.
- Sharpened the one-dimensional-intersection stratum further.  After one
  scalar phase every such matrix has the exact form
  \[
  C=\gamma|w\rangle\langle w|+\delta|u\rangle\langle v|,
  \qquad \gamma\in\mathbb R.
  \]
  Therefore this whole stratum is equivalent to the single three-vector
  Gram inequality
  \[
  |\mathcal B_3(P_w,|u\rangle\langle v|)|^2
  \le Q_3(P_w)Q_3(|u\rangle\langle v|).
  \]
  A direct determinant calculation shows why the self-adjoint rank-two
  theorem cannot polarize this term: every nontrivial mixed Hermitian
  quadrature has rank three.
- Exactly refuted a tempting sufficient operator-norm bound for that Gram
  inequality.  For the three-qubit GHZ vector \(w\),
  \(Q_3(P_w)=1/2\) while
  \(\|\mathcal L^{\otimes3}(P_w)\|_\infty=1/2\), violating the proposed
  squared bound by a factor of four.  The actual Gram inequality is
  saturated, not violated, by the corresponding opposite-phase GHZ
  projector, so the state-dependent diagonal energy cannot be replaced by
  its universal rank-one lower bound.
- For fixed anchors \(w,v\), reduced the surviving Gram inequality exactly
  to the positive-map condition
  \[
  Q_3(P_w)K_v-A_wP_vA_w\succeq0,\qquad
  K_v=\sum_{S\subseteq[3]}(-1/2)^{|S|}
       \rho_S^v\otimes I_{\bar S}.
  \]
  This is the smallest current intersection-one lemma: it preserves the
  state-dependent compensation that the false operator-norm bound discards.

## 2026-07-28 — unrestricted \(n=3\) unshifted-minor falsifier

- Identified the corrected exterior-sector target
  \[
  (0,1,4,13;\ 1,0,-3,-12)
  \]
  as exactly one half of the already proved strong positive-rank-two
  defect kernel
  \[
  G_{\rm psd}
  =F_K\prod_{i=1}^3(2I-F_i)-2F_K+I.
  \]
  The unresolved theorem is therefore crossed positivity
  \(\langle A\otimes B,G_{\rm psd}A\otimes B\rangle\ge0\) for two
  purifications with a common qubit marginal; the established theorem is
  only its diagonal specialization \(B=A\).
- Exactly ruled out a sector-diagonal certificate made from the three
  natural grouped three-block defects plus nonnegative sector masses.
  After physical symmetrization their \((k,r)=(1,1)\) coefficients are
  \(2,3,2\), while the target coefficient is zero.  Nonnegative
  multipliers must all vanish and therefore cannot generate the target's
  negative \((1,2)\) and \((1,3)\) coefficients.
- Exactly refuted the proof route “ordinary crossed Cauchy--Schwarz plus
  energy Monge.”  At
  \(u_1=v_1=|000\rangle,\ u_2=v_2=|111\rangle\), the true unshifted
  determinant is equality, but the two crossed Cauchy diagonals have
  product \(64\) while the matched product is \(1\).
- Computed the full constrained Hessian at the canonical nonnormal zero
  \[
  C_0=|000\rangle\langle110|+|001\rangle\langle111|.
  \]
  In the \(204\)-real-dimensional qutrit partial-isometry chart it is
  positive semidefinite of rank \(149\) and nullity \(55\), splitting
  exactly into \(149\) rational positive rank-one blocks.  Exact
  polarization verifies that every cubic Taylor coefficient on the
  \(55\)-dimensional flat space vanishes.  Hence the first possible local
  negative branch is one explicit quartic form; its sign remains open.
  Exact finite cross-checks in local dimensions \(2,4,5\) likewise found
  no negative Hessian direction, but no general dimension-compression
  theorem is claimed.

## 2026-07-28 23:43 PDT — exact SOS at the canonical nonnormal zero

- Settled the first unresolved local term at
  \[
  C_0=|000\rangle\langle110|+|001\rangle\langle111|.
  \]
  The complete \(55\)-variable quartic on the constrained-Hessian kernel
  is nonnegative and has an exact rational positive-Gram certificate.
- The quartic's \(14\)-dimensional coordinate-sign symmetry splits the
  Gram problem into \(192\) character blocks.  Exact zero-diagonal
  elimination leaves \(969\) quadratic monomials; the reconstructed
  rational minimal faces have total rank \(618\) and maximum block size
  \(24\).
- On those faces, coefficient matching is an exact sparse system of
  \(3348\) equations in \(1894\) reduced Gram variables.  Its rational
  rank is \(1361\).  An exact solution with \(533\) free rational
  parameters makes every reduced Gram block positive definite.
- Added the \(126\)-kilobyte certificate
  `verification/certificates/n3_boundary_flat_quartic_sos.json` and the
  independent verifier
  `verification/verify_n3_boundary_flat_quartic_sos.py`.  Certificate
  version 2 vendors the expanded exact quartic, so the verifier is
  standard-library-only.  It checks exact positive \(LDL^T\) pivots for
  all \(192\) blocks and matches all \(3348\) rational coefficients.
- Hostile-review correction: this is the raw quartic restriction to the
  Hessian kernel, not yet the Lyapunov--Schmidt effective quartic.
  Positive-Hessian coordinates of order two can couple through mixed
  cubic terms and subtract a Hessian-inverse square.  Therefore the
  certificate alone does **not** prove quartic-order local stability.
  Computing that exact Schur complement is the next local target.

## 2026-07-29 00:02--00:38 PDT — effective quartic SOS and exact equality decomposition

- Computed all \(149\) exact mixed-cubic quadratic forms at
  \[
  C_0=|000\rangle\langle110|+|001\rangle\langle111|
  \]
  and formed the genuine Lyapunov--Schmidt quartic
  \[
  q_{4,\mathrm{eff}}(k)
  =q_{4,\mathrm{raw}}(k)
   -\sum_{j=1}^{149}\frac{\ell_j(k)^2}{4h_j}.
  \]
  The forms contain \(544\) terms in total; the resulting effective
  quartic has \(1448\) nonzero terms.
- Found and reconstructed an exact rational positive Gram certificate
  for \(q_{4,\mathrm{eff}}\).  Its \(30\)-dimensional sign symmetry gives
  \(505\) quadratic monomials in \(158\) blocks of size at most \(24\).
  The exact face rank is \(300\).  Coefficient matching has \(1759\)
  equations and \(670\) reduced variables, exact rank \(555\), and
  \(115\) free rational parameters.  Every nonzero reduced Gram is
  positive definite; the smallest numerical eigenvalue is \(1/2\).
- Hardened the verifier so that no Taylor coefficient is trusted.
  `verification/derive_n3_boundary_effective_quartic.py` starts from
  the definition of \(Q_3\) and the explicit polar chart, then
  independently reconstructs the \(204\)-coordinate Hessian, its
  \(55+149\) exact splitting, \(2446\) raw quartic terms, all mixed
  forms, and the effective quartic using only Gaussian-rational
  arithmetic.  The standard-library verifier
  `verification/verify_n3_boundary_effective_quartic_sos.py` checks
  this derivation, the Hessian-inverse subtraction, every exact
  positive \(LDL^T\) pivot, and all Gram coefficients.
- Classified the effective-SOS equality ideal exactly.  Its \(300\)
  quadratic equations comprise \(278\) products using only \(36\)
  independent linear forms and \(22\) ambiently irreducible quadrics.
  The product graph has \(64\) maximal branches with size profile
  \(2\times18,6\times10,56\times6\).  Recursive exact factorization
  visits \(486\) rational linear states, has no nonlinear terminal
  ideal, and reduces \(148\) leaves to four maximal linear components:
  \[
  \{q_{4,\mathrm{eff}}=0\}
  =L_0\cup L_1\cup L_2\cup L_3,\qquad
  \dim(L_0,L_1,L_2,L_3)=(37,37,27,27).
  \]
  Exact generic Jacobian ranks are \(18,18,28,28\).
- Added a separate \(299\)-kilobyte finite branching certificate and
  the standard-library verifier
  `verification/verify_n3_boundary_effective_zero_decomposition.py`.
  It reconstructs the \(300\) equations from the positive Gram
  certificate, checks all \(278\) ambient factorizations, independently
  enumerates the \(64\) initial branches, verifies every split in the
  \(486\)-node DAG and all \(148\) leaves, and checks equality with the
  asserted four-component union.  The complete exact check passes in
  about \(17\) seconds.
- Identified \(L_0\) intrinsically as the tangent space to the exact
  zero manifold
  \[
  C=|a\rangle\langle b|_{12}\otimes P_W,\qquad\operatorname{rank}P_W=2.
  \]
  This explains its dimension \(16+16+4+1=37\) and exact vanishing.
  The other three components are the now-isolated higher-order local
  frontier.  Three exact rational Hessian-minimizing paths in each have
  first nonzero coefficient at order six, positive in every sample;
  this is discovery evidence, since secondary kernel and positive
  corrections have not yet been eliminated.
- Added the proof note
  `notes/agent_n3_boundary_effective_quartic_sos.md`, the exact
  equality-decomposition script
  `discovery/decompose_n3_boundary_effective_zero_ideal.py`, and exact
  higher-path probes.

## 2026-07-28 — unrestricted \(n=3\) exterior/Koszul reduction

- Recast the unshifted operator target
  \[
  M_Q(P)=\prod_{i=1}^3(2E_i-I)(P)\succeq0
  \]
  as the equal \(8\)-versus-\(8\) universal-inversion cube
  \[
  \sum_{S\subseteq[3]}M_{KS}(P)
  \preceq\sum_{S\subseteq[3]}M_S(P).
  \]
  Every \(M_T(P)\) is independently positive and has an exact
  antisymmetric-frame Gram representation.  The remaining issue is one
  state-dependent contraction between the two cube analysis operators.
- Proved by exact boundary tables that no contraction diagonal in the
  subset label can work.  The spin-flip zero requires complement routing
  \(m_{K,S}=m_{S^c}\), while the nilpotent zero requires a single-bit
  translation \(m_{K,S}=m_{S\triangle\{1\}}\) on its nonzero cube face.
  A valid incidence map must therefore mix cube vertices and vary with the
  common anchor.
- Derived the coupled Pauli--exterior formula, the sharper
  \(15\)-frame Koszul target, the phase-superposition identity, and an
  exact five-gamma inequality under a common-commutant hypothesis.
  Exact rational examples refute the two tempting completions: a
  conditional phase absorption and the use of individually optimal,
  noncommuting Clifford signs.
- Found an exact obstruction to the naive three-replica \(S_3\) Gram/SOS
  route.  In the qutrit-only isotypic block
  \[
  [21]_K\otimes[111]_{H_1}\otimes[111]_{H_2}\otimes[21]_{H_3},
  \]
  the repeated-\(A\) compression of the lifted unshifted kernel is
  \[
  \frac94\begin{pmatrix}-5&-3\\-3&3\end{pmatrix},
  \]
  with exact eigenvalues \(9,-27/2\).  Hence no positive
  three-replica permutation-algebra Gram operator, equivalently no
  holomorphic cubic Hermitian SOS, can prove the theorem.  The negative
  linear-span direction is not a physical Veronese tensor
  \(A\otimes A\otimes B\), so this is a nonlinear-realizability
  obstruction rather than a counterexample.
- Added exact notes and standard-library verifiers:
  `notes/agent_n3_exterior_koszul_recoupling.md`,
  `verification/verify_n3_exterior_koszul_recoupling.py`,
  `notes/agent_n3_three_replica_s3_obstruction.md`, and
  `verification/verify_n3_three_replica_s3_obstruction.py`.
- Exactly refuted positivity of the separated odd-parity anchor.  In
  \(K=2\) and three qutrit physical spaces,
  \[
  {\cal A}=-|0000\rangle+|0120\rangle-|0210\rangle+|1120\rangle,
  \quad
  {\cal B}=|1000\rangle-|1120\rangle+|1210\rangle
  \]
  gives \(D_{\rm odd}=-1/2\).  This is not a three-copy witness:
  \(D_{\rm even}=8\), \(D=15/2\), and \(Q_3=9/8\).  An exact rational
  \(LDL^T\) certificate proves that the same anchor's full unshifted
  operator \(M_Q(P_{\cal A})\) is positive definite.  Thus the two
  parity halves must be coupled even away from the known zero manifolds.
- Reduced the intersection-one three-vector inequality to the
  four-replica expectation of
  \[
  {\cal O}=Y_{12}Y_{34}-Y_{14}Y_{23}F_{13}F_{24}
  \]
  on \(w^{\otimes2}\otimes u\otimes v\), and exactly ruled out proving it
  from the linear symmetry \(F_{12}=+1\) alone.  In the qutrit-allowed
  \([22]^{\otimes3}\) block, the rational \(F_{12}\)-even vector
  \((-2,1,1,-1,1,-1,-1,1)\) has norm \(18\) and expectation
  \(-891/8\).  Hence a proof must use the nonlinear repeated-\(w\)
  Veronese equations, rather than a
  positive \(S_4\)-algebra compression.  Added
  `notes/agent_n3_intersection_one_s4_obstruction.md` and its exact
  standard-library verifier.
- The repeated-\(w\) restriction does not repair the bad block
  separately.  The exact physical triple
  \(w=|000\rangle,\ u=v=|111\rangle\) has local \([22]\)-projected
  vector
  \[
  \tfrac13(|0011\rangle+|1100\rangle)
  -\tfrac16(|0101\rangle+|0110\rangle+|1001\rangle+|1010\rangle),
  \]
  whose three-site block contribution is \(-19/96\).  Nevertheless the
  full determinant is zero: \(a=b=1/8,\ z=-1/8\).  Thus even on the
  physical Veronese variety an \(S_4\) proof must couple different local
  isotypic blocks; blockwise positivity is exactly false.
- For a real whitened anchor \(U\), introduced the physical logical
  skew \(J=U\epsilon U^{\mathsf T}\).  It exactly converts the negative
  Fierz coefficient into a trace coefficient:
  \[
  \operatorname{Tr}(U^{\mathsf T}J^{\mathsf T}RV)
  =(U^{\mathsf T}RV)_{12}-(U^{\mathsf T}RV)_{21}.
  \]
  The complete logical quaternion frame gives the exact equivalent
  target \(E_\epsilon\le E_I+E_X+E_Z\).  A trace-only recoupling is
  rigorously too small: with
  \(U=(|000\rangle,(3|001\rangle+4|010\rangle)/5)\) and
  \(X=|000\rangle\langle000|\), its Fierz weighted squared norm grows
  from \(1/8\) to \(1/4\).  Thus a one-site Hodge/Racah map must retain
  all three positive logical channels.
- Exactly ruled out a scalar convex interpolation of the two cube boundary
  routings.  For the spin-flip anchor, suppose fixed nonnegative weights on
  the four odd translations satisfied
  \[
  m_{KS}(A,B)\leq\sum_{T\ {\rm odd}}\lambda_Tm_{S\triangle T}(A,B)
  \quad\text{for every }B,S.
  \]
  Saturation by the spin kernel uniquely forces
  \(\lambda_{\{1,2,3\}}=1\), i.e. pure complement routing.  For the same
  anchor and \(B=|0000\rangle\), however,
  \(m_K=1/2>m_{123}=1/4\).  Hence any successful cube incidence map must
  interpolate coherently at the vector level and distinguish input
  subspaces for a fixed anchor; an anchor-dependent probability mixture
  of cube translations is exactly insufficient.  The proof and rational
  checks were added to the exterior/Koszul note and verifier.

## 2026-07-29 01:40 PDT — Complex logical-quaternion/PPT reduction

- Extended the logical-skew recoupling from real to fully complex
  rank-two matrices.  For an isometry \(U:\mathbb C^2\to{\cal H}\), the
  correct physical skew is \(J=U\epsilon U^\dagger\).  Although \(J\) is
  not generally transpose-skew, \(U^{\mathsf T}\overline U=I_2\) gives
  the exact identity
  \[
  \operatorname{Tr}(U^{\mathsf T}J^{\mathsf T}RV)
  =(U^{\mathsf T}RV)_{12}-(U^{\mathsf T}RV)_{21}.
  \]
- Let \({\cal F}_U(V)_R=\operatorname{Tr}(U^{\mathsf T}RV)\) and
  \(G_U={\cal F}_U^\dagger{\cal F}_U\).  The four-channel Pauli twirl and
  the qubit reduction/partial-transpose identity prove the exact
  equivalence
  \[
  Q_3(UV^\dagger)\ge0\ \text{for every }V
  \quad\Longleftrightarrow\quad
  G_U^{\Gamma_{\rm log}}\succeq0.
  \]
  In blocks \(G_U=\begin{psmallmatrix}A&C\\C^\dagger&B\end{psmallmatrix}\),
  the entire unrestricted frontier is therefore the single coupled
  inequality
  \[
  \begin{pmatrix}A&C^\dagger\\C&B\end{pmatrix}\succeq0,
  \]
  equivalently \(B-CA^{-1}C^\dagger\succeq0\) in the nonsingular case.
  Ordinary Gram positivity has the opposite off-diagonal order, exactly
  isolating the residual nonnormal geometry.
- The blocks are intrinsic:
  \[
  (G_U)_{ab}={\cal K}^{\otimes3}
  (|\overline u_a\rangle\langle\overline u_b|),\qquad
  {\cal K}(X)=\operatorname{Tr}(X)I-\tfrac12X^{\mathsf T}.
  \]
  Thus the remaining assertion is that the Choi matrix of this
  restriction to every common two-plane is PPT.  This is an exact
  reduction, not yet a positivity proof.
- Added exact rational coefficient checks of both the four-channel
  Pauli twirl and the qubit reduction/partial-transpose congruence to
  `verification/verify_n3_exterior_koszul_recoupling.py`.

## 2026-07-29 01:42 PDT — Reversed Schur complement and normal locus

- Strengthened the logical-PPT reduction to the direct four-channel
  operator identity
  \[
  \Gamma_I+\Gamma_X+\Gamma_Z-\Gamma_\epsilon
  =2G_U^{\Gamma_K}.
  \]
  Hence \(Q_3(UV^\dagger)=\langle V,G_U^{\Gamma_K}V\rangle\)
  with no intervening relaxation or congruence.
- Writing
  \(G_U=\begin{psmallmatrix}A&B\\B^\dagger&D\end{psmallmatrix}\),
  complete positivity gives
  \(D-B^\dagger A^{-1}B\succeq0\), while the unrestricted endpoint is
  exactly the reversed Schur inequality
  \[
  D-BA^{-1}B^\dagger\succeq0,
  \qquad
  \|A^{-1/2}B^\dagger D^{-1/2}\|\leq1.
  \]
  The rank-one lower bound gives \(A,D\succeq I/8\), so no
  pseudoinverse is needed for a whitened two-column anchor.
- Proved that no frame-element-by-frame-element PPT certificate can
  establish this inequality.  Each Fierz Gram atom is a pure
  bipartite projector; whenever its analysis matrix has rank two, its
  logical partial transpose has eigenvalue
  \(-s_1s_2\).  An invertible identity-frame atom always supplies such
  a negative term for an isometric anchor.  Any proof must recouple
  different physical frame elements.
- Recorded the Gram reduction's compatibility with the already
  established normal rank-two theorem.  In a spectral decomposition
  \(C=\lambda_1P_1+\lambda_2P_2\), the two-by-two coefficient form is
  real symmetric, and its minimum over the relative phase occurs at
  phase \(0\) or \(\pi\), reducing directly to the self-adjoint
  theorem.  Thus the reversed Schur inequality can fail, if at all,
  only through genuinely nonnormal left/right-plane geometry.
- Added
  `notes/agent_n3_four_channel_ppt_schur.md` and the independent
  standard-library exact verifier
  `verification/verify_n3_four_channel_ppt_schur.py`.

## 2026-07-29 01:57 PDT — Exact qutrit determinant-gap obstruction

- Exactly disproved the proposed qutrit spectral strengthening
  \[
  M_Q(P_{\mathcal U})\succeq
  \frac32\left(\sum_i\det\rho_i\right)I.
  \]
  The isometric code
  \[
  u_0=(|111\rangle+|222\rangle)/\sqrt2,\qquad
  u_1=(|100\rangle+|200\rangle)/\sqrt2
  \]
  has local determinant vector \((0,1/4,1/4)\).
- More generally, replacing the two equal superpositions by
  \[
  u_0(t)=\frac{|111\rangle+t|222\rangle}{\sqrt{1+t^2}},
  \qquad
  u_1(t)=\frac{|100\rangle+t|200\rangle}{\sqrt{1+t^2}}
  \]
  gives determinant sum \(2t^2/(1+t^2)^2\) and an exact eigenvalue
  \(2-2\sqrt{1+t^4}/(1+t^2)\).  Their ratio tends to \(1\), already
  excluding every constant greater than \(1\).  A separate symbolic
  verifier checks the characteristic-polynomial factor and limit.
- An invariant rational \(6\times6\) block of its exact anchored
  operator has eigenvector
  \[
  (0,-1-\sqrt2,1,-1-\sqrt2,1,0)
  \]
  with eigenvalue \(2-\sqrt2\).  Its expectation is \(8\), whereas the
  proposed lower bound gives \(6+3\sqrt2>8\).  Thus the exact ratio is
  at most \(4-2\sqrt2<3/2\).
- This is an exact counterexample only to the intermediate spectral-gap
  claim: the eigenvalue remains positive and does not challenge
  three-copy endpoint positivity.  Added the reconstruction and
  algebraic certificate to
  `verification/verify_n3_qutrit_det_gap_obstruction.py`.
- The same proposed mechanism fails more strongly for every positive
  coefficient.  The factorized isometric anchor
  \[
  |\mathcal U\rangle
  =|\Omega_3\rangle_{12}\otimes
   (|00\rangle+|11\rangle)_{K3}
  \]
  has local determinant vector \((8/27,8/27,0)\), but
  \[
  M_Q(P_{\mathcal U})
  =\left(\frac83I+P_{\Omega_3}\right)
   \otimes(2I-P_{\Phi_2})
  \]
  has an exact nonzero kernel.  Hence no inequality
  \(M_Q\succeq c(\sum_i\det\rho_i)I\) can hold with \(c>0\).
  The verifier reconstructs the full rational \(54\times54\) operator
  and its kernel exactly.  Any viable determinant/Hodge correction
  must vanish on tensor-factorized endpoint zeroes rather than merely
  on the all-local-qubit boundary.
- **Discovery-only next candidate.**  The operator-valued cofactor form
  \[
  {\cal H}(U)=
  \sum_{\{i,j,k\}=\{1,2,3\}}
  (\det\rho_j)(\det\rho_k)\,
  [\operatorname{adj}(\rho_i)]_i\otimes I_{K\bar i}
  \]
  is kernel-compatible: on the factorized zero above, only the
  \(i=3\) term survives and its adjugate projects onto the missing local
  qutrit direction, annihilating the endpoint kernel.  Unrestricted
  complex probes and transverse perturbations did not violate
  \(M_Q\succeq2{\cal H}(U)\); the smallest generalized eigenvalues
  approached roughly \(2.77\).  This is conjectural discovery evidence,
  not a theorem.  Its value is structural: every factor is an exact
  qutrit Hodge/cofactor Gram and it avoids the now-disproved scalar-gap
  obstruction.

## 2026-07-29 02:20 PDT — Exact two-copy pencil residual and second zero tangent

- Put every qutrit two-plane into the singular-pencil gauge
  \[
  D=\operatorname{diag}(a,b,0),\qquad
  Z=\begin{pmatrix}bc&p&q\\r&-ac&s\\t&u&d\end{pmatrix}.
  \]
  For
  \[
  {\cal S}_X(Y)=
  \bigl((YX^\dagger)_0,(X^\dagger Y)_0\bigr),
  \]
  the complete qutrit two-copy inequality is exactly positivity of the
  explicit \(9\times9\) Schur residual
  \[
  2I-{\cal S}_Z^\dagger{\cal S}_Z
  -{\cal S}_Z^\dagger{\cal S}_D
   (2I-{\cal S}_D^\dagger{\cal S}_D)^{-1}
   {\cal S}_D^\dagger{\cal S}_Z.
  \]
  The pivot block is nonsingular, with
  \[
  \det(2I-{\cal S}_D^\dagger{\cal S}_D)
  =\frac83(1+a^2b^2)(1+a^2)^2(1+b^2)^2.
  \]
  This is an exact finite reduction, not yet a proof of its positivity.
  The accompanying dependency-free verifier reconstructs the tangent
  maps, the singular-pencil relation, and the Schur complement exactly.
- Discovery suggests the sharper flattening-volume bound
  \[
  2I-{\cal T}_X^\dagger{\cal T}_X
  \succeq\frac{\det\rho_L+\det\rho_R}{2}I,
  \]
  but it remains conjectural.  An exact saturation example with
  \(D=\operatorname{diag}(3/5,4/5,0)\) and
  \(Z=\operatorname{diag}(4/5,-3/5,0)\) has
  \(D\times Z=(7/25)E_{33}\ne0\), ruling out a gap based on the full
  mixed Hodge cross product.  Any valid certificate must retain only
  the transverse flattening volume.
- Identified the second \(37\)-dimensional component of the exact
  Lyapunov--Schmidt quartic zero set at
  \[
  C_0=|000\rangle\langle110|+|001\rangle\langle111|
  \]
  as precisely the tangent to the embedded local-qubit spin-flip family
  \[
  V=-\epsilon^{\otimes3}\overline U\,\epsilon.
  \]
  Every matrix in this family is an exact endpoint zero because, on
  three qubit supports, \(Q_3(C)\) is the squared norm of the fully
  traceless component, and that component vanishes by the
  skew-versus-symmetric trace identity.
- The family has \(28\) real Stiefel parameters and \(12\) local-plane
  parameters, with exactly the expected three-dimensional logical
  \(SU(2)\) gauge.  Exact row reduction gives differential rank \(37\);
  its \(18\)-row annihilator agrees entry-for-entry with component \(1\)
  of the certified quartic zero decomposition.  Hence every direction
  in this component integrates to an exact-zero curve, explaining the
  vanishing secondary Schur minimum to all orders.  The two
  \(27\)-dimensional formal quartic-flat components remain unclassified.

## 2026-07-29 03:43 PDT — Full qutrit two-copy theorem and the three-copy local-support boundary

- **The unrestricted qutrit two-copy endpoint is proved.**  For every
  \(C\in M_9(\mathbb C)\) of rank at most two,
  \[
  Q_2(C)=\|C\|_2^2-\frac12\left(
  \|\operatorname{Tr}_1C\|_2^2+
  \|\operatorname{Tr}_2C\|_2^2\right)
  +\frac14|\operatorname{Tr}C|^2\geq0.
  \]
  The proof first establishes the independent qutrit rank-two
  projector inequality
  \[
  P\preceq \rho_A\otimes I+I\otimes\rho_B
  \qquad
  (\operatorname{rank}P=2,\ P\subset\mathbb C^3\otimes\mathbb C^3).
  \]
  Testing against a Schmidt-diagonal vector reduces this to an exact
  \(3\times3\) rank-one perturbation.  A Ky Fan argument and the
  polynomial remainder
  \[
  \frac{
  x_1(x_2-x_3)^2+2(x_2+x_3)^3
  }{
  (2x_1+x_2+x_3)(3x_2+x_3)(x_2+3x_3)
  }\geq0
  \]
  prove the operator order.
- In qutrit Hodge notation, the projector order gives
  \[
  {\cal C}_D{\cal C}_D^\dagger+
  {\cal C}_Z{\cal C}_Z^\dagger\preceq2I
  \]
  for every Hilbert--Schmidt orthonormal pair \(D,Z\).  Completing the
  reversed Hodge block then proves the stronger exact inequality
  \[
  \begin{aligned}
  &\|y\|^2+\|w\|^2+\|y\times D\|^2+\|w\times Z\|^2
  +2\operatorname{Re}\langle y\times Z,w\times D\rangle\\
  &\hspace{25mm}\geq
  \frac12|\langle D,y\rangle+\langle Z,w\rangle|^2.
  \end{aligned}
  \]
  The coefficient \(1/2\) is exactly strong enough to restore the
  scalar \(z/\sqrt6\) dual coordinate omitted by the traceless tangent
  problem.  This closes the full two-copy theorem, not only its
  tangent residual.  The dependency-free exact verifier checks the
  polynomial identity, mixed-Hodge algebra, operator completion, and
  scalar normalization.
- **Same-copy three-copy boundary theorem.**  Let \(C\) have rank at
  most two on three qutrits, with left and right singular planes
  \(U=\operatorname{ran}C\) and
  \(V=\operatorname{ran}C^\dagger\).  If any one-site code reduction
  of either plane is singular, then
  \[
  Q_3(C)\geq0.
  \]
  Indeed, if the left plane has local support
  \(W\subset\mathbb C^3\), \(\dim W\leq2\), the compressed one-site
  endpoint factor is
  \[
  (P_W\otimes I)X_3(P_W\otimes I)
  =
  \left(I_W\otimes I_{\bar W}
  -\frac12|\Phi_W\rangle\langle\Phi_W|\right)
  +P_W\otimes P_{\bar W^\perp}.
  \]
  Its \(2\times2\) block has an explicit six-product Pauli
  decomposition and is separable.  Tensoring a separable positive
  factor with the now-proved two-copy two-block-positive operator
  preserves two-block positivity.  The right-plane case follows from
  \(Q_3(C^\dagger)=Q_3(C)\).
- Consequently, every qutrit three-copy counterexample must be
  genuinely interior:
  \[
  \det\rho_i^U>0,\qquad\det\rho_i^V>0
  \qquad(i=1,2,3).
  \]
  This is a nonlinear common-code restriction and uses no extra copy,
  long flag, normality, reality, or equal-singular-value assumption.
- The stronger conjectural cofactor gap
  \(M_Q(P_U)\succeq2{\cal H}(U)\) is **not** claimed.  On a boundary
  \(\det\rho_i=0\), it reduces to a quantitative determinant-weighted
  two-copy lemma.  The theorem above proves only the unshifted
  positivity needed for \(Q_3\geq0\).
- Exact reversed-Schur audits also ruled out two tempting generic
  closures: ordinary Gram positivity plus floors/unitality/Kadison
  bounds does not imply the reversed Schur complement, and separate
  sharp quaternion-channel multiplier norms cannot be combined
  scalarly.  Any full three-copy proof must mix the common tensor-Fierz
  channels coherently before taking norms.

## 2026-07-29 04:37 PDT — Exact sixth-order closure of the two 27-dimensional components

- Completed the exact secondary Lyapunov--Schmidt calculation on both
  unresolved 27-dimensional components \(L_2,L_3\) of the effective
  quartic zero set at
  \(C_0=|000\rangle\langle110|+|001\rangle\langle111|\).
  The two components are related by swapping physical sites one and
  two.
- After quotienting fifteen local-unitary, local-plane, and phase
  directions, the invariant first-order data are
  \(z,d\in\mathbb C\) and \(w\in\mathbb R^6\).  With
  \[
  \xi=w_0+iw_1,\quad\beta=w_2+iw_3,\quad\chi=w_4+iw_5,
  \]
  \[
  t=\frac54(|\xi|^2+2|\beta|^2+2|\chi|^2),\qquad
  \eta=\frac14\xi^2+\beta\chi,\qquad
  \Delta=t^2-|\eta|^2,
  \]
  the exact order-six Schur minimum is
  \[
  \sigma_6=
  \frac{4t}{25\Delta}
  \left[(3t^2-5|\eta|^2)|z|^2|d|^2
  +2t\operatorname{Re}(\eta z^2d^2)\right].
  \]
- The original 177-variable rational minimization reduces exactly to
  a two-variable core
  \[
  h^TKh+h^TLd+d^TJKJd,
  \]
  where
  \[
  K=\frac12\begin{pmatrix}t+\Re\eta&\Im\eta\\
  \Im\eta&t-\Re\eta\end{pmatrix},
  \quad
  L=\begin{pmatrix}\Re\eta+t/5&-\Im\eta\\
  \Im\eta&\Re\eta-t/5\end{pmatrix}.
  \]
- Triangle inequality and AM--GM give the sharp structural bound
  \[
  |\eta|\le t/5.
  \]
  This proves \(\sigma_6\ge0\), strictly when \(z,w,d\) are all
  nonzero.  The complete secondary zero set is therefore
  \(z=0\), \(w=0\), or \(d=0\).  The first two are the known
  intersections with the exact-zero tangent components \(L_1,L_0\).
  The branch \(d=0\), of dimension 25 in \(L_2\), initially appeared
  to be the new higher-order local frontier.
- The \(d=0\) branch in fact integrates to a new exact-zero family.
  In canonical gauge, put
  \[
  B=\begin{pmatrix}-w_0+iw_1&w_2-iw_3\\w_4-iw_5&0\end{pmatrix},
  \qquad D=B-(\operatorname{Tr}B)I=-\operatorname{adj}B,
  \qquad A=D^\dagger.
  \]
  The raw frames factor across site one and have two-site factors
  \((I,sB)^T\) and \((sA,I)^T\).  If \(M=B^\dagger B\), then
  \(A^\dagger A=\operatorname{adj}M\), and
  \[
  (I+s^2M)(I+s^2\operatorname{adj}M)
  =(1+s^2\operatorname{Tr}M+s^4\det M)I.
  \]
  Hence polar normalization changes their product only by a scalar.
  The remaining two-copy coefficient matrix has site-two blocks
  \(sD,I,s^2BD,sB\).  Cayley--Hamilton makes both off-diagonal
  blocks and the diagonal difference scalar on site three, so its
  fully traceless component vanishes exactly.  Therefore the whole
  rank-two partial-isometry path has \(Q_3=0\) for every path
  parameter.
- All sixth-order zeros on \(L_2,L_3\) now integrate to exact-zero
  families: \(z=0\) to spin flip, \(w=0\) to the factorized family,
  and \(d=0\) to the new adjugate family.  Exact continuation code
  independently returned zero coefficients through order twelve, but
  the adjugate proof gives all-order vanishing.
- The exact formula yields the uniform sector bound
  \[
  \sigma_6\ge\frac{12}{25}|z|^2\|w\|^2|d|^2.
  \]
  Hence every closed projective sector separated from the three
  zero branches is genuinely locally nonnegative.  This is not yet a
  full-neighborhood theorem: the bound degenerates at the exact-zero
  branches, and simultaneous radial approach can shift the first
  unresolved comparison to higher order.  A tubular normal-form or
  finite blow-up estimate compatible at all intersections remains
  necessary before claiming an entire neighborhood of \(C_0\).
- The exact theorem and proof are in
  `notes/agent_n3_boundary_l2_secondary_theorem.md`.  The
  compact exact symbolic core check plus three comparisons against the
  full 177-variable calculation are in
  `verification/verify_n3_boundary_l2_secondary_core.py`; the
  exact-family identities are checked in
  `verification/verify_n3_boundary_l2_d0_exact_family.py`.

## 2026-07-29 04:48 PDT — Exact audits of two proposed three-copy recursions

- The partial anchored recursion
  \[
  (2E_2-I)(2E_3-I)(P)\stackrel{?}{\succeq}0
  \]
  is false.  For
  \(u_0=\Omega_{12}|0\rangle_3\),
  \(u_1=\Omega_{12}|2\rangle_3\), and the test column
  \(b_0=\Omega_{12}|1\rangle_3\), complement reversal gives
  \[
  \langle{\cal B},(2E_2-I)(2E_3-I)(P){\cal B}\rangle
  =4Q_2\!\left(\frac13I_3\otimes|0\rangle\langle1|\right)
  =-\frac23.
  \]
  This does not contradict the rank-two two-copy theorem: tracing the
  untouched site produces the displayed rank-three coefficient
  matrix.  It exactly rules out iterating the two-copy result while
  treating an untouched physical site as a harmless ancilla.
- A proposed determinant-weighted two-site cofactor lemma also needs
  the auxiliary normalization
  \(\operatorname{Tr}_{12}R=I_K\).  Without it, the exact rank-two
  projection
  \(R=|0\rangle\langle0|_K\otimes
  (P_{\Omega_0}+P_{\Omega_1})\), where
  \(\Omega_0,\Omega_1\) are two orthogonal qutrit Bell shifts, has
  maximally mixed physical marginals but an entire zero \(K=1\)
  sector.  Hence no strictly positive scalar identity floor can hold
  from rank, trace, and physical determinants alone.
- Even with \(\operatorname{Tr}_{12}R=I_K\), the stronger factorized
  floor
  \[
  M_{Q,2}(R)\succeq
  6\det\rho_1\det\rho_2\,(2I-R)
  \]
  is false.  The rank-one balanced anchor
  \[
  |A\rangle=|0\rangle_K|00\rangle+
  |1\rangle_K\frac{|11\rangle+|22\rangle}{\sqrt2}
  \]
  gives an exact negative eigenvalue
  \((13-\sqrt{185})/8\) for the proposed residual, and a rational
  rank-two continuation preserves the violation.  The weaker scalar
  cofactor floor itself remains open.
- These three failures are mechanism no-go results, not negative
  rank-two witnesses for \(Q_3\).  Exact notes and independent
  checkers are in
  `notes/agent_n3_partial_recursion_counterexample.md`,
  `notes/agent_n3_cofactor_boundary_condition_audit.md`,
  `notes/agent_n3_cofactor_factor_floor_obstruction.md`, and their
  correspondingly named files in `verification/`.

## 2026-07-29 05:14 PDT — Quantitative-PPT and swap-sector Lorentz implication is false

- The proposed abstract diagonal-to-dyad implication remains false even
  after imposing the quantitative physical partial-transpose floor,
  swap invariance, positivity on both sides of partial transpose, and
  all known swap-sector spectral windows.
- An exact rational counterexample is
  \[
  K=\frac25I+\frac25P_{\Phi^+},\qquad
  G=K^\Gamma=\frac25I+\frac15F,\qquad
  T=\frac35X,\qquad a=\frac35.
  \]
  The Bell eigenvalues of \(K\) are \(4/5,2/5,2/5\) on the symmetric
  sector and \(2/5\) on the antisymmetric sector, so
  \[
  \frac18P_{\rm sym}\preceq K_{\rm sym}\preceq
  \frac98P_{\rm sym},\qquad
  \frac38P_{\rm asym}\preceq K_{\rm asym}\preceq
  \frac{27}{8}P_{\rm asym}.
  \]
  Also \(K\succeq2I/5\), \(G\succ0\), and \([K,F]=0\).
  Unlike the first unscaled version of the obstruction, these data
  obey the elementary physical normalization windows:
  \(a=3/5\in[1/8,5/8]\) and
  \(g(P_x)\in[2/5,3/5]\) for every pure logical projector.  They also
  obey the sharp self-adjoint singular-value bound and the known sharp
  scalar projector-pair bounds (with the compatible formal overlap
  profile \(r_x^2=(1+n_x)/2\)).
- For every pure qubit projector with Bloch vector
  \((n_x,n_y,n_z)\),
  \[
  a\,g(P_x)-|\operatorname{Tr}(TP_x)|^2
  =\frac9{25}n_z^2+\frac6{25}n_y^2\ge0.
  \]
  Nevertheless, for \(D=|0\rangle\langle1|\),
  \[
  a\,g(D)-|\langle1|T|0\rangle|^2
  =\frac6{25}-\frac9{25}=-\frac3{25}.
  \]
- This is a no-go for the abstract Lorentz/PPT-floor mechanism, not a
  physical Werner witness.  The missing input must constrain the joint
  common origin of \(G\) and \(T\), beyond their separate spectral and
  diagonal-test properties.
- Full derivation:
  `notes/agent_n3_intersection_lorentz_nogo.md`.
  Dependency-free exact checker:
  `verification/verify_n3_intersection_sector_ppt_nogo.py`.

## 2026-07-29 05:40 PDT — Exact common-origin moment constraint for intersection one

- Encoded the two intersection-one planes simultaneously in one logical
  qutrit isometry \(W|0\rangle=w\), with
  \(W\operatorname{span}\{|1\rangle,|2\rangle\}=w^\perp\) on the
  three-vector support.  With \(J=W\otimes W\), local replica swaps
  \(F_i\), logical swap \(F\), and
  \(R_i=J^\dagger F_iJ\), the entire three-copy endpoint compression
  collapses exactly to
  \[
  K=I-\frac18F-\frac12(R_1+R_2+R_3)
    +\frac14(R_1+R_2+R_3)F.
  \]
  This uses the complement identities
  \(J^\dagger F_iF_jJ=R_kF\).
- Derived the first nonlinear simultaneous-realizability constraint.
  If \(Z_i=(I-JJ^\dagger)F_iJ\), then the \(3\times3\)
  operator-valued leakage Gram is positive and has the intrinsic form
  \[
  {\mathfrak G}_{ii}=I-R_i^2,\qquad
  {\mathfrak G}_{ij}=R_kF-R_iR_j.
  \]
  This relation is forced specifically by the common tensor-square
  origin and is invisible when the three one-cut channels are treated
  independently.
- Proved that leakage positivity and a common commuting-symmetry
  dilation alone are still insufficient.  Every abstract \(K\)
  satisfying the sharp physical parity windows admits such a dilation
  by an explicit eight-effect POVM.  The rational \(9\times9\) example
  in the note has the correct windows and
  \[
  K_{00,00}K_{12,12}-|K_{02,10}|^2=-\frac{13}{320}.
  \]
  Thus the missing condition is genuinely the Veronese requirement
  \(J=W\otimes W\), not merely a common first-moment dilation.
- Proved the complementary no-go: three rational isometries
  \(V_i:\mathbb C^3\to\mathbb C^2\otimes\mathbb C^2\) give three
  individually legitimate one-cut swap moments and a formal endpoint
  compression obeying every sharp parity window, but with crossed
  minor
  \[
  -\frac{209202211}{4826809000}.
  \]
  They cannot have one common origin.  The minimal exact separator is
  the leakage principal block
  \[
  \begin{pmatrix}0&135/169\\135/169&144/169\end{pmatrix},
  \qquad \det=-\frac{18225}{28561}.
  \]
- These are mechanism no-go and nonlinear realizability results, not a
  physical negative \(Q_3\) witness.  The remaining lemma is now the
  crossed \(2\times2\) minor inequality for a triple of compressed
  swaps which has both individual channel origin and one common
  rank-one Stinespring tensor.
- Strengthened the separation once more.  A single rational isometry
  \(V:\mathbb C^3\to\mathbb C^3\otimes\mathbb C^2\), used for all
  three formal one-cut moments, has symmetric swap spectrum
  \[
  \{0,1,1,1,153/169,3937/28561\}
  \]
  and antisymmetric spectrum
  \(\{0,-7/169,-153/169\}\).  Hence the identical triple satisfies
  the full leakage Gram condition and every moment separately has a
  genuine tensor-square channel origin.  Its formal endpoint crossed
  minor is nevertheless
  \[
  -\frac{50166283391}{161605221128}.
  \]
  Thus even the conjunction of separate channel origins, complement
  moments, leakage positivity, and sharp parity windows is
  insufficient.  The remaining constraint is specifically that the
  three channels are compatible marginals of one common rank-one
  Stinespring tensor.
- Derived an exact rank-one-Stinespring compatibility inequality which
  excludes that strongest formal model.  If \(y,z\) are orthonormal
  three-party vectors and every one-site reduction of \(P_y\) is pure,
  then
  \[
  2\sum_i\|\operatorname{Tr}_{\bar i}|z\rangle\langle y|\|_2^2
  \leq
  \sum_i\operatorname{Tr}(\rho_i^z\rho_i^y).
  \]
  It follows by diagonalizing
  \(\sum_iP_i-2\sum_{i<j}P_iP_j\); its only negative sector is the
  product line \(\mathbb Cy\).  For the identical-channel formal model,
  the two sides are \(96/169\) and \(27/169\), respectively.  Hence no
  common tripartite isometry realizes the formal moment tuple.  This is
  a new exact nonlinear/common-marginal separator, but it presently
  controls only the product-column boundary.
- Audited the geometric scope: a generic intersection-one normal form
  does **not** make the dyad vectors orthogonal to the Hermitian anchor.
  The common-qutrit compression remains valid after taking
  \(W|0\rangle=w\) and an orthonormal basis of
  \(\operatorname{span}\{w,u,v\}\cap w^\perp\), but the original
  \(u,v\) become arbitrary logical qutrit vectors.  All orthogonal
  crossed minors in the no-go models are diagnostic slices only; the
  final common-origin lemma is stated for arbitrary logical \(x,y\).
- Full derivation:
  `notes/agent_n3_intersection_common_origin_moment.md`.
  Dependency-free exact checker:
  `verification/verify_n3_intersection_common_origin_moment.py`.

## 2026-07-29 05:30 PDT — Weighted merged adaptive frames are insufficient separately

- Applying the strong positive rank-two theorem to
  \(x|{\cal A}\rangle\langle{\cal A}|+
    y|{\cal B}\rangle\langle{\cal B}|\)
  under each grouping \((Ki)|j|k\) gives eighteen exact weighted
  per-permutation Gram inequalities.  Their full trace-norm
  \(\alpha+\sum\beta\) resolutions have been derived for every
  \(x,y\geq0\).
- An exact enriched formal marginal model passes all eighteen weighted
  inequalities, all six original adaptive inequalities, local
  one-block positivity, Hilbert--Schmidt Cauchy, and nonnegative exact
  self/crossed swap-sector masses, but has
  \[
  D_0=0,\qquad E=-1,\qquad
  D=-1,\qquad Q_3^{\rm formal}=-\frac14.
  \]
  This is a mechanism no-go only: the formal marginals do not have a
  common global realization and give no physical Werner witness.
- The first violated common-origin condition is explicit.  Saturation
  of two cyclic adaptive frames would require a common \(+1\)
  eigenvector of Hermitian unitaries \(M,N\), while exact Pauli
  multiplication gives
  \[
  \{M,N\}=\frac23J,\qquad J^3=8J,\qquad
  \|\{M,N\}\|=\frac{4\sqrt2}{3}<2.
  \]
  Consequently every physical state obeys the joint-frame separator
  \[
  \langle M\rangle^2+\langle N\rangle^2
  \leq1+\frac{2\sqrt2}{3}<2,
  \]
  whereas the formal model demands both expectations equal one.
- More generally, if \({\cal M}_\pi,{\cal M}_\tau\) are the normalized
  adaptive sign combinations for two permutations, their separate
  anticommuting gaps satisfy the exact common-origin inequality
  \[
  \alpha_\pi+\alpha_\tau
  \geq
  T^2\left(
  1-\frac12\|\{{\cal M}_\pi,{\cal M}_\tau\}\|
  \right).
  \]
  This is the first finite nonlinear constraint coupling two adaptive
  frames rather than bounding them independently.
- The complete fifteen-pair orbit of this new separator still does not
  close the formal relaxation.  A second exact rational model has
  nonnegative self/crossed swap-sector masses, satisfies every
  Hilbert--Schmidt Cauchy bound, all separate weighted merged
  trace-norm inequalities, and all pairwise joint-frame constraints,
  but gives
  \[
  D_0=\frac3{50},\qquad
  E=-\frac{203}{200},\qquad
  D=-\frac{191}{200},\qquad
  Q_3^{\rm formal}=-\frac{191}{800}.
  \]
  For relative three-cycles its Pauli-frame anticommutator norm is
  \(4\sqrt2/3\), and the required joint inequality reduces exactly to
  \(2/25\ge1-2\sqrt2/3\); transposition pairs have the trivial norm
  bound \(2\).
- The remaining adaptive-frame lemma is therefore strictly smaller:
  one must either couple at least three permutations in one Gram
  constraint, or quantitatively tie the pairwise anticommutator norms
  to the exterior overlaps.  Independent pair deficits can still float
  too freely.
- The live adaptive-frame problem is therefore smaller and nonlinear:
  couple the Gram matrices of different state-dependent sign frames
  and show that their joint incompatibility deficit absorbs the
  exterior correction.  Independent per-permutation gaps cannot do so.
- Full derivation:
  `notes/agent_n3_merged_adaptive_nogo.md`.
  Dependency-free checker:
  `verification/verify_n3_merged_adaptive_nogo.py`.

## 2026-07-29 06:09 PDT — Exact \(3/4\) theorem on the flagged two-copy boundary

- The numerically recurring orthogonal-triple ratio \(3/4\) is now
  proved sharp, rather than merely observed.
- For an arbitrary normalized two-qubit vector \(W\) and any
  orthonormal maximally entangled pair \(U,V\), the exact inequality
  \[
  |{\cal B}_2(P_W,|U\rangle\langle V|)|^2
  \leq
  \frac34Q_2(P_W)Q_2(|U\rangle\langle V|)
  \]
  holds.
- In the canonical Pauli frame
  \(U=I/\sqrt2,V=X/\sqrt2\), write
  \(W=(aI+bX+cY+dZ)/\sqrt2\), set
  \(t=|\operatorname{Im}(\bar ab)|\) and
  \(D=a^2-b^2-c^2-d^2\).  Then
  \[
  Q_2(P_W)=\frac14+\frac12|D|^2,\quad
  Q_2(|U\rangle\langle V|)=\frac12,\quad
  |{\cal B}_2|=t,
  \]
  while normalization forces the sharp determinant/interference
  tradeoff
  \[
  |D|\geq\max(0,4t-1).
  \]
  The remaining scalar gap is exactly
  \((8t-3)^2/32\).
- Equality occurs at
  \[
  W=\frac1{\sqrt2}\left(
  \sqrt{\frac38}I+i\sqrt{\frac38}X+\frac12Y\right).
  \]
  Adding orthogonal one-qubit flags gives mutually orthonormal
  three-qubit vectors \(w,u,v\) with
  \[
  Q_3(P_w)=\frac3{16},\quad
  Q_3(|u\rangle\langle v|)=\frac14,\quad
  {\cal B}_3(P_w,|u\rangle\langle v|)=-\frac{3i}{16},
  \]
  and hence exact ratio \(3/4\).
- This does not prove the unrestricted orthogonal-triple conjecture.
  It proves that \(3/4\) is the optimal possible constant and
  identifies the equality mechanism as a determinant/phase balance
  on a locally flagged two-copy boundary.
- Full proof:
  `notes/agent_n3_orthogonal_triple_three_quarter_sharpness.md`.
  Dependency-free exact checker:
  `verification/verify_n3_orthogonal_triple_three_quarter_sharpness.py`.

## 2026-07-29 06:55 PDT — Pair-sector rank-one SOS and shifted Gram frontier

- For every rank-one qutrit three-copy operator
  \(C=|x\rangle\langle y|\), the sharp theorem
  \[
  \|\Pi_2C\|_2^2\le\frac49\|C\|_2^2
  \]
  follows from the exact local-swap sum of squares
  \[
  4\|C\|_2^2-9\|\Pi_2C\|_2^2
  =
  \sum_{i<j}\langle(I-F_i)(I-F_j)\rangle
  +\langle\prod_i(I-F_i)\rangle.
  \]
  The constant is attained by product dyads.
- If \(C_r=|x_r\rangle\langle y_r|\) are the two matched singular
  dyads and
  \(G_{rs}=\langle C_r,\Pi_2C_s\rangle\), then unrestricted
  rank-two pair-sector positivity is exactly
  \(G\preceq(2/3)I_2\).
- The rank-one theorem gives
  \(G_{11},G_{22}\le4/9\).  The only remaining condition is therefore
  the shifted determinant
  \[
  (2/3-G_{11})(2/3-G_{22})\ge|G_{12}|^2.
  \]
- Partial transpose makes the missing exterior geometry explicit:
  \[
  \left(\frac23I-\Pi_2\right)^\Gamma
  =\frac29I+\frac49\Pi_{q=2}^-+\frac{20}{9}\Pi_{q=3}^-.
  \]
  Orthogonality of both singular frames kills the identity term in
  the off-diagonal entry.  The remaining lemma is a crossed
  Cauchy inequality coupling the exactly-two and exactly-three local
  exterior sectors of the same two decomposable planes.
- The constant is sharp.  For
  \(C_r=E_{01}\otimes E_{01}\otimes P_r\), \(r=0,1\),
  \[
  G=\frac13\begin{pmatrix}1&1\\1&1\end{pmatrix},
  \]
  so the shifted determinant vanishes.
- Full derivation:
  `notes/agent_n3_pair_sector_shifted_gram.md`.
  Dependency-free exact checker:
  `verification/verify_n3_pair_sector_shifted_gram.py`.

## 2026-07-29 06:13 PDT — The full adaptive-frame support hierarchy is insufficient

- The first genuinely three-frame constraint was evaluated exactly.
  The six Pauli frames split into even and odd triples, and each
  integer-Pauli triple sum has norm \(5\).  Hence a common equal frame
  expectation \(m\) obeys \(m^2\leq25/27\).  This excludes the second
  formal survivor, whose value is \(24/25\).
- A third exact rational formal model passes that new bound, the
  complete pair orbit, every separate weighted merged inequality,
  exact sector positivity, and Cauchy constraints, yet has
  \[
  D_0=\frac3{25},\qquad E=-\frac{509}{500},\qquad
  D=-\frac{449}{500},\qquad Q_3^{\rm formal}=-\frac{449}{2000}.
  \]
- Arbitrarily weighted triples and higher frame support functions do
  not remove this survivor.  If
  \(\widehat M_\pi=\sqrt3\,{\cal M}_\pi\) and
  \(H=\sum_{\pi\in S_3}\widehat M_\pi\), exact Pauli algebra gives
  \[
  (H-10I)(H-6I)(H+2I)(H+6I)=0.
  \]
  The explicit orthonormal vectors
  \[
  u=(-e_1-e_2-e_4+3e_8)/\sqrt{12},\qquad
  w=(e_5-e_6-e_9+e_{10})/2
  \]
  satisfy, for every frame,
  \[
  \langle u,\widehat M_\pi u\rangle=5/3,\quad
  \langle w,\widehat M_\pi w\rangle=1,\quad
  \langle u,\widehat M_\pi w\rangle=0.
  \]
  Therefore, with
  \(t=3(\sqrt{69}-5)/10\), the exact pure state
  \(\sqrt t\,u+\sqrt{1-t}\,w\) has all six normalized frame
  expectations equal to \(\sqrt{23}/5\), precisely the third model's
  value.
- It follows that every real-weight support inequality over any subset
  of the six frames, and the free covariance Gram completion, is
  automatically satisfied by a genuine pure common state.  The
  eigenvalue-\(10\) projector also gives a mixed realization of all
  nine individual Pauli first moments.
- This sharply redirects the adaptive approach: a successful
  separator must retain pure common-marginal geometry of the nine
  individual sign observables and relate it to the exterior overlaps.
  No first-moment support function or Gram matrix with free cross
  entries can suffice.

## 2026-07-29 07:05 PDT — Exact three-copy Ky--Fan dual and pair-sector frontier

- Independently derived the unrestricted qutrit three-copy dual with
  all constants fixed.  Every dual operator has the orthogonal form
  \[
  D=cI_{27}+\sum_iA_i^{(i)}+\sum_{i<j}B_{ij}^{(ij)},
  \]
  where the \(A_i\) are traceless and the \(B_{ij}\) have both
  one-site traces zero.  Unrestricted rank-two endpoint positivity is
  exactly equivalent to
  \[
  s_1(D)^2+s_2(D)^2
  \leq
  24|c|^2+12\sum_i\|A_i\|_2^2+
  2\sum_{i<j}\|B_{ij}\|_2^2.
  \]
- Isolated the first sharp subproblem:
  \[
  s_1\!\left(\sum_{i<j}B_{ij}^{(ij)}\right)^2+
  s_2\!\left(\sum_{i<j}B_{ij}^{(ij)}\right)^2
  \leq2\sum_{i<j}\|B_{ij}\|_2^2.
  \]
  It is exactly equivalent, without relaxation, to
  \[
  \|\Pi_2C\|_2^2\leq\frac23\|C\|_2^2
  \qquad(\operatorname{rank}C\leq2),
  \]
  where \(\Pi_2\) is the sector with exactly two traceless local
  factors.  Both constants are attained by explicit rank-two matrices.
- The witness \(W=(2/3)I-\Pi_2\) has the exact positive partial
  transpose
  \[
  W^\Gamma=\frac29I+\frac49E_2+\frac{20}{9}E_3.
  \]
  Hence an alleged violation has only one possible negative direction:
  the crossed decomposable bivector arising from the two common
  singular planes.
- The same operator has the reciprocal two-atom decomposition
  \[
  W^\Gamma=\frac29\left[
  p({\mathsf S}+t_+{\mathsf A})^{\otimes3}
  +q({\mathsf S}+t_-{\mathsf A})^{\otimes3}\right],
  \]
  with \(t_\pm=2\pm\sqrt3\), \(t_+t_-=1\),
  \(p=(\sqrt3-1)/(2\sqrt3)\), and
  \(q=(\sqrt3+1)/(2\sqrt3)\).  The reciprocal pairing is exact, but
  its two summands are not separately two-block-positive.
- Eliminating the left singular plane gives one intrinsic code
  inequality.  If \(V:\mathbb C^2\to(\mathbb C^3)^{\otimes3}\) is an
  isometry,
  \(R=|\boldsymbol V\rangle\langle\boldsymbol V|\), and
  \({\cal R}_i(X)=I_i\otimes\operatorname{Tr}_iX-X/3\), the pair theorem
  is equivalent to
  \[
  \sum_{i<j}{\cal R}_i{\cal R}_j(R)\preceq2I.
  \]
  This retains the common rank-one Stinespring origin and is strictly
  smaller than the original two-plane optimization.
- Two natural shortcuts are now excluded.  A termwise determinant
  bound over Hodge Kraus operators fails by a factor two on the exact
  equality code, and the stronger one-singular-value dual bound fails
  for the exact diagonal choice
  \(B_{ij}=(|0\rangle\langle0|-I/3)^{\otimes2}\).  The desired
  top-two singular-value sum remains valid on that example.
- Exact derivation:
  `notes/agent_n3_dual_kyfan_pair_sector.md`.
  Dependency-free checker:
  `verification/verify_n3_dual_kyfan_pair_sector.py`.

## 2026-07-29 — Pair-sector critical equations and boundary reduction

- For a normalized rank-two local maximum, put
  \(D=\Pi_2C\), \(f=\|D\|_2^2\), and
  \(C=U\Sigma V^\dagger\).  The complete first-order system is
  \[
  D=fC+R,\qquad U^\dagger R=0,\qquad RV=0,
  \]
  equivalently
  \(D^\dagger C=fC^\dagger C\) and
  \(DC^\dagger=fCC^\dagger\).  The complementary critical block has
  the exact norm
  \[
  \|R\|_2^2=f(1-f).
  \]
- The second variation along every rank-preserving local-filter line
  gives
  \[
  \|\Pi_2(A_iC)\|_2^2\leq f\|A_iC\|_2^2,\qquad
  \|\Pi_2(CB_i)\|_2^2\leq f\|CB_i\|_2^2.
  \]
  If \(A\) or \(B\) has rank at most two, the filtered matrix lies on
  the established one-site-support boundary and satisfies the
  sharper constant \(2/3\).
- Therefore a hypothetical full-support critical point with
  \(f>2/3\) induces, at every left and right site, a \(3\times3\)
  local-filter quadratic form which is nonnegative on every
  rank-at-most-two filter but negative at the full-rank identity
  direction; the identity is also its generalized eigenvector.  This
  is the remaining full-support critical lemma.
- Unrestricted complex alternating critical iteration repeatedly
  converged to \(f=2/3\).  Every generic limiting equality point
  checked had rank-two one-site reductions at all three sites on both
  singular planes.  Twenty random genuinely full-support right
  planes had fixed-plane maxima only between approximately \(0.476\)
  and \(0.530\).  These are discovery observations, not proof.
- Exact derivation:
  `notes/agent_n3_pair_sector_critical_boundary.md`.
  Dependency-free checker:
  `verification/verify_n3_pair_sector_critical_boundary.py`.
