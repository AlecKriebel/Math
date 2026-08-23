# Phase 2: symmetric weighted K4 families

**[PROVED]** Every nonuniform member of the natural complete-support 1+3 and
2+2 weighted K4 families is a strict death--birth suppressor for every `r>1`.

The self-contained proof is in `n4_symmetric_classification.md`.

The certified package launcher runs the two theorem-bearing programs. For
individual development invocations from the project root with its prepared
environment, use:

```bash
PAPER1_DEV_PYTHON=python3.14
"$PAPER1_DEV_PYTHON" phase2_n4/derive_lumped_certificates.py
"$PAPER1_DEV_PYTHON" phase2_n4/crosscheck_full_chain.py
```

The omitted `search_exact_k4.py` is an exploratory finite search retained only
in the development repository. It is intentionally absent from the public
certificate bundle and is not used as a universal proof.
