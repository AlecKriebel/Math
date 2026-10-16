# Bounded metadata status gate adversary

The reviewed source passed this bounded review. No required or optional candidate defect was found. This is an offline engineering result; it does not certify a live scope-clear scan or the larger research goal.

Reviewed current entire source SHA-256: `fc8ef5d6493c0088d94441e3a1876b9dc99bbaef84a98320647b84d15d5d048e`.

Reviewed old entire source SHA-256: `d37a9c47c9b682d867516e4a74339529902cd0146fca9a0e9c072270bc730084`.

Authenticated initial suite SHA-256: `ca6e25bd7521c8a9be14259c7bcd6cc8818e5a6f6115a1e1f8bce202263b7510` (9,937 bytes). The parent supplied and explicitly confirmed this external pin before the inherited suite was executed. The initial observation in SOURCE_PINS.json remains unchanged as a historical receipt.

## Exact claim and validation

The legacy identity correction may reconcile one original target only when there is no recognized native attempt ID, the current head equals the original submitted head, the original seed has one well-typed numeric ID and a lowercase 64-digit row fingerprint, and fresh complete canonical changed filenames contain the exact QUEUE path plus files exclusively below one legacy top-level directory whose numeric suffix equals that ID. The fresh authenticated immutable-head QUEUE must contain exactly one matching row, and its SHA-256 must equal the original row fingerprint before status classification. Only stripped cell 8 equal to `claimed_solved` is eligible.

I read the entire current sweeper and entire initial offline harness, authenticated the old snapshot, and independently generated/reviewed the exact old/new diff. The diff changes only legacy mapping and the associated pre-classification row-fingerprint guard. I reviewed all unchanged safety paths, including the actual live base pointer, bounded filename pagination, exact target-row selector, Git blob and byte-size authentication, literal status decision, before/after complete metadata snapshots, and failure handling.

| Actual Python mode | Independent cold controls | Inherited controls | Failed |
| --- | ---: | ---: | ---: |
| Normal, optimize 0 | 84 | 49 | 0 |
| `-O`, optimize 1 | 84 | 49 | 0 |
| `-OO`, optimize 2 | 84 | 49 | 0 |

The final own-bound runs contain 133 named controls per mode and 399 passing executions. These counts include related controls across the independent and inherited suites; they are not 399 different scenarios. The independent suite executes the actual 101-PR controller in 71 synthetic scan cases per mode, with two complete metadata snapshots, fresh file/QUEUE requests where applicable, and raw synthetic receipts. Other controls directly test parsers and immutable-input rejection. No actual service or Git call occurred.

The three earlier independent pilot runs also passed 84 each. They used the shared source filename only for compile/traceback metadata and initial `__file__`; every actual controller fixture already replaced the subject's P with own scratch before execution. I tightened this binding to the authenticated own source copy, preserved the exact adapter and pilot source/receipts, and reran all three modes. The final primary independent receipts are in `own_bound_actual0`, `own_bound_actual1`, and `own_bound_actual2`; `actual0`, `actual1`, and `actual2` are explicitly retained pilot evidence. Total archived passing executions including pilots: 651; primary acceptance count: 399.

The checks cover arbitrary fresh legacy statuses, claimed-solved eligibility, cached-status nonauthority, same-head live-base advances, the exact-known-head/live-base cache exception, changed-head fallback rejection, native identity preservation, missing/ambiguous roots and QUEUE, suffix/seed mismatches, malformed ID/hash seeds, forged/stale fingerprints, duplicate/missing rows, path traversal and case aliases, incomplete/repeated/changed pagination, drift, GraphQL errors, binary/type/size/GitBlob failures, unknown current base pointers, and branch names without immutable-head authority. Native attempt IDs retain the prior authoritative native route and never invoke the new legacy fallback; multiple native IDs remain unresolved.

Every tested subject/harness compilation was preceded by unconditional external whole-file hash checks in the actual Python mode. The trust checks and expectations use explicit errors, not assertions. The separate independent suite starts from fresh subject namespaces and does not reuse the inherited harness. The inherited adapter changes only one historical output-description sentence; its exact bytes and derived hash are recorded in each ADAPTER.json. Its bindings and transient fixture root resolve inside independent own copied directories.

## Limits and scope

No real PR mathematical folder/file, proof, source artifact, PR body, prior mathematical audit, or comment was read. In particular, no excluded PR content was inspected. All numbered synthetic PRs and synthetic queue rows in receipts are fixtures, not actual GitHub observations. I did not independently re-fetch the actual two legacy status rows. The parent retains responsibility for current real metadata/status evidence and the two new stable full-range clear scans. The earlier nonclear scan was not modified or retroactively relabeled.

No shared existing file was edited. No checkout, ref, index, configuration, installation, communication outside the parent, remote mutation, or live fetch occurred. All new files, copies, fixture directories, and receipts are under this adversary directory; no hard links or symbolic links were used.

The conclusion assumes the initial inventory remains trusted as originally recorded. Synthetic tests check algorithmic guards and do not authenticate production service responses. The required remaining workflow is two new complete stable live metadata/status scans; this adversary result is not a substitute for them.

Narrow assigned review completion: **100%**, at the final timestamp in RESULT.json. Larger research goal completion is not estimated here.

## Reproduction

From this directory, run `python3 independent_controls.py --output replay_independent0`, `python3 -O independent_controls.py --output replay_independent1`, and `python3 -OO independent_controls.py --output replay_independent2`. Run the analogous three commands with `run_existing_suite.py` and distinct new output directory names. Each command requires an unused output directory and preserves existing evidence. The live shared source and original harness must still match their externally supplied pins.

MANIFEST.json explicitly allowlists all sealed public evidence by relative filename and SHA-256/byte count, and excludes itself to avoid self-reference. Authenticate its externally transmitted fingerprint before accepting the package.
