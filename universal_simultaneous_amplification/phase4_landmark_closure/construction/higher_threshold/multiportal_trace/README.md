# Symmetric two-portal protected-pair module

This folder contains an exact class no-go for the simplest growing module in
which two portals can be mutant simultaneously.

- `TWO_PORTAL_PAIR_NO_GO.md`: derivation and theorem.
- `verify_two_portal_tradeoff.py`: exact symbolic certificate.
- `verify_finite_lumping_exact.py`: independent exact labelled-state
  strong-lumping and quotient-rate audit.
- `check_finite_two_portal.py`: independent exact-lumping finite-chain audit.
- `search_two_portal.py`: numerical reconnaissance, explicitly not a proof.
- `RESEARCH_LOG.md`: timestamped research record.

Run the exact certificate with:

```text
./.venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/construction/higher_threshold/multiportal_trace/verify_two_portal_tradeoff.py
./.venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/construction/higher_threshold/multiportal_trace/verify_finite_lumping_exact.py
```

No literature search or external contact was used.
