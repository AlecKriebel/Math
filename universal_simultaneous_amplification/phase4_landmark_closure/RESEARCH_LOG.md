# Research log

## 2026-08-01 21:08 PDT — landmark-closure program initialized

- Froze Paper I and inherited its fixed-graph obstruction, directed
  sum-of-squares coefficient, support-degree condition, and phase-three
  excluded regimes without rederivation.
- Opened independent obstruction, construction, and threshold tracks.
- Prioritized a universal Bd--dB heterogeneity tradeoff and, in parallel,
  dense asymptotically regular or mesoscopic candidates whose leading dB
  behavior ties the well-mixed limit but whose lower-order correction is
  positive.
- Imposed the discovery literature embargo and exact claim-status vocabulary.
- Recorded the independent-research policy: publication artifacts are in
  scope after a qualifying theorem; specialist outreach materials and contact
  are not.
- Best-guess completion toward Alternative U, Alternative O, exact `R_sim`, or
  the required two-sided threshold advance: **3%**. The publication phase is
  **0%** because no qualifying new theorem has yet been proved.

## 2026-08-01 22:14 PDT — first construction and tradeoff checkpoint

- Derived the exact singleton-changing probabilities in terms of the
  row-normalized kernel `P`: a mutant at `i` reaches two mutants before
  extinction with probability `r/(r+t_i)` under Bd, where
  `t_i=sum_j P_ji`, and with probability `lambda_i/(1+lambda_i)` under dB,
  where `lambda_i=sum_j r P_ji/(1+(r-1)P_ji)`.
- [EXACTLY COMPUTED] Corrected quotient-chain scans of weighted windmills,
  clique blades of sizes two through four, asymmetric two-vertex blades,
  matched clique--pendant coronas, and two weakly coupled cliques found no
  simultaneous amplification in the tested parameter grids. These are
  falsification data, not asymptotic theorems.
- [EXACTLY COMPUTED] The matched clique--pendant corona amplifies Bd and
  suppresses dB throughout the completed grid; both deviations shrink toward
  zero as the matching weight grows.
- Found a discovery-code defect in the inherited windmill scanner: the Bd
  loss rate from a mixed blade is divided by total fitness twice. The Phase-3
  analytic statements do not cite that scan as a proof. A phase-4 verifier
  must not reuse the faulty expression.
- [PROVED, obstruction track] A dominating multitype branching process gives
  an explicit universal dB upper bound of well-mixed limit plus
  `O_r(log(n)/n)`. This is quantitatively new but is not yet a fixed-fitness
  obstruction because the complete dB baseline lies `Theta(1/n)` below its
  limit.
- [FORMAL ASYMPTOTIC, proof package in progress] Near a doubly stochastic
  kernel, the second-order Bd branching gain is at most `1/r` times the dB
  branching loss. The statement currently concerns establishment rather than
  full finite-population fixation and therefore does not change the mission
  status.
- The surviving issue is now sharply localized: either exploit the
  finite-population `1/n` correction to build a family, or control it strongly
  enough to turn the establishment tradeoff into a universal obstruction.
- Best-guess completion toward a mission-qualifying theorem: **14%**.
  Publication remains **0%** pending such a theorem.

## 2026-08-01 22:40 PDT — independently audited `3/2` lower theorem

- [PROVED] Constructed an explicit fitness-independent rational family with
  `N` center vertices and `N^2` singular weighted triangles.  The triangle
  weights are `1,N^-4,N^-4`, center-clique edges have weight `N^-3`, and
  every center--triangle edge has weight `N^(-N^3)`.
- [PROVED] For every fixed `r>1`, both Bd and dB uniform-initialization
  fixation probabilities converge to `1/3`.  Since both complete-graph
  baselines converge to `1-1/r`, the family strictly amplifies both rules for
  every fixed `1<r<3/2` eventually.  This improves the inherited lower bound
  from `6/5` to `3/2`.
- The proof combines exact six-transient-state triangle formulas, exact
  center-clique formulas, a quantitative rare-edge trace coupling, and
  forward/reversal bounds through all `N^2` module conversions.
- An independent hostile audit rebuilt every module and macro rate from the
  update definitions, checked the scale window, found two local presentation
  issues, and verified their repairs.  Five exact certificate suites now pass,
  including full-chain aggregation for both rules.
- [PROVED] At the endpoint `r=3/2`, this family is suppressing under both
  rules.  Its graph-minus-complete differences are
  `-4/(3N^2)+o(N^-2)` for Bd and `-16/(81N^2)+o(N^-2)` for dB.  An independent
  audit verified all endpoint constants and that every trace, excursion-tail,
  and center-reversal error is `o(N^-2)`.  Thus `(1,3/2)` is the exact
  asymptotic fixed-fitness interval of this family.
- [OPEN] A universal upper bound and Alternatives U/O remain unresolved.  The
  obstruction track is testing sharp fixed-fitness inequalities at and above
  `3/2`; none is yet a theorem.
- Best-guess completion toward one of the user's full landmark outcomes:
  **42%**.  Mathematical packaging of the proved lower theorem is **20%**;
  public-preprint work remains deferred while the exact-threshold obstruction
  is still under active attack.

## 2026-08-01 22:55 PDT — genealogy obstruction retracted

- [RETRACTED] The claimed universal bound
  `limsup rho_dB(G_n,r)<=1-1/r` contradicts the independently audited
  center--triangle theorem when `1<r<3/2`, where the left side is `1/3`.
- The invalid step is the asserted coupling of the replacement genealogy to
  an independent linear branching process.  A reproduction by one lineage is
  the same event as another lineage's death.  Marginal predictable-intensity
  bounds do not permit both clocks to be embedded as independent branching
  clocks.  Once one ancestry fills an internally closed module, every death
  is paired with a descendant birth, illustrating exactly why the proposed
  branching tree may die while the actual ancestry cannot.
- Exact singleton identities, the weight-concentration and temperature
  necessities, the abstract branching fixed-point algebra, and the statewise
  cut inequality are unaffected.  They no longer imply a fixation bound.
- The construction theorem and `R_sim>=3/2` remain proved.  The false
  obstruction will not be pushed or used in the paper.

## 2026-08-02 01:22 PDT — exact-duality and boundary checkpoint

- [PROVED] Derived exact branching--coalescing set duals for both rules.
  The Bd dual uses neutral copying and selective OR arrows; the dB dual
  replaces an occupied test vertex by the union of a geometric number of
  neighbor samples.  Uniform-singleton fixation equals stationary dual
  density, while fixation at reciprocal fitness equals stationary singleton
  mass for either rule.  Two independently implemented exact-rational
  verifiers reconstruct the forward and dual chains and check the identities.
- [PROVED / EXACTLY COMPUTED] The complete graph fails to maximize dB
  fixation at `r=3/2`, `7/4`, and `9/5`.  Exact 7-, 9-, and 11-vertex
  weighted windmills certify the three strict counterexamples.  Thus a
  dB-only obstruction below `2` is unavailable by this route.
- [PROVED DIAGNOSTIC] At `r=3/2`, the complete graph strictly maximizes
  `rho_Bd+rho_dB` among positive weighted triangles unless all three weights
  agree.  The numerator is certified by 24 positive squared-difference
  atoms.  The corresponding arbitrary-graph sum inequality remains OPEN.
- [PROVED FAMILY-SPECIFIC NO-GO] A natural separated four-vertex module has
  a dB establishment interval extending to `1.543689...`, but its exact Bd
  and dB center-load windows are disjoint by
  `-(r-1)^2(r^2+1)<0`.  A separate weighted triangle has a root favorable to
  both rules at `31/20`, but no verified handoff retains that local gain under
  uniform initialization.
- [OPEN] The leading closure targets are now a universal dB maximization
  theorem at `r=2`, the cross-rule sum inequality at `r=3/2`, or a
  construction whose interval exceeds `3/2`.  Landmark-closure completion is
  estimated at **52%**; publication packaging remains deferred until one of
  the requested full outcomes is proved.

## 2026-08-02 06:22 PDT — exact `1/n` modular tradeoffs

- [PROVED] For any separated collection of weakly coupled complete modules
  on an arbitrary connected weighted macrograph, both fixation excesses have
  the exact form `n*Delta_U/(1-1/r)=E_U-L_U`: an additive local finite-size
  budget minus a nonnegative global macro-failure charge.
- [PROVED] If every module size diverges, each additional module contributes
  one negative dB unit.  For `q_n` modules this gives dB deficit
  `(1-1/r)(q_n-1-o(q_n))/n`, regardless of module proportions, degree scales,
  or macrograph.
- [PROVED] In a separated star with one growing complete core and arbitrarily
  many heterogeneous `o(core)` complete satellites, actual dB amplification
  forces a Bd deficit of order `q_n/n` for every fixed `r>sqrt(2)`.  The
  scalar certificate is uniform over satellite sizes and scales, and
  `sqrt(2)` is its exact coefficient-one threshold.
- [PROVED ROUTE FALSIFICATION] A two-dense-clique family with a superweak cut
  has complete support, normalized collision `O(1/n)`, temperatures tending
  uniformly to one, and asymptotically saturates the inherited `r^3` cut
  product, yet its fixation-sum deficit is only order `1/n`.  Local
  diffuseness, temperature regularity, and the sharp cut product therefore
  cannot yield a constant obstruction without a finite-size stability term.
- [OPEN] These are class theorems, not a reduction from arbitrary graphs.
  The exact complete-graph sum bound at `r=3/2`, the dB stationary
  half-density/finite-size inequality at `r=2`, and any construction above
  `3/2` remain open.  Landmark-closure completion is estimated at **59%**;
  publication remains deferred pending a mission-level theorem.
