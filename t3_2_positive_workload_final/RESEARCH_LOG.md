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

## 2026-08-09T21:52:00-07:00 - smallest cross-linkage gate isolated

- Proved a conditional sequence-to-uniform physical-time Foster closure for
  the global residual-factorial potential.
- Isolated an exact available/shielded support where the current target can
  remain in a quadratic neutral linkage while the stabilizing linkage is rare
  in embedded count. The atlas labels the latter available but supplies no
  unconditioned wait-activation-relaxation resolvent estimate.
- Verified that the exceptional service quantity (B-C) can descend while
  the residual-factorial reward is exactly zero, so a proper linear-corrected
  potential and a large-(C)/bounded-(C) seam are required.
- Found that the inherited upward-(C) service time has factorial growth and
  infinite stationary mean; factorial environment tails alone do not control
  that resolvent.
- Recorded a plausible closed countable-phase alternative and the exact
  promotion example showing why closure must be proved, not assumed.
- Completed a release audit: finite replays pass, but hashes, dependencies,
  provenance, mutating scripts, layout, metadata, and theorem-status claims
  all require replacement after the proof closes.
- Replaced the undefined “active species/linkage” wording by an exact
  classwise projection: every bounded-but-varying coordinate counts; only
  classwise constant coordinates can be absorbed into rates and deleted.

## 2026-08-09T22:05:19-07:00 - exact shielded/available seam closed

- Replaced the embedded-count activation calculation for
  `{2B,A+B}` and `{C,A+C,B+C}` by a direct physical-time factorial Foster
  argument. The fast linkage's corrected positive drift is only linear,
  while the catalyst-scaled monomolecular linkage has negative drift of order
  at least `-n log log n`.
- Replayed the shielded-linkage reduction and proved that exactly seven
  positive-invariant shielded supports are compatible with the fixed
  available support `{C,A+C,B+C}`. Six are handled by the factorial Foster
  argument; the remaining autonomous support `{0,2C}` has an explicit
  parity-law times product-Poisson stationary probability.
- Added a self-contained finite certificate and seven tests. The complete
  local suite now has 14 passing tests.
- Kept claim scope explicit: the direct fast-generator lemma covers 17 of the
  25 positive-invariant shielded masks, leaving eight multi-vertex masks in
  arbitrary pairings and all four signed one-active masks outside this note.

## 2026-08-09T22:18:00-07:00 - primary theorem interfaces checked

- Checked the relevant published tier-Foster, single-linkage, and
  one-dimensional recurrence theorems at their primary sources.
- Verified that the Anderson--Kim global top-S-tier criterion does not apply
  to the exact fast-neutral seam: its global top sources are neutral while
  the descending linkage is one rate tier lower.
- Recorded this as a scope check only, not a priority or novelty audit.

## 2026-08-09T22:31:00-07:00 - first residual corrector gate isolated

- Exhaustive rank reduction closed six additional minimal available partners
  by full-network deficiency zero, but showed why larger available supports
  cannot be inferred from those minimal subnetworks.
- Isolated the first exact arbitrary pairing
  `{B,2A,B+C}` / `{0,A,C}` and an orientation for which the natural tilted
  factorial generator has positive drift of order `B` at `(n,n^2,0)`.
- Reduced the next analytic task to a shell-uniform Poisson corrector or
  killed-resolvent estimate for the deficiency-zero fast phase on
  `A+2B=N`, including its unbounded Poisson `C` coordinate.
- Retained the four signed masks as a separate unresolved seam.

## 2026-08-09T22:48:00-07:00 - residual fast phase stress-tested

- Derived the exact conditional product law and factorial moments for the
  fast `{B,2A,B+C}` linkage. Its equilibrium exposes `A=Theta(sqrt(q))`,
  and the available linkage has averaged `q` drift `-Theta(sqrt(q))`.
- Obtained a shell spectral-gap route of order at least `sqrt(q)`, but found
  that stationary `L2` control does not give the required pointwise weighted
  corrector bound from arbitrary phases.
- Refuted the naive proper-workload shortcut `H=q+C`: after one positive
  actual target, the next workload change can be positive with probability
  tending to one and instantaneous drift of order `q`.
- Isolated the genuine remaining episode as a whole fast busy-period
  contraction, with a separate weighted `q+rho C` large-environment region.
- Found no physical null or transient network; the effective averaged level
  chain is strongly inward, so the result remains plausible but uncertified.

## 2026-08-09T23:08:26-07:00 - hard-stop package verified

- Derived the exact fast-phase scalar
  \(Z=A+(2v/(t+v))C\), whose generator is
  \(2\alpha B-\beta(A)_2\), and recorded the associated square-root-scale
  Riccati limit. It identifies the transient mechanism but does not replace
  the missing shell-uniform killed-resolvent estimate.
- Completed a consistency pass over the status, certification report,
  research notes, finite certificates, and release audit.
- Replayed the isolated non-mutating verifier: all 15 finite tests passed and
  the declared files were unchanged.
- Enforced the repair program’s hard stop. No replacement theorem manuscript
  or PDF was created because global T3-2 and the signed-service seam remain
  unproved.
