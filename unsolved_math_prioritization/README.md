# UnsolvedMath research queue

A reproducible, provisional expected-value ranking of all 15,458 records in
[ulamai/UnsolvedMath](https://huggingface.co/datasets/ulamai/UnsolvedMath), with
persistent local assessments and research statuses.

**The exhaustive five-turn review is in progress.** See [review progress](review_v2/PROGRESS.md).
The active exports still use the initial policy until complete coverage passes validation.
The following describes the replacement workflow being prepared.

Start with **[QUEUE.md](QUEUE.md)** (all eligible candidates), **[SHORTLIST.md](SHORTLIST.md)**
(the leading 100 explained), or **[ranking.csv](ranking.csv)** (every record and short review).
These are promising candidates, not certified AI-solvable problems. A desk review
identifies a proof route and obstacle; it does not prove that the route will succeed.

## Expected value and its limits

For a **fixed budget of five substantive proof-attempt turns with ChatGPT6 Astra
at ultra reasoning**, rank by:

`EV = impact × P(valid, still open, novel target) × P(verified full resolution | valid target, budget)`

This is expected value per five-turn attempt. Turn duration varies, so it is not
a measured expected value per hour. Changing budgets requires new
probability estimates. Full resolution means a proof or counterexample settling
the exact target, including every part of a bundled question. A promising
special case must become a separately identified subproblem; do not quietly
substitute it for the original target.

Impact is a subjective **cardinal utility on a 1–10 scale**, not prize money:
1 = narrow isolated fact; 3 = substantive specialized result; 5 = useful result
across a research area; 7 = major bridge or barrier; 10 = foundational breakthrough.
This bounded scale encodes our preference to pursue achievable research rather
than allow huge speculative utility for a famous conjecture to dominate.

The probabilities are **uncalibrated planning assumptions**, not measurements,
confidence levels, or a claim about any particular AI model. Impact and probability
can both be overridden after reading the actual mathematics. Every record receives
an individual semantic review of its statement, difficulty, and available context.
Only selected proof or modest-computation candidates enter the working queue.
Large exhaustive searches, known resolutions, unverified solution claims, unclear
statements, and routes that merely restate the hard part are held out.

Age supplies a small impact bonus, capped at 15% and at total impact 10:
`1 + 0.15 × min(1, log(1 + age) / log(101))`.
Only an explicit `proposed_year` is used; missing years remain unknown. Age is a
weak proxy for impact and also evidence of difficulty, not a reason to expect an
easy proof. `policy.json` fixes the reference year for reproducibility. Upstream
difficulty informs the individual judgment; neither a low difficulty label nor
membership in Kourovka or any other collection earns an automatic bonus.

Legacy automatic scores remain fallback metadata for new or changed records,
which cannot enter the five-turn queue without a fresh individual assessment.
All estimates have low confidence. `ev_low` / `ev_high` vary success probability by ×0.2 / ×3 and validity by −/+0.2
(with clipping); these are sensitivity scenarios, **not statistical intervals**.
Overlapping values should be treated as priority bands. Equal EV values are ties;
the numeric-ID tiebreak has no substantive meaning.

After the first 10–20 budgeted attempts, reassess the priors using time spent,
verification outcomes, failure modes, and contribution size. Include occasional
lower-ranked and different-domain probes to expose selection bias. This policy favors short, checkable proofs and constructions, with modest exact
checks when useful. It does not measure the value of entire mathematical fields.

## Update and inspect

Requires Python 3.10+ with its standard library; no API keys, paid model calls,
or Python packages. Run these commands from the repository root:

```sh
# Fetch latest immutable revision, rebuild local index, update the ranking.
python3 unsolved_math_prioritization/queue.py sync

# Restore exactly the original snapshot on a fresh clone.
python3 unsolved_math_prioritization/queue.py sync --revision 37e53eabe540fb458758e198be61634bd02ee008

# Recompute without downloading; inspect a complete problem and prior AI report.
python3 unsolved_math_prioritization/queue.py rank
python3 unsolved_math_prioritization/queue.py show 30004033

# Run regression tests, using temporary synthetic data (no network).
python3 unsolved_math_prioritization/test_queue.py
```

Use the revision currently in `manifest.json` when restoring a later snapshot.
`sync --revision <recorded SHA> --use-cache` verifies cached file sizes/hashes
against the existing manifest before rebuilding. It cannot establish provenance
for arbitrary unrecorded files. Normal sync downloads both source files, about
149 MB in this snapshot; it never downloads the redundant combined dataset or
PDF. Import uses standard JSON parsing (memory proportional to these files),
then SQLite for selective retrieval; ranking reads one problem/report at a time.
There are no 15,458 individual network requests or model calls. Repeated ranking
is offline. Full sync is manual, not a background automation.

Raw source JSON and SQLite stay in ignored `cache/`. Git stores the compact
catalog, ranking, policy, provenance checksums, assessments, statuses, and logs.
The immutable upstream SHA and SHA-256 checksums identify what was analyzed.
The original short reviews, including every exclusion and deferral, are kept in
[`review_v2/reviews_0.json`](review_v2/reviews_0.json) through `reviews_5.json`.
[`adversarial_overrides.json`](review_v2/adversarial_overrides.json) preserves later
corrections without erasing those first judgments. The review assignments and
merge manifest bind this ledger to its source revision. Keep the completed ledger
as a historical snapshot when reviewing another dataset version.
`assessments.json` holds the current effective reviews; subsequent assessment
changes also append to `assessment_history.jsonl`. A refresh does not delete these
files or local attempt statuses. Changed records are held out until re-reviewed.
`last_update.json` lists added, changed, and removed numeric IDs;
`update_history.jsonl` preserves sync history. Removed rows stay visible, with
notes and statuses intact. Their original full text can be restored from the old
pinned revision; local source cache reflects the latest import.

**Identity is the numeric upstream `id`, not `problem_number`.** This snapshot
contains repeated problem codes belonging to unrelated problems. Both are
retained in the catalog. A future reused numeric ID requires manual identity
review; source changes will invalidate assessments rather than transfer readiness.
Ambiguous research-report joins are held for review.

Any change to a problem or its prior report invalidates its local assessment and
readiness via `review_hash`. `statement_hash` separately identifies its wording.
Changes to incidental upstream metadata may also conservatively trigger review.
Local statuses are preserved, never replaced by upstream classifications.
Identical normalized statements are **possible duplicates**, not merged records.
Related formulations and cross-collection duplicates still need manual checking.

Use a single writer for queue commands. Review generated diffs before committing.
No scheduler, GitHub release, or Zenodo DOI is created by the tool.

## Research lifecycle

`queued → ready → in_progress → candidate_result → independent_verification → verified_solved`

Also available: `partial`, `blocked`, `deferred`, `already_solved`, `invalid`,
`duplicate`, `unreviewed`, and `exhausted`. Eligible desk-reviewed candidates start
as `queued`; this does not mean source/readiness verification is complete.
The separate `assessment` column distinguishes individual review from automatic
fallback scoring. Upstream solution claims are review holds, not local achievements.
A partial resolution of a bundled question requires a separately defined remaining target.

Count an assistant response that advances the proof attempt as one turn; individual
tool calls and desk triage do not each count as turns. Record each substantive
attempt turn. After the fifth unfinished turn, the tool
marks the problem `exhausted`; move to the next problem. A candidate result found
by turn five may proceed to independent verification. Verification is not an
extension for continuing an unfinished search, and `partial` does not reset the counter.

```sh
python3 unsolved_math_prioritization/queue.py turn 30004033 --note 'Attempt 1: mechanism and exact remaining gap recorded in research log'
python3 unsolved_math_prioritization/queue.py turn 30004033 --outcome candidate --note 'Complete candidate proof saved for independent verification'
```

These examples do not start an attempt. `Status` and `Turns` appear in QUEUE.md;
finished and active attempts remain in its history table.

Before `ready`, record an evidence JSON with these nonempty fields:

- `review_hash`: current hash from `show`, binding evidence to the source read.
- `exact_claim`: full quantifiers, hypotheses, domain, and boundary cases.
- `primary_sources`: source links and exact locations checked.
- `literature_checked_at`: dated primary-source literature review.
- `success_test`: what artifact would settle the **entire** exact claim.
- `budget`: exploration, verification, and compute budget.
- `prior_attempt_gap`: independent audit of earlier reports and failed routes.
- `duplicate_check`: search related dataset records and this repository's work.

```sh
python3 unsolved_math_prioritization/queue.py status 30004033 ready --note 'Source and scope verified' --evidence unsolved_math_prioritization/attempts/30004033/readiness.json
python3 unsolved_math_prioritization/queue.py status 30004033 in_progress --note 'Begin budgeted attempt' --evidence unsolved_math_prioritization/attempts/30004033/readiness.json
python3 unsolved_math_prioritization/queue.py status 30004033 blocked --note 'Route reduces to an unsupported conjecture; see research log'
```

These are examples, not actions already performed. Each status change updates
`state.json` and appends to `history.jsonl`. Keep each actual attempt under its own
`attempts/<numeric-id>/` folder, with timestamped research log, completion estimates,
exact claims, proof/computation artifacts, and materially independent approaches
and adversarial review as required by the repository's AGENTS.md. A blocked route
reopens only with a new mechanism or evidence. Never contact external researchers.

To mark `verified_solved`, the preceding status must be `independent_verification`
and the source hash must still match. Provide `proof_artifact`, `independent_review`,
`novelty_check`, `exact_claim`, and the current `review_hash` in evidence JSON. The tool enforces record
requirements; it **cannot judge whether a proof or a review is correct**.

## Change an assessment or resolve a hold

Write a JSON containing the current `review_hash` from `show`, `impact`, `p_solve`, `p_valid_open`, `rationale`,
`remaining_gap`, `first_experiment`, and `sources`. Under the five-turn policy also
include `review_policy: "2.0-five-turn-proof"`, `route` (`proof`, `hybrid`,
`large_search`, or `unclear`), `decision` (`candidate`, `defer`, `exclude`, or
`repair`), and a concise individual `note`. Then run:

```sh
python3 unsolved_math_prioritization/queue.py assess 30004033 --file unsolved_math_prioritization/attempts/30004033/assessment.json
```

The command rejects missing or stale source hashes and binds the review to current source hashes and appends assessment
history. `holds` can add concerns. To clear a specific hold, include a
`clear_holds` object mapping the **exact hold string** to a checkable evidence
reference and rationale. For duplicate suspicion, preserve both records and
explain their distinct mathematical scopes, or mark the redundant row `duplicate`.
For a changed-source readiness hold, supply fresh readiness evidence. For stale
assessments, re-read the changed source and record a new assessment.

Do not clear a solved/statement-repair hold merely to raise a rank. A resolved
problem belongs in `already_solved`; a newly scoped residual is a separate target.

## Attribution

Dataset: *UnsolvedMath: A Curated Collection of Open Mathematics Problems*,
UnsolvedMath Contributors (2026), [Hugging Face](https://huggingface.co/datasets/ulamai/UnsolvedMath).
Curation and original metadata: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Underlying source documents retain their own terms. Our derivative compact catalog
retains problem titles and links, adds scores/holds/local review metadata, and
omits the large statement/report corpus. Upstream AI reports are untrusted research
aids, not proof certificates. Report titles sometimes describe a prior partial
result rather than the original problem; always inspect the actual statement.

Project author metadata: Alec Kriebel, [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).
