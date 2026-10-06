# Independent scoped acceptance audit

Problem 30001176 / OWR-3392-002, 2026-10-06.

Read AUDIT.md for the disposition: the canonical-filtration and prescribed-singleton obstruction is accepted; an unqualified historical-conjecture resolution is not accepted. INDEPENDENT_LEMMAS.md expands the infinite mathematics. The original author freeze has not been altered.

Run the audit package from any working directory with Python 3.10 or later:

    python3 -B /path/to/release/verify_audit.py
    python3 -B -O /path/to/release/verify_audit.py
    python3 -B /path/to/release/test_audit_package.py

The directory must contain exactly its manifested regular files and MANIFEST.json. Extra files or directories, caches, symlinks, FIFOs and sockets are rejected. Redirect output outside the package. No network or third-party library is needed.

The manifest and code pins verify internal integrity and replay, not mathematical correctness. Verify the externally supplied ZIP and manifest hashes before execution. Replacing the packet and all its trust anchors is outside the threat model. Recorded external-source inspections and author replay receipts are historical audit evidence; the portable verifier does not reread source PDFs or corpora.

Included: authored audit and proof details; independent code; finite results; public titles, URLs, hashes, sizes and inspection metadata. Excluded: source PDFs and extracts, dataset contents, private sources, private personal data, and private coordination material. The package makes no novelty or exhaustive-history claim.
