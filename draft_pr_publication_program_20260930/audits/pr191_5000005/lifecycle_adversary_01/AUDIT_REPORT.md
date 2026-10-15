# Independent PR191 lifecycle audit — frozen proposal01

**Verdict: REPAIR_REQUIRED. Do not promote this frozen proposal to production clearance.**

Audit completion: 100% of the assigned frozen-input audit. Operational/publication completion is not established by this audit. No mathematical result is promoted or re-reviewed here.

## Independence and exact input

The acceptance plan was written and sealed before any proposal file or author audit/self-test judgment was read. Its SHA256 is `0af50fd3179ec2db88c8fca01be6db30112d927a3aa1e39d427ce6d280439003`. Root's explicit terminal signal authorized inspection after proposal01 was frozen. The authoritative proposal seal is `314f462a0900749d685125edd823cfd2c235657cc3c701ff0067ba50488d35cd` (8661 bytes); the live common module is `92ab6a4172eefe7965cdcc5288059bc6f57dd2c15c7504b4e721aed51eccafee` (44685 bytes). All listed proposal-seal manifest identities were independently verified. Historical PRE_PARENT_QUEUE_CORRECTION_SNAPSHOT_01 files were not treated as live implementation.

All nine live runtime modules, the separate generator guard, GATE_CONTRACT.md and PROPOSED_FILE_ALLOWLIST.json were source-inspected. The final author audit and self-test reports were not relied on; author SELFTEST.py was neither read nor imported. The seal's verdict/count fields were visible while authenticating its file list and were treated as untrusted judgments, not test evidence. Independent probes were designed from the presealed plan and source trace.

`independent_probe.py` records 39 completed independent offline cases with zero unexpected harness failures. A PASS in its result file means the stated probe expectation was reproduced; cases marked "confirm gap" are successful reproductions of a safety failure, not approval of the controls. Fixtures were created only under this own folder and removed. Socket/process entrypoints were replaced with fail-closed guards before the inert lifecycle module was imported. Native API calls were serviced by an in-memory immutable-object stub. No production native helper module was imported or executed; no network/process call, Git/index/ref/checkout operation, installation, remote mutation, outreach, or editor tab was used.

## Required repair R1 — acceptance trusts a shrinkable selected map and insufficiently bound diff witness

**Material blocking failure; source: lifecycle_common.py lines245–248,263–266,323–324,330–331,339–340.**

`require_merge_scope` requires only a lower bound consisting of native and package members. It does not require the exact Root-vetted FINAL_MAIN_SCOPE selected set, all control/factual members, or a binding to its exact plan. `verify_prepared` checks the supplied selected map against the supplied prepared tree. Consequently, the actual-MAIN lookup is only as complete as that mutable map.

Independent exploit `integration_pruned_map`: prepare a valid 109-member merge candidate, retain its original commit/tree and parents, remove only CASE/CURRENT_CASE_STATUS.json from the local SCOPED_MERGE_PREPARATION.selected_files, and place a descendant on actual MAIN that changes that omitted file. All packet/native members remain unchanged. integration_accept emits ACTUAL_ORIGINAL_HEAD_TWO_PARENT_MERGE_FULL_SCOPE_CURRENT_IDENTITIES_ACCEPTED with108 selected entries, although current MAIN has the wrong selected factual file. This attacks the exact acceptance invariant, not the already-prepared tree.

Independent exploit `factual_pruned_merged_map`: after valid merge and factual preparation, remove merged-only CASE/METADATA_PROPOSAL.json from the local merged map and change it in a descendant of the factual candidate at actual MAIN. factual_accept emits ACTUAL_FACTUAL_COMPLETION_MAIN_PARENT_FULL_SCOPE_COMBINED_CURRENT_IDENTITIES_ACCEPTED. Its combined map silently omits that original selected control member. Mandatory packet/native pins alone cannot establish the full selected scope.

A related witness check is also missing: `verify_prepared` does not require receipt.parent_tree to equal the actual expected_main commit's tree, or derive expected changes from selected pins against that actual parent. The independent `extra_merged_forged_foreign_receipt` constructs a different immutable commit with the correct two parents and all selected members, but a changed foreign path, then supplies its tree as parent_tree and an empty changed_paths list. Acceptance succeeds. This case creates new objects; it does not rely on changing an existing immutable Git object's bytes under the same identity.

**Required acceptance behavior:** derive or authenticate an exact stage-specific scope from final gated inputs; bind each preparation receipt to that exact plan, gate and original head; reject map omissions/additions or plan drift at integration acceptance and both factual stages. Reverify the merged receipt and exact merged map before factual preparation and at factual acceptance. Require parent_tree to equal the native tree of expected_main; compute the full actual tree delta and the expected selected delta directly, require equality, and prohibit foreign changes rather than trusting changed_paths as its own witness. Preserve retry generations and permit a new fresh-MAIN lease without changing the scientific gate.

## Required repair R2 — two own-row reads do not establish one tracker row

**Material blocking failure; source: lifecycle_common.py lines161–176.**

DOI uniqueness is counted only in the preappend full-sheet read. Both fresh postwrite reads fetch only the append range. An identical DOI row introduced concurrently after the pre-read is invisible to them. Independent `tracker_duplicate` adds a second identical row during the append response; exactly one RAW append call is made by this workflow, both own-row reads match, and TRACKER_ACCEPTANCE is still written although two rows contain the DOI.

`tracker_foreign_loss` also shows that a changed foreign row is invisible to the acceptance record. The source performs no postwrite full-sheet comparison. This does not prove the actual GWS append endpoint overwrites rows; it proves the controls cannot support an observed foreign-row-preservation claim from these readbacks.

**Required acceptance behavior:** after the external write or existing-row reconciliation, freshly read the whole relevant sheet at each acceptance readback, revalidate the header/target, require exactly one DOI occurrence with the exact approved row, and ensure the own range matches the unique row. Where foreign-row preservation is asserted, reconcile against the pre-read, allowing concurrent additions while refusing unexplained loss/change. Keep other sheet rows private; export only own row and sanitized counts/digests. Unknown or conflicting outcomes must stop for reconciliation without appending again or deleting rows automatically. This cannot guarantee that no future concurrent writer changes the sheet; acceptance must truthfully describe the states actually observed.

## Required repair R3 — completed native prose retains a live pending-merge sentence

**Factual consistency repair; source: lifecycle_common.py lines201–216, especially the merged text append at line215.**

The95% generation replaces the reviewed pending sentence with text saying the original-head merge "remains pending at this preparation." The100% generation appends another paragraph instead of replacing or explicitly retiring that current-status paragraph. `actual_native_factual_aliases` uses the actual pending01 README.md and review/REVIEW.md bytes and confirms that both final documents contain the pending and accepted merge sentences together. The JSON aliases are updated correctly.

**Required acceptance behavior:** replace the exact generated95% current-status sentence with the100% accepted statement, or explicitly move/mark the prior statement as a dated historical snapshot. Preserve immutable pending/final generations and historical logs. Do not edit proof/code/original16 bytes or alter the scientific/credit qualifications.

## What independently held on the exercised routes

- Full gate acceptance with exact packet roles and three upload entries; rejection of payload/proof/original16 drift, wrong original head, duplicate reviewer identities and changed pinned review bytes.
- Explicit review report/seal/root-authentication pins are checked, and publication/tracker receipts bind to the exact gate hash. Changing a valid gate invalidates an older publication receipt.
- RAW tracker request targets the fixed spreadsheet/gid/tab/header; one append and two actual own-row calls occurred on the exercised happy path. An unknown successful append was reconciled through the existing DOI with one write total; an unknown outcome without a visible row blocked another append.
- Wrapper unknown stage outcome led to calls [stage,inspect], with no second stage when inspection could not reconcile. Unknown publication led to [inspect,publish,inspect], with no second publish. An already-published saved record was reused by inspection alone. The actual tool source was inspected for its saved-state reuse and publish-readback design; no live Zenodo state was read or changed.
- Native generation protects all original16 through its manifest, rejects extra native files and changed protected code even if the mutable current manifest is updated, and updates the actual known native JSON status aliases. Science and credited/no-novelty claim content were not re-adjudicated.
- With an intact full selected map, altered actual-current-MAIN selected identities are rejected even when the prepared tree remains intact. Wrong actual PR head and wrong prepared parent order are independently rejected. A foreign path introduced improperly by a tree builder is rejected during preparation; foreign queue target-row edits are refused.
- Successful native integration uses parents [fresh MAIN, original HEAD], preserves foreign paths, and performs fresh proof/packet body checks. Metadata mismatch is refused. The successful factual postimage has40 completed /24 published, current191, last191 and next192; tested stale aliases are retired.
- Both stale merge and stale factual preparations refuse adoption after MAIN advancement; a fresh generation preserves new foreign bytes and the abandoned receipt, and retains the same gate hash. Protected native generations are reusable on the tested retry route.
- The supplied generator guard refuses overwriting an existing audited output. Path checks reject private state and unapproved media derivatives on the exercised inputs.

## Trust boundaries and limits

The review gate hashes files and checks distinct reviewer labels and Root assertions, but does not parse report/seal/authentication semantics or independently infer chronology, final-input coverage or repair resolution. `review_bodies_contradict_gate_accepted` demonstrates that contradictory/future synthetic review bodies pass if a Root gate itself asserts PASS and pins those bodies. This is an explicit trusted-Root boundary in the contract, not evidence that such false final authentication exists. Before issuing a real gate, Root must authenticate the final actual report/seal/scope succession and final current proof, packet/native/control hashes. A seal count or arbitrary labels cannot establish that review fact. The exact Root gate does not yet exist.

The native object helper chain is loaded lazily from prior-case code and the uploader/GWS executables are external dependencies. This audit did not certify or execute their entire transitive implementations; the in-memory stub tests this proposal's logic. Root must use the previously authenticated native helper/API and uploader versions and separately perform expected-old/nonforce adoption. No API stub can establish a future real DOI, append, PR state or current-MAIN observation.

Synthetic test rows contain no actual other people's tracker data. The real input inspection was confined to approved proposal/control/native-factual records and the named original-parent guard; no external paper body was copied. The strongest verified result is the set of reproduced safety properties and counterexamples above. Proposal01 production safety remains unestablished until R1–R3 are repaired and independently checked against a separately frozen generation. Root reported that no canonical installation, gate, actual publication, append or PR mutation had occurred during this audit.

## Artifacts and reproduction

INDEPENDENT_PROBE_RESULTS.json contains all39 assertions/outcomes. The harness is independent of the author self-test. To rerun without altering this sealed checkpoint, copy only independent_probe.py into a fresh sibling audit folder under the same PR191 case and run that copy with Python -B; it resolves the still-frozen proposal01 and named native factual inputs from the case root, creates only local temporary fixtures under the new folder, and writes its own result file there. Input identities are in INPUT_BINDINGS.json. SAFE_ALLOWLIST.json is the exact public selection. FINAL_MANIFEST.json and FINAL_SEAL.json bind this checkpoint without a hash cycle. All owned deliverables are0444.
