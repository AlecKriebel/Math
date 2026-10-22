# Additive byte-integrity correction for the earlier WIP checkpoint

2026-10-02. The mathematical verdict and every frozen proof/review hash remain unchanged. This addendum corrects the initial review's blanket claim that all 29 author files matched the earlier remote checkpoint byte-for-byte.

The initial readback compared decoded text after newline normalization. A subsequent Git-blob verification identified exactly one difference at author commit 3e86c9c69a92b2df5bfd3ff276399e5272e6ca92: TURN_4_CERTIFICATE.csv had been uploaded with LF line endings, while the frozen author manifest and exact checker replay bind the original CRLF bytes. All 720 data rows and the header are identical; all other 28 author blobs match the frozen bytes.

Authoritative frozen CSV:

- 13,261 bytes, including 721 CRLF endings
- SHA256: 133d3404e2872d020cdcc9e7cebacb36db8c50cafe4dd07c6dd0d5d791f6b837
- Git blob SHA: b4b52c71cdea1e11a248469f7dc66b0a15807c31

Earlier WIP CSV:

- 12,540 bytes, LF-normalized
- SHA256: 651c2142344303af73fb7366aa2060b3400aeb7d0fa3c4d9a8b4b91be76a9c55
- Git blob SHA: 9f4eb6f75b7990c4ceae8c39b495b5286aa3e578

Publication must restore the original frozen CRLF bytes and verify the resulting Git blob, rather than normalize the manifest or change the mathematics. The earlier WIP commit remains an ancestor, and its newline discrepancy remains documented. The original INDEPENDENT_REVIEW.md and REMOTE_READBACK.json are historical records; their blanket remote-exact wording must be read with this correction. FROZEN_VERIFICATION.json's local manifest checks and AUTHOR_REPLAY.json's raw stdout/CSV replay remain valid.

This is an integrity repair only, not a new author proof turn. Original disposition stays unresolved after 5/5, and the scoped mathematical PASS is unchanged.
