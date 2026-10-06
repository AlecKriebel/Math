# Second analytic audit of the Ricci flow bridge

The analytic verdict is ACCEPT_SCOPED_THEOREM. The complete high-dimensional classification remains UNSOLVED HERE.

Read SECOND_ANALYTIC_AUDIT.md for the proof-level review. The new audit preserves both prior freezes and includes no mathematical correction patch. Fresh full-corpus verification is recorded separately from the first audit's historical NOT_RUN status.

This release contains authored review, exact finite diagnostic code, and permitted provenance metadata. It contains no source PDF, source extract, dataset content, target record content, or private coordination material.

## Replay

Run Python 3 with SymPy installed. Supply the external manifest SHA-256 from the delivery receipt:

    python -B verify_release.py --expected-manifest EXPECTED_SHA256
    python -O -B verify_release.py --expected-manifest EXPECTED_SHA256

The release verifier checks the complete member set, byte lengths, hashes, and exact replay of stress_results.json. The caller's pinned archive or manifest hash is the trust anchor; computing a new anchor from an untrusted modified package does not authenticate it. The verifier does not certify the mathematics.

To replay the separate corpus verification, provide the three complete original files yourself:

    python -B verify_corpus_inputs.py --catalog CATALOG_PATH --problems PROBLEMS_PATH --reports REPORTS_PATH

Only verification metadata is printed. External corpus contents are neither included in nor required for the self-contained release verification. INPUT_REPLAYS.json documents normal and optimized replays of the two authenticated input releases. Their full mutation harnesses were not rerun in this second review.
