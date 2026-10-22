# PR280 narrow operational repair after completed reviewer02

Both requested defects have local code repairs and passing offline controls. **A new independent complete reviewer03 is still required. No scientific clearance, publication readiness or lifecycle outcome is asserted.** No GitHub, Zenodo, GWS, Git/index/ref or unrelated local-state mutation was performed.

Only two canonical helpers changed: `publication_live_gates.py` and `record_publication_ledger.py`. The other five helpers are byte-identical to reviewer02’s binding. `CURRENT_HELPER_BINDING.json` supplies all seven current SHA-256 values and their old identities; `REPAIR.diff` contains the complete exact two-file diff.

## Historical preservation and reproduced failures

Before any canonical edit, all16 files from historical preparation manifest SHA256 `999852717308827d82c11825f1ccb727be39da786fa5a1f34a6dde229c26c6e5`, plus that manifest itself, were verified and copied with audit-relative paths into `publication_operations_preparation/prior_review_02_full/`. `PRESERVATION_RECEIPT.json` records all seven old helper hashes and the16-entry verification. All17 copied files and the original historical manifest remain unchanged. Original preparation evidence files also remain unchanged. That old manifest is historical and must be verified against its preserved snapshot; it is **not a seal of the two repaired canonical helpers**.

The completed reviewer02 REPORT, VERDICT, actual independent operations counterexample code and both result files were read. `REVIEW02_READ_RECEIPT.json` pins those read-only sources. Reviewer02’s completed review and all its sealed artifacts were left untouched.

`reproduce_old_findings.py` executes exact preserved old helper sources, with read-only runtime paths resolved to the canonical location and all provider boundaries trapped. `OLD_FINDINGS.json` and `OLD_FINDINGS_OPTIMIZED.json` freshly reproduce both defects in normal and optimized Python:

- P280-OPS-01: the actual old gate accepts an exact target row marked as a non-target exemption, loses it from target_rows, and the actual old append function makes one synthetic duplicate append before rejecting at readback.
- P280-OPS-02: the actual old gate accepts a fully metadata/files-bound distinct record without local state, then rejects solely after adding that record’s unrelated synthetic state, both before integration and with target ID999.

These failed old behaviors are retained as evidence, never relabeled as passing repaired behavior.

## P280-OPS-01 repair

The repaired gate checks the current exact DOI anywhere in the row, including Notes, **before** applying any non-target digest exemption. If a row bearing that DOI is also in root ledger exemptions, it rejects the contradictory classification. Without that contradiction, one exact desired row is accepted only in the permitted idempotence phase and is counted in target_rows; changed wording, an unexpected current-DOI row and duplicate target rows reject. Ordinary explicitly reconciled non-target rows remain eligible for exemption.

The append function independently rejects a current-DOI row hidden by any root digest exemption before filtering or mutation, even if its upstream gate is stubbed or bypassed in a test. Its existing unfiltered full-sheet DOI check still rejects changed-notes same-DOI rows and duplicate DOI rows. Readback also preserves current-DOI rows before any non-target filtering. Thus a contradictory exact-target exemption produces **zero append calls**. A correct exact existing row remains idempotent with zero append calls. Only a verified absence path makes one append after the durable intent.

## P280-OPS-02 repair and root schema

The root reconciliation gains the optional field below. Omitting it means no unrelated local state is exempt. Every entry must have **exactly** these four fields:

```json
{
  "unrelated_local_state_exemptions": [
    {
      "path": ".zenodo-state/metadata-101-production.json",
      "sha256": "<actual 64-character lowercase SHA-256>",
      "deposit_id": 101,
      "disposition": "distinct_non_target"
    }
  ]
}
```

The ID101/name above is synthetic schema illustration, not an actual root classification or exemption. No root reconciliation or clearance was authored by this repair. The parent must decide identity using fresh private full-account/full-ledger evidence and bind the actual path/hash/ID it reviewed.

For each exemption the actual gate requires:

- An exact positive integer ID, never bool/float/string, that is already a root `distinct_non_target` account lead whose complete metadata and entire files projection have just matched the saved digest. The current target ID and unknown/unbound IDs cannot be exempted.
- An exact normalized repository-relative path consisting of `.zenodo-state/` and one JSON filename. Absolute paths, traversal, aliases, other directories, nested paths, symlink files and symlink directories reject. The actual regular file must exist.
- Exact SHA-256 of the actual current file bytes, a parsable JSON state, and the same exact integer `id` (or the collector’s existing `deposit_id` fallback). A changed observed or actual path/hash/ID rejects.
- No duplicate path, duplicate ID, conflicting entries, extra/missing fields, wrong disposition, or malformed root/observed lists. The contract deliberately permits one explicit unrelated file per unique ID; ambiguity requires root reconciliation.

The current target’s legitimate state remains a target-state observation, never an unrelated exemption. Valid non-target exemptions work before integration and in later phases. All matched unreviewed non-target state remains rejected by default. The helper only reads files and returns the accepted exact bindings; it never edits or removes a state file.

The parent reported a real broad-keyword match in its private initial collector. This child did not classify that article or copy any account/ledger body into public evidence. The schema repair enables the root to represent its own exact verified distinct-state decision without deleting unrelated state.

## Verification

All guards use explicit checks rather than production `assert` statements.

| Suite, each normal and optimized | Accept | Reject | Total | Provider attempts |
|---|---:|---:|---:|---:|
| New P280-OPS-01/02 hostile/idempotence/exemption controls |11|62|73|0|
| Preserved original regression control logic, repaired current helpers |22|136|158|0|
| Combined repaired controls per mode |33|198|231|0|

New `repair_controls.py` calls actual gate and append functions with synthetic providers, account records, ledger rows and temporary state files. It independently tests the append layer with the gate bypassed so gate rejection alone cannot mask a duplicate-append bug. Covered cases include exact desired-row idempotence, contradictory target exemptions at both layers, current DOI only in Notes, changed notes, duplicate exact DOI rows, ordinary non-target rows, target absence; valid unrelated-state exemptions before integration and later; changed path/hash/ID/bytes; unknown and current-target ID; unsafe/symlink/missing/non-file paths; duplicates/contradictions; strict ID/schema types; and missing/changed full account projection bindings. Every synthetic state fixture is checked byte-identical across the actual gate call, including rejected cases.

`replay_regression_controls.py` reads the exact preserved158-control source, checks its old hash, and changes only scratch/output locations before executing it against the repaired canonical helpers. It writes into `regression_normal/` and `regression_optimized/`, leaving historical test source/results/seals untouched.

`LOCAL_STATE_PRESERVATION.json` records an identical before/after aggregate inventory for all314 actual local state files: digest `1d241f0c6e2450ec0df942bf36bfe438f937d5ad530414028b3b47fcf827010b`. No state file was changed or deleted. The public receipt contains only aggregate counts/digest, not private bodies or the full state inventory. The scientific five release payloads and release manifest remain byte-identical to their frozen binding; original17 and historical scientific/package seals were not edited.

From the PR280 audit directory, reproduce without any provider action:

```text
PYTHONDONTWRITEBYTECODE=1 python3 ops_repair_20261021/reproduce_old_findings.py
PYTHONDONTWRITEBYTECODE=1 python3 -O ops_repair_20261021/reproduce_old_findings.py
PYTHONDONTWRITEBYTECODE=1 python3 ops_repair_20261021/repair_controls.py
PYTHONDONTWRITEBYTECODE=1 python3 -O ops_repair_20261021/repair_controls.py
PYTHONDONTWRITEBYTECODE=1 python3 ops_repair_20261021/replay_regression_controls.py
PYTHONDONTWRITEBYTECODE=1 python3 -O ops_repair_20261021/replay_regression_controls.py
PYTHONDONTWRITEBYTECODE=1 python3 ops_repair_20261021/seal_repair.py --verify
```

Replaying tests intentionally refreshes only new repair test receipts and therefore changes the current repair seal inputs. Verify the delivered seal before replaying, and place independent rerun outputs in a reviewer’s own directory or reseal only an explicitly new checkpoint. Historical manifests/results are never regenerated.

## Handoff

Repair implementation and evidence completion estimate: **100%**. Independent acceptance and publication work remain pending. The new repair manifest separately binds all seven current helpers, all new repair artifacts, the17 preserved old files, and the unchanged original historical manifest/seal checksum. It does not overwrite or reinterpret the historical seal.

The parent should verify this new seal, inspect both exact diffs, reproduce the controls in separate custody, and assign a new history-free complete reviewer03 across the frozen five-file package and all seven current helpers. Any future root clearance must pin all seven current helpers **and** the actual root-authored lead reconciliation containing any local-state exemptions, along with its full report/seal evidence. Existing scientific/package/lifecycle gates remain mandatory. No publication-ready claim or live operation is authorized by this repair report.
