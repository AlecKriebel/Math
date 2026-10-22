# Independent binary checkpoint safety review

Verdict: **PASS for the narrow binary extension; no blocking defect found.**
Review completed 2026-10-21 UTC. Completion estimate: **100% of this scoped
tooling review**, with no estimate or endorsement of the scientific package.

The reviewed `overlay_entry()` change represents non-UTF-8 files as base64 Git
blobs, checks the returned blob identifier against the independently computable
Git identifier of the frozen bytes, and passes only that identifier to the tree
overlay. The existing exact-tree check then independently binds every selected
changed entry to its expected byte hash before creating a commit or moving
`main`. UTF-8 data remains inline, including non-ASCII text, NUL, BOM, CRLF, and
combining characters. A server-side transformation of that inline data causes
the final tree check to reject the operation.

## Exact reviewed source

| File | SHA-256 |
| --- | --- |
| `remote_checkpoint.py` | `aba5c0a0502966b63cd0443044cc26599913f3f9ef45db3222789ca4023d8bac` |
| `checkpoint.py` | `f9e0574a9bdc92bae041c282bb0e9448a6dfbab4809fc564425ac3e3033a6d02` |
| `sweep_io.py` | `23f840ba1c7318d7fe3bec8f06beb868e4fbfdbb4d9db861f5323f5a8f130697` |

The `reviewed_*.py` files preserve exact source snapshots. The initial and final
binding JSON files establish that the live reviewed sources were unchanged
through the control run. The final seal binds the report, controls, outputs,
snapshots, and research log. Changes to the implementation invalidate this
source-specific verdict; allowlist-only additions require checking the added
paths and their final bytes.

## Claim, assumptions, and criteria

The hypothesis under test was that adding binary artifacts does not weaken the
existing checkpoint guarantees: selected frozen bytes remain exact, every
unselected root entry and owned-folder leaf remains intact, the destination is
fixed, and moving `main` uses a fresh parent and a non-forced fast-forward.
Dry run must perform no blob, tree, commit, or reference write.

The review assumes normal Git object identity, a truthful GitHub object API,
and the project's ownership of its explicit selected paths. It does not assume
that a returned blob hash is correct without checking it. Faults in returned
trees and commit bindings were actively injected. A partial failure may leave
unreferenced immutable blobs/trees/commits; publication is the later reference
update, whose guards must still hold.

## Independent controls and results

All **32 of 32 controls passed**. The controls import only frozen source
snapshots. They disable real subprocess and socket calls, replace every API
call with a local Git-object model, and use an independent hash calculation.
The model serializes every request through JSON and UTF-8 before interpreting
it, rather than passing Python objects directly to the simulated server.

- **273 payload cases:** every possible single byte, deterministic varied
  binary strings, all-byte blocks, empty data, ASCII, Unicode, NUL, invalid and
  overlong UTF-8, a minimal PDF with a binary header, and a valid ZIP containing
  binary and Unicode entries. The dispatch made 140 base64 uploads and kept
  133 valid UTF-8 payloads inline. Every reconstructed payload was byte-exact.
- **Whole checkpoint:** PDF, ZIP, all-byte binary data, empty text, and
  Unicode/NUL text were committed in the local model. Five unrelated leaves,
  including executable, symlink, submodule, unrelated subtree, and unselected
  nested content, retained their full mode/type/hash identity.
- **Blob rejection:** wrong or missing uploaded SHA, and an upload exception,
  stopped before any tree/commit/reference creation. A wrong or missing hash
  produced the explicit binary identity mismatch error.
- **Tree and commit rejection:** inline NUL corruption, unrelated root mode
  changes, nested deletion, symlink mode corruption, truncated tree listings,
  and wrong commit parents/tree bindings all stopped before a reference move.
- **Concurrency:** a main advance immediately before the fresh-ref check and a
  non-fast-forward rejection during the patch both caused reconstruction on
  the new parent and preserved the concurrent writer's file. Three consecutive
  pre-patch races aborted after three attempts without attempting a ref update.
  A descendant appearing after a successful patch verified as `ahead`.
- **Other guards:** dry run and already-recorded files issued no writes;
  traversal, absolute paths, symlinks, absent files, journal gaps, cursor
  mismatch, and a size-changing read race were rejected before API calls. A
  second destination check failure stopped the reference update. Retries used
  the original frozen bytes even after the local file changed.
- **Wrapper and recovery:** the actual API wrapper was intercepted and checked
  for `--hostname github.com`, the fixed `AlecKriebel/Math` destination, and a
  structured base64 stdin body with no shell. A failed final ancestry check
  emitted no success receipt. A simulated local receipt write failure after
  saving retained the printed success receipt.

Evidence: `CONTROL_RESULTS.json`, `PAYLOAD_CONTROLS.json`, and
`API_EVENT_SUMMARY.json`. Reproduction from this directory:

```text
python3 -B independent_controls.py
```

The independent harness and evidence files are intended as tooling validation,
not as scientific checks of the publication contents.

## Concrete operational gap

**The reviewed `checkpoint.py` allowlist contains no PDF or ZIP file path.**
All 261 unique entries were present and valid UTF-8 when inventoried. Therefore
the present source can transport binary bytes safely in the tested model, but
it does not yet select the final publication PDF/ZIP. Add the exact intended
artifact paths to `NAMES` before publication, then inspect a dry-run receipt
for their byte counts, SHA-256 hashes, and Git blob hashes. This is an explicit
selection gap, not a defect in the binary encoding helper. See
`ALLOWLIST_REVIEW.json` for the complete source-bound inventory.

## Boundaries and remaining uncertainty

No live repository API mutation, Git command, branch change, shared index write,
Sheet/PR action, release, or Zenodo action occurred in this review. Writes were
confined to this review folder. No other individual was contacted. Two public
GitHub documentation pages were retrieved read-only to check the API contract;
the probes themselves were entirely offline.

GitHub documents base64 content for blob creation and the mutually exclusive
tree `sha`/`content` representations used here. It also documents the
`base_tree` overlay that the tool verifies after creation. These checks support
the API model but do not constitute an end-to-end service test. See the official
[blob API](https://docs.github.com/en/rest/git/blobs#create-a-blob) and
[tree API](https://docs.github.com/en/rest/git/trees#create-a-tree).

The production service's acceptance of the final artifact sizes, current
permissions, rate limits, and exact uploaded files remains untested. Upload
errors before the ref patch stop publication. The implementation keeps the
whole selection in memory and also creates base64/JSON representations, so it
is not a streaming uploader.

The existing per-file size/mtime check is not a transaction across all selected
files and does not defend against a local adversary who deliberately restores
size and mtime after altering a file. Keep the selected effort files quiescent
while taking a checkpoint. The journal check establishes numeric contiguity
and the last cursor, not semantic agreement of every record's contents.

Final ancestry or receipt-write failures can occur after `main` has already
advanced. The probes confirm that distinction; such an exception must not be
interpreted as proof that nothing was saved. A fresh read/dry run provides the
current object identities without forcing or rolling back the branch.

The strongest verified conclusion is byte-exact representation and guarded
checkpoint control flow for the bound source under an independently implemented
local API model. The exact remaining publication task is explicit selection
and source/hash binding of the final PDF/ZIP, followed by normal live receipt
verification by the owning task.
