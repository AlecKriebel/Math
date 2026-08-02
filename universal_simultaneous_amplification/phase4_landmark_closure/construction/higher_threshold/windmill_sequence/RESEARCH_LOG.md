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
