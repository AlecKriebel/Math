# Independent preview-preservation implementation review

Checkpoint UTC: 2026-10-10T21:40:52.688930+00:00. Reviewer: papers_group_4. Initial completion estimate: 95%. Final checkpoint UTC: 2026-10-10T21:45:05.446235+00:00; completion estimate: 100%. Final result: PASS — 96 legacy/helper checks and 46 native checks, including all 25 direct-native records and the resolved native staged-session integrity gates.

## Scope and source

This review is independent of the implementer's tests. It uses exact saved public baselines and reviewed proposal files, fake request clients, and temporary effort-local directories. No credentials were loaded, no network request was sent, no Zenodo object was modified, and no proposal was edited.

The supplied Invenio snapshots and the separate independent source-design note establish that an omitted `files.default_preview` becomes `None` on draft PUT, and omitted `files.enabled` falls back to a service default. Sending original enabled, default preview and order as display settings carries no file entries or file contents. The shown update handlers do not assign order, so preservation depends on unchanged edit-copy order and strict read-back; any order drift must stop. See [source-design review](PREVIEW_PRESERVATION_SOURCE_NOTE.md).

## Native route — PASS after staged-session integrity hardening

Independent [native integration checks](NATIVE_PREVIEW_INDEPENDENT_CHECKS.json) cover all 25 actual eligible direct-native baseline/proposal pairs through fake stage and existing-record publish. The fake server independently reconstructs the intended native target using the receipt auditor's separate implementation, asserts only original display options accompany metadata/custom fields, and simulates missing draft OAI/generated file links. Every original public rich metadata field outside the patch, file entry dictionary, display setting, access/custom field, record/concept DOI, PIDs and complete version registry is preserved. Stage/read-back and publication drift probes stop on unexpected changes, and no create/newversion/upload/entry mutation route is used.

The initial fresh path passed 39 checks. An additional adversarial test identified a saved-session integrity gap: an altered saved target and equally altered live draft could agree without independently reconstructing the target before POST. Parent was immediately informed and maintained fresh-stage-only operation for the already-running batch, which created exact targets from frozen patches and rejected pre-existing sessions. After that batch, the implementer added `require_reviewed_session`: before publish it binds record/patch, exact saved original rich metadata/full files/parent/version/PIDs/access/custom fields to the baseline, validates the protected snapshot, and reconstructs the exact target using original plus frozen patch. It also rereads the unchanged original public record and complete version registry before checking the draft and issuing POST.

All 46 final independent native checks now pass. They include the original 25 baseline/proposal integrations plus altered staged target and matching draft, wrong session ID, altered original/protected snapshot, and public version/rich-metadata/full-file drift after stage; each unsafe case stops before publication. The checked current native hash is `6a797eca29794f5527255a6d499e04bb34222acf6c386b93da7f18aeabdd91ac`. The previous fresh-only signoff hash was `845ad83ec3011240b13525e46f3207ab7c356695297ed2447fc4c17a35fe2b6d`; the final hardening does not change canonical metadata translation or display options used by that completed batch.

## Owned legacy preview repair and recovery — PASS

All 96 independent [legacy/helper checks](PREVIEW_INDEPENDENT_CHECKS.json) pass. The helper requires the exact selected record, production environment, owned update_requested/staged phase, original legacy/native metadata, complete file inventory, DOI, patch fields and exact frozen target/hash. It reads unchanged original public rich metadata, full native files and complete version registry, then verifies the live pending legacy target and exact independently expected native target. Only original string-preview loss to None, with every other normalized file value unchanged, admits one display-only native PUT.

Its durable request receipt is saved before mutation; previous uncertain requests are not retried while preview loss remains. A successful recovery checks full files, rich metadata, PIDs/access and original public identity again, records raw before/after evidence, and creates a hash-bound recovery marker. Tests exercise the actual BoundClient.update hook, the selected recovery runner, and recovered run_one to existing-record publication. Raw old session/guard artifacts remain unchanged; repeated successful recovery is read-only and produces no second PUT.

The bound repair PUT rejects top-level PIDs/access, file entries, file arguments and any display configuration other than the original. Unknown records, create/newversion/file-content/upload/delete routes are rejected. The wrapper checks exact target, full file objects, PIDs/access/custom fields and identity on every draft read; immediately before publication it rereads original public rich metadata/files and the full version registry. A preserving-repair DepositError is made fatal instead of being swallowed by the legacy single-read uncertain-outcome recovery.

## Adversarial findings resolved

1. Mandatory helper translation initially rejected the already-reviewed 22770864 creator-order correction and 22929556 software-to-preprint correction. The implementer added exact selected-record exceptions preserving all author affiliations/identifiers and changing only the reviewed resource type. Independent tests cover the real patches and exact preserved native creator structure.
2. Native repair routes initially permitted arbitrary PUT payloads. The implementer added exact metadata/custom_fields/display-only payload gates, including refusal of entries/access/PIDs/file arguments. Independent unsafe-route and unsafe-payload probes pass.
3. A matching saved staged view and recovery marker could initially agree on an unreviewed extra native subject while the legacy projection stayed exact. Every draft read now reconstructs the expected native target from baseline plus reviewed patch; the forged matching pair stops before publish. Complete public version/file/rich-metadata drift also stops before publish.

## Bound code and reproducible evidence

Legacy/helper approval applies to these exact SHA-256 values:

- `preview_preservation.py`: `39d6055a0bb70506baec50d86ca62be4db12b899ac67985515bf226ce5191188`
- `repair_owned_preview.py`: `23ba851152e3e5d28053b7fa404456bbf4ddf00765137df0e6921f108108acb6`
- `apply_reviewed.py`: `14aa8d9bf3650e6d57c78684d1191ccda0d967c2d28ce98ad82f88baa1358cc9`
- `native_metadata.py`: `6a797eca29794f5527255a6d499e04bb34222acf6c386b93da7f18aeabdd91ac`
- `native_views.py`: `9e1ce726a3247eb2b2b9b044918a8ee8a5345b6360e853b51d34ae3f5b421a4f`

Reproducible offline scripts: [preview_independent_checks.py](preview_independent_checks.py), [native_preview_independent_checks.py](native_preview_independent_checks.py). They write only their own JSON test results and temporary local receipts, and do not execute real update/publication calls.

No implementation-review gap remains in the signed-off native and owned legacy repair/recovery flows, assuming the exact bound hashes and mandatory production record lock are used. Final public receipts must still be independently audited against original baselines and frozen scientific targets; these offline tests do not substitute for actual public receipt verification.
