# Simple polygonalizations: exact-counting audit

This package does not settle TOPP Problem 16. It contains self-contained partial proofs, explicit counterexamples to particular counting shortcuts, and a bounded exact checker.

- [REPORT.md](REPORT.md): exact scope, source corrections, five approaches, proofs and remaining gaps.
- [check_counting.py](check_counting.py): standard-library exact verification; requires Python 3.10+ and UID 1000.
- [EXPECTED_RESULTS.json](EXPECTED_RESULTS.json): synthetic examples and exact outputs.
- [VALIDATION.md](VALIDATION.md): reproduction commands and execution limits.
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public source URLs, hashes where original bytes were retrieved, and inspection limits.
- [MANIFEST.json](MANIFEST.json): SHA-256 hashes and byte counts of this authored package.

Status: unresolved. No polynomial-time algorithm, hardness classification, novelty claim, or exhaustive literature-coverage claim. The finite computation is not a complexity proof. Cited source documents and source datasets are not included.
