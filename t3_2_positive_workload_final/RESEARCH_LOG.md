# Research log

## 2026-08-09T20:58:36-07:00 - project initialization

- Created a dedicated final-repair project.
- Preserved the supplied workload-reactivation release unchanged under
  `inherited/workload_reactivation_candidate/`.
- Accepted the independent audit's two load-bearing objections for analysis:
  tightness is not finite support, and physical-time recurrence cannot be
  inferred by counting fast neutral embedded jumps.
- Withdrew the inherited global T3-2 certification pending a new proof.
- Opened three independent read-only tracks: theorem construction,
  adversarial counterexample/proof audit, and release reproducibility audit.
- Initial structural observation: finite lexicographic comparisons of
  complexes can be scalarized with sufficiently separated rational weights,
  but that fact alone gives no shell-uniform service margin or physical-time
  descent. Those are separate proof obligations.

## 2026-08-09T21:23:49-07:00 - claim-neutral verification regressions

- Added exact generic witnesses showing that pointwise shell-dependent negative
  drift can coexist with null recurrence and that a finite-mean primary
  lexicographic descent can expose an infinite-mean lower-component drain.
- Added positive-recurrent CRN regressions for a tight Poisson environment with
  infinite support and for arbitrarily large fast-neutral reaction count at
  fixed mean physical trace duration.
- Added a standard-library-only isolated verifier that hashes its scope before
  and after testing and never reads or modifies the inherited candidate.
- These regressions constrain future proof interfaces; they make no T3-2
  certification claim.

## 2026-08-09T21:24:00-07:00 - proposed bridge stress-tested

- Proved the finite lexicographic scalarization lemma with its missing
  positivity hypothesis and recorded the valid scalar shell-Foster theorem.
- Found that pointwise shell-dependent service margins are insufficient: an
  exact birth-death chain has negative drift at every level but is null
  recurrent with infinite mean clearing time.
- Found that naive lexicographic physical-time descent is insufficient: an
  exact CTMC lowers its primary coordinate in finite mean but creates a
  heavy-tailed lower coordinate with infinite expected clearing cost.
- Recorded a tight infinite-support CRN environment, a fast-neutral physical
  trace regression, and the mismatch between signed service (B-C) and any
  positive scalar workload.
- Refined the central open gate to a global drift-cost episode inequality for
  one proper residual-factorial potential. The finite atlas does not by
  itself provide that stochastic inequality.
