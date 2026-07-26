# Replaying the accepted order-12 frontier

The acceptance record is
`results/order12_frontier_acceptance.json`.  It states exactly one finite
frontier result:

> relative to the published MacGillivray--Mynhardt--Virgile computation
> through order 11, every counterexample has order at least 13.

It does not claim a universal proof, a counterexample, or an independent
campaign enumeration at orders 10 and 11.

From the campaign directory, check every bound theorem, source, review, and
certificate byte, and independently parse the exact parameter-four DIMACS
census:

```text
python3 repro/c050/replay.py
```

The expected verdict is:

```text
VERIFIED_ORDER12_FRONTIER_BINDINGS
```

To decompress and replay the accepted 228,381,671-byte LRAT proof as well:

```text
python3 repro/c050/replay.py --full
```

The expected verdict is:

```text
VERIFIED_ORDER12_FRONTIER_BINDINGS_AND_EXACT_LRAT
```

Full mode requires `zstd` and the hash-pinned `lrat-check`; run
`./tools/bootstrap_sat.sh` if the checker is not yet installed.  Neither
mode invokes a SAT solver.
