# Heterogeneous-windmill sequence log

All times are America/Los_Angeles.  No literature search or external contact
was used.

## 2026-08-02 — strong-pair trace and scalable sequence

- Derived the leading strong-pair hazards under dB and a rigorous Bd
  first-handoff upper bound.  Literal trace claims for the center/blade table
  were retracted during hostile audit because order-one center updates can
  overlap pair resolution; the exact fast-center blade reduction survives.
- In the fast-center dB limit, identified the blade process as a rank-one
  biased voter chain with effective fitness `R=r^3`.
- Proved the booster lemma: a parent-dominant, still-faster target site squares
  the effective fitness of the older blade process.
- Constructed a diagonal family with `N-floor(sqrt(N))` ordinary blades and
  `floor(sqrt(N))` boosters.  Ordinary-blade fixation tends one, yielding
  uniform dB fixation `1/2` for every fixed `r>1` and the exact interval
  `(1,2)` for dB amplification.
- Proved that the same hierarchy has Bd fixation tending zero through the
  first center-seeding odds.
- Proved that dynamically negligible support completion leaves collision
  tending one, and that growing clique blades are dB-suppressing.
- General growing diffuse non-clique blades remain open.

## 2026-08-02 — final hostile audit

- Corrected the dB labeling: the displayed center/blade table is a leading
  hazard generator, not the literal trace, because pair resolution can
  overlap a center death.  Derived the exact blade chain directly after
  fast-center averaging; the `R=r^3` reduction is unchanged.
- Proved the population `limsup<=1/2` with an explicit entrance-law bound
  `h_i<=r p_i/4`, rather than assuming independent local resolution.
- Replaced the informal diagonal choice by a canonical integer hierarchy and
  rational `eta=1/H` first-passing enumeration, with exact Sturm-decidable
  tests on a moving rational interval.
- Made the quantifiers uniform on
  `[1+1/N,floor(sqrt(N))]`; this interval eventually contains every fixed
  `r>1`, while all displayed upper and lower errors vanish uniformly.

## 2026-08-02 — reversed ordinary scale falsified

- Tested the proposed regime with density-one ordinary blades satisfying
  `lambda_i/p_i -> infinity` and tiny total parent mass.
- Derived an exact two-state dB stopping chain that includes all overlapping
  center/pair events.  From a singleton ordinary mutant, fixation is at most
  `3r(r+1)p_i/lambda_i`.
- Therefore the density-one ordinary contribution tends zero and the
  exceptional boosters have vanishing initial mass.  The full uniformly
  initialized dB fixation tends zero before any post-seeding sweep can help.

## 2026-08-02 — balanced handoff window and guard-block no-go

- Derived the exact balanced-ratio singleton handoff limits
  `2r^2 c/[1+2r(r+1)c]` for Bd and `r^2/[2(r^2+c)]` for dB.
- Comparison with the infinite complete baseline gives the necessary window
  `(r-1)/(2r) < c < r^2(2-r)/(2(r-1))`.
- Solved its closing equation exactly:
  `r_hand=(1+sqrt(2)+sqrt(2sqrt(2)-1))/2=1.8832035...`.
- Proved that any strong-pair mesoscopic post-seed block faces an exact
  contradiction: dB fixation tending one requires total ratio mass
  `sum lambda -> infinity`, while Bd requires `sum lambda -> 0`.

## 2026-08-02 — growing-clique guard falsified

- Derived from the clique count chain the exact forward and reverse
  establishment probabilities for both update rules.
- Derived the center-to-module, module-to-center, and reverse module hazards
  for weakly center-coupled clique modules.
- Although reverse establishment is exponentially small after a clique is
  mutant, the initial race is fatal: dB requires aggregate coupling
  `sum s_j theta_j -> infinity`, whereas Bd center persistence requires the
  same aggregate to tend zero.
- The proof grants success at the first mutant copy, so overlapping
  introductions and all post-establishment persistence only strengthen the
  no-go.
