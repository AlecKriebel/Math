# Independent scope audit for Problem 30001405

Unrefereed, source-free audit. The literal counterexample is accepted; the strengthened intended target is unresolved here. No novelty claim.

- `INDEPENDENT_AUDIT.md`: full mathematical, contextual, source, and disposition review.
- `DISPOSITION.json`: machine-readable verdict and exact remaining scope.
- `SOURCE_VERIFICATION.json`: independently checked public source metadata and access limitations.
- `audit_checks.py` and `AUDIT_CHECK_RESULTS.json`: reproduced frozen diagnostics, five negative controls, packet integrity, and optional corpus metadata verification.
- `CITATION_REFINEMENT.patch`: optional pagination-only refinement, not applied to the frozen packet. If adopted, regenerate that packet's manifest and retain the original freeze separately.
- `MANIFEST.sha256`: hashes of every other file in this audit packet.

Run `python3 audit_checks.py PATH_TO_FROZEN_PUBLIC [PATH_TO_CORPUS_DIRECTORY]`. The script reads the input packet, runs its inspected verifier in subprocesses, and prints JSON. It has no network operations and edits no files. Negative mutations occur in memory. SymPy is needed by the inspected verifier. Corpus input is optional; no corpus contents are emitted.

Run `sha256sum -c MANIFEST.sha256` in this audit directory for its integrity check. This audit performs no publishing or repository operations. Source files and private work are excluded.
