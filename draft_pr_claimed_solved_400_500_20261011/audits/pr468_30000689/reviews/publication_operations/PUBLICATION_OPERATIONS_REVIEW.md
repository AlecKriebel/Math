# Independent publication-operations review — PR468

**Verdict: REQUIRED_CORRECTION. Blocking issues: 0. Required corrections: 1. Optional observations: 1.**

The archive-removal and tracker unknown-response mechanisms pass the tested contract. Branch installation preserves the captured latest-main tree outside attempt 30000689 and changes exactly one QUEUE row, but its acceptance check omits required corrections. Correct R1 before using that helper. This is an operations review; it does not accept the mathematical packet or establish any live publication state.

## Inputs and isolation

Reviewed the three frozen helper copies listed in `REVIEW_INPUTS.json`; read the existing `zenodo.py` only as the kit contract. The real kit client, credential reader, saved state reader, and apply command were never instantiated or called. All API boundaries, including GWS and GitHub, were replaced by in-memory mocks before invoking the frozen helpers. Tests mutated only `private_sources/fixtures/`. Safe packet, metadata, operation-context, and original-source copies are preserved in `private_sources/frozen_context/`. There were no remote writes, outside communications, shared checkout/index changes, commits, or pushes.

`MOCK_TEST_RESULTS.json` records **40 reproducible isolated cases**. Every harness assertion passed; two assertions deliberately establish the witnesses below. Rerun from this folder with `python3 -B private_sources/test_operations.py`. The frozen helper sources and context make the run independent of subsequent root repairs. No synthetic fixture is a public mathematical or publication artifact.

## R1 — required: integration permits an unresolved required correction

Frozen `integrate_pr468_publication.py`, lines 78–80, checks each accepted review's `verdict == PASS` and `blocking_issue_count == 0`, but does not require `required_correction_count == 0`. This differs from the replacement helper, lines 52–55, and from operation-plan steps 1–2: resolve all material findings and repeat fresh review until no issue remains.

Concrete witness `integration_required_review_issue`: start with the valid private baseline, leave review hash, package hashes, publication/tracker receipts, original PR, source scope, and main unchanged, and set the second review entry's `required_correction_count` to 1. Integration returns `branch_updated_verified` and updates the mocked existing branch. The same change is rejected before DELETE by `archive_required_review_issue`. Thus the final integration safety check has a reproducible false acceptance; this does not require an untrusted server, path attack, or race.

Required correction: make every complete-package review require zero required corrections before any remote mutation, including treating an absent/invalid count as failure. Preserve the report-hash binding. The regression criterion is that this witness raises before the first blob/tree/commit/ref mutation, while the zero-count baseline still succeeds. Root owns the correction and its new independent review; this frozen-input report remains unchanged.

## O1 — optional: concurrent registration can evade final uniqueness detection

`tracker_concurrent_same_doi` inserts an identical canonical DOI row after the helper's full-sheet duplicate search but before its append. The append then adds its own row and its returned-range readback succeeds. The helper reports `verified: true` with two DOI rows present. Its ordinary successful-append path checks only the returned row; the lost-response path also checks global DOI cardinality.

This is a concrete second-runner timing limit, not a demand for an unadvertised transactional Sheets append. It does **not** defeat the promised no-repeat behavior for lost responses in a serialized run. Keep one runner for this DOI. A final full-column duplicate check would detect this race before declaring verification, although it cannot undo an already completed concurrent append or provide atomic exactly-once semantics. No arbitrary sheet cleanup is proposed by this review.

## Verified mechanisms and exact limits

| Area | Checkable evidence | Result |
|---|---|---|
| Premature acceptance | Actual captured HOLD gate; stale round3 freeze; report-hash and packet drift | Archive and integration stop before remote mutation. Archive explicitly binds round4; integration reads the gate's named input and rejects current round4 bytes against the actual stale round3 freeze. |
| Same draft and retained files | Saved-ID mismatch, published record, wrong ZIP checksum, extra remote filename, changed PDF, metadata drift, unsafe file ID | Each stops before DELETE. Successful deletion targets only the exact ZIP ID at draft 23310484; retained PDF checksum/size and canonical metadata are rechecked. |
| DELETE204/lost outcome | Kit request contract rejects empty 204 JSON; mocked 204, successful DELETE with lost response, later GET loss and resumed invocation | One DELETE maximum; GET confirms ZIP absent. Resume after lost readback succeeds without a second DELETE. If the request did not reach the service and ZIP remains, repeat invocation fails for reconciliation. Already-accepted archive is idempotent with no deletion. |
| Tracker identity and registration | Production publication/title checks; header; DOI URL and bare-token duplicate search; existing exact and differing rows | Exact row contains problem/source locator, blank chat URL, confirmed DOI, canonical title, author/date/version, PR URL and disclosures. Unpublished/title-drift and preexisting duplicate/differing registrations fail. |
| Tracker unknown response | Successful append response lost; append not reached; subsequent invocation | A successful lost response recovers by full-sheet readback and does not append twice. An absent/unconfirmed row leaves `append_attempted_once`; rerun refuses another append. |
| Source/plan binding | `CONTEXT_CHECKS.json`: seven round4 frozen files; all 71 plan entries; all 15 original source files | SHA256 and declared byte lengths match; deposit metadata equals canonical metadata. No current install-plan drift or unintended private destination found. |
| Git integration | Latest-main unrelated file and row sentinel; original source hash and scope drift; changed main disposition | Accepted path creates a main-tree-based 93-file mock payload, exactly one selected QUEUE line changes, unrelated main bytes/rows survive, original claim status/3/5 are gated, unrelated original paths reject. |
| Ref race and recovery | Two-parent commit, nonforce PATCH, moved branch head, successful PATCH with lost response | Parents are original PR head and captured latest-main head. A normal competing descendant head causes non-fast-forward rejection and remains untouched. Lost update response recovers by reading the exact created commit. The receipt records that commit before the update. |

The helpers do not merge. Root must separately verify and merge the exact `branch_updated_verified` commit recorded in the receipt; the report is not evidence that a branch update or merge occurred. Latest-main preservation means the immutable main SHA captured for this installation, not an atomic lock on main during the whole operation. The later merge must account for any newer main changes.

The kit's stage/inspect/publish code uses the stable manifest state, preserves an existing matching PDF, uploads the absent replacement, verifies both files and metadata, and resolves a lost publish response by GET rather than repeating that POST within the same invocation. That contract was read, not run or tested against live Zenodo. Actual credential permissions, network/API behavior, public DOI resolution, and the later exact-head merge remain outside this offline review. No additional blocker is inferred from those unperformed live operations.

## Remaining gap and completion

This audit goal is **100% complete**. Operations readiness remains conditional on R1's fix and a new independent frozen-helper review, actual round4 packet acceptance, and the normal live receipt/readback sequence. O1 is the sole optional observation. No claim of stronger atomicity, malicious-authenticated-server defense, or ancestor-symlink hardening is made or required.
