# Mesoscopic search checkpoint

The main note is `ATTACHMENT_REDUCTION_AND_SEARCH.md`.

- `search_modules_6_8.py` builds the finite Bd and dB subset chains, removes
  the attachment variables by the proved two-vertex reductions, and performs
  randomized plus local module-weight reconnaissance.
- `verify_attachment_reduction.py` independently checks the pair optimizer,
  repeated-module feasibility witnesses, and the exact regular-replacement
  Bd identity.
- `RESEARCH_LOG.md` records the scope and claim labels.

Quick verification:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  .venv/bin/python \
  phase4_landmark_closure/construction/higher_threshold/mesoscopic_search/verify_attachment_reduction.py
```

The search found no candidate beyond `3/2`.  The negative numerical values
are not impossibility claims.
