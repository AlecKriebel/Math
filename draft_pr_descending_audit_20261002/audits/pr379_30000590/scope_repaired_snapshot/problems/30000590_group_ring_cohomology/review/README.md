# Portable independent audit

The full scoped audit passes with the additive Davis book locator correction; the original remains unresolved after five author turns.

Run:

    python verify_review.py --author /path/to/group_ring_cohomology_30000590

This verifies the original and correction manifests, recorded raw Git blob IDs, all five author receipts and the independent exact controls. It needs only Python's standard library. Raw source PDFs and local rendered pages are not part of this public review. The recorded full audit checked all six source hashes and the relevant primary passages; the portable script does not claim to redownload them.
