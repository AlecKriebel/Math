# Research log

## 2026-07-28 21:34 PDT — Program initialized

- Created a dedicated research directory on the repository's `main` branch.
- Recorded the exact matrix-class question and separated it from standardness
  and faithful-localization variants.
- Established independent proof, arithmetic, and \(d=6\) falsifier tracks.
- Recorded hardware and core dependency versions before the first new
  experiment.
- Noted that unrelated staged, modified, and untracked files already exist in
  the shared worktree.  This project will stage and commit only paths under
  `exceptional_ybe_spectrum/`.
- Initial logical observation to audit: the abstract relation for two
  projections appears to force principal-angle square \(1/3\) on every
  nontrivial two-dimensional block, but this has not yet been promoted to a
  proved claim.

## 2026-07-28 21:37 PDT — Gate 1 matrix reproduction passed

- Reran the published verifier suite from its checked source on the recorded
  environment.
- Three independent exact routes passed: dependency-free sparse matrices,
  abstract tensor-word algebra, and the preserved SymPy verifier.
- Reproduced Hermiticity, involutivity, zero trace, both cubic formulations,
  projection rank, unitarity, Hecke polynomial, both scalar partial traces,
  and the sitewise-swap \((3,2)\)-generalized factorization.
- Source hashes agree with the published release manifest.
- This upgrades only the concrete \(d=4\) witness.  It gives no permission to
  import Pauli, Clifford, scalar-partial-trace, or generalized-factorization
  assumptions into the arbitrary-\(d\) problem.

## 2026-07-28 21:44 PDT — Standardness and all-level arithmetic resolved

- Proved the complete abstract two-projection normal form.  The only
  nontrivial principal-angle blocks have squared cosine \(1/3\).
- Audited Lechner's Propositions 2.3--2.4 and Lemma 3.1.  Because the
  exceptional spectrum has no opposite eigenvalue pair, every arbitrary
  solution is automatically Markov and has
  \(\operatorname{Tr}_1P=\operatorname{Tr}_2P=(d/2)I\).
- Derived the exact three-strand multiplicities
  \(d^3/8,d^3/8,3d^3/8\).  Dimension six passes with \(27,27,81\).
- Proved that every solution automatically gives a faithful representation
  of the trace quotient \(H_n(3,6)\).
- Computed the general simple-block multiplicity formula
  \(m_{\lambda,n}=D_\lambda(d/2)^n\), with
  \(D_\lambda\in\{1,2,3\}\).
- Replayed three independent exact implementations.  The entire tower,
  not merely low levels, imposes only evenness.  Therefore any
  divisibility-by-four obstruction must be a strict tensor-local/coherence
  obstruction; central ranks and branching arithmetic cannot supply it.

## 2026-07-28 22:04 PDT — First exact \(d=6\) ansatz exhausted

- Reduced the standard cyclic Gaussian functional ansatz to 20 spectral
  sign assignments.
- Exhausted all cases in exact twisted-group-algebra arithmetic.
- No candidate survives.  The alternating cases leave an explicit
  coefficient of magnitude \(2/3\).
- This is recorded only as an ansatz-level no-go and is not evidence for
  global nonexistence.

## 2026-07-28 23:10 PDT — Construction and falsifier checkpoint

- Completed calibrated unrestricted, symmetry-reduced, and heterogeneous
  \(d=6\) searches.  No numerical candidate was found; failures remain
  explicitly non-probative.
- Identified the recurring heterogeneous residual \(\sqrt{12}\) as an
  involutive braid stratum, not a near-solution.
- Proved an exact heterogeneous blocking lemma reducing spectator-form
  \(d=6\) construction to a \(12\times12\) shifted problem.
- Proved exact no-go results for scalar-cross gluing, controlled middle
  colors, graph-phase/product-flip qutrit extensions, diagonal \(SU(2)\),
  central \(S_4\), Clifford/qutrit substitutions, ice-rule operators, and
  all monomial Hecke operators.
- Proved that one-sided tensor-tower coherence exists for every even
  dimension and audited away unsupported Frobenius--Schur, Brauer, and
  quaternionic parity arguments.
- Computed the exact asymmetric leg-commutant signature of the published
  solution.  It explains the known \(4m\) stabilization family but is not
  universal.
- An independent checkpoint audit replayed all exact certificates and
  numerical summaries.  It found no mathematical defect at the stated
  scopes and repaired candidate-file overwrite behavior.  The audit also
  disclosed that early exploratory numerical logs predate the final
  source-logging schema, so they are not byte-for-byte source-replayable.

## 2026-07-28 23:25 PDT — Color/face reduction

- Extracted two commuting \(2+2\) canonical-channel fixed decompositions
  from the independently discovered numerical \(d=4\) point.
- Derived exact reduced cubic systems for equal-sector mixed colors and for
  crossed operator-valued face blocks.
- Found and symbolically proved an exact one-parameter \(d=4\) family
  \(s^2+2t^2=1\), validating the reduction independently of the numerical
  point.
- Completed 39 reproducible \(d=6\) runs in the two face models.  No
  residual approached zero; the best was \(4.958747221723511\).  This is
  retained as numerical falsifier evidence only.

## 2026-07-28 22:42 PDT — Exact rank-one face no-go

- Calibrated a separate rank-one controlled-reflection search at \(d=4\)
  and completed four \(d=6\) production runs. No numerical candidate was
  found.
- Replaced that numerical evidence with a human proof covering the entire
  continuous ansatz at \(d=6\).
- The compressed cubic relation forces the six Bloch vectors to span
  \(\mathbb R^3\), forces the control basis to be maximally entangled, and
  then forces every off-diagonal Bloch inner product to equal \(-1/3\).
  The resulting six-vector Gram matrix has eigenvalue \(-2/3\), a
  contradiction.
- An exact companion verifier checks the cubic normalization, all
  compression signs, channel-leg orientation, Pauli algebra, and Gram
  spectra.
- The remaining predeclared numerical seeds were cancelled because the
  exact theorem supersedes them. This is an ansatz-level no-go, not a
  theorem for arbitrary \(d=6\) matrices.

## 2026-07-28 23:25 PDT — Noncontrolled branch isolated

- Proved the invariant controlled-leg divisibility theorem: every rank-\(r\)
  projection in either one-leg commutant forces \(8\mid rd^2\), with
  restricted common-one and common-zero multiplicities \(rd^2/8\).
- Consequently, a hypothetical \(d\equiv2\pmod4\) solution has no odd-rank
  leg-commutant projection. This exactly excludes every directly controlled
  solution, every leg-commutant MASA, and the full diagonal-regular
  group-relative ansatz.
- Independently excluded the complete cyclic \(C_6\) group-relative ansatz
  by dual Fourier support arithmetic and exactified the \(V_4\) calibration
  as a skew-conference construction.
- Completed an exact low-Schmidt three-color no-go and retained the
  two-color \(d=4\) family as calibration.
- Reconstructed the Evans--Pugh \(D^{(6)}\) connection from its published
  cells in two independent exact implementations. It is an exceptional
  \(20\times20\) path-space operator, not an ordinary \(36\times36\)
  local matrix; the obvious zero and scalar completions fail.
- Derived canonical completely positive channels for arbitrary solutions
  and built an exact \(d=6\) Weyl countermodel satisfying every currently
  isolated channel-level constraint. Thus channel spectral arithmetic
  cannot prove \(4\mid d\) by itself.
- Identity-pairing the Weyl Schmidt directions unexpectedly produced an
  exact Hermitian traceless cubic solution \(H_0\), but its eigenvalue
  multiplicities are \(9\) and \(27\) and it is not an involution. Its
  affine involution has trace \(18\), so no \(d=6\) witness has yet been
  obtained.
- The unresolved problem is now sharply localized: construct or exclude a
  genuinely noncontrolled shared involutive realization whose two
  one-leg commutants contain only even-rank projections.

## 2026-07-28 23:56 PDT — Full-color and endpoint arithmetic audited

- Rewrote the Weyl channel countermodel as the exact cubic point
  \[
  H_0=(YY\otimes I_9+(XX+ZZ)\otimes F_3)/\sqrt3.
  \]
  Its wrong quadratic stratum is now certified without dense matrices.
- Proved that no diagonally \(U(m)\)-equivariant exceptional solution exists
  on \(\mathbb C^2\otimes\mathbb C^m\) for odd \(m\). The only unbalanced
  \(m=3\) possibility is killed by the basis-free determinant gap
  \(1/16<1/9\).
- Exactly excluded all Weyl Schmidt pairings preserving or interchanging
  the two nine-dimensional color blocks. General block-mixing deformations
  remain numerical.
- Exhausted all one-leg \(C^*\)-algebra types compatible with the
  odd-leg-projection theorem at \(d=6\). Every one-sided and two-ended
  central multiplicity equation has an explicit nonnegative integral
  product solution; all \(25\) endpoint pairs pass.
- Audited Conti--Lechner's distinction between algebraic fixed points and
  von Neumann ergodicity. Exceptional solutions with \(d>2\) are
  nonergodic, but that fact alone does not force a finite-level or one-site
  fixed projection.
- Observed that the complete crossed-factor face ansatz is already excluded
  exactly by the rank-three leg projection on one side. The genuinely
  surviving controlled \(d=6\) face branch has rank-two atoms on both
  sides.
- No complete spectrum theorem or \(d=6\) witness has yet been obtained.

## 2026-07-29 00:04 PDT — Four-site intersection law proved

- For arbitrary exceptional \(P\), proved by a faithful-trace
  zero-variance argument that the shifted common-one projections satisfy
  \(e_{123}e_{234}e_{123}=e_{123}/4\). Common-zero projections satisfy the
  same relation, and opposite signs are orthogonal.
- Derived all forced outer and one-site marginals of the common projections.
  The middle two-site marginal is positive with maximally mixed one-site
  marginals but need not be scalar.
- Audited determinant, Clifford, QCA-index, Frobenius--Schur, and marginal
  purity routes. The exact block count is \(d^4/8\) and still forces only
  evenness.
- Built an exact \(d=6\) GHZ-times-\(\mathbb C^3\) limitation model
  satisfying the entire derived marginal/angle package while failing the
  original cubic/full-intersection condition.
- Independently replayed the universal scalar certificate, the dense exact
  \(d=4\) witness over \(\mathbb Q(\sqrt2,\sqrt3)\), and the \(d=6\)
  limitation model. All checks passed.

## 2026-07-29 00:15 PDT — Standard tensor-product route closed

- Re-audited the dimension-changing operation in Lechner's classification
  from the source PDF, including a visual check of pages 15--16.
- Proved that the multiplicative stabilizer of
  \(\{-1,e^{i\pi/3}\}\) is trivial. Hence a tensor product remains in the
  exceptional class only when its second factor is an identity spectator.
- This rigorously explains why the published construction yields dimensions
  \(4m\) but supplies no route to \(d=6\). Non-product gluing remains open.

## 2026-07-29 00:35 PDT — Odd factor leg excluded; rank-two audit corrected

- Proved for every \(d=2m\) with \(m\) odd that neither one-leg commutant
  can contain \(M_m(\mathbb C)\otimes I_2\). Automatic standardness and
  involutivity turn such a factor into rank-one control on the opposite
  leg, contradicting the controlled-leg divisibility theorem.
- Independently replayed the Pauli coefficient separation, factor-form
  guard, opposite rank-one controls, and the \(8\nmid36\) contradiction.
- Exhausted the integer bookkeeping for the remaining \(d=6\) branch with
  three rank-two central atoms. The nine cell ranks and nine endpoint
  intersection ranks are not forced to be uniform: 217 and 1540 labelled
  tables survive, respectively.
- Proved the stronger fact that left/right three-color decompositions
  cannot share even one rank-two atom. The shared cell reduces to the
  empty base-\(2\) problem or the rank-one determinant gap; scalar
  propagation across its row then contradicts automatic standardness.
  Any surviving three-color branch must therefore be genuinely transverse.
- Broadened the all-rank-two numerical falsifier to arbitrary relative
  \(U(6)\) position. Four reproducible runs found no candidate, but this
  is neither a proof within that subansatz nor a test of the nonuniform
  rank branches.
- Audited Bytsko's \(Q=\sqrt3\) characteristic-matrix and
  antisymmetrizer formulations. Their exact multiplicities are
  \(d^3/8\) and \(3d^3/8\), so they recover the existing evenness
  obstruction but contain no additional parity condition.

## 2026-07-29 01:03 PDT — Every three-color rank orbit sampled

- Extended the full-relative-\(U(6)\) falsifier from uniform
  signature-\((2,2)\) cells to the nine canonical cell-rank patterns
  representing all \(217\) standardness-compatible rank tables.
- Predeclared one seed and 800 iterations per orbit before running them.
  An accidental system-Python pilot was interrupted and retained
  separately; the declared runs were restarted from the same seeds under
  the project virtual environment.
- Verified the combined block and relative-unitary gradient against an
  independently assembled directional derivative with relative error
  \(7.013199327717132\times10^{-9}\).
- None of the nine runs approached a witness.  The smallest final cubic
  residual was \(6.000000000000004\), in orbit \(7\).
- Status remains NUMERICAL_EVIDENCE.  This closes a discrete coverage gap
  in the falsifier but is not an exhaustive optimization certificate and
  does not change the unresolved spectrum.

## 2026-07-29 01:12 PDT — The two leg commutants have scalar intersection

- Strengthened the shared-color-atom argument to a basis-free theorem:
  every hypothetical \(d=6\) solution has
  \(\mathcal C_L(P)\cap\mathcal C_R(P)=\mathbb C I_6\).
- The controlled-leg theorem makes every common projection even-rank.
  In six dimensions it therefore yields a rank-two projection after
  complementation.  Its \(2\times2\) cubic cell is scalar; the cubic
  propagates this scalar to a full row and contradicts automatic
  standardness.
- This excludes aligned and tensor-flip-symmetric versions of both
  surviving two-block algebra types.
- Independently checked the proof and exact verifier.  Exact permutation
  and abstract-cubic countermodels show that arbitrary transverse
  one-sided block types still survive the present invariants.

## 2026-07-29 01:25 PDT — Common reductions become an induction principle

- Generalized the \(d=6\) common-leg proof to arbitrary dimension without
  assuming that the diagonal compression is balanced.
- Proved that the two diagonal normalized ranks can only be
  \((1/2,1/2)\), or \((1/3,1/3)\) at equal complementary dimensions, or
  \((2/3,2/3)\) at equal complementary dimensions.
- In a \(d\equiv2\pmod4\) ambient solution, the controlled-leg
  divisibility theorem makes every common projection even-rank, whereas
  the unbalanced alternatives require rank \(d/2\), which is odd.
  Therefore every common reduction splits off two balanced exceptional
  solutions, one in a smaller unresolved dimension.
- Exact qutrit Gaussian and complementary witnesses guard against the
  false simplification that every local cubic compression is half-rank.
- The theorem proves that a minimal \(2\bmod4\) solution must be
  common-leg-irreducible.  It does not exclude such an irreducible
  solution, so the complete spectrum remains open.

## 2026-07-29 01:42 PDT — Scalar contraction routes exhausted

- Reduced all six \(S_3\) scalar closures of the cubic exactly: four are
  tautologies and two are only functionals of the known outer channel
  identities.
- Derived the remaining middle partial contraction, its exact positivity
  bounds, total trace, and scalar one-site marginals.
- Constructed an exact \(d=6\) scalar model satisfying all middle
  contraction data.
- More decisively, constructed a standard rank-half \(d=6\) involution
  invisible to all 48 sitewise-partially-transposed permutation tests
  while its cubic residual has squared norm \(192\).
- This exhausts scalar permutation/Brauer contractions as a
  four-divisibility route. Any successful proof must preserve
  operator-valued spatial overlap data.

## 2026-07-29 01:50 PDT — Full retained Weyl coefficient search completed

- Expanded the \(d=6\) Weyl falsifier to all \(361\) real coefficient
  entries in the retained traceless-Hermitian operator frame.
- Calibrated its analytic gradient to \(1.38\times10^{-9}\) maximum
  relative error and completed forty predeclared multistart,
  continuation, direct-joint, and mixed-strata runs.
- No run approached both equations. All endpoints normalize numerically
  to either the exact Weyl cubic with the wrong quadratic or an
  adjacent-anticommuting involution.
- Proved exactly that the latter branch has cubic coefficient \(1\), not
  \(1/3\), and independently replayed an integer \(d=6\) example and the
  scalar objective law.
- Status remains NUMERICAL_EVIDENCE for the search. It is not an
  exhaustive no-go even inside the retained frame.

## 2026-07-29 02:02 PDT — Fusion anomaly isolated but does not descend

- Identified the neutral \(SU(3)_3\) fusion component exactly with
  \(R(A_4)\) and its degree-one module with the nontrivial projective
  \(A_4\) class.
- Verified directly that the twisted algebra is
  \(M_2(\mathbb C)^{\oplus3}\); an action on an
  \(s=d/2\)-dimensional space would prove the desired parity.
- Proved that the currently natural action lives instead on the
  \(2s\)-dimensional local space and therefore exists for odd \(s\).
- Audited the determinant blocks, grading, non-self-duality, and
  reflection mechanisms. The published exact \(d=4\) solution is not
  flip- or determinant-reflection-invariant, so bare reversal cannot
  supply the missing quaternionic action.
- Recorded the precise remaining categorical target: construct an
  invariant \(s\)-dimensional multiplicity space carrying the nontrivial
  projective \(A_4\) algebra from the simultaneous spatial placements.

## 2026-07-29 02:03 PDT — Restrictable dimension six ruled out exactly

- Constructed the four-strand \(q\)-symmetrizer and
  \(q\)-antisymmetrizer and derived their arbitrary-parameter trace
  factorizations. Their unique common zero is \(\eta=1/2\).
- Proved that the ambient balanced tower annihilates both idempotents,
  while any square-invariant local restriction inherits that
  annihilation.
- The scalar, \(1/3\), and \(2/3\) restricted branches each detect one
  of the two idempotents, so every nonzero square restriction is again
  balanced and has even local dimension.
- Concluded that every restrictable \(d=2\bmod4\) witness descends to a
  smaller one in the same congruence class. In particular, no
  restrictable \(d=6\) witness exists; any hypothetical witness must be
  non-restrictable.
- Replayed the Hecke calculation and the complete operator-valued
  mixed-color equations exactly.

## 2026-07-29 02:05 PDT — Determinant boundary route closed at all levels

- Proved that either three-site determinant corner satisfies
  \((a\otimes I)\mathcal A_{m+3}(a\otimes I)=a\otimes\mathcal A_m\)
  for every number of added boundary sites.
- The proof uses the simple-current fusion-graph automorphism and a
  dimension comparison with the injective disjoint Hecke copy.
- Therefore every closed boundary word and endpoint contraction is
  scalar on the rank-\(s^3\) determinant multiplicity.
- Located the apparent six-site Clifford pair exactly on the added
  three-site \(M_2\) path factor; its module multiplicity \(3s^6\) may
  be odd and supplies no parity of \(s\).
- Replayed an exact \(d=6\) abstract four-strand model satisfying all
  boundary, angle, rank, and opposite-sign identities used by this
  route. The model is a limitation certificate, not a spatial
  \(36\times36\) witness.

## 2026-07-29 02:15 PDT — Complementary invariance reduced to one variance

- For a balanced square-invariant \(W\), isolated the exact obstruction to
  invariance of \(U=W^\perp\):
  \[
  \delta=\frac{u^2}{2}-\operatorname{Tr}(K^2)
  =\|P_{\rm mixed}PP_{U\otimes U}\|_{\rm HS}^2
  =\frac12\|[P,P_{U\otimes U}]\|_{\rm HS}^2.
  \]
- Proved that \(\delta=0\) is equivalent to complementary square
  invariance.
- Built and independently verified an exact rank-18 \(d=6\) two-site
  limitation model with scalar partial traces, the exact published
  \(d=4\) restriction, and \(\delta=1/2\).  Its ambient cubic fails at
  coefficient \(-\sqrt2/48\).
- Concluded that the full mixed-sector cubic, not projection positivity or
  marginal data, is essential to any proof that one-sided invariance
  propagates to the complement.
- Nine reproducible one-sided \(4+2\) numerical runs found no candidate;
  this remains failed-search evidence only.

## 2026-07-29 02:36 PDT — Identity-amplification cut-down ruled out

- Calibrated a complex-Grassmann search for square-invariant subspaces of
  the exact \(d=8\) identity amplification.  Four rank-four controls
  reached zero to \(10^{-22}\), while all 32 predeclared rank-six runs
  converged within \(9.58\cdot10^{-15}\) of \(23/96\).
- Used the common numerical endpoint only for discovery.  The final proof
  is exact and does not claim that \(23/96\) is a global minimum.
- Rewrote every identity amplification as a three-term
  operator-Schmidt sum.  The second-site pencil has an exact Bell-basis
  rank-at-most-two cone consisting of six real lines.
- Proved for every \(m\ge2\) that
  \[
  [H^{(4)}\boxtimes I_m,Q\otimes Q]=0
  \quad\Longrightarrow\quad
  \operatorname{rank}Q\ne4m-2.
  \]
  Corank-two leakage forces two independent Pauli commutants and hence the
  full active \(M_4\), whose commuting projection ranks are multiples of
  four.
- A hostile independent audit reconstructed the Schmidt coefficients by
  partial contraction and checked the active commutant by a separate
  rank-15 linear system.  Both exact verifiers pass.
- This closes the neighboring \(4m\to4m-2\) cut-down mechanism; it does not
  exclude genuinely new unresolved-dimension solutions.

## 2026-07-29 02:40 PDT — Quaternion-frame descent audited

- At one bond, Rowell's braid generator determines only
  \(K_i=u_i+v_i+u_iv_i=-2qR_i-1\) inside the two-dimensional algebra
  \(\mathbb C[R_i]\).
- The individual anticommuting quaternion generators live in the larger
  ambient \(Q_n\) and are not recoverable as one-bond braid words.
- Therefore quaternionic parity on an \(s=d/2\) factor requires a new
  compatible frame-selection or splitting theorem; it is not a
  consequence of the Hecke/Yang--Baxter relations.  This agrees with the
  exact fixed-level split-module models for odd \(s\).

## 2026-07-29 03:06 PDT — Full-cubic color implication sharply limited

- Derived the exact mixed-boundary consequences of the ambient cubic for a
  one-sided balanced restriction:
  \[
  \|e_1e_2f_3P_{23}P_{12}\|_{\rm HS}^2
  =\|f_1e_2e_3P_{12}P_{23}\|_{\rm HS}^2
  =r^2u/4.
  \]
- Compressed the complete operator identity and located the obstruction:
  it contains \(L^*P_{12,\perp}L\), whereas complementary invariance needs
  the unweighted zero-variance statement \(L^*L=0\).
- Constructed and exactly verified a \(216\)-dimensional abstract balanced
  \(H_3\) model with the full \(d=6\) multiplicities, an inherited \(d=4\)
  summand, all eight exact \(4+2\) color-sector ranks, scalar one-color
  traces, and every color-level locality commutator.
- Both abstract complementary-pair leakages remain exactly \(16/9\).
  Hence no trace/SOS proof at the abstract cubic or commutative-color level
  can force \(\delta=0\).
- Scope guard: the model is not tensor-local and is not a \(d=6\)
  Yang--Baxter witness.  The genuine implication remains open and can only
  use the full spectator matrix algebras/common factorization
  \(P_{12}=P\otimes I_6,\ P_{23}=I_6\otimes P\).

## 2026-07-29 03:16 PDT — Standard balanced super-Hecke candidate excluded

- Fixed the normalized standard Manin \(GL(r|s)\) formula directly in the
  \((T+I)(T-qI)=0\) convention, avoiding a sign ambiguity among printed
  conventions.
- Proved with ordinary tensor placements that it obeys the braid relation.
  For \(r=s\), the \(q\)- and \((-1)\)-eigenspaces both have dimension
  \(d^2/2\), so the family has exactly the tempting algebraic data for all
  even \(d\).
- Proved that no positive local metric \(G\) can make it unitary at
  \(q=e^{i\pi/3}\).  Even/odd diagonal eigenvectors first force the parity
  spaces to be \(G\)-orthogonal; the mixed eigenvectors then have the
  unavoidable nonzero overlap
  \((\bar t-t)G_{ii}G_{aa}\).
- Independently replayed the \(d=6\) formula over
  \(\mathbb Q(\sqrt3,i)\): the complete \(216\times216\) ordinary braid
  residual and \(36\times36\) Hecke residual vanish, both multiplicities
  are \(18\), and the standard unitarity-defect norm squared is \(45\).
- This closes only the standard one-parameter quantum-supergroup
  construction and its local conjugates.  The unrestricted \(d=6\)
  problem and multiparameter/twisted variants remain open.

## 2026-07-29 03:20 PDT — Complete \(S_4\)-equivariant branch excluded

- Reconstructed the exact rational \(S_4\) actions on \(V_2\) and \(V_3\)
  and proved that the active commutant on
  \(V_2\otimes V_3\otimes V_2\) is \(M_2\oplus M_2\).
- Parametrized every noncentral trace-zero Hermitian involution by the
  complete product of Bloch spheres \(S^2\times S^2\).
- Extracted 20 sparse exact cubic coordinates. Exact Gröbner reductions
  yield seven branch relations, and three additional coordinates exclude
  the resulting real cases.
- Independently checked that the selected 23 coordinates and the two
  sphere equations generate the unit ideal over \(\mathbb Q\).
- Combined with the prior central check, this proves the full
  \(S_4\)-equivariant heterogeneous rank-six branch empty. The theorem is
  symmetry-scoped and does not settle unrestricted \(d=6\).

## 2026-07-29 03:24 PDT — Binary-tetrahedral \(\mathbb{CP}^2\) branch excluded

- Verified exactly, on all 24 Hurwitz units, the decomposition
  \[
  A\otimes B\otimes A
  \cong1\oplus1'\oplus1''\oplus3^{\oplus3}
  \]
  and commutant dimension \(12\).
- Proved that the only balanced equivariant signatures are a
  \(\mathbb{CP}^2\) rank-one multiplicity direction and its complement, so
  the parameterization covers the complete branch.
- Predeclared and completed 64 genuinely complex \(\mathbb{CP}^2\) runs.
  No candidate appeared; the best observed normalized squared residual was
  \(16/9\). The search is retained only as a falsifier.
- Replaced the numerical evidence by an exact three-coordinate
  certificate. Two residual entries force \(a^2=1/3\) and
  \(\operatorname{Re}(\bar z_1z_2)=0\); under those conditions a third has
  fixed squared modulus \(16/729\).
- Concluded that the full balanced diagonal-\(2T\)-equivariant
  heterogeneous branch is empty. This is symmetry-scoped and leaves the
  unrestricted \(d=6\) problem open.

## 2026-07-29 03:27 PDT — Finite-image fixed-point shortcut closed

- Verified from Rowell's primary proof that the canonical braid subgroup
  inside every \(H_n(3,6)\) is finite. Hence every exceptional localizer
  has finite braid image at every fixed strand number; finite
  dimensionality of the quotient alone would not have sufficed.
- Rechecked Conti--Lechner's published numbering and corrected the earlier
  citations: algebraic fixed points are Proposition 7.10 and the
  partial-trace ergodicity obstruction is Proposition 7.12.
- Constructed the exact family
  \[
  S_m=(q-1)(I_m\boxplus I_m),\qquad d=2m\ge4.
  \]
  It has \(|\rho_{S_m}(B_n)|\le3n!\), order-six local generators, exactly
  the exceptional normalized partial trace \((q-1)I/2\), scalar left and
  right leg commutants, no nontrivial algebraic fixed points, and a
  nontrivial von Neumann fixed algebra.
- Replayed the construction exactly at \(d=4\) and \(d=6\): all basis
  braid identities hold, both commutant linear systems have nullity one,
  and the normalized partial-trace norm squared is \(1/4\).
- Scope guard: the family has an opposite eigenvalue pair. It disproves
  the finite-image-plus-trace inference, not a stronger
  exceptional-specific theorem using no-opposite-spectrum and the
  resulting irreducibility of
  \(\varphi(\mathcal L_R)\subset\mathcal L_R\). The audited sources contain
  no bridge from that horizontal irreducibility to algebraicity of the
  vertical fixed algebra \(\mathcal L_R'\cap\mathcal N\).

## 2026-07-29 03:33 PDT — Orthogonalized Manin basin calibrated

- Added a full-complex rank-eighteen Grassmann initializer built from the
  orthogonal projection onto the balanced \(GL(3|3)\) Manin
  \((-1)\)-eigenspace.
- Predeclared and ran eight unrestricted seeds without marginal
  regularization and eight with unit marginal penalty. All sixteen
  returned numerically to the same nonstandard near miss.
- Verified that point independently over
  \(\mathbb Q(\sqrt3,i)\): the associated \(H\) is a trace-zero Hermitian
  involution, while the cubic squared residual is \(140/3\) and each
  partial-trace scalar-deviation squared norm is \(6\).
- The unpenalized and penalized limiting objectives are therefore exactly
  \(140/3\) and \(176/3\). This is a search calibration only; it is not a
  local-minimum certificate or an unrestricted \(d=6\) obstruction.
