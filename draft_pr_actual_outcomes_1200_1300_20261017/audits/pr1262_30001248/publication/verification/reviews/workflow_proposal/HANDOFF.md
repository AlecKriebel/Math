# PR1262 guarded publication workflow proposal

This is an isolated tooling proposal. No current paper, mathematical or priority
PASS, release metadata, compilation/layout receipt, reviewer approval, deposit,
tracker row, PR edit or merge was created. Nothing in this folder clears a real
release. Root must deploy and inspect the actual final package, then obtain new
sequential independent whole-package reviews.

## Deployment

Copy the first eight files without rewriting their bytes:

| Proposal file | Actual destination relative to the PR1262 audit |
|---|---|
| prepare_package.py | publication/prepare_package.py |
| build_package.py | publication/build_package.py |
| compile_note.py | publication/compile_note.py |
| verification_verify.py | publication/verification/verify.py |
| append_tracker.py | publication/append_tracker.py |
| update_pr_publication.py | publication/update_pr_publication.py |
| check_public_downloads.py | publication/check_public_downloads.py |
| workflow_regression.py | publication/workflow_regression.py |

Copy deposit_coordinator.py to the program's publication_coordinators/pr1262.py.
Copy verify_pr1262_merge.py to publication_coordinators/verify_pr1262_merge.py.
The operative coordinator is separately hashed by the final release gate. The
postmerge script must be an explicit external input of the fresh whole-package
reviewers. offline_fault_checks.py is an additional offline test body, not a
required eighth release helper or automatic portable diagnostic replay. Its
proposal tests intentionally expect actual metadata to be absent. The deployed
workflow_regression.py can additionally compare the actual supplied metadata
when it exists.

The proposal-layout fallbacks load the root-level portable checker and
coordinator only for offline synthetic fixtures. In deployment they resolve the
actual program coordinator and publication/verification/verify.py. No shared
kit, historical candidate, previous workflow, Git index, checkout, ref, branch,
external record or unrelated shard was modified.

## Exact identity and eight/thirteen scope

PR1262: https://github.com/AlecKriebel/Math/pull/1262

Problem 30001248, OWR-3473-009. Original head:
fb7b750865f3e220590f128661c487c5984bae75.

Original branch:
publication/triangle-modular-threshold-30001248-recovered-20261011.

Original body SHA256:
3ab8f23a031f563bb7b5367792af9b723b1d637ada5cc78d44c717197be51d3c.

Base: unsolved_math_prioritization/attempts/30001248.

The original and current editions each contain exactly these eight files:
ACCEPTANCE.json, ACCEPTANCE.md, AUDIT.md, MANIFEST.json, PROOF.md, README.md,
SOURCES.json and VERIFICATION.json. Current explicit prose is exactly the four
Markdown files; current structured records are exactly ACCEPTANCE.json,
SOURCES.json and VERIFICATION.json. MANIFEST.json is generated from those seven
records with problem_id=30001248, members equal to the eight unique filenames,
self_hash_excluded="MANIFEST.json", and exactly seven nonself entries using
file/bytes/sha256. The historical manifest has that same selected field shape.
The original eight files remain byte-identical and independently checked for
size, SHA256 and Git blob identity against SUBMITTED_SNAPSHOT.json.

The exact final PR map has thirteen paths: the eight current records and five
files in publication_20261017/: Triangle_Modular_Threshold_Note_v1.0.pdf,
Triangle_Modular_Threshold_Verification_v1.0.zip, zenodo-deposit.json,
PUBLICATION_RECEIPT.json and README.md. No old seven/twelve contract remains.
The helper verifies every desired final byte; changed paths may be a subset of
those thirteen when some records are unchanged. The publication commit has
exactly the original head as its sole parent. Git objects preserve all unrelated
tree entries; the index and checkout are unused and pushes are not forced.
Native Git tree creation/push is source-reviewed, not executed by these tests.

## Current context and fail-closed material inputs

Root must supply CURRENT_PR1262_CONTEXT.json at the audit root with exactly:

schema, pr, problem_id, original_head, original_branch, original_body_sha256,
title, expected_pdf_pages, source_date_epoch, edition_text, structured_records,
disclosures, metadata, publication_text, tracker, authored_freezes,
portable_files, diagnostic_replays, gate_bindings, document_bindings.

The schema is math-pr1262-current-context-v1; all identity fields are pinned.
The title must equal the supplied metadata title. No theorem or priority result
from PR1261 is inherited. publication_text has exactly summary,
priority_statement and verification_scope; tracker has original_problem
(including 30001248) and notes. These actual context strings drive public
wording and the final disposition. expected_pdf_pages is the positive observed
page count, never a previous paper's count. source_date_epoch is a chosen
reproducible build stamp, while actual receipt times are recorded separately.

The exact disclosures are firstness_claim=false, current_openness_claim=false,
ai_assisted=true, unrefereed=true. Release wording records extensive AI use, AI
internal reviewing agents, unrefereed status, no external human peer review and
no formal proof-assistant certification.

metadata must have exactly eleven fields: title, upload_type,
publication_type, description, creators, access_right, license, version,
publication_date, keywords and related_identifiers. Values require publication,
preprint, open and version 1.0. Title/description are explicit ASCII text;
creator affiliation is explicitly present (null is allowed); related DOI
identifiers use bare DOI strings. There is no invented current metadata or
prospective release DOI. All eleven fields are compared publicly after only
the documented public-schema projection, without content normalization.

MATH_GATE.json and PRIORITY_ADJUDICATION.json must identify the exact PR,
problem and original head and have literal status PASS. Priority must explicitly
disclaim firstness/current openness. gate_bindings supplies their exact hashes
and the original snapshot hash. document_bindings supplies source, PDF,
compile-receipt and layout-receipt hashes. Missing material inputs fail closed;
no acceptance placeholder is created. Bootstrap compilation may read only the
identity and epoch; final building requires successful actual compilation,
current source/PDF hashes, actual receipt timestamps, independent pdfinfo count
and recorded visual inspection of every page. A compile success does not claim
byte determinism across environments.

## Explicit immutable evidence registry

Each authored_freezes registration explicitly supplies path, base, entries_key,
path_key, size_key and sha256. Supported triples are in SCHEMAS in the portable
checker; no guessing is performed. Mandatory current registrations are:

- reviews/source_question_family/manifest.json using files/relative_path/size_bytes;
- reviews/analytic_adversary/MANIFEST.json using authored_files/path/bytes;
- at least one final priority family manifest, explicitly declared.

Root must reconcile these exact shapes with the actual sealed family manifests
before deployment and final review. All other retained authored freeze manifests
must also be registered explicitly. The authored manifest for this tooling
proposal uses authored_files/path/bytes. Root must preserve the original seals,
not rewrite them to fit a different guessed schema.

Legacy members/path/bytes, authored_members/path/bytes and
authored_outputs/path/bytes require the explicit
path_mode=absolute_under_family_root opt-in. The selected absolute root key is
family_root by default or explicitly review_root. Normalization is lexical and
requires the expected family suffix; original host paths are never opened.
Unused source/input/absolute fields are receipts, not package membership.

portable_files explicitly lists path/bytes/sha256/role for retained payloads.
Every registered freeze and authored member must be included. A source
inventory is not interpreted as proof that omitted third-party bodies are
retained. The archive binds the exact original eight records, current eight,
context, gates, source and actual compilation/layout receipts. It requires three
outside trust anchors: root manifest, current context and submitted snapshot.
The archive cannot authenticate replacement of itself without an outside trusted
checksum.

Declared diagnostics supply program, mode, result, output_mode, scope, layout,
arguments and comparison. Only the specified top-level runtime keys may be
ignored. Original-submission-layout diagnostics receive temporary copies of all
eight originals and the snapshot; frozen program bytes are never changed.
Assertion-dependent diagnostics must remain normal-only. The offline workflow
suite and additional suite are not implicitly portable replay contracts; they
need compiler/kit/template dependencies that must be accounted for separately.

## Actual review and mutation guards

FINAL_REVIEW_GATE.json must use math-preprint-final-review-gate-v1, status pass,
pinned identity and exact eight deployed helper hashes, operative coordinator
hash, actual shared kit hash, source/PDF/ZIP/metadata/current-context hashes.
There must be at least two distinct, actual, chronologically increasing NEW
whole-package review rounds. The latest must be CLEAN on the current complete
frozen input set. Earlier CHANGES_REQUIRED evidence remains historical and may
have older context/artifact hashes; it requires explicit anchored root
resolution items, completed before the later CLEAN. It does not require two
CLEAN-current rounds after repair. The validator binds report, verdict, authored
manifest, input freeze and their explicit schemas/hashes. Latest input coverage
includes all actual package/code/context/gates/evidence and earlier reviews and
resolutions. The fresh whole-package verdict schema is
math-pr1262-whole-package-review-v1; root resolution schema is
math-pr1262-review-resolution-v1.

The unchanged actual shared Zenodo kit is loaded and its actual verify function
is wrapped strictly before every kit.run. Any permitted generic-kit metadata
normalization is rejected by this wrapper. Publication first obtains a fresh
same-known-ID inspection; kit.run performs another GET and strict verify before
its actual publish POST. Stage and publish create exclusive one-attempt intent
files. Unknown creation requires account/saved-ID read-only reconciliation;
unknown publish requires inspecting the known ID. A confirmed published record
is recovered without another POST. A ready draft with an unresolved intent is
not retried. Live original draft/head/branch/body and tracker uniqueness are
checked before mutation. No additional permission question is introduced.

After publication the public checker verifies canonical production record/DOI
identity, all eleven metadata fields, both exact filenames, bytes and SHA256.
Tracker operations use GWS CLI against spreadsheet
1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20, gid 1254632077, tab Math Puzzles,
exact headers Original Problem|Solution Chat URL|DOI|Notes and four full cells
with B blank. Intent precedes the one append. Accepted-but-lost append outcomes
recover only from one exactly matching full row; duplicates/collisions fail.
The exact resulting A:D range is read back.

The PR helper requires public/tracker/actual-review receipts, expected original
parent, intended thirteen paths, exact body/head/branch, saved intents and final
remote/body readback. Root's merge operation must use the reviewed publication
head as the expected head, e.g. gh pr merge 1262 --merge --match-head-commit
<reviewed-head>, after any authorized draft-ready transition. This proposal does
not issue that operation. The postmerge verifier independently checks the merged
API head/branch/body, expected second merge parent, every one of thirteen merge
blobs, the unique exact tracker row and successful DOI200 before advancing
program state from1262 to1268. Its disposition wording and PDF pages come from
the actual current context. It fetches only the immutable merge object into this
program's own ref; it never modifies the checkout/index.

## Offline evidence and remaining work

WORKFLOW_REGRESSION_RECEIPT.json and ADDITIONAL_FAULT_RECEIPT.json each report
identical successful normal/-O/-OO runs. All compiler/pdfinfo/service/Git calls
in synthetic fixtures are mocked. The actual unchanged shared kit.run is
exercised with a fully mocked client. Every supplied metadata field plus file
size, checksum, missing/extra files and wrong ID is rejected before a mock POST.
Unchanged metadata permits exactly one mock POST. Actual adapted postmerge main
uses the actual full gate and saved-tree validators and passes success→1268;
eight faults (head, body, merge parent, merged bytes, duplicate row, column B,
headers and unresolved DOI) are rejected without state advance. The actual
current eight historical Git blobs and seven nonself manifest entries are also
authenticated read-only, separately from synthetic acceptance evidence.

The proposal itself underwent no independent full-package review. Root must
supply real math/priority gates, current prose/structured records, paper,
metadata, observed layout, final authored registries and exact actual bytes;
rerun deployed checks; obtain different fresh whole-package reviewers in
sequence; then publish, verify public bytes, append/read tracker and merge with
expected head. This preserves human authorization already supplied without
pretending synthetic fixtures clear a release. No person was contacted, no
outreach was prepared, and no other shard was inspected or messaged.
