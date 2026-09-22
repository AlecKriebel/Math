# Five-turn proof-first reassessment

This effort replaces the initial keyword screen with a short individual semantic
review of every dataset record. See [PROGRESS.md](PROGRESS.md) for checkpointed
coverage. Until all six batches pass coverage validation, the original working
queue remains in place; partial reviews are not mislabeled as exhaustive.

## Target and ordering

One attempt means at most **five substantive proof-development turns with
ChatGPT6 Astra at ultra reasoning**, with modest exact checks. Tool calls do not
count as separate turns. Finding a candidate proof within five turns may be
followed by independent verification; verification cannot silently become a
sixth proof-development attempt. If no candidate proof resolves the full problem
after five turns, mark it `exhausted` and move on.

`EV = impact × age_modifier × P(valid/open/novel scope) × P(full verified solution in five turns)`

Effective impact is capped at 10. Base impact is an individual estimate of the
mathematical contribution, not a difficulty score. Upstream difficulty is used
as evidence during review and displayed in the queue; it is unreliable in parts
of this corpus (some notorious open conjectures are L1, and many L3s are defaults).

Age is a weak impact proxy, not proof of importance. The modifier increases
smoothly from 1.00 to 1.15 over 100 years and then stops. It uses the supplied
`proposed_year` only; missing dates receive no bonus. Import dates are never
substituted. The date is not an independent certification that a problem stayed
open continuously. Historical resistance is separately considered in feasibility.
No source collection, including Kourovka, receives a bonus.

Only individually selected `proof` or `hybrid` routes can enter the working queue.
A hybrid route permits small exact sanity checks; it does not permit a large
exhaustive search. Known resolutions, resolution claims requiring audit,
malformed targets, missing definitions, huge searches, and targets with no
plausible five-turn mechanism are retained in the full review ledger with their
exclusion/deferral reason.

These probabilities are subjective and uncalibrated. The purpose is to make the
best informed allocation of a limited attempt budget, not to certify that AI can
solve an open problem or that no lower-ranked problem would be better. Outcome
tracking will let us revise those judgments rather than preserve a false precision.

## Individual notes and validation

`reviews_0.json` through `reviews_5.json` contain individually authored short
notes, impact, feasibility, validity, and route/disposition. `assignments.json`
fixes complete, disjoint source coverage at an immutable upstream revision.
`batches.py` packages complete statements and brief prior-report excerpts; it
never authors a mathematical review. `merge.py` rejects wrong or duplicated IDs,
invalid fields, and incomplete coverage before activating the replacement policy.
`adversarial_overrides.json` records additional primary-source checks of apparent
leaders, preserving the first review rather than silently rewriting it.

Every note names a mechanism and an obstacle or a specific exclusion reason.
Reviewers do not spend five turns solving each problem during this pass. Most
reviews rely on the supplied statement and available prior research metadata;
they are not exhaustive literature searches. Leaders receive extra scrutiny.

## Working status and turn count

After activation, `QUEUE.md` lists every admitted candidate, with upstream
problem code, difficulty, proposal year, local **Status**, and **Turns** used.
Completed, blocked, partial, and exhausted attempts remain in its attempt-history
table. The full CSV also retains every excluded/deferred row and review note.

Start using the existing `status ... in_progress --evidence ...` command after
checking exact formulation and current literature. After each actual substantive
proof turn, record it once:

```sh
python3 unsolved_math_prioritization/queue.py turn NUMERIC_ID --note 'Turn summary and exact unresolved gap'
python3 unsolved_math_prioritization/queue.py turn NUMERIC_ID --outcome candidate --note 'Candidate proof artifact and scope'
```

These are examples, not already executed research turns. The fifth unsuccessful
turn becomes `exhausted` automatically. Subsequent status changes do not reset
its counter. A candidate is never a verified solution without independent proof
review and novelty checking. No mathematical problem is launched by the review
or ranking tools themselves.
