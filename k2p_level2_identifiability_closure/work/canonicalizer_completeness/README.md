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
.venv/bin/python -B work/canonicalizer_completeness/test_canonicalizer_mutations.py
```

The first command uses up to eight local workers.  A clean full regeneration
and byte comparison is available as:

```sh
.venv/bin/python -B work/canonicalizer_completeness/verify_canonicalizer_completeness.py --full
```

The authoritative mathematical argument is in [PROOF.md](PROOF.md).  The
generated certificate binds the exact atlas and raw-ledger bytes.  No frozen
ledger is rewritten by this audit.
