# Phase V — source-flag closure

This directory contains the final single-linkage resolution of the
bimolecular stochastic positive-recurrence problem.

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

From `/mnt/data/bimolecular_positive_recurrence`:

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

Python dependencies are inherited from the project-level
`requirements.txt`.  All deterministic source files have self-tests.  The
independent verifier records source hashes, test results, the exhaustive
atlas digest, and calibration output in
`certificates/independent_verification.json`.
