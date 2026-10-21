# PR948: focused publication reconciliation review

Verdict: **safe under the exact preconditions below**. I found no reason to prohibit one new invocation of the unchanged publish helper after a durable, explicit reconciliation of this specific pre-client failure. This is not permission to remove an intent guard after an uncertain publish request.

## Authenticated evidence and scope

Before source intake, I authenticated the actual core `accept_pr948.py` SHA-256 `3be81538c4e17e6b220208992a8d56422218f37773f84c8a690a4ab10a41d823` and unchanged repository kit SHA-256 `a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca`. I subsequently authenticated all seven operational sources against inventory `500866df6a5c92a38f133dbe7088da956bc52b54ade02b3fa258a07c3af4e002`, the current freeze and descriptor, the two current upload copies, saved stage/inspection/intents, and the exact saved kit-state ID. I read no other PR mathematics and made no authoritative, Git, account, or API mutations.

The successful unchanged-helper inspection, SHA-256 `ebb70a8ccf7d943a6fd9eeeba817b55625792fe76e8d33e35a287820b473d532`, says production ID **23422055** is **ready_to_publish**, matching the staged PDF (76,849 bytes; SHA-256 `14063ce9fef470a6a3875dc429a1c3d34372d60cbd73eb7e22e77b46b1639f60`) and ZIP (630,346 bytes; SHA-256 `ae7d51ded2f03cd307ec394728a94f3e2e6e568903905713da8bfdf0007a24d6`). It records no metadata normalization. Its source path verifies the remote metadata and server file list/checksums before returning that state. These receipts are checkable evidence of the root's real inspection; I did not independently make another API request or download private draft bytes.

## Why this failure was before any publish POST

The root reported an actual exit-1 traceback at core line 865 `guard()`, raised at merged-gate line 693. Its durable observation is `publication/ROOT_PUBLISH_ATTEMPT01_NO_POST_FAILURE.json`, SHA-256 `d0c06f750c618632d829b9ff6f323c0ed6a6ddda6283b0b10434e54d37687f63`. I did not witness the original process, and that observation is not the original raw traceback. My conclusion about the actual failure boundary relies on the root's trusted tool observation. The exact before/after dictionary difference is **unknown** and I do not infer its cause.

In the authenticated core, line 861 saves the intent, line 865 invokes the guard, line 866 constructs the client, and line 868 calls the kit with command publish. The exception at line 865 therefore prevents both later steps. The earlier kit invocation is explicitly command check; authenticated kit lines 411–412 return before saved state, client creation, or service calls. The kit's non-main module initialization defines functions/classes/constants and does not publish. An absent publish/failure receipt alone would not establish this fact: the exact failure site and authenticated control flow do.

I independently ran **20 inert checks** using unmodified selected AST definitions and in-memory doubles, with no network or Git calls. The actual core zenodo function saved an intent and propagated the simulated line-865 failure without token access, client creation, publish-command execution, or inner-try failure receipt. The tests also checked exact-ID rejection, inspect's inability to publish, already-submitted no-POST behavior, and one-POST counters including uncertain transport. Their source and actual results are sealed here.

## Conditions for the proposed one new invocation

1. Preserve the original intent's **exact 8,208 bytes**, SHA-256 `11527cb87e87a90a1b2b19965fd8ea61fbb11a2e09308c517eda359cc55984da`, in a unique exclusive history file. Verify its bytes and make the archive and reconciliation receipt durable before removing the canonical blocking intent. Do not overwrite, relabel as success, or lose the original attempt.
2. The durable reconciliation must bind that archive, the actual failure observation, the exact successful inspection and ID, this review seal, and the unchanged core/kit/inventory. Describe the attempt as aborted before client construction, not as a remote publish attempt or a withdrawal. Keep the before/after difference unknown.
3. Recheck that no operator/process is concurrently publishing this same saved deposit and that no intervening publish receipt or conflicting state has appeared. The reviewed inspection and saved kit state must still identify 23422055. Do not stage or create a replacement deposit.
4. Invoke the exact unchanged helper once, retaining all merge, acceptance, review, descriptor, exact-ID, fresh-GET and per-boundary guards. That helper validates stage/state identity, and both the kit and guarded client re-read the exact deposit; if it is already submitted they avoid a publish POST.
5. If the next invocation fails, reconcile its actual phase and outcome anew. Once a POST may have happened, inspect that same ID and preserve the uncertainty; this review does not authorize another automatic retry. Finish with the required independent public PDF/ZIP byte hashes and DOI resolution before reporting publication or advancing the tracker.

Archiving an aborted intent is a deliberate operator state transition, not normal helper idempotence. Under these conditions it restores the guard for one new invocation without weakening the frozen code. The counter is per invocation, so durability and single-operator control are necessary.

## Limits and remaining issues

No actionable issue remains in this narrowly proposed recovery. This is not a new full-package mathematical/priority review, account-wide absence-of-other-deposits certificate, independently witnessed original traceback, guarantee of future network success, or confirmation of publication. A subsequent guard can still abort safely. The inspection verifies metadata and server-advertised draft checksums; independent public byte verification remains mandatory after publication.
