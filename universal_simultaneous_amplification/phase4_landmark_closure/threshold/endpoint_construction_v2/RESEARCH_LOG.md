# Research log: endpoint construction v2

Started: 2026-08-08 (America/Los_Angeles)

## Scope

- Search for an actual simultaneous endpoint amplifier, prioritizing graph
  sequences with a scalable mechanism.
- Optimize the normalized minimum, never infer simultaneous amplification
  from a product or weighted mean.
- Work outside classes already excluded in the project: use vanishing or
  growing exceptional sets, noncompact weight scales, and direct portal
  networks.
- No literature search and no external contact.

## 2026-08-08: initialization

Added a direct strongly lumped solver for arbitrary equitable weighted
classes.  The solver retains only type-changing events and constructs every
Bd and dB rate from the update rules.  Floating searches remain discovery
only.

## 2026-08-08: dilute hybrid breakthrough and independent audit

- An exact two-class affine witness from the parallel separator branch
  exposed a narrow compatible cone between a dilute strong-pair defect and a
  dilute growing hub-pendant defect.
- Independently built the full positive-coupling orbit chain with state
  `(h,i,u,v,l)` and an independent rare-migration star trace.
- **EXACTLY VERIFIED:** labelled enumeration on a nine-vertex rational
  instance matches all 512 Bd and dB rows across 108 orbit fibres.
- **EXACTLY VERIFIED:** the rare trace matches the full chain as coupling
  vanishes, and the symbolic coefficients are

  `G_B=2(sigma-1)/(1+sigma(r^2-1))+lambda/(r-1)` and
  `G_D=2(r(2-r)-sigma)/(sigma+2r(r-1))-lambda`.

- **PROVED CONSTRUCTION:** optimizing the fixed algebraic constants gives a
  fitness-independent family amplifying both rules for every fixed
  `1<r<R_*`, where `R_*=1.5028569127905696...` is the unique root in
  `(3/2,1.51)` of

  `r^6-8r^5+22r^4-30r^3+21r^2-6r+1`.

- A fully rational specialization `sigma=19/137`, `lambda=20/27` already
  proves a threshold `1.50176815223369...`; its endpoint margins are exactly
  `232/17361` and `65/12123`.
- The construction proof, full post-establishment trace, explicit diagonal,
  and exact class optimization are recorded in
  `HYBRID_CONSTRUCTION_AUDIT.md`.
