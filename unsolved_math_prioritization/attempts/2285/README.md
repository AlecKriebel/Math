# Erdős #734: accepted partial reconstruction, target unresolved

Row 1868; problem ID 2285. Prepared 2026-10-21 UTC.

This authored package gives a complete reconstruction of the known O(n^(3/4)) existence bound for every n≥10, plus deterministic dense-truncation and full-plane-refinement barriers. It does not solve the O(sqrt(n)) target, assert novelty, or claim a 1−o(1) success probability. Its barriers apply only to their stated construction classes.

Read RESEARCH.md and RECONSTRUCTION_AUDIT.md together. The independent audit accepts the corrected threshold n≥10. The research note’s closing request for review and the earlier source gate’s statement that omitted estimates were not reconstructed describe their original stages; the later reconstruction audit supplies that review. The source gate retains its bounded-search and unverified-live-tracker qualifications. No current tracker access is claimed. The separate bounds audit is supplemental.

Only authored mathematical notes, code, exact finite check aggregates, and public bibliography/retrieval metadata are included. No source PDFs, copied third-party source text, dataset contents, private corpus extracts, or coordination material is included. Null PDF hashes and byte counts mean no certified local retrieval, not empty files.

Run `python verify.py` and `python -O verify.py` for recursive inventory validation. Run `python checks.py` and `python -O checks.py` for exact finite checks. Run `python controls.py` for the negative controls in both modes. These computations supplement proofs, not replace them. Original assertion-based code is retained solely for provenance; acceptance runs use the exception-based checks.py, which remains active under -O. Validation does not change package files.

TRANSFORMATION_PROVENANCE.json records exact inputs and transformations. VALIDATION_LOG.json consolidates normal/optimized execution and negative controls. MANIFEST.json inventories every other package file recursively, with exact byte counts and SHA-256 hashes; the verifier rejects symlink roots/entries and all non-regular, non-directory filesystem entries (including FIFOs); its self-exclusion avoids a hash cycle. A separate frozen receipt binds the manifest and entire inventory. No GitHub or queue edits are part of this package.
