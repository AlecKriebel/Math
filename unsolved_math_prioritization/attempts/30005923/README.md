# Row-ball moment and determinant covariance audit

This source-free, target-only packet publishes an authored reconstruction and independent acceptance audit for target 30005923 with an explicit companion disposition for 30005922. Main target: HOLD_VARIABLE_COUNT_UNIFORMITY. Companion: credited repaired prior result in the fixed-parameter scope. Proof turns: zero.

Read AUDIT_REPORT.md, FIXED_G_PROOF.md, INDEPENDENT_AUDIT.md, PROOF_INTERFACE_ADDENDUM.md, and ACCEPTANCE.md together. The mathematical documents are byte-identical to the accepted audit. Historical references to original/FIXED_G_PROOF.md and original/AUDIT_REPORT.md now refer to their same-byte top-level counterparts. References to the earlier original verifier, manifests, and replay history describe the earlier audit stage, not this delivery. HISTORICAL_* records are labeled historical evidence only.

The original verify.py unconditionally writes CHECK_RESULTS.json and is excluded from executable publication verification. Its replay is NOT_RUN. The earlier verify_audit.py wrapper is not replayed; its read-only finite calculation core is retained in verify_row_ball.py with explicit publication scope guards and separately tested code mutations.

Authenticate BOOTSTRAP.py against its externally published SHA-256 before running it. With directory mode 0555, file modes 0444 and real UID=EUID=1000, use python3 -I -S -B BOOTSTRAP.py <packet-directory>, or add --controls before the directory. Repeat with -O and -OO. A self-replaced manifest is not an external trust anchor.

The pinned bootstrap authenticates the verifier and controls before execution. Its fixed manifest authenticates the complete remaining packet, including acceptance, references, and explicitly pre-seal receipts. Complete fresh stdout/stderr are compared byte-for-byte, with recursive exact JSON types and no normalization. Source-body replay, original-verifier replay, historical-audit-wrapper replay, dataset replay and formal proof-assistant verification are NOT_RUN. Remote readback and CI remain NOT_RUN until publication.

No source PDF, TeX, extracted text, screenshot, dataset content, private source, private coordination record, or identifying internal metadata is included. This is a draft-publication candidate and does not change any queue or other target.
