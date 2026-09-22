# Independent workflow audit

Reviewer: shard 5 reviewer, independent of the workflow implementation. Initial audit: 2026-09-22 UTC. Scope: `queue.py`, `review_v2/merge.py`, their tests, and documented lifecycle. Bounded review; no production queue, policy, assessments, or source cache was changed by this reviewer. All mutation probes used temporary synthetic fixtures from the existing tests.

The initial 26 regression tests passed. Seven additional adversarial probes exposed the findings below. The parent was notified and is implementing corrections; the initial findings are preserved here pending independent retest.

## Findings

### F1 — P1: A routine assessment update can readmit a known solved problem

In `queue.py:267–282`, `assess` replaces the entire existing assessment with the supplied file. Omitting `holds` or `resolution` therefore deletes previously recorded primary-source findings, despite the documented requirement for explicit `clear_holds` evidence.

Reproduction: take the five-turn fixture, clear its attempt state, set its assessment to `holds=["primary_source_resolution_found"]` and `resolution="already_solved"`, then submit the documented ordinary assessment fields with the current hash but without those two optional fields. Observed transition: `already_solved`, ineligible → `queued`, eligible, no holds. No clearance evidence was supplied.

Required correction: preserve existing holds and resolution by default. Require explicit, checkable evidence for removing a resolution or clearance. Regression should assert that a new score alone cannot restore queue eligibility.

### F2 — P2: `partial` bypasses readiness requirements

In `queue.py:227–247`, readiness checks apply only to `ready` and `in_progress`. `record_turn` also accepts `partial`. An untouched candidate can be assigned `partial` without evidence and immediately record its first substantive turn.

Reproduction: clear the five-turn fixture state; invoke `status partial` without evidence; invoke `turn --outcome continue`. Observed state: `in_progress`, one turn, `evidence={}`. No exact claim, literature check, prior-gap review, or duplicate check had been required.

Required correction: retain a content-bound readiness marker and require it whenever entering or continuing proof development, including via `partial`; keep the marker separate from the latest status note/evidence.

### F3 — P2: Exhaustion can be bypassed by manually creating a late candidate

After five unsuccessful turns, `status candidate_result` and `status independent_verification` are unrestricted. Supplying the ordinary verification fields then permits `verified_solved`, even though no candidate was recorded within the allowed five turns.

Reproduction: record five `continue` turns, then those two status changes, then `verified_solved` with current hash and nonempty required fields. Observed final state: `verified_solved`, five turns. The history contains five unfinished turns followed by the unbudgeted candidate transition.

Required correction: bind candidate provenance to a recorded `turn --outcome candidate` event at or before the limit, and preserve it through verification. A failed verification may not restart development beyond the remaining budget.

### F4 — P2: Effective merge overrides are not validated

`merge.py:30` validates original reviews, then line 43 overlays unvalidated `adversarial_overrides`. A probability of 2 was written to active assessments and v2 was activated. An override with a mistyped unknown ID was silently ignored, which could omit a known-resolution exclusion.

Required correction: reject unknown override IDs and validate every effective merged record, including allowed routes/decisions, finite score ranges, notes, and hold/evidence structure, before replacing any active file. At the audit checkpoint all 47 actual override IDs and score values were valid; the issue concerns future edits and fail-closed behavior.

### F5 — P2: Re-running merge silently overwrites later current assessments

`merge.py:43–55` preserves prior holds and sources but replaces later individual scores and reasoning with the initial shard snapshot. It writes no assessment history for that replacement.

Reproduction: merge once, update the current record to `p_solve=.001`, a later source-audit note and `reviewed_at`, then merge again. Observed values revert to the original `.08` and original note; no assessment history exists in the fixture.

Required correction: make activation explicitly one-time, reject a rerun when current assessments have diverged, or preserve later edits with a clear migration and history policy. The immutable initial ledger should not silently overwrite the current assessment layer.

### F6 — P2: Merge can partially activate before discovering invalid/missing inputs

`merge.py:57` rewrites assessments before reading `policy_v2.json` at line 58. Removing that policy file produces `FileNotFoundError` after assessments have changed while the old policy remains active.

Required correction: read and validate all inputs and prepare all outputs before publication; stage file replacements and provide a recoverable activation boundary. At minimum missing or invalid input files must fail without mutation.

### F7 — P3: Retired-row hold ordering is not reproducible across processes

`queue.py:170` forms removed-record holds with `list(set(...))`. Using hash seeds 1, 2, and 3 yielded different hold orders and different catalog bytes from identical source data. Active candidate ranking order and active catalog bytes were identical in the same cross-process probe.

Required correction: use stable ordered deduplication or sorting for retired holds. This affects deterministic exports and review diffs, not mathematical EV ordering.

## Checks that passed

- All 26 existing tests passed on the initial implementation.
- A source status change to solved produced `upstream_resolution_claim` and `assessment_stale`, excluded the record, and preserved assessment-file bytes.
- Missing source cache, wrong cache revision/IDs, incomplete coverage, and duplicated assignments are rejected by the existing tested paths.
- Ordinary recorded turns stop at five and status changes preserve the numeric turn counter.
- A candidate recorded on the fifth turn is preserved for verification.
- Large searches and missing proof routes cannot enter the five-turn working queue.
- Active catalog bytes were identical across three independent processes/hash seeds. Age uses a fixed policy reference year.
- Shard 5 has all 2,576 individual reviews, exact assignment order, and unique IDs. At the audit checkpoint other shards were still completing, so this audit does not claim complete-program coverage or activation.

## Retest status

Pending parent corrections and a fresh independent run. No mathematical solvability or literature status is certified by these workflow tests.

## Independent retest — 2026-09-22T05:13:17.188209+00:00

All seven initial reproductions were rerun against the corrected implementation using temporary fixtures. The 34 current regression tests passed.

| Finding | Retest result |
|---|---|
| F1 | Fixed: an ordinary fresh assessment preserves the resolution and exclusion hold; the row remains ineligible. A resolution-only assessment also produces a known-resolution hold even when local status says queued. |
| F2 | Fixed: entering partial without current readiness is rejected, and recording a turn also checks a separate readiness hash. |
| F3 | Fixed: manual late candidate promotion is rejected. A legitimate candidate recorded on turn five still proceeds through independent verification to verified_solved. |
| F4 | Fixed for reproduced cases: invalid effective scores and unknown override IDs are rejected before any active file mutation. |
| F5 | Fixed: the merge manifest binds the activated assessment bytes; remerge over a later assessment is rejected and preserves the newer file exactly. |
| F6 | Fixed for invalid-input failure: missing policy is rejected before active files change; all outputs are prepared and staged before replacement. |
| F7 | Fixed: retired-row catalog bytes now match across hash seeds 1, 2, and 3. |

Additional safeguard verified by the current tests: changed-source reassessment requires an explicit fresh five-turn note, route, decision, and policy; preserved old semantic fields cannot silently stand in for that rereview.

No unresolved blocking finding remains among these bounded probes. File replacement across assessments, policy, and manifest is sequential, not a filesystem-wide transaction; abrupt process termination or disk failure between replacements was not fault-injected. The final manifest acts as the activation marker. This is a workflow audit, not an assertion that any mathematical candidate is solved or has received exhaustive literature verification.

Retested file fingerprints:

- `queue.py`: `f72aee023f837bad092da58531c2cc069ce2cf094e835d090221107d20f07ab2`
- `review_v2/merge.py`: `3a9ec162c25b867f759f42736b37b15c2b92b18693d7b0f903cc26b589372ef1`
- `test_queue.py`: `9db927eda68f406cea3dcb637355f757f637b09ab71b1745a132e88cc1634f4f`
- `test_merge.py`: `ebe324ad074626dd93da88afe80e23f10b6c91893d5890ea8a37f6e4afe47d1f`
