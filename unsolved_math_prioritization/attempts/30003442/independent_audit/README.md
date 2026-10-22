# Independent audit for problem 30003442

Verdict: **PASS within the author's partial scope min(m,d) ≤ 3**. The unrestricted question remains unresolved by this work. See `AUDIT_REPORT.md` for the proof review, source distinctions, limitations and one optional manifest-symlink hardening correction.

Requirements: Python 3.11+ and SymPy 1.14.0.

Run the independent exact verifier against the unpacked frozen safe directory:

    python -B independent_verify.py --author /path/to/author/safe
    python -B -O independent_verify.py --author /path/to/author/safe

Run the independently pinned integrity check and nineteen corruption controls:

    python -B audit_integrity.py --author /path/to/author/safe --archive /path/to/STABLE_ROOTS_30003442_AUTHOR_PACKET.zip --self-test

These scripts are offline and import no author code. They require only the safe author packet and, for the archive check, its pinned ZIP. They do not need the source PDFs or corpora. Reproduction is computational support for the separately reviewed universal proof, not a proof of the unrestricted conjecture.

The directory is a safe audit artifact. No source PDF, text extract, screenshot, raw dataset or private coordination is included. The author freeze is preserved and no remote write was performed.
