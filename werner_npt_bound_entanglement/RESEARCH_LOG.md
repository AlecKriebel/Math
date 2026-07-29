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

## 2026-07-29 — Exact audit of the cut-projection bridge

- The rank-two qutrit projection inequality
  \[
  P\preceq\rho_A\otimes I+I\otimes\rho_B
  \]
  does not extend to \(3\times m\).  An exact \(3\times4\)
  counterexample has test-vector Schmidt weights
  \((1/2,1/4,1/4)\); the violating rank-two plane is spanned by the
  positive diagonal-block eigenvector and the unused-column vector
  \(|3,4\rangle\).  Its exact violation is
  \((\sqrt5-2)/4\).
- The sharp dimension-free replacement for a rank-two projection on
  \(\mathbb C^3\otimes\mathbb C^m\) is
  \[
  P\preceq\frac43
  (\rho_A\otimes I+I\otimes\rho_B).
  \]
  The coefficient \(4/3\) is optimal for \(m\ge4\).  Sharpness follows
  from the exact threshold determinant
  \[
  \det(H_c-c\varepsilon I)
  =c\varepsilon(3c-4+3\varepsilon).
  \]
- Even formally granting coefficient one on every cut does not close
  the pair-sector Ky--Fan estimate.  For the sharp operator
  \(D=E_{01}\otimes E_{01}\otimes I_3\), each of the three right-plane
  marginal majorants has trace pairing \(8\) with \(D^\dagger D\).
  Their sum is \(24=8\operatorname{Tr}(D^\dagger D)\), not at most
  \(2\operatorname{Tr}(D^\dagger D)\).  The left plane gives the same
  obstruction.
- The pair-sector logical Gram also admits the exact qubit spin-flip
  reduction
  \[
  (mI+K_{\rm f})^{\Gamma_2}
  =(mI+A)\otimes I-\widetilde K,\qquad m=2/9.
  \]
  On the sharp code, both the raw Gram and its feature part are
  full-rank and non-idempotent, excluding a direct identification
  with the rank-two projection in the qutrit theorem.
- Exact notes:
  `notes/agent_n3_cut_projection_extension_obstruction.md` and
  `notes/agent_n3_pair_qubit_reduction_bridge.md`.
  Exact checkers:
  `verification/verify_n3_cut_projection_extension_obstruction.py` and
  `verification/verify_n3_pair_qubit_reduction_bridge.py`.

## 2026-07-29 — Pair-boundary equality rigidity and feature no-go

- On the established one-site-support boundary, pair-sector equality
  \(w_2=2/3\) forces
  \[
  (w_0,w_1,w_2,w_3)=(0,0,2/3,1/3).
  \]
  Globally, every rank-two matrix with \(w_2=2/3\) satisfies
  \[
  Q_3(C)/\|C\|_2^2=-\frac98w_0-\frac34w_1.
  \]
  Thus a full-support equality with a nonzero low sector would already
  be an exact negative three-copy witness.
- Identified two inequivalent exact pair-equality mechanisms:
  factor--Hodge matrices
  \[
  |a\rangle\langle b|_{12}\otimes P_W,\qquad
  AB^\dagger=B^\dagger A=0,
  \]
  and trace-zero embedded three-qubit spin-flip partial isometries.
- The complete pair-deficit Hessian at
  \(C_0=|000\rangle\langle110|+|001\rangle\langle111|\) is exactly
  positive semidefinite of rank \(165\) and nullity \(39\).  Of the
  \(36\) left support-leakage coordinates, only the four common-plane
  motions occur in its kernel.  The whole flat space is spanned by
  the \(21\)-dimensional factor and \(35\)-dimensional
  trace-zero-spin-flip flat tangents.
- This outward rigidity has a sharp local determinant form.  If
  \(\rho_3^U(t)\) and \(\rho_3^V(t)\) are the two singular-plane
  reductions at the deficient third qutrit, then
  \[
  {\cal G}(C(t))\geq\frac29t^2\left(
  [t^2]\det\rho_3^U(t)+[t^2]\det\rho_3^V(t)
  \right)+O(t^3),
  \]
  where the bracketed notation denotes the corresponding quadratic
  determinant coefficient before multiplication by \(t^2\).
  Equivalently, the \(64\) genuine left/right support-opening
  coordinates are isolated Hessian blocks with coefficients
  \(2/9,1/3,\) or \(2/3\).  The constant \(2/9\) is attained.
- Exactly disproved
  \[
  \lambda_{\max}(K_{\rm f})
  \le\frac29+\lambda_{\min}(\operatorname{Tr}_2K_{\rm f}).
  \]
  The exact physical code
  \(U=(|000\rangle,|222\rangle)\),
  \(V=(|000\rangle,|100\rangle)\) has
  \[
  K_{\rm f}=\operatorname{diag}(0,0,4/9,4/9),
  \quad
  \operatorname{Tr}_2K_{\rm f}=\operatorname{diag}(0,8/9),
  \]
  giving the exact violation \(2/9\).  Its partial transpose remains
  positive, so only the stronger sufficient condition fails.
- Exact notes:
  `notes/agent_n3_pair_boundary_equality_hessian.md` and
  `notes/agent_n3_local_s4_recoupling_nogo.md`.
  Exact checkers:
  `verification/verify_n3_pair_boundary_hessian.py` and
  `verification/verify_n3_local_s4_recoupling_nogo.py`.

## 2026-07-29 — Exact recoupled product obstruction

- The stronger claim that the recoupled operator
  \[
  {\cal B}=\widehat{\cal K}-L\widehat{\cal K}R
  \]
  is block positive across
  \((L_1L_2):(R_1R_2)\) is false.
- An exact site-factorized product has local left factors
  \((|01\rangle,|00\rangle,\Phi_3)\) and local right factors
  \((|01\rangle,|11\rangle,\Phi_3)\).  Its direct and crossed
  contractions are respectively \(8/9\) and \(1\), giving
  \[
  \langle{\cal B}\rangle=-1/9.
  \]
- This sharpens the hierarchy of failed relaxations: the unrestricted
  local-\(S_4\) ambient space is negative at \(-24\) with grouped
  Schmidt rank \(64\); the new left--right product is negative at
  \(-1/9\) with grouped ranks \(3,3\); the physical four-fold Segre
  locus has grouped ranks \(1,1\) and remains unresolved.
- Exact note:
  `notes/agent_n3_recoupled_site_product_counterexample.md`.
  Exact checker:
  `verification/verify_n3_recoupled_site_product_counterexample.py`.

## 2026-07-29 — Six-map covariance and the missing compatibility

- At a critical point of the pair-sector functional, with
  \(D=\Pi_2C\) and \(f=\|D\|_2^2\), the six left/right response maps
  obey the exact sitewise identity
  \[
  T_i^L(A)-T_i^R(A)=[A_i,D].
  \]
  For a traceless orthonormal local basis \((F_\mu)_{\mu=1}^8\),
  \[
  \sum_\mu\|[F_\mu^{(i)},D]\|_2^2=6(f-p_i),
  \qquad
  \sum_{i,\mu}\|[F_\mu^{(i)},D]\|_2^2=12f,
  \]
  where \(p_i\) is the sector mass scalar at site \(i\).
- The scalar covariance and norm identities are not sufficient. An
  exact formal model with sectors
  \((w_0,w_1,w_2,w_3)=(1/9,0,2/3,2/9)\) passes all of them while
  giving formal value \(Q_3=-1/8\). It is not asserted to be a
  physical rank-two matrix; in particular its \(w_0\) already exceeds
  the elementary physical trace bound \(w_0\leq2/27\).
- What scalar covariance discards is the common-origin Lie relation
  \[
  [A_i,[B_j,D]]=[B_j,[A_i,D]]
  \qquad(i\ne j).
  \]
  Any successful six-map proof must retain this compatibility.
- Exact note:
  `notes/agent_n3_six_map_covariance.md`.
  Exact checker:
  `verification/verify_n3_six_map_covariance_obstruction.py`.

## 2026-07-29 — Haar filters, equality forms, and a strict sector reduction

- Averaging the deficient-support theorem over local rank-two filters
  \(A_z=I-|z\rangle\langle z|\) gives the exact sitewise and pairwise
  inequalities
  \[
  \frac14w_i-\frac12(w_{ij}+w_{ik})+w_{123}\geq0,
  \qquad
  w_{ij}\leq2w_{123}.
  \]
  Summing the first family yields
  \[
  w_2\leq\frac34-\frac34w_0-\frac{11}{16}w_1,
  \qquad
  Q_3(C)\geq-\frac18+\frac9{32}w_1.
  \]
  Consequently unrestricted three-copy positivity is proved
  throughout the exact sector region \(w_1\geq4/9\).
- Classified equality in the local Haar boundary form. If a Hermitian
  sesquilinear form \(h\) on \(M_3\) is nonnegative on every singular
  matrix and vanishes on every rank-two projection
  \(I-|z\rangle\langle z|\), then
  \[
  h(A,B)=\gamma\left(
  \langle A,B\rangle-\frac12\overline{\operatorname{Tr}A}
  \operatorname{Tr}B\right),\qquad\gamma\geq0.
  \]
- Therefore any negative stationary point saturating the grouped Haar
  inequality must have all six one-site singular-plane marginals
  maximally mixed:
  \[
  \rho_i^L=\rho_i^R=I_3/3,\qquad i=1,2,3.
  \]
  This converts the previously diffuse full-support boundary into an
  isotropic polynomial system.
- At this boundary, the stronger fixed-support rank-two normal
  equations also hold for every \(z\):
  \[
  C^\dagger A_zL_i(A_zE)=0,\qquad
  A_zL_i(A_zE)C^\dagger=0,
  \quad E=(L_j\otimes L_k)C.
  \]
  Extracting the nonconstant \(\mathbb{CP}^2\) harmonic components is
  the current equality-track bottleneck.
- Exact notes:
  `notes/agent_n3_haar_boundary_filter_strengthening.md` and
  `notes/agent_n3_boundary_zero_form_classification.md`.
  Exact checkers:
  `verification/verify_n3_haar_boundary_filter_strengthening.py` and
  `verification/verify_n3_boundary_zero_form_classification.py`.

## 2026-07-29 — True grouped rank-two Hessian and four-column reduction

- After grouping the replicated variables, the rank-two factorization
  reduces the recoupled remainder to an exterior \(4\times4\) Gram
  tested only on positive product rays \(s\otimes t\), not on all
  four-vectors.
- At the rank-two boundary family \(\Phi_2\), the full constrained
  Hessian, including the second fundamental form of the rank-two
  variety, is positive semidefinite. Its real tangent dimension is
  \(416\), rank \(354\), and nullity \(62\). Thus this exact zero is a
  genuine quadratic local minimum; any violation must be higher-order
  along a flat direction or lie away from this boundary.
- For factorizations \(A=XY^\dagger\), \(B=UV^\dagger\), introduce
  their four tensor-grid columns \(E,F\), put \(Z=2I-3\Pi_2\), and set
  \[
  G_E=E^\dagger ZE,\quad G_F=F^\dagger ZF,\quad H=E^\dagger Z\bar F.
  \]
  The target remainder is exactly
  \[
  R=\operatorname{Tr}(G_EG_F)-\|H\|_F^2+
  \frac12\|H-H^T\|_F^2.
  \]
  Hence the surviving four-column lemma is
  \[
  \operatorname{Tr}(G_EG_F)+\|H_{\rm a}\|_F^2
  \geq\|H_{\rm s}\|_F^2.
  \]
- Two natural strengthenings were disproved exactly. Ordinary
  cross-Gram contraction fails by \(-4/9\), with the antisymmetric
  term restoring a positive physical remainder \(4/3\). Moreover the
  exterior Gram itself can have spectrum \((-2,2,4,4)\); its negative
  eigenvector is not a permitted positive product ray. For the exact
  common-origin example the required ray satisfies
  \[
  (s\otimes t)^TW(s\otimes t)
  =4\left((s_1t_1)^2+(s_2t_2)^2+s_1s_2t_1t_2\right)\geq0.
  \]
  Thus the remaining statement is positive-Segre copositivity, not
  positive semidefiniteness of an ambient Gram matrix.
- Exact notes:
  `notes/agent_n3_recoupled_grouped_rank2_boundary.md` and
  `notes/agent_n3_recoupled_four_column_reduction.md`.
  Exact checkers:
  `verification/verify_n3_recoupled_rank2_boundary.py` and
  `verification/verify_n3_recoupled_four_column_nogo.py`.

## 2026-07-29 — Current unrestricted three-copy frontier

- No exact rank-two matrix with \(Q_3(C)<0\) has been found.
- No complete proof of unrestricted three-copy positivity has been
  obtained.
- The supplied positive-operator/Ky--Fan formulation and
  deficient-local-support reduction are consistent with, and now
  subsumed by, the current proof tracks.
- Three lossless forms of the remaining common-origin obstruction are
  being pursued:
  1. the one-plane \(3\)-versus-\(1\) inequality for
     \(H=2I+\sum_{i<j}(I-F_i)(I-F_j)+\prod_i(I-F_i)\), whose parity
     eigenvalues are \(2,2,6,22\);
  2. positive-Segre copositivity of the exterior four-column Gram;
  3. the maximally-mixed-marginal fixed-support polynomial system at
     Haar equality.
- The four-copy projector and all-copy programs remain secondary.
  Nothing in these three-copy reductions has yet been proved to
  tensorize.

## 2026-07-29 — Haar block collapse and fixed-left kernel rigidity

- Fixing one physical site and writing \(C=(C_{ap})_{a,p=0}^2\), put
  \[
  \beta_{ap,bq}
  =
  \left\langle C_{ap},L^{\otimes2}(C_{bq})\right\rangle .
  \]
  The polarized isotropic local form forced at a negative
  Haar-filter equality determines all \(81\) entries uniquely:
  \[
  \boxed{\beta_{ap,bq}=\gamma\delta_{ap}\delta_{bq}.}
  \]
  Thus the full two-copy block Gram has rank one; the result is much
  stronger than the previously known grouped sector equalities.
- For a two-qutrit two-plane \(U\), let \(T_U\) be the positive
  fixed-left compression
  \[
  \langle W,T_UW\rangle=Q_2(UW^\dagger).
  \]
  Equality in the exact two-copy completion has now been classified:
  \[
  \ker T_U\ne0
  \quad\Longrightarrow\quad
  U\subseteq E\otimes F,\qquad
  \dim E,\dim F\le2.
  \]
  The proof keeps every equality condition in the reversed-Hodge
  Schur chain.  The only apparent full-support alternative is,
  up to local unitaries,
  \[
  U=\operatorname{span}\{aE_{11}+bE_{22},E_{33}\};
  \]
  direct substitution into the final equality equations excludes it.
- The boundary kernel dimensions are exact:
  \[
  \dim\ker T_U=
  \begin{cases}
  1,&U\text{ has minimal support }(2,2),\\
  3,&U\text{ has a fixed local factor }(1,2)\text{ or }(2,1).
  \end{cases}
  \]
  Combining this with the preceding theorem proves the global
  rigidity statement
  \[
  \boxed{\dim\ker T_U\ge2
  \Longrightarrow U\text{ has a fixed local factor}.}
  \]
- Exact note:
  `notes/agent_n3_haar_block_gram_collapse.md`.
  Exact checker:
  `verification/verify_n3_haar_block_gram_collapse.py`.

## 2026-07-29 — The formal negative Haar equality is not physical

- Write a rank-two factorization \(C=XY^\dagger\) and, at a selected
  site,
  \[
  X=\sum_r|r\rangle X_r,\qquad
  Y=\sum_p|p\rangle Y_p.
  \]
  The block collapse gives
  \[
  \left\langle X_rY_p^\dagger,
  L^{\otimes2}(X_rY_q^\dagger)\right\rangle
  =\gamma\delta_{rp}\delta_{rq}.
  \]
  Hence the two independent slices \(Y_p\), \(p\ne r\), lie in
  \(\ker T_{\operatorname{ran}X_r}\).  Kernel rigidity forces every
  generic contracted plane \(\operatorname{ran}X(\xi)\) to have a
  fixed factor on one of the other two physical sites; the same holds
  on the right.
- The two possible fixed-factor types are closed determinantal
  varieties.  Irreducibility of the contraction-parameter space
  forces one type to hold identically.  A linear space of matrices
  all of rank at most one has either a common image line or a common
  row factor: for two decomposable tensors, rank one of every linear
  combination forces one of their factors to be proportional.
  Applied to the \(3\times6\) flattening of the slice pencil, this
  makes one physical local support of the original singular plane
  deficient.
- A negative three-copy matrix cannot have such deficient support by
  the established local-support theorem.  Therefore
  \[
  \boxed{\text{no rank-two three-qutrit matrix with }Q_3(C)<0
  \text{ can saturate the sharp grouped Haar-filter bound}.}
  \]
  In particular, the formal negative sector point
  \((w_0,w_1,w_2,w_3)=(1/9,0,2/3,2/9)\) is not physically realizable.
- This is a nonlinear rank-two realizability theorem, but it is not
  yet unrestricted three-copy positivity: a hypothetical negative
  critical point with strict Haar slack remains to be excluded.

## 2026-07-29 — Finite fixed-support normal equations

- At Haar equality, every local rank-two filter
  \(P_z=I-|z\rangle\langle z|\) obeys the exact normal equations
  \[
  X^\dagger N_i(z)=0,\qquad N_i(z)Y=0
  \]
  in a thin factorization \(C=XY^\dagger\).  Clearing the harmless
  \(\|z\|^2\) denominator leaves only \(36\) coefficient matrices of
  bidegree \((2,2)\) per site, together with a Haar-constant equation.
  This independently converts the continuum of filtered equality
  conditions into a finite polynomial system.
- Exact note:
  `notes/agent_n3_haar_fixed_support_normality.md`.
  Exact checker:
  `verification/verify_n3_haar_fixed_support_normality.py`.

## 2026-07-29 — Sitewise strictness and quantitative Haar stability

- The Haar-equality exclusion is sitewise.  If the single-site
  bracket
  \[
  g_i=\frac14w_i-\frac12(w_{ij}+w_{ik})+w_{123}
  \]
  vanished at a negative rank-two matrix, the block collapse at that
  one site would force a singular plane to have deficient support at
  another site.  The one-sided local-support theorem would then give
  \(Q_3(C)\ge0\).  Hence every hypothetical negative matrix obeys
  \[
  \boxed{g_i>0\quad(i=1,2,3).}
  \]
- At a normalized negative critical point \(q=Q_3(C)\), the positive
  local Hessian form \(G_i=h_i-qn_i\) satisfies the exact trace
  identity
  \[
  \operatorname{Tr}_{HS}G_i+8q
  =\frac{15}{2}g_i
  =12\,\mathbb E_zQ_3((I-|z\rangle\langle z|)^{(i)}C).
  \]
- A quantitative version of the determinantal equality
  classification is now proved:
  \[
  \left\|{\mathscr H}_i+\frac{2q}{3}{\cal L}\right\|_{\rm op}
  \le360\sqrt{15}\sqrt{g_i}.
  \]
  The proof uses the \(36\)-dimensional bidegree-\((2,2)\)
  reproducing kernel on \(\mathbb {CP}^2\), positive-form
  Cauchy--Schwarz on row/column singular subspaces, and an explicit
  four-projection polarization.  Two independent hostile audits
  found no gap.
- Explicit inversion of the local block equations gives
  \[
  \left\|
  \beta-\left(-\frac{2q}{3}\right)
  |\operatorname{vec}I\rangle\langle\operatorname{vec}I|
  \right\|_2
  \le4752\sqrt{15}\sqrt{g_i}.
  \]
  Thus small Haar slack forces the entire common \(9\times9\) block
  Gram, not merely its sector sums, close to the forbidden rank-one
  collapse.
- At a critical point \(q=-\delta<0\), stationarity gives the
  complementary marginal estimate
  \[
  g_i\ge
  \frac{\delta^2}{5\,832\,000}
  \left\|\rho_i^{L,R}-\frac13I\right\|_2^2.
  \]
  Exact notes:
  `notes/agent_n3_haar_block_kernel_reduction.md` and
  `notes/agent_n3_stationary_haar_marginal_gap.md`.

## 2026-07-29 — Quantitative interior reduction at a negative minimizer

- If a normalized global rank-two minimizer had value
  \(q=-\delta<0\), every one of its six one-site densities would obey
  \[
  \boxed{\rho_i^L,\rho_i^R
  \succeq\frac{\delta}{1+2\delta}I_3.}
  \]
  For a rank-one filter \(P=|z\rangle\langle z|\) and its rank-two
  complement \(I-P\), the critical Hessian gives equal quadratic
  values.  Boundary positivity supplies the lower bound
  \(\delta(1-r_z)\), while
  \({\cal L}^{\otimes3}\preceq I\) supplies the upper bound
  \((1+\delta)r_z\).
- The same floor passes to the unweighted left and right singular
  planes.  Their one-site determinants therefore satisfy
  \[
  \det\sigma_i^{U,V}\ge2m^2(1-m),
  \qquad m=\frac{\delta}{1+2\delta}.
  \]
  This removes every locally degenerating sequence at fixed negative
  depth.  Combined with the preceding stability theorem, the only
  unresolved critical regime is a well-conditioned common-code core
  with all six marginals nearly maximally mixed.
- Exact note:
  `notes/agent_n3_negative_minimizer_marginal_gap.md`.
  Exact checker:
  `verification/verify_n3_negative_minimizer_marginal_gap.py`.

## 2026-07-29 — Lossless one-plane transition frontier

- The pair-sector Ky--Fan problem is exactly equivalent to the single
  transition contraction
  \[
  |\langle u\otimes v_1,E(w\otimes v_0)\rangle|^2
  \le
  (2+\langle u\otimes v_0,E(u\otimes v_0)\rangle)
  (2+\langle w\otimes v_1,E(w\otimes v_1)\rangle),
  \]
  for all orthonormal \(v_0,v_1\) and unit \(u,w\), where
  \[
  E=\sum_{i<j}(I-F_i)(I-F_j)
  +(I-F_1)(I-F_2)(I-F_3).
  \]
  Equivalently, one normalized \(27\times27\) off-diagonal block must
  be a contraction.  A second exact form is a five-versus-five
  exterior comparison coming from one common rank-one tensor.
- The pair and triple layers cannot be bounded separately.  An exact
  flagged maximally-entangled plane violates the triple-only estimate
  by \(1/6\), with the pair matched mass repairing it.  Ordinary
  crossed Cauchy--Schwarz is also too weak: on the canonical equality
  plane it gives \(4\), while coherent common-plane geometry gives
  the required sharp value \(3\).
- Exact note:
  `notes/agent_n3_one_plane_polarized_exterior.md`.
  Exact checker:
  `verification/verify_n3_one_plane_polarized_exterior.py`.
- Neither the normalized transition contraction nor the remaining
  well-conditioned near-six-uniform critical core has yet been
  resolved.  Therefore unrestricted three-copy positivity and the
  all-copy Werner question both remain open in this project.

## 2026-07-29 — Mixed derivations: exact information and exact limit

- For the pair-sector critical operator
  \(D=\Pi_2C=\sum_kD_{\widehat k}\), mixed local derivations isolate
  the common pair component:
  \[
  [A_i,[B_j,D]]
  =[A_i,[B_j,D_{\widehat k}]]
  \qquad(\{i,j,k\}=\{1,2,3\}).
  \]
  Their complete double-frame operator and Casimir identities are now
  explicit, including
  \[
  \sum_{\mu,\nu}
  \|[F_\mu^{(i)},[F_\nu^{(j)},D]]\|_2^2
  =36\|D_{\widehat k}\|_2^2.
  \]
- An exact degree-two qutrit operator \(D_*\) shows the limitation:
  every first-derivation map has full traceless rank eight, all
  cross-site first-derivation Gram blocks vanish, and all mixed
  Casimir/reconstruction identities hold.  Thus scalar commutator
  moments cannot prove the sharp pair-sector bound.
- The rank-two critical support equations have also been completely
  classified.  If
  \[
  CD^\dagger=fCC^\dagger,\qquad
  D^\dagger C=fC^\dagger C,
  \]
  then \(C\) is a scaled singular subsystem of \(D\), and necessarily
  \[
  s_1(D)^2+s_2(D)^2\ge f^2.
  \]
  This excludes \(D_*\) from the physical critical locus exactly:
  its top-two singular mass is \(1/9\), whereas \(f=2/3\) would require
  \(4/9\).
- Exact note:
  `notes/agent_n3_mixed_derivation_gram.md`.
  Exact checker:
  `verification/verify_n3_mixed_derivation_gram.py`.

## 2026-07-29 — Quantitative slice-to-factor bridge

- For a genuine \(2\times2\)-supported two-qutrit plane \({\cal U}\),
  let \(H_{\cal U}\) be the fixed-left two-copy compression and let
  \(M_{\cal U}\) be its intrinsic factor-plane Pluecker matrix.  The
  complete qutrit operator, including the previously omitted outside
  column sectors, satisfies
  \[
  \boxed{\lambda_2(H_{\cal U})
  \ge\frac1{20}\|M_{\cal U}\|_F^2.}
  \]
  Moreover \(M_{\cal U}=0\) exactly on the two factor-plane rulings.
- The bound yields the explicit two-slice implication
  \[
  \|M_{\cal U}\|_F^2
  \le\frac{40B}{\kappa^2m}
  \]
  when two conditioned right slices have Gram floor \(m\), the left
  factor has least singular value \(\kappa\), and their common
  two-copy endpoint defect is at most \(B\).
- Slice conditioning and projection have now been made quantitative.
  If
  \[
  B\le\frac{\gamma m^2}{77\,760\,000},
  \]
  all six relevant slice factors have least singular value at least
  \[
  \frac{\sqrt\gamma\,m}{6750\sqrt6}.
  \]
  Almost-\(2\times2\) planes can be projected to the boundary with
  controlled error, and on the whole boundary
  \[
  \boxed{\lambda_2(H_{\cal U})
  \ge\frac1{1280}
  \operatorname{dist}({\cal U},\mathrm{Factor})^4.}
  \]
- Exact notes:
  `notes/agent_n2_qubit_support_second_kernel_gap.md` and
  `notes/agent_n3_quantitative_slice_pencil_bridge.md`.
  Exact checkers:
  `verification/verify_n2_qubit_support_second_kernel_gap.py` and
  `verification/verify_n3_quantitative_slice_pencil_bridge.py`.

## 2026-07-29 — Sharp common-pencil product and marginal floor

- If \(a(z)\) and \(b(z)\) are the two sums of squared quadratic
  Pluecker minors detecting the two factor-plane rulings of one
  contracted slice pencil, then their common quadratic origin gives
  the sharp correlation inequality
  \[
  \boxed{\mathbb E[a(z)b(z)]
  \ge\frac25\,\mathbb E a(z)\,\mathbb E b(z).}
  \]
  The constant \(2/5\) is sharp.
- For an isometric plane tensor \(T\), the averaged minor mass on
  either side has the exact marginal lower bound
  \[
  {\cal A}(T)
  \ge
  \frac{(\det\sigma_B\det\sigma_C)^2}{1\,269\,600}.
  \]
  Hence, if the relevant marginals satisfy
  \(\sigma_B,\sigma_C\succeq mI\) and have trace two,
  \[
  {\cal A}(T)
  \ge\frac{m^8(1-m)^4}{79\,350}.
  \]
  Combining the two sides with the sharp \(2/5\) correlation gives
  \[
  \mathbb E[a(z)b(z)]
  \ge
  \frac{m^{16}(1-m)^8}{15\,741\,056\,250}.
  \]
  An independent hostile audit checked the constants and all
  determinant branches.
- Exact note:
  `notes/agent_n3_factor_pencil_product_gap.md`.
  Exact checker:
  `verification/verify_n3_factor_pencil_product_gap.py`.

## 2026-07-29 — Current unrestricted three-copy bottleneck

- The quantitative equality-exclusion chain is now complete on the
  \(2\times2\) boundary and has explicit conditioning, projection,
  no-switching, and marginal-floor estimates.
- The remaining local theorem is sharply isolated: extend the quartic
  second-kernel distance estimate
  \[
  \lambda_2(H_{\cal U})
  \ge c\,\operatorname{dist}({\cal U},\mathrm{Factor})^4
  \]
  from the complete \(2\times2\) boundary to arbitrary complex
  two-qutrit planes, for some explicit \(c>0\), or prove an equivalent
  determinant modulus.  Qualitatively, compactness and the exact
  nullity classification already give a non-explicit modulus; the
  missing point is a usable global quantitative one.
- This would finish the current local common-factor stability bridge,
  but a final global inequality converting it into \(Q_3(C)\ge0\)
  for every negative depth would still have to be written and checked.
  No unrestricted three-copy theorem, three-copy counterexample, or
  all-copy conclusion is claimed.

## 2026-07-29 — Exact obstruction to closing the large-slack branch

- The current scalar, local-stationary, Hessian, marginal-floor,
  quantitative-isotropy, block-Gram, and separately imposed
  common-pencil inequalities are jointly insufficient.  For every
  \(0<\delta<1/8\), there is exact abstract critical data with
  \[
  q=-\delta,\qquad
  (w_0,w_1,w_2,w_3)
  =\left(0,0,\frac{2(1+\delta)}3,
  \frac{1-2\delta}3\right),
  \qquad
  g_i=\frac{1-8\delta}{9},
  \]
  balanced left and right marginals, a positive critical Hessian,
  and the exact local block Gram
  \[
  \beta=
  \left(\frac{2\delta}{3}+\frac{2t}{3}\right)
  |\operatorname{vec}I\rangle\langle\operatorname{vec}I|
  +\frac{2t}{15}I_9,\qquad
  t=\frac{15g_i}{16}.
  \]
- The sector data obey the proved rank-two scalar-trace and
  pair-sector ceilings.  The minor data can separately be realized
  by a genuine balanced qutrit code with
  \[
  \mathbb Ea=\mathbb Eb=\frac5{36},\qquad
  \mathbb E(ab)=\frac{47}{2430}.
  \]
  Thus the obstruction is not caused by replacing the common
  quadratic minor pencil by arbitrary nonnegative numbers.
- This is **not** a physical coefficient matrix.  It proves instead
  that the missing large-slack ingredient must tie the block Gram
  and the Pluecker/minor tensor to the same pair of singular planes.
  Completing the local distance modulus alone cannot settle
  unrestricted three-copy positivity.
- Exact note:
  `notes/agent_n3_large_slack_critical_data_obstruction.md`.
  Exact checker:
  `verification/verify_n3_large_slack_critical_data_obstruction.py`.

## 2026-07-29 — Corrected global second-kernel target

- For a two-qutrit plane \({\cal U}\) with projection \(P_{\cal U}\)
  and one-body plane marginals \(\rho_L,\rho_R\), the distance to the
  two fixed-factor rulings is exactly
  \[
  \operatorname{dist}_2({\cal U},{\sf Fac})^2
  =4-2\max\{\lambda_{\max}(\rho_L),
             \lambda_{\max}(\rho_R)\}.
  \]
- The fixed-left second eigenvalue has the exact augmented
  tangent-map form
  \[
  \lambda_2(H_{\cal U})
  =1-\frac12s_2(\widehat{\cal T}_{\cal U})^2.
  \]
  Hence the desired quartic modulus with constant \(1/1280\) is
  equivalent to one explicit second-singular-value inequality for a
  \(17\)-to-\(18\) dimensional map.
- The tempting unaugmented replacement is false.  For
  \({\cal U}=\operatorname{span}\{E_{11},E_{22}\}\),
  \[
  \chi_{H_{\cal U}}(x)=x(x-1)^8(x-\tfrac12)^9,\qquad
  \chi_{S_{\cal U}}(x)=x^8(x-1)^8(x-2)^2.
  \]
  Thus the raw contraction has two saturated singular directions
  even though the plane is a positive distance from both factor
  rulings.  The scalar rank-one correction in the augmented map is
  essential.
- Exact note:
  `notes/agent_n2_global_second_kernel_reduction.md`.
  Exact checker:
  `verification/verify_n2_global_second_kernel_reduction.py`.

## 2026-07-29 — Lossless Schur reduction of the intersection-one stratum

- The remaining three-vector inequality in the intersection-one
  nonnormal stratum has been reduced without relaxation to two
  vectors.  With
  \[
  A_w=L^{\otimes3}(P_w),\quad
  K_u=M^{\otimes3}(P_u),\quad
  a=Q_3(P_w),
  \]
  positivity for every third vector \(v\) is equivalent to
  \[
  aK_u-|A_wu\rangle\langle A_wu|\succeq0
  \quad\Longleftrightarrow\quad
  \langle A_wu,K_u^{-1}A_wu\rangle\le a.
  \]
  The exact floor \(K_u\succeq I/8\) is not strong enough; the full
  state-dependent inverse is genuinely needed.
- The Schur inequality is proved sharply for fully product anchors
  in every copy number and arbitrary local dimensions.  It is also
  proved whenever \(w,u\) have common qubit support at every site.
  For three copies, the exact two-copy theorem strengthens this:
  common support of dimension at most two at even one site suffices,
  with no restriction on \(v\).
- Consequently any violation of this reduced nonnormal inequality
  must have combined local support dimension three at all three
  sites.
- Exact note:
  `notes/agent_n3_three_vector_schur_reduction.md`.
  Exact checker:
  `verification/verify_n3_three_vector_schur_reduction.py`.

## 2026-07-29 — Exact factor-normal Hessian and qualitative global modulus

- At either fixed-factor ruling, the complete normal Schur Hessian of
  the fixed-left two-copy compression has been calculated exactly.
  If \(V\) is a Grassmann-normal tangent of squared norm \(N\), its
  three-dimensional effective matrix \({\cal M}(V)\) obeys
  \[
  \operatorname{Tr}{\cal M}
  =N+\frac18(B_0+C_0),\qquad
  0\preceq{\cal M}\preceq\frac N2I,
  \]
  and therefore
  \[
  \lambda_2({\cal M}(V))\ge\frac N4.
  \]
  Thus there are no quartically flat non-factor normal directions.
- Taylor and Schur-complement estimates make the local statement
  effective:
  \[
  d_{\rm Gr}({\cal U},{\sf Fac})\le\frac1{4096}
  \quad\Longrightarrow\quad
  \lambda_2(H_{\cal U})
  \ge\frac1{10}d_{\rm Gr}({\cal U},{\sf Fac})^2
  \ge\frac1{20}\operatorname{dist}_2({\cal U},{\sf Fac})^2.
  \]
- Combining this uniform tube with the exact nullity classification
  and compactness proves an exact, but non-effective, global theorem:
  there exists \(c_*>0\) such that
  \[
  \lambda_2(H_{\cal U})
  \ge c_*\operatorname{dist}_2({\cal U},{\sf Fac})^2
  \]
  for every two-qutrit plane.  Hence a global quartic modulus exists
  as well.  Effectivizing the far-region minimum, in particular proving
  the proposed explicit \(1/1280\), remains open.
- Exact note:
  `notes/agent_n2_factor_normal_hessian.md`.
  Exact checker:
  `verification/verify_n2_factor_normal_hessian.py`.

## 2026-07-29 11:38 PDT — Positive-definite crossed-Hodge inertia obstruction

- Falsified the proposed universal bound
  \[
  \operatorname{ind}_-(P_-\beta^\Gamma P_-)\leq1
  \]
  for the structured one-site two-copy block Gram of a rank-two
  three-qutrit coefficient matrix.  The obstruction persists even
  under the additional condition \(\beta\succ0\).
- An explicit rational rank-two factorization gives all nine leading
  principal minors of \(\beta\) strictly positive, while the normalized
  antisymmetric compression is
  \[
  \begin{pmatrix}
  1&0&1/8\\
  0&-1/32&0\\
  1/8&0&-5/32
  \end{pmatrix},
  \]
  which has exactly two negative eigenvalues.
- The example has \(Q_3(C)=801/256>0\).  It is not a distillation
  witness; it proves that a Hodge/logical-\(\epsilon\) argument cannot
  terminate in a universal PSD-minus-one-square formula, even after
  assuming positivity of the full block Gram.  Exact stationarity,
  exact isotropy, or a stronger multi-site common-\(C\) relation is
  indispensable.
- Exact note:
  `notes/agent_n3_crossed_hodge_inertia_counterexample.md`.
  Exact checker:
  `verification/verify_n3_crossed_hodge_inertia_counterexample.py`.

## 2026-07-29 — Pair-sector frontier reduced to one \(3\times3\) determinant

- The sharp two-site degree-one inequality
  \[
  \|\Pi_1^{(2)}C\|_2^2\leq\frac23\|C\|_2^2
  \qquad(\operatorname{rank}C\leq2)
  \]
  follows exactly from the established two-copy endpoint theorem via
  \[
  \frac23\|C\|_2^2-\|\Pi_1^{(2)}C\|_2^2
  =\frac23Q_2(C)+\frac12\|\Pi_0^{(2)}C\|_2^2.
  \]
- Expanding a three-copy matrix in spectator matrix units preserves
  rank at most two blockwise.  Summing the two-site inequality and
  then applying the remaining traceless projection proves the
  three-copy pair-sector bound whenever any one of its three
  components vanishes.
- In the dual fixed-plane formulation, with
  \(X_i=D_{\widehat i}V\),
  \(d_i=2\|B_{\widehat i}\|_2^2-\|X_i\|_2^2\), and
  \(c_{ij}=\langle X_i,X_j\rangle\), every \(2\times2\) principal
  matrix
  \[
  \begin{pmatrix}d_i&-c_{ij}\\-\overline{c_{ij}}&d_j\end{pmatrix}
  \]
  is positive semidefinite.  Therefore the full pair-sector theorem
  is now equivalent to the single remaining condition
  \[
  d_1d_2d_3-\sum_{\{i,j,k\}=\{1,2,3\}}d_i|c_{jk}|^2
  -2\operatorname{Re}(c_{12}c_{23}\overline{c_{13}})\geq0.
  \]
  This is the common three-component Gram-compatibility obstruction;
  separate pairwise estimates contain no further information.
- Exact note:
  `notes/agent_n3_pair_sector_three_component_determinant.md`.
  Exact checker:
  `verification/verify_n3_pair_sector_three_component_determinant.py`.

## 2026-07-29 — Phase--nuclear route fails on intersection-one

- The tensor-independent phase-quadrature sufficient condition
  \[
  \inf_\theta\left(
  \|\operatorname{Re}(e^{-i\theta}C)\|_1^2+
  \|\operatorname{Im}(e^{-i\theta}C)\|_1^2
  \right)\leq2\|C\|_2^2
  \]
  is false even for a rank-two matrix whose row and column planes
  have one-dimensional intersection.
- For \(C=E_{01}+E_{02}+E_{12}\), every Hermitian quadrature is
  traceless with squared Hilbert--Schmidt norm \(3/2\), and its
  determinant is \(\cos\theta/4\); the complementary quadrature has
  determinant \(-\sin\theta/4\).
- Inverting the exact cubic \(r^3-\frac34r-x=0\) and using convexity
  of \(h(y)=y(y-\frac34)^2\) proves uniformly in the phase that
  \[
  \|A_\theta\|_1^2+\|B_\theta\|_1^2\geq7
  >6=2\|C\|_2^2.
  \]
  The exact gap is one. This is not a negative Werner witness; it
  proves that physical tensor geometry cannot be replaced by spectra
  of the coupled Hermitian quadratures, even on the smallest genuinely
  nonnormal support stratum.
- Exact note:
  `notes/agent_n3_intersection_phase_nuclear_obstruction.md`.
  Exact checker:
  `verification/verify_n3_intersection_phase_nuclear_obstruction.py`.

## 2026-07-29 — Exact all-component pair-cycle equality

- Found an exact pair-sector equality with all three dual pair
  components nonzero.  For
  \[
  V=\left(|000\rangle,\,
  (|110\rangle+|012\rangle)/\sqrt2\right)
  \]
  and explicit sparse doubly-traceless pair coefficients, the residual
  data are
  \[
  d=(5/2,4,5/2),\qquad
  (c_{12},c_{23},c_{13})=(2,2,1/2).
  \]
  The full deficit matrix has the exact SOS
  \[
  M=
  (1,-2,1)^T(1,-2,1)
  +\frac32(1,0,-1)^T(1,0,-1),
  \]
  so its spectrum is \(\{0,3,6\}\) and its kernel is
  \(\mathbb C(1,1,1)\).
- Every \(2\times2\) principal determinant equals \(6\), but the full
  determinant vanishes.  The example exactly falsifies the stronger
  normalized row-contraction estimate: its middle normalized row sum
  is \(4/\sqrt{10}>1\).
- A six-parameter sparse cycle family factors as
  \[
  \det M=(d+z)\bigl(e(d-z)-2x^2\bigr),
  \]
  and the second factor is nonnegative by one local profile-overlap
  Cauchy inequality.  This supplies a concrete cycle-SOS motif for the
  remaining global determinant search.
- Exact note:
  `notes/agent_n3_pair_sector_three_cycle_equality.md`.
  Exact checker:
  `verification/verify_n3_pair_sector_three_cycle_equality.py`.

## 2026-07-29 — Exact same-code obstruction to local crossed-Hodge inertia

- Interval-certified a real algebraic rank-two matrix
  \(C=XY^{\mathsf T}\in M_{27}(\mathbb R)\) whose one-site block Gram
  has the exact isotropic form
  \[
  \beta=B\left(I_9+\frac65|\operatorname{vec}I_3\rangle
  \langle\operatorname{vec}I_3|\right),\qquad B>0,
  \]
  with both one-site marginals equal to \(I_3/3\).
- Hence \(\beta\succ0\), both left and right stationarity equations
  hold, and both separate local-filter Hessians have positive
  traceless gap \(9B/5\).  Nevertheless,
  \[
  P_-\beta^{\Gamma_2}P_-=-\frac B5P_-,
  \]
  so its antisymmetric negative inertia is three, not at most one.
- The square rational polynomial system has 56 free variables.  An
  outward-rounded Krawczyk certificate isolates a unique algebraic
  zero with contraction-factor upper bound
  \(2.55451\cdot10^{-5}\) and strict inclusion margin
  \(9.99396\cdot10^{-10}\).  Certified factor minors prove
  \(\operatorname{rank}C=2\).
- This exactly rules out deriving the desired inertia bound from
  same-\(C\) origin, block-Gram positivity, balanced one-site
  marginals, two-sided one-site stationarity, and the two separate
  one-site Hessians.  It is not a negative Werner witness:
  \(Q_3(C)=57B/10>0\).  A proof may still use \(Q_3(C)<0\), all sites,
  or the full coupled rank-two Hessian.
- Exact note:
  `notes/agent_n3_isotropic_block_gram_stationary_counterexample.md`.
  Rigorous verifier and isolating data:
  `verification/verify_n3_isotropic_local_stationary_counterexample.py`
  and
  `verification/data/n3_isotropic_local_stationary.json`.

## 2026-07-29 — Isotropic same-code target reduced to one Plücker norm and one Schmidt-number threshold

- For an isotropic one-site block Gram
  \[
  \beta=A|\operatorname{vec}I_3\rangle
  \langle\operatorname{vec}I_3|+BI_9,
  \]
  defined the invariant contractions
  \[
  T=\operatorname{Tr}\beta=\sum_{a,p}Q_2(C_{ap}),\qquad
  S=\langle\operatorname{vec}I,\beta\operatorname{vec}I\rangle
  =Q_2(\operatorname{Tr}_iC).
  \]
  Exact inversion gives
  \[
  A=\frac{3S-T}{24},\quad B=\frac{3T-S}{24},\quad
  5B-A=\frac{2T-S}{3}.
  \]
- For a thin factorization \(C=XY^\dagger\), proved
  \[
  \beta^{\Gamma}=G_+-G_-,
  \]
  where \(G_+\) is the positive Gram of the three logical
  symmetric-square companions and \(G_-\) is the positive Gram of the
  unique mixed logical bivector
  \(w=(x_0\otimes y_1-x_1\otimes y_0)/\sqrt2\).
- If \(m_{\sigma,\tau}=\operatorname{Tr}(P_\sigma^A G_\tau)\), then
  \[
  3(5B-A)
  =m_{+,+}+3m_{-,+}-m_{+,-}-3m_{-,-}.
  \]
  Thus physical isotropic positivity is exactly one weighted
  symmetric-square-versus-exterior domination.  The exterior entries
  retain the common Plücker factorization
  \[
  w_{\alpha\beta}w_{\gamma\delta}
  -w_{\alpha\delta}w_{\gamma\beta}
  =(x_0\wedge x_1)_{\alpha\gamma}
   (y_0\wedge y_1)_{\beta\delta}.
  \]
- Proved a second exact equivalence: for \(A,B\geq0\), the isotropic
  operator \(BI+A|\operatorname{vec}I\rangle
  \langle\operatorname{vec}I|\) has Schmidt number at most two if and
  only if \(A\leq5B\).  The boundary decomposition is
  \[
  I+5|\operatorname{vec}I\rangle\langle\operatorname{vec}I|
  =12\,\mathbb E_P
  |\operatorname{vec}P\rangle\langle\operatorname{vec}P|,
  \]
  over rank-two qutrit projections \(P\).
- Therefore the remaining isotropic same-code lemma can be phrased
  either as the weighted Plücker inequality or as proving that a
  positive physically realizable isotropic block Gram has Schmidt
  number at most two.  This is an exact smaller target, not yet its
  proof.
- Exact note and dependency-free rational checker:
  `notes/agent_n3_isotropic_plucker_reduction.md` and
  `verification/verify_n3_isotropic_plucker_reduction.py`.

## 2026-07-29 — Exact obstruction to erasing the pair-cycle phase

- Constructed an exact algebraic two-dimensional code and explicit
  Gaussian-integer doubly-traceless \(B_{\widehat i}\) for which an
  inconsistent \(e^{i\pi/4}\) twist of one component edge gives the
  exact excess
  \[
  -\frac{1637114}{5}+232824\sqrt2>0
  \]
  over the pair-sector denominator.  The sign is certified by
  \[
  2(1164120)^2-(1637114)^2=30208499804>0.
  \]
- It follows that the phase-forgotten comparison matrix with
  off-diagonal entries \(-|c_{ij}|\) is not always positive
  semidefinite.  Thus absolute-value diagonal dominance and any proof
  which optimizes the three edge phases independently are false.
- For the same physical, untwisted triple, the genuine quadratic
  deficit is \(375674/5>0\).  This is not a Werner witness; it isolates
  the gauge-invariant phase of
  \(c_{12}c_{23}\overline{c_{13}}\) as indispensable data.
- Exact note:
  `notes/agent_n3_pair_sector_phase_erasure_obstruction.md`.
  Exact checker:
  `verification/verify_n3_pair_sector_phase_erasure_obstruction.py`.

## 2026-07-29 — Exact obstruction to a logical block-Gram proof

- Disproved the stronger \(6\times6\) logical block-Gram certificate
  \[
  [\,\delta_{ij}\|B_{\widehat i}\|_2^2I_2
    -(D_{\widehat i}V)^\dagger(D_{\widehat j}V)\,]_{ij}
  \succeq0
  \]
  by an exact example on
  \(\operatorname{span}\{|000\rangle,|111\rangle\}\).
- With three explicit rational doubly-traceless pair matrices and
  independently selected logical vectors, the output-to-budget quotient is
  exactly \(7/3\), so the proposed block quadratic form equals
  \(-28/9\).
- The same example has genuine scalar deficit matrix
  \[
  \begin{pmatrix}
  1&0&0\\
  0&8/9&-4/9\\
  0&-4/9&8/9
  \end{pmatrix}\succ0.
  \]
  Hence the obstruction is not a Werner witness; it proves that a successful
  scalar determinant argument must retain the common logical-frame coupling
  and cannot allow independent code vectors for the three pair components.
- Exact note:
  `notes/agent_n3_pair_sector_logical_block_gram_obstruction.md`.
  Exact checker:
  `verification/verify_n3_pair_sector_logical_block_gram_obstruction.py`.

## 2026-07-29 — Logical spin-flip completion isolates the surviving common-frame channel

- For the pair-sector deficit, put
  \[
  A_{ij}=(D_{\widehat i}V)^\dagger(D_{\widehat j}V),\qquad
  {\mathbb N}_{ij}
  =\delta_{ij}\|B_{\widehat i}\|_2^2I_2-A_{ij}.
  \]
  With the logical-qubit spin flip
  \({\mathfrak s}(A)=(\operatorname{Tr}A)I_2-A\), proved the exact
  identity
  \[
  M\otimes I_2={\mathbb N}+{\mathfrak s}_K({\mathbb N}).
  \]
  Thus the scalar \(3\times3\) determinant retains two correlated
  logical channels; neither channel may be discarded.
- Gave an exact physical qutrit code for which
  \(\lambda_{\min}({\mathbb N})=-4/243\), while the true scalar
  deficit has spectrum
  \[
  \{7/243,8/81,8/81\}.
  \]
  A second exact physical construction gives a \(-1\) principal minor
  in the spin-flipped Gram.  These examples rule out proving the
  determinant by separate positivity of either logical channel.
- At the known all-three-component equality, the two logical
  residual blocks are respectively a path Laplacian and a weighted
  triangle Laplacian.  Both are positive, share the all-ones kernel,
  and sum to a scalar deficit with spectrum \(\{0,3,6\}\).
- The polarized \(2\times2\) Cayley--Hamilton identity rewrites the
  cubic cycle phase in terms of common logical matrix traces.  This is
  now the smallest exact phase-aware route still standing, but the
  required global domination is not yet proved.
- Exact note:
  `notes/agent_n3_pair_sector_logical_spinflip_obstruction.md`.
  Dependency-free checker:
  `verification/verify_n3_pair_sector_logical_spinflip_obstruction.py`.

## 2026-07-29 — Spectral gap at product saturation of the rank-one pair slack

- Recast the pair-sector Ky--Fan target through
  \[
  K_D=\frac43S I-D^\dagger D,\qquad
  S=\sum_{i<j}\|B_{ij}\|_2^2.
  \]
  The desired theorem is that every two-plane has \(K_D\)-trace at
  least \(2S/3\).
- Proved an exact boundary theorem.  If the sharp rank-one estimate
  \(s_1(D)^2\leq4S/3\) is saturated through a product left vector,
  then the exposing rank-one pair is product--tangent and
  \[
  s_2(D)^2\leq S/3,\qquad
  s_1(D)^2+s_2(D)^2\leq5S/3.
  \]
  Equivalently, the two smallest eigenvalues of \(K_D\) sum to at
  least \(S\), with one-third more slack than the global target
  requires.
- The core certificate is the operator inequality
  \[
  E^\dagger E\preceq
  \frac4{81}I+\frac{12}{81}|y\rangle\langle y|,
  \quad E=\Pi_2(|000\rangle\langle y|),
  \]
  for every normalized product-tangent vector
  \(y=a|000\rangle+b|100\rangle+c|010\rangle+d|001\rangle\).
  A complete \(4\times4\), \(3\times3\), and \(2\times2\) Schur-block
  decomposition proves the certificate.  The \(S/3\) second-value
  constant is attained.
- This excludes one exact operator-norm boundary mechanism but does
  not yet classify non-product rank-one saturation pairs or provide
  the quantitative stability estimate needed away from saturation.
- Exact note and symbolic checker:
  `notes/agent_n3_pair_rankone_slack_saturation.md` and
  `verification/verify_n3_pair_rankone_slack_saturation.py`.

## 2026-07-29 — One-plane marginal Schur and invariant-Gram no-gos

- For the one-plane marginal defect
  \[
  {\cal D}_V
  =6I+2\sum_i e_i(R)-3\sum_{i<j}e_ie_j(R)-R,
  \]
  isolated its canonical three-term allocation
  \[
  {\cal D}_V=\sum_{i<j}
  \left(2I+e_i(R)+e_j(R)-3e_ie_j(R)-R/3\right).
  \]
- On the sharp code
  \(V=(|110\rangle,|111\rangle)\), the three summands have exact
  negative Rayleigh quotients \(-4,-1,-1\).  Thus even the equality
  plane requires compensation among all three physical pairs; a
  termwise two-site Schur proof is impossible.
- In the two-replica form, the physical swap polynomial has sector
  values \(h=(2,2,6,22)\).  The scalar isometry relation is
  \[
  \langle F_K-\tfrac12I\rangle=0.
  \]
  Adding its most general scalar invariant multiplier produces
  \(G_t=F_KH+t(F_K-I/2)\).  Positivity would require simultaneously
  \(t\ge-4\) from the logical-symmetric/physical-\(r=0\) sector and
  \(t\le-44/3\) from the logical-antisymmetric/physical-\(r=3\)
  sector.  Hence no such invariant degree-\((2,2)\) Gram completion
  exists.
- These are proof-mechanism obstructions, not a negative Werner
  witness.  Matrix-valued, higher-degree, or genuinely
  Pluecker/Koszul use of the common code remains open.
- Exact note:
  `notes/agent_n3_pair_marginal_schur_nogos.md`.
  Dependency-free checker:
  `verification/verify_n3_pair_marginal_schur_nogos.py`.

## 2026-07-29 — The logical residual has physical negative index two

- Exactly disproved the prospective common-frame inertia lemma
  \(\operatorname{inertia}_-({\mathbb N})\leq1\), where
  \[
  {\mathbb N}_{ij}
  =\delta_{ij}\|B_{\widehat i}\|_2^2I_2
   -(D_{\widehat i}V)^\dagger(D_{\widehat j}V).
  \]
- For the GHZ code \(V=(|000\rangle,|111\rangle)\), constructed three
  exact doubly-traceless pair coefficients for which
  \[
  {\mathbb N}\simeq H\oplus H,\qquad
  H=
  \begin{pmatrix}
  1&-2/3&-2/3\\
  -2/3&8/9&-4/9\\
  -2/3&-4/9&8/9
  \end{pmatrix}.
  \]
  The exact \(LDL^\dagger\) pivots of \(H\) are
  \(1,4/9,-4/3\), so
  \(\operatorname{inertia}({\mathbb N})=(4,2,0)\).
- The second compound is also genuinely indefinite: its quadratic
  value on an explicit decomposable bivector is \(-56/27\).
  Therefore a proof based on
  \(\bigwedge^2{\mathbb N}\succeq0\), or on a unique residual negative
  direction repaired by the logical spin flip, is impossible.
- This is not a pair-sector counterexample.  The true scalar deficit
  is strictly positive, with spectrum
  \(\{2,8/9,8/3\}\) and determinant \(128/27\).
  Thus the spin-flip completion can cancel a two-dimensional negative
  residual sector.
- Exact note:
  `notes/agent_n3_pair_sector_residual_inertia_two.md`.
  Dependency-free checker:
  `verification/verify_n3_pair_sector_residual_inertia_two.py`.

## 2026-07-29 — Cayley residual factorization and exact termwise obstruction

- Put \(E_i=b_iI_2-X_i^\dagger X_i\) and
  \(\Delta_{ij}=\operatorname{Tr}(E_iE_j)-|c_{ij}|^2\).
  Polarized \(2\times2\) Cayley--Hamilton gives the lossless identity
  \[
  \det M
  =\sum_{\{i,j,k\}=\{1,2,3\}}d_k\Delta_{ij}
   -2\operatorname{Re}\!\left[
    \operatorname{Tr}(E_1E_2E_3)+c_{12}c_{23}c_{31}
   \right].
  \]
- The scalar cycle was also rewritten exactly through the positive
  physical residuals
  \(R_i=b_iI-X_iX_i^\dagger\).  For
  \[
  g^{(i)}_{jk}
  =\operatorname{Tr}(X_j^\dagger R_iX_k),
  \]
  each \(G^{(i)}=[g^{(i)}_{jk}]\) is a positive Gram matrix and
  \[
  g^{(i)}_{jk}
  =b_ic_{jk}-\operatorname{Tr}(A_{ji}A_{ik}).
  \]
  Cayley--Hamilton expresses \(c_{12}c_{23}c_{31}\) through these
  three Grams and the two ordered common-frame cubic contractions.
- Exactly disproved the tempting termwise claim
  \(\Delta_{ij}\geq0\).  For the code
  \(V=(|000\rangle,|110\rangle)\) and sparse doubly-traceless rational
  pair coefficients,
  \[
  \Delta_{12}=-\frac{14}{81}.
  \]
  This is not a pair-sector counterexample: the true scalar deficit
  has spectrum \(\{2/9,2,2\}\) and
  \[
  \det M=\frac89>0.
  \]
  The positive amount missing from \(\Delta_{12}\) is exactly the
  logical spin-flip term
  \(\operatorname{Tr}(E_1{\mathfrak s}(E_2))\).
- Exact note and dependency-free verifier:
  `notes/agent_n3_pair_sector_cayley_residual_factor.md` and
  `verification/verify_n3_pair_sector_cayley_residual_factor.py`.

## 2026-07-29 — Residual inertia cannot imply the scalar determinant

- Exactly disproved the proposed algebraic implication
  \[
  \operatorname{ind}_-{\mathbb N}\leq2,\quad
  {\mathbb N}+{\mathfrak s}_K({\mathbb N})=M\otimes I_2,
  \quad M[\{i,j\}]\succeq0
  \ \Longrightarrow\ \det M\geq0.
  \]
  The obstruction already has \(\operatorname{ind}_-{\mathbb N}=1\).
- Take the scalar matrix with diagonal \(1\) and every off-diagonal
  entry \(-3/4\).  Its one- and two-dimensional principal minors are
  \(1\) and \(7/16\), while
  \[
  \operatorname{spec}M=\{-1/2,7/4,7/4\},\qquad
  \det M=-49/32.
  \]
  For \(P_0=|0\rangle\langle0|\), the logical residual
  \({\mathbb N}=M\otimes P_0\) obeys the exact spin-flip identity and
  has inertia \((2,1,3)\).
- The no-go survives stronger formal constraints: every
  two-component \(4\times4\) principal block of \({\mathbb N}\) is
  positive semidefinite, and
  \[
  {\mathbb N}=\operatorname{diag}(2I_2,2I_2,2I_2)-G
  \]
  for one positive definite common Gram matrix \(G\), with each
  diagonal Gram block bounded by its budget.
- This construction is **formal, not physically realized** as
  \(X_i=(I_i\otimes B_{\widehat i})V\).  It proves that even a future
  physical negative-index-two theorem cannot finish the scalar
  determinant without additional nonlinear common-code
  realizability information.
- Exact note:
  `notes/agent_n3_pair_sector_inertia_completion_nogo.md`.
  Dependency-free checker:
  `verification/verify_n3_pair_sector_inertia_completion_nogo.py`.

## 2026-07-29 — Strengthened pair conjecture reduced to balanced spectra

- Introduced the numerically sharp strengthening
  \[
  \|\Pi _2C\|_2^2\stackrel?{\leq}
  \frac49\left(s_1^2+s_2^2+s_1s_2\right).
  \]
  It implies the unresolved pair-sector theorem.
- Dualized its two-singular-value gauge exactly.  For a pair-sector
  operator \(D\), with \(d_1\geq d_2\), the dual gauge is
  \[
  \begin{cases}
  d_1^2,&d_1\geq2d_2,\\[1mm]
  \frac43(d_1^2-d_1d_2+d_2^2),&d_1\leq2d_2.
  \end{cases}
  \]
- The first branch is exactly the already proved sharp rank-one
  operator-norm bound \(d_1^2\leq4\|D\|_2^2/9\).  Hence every
  spectrally imbalanced case \(d_2\leq d_1/2\) is settled.
- The sole remaining strengthened claim is the balanced tail-mass
  inequality
  \[
  \sum_{j\geq3}d_j^2
  \geq2d_1^2+2d_2^2-3d_1d_2,
  \qquad d_1/2\leq d_2\leq d_1.
  \]
  This is strictly smaller than the original pair-sector problem and
  makes the missing spectral-spreading mechanism explicit.
- Exact note and checker:
  `notes/agent_n3_pair_shifted_dual_band.md`,
  `verification/verify_n3_pair_shifted_dual_band.py`.

## 2026-07-29 13:34 PDT — Complete rank-one saturation classification and uniform second-mode gap

- Completely classified equality in the sharp rank-one pair-sector
  estimate
  \[
  \|\Pi _2(|x\rangle\langle y|)\|_2^2\leq4/9.
  \]
  Up to swapping \(x,y\), every nonzero equality pair is either:

  1. a product vector together with a tangent vector to the
     product-vector variety; or
  2. a common one-site factor together with two \(2\times2\)
     coefficient matrices \(X,Y\) satisfying
     \(\operatorname{Tr}(X^{-1}Y)=0\).
- The proof uses the exact classification of the kernel of the
  polarized \(2\times2\)-minor map.  It forces every local flattening
  rank to be at most two.  In the full \((2,2,2)\) case the common
  local traceless actions have equal determinants:

  - the nonzero-determinant branch is a GHZ pair and is excluded by
    its nonzero three-local-exterior component;
  - the nilpotent branch is
    \[
    x=p|000\rangle+q(|100\rangle+|010\rangle+|001\rangle),
    \qquad y=q|000\rangle,
    \]
    hence is the product/tangent mechanism with the orientation
    reversed.
- Proved the previously conjectural operator certificate throughout
  the common-factor branch:
  \[
  E^\dagger E\preceq
  \frac4{81}I+\frac{12}{81}|y\rangle\langle y|,
  \qquad E=\Pi _2(|x\rangle\langle y|).
  \]
  The only nontrivial block reduces to an exact \(4\times4\)
  determinant.  After setting \(d=a^2-b^2\), \(k=2ab\), its determinant
  has a strictly positive lower bound away from \(d=0\) and \(z=0\);
  both boundary sets have direct Cauchy--Schwarz proofs.
- Combining this with the product-left certificate and its adjoint
  gives the uniform complete-boundary spectral statement
  \[
  s_1(E)=\frac49,\qquad s_2(E)\leq\frac29.
  \]
  Thus every pair-only dual operator exposed at rank-one saturation
  satisfies the strict estimate
  \[
  s_1(D)^2+s_2(D)^2\leq\frac53
  \sum_{i<j}\|B_{ij}\|_2^2,
  \]
  leaving a \(1/3\) margin below the target constant \(2\).
- This does not yet settle the unrestricted pair sector: the next
  missing statement is a quantitative stability theorem keeping
  near-saturating rank-one vectors near the two classified equality
  varieties.
- Exact note and checker:
  `notes/agent_n3_pair_rankone_equality_classification.md`,
  `verification/verify_n3_pair_rankone_equality_classification.py`.

## 2026-07-29 — Feature concurrence implies the stronger shifted pair bound

- Proved an exact bridge from the existing qutrit Hodge feature-state
  target to the strengthened singular-value inequality.  If the positive
  logical feature state \(Q\) has
  \[
  {\cal C}(Q)\leq\frac49,
  \]
  then a Takagi-optimal pure-column decomposition
  \(Q=\sum_a|\operatorname{vec}M_a\rangle
  \langle\operatorname{vec}M_a|\) has
  \[
  \sum_a|\det M_a|\leq\frac29.
  \]
  The elementary identity
  \(m_{01}m_{10}=m_{00}m_{11}-\det M\), followed by
  Cauchy--Schwarz, gives
  \[
  |G_{12}|
  \leq\frac29+
  \sqrt{\left(\frac49-G_{11}\right)
        \left(\frac49-G_{22}\right)}.
  \]
- Substitution leaves the exact square
  \[
  \frac49(s_1^2+s_2^2+s_1s_2)-\|\Pi _2C\|_2^2
  \geq
  \left(
  s_1\sqrt{\frac49-G_{11}}-
  s_2\sqrt{\frac49-G_{22}}
  \right)^2.
  \]
  Thus the unproved invariant Hodge concurrence bound implies the new
  stronger pair theorem, not merely the old unshifted \(2/3\) theorem.
- The shifted determinant is also proved exactly when one diagonal
  rank-one slack vanishes through the already classified
  product-left or product-right saturation mechanism.  The established
  operator estimate on the projected dyad gives
  \(|G_{12}|\leq2/9\), which is the exact boundary value.
- The Hodge concurrence estimate itself remains unproved.
- Exact note and dependency-free checker:
  `notes/agent_n3_pair_shifted_concurrence_bridge.md` and
  `verification/verify_n3_pair_shifted_concurrence_bridge.py`.

## 2026-07-29 — Exact qutrit-GHZ no-go for a copositive Schur certificate

- Recast the fixed-anchor intersection-one theorem exactly as positivity
  of
  \[
  \Phi_w(V)=Q_3(P_w){\cal K}(V)-A_wVA_w.
  \]
  This suggested proving a stronger reflection certificate through the
  partially transposed Choi matrix \(J(\Phi_w)^\Gamma\).
- Disproved that strengthening exactly, already at the two-block level.
  For the normalized qutrit GHZ anchor and
  \[
  q=|000,000\rangle+|111,111\rangle,
  \qquad \operatorname{SR}(q)=2,
  \]
  direct rational calculation gives
  \[
  \langle q,J(\Phi_w)^\Gamma q\rangle=-\frac5{72}.
  \]
- This is only a no-go for complete-copositivity and
  two-block-copositivity proof routes.  It is not a violation of
  positivity of \(\Phi_w\), not a counterexample to the intersection-one
  inequality, and not a Werner witness.
- Exact note and dependency-free checker:
  `notes/agent_n3_intersection_cocopositive_obstruction.md` and
  `verification/verify_n3_intersection_cocopositive_obstruction.py`.

## 2026-07-29 13:51 PDT — Exact quantitative pair-frontier target, generic Hessian gaps, and quartic intersection

- Rewrote the strengthened balanced pair-sector theorem exactly in
  terms of the normalized rank-one slack
  \[
  \varepsilon=\frac49-d_1^2.
  \]
  Its remaining content is precisely
  \[
  (2d_2-d_1)^2\leq3\varepsilon.
  \]
  If \(d_2/d_1=1/2+t\), this is equivalently
  \[
  \varepsilon\geq\frac{16t^2}{27+36t^2}.
  \]
  This identifies the required rate and coefficient; qualitative
  convergence to the equality locus is insufficient.
- Derived the complete polynomial rank-one-slack Hessian and audited
  exact generic representatives of both classified equality
  components:

  - at a generic product--tangent point, the complex \(54\times54\)
    Hessian Gram has rank \(40\), nullity \(14\), and every nonzero
    eigenvalue is \(>1/2\);
  - at a generic common-factor point, it has rank \(41\), nullity
    \(13\), and every nonzero eigenvalue is \(>2\).

  The nullities equal the exact component dimensions, so both generic
  strata have genuine local quadratic normal error bounds.
- Found an exact obstruction to patching those Hessians uniformly.
  At the spectrally sharp intersection
  \[
  x_0=|000\rangle,\qquad y_0=|100\rangle,
  \]
  the Hessian nullity jumps to \(18\).  Along
  \[
  x(t)=|000\rangle+t|101\rangle,\qquad
  y(t)=|100\rangle+t|010\rangle,
  \]
  the exact homogeneous slack is
  \[
  \Delta(x(t),y(t))=4t^4,
  \]
  or \(4t^4/(1+t^2)^2\) after normalization.  Thus quartic
  compatibility at component intersections is essential.
- Proved a global compactness corollary for the original pair-sector
  theorem: there exists \(\varepsilon_0>0\) such that
  \(d_1^2\ge4/9-\varepsilon_0\) implies
  \(d_1^2+d_2^2<2/3\).  Indeed exact saturation forces
  \(D=(3/2)e^{i\theta}E\), and the complete equality classification
  gives \(d_2^2\le1/9\), so the top-two sum is at most \(5/9\).
- This is an exact qualitative exclusion, not an explicit numerical
  value of \(\varepsilon_0\), and does not prove the sharp stability
  inequality.
- Exact note and checker:
  `notes/agent_n3_pair_quantitative_stability_frontier.md`,
  `verification/verify_n3_pair_quantitative_stability_frontier.py`.

## 2026-07-29 13:56 PDT — Symmetric Hodge split and exact component obstruction

- Split the positive shifted-pair feature operator canonically as
  \[
  S=S_{(2)}+S_{(3)},\qquad
  S_{(2)}=\frac49\sum_{i<j}{\mathsf A}_i{\mathsf A}_j,\qquad
  S_{(3)}=\frac89{\mathsf A}_1{\mathsf A}_2{\mathsf A}_3,
  \]
  where \({\mathsf A}_i=(I-F_i)/2\).  Compression gives
  \(Q=Q_{(2)}+Q_{(3)}\), and homogeneous concurrence is subadditive.
  Hence
  \[
  {\cal C}(Q_{(2)})+{\cal C}(Q_{(3)})\le4/9
  \]
  is a smaller sufficient target for the shifted pair theorem.
- Verified exact sharpness: the code
  \(U=(000,001)\), \(V=(110,111)\) has concurrence \(2/9\) in each
  component.
- Disproved the tempting separate \(2/9\) component budgets by an
  exact physical code.  For
  \[
  \Phi=(00+11+22)/\sqrt3,\quad
  U=(-\Phi0,-\Phi2),\quad V=(\Phi2,-\Phi0),
  \]
  the exact component concurrences are
  \[
  {\cal C}(Q_{(3)})=8/27>2/9,\qquad {\cal C}(Q_{(2)})=0.
  \]
  Thus compensation between the two exterior degrees is essential.
- The same code gives two exact no-go certificates for naive
  triple-Hodge arguments:
  \[
  \sum_{pqr}|\det(U^{\mathsf T}
    (A_p\otimes A_q\otimes A_r)V)|=1/6>1/8,
  \]
  and an explicit triple-skew tensor with
  \(\|D\|_{\rm op}^2/\|D\|_2^2=1/6>1/8\).
- Upgraded the shifted-Gram theorem on the boundary: the complete
  rank-one equality classification gives \(s_2(\Pi_2E)\le2/9\), so
  the shifted determinant bound holds on every saturation orbit, not
  only the product-left/right strata.
- Exact note and checker:
  `notes/agent_n3_pair_feature_concurrence_split.md`,
  `verification/verify_n3_pair_feature_concurrence_split.py`.

## 2026-07-29 14:08 PDT — Cubic adapted-frame critical ceiling

- Audited equations (26), (45), and (48) of the full-support filter
  classification.  The proposed adapted-basis calculation is exact:
  it gives
  \[
  32w_1+97f+6w_3\le78,\qquad f\le78/97.
  \]
- Found that this is not the best prover-chosen adapted basis.  For a
  unit traceless Hermitian qutrit matrix \(F\), with
  \(q(F)=\operatorname{Tr}(F^3)\),
  \[
  r(F)^2\ge\frac12+\frac{|q(F)|}{\sqrt6}
  \ge\frac12+q(F)^2.
  \]
- For any distinguished unit direction \(n\), an exact Haar average
  over orthonormal bases of \(n^\perp\) proves that some completion
  satisfies
  \[
  \sum_{a=2}^8q(F_a)^2\ge\frac3{11}.
  \]
  The calculation uses the restricted cubic-tensor invariants
  \[
  \|T_{n^\perp}\|^2=\frac{14}{3}-q(n)^2,\qquad
  \|\operatorname{tr}T_{n^\perp}\|^2=\frac16-q(n)^2.
  \]
- Found a stronger explicit frame construction.  For every unit
  traceless Hermitian qutrit direction \(n\), the hyperplane
  \(n^\perp\) contains three Hilbert--Schmidt orthonormal matrices of
  spectrum \((2,-1,-1)/\sqrt6\).  Diagonalizing \(n\), choose a
  probability vector \(w\) with zero \(n\)-expectation and
  \(\sum w_k^2=5/9\); the three phase-orbit vectors
  \(z_j=(\sqrt{w_k}\omega^{jk})_k\) have pair overlaps squared \(1/3\),
  and their centered rank-one projectors give the required triple.
- Completing this triple to an adapted seven-frame gives the exact
  spectral-radius sum
  \[
  \sum_{a=2}^8r(F_a)^2\ge3(2/3)+4(1/2)=4.
  \]
  Consequently every hypothetical normalized full-support pair-sector
  critical point with \(f>2/3\) obeys
  \[
  16w_1+53f+3w_3\le42,
  \qquad
  f\le\frac{42}{53}=0.7924528301\ldots.
  \]
- This supersedes the intermediate cubic-Haar ceiling
  \(f<51/64\), while remaining short of the required \(f\le2/3\).
  No claim is made that the total adapted-frame spectral-radius
  constant \(4\) is optimal.
- Proved an exact no-go for every scalar improvement of this frame
  trace.  If \(K\) is any universal lower bound on the best
  seven-frame spectral-radius sum, the argument can give at most
  \[
  16w_1+(17+9K)f+3w_3\le18+6K,\qquad
  f\le\frac{18+6K}{17+9K}.
  \]
  The latter ceiling exceeds \(2/3\) by
  \(20/[3(17+9K)]\).  Since every frame vector has
  \(r(F)^2\le2/3\), even the impossible all-extremal ideal
  \(K=14/3\) yields only
  \[
  f\le46/59>2/3.
  \]
  Therefore the scalar, separately summed trace route is structurally
  incapable of closing the theorem; a continuation must retain
  matrix-valued common-frame or cross-site information.
- Exact note and checker:
  `notes/agent_n3_critical_filter_trace_bound.md`,
  `verification/verify_n3_critical_filter_trace_bound.py`.

## 2026-07-29 14:17 PDT — Four-string square-zero falsifier closed exactly

- Considered the direct nonnormal rank-two completion of a diagonal
  inertia-\((2,2)\) Hermitian quadrature on four distinct computational
  strings:
  \[
  H=\tfrac12(P_{p_0}+P_{p_1}-P_{n_0}-P_{n_1}),\qquad
  B_U=\tfrac12\begin{pmatrix}0&U\\U^\dagger&0\end{pmatrix},
  \quad U\in U(2).
  \]
  Then
  \[
  C_U=H+iB_U,\qquad C_U^2=0,\qquad \operatorname{rank}C_U=2.
  \]
- Proved the exact obstruction theorem
  \[
  Q_3(H)<0\quad\Longrightarrow\quad Q_3(C_U)\ge\frac14
  \]
  in arbitrary local dimensions.  The constant is sharp.
- The proof classifies the local equality patterns of the four strings.
  There are \(15\) set partitions per site and hence \(15^3\) cases.
  Exactly \(294\) cases have \(Q_3(H)<0\), falling into ten integral
  Gram types.  In every type the off-diagonal completion contributes
  enough endpoint energy to overcompensate the negative Hermitian
  quadrature.
- This does not prove unrestricted three-copy positivity.  It rules out
  a concrete exact falsifier mechanism; any negative nonnormal witness
  must use entangled quadrature eigenvectors or a more general
  unbalanced coupling.
- Exact note and integer-only checker:
  `notes/agent_n3_squarezero_string_completion.md`,
  `verification/verify_n3_squarezero_string_completion.py`.

## 2026-07-29 14:31 PDT — Phased unequal-weight string completions

- Strengthened the four-string square-zero obstruction to the
  fixed-pairing family
  \[
  C=c_0D_{\theta_0}(p_0,n_0)+c_1D_{\theta_1}(p_1,n_1),\qquad
  D_\theta(p,n)=\tfrac12
  |p+e^{i\theta}n\rangle\langle p-e^{i\theta}n|.
  \]
  For arbitrary complex weights and phases,
  \[
  C^2=0,\qquad\operatorname{rank}C\le2,\qquad Q_3(C)\ge0.
  \]
- The exact \(2\times2\) Gram determinant has only thirteen possible
  Laurent types over all \(15^3\) local equality patterns: nine positive
  constants and two phase-polynomial shapes, each with either
  \(w=z_0z_1\) or \(w=z_0/z_1\).  The latter reduce to
  \[
  64(1-x^2),\qquad16(1-x)(3+x),\qquad x=\operatorname{Re}w,
  \]
  and are nonnegative on \([-1,1]\).
- The integer-only checker now verifies the complete Laurent
  classification and multiplicities.  This closes unequal singular
  weights and arbitrary internal phases within the paired-product
  quadrature mechanism; it still does not cover entangled quadrature
  eigenvectors or arbitrary mixing between the two pairs.

## 2026-07-29 14:48 PDT — Balanced string completion is unconditional

- Removed the negative-quadrature hypothesis from the balanced-unitary
  four-string theorem:
  \[
  C_U=\tfrac12
  \begin{pmatrix}I&iU\\iU^\dagger&-I\end{pmatrix},
  \quad U\in U(2)
  \quad\Longrightarrow\quad
  C_U^2=0,\ \operatorname{rank}C_U=2,\ Q_3(C_U)\ge0.
  \]
  The earlier sharp \(Q_3(C_U)\ge1/4\) conclusion remains valid when
  the Hermitian quadrature itself has negative endpoint energy.
- For each local equality pattern, homogenizing the constant
  quadrature term with \(\|U\|_2^2=2\) produces an \(8\times8\) real
  integer matrix \(M\) satisfying
  \[
  32Q_3(C_U)=x^{\mathsf T}Mx,\qquad
  x=(\operatorname{Re}\operatorname{vec}U,
     \operatorname{Im}\operatorname{vec}U).
  \]
  The \(2707\) valid partition triples give \(228\) full Gram types
  and \(227\) distinct homogenized matrices.
  Every matrix is positive semidefinite by exact rational
  \(LDL^{\mathsf T}\) elimination.
- This completes all unitary mixing at equal weights for product-string
  quadrature eigenvectors.  Together with the phased unequal-weight
  fixed-pairing theorem, it substantially narrows the product-string
  square-zero falsifier, but does not address entangled quadrature
  eigenvectors.

## 2026-07-29 15:22 PDT — Crossed-energy Cauchy bridge is exactly false

- Tested the natural attempt to repair shifted Cauchy--Schwarz using
  only the four rank-one energies \(e_{ab}\):
  \[
  (e_{01}-m)(e_{10}-m)
  \stackrel?{\le}
  \left(m+\sqrt{(e_{00}-m)(e_{11}-m)}\right)^2,\qquad
  m=\frac18.
  \]
- Found an exact real qutrit counterfamily.  At its rational point
  \(t=1\),
  \[
  e_{00}=e_{11}=\frac{11}{32},\qquad
  e_{01}=e_{10}=\frac34,
  \]
  and the proposed right-minus-left defect is
  \[
  -\frac{279}{1024}.
  \]
- This is not a Werner witness: the true interference is only
  \(-1/32\), and the associated rank-two matrix has
  \(Q_3=5/8\).  For the full parameter family the false tradeoff defect
  factors as
  \[
  \frac{t^2(t^2-10)(3t^4+26t^2+2)}
       {64(1+t^2)^4},
  \]
  while the actual rank-two energy is
  \(t^2(t^2+4)/(2(1+t^2)^2)\ge0\).
- Therefore no proof can pass from ordinary shifted
  Cauchy--Schwarz to the matched bound using only the four diagonal
  rank-one energies.  The actual interference must remain coupled to
  the common Pluecker geometry.
- Exact note and dependency-free rational checker:
  `notes/agent_n3_crossed_energy_tradeoff_obstruction.md`,
  `verification/verify_n3_crossed_energy_tradeoff_obstruction.py`.

## 2026-07-29 14:31 PDT — Pointwise common-derivation filter inequality

- Replaced the exhausted scalar trace route by an exact pointwise
  coupling of the left and right residual maps.  For every local
  \(A\), with weighted centerings \(B_L,B_R\),
  \[
  \begin{aligned}
  &\|[A_i,D]\|_2^2-f|\ell(A)-r(A)|^2\\
  &\quad+2(f-\tfrac23)
    \bigl(r(B_L)^2+r(B_R)^2\bigr)\\
  &\le\frac43\bigl(
    {\cal N}_L(B_L,B_L)+{\cal N}_R(B_R,B_R)\bigr).
  \end{aligned}
  \]
  An exact SOS identity shows that its slack is the sum of the two
  filter slacks and
  \(\|T_{0,L}(A)+T_{0,R}(A)\|_2^2\).
- Proved the sharper square-root form obtained before the
  parallelogram relaxation.  On the common-centered hyperplane it
  specializes to
  \[
  \|[A_i,D]\|_2^2+4(f-\tfrac23)r(A)^2
  \le\frac43\operatorname{Tr}
  \bigl(A^\dagger A(\rho_i^L+\rho_i^R)\bigr).
  \]
- Computed the complete \(9\times9\) commutator Gram superoperator:
  \[
  {\mathscr C}_i^\dagger{\mathscr C}_i(A)
  =A R_L+R_RA-\Phi_D(A)-\Psi_D(A),
  \]
  and
  \[
  (T_{0,L}-T_{0,R})^\dagger(T_{0,L}-T_{0,R})
  ={\mathscr C}_i^\dagger{\mathscr C}_i
   -f|\rho_i^L-\rho_i^R\rangle\!\rangle
    \langle\!\langle\rho_i^L-\rho_i^R|.
  \]
- Recorded the exact Leibniz, same-site curvature, and cross-site
  integrability identities obeyed by the three derivations
  \(A\mapsto[A_i,D]\).  These are precisely the common-operator
  polynomial constraints omitted by the earlier norm-only formal
  six-map model.
- This is a new necessary matrix-valued restriction, not yet an
  exclusion of \(f>2/3\).
- Exact note and checker:
  `notes/agent_n3_common_derivation_filter_inequality.md`,
  `verification/verify_n3_common_derivation_filter_inequality.py`.

## 2026-07-29 14:37 PDT — Pair-Casimir obstruction to derivation-only closure

- Adversarially tested the new common-derivation inequalities and
  constructed an exact formal model showing that they are still
  insufficient.  Let
  \[
  D_*=\frac16(\Omega_{12}+\Omega_{13}+\Omega_{23}),
  \qquad
  \Omega_{ij}=\sum_{a=1}^8F_a^{(i)}F_a^{(j)}
  \]
  with the third site carrying the normalized scalar factor.  Then
  \(D_*\) is a physical Hermitian degree-two qutrit operator with
  \(\|D_*\|_2^2=2/3\).
- The exact qutrit adjoint-Casimir identity makes every local
  commutator Gram isotropic.  After scaling to norm squared \(f\),
  \[
  \langle[A_i,D_f],[B_i,D_f]\rangle
  =\frac f2\langle A_0,B_0\rangle.
  \]
  Thus all same-site and cross-site integrability relations come from
  one actual common \(D_f\).
- Added abstract common residual-sum isometries \(Z_i\), orthogonal to
  \(D_f\) and all commutator images, and set
  \[
  X_i=Z_i+\tfrac12[\cdot,D_f],\qquad
  Y_i=Z_i-\tfrac12[\cdot,D_f].
  \]
  With \(\|Z_i(B)\|^2=(5f/72)\|B\|^2\) and all six densities \(I/3\),
  every pointwise filter inequality holds for
  \[
  2/3\le f\le24/31.
  \]
  The sharp elementary input is
  \(r(B)^2\le(2/3)\|B\|_2^2\) for every complex traceless qutrit
  matrix.
- The formal sector distribution
  \((w_0,w_1,w_2,w_3)=(1-f,0,f,0)\) then satisfies exactly the
  common-origin Gram trace, residual norms, cross trace, and total
  covariance.  Hence even the full commutator Gram plus all
  derivation identities and pointwise filters leave formal negative
  critical data through \(f=24/31\).
- The model is not asserted to arise from rank-two \(C\).  It isolates
  the missing datum more sharply: the symmetric/anticommutator part
  \(T_i^L+T_i^R=\Pi_2(A_iC+CA_i)\) must come simultaneously from one
  common rank-two \(C\).
## 2026-07-29 16:05 PDT — Conjugation-correct common-plane floor reduction

- Derived the sufficient two-qubit matrix floor
  \[
  Q_{(2)}^\Gamma+
  \left(\frac29-\frac12\operatorname{Tr}Q_{(3)}\right)I_4
  \succeq0.
  \]
  It combines with the universal exact bound
  \(R^\Gamma+\tfrac12\operatorname{Tr}(R)I_4\succeq0\) for positive
  two-qubit \(R\), and therefore directly implies the shifted pair
  theorem.
- Corrected a crucial conjugation error in an earlier tentative
  projection formulation.  On
  \({\cal L}=\overline{\operatorname{ran}U}\otimes
  \overline{\operatorname{ran}V}\), the floor is losslessly equivalent
  to
  \[
  P_{\cal L}(P_0-P_1+4P_3)P_{\cal L}
  +\frac12(r_1-r_2+3r_3)I_{\cal L}\succeq0.
  \]
  Here \(P_k\) is the sector with exactly \(k\) local maximally
  entangled factors and \(r_k=\operatorname{Tr}(P_{\cal L}P_k)\).
- Proved this corrected floor exactly on the common-factor chart
  \(u_a=x\otimes e_a,\ v_a=y\otimes e_a\).  With
  \(\eta_i=\langle\bar x\otimes y|{\mathsf A}_i|
  \bar x\otimes y\rangle\), its least eigenvalue is
  \[
  \frac29(1-\eta_1-\eta_2)\ge0.
  \]
  The same chart obeys the stronger exact concurrence tradeoff
  \({\cal C}(Q_{(2)})+{\cal C}(Q_{(3)})\le4/9\).
- The reduction remains unproved for arbitrary complex singular
  planes.  Numerical attacks have approached equality without a
  violation; this is discovery evidence only.
- Exact note and checker:
  `notes/agent_n3_pair_common_plane_floor.md`,
  `verification/verify_n3_pair_common_plane_floor.py`.

## 2026-07-29 14:37 PDT — Sharp triple-skew stable-rank theorem

- Isolated the sharp surviving triple-Hodge target
  \[
  \left\|\sum_{p,q,r}t_{pqr}A_p\otimes A_q\otimes A_r
  \right\|_{\rm op}^2
  \le\frac16\sum_{p,q,r}|t_{pqr}|^2.
  \]
  This inequality is now proved exactly and is sharp.
- Proved the exact marginal identity
  \[
  8D_t^\dagger D_t
  =I-\rho_A-\rho_B-\rho_C+\rho_{AB}+\rho_{AC}+\rho_{BC}-\rho,
  \]
  and reduced the stable-rank statement equivalently to a cross-marginal
  purity inequality, a rank-two-code purity inequality, a decomposable
  Hodge--Pluecker inequality, and a four-party collision-purity monogamy
  inequality.
- Proved the collision-purity form using a new state-dependent qutrit
  sign frame.  For every traceless Hermitian \(X\in M_3\) and qutrit
  state \(\sigma\), constructed a Hermitian contraction \(G\) such that
  \[
  \operatorname{Tr}(XG)=\sqrt2\|X\|_2,\qquad
  \operatorname{Tr}(\sigma G^2)
  \le\frac23(1+\operatorname{Tr}\sigma^2).
  \]
  Applying these contractions to the three reduced encoded Pauli
  directions, anticommutation and the qutrit purity floor give
  \[
  \sum_{i,a>0}\|X_{a,i}\|_2^2
  \le\sum_i\|X_{0,i}\|_2^2+\frac13,
  \]
  exactly the required Hodge inequality.
- Identified the exact sharp equality orbit
  \(t=\Phi_{AB}\otimes|0\rangle_C\),
  \(x=\Phi_{AB}\otimes|2\rangle_C\).  It gives
  \(D_t=3^{-1/2}(\sum_pA_p\otimes A_p)\otimes A_0\) and
  \(\|D_t\|_{\rm op}^2=1/6\).
- Classified every nonzero equality case.  Equality in all six refined
  sign frames forces the encoded Pauli information onto one qutrit,
  makes the other two qutrit marginals maximally mixed, and then forces
  a Bell pair on the logical qubit and the active qutrit.  The
  complementary two-qutrit state is maximally entangled.  Hence the
  displayed biseparable orbit is the complete equality locus.
- Extracted an exact joint-compensation corollary.  If the logical
  triple-skew feature reaches its sharp maximum
  \({\cal C}(Q_{(3)})=8/27\), compression equality places both singular
  planes on the common-factor top spaces above.  The exact common-plane
  formulas then give
  \[
  {\cal C}(Q_{(2)})=0,\qquad
  {\cal C}(Q_{(2)}+Q_{(3)})=8/27,
  \]
  and the corrected common-plane floor has strict margin \(2/27\).
  Quantitative compensation away from this maximal locus remains open.
- Disproved the naive two-site induction mechanism exactly.  For the
  qutrit antisymmetric channel \({\cal W}\), the comparison map
  \((1/3)\operatorname{Tr}(\cdot)I-{\cal W}^{\otimes2}\) is not even
  two-positive: the sharp double-skew tensor has top-two squared
  singular-value mass \(5/12\), producing Choi expectation at most
  \(-1/12\).
- The stable-rank theorem gives only the sharp component
  bound \({\cal C}(Q_{(3)})\le8/27\), not the required coherent
  \(4/9\) theorem.  Compensation from the two-skew component remains
  essential.
- Exact note and checker:
  `notes/agent_n3_triple_skew_reduction.md`,
  `verification/verify_n3_triple_skew_reduction.py`.
## 2026-07-29 16:42 PDT — Paired-Pluecker exterior determinant

- Eliminated the remaining logical-vector optimization from the
  corrected common-plane floor.  For the Slater vector
  \(\Omega_{\cal L}\in\bigwedge^4{\cal K}\), let \(m_\nu\) be its
  mass with \(\nu_k\) factors in sector \({\cal K}_k\).  Then the
  sector traces and scalar shift are the first moments
  \[
  r_k=\sum_\nu\nu_km_\nu,\qquad
  s=\frac12\sum_\nu(\nu_1-\nu_2+3\nu_3)m_\nu,
  \]
  while the exact determinant of the scaled floor is
  \[
  \sum_\nu m_\nu(1+s)^{\nu_0}(s-1)^{\nu_1}
                 s^{\nu_2}(s+4)^{\nu_3}.
  \]
- Once the scalar trace bound \(s\ge0\) is proved, nonnegativity of
  this single determinant is sufficient for the full matrix floor.
  Strict block positivity handles \(s>0\); real-analytic continuity
  handles its boundary.
- Identified the exact remaining realizability input:
  \(\Omega_{\cal L}\) is the fixed \((2,2)\)-Young image of the two
  common decomposable bivectors \(\omega_U,\omega_V\).  Thus the
  remaining statement is a paired Segre--Pluecker inequality, not an
  inequality for arbitrary exterior occupation masses.
- Constructed an exact relaxed obstruction.  Three sector-zero
  directions and one sector-one maximally-entangled logical direction
  give a block-positive compression \(I-2P_{\Phi_2}\), shift \(s=1/2\),
  and floor spectrum \((-1/2,3/2,3/2,3/2)\).  Hence sector data,
  ordinary four-plane decomposability, and block positivity are still
  insufficient; the paired Pluecker relations are essential.
- Exact note and checker:
  `notes/agent_n3_pair_common_plane_exterior_determinant.md`,
  `verification/verify_n3_pair_common_plane_exterior_determinant.py`.

## 2026-07-29 17:05 PDT — Full reversed-Schur orientation reduction

- Returned from the pair-only frontier to the complete three-copy
  logical compression
  \(K=(U^\dagger\otimes V^\dagger)Y(U\otimes V)\).
  Writing
  \(K=\left(\begin{smallmatrix}A&B\\B^\dagger&D\end{smallmatrix}\right)\)
  in \(2\times2\) logical blocks and setting
  \[
  X=A^{-1/2}BD^{-1/2},\qquad
  Z=A^{-1/2}B^\dagger D^{-1/2},
  \]
  proved the exact determinant identity
  \[
  \frac{\det K^\Gamma}{\det A\det D}
  =
  \det(I-X^\dagger X)+\|X\|_2^2-\|Z\|_2^2.
  \]
- Since \(K\succ0\), \(X\) is a strict contraction.  Therefore full
  unrestricted three-copy positivity is exactly the scalar orientation
  inequality
  \[
  \|Z\|_2^2-\|X\|_2^2
  \le(1-s_1(X)^2)(1-s_2(X)^2).
  \]
  The right side is the ordinary positive-Gram Schur slack; the left
  side is the sole reversal defect.
- Identified automatic charts \(A\propto D\) and
  \(B=e^{i\theta}H\) with \(H=H^\dagger\), where the orientation defect
  vanishes.
- Gave an exact abstract obstruction
  \(K_*=\frac12I+|\Phi_2\rangle\langle\Phi_2|\): it is positive and its
  spectrum lies inside the physical filter interval, but its orientation
  defect is \(32/9\), its ordinary Schur slack is \(5/9\), and
  \(\det K_*^\Gamma=-27/16\).  Thus positivity, spectral bounds, and
  the ordinary Schur contraction alone cannot prove the endpoint; the
  common three-fold tensor origin must control the reversal.
- Exact note and dependency-free checker:
  `notes/agent_n3_full_reversed_schur_orientation.md`,
  `verification/verify_n3_full_reversed_schur_orientation.py`.

## 2026-07-29 17:40 PDT — Full logical transfer/Pluecker identity

- Identified the reversed-Schur orientation defect intrinsically.  If
  \(K(U,V)\) is regarded as the Choi matrix of the physical logical
  qubit map \(\Lambda_{U,V}\), with real Pauli transfer matrix \(T\),
  then
  \[
  \det K(U,V)^\Gamma=\det K(U,V)-\det T(\Lambda_{U,V}).
  \]
  Hence full unrestricted three-copy positivity is exactly
  \(\det T(\Lambda_{U,V})\le\det K(U,V)\) for all two code planes.
- Wrote the physical map without logical coordinates:
  \[
  \Lambda_{U,V}
  ={\cal E}_V^*\Psi_3^{\otimes3}{\cal E}_{\bar U},
  \qquad
  \Psi_3(R)=\operatorname{Tr}(R)I-\frac12R^{\mathsf T}.
  \]
  Its transfer determinant is the paired fourth-exterior contraction
  \[
  \det T(\Lambda_{U,V})
  =
  \langle\Omega_V,
  (\bigwedge^4\Psi_3^{\otimes3})\Omega_{\bar U}\rangle.
  \]
  In an eigenbasis this is an explicit weighted sum of paired fourth
  Pluecker coordinates of the two common code planes.
- The positive comparison term is the exact Gram volume
  \[
  \det K(U,V)
  =
  \left\|
  \bigwedge_{a,b=0}^1
  Y^{1/2}(u_a\otimes v_b)
  \right\|^2.
  \]
  Thus the remaining theorem is one lossless paired
  Segre--Pluecker inequality in the common left/right bivectors, with
  all scalar, one-body, and pair components retained.
- Exact note and checker:
  `notes/agent_n3_full_reversed_schur_orientation.md`,
  `verification/verify_n3_full_transfer_plucker.py`.
## 2026-07-29 17:26 PDT — Two-column Hodge recursion and factor-plane theorem

- Recast the scalar floor requirement
  \(\operatorname{Tr}Q_{(3)}\le4/9\) as the exact two-column spectral
  inequality
  \[
  \lambda_1(R_U)+\lambda_2(R_U)\le\frac12,\qquad
  R_U=\sum_{a=0}^1T_{u_a}^\dagger T_{u_a}.
  \]
- Exactly disproved the tempting separate bound
  \(\lambda_2(R_U)\le1/6\).  The canonical plane
  \(U=\operatorname{span}\{|000\rangle,|001\rangle\}\) has four
  eigenvalues \(1/4\).  The correct equality geometry includes both
  the balanced spectrum \((1/4,1/4)\) and the spiked spectrum
  \((1/3,1/6)\).
- Proved the sharp double-Hodge inequalities
  \[
  \mu_1(D_x^\dagger D_x)\le\frac13,\qquad
  \mu_1+\mu_2\le\frac12
  \]
  by reducing to the singular values of the two-qutrit coefficient
  matrix, a \(3\times3\) weighted triangle block, and three elementary
  \(2\times2\) blocks.
- As a consequence, proved
  \(\operatorname{Tr}Q_{(3)}\le4/9\) whenever one singular plane is
  \(x\otimes W\) with \(\dim W=2\), while the other plane is completely
  arbitrary.
- For a general plane sliced as
  \(u_a=\sum_rx_{ar}\otimes e_r\), derived the lossless common-Gram
  recursion
  \[
  R_U=\frac12(G\otimes I-H^{\Gamma_3}),\qquad
  H_{rs}=\sum_aD_{x_{ar}}^\dagger D_{x_{as}},\quad H\succeq0.
  \]
  The remaining scalar theorem is a Ky--Fan-two inequality for this
  structured partial-transpose difference.
- Exact note and checker:
  `notes/agent_n3_triple_hodge_two_column_recursion.md`,
  `verification/verify_n3_triple_hodge_two_column_recursion.py`.

## 2026-07-29 18:35 PDT — Full logical filtering and octahedral frontier

- Proved from first principles that every physical \(4\times4\)
  two-plane compression is locally filter-equivalent to the
  Bell-diagonal form
  \[
  K_{\boldsymbol t}=\frac14\left(
  I\otimes I+t_1X\otimes X+t_2Y\otimes Y+t_3Z\otimes Z
  \right).
  \]
  Strict positivity is automatic because the four product vectors
  \(u_a\otimes v_b\) are independent and the physical operator
  \(Y^{\otimes3}\) is invertible.
- Local filtering preserves both \(\det K^\Gamma\ge0\) and the common
  physical code-plane origin.  Positivity of \(K\) gives the four
  Bell inequalities with sign product \(-1\); the desired partial
  transpose positivity supplies the complementary four.  Together
  they are exactly
  \[
  |t_1|+|t_2|+|t_3|\le1.
  \]
- Equivalently, after filtering the physical logical Pauli transfer
  matrix has scalar marginals and block form
  \[
  T=\begin{pmatrix}s&0\\0&C_{\rm sp}\end{pmatrix},
  \]
  and the entire unrestricted three-copy endpoint is the single
  \(3\times3\) trace-norm inequality
  \[
  \|C_{\rm sp}\|_1\le s.
  \]
  This is an exact reduction, not yet a proof of the inequality.
- Exact note and dependency-free checker:
  `notes/agent_n3_full_reversed_schur_orientation.md`,
  `verification/verify_n3_full_lorentz_normal_form.py`.

## 2026-07-29 — High-principal-overlap scalar region

- Strengthened the sharp pointwise triple-skew estimate by retaining
  its exact kernel:
  \[
  \langle t\otimes x,{\mathsf A}_1{\mathsf A}_2{\mathsf A}_3
  (t\otimes x)\rangle
  \leq\frac16\left(1-|\langle t,x\rangle|^2\right).
  \]
- Summing over two orthonormal frames \(U,V\) gives the global
  principal-angle bound
  \[
  r_3(U,V)\leq
  \frac{4-\operatorname{Tr}(P_UP_V)}6.
  \]
  Hence the scalar corrected-floor requirement
  \(\operatorname{Tr}Q_{(3)}\leq4/9\) holds whenever
  \(\operatorname{Tr}(P_UP_V)\geq1\), with exact margin
  \[
  \frac49-\operatorname{Tr}Q_{(3)}
  \geq\frac4{27}\bigl(\operatorname{Tr}(P_UP_V)-1\bigr).
  \]
  Any failure of this scalar route is therefore confined to two
  singular planes whose squared principal-angle cosines sum to less
  than one.
- Exact note and checker:
  `notes/agent_n3_high_principal_overlap_scalar.md`,
  `verification/verify_n3_high_principal_overlap_scalar.py`.

## 2026-07-29 — Adversarial correction to the split-budget record

- Corrected an overstatement in
  `notes/agent_n3_pair_feature_concurrence_split.md`.  The exact
  common-factor countercode proves
  \({\cal C}(Q_{(3)})=8/27>2/9\), but it has
  \({\cal C}(Q_{(2)})=0\).  It therefore disproves only the proposed
  standalone triple-skew budget, not the standalone two-skew bound.
- The status of
  \[
  {\cal C}(Q_{(2)})\leq\frac29
  \]
  is now recorded correctly as conjectural: neither proved nor
  disproved.  This distinction matters because that bound, combined
  with a global version of the quantitative triple-skew compensation,
  would directly imply the sufficient split target.

## 2026-07-29 15:11 PDT — Exact triple-skew deficit and chart compensation

- Refined the sharp triple-skew theorem to the lossless stable-rank
  deficit identity
  \[
  \frac16-\|D_tx\|^2
  =\frac1{32}\sum_{\pi\in S_3}(R-s_\pi).
  \]
  Each frame gap \(R-s_\pi\) now has an explicit sum of nonnegative
  global-purity, local qutrit-frame, and variance gaps.  This gives a
  compactness-free quantitative form of the equality classification.
- Split the logical AAA concurrence deficit exactly into three
  nonnegative pieces: Hodge stable-rank deficit, compression-plane
  misalignment, and residual Takagi mass.
- On the entire common-factor singular-plane chart, proved the
  quantitative corrected-floor compensation
  \[
  m\geq
  \max\{0,\mathcal C(Q_{(3)})-2/9\}.
  \]
  It interpolates sharply from the zero-floor threshold to the
  maximal-AAA equality orbit, where \(m=2/27\).
- Combined the complete equality classification with compactness to
  prove an exact strict high-AAA exclusion band: there exists
  \(\delta>0\) such that
  \[
  \mathcal C(Q_{(3)})>8/27-\delta
  \quad\Longrightarrow\quad
  \mathcal C(Q_{(2)}+Q_{(3)})<4/9.
  \]
  This removes a whole neighborhood of the maximal orbit from the
  unresolved joint problem, although the present proof does not give
  an explicit numerical value of \(\delta\).
- This does not yet extend the joint bound to arbitrary pairs of
  singular planes.  The remaining problem is to convert the invariant
  stable-rank deficit into a common-plane or reversed-Schur margin.
- Proof and exact checker:
  `notes/agent_n3_triple_skew_reduction.md`,
  `verification/verify_n3_triple_skew_reduction.py`.
## 2026-07-29 17:44 PDT — Paired compression identity

- Added the exact alternating-contraction identity
  \[
  P_UR_UP_U=p_UI_U,\qquad
  p_U=\|T_{u_0}u_1\|^2\le1/6.
  \]
- The balanced and spiked scalar-equality spectra lie on the common
  affine line
  \[
  (1/4+p_U/2,\ 1/4-p_U/2).
  \]
  This exposes the precise conjectural strengthening whose two
  inequalities would imply the Ky--Fan-two target.  It is currently
  supported only by discovery searches away from the two exact
  endpoint families.

## 2026-07-29 15:26 PDT — Exact obstructions to separate-column Hodge bounds

- Disproved the second proposed affine spectral bound
  \[
  \lambda_2(R_U)\leq\frac14-\frac12p_U
  \]
  exactly.  For
  \(U=(|00\rangle+|11\rangle)/\sqrt2\otimes
  \operatorname{span}\{|0\rangle,|1\rangle\}\), one has
  \(p_U=1/8\) and \(\lambda_2(R_U)=1/4\), a gap of \(1/16\).
  The actual Ky--Fan-two sum is still exactly \(1/2\).
- Disproved the tempting separate-column operator-norm estimate
  \[
  \|D_{u_0}\|_{\rm op}^2+\|D_{u_1}\|_{\rm op}^2
  \leq\frac14+\frac12p_U.
  \]
  Two orthogonal maximally entangled \(AB\) states with a common
  one-site factor have \(p_U=0\), while both column norms equal
  \(1/6\), giving an exact violation of \(1/12\).
- These obstructions isolate the indispensable remaining datum:
  the two Hodge columns must be tested on one common maximizing
  two-plane.  Separate column maxima lose precisely that
  compatibility.
- Updated the dependency-free exact checker
  `verification/verify_n3_triple_hodge_two_column_recursion.py`.

## 2026-07-29 20:10 PDT — Simultaneous critical Bell reduction

- Translated the scalar logical-marginal equations into exact
  cancellations among one physical rank-two matrix and its three
  Pauli companions.  After spatial alignment the four matrices are
  pairwise orthogonal for the full alternating partial-trace form and
  share the product of their two nonzero singular values.
- Proved that any negative witness would yield a negative global
  minimizer under the normalization \(s_1(C)s_2(C)=1\).  This slice
  is coercive, and its exact Euler--Lagrange equations are
  \[
  L^{\otimes3}(C)V=\lambda U\Sigma^{-1},\qquad
  L^{\otimes3}(C)^\dagger U=\lambda V\Sigma^{-1},
  \quad \lambda=Q_3(C)/2<0.
  \]
- Proved that the same physical critical matrix can be put into the
  balanced Bell form without changing it.  Its projected critical
  equation makes the logical Pauli transfer matrix symmetric.  A
  determinant-one linked filter, obtained by minimizing
  \(\operatorname{Tr}(P\Lambda(P))\), makes both marginals scalar;
  its action on \(K^\Gamma\) is \(H\otimes H\), which fixes the
  logical singlet exactly.
- Gave an exact computational-basis balanced example whose two
  singular values have ratio \(\sqrt2\).  Thus balance alone does not
  imply equal singular values or the ordinary Frobenius critical
  equations.
- Exact note and checkers:
  `notes/agent_n3_balanced_companion_stationarity.md`,
  `verification/verify_n3_balanced_companion_obstruction.py`, and
  `verification/verify_n3_full_lorentz_normal_form.py`.

## 2026-07-29 15:48 PDT — Explicit quantitative high-AAA exclusion

- Made the qualitative maximal-AAA neighborhood fully explicit:
  \[
  {\cal C}(Q_{(3)})>\frac8{27}-10^{-120}
  \quad\Longrightarrow\quad
  {\cal C}(Q_{(2)}+Q_{(3)})<\frac49.
  \]
  The constant is deliberately conservative but exact.
- Used the lossless stable-frame deficits to prove quantitative
  signal concentration on one physical qutrit.  If
  \(h=1/6-\|D_t\|_{\rm op}^2\), the associated four-party
  purification lies within \(23h^{1/8}\) of the classified
  Bell-pair times maximally-entangled-qutrit orbit.
- Combined the compression-determinant deficit with the exact
  equality singular-value gap to pin both logical planes:
  their squared leakage from the equality planes is less than
  \(340\varepsilon^{1/8}\).
- A self-contained square-root perturbation estimate then bounds the
  two-skew concurrence by the available \(4/27\) margin.  This proves
  a genuine non-chart neighborhood, rather than assuming exact
  common-factor form.
- The estimate is not invariant under arbitrarily ill-conditioned
  logical Lorentz filters, so transfer to a uniform balanced-scalar
  neighborhood remains open.
- Nevertheless it gives an exact plane-invariant Lorentz consequence:
  every hypothetical negative critical Bell representative, after
  re-orthonormalizing its unchanged two physical planes, must satisfy
  \[
  {\cal C}(Q_{(3)})\leq8/27-10^{-120}.
  \]
  Hence the same high-AAA plane region is excluded from the balanced
  frontier even though no direct margin in the filtered transfer
  entries has yet been obtained.
- Proof and exact constant checker:
  `notes/agent_n3_quantitative_high_aaa.md`,
  `verification/verify_n3_quantitative_high_aaa.py`.

## 2026-07-29 15:53 PDT — Complete determinant-critical Hessian

- Starting from the simultaneous critical Bell representative, derived
  the full second variation on the determinant-normalized rank-two
  manifold, including arbitrary motion of both physical singular
  planes.  If
  \[
  L^{\otimes3}(C)=\lambda U\Sigma^{-1}V^\dagger+R,
  \qquad \lambda=Q_3(C)/2<0,
  \]
  then the constrained Hessian is the ambient quadratic form plus the
  exact determinant correction, the two Stiefel curvature terms, and
  the second-fundamental-form pairing with the normal residual \(R\).
- Solved the full determinant-one problem inside the fixed logical
  pencil.  Singlet minimality there is equivalent to
  \(\lambda_j+\lambda_0\geq0\); these are exactly the strict physical
  rank-one tests already implied by the positive logical Gram, so the
  fixed pencil contains no additional obstruction.
- The first genuinely physical frame condition comes from simultaneous
  left/right leakage.  For every pair of leakage velocities, the exact
  Hessian condition is
  \[
  a,b\geq0,\qquad (|p|+|q|)^2\leq ab,
  \]
  where \(p\) is the ordinary crossed response and \(q\) is the normal
  residual paired with the second fundamental form.  The two responses
  consume one common budget and cannot be bounded independently.
- The first-order critical equations also force reciprocal rank-one
  energies, \(b=r^4a\), the compact restriction \(1\leq r^4\leq27\),
  and a strict reverse-Cauchy defect at every hypothetical negative
  critical point.
- Exact derivation and dependency-free audit:
  `notes/agent_n3_determinant_critical_hessian.md` and
  `verification/verify_n3_determinant_critical_hessian.py`.

## 2026-07-29 16:06 PDT — Reverse-Cauchy/leakage bridge isolated

- Proved that the singular-component reverse-Cauchy defect cannot be
  recovered from the determinant-critical Hessian alone.  The exact
  abstract form
  \[
  {\cal Q}(D)=\|D\|_2^2-\frac34|\operatorname{Tr}(PD)|^2
  \]
  has a strict rank-one floor and a negative global minimizer \(P\)
  on the rank-two slice \(s_1s_2=1\).
- At this minimizer, \(a=b=1/4\) and \(c=-3/4\), so
  \(|c|^2-ab=1/2\), while the normal residual vanishes and every
  paired leakage has \(p=q=0\).  Hence no abstract identity or bound
  \(|c|\leq|p|+|q|\) follows from block positivity, criticality, or
  the complete second variation.
- Isolated a smallest sufficient physical bridge.  It would suffice
  to produce physical leakage directions \(X,Z\) satisfying
  \[
  \frac{|p|+|q|}{\sqrt{A_XB_Z}}
  \geq\frac{|c|}{\sqrt{a_0b_0}}.
  \]
  Criticality makes the right side strictly larger than one, while
  the Hessian makes the left side at most one.  Any proof of this
  bridge must use the explicit three-fold partial-trace structure.
- Exact note and audit:
  `notes/agent_n3_reverse_cauchy_leakage_obstruction.md` and
  `verification/verify_n3_reverse_cauchy_leakage_obstruction.py`.

## 2026-07-29 16:10 PDT — Independent complex Hessian audit and Hodge obstruction

- Re-derived the complete determinant-critical Hessian in a
  nonisometric graph chart.  This independently confirms the factor
  two in the normal-curvature term, its holomorphic
  \(\alpha\beta\) phase law, the sesquilinear
  \(\overline\alpha\beta\) law of the ordinary crossed response, and
  the Bell-companion Schur denominators.
- Constructed an exact strictly positive bipartite parent
  \[
  Y=P+3|\Phi\rangle\langle\Phi|+2(I-P)\succ0
  \]
  whose partial transpose has a negative determinant-critical
  singlet and a positive-semidefinite complete rank-two Hessian.
  Hence positivity before partial transpose, strict rank-one
  positivity, and the full critical Hessian still do not contradict a
  negative value without the special threefold qutrit contraction
  identities.
- Specialized the coupled leakage Hessian to the canonical qutrit
  triple-Hodge normals
  \[
  h_U=\overline{D_{u_1}u_2},\qquad
  h_V=\overline{D_{v_1}v_2},
  \]
  obtaining the exact two-direction test
  \((|P_k|+|T_k|)^2\leq A_kB_k\).
- Found an exact limitation of that test.  The full-local-support
  plane
  \[
  u_0=(|000\rangle+|111\rangle+|222\rangle)/\sqrt3,\qquad
  u_1=(|012\rangle+|120\rangle+|201\rangle)/\sqrt3
  \]
  has \(D_{u_0}u_1=0\).  Thus a complete Hodge leakage bridge must
  couple the one-, two-, and three-skew sectors; the triple-skew
  normal alone can be identically absent.
- Exact note and independent complex checker:
  `notes/agent_n3_critical_hessian_hostile_audit.md` and
  `verification/verify_n3_critical_hessian_hostile_audit.py`.

## 2026-07-29 16:18 PDT — Standalone coherent two-skew bound disproved

- First reduced the proposed logical inequality
  \[
  {\cal C}(Q_{(2)})\leq\frac29
  \]
  losslessly to the rank-two exterior inequality
  \[
  {\cal J}(C)+\frac12s_1(C)s_2(C)\geq0,
  \]
  where
  \[
  4{\cal J}(C)=
  3\|C\|_2^2
  -2\sum_i\|\operatorname{Tr}_iC\|_2^2
  \sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2.
  \]
- Disproved this intermediate inequality with an exact
  Gaussian-integer rank-two matrix \(C=XY^\dagger\).  Its certificate
  is
  \[
  4{\cal J}(C)=-15662399,\qquad
  (s_1s_2)^2=50588196320972,
  \]
  together with the radical-free comparison
  \[
  15662399^2-4(50588196320972)
  =42957957151313>0.
  \]
  Hence \({\cal J}(C)+s_1s_2/2<0\) exactly.
- This is not a three-copy Werner counterexample.  The same exact
  contraction gives
  \[
  \operatorname{Tr}C=-6525+6981i,\qquad
  8Q_3(C)=617243800,
  \]
  so \(Q_3(C)=77155475>0\).  The result rules out proving the
  endpoint by imposing independent \(2/9\) budgets on the two- and
  three-skew features.
- Exact note and dependency-free checker:
  `notes/agent_n3_q2_concurrence_exterior_reduction.md` and
  `verification/verify_n3_q2_concurrence_exterior_reduction.py`.

## 2026-07-29 16:06 PDT — Small counterpencil and exact coupled repair

- Compressed the dense coherent-two-skew counterexample to the binary
  corner \((\mathbb C^2)^{\otimes3}\), with a one-real-parameter
  Gaussian-integer pencil
  \[
  C_t=xy^\dagger+tze_{000}^\dagger
  \]
  whose coefficients have modulus at most \(3\sqrt {10}\).
- Its exact contractions are
  \[
  \begin{aligned}
  4{\cal J}_2(C_t)&=20t^2-1980t+141,\\
  8{\cal J}_3(C_t)&=4t^2-708t+5,\\
  s_1(C_t)s_2(C_t)&=|t|\sqrt{806080}.
  \end{aligned}
  \]
  At \(t=1\), the radical-free gap
  \(1819^2-4(806080)=84441>0\) proves
  \({\cal J}_2+s_1s_2/2<0\).
- The omitted triple-skew sector repairs this entire pencil exactly:
  \[
  4({\cal J}_2+2{\cal J}_3+s_1s_2)
  =24t^2-2688t+146+4|t|\sqrt{806080}>0
  \]
  for every real \(t\).  The original endpoint form also has the
  completed-square certificate
  \[
  8Q_3(C_t)
  =66\left(t-\frac{815}{33}\right)^2+\frac{2880700}{33}>0.
  \]
- Exact note and dependency-free checker:
  `notes/agent_n3_q2_small_qubit_counterfamily.md` and
  `verification/verify_n3_q2_small_qubit_counterfamily.py`.
