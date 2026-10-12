# PR464 publication operations helpers

These sources are prepared for parent-agent review. They have not staged,
published, appended, updated a branch, marked a PR ready, or merged anything.
The parent owns all actual external operations. A new independent operations
adversary must review these exact sources before they are used for writes.

The four helpers share strict local validation in `common.py`. Defaults are
read-only externally: `zenodo_pr464.py` performs the repository kit's local
check; tracker and integration perform external read-only preflight and save
local preflight receipts. No helper changes the shared checkout or Git index.
No helper contacts an individual, sends a message, creates a release, or
submits a journal manuscript.

## Required final acceptance contract

`FINAL_ACCEPTANCE_GATE.json` lives in the PR464 audit root. It must contain:

- `verdict: ACCEPTED_FOR_PREPRINT_PUBLICATION`, `pr: 464`,
  `problem_id: "30004807"`, `original_pr_head:
  "97b2ed225574ca61bd03cb8db021a533e04938dc"`, and
  `status_gate: "claimed_solved"`.
- Integer `remaining_package_issues: 0` and boolean
  `root_read_entire_final_report: true`.
- Exact SHA-256 strings in `source_receipt_sha256`,
  `mathematical_acceptance_gate_sha256`, `review_input_manifest_sha256`,
  `branch_install_plan_sha256`, and `zenodo_kit_sha256`.
- `review_input_manifest: PACKAGE_REVIEW_INPUT_N.json` for a positive integer
  N. Its `files` mapping binds all top-level outputs to `sha256` and integer
  `bytes`; `final_files` in the gate equals that exact mapping. Required names
  include README.md, manuscript.tex, manuscript.pdf, metadata.json,
  deposit.json, SHA256SUMS.json, and regular_zas_bianchi_verification_v1.zip.
  Include any external archive receipt in that mapping as well.
  The manifest itself must also identify exact `pr: 464`,
  `problem: "30004807"`, and `original_head`, and its
  `source_receipt_sha256`, `mathematical_acceptance_gate_sha256`, and
  `branch_install_plan_sha256` must equal the final gate's bindings to the
  actual checked bytes. Separately updating the final gate cannot substitute
  a different source/math/plan after the reviewed freeze.
- `complete_package_reviews`, containing clean PASS reviews only; retain
  earlier reports requiring repairs as historical evidence elsewhere. Every
  listed review has integer `round`, nonempty distinct `identity` or `reviewer`,
  audit-relative `path`, exact `sha256`, `verdict: PASS`, and integer
  `blocking_issue_count: 0` and `required_correction_count: 0`. The final two
  rounds are successive and each has `input_manifest_sha256` equal to the
  final accepted manifest SHA. This requires two fresh clean reviews of the
  final bytes, not two reviews of superseded versions.
- `operations_review`, with audit-relative report `path`, `sha256`,
  `verdict: PASS`, integer-zero `blocking_issue_count` and
  `required_correction_count`, and `helpers` mapping exactly the four names
  `operations/common.py`, `operations/zenodo_pr464.py`,
  `operations/register_pr464_tracker.py`, and
  `operations/integrate_pr464_publication.py` to their exact SHA-256 strings.

The current mathematical gate's three independent families, bounded priority
report, whole-candidate report and whitelists are independently hash-checked.
All thirteen captured original source files must still match their snapshot.
The historical standalone author-manifest SHA remains unattested; no helper
manufactures missing source bytes or a human-review/first-priority claim.

`BRANCH_INSTALL_PLAN.json` is a positive `entries` list. Each item has
`local_program_path` relative to the repository, `repository_destination`,
`sha256`, and integer `bytes`. Sources must be inside the accepted `package/`
folder, destinations must preserve their exact package-relative paths under
`unsolved_math_prioritization/attempts/30004807/preprint_20261012/`, and the
selected paths must equal exactly all file entries of the reviewed ZIP plus
the frozen top-level outputs. The ZIP has no directory entries, duplicate
paths, symlinks, forbidden/private paths, or circular external PDF/archive/
deposit outputs. Every ZIP payload must equal its corresponding local bytes.
The thirteen original sources appear under
`verification/frozen_history/` and match their original bytes.

The ordinary kit deposit syntax is accepted: each file item has `path` and an
optional `name`. Its effective uploads must be exactly
`regular_zas_bianchi_defect.pdf` from `manuscript.pdf`, and
`regular_zas_bianchi_verification_v1.zip` from the same-named local ZIP.
Deposit metadata must equal metadata.json; no canonical metadata
normalization is accepted in this particular workflow.

## Parent-owned operation sequence

After final paper and fresh operations acceptance, the parent may use the
following commands from the repository root. None were executed during
preparation; `check_operations.py` uses private fabricated fixtures only.

```sh
python3 draft_pr_claimed_solved_400_500_20261011/audits/pr464_30004807/operations/zenodo_pr464.py
python3 draft_pr_claimed_solved_400_500_20261011/audits/pr464_30004807/operations/zenodo_pr464.py --mode stage --apply
python3 draft_pr_claimed_solved_400_500_20261011/audits/pr464_30004807/operations/zenodo_pr464.py --mode inspect
```

Publication additionally requires `--mode publish --apply --confirm-id`
followed by the actual verified draft integer. This invokes the unchanged
top-level `zenodo_deposit_tool/zenodo.py` kit. It preserves an operation record
before dispatch; an uncertain stage/publication is recovered with `--mode
inspect`, never by blindly rerunning a write. The published deposition is
reinspected through the original kit, then both public files are downloaded
without authentication and their exact byte counts and SHA-256 values are
checked. Actual confirmed receipts are stored in the audit root.

The parent can then run tracker preflight, review it, and invoke the same
tracker helper with `--apply`. It reconfirms publication read-only, validates
the requested spreadsheet/gid/tab and A:D headers, leaves the chat URL cell
blank, searches all DOI cells for URL/token forms, and issues one native GWS
append. A lost response triggers readback only. Exact final range and unique
DOI registration are verified; unrelated tracker rows are not saved.
A surviving attempted or verified operation, or an independently saved
verified receipt, requires read-only reconciliation if its row disappears.
It cannot authorize another append. Unknown operation states and unrelated
or differing receipt bytes are rejected. Default reads preserve all durable
write guards; history is rechecked immediately before a proposed append.
If every local write record is deleted, these local guards cannot establish
the missing history or provide a global exactly-once guarantee.

Integration preflight follows confirmed publication and tracking. It checks
both against their actual live read-only representations, validates the
original PR number/repository/base/head/branch/draft state and exact fourteen
changed paths, then prepares only the accepted positive paths over captured
latest main. Only the selected QUEUE row changes; status remains
claimed_solved, original research count remains 1/5, and DOI/findings are
updated with the accepted scope and classical credits. Other current main
rows and files are preserved. Conflicting current-main source/package bytes
stop preparation instead of being overwritten. This comparison covers every
prospective payload destination, including added publication receipts,
generated PUBLICATION_MANIFEST.json, and the current landing note. Identical
existing bytes are allowed. The only different existing payload expressly
superseded is the captured immutable original PUBLICATION_NOTES.md;
selected QUEUE-row updates remain separately checked byte by byte.

`integrate_pr464_publication.py --apply` creates the commit with original PR
head and captured main as its two parents. It verifies the exact changed-file
set (rejecting the GitHub compare limit), all installed targets through
immutable Git trees/blobs, and all live prerequisites again. It saves the
operation before one nonforced ref PATCH. A lost response is read back;
`--reconcile` performs only reads of a saved commit/ref and revalidates all
target bytes. A prior write record prevents a blind repeat of `--apply`.
If saved Git objects exist but the branch was never updated, the parent must
inspect and explicitly reconcile that record before preparing a new attempt.
This helper intentionally does not mark ready or merge; the parent performs
those later operations against the exact verified installed head.

Fresh checks followed by nonforced writes and final duplicate snapshots are
not an atomic multi-runner lock. The GitHub ref endpoint offers no atomic
expected-old-head compare, and Google Sheets can admit a concurrent append.
These limits are explicitly recorded rather than disguised as guarantees.

## Offline controls

```sh
python3 draft_pr_claimed_solved_400_500_20261011/audits/pr464_30004807/operations/check_operations.py
python3 -O draft_pr_claimed_solved_400_500_20261011/audits/pr464_30004807/operations/check_operations.py
```

Each mode passes 158 cases, with identical structured results and zero real
external calls. The cases include invalid integer-zero review counts; stale
gates/reports/metadata/source; private, escaping and symlink paths; duplicate
or unreviewed installations; exact eligible PR identity; modified source and
truncated/unrelated diffs; binary immutable readback; complete mocked branch
installation with retained other main rows/files; lost branch responses;
native tracker duplicate/uncertain append scenarios; and staged/published
Zenodo lost-response reconciliation without another write. These finite
controls are operational evidence, not a mathematical proof, independent
operations review, or atomic concurrency guarantee.

The first fresh operations adversary found three blocking helper defects
despite the original 127 checks passing, and one builder defect assigned to
the parent. Its historical REQUEST_CHANGES report remains authoritative for
those original source bytes. Thirty-one new regressions cover the three
helper repairs. `replay_round1_attacks.py` additionally replays the reviewer's
thirteen unmodified helper probes normally and with optimized Python; all
expectations are now met, including the previously unsafe scenarios, with
zero real calls. This repairer replay is expressly not a new independent
review. The parent owns the builder repair and a NEW fresh operations
adversary must inspect every final source before acceptance.

The before-repair whitelist and valid control summaries are preserved as
`*_BEFORE_REPAIR.json`; their paths refer to originals immutably published in
checkpoint 22, commit `e1b54d91a8cd5141b69f5bcadd232cc769fbce7c`.
Their recorded hashes are historical, not claims about the repaired current
source bytes. The current positive whitelist binds the repaired helpers,
updated evidence and explicit historical snapshots.

Fixtures are generated only in ignored `private_cases/` and removed after
each successful test. Never publish or package private fixture directories,
credentials, ignored API state, foreign source corpora or environments.
The positive public whitelist lists only these authored helper sources,
documentation, log and valid control summaries.
