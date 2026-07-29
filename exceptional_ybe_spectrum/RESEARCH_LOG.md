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
