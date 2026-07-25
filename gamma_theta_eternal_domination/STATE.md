# Campaign State

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
