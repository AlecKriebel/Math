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
