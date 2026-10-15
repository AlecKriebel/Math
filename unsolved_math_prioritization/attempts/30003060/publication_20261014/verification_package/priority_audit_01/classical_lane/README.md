# Classical-priority audit artifacts

`REPORT.md` contains the source-to-result deduction and bounded priority conclusion. `DECISION.json` records the machine-readable disposition; `SOURCE_LEDGER.md` and `QUERY_LEDGER.md` record provenance and scope. `RESEARCH_LOG.md` records checkpoints.

The current `check_operator_blocks.py` uses explicit checks that remain active under Python optimization. `OPERATOR_CHECK.json` retains the original accepted output unchanged. To reproduce the interface audit without rewriting that accepted output, run:

```
python3 replay_operator_blocks.py
```

This driver creates and removes disposable copies inside this folder, runs the current diagnostic with ordinary and optimized Python, compares each result byte-for-byte and semantically to the preserved original, and verifies that a deliberately corrupted expected scalar is rejected before acceptance in both modes. It writes the current `REPLAY_RECEIPT.json`. Every driver acceptance condition is also an explicit check.

`historical_v1/` preserves the first script/output/decision bytes. Its script used removable assertions and is retained only for provenance; the parent-folder script is the current diagnostic. The guard-normalized syntax-tree check verifies that the interface repair changed no mathematical expression. `MANIFEST.json` pins authored artifacts, excluding itself and ignored `private_sources/`. Raw literature copies and extraction files are confined to that ignored folder and are not part of the public audit package.
