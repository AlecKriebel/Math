# Line arrangement shortest path audit

This packet concerns exact Euclidean shortest paths along full lines. It does not settle the general subquadratic-algorithm or quadratic-lower-bound question.

- `REPORT.md`: problem normalization, attributed historical corrections, five mathematical routes, proofs, counterexamples, and exact gaps.
- `CORRECTIONS.md`: contextual correction distinguishing the two-edge hop witness from the other one-bend route.
- `verify.py`: modest deterministic exact checks; Python standard library only.
- `SOURCES.json`: public bibliographic metadata, retrieval and inspection limits, hashes and byte counts. Source documents themselves are not redistributed.
- `VALIDATION.json`: observed normal, -O, and -OO runs as UID 1000 with failed-write probes.
- `MANIFEST.json`: SHA-256 and byte counts of the other files.

Ordinary verification: `PYTHONDONTWRITEBYTECODE=1 python3 verify.py`.

For read-only checks, make this directory non-writable and its files non-writable, then run as UID/EUID 1000: `PYTHONDONTWRITEBYTECODE=1 python3 verify.py --require-readonly`. Repeat with `python3 -O` and `python3 -OO`. The verifier writes only to standard output; it deliberately tests that writing its own file and creating a file in its directory both fail.

Finite tests are not a proof of a universal running-time bound. Public source checks were made on 8 October 2026. The 2020 thesis abstract was inspected, but its full PDF was not available to this inspection.
