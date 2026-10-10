# Finite diagnostic validation

These tests validate the finite audit checker. They do not compute an invariant-functional space and do not independently establish the analytic theorem.

## Baseline

The independently written checker passes in normal Python, `python -O`, and `python -OO`. Every mathematical test uses explicit guards raising exceptions. No required guard depends on an `assert` statement.

The baseline covers all 15 unordered partitions, every ladder-side hypothesis, all possible matching edges and isolated Hall vertices, all three ordered-form/FLO hypotheses, fourteen exact rational pair/sign checks, the nested E-side scalar checks, and all sixteen parity assignments.

## Actual mutants

Six altered copies of the real checker were executed, each in all three Python modes. Every mutant exited nonzero for its intended mathematical diagnostic:

| Actual change | Required failure reason | Modes rejected |
|---|---|---|
| Reverse the second-coordinate matching relation | MATCHING_ORIENTATION | normal, -O, -OO |
| Shift the first segment right instead of left in Y | SHIFT_DIRECTION | normal, -O, -OO |
| Replace the reverse/forward gamma ratio by its reciprocal | Bad scalar valuation | normal, -O, -OO |
| Incorrectly cap each positive zero order at one | Bad scalar valuation | normal, -O, -OO |
| Replace ECDBA by the illegal linked-swap order CEDBA | Invalid order | normal, -O, -OO |
| Omit the closing C–E parity edge | Parity obstruction absent | normal, -O, -OO |

The fresh public runner records each exact edit, actual mutant hash, exit code, full output, and intended reason. These are executable mutations, not hypothetical descriptions. The two source-relation guards distinguish the shift and matching-direction failures.

## Genuine read-only probes

The process ran as UID1000/EUID1000, not root. A separate checker copy was given mode0444 in a mode0555 directory. It passed all three Python modes with its read-only output option. A real append-open on the checker and a real sibling-create-open in its directory were each denied by PermissionError/errno13. The input SHA-256 stayed unchanged and no sibling file was created. The validator then restored permissions solely to clean up its temporary fixture.

The historical checks described above do not modify the original inputs. The public replay executes authenticated altered checker source in memory, using explicit exceptions and full JSON output. Its three-mode receipts and actual mutations are in `FINITE_CONTRACT.json`, `CHECK_RUNS.json`, and `check_case.py`. The fixed-bootstrap publication controls separately verify physical read-only behavior, hostile import isolation, complete outputs, and unchanged delivery snapshots.
