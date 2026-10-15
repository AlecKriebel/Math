# PR905 independent integration review

**PASS — clean integration, no repairs.** Completed 2026-10-13T05:47:36.433100+00:00; completion estimate
100% of this narrow nonmathematical integration review. No integration gap was
found. This review does not replace the completed mathematical, computation,
source/model, or sequential full-package reviews.

## Exact claim and falsifiable success criteria

The integrated commit `fb2d639e2508cc45c9327e02624ae7a38e82b58a` must preserve the original packet at
`330a544a53b9e3e01bb0ed70817a5f4a79cc6a0a` and the eight frozen publication files of revision 2. Relative to
its recorded main parent `01ad94d92e7938d71aa38a2e504c64fc4eae04fb`, differences must be confined to the 30
target packet files and the exact accepted target 30000717 queue row. Every
other tree entry and queue byte must be preserved, source identity and holds
must remain unchanged, and live PR metadata must identify the same objects.
Any unexpected path, mode, object hash, packet byte, queue cell, source hash,
hold, or identity change falsifies the clean-integration conclusion.

## Independently reproduced evidence

- Recomputed Git SHA1 object identities from raw commit/root-tree bytes for
  the original head, recorded main parent, and integrated head. The integrated
  tree is `eb329e2c8d6772d7b5f56fc2ba281bd04db97630`; its ordered parents are the original audited head and
  recorded main parent. Their common base is the original commit's parent.
- Enumerated the complete recursive trees. The difference from main has
  exactly 31 paths: 30 added target packet files and `QUEUE.md`. All
  170,884 other main leaf entries,
  including their modes and object IDs, are identical. The packet has exactly
  its original 30-file membership, unchanged modes and blob IDs. Recomputed
  each file's SHA256 and Git blob SHA1; compared original commit, integrated
  commit, and captured local bytes directly against `ORIGINAL_SNAPSHOT.json`.
- Removed the unique target row from both main and integrated queues and
  directly compared the remainder: all 411,942
  bytes are identical. The integrated target row equals both the original
  row and `GATED_QUEUE_ROW.md` byte-for-byte. Only Status, Turns, and Findings
  differ from main; status is `claimed_solved`, turns are `1/5`, holds empty.
  This also checks headers, whitespace, row ordering, unrelated notes/links,
  newline termination, and every other queue cell.
- Recomputed `statement_hash` from the private statement bytes and
  `review_hash` from the documented sorted-JSON encoding of problem and prior
  research. They match the preflight and all original/main/integrated
  catalogue/assessment records. Target identity remains 30000717 /
  OWR-1465-011, present; catalogue and assessment holds remain empty. The
  original native state remains absent. No private statement content is
  redistributed in this review.
- Compared all eight active publication files by size and SHA256 to
  `PREPUBLICATION_FREEZE.json`, including PDF, ZIP and deposit metadata. They
  match frozen revision 2 exactly. The latest full-package review still binds
  the original head and says `PASS_FROZEN_REVISION2_NO_REPAIRS`.
- Independently refreshed all six previously identified primary-source URLs
  in memory. All sizes and SHA256 values match the fresh full-package review;
  no PDF or other raw third-party source data was saved or copied.
- Two authenticated read-only GitHub metadata routes identify the same live
  open, nondraft, unmerged PR head and recorded base. GitHub's Git commit API
  confirms the tree and both ordered parents. Its paginated changed-file
  list has exactly the expected 31 paths, and every reported Git blob SHA
  matches the independently checked local integrated tree. The queue has
  one addition and one deletion; all 30 packet files are additions.

## Boundary and promotion conclusion

No mathematical candidate edit occurred. A merge commit's comparison with
its first parent includes inherited main history; the relevant preservation
test is its comparison with the recorded current-main second parent. That
comparison contains no unrelated changes. The eight publication files are
local frozen artifacts, so their preservation is checked separately from
the original PR's 30-file packet.

The exact integration is cleared. The latest REST response's mergeability
field was `null/unknown`, after a connector response reported `true`; this
transient field is not evidence for or against byte preservation. Ordinary
live merge eligibility should be checked by the root at the action boundary.
The exact-head and exact-parent checks are time-bound observations; a later
head/base movement requires a renewed identity check. No first-priority,
current-open-status, conventional human-peer-review, or exhaustive-literature
claim is added by this review. Existing package limitations remain intact.

## Checkable artifacts and action boundary

`verify_integration.py` reproduces local tree, packet, queue, source-identity,
and frozen-byte checks using read-only Git operations. `refresh_source_hashes.py`
repeats only the six source-byte checks in memory. `seal_review.py` validates
recorded remote metadata and seals the explicit public allowlist. Evidence is
in `evidence/tree_and_frozen_checks.json`, `evidence/fresh_source_hashes.json`,
and `evidence/remote_metadata.json`.

All writes were confined to this integration review folder. The shared
checkout remained on `main`; no Git mutation, candidate change, external
human contact, merge, deposit, release, or spreadsheet action was performed.
The parent/root remains responsible for its separately authorized actions.
