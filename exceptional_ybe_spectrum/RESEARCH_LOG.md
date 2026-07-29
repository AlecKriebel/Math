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
