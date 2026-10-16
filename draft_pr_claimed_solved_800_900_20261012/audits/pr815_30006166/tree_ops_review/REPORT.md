# PR815 scoped tree publication adaptation review

Decision: **CLEAR** for the sealed PR815 revision and the four reviewed helper versions. Review completion: **100%** at 2026-10-14T04:30:50.236799+00:00.

## Claim and scope

The adaptation constructs a tree from the fetched main tree plus explicit reviewed regular-file entries, preserves all other tree entries and all queue bytes outside problem 30006166's unique row, and leaves the shared checkout, local main branch, and shared index untouched. This review covers `scoped_git_tree.py`, `prepare_pr_revision.py`, `record_publication_main.py`, and `checkpoint_main.py`; it does not reopen the accepted mathematics or publication package. It authorizes no remote operation by this reviewer.

## Independently verified prepared revision

- Prepared commit: `eba2384c210aa36ee748e141a79079bd1e6f9cf5`; fetched main base: `6a1fec109652ebcd8735012fda7d3a1b65df7969`.
- Both parents are the frozen old PR head and the recorded current main base, in that order.
- All **192** mapped Git blobs have the exact SHA256 values in `FINAL_PR_MAPPING.json`.
- Target subtree is exactly `10b95122c72fb715d21fb5567d95959c39e95ec0`, matching the expected target from the final package reviews.
- Diff has **193** paths, exactly the receipt list: the 192 explicit target files and the queue.
- Removing the unique target row from both queue versions leaves byte-for-byte identical data.
- All **182863** recursive entries outside the target subtree and queue retain exact mode/type/OID values.
- The receipt remains a preview (`pushed: false`). These checks used Git reads and independent SHA256 computations; no network operation was performed.

## Tree helper adversarial checks

A private bare fixture exercises replacement, creation of nested trees, Unicode and space-containing names, an unchanged executable, symlinks, a submodule/gitlink, invalid UTF-8 names, and names containing tab/newline. All untouched entries retain exact modes, object types, and OIDs. A no-op tree patch reconstructs the identical root tree. Eighteen invalid path, invalid object, and file/directory collision cases are rejected, including traversal through a regular file or symlink, directory replacement, both insertion orders of a colliding edit, nonblob OIDs, uppercase/short OIDs, absolute paths, dot segments, double separators, backslashes, and NUL.

The helper reads complete immediate tree inventories with NUL-delimited Git output and writes trees with NUL-delimited `mktree`; names from existing entries remain raw bytes. Only the ancestor trees of named updates are reconstructed. Git performs canonical ordering. It never deletes an entry. All named output leaves have the explicit mode `100644`; the 192 sealed target entries and the existing 408-file own checkpoint scope all have that mode, so this policy causes no unintended current mode change. Unnamed executable/symlink/gitlink entries were independently preserved.

## Caller and remote-write safeguards

`prepare_pr_revision.py` restricts mapped entries to the selected attempt, checks file SHA256 values, refuses leaf symlinks, requires an open PR at its recorded head and a compatible unique queue row, and checks the final diff scope. Preview is default; pushing requires both `--push` and CLEAR. Its ordinary non-force push preserves old-head ancestry and retains an ambiguous failure receipt. The readback repeats only metadata reads and refuses further mutation on an unconfirmed new head.

`record_publication_main.py` requires CLEAR, a production published record with a Zenodo DOI URL, a merged PR contained in the refreshed main base, and unchanged protected core hashes. It refuses receipt paths overlapping protected core and permits only explicit shard/target files plus the queue. It produces a child of the freshly fetched main tree and uses a non-force main push. On concurrent main advance, it refetches and rechecks the accepted core and queue before reconstructing the receipt-only tree. Other failures stop with a retained receipt.

`checkpoint_main.py` resolves only explicit own-shard pathspecs through Git's cached/other non-ignored inventory, then checks every returned name remains in the own shard and is a present nonsymlink file. Missing tracked files fail rather than becoming deletions. Its candidate preserves all other main entries, checks output scope, and pushes a child of refreshed main without force. Shared index/checkout commands and local main updates do not occur in any reviewed helper. Fetches may update remote-tracking information and object-writing commands populate the object store; those are part of the root's operation, not checkout/index mutations.

## Limits and exact remaining gap

This is a CLEAR verdict for the concrete sealed preview and the reviewed helper hashes in `VALIDATION.json`, not for arbitrary future mappings. Named leaves use regular mode 100644; future executable/symlink mappings would require a distinct mode policy. Local hash verification and later `hash-object` reads are separate steps; as with the prior approach, independent byte verification of each resulting candidate remains the binding evidence if source files could change concurrently. The root's verified current candidate passes that evidence. Remote pushes and production publication state were not exercised by this reviewer. There is no remaining gap in the requested local tree-adaptation audit.

## Artifacts

`review_checks.py` reproduces the private fixture checks and the read-only sealed-preview checks. `VALIDATION.json` records source hashes, all mapped file hashes, checked OIDs, preservation results, and fixture rejection cases. The tiny fixture is under `private_sources/fixture.git`; shared repository refs and index were not written. No helper or core file was edited, and no external communication occurred.
