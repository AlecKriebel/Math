# Administrative service-driver adversarial review

2026-10-17T03:56:49.169028+00:00 — 100% of assigned source review complete. This is not a mathematical or preprint whole-package review. No external service calls or canonical script/package edits were made.

## P1 D01 — Advancing STATE before other checkpoint writes makes interruption unrecoverable

Reviewed `run_service.py`, lines 98,104. Inject OSError on CLAIM_REGISTRY.json save after STATE save. First complete raises, but STATE already includes1033 and next_pr1034. Retrying complete returns WORKFLOW_COMPLETED while registry stays PENDING and log/README never get the checkpoint.

Minimal correction: Use a durable completion event, idempotently reconcile registry/log/README even for already-completed PRs, then atomically advance STATE last. Use one shared state lock for completion and other state writers, and atomic replace for JSON.

## P2 D02 — Merge retry repeats a PR update and nests accepted text before noticing prior merge intent

Reviewed `run_service.py`, lines 82,86. PATCH succeeds; merge command fails with PR still open. First invocation leaves MERGE_INTENT. Second merge PATCHes again, embedding the first full accepted body as preserved original, then fails at existing MERGE_INTENT. Counterexample produces two accepted headers and two PATCHes for one merge request.

Minimal correction: Save one stable original-body snapshot and intended acceptance payload before first write; record PATCH/ready intents and reconcile exact live readback on retry. Check unresolved MERGE_INTENT before any further PR mutation.

## P2 D03 — Historic tracker receipt permits merge after the required DOI row changes

Reviewed `run_service.py`, lines 79,91. After track, another authorized editor deletes or changes the row. merge consumes only local TRACKER_VERIFIED and attempts external merge without any Google read; complete likewise accepts the historical receipt. Offline probe confirms zero GWS calls before merge attempt.

Minimal correction: Re-resolve the intended gid and verify current header, one DOI match and exact full row immediately before merge and final completion; update observed row number if concurrent inserts moved the row.

## P2 D04 — Exact reviewed head is accepted on an unintended base branch

Reviewed `run_service.py`, lines 36,37,87,88. Return an open same-head PR whose base.ref is other-branch. Driver performs acceptance PATCH and attempts gh pr merge; no assertion requires main. A successful merge would pass head-parent proof and completion despite reaching the wrong base.

Minimal correction: Pin expected base repository and main in config; assert them on each live read and immediately before merge. Where base-retarget races matter, ensure final merged base is also checked and record it.

Seven offline fault/control probes passed; see PROBE_RESULTS.json and probe_driver.py. Reviewed source bytes are preserved as REVIEWED_*.txt. prepare_service_configs.py has no additional actionable finding in this narrow review. Root fixes and verification remain required before external execution.
