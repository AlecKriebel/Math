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
