# PR207 completion100 source-freeze preparation v2

V2 changes only current JSON/Markdown checkpoint wording and versioned preparation filenames. It preserves v1 source, documents, static receipt, manifest and seal byteexact. Functional prerequisites, source closure and historical dated pending-at-freeze entries are unchanged.

This is source code prepared for Root review. **The builder has not been imported or executed.** No actual95 or100 receipt, pointer, source packet, current view, QUEUE, API request, Git operation, ref change, PR action, publication action, or tracker action was created here. Publication/tracker facts are Root-supplied context; this preparation does not produce their evidence.

`freeze_completion100_v2.py` uses the independently accepted `native_integration_preparation_01/native207_v2.py` unchanged (31634B/SHA256 e850bb9adcb40db4d9949251c103677e37651f3ec3daad16219227729f7e1efc). It has only GET native API calls and source-freeze output writes. It cannot perform the later candidate/verification/CAS/sync steps. Root must read all five proposed documentary diffs before promoting them.

## Exact prerequisite boundary

The builder is specific to the already frozen merge95 manifest159432B/SHA256 d636727bdb719b0d9acbc76e5ef7e7040a3d2e92e55f7f539601845c45d47861 (311 selected files,2594743B), candidate cd33621f1fa67d272e64ce4186bb4ccff4d4c1af and tree4e5a94115fcd1e974c7e8f9e4a3490cd726d048d. A candidate object's existence does not satisfy this boundary.

Execution first requires all nine real, separately pinned local records at these exact A-relative paths:

| Role | Path |
|---|---|
| acceptance | native_integration_preparation_01/ROOT_MERGE95_ACCEPTANCE_01.json |
| pointer | native_integration_preparation_01/ROOT_ACTUAL_MERGE95_POINTER.json |
| sync | native_integration_preparation_01/root_merge95_local_sync_01/LOCAL_GLOBAL_FIVE_SYNC.json |
| original_PR_merge | ROOT_ACTUAL_ORIGINAL_PR_MERGE_01.json |
| plan | root_native_integration_execution_01/MERGE95_PLAN.stdout.json |
| verification | native_integration_preparation_01/root_merge95_independent_verify_01/VERIFIED.json |
| cas_intent | root_native_integration_execution_01/MERGE95_CAS_INTENT.json |
| cas_result | root_native_integration_execution_01/MERGE95_CAS_TOOL_RESULT.json |
| ref_readback | root_native_integration_execution_01/MERGE95_REF_READBACK.json |

A is the existing PR207 case, B is its existing native_integration_preparation_01 helper folder. Root's actual95 acceptance must pass unchanged helper v2's acceptance contract, including expected-SHA force=false confirmed CAS. Actual sync/pointer must bind that acceptance, manifest, exact candidate/tree/facts, exact five postimages and actual sync path. All five local files must still equal those accepted95 source bytes. Neither a prospective gate nor a preparation report qualifies.

The original PR merge proof must use schema `pr207-root-actual-original-pr-merge-v1`, evidence_scope ACTUAL_ROOT_RECEIPT, integer PR207, accepted true, original_head/tree, actual_original_PR_head=a7f8486548122c7d545430821afeedbccf48b3e7, state closed, is_draft false, merged true, actual_original_PR_merge_commit, merge95_candidate/tree, actual_MAIN_observed=candidate. Field names are `actual_original_PR_state`, `actual_original_PR_is_draft`, `actual_original_PR_merged`; original identities use `original_head`, `original_head_tree`.

Ref readback schema is `pr207-root-native-ref-readback-v1`, evidence_scope ACTUAL_ROOT_RECEIPT, PR207,phase merge95,expected_parent,candidate,tree,parents,actual_MAIN_observed=candidate,accepted true, and `actual_PR:{state:"closed",draft:false,merged:true,head:<original HEAD>,merge_commit_sha:<actual native merge commit>}`. CAS intent/tool-result files remain raw separately pinned heterogeneous events; actual Root acceptance and independent native ref/PR observations provide the semantics.

Only after every local actual record/source pin is accepted does the builder create a fresh GET-only journal and inspect GitHub. Current MAIN must exactly equal accepted95 candidate, with exact parents/tree/message. The original HEAD/tree and actual ready PR207 must be closed/merged/non-draft, with the Root proof's exact native merge commit. Original HEAD ancestry is checked. Every prior311 selected native preimage tuple is authenticated through immediate tree SHA reconstruction. The actual five bodies and QUEUE body are fetched and compared byteexact. Fresh MAIN and local five are checked again before output and before the final source-freeze receipt. Concurrent progress refuses rather than broadening scope.

## Root control file

After actual95 CAS/acceptance/sync/PR merge, Root creates a canonical0444 control JSON **inside this new preparation folder**, then passes its byte count and SHA256 separately. Required fields:

- schema `pr207-root-completion100-freeze-control-v1`, evidence_scope ACTUAL_ROOT_RECEIPT,PR207,accepted true,prepare_sources_only true,no_ref_or_existing_view_write true.
- `candidate95`, `tree95`: the exact identities above.
- `builder_pin`: actual `{bytes,sha256}` for this frozen builder.
- `preparation_manifest_pin` and `preparation_seal_pin`: this folder's frozen public manifest/seal identities.
- `pins`: exactly the nine role names in the table, each a strict `{bytes,sha256}` for the actual corresponding file. Boolean byte counts are refused.

No example file with fabricated actual receipt pins is supplied. Do not use a planning or test record as control authority.

Once prerequisites actually hold and Root approves the source, the command is:

`python3 -E -S -B -P freeze_completion100_v2.py --control /absolute/owned/control.json --control-bytes N --control-sha256 SHA`

Do not invoke it under optimization. Ordinary flags are checked before arguments. Existing actual events may be ordinary canonical pinned files; the existing helper, operational manifest/source copies and synced five must satisfy the accepted sealed-source requirements. Every new source copy is exclusive0444 and fsynced with its directory. A partial output is not resumable or automatically retried; Root must inspect it.

## Exact proposed source changes

All311 previous selected paths remain selected. Exactly the five existing documentary views may receive different bytes. Native22, original archive20, whole accepted QUEUE, source science, known-priority attribution, code/runs, prior gate/review/publication/tracker evidence all remain byteexact. No extra full QUEUE snapshot or foreign subtree is archived.

The program JSON preserves the ordered prior49 completed IDs then appends only207, preserves every ordered published34 ID, and sets50 completed/34 published,last207,cursor208,advance true,goal false,percent100 and matching aliases/fraction. JSON changes use an explicit documentary-field allowlist; mathematical/source/readiness/priority fields are compared unchanged. Current JSON status explains that the separate Root actual completion100 receipt/pointer certifies native installation and exact local-five sync once this checkpoint becomes current. Before promotion these remain prospective source bytes; the builder creates neither receipt nor pointer. Historical dated freeze/log entries retain their truthful pending-at-freeze wording. The two research logs retain historical bytes and dated entries, remove only their one exact current95 marker, then append the dated100 source-freeze entry and one current100 marker. CURRENT_PROGRESS.md changes only exact documentary progress phrases/time/marker and adds the dated terminal-pending entry; scientific paragraphs remain unchanged. Its current header/native paragraph refers certification to the separate Root actual completion100 receipt/pointer, while the dated historical freeze entry records terminal acceptance/sync as pending at that moment. No next-case intake is performed.

New selected additions are a small fixed allowlist: the nine named actual/narrow records; previous operational manifest; Root source-input acceptance; the four public peer merge95 followup files plus its manifest/seal; this builder's four public prep files plus manifest/seal; and the prospective completion100 gate. No API receipt directory, private fixture or broad folder is recursively copied. New additions are bounded to30 paths. Completion gate roles reuse the already accepted scientific/whole-package/publication/tracker bytes and add only actual ready_PR_merge proof. No actual100 acceptance or pointer is fabricated.

Future output paths are B/phase_completion100_sources_01/, B/COMPLETION100_INPUTS_01.json, B/root_completion100_freeze_get_01/ (GET journal), and this folder's COMPLETION100_SOURCE_FREEZE_01.json. They do not exist in this preparation. The output manifest is checked by unchanged helper v2 but remains prospective until separately reviewed candidate generation, independent verification, external Root CAS/readback/acceptance and stable-lock local-five sync occur.

## Verification and remaining gap

`AST_CHECK_RECEIPT_V2.json` records syntax compilation without executing or importing the builder, AST checks for literal GET-only API calls and mutate=false, absence of direct network/subprocess imports and directory globbing, unchanged helper pin and exact current95 documentary phrase applicability. It is not an execution receipt or a claim that runtime preconditions already hold. Root must independently review the source and later all five generated diffs, actual-event links and complete resulting manifest before operational promotion.

`PREPARATION_MANIFEST_V2.json` is the exact four-file public allowlist. The seal pins it. Only this allowlist plus its manifest/seal should be archived for this preparation; future actual controls/journals/sources require separate review and allowlisting.
