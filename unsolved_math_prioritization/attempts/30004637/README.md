# 30004637: branching Brownian unbalanced transport algorithms

The general fast-algorithm question remains unresolved in this attempt.
Five approaches yield fully proved, explicitly limited computational facts:
a nonlinear-endpoint obstruction, binary local proximal formulas, an
FFT/tridiagonal affine projection, a restricted finite-grid rate and dual gap,
and a quantitative bound for a quadratic growth-cost surrogate.

The existing Baradat–Lavenant numerical method receives full credit. A June
2026 proposed scalable method still uses a WFR approximation. Neither is
silently turned into an exact solution of the original general question.

Files:

- `PROOF.md`: complete statements, proofs, restrictions and exact remaining gaps
- `SOURCE_GATE.md`: primary-source, version, previous-attempt and PR checks
- `ATTEMPT_LOG.md`: the five substantive approaches and checkpoints
- `verify.py` and `checks.json`: reproducible symbolic and small floating checks
- `SOURCE_MANIFEST.json`: public URLs and local source hashes, without source copies
- `STATUS.json`: outcome and the own-row-only queue delta
- `FROZEN_MANIFEST.json`: publication file sizes and SHA-256 hashes

Run `python3 verify.py --output /tmp/30004637-checks.json` with the dependencies
in `requirements.txt`. The script performs no network or source-file reads.
The checks are not a general transport solver or an interval certificate.

AI-assisted and unrefereed. No novelty, priority, or full-resolution claim.
