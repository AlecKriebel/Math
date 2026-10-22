# Positive PCA tightness: an attributed negative resolution

Problem 2800905 / AMR-027-0905, queue rank 1760.

The exact original question is Bandeira's Open Problem 9.5: the trace-one,
entrywise-nonnegative semidefinite relaxation of nonnegative PCA in the
unspiked Gaussian Wigner model with variance 1/n for every independent
upper-triangular entry.

The SDP value tends to 2 in probability and expectation. The full proof here
independently bounds the nonnegative unit-vector optimum by sqrt(2) + o(1)
with high probability. Consequently no optimal SDP matrix has rank one with
probability tending to one. This is a reconstruction and application of the
published Bandeira–Kunisky–Wein result, not a claim of novelty. The stronger
true-optimum limit sqrt(2) is attributed to Montanari–Richard; its lower-bound
proof is not reproduced or independently audited here.

## Reading order

- [PROOF.md](PROOF.md): the complete authored proof, including elementary
  tail, rank-one, feasibility, expectation, and diagonal-transfer arguments.
- [AUDIT.md](AUDIT.md): the complete independent mathematical and source audit.
- [ACCEPTANCE.md](ACCEPTANCE.md): accepted scope, attribution, review limits,
  and the publication boundary.
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public URLs, source byte/hash
  identities, historical retrieval times, and recorded inspection scope.
- [VERDICT.json](VERDICT.json): unchanged historical machine-readable verdict.
- [EDITORIAL_CHANGES.json](EDITORIAL_CHANGES.json): documented presentation
  changes and original/public identities.
- [MANIFEST.json](MANIFEST.json): exact inventory and hashes of the other seven
  files. The manifest does not hash itself or constitute a digital signature.

## Main references and source qualification

Bandeira's original notes, Open Problem 9.5, printed pp. 130–131:
https://people.math.ethz.ch/~abandeira/TenLecturesFortyTwoProblems.pdf

Bandeira, Kunisky and Wein, *Average-Case Integrality Gap for Non-Negative
Principal Component Analysis*, PMLR 145 (publisher citation year 2022),
153–171, Theorem 4: https://proceedings.mlr.press/v145/bandeira22a.html

Montanari and Richard, *Non-negative Principal Component Analysis: Message
Passing Algorithms and Sharp Asymptotics*: https://arxiv.org/abs/1406.4775

The published integrality-gap paper visibly reverses its displayed GOE
diagonal/off-diagonal variances. The diagnosis as a typographical error is
mathematical, not an author-confirmed erratum. The proof explicitly uses
invariant GOE with diagonal variance 2/n, then proves an asymptotically small
diagonal transfer to the exact original variance-1/n model.

This AI-assisted manuscript and independent AI-assisted audit are unrefereed.
Acceptance here is a mathematical assessment, not external human peer review,
journal acceptance, or formal proof-assistant certification. Named standard
probability theorems are invoked with checked hypotheses, not reproved.
No executable or omitted dataset is required for the written proof.
