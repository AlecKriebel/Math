# Endpoint combined trees

This folder contains one exact combined reduction of the endpoint
Bd--dB fixation-product conjecture and an exact obstruction to the natural
reverse/complement path involution.

Files:

- `COMBINED_FOREST_REDUCTION.md` -- the analytic identities, paired forest
  signs, hostile screen, and precise remaining gap;
- `verify_combined_forest_identity.py` -- independent dual/event-Palm/tree
  reconstruction over `QQ`;
- `verify_forward_forest_obstruction.py` -- direct forward absorbing-chain
  determinants, exact `P3` forest enumeration, and reciprocal edge-factor
  witnesses;
- `HIDDEN_TARGET_AUDIT.md` -- exact labelled degree ratios and the first
  collision obstruction to target-only conjugation;
- `verify_hidden_target_conjugation.py` -- exact `1:17` path certificate for
  the one-selective and full geometric-mixture failures;
- `RESEARCH_LOG.md` -- checkpoint history and status labels.

Replay from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  universal_simultaneous_amplification/phase4_landmark_closure/obstruction/endpoint_combined_trees/verify_combined_forest_identity.py

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  universal_simultaneous_amplification/phase4_landmark_closure/obstruction/endpoint_combined_trees/verify_forward_forest_obstruction.py

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  universal_simultaneous_amplification/phase4_landmark_closure/obstruction/endpoint_combined_trees/verify_hidden_target_conjugation.py
```

The universal paired-tree sign is **OPEN**.  No endpoint counterexample was
found in the mandatory hostile corpus.
