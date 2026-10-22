# PR1261 guarded publication tooling proposal

This is tooling only. No actual paper, context, mathematical acceptance, priority
clearance, metadata, PDF, deposit, tracker row or PR update was created. Nothing
here authorizes release. Actual mathematical and priority adjudication remain
with the root research effort. A later package needs different fresh independent
whole-package reviews after its final bytes exist.

## Authored files and deployment

All durable work is at this folder root. `_local/` contains ignored synthetic
fixtures and scratch output. No existing template, shared kit, submitted file,
other research family, Git index/ref/branch or service was modified.

| Proposal file | Future deployment |
|---|---|
| `prepare_package.py` | `publication/prepare_package.py` |
| `build_package.py` | `publication/build_package.py` |
| `compile_note.py` | `publication/compile_note.py` |
| `verification_verify.py` | `publication/verification/verify.py` |
| `append_tracker.py` | `publication/append_tracker.py` |
| `update_pr_publication.py` | `publication/update_pr_publication.py` |
| `check_public_downloads.py` | `publication/check_public_downloads.py` |
| `workflow_regression.py` | `publication/workflow_regression.py` |
| `deposit_coordinator.py` | `publication/deposit_coordinator.py` |

The first eight are exactly the required workflow hashes in a real final review
gate. The coordinator has a separate mandatory hash. The portable checker is
standalone; its root-level proposal filename avoids globally ignored authored
nested directories. The regression loader supports this proposal layout and
copies the checker to its deployed path only in ignored synthetic fixtures.

`TEMPLATE_INPUTS.json` records observed hashes of the eight read-only PR1241
templates, strict coordinator, actual shared Zenodo kit, original PR1261
snapshot and the two actual custom family manifests. Templates were used as
guards/structure, with this target's file/schema/title contracts rewritten.
`WORKFLOW_REGRESSION_RECEIPT.json` is synthetic offline evidence, not a real
package verification/reviewer receipt. `OFFLINE_VALIDATION.md` explains limits.

## Pinned target and seven/twelve counts

- PR: `https://github.com/AlecKriebel/Math/pull/1261`.
- Problem: `30003990`.
- Original head: `d1ecd7c4368f4909653a44db0c9ca4a5463e6552`.
- Branch: `convex-body-sos-30003990-reviewed`.
- Original body SHA256:
  `729ff3e25a2654fad80086dcb80197e064bb9d6418358d82483c8b7cc28fe77e`.
- Base: `unsolved_math_prioritization/attempts/30003990/`.

Original and current mathematical editions each have exactly seven files:
`ACCEPTANCE.json`, `AUDIT.md`, `MOMENT_FORMULATION.md`, `PROOF.md`,
`PUBLIC_MANIFEST.json`, `RESULT.md`, `SOURCE_VERIFICATION.json`.
Four current prose records and two current structured records come from the
explicit context. A generated current `PUBLIC_MANIFEST.json` binds the other
six via `members/path/bytes/sha256`, with `manifest_self_excluded: true`.
The historical original seven are never rewritten; their bytes, SHA256 sizes
and Git blob identities are independently checked against the snapshot.

The desired PR map is exactly twelve paths: those current seven plus
`publication_20261017/` containing these five:

1. `Convex_Body_SOS_Density_Note_v1.0.pdf`
2. `Convex_Body_SOS_Density_Verification_v1.0.zip`
3. `zenodo-deposit.json`
4. `PUBLICATION_RECEIPT.json`
5. `README.md`

There is no invented original `README.md`, `ACCEPTANCE.md`, `MANIFEST.json`,
`SOURCES.json` or `VERIFICATION.json`. Actual commit changed paths must be a
subset of the twelve desired paths, and every desired path's final bytes are
checked. This correctly permits a current record that is byte-identical to its
historical version; it does not require artificial edits merely to inflate a
diff count. A saved commit must have exactly the original head as its parent.
No shared Git index, checkout, force push or GitHub release is used.

## Explicit current context contract

The future root-authored audit file `CURRENT_PR1261_CONTEXT.json` must have
exactly these top-level keys (the code rejects extras/missing keys):

```
schema, pr, problem_id, original_head, original_branch, original_body_sha256,
title, expected_pdf_pages, source_date_epoch, edition_text, structured_records,
disclosures, metadata, publication_text, tracker, authored_freezes,
portable_files, diagnostic_replays, gate_bindings, document_bindings
```

`schema` is `math-pr1261-current-context-v1`; pinned identity literals are as
above. `title` is supplied later and must equal `metadata.title`. No title or
matching DOI from another problem is hardcoded. `expected_pdf_pages` is the
positive integer observed in the final current PDF; no eight-page assumption
exists. The fixtures deliberately use three pages.

`edition_text` has exactly `AUDIT.md`, `MOMENT_FORMULATION.md`, `PROOF.md`,
`RESULT.md`, each nonempty string. `structured_records` has exactly
`ACCEPTANCE.json` and `SOURCE_VERIFICATION.json`, each a supplied nonempty
object. These objects are copied exactly as supplied, rather than mined from
historical records or silently wrapped in acceptance claims.

`disclosures` is exactly:

```json
{"firstness_claim":false,"current_openness_claim":false,"ai_assisted":true,"unrefereed":true}
```

`publication_text` has exactly nonempty `summary`, `priority_statement`,
`verification_scope`; actual mathematical and source/priority wording belongs
here. `tracker` has exactly nonempty `original_problem` (including `30003990`)
and `notes`. Publication README/body and tracker rows add generic explicit
no-firstness/current-openness, extensive AI use and unrefereed disclosures.
They do not inherit another problem's theorem or priority statement.

`metadata` has exactly these eleven supplied public fields:

```
title, upload_type, publication_type, description, creators, access_right,
license, version, publication_date, keywords, related_identifiers
```

`upload_type=publication`, `publication_type=preprint`, `access_right=open`,
`version=1.0`. Use explicitly reviewed ASCII title/description punctuation and
text. Every creator must explicitly supply `affiliation` (JSON null allowed),
avoiding the kit's otherwise allowed null-affiliation normalization. Supplied
related DOI identifiers are bare `10....` DOI strings, not resolver URLs.
No release DOI is invented. The exact eleven-field projection is verified
publicly, mapping only upload/publication types to `resource_type` and license
to its public `{id:...}` shape. Server-generated fields are separate. No
punctuation, description, creators, list order or metadata content normalization
is accepted by the strict coordinator or public checker.

`gate_bindings` has exactly `math_gate_sha256`,
`priority_adjudication_sha256`, `submitted_snapshot_sha256`. Audit-root
`MATH_GATE.json` and `PRIORITY_ADJUDICATION.json` must each identify this exact
PR/problem/original head and have literal `status: "PASS"`; pending/fail or
`PASS_something` is rejected even if its digest is updated. The actual priority
record must explicitly disclaim firstness and current openness. Its final
source result and interpretation are supplied later; no matching publication
DOI or clearance is assumed here.

`document_bindings` has exactly `source_sha256`, `pdf_sha256`,
`compile_receipt_sha256`, `layout_receipt_sha256`, binding current
`publication/manuscript/main.tex`, `publication/output/pdf/main.pdf`,
`COMPILE_RECEIPT.json`, `LAYOUT_VERIFICATION.json`. Bootstrap the explicit
context with its epoch and pinned identity, compile, perform actual all-page
visual inspection, then fill these final anchors. Compilation reads only the
bootstrap identity/epoch, so it does not require a circular context digest.
Compilation receipts do not hash the mutable bootstrap context.

`source_date_epoch` is an explicit decimal-string reproducible build stamp.
It is not completion, compilation or publication time. `at_utc` records actual
compilation receipt time separately. Build also requires actual nonempty
compile/layout timestamps, exact source/PDF hashes, a successful compilation,
all pages visually inspected and independent `pdfinfo` page count. Successful
compilation alone does not claim byte determinism across compilers/caches.

## Freeze registry, portable evidence and replays

Every `authored_freezes` registry entry has exactly:

```
path, base, entries_key, path_key, size_key, sha256
```

All paths are canonical safe relative paths inside review/priority families.
`path` is the manifest, `base` is its family root, `sha256` is the outside
anchor for the immutable original nested manifest. No schema guessing occurs.
The allowlisted exact `(entries_key, path_key, size_key)` triples are:

```
(files, relative_path, size_bytes)
(authored_artifacts, relative_path, bytes)
(entries, path, bytes)
(entries, file, bytes)
(authored_files, path, bytes)
(files, path, bytes)
(all_authored_content_files, path_relative_to_authored_root, bytes)
```

Mandatory current-family registrations are:

```
reviews/source_question_family/manifest.json
  base=reviews/source_question_family
  entries_key=files; path_key=relative_path; size_key=size_bytes
reviews/analytic_adversary/MANIFEST.json
  base=reviews/analytic_adversary
  entries_key=authored_artifacts; path_key=relative_path; size_key=bytes
```

At least one final priority authored freeze must be registered, and all other
final authored freezes must be included explicitly. Both current-family
manifests also carry absolute `path` fields; those unused fields are never
followed. Their original schema and bytes remain unchanged in the archive.
The analytic `ignored_source_and_scratch_inventory` is receipt-only, not
portable authored payload membership. Original `PUBLIC_MANIFEST.json` is
separately checked through `members/path/bytes` over its six original entries.

`portable_files` explicitly inventories each retained file via exactly
`path`, `bytes`, `sha256`, `role`. Roles are `authored_evidence`,
`source_receipt`, `historical_receipt`. Every registered manifest and all its
frozen authored members must appear; duplicates and reserved package paths
are rejected. Authored manifest/freezes in this inventory must be registered.
Source inventories are ordinary retained receipts, never automatically
interpreted as manifests for omitted source bodies. Preserve the distinction
between read/retained sources, source receipts, authored diagnostic bodies,
and historical omitted-code claims in the actual current prose/records.

Each `diagnostic_replays` entry has exactly:

```
program, mode, result, output_mode, scope, layout, arguments, comparison
```

Programs/results must be retained inventory members. `mode` is `normal` or
`normal_O_OO`; `output_mode` is `stdout` or `file`; `layout` is `isolated` or
`original_submission`; `arguments` is `[]` or `["--output","{output}"]`.
`comparison` is `bytes_exact`, `json_exact` or `json_ignore_runtime` (only
top-level `run_utc`, `python`, `optimization` are excluded). Scope is explicit.
These are finite diagnostics, not proof/priority acceptance.

For the actual analytic checker, use its retained original program and
`layout=original_submission`, `arguments=["--output","{output}"]`,
`output_mode=file`, `comparison=json_ignore_runtime`. It receives an untouched
temporary copy at `root/reviews/analytic_adversary/<program>`, together with
`root/SUBMITTED_SNAPSHOT.json` and `root/submitted/<original seven>`. This
reconstructs the code's expected layout from archive `provenance/` and
`original_submitted/`; the archive itself is not falsely described as already
matching the historical layout. Frozen code is never rewritten. For actual
source-family code writing beside itself with essential assertions, choose
`layout=isolated`, `arguments=[]`, `mode=normal`, file output and exact bytes.
Only temporary copies execute; frozen original bytes are checked again after.

The portable checker requires three outside CLI anchors:

```
python -B verify.py --expected-manifest-sha256 <trusted-root-manifest-hash>
  --expected-context-sha256 <trusted-current-context-hash>
  --expected-snapshot-sha256 <trusted-original-snapshot-hash>
```

They appear in `BUILD_RECEIPT.json` and must be obtained from an independently
trusted reviewed/published receipt/artifact. Without outside anchors it fails
closed. Coupled outer-manifest/payload rewriting still hits immutable nested
anchors; rewriting context/registry too hits the outside context anchor. An
attacker replacing the checker itself must be excluded by trusted published
artifact checksums; no self-contained archive can establish its own external
authenticity.

## Actual review gate and mutation order

No real `FINAL_REVIEW_GATE.json` was written by this effort. Later, its schema
is `math-preprint-final-review-gate-v1`, status `pass`, target identity pinned.
It must bind all eight deployed workflow hashes, the coordinator hash, the
actual read-only shared kit hash (`shared_kit_sha256`),
source/PDF/ZIP/metadata/current-context hashes, and `reviews` of length at least
two with distinct reviewer IDs, strictly increasing actual UTC times and
`latest_review` exactly equal to the last record. Each review record supplies
`status=CLEAN`, `actual_review=true`, `reviewer_id`, `report`, `verdict`,
`input_freeze` and each corresponding SHA256. Evidence must be inside this
problem's `reviews/` tree. The literal verdict JSON itself must have schema
`math-pr1261-whole-package-review-v1`, actual CLEAN status, matching reviewer,
PR/problem/head/context, `input_freeze_sha256`, and actual ISO UTC `at_utc`.
A clean label outside a changed/nonclean verdict file is insufficient.

Reviewer input freezes use `files` plus `external_readonly_inputs` entries
with `path/bytes/sha256`. The validator checks every listed binding and requires
coverage of all eight deployed scripts, coordinator, source/PDF/ZIP/metadata,
compile/layout/build receipts, context, math/priority gates, snapshot and the
actual read-only shared kit.
Actual whole-package reviewers should also include all original/current
records and retained evidence. Context anchors
independently authenticate every frozen evidence member before mutation.

The coordinator loads the actual unchanged `zenodo_deposit_tool/zenodo.py`,
wraps its actual `verify`, and rejects every returned metadata normalization.
The wrapper is installed in the same module object that performs `kit.run`.
Thus the shared kit's second GET and strict verification occur inside its
actual publication path before its actual publish POST. A fresh same-known-ID
inspect is required first; a saved inspection is never authority.

Both stage and publish use exclusive-create intent files before their single
attempt. Unknown creation with no ID is an account/saved-ID read-only
reconciliation problem, not permission to restage. Unknown publication is
reconciled by inspecting the saved ID. If it is already published, canonical
same-ID DOI/record identity is checked and the receipt is recovered without
another POST. An existing unresolved intent and ready draft refuses retry.
The live original draft/head/body/branch and tracker uniqueness preflight is
repeated before publication. There is no extra consent gate.

After actual publication, public verification checks canonical production ID,
DOI and record URLs, all eleven supplied metadata fields, both public artifact
names, sizes and SHA256 hashes. Tracker A:D is the designated `Math Puzzles`
tab at spreadsheet `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`, gid
`1254632077`, exact headers `Original Problem|Solution Chat URL|DOI|Notes`.
Column B stays blank. Exact full-row identity, duplicate/collision refusal,
exclusive intent and full-row readback protect append/recovery. A renamed tab
is rejected. The PR update requires these publication/tracker/public receipts,
exact intended paths/blobs/parent and live body/branch checks, with idempotent
intent/body/remote readback. It never touches the shared index or force-pushes.

## Outstanding operational work

Root must supply the actual final paper, full mathematical/priority decisions,
current prose/structured records, bibliography/source receipts, metadata,
actual page count, final freeze registry and scoped diagnostics. Deploy only
after inspecting this proposal. Compile/render/inspect actual all-page layout,
freeze actual sources/artifacts, rerun the workflow against real metadata, then
obtain different fresh sequential independent whole-package reviews. The
synthetic reviewer records in these tests are explicitly fabricated fixtures.

No real Tectonic/PDF rendering, live GWS/Zenodo/GitHub integration, original
body-positive live preflight, Git object/tree creation or push was exercised.
Their guards were preserved/inspected and portions mocked; the concrete later
integration still requires actual read-only preflights and exact frozen bytes.
Metadata rejected by the server must be revised locally, reviewed/refrozen,
then reconciled through known state; normalization must never be silently
accepted or an uncertain deposit replaced.

No person was contacted; no other agent was messaged or delegated to. No
outreach was prepared. Original research/math/priority conclusions remain
outside this tooling proposal. The final authored freeze excludes its own
digest by necessity; the outside final handoff message reports that digest
and the handoff/report digests.
