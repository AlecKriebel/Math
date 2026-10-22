# Verification package for OWR 15957 002

Read REPORT.md for the outcome and PROOFS.md for the proof interfaces and complete elementary controls. Both original primary questions have prior resolutions: rational general factorability is false; unscaled integral factorability in order two is true. Attribution and manuscript-status qualifications are essential.

## Files and execution

- verify_certificate.py independently checks Holden's public finite certificate. It imports no source-package code and uses only the Python standard library.
- integer2_controls.py implements the all-input integral descent and finite countercontrols.
- test_corruption.py verifies rejection of five deliberately damaged public inputs.
- *_result.json and verification_stages.txt record actual checks.
- pinned_source_metadata.json fixes the exact external witness bytes, sizes, URLs and commit.
- source_metadata.json records primary-source inspection and retrieval results.
- MANIFEST.json hashes only authored work and public verification metadata.

Supply the five external files in one DATA directory: exact_algebraic_certificate.json, rational_cone_certificate.json, facets.json, R_integer.csv and A_integer.mtx.gz. Retrieve them using the exact immutable URLs in pinned_source_metadata.json. Validate their hashes before replay. No source dataset is included in this package.

From any working directory, with PACKAGE replaced by this package's directory:

    python3 PACKAGE/verify_certificate.py DATA
    python3 PACKAGE/verify_certificate.py --selftest
    python3 PACKAGE/integer2_controls.py
    python3 PACKAGE/test_corruption.py DATA

The mathematical checker raises explicit exceptions; Python optimization does not disable its checks. A successful replay prints PASS. Elapsed time is variable metadata and need not match the recorded duration.

All matrix predicates and field sign decisions use exact arithmetic. No program from the source repository needs to be installed or run. The absence of all-width rational factors follows from PROOFS.md and the checked certificate, not from enumeration of candidate Gram factors.

## Publication gate

This is an authored freeze prepared for independent audit. No fresh uninvolved review of this package has yet been completed. No remote writes were made. Do not publish source PDFs, extracts, downloaded source data or private coordination material with this package. The exact source witness remains accessible through its public immutable links.
