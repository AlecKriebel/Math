# Portable audit supplement

This authored-only supplement audits the frozen 12-file checkpoint for problem 30003592 (OWR-15586-003). Verdict: pass as unsolved partial mathematics, with one non-blocking notation clarification. It does not certify a solution, novelty, or literature completeness.

Read AUDIT.md for the mathematical review and CORRECTIONS.md for suggested clarifications. AUDITED_INPUT_MANIFEST.json binds every input byte, the source-tree digest, and the original archive. SOURCE_CHECKS.json contains citations, locators, and source digests only; it contains no source PDFs or full text.

Using Python 3 with no extra packages:

    python3 independent_checks.py

For a full replay, pass the original frozen submission directory and archive:

    python3 independent_checks.py --submission /path/to/submission --archive /path/to/rank631-30003592-authored-packet.zip --replay

The original archive has exactly 12 members under submission/. Extract it to a temporary directory if the original source directory is unavailable. The script does not download anything and does not alter the submission. No absolute local source path is required by the portable audit.

AUDIT_SHA256SUMS.json excludes itself to avoid circular hashing and covers all other audit files. The outer AUDIT_RECEIPT.json, distributed next to this directory and the audit ZIP, binds the full audit tree and ZIP. As usual, a hash verifies consistency of supplied bytes, not the truth of their mathematical content or the identity of a signer.

The audit contains no third-party PDFs, full-text extractions, source page images, upstream corpora, private repository snapshots, or private coordination transcripts. The original submission remains unchanged. No remote writes were performed by the auditor.
