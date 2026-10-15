# Prepared PR36 acceptance helpers — execution remains gated

These four Python sources were prepared without execution or import. The live
NEW whole-current-packet gate is still pending. Preparation changes only this
folder. No canonical attempt, queue, state, history, inventory, remote, branch,
Git index or commit was changed here. No outside individual was contacted.

The future root-owned workflow is `integrate_reviewed_partial.py preflight`,
`overlay`, `finalize`; then `state_mirror_reconciliation.py`; then
`verify_post_acceptance.py`. Every phase requires `--execute`, an actual final
NEW whole manifest path and SHA256, and an actual final root reproduction
receipt path and SHA256. Paths are repository-relative and must resolve inside
the PR36 audit. No placeholder final SHA is supplied or accepted.

## Exact final-root receipt contract

The final root receipt must contain these exact fields; additional actual-run
detail is welcome. Reconcile this contract to the independently produced final
receipt by a reviewed helper revision or a clearly attributed root receipt.
Never manufacture a PASS or replace an actual review with this preparation.

```json
{
  "status": "PASS",
  "pr": 36,
  "problem_id": 20001424,
  "original_head": "35be7fe58a2832c4d7012cf69c973810fb4c42f8",
  "reviewed_candidate_manifest_sha256": "75d103fcfe2bce2322ff091fea73d0f03c7875b00c7c7af8f6e20ff741a2975c",
  "current_proof_dependencies_sha256": "f6b0af0f11ee8aae60678cc37e7cb24373d99484918f893e1a94e9e703d43261",
  "whole_manifest_sha256": "ACTUAL FINAL NEW WHOLE MANIFEST SHA256 REQUIRED",
  "queue_status": "already_solved",
  "priority_classification": "PRIOR_APPLICATION",
  "mandatory_corrections": [],
  "entire_current_packet_checked": true,
  "root_actual_reproduction": true,
  "original_substantive_attempts": 1,
  "new_substantive_attempts": 0,
  "verification_attempts_added": 0,
  "paper_or_new_doi_or_tracker": false
}
```

The illustrative non-hash sentence above fails the helper's SHA256 validation.
The whole manifest must be final, self-excluding and exact for its entire
authored directory. Earlier family manifests and the frozen candidate manifest
cannot substitute for the NEW whole gate.

## Future root execution order

1. Finish the NEW whole source-first adversary, actual root reproduction,
   complete final gate review and checkpoint on `main`. Independently read the
   entire helper sources and this schema. Record the actual final manifest and
   root receipt pins. Checkpoint tracked changes before preflight.
2. Run `preflight` with those four gate arguments and `--execute`. It requires
   actual OPEN/draft exact original head, absent canonical attempt, no merge or
   staged/unstaged tracked changes, post-PR35 state26/31 and25 complete primaries.
   It saves the full current queue and inventory preimages and the concrete
   accepted PR body in the audit. If only unrelated queue bytes differ from the
   dated builder preimage, separately review that exact named-row rebase and
   provide `--allow-named-row-rebase`; the selected full row must remain exact.
3. Review `accepted_pr_body.md`. Root performs the authorized remote body edit
   and draft-ready operation separately. No helper performs either operation.
4. Root begins a local no-ff, no-commit merge of exact original head
   `35be7fe58a2832c4d7012cf69c973810fb4c42f8` into the captured main HEAD. Do not
   commit another checkpoint between preflight and this merge. Only the queue
   may be conflicted. Retain and inspect any unexpected conflict or failure.
   Inspect the untouched automatic working queue and its index stages, then
   capture its SHA256 before any manual edit. This additional root-reviewed
   preimage is required as `--merge-queue-preimage-sha256` for overlay. The helper
   cannot reconstruct arbitrary Git conflict-marker conventions; it requires
   this explicit root provenance guard, exact actual HEAD/stage2 main queue
   and original-head stage3, and an immediate final working-preimage recheck.
   If the automatic queue has already been edited, preserve that evidence and
   inspect/review the changed scope; do not pass a newly computed blind hash.
5. Run `overlay` with the same pins. It verifies actual remote ready/body,
   original MERGE_HEAD, original canonical16 and unchanged state/history/inventory.
   It copies the frozen current60 members and archives the six pending mutable
   administration files plus candidate manifest before accepted edits. It
   replaces only selected Status/Turns/Findings on the saved complete current
   queue preimage; all other bytes and selected Chat/DOI survive. It never
   replays the old base-Q patch.
6. Root reviews, resolves/stages the concrete overlay and creates the actual
   no-ff merge commit. Independently check the complete committed canonical
   overlay membership, bytes and exact named queue against `integration_check.json`
   before pushing main. No helper stages, commits, merges or pushes. Verify the actual remote recognizes the exact original head as
   MERGED; do not fabricate a merge receipt.
7. Run `finalize` with unchanged pins. It independently fetches remote
   MERGED/nondraft/date/body, checks actual parents `[captured main, original
   head]` and ancestral membership, and checks merge-state/history preimages.
   It writes lowercase `acceptance.json`, `ACCEPTANCE.md`, exact canonical
   self-excluding manifest, audit acceptance and selected inventory update.
   Original root/science/source/prior/dependency/ledger bytes remain unchanged.
8. Run the mirror helper. It starts from the frozen PR35/2744 proposal; preserves
   every earlier entry and duplicate; binds raw `problem.json`, current
   `CURRENT_UNIVERSAL_CERTIFICATE.md` and native `jsonl_turns`; preserves the
   PR23 string-ID zero ledger and PR35 original-response schemas. Under the
   existing cooperative lock it writes a durable intent, then appends exactly
   one PRESENT acceptance event to the complete old history prefix, then writes
   state. Counts become27 targets/32 consumed turns,26 complete primaries plus
   the existing1 duplicate. No historical proof event or new research turn.
9. Run postvalidation immediately. It independently checks all bytes, remote
   and merge parents, queue preimages, original1/5 ledger, all26 prior state
   entries and complete history prefix. A fresh in-memory core proposal
   refreshes only current inventory and must reproduce a byte-preserving no-op.
   It writes only a new audit verification receipt. Root checkpoints and pushes
   the resulting verified administration in accordance with project policy.

Each command has the argument shape:

```text
python3 <this-folder>/<helper>.py [phase] --execute
  --whole-manifest <actual repository-relative final manifest>
  --whole-manifest-sha256 <actual final SHA256>
  --root-final-receipt <actual repository-relative final root receipt>
  --root-final-receipt-sha256 <actual final SHA256>
```

All mutation phases are future root work, not preparation validation. Failures
are retained as uniquely dated `FAILURE_*.json` in this folder. Any existing
preflight/acceptance/mirror intent or temporary requires inspection before
retry. The two-file lock is cooperative and cannot prevent a writer that
ignores it. No recovery, deletion or automatic retry is implemented.

## Attribution and limits

`SOURCE_READING_MANIFEST.json` binds every read pattern and source revision;
`read_only_pattern_archive/` preserves the exact PR34 integration/mirror/post
helpers and core revision2/root writer as read-only reference data. The new
helpers use explicit exceptions that remain active under optimization, native
PR36 layouts, a raw source binding, exact current12-column named replacement,
required future final gate pins and preserved failure receipts. The archived
pattern scripts are not PR36 executables and must never be imported/run here.

`STATIC_VALIDATION.json` records AST parsing and direct frozen-data binding
checks only. It certifies no scientific gate or dynamic behavior. Final helper
root review and all runtime operations remain outstanding. No paper, new DOI,
tracker row, release, novel universal resolution, narrow degree11 priority,
earliest worldwide PCF attribution or human peer review is asserted.
