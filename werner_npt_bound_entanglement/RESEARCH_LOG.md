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
