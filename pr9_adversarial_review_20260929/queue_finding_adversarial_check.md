# Adversarial check of the provisional queue finding

**Reviewed head:** `a29887ed0e341851d02fa992c26500d4089267be` (PR #9).  
**Reviewed base:** `01358d66fc67d1c462bddf31c0d4ee5b120e6737`.  
**Scope:** Queue reproducibility/workflow only. No theorem proof was rerun.  
**Checkpoint:** 2026-09-30 04:42:20 UTC; 100% of this assigned check complete.

## Verdict and corrected classification

The reproduction is safe, genuine, and successful: the exact head's `rank()` replaces the edited target row with `queued`, `0/5`, and `eligible=true` in an isolated one-record database. However, **the proposed classification as a new P2 PR defect or merge blocker should be withdrawn**. The repository already deliberately maintains its live queue manually because the older generator discards maintained statuses and additional columns. That incompatibility and the empty global state/history files predate this PR.

The remaining supported finding is a **documented repository-wide conditional regeneration risk**: running the older `queue.py rank` or another command that calls it can overwrite the maintained queue, including this PR's row. No automatic regeneration, actual live loss, or new incompatibility introduced by this PR was demonstrated. The mathematical pass verdict is unaffected. An actionable PR comment requiring this proof PR to fix the queue is not supported by this check.

## What was executed and why it was safe

I read `reproduce_queue_finding.py` before executing it. Its `at_head()` uses only `git show` on an immutable object; the live SQLite connection is explicitly read-only (`mode=ro`, script lines 43–47). It loads the exact PR-head queue module into a temporary directory under this review's `tmp/`, asserts that the module's `ROOT` is that directory, and supplies sandbox policy, state, assessment, manifest, catalog, and queue files there (lines 54–77). At import, queue.py defines functions and constants; its `main()` is guarded by `if __name__=='__main__'` (head queue.py line 317). The reproduction invokes `rank`, not the network-bearing `sync` function.

All generated ranking/catalog/queue/shortlist/summary files therefore remain within the sandbox. The persistent reproduction result is this review's `queue_reproduction.json`; no candidate file, live queue, live state, branch, commit, or remote was modified by my check.

The script executed successfully with exit code zero and produced:

| Field | Observed value |
|---|---|
| Before maintained queue row | Head `QUEUE.md` line 38: `claimed_solved`, `1/5`, finding and draft-PR link |
| Head global state entry | None (`state.json` is `{}`) |
| After generated local status | `queued` |
| After generated turns used | `0` |
| After generated eligibility | `true` |
| `claimed_solved` accepted by the older CLI | No |

The displayed regenerated rank becomes 1 rather than 27 because the reproduction deliberately contains one record. That difference is a simulation artifact and is irrelevant to the observed status/turn replacement.

## Identity and source-hash checks

The target is the numeric ID `30005473` / code `OWR-12697711-006`, consistently in the immutable queue row, committed catalog, SQLite cache, and local artifact metadata. Independently computed cache hashes are:

- Statement SHA-256: `bc2ec178d47d8fd7483f15458f9e475f05a4349f531473ab88b65ae04d91cb8d`.
- Full record/report review SHA-256: `8a6c56f920e9fb0301b694074b6d4fad1bc5d99832848b5ade4e07b5aba4fdc8`, using exactly `json.dumps([problem, report], sort_keys=True)`.
- Prior report: `{}`.

Both hashes match head `catalog.json`, `attempts/30005473/source_record.json`, and the review hash in `attempts/30005473/readiness.json` line 3. The reproduction also independently asserts the review-hash match at script line 62. The simulated result is not caused by misidentifying the record, a stale assessment, or a different source statement.

## Actual older-generator mechanism

The following references are to `unsolved_math_prioritization/queue.py` at the reviewed head; the entire file is byte-identical at the reviewed base.

1. **Line 7:** `STATES` includes `candidate_result`, `independent_verification`, and `verified_solved`, but excludes `claimed_solved` and `preprint_published`.
2. **Lines 123–134:** `rank()` reads policy, effective assessments, global `state.json`, previous catalog, and SQLite source records. It selects local state with `state.get(key,{})`.
3. **Lines 158–163:** The current candidate assessment with no holds supplies default `queued`; absent global state supplies zero turns; queued with fewer than five turns remains eligible.
4. **Lines 178–180:** Prior catalog fields are retained only for records absent from the current source. This target is present, so previous catalog data cannot override recomputation. In any event, the head catalog already says `queued`, zero turns, eligible true.
5. **Lines 192–204:** The generator constructs its own limited table from computed rows and calls `write_text` on `QUEUE.md`. It never reads the existing queue to preserve edited rows or the Chat/Findings/DOI columns.
6. **Lines 198–201:** Generated attempt history depends on membership in global `state`; it does not discover local attempt artifacts.

I also parsed the full queue.py with Python's AST: it contains no string reference to `turns.jsonl` or an `attempts` folder. The local ledger's omission from the reproduction cannot explain away the old generator's result; that generator does not consult the ledger even when it exists. The one-record experiment removes cross-record duplicate effects, but the actual committed full catalog also has `holds=[]` and `eligible=true` for this exact source hash. The source logic and immutable full-catalog evidence support the narrow status/turn conclusion without claiming a full-corpus rank reproduction.

## Falsification evidence: the maintained queue is already a manual ledger

These observations contradict the stronger claim that this PR newly mishandles a generated queue or fails to preserve *any durable* turn accounting.

### 1. Explicit documentation at both base and head

`unsolved_math_prioritization/RESEARCH_LOG.md` **line 29**, at **both reviewed revisions**, records a 2026-09-26 direct publication-row edit and explains:

> Applied the requested direct row edit because the older generator lacks this publication status and the live Chat/Findings/DOI columns; running it would discard maintained queue information.

This passage predates both PR commits and explicitly recognizes the inherited incompatibility. It is not a post-review excuse.

The base queue already contains **14** manually maintained `claimed_solved`, `preprint_published`, or `in_progress` rows, while base `state.json` is `{}` and base `history.jsonl` is empty. Examples include the published rows at base `QUEUE.md` lines 11–13. Consequently the state-versus-manual-queue mismatch is repository-wide before this PR.

Head and base copies of `queue.py`, `state.json`, `history.jsonl`, `catalog.json`, `README.md`, `AGENTS.md`, and `apply_impact_scores.py` are byte-identical. The new head commit `a29887ed0` changes only the maintained target row. The preceding PR commit `5699f942a` adds the dedicated mathematical artifact folder. Comparing the full PR against base confirms no changes to the generator or global state/history.

### 2. Newer code explicitly recognizes manual statuses

At both revisions, `unsolved_math_prioritization/apply_impact_scores.py` **lines 6–8** defines `QUEUE` as the input and includes `claimed_solved` and `preprint_published` in `OPEN_STATUSES`. Its **lines 20–21, 42–53, and 65–73** read the existing queue and preserve row fields while inserting impact scores. Thus the repository has newer queue processing that recognizes the maintained statuses which the older CLI does not recognize. It is inaccurate to treat the latter CLI's `STATES` list as the sole authoritative definition of every live queue status.

`unsolved_math_prioritization/README.md` **lines 22–34**, also unchanged by the PR, describes the newer importance column and instructs reapplication of those scores after regeneration. `VALIDATION.md` **line 16** already describes 12 rows marked published or claimed awaiting human verification. These reinforce the existence of a maintained queue layer beyond the older generated table.

### 3. Durable local accounting exists

Head `unsolved_math_prioritization/attempts/30005473/turns.jsonl` **line 1** is a committed, timestamped record of substantive turn 1, outcome `candidate`, its mechanism, artifact, scope, and remaining gap. The folder's `README.md` **lines 3 and 9** reports 1/5 and links that ledger; its `RESEARCH_LOG.md` **lines 17–23** records the substantive candidate attempt and count. These are durable, checkable accounting artifacts even though the older global workflow does not import them.

Therefore “no durable state/history was changed” is too broad. The accurate statement is “no **global CLI state/history** entry was added; a committed **local turn ledger and research log** were added.” The reproduction demonstrates failure to integrate those records into that CLI, not absence of records.

Head `attempts/30005473/readiness.json` **line 29** says local-only readiness/turn accounting and avoidance of `sync/rank/status/turn` were per task instructions. This is evidence of the author's recorded routing choice. It is **not independent trusted evidence of the original human authorization**, which is unavailable in this audit, and I do not infer either compliance or disobedience from that artifact alone.

### 4. “Becomes eligible again” also needs qualification

The head's global `catalog.json` already lists this target as `eligible=true`, `local_status=queued`, zero turns before reproduction. The maintained `QUEUE.md` row carries the new result and turn count. Thus the reproduction changes the **regenerated displayed queue** and reproduces the **existing CLI catalog view**; it does not show a transition from an ineligible durable CLI state to an eligible one. Its JSON conclusion should be read with this limitation.

## Conflicting standing workflow documentation

There is a real documentation mismatch that should be preserved in the research record, but it is inherited:

- `unsolved_math_prioritization/AGENTS.md` **line 8** says to record each substantive response with `queue.py turn`; **line 13** says to regenerate after status or assessment changes.
- `README.md` **lines 100–101** advertises offline ranking; **lines 164–178** prescribe turn accounting through the CLI; **lines 200–201** describe writes to global state/history.
- The later base `RESEARCH_LOG.md` **line 29** documents avoiding the older generator to preserve the maintained queue's published statuses and additional fields.

A new proof PR need not silently undertake a repository-wide queue migration to resolve this accumulated mismatch. Nor can this audit adjudicate whether the original task carried a more specific human instruction overriding the standing workflow. The supported narrow risk is that following the older regeneration instructions literally can overwrite the manually maintained ledger.

## Suggested wording for the root review

“An isolated source-hash-verified check confirmed that the legacy queue generator would replace the manually recorded result and turn count with `queued 0/5`. This is an already documented repository-wide limitation of the maintained queue, not a new mathematical or PR-specific defect. The attempt has a committed local turn ledger. The provisional P2 finding was withdrawn; no corrective PR comment is warranted on this evidence.”

**Strongest verified result:** exact older-generator replacement behavior and documented prior incompatibility. **Remaining uncertainty:** the original task's trusted authorization and any intended future migration of maintained queue data into the older CLI. No actual live regeneration was performed or observed.
