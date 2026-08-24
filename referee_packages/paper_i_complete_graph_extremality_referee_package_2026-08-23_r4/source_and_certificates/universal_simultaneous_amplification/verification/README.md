# Independent exact verifier

Run from the research-program root with a Python environment containing the
pinned SymPy version:

```bash
PYTHONPATH=. python verification/verify_obstruction.py
```

The verifier is independent of `src/exact_markov.py`.  It reconstructs every
tested subset-state transition from aggregate single-flip formulas, checks
row normalization and exact positivity certificates, verifies strong
lumpability of `K_n` by mutant count, solves the absorbing equations over
`QQ(r)`, checks both complete-graph formulas, extracts sparse-support limits
and complete-support `1/r` coefficients, and proves a sample comparison's
numerator and denominator signs on `r>1` by exact shifted-coefficient
certificates.

The universal theorem itself does not depend on a finite computation: its
certificate is the vertexwise Cauchy--Schwarz inequality recorded in the
manuscript and in `certificates/strong_selection_certificate.md`.

