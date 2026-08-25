# Fixed-full K3P restoration package

This directory contains the active K3P replacement for the imported corrected
K2P restoration algebra.  The frozen forest supplies only graph, parentage,
repair-role, ordering, and exact transport metadata.  All physical graphs and
all algebraic pullbacks are regenerated with independent C, G, and T sectors.

Run:

```bash
../.venv/bin/python regenerate_k3p_restoration.py --resume
../.venv/bin/python verify_k3p_restoration.py
../.venv/bin/python test_k3p_restoration_mutations.py
```

The active theorem terminates all 36,568 first-layer rows.  The imported forest
still has 32 structural continuation nodes and 256 depth-two edges; those edges
are replayed and verified but are redundant in K3P.  Consequently 36,568 is
the minimal K3P terminal count, while 36,792 is the legacy/full-forest leaf
count.  These counts must not be conflated.

Primary files:

* `RESTORATION_MANIFEST.json` — active counts, hashes, and claim boundary;
* `restoration_ledger.jsonl.gz` — all 36,824 ordered forest edges;
* `restoration_proof_registry.json.gz` — exact proof certificates;
* `K3P_RESTORATION_INDEPENDENT_VERIFICATION.json` — independent replay;
* `K3P_RESTORATION_MUTATION_CERTIFICATE.json` — 20/20 rejected mutations;
* `K3P_RESTORATION_THEOREM_REPORT.md` — mathematical reader report.
