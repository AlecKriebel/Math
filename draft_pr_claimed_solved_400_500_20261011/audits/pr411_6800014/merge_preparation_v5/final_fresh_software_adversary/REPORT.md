# Fresh final independent V5 software review — BLOCKED

This is a new independent review begun after both repairs at exact helper SHA256 `abd32d4d0a1d18c54825246e773b6ea3d13090d762850a20962f0f885b9c5279`. It does not reuse or replace the earlier reviewer, and it does not endorse any later repair.

The requested finite ADMIN-only mechanism must admit one separately approved successor of the genuine pinned zero-remote-intent merge abort, retain the original custody, preserve all existing phase/action/evidence guards, and prevent further remote writes after the successor reaches a terminal STOP. A per-run one-remote-intent fence is necessary but does not by itself establish that terminal phase-attempt property.

## Blocking counterexample

Construct one isolated continuation Journal from copied, path-adjusted ADMIN custody. Invoke the unchanged `execute()` with a valid exact-plan approval and a synthetic current PR that is not clean/mergeable. It records `STOP_UNCONFIRMED_OR_DRIFT` with `mutation_resume_permitted=false`; no remote intent or synthetic API call occurs. Keep that same Journal object open. Invoke `execute()` again with the same plan and approval, now supplying a synthetic clean/mergeable observation. It records the first remote intent and issues one synthetic expected-head ordinary merge PUT. The second call subsequently fails with `FileExistsError` when it reaches the existing terminal receipt.

Both normal and optimized Python reproduce this sequence. The old terminal receipt and copied originals remain byte-identical. The successor has exactly one remote intent, so the narrower one-intent fence holds while the terminal phase-attempt guarantee fails. `Journal.add()` checks original custody, the plan, the continuation guard and the remote-intent fence, but does not reject an existing successor terminal receipt before admitting its first intent. Rejection when writing the final receipt occurs after the synthetic PUT.

This is a blocker against the requested scope. The review does not narrow the accepted claim to the one-shot CLI. Raw before/after receipts, journals and synthetic API call records, plus standalone counterexample code and results, remain private under pinned references in `NATIVE_VERDICT.json`.

## Strongest verified partial result

| Independent evidence | Result |
|---|---:|
| Normal Python controls | 89 pass |
| Optimized Python controls | 89 pass |
| Isolated CLI subprocess controls | 14 pass |
| Terminal-STOP reuse counterexample | Reproduced in both modes |

The independent controls verify the exact descriptor/claim/run/root/plan/STOP/completed-CLI/acceptance join; rejection of extra, torn, acknowledgment and intent-bearing original journals; type, path, symlink and canonical-byte boundaries; original copied custody preservation; exclusive successor allocation under a six-way race; exact ordinary merge action binding; late custody/plan/guard rechecks; same-object response-loss and invalid-response reuse; a twelve-way same-object intent race; failures before fence allocation and after allocation, file/directory/journal fsync and partial append; consumed torn or symlink fences; and closed-object rejection before any open. After an allocation failure before a fence exists, a later direct call may claim its first intent; no allocated fence is removed. Fresh Sheet, exact approval, claimed scope and clean merge checks continue to reject synthetic drift.

The CLI controls exercise actual isolated `main()`/argument parsing/Journal/execute behavior with fake prepare, observations and API responses. Plan-only, stale and bad-approval paths allocate no successor guard. The one-shot CLI closes its Journal after STOP and a second CLI run cannot acquire the consumed continuation guard. No automatic retry is present. These successes do not cure the direct same-object terminal-STOP counterexample.

AST comparison to pinned V4 SHA256 `e4c9bd76594127b23cf6439df0b2c7a965f39b8f027d6debdb7cdf8e393aaa14` finds only `Journal` and `main` changed among original top-level nodes; 82 remain unchanged, including execution, mutation, preparation, evidence, approval, deadline, main/head, preservation and recovery logic. Only the read-only validator is added. The current supplied `TEST_RESULTS.json` is exactly 40,954 bytes and contains outcomes/hashes/private references rather than raw captures, plans or queue content. All twelve final packet pins matched before testing and are retained as exact private frozen bytes.

## Limits and exact remaining gap

Synthetic matching fields establish structural consistency only. Provenance requires the caller's authentic pinned root acceptance and original captures. The genuine descriptor SHA256 `7bc150a109e2ad48edafe5669e57d261944f5eeaad8de31526a4cfae2a417c48` received read-only validator replay; no actual root Journal was instantiated or mutated. Finite controls and ordinary POSIX exclusive-file/fsync behavior provide local software evidence, not native service success, new phase approval, a scientific result, or an exhaustive theorem about all external states.

The remaining gap is to prevent any first remote intent after a successor terminal receipt already exists, including same-open-object reuse, without weakening existing guards. Any proposed repair must receive its own frozen tests and a new final independent review. This review grants no live continuation acceptance. Earlier blocked reviews and their counterexamples remain unchanged and are not relabeled.

No native requests or mutations, external communications, scientific file or asset reads, Git operations, actual root Journal operations, or live approvals occurred. Exactly five compact public files are sealed; raw code, fixtures, custody, plans, journals and captures remain private. The actual seal digest is held separately to avoid a self-hash cycle.
