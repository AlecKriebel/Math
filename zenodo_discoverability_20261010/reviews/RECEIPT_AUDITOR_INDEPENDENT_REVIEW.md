# Final repair disposition: pass

Checkpoint: 2026-10-10T21:38:02.588826+00:00. Independent repair-review effort: 100% complete. **The repaired receipt auditor and completion report builder pass this review.** No material unresolved false-pass path remains among the claims and controls reviewed here. Actual publication is still in progress; this is a workflow review disposition, not a claim that every paper update is complete.

The latest production audit checkpoint records 44/73 passing completed public receipts, 29 pending and 0 failures. Its 16 official falsification controls pass and are bound to the current auditor bytes. All 73 frozen original-baseline entries were hash-checked in the independent recheck. The all-versions scope now contains 97 explicitly catalogued records and the approved paper scope contains 73 records, including the independently reviewed earlier Yang–Baxter paper.

The receipt auditor now binds original record DOI and concept identity to the immutable original inventory, augmenting it only with missing entries from the recorded all-versions discovery. It requires the exact public OAI identifier/provider, correct record-bound native public file links, and original full native public parent ID. Its append-only baseline hash manifest catches coherent later changes to both original/final rich metadata, file dictionaries or version registries. Complete original public identity, full version list/count, metadata and files remain required at the final boundary. The special 21699069 alternate original public snapshot remains narrowly bound and the draft-only DOI/OAI/file-link representation exception still has an independent first-record check.

The completion builder now requires a globally passing audit, a passing first-record representation check, current successful falsification controls, current auditor source hash, current baseline-manifest hash and each original receipt hash. It additionally checks every whitelisted raw receipt artifact named in the per-record audit hash dictionary and both raw first-record evidence hashes. It also requires a passing current native route audit bound to its four current source files; the separate native workflow agent owns that route-content certification.

Independent repaired-auditor controls: **8/8 pass**, including unchanged positives before/after the mutants, jointly altered concept identity, jointly removed OAI, jointly changed file link, contradictory full native parent ID, jointly altered native affiliation and jointly expanded version list. These mutants exist only in cloned temporary data.

Independent completion-gate verification rejects the original global-audit failure, stale/failed controls, stale auditor code, stale baseline-manifest hash and rebinding an incorrect original baseline digest. The final raw-evidence controls are **5/5 pass**: fresh positive, stale native-public parent receipt rejected, stale first guard-stop DOI rejected, stale draft/public file-comparison evidence rejected, and fresh positive after restoring all evidence. The final positive fixture includes the newly added native route audit and its exact current source files. An intermediate positive fixture omitted that newly introduced gate and was correctly incomplete; this was a fixture update, not a tool defect.

Current independently tested source bytes:

- `audit_receipts.py`: `7529b1cab6bcca02cd0bd0cc5227700147d5e53bfda344f12b4151c0fa5b6466`.
- `build_results.py`: `369518b3337d63fcde331597dce7ed1a8ebc35684958480b38a7de9b3de44fa0`.
- Original-baseline manifest at this checkpoint: `c315fe7246e139439296a00d44c314129abf46516e376249d740f0798075a197`.

Checkable histories and repair controls remain in [RECEIPT_AUDITOR_INDEPENDENT_CONTROL_RESULTS.json](RECEIPT_AUDITOR_INDEPENDENT_CONTROL_RESULTS.json) and [BUILD_RESULTS_INDEPENDENT_CONTROL_RESULTS.json](BUILD_RESULTS_INDEPENDENT_CONTROL_RESULTS.json). No network, credential, publication, Git, approved-patch edit or actual receipt edit was performed by this reviewer.

The remaining trust boundary is explicit: local hashes freeze the recorded authenticated API snapshots and detect later local drift; they cannot retroactively authenticate those API responses, re-download file bytes, or prove manuscript results. The actual snapshots and native/inventory consistency checks establish the original capture provenance within the recorded workflow.

---

The initial findings below are preserved as history. Their missing checks were repaired and independently verified above.

# Independent adversarial review of receipt auditor and completion gate

Checkpoint: 2026-10-10T21:31:40.781635+00:00. Review effort: 100% complete; fixes and final live publication remain with the parent. Read-only remote scope: no network/API/client/token/Git operations, and no approved patch or actual receipt was modified. Temporary cloned data supplied all mutation controls.

## Actual-data result

At the independent checkpoint, all 23 completed public receipts passed `audit_one`; 49 records remained pending and none failed. The current 72 approved IDs are distinct and match all 72 catalog entries classified as papers. Native reconstruction preserves whole original author objects while adding ORCID, whole pre-existing related-identifier objects, non-note additional descriptions, all unpatched native metadata, and full file dictionaries. Intended resource/language/reference controlled-vocabulary labels are the only display-label normalization. No actual DOI, OAI, concept, version, file, author, or scientific-scope corruption was found.

The 21699069 exception is confined to that ID and an empty initial inventory file list. It binds the baseline file projection, full file dictionary, native metadata/PIDs/access/custom fields, and concept PIDs/local version flags to the pre-discard published native snapshot. This is a justified alternate public baseline for a known pre-existing pending legacy projection; it is not a general omission allowance. Complete version IDs/count still come from the separate before/after identity snapshots.

## Material false-pass paths in the reviewed auditor

1. **Original concept identity not bound to inventory.** `audit_one` binds original legacy metadata/files but initially did not compare `before.conceptrecid`/native parent ID to `INVENTORY.conceptrecid`. In cloned 23271172 receipts, changing both before/after concept ID to 99999998 and both parent DOI values coherently left every audit check passing. Add the direct original-inventory record/DOI/concept identity check.

2. **Full native publication receipt parent ID unchecked.** The optional `native_published.json` branch checks record ID, full metadata/files/PIDs/access/custom fields, parent PIDs and local version flags, but initially omitted `rec.parent.id`. A cloned full native publication receipt with parent ID 99999998 and unchanged parent PIDs passed. Bind the parent ID to the original identity.

3. **Trust boundary for before snapshot not frozen.** Coherent deletion of OAI from both before/after native+identity PID dictionaries passed, as did coherent modification of an original file content link in both full native file dictionaries. These controls alter the claimed baseline itself; they are not evidence of a real remote alteration. The first-record separate file comparison detects the paired file-link alteration only for that first record. Exact original public OAI presence/identity and an append-only approved baseline hash manifest are appropriate safeguards for reruns. Full before/after equality otherwise proves preservation relative to the captured baseline rather than authenticity of the original capture.

Checkable cloned-control outcomes: [RECEIPT_AUDITOR_INDEPENDENT_CONTROL_RESULTS.json](RECEIPT_AUDITOR_INDEPENDENT_CONTROL_RESULTS.json). The positive control passed and all four intentionally bad controls also returned pass in the originally reviewed code. The parent was told immediately and is adding inventory identity binding, exact public OAI validation, native parent-ID comparison, and the baseline hash manifest. No claim that these fixes are verified is made here.

## Completion report gate

`build_results.py` correctly refuses completion until every approved record has public receipts and matching per-record audit/input hashes, and until all owned all-version record IDs receive catalog scope dispositions. At the checkpoint, 97 owned IDs versus 78 catalog entries leaves 19 safely unaccounted; this is expected bookkeeping, not a publication failure.

The original completion predicate nevertheless omitted three material global checks. A temporary single-approved-record fixture using the real 23271172 receipts, proposal, content review and source text returned **complete=true** when (a) global independent `audit.status` was `fail` because first-record representation failed; (b) falsification controls had `all_passed=false` and `same_audit_tool=false`; and (c) `audit_tool_sha256` did not match the current auditor. Per-record status/hash checks remained valid in these controls. Completion must require the global passing audit, passing first-record representation, passing controls against the current audit source, and current baseline-manifest hash binding.

Checkable gate controls: [BUILD_RESULTS_INDEPENDENT_CONTROL_RESULTS.json](BUILD_RESULTS_INDEPENDENT_CONTROL_RESULTS.json). This is a schema-valid minimal local fixture to isolate the predicate; it does not describe actual completed account scope. The parent was told the findings promptly.

## Evidence and limits

- Approved proposal manifest SHA-256 observed: `87e3343200bd569256998acf9f00de81f61403eb2bbfe997737606bae9e043d5`.
- Inventory SHA-256 observed: `29614750d35819761a505a882bbe2aa081bd48f207c9937654e87e794d3df8ca`.
- Catalog SHA-256 observed: `077b7af02c0e9e596b21ceaa7aa8d58fe56740b2dd77dd3d91e69cfd73c3ff71`.
- Completion-report source SHA-256 observed: `08bb674641df0012510392f7141b628970d52b383230f80718a776647c18a0d0`.
- The auditor and controls were inspected at field/path level; passing actual receipts were evaluated with the independent module, without rewriting the production audit outputs.
- Existing receipt controls already catch after-only DOI, concept DOI, version, OAI, file-link/hidden-access, affiliation, scientific-scope, unsupported subject, language, and frozen-patch alterations. They originally exercised one public record, so native-rich creator/notes/resource/reference reconstruction and baseline-coherent controls require additional fixtures.
- A disk-only audit cannot authenticate an API response independently, download unchanged file bytes, or certify mathematical results. Original recorded API provenance and the frozen snapshot trust boundary must remain explicit. These limitations do not imply a remote problem was observed.


