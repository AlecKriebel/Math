# Reproduce reviewer03

Use the exact helper/release hashes in `FINAL_CANONICAL_BINDING.json` and `REPORT.md`. All operations below are read-only against real services or operate only on synthetic local fixtures. No provider mutation, Git ref/index operation, or live spreadsheet append is part of reproduction.

The retained private directory is `/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/private/pr0399_package03`. It contains the fresh extracted frozen archive, copied test support and historical bindings, and an exact private copy of all seven reviewed helpers. The support loader points AUDIT at the actual canonical audit, while HERE/FROZEN and all outputs point to private copies. If canonical helpers later change, first compare hashes; a repaired helper is not the reviewed old binding.

From `/Users/alec/Documents/Math`, run:

```
.venv/bin/python3.9 -B final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/reviews/package_adversary_03/novel_identity_controls.py
.venv/bin/python3.9 -O -B final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/reviews/package_adversary_03/novel_identity_controls.py
.venv/bin/python3.9 -B final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/reviews/package_adversary_03/analytic_controls.py
.venv/bin/python3.9 -O -B final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/reviews/package_adversary_03/analytic_controls.py
.venv/bin/python3.9 -B final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/reviews/package_adversary_03/archive_mutants.py
```

The novel identity program uses actual collector/reconciliation/appender/readback bodies, simulates only provider boundaries and prerequisite clearance/public-download facts, and expects 72 false-uniqueness cases plus seven rejection controls per mode. Its actual-provider traps must remain unused. The independent analytic program should emit byte-identical outputs across modes, with counts given in `ANALYTIC_CONTROLS.json`. It does not establish infinite-dimensional assertions.

The extracted archive's `tools/reproduce.py` can be run normally, with -O, and with inherited PYTHONOPTIMIZE=2. Its 81-file integrity report and complete finite replay output should agree exactly. Run its `tools/test_integrity_controls.py` using the private directory outside the extracted bundle. `archive_mutants.py` independently rehashes six hostile semantic failures and requires replay to reject each after byte integrity passes.

The retained copied operational tests in `private/pr0399_package03/ops_tests` can be run normally and with -O using -B. Pass `--canonical` to `integrated_controls.py`, `repair_controls.py` and `replay_regressions.py`. Their control counts are 123, 83 and 324. `replay_counterexamples.py` uses the preserved old binding and reproduces the old defects; it is not a test against repaired current bytes. Read the retained regression fixture diff before interpreting its outcomes.

Optional real **GET-only** route probes are reproducible with `probe_public_aliases.py`. They access the unrelated already-published record 23333353, save bodies privately, and bind observed canonical links/JSON record ID. They neither test nor create an actual record999. Route behavior may change later; saved exact bodies and hashes preserve what was observed.

The final authored manifest excludes only itself and its checksum. Verify every path/length/SHA256 entry, then the checksum of the manifest. Private custody is separately hash-inventoried. Re-running a program that rewrites a reviewed receipt requires a new seal; do not silently replace historical evidence.
