# T3-2 positive-workload final repair

This directory is an adversarial repair workspace for the proposed theorem
that every finite bimolecular weakly reversible stochastic mass-action network
with at most three dynamically active species and at most two active linkage
classes is positive recurrent on each closed communicating class.

The inherited candidate release is preserved under `inherited/`. Its finite
atlas and local aggregate-debt calculation remain useful, but its global
certification claim is withdrawn while the tight-environment and
trace-to-physical-time interfaces are reworked.

The active research record is `RESEARCH_LOG.md`; the current certification
state is `STATUS.md`.

## Claim-neutral regression replay

The current generic recurrence-interface regressions can be replayed without
external packages or writes to the project:

```bash
python3 -I -B verify_read_only.py
```

See `RELEASE_ENGINEERING.md` for their exact scope and the final-release
requirements. Passing these regressions is a proof-discipline check, not a
T3-2 certification.
