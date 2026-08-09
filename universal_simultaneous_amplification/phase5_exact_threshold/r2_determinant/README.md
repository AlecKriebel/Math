# Fitness-two active determinant

This branch isolates the determinant coefficient exactly equivalent to
universal dB complete-graph maximality at fitness two and distinguishes it
from the stronger stationary-promotion coefficient.

## Scope and status

The package proves the exact target/promotion implication, transfer to the
smaller subset determinant, two centered triangle forest certificates, the
full antisymmetric sector of the complete-refresh Hessian in every order,
the stationary standard and symmetric inverse-rank sectors, and explicit
obstructions to uncentered coefficient/root shortcuts.  It does **not** prove
or refute the universal active-tree sign for arbitrary order.  That sign
remains the theorem target of this branch.

Run the exact symbolic audit from this directory:

```text
../../.venv/bin/python verify_r2_determinant.py
```

The verifier reconstructs the nine-state active chain for a symbolic
weighted triangle, expands every rooted cofactor, checks the determinant
coefficient, and verifies the centered squared-difference certificate.

Run the independent subset-root-polynomial hostile audit with

```text
../../.venv/bin/python verify_root_polynomial_obstructions.py
```

It certifies failures of real-rootedness, ultra-log-concavity, ordinary
log-concavity, and direct level-tail domination.

The distinct factorial-moment route and its exact stationarity recurrence
are documented in `FACTORIAL_MOMENT_ROUTE.md`.  Replay its independent
rational screen with

```text
../../.venv/bin/python verify_factorial_moment_route.py
```

The hierarchy survives the finite corpus, but its order-one member is the
original open theorem.  The verifier also gives an exact path-graph witness
against any pointwise complete-transition proof.

The complete-refresh interpolation and its forest expansion are documented
in `COMPLETE_REFRESH_FOREST.md`.  Replay the symbolic triangle certificate
and the exact finite Bernstein screen with

```text
../../.venv/bin/python verify_complete_refresh_forest.py
```

The all-order antisymmetric proof has two independent exact checks:

```text
../../.venv/bin/python verify_antisymmetric_hessian.py
../../.venv/bin/python verify_hessian_sectors.py
```

The first verifies the rank recurrence through order 40 and against the full
active chain through order seven.  The second uses an independent stabilizer-
orbit reduction to compute all three invariant Hessian eigenvalues exactly
through order twelve.

The weaker transient-baseline route is documented in
`TRANSIENT_BASELINE_FLOOR.md`.  Its verifier proves the directed-triangle
time-three identity and exact negative packet obstructions, then replays the
finite boundary and complete-ray Bernstein screens:

```text
../../.venv/bin/python verify_transient_baseline_floor.py
```

The first open fixed-count coefficient is reduced sector by sector in
`FIXED_COUNT_TWO_REPLICA.md`.  Its independent verifier checks the full-chain
word identity, the all-time antisymmetric proof, the all-time three-vertex
and four-vertex standard certificates, and the exact finite screen of the
two unresolved rank systems:

```text
../../.venv/bin/python verify_fixed_count_two_replica.py
```

The standard sector now has a second, probabilistic reduction in
`STANDARD_PIN_VARIATION.md`.  One verifier reconstructs the distinguished-
pin line and exact convexity counterexample; another independently checks
the `3N-1` quotient, the binomial/Krawtchouk identities, and the surviving
one-crossing and positive-quotient signs.  A third performs the stronger
multinomial Schur-convexity screen:

```text
../../.venv/bin/python verify_standard_pin_bernstein.py
../../.venv/bin/python verify_standard_pin_one_crossing.py
../../.venv/bin/python verify_pin_multinomial_schur.py
```

The stronger all-order marked-cache/PGF route is exactly refuted in
`STANDARD_MARKED_CACHE_HAUSDORFF.md`.  The true stationary inverse-rank
scalar nevertheless has a complete phase-contraction proof in
`TRUE_INVERSE_RANK_PHASE_CONTRACTION.md`.  Replay its independent exact
certificate with

```text
../../.venv/bin/python verify_true_inverse_rank_phase_contraction.py
```

It reconstructs the signed two-label quotient and inverse-rank coboundary,
checks every coefficientwise rational certificate, and independently
recomputes the seven small-order Schur complements.  This closes the
stationary standard irreducible Hessian sector, not the finite-time standard
coefficient.

The companion stationary symmetric-sector theorem is in
`TRUE_INVERSE_RANK_SYMMETRIC_PHASE_CONTRACTION.md`.  Replay it with

```text
../../.venv/bin/python verify_true_inverse_rank_symmetric_phase.py
```

The verifier rebuilds the signed two-channel rank system, solves all small
orders exactly, checks every finite rational phase margin, and reconstructs
the two all-order discriminant certificates.  This closes the stationary
symmetric irreducible Hessian sector, not its finite-time fixed-count
coefficient.

The cubic and quartic optional-potential variants are now closed by exact
Farkas certificates in `CUBIC_OPTIONAL_FARKAS_REFUTATION.md`.  The independent
replay is `../../.venv/bin/python verify_cubic_optional_farkas.py`; it
checks the full labelled-to-quotient audit, the cubic and quartic dual
rays, and the strict quartic repair on the first witness.

The more flexible rank-dependent additive potential is also exactly
refuted in `RANK_DEPENDENT_ADDITIVE_FARKAS_REFUTATION.md`.  Replay
`../../.venv/bin/python verify_rank_dependent_additive_farkas.py`; it checks
the 196 exact quotient rows, reconstructs a positive 48-state Farkas ray,
and independently solves the witness graph's dB fixation system over the
rationals.  The witness is dB-suppressing at fitness two, so this result
closes only the certificate ansatz.

The global fixed-colour numerator has two exact aggregate forms in
`FIXED_COLOUR_UNICYCLE_REDUCTION.md`: a uniform row-mixture/root-response
sum and a coloured spanning-unicycle circulation.  Replay

```text
../../.venv/bin/python verify_fixed_colour_unicycle.py
```

The verifier reconstructs the active chain independently, checks the
root-vector recurrence and degree-elevated row-mixture identity, and gives
exact reversible-triangle counterexamples to both a single-row sign and a
single-unicycle sign.  Thus the surviving open certificate must cancel
simultaneously across colour locations and unicycle skeletons.

Status:

- **PROVED:** exact target/promotion implication audit;
- **PROVED:** exact active-tree coefficient for the true target;
- **PROVED:** centered positive triangle certificate;
- **PROVED:** zero constant and linear complete-refresh forest coefficients;
- **PROVED:** positive Bernstein coefficients along the complete-refresh
  interpolation for every weighted triangle;
- **PROVED:** strict positivity of the all-order antisymmetric Hessian sector;
- **PROVED:** transient baseline-floor implication and its exact
  quenched-versus-annealed formulation;
- **PROVED:** positive time-two and time-three grouped path certificates for
  every directed triangle;
- **PROVED:** every antisymmetric fixed-count two-colour packet is positive
  for all population orders and both time lags;
- **PROVED:** the complete two-colour coefficient is positive for every
  noncomplete directed three-vertex kernel and every time;
- **PROVED:** every four-vertex standard-sector fixed-lag diagonal is
  positive for every time;
- **PROVED:** exact common-pin collision and one-dimensional Bernstein
  reductions of the standard two-replica sector;
- **PROVED:** exact `3N-1` stabilizer quotient for the distinguished-pin
  pencil;
- **PROVED:** all-order determinant factorization and semisimple generalized
  spectrum of the distinguished-pin pencil;
- **PROVED:** strict positivity of the stationary standard irreducible
  inverse-rank sector in every population order, by an explicit all-reentry
  phase contraction;
- **PROVED:** strict positivity of the stationary symmetric row-zero
  inverse-rank sector in every population order, by a second explicit
  all-reentry phase contraction;
- **EXACTLY REFUTED:** pointwise convexity of the standard pin-count
  controls;
- **EXACTLY REFUTED:** the all-order marked-cache Bernstein/PGF order, by an
  exact eight-vertex, length-26 two-pin witness;
- **EXACTLY REFUTED:** universal degree-three and degree-four
  optional-potential feasibility, by sparse exact Farkas rays;
- **EXACTLY REFUTED:** the rank-dependent additive optional-potential ansatz,
  by a positive exact 48-state Farkas ray on a 17-vertex graph;
- **PROVED:** a strict degree-four optional potential on the first cubic
  counterexample;
- **EXACTLY COMPUTED:** the rank-additive witness has normalized dB fixation
  `0.8734550749036819...<1` at fitness two, by an exact 196-state solve;
- **EXACTLY COMPUTED:** first-difference and curvature one-crossing, and
  positive derivative-quotient Bernstein controls, for `3<=n<=8` and
  `2<=t<=50`;
- **EXACTLY COMPUTED:** 95,495 multinomial discrete-Schur comparisons on the
  exact finite ranges stated in `STANDARD_PIN_VARIATION.md`;
- **EXACTLY COMPUTED:** positive standard, symmetric, and antisymmetric
  Hessian sectors through order twelve;
- **EXACTLY REFUTED:** termwise transverse-excursion and two-colour-word
  positivity;
- **EXACTLY REFUTED:** monotonicity of complete-ray controls in the number
  of actual-coloured updates;
- **EXACTLY REFUTED:** raw edge-monomial coefficient positivity;
- **PROVED:** exact fixed-colour row-mixture/root-response and spanning-
  unicycle circulation identities;
- **EXACTLY REFUTED:** pointwise signs for an individual row location and
  for an individual level-two spanning-unicycle packet;
- **PROVED:** exact factorial-moment stationarity recurrence;
- **EXACTLY REFUTED:** pointwise factorial domination by a complete update;
- **OPEN:** the stationary factorial-moment hierarchy;
- **OPEN:** all-order finite-time positivity of the standard and symmetric
  Hessian sectors;
- **OPEN:** positivity of every higher complete-refresh forest coefficient;
- **OPEN:** the universal transient baseline floor and its complete-ray
  Bernstein strengthening;
- **OPEN:** the standard and symmetric all-order two-colour sector signs;
- **OPEN:** an all-order variation-diminishing or positive-quotient theorem
  for the standard common-pin pencil;
- **OPEN:** the arbitrary-order active-tree coefficient.
- **OPEN:** the aggregate all-location, all-unicycle fixed-colour sign.
