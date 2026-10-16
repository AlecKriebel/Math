# PR411 prepared scientific package updater

This is a software preparation artifact. No scientific conclusion, priority verdict, production object, branch update, or PR body update was made. The parent controls the actual packet, body approval, plan approval, and any later invocation of apply.

`update_package.py` uses Python's standard library and the configured `gh api` session. It never reads credentials, touches the git index, invokes checkout/commit/push, changes QUEUE, changes the PR title, or writes outside the explicitly mapped scientific prefix. Its public plan contains hashes and metadata; exact native request/response custody stays under the case's `private_sources/package_update_preparation/`.

The parent-provided spec has exactly these top-level fields:

```json
{
  "schema": 1,
  "package_root": "/absolute/case/prepared_packet",
  "files": [
    {
      "local_path": "/absolute/case/prepared_packet/README.md",
      "remote_path": "unsolved_math_prioritization/attempts/6800014/README.md",
      "sha256": "exact SHA256 of every local byte",
      "blob_sha": "exact Git blob SHA1 of every local byte",
      "mode": "100644",
      "size": 123
    }
  ],
  "body": {
    "local_path": "/absolute/case/parent_approved_body.md",
    "sha256": "exact SHA256 of UTF8 body bytes",
    "complete_packet_approved": true
  },
  "source_receipt": {
    "local_path": "/absolute/case/SOURCE_RECEIPT.json",
    "sha256": "exact independent source receipt SHA256"
  },
  "commit": {
    "message": "Parent-approved commit message\n",
    "author": {"name": "approved name", "email": "approved email", "date": "2026-10-13T00:00:00Z"},
    "committer": {"name": "approved name", "email": "approved email", "date": "2026-10-13T00:00:00Z"}
  }
}
```

The example is a schema illustration, not an actual approved packet or a runnable spec. Every regular file in `package_root` must appear exactly once; the root must be inside this case. Private paths, symlink ancestors, symlinks, FIFOs, unexpected files, duplicate mappings, incompatible source objects, and mismatched SHA256/Git blob/mode/size pins are rejected. Candidate bytes are used only as opaque bytes. Source receipt metadata reconstructs the complete selected source tree and binds its independent digest to the native source; the helper does not need to open the source paper.

Run `python3 update_package.py plan --spec SPEC --plan-out PLAN` for a read-only remote plan. `PLAN` must be a new file directly in this preparation directory. The first work is a fresh native PR/ref/source/QUEUE gate; it checks OPEN draft, the fixed head/branch, original QUEUE blob and bytes, and selected ID/status/turns derived from the table header. The returned plan digest pins candidate bytes, receipt, old/new body, title, complete immediate-tree replacements, and the exact predicted new commit.

Only an explicitly approved exact plan can be applied: `python3 update_package.py apply --spec SPEC --journal JOURNAL --approved-plan-sha256 DIGEST`. `JOURNAL` must be new and directly in this preparation directory. Apply recomputes the plan from fresh native evidence before accepting the digest. Each external mutation has a durable fsynced intent and exact private request custody. Object creation precedes one nonforced ref PATCH. Native commit identity verifies the predicted SHA/tree/parent/author/committer, while API message text may normalize away the final newline; no historical raw commit hash is inferred from normalized API text. All mapped native file bytes/modes, root preservation, QUEUE bytes, head, draft/open state, and body/title pins are verified before a separate body-only PATCH. The parent-approved body must describe the prepared complete packet before new whole-package reviews.

If any request or readback is uncertain, STOP. Never rerun apply with its existing journal. Use `python3 update_package.py reconcile --journal JOURNAL --approved-plan-sha256 DIGEST` for GET-only observations. Reconciliation rebuilds the deterministic replacement trees from the authenticated original root and checks the exact planned commit and every mapped native byte. It distinguishes confirmed complete, branch confirmed with body pending, and source observed without branch confirmation. Stale source GETs cannot establish that a write did not occur. Reconciliation never retries or resumes a write; a pending body requires a separate parent-controlled recovery decision.

GitHub's native ref API has no atomic compare-and-swap. Fresh immediately preceding ref/PR/QUEUE/body/title reads plus `force:false` reduce the race, and exact final verification detects drift, but cannot eliminate the interval between read and PATCH. The same limitation applies to body PATCH without an atomic body lease. Native API object identity is trusted for commits; immediate trees and blob bytes are independently SHA-verified. An unexpected server commit serialization/signature produces a safe stop before the ref PATCH.

Validation: `python3 test_update_package.py` uses synthetic offline models, including independent `git hash-object --stdin` verification of the planned commit. It exercises status/turns/head/body/title drift, truncated and omitted tree entries, file/digest/mode/private/symlink/FIFO/extra rejection, sibling preservation, errors before objects/ref/body, lost ref response with stale and later GET reconciliation, lost body response, and successful normalized-message readback. Mock results carry `evidence_kind: offline_mock`; they are not native success receipts. `NATIVE_GATE_REPORT.json` documents actual GET-only preparation evidence, with zero writes.
