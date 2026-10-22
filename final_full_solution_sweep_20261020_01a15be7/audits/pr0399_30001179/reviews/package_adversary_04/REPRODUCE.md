# Review reproduction

All operations are offline. Real network/process provider boundaries are trapped in the actual-function operation tests. Canonical helpers and scientific files must retain the reviewed hashes. This is a review, not lifecycle permission.

From the repository root, run the independent finite analytic checks with ordinary Python and `-O`; both JSON outputs must agree:

```
PYTHONDONTWRITEBYTECODE=1 python3 -B final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/reviews/package_adversary_04/analytic_checks.py
PYTHONDONTWRITEBYTECODE=1 python3 -O -B final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/reviews/package_adversary_04/analytic_checks.py
```

Run the actual-function operation checks with `--output` pointing to a NEW absolute directory under the sweep's `private/` tree, once normally and once with `-O`. Do not reuse sealed output directories:

```
PYTHONDONTWRITEBYTECODE=1 python3 -B final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/reviews/package_adversary_04/operations_checks.py --output /Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/private/pr0399_package04/NEW_operations_normal
PYTHONDONTWRITEBYTECODE=1 python3 -O -B final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/reviews/package_adversary_04/operations_checks.py --output /Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/private/pr0399_package04/NEW_operations_optimized
```

The expected output is55 passing nonfinding controls, four entries demonstrating the DOI-destination chain (actual resolver response, two accepted wrong destinations, actual final verification/appender), and zero real provider attempts. The current gap is expected acceptance by the actual reviewed verifier, not a rejected test execution. The explicit clearance/collector simulation is documented in the source and report.

The independent archive runner can extract and test a fresh copy, reproduce the baseline, run the27-mutation suite and execute two rehashed false-assertion mutants:

```
PYTHONDONTWRITEBYTECODE=1 python3 -B final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/reviews/package_adversary_04/archive_checks.py --output /Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/private/pr0399_package04/NEW_archive
```

The provided repair `replay_read_only.py` is separately rerunnable with NEW private output directories, normally and `-O`. Each should record1651 current controls,72 preserved old false-uniqueness cases,7 old recognized rejections and176 cached rows. Do not count those historical failures or cached rows as additional current passing obligations.

`verify_inputs.py` independently reconstructs every current/historical bound entry and actual Git original. Its saved `INPUT_VERIFICATION.json` is part of this seal; to rerun without writing it, pass `--output` with a NEW absolute JSON path under the sweep private directory. No provider or Git mutation is needed. Do not run any canonical lifecycle helper command or create clearance to reproduce this review.

The report's analytic deductions remain essential. None of these finite executions certifies the infinite-dimensional theorem or worldwide priority.
