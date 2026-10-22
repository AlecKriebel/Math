# Acceptance report for problem 30000773

**Authorship and review status:** This authored report was prepared with AI assistance and is unrefereed. It is an audit of the prior Cotar–Thacker result, whose journal publication is bibliographically verified. The report itself has no journal peer review or proof-assistant certification.

## Decision

**Accept a credited prior resolution of the original attracting-edge question under common finite integer initialization on connected bounded-degree simple undirected graphs, including the triangle, for every positive finite reciprocally summable reinforcement sequence.** The result is due to Cotar–Thacker (2017); this report makes no new solution or priority claim. Zero new proof-search turns were used.

The finite theorem is directly applicable and is independently verified in the audit for all finite initial-offset configurations whose shifted reciprocal series converge. The infinite source-level application is fully verified by the finite proof, a corrected frontier-trapping bound, and a finite-path domination argument. The same scoped verification covers finitely many real initial offsets when each shifted reciprocal series converges, and nonnegative integer offsets satisfying the stated reciprocal-summability and bounded-initial-reinforcement assumptions.

## Required qualifications

1. Preserve the uniform shifted reciprocal-sum condition (6) and the initial-reinforcement bound (8) when citing the infinite theorem. Explain why they hold for the accepted common initial count.
2. Preserve bounded degree, undirected edge reinforcement, positive finite weights, and almost-sure eventual fixation. No nondecreasing-weight assumption was introduced.
3. The inspected manuscript's formula (36) is not accepted as written. PROOF_AUDIT.md gives an exact counterexample to that estimate and a complete repair for the finite-offset scope needed here. This is not a counterexample to fixation.
4. The arbitrary real edge-dependent initial-state generality of Theorem 1.1 is theorem-cited but not independently proof-certified. No extension to that generality is silently inferred from the scoped repair.
5. The inspected full proof is arXiv v3. Published status was verified bibliographically; the journal proof was not obtained. No journal-text identity, journal-specific error claim, or complete-paper proof audit is asserted.
6. Do not credit the triangle as still open or claim a new solution. Preserve the older Limic–Tarrès monotone-weight result as prior work.

## Deliverables

- PRIOR_APPLICABILITY_CERTIFICATE.md: original-source interpretation, exact model, hypothesis matching, and accepted boundaries.
- PROOF_AUDIT.md: complete finite count-vector proof, finite-offset infinite-range repair, confinement-to-fixation argument, and exact manuscript-estimate discrepancy.
- SOURCE_LEDGER.md: public citations, retained PDF hashes and sizes, inspection history, publication verification, and retrieval limits.

This edition contains the authored documents and public verification metadata. It includes no source-document bodies, extracts or images; dataset contents; computational scripts, logs or result artifacts; or private coordination material.
