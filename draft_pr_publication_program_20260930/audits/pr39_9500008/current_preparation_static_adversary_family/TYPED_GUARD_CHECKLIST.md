# Required typed guard before PR39 current preparation execution

This is a source-only contract repair checklist for the unchanged 505-line
builder, SHA256 `9d6dbd07e063a8e588846264ac51e00998220d4e90208cb18598447988380ac0`.
The supplied approved inputs are correctly typed. An altered input would fail
the existing approved full-file checksum. The issue concerns the broader
claim that the builder itself rejects malformed types, and is not an actual
receipt failure or a demonstrated complete-builder bypass.

Every listed field is required to exist. Use `type(x) is int` for integers and
`type(x) is bool` for booleans. Required nulls mean a present key with value
`None`; `.get(key) is None` alone is insufficient. Required paths, labels,
reasons, identifiers and digests are nonempty strings; digests additionally
match lower-case hex64, Git commits/blobs hex40. Preserve all existing exact
value, whole-byte, path, membership and mathematical checks in the builder.
Extra genuine metadata may remain allowed. This guard does not supply a
scientific verdict and must not alter any closed file or original ledger.

## Named metadata inputs and fields

- `source_snapshot/readiness.json` (builder 251,254–256): `id`,
  `budget.used`, `budget.maximum_substantive_attempts` are integers; claim,
  outcome, review/artifact/statement/pair hashes and historical exposure/deadline
  fields are strings. The historical fields stay archival. The complete
  original file remains byte pinned.
- `source_snapshot/turns.json` (254–256): `id`, `count`, each
  `attempts[*].number` are integers; `attempts` is a list of exactly two
  dictionaries; route/outcome/gap and the second artifact/SHA are strings.
- `source_snapshot/source_record.json` and `prior_report.json` (251–253,258):
  source `id` is integer; `problem_number`, `statement` are strings; whole
  source/prior bodies retain exact checksums and type-sensitive complete-object
  equality. Do not narrow or reserialize the imported prior.
- `source_snapshot/review/verdict.json` (255–256): `full_problem_solved`
  is boolean false; `artifact_sha256` is a digest string. Historical PASS stays
  explicitly archival, with no current verdict transfer.
- `ROOT_PRIMARY_READ_LEDGER.json` (205–206): `reading_completed` is boolean;
  `new_substantive_attempts`, `original_substantive_attempts` and
  `verification_attempts_added` are integers; certificate hash is a digest;
  `current_model`, `current_reasoning_effort`, `current_deadline_utc` are present
  nulls. Its dated replay/current PENDING fields stay unchanged.
- `ROOT_PRIMARY_READ_ADDENDUM.json` (207–209):
  `new_substantive_attempts`, `audit_attempts_added` are integers;
  `prior_read_ledger_sha256`, `prior_scope_certificate_sha256`,
  `primary_proof_qualification_sha256` are digest strings;
  `full_problem_solved` is boolean false.
- `ROOT_SCIENCE_CARD.json` (211–217):
  `original_substantive_attempts`, `turn_limit`, `new_substantive_attempts`,
  `audit_attempts_added` are integers; `full_problem_solved`, `partial_valid`,
  `novelty_claimed` are booleans; `current_model`,
  `current_reasoning_effort`, `current_deadline_utc` are required present nulls;
  `status`, `new_whole_current_gate` are strings; all six certificate/read/
  addendum/qualification/actual-receipt/actual-attestation SHA fields are digest
  strings. Preserve status UNSOLVED, gate PENDING and existing values.
- `ROOT_REPLAY_READ_ATTESTATION.json` (218–222):
  `original_substantive_attempts`, `new_substantive_attempts`,
  `audit_attempts_added` are integers; `reading_completed`,
  `primary_read_ledger_modified` are booleans; receipt/certificate/read/addendum/
  qualification/entrypoint/collector hashes are required digest strings.
- `ROOT_CURRENT_INPUT_PREIMAGES.json` (223–234): `approved_by_root` is
  boolean true; `reason` and `current_head` are nonempty strings, current HEAD
  hex40; `files` is a list of exactly thirteen unique dictionaries. Each row
  requires a canonical string path, nonnegative integer `size`, digest string
  `sha256`. Complete live preimage checks and exact set remain unchanged.

## Actual root receipt and nested contracts

For `ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json`:

- Lines 194–202: `status`, `head`, `base`, root/collector source paths and
  SHA fields are required strings; `exact_original_file_count`,
  `changed_diff_path_count`, `closed_family_count`,
  `authored_members_verified_before_and_after`, `original_substantive_turns`,
  `turn_limit`, `new_substantive_attempts`, `audit_turns` are integers;
  `full_problem_solved` is boolean; `retention_errors` is a list.
- Lines 210,225–226: reading/current artifact rows are dictionaries with
  required typed path/size/SHA; `native_full_file_preimages_before_and_after`
  is the complete thirteen-row typed list and `current_head_unchanged` a commit
  string. Compare nested rows with type-sensitive equality.
- Lines 257–265: `provenance.status`, `SQL_mode`, `full_diff_sha256` are
  strings; `raw_corpus_bytes`, `problem_count`, `research_report_count`,
  `full_diff_bytes`, authored/new/audit/limit counts are integers; raw-prior
  presence/fallback/full-pair/full-SQL/target-absence flags are booleans.
  `current_native_target.state` is required null, history is a required list,
  catalog `local_status` string and `turns_used` integer. Original Git rows
  carry typed size/path/mode/blob/SHA. Complete prior, source and pure-score
  comparisons must distinguish booleans from numeric values.
- Lines 266–282: strict closure flags and every family
  `strict_recursive_coverage` are booleans; member/foreign counts are integers;
  manifest path/hash strings; cache prefix is its exact declared string or
  present null. `real_packet_controls` has exactly six rows;
  `real_manifest_controls` exactly twenty-eight distinct rows. In each row,
  `observed_expected` and `strict_root_guard_pass` (where declared) are booleans;
  actual/expected exit fields integers; labels/cases/families/digests strings.
  `real_uniform_prose_and_code_control_count` is integer ten.
- Lines 312–327: actual outer/nested/admin run collections are lists of
  dictionaries. Every declared launch/execution/completion/source/stream
  availability flag is boolean; exit/returncode/index fields integers (null
  only for genuinely incomplete or unlaunched attempts, which the builder
  already refuses as successful prerequisites). `argv` is a list of strings.
  Label, cwd, source SHA and artifact paths are strings. All declared artifact
  references, including stdin when present, have typed size/SHA/path. PR39 has
  no supplied stdin; do not impose PR38's different sixteen-stdin rule.
- Lines 330–353: policy flags and comparison success/equality flags are
  booleans; clock keys list and both prefix strings are present; comparison
  rows and precise qualifications are structured dictionaries/lists, with
  complete actual/saved artifact references. Keep the existing recursive
  type-sensitive `differences` function and exact full stream qualification.
- Lines 355–365: original replay exit/count fields are integers; whole-file/
  whole-JSON result flags booleans; full generated/stdout/stderr references
  typed; default failure exit integer one and absence flag boolean true.
  Runtime version-info components 0,1,2,4 are integers, component3 string.

## Manifest and pin rows

- `PREPARATION_MANIFEST.json` (184–190): files list length exactly seven,
  unique paths and exact required set. Root self exclusion is exactly the
  single string `PREPARATION_MANIFEST.json`. All row paths/SHA strings and
  nonnegative integer sizes. The current code checks a set, so an additional
  duplicate unchanged row would otherwise not be excluded by that test alone.
- `INPUT_PINS.json` (190,249,261,274–291): original/head/base/problem/count
  fields and all artifact rows have declared exact types. `families` is exactly
  the three named dictionaries; `member_count` integers; member rows unique
  with typed path/size/SHA; `foreign_members` lists; `cache_prefix` exactly the
  original string or required null. Check row lengths equal stated counts.
- `snapshot_manifest.json` (236–248): original sixteen and seventeen-path
  lists, exact identity fields, unique paths, typed size/mode/blob/SHA rows;
  diff-byte and PR/problem numeric fields are integers where the actual
  frozen format uses integers. Do not change their frozen serialization.
- `ROOT_SUPPORT_MANIFEST.json` (293–309): status/path-base/support-anchor
  strings; self-excluding and foreign-body flags booleans; exact one-root-self
  exclusion; unique row list, typed path/size/SHA. Artifact references may use
  the already reviewed `size` or `bytes` spelling, but the declared value must
  be a nonnegative exact integer. Root receipt references need all three keys.
- Closed family manifests remain full-byte pinned to the reviewed inputs.
  Apply row typing according to each actual manifest's retained schema;
  do not rewrite them into one new format.

Parse only the named metadata needed by this entry guard. The five malformed
negative-fixture JSON files are retained intentionally and exactly identified
by path, size and SHA in `STATIC_INPUT_DATA_CHECKS.json`. Their bytes are not
proof receipts; neither a blanket skip of fixture JSON nor a blanket demand
that every JSON file parse is correct. The new guard and its source-only
validation/capture must be explicitly pinned and retained with actual current
execution evidence. The new whole-current review remains pending.
