# PR1268 guarded publication tooling

This sealed effort supplies code and offline evidence only. It creates no actual
paper, metadata, mathematical/priority PASS, current context, PDF, whole-package
approval, deposit, tracker row or PR modification. All positive reviews in the
fixtures are explicitly synthetic and remain in scratch. Root must supply real
accepted decisions and obtain the new independent whole-package review loop.
No inference about mathematical correctness, priority or novelty is made here.

## Deployment and identity

The following eight files deploy relative to this PR1268 audit:

| Authored source | Destination |
|---|---|
| prepare_package.py | publication/prepare_package.py |
| build_package.py | publication/build_package.py |
| compile_note.py | publication/compile_note.py |
| verification_verify.py | publication/verification/verify.py |
| append_tracker.py | publication/append_tracker.py |
| update_pr_publication.py | publication/update_pr_publication.py |
| check_public_downloads.py | publication/check_public_downloads.py |
| workflow_regression.py | publication/workflow_regression.py |

The uniquely named actual program/publication_coordinators/pr1268.py and
verify_pr1268_merge.py have also been written. Their exact in-family source
copies are deposit_coordinator.py and verify_pr1268_merge.py. INPUT_END_BINDINGS
records their explicit external paths/hashes and byte equality, never claiming
external paths as family authored membership. Do not copy the coordinator or
additional test bodies into publication/ as extra release helpers. The gate
must bind the actual operative coordinator separately, and complete-package
reviewers must freeze both actual coordinators explicitly.

Pinned PR1268/problem10900050/AMR-108-0050; original head
cecd7da6e8b5bb84b4294e169d940189b269a956; branch
research/10900050-prime-difference-counterexample; original body SHA256
80632e6a02d184fe4a5818161493a40b57af96a03a2cfd2f99e912c1e80d5162.
Base is unsolved_math_prioritization/attempts/10900050.

Exactly ten originals/current files are recognized: ACCEPTANCE.json,
ACCEPTANCE_REPORT.md, AUDIT_MANIFEST.json, EDITORIAL_MAP.json,
LITERATURE_CHECK.json, PROOF.md, PUBLIC_MANIFEST.json, README.md,
RESEARCH_LOG.md and SOURCE_MANIFEST.json. Actual original bytes, sizes, SHA256
and Git blob identities are authenticated against SUBMITTED_SNAPSHOT.json.
PUBLIC_MANIFEST has problem_id10900050, file_count10, and exactly nine nonself
files/path/bytes/sha256 rows. Its own identity is bound outside itself. No
MANIFEST.json/entries schema or old eight-file scope is assumed.

The final intended map is exactly fifteen paths: those ten and five files in
publication_20261017/: Prime_Difference_Counterexample_Note_v1.0.pdf,
Prime_Difference_Counterexample_Verification_v1.0.zip, zenodo-deposit.json,
PUBLICATION_RECEIPT.json and README.md. Every final byte is checked; changed
paths may be only those five additions when originals are preserved. A saved
publication commit has exactly the pinned original head as parent. Native Git
object creation/nonforce branch push remain later integration operations; the
shared index and checkout are never used by this code.

## Explicit context and two current-edition modes

CURRENT_PR1268_CONTEXT.json must supply exactly the standard context fields:
schema, pr, problem_id, original_head, original_branch, original_body_sha256,
title, expected_pdf_pages, source_date_epoch, edition_mode, edition_text,
structured_records, disclosures, metadata, publication_text, tracker,
authored_freezes, portable_files, diagnostic_replays, gate_bindings,
document_bindings. Schema is math-pr1268-current-context-v1.

Root chooses edition_mode after actual math/priority review:

- preserve_submitted: edition_text and structured_records must both be empty
  objects. Preparation copies all ten originals byte for byte, including their
  original PUBLIC_MANIFEST. Both local and portable guards compare EVERY current
  file to its authenticated original, so a rehashed current/outer manifest
  cannot substitute changed mathematical records.
- explicit_current: edition_text supplies exactly ACCEPTANCE_REPORT.md, PROOF.md,
  README.md and RESEARCH_LOG.md; structured_records supplies exactly the five
  other JSON records excluding PUBLIC_MANIFEST. All values must be explicit and
  nonempty. Preparation generates a current PUBLIC_MANIFEST over those nine.
  If historical hashes/edits/review claims are retained, root must clearly wrap
  them as history; this tooling does not invent acceptance or repair that prose.

MATH_GATE and PRIORITY_ADJUDICATION must each identify this exact target/head and
have literal status PASS; context carries outside hashes. Priority and context
must disclaim firstness/current openness. Publication wording/summary/priority
and verification scope come entirely from the supplied current context, never
from the1262 template's theorem. Extensive AI use/unrefereed/no external human
peer review/no formal certification are disclosed. No actual title or result
metadata is hardcoded except the target-specific artifact basenames.

Metadata has exactly eleven fields: title, upload_type, publication_type,
description, creators, access_right, license, version, publication_date,
keywords and related_identifiers. Require publication/preprint/open/version1.0,
ASCII title/description, explicitly supplied creator affiliations and bare DOI
identifiers. Title contains no raw angle signs. Description is angle-free plain
text or simple paragraph HTML whose text contains no raw less/greater signs;
use words or stable entities such as &gt; and &lt;. This rejects the raw comparator
HTML mismatch encountered earlier. Authors should explicitly encode intended
HTML characters; no server content normalization is accepted by the concrete
strict coordinator. A current metadata projection check is rerun after actual
metadata exists; these fixtures supplied no real metadata.

Expected page count must be the actual positive observed count. Epoch is an
explicit reproducible build stamp, separately from actual compile timestamps.
Successful actual compilation, current source/PDF hashes, independent pdfinfo
count and an actual every-page visual QA receipt are all required before build.
Compilation can bootstrap only identity/epoch; no fictitious layout is inferred.

## Explicit relative evidence and scoped replay

Every authored_freezes registration supplies exactly path, base, entries_key,
path_key, size_key, sha256 and role (optional path_mode only if relative). Roles
are math, priority, workflow or documentary; at least one actual math and one
actual priority family must be explicitly registered. Root registers every
actual sealed family once its exact schema is known. No folder-name guessing
or inherited1262 mathematical-family requirement exists. Supported relative
field triples include files/relative_path/size_bytes and authored_files/path/
bytes, as well as the other explicit SCHEMAS allowlist. Absolute membership
modes are rejected. Unused absolute inputs/source paths in original receipts
are never followed as membership. Canonical paths, physical component case,
case-fold collisions, symlinks and outside anchors are checked.

portable_files explicitly inventories retained path/bytes/sha256/role. Every
registered manifest/member must appear; source inventories are retained receipts
and do not imply omitted raw sources are archive members. Actual current and
original records are separately handled, not recursively treated as evidence
manifests. Portable integrity needs independently trusted root manifest,
current-context and original-snapshot hashes; self-computed archive hashes are
not outside trust anchors.

Diagnostics must explicitly declare program, mode, result, output_mode, scope,
layout, arguments and comparison. Use the source family's self-contained stdout
checker and an explicitly authored portable root math checker if root chooses.
Do not pretend repository-authentication scripts portable: a candidate script's
actual Git/absolute-REPO prerequisites, or a root repo-auth checker, cannot be
silently imported or bypassed by this wrapper. A separately authored scoped
math-only adapter requires its own honest description and frozen bytes. All
executions use temporary copies; assertions require normal mode with
PYTHONOPTIMIZE removed. Supported comparisons preserve exact payloads while
omitting only the explicitly selected top-level runtime fields. No automatic
bitwise floating comparison should be imposed without a justified contract.

## Gate and mutation guards

The actual final gate uses math-preprint-final-review-gate-v1/status pass and
binds all eight actual helpers, actual coordinator, unchanged shared kit,
source/PDF/ZIP/metadata/current context. At least two different new actual
chronologically sequential whole-package reviews are required, latest CLEAN
on current complete inputs. Earlier CHANGES_REQUIRED remains immutable history
and needs explicit root resolutions preceding that latest CLEAN. It does not
require two further clean-current rounds after repair. Review verdict schema
is math-pr1268-whole-package-review-v1; resolution schema is
math-pr1268-review-resolution-v1. Actual report/verdict/manifest/input freeze,
explicit authored schema, current code/artifact coverage and history/resolution
anchors are all verified. This tooling VERDICT has a different schema/status
and cannot count as that actual complete-package clearance.

Before any actual stage/publish, the operative coordinator installs strict
verification in the actual unchanged shared kit module. A fresh same-ID inspect
precedes publish and actual kit.run repeats GET/strict verify BEFORE its POST.
Every returned normalization is rejected. Stage/publish use exclusive one-
attempt intents; unknown creation/publication is reconciled read-only using
saved/account evidence, never by blindly creating/retrying. Live original
head/branch/body/draft and tracker uniqueness are checked before mutation.

Public verification checks canonical production DOI/record identity, exactly
two public files with exact bytes/SHA256, and ALL eleven supplied fields after
only explicit public-schema projection. Tracker uses the designated sheet/gid,
Math Puzzles tab/exact four headers, the entire four-cell row and blank B.
Intent precedes one append; accepted-but-lost responses recover only from one
exact matching row. Duplicates/collisions and wrong ranges fail; full row is
read back. PR helper checks exact original/current body, head/branch, intended
fifteen paths/blobs/parent, publication/public/tracker receipts, saved intents
and final remote/body readback, without index/force. Root must use expected-head
merge, e.g. gh pr merge1268 --merge --match-head-commit <reviewed-head> after any
authorized ready transition. No merge was issued here. Postmerge main verifies
actual reviewed head/body/two parents, fifteen merged bytes, unique exact row
and resolved DOI200 before advancing only1268 to1271. Its actual mathematical
and priority disposition text comes from context, not inherited prior claims.

## Evidence and outstanding integration

Three sealed receipts report identical normal/-O/-OO: WORKFLOW_REGRESSION,
ADDITIONAL_FAULT and EDITION_AND_PATH. These use synthetic compiler/pdfinfo,
review records and service/Git I/O. Actual shared kit.run is exercised with mock
clients; all eleven supplied fields and file/ID corruption stop before mock
POST. Actual postmerge main and full gate/saved-tree checks run on synthetic
inputs; head/body/parent/blob/duplicate/B/header/DOI faults cannot advance state.
Preserve10+only5changes, explicit-current mode, relative/case/role checks, safe
HTML, coupled manifest attacks, uncertain operation recovery and historical
review repairs are covered. Actual original10 snapshot/Git blobs and PUBLIC9
nonself bindings were authenticated in all modes; that is integrity only.

Native tree serialization/push, actual source compilation/rendering and live
GitHub/GWS/Zenodo integration are NOT claimed. The source of tree construction
was read; it preserves unrelated tree entries recursively. Additional test
mains write scratch receipts only; use worker or isolated scratch on later
reruns. Do not overwrite sealed durable receipts or rerun their generators.
Root must supply/review actual math/priority decisions, current edition mode,
source/paper, metadata, page QA, complete schemas/registries and scoped portable
diagnostics, deploy the eight exact helpers, rerun appropriate actual-data
checks, then commission the new independent complete-package review loop.
No other shard was contacted or inspected; no outreach was prepared.
