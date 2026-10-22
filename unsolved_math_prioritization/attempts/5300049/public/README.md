# Accessibility of positive-exponent boundary points

Problem 5300049 / AMR-052-0049, Przytycki (1992), Problem 1.2.

**Unresolved after five substantive approaches. No full proof or counterexample is claimed.**

The general question asks whether a boundary point with positive lower Lyapunov exponent must be accessible from a simply connected attracting basin. The important source distinction is that the published pointwise theorem retains local backward invariance. In the 2021 PDF, the exponent is underlined: a text-only extraction can misleadingly hide that it is the lower exponent.

This packet contains six proved auxiliary propositions, exact examples showing why several tempting shortcuts fail, and an explicit account of the unproved basin-side step. The topological, scalar and abstract-tree examples are not counterexamples to the original dynamical problem.

- `PROOF.md`: exact scope, mathematical arguments and remaining gap
- `ATTEMPT_LOG.md`: five distinct approaches and their outcomes
- `SOURCE_GATE.md`: primary-source scope and bounded prior-work checks
- `SOURCE_HASHES.json`: identification of the inspected source bytes
- `verify.py`, `verification.json`: reproducible, modest exact checks
- `STATUS.json`: machine-readable outcome
- `SHA256SUMS`: integrity manifest for every other file in this packet

Run with Python 3, using only its standard library:

    python3 verify.py --check-manifest

The saved deterministic output can be regenerated with `python3 verify.py --write`.
The written proofs establish the infinite statements; finite tests do not certify the original question, and no formal proof assistant was used.

Source PDFs and extracted source text are not redistributed.
