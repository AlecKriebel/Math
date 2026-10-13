# Independent operations adversary report: PR 436 / 2569

The exact revised administrative helper and plan are accepted. No required code repairs remain. This verdict covers changing the frozen selected QUEUE status from `claimed_solved` to `already_solved`; it does not independently judge the mathematical priority conclusion. The final accepted priority gate and every required finding must still pass the helper's remote-main publication checks before the sole real mutation attempt.

The review stayed within this selected case. It added zero proof-search attempts, sent no messages to individuals, made no PR or branch mutation, and did not edit the root helper. The root owns publication and execution. Research-review progress is 95%; final accepted-gate readback is pending.

## Exact reviewed candidate

| Artifact | SHA-256 |
| --- | --- |
| `status_operation.py` | `73f14bb65c29aad2643aabddb76773f86b43b01f028d43911698deb3be556cec` |
| `STATUS_OPERATION_PLAN.json` | `ae6b6d85d86659fceb3d347874e89ae9f3878a228cc33f354ef99417e5bc8fd5` |
| Frozen original QUEUE | `4c7debabda92cbcf1fda654ca4082cdd663a62b450ba16ce3f5257c58f64fd28` |
| Intended changed QUEUE | `e50d06e91a26966ad942acf7cf8ed6b3545cf0cdc69d1d76ec6f51559410d1d6` |
| Frozen branch head | `c7805ab0804f50c6f4b0d1dda99e433dbb702ae2` |

The operation is bound to `research/semiperfect-sl2five-2569`, PR 436, repository `AlecKriebel/Math`, and `unsolved_math_prioritization/QUEUE.md`. The selected row retains `5/5`. The pending-gate structure binds the operation's exact code, complete plan, old and new QUEUE hashes, original head, and this review's machine result; its required-findings map contains the independent priority findings and root integrity receipts. Pending acceptance placeholders are not execution authorization.

Criteria were sealed before any verdict in `CRITERIA_SEAL.json`; revised tests were sealed in `REVISED_TEST_PLAN_SEAL.json`; final candidate hashes were sealed in `FINAL_CANDIDATE_SEAL.json` before isolated execution. Initial helper SHA `0448e24b442aa2024497d7428dc2f2a272606990706fffd568b213a55a4a3d2c` and unexecuted first draft mocks are preserved privately. No old-apply test outcome is claimed.

## Findings and repairs

1. **Remote-main publication, repaired.** The initial helper trusted a checkpoint's `branch: main` string and gate bytes at an arbitrary commit. The revised helper walks commit-parent metadata from remote `main`, binds every required local finding by SHA-256 to the checkpoint, and compares its published bytes at that checkpoint. An available gate at a nonancestor commit is rejected before mutation.
2. **Stale-head concurrency, repaired.** The original nonforced REST ref update could accept a reset to an ancestor after its head check. The replacement makes one `createCommitOnBranch` request with the exact `expectedHeadOid`; both ancestor-reset and sibling-advance mock controls reject atomically. The captured input contains precisely one QUEUE addition, the intended base64 contents, the exact branch/repository, and no deletions or other file changes. GitHub describes this mutation as creating a child of the branch head and advancing the branch, and specifies the expected head input. [GitHub's current commit reference](https://docs.github.com/en/graphql/reference/commits#createcommitonbranch) supports that mechanism. Root's live read-only schema receipt establishes the current `branchName` field, correcting stale prose mentioning `refName`.
3. **Tree/parent and after-classification scope, repaired.** The first helper verified its blob but only detected wrong tree/parent outcomes after a separate ref update. The final helper submits one atomic file change and confirms the returned parent, commit, tree, and full metadata delta on the path to QUEUE. All unrelated tree entries retain their modes, types and Git object hashes. It reads no source patches. Mock wrong-parent, unrelated-tree, truncated-tree, and wrong-QUEUE responses produce no preservation receipt.
4. **Exact reviewed-input binding, repaired.** Code hashes only in a refreshed mutable plan were insufficient. The final gate independently pins the code and full plan hashes, expected head, both QUEUE hashes, and accepted operations result. The result must accept those exact code/plan hashes. Required finding paths are confined to this selected case and must match local bytes, checkpoint hashes and published bytes.
5. **Uncertain outcome custody and reconciliation, repaired.** The full request is saved and fsynced; its SHA is stored in an exclusive fsynced attempt sentinel before the sole subprocess call. An existing sentinel always blocks `apply`. Response custody is saved before interpretation. Transport loss, malformed success JSON, wrong response client ID and wrong response parent are reconciled read-only in the controls, without a second mocked mutation. A still-original readback records uncertainty and retains the no-resend rule.
6. **Descendant receipt overclaim, repaired.** A prior reconciliation candidate allowed a descendant ref while only verifying the repair child's tree. A descendant could change an author file while QUEUE stayed identical. The final helper requires `ref == candidate`; the synthetic descendant with an altered unrelated blob produces no preservation receipt and no resend.
7. **Eligibility-first ordering, repaired by root.** Root independently identified that gate/finding reads preceded fresh eligibility. Final `apply` checks the selected PR/ref/QUEUE immediately after its attempt-sentinel check, and repeats that check before mutation. Already-classified and stale-head controls stop before any gate fetch. A nonexistent gate on an excluded head still produces the eligibility error first.

## Checkable validation

Eight parser/payload checks pass under normal Python and `-O`. They reproduce the exact after hash, demonstrate one changed Status cell and preservation of every other QUEUE byte and `5/5`, use header positions, and reject duplicate/missing targets, changed turns/status/display fields, and a missing header.

Thirty-three isolated atomic/administrative scenarios pass under each mode. They cover refused or unbound review inputs; absent checkpoint bindings; altered published bytes; non-main checkpoint ancestry; stale PR/head/base/repository/QUEUE; existing attempt custody; ancestor and sibling races; uncertainty and GraphQL errors; parent/tree/QUEUE readback failures; excluded heads; and read-only reconciliation. Every mutation-capable fixture captures exactly one mocked GraphQL attempt. Explicit trace checks allow only administrative commit/tree/ref/PR metadata and QUEUE endpoints after the attempt. REST mutations and unrecognized subprocess calls raise errors in the mock boundary. Both API and subprocess interfaces are replaced before `apply`; test network calls and real mutations equal zero. Tests use explicit checks rather than Python `assert`, so optimization does not remove guards.

Actual argv, from `/Users/alec/Documents/Math`:

```text
python3 draft_pr_claimed_solved_400_500_20261011/audits/pr436_2569/reviews/status_operations_adversary/atomic_guard_tests.py
python3 -O draft_pr_claimed_solved_400_500_20261011/audits/pr436_2569/reviews/status_operations_adversary/atomic_guard_tests.py
python3 draft_pr_claimed_solved_400_500_20261011/audits/pr436_2569/reviews/status_operations_adversary/parser_checks.py
python3 -O draft_pr_claimed_solved_400_500_20261011/audits/pr436_2569/reviews/status_operations_adversary/parser_checks.py
```

The public `TEST_RESULTS.json` contains the full administrative mock traces and test timestamps; `RESULT.json` binds it and both test scripts. The parser tests expect the frozen administrative QUEUE fixture produced by read-only `prepare`; its entire content is intentionally not reproduced in this report. Normal and optimized runs each have 33 atomic scenarios plus 8 parser checks, for 82 final-candidate controls total.

## Exact remaining limits

These tests prove the helper's guard and custody behavior against the listed fixtures; they do not execute GitHub's mutation service. API semantics rest on the official reference and root's live schema receipt. The actual response and positive administrative readback must still be retained by execution. `clientMutationId` binds response custody; it is not claimed to be server-side deduplication. Safety instead rests on the persistent no-resend sentinel.

Concurrent PR metadata changes are not atomically coupled to branch commit creation; the helper itself has no PR state mutation and refuses a positive receipt unless the readback is OPEN draft. A branch advance after the repair likewise yields no preservation receipt. The bounded main-ancestry walk can fail closed after 256 inspected commits. Corrupted local custody, unrelated descendants, or persistently inconsistent administrative readbacks require manual read-only reconciliation; none authorize replay. A readback that still shows the original head does not rule out delayed completion of an earlier request.

The pending gate must be finalized with this real result hash, augmented with root's final source-integrity finding, and freshly checked before application. No release, preprint, Zenodo, spreadsheet, comment, close, ready-for-review, or merge action is part of the accepted operation.
