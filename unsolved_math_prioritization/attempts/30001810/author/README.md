# Ordinary versus immersive simplicial volume

Problem 30001810 / OWR-5158-010, rank 980.

Disposition: **PARTIAL-PROGRESS; general equality unresolved.** Five actual mathematical approaches are recorded chronologically.

The report proves rational and pseudomanifold formulas, finite-cover multiplicativity and self-cover vanishing, a shuffle-product upper bound, an explicit fixed-boundary obstruction on the aspherical torus, and exact duality with a bounded-cocycle replacement criterion. The obstruction rejects a local proof strategy; it does not refute the conjecture. Elementary structural facts are not claimed to be new.

- `MATHEMATICAL_REPORT.md`: complete proofs, assumptions, scope, and precise remaining gap
- `APPROACH_LEDGER.md`: five mathematical approaches and their outcomes
- `SOURCES.md` and `SOURCE_METADATA.json`: verified definitions, literature distinctions, and public source hashes
- `CHECKS.md`: what was and was not checked
- `check_exact.py` and `EXACT_CHECKS.json`: reproducible exact-arithmetic tests
- `MANIFEST.json`: frozen file sizes and SHA-256 hashes

Run the finite checks from this directory with `python check_exact.py`. The JSON output should match `EXACT_CHECKS.json`. It is not a computational proof of the open comparison.
