# Graph-derived K2P parameter transports

This directory closes the parameter-level gap left by the frozen mixed-graph
transport ledgers.  It does not change or reinterpret those ledgers.  Starting
from the primitive graph encodings, it reconstructs every probe equality,
reverse marginal, probe parent restriction, and restoration restriction and
then records:

- the paired `s`/`g` serial-product action on every physical edge;
- the exact permutation of reticulations and their ordered incoming parents;
- `lambda -> 1-lambda` exactly when that parent order is reversed;
- the special handling of root-suppressed incoming reticulation edges; and
- the ordinary-triangle common reticulation as a rank-nine local-section
  parameter, never as an affine inheritance flip.

Run from the project root:

```sh
.venv/bin/python -B work/canonicalizer_completeness/inheritance_transport/build_parameter_transport_certificate.py
.venv/bin/python -B work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py
.venv/bin/python -B work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py --output /tmp/k2p-parameter-transport-mutations.json
```

The mutation output must be caller-owned and outside the project tree.  An
authoritative reseal requires `--allow-authoritative-output` with the exact
nonsymbolic canonical report path. Publication uses an fsynced atomic replace,
so external hardlinks and late output-symlink swaps cannot modify source bytes.

The full verifier regenerates all three ledgers in a disposable directory and
requires byte-for-byte equality.  `--structural-only` checks hashes, schemas,
counts, affine actions, paired products, and closure without regeneration.
