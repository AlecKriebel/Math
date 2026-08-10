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

## 2026-08-10T08:12:00-07:00 - exact signed-service seam closed

- Replaced the nonproper signed-workload shortcut by a two-region physical-time
  proof. A positive linear workload has quadratic generator drift outside the
  bounded-(A,C), large-(B) tube; inside that tube, stopped regeneration
  cycles turn the order-(1/B) signed service probability into a uniform
  negative drift for the square of the proper workload.
- Used exact compensators rather than a genealogical ledger, stopped rare
  cycles at shell exit, and included autonomous boundary classes.
- Exhaustively checked every strongly connected orientation of the displayed
  supports. An independent adversarial review found no counterexample or
  remaining gap at the exact stated scope.
- Recorded the strict limitation: the theorem is not monotone under adding
  complexes. It contributes exactly two new non-deficiency-zero pairs to the
  positive support table and zero pairs to the signed shielded/available row.

## 2026-08-10T08:36:00-07:00 - residual fast-shell pair closed

- Proved positive recurrence for
  `{B,2A,B+C}` / `{0,A,C}` for every strongly connected orientation and every
  positive choice of present rates.
- Constructed a proper linear return workload whose bad set lies in the core
  `A=O(sqrt(q)), C=O(1)`, where `q=A+2B`.
- On a window of length `T/sqrt(q+1)`, used the exact scalar
  `Z=A+(2v/(t+v))C` to obtain a uniform Riccati limit and strict negative
  expected `q` drift. Transient immigration--death domination controls the
  unbounded `C` coordinate from every core state.
- Added a fixed square-root safety margin, super-polynomial cleanup-exit
  bounds, and polynomial exceptional-return/count moments before telescoping
  the core trace. This closes the prior stationary-start and endpoint-cost
  gaps.
- Two independent proof audits found no remaining load-bearing defect. The
  finite certificate exhausts all `18 x 18` strongly connected three-node
  orientation pairs.

## 2026-08-10T08:51:20-07:00 - global interface compressed

- Replayed the full shielded/available support universe without deleting
  reactions or assuming recurrence is monotone under support enlargement.
- After finite classes, common active invariants, full deficiency zero, the
  three exact physical-time branches, and the Anderson--Kim one-step tier
  theorem, exactly 2,312 positive-invariant and 199 signed ordered support
  pairs remain.
- Enumerated the complete monomial comparison arrangement: 21 comparison
  planes, 37 simplex vertices, 193 tier/active types, and 259 exact
  availability descriptors. Twelve canonical asymptotic gate types cover all
  remaining one-step tier failures.
- Opened the next structural proof at the one-active gates: replace the false
  finite phase by a killed or closed unimolecular cofactor process, with
  explicit promotion and endpoint-cost alternatives.

## 2026-08-10T09:41:08-07:00 - affine flags certified; phase gates isolated

- Proved an exact levelwise Gordan alternative for whether a tier flag can
  occur in one real affine stoichiometric class, and checked every failed
  pair--descriptor incidence with exact rational arithmetic.
- Closed 151 additional support pairs classwise (143 positive, eight signed):
  none has an affine-feasible failed descriptor, so the class-local
  Anderson--Kim entropy Foster argument applies. Two independent audits found
  no load-bearing gap; lattice reachability is not used in this implication.
- Replaced the proposed one-active theorem by a claim-neutral local record:
  the killed unimolecular actual-target estimate is proved, while uniform
  old-debt clearance, total nested-entry control, and marked Foster gluing are
  stated explicitly as open.
- Classified all affine-feasible two-active failures into seeded/dormant
  promotion, 930 rank-one top-phase incidences, and 42 incidences with the
  unique rank-two support `{B,2A,B+C}` up to relabeling. The structural
  classification passed adversarial review and makes no recurrence claim.
- Added the exact all-active finite classification: 1,269 incidences on 403
  pairs, each with one whole flat top linkage, compressed to five
  rank/deficiency shapes. Its analytic gluing theorem remains open.

## 2026-08-10T11:03:11-07:00 - fixed-box service refuted; countable averaging opened

- Found an exact stabilizing one-active network in which a fast
  immigration--death cofactor leaves every fixed inactive box before a slow
  old-debt service clock rings with probability tending to one. This refutes
  the proposed finite-box stopped-kernel minorization and prevents the same
  tightness-to-finite-support error from re-entering the repair.
- Replaced that step by a quantitative countable unimolecular averaging
  lemma. Degree-two lower propensities admit polynomial Poisson correctors;
  Dynkin's formula gives an `O(N^-1/2)` physical-time integrated-clock error
  from bounded initial phases while retaining every slow reaction.
- Isolated a sharper structural reduction: disjoint linkage supports force
  the only non-invariant open countable phase to be a one-dimensional
  immigration--death linkage `{X,X+U}` (up to relabeling). Conservative
  phases are finite on their fixed inactive-total classes, while the whole
  open triple makes `X` an exact invariant. The remaining one-active task is
  therefore a finite marked return graph driven by explicit Poisson-averaged
  hazards, followed by the global entropy/debt seam.

## 2026-08-10T12:06:23-07:00 - phase scope frozen; global seams narrowed

- Added an exact, claim-neutral one-active shape certificate. The
  affine-filtered candidate branch has 1,227 support pairs and 3,297 failed
  incidences; the only wholly top countable phase is the one-dimensional
  open pair {0,U}, occurring in 222 incidences on 74 pairs. The row hash is
  5086c198fab678cba7e8ce8d10d6621887456f9f7caa8a188e5d68a214c52854.
- Proved the conditional common-potential physical-time gluing lemma:
  generator-good motion is appended by Dynkin's formula, while each bad-tube
  episode must have strict drift for the same proper endpoint potential.
  This removes switch tolls but does not manufacture a missing local
  episode.
- Recorded a crucial limitation: a negative descriptor workload increment
  does not automatically imply negative factorial-entropy drift under
  subpower tier separation. Every carrier theorem must retain the actual
  logarithmic endpoint reward, a fixed pairwise rate correction, or a direct
  entropy estimate.
- Found a rate/orientation-dependent positive top invariant
  q_b=(2,b,4-b) which closes all twelve former two-node all-active curvature
  seam pairs. The strong lower graph makes the relevant coefficient
  intervals overlap. Also observed that every rank-two whole-top incidence
  has lower linkage {0,C}, so its displayed positive top invariant has
  immediate negative linear drift when C is large. These all-active claims
  are being independently encoded and audited.
- The 895 seeded/top-activation rank-one carrier incidences now have audited
  integrated-hazard and race bounds as scalar-workload episodes, but still
  require a fast-phase corrected-factorial endpoint lemma. The 25 cap-zero
  activations additionally require an interior lower-tail estimate before
  their geometric service count is valid.

## 2026-08-10T12:20:42-07:00 - all fourteen rank-two partners certified

- Extended the residual fast-shell proof with top support
  \(\{B,2A,B+C\}\) to every one of the fourteen compatible lower supports
  in the rank-two two-active atlas, for arbitrary strongly connected
  orientations and positive present rates.
- Used one proper outer workload to return large \(q=A+2B\) states to the
  moving Riccati core. Ten partners have direct quadratic \(2C\) control;
  the other four use explicit physical-time unbounded-\(C\) regenerative
  blocks, including the dormant \(\{0,A,AC\}\) atom.
- Added the all-fourteen cleanup estimate: on the typical core event,
  \(C\)-death is at least order \(NC\), all added \(C\)-birth is at most
  \(KN+K\sqrt N\,C\), and the positive-\(q\) occupation cost is
  \(O((\log N+C_0+C_0^2)/N)=o(1)\).
- An independent proof replay checked the workload coefficient intervals,
  large-\(q\) bad-set geometry, all three linear-phase alternatives, both
  dormant targets, squared-workload iteration, cleanup endpoint moments,
  and the final random-time Foster trace. No load-bearing gap or
  orientation/rate counterexample remained.
- The family has 42 descriptor incidences on fourteen ordered support
  pairs. The phase classifier runs after the previously certified
  \(\{0,A,C\}\) residual branch is removed, so the prior overlap is zero:
  all fourteen are new positive-invariant pairs and none is signed. The
  certified remainder changes from \((2169,191)\) to \((2155,191)\).
  Global T3-2 remains unclaimed.

## 2026-08-10T12:35:41-07:00 - all-active local theorem independently audited

- Completed an independent proof replay of the all-active physical-time
  generator theorem on all 403 affected support pairs. The exact disjoint
  split is \(288+91+24=403\): two-node rank-one, arbitrary directed
  three-node rank-one, and rank-two whole-top supports.
- Checked the two-node rate-correction inequalities including all twelve
  curvature seams, the triple-top lower-rate domination on both failed and
  passing cones, and the rank-two exact positive invariant with lower
  support \(\{0,C\}\). No orientation/rate counterexample or analytic gap
  remained at this scope.
- Added separate certificate flags for the local all-active theorem,
  pair-level recurrence, and global T3-2. Only the first is true. No pair
  count was promoted: corrected-factorial endpoints and lower-dimensional
  interface composition remain open.

## 2026-08-10T12:51:40-07:00 - 51 all-active-only pairs certified classwise

- Independently replayed the exact all-active-only selector: all 209 failed
  incidences on its 51 positive-invariant pairs occur in the certified
  all-active table, share the pair's fixed reversible two-node rank-one
  deficiency-zero top, and satisfy the curvature-cofactor hypothesis.
- Corrected the audit-pending draft's potential from log-factorial entropy to
  the continuous rate-adjusted entropy proved in Proposition 5.2. Its
  difference from ordinary entropy is exactly affine, so bounded reaction
  increments preserve the Anderson--Kim logarithmic exit on every passing
  boundary descriptor.
- Verified the classwise compactness step: every divergent sequence has a
  subsequence with generator tending to minus infinity, hence the set where
  the generator exceeds `-1` is finite. Shifted nonnegative entropy,
  localized Dynkin, nonexplosion, and the finite trace give finite mean
  positive return on every closed irreducible class.
- Promoted only this exact branch. It is disjoint at the current ordered
  stage and changes the certified remainder from `(2155,191)` to
  `(2104,191)`. Global T3-2 remains uncertified.

## 2026-08-10T13:30:10-07:00 - rank-one factorial endpoints audited

- Proved and independently replayed the corrected-factorial endpoint
  theorem for all 920 nonfinite exact-flat rank-one incidences. The replay
  checked the exact \(\{B,2A\}\) generator inequality, the
  \(\{2A,R+I\}\) factorial-ratio cancellation and killed exponential
  moment, the independent zero-clock semigroup, subpower
  propensity-times-log uniform integrability, and both carrier debt blocks.
- Turned on only the narrowly named local endpoint flag. Pair-level
  recurrence remained unclaimed and global T3-2 remained uncertified.
- Encoded the exact rank-one no-promotion selector. The 310 rank-one pairs
  split into 77 with a two-active promotion obstruction and 233 without.
  The 233 local branch splits as 154 safe reversible all-active, 67
  directed triple, and twelve with no all-active failure.
- Found the load-bearing post-counterexample boundary: 92 of those 233
  still have a feasible one-active failed descriptor. The remaining 141
  have none and split \(72+57+12\) across the same all-active branches.
  Their pair-level common-potential composition is a candidate under
  independent audit; no recurrence count has yet been promoted.

## 2026-08-10T13:38:46-07:00 - 141 rank-one no-promotion pairs certified

- Repaired the only composition seam found by independent audit: the
  reversible all-active theorem used continuous entropy while the carrier
  used discrete log-factorial entropy. The exact detailed-balance
  finite-difference identity bounds the discrete top drift by the same
  curvature-cofactor monomials, and the lower factorial exit dominates by
  a divergent logarithmic factor.
- Independently replayed the full 141-pair selector and common-potential
  proof: unique top-mask compatibility, all feasible descriptor branches,
  the sequence-to-finite-exception step, duration and endpoint
  integrability, nonexplosion, and classwise positive return all passed.
- Promoted exactly the 141 positive no-promotion pairs having no
  affine-feasible one-active failure. The 233-pair higher-dimensional local
  theorem remains useful, but its other 92 pairs are explicitly blocked by
  one-active failures.
- The branch is disjoint from all prior ordered closures and changes the
  certified remainder from \((2104,191)\) to \((1963,191)\). Global T3-2
  remains uncertified.
