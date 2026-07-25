# Campaign State

## Checkpoint 001 — 2026-07-25 14:28 PDT

- Campaign day: 1 of 27; 26 campaign days remain.
- Repository branch: `main`.
- Published campaign commit:
  `e05d451eb4edb6d67c26aab7286950d50c39bf59`.
- Completion estimate for the campaign work plan: **15%**.
- Completion estimate toward an actual universal resolution: **3%**.
  The conjecture remains unresolved; neither estimate is a mathematical
  probability.
- Literature audit date: 2026-07-25, including a direct current-search refresh
  and the full April 2026 Kimura--Matsumoto--Sato article.

### Verified facts and artifacts

- Required reductions are proved in `math/reductions.md` and accepted in
  `reviews/reductions_hostile_review.md`.
- Exact evaluator A and structurally independent evaluator B are implemented
  and hostile-reviewed. The deliberate model-error probes distinguish
  one-guard movement, unoccupied attacks, domination checks, and \(G\) from
  \(\overline G\).
- The exact 56-record MMV Table 9 catalog is reproduced. Both evaluators agree
  on every parameter and greatest eternal family at every \(k\); all 56
  values \(\theta=4\) have independently replayed non-3-colorability traces
  and direct 4-colorings.
- The 55 graphs with
  \(\alpha=\gamma^\infty=3<\theta=4\) all fail explicitly because
  \(\gamma<\alpha\): two have a universal vertex and 53 have a recorded
  dominating pair.
- New proved tools: the maximum-independent-state/private-region obstruction
  and the complement-side \(k=3\) dictionary, each with an independent hostile
  review and exhaustive small-graph audit.
- Current fully completed exhaustive frontier: all 12,113 connected unlabeled
  graphs through order 8. No \(\gamma^\infty<\theta\) graph occurs there.

### Literature and restriction status

- No universal proof or certified counterexample was located through
  2026-07-25.
- The original assertion is Theorem 14 of
  Klostermeyer--MacGillivray (2009); its proof was explicitly corrected in
  Klostermeyer--Mynhardt (2015), which posed the open question.
- Subcubic and triangle-free restrictions are primary-source verified.
  Taletskii's all-planar theorem statement is verified but its long proof
  remains queued for hostile audit.
- The \(C_4\)-free result still traces only to an unavailable 2018 manuscript.
  The purported 4-cycle restriction is provisional and is not a hard filter.
- The July 2026 Cayley work concerns
  \(\gamma_{\rm all}^\infty\), not the one-guard parameter, and is excluded.

### Approach registry

| Route | Status | Exact gate/obstruction |
|---|---|---|
| Literature/status audit | active-weekly | Phase 0 checkpoint complete; 2020 chapter, unavailable \(C_4\)-free manuscript, and general well-covered generators remain source gaps |
| Exact evaluators/certificates | active-validation | A/B and coloring-trace hostile audits accepted; connected order-9 partition is running |
| Required reductions | complete | All requested core reductions accepted; class-citation qualifications remain separate |
| MMV near-miss extensions | active-prelaunch | Exact 110,537-case scope accepted; engine is under hostile crash/candidate-state repair; full run not launched |
| Direct synthesis `(12,3)` | pending | Opens only after order-9 validation and near-miss kill test |
| Structural \(k=3\) lane | active | Two proved mechanisms obtained; next structural lemma is under independent development |
| General well-covered generation | blocked | No audited complete constructive generator/catalog for orders 12--16 yet |

### Running jobs and resume state

- Order-9 shard `1/8` is complete (35,236 graphs).
- Shards `0/8` and `6/8` are running with atomic checkpoints in
  `results/checkpoints/`; each uses one CPU core and roughly 27 MiB resident
  memory. No more than two workers run concurrently.
- Remaining order-9 shards are queued by descending estimated cost. Resume
  uses the same `search.unlabeled_regression` command and existing checkpoint.
- No extension, synthesis, SAT, or other novel exhaustive job is running.

### Resource usage

- Host remains MacBookPro18,1, Apple M1 Pro, 10 cores, 16 GiB RAM.
- Current campaign workers use about 54 MiB aggregate resident memory and two
  CPU cores. Free disk is approximately 10 GiB.
- The one-vertex-extension engine has a 1 GiB memory gate and 45-minute
  resumable wall gate; it remains closed pending hostile acceptance.

### Next three highest-value actions

1. Finish and aggregate all eight order-9 validation shards; compare the
   261,080 total and parameter counts to the published table.
2. Close every hostile extension-engine finding, run the independent review,
   and only then launch the 110,537-case one-vertex-extension kill test.
3. Build the standalone post-run coverage/isomorphism checker while continuing
   the structural \(k=3\) proof lane.

### Claim boundary

No checkpoint-001 result resolves the conjecture. The order-at-most-11
statement remains the published MMV frontier rather than a newly certified
campaign enumeration, and the extension universe has not yet been searched.

## Checkpoint 000 — 2026-07-25 13:02 PDT

- Campaign day: 1 of 27.
- Repository branch: `main`.
- Repository commit at campaign start:
  `87e9672b4fabecc9fd59bd42c0da8d27d97d1c6f`.
- Completion estimate toward the full conjecture-resolution goal: **1%**.
  This is a deliberately low prior and may move non-monotonically.
- Literature audit date: initiated 2026-07-25; no campaign claims accepted yet.
- Verified facts: none newly produced by this campaign.
- Current exhaustive frontier: none.
- Certificate status: no campaign certificates yet.

### Machine and resource envelope

- Model: MacBookPro18,1 (Apple M1 Pro).
- CPU: 10 physical/logical cores.
- Physical memory: 17,179,869,184 bytes (16 GiB).
- Free filesystem space at start: approximately 11 GiB.
- Policy: at most two memory-heavy jobs; aggregate target below 12 GiB; keep
  interactive load responsive; no blind order-12 graph enumeration.

### Repository isolation

The `main` worktree contained unrelated dirty research before this campaign
started. All campaign artifacts are isolated in
`gamma_theta_eternal_domination/`. Checkpoints stage only this directory.
Existing unrelated modifications are not to be edited, staged, or committed.

### Approach registry

| Route | Status | Current gate |
|---|---|---|
| Literature/status audit | active | Verify original attribution, 2022 catalog, later citations, and current resolution status |
| Exact evaluator A | active | Implement directly from the greatest-fixed-point definition |
| Exact evaluator B | active | Implement independent colored configuration digraph |
| Required reductions | active | Produce self-contained proofs, then hostile review |
| Near-miss extensions | pending | Requires evaluator validation and exact appendix data |
| Direct synthesis `(12,3)` | pending | Requires 72-hour validation gate |
| Structural `k=3` proof lane | pending | Begin after reductions and literature restrictions are fixed |

### Running jobs

None at checkpoint creation.

### Resume

1. Read `STATE.md`, `CLAIMS.md`, and the latest entries of
   `RESEARCH_LOG.md`.
2. Inspect `git status --short -- gamma_theta_eternal_domination`.
3. Run the test command recorded in the most recent checkpoint.

### Next three highest-value actions

1. Complete the primary-source literature audit and obtain the 2022 appendix
   Graph6 data.
2. Finish two independent exact evaluator stacks and unit tests.
3. Prove and adversarially audit the parameter chain, equality collapse,
   component reduction, imperfection obstruction, and minimum-parameter facts.

### Known constraints and risks

- Only about 11 GiB of disk was free at launch.
- `main` is a shared dirty worktree, so commits must be path-scoped.
- The repository policy forbids preparing or initiating outside outreach,
  despite the campaign brief's later publication wish list.
