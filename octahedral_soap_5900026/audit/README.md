# Independent octahedral soap-film audit

**Verdict: accepted with explicit formulation corrections, as partial results only. Problem 5900026 remains UNSOLVED, 5/5 approaches.**

- AUDIT_REPORT.md: complete proof-by-proof acceptance report and limits.
- CORRECTION.patch: exact Section 0 correction against the frozen mathematical note.
- MATHEMATICAL_NOTE_CORRECTED.md: the resulting reading copy; original historical review-pending wording is retained, and the present audit is recorded separately.
- CORRECTION_RECEIPT.json: old/new/patch hashes and byte counts.
- independent_controls.py and INDEPENDENT_RESULTS.json: 1,075 independent exact checks; Python standard library only.
- REPLAY_RESULTS.json: original-packet, mutation, relocation, and patch-application verification.
- SOURCE_VERIFICATION.json: public bibliographic metadata, retrieval limits, hashes, and dataset identity only.
- AUDIT_MANIFEST.json and verify_audit.py: externally anchored audit inventory and replay.

Keep the original authored packet unchanged. The current-definition correction explicitly requires compact support and finite current regularity and supplies a classical-field pairing proof. It does not change any candidate, numerical value, or proof in Approaches 1–5.

Verify using an independently retained manifest SHA-256:

`python3 verify_audit.py --manifest-sha256 ANCHOR --original-packet /path/to/original/authored`

Omit the original-packet argument to verify the audit and independent diagnostics alone. Normal and optimized interpreter runs should agree. The optional original-packet check additionally needs the standard `patch` executable.

This packet contains authored analysis, correction text, code, public citations, and verification metadata. It contains no source PDFs, extracted source text, copied figures, dataset contents, or private coordination material. No publication was performed by the auditor.
