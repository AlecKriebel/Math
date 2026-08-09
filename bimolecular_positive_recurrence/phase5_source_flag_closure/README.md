# Phase V — source-flag closure

This directory records Phase V, the immediate historical predecessor of the
version 0.3 manuscript and standalone verifier.  Its proof architecture led to
the current result, but this archived manuscript and its certificates are
superseded by `../manuscript/` and `../code/` for publication and citation.

## Result

Every one-linkage-class bimolecular weakly reversible stochastic mass-action
network is positive recurrent on every closed communicating class, for every
positive rate vector.

The proof is self-contained except for the inherited nonexplosion statement.
It does not claim the multiple-linkage theorem.

## Main files

- `main_manuscript.pdf` — expert-audit manuscript.
- `theorem_statement.md` — exact theorem and Foster certificate.
- `complete_credit_elimination.md` — target/source residual identity and
  scalar path recursion.
- `source_rate_flag_theorem.md` — normalized-log compactification.
- `zero_layer_gluing.md` — exact global conservation alternatives.
- `defect_promotion.md` — deterministic overshoot and duration bounds.
- `global_foster_theorem.md` — uniformization and trace-chain closure.
- `proof_audit.md` — compactness, rate, boundary, and Markov-chain audit.
- `technical_summary.md` — concise result summary.

## Verification

From the repository's `bimolecular_positive_recurrence` directory, first
create a Python 3.11-or-newer environment and install the historical verifier
dependencies.  For the exact version 0.3 audit environment, use:

```bash
python -m pip install -r requirements-tested.txt
```

The compatible ranges in `requirements.txt` are available for exploratory
reruns on other supported environments.

Then run:

```bash
PYTHONPATH=. pytest -q phase2_trigger_drain/tests \
  phase5_source_flag_closure/tests

PYTHONPATH=. python -m \
  phase5_source_flag_closure.src.phase5_independent_verifier
```

Regenerate the finite three-species atlas with:

```bash
PYTHONPATH=. python -m \
  phase5_source_flag_closure.src.bad_sequence_flags
```

The universal proof does not depend on finite enumeration.

## Reproducibility

Python dependencies are inherited from the project-level `requirements.txt`.
The version 0.3 certificate was regenerated with Python 3.14.6, SymPy 1.14.0,
NetworkX 3.6.1, and pytest 9.1.1.  Those exact package versions are recorded in
`../requirements-tested.txt`; compatible major-version ranges are retained in
`../requirements.txt` for additional supported-environment reruns.

All deterministic source files have self-tests.  The independent verifier
records source hashes, normalized test results, the exhaustive atlas digest,
and calibration output in `certificates/independent_verification.json`.
Pytest wall-clock time, machine paths, and interpreter metadata are excluded
from the mathematical certificate.  The Phase-V `package_manifest.json`
hashes the archived package after certificate generation.  These materials
are provenance aids; the current release verifier is `../code/reproduce.sh`.
