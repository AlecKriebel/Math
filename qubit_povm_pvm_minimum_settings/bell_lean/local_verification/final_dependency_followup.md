# Independent dependency-review follow-up

Timestamp: 2026-09-11T02:21:35.096754+00:00. Follow-up review completion estimate: 100%. This note supersedes the unresolved-runner-issue status in `final_dependency_review.md`; it does not certify a fresh final run that has not yet completed. Review was read-only except for this note. No production, script, contract, inventory, or prior-report file was changed, and no Lean build was run.

## Earlier provenance findings: resolved in the reviewed code

- **Scratch inventory contamination is resolved.** The scanner explicitly covers `Bell.lean`, non-audit `Bell/*.lean`, and validation sources. It excludes `local_verification` probes. Both validation files currently contain anonymous `example` contracts, so they do not generate unimported named theorem queries. The current generated inventory has **675 public theorem queries**, all named declaration sources are production `Bell/` files, and its names/count exactly match `Bell/Audit.lean`.
- **Moved theorem ownership is resolved.** The target inventory now expects `main_claims_with_strengthening` in `Bell/Assembly.lean`. The generated source inventory records that same ownership. Its serial order contains **58 distinct production modules**.
- **Generated-inventory freshness is resolved.** `source_snapshot` includes both `reports/declarations.json` and `reports/source_completion/source_inventory.json`. They are hashed after the static generators succeed and compared together with production source, scripts, and contracts at completion. This closes the previously identified omission under the final writer-freeze procedure.
- **Recovered panic diagnostics now fail closed.** `check_no_errors` rejects `PANIC` even if Lean or Lake returns zero. The root agent reports replacing the triggering vector-entry simproc use and rebuilding the affected witness cleanly. This review confirms the runner's rejection logic; it does not independently reconstruct the earlier panic. The current `runner_tests.log` reports **45 tests passing**; these remain mocked control-flow/unit tests, not kernel-proof evidence.

## Supplementary contracts and final-run sequence

The runner now independently invokes **both** `validation/Statements.lean` and `validation/PhysicalContracts.lean`, checks each exit status and diagnostics, and records both source names in the statement audit. Both files are included in the protected input snapshot.

The supplementary contracts expose POVM validity, nonnegative normalized nonsignaling Born probabilities, the fully expanded conjunction behind `MainClaims`, the explicit witness value, the rational PVM hull bound, the displayed gap identity, the at-most-two-input equality, and the strengthened attained value. They add no hypotheses to production declarations. These expanded contracts materially reduce the risk of accepting a theorem name whose proposition alias had drifted.

The actual final sequence remains: verified compiler and pinned dependencies; positive and negative compiler controls; removal/backup of the local project build; serial production builds followed by `lake build Bell`; two contract elaborations; complete generated public-axiom audit; matching final source/manifest fingerprints; dependency revision and cleanliness recheck; and a single successful final receipt. Each substantive command's failure is handled independently by `RunFailure`; a later shell command cannot hide it inside this runner.

Reviewed runner SHA-256: `d09331a23dad52668c6e27570af5b67aa6bf99265c9016a7a896ee86157249e0`.

## Current disposition and remaining conditions

No unresolved blocking defect from the earlier runner review remains in the inspected code. The root agent reports all 58 production modules and the umbrella built; this reviewer independently observed the root `Bell.olean` and the matching 58-module inventory. Existing successful object files are still preliminary evidence relative to the requested fresh run.

At this note's read checkpoint, `reports/kernel_report.json` still had the historical `failed_or_not_run` status. Therefore this note does **not** claim the final fresh run has passed. Before delivery:

1. Keep the agreed production/script/contract/inventory writer freeze through the real final run.
2. Require its new success receipt, both contract passes, all 675 public dependency reports, and unchanged snapshot checks. If the run fails or reports a panic, resolve the cause and obtain a new successful complete run.
3. Check that the final committed proof inputs match that successful receipt, and retain its run-specific logs and hashes. Subsequent proof or verifier edits invalidate a previously matching receipt.
4. Complete/retain the independent paper-to-statement review and accurately state the formal scope, including the corrected implicit partition-preservation helper premise and the fixed complex-qubit model.

The usual compiler/kernel, runtime, filesystem, and pinned Mathlib cache-producer trust assumptions remain unchanged. The check freshly rebuilds this project's Lean sources; it is not an independent bootstrap rebuild of every third-party dependency. Historical uncompiled-source notices and mock/preflight successes should remain clearly distinguishable from the new final receipt.
