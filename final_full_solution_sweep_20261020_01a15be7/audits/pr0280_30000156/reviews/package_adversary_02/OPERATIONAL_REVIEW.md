# Independent operational adapter review

**Verdict: mandatory repair required, P280-OPS-01 and P280-OPS-02.** The seven-helper implementation at the completed preparation binding is not cleared for live use. The scientific/five-release-file package remains clean under its stated scope. No live operation was executed by this reviewer.

The completed operations manifest is SHA256999852717308827d82c11825f1ccb727be39da786fa5a1f34a6dde229c26c6e5. All16 entries were independently length/hash verified and copied, together with the manifest, into bound_ops/. OPS_INPUT_BINDING.json gives the exact seven-helper and evidence identities. LIFECYCLE_REVIEW_PLAN.md was written before those files were read. I then read all seven helper bodies and the complete offline control code. Relevant calls into the existing Zenodo verifier/lifecycle and atomic-write infrastructure were also inspected; no provider action was invoked.

## P280-OPS-01: a contradictory ledger exemption can hide the exact existing target row and cause a duplicate append

PriorityP2, material operational defect. This requires an inconsistent or stale root-authored reconciliation that labels the already exact desired target row as distinct_non_target. It is not a claim that a correctly classified root file triggers the defect. The helpers nevertheless expressly protect target identity/DOI uniqueness and already forbid the analogous contradictory account-ID exemption; the target-row pre-append check must also take precedence over exemptions.

The frozen publication_live_gates.py, lines52-59, checks whether a row digest is in prior_rows before checking whether it is the expected exact target. Consequently an exact current target row included in root ledger_leads is skipped; reconcile returns target_rows=[] and accepts the gate. This is a real actual-helper result, not a replacement stub for reconcile.

The frozen record_publication_ledger.py, lines76-85, correctly detects the one existing DOI row and permits it when it equals desired_row(identifier). It then removes that row from found because the digest is in the root non-target exemptions. The empty found list enters lines92-103 and performs an append of the same row. Lines109-115 reject only after the duplicate has already been appended. The resulting error does not undo the external mutation.

The reproduction in independent_operations_controls.py uses synthetic record999 and contains no actual account/ledger data. It calls actual gate.reconcile, which accepts the contradictory exemption, and then actual ledger.append_verified with only public/provider/read boundaries mocked. Both normal Python and -O produce:

- one pre-existing exact DOI/desired row;
- actual reconciliation accepted, with target_rows=[];
- exactly one synthetic append of that same row again;
- only afterward, RuntimeError: Target row readback/uniqueness mismatch; no retry.

INDEPENDENT_OPERATIONS_RESULTS.json and its optimized counterpart preserve those outcomes. Generic subprocess, URL and Zenodo-client mutation/read boundaries are trapped; there was no actual provider access.

Required repair: at both the reconciliation and append layers, an exact desired target row or a row containing the exact current DOI must never disappear under non-target filtering. A contradictory root exemption should reject before mutation, or exact-row idempotence should take precedence while counting every current DOI occurrence independently. Preserve the present binding and reproduce the failing case against it. Test the repaired exact-existing-row path, contradictory exemption path, changed-notes same-DOI path, duplicate exact rows, ordinary non-target model rows and absence-of-target path, normal and optimized. A new independent full-package review must inspect the revised implementation after repair. This reviewer made no canonical edits.

## P280-OPS-02: a properly classified distinct record's unrelated local state blocks every phase

PriorityP2, material operational false block. This second finding was first reported by the parent after its read-only initial live collector; I independently checked the implementation predicate, actual local-state byte binding and synthetic behavior. I did not execute a live collector or repeat a full review of the unrelated article.

The actual root gate has phase before_integration, expected_deposit_id=null, one account lead23137834 and one local-state match at .zenodo-state/metadata-23137834-production.json. The current state file independently matches the reported SHA2560d9f0bc4ffc005cd0c36c15bde7a32f4bb451adb77671e8befbeed3b20337ef5. The gate hash is fad7eb4879ae25844436c835e0ea336cf07fd0d6d27fd8d74cbcc6ae2dc0d694. ROOT_REPORTED_LOCAL_STATE_OBSTRUCTION.json records only the necessary identifiers/hashes and predicate; no raw account/ledger body was copied. The parent identified the published regular-pentagon/torsion work as problem20000450/PR329, distinct from this target; that article classification is parent-supplied context.

Frozen publication_live_gates.py, lines62-65, rejects any nonempty local state match when the expected target ID is absent, and later requires every matching state to use the target ID. It provides no exception for the correctly metadata/full-files-bound distinct account records already accepted in lines27-35. Since the broad model keyword can match a legitimate unrelated record's metadata-state file, an honest root reconciliation cannot clear the initial gate, and cannot clear later gates while preserving that state.

Independent actual-helper controls supply an explicitly distinct synthetic record101 with exact full metadata/files projection binding. Actual reconcile accepts without local state, then rejects solely after that same known record's synthetic local state is added, both with expected target IDNone and999. The normal/-O results are in INDEPENDENT_OPERATIONS_RESULTS*.json. These tests involve no actual service access or local-state modification.

Required repair: provide a narrowly root-authored unrelated-local-state exemption bound to exact relative path, SHA256 and integer deposit ID, and require that ID to be among the correctly metadata/full-files-bound distinct account records. Never exempt the current expected target ID, unknown records, changed paths/bytes/IDs, unsafe paths or duplicate contradictory entries. Preserve all unrelated state files. A default reject when no valid explicit exemption exists remains appropriate. Tests must include the valid unrelated state, changed hash/path/ID, unknown or current target record, no exemption, before-integration and later phases, normal and optimized. Preserve this current binding and obtain a new independent full review after both repairs.

## Completed control and code review scope

The frozen preparer's actual158 offline controls were replayed twice, normally and with-O, with only scratch/output location redirected into this review. Both runs pass22 positive cases and136 negative cases and record zero actual provider access attempts. Their actual detailed per-case receipts are in operations_replay_normal/ and operations_replay_optimized/; this did not overwrite preparer evidence. The controls cover the candidate-specific17 source files, nested preservation, exact parent/head queue accounting and Notes, metadata/full-file non-target projection, merged-head phases, expiring gates, public metadata/download/DOI identity, durable intents and ledger uniqueness. Their pass does not cover the new contradictory-ledger-exemption case, which is why the independent test was necessary.

Direct code inspection confirms the intended PR280 constants, exact release binding, original-parent/head queue rows,17-file snapshot mapping and64-entry list archive handling. The Git overlay uses exact candidate paths, a base tree and non-forced ref update, with checks of nested siblings and queue bytes. Lifecycle stage/publish intents stop blind repeats, and authenticated/public metadata plus downloaded file bytes are verified before ledger work. These are observations about the frozen code and mocked controls, not certification of future account state, network schemas, a cross-service lock or scientific correctness. The root clearance and lead reconciliation remain root-authored trusted assertions; reports/seals/helpers are checked as byte identities, not interpreted as mathematical proof by metadata.

No additional material issue was identified in the completed planned scope. Both P280-OPS-01 and P280-OPS-02 prevent operational clearance of this binding. The parent has acknowledged mandatory repair and will preserve/repair the helpers and arrange a new independent full review. Publication, DOI allocation, staging, merge and ledger actions remain unperformed by this reviewer.
