# Research log: 30006231 / OWR-14299094-001

## 2026-09-30 12:23 UTC — source and prior-attempt gate

Read repository instructions, the current row, the full pinned record, and the original contribution through the complete report. Checked all-state PRs, the target branch/path history, prior statuses, assessments and related-target records; no earlier campaign attempt was found. No keyed upstream report or exact duplicate was found. The unedited queue row was rank 179, queued 0/5. The pinned dataset revision is 37e53eabe540fb458758e198be61634bd02ee008.

Actual model: GPT-6 Astra, xhigh. Research ceiling: two hours to 14:23 UTC, at most five substantive approaches. Parent owns queue/status changes. Completion estimate toward the curated bundle: 5%.

## 2026-09-30 12:33–12:43 UTC — approach 1: semidefinite parameter geometry

Recovered the exact finite-dimensional commuting-observable hypotheses. The original asks parameter uniqueness and proves the regular case itself; the curated state-uniqueness clause is broader. The 2023 geometry paper and its 2024 arbitrary-observable appendix supply important prior context. The latter appendix is not part of the journal version.

Derived the full representing-parameter spectrahedron and the exact radial positive-semidefinite criterion, including the necessary nullspace-to-complement coupling condition. Recorded the standard maximal-support ensemble criterion with a direct Hermitian proof and explicit credit to SDP uniqueness theory. This is an actual proof route, not source triage counted as zero. No novelty claim is made.

Completion estimate toward the expanded bundle: 55%.

## 2026-09-30 12:44–12:47 UTC — approach 2: pure versus ensemble uniqueness

Tested whether ensemble uniqueness can stand in for pure-state uniqueness. A seven-dimensional compression example has commuting diagonal observables, an interior critical expectation, a unique representing parameter and a unique pure representative, but multiple mixed representatives. The explicit isometry compresses the observables to the Pauli matrices.

This blocks that identification. The general pure-state question still contains rank-one fiber feasibility; this attempt does not replace it by a new geometric classification. The infinite-dimensional question is separately excluded. Froze the partial artifact at SHA-256 e72f9e5a0f08cf1190b578b307dd9f19ef8825a2d30d7645da4d37470c83b9af.

Conservative outcome: unsolved, two of five approaches used. Completion estimate: 55%; the remaining classification and source-scope gap is explicit.

## 2026-09-30 12:49 UTC — verification and review checkpoint

All 7,589 exact controls pass. These cover the radial test in small rational matrix families, non-coordinate compressed nullspaces, empty-block cases, Pauli compression, the Bloch identity, complex-Hermitian support dimensions, and boundary/critical diagnostics. Universal claims are proved in the artifact.

Full original, 2023/2024 geometry, 2025 imaginary-time and SDP-note PDFs were retrieved locally after earlier transfer timeouts. The original uniqueness page and the arbitrary-observable appendix were rendered and inspected. The final artifact, verifier and receipt hashes were sent to the separate reviewer. No result PR is opened before the review.

