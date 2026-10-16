# Accepted-state synchronization proposal, revision 2

This bounded infrastructure assignment is complete. The proposal mirrors exactly twelve completed primary acceptances and the explicitly accepted duplicate 20002052. All **30 revision-specific offline tests passed**, and the fresh read-only preflight reproduced the entire proposed state/history from the evidence and checked **13 targets, 145 bindings to 131 distinct files**. No live import was performed.

The complete proposed state and exact thirteen history lines are in `CURRENT_PLAN_v2.json`; their reviewable source bindings are in `bindings_v2.json`. The stdlib helper `accepted_state_sync_v2.py` defaults to dry-run and has no live apply option. Its only replay/recovery writer is confined to this revision's ignored temporary directory. The root owns any eventual live import.

## Preservation and exact revision boundary

The original nine first-party v1 artifacts were independently hashed and sealed before this revision was created. `V1_PRESERVATION.json` records their sizes and original hashes. They remain byte for byte unchanged, including the old ten-target plan and manifest. The old plan is historical and correctly stale against the new inventory and queue; it is not silently promoted to the current scope.

- Original v1 plan SHA-256: `ab03a74a381c889bc9ebe658e1ec874ac02ee0e3d76432479c71f621dcba0a98`.
- Original v1 manifest SHA-256: `a44e734e1094e3f5f588cd0d27f165401dc561c8951a703b1cbe7de3ab1b49a7`.
- Revision 2 plan SHA-256: `7c44f3ffbeda7e8eae96fc9ebfae785bdac2d70e3742eda4f98a884b546502eb`.

The original ten individual entries and all their evidence pointers/hashes are identical to v1. Only the explicit revision scope and current global inventory/queue bindings are refreshed; PR21, PR22 and the accepted PR22 duplicate are separately added. The helper requires the actual completed-primary inventory set, the explicitly requested set and the twelve primary entries to agree exactly. A subsequent completed PR makes this fixed proposal stale and requires a separately reviewed revision. PR8 and pending PR23 are outside this proposal.

## Proposed outcomes and original accounting

| PR | Selected ID | Accepted status | Original consumed budget | Existing DOI |
|---|---|---|---|---|
| 9 | 30005473 | preprint_published | 1/5 | 10.5281/zenodo.23074543 |
| 10 | 30005795 | already_solved | 1/5 | none |
| 11 | 30002867 | already_solved | 1/5 | none |
| 12 | 30005897 | already_solved | 1/5 | none |
| 13 | 11000263 | unsolved | 1/5 | none |
| 14 | 30005934 | already_solved | 1/5 | none |
| 15 | 30000819 | already_solved | 1/5 | none |
| 16 | 30000439 | preprint_published | 1/5 | 10.5281/zenodo.23088066 |
| 17 | 30000224 | unsolved | 4/5 | none |
| 19 | 30006390 | unsolved | 2/5 | none |
| 21 | 30001696 | already_solved | 1/5 | none |
| 22 | 20002011 | already_solved | 1/5 | none |
| 22 duplicate | 20002052 | duplicate | 0 additional; shares 20002011's 1/5 | none |

The twelve primary records preserve **16 consumed substantive attempts** in total. The duplicate adds zero, and this assignment creates no proof attempt. Every selected primary budget is checked against the explicit current queue cell, original attempt ledger, five-turn policy and acceptance counters where present. Missing/ambiguous budgets, gapped or duplicate ledger numbers, and any decrease in existing usage are rejected. No number is inferred from a stale catalog or narrative.

## New PR21 and PR22 bindings

PR21 is tied to original head `096aacd71a1dc6dd3a73bea3c1055877dc8c0451`, merge `eb1e4bbc83efb4b0dcc33d81395b7816be9c1c42`, and merged time `2026-10-01T20:30:15Z`. Its canonical acceptance, audit acceptance, accepted proof hash, full source record, original attempt ledger, canonical acceptance text, saved remote receipt and canonical manifest are independently bound. The original ledger is `ORIGINAL_attempt.json`, with one consumed attempt and limit five.

PR22 is tied to original head `5dff69d1f25ac585a87bd8c71bc9d9c136e8c13c`, merge `f5d341110d3a993575dd42862c1fa6462ecb71eb`, and merged time `2026-10-01T20:33:45Z`. Its canonical acceptance, audit acceptance, accepted source-status hash, full source record, numbered original ledger, acceptance text, remote receipt and manifest are separately bound. The ledger explicitly records `used=1`, `limit=5`, the consecutive original turn number, and `shared_duplicate=20002052`.

For both new primary records, the audit acceptance must agree on the selected ID, PR, original head, merge and status and must supply the exact canonical manifest SHA-256. The helper checks every canonical manifest member's actual file hash and byte count and rejects unsafe or duplicate manifest paths. A matching acceptance JSON cannot hide an altered accepted package.

The 20:55 UTC input check confirmed these bindings and the current thirteen exact source records. At 20:53:38 UTC the root separately queried GitHub for all twelve completed primaries. Its first-party `root_apply/FRESH_REMOTE_VERIFICATION.json` receipt was read and independently cross-checked against this plan's exact PR URLs, MERGED/non-draft states, original heads and merges. The receipt path/hash and attribution are recorded in `VALIDATION_RECEIPT_v2.json`. This subagent did not itself authenticate a new GitHub observation; the helper verifies pinned saved receipts. The root should keep the fresh remote result current and rerun the complete preflight immediately before import.

## Explicit duplicate semantics

The current manual queue correctly says duplicate 20002052 at 0/5, while the stale catalog still says queued/eligible. Ignoring that row would leave a separate research-eligible copy. A duplicate mirror is therefore required and is included expressly, using evidence stronger than a matching title:

- Canonical PR22 acceptance identifies primary 20002011, duplicate 20002052, accepted duplicate status and zero additional duplicate attempts.
- Canonical provenance identifies both source IDs and hashes the preserved full duplicate source record. That exact full record is checked against the actual pinned read-only source database and its current statement/review hashes.
- The original ledger explicitly shares this duplicate with primary 20002011 and fixes the owner's actual one-of-five usage. Canonical acceptance text records the same selection and accounting.
- The unique queue row must be duplicate, zero-of-five and without DOI. Any existing duplicate proof usage must be exactly zero; the helper will not erase a genuine extra turn to fit the proposal.

The duplicate state's `turns_used=0` means zero independent/additional attempts. Its `turn_limit=5` preserves the displayed existing queue value; it does **not** allocate an independent five-turn budget. This is explicit in `independent_budget_allocated=false`, `shared_budget_owner="20002011"`, `shared_turns_used=1` and `shared_turn_limit=5`. Its history event is `acceptance_duplicate_mirror_import` and says that the five-turn limit belongs to the shared owner. No new attempt folder, proof turn, paper or DOI is proposed for the duplicate. There is no unresolved source/accounting type gap for this accepted relation.

The three earlier duplicate counterparts 30005796, 30002868 and 30006391 remain deferred/ineligible with their original decisions. Their selected primary group evidence remains bound, and this revision creates no state or second budget for them. Historical desk priors are retained as historical assessments; an accepted current verdict is not written back into earlier reviews.

## Current-mirror meaning and preflight strength

The primary event is `acceptance_mirror_import`. Both event kinds expressly record a present-day human-authorized mirror of current acceptance and disclaim reconstructing historical readiness/candidate/verification transitions. The import timestamp is current; historical merged times are evidence, not invented history timestamps. Neither `candidate_turn` nor `readiness_review_hash` is fabricated. Unrelated state is preserved.

Deterministic event IDs bind the selected source, status, original budget, exact accepted source, original reviewed head, merge and evidence hashes. Replay reuses the existing event and import time and appends no extra history. A conflicting old mirror requires explicit revision review.

The checker verifies every evidence binding, current state/history preconditions, full proposed byte hashes, all current source hashes, unchanged unrelated state and shared duplicate accounting. It then **rebuilds the entire plan from the current acceptance evidence and original import timestamp** and requires exact equality. Thus an altered proposed status or history event cannot pass merely by refreshing the plan's byte hashes.

## Offline tests and protected scope

The thirty new tests use frozen copies of all current bound inputs and a small SQLite source database populated from the actual pinned source records. All semantic falsifications run only in isolated ignored temporary copies. No legacy rank/status/turn command or function is invoked. One test reads and evaluates only the actual legacy pure eligibility expression for duplicate status.

Tests reject pending/unmerged/unpublished records; crossed PR21/22 receipts; wrong exact head; wrong original budgets and numbered ledgers; altered canonical package members or audit manifest hashes; omitted eligible duplicate; wrong accepted duplicate/owner relation, status or source; requested or recorded extra duplicate attempts; changed current queue usage; pre-existing duplicate usage; missing primary budget; a second DOI owner; changed historical v1 bytes; and a scope omitting a completed primary. Further tests reject tampered proposed status/history even with refreshed byte hashes and a mismatched shared owner counter.

Positive tests verify exactly twelve primary outcomes plus one duplicate, sixteen original consumed attempts, no fabricated readiness/candidate fields, unchanged old duplicate decisions, thirteen-event idempotent replay, original import timestamp reuse and exactly-once recovery after an injected interruption between history and state writes. The original v1 thirty-one-test results remain a historical receipt; they were not overwritten or represented as newly rerun.

No live state/history, queue, catalog, historical assessments, source/canonical artifacts, prior mathematical audit files, Git state, PR state, publication or tracker data was changed. No external individual communication occurred.

## Operational limits and root-owned import

The legacy CLI lists `already_solved` and `duplicate` but omits `unsolved` and `preprint_published`. Direct state mirrors still preserve all four terminal strings because the ranking reader does not impose the CLI choices. Its actual eligibility expression permits only queued/unreviewed/ready, so all thirteen mirrored records become ineligible when consumers honor state. Current `review_hash` prevents a stale-review hold; `statement_hash` records the exact source.

This bounded proposal leaves four wider issues explicit:

1. Legacy ranking still unconditionally rewrites the manual queue into its old format, losing custom impact/findings/chat/DOI columns. Do not invoke the generator as an import side effect.
2. Catalog-only consumers still see the stale catalog until a separately reviewed operational or catalog change makes them honor acceptance state.
3. A deliberate legacy ready/in_progress override can reopen an accepted target with remaining turns. A separate accepted-terminal guard is needed to control such reopening.
4. Two-file mutation needs an exclusive writer. The ignored sandbox demonstrates a durable PREPARED intent receipt, exact before/after hashes, history-first ordering, idempotent recovery and rejection of unknown outcomes; it is not a production concurrency lock or live writer.

The root should fully review this proposal, retain its exact plan hash, independently keep remote acceptance verification current, rerun preflight immediately before mutation, obtain exclusive writer access, preserve all before/after hashes and create its own durable intent/completion receipt. Any changed inventory/evidence/source/state/history precondition requires stopping and a new reviewed proposal rather than automatic scope expansion or retry.

```text
python3 accepted_state_sync_v2.py --repo /Users/alec/Documents/Math --check-plan CURRENT_PLAN_v2.json
python3 -m unittest -v test_accepted_state_sync_v2
```

`VERDICT_v2.json`, `VALIDATION_RECEIPT_v2.json`, the research log and `MANIFEST_v2.json` seal this revision distinctly from the immutable original proposal.
