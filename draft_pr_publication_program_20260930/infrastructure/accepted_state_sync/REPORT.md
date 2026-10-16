# Accepted-state synchronization: bounded infrastructure validation

Completed 2026-10-01 UTC. This is a proposal and offline validation for process metadata. No new mathematical claim, proof search, paper, DOI, tracker row, Git operation, shared queue regeneration or live state/history mutation was performed.

## Outcome

The legacy `state.json` is `{}` and `history.jsonl` is empty, while the manually maintained queue correctly records ten completed acceptances. The legacy catalog still lists those ten targets as queued at zero turns. A narrowly targeted current-acceptance mirror would prevent legacy ranking from automatically restoring those targets to a research-eligible status and would preserve their actual consumed budgets. **It would not protect the custom queue layout from a legacy rank rewrite.**

[accepted_state_sync.py](accepted_state_sync.py) is a concrete, stdlib-only dry-run helper. [bindings.json](bindings.json) fixes the explicit ten-target scope and hashes each existing evidence file. [CURRENT_PLAN.json](CURRENT_PLAN.json) contains the complete proposed state document, exact history lines, deterministic event IDs, per-target decisions, source and evidence bindings, before/after hashes and limitations. Its fresh read-only preflight passed for all ten targets and 59 file bindings. There is **no live apply command**. The only write/recovery routine is hard-restricted to this folder's ignored `tmp/` for offline demonstrations.

## Proposed targets, with original accounting

| PR | Selected ID | Accepted status | Original consumed budget | Existing publication DOI |
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

The table uses the explicit current queue `Turns` cells, independently checked against the original per-attempt ledgers and acceptance counters where present. Limits must match the current five-turn policy. No empty/stale catalog counter is substituted, no count is guessed from narrative findings, and a gapped or duplicated turn ledger is rejected. There are 14 consumed substantive attempts in these ten records; no new proof turn is invented.

Known duplicate selections remain 30005795 over 30005796, 30002867 over 30002868, and 30006390 over 30006391. Their explicit duplicate evidence is bound, and the helper checks that the counterpart is already ineligible in the current catalog. It does not allocate a second budget or write a new duplicate state. The three counterparts currently remain deferred with their existing holds. Other selected IDs have no additional duplicate group asserted by this proposal.

PR8 and every target that was pending at assignment are outside this fixed proposal scope, even if another audit finishes while this helper is being reviewed. A changed inventory invalidates this plan's binding and requires a fresh explicitly reviewed scope/binding update; it does not automatically add newly completed targets.

## Exact evidence and source validation

Each target must satisfy all of the following before an event is proposed:

- The inventory stage is exactly `complete`; its selected numeric branch, reviewed original head and merge commit match the acceptance.
- The saved remote receipt says `MERGED`, supplies the exact same original head, merge commit and merge time, and matches the PR number/URL when present. PR17's existing envelope does not contain a number/URL but does contain the exact head/merge/time and an independently recorded ancestor verification; it is bound to its explicit PR17 audit path and selected inventory identity.
- The acceptance record and current queue agree on the accepted status, and the selected queue row is unique and structurally parseable.
- Accepted canonical artifacts match the accepted artifact hash. The pointer/hash to canonical acceptance is stored. PR19 has no canonical `acceptance.json`; its existing authoritative audit acceptance JSON is paired explicitly with the canonical `attempts/30006390/ACCEPTANCE.md` pointer/hash and accepted `BASELINE.md` hash. No JSON acceptance is fabricated for it.
- The accepted source statement and full source record context match the actual pinned read-only source database. Current `review_hash` and `statement_hash` are computed from the actual pinned problem/prior-report payloads and compared with the catalog. A changed statement/source is rejected rather than silently rebinding a stale verdict.
- The original ledger, current explicit queue budget, policy limit and acceptance's original counters agree.
- A `preprint_published` record must have the identical existing DOI in acceptance, inventory, queue DOI cell and published-verification receipt. It must have a unique queue owner and a verified public record. An unsolved/known partial cannot acquire a new DOI.

Two narrow source encoding adapters were needed and are recorded, not hidden: PR10's preserved raw source record has a first-party `statement_audit` annotation appended; that sole explicitly named audit annotation is removed when comparing the original full upstream payload. Stripping mathematical/source fields is prohibited. PR17 records absence of a prior report as JSON `null`, while the pinned cache uses `{}`; only this empty-report representation is normalized. The accepted initial catalog review hash is also checked where present. PR9's compact source provenance directly supplies the upstream statement hash and original review hash rather than a full statement payload, and both must match current pinned source.

The helper verifies **saved, pinned remote receipts offline**. It neither contacts GitHub nor authenticates those receipts independently. Before any live import, the root should perform its exact current remote acceptance check, then rerun the read-only preflight immediately before writing. This limitation is explicit; a matching local hash is not represented as a fresh network observation.

## Mirror semantics and preservation

The event is named `acceptance_mirror_import` and uses the present import/proposal UTC timestamp. Its note and evidence explicitly say that this is a **human-authorized current acceptance mirror**, and that historical readiness, candidate and verification transitions are not reconstructed. Actual historical merge times remain evidence data, not synthetic history timestamps. No `candidate_turn` or `readiness_review_hash` is invented. Existing unrelated state and any genuine prior fields are preserved; an existing consumed counter may not be decreased.

An event's deterministic ID binds the selected ID, PR, accepted status, original budget, exact accepted source, reviewed head, merge and evidence hashes. An accepted replay reuses the original recorded mirror event and import time; it appends no duplicate history line and makes no state-byte change. A differing pre-existing mirror is held for explicit revision review instead of being overwritten.

The proposal does not edit `catalog.json`, `assessments.json`, historical `review_v2/reviews_*.json`, initial desk priors, manual impact values, findings, chat links, DOI columns or other queue rows. A historical estimate that a problem might be open is retained as a historical estimate; it is not rewritten to look like an accepted verdict was known earlier.

## Meaningful offline validation

[test_accepted_state_sync.py](test_accepted_state_sync.py) passed **31 tests**, all in isolated ignored temporary folders. It constructs a real small read-only source database and explicit independent acceptance/remote/ledger fixtures, then changes their semantic facts while refreshing hashes where appropriate. Thus wrong facts cannot pass merely because the new bytes have a fresh hash.

The tests reject pending/unmerged/unpublished records; wrong PR ID, original head or merge; stale acceptance bytes; changed exact source and catalog context; unaccepted replacement artifacts; duplicate selected queue rows and DOI owners; ambiguous/missing budgets or ledger counts; decreasing usage; an eligible duplicate counterpart; a new DOI on an unpublished partial; mismatched public DOI; incomplete history tails; unrelated state additions; and a concurrently changed reviewed-plan precondition.

Positive tests verify that dry-run leaves all inputs untouched, retains unrelated state and original budget, introduces no fake readiness/candidate transition, preserves duplicate selection without a new budget, imports once, replays without a byte change, and generates a new no-op plan with the original mirror timestamp. An injected interruption after history commit is recovered once from the durable intent receipt, with no duplicate event; an unknown concurrent state change is rejected without overwrite. Live-path replay is rejected.

Two tests use the **actual current legacy queue implementation**, not a restatement of helper logic: one extracts and evaluates its eligibility expression for all three accepted status strings; another imports it only in an isolated temporary fixture and verifies that its actual `record_turn` rejects a terminal mirror before changing state. No legacy `rank` function was run, even in a fixture.

## Legacy behavior and irreducible limitations

The legacy `STATES` CLI choices include `already_solved` but omit `unsolved` and `preprint_published`. This does not prevent direct state mirrors from working: `rank` reads the stored string without a `STATES` membership check, preserves it as `local_status`, and only makes `queued`, `unreviewed` and `ready` eligible. The three proposed accepted statuses therefore all become ineligible. Matching current `review_hash` avoids the `status_review_stale` hold, while `statement_hash` supplies explicit source provenance. The normal proof-turn command also requires an `in_progress`/`partial` prior state and rejects these mirrors.

Three limitations remain outside this narrow write scope:

1. **Legacy ranking unconditionally regenerates the entire manual queue**, using a different eight-column format, recomputing impacts/ordering and omitting Findings, Chat and DOI columns. State mirroring prevents requeue eligibility but does not preserve this presentation or all human-maintained data. Do not run the legacy rank/status/turn/assess commands against the live repository as a side effect of this import. A separate authorized queue preservation change would be needed before those commands are safe for the current layout.
2. **The current catalog remains stale until separately synchronized.** Consumers that ignore state and read only its old `eligible=true`/zero-turn rows would still see stale data. This proposal does not rewrite the catalog because the assigned scope prohibits that mutation. Root should make those consumers honor acceptance state or separately review a narrowly targeted catalog repair; no automatic broader repair is implied.
3. **A deliberate legacy ready/in_progress command can reopen an accepted record** with matching readiness evidence and remaining turns, because the CLI lacks an accepted-terminal reopening gate. The mirror prevents automatic requeue and direct new proof turns, but is not a permanent policy lock against a later explicit status override. A separate accepted-terminal guard could require explicit human-authorized reopening. No such transition, readiness reconstruction or shared code change is made here.

Two-file state/history mutation is not intrinsically transactional. The sandbox demonstrates a durable PREPARED intent receipt, exact before/after hashes, history-first ordering, state replacement, completed receipt, idempotent recovery and rejection of unrecognized outcomes. It is a protocol demonstration, not a live production writer or a concurrency lock. The root's eventual targeted writer should hold exclusive access, verify every reviewed precondition/evidence immediately, persist its own intent receipt, and stop on any unexpected outcome. The root owns all such mutations.

## Review and preflight commands

Run the helper from this dedicated folder. It has no network calls and no live mutation option:

```text
python3 accepted_state_sync.py --repo /Users/alec/Documents/Math --bindings bindings.json --output CURRENT_PLAN.json
python3 accepted_state_sync.py --repo /Users/alec/Documents/Math --check-plan CURRENT_PLAN.json
python3 -m unittest -v test_accepted_state_sync
```

Inspect the ten decisions, complete proposed state and exact history lines before any targeted import. If a bound source/acceptance/inventory/queue file changed, the old plan is stale by design. Refresh only reviewed evidence bindings and rebuild a concrete plan; do not weaken the validation or silently infer a budget to make it pass.

The first-party manifest records the helper, tests, proposal, checks and report. Raw temporary test work stays ignored. The prior PR21 priority-family files and its manifest were not modified.
