# Research log: weakly reversible continuum without a common factor

## 2026-08-01 15:23 PDT — Program opened

- Objective: construct and exactly verify a finite weakly reversible mass-action
  system having a positive-dimensional equilibrium continuum inside one
  positive stoichiometric class, while the coordinate vector-field polynomials
  have gcd (1).
- Discovery policy: first-principles algebra and local symbolic computation
  only. No literature, web, database, or earlier-project search before a
  complete result.
- Acceptance gate: a standalone exact verifier must reconstruct the vector
  field from the reaction list and certify positivity, graph properties,
  stoichiometry, the parametrized continuum, and the gcd assertion.
- Parallel avenues begun: direct three-species construction; structured exact
  search over reversible realizations; structural/minimality analysis and a
  higher-species fallback.
- Repository note: the supplied worktree was already on
  `codex/h668-theory`, with unrelated modified/untracked work, while `main` is
  checked out in another heavily dirty worktree. To avoid altering or losing
  independent work, this program is being isolated by path and commits will
  stage only this directory. This pre-existing branch-state conflict should be
  resolved by the human before any eventual integration to `main`.

