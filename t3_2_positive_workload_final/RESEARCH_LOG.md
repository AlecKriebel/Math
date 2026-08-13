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

## 2026-08-10T14:28:00-07:00 - remaining 92 rank-one pairs certified

- Classified all 272 one-active failed incidences on the remaining 92
  no-promotion pairs into 230 direct enabled-top rows, 32 zero-source seed
  rows, and ten frozen singleton faces. The partition and its arbitrary
  strongly connected orientation proof are exact at this support scope.
- Replaced the invalid universal old-debt minorization by a zero-contest
  physical episode. Refined tier compression makes both inactive counts
  eventually fixed on a genuine one-active subsequence; the stripped killed
  immigration/death/conversion phase has exponential endpoint and
  polynomial-log occupation bounds. Retaining all lower interruptions costs
  \(O(\log N/N)\), while the unperturbed endpoint gives common
  corrected-factorial drift \(-\log N+O(1)\).
- Independent adversarial audit verified the geometric seed restart, the
  size-biased interruption compensator, the frozen-class alternative, and
  same-potential classwise gluing. Focused replay passed all seven tests.
- Promoted exactly these 92 disjoint positive pairs. The certified remainder
  changes from \((1963,191)\) to \((1871,191)\). Universal one-active closure
  outside this branch and global T3-2 remain uncertified.

## 2026-08-10T14:47:08-07:00 - 36-pair promotion candidate held at audit gate

- The exact promotion-only selector contains 36 pairs (32 positive and four
  signed), each with one feasible two-active failure. Its seeded and
  finite-shell estimates passed initial review.
- Independent audit found that the dormant \(\{B,2A\}\) argument incorrectly
  treated \(BC\)-source and \(AC/A\)-source clocks as being on the same
  scale: the former can be \(\Theta(N^2)\) while the latter are
  \(\Theta(N)\). Consequently the asserted uniform direct-race probability
  and geometric debt bound are not proved.
- No counterexample was found. The candidate note now records the required
  finite priority-macrochain lemma and leaves every analytic, recurrence,
  and global flag false. If repaired and certified, the correct ordered
  arithmetic would be \((1871,191)\to(1839,187)\).

## 2026-08-10T15:07:08-07:00 - exact 36-pair promotion branch certified

- Replaced the invalid equal-scale dormant race by a finite physical
  priority macrochain. The exact dormant split is seven unique-\(0\) rows,
  seven \(A\)-enabled \(\{B,2A\}\) rows, and two disabled finite classes.
  Whenever \(C>0\), every \(BC\)-source edge has order \(N^2\) and lowers
  descriptor workload; \(A/AC\) interference has probability \(O(N^{-1})\).
- Tracked at most two units of reflected workload debt and excluded every
  service-free reset SCC in \(\{0,A,BC\}\) by strong connectivity to
  \(2C\). Equal-scale internal \(AC/BC\) reactions have a geometric count,
  and killed \(BC\)-windows have \(O(N^{-1})\) whole-shell factorial cost.
- Two independent replays passed the twenty seeded paths, sixteen dormant
  phases, common corrected-factorial lift, duration and endpoint moments,
  fixed-class disabled alternative, and exact disjoint selector. Focused
  finite replay is green.
- Promoted exactly 32 positive-invariant and four signed pairs. The certified
  remainder changes from \((1871,191)\) to \((1839,187)\). The suppressed
  no-whole-top promotion orbit and global T3-2 remain uncertified.

## 2026-08-10T16:02:48-07:00 - suppressed four-pair orbit certified

- Isolated the exact support orbit
  \(\{U,I+V\}/\{0,I,2I,I+U\}\): four positive-invariant pairs,
  28 affine-feasible failed incidences, no signed pair, and no overlap with
  any earlier certified branch. The selector and exact cleaned macro rewards
  are frozen by the scoped certificate.
- Proved a transient top-shell birth--death occupation lemma using the
  invariant \(Q=U+2V-I\). The proof treats the one-active rows, the
  equal-depth immediate-stop flag, the balanced cut-hazard window, and both
  extreme regimes \(M^2/D\to0,\infty\), while retaining every physical
  reaction clock.
- Two independent audits replayed all six obligations: macro endpoints,
  martingale and size-biased moment bounds, all-clock cleanup, arbitrary
  strong-orientation cut service, rare positive endpoint cost, and the
  single corrected-factorial composition. Focused tests are green.
- Promoted exactly four additional positive-invariant pairs. The certified
  remainder changes from \((1839,187)\) to \((1835,187)\). Global T3-2
  remains uncertified.

## 2026-08-10T16:40:23-07:00 - critical fifteen-pair one-active trace certified

- Froze an exact fifteen-pair selector with 83 feasible failed incidences:
  75 coefficient-critical active-\(C\) rows and eight companion rows. All
  fifteen pairs are positive-invariant, their overlap with every previously
  certified selector is zero, and the pair fingerprint is
  `6ec74f95e50e39ecda002b988d8233ae74c040ff9bb3518892dfd980bfad06d3`.
- Proved the full-reaction positive-\(Q\) trace for
  \(\{0,A+C,B+C\}\). Continuous-time Kac gives a unary-to-quadratic
  event with coefficient \(a_-/\{\Lambda N\}\); all reverse or multiple
  lower events are order \(N^{-2}\). A multiplicative phase corrector and
  subcritical block comparison give exponentially small inactive/level
  boundary exits with polynomial endpoint UI.
- Corrected the six direct companion rows to use their genuine countable
  stripped \(\{0,B\}\) immigration--death phase, not a finite carrier.
  Two additional zero-source templates have geometric exact-base resets.
  One squared corrected-factorial potential covers the critical trace,
  companion episodes, and every passing cone.
- Two independent audits passed the Kac coupling, Catalan-aware boundary
  estimate, squared-potential drift, all four companion templates, and
  classwise sequence gluing. Promoted exactly fifteen positive pairs. The
  certified remainder changes from \((1835,187)\) to \((1820,187)\).
  Global T3-2 remains uncertified.

## 2026-08-10T18:18:27-07:00 - excluded equality-order stress case resolved locally

- Audited the sharp relative-debt equality network
  \(0\leftrightarrow B+C\),
  \(B\to A\to A+B\to2B\to B\). Its two selected order-two return
  words do not determine the physical sign: a primary \(B\to A\)
  activation occurs with probability \(\kappa_1/(\beta N)+O(N^{-2})\)
  and opens a macroscopic stabilizing excursion.
- Recorded the exact identity
  \(Q=C-A-B\),
  \({\cal L}Q=-\kappa_2A+\kappa_4(B)_2\), together with the exact
  immigration--death chain obtained from the clock
  \(u=\int B_t\,dt\). The longer literal base-return asymptotic remains
  explicitly conditional and is not used as a theorem.
- Proved instead an all-reactions-retained stopped block. Conditional on
  the rare activation, a fixed positive probability of
  \(\lfloor\varepsilon N\rfloor\) clean \(A\to A+B\),
  \(B+C\to0\) stages gives a fixed-fraction population loss. For the
  common potential \(W=(1+{\cal F}_\ell)^4\), the successful contribution
  is \(-\Theta(N^3\log^4N)\), failed endpoints cost only
  \(O(N^2\log^4N)\), and the unconditional mean duration is bounded.
- Two independent audits passed the stopped episode, endpoint moments,
  nonleading-trigger stop, debt transfer, and duration accounting. The
  equality/PDMP focused suite passes 12 tests. This is a local theorem only:
  no support-pair count or global flag was changed.

## 2026-08-10T20:10:05-07:00 - universal one-active 1,227-pair branch certified

- Completed the arbitrary-orientation graph-to-physical-kernel lift for all
  3,297 affine-feasible failed incidences on the exact all-one-active
  selector. Finite mixed phases use a classwise killed-resolvent expansion;
  the sole open wholly-top phase uses its Poisson regeneration theorem.
  Family-II cap label two is now correctly interpreted as an arbitrary fixed
  class invariant $a_\Gamma\ge2$, with class-dependent constants.
- Used the common potential
  $W=(1+K+\sum_i\log(X_i!))^4$. Neutral base returns telescope before the
  first nonneutral endpoint; random upward overshoots have conditional
  moments of order $q>8$; and an endpoint-weighted $n^{1/8}$ boundary
  estimate pays every promotion or simultaneous boundary tie. The separate
  unweighted third-interruption estimate preserves the order-$n^{-3}$
  upward bound in the resistance-two case.
- Composed the local episodes on the all-species reflected marked chain.
  Atlas identity (8.6) yields a genuine fixed-width state-sequence tube, the
  $D_X=0$ part is finite classwise, and frozen/no-history bases cannot carry
  reachable positive old debt. A common-potential bad-sequence argument and
  the linear-growth birth bound give classwise recurrence and nonexplosion.
- Independent pair audit returned PASS (confidence 0.91) and replayed the
  exact selector hashes. The 1,227-pair set contains 1,076 positive and 151
  signed pairs; its only prior overlap is the fifteen critical positive
  pairs. Promoted the net new contribution of 1,061 positive and 151 signed
  pairs, changing the certified remainder from $(1820,187)$ to
  $(759,36)$. Global T3-2 remains uncertified.

## 2026-08-10T21:45:00-07:00 - exact 26-pair common-factorial branch certified

- Replayed the claim-neutral 26-pair selector inside the prospective 795.
  Its 124 feasible failed incidences split as 30 one-active, zero two-active,
  and 94 all-active. The 30 one-active rows reduce to twenty direct
  pure-active-source rows, eight Family-III resistance-zero origin-service
  rows, and two frozen/no-history rows for arbitrary strong orientations.
- Proved the missing discrete powered-top estimate. With the rate-adjusted
  correction \(\ell\), the reversible top drift is negative entropy
  dissipation plus a curvature-cofactor-sized error. The exact fourth-power
  carré/Taylor remainder is absorbed by that dissipation and the partner
  linkage's divergent logarithmic exit on all 94 failed all-active rows.
- Used the same \(W=(1+F_\ell)^4\) in the one-active aggregate kernel,
  passing cones, and all-active cones. The endpoint-weighted \(q>8\)
  three-interruption estimate pays the full \(O(L_n+J)\) linear-correction
  boundary cost. Reflected all-debt gluing and the linear-growth birth bound
  give classwise positive recurrence and nonexplosion.
- Independent final audit returned PASS. The branch contains 26 positive and
  zero signed pairs, is a subset of the prospective 795, and has zero overlap
  with all prior-certified branches. Promoted the exact update
  \((759,36)\mapsto(733,36)\), leaving 769 pairs. Global T3-2 remains
  uncertified.

## 2026-08-10T21:41:03-07:00 - dormant 407 and generalized-FII seam frozen for audit

- Froze the exact 407 dormant, no-wholly-top two-active incidences on 333
  pairs.  Their normalized support menu has 188 ratio-sensitive templates
  and 154 templates after the ratio is forgotten.  The
  arbitrary-orientation cut proof has aggregate service-resistance split
  \(395+10+2\), with maximum two and an upward gap of one.
- Replaced the exceptional finite-phase shorthand by its exact countable
  birth--death chain.  Its product ratio gives factorial cofactor tails,
  all fixed endpoint moments, and the physical-duration estimate needed by
  the all-reaction resolvent.  The only subpower-neutral macro pair is
  handled by a propensity-times-entropy-gap trichotomy for arbitrary fixed
  \(\ell\).
- Classified all 1,104 one-active failures on the same 333 pairs.  The 951
  generalized-Family-II rows lie on exactly 317 pairs.  Relabeling the
  spectator, old active species, and unique top cofactor as \(U,V,I\)
  produces 146 normalized support templates shared exactly with 317 hard
  \((1,3,0)\) targets.  Every target has three source rows, one for each
  spectator cap; the exact map hash is
  2b34a3c828fa55a93a5595555f7dd5160e7a676338245bd0611809f399b4296f.
- Wrote the candidate killed one-species Green lemma, factorial promotion
  boundary, charged entry-macrojump estimate, and same-\(W_\ell\)
  telescoping handoff.  Six focused tests pass.  This checkpoint is pending
  independent analytic audit; no pair or global certification flag was
  changed.

## 2026-08-10T23:10:00-07:00 - exact 416 easy-promotion branch certified

- Proved the positive-overshoot exponential Lyapunov estimate for the
  reversible rank-one and homogeneous quadratic shells, yielding the
  conditional moments above order eight required by the common fourth-power
  potential. Replaced the overbroad finite-shell citation by an explicit
  six-support reset-cut argument and froze the actual mixed-phase
  pure-active-source premise in the executable selector.
- Composed 762 easy promotion incidences, 1,455 compatible one-active
  incidences, 117 closed rank-one incidences, and 117 all-active incidences
  with one pair-fixed corrected-factorial fourth power. The marked
  fixed-class argument charges every moving-boundary endpoint and retains
  every reaction clock.
- Independent audit returned PASS and replayed the exact 416-pair selector:
  414 positive-invariant and two signed pairs, with fingerprint
  `8c3325983568c53772f024080c0b95d37873cfe0a149386ec9829d1d9323e186`.
  Promoted \((733,36)\mapsto(319,34)\). The hard 333-pair family and global
  T3-2 remain uncertified.

## 2026-08-10T23:25:00-07:00 - rank-two thirteen-pair common scalar certified

- Closed the rank-two workload/factorial switch with one proper scalar per
  pair: \((1+F)^4+\eta(1+H_w)^6\) on eleven homogeneous supports and the
  fifth workload power on the two weighted supports. The failed all-active
  polynomial gaps are respectively one and one-half; passing bounded-\(C\)
  cones have the extra powered-factorial logarithmic gap.
- Independent audit replayed all thirteen supports, every possible strong
  orientation and positive rate choice, the rank-two flat scaling, exact
  fourth-power terms, nonexplosion, and localized Dynkin. No counterexample
  was found.
- The thirteen pairs are positive-invariant and disjoint from the 416-pair
  branch. Promoted \((319,34)\mapsto(306,34)\), leaving 340 pairs. Global
  T3-2 remains uncertified.

## 2026-08-10T23:40:00-07:00 - hard 333 uniform Green claim fails audit

- Independent audit preserved the exact 407-incidence/333-pair selector and
  the 951-to-317 promotion map, but refuted Lemma 7.1 as written. Complete
  strong digraphs on \(\{U,I,V+I\}\) and \(\{0,2U,U+I\}\) admit
  historically consistent positive-debt bases with arbitrarily large
  spectator \(U\); taking \(U_n\asymp\log n\) contradicts the claimed
  start-uniform polynomial Green sum.
- This is not a T3-2 counterexample. The likely repair is a start-weighted
  factorial Green estimate combined with expectation-level workload
  accounting; the current pathwise service inequality also cannot ignore
  accumulated spectator mass. All 333 pair/global flags remain false.

## 2026-08-10 - final seven stopped-service branch certified

- Replaced four invalid shortcuts in the rank-two mixed-profile seven-pair
  candidate: the seed count now uses localized PF trial times and a
  compound-geometric exponential moment; activation and service populations
  have separate exact birth/death counters; the service deaths use their
  random compensator rather than a fixed Poisson domination; and all top
  reactions are restored through the deterministic maximal-factorial/total
  population envelope.
- The resulting common scalar is
  \(V=(1+F)^4+\lambda(1+A+B+C)^6\).  The stopped wedge episode has moments
  above order eight and negative physical-time drift, while every divergent
  state outside the dormant wedges is generator-good for the same \(V\).
- Independent audit exhausted 569,898 strongly connected carrier digraphs,
  replayed the ODE invariant-set and uniform service-integral argument, and
  passed the shell, endpoint, gluing, nonexplosion, test, and PDF-render
  obligations.  The promoted exact payload is
  `0c06d14f1ad53c357d0c3ba0127e0c0ce3bac12db8c866523dedd3b5fb401eee`.
- Promoted exactly seven positive-invariant pairs and no signed pair:
  \((306,34)\mapsto(299,34)\).  The remaining 333 pairs are exactly the hard
  dormant/generalized family.  No hard-family or global flag was changed.

## 2026-08-11T22:21:00-07:00 - proof-only hard-317 audit finds singular renewal

- A hostile analytic audit refuted the repaired local theorem even under its
  historical positive-debt hypothesis.  On
  \(L_+=\{0,V+I\}\), \(L_0=\{I,2U,2I,U+I\}\), complete strong digraphs
  admit historically reachable bases \((U,V,I)=(0,n,0)\) with \(D_V=n\).
  The immediate proper return has probability \((n+1)/(n+5)\), so the pure
  renewal is order \(n\), the first upward endpoint has probability at least
  \(1/4\), and the physical duration is order \(n\).  This is a counterexample
  to the proposed local kernel, not to recurrence or T3-2.
- Derived a proof-first replacement trace.  For an exact proper pair
  \(\{aU,V+I\}\), put \(w_a(cU+bI)=c+ab\) and
  \(m_a(u)=\min\{b:w_a(cU+bI)\le u\}\).  Every leading cleaned lower macro
  satisfies the exact coboundary
  \(\Delta\{V+m_a(U)\}=m_a(U')-b_{\rm target}\le0\).
  Strong connectivity forces strict drops from every equality phase; at
  most three strict drops force a physical old-active service.  The candidate
  priority block has rare dirty macros of order \(n^{-1+o(1)}\), duration
  \(n^{2+o(1)}\), factorial endpoint occupation, and common fourth-power
  drift.  It is frozen for independent proof audit and is not promoted.
- Classified every exact proper base without orientation enumeration.
  Priority is needed exactly when the proper opening is enabled but no
  cofactor-free lower source is enabled.  This occurs at finite bases in all
  six source-zero supports and at \(u=1\) for the single source-\(U\) support
  \(\{U,V+I\}/\{I,2U,2I,U+I\}\); no source-\(2U\) base is singular.
  All hard-family and global flags remain false.

## 2026-08-11T22:34:31-07:00 - exact-pair ordinary kernel separated correctly

- Proved the enabled-base renewal comparison with the total clock of every
  physically enabled lower escape in the numerator.  This removes the
  invalid denominator comparison when another degree-two escape dominates.
- Split the renewed stopped kernel into the order-one direct lower kernel
  \(Q_0\), the \(O(n^{-1})\) interrupted-proper kernel, and the
  superpolynomial proper-only boundary kernel.  The direct branch is no
  longer assigned a false \(n^{-1}\) estimate.  A slow/fast geometric race,
  reserve pairing, and physical holding-time recursion give all-order
  polynomial, factorial-endpoint, and fixed time-moment bounds without a
  finite interruption cap.  No certification flag was changed.

## 2026-08-11T22:58:05-07:00 - exact proper-cloud averaging audited

- Derived the exact reversible carrier product and the resulting effective
  lower-source hazard
  \(n^{-b}(u)_{ab+c}\) for every exact proper pair.  The same bounded
  coboundary \(V+m_a(U)\) therefore governs both ordinary and singular
  bases; all seventeen actual equality sets are proper, and the unbounded
  equality trace has the expected maximal-source factorial Foster drift.
- A hostile proof audit found no network counterexample but rejected the
  draft as incomplete.  A sourcewise two-insertion Green estimate is needed
  for the relative first-kill error; the contracted equality kernel needs an
  explicit uniform compact minorization; physical duration must be carried
  through an augmented Green recursion; and static no-feasible faces must
  be discharged by the historical positive-debt scope.  No flag was changed.

## 2026-08-12T00:02:37-07:00 - exact-cloud common-fourth-power block proved

- Replaced the incomplete first-kill argument by an exact base-local-time
  decomposition and a reversible ordered-Green identity.  For every lower
  edge, direct level-zero clocks are separated from opened-excursion
  occupation, and the sourcewise two-insertion error is
  (O((1+u)^2/n)) relative to the exact effective hazard.  A shifted
  downward-carrier potential also pays a second lower firing at its actual
  included endpoint with arbitrary fixed polynomial weight.
- Closed the four missing analytic seams for all seventeen exact proper
  pairs: uniform compact killing after cofactor-rate normalization, a
  time-marked additive-functional Green recursion for physical duration,
  a continuation/terminal logarithmic entropy majorant retaining the actual
  service endpoint, and a disjoint (D/E/B) uniform-integrability split for
  the fourth-power Taylor expansion.
- Two independent hostile proof replays issued strict PASS on the identical
  completion SHA
  `33dab04fba9d8f70b30f0ac43dffe7e432124867c51f5c647300f9e0bf80e6e4`;
  the ordered-Green input SHA is
  `ea92e6c7a249f75a33d841682be2df620c4d0cab638f982ff40c7e4ca6bf50c2`.
  This is a local theorem only.  No incidence, pair, or global flag was
  promoted; the remaining 129 hard templates and final marked composition
  are still under proof and audit.

## 2026-08-12T00:26:04-07:00 - separated-six regenerative repair derived

- Replaced the selected-cycle hazard heuristic for the six separated
  supports by a full proper-cycle Feynman--Kac calculation.  An
  orientation-free slack-lifting lemma makes every required \(I\)-order-one
  lower source accessible in every proper residue class.
- Resolved the proposed \(\{0,U,2U,V+I\}/\{2I,U+I\}\) counter-witness:
  its single graph lap misses \(U+I\), but a legal pre-return slack word has
  fixed proper probability followed by an order-\(n^{-1}\) \(U+I\) race.
  Thus the aggregate cycle hazard is order \(n^{-1}\), while \(2I\)-source
  hazards are order \(n^{-2}\).
- Corrected the two-mark estimate: shared nested openings give
  \(\mathbb E J_{2I}^2=\Theta(n^{-3})\), so the valid common bound is
  \(O(n^{-(\max(b_y,b_z)+1)})\), which still gives the required
  \(O(n^{-2})\) first-kill error.  The resulting local block has
  \(n^{1+o(1)}\) physical duration and common-fourth-power drift.  The note
  is claim-neutral and no certification flag was changed.

## 2026-08-12T02:20:00-07:00 - direct/open one-active subpower seam repaired

- The strict one-active audit exposed that a single service pays only
  \(\log n\), while a deterministic inactive cloud
  \(u=n^{o(1)}\) can have factorial-linear endpoint cost of order
  \(u\log(2+u)\).  Replaced the bounded-start inference by an all-clock
  episode completing \(K=1+u\) net active services.  Its active reward
  \(-K\log n\) dominates the entire one-sided inactive entropy, and the
  active population remains \(n-n^{o(1)}\).
- For the 99 direct incidences, proved a background-independent service
  margin with a Harris labelled-particle subclock in the stripped
  unimolecular top process.  Negative-binomial service time, compound
  Poisson inactive mass, and the degree-two lower compensator give
  endpoint-weighted defect probability \(n^{-1+o(1)}\), superpolynomial
  moving-boundary error, and actual post-jump endpoint moments.
- For the six open incidences, constructed the service ladder from the
  exact support \(\{C,A+C\},\{0,B,2B,B+C\}\).  The unlocalized service/defect
  stopping time is measurable in the autonomous \((B,C)\) process; only
  afterward is the \(A\)-boundary imposed.  Conditional on the \((B,C)\)
  path, the exact binomial-plus-Poisson immigration--death law gives the
  one-sided endpoint entropy and factorially small boundary tail.
- The arbitrary fixed correction is charged only through the telescoping
  terminal difference \(\ell\cdot(X_\tau-X_0)\), not once per fast internal
  reaction.  The byte-frozen candidate note has SHA-256
  `fbd9f42815b08a2030d931482b70ff10aca9a92df3c080e2533f275fa6733c2a`;
  focused tests passed 9/9 and a Tectonic render completed.  All certification
  flags remain false pending a fresh hostile proof replay.

## 2026-08-12T03:15:00-07:00 - proof-first global composition and one-linkage gate

- A fresh hostile proof replay returned strict PASS on the byte-frozen
  direct/open multi-service repair
  `fbd9f42815b08a2030d931482b70ff10aca9a92df3c080e2533f275fa6733c2a`.
  The audit checked the background-independent tagged service clock, the
  autonomous open stopping law, endpoint-weighted defects, factorial
  upcrossings, arbitrary linear corrections, and the exact fourth-power
  expansion.  Its audit note SHA is
  `9ecd375375e6942d803d068591c80f87a27119a37927dd3617f2e743afdab848`.
- An audit of the inherited one-linkage citation found a genuine global proof
  gap: the published theorem assumes a pure multiple for every species.  The
  support `{0,B,2B,A+B}` and a full-rank three-species analogue violate its
  tier hypothesis inside one irreducible class.  These are proof-interface
  counterexamples, not recurrence counterexamples.
- Proved the unique two-dynamic-species exception by an all-clock geometric
  origin-launch service block and physical-time Foster composition.  Its
  theorem SHA is
  `17da97fb25965c2f5ec9369691343927c34f6b0da75cad31cdf99ec2611c0d13`;
  hostile replay is pending.  The genuinely three-species one-linkage carrier
  theorem remains a publication gate.
- Added a proof-first global classwise composition note which separates the
  analytic projection, zero/one/two-linkage branches, nonexplosion, common-
  potential descriptor gluing, and finite support-set identity.  It explicitly
  leaves the single-linkage and hard-family inputs open and promotes no flag.

## 2026-08-12T03:30:00-07:00 - hard-333 fixed-class composition strict PASS

- Completed a fresh proof-first hostile audit of the frozen hard-333 theorem
  at theorem/source/test hashes `ddcc1f...`, `de618c...`, and `fb1bec...`.
  The common corrected-factorial fourth power, reflected-debt eligibility,
  repaired `D_1`-internal/`D_K`-terminal multi-service timing, actual endpoint
  and duration moments above order eight, dimensional handoffs, random-time
  Foster gluing, properness, nonexplosion, and finite-mean return all pass.
- Independently replayed the finite premises only.  The exact routing remains
  `1104+702+154=1960`, and all 407 dormant incidences normalize to the audited
  188 templates.  A stronger literal correction check found exactly one top
  mask on all 46 correction-relevant pairs; all 38 rank-one/all-active
  overlaps have identical masks.
- Frozen the audit in
  `research_notes/hard333_final_composition_independent_audit.md` (SHA-256
  `8bba33d321e7812a22b2422ca06c33d0abe2e4736c68e9c11be037d8a8819fd6`)
  with independent source/test and payload hashes `77deb4...`, `49771d...`,
  and `1fa6a3...`.  The mathematical verdict establishes recurrence of all
  333 hard pairs at this scope.  Candidate and global flags were not edited;
  the separate single-linkage theorem remains the global publication gate.

## 2026-08-12T04:10:00-07:00 - separated one-linkage carrier strict PASS

- Replaced the two rejected separated-scale constructions by a completed
  physical joint-return kernel.  The proof contracts only literal clean
  returns, retains every carrier and lower-source clock after the first
  mark, and uses the exact terminal priority
  \(B_O>S\text{ or }E>B_0\).  A normalized open-phase weight is raw at
  every completed base return, so no false unweighted spectator moment is
  needed even for a critical carrier genealogy.
- Proved the frozen/invariant/physical-loss trichotomy on one fixed closed
  irreducible class, the same-exponent clean Green bound, the full
  first-mark resolvent, raw exponential service/mark estimates, included
  boundary payment, almost-sure termination, all fixed duration moments,
  and the direct raw-exponential-to-fourth-power lift.  Finite support,
  orientation, reaction-word, and population enumeration play no role in
  these estimates.
- The publication theorem is frozen at
  `research_notes/proof_first_separated_full_all_clock_joint_return_theorem.md`,
  SHA-256
  `389e3b446006e9313238a0b4b0029f39e0f1cee0c2d90faf6e63cccf38a581e1`.
  An independent exact-byte hostile audit returned **STRICT PASS** and is
  frozen at
  `research_notes/proof_first_separated_full_all_clock_joint_return_independent_audit.md`,
  SHA-256
  `096ba806daa3f7f1bc336986d3248976ac8ade084cfbf5a60e524ceec96f75a6`.
  This closes the last local analytic obstruction in the three-species
  one-linkage classification; the unconditional one-linkage and global
  compositions remain separate proof and audit gates.

## 2026-08-12T07:55:00-07:00 - current universal-1212 theorem strict PASS

- Replayed the current universal one-active pair theorem from its present
  bytes rather than inheriting the audit of an older snapshot.  The exact
  target/source/test hashes are `0ab1cff9...`, `88537bc3...`, and
  `d31a410...`; the current payload is `85847255...`.
- The proof audit verified the aggregate all-clock killed kernel, all three
  interruption orders, actual cutoff-causing reactions and tie priority,
  endpoint moments above order eight, the open Poisson block, physical
  duration (O(n^3)), and the common fourth-power reflected-debt glue.
  Uniform fixed-class constants follow from finitely many literal
  fixed-width tubes plus sequential coercivity, not from descriptor
  compactness alone.  Mid-episode target hits are recorded immediately and
  the first return propagates the reflected mark before projecting the
  finite cycle occupation measure to the physical chain.
- The new exact-byte independent audit is
  `research_notes/one_active_fourth_power_pair_composition_current_independent_audit.md`,
  SHA-256
  `119918037899e9af543f321d3d019006abcbcf947b34c51b0af611c74b017db7`.
  Finite computation was used only to replay the net 1,212-pair set identity.

## 2026-08-12T08:05:00-07:00 - unconditional one-linkage theorem strict PASS

- Composed the classwise theorem for one active weakly reversible linkage,
  binary complexes, and at most three dynamic species.  A failed proper top
  tier is classified symbolically: the two-dimensional exception, separated
  singleton top, balanced tied top, and bounded two-disabled-top family are
  the only nonstandard cases.  The final separated dependency is the audited
  completed all-clock joint-return theorem, not either rejected predecessor.
- Repaired the composition's statewise seam.  A finite menu of literal
  all-clock rules is fixed, and outside a finite set the selector chooses the
  least rule which actually satisfies the common drift inequality.  A bad
  sequence plus proper-tier extraction would contradict the coercive estimate
  of one fixed candidate.  This proves uniform constants without assigning a
  tier label directly to a single state.
- The theorem is frozen at
  `research_notes/proof_first_single_linkage_at_most_three_species_theorem.md`,
  SHA-256
  `b7306d448d0556beff1879796c1b399ed7786fdca086d8fd9125b0832d090563`.
  Its exact-byte independent audit returned **STRICT PASS** at
  `research_notes/proof_first_single_linkage_at_most_three_species_independent_audit.md`,
  SHA-256
  `bebda68bb91bb5b22bcf4ee5d1eaf7920accde02a82210b6ffbacd9e57d6ee35`.
  Both MathJax and Tectonic renders passed.  No support, orientation,
  reaction-word, or population enumeration enters this theorem.

## 2026-08-12T08:15:00-07:00 - current stopped-service seven strict PASS

- Replayed the promoted seven-pair rank-two stopped-service theorem from its
  current bytes rather than inheriting an audit of the older claim-neutral
  snapshot.  The target/source/test/selector hashes are `e8045791...`,
  `2130fe04...`, `bcc73972...`, and `d5a5df33...`.
- The proof-first replay checked killed-carrier transience, the
  orientation-independent directed cut, exact all-clock stopping and
  almost-sure termination, actual endpoint identities, event-weighted
  service, the derivative ledger, shell branches, one common potential,
  duration, and fixed-class finite return.  No strong digraph or population
  space was enumerated; the finite replay checked only the seven-pair set.
- The exact-byte audit is frozen at
  `research_notes/rank_two_mixed_profile_7_stopped_service_current_exact_byte_audit.md`,
  SHA-256
  `658250797d819a961c8889435f1df795021c0d15d97eb90143f9bdabdbfdef98`.

## 2026-08-12T08:20:00-07:00 - corrected S-tier superlevel cut

- A hostile symbolic audit found that the legacy universal-orientation
  criterion used the absolute top D-tier and was sufficient but not
  necessary when that tier was wholly disabled.  The exact theorem uses,
  in each linkage, the D-superlevel at the deterministic level occupied by
  the global top S-tier.  Strong connectivity forces a descending top-S
  edge iff one such nonempty proper superlevel is contained in the top
  S-tier.  A Hamiltonian-cycle construction proves necessity without
  enumerating orientations.
- The correction removes 208 false failing pair--descriptor incidences.
  Exact totals are now 12,678 failures, 9,709 affine-feasible failures, and
  2,969 infeasible failures.  No pair classification changes: the
  1,219/159 tier-pass sets, 2,312/199 residual sets, exact 2,511 residual,
  and affine151 set/fingerprints are identical.
- The corrected publication dependency is
  `research_notes/s_tier_superlevel_cut_and_affine151_corrected.md`, SHA
  `d91f369d34cadfb28ddb872df8fb9f6d17799ec207da29933037f55ae95f0407`.
  Its source/test hashes are `1a4e27fc...`/`4d9f960d...`, payload
  `77c7ce0d...`; the hostile old/new disposition is frozen at audit SHA
  `62378e56b43ce205b7d3f36fe6829dc361800c991a6f1a86d3b654292f7dd354`.
  The journal citation is Anderson--Kim (2018), Theorem 9; the old arXiv
  theorem number and legacy incidence totals are retired.

## 2026-08-12T08:35:00-07:00 - four residual branches strict PASS

- Completed a consolidated proof-first exact-byte audit of the rank-one
  no-promotion 141, post-rank-one one-active 92, critical positive-shell 15,
  and exact common-factorial 26 pair theorems.  Their respective frozen
  theorem hashes are `adc325b7...`, `b4944d0b...`, `01a7827e...`, and
  `c78e53f1...`.
- Each theorem proves standalone classwise positive recurrence for arbitrary
  strong orientations and fixed positive rates.  Each also has a stronger
  pair-fixed all-clock common-potential interface; no common potential across
  different support pairs is asserted or needed.  The four pair sets are
  disjoint and their 274-pair union has fingerprint `68eb9253...`.
- The hostile audit is frozen at
  `research_notes/proof_first_141_92_15_26_current_exact_byte_audit.md`,
  SHA-256
  `d68293a3d47f8f708b604467e90fdd1801f3b3ed583d07fb53e7b9e64b987239`.
  Finite replays checked only support/profile identities; no reaction
  orientation, history, or population state space was enumerated.

## 2026-08-12T08:45:00-07:00 - final three residual row audits strict PASS

- Hostile proof replays returned strict exact-byte passes for the rank-two
  return 14, all-active reversible-top 51, and two-active promotion 36
  branches.  Their target hashes are respectively `821478a8...`,
  `3f8c3662...`, and `2f52d0ed...`; the rank-two derivative differs only by
  repaired display tags and glyph-safe notation.
- The rank-two theorem is a valid standalone nested two-workload proof, not a
  one-common-potential episode theorem.  Its proper outer workload gives
  finite-mean return to a bounded-inactive core with integrable endpoint; the
  core workload then supplies the full-clock strict drift and the cleanup
  returns to the core with finite physical-time and endpoint moments.  No
  handoff cost is omitted.
- The consolidated audit is frozen at
  `research_notes/proof_first_three_two_linkage_pair_theorems_consolidated_exact_byte_audit.md`,
  SHA-256
  `13f328883635ae832570620f3fabde0081af0358a0a5c69bcd316236f633df02`.
  Tectonic and MathJax renders passed.  No orientation, reaction history, or
  population box was enumerated.

## 2026-08-12T08:50:00-07:00 - pre-residual physical seams strict PASS

- Independently replayed the seven-support physical seam, signed-service
  seam, and unique residual-pair theorem at exact theorem hashes `d8e037a1...`,
  `4ec0ae70...`, and `dcca51ed...`.  All three pass for arbitrary strong
  orientations and positive rates at their literal support scopes.
- The signed-service theorem is intentionally nonmonotone: its Section 10
  excludes strict supersets, and the 38 such supersets cannot inherit the
  theorem by deleting or restoring clocks.  The finite pre-residual map uses
  only the displayed literal supports, so this boundary is respected.
- The hostile audit is frozen at
  `research_notes/proof_first_exact_physical_seams_independent_audit.md`,
  SHA-256
  `e7e76b76cd1371f98d19da0a1f5362ab4a0696548fba62028b29ccd2950617c9`;
  its byte manifest has SHA `d3f9ef2a...`.  No orientation, path, or
  population enumeration was used.

## 2026-08-12T08:55:00-07:00 - corrected 2,511-pair finite union frozen

- Built a publication-safe derivative that reconstructs the two-linkage
  residual directly from the corrected S-tier-superlevel cut and then checks
  the exact disjoint union of the fourteen independently audited analytic
  scopes.  The reconstructed baseline is 2,312 positive plus 199 signed
  pairs, fingerprint `0c57f530...`; all pairwise intersections are empty
  and the remainder is zero.
- The finite certificate performs support, tier, affine, and set identities
  only.  It enumerates no orientation, rate vector, reaction history,
  stochastic trajectory, or population box, and it asserts no global T3-2
  theorem.  Every analytic theorem and independent audit is byte-pinned in
  its branch manifest, including the corrected affine151 dependency.
- The canonical 2,511 ownership rows retain SHA-256 `9e9c6be4...`; the new
  payload is `efd810c7...`.  The frozen JSON file hash is `b84e6795...`.
  All five focused finite-union tests pass.

## 2026-08-12T09:10:00-07:00 - two-link composition stopped at the both-available gate

- A fresh proof-first audit found that the proposed two-link composition did
  not exhaust the raw support universe.  Across the four two-active workload
  representatives, the exact top classifier has 163,612 available/available
  incidences, 11,715 incidences in each mixed order, and 446
  shielded/shielded incidences.  The audited 4,761/408 atlas input is the
  deduplicated mixed stratum; it is not the available/available stratum.
- The hostile audit freezes the failed theorem bytes at SHA `41fbb5b2...` and
  is itself frozen at
  `research_notes/proof_first_two_linkage_at_most_three_species_hostile_audit.md`,
  SHA-256
  `69ced5b2d7ab43ab1c81ae0b312df300c995d5bf9af9744754eac9c759329328`.
  It gives five minimal full-rank deficiency-one witnesses, one in each of
  the symbolic families U--U, Q--U, C--U, C--Q, and C--C.  These are proof-
  interface witnesses, not recurrence counterexamples.
- Projection, nonexplosion, the corrected tier/affine branches, all literal
  seams, the exact 2,511-pair set union, and all fourteen standalone row
  theorems retain their strict PASS dispositions.  The global theorem and
  publication manuscript remain blocked.  The exact remaining theorem is an
  unconditioned rate-weighted current-target result for the both-available
  branch; finite support enumeration will not be used in place of that
  stochastic proof.

## 2026-08-12T09:25:00-07:00 - both-available current-target theorem strict PASS

- Proved the missing scoped stochastic theorem with the actual target of the
  previous physical reaction carried as a mark.  For
  (F(x,t)=\sum_i\log((x_i-t_i)!)), the next all-clock jump has the exact
  expected increment
  (D(x,t)=\log p_t-\sum_y p_y\log p_y-\log K_t+\sum_y p_y\log K_y), hence
  (D\le\log p_t+C).  A same-linkage simple path to a rare terminal gives
  the exact unconditioned Bellman recursion (J_i=D_i+a_iJ_{i+1}).  At the
  first vanishing source probability the negative term diverges, while the
  positive tail is multiplied by that same vanishing probability.  The
  activation/deviation jump is the terminal jump of the already-running
  episode and is never conditioned upon or double counted.
- The frozen theorem is
  `research_notes/proof_first_both_available_current_target_theorem.md`,
  SHA-256
  `157e94cd035dec9a41947129dfcbbab0ebc6e72c01abde6bcf6626052954f1ed`.
  It includes actual endpoints, every physical clock, bounded episode jump
  count, endpoint moments, uniformly integrable physical duration, the
  proper potential (W=1+F), and a negative-drift-or-positive-structural-
  exit alternative.  Its independent exact-byte audit is SHA-256
  `711e4f14f9e5de39290825de7eab2baacaf750dcee9dcaa603d36f1e6c8859ce`
  and returns STRICT PASS.
- The symbolic Q/U/C bridge is frozen separately at
  `research_notes/proof_first_quc_classifier_bridge_and_raw_trichotomy.md`,
  SHA-256
  `7b11bb57a464cfd5f7c02f07473100922e99866792dbca4d8eeab209873a148d`.
  Q and U use an active-only faster top source; C uses a top and lower
  complex sharing the bounded cofactor.  From every actual target, strong
  connectivity supplies a physical path to the lower complex, whose success
  endpoint enables the faster source and makes the lower source rare.  This
  proves the bridge analytically; the 163,612 AA / 23,430 mixed / 446 SS
  counts are finite regression identities only.

## 2026-08-12T09:35:00-07:00 - hostile entropy--Bellman replay strict PASS

- Independently replayed the exact marked factorial identity, source-weighted
  positive moments, stopped-on-first-deviation Bellman recursion, first-rare-
  source coercivity, physical path feasibility, structural-exit alternative,
  bounded episode duration, actual endpoints, common proper potential,
  nonoverlap, and marked-to-physical projection.  No stochastic search or
  orientation/history/population enumeration was used.
- The earlier C-type obstruction applies only to a rule starting from a
  disabled top source.  The repaired rule starts from the actual enabled
  target and follows a same-linkage path to a lower terminal; the success
  endpoint enables the faster comparison source.  The symbolic Q/U/C bridge
  therefore passes for Q, U, and C, including the former C--C witness.
- The exact stochastic theorem remains frozen at SHA-256 `157e94cd...`; the
  final render-fixed bridge is SHA-256 `014a3176...` (superseding the stale
  pre-render bridge hash in the preceding entry).  The hostile audit is
  `research_notes/proof_first_both_available_entropy_bellman_hostile_exact_byte_audit.md`.
  Its SHA-256 is `fd80b93f90ad0ccb3052969381c5d10453a8ec4f3fc3e67fef8a2fabed081c81`;
  MathJax and five-page Tectonic renders passed without warnings.
  Its strict pass is scoped to raw available/available two-active charts;
  mixed, shielded/shielded, other active-set charts, and global composition
  still require their separately pinned dependencies.

## 2026-08-12T09:50:00-07:00 - no-mixed one-active symbolic audit

- A proof-first token classification found no residual support-pair
  counterexample after removing every pair with a raw mixed two-active
  occurrence.  For active `X`, dormant supports are exactly the three shapes
  in (2.4) of
  `research_notes/proof_first_one_active_no_mixed_symbolic_hostile_audit.md`.
  No-mixed compatibility eliminates both single-token shapes.  The remaining
  dormant support `{0,X+U,X+V}` has exactly five compatible flat partners,
  all preserving the global signed invariant `X-U-V`.
- The exact classifier replay returned 9,489 unordered no-mixed pairs for a
  fixed active species: 6,050 Q/B, 1,406 Q/flat, 1,224 B/B, 731 B/degree-zero-
  flat, 73 flat/flat, and five dormant/degree-zero-flat.  These counts are
  regression evidence only; the token argument is the proof.
- The 731 Bellman/flat pairs expose a stochastic interface which cannot be
  covered by the scoped both-available theorem.  A finite all-clock flat-phase
  prelude must wait unconditionally for the first Bellman-linkage reaction or
  record exit/no-history, include that activation jump, and append the marked
  Bellman episode.  The degree-zero flat property makes reward, count, and
  physical duration uniform.  A terminal Green contradiction then needs no
  common potential across distinct chart alternatives, but a direct global
  Foster composition would.

## 2026-08-12T10:05:00-07:00 - one-active exhaustion and flat0 prelude proved

- Froze a standalone proof-first seam theorem in
  `research_notes/proof_first_one_active_no_mixed_exhaustion_and_flat0_prelude.md`.
  It proves the exact Q/F/B/D support alternative symbolically, eliminates
  every single-token dormant support by a seven-row two-active classifier
  table, and identifies the only five surviving dormant/flat pairs.  Each of
  those five preserves the exact common invariant `X-U-V`.
- For the 731 Bellman/degree-zero-flat support pairs, the new theorem builds a
  literal finite all-clock prelude from the bounded inactive phase.  It does
  not assume activation probability: graph reachability proves a uniform
  lower bound when activation is possible, while its failure gives physical
  exit or a closed flat-only no-history component.  Flat waiting rewards have
  bounded increments and geometric reaction-count/duration moments.
- The first Bellman-linkage reaction is included once and its actual target
  initializes the marked Bellman path.  The combined expected marked
  factorial reward tends to minus infinity, or records exit/no-history, with
  actual endpoints and every fixed positive reward and physical-duration
  moment.  No recurrence or global-composition claim is made by this seam
  theorem pending independent audit.

## 2026-08-12T10:07:06-07:00 - residual 336 all-active branch proved

- Froze the standalone analytic theorem in
  `research_notes/proof_first_all_active_residual_levelset_336_theorem.md`.
  The exact family has a rank-two linkage `T` on positive workload level
  `2s` and a linkage `R={0} union U`, where `U` consists of two or three
  unaries on level `s`.  For `H=h dot x`, every `T` reaction is neutral and
  strong connectivity of `R` forces a unary-to-zero edge.  Consequently
  `L H <= b_0-c x_i`, which tends to minus infinity on every all-active
  escaping sequence.  This is an arbitrary-orientation, arbitrary-fixed-rate
  physical-time proof, not an orientation or path enumeration.
- The finite certificate starts from all 46,872 ordered disjoint support
  pairs, removes the 27,894-pair mixed-atlas orbit, and removes only the 146
  pairs with a strictly positive proper invariant.  It deliberately retains
  the 68 additional pairs detected only by the weaker two-active invariant;
  all 68 have zero corrected affine-feasible all-active failure incidences.
  The corrected cut/affine selector and the independent level-set predicate
  are exactly the same 336 incidences on 336 pairs.
- The canonical incidence fingerprint is
  `d0c31db81db2400e0ead6e4a1a86b237fbf3b8bbb597340856a2756e9f6c884d`;
  the independent insertion-key encoding is
  `2bd4025f29d20ea4af467d46704c598652c9332ac4e32df18669cb7eb75c75a0`.
  Five dedicated tests and 35 total relevant dependency tests pass.  A
  four-page Pandoc/Tectonic render completed without warnings.

## 2026-08-12T10:31:49-07:00 - charged-seam terminal Green duality

- Froze a standalone candidate composition theorem at
  `research_notes/proof_first_terminal_chart_green_foster_duality.md`.  From
  an infinite embedded mean return it uses the killed labelled
  reaction-count Green occupation, exact finite-partition balance, a finite
  terminal circulation, and a nonoverlapping episode trace.  On one selected
  terminal component it uses only that component's potential; no
  statewise-switched potential is constructed.
- The proof isolates the necessary weighted condition
  `E[seam charge] / E[episode starts] -> 0`.  Under this condition, uniform
  local negative drift or uniformly positive exit probability, zero
  normalized exit count, and a fixed positive endpoint moment contradict
  pathwise telescoping.  Bounded episode words and uniformly geometric
  phases verify the seam condition only when the complete reentry recharge
  and initial lower-cut charge are included.
- The exact boundary formulation uses the chart-run entry subprobability
  `beta_m`: unweighted terminal flow proves only `beta_m(E) -> 0`, whereas
  the required weighted conclusion is uniform integrability of the incoming
  chart-potential values,
  `lim_R limsup_m integral_{V>R} V d beta_m = 0`.  A uniform
  `(1+gamma)` moment of the incoming values is a stronger sufficient
  condition.  This is strictly stronger than a moment bound for positive
  increments inside local episodes.
- A hostile diagnostic inside the theorem shows that unweighted terminality
  alone is false as a gluing principle.  An irreducible transient biased
  birth--death chain, divided into alternating growing blocks, has one-step
  local drift `-1/2`, every positive increment bounded by one, and normalized
  chart-exit frequency tending to zero.  Rare block changes recharge the
  alternating potentials at linear total order.  This is exactly the seam
  term excluded by the theorem.
- Candidate SHA-256 is
  `899aa11e15d3e23f629bf06cdfac3a05a47915f5a90378bb8d91982ae0ed6211`.
  A seven-page Pandoc/Tectonic render completed without warnings.  An
  independent hostile audit found the same weighted-entry obstruction and
  conditionally passed the charged-seam repair, while confirming that the
  presently frozen local chart theorems do not themselves prove the incoming
  boundary uniform-integrability condition.  The final derivative makes
  episode-start predictability explicit and requires any pre-solved branch
  in the finite-library corollary to provide classwise recurrence, rather
  than treating an arbitrary CTMC invariant law as a jump-chain invariant.
  It also uses proper block potentials in the transient obstruction, with
  values between `m` and `2m` throughout block `m`; the drift, increment,
  and linear seam-charge scalings are unchanged.  The final proof of the
  geometric-reentry estimate uses predictable conditional summation, so it
  does not make an unstated independence assumption.

## 2026-08-12T14:05:00-07:00 - anisotropic residual family closed

- Froze the support-global anisotropic theorem at
  `research_notes/proof_first_336_h112_quotient_foster_theorem.md`, SHA-256
  `9206aa2b07aa802e4d06a769b3b60d520b2dbd12752312497aa5b41156780d48`.
  It treats every residual weight permutation of `(1,1,2)` with lower
  support `{0,A,B}` and upper support `{C}` plus at least two of
  `{2A,A+B,2B}`, for arbitrary strong orientations and positive rates.
- The proof uses the one global proper marked potential
  `H + epsilon F/(H+1)`.  The exact global hazard lower bound is linear in
  `H`.  Lower marks follow an all-clock Bellman path to the rare constant
  source.  Upper marks split into a rare-source Bellman branch or a
  simultaneous-nonrare branch; in the latter the exact four-support
  geometry forces `A,B=Theta(sqrt(H))`, and one ordinary jump has workload
  service of order `H^(-1/2)`, dominating quotient and duration terms.
- A false intermediate bounded-shift factorial comparison was caught before
  freeze.  The corrected proof uses the exact total-hazard estimate
  `Lambda(w+b) <= C_b(Lambda(w)+H(w)+1)`, which is sufficient because the
  nonrare `C` endpoint already has hazard `Theta(H)`.
- Independent exact-byte audits are
  `research_notes/proof_first_336_h112_quotient_foster_derivative_exact_byte_audit.md`
  (SHA `9f0e6eebd431735526f529756a7db1c7a51cfd5409381c61dfcf84aba9ada713`)
  and
  `research_notes/proof_first_336_h112_quotient_foster_exact_byte_audit.md`
  (SHA `992448ad8b6520f014e783adb26a4f9b393b0e6a5f38c3a6262dd9b2fa0c1764`).
  Both transfer a strict mathematical PASS to the final render-only
  derivative; theorem and audits render cleanly and were visually checked.

## 2026-08-12T14:10:00-07:00 - workload-only interface certified

- Froze the conditional workload-only physical-time Foster theorem at
  `research_notes/proof_first_levelset_h_alone_physical_time_foster_lemma.md`,
  SHA-256
  `8cf2a8d41f0fab64bf34b6608fa7cf6b0f1b385a30f4a01afeb10c7732851b2a`.
  It proves that one all-clock occupation macro on the bounded
  direct-death region, combined with ordinary one-jump rules elsewhere,
  gives finite mean return under the single physical workload `H`.  It
  permits vanishing embedded-jump drift because the positive coercive term
  is physical duration.
- The exact remaining macro is only the stopped count inequality
  `s E(D-B) >= eta E(tau)`.  Stopped birth/death compensation supplies
  endpoint integrability automatically; no polynomial endpoint moments or
  switched-potential boundary estimates are required.
- Independent exact-byte audit
  `research_notes/proof_first_levelset_h_alone_physical_time_foster_lemma_exact_byte_audit.md`,
  SHA
  `9d8fc8b5e15178e7a8305422ba7fd08e6875e851c37951207815d5d84babcc67`,
  gives a strict conditional PASS after replaying the compensation,
  episode tiling, nonexplosion, and finite-set return argument.

## 2026-08-12T14:20:00-07:00 - final homogeneous catalyst seam isolated

- The only unresolved residual family is now the homogeneous
  `h=(1,1,1)` dormant common-catalyst support
  `T={X+Y,Y+Z,2Y}`.  The exact factorization is
  `L_T = Y L_lin` after subtracting the persistent catalyst.
- Hostile audit
  `research_notes/proof_first_h111_common_catalyst_macro_hostile_audit.md`,
  SHA
  `04dd05072952e71b0a010f54fb23ba9e79d13ee761f6c72a620780fdd91b9d64`,
  disproves the tempting first-death/geometric-activation shortcut: before
  top-interior entry the death compensator can grow like `log H`, and the
  whole face `Y=0` is top-dead.  A first death merely cancels the catalyst
  seed and cannot pay positive physical time.
- The sharpened constructive target is an operational-time
  ledger-or-interior block.  Label the `H-1` independent top particles;
  prescribed particle paths to `Y` give a uniform positive success
  fraction, while lower `Z->Y` transfers help and direct deaths contribute
  to the exact ledger.  Repeated all-clock blocks should yield either a
  chosen net death surplus or a compact interior endpoint with uniformly
  bounded expected birth debt, after which the audited single-linkage
  service window finishes the occupation macro.  This final block is under
  independent construction and hostile replay; no global theorem is yet
  asserted.

## 2026-08-12T21:01:33-07:00 - final T3-2 theorem and release checkpoint

- The common-catalyst block was completed for every lower-support pattern by
  a protected-label operational coupling and a net birth/death ledger.  The
  homogeneous and anisotropic level-set cases now have independently audited
  physical-time Foster theorems.
- The formerly missing outside-mixed family was closed by an exact
  11,842/6,654 split.  The first branch uses statewise population-factorial
  drift; the second uses one common actual-target marked potential, an
  unconditional two-active AA rule, and the cap-free Flat0 killed resolvent.
- The exact final two-linkage universe is the pairwise-disjoint union
  `27,462 + 432 + 146 + 336 + 18,496 = 46,872`.  The final theorem is frozen
  at SHA-256
  `dae2a58f170836427ffc053ff931c1909d64ac591d77b971591b0d5814526cde`
  and has three independent exact-byte strict-pass audits.
- The fixed-class global theorem is frozen at SHA-256
  `781d2520cbb3ad30e1749814f620d49d4c503c5c341ccd1add39a5fec31e2b7f`.
  Its projection/conjugacy, linkage routing, recurrence transport, and
  nonexplosion arguments received two independent strict-pass audits.
- The isolated read-only verifier passed all 418 tests in 553.065 seconds
  without mutating its declared scope.  This executable evidence remains
  finite-identity and regression evidence, not a substitute for the analytic
  stochastic proof.
- The publication build authenticated all 40 proof-note inputs.  The 7-page
  main article and 189-page technical supplement compile without warnings;
  contact-sheet inspection of all supplement pages and high-resolution checks
  of representative and final pages passed.
- This checkpoint supersedes all earlier present-tense statements that the
  global theorem is open.  Earlier failed interfaces and local obstructions
  remain preserved as chronological proof provenance.
