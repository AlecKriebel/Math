# Strong Heegaard diagram diagnostic for Problem 2851

This package records a stalled partial investigation of KP-3.53. It does not prove or refute the assertion that every strong L-space is an alternating-link double branched cover.

Read REPORT.md for the exact scope, the finite geometric obstruction, source qualifications, and the unresolved step. ATTEMPT_LOG.md records the three approaches. STATUS.json is the machine-readable outcome.

Run the diagnostic with Python 3 using either:

    python verify.py
    python -O verify.py

Both modes must return PASS_RESTRICTED_DIAGNOSTIC with identical output. CHECK_RESULTS.json is the recorded output. The finite claim concerns only the positive unweighted Fano matrix in claims.json. Input-rejection tests are built into the verifier; no acceptance check uses Python assert.

SOURCE_AUDIT.json contains verification metadata and public scholarly URLs. This archive contains authored analysis and code only, with source metadata. It contains no copied source PDFs, corpus records, source text, or private coordination material.
