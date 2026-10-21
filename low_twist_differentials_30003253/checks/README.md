# Exact branch-integrality checks

The implementation uses Python 3.12 and SymPy 1.14.0. Prefer the package-level `replay.py`: it verifies hashes and computes in isolated copies, leaving the evidence unchanged.

## Implementations

- `branch_integrality.py`: exact rational incidence-quotient generator, Gröbner branch normal forms, rank/nullspace search, input guards, and independent witness validation. This is the final audited generator without publication changes.
- `audit_independent_model.py`: larger Euler-horizontal tensor system and three tangent fields, using an independently written sparse lexicographic normal form, not SymPy remainder or Gröbner reduction.
- `audit_division_free.py`: exact coefficient blocks E(P)−FQ, avoiding polynomial division entirely.
- `audit_saved_cases.py`: reproduces all 49 saved spaces using both independent methods, verifies complete lower-twist coverage, and validates all 12 witnesses.
- `publication_controls.py`: 17 additional negative controls plus conic, additivity, split/product, and guard-structure checks.

Every script uses explicit exceptions rather than optimization-removable assertions. Publication-only guard changes to the three audit scripts are documented in the package edit ledger and complete diff. They preserve all original conditions.

## Saved evidence

- `exact_results.json`: 12 authored examples, 49 searched dimensions/ranks, and 12 first-success witnesses.
- `validation_controls.json`: nine main rejections, six coordinate transformations, and split/product equivalence.
- `audit_independent_results.json`: 14 structural/regression cases and the nonreduced-input guard.
- `audit_division_free_results.json`: transformed-conic and multiple-branch cases, plus altered and zero-witness controls.
- `audit_saved_results.json`: all saved cases, witnesses, search coverage, and exact source-results hash.
- `optimized_run.txt`: output from the corrected main generator under `python -O`.

The earlier shared `Poly.rem` defect is disclosed in the main README and final audit. Only repaired outputs are included. These checks do not verify arbitrary future inputs, general algebraic-number-field support, the broad original surface problem, or new priority.

Running an individual script directly writes its results beside that script. The package-level replay instead creates fresh copies, reruns all stages normally and with `-O`, compares exact bytes, and tests five saved-result corruptions in each mode.
