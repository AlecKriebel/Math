# K3 Problem 3.47: authored partial-results packet

Status: unresolved in both universal classes after five distinct mathematical approaches.

- `REPORT.md`: statement normalization, complete elementary reductions, conditional results, five approaches, exact remaining gaps, and public citations.
- `STATUS.json`: machine-readable scope and completion status.
- `SOURCE_PINS.json`: public bibliographic and verification metadata only.
- `verify_exact.py`: dependency-free exact arithmetic controls for the matrix and Lefschetz formulas.
- `EXACT_CHECKS.json`: recorded output of those controls.
- `AUDIT.md`: scope and inference checks.
- `MANIFEST.json`: byte counts and SHA-256 hashes of this authored packet.

Reproduce the arithmetic checks:

    python3 verify_exact.py
    python3 -O verify_exact.py

Both commands produce the recorded `EXACT_CHECKS.json` content. The script uses explicit exceptions rather than assertions, so optimization does not disable verification. The checks validate finite algebraic controls; the report separately proves the general identities. They do not establish a solution of either universal problem.

No source PDFs, copied source text, datasets, or private coordination material are included. No novelty is claimed for the deductions.
