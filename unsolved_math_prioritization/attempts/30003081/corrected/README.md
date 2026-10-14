# Source-free authored packet

Start with [RESULT.md](RESULT.md), then read the five complete approach notes. [READINESS.json](READINESS.json) documents the bounded duplicate gate and source correction. [LEDGER.json](LEDGER.json) records the chronological route completions. [SOURCES.json](SOURCES.json) distinguishes inspected primary material, imported results, and unverified literature claims.

Status: original broad target unresolved, 5/5 approaches. The explicit seven-plane obstruction is credited to Abe–Kawanoue; the packet does not claim a new general resolution or expert peer review.

## Reproduction

Python 3 standard library only. Authenticate verify_packet.py, mutation_tests.py and MANIFEST.json against the external hashes supplied with the frozen delivery before executing them. A manifest authenticated only by itself does not establish origin or trust.

Run, substituting the independently obtained manifest hash:

    python3 -I -B verify_packet.py --manifest-sha256 EXTERNAL_MANIFEST_SHA256
    python3 -O -I -B verify_packet.py --manifest-sha256 EXTERNAL_MANIFEST_SHA256
    python3 -OO -I -B verify_packet.py --manifest-sha256 EXTERNAL_MANIFEST_SHA256
    python3 -I -B mutation_tests.py --manifest-sha256 EXTERNAL_MANIFEST_SHA256

The verifier enforces a closed flat inventory, ordinary regular files, unique safe paths, sizes and SHA-256 values. It rejects assert statements in executable packet members and replays the exact mathematical output in an unrelated temporary working directory, with the actual child optimization level checked. The mutation suite tests all three optimization levels, including relocated clean packets, 12 integrity corruptions and four false mathematical controls per level. This is targeted reproducibility checking, not a general software-security guarantee.

Third-party source PDFs, extracts, screenshots and dataset contents are deliberately absent. Portable replay checks their historical hashes as metadata only and reports source-byte reverification as NOT_RUN. Reobtaining scholarly sources or checking public corpus hashes requires separately supplied source bytes and is not performed by these scripts. No internet access is used in replay.

Finite rational computations supplement the written proofs. They do not prove all-dimensional sheaf statements, audit every imported theorem, establish exhaustive literature status or certify novelty.
