# Phase 2: symmetric weighted K4 families

**[PROVED]** Every nonuniform member of the natural complete-support 1+3 and
2+2 weighted K4 families is a strict death--birth suppressor for every `r>1`.

The self-contained proof is in `n4_symmetric_classification.md`.

Replay:

```bash
./.venv/bin/python phase2_n4/derive_lumped_certificates.py
./.venv/bin/python phase2_n4/crosscheck_full_chain.py
./.venv/bin/python phase2_n4/search_exact_k4.py
```

The first two commands are exact proofs/checks.  The last is explicitly a
finite exact-rational search and is not used as a universal proof outside the
classified families.
