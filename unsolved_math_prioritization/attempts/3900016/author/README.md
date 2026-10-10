# Convex-polygon triangulations with distinct areas

This source-free packet contains self-contained partial results for problem 3900016 (AMR-038-0016). The full target remains unresolved here; terminal status is exhausted, 5/5 substantive approaches. No novelty or best-known-bound claim is made.

Read REPORT.md for the mathematical definitions and proofs, SOURCE_AUDIT.md for literature limitations, SOURCE_MANIFEST.json for inspected-source metadata, and VERIFICATION.md for the executed finite checks.

Run with Python 3.10 or later and no third-party dependencies:

    python3 -B check_claims.py
    python3 -B -O check_claims.py
    python3 -B -OO check_claims.py

For a copy with directory mode 0555 and file modes 0444, run as non-root UID 1000:

    python3 -B check_claims.py --require-readonly

The checker prints JSON. An optional --output path must be outside the packet. Read-only mode performs actual denied create and write-open probes without truncating files. Payload hashes bind every file except the pin manifest itself; freeze receipts or archive hashes provide the external manifest binding.

The suite is deliberately small. Exact finite checks support, but do not replace, the proofs and do not decide the unresolved extremal functions. The packet contains no dataset bodies, copied papers, or correspondence.
