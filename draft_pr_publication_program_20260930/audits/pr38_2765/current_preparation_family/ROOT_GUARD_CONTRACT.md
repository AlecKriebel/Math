# Root-only PR38 administrative guard contract

This is a proposed static interface to the actual root collector. The current
packet cannot exist on the strength of this contract alone. Root must fully
read all sources, finish actual reproduction, retain actual failures and
successes, and supply explicit final hashes. Missing, stale, differently
shaped or false evidence fails closed before the candidate is published.
Preparation makes no primary-reading, mathematical PASS or replay claim.

## Explicit execution pins

The builder requires `--execute`, `--root-receipt` (default
`ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json`) and its SHA256,
`--root-replay-script` and its SHA256, exact root scope SHA256, root read-ledger
SHA256, and root retention-manifest path/SHA256. The optional additional support
manifest requires both path and hash. All paths are audit-relative. The scope
certificate remains exactly
`4e042ef2328c73cf871627ccf15c3ffe98366019c67c34951a7d9a221e1a47fa`.
The read ledger must bind that certificate and describe completed direct root
reading. Its actual future hash is supplied explicitly. Its dated pending
replay field is not silently changed into an earlier proof event.

The final actual receipt is the collector's original full receipt, not a
second invented summary. It must have status PASS, exact head
`980719c79e13ffbc3f5cfbf149c325ea2fb51df0`, base
`c6975ca76f9f667f1250ba403d0e6da2aafe14d0`, original-file count16, changed-path
count17, closed-family count3, all169 before-and-after members, original2/5,
new0/audit0, root wrapper path/hash, actual executed collector path/hash, and
the exact read-ledger path/size/hash. No total of future actual runs or output
files is hardcoded.

## Complete actual evidence

`provenance` must be the entire actual inspect_source_native result:
PASS_READONLY_PROVENANCE_REPRODUCTION; complete flat source object; every
original16 Git path/mode/blob/size/SHA; original17 changed paths; whole raw
149266659-byte corpus;15458 problems;6701 reports; entire read-only SQL importer
join; SQL `ro, immutable, query_only`; exact statement/native-pair hash; absent
raw report key; original literal null; qualified native empty fallback; and
initial native target absent in state/history, queued0 in the catalog. Full
source object equality is independent of ASCII/Unicode stored serialization.

`original_replays` has exactly the two original programs in author/reviewer
order. Each row must bind program/program_sha256, exit_code0, assertions30 or
72, whole_stdout_BYTE_equal and whole_stdout_JSON_equal, complete materialized
receipt SHA, generated_complete_receipt_BYTE_equal/JSON_equal, plus full stream
records. `generated_receipt_behavior` must explicitly identify the collector's
materialized stdout copy when originals do not emit files. Both stdout streams
are whole JSON; PR37's metadata-only convention must never be imported here.
The receipt must expose actual original runtime `/usr/bin/python3`, actual3.9
version, SymPy1.14.0, and retained default3.14 missing-SymPy failure evidence.

`actual_outer_program_runs`, `actual_nested_program_runs` and
`full_structured_receipt_comparisons` must be nonempty actual evidence lists.
All final outer runs exit0. All outer/nested program-source hashes must occur
in retained evidence. Every referenced full actual stream and structured
receipt is checked against retained path/size/SHA. Saved comparison artifacts
remain bound to exact original/family inputs. Each comparison must close all
remaining fields; each residual difference is kept verbatim and matched to
its exact qualification. The only declared normalization is the exact five
clock keys and one private-repository path prefix. Broad native/runtime
ignoring is prohibited. Complete qualified differences stay in the full JSON.

## Closed169 and original helper limitations

The exact family pins are primary52 manifest
`56cbbc079ee9f05dd3f43f75b068bfc1ec691a363f44ab94054925a0cedba09c`,
current-measure63 manifest
`1e6905dddeb96b57e8d5362724947ab2862791ded39f174b4de4b57c850d0082`,
and trace54 manifest
`82ec472f35d4e4b45dea5128c58e2d0ec61318c285bcf9ca5e88de3bf5d2aeac`.
The original family manifests, all members, and their hidden `.gitignore`
files remain byte exact. No closed code is repaired.

`strict_root_closure_before_and_after` must bind both exact full summaries,
with equality true. Each family summary records its audit-relative manifest
path/SHA/count, strict_recursive_coverage true, and exact exclusions: the
single root manifest path and primary top-level ignoredtmp/ or other top-level
tmp/. The builder repeats the strict recursive check independently.

The two administrative_guard_findings are primary nested_manifest_extra and
nested_ignoredtmp_extra. They preserve the actual old helper's acceptance and
the strict-root rejection, with full mutations, argv, exits and streams.
Explicit strict_root_exact_recursive_closure_verified and
primary_nested_manifest_exploit_rejected_by_strict_root booleans accompany
the structured receipts. This qualifies old-helper coverage, rather than
claiming its historical PASS guarded all nested extras.

## Retention and output boundaries

Required and optional support manifests use path_base `support_directory`,
an explicit audit-relative support_directory, status PASS, and the exact
root_reproduction_receipt_sha256. Each resides at support_directory/
ROOT_SUPPORT_MANIFEST.json and self-excludes only that root filename.
`files` lists every regular file recursively using support-relative paths,
size/bytes and SHA256. The builder independently compares the exact recursive
set. `.py`, `.json`, `.jsonl`, `.stdout`, `.stderr`, `.patch`, `.md`, `.txt` and
basename `.gitignore` are supported explicit first-party capabilities.
Foreign corpus/SQL/PDF/OCR/cache/private scratch retention must be false.
First-party case inputs with historically named ignoredtmp components are
allowed within support; arbitrary external cache exclusions are not.

The actual wrapper and collector sources must be retained by hash. Original
and closed-family sources, all nested programs, full streams, generated first-
party receipts, failure/revision records, current root preimages, collector
instrumentation, root certificate/read ledger and the actual builder are
anchored by audit-relative CURRENT_PROOF_DEPENDENCIES. Support copies are
preserved exactly. Source PDFs and full raw/SQL corpus are not copied.

The new candidate contains exact original16 archive and17 diff, unchanged
mathematical/code/whole-receipt/source/two-turn copies, current explicitly
scoped notes/status/body/context, prospective named queue preimage and patch,
and a strict recursive current manifest excluding only MANIFEST.json.
The mathematical partial results require no repair. Source/status wording is
current administration. The complete target remains unsolved; NEW whole-
current source-first adversarial review remains pending. Old verdicts transfer
no approval. No shared, canonical, Git or remote mutation is performed.

This contract does not authorize publication, acceptance, paper/DOI/tracker/
release, or outside-person communication. A later acceptance record may
describe the present only, never fabricate historical proof/turn events.
