# Independent acceptance of the bounded-lead reductions

Auditor: survival lane, shared PASS4. This is an independent mathematical review, not a new solution of the full game.

Accepted artifacts:

- `pass4_audit/BOUNDED_LEAD_FINITE_ARENA.md`, SHA256 `0a46caf2242d3ea0e4e2f93247c537e56e4737a138f8bbac544287ce62d5176b`.
- `pass4_audit/ALL_FINITE_LEADS_REDUCTION.md`, SHA256 `1680b4843f30390904a6dbd50d0cf5af560f7890530784967d6386fa9b4db7ca`.

## Checks

1. The reachable-cone deletion is permanent: an outside-cone point cannot become reachable after a legal move. Keeping a null action preserves the effect of arbitrary irrelevant announcements.
2. The tail-age inequalities count distinct announcement witnesses, so repeated timestamps cause no problem. The bound at lag j is exactly H-j+1 for a post-announcement state.
3. The descending-lag witness assignment realizes every budget-feasible state along a legal stationary Angel history, without claiming strategic forceability. No hidden age information is necessary for future state values.
4. The transition is Angel move first, then universally quantified Devil announcement. The finite safety fixed point therefore has the claimed online interpretation. Stabilization supplies a positional normalized-state strategy in the winning region and finite forcing ranks outside it.
5. In the all-H reduction, the virtual Devil may retain all omitted real-history values internally. Consequently projection of distant announcements does not silently weaken adaptive adversarial information.
6. The extraction uses nested subsets of nine Angel moves, not a finite-branching assumption for the Devil. It requires neither compatible bounded-H policies nor uniform tracking bounds.

No correction is required. These results prove exact reductions and decidability for each fixed H; they do not certify the empty state for arbitrary H.
