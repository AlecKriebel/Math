# PR468 independent publication operations review, round 2

Verdict: **PASS within the stated operational scope**. Mandatory issues: **0**;
blocking issues: **0**; required corrections: **0**; optional issues: **0**.
Review completion: **100%**. This is an operational review, not mathematical
acceptance or evidence of a live publication, tracker write, branch update, or
merge. The actual gate captured at the start remained
`HOLD_METADATA_RECONCILIATION`; its contents were used only as a negative test.

The current complete `integrate_pr468_publication.py`,
`register_pr468_tracker.py`, `replace_pr468_draft_archive.py`, and existing
`zenodo_deposit_tool/zenodo.py` contract were independently read and frozen.
The subsequently requested `publish_checkpoint.py` was separately read and
frozen. `SOURCE_FREEZE_RECEIPT.json` records their exact SHA-256 values;
`SOURCE_PRESERVATION_RECEIPT.json` confirms all five remained byte-identical at
completion. No original helper was changed.

## Checkable evidence

The independently authored `test_publication_operations.py` executed **94
cases, 94 PASS, 0 FAIL**. `MOCK_DIAGNOSTICS.json` records each case, its observed
mock mutation calls, and its result. The harness runs complete helper entry
points with isolated filesystem contexts, synthetic remote clients, disabled
external subprocesses, and a network guard. It uses raw frozen packet/source
bytes as data; prior reviews' verdicts or test assertions are not imported as
proof. Synthetic acceptance reports and publication receipts are explicitly
mock fixtures kept under `private_cases` and excluded from publication.

| Family | Cases | Verified mechanism |
| --- | ---: | --- |
| Review-count and actual-HOLD guards | 34 | Both relevant helpers reject malformed/nonzero counts before mutation; HOLD rejects apply |
| Integration | 16 | Source/packet/review binding, original scope, current-main preservation, nonforced branch update and recovery |
| Archive replacement | 20 | Same draft, known old ZIP only, preserved PDF, at-most-one DELETE and read-only recovery |
| Tracker | 11 | Exact readable row, no repeated append after uncertainty, final DOI uniqueness and exact-range readback |
| Existing Zenodo contract | 5 | Stable-manifest staging, lost upload/publication responses, verified or failed readback |
| Checkpoint selection | 8 | Public-only selection and rejection of excluded/resolved/symlink paths before any remote call |

Run locally with `python3 -B test_publication_operations.py` in this review
folder. The harness requires the excluded raw frozen inputs in
`private_sources`; it verifies the frozen helper hashes before testing and
regenerates fixtures exclusively in `private_cases`. The public manifest does
not include these working copies or fixtures.

## Findings

**Acceptance counts fail closed.** For each of `blocking_issue_count` and
`required_correction_count`, missing values, null, false, true, floating zero,
string zero, one, and negative one were concretely rejected in integration and
replacement. The actual HOLD snapshot also rejects apply. The zero-integer
baseline succeeds. Changed accepted reports, accepted PDF bytes, original
source bytes, and install-plan hashes fail their binding checks.

**Archive replacement is narrowly bound.** The same saved production draft
23310484 must remain unpublished, with exact canonical metadata and the
reviewed PDF. Deletion requires the old ZIP backup's SHA-256 to match round 3,
its MD5 to match the earlier draft receipt, and the current remote ZIP's
checksum and size to match that known backup. Unknown ZIPs, a different saved
or returned draft, a published record, metadata/PDF drift, extra files, unsafe
file IDs, or a missing ZIP without the recorded operation fail. The operation
is saved before DELETE. The existing kit rejects empty successful HTTP204
content as an unconfirmed JSON response; the helper catches that error and
uses GET readback. Committed lost responses recover without a second DELETE;
an unchanged ZIP or failed/drifted readback does not produce a successful
receipt. A recorded operation with an absent ZIP resumes using GET alone; a
prior operation with the old ZIP still present blocks another DELETE. An
already accepted ZIP verifies the full packet without deletion. The unchanged
kit then stages the accepted ZIP on the same stable manifest/draft, skips the
PDF, and avoids a duplicate upload after a committed lost response. Publication
POST loss recovers from submitted-record readback; unconfirmed publication or
checksum drift fails without a verified publication receipt or automatic retry.

**Tracker registration is readable and bounded.** The row identifies
`30000689 / OWR-1455-008 — Embedding Obstructions from Missing Simplicial Faces`,
the original conjecture at
`https://ems.press/content/serial-article-files/46090` (p. 238, Conjecture 4),
and the confirmed DOI. Its notes give the canonical title, Alec Kriebel,
version 1.0, 12 October 2026, and the PR468 source link, with the disclosed
unrefereed/AI-assisted status. The blank solution-chat cell is preserved.
Existing duplicate or nonidentical same-DOI rows fail without another append.
A committed lost append response is recovered by exact readback; an
unconfirmed saved attempt with no matching row blocks a rerun's append. A
concrete second same-DOI insertion after the initial append-range readback is
detected by the new final whole-column scan. A subsequent edit to the final
identified range is also detected. Unrelated rows remain unchanged. The
receipt explicitly limits uniqueness to its final snapshot; it makes no
atomic multi-runner guarantee.

**Integration preserves scope and latest main.** Tests reject a moved original
PR head, excluded original status, unrelated original paths, duplicate target
QUEUE rows, changed main disposition, and an existing different DOI. The
successful mocked tree extends the captured latest-main base, preserves
unrelated paths and rows, modifies exactly the single target QUEUE row,
retains claimed_solved and the original 3/5 count, and installs accepted bytes.
Original audit/author files remain identical; all 15 original source files
also remain identical in the installed historical folder. The existing PR
branch is patched nonforcibly. Its proposed commit is recorded before the ref
write; a lost ref response succeeds only after readback equals that exact
recorded commit. A rejected competing branch head fails verification. PR
movement after blob preparation stops before tree/ref installation; created
blobs may remain orphaned. Installed-file drift fails the successful receipt.
The helpers do not merge. A subsequent live merge still requires the root's
exact-head check.

**Checkpoint publication excludes every private path.** With valid own-public
files first in the list, appending any path component `private_sources`,
`mutation_fixtures`, `.secrets`, `.zenodo-state`, or `__pycache__` concretely
fails before **any mocked API call**, not merely before a ref write. A directory
alias resolving into `private_sources` and a direct file symlink also fail.
The source additionally excludes `.pyc`. A normal explicit two-file own-public
list succeeds, sends only those blobs, preserves the main base tree, updates
main nonforcibly, and verifies its recorded commit. All selection validation
precedes remote blob creation. This review's own publication manifest applies
a positive whitelist and excludes **all** `private_sources` and `private_cases`
paths regardless of whether their contents are authored, valid, or fixtures.

## Strongest verified limit

The inspected mechanisms pass the stated adversarial mock checks with no
remaining concrete false-acceptance witness. No atomic tracker concurrency,
future remote immutability, or live service success follows from these tests.
This review made zero live remote calls, zero credential or local Zenodo-state
reads, zero Git/index/branch/shared-source changes, zero cloud writes, and zero
outreach. Actual acceptance, publication receipts, registration receipts, and
the root's eventual merge must be established separately from the real
operations; none of the synthetic test receipts is promoted as that evidence.
