# PR421 author-packet operation

Prepared on 2026-10-12. No live plan or remote write was executed in preparing this helper. The root researcher controls candidate approval, the live read-only plan, and any later `--apply` invocation.

`update_draft_pr421.py` uses the GitHub Git-data API through existing `gh` authentication. It does not access or print authentication values. It is specific to `AlecKriebel/Math`, draft PR421, and `research/20001515-explicit-cubulation`. It never modifies a checkout, index, QUEUE, PR title/body/comments, main, merge state, or release.

## Manifest and commands

All local paths are relative to this case folder (`audits/pr421_20001515`), and each remote path must be strictly below `unsolved_math_prioritization/attempts/20001515/`. The manifest is a positive allowlist, not a directory scan:

```json
{
  "schema_version": 1,
  "expected_head": "d5bf8b5a25cabb177433338fae60af52ebfecf1c",
  "expected_branch": "research/20001515-explicit-cubulation",
  "entries": [
    {
      "local_path": "global_candidate/author_packet/ATTEMPT_1.md",
      "remote_path": "unsolved_math_prioritization/attempts/20001515/ATTEMPT_1.md",
      "sha256": "c022afdfe003d0692a032cee48855ddf712de22953b358b895c485215875d8a6"
    }
  ]
}
```

Run from any directory. The current root candidate is `global_candidate/packet-update-manifest.json`; the command below is documentation and has not been executed:

```sh
python3 -B operations/update_draft_pr421.py \
  --manifest global_candidate/packet-update-manifest.json \
  --expected-head d5bf8b5a25cabb177433338fae60af52ebfecf1c \
  --expected-branch research/20001515-explicit-cubulation \
  --run-id root-reviewed-plan-01
```

The example assumes the case folder as the shell working directory. Without `--apply`, the helper makes only GET requests. To execute an approved candidate later, use the same explicit bindings, a fresh run-id, and `--apply`. Every run writes private journals and receipts under `private_sources/operations/runs/<run-id>/`. Existing run directories are rejected.

The helper uses the root-confirmed checkout identity, `Alec Kriebel <me@aleckriebel.com>`, for both new author and committer. A fresh UTC date and exact commit specification are durably recorded before any object creation. Candidate bytes remain pinned in memory after their complete hash check.

## Gates and mutation order

Before opening even the candidate manifest, the helper reads fresh PR421 metadata and its branch ref. It requires OPEN, draft, the exact expected SHA, branch, and repository. It reads QUEUE at that exact head, derives column positions from its header, locates one exact `20001515` row, and requires `Status == claimed_solved`.

It then validates every manifest entry and opens every component without following symlinks. All candidates must be regular files confined to this case; traversal, duplicate paths, private/runtime/credential paths, and recognizable authentication secrets are rejected. Every SHA-256 must match before any POST. The current full PR tree must be untruncated. Existing symlinks or submodules cannot be replaced.

The complete expected tree is the exact base-tree leaf inventory with only the positive allowlist replacements/additions. Existing modes and all unrelated leaves and directories, including empty directories, are preserved. The helper computes Git blob, tree, and unsigned commit identities locally. If GitHub serializes an object differently, the helper stops unless the exact expected object can be verified by read-only access.

The second administrative gate precedes blob creation. Before every POST or PATCH, a journal intent is appended and fsync'd. An exclusive durable source-head claim prevents a new run-id from blindly repeating uncertain writes at the same old head. The order is blobs, tree, commit, a durable created-commit record, complete parent/tree verification, a third fresh administrative gate, and one non-force PATCH.

The last read is a precondition, not an atomic compare-and-swap supplied by GitHub: `force:false` rejects a concurrent branch advance to a sibling commit. A concurrent force rollback by another actor is outside this protection. The root should maintain exclusive control of this draft branch during the operation.

## Recovery and actual-head receipt

No failed/unconfirmed write is automatically retried. Object response loss is reconciled by GET of the expected content-addressed object. Ref response loss is reconciled by fresh PR/ref readback and, if needed, a GitHub comparison proving that the created commit is an ancestor of the actual head. If that proof fails, the helper stops uncertain. A published ancestor establishes historical publication evidence. Current-packet verification additionally requires every exact candidate byte binding at the actual head, current OPEN and draft state, and the exact `claimed_solved` QUEUE status. A final PR/ref read checks that the head did not change while the candidate bytes were read.

If publication is observed but any current-packet condition fails, the apply run durably records `publication_observed: true`, `current_packet_verified: false`, the actual readback and drift reasons in its journal and receipt, then raises `PacketDrift` and exits nonzero. It never retries the mutation. A drift receipt uses `result: published_current_packet_drift`; only a passing current packet uses `published_current_packet_verified`.

After process interruption, the root can inspect the existing journal using only reads:

```sh
python3 -B operations/update_draft_pr421.py --reconcile --run-id ROOT_RUN_ID
```

Reconciliation never resumes writes. On current-packet drift it emits structured historical publication evidence with `current_packet_verified: false`, raises `PacketDrift`, and exits nonzero. Its passing result is `current_packet_verified_by_read_only_reconciliation`. It does not rewrite the original journal/receipt. A journal without a ref intent reports that no ref intent was recorded; it does not grant permission to retry objects. Do not remove source-head claims or start another apply against the same head without an independently checked disposition of the earlier run. A partial/unreadable journal stops reconciliation.

The receipt binds manifest SHA-256, every local/remote file pair and SHA-256/Git blob SHA, exact parent/tree/created commit metadata, actual PR head and branch, OPEN/draft readback values, the header-derived QUEUE row, and candidate hashes read from the actual head. That actual head is the source for the subsequent whole-package adversarial review.

## Offline evidence

The private fixture driver is `private_sources/operations/test_fake_api.py`. It uses a separate recursive Git-tree serializer and fake API. Run normal and optimized modes with `python3 -B` and `python3 -B -O`, respectively. Public JSON results bind the helper SHA-256. There are no bare assertions in security gates or the driver. No fixture, simulated journal, runtime directory, or private source is on the public output allowlist.

The earlier preparation is preserved under `history/preparation_v1_20261012T232846Z/`, with its original helper SHA-256 `3526d36e6f9e99629c56126e1d34c2a05ed682a68db6d357ae733e1c44d8bea3` and seven original public artifacts. That version is historical evidence and must not be executed. The current top-level helper and its current hash-bound receipts supersede it.
