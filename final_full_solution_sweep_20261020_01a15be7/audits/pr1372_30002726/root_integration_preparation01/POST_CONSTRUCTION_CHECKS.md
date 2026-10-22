# Root checks and construction boundary

This folder contains inert data and GET-only verifiers. It contains no
Git/service mutation driver. The root1208integration HOLD must be resolved
by root before ANY Git mutation. Root must independently re-adopt the exact
plan/public pointer and perform fresh complete account/DOI/ledger/public
duplicate and live PR/main checks. Dated preflight is not action clearance.

The plan uses original head d34aba3697196aff2e4fc06e29f71afb5d793499 and
main31fe66f18508441733a0e25e0fc295f5e25cc010. Main was equal at both plan
observations and again18:33:48UTC. If main moves, create a NEW preparation
against latest main; do not amend this closed folder. Recheck that the exact
original queued target row still matches. Any changed target row or existing
project on main requires reconciliation/HOLD, not forced replacement.

1. Verify this folder using verify_closed_preparation.py with the separately
   supplied MANIFEST SHA256, then run the offline verifier command below.
2. In root's separate approved action area, reconcile/create only the unique
   blobs in PAYLOAD_CATALOG.json. The32 Git blob identities represent34
   selected paths;14 original payloads were fetched from pinned GitHub blobs
   and match the prior cache. Unqueried new blob presence is unknown, not
   asserted absent. Never rely solely on a successful request return code.
3. Construct a tree using the complete pinned main tree as base and exactly
   the34 TREE_OVERLAY_TEMPLATE tree_elements. Each path is a regular blob.
   The project is TOP-LEVEL initial_odd_ears_30002726, not an attempts child.
   Expected complete root is dabbe2a466b4ce6c034f4355f1c948f99d500430.
4. Construct a commit with ordered parents [originalhead,currentmain] as
   recorded by the plan. No commit SHA is predetermined: metadata matters.
   The first parent ensures any later original-branch update is a fast-forward.
5. Before moving any ref, run the GET-only candidate verifier with the actual
   candidate SHA. It checks ordered parents, complete expected root, exact
   shallow Merkle siblings,33 project leaves and directory namespace, all
   selected modes, the queue's exact prefix/suffix preservation and every
   unique selected blob's complete actual bytes/SHA256. It rechecks all
   immutable scientific/review inputs before and after reads.
6. Root must then repeat live original-head/main/PR/duplicate/CASE checks
   before any existing-branch update, draft readiness or merge. If a response
   is ambiguous, inspect actual remote state and reconcile before retrying.
   No force-push or unrelated tree overlay is part of this plan. Refresh
   and verify the exact actual PR diff and integration state before merging.

Read-only commands, from this folder, using separately trusted hashes:

    python3 -I -S -B verify_closed_preparation.py --expected-sha256 MANIFEST_SHA256
    python3 -I -S -B verify_git_candidate_readonly.py dbe37e568333ca9b50a9f19121e435354af4c5aa4089e088e6ea74392db43c28 --offline
    python3 -I -S -B verify_git_candidate_readonly.py dbe37e568333ca9b50a9f19121e435354af4c5aa4089e088e6ea74392db43c28 ACTUAL_CANDIDATE_COMMIT_SHA

The last command has NOT run against an actual new commit: none was created.
Its complete readback path passed an explicitly labeled in-memory mock with
40 mocked GETs;15 active scope controls failed as intended. This is test
coverage, not an actual candidate/branch/merge certificate.

The original fourteen-file manifest/verifier remains byte-preserved. Its
strict recursive scope intentionally rejects added PUBLICATION.md or
publication/ contents. LEGACY_MANIFEST_SCOPE.json records actual isolated
original14 PASS and plus-pointer rejection. PUBLICATION.md explains separate
historical replay and the current publication source's own reproduction.
