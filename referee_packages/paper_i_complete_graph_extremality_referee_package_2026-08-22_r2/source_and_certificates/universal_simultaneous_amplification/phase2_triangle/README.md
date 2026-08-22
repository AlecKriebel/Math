# Phase 2: weighted-triangle dB classification

**[PROVED]** Every nonuniform complete-support undirected weighted triangle is
a strict death--birth suppressor relative to `K_3` for every `r>1`; uniform
weights tie exactly.

The self-contained proof is in `triangle_classification.md`.

Replay the independent derivation and the full subset-state cross-check with:

```bash
./.venv/bin/python phase2_triangle/derive_certificate.py
./.venv/bin/python phase2_triangle/crosscheck_exact_solver.py
./.venv/bin/python phase2_triangle/audit/independent_triangle_audit.py
```

None uses floating-point arithmetic.  The derivation script does not import
the project solver; the transition cross-check intentionally does.  The
hostile replay imports neither and independently reconstructs the certificate.
