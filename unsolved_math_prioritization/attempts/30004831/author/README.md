# Monoidal invariance of Hopf algebra cohomological dimension

Problem 30004831, OWR-8415347-009, rank 784. Checked 5 October 2026.

**Conclusion: already resolved negatively in existing work.** Ruipeng Zhu's Example 4.11 gives monoidally equivalent Hopf algebras with global dimensions 1 and infinity. The inspected original question has no finiteness, smoothness, or cosemisimplicity hypothesis. The dataset's partially-solved classification therefore understates the available resolution.

This packet independently reconstructs the order-two example with consistent coproduct conventions and elementary dimension arguments. Mathematical credit remains with Zhu and the cited background authors. It makes no novelty, editorial acceptance, or community-validation claim for this packet. No independent audit has yet been performed.

- `PROOF.md`: fully specified counterexample, canonical-map inverses, and dimension proof
- `SOURCE_AND_SCOPE.md`: exact question, hypotheses, literature boundaries, and source display cautions
- `RESULT.json`: machine-readable conclusion and zero new proof-attempt turns
- `DATASET_VERIFICATION.json`: hashes, sizes, exact-record match facts, and absence of an exact research-results record
- `PRIOR_WORK_CHECK.json`: bounded actual repository checks, separate from literature and triage
- `SOURCE_METADATA.json`: public scholarly metadata and retrieval/inspection history
- `verify_algebra.py`: exact rational normal-form checks and two source-display negative controls
- `CHECK_RESULTS.json`: reproducible finite-check output; not a machine proof of infinite-dimensional statements
- `verify_manifest.py` and `MANIFEST.json`: immutable-file allowlist and SHA-256 verification

Run `python3 verify_algebra.py` and `python3 verify_manifest.py` from this directory. The first command writes only standard output; its result should equal `CHECK_RESULTS.json` after JSON parsing.

The archive intentionally excludes scholarly PDFs, extracts, images, dataset records or corpora, raw repository responses, and private coordination material. Source hashes and public bibliographic facts are included for verification.
