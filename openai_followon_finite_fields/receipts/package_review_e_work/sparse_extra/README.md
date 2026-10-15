# Additional independent sparse falsification checks

`audit_sparse_extra.py` preserves the additional audit reported by the sparse
adversarial reviewer. It checks every rational descent stage against dense
factorization for 2,855 exhaustive and seeded inputs over six finite fields,
then checks three explicit large-bit constructions without a dense oracle.
The expected 5,758 stages, 66 negative-residue stages and largest denominator
degree 14 are asserted. This harness does not rerun the package unittest suite.

Run from any directory with Python 3:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 /Users/alec/Documents/Math/openai_followon_finite_fields/receipts/package_review_e_work/sparse_extra/audit_sparse_extra.py
```

It writes only `results.json` beside itself. That receipt includes UTC run
timestamps, Python version, deterministic seed, script and frozen-input hashes,
field parameters, construction inputs, counts, checked invariants and scope
limitations. Expected frozen-input hashes are embedded in the script; changed
inputs cause failure. Bytecode writing is disabled before local imports.

The dense reference and sparse functions share `finite_fields.py` arithmetic.
Feasible dense tests use the explicitly small-test-only exhaustive prime oracle.
The large constructions use known linear factors and avoid that oracle. These
are reproducible finite falsification checks of the conditional sparse reduction,
not verification of the upstream unconditional prime-field theorem or novelty.
