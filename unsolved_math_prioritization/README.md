# UnsolvedMath research queue

A reproducible, provisional expected-value ranking of all 15,458 records in
[ulamai/UnsolvedMath](https://huggingface.co/datasets/ulamai/UnsolvedMath), with
persistent local assessments and research statuses.

Start with **[QUEUE.md](QUEUE.md)** (top 100), **[SHORTLIST.md](SHORTLIST.md)**
(individual reasoning), or **[ranking.csv](ranking.csv)** (every record, sortable).
The initial pass includes 23 individual desk assessments. None is certified as
AI-solvable, ready for research, or newly solved. Most rows are cheap automated
triage; a precise ordering among those rows is not justified by the evidence.

## Expected value and its limits

For a **fixed budget of 8 agent-hours of exploration plus 2 agent-hours of
independent verification**, rank by:

`EV = impact × P(valid, still open, novel target) × P(verified full resolution | valid target, budget)`

This is expected value per attempt, not impact divided by difficulty. With equal
budgets it also orders expected value per hour. Changing budgets requires new
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
can both be overridden after reading the actual mathematics. `policy.json` makes
the automatic assumptions explicit. Its weak initial priors give L4/L5 entries
more impact but sharply less feasibility; L1/L2 receive **no easy-problem bonus**.
OWR L3 is a collection default. Exact/corrected wording gets a somewhat higher
combined validity/open-status prior, but proves neither novelty nor open status.
Popularity and views do not influence ranking.

Automatic signals use computable objects, constructions, broad programs,
asymptotic targets, and general polynomial-time algorithm requests. These are
retrieval aids, not mathematical arguments. Individual assessments describe a
mechanism and exact remaining gap. All initial estimates have low confidence.
`ev_low` / `ev_high` vary success probability by ×0.2 / ×3 and validity by −/+0.2
(with clipping); these are sensitivity scenarios, **not statistical intervals**.
Overlapping values should be treated as priority bands. Equal EV values are ties;
the numeric-ID tiebreak has no substantive meaning.

After the first 10–20 budgeted attempts, reassess the priors using time spent,
verification outcomes, failure modes, and contribution size. Include occasional
lower-ranked and different-domain probes to expose selection bias. This initial
policy favors symbolically/computationally checkable problems; it is not a claim
that other mathematical fields are less valuable.

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

`unreviewed → ready → in_progress → candidate_result → independent_verification → verified_solved`

Also available: `partial`, `blocked`, `deferred`, `already_solved`, `invalid`,
`duplicate`. Desk triage leaves the local status `unreviewed`; the separate
`assessment` column says whether it has an individual assessment. Upstream
solution claims are review holds, not locally verified achievements.

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
`remaining_gap`, `first_experiment`, and `sources`, then run:

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
