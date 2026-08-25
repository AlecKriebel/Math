# K2P canonicalizer completeness audit

This layer closes the independent merge/split gate without an infeasible
all-pairs comparison.  It proves the exact finite action, compares the slow
and optimized descriptor implementations on every primitive archetype, and
independently replays every graph-relation candidate that reaches the
four-port quotient.

Run from the project root with the pinned environment:

```sh
.venv/bin/python -B work/canonicalizer_completeness/canonicalizer_audit.py
.venv/bin/python -B work/canonicalizer_completeness/verify_canonicalizer_completeness.py
.venv/bin/python -B work/canonicalizer_completeness/test_canonicalizer_mutations.py --output /tmp/k2p-canonicalizer-mutations.json
```

The first command uses up to eight local workers.  A clean full regeneration
and byte comparison is available as:

```sh
.venv/bin/python -B work/canonicalizer_completeness/verify_canonicalizer_completeness.py --full
```

The mutation runner requires a caller-owned output outside the project tree.
Only an explicit `--allow-authoritative-output` naming its exact nonsymbolic
canonical certificate may reseal that certificate. Report publication is an
fsynced atomic replacement and cannot truncate a hardlinked or late-symlinked
source file.

The authoritative mathematical argument is in [PROOF.md](PROOF.md).  The
generated certificate binds the exact atlas and raw-ledger bytes.  No frozen
ledger is rewritten by this audit.
