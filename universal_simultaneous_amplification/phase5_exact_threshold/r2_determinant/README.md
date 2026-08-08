# Fitness-two active determinant

This branch isolates the determinant coefficient exactly equivalent to
universal dB complete-graph maximality at fitness two and distinguishes it
from the stronger stationary-promotion coefficient.

## Scope and status

The package proves the exact target/promotion implication, transfer to the
smaller subset determinant, two centered triangle forest certificates, the
full antisymmetric sector of the complete-refresh Hessian in every order,
and explicit obstructions to uncentered coefficient/root shortcuts.  It does
**not** prove or refute the universal active-tree sign for arbitrary order.
That sign remains the theorem target of this branch.

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
one-crossing and positive-quotient signs:

```text
../../.venv/bin/python verify_standard_pin_bernstein.py
../../.venv/bin/python verify_standard_pin_one_crossing.py
```

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
- **EXACTLY REFUTED:** pointwise convexity of the standard pin-count
  controls;
- **EXACTLY COMPUTED:** first-difference and curvature one-crossing, and
  positive derivative-quotient Bernstein controls, for `3<=n<=8` and
  `2<=t<=50`;
- **EXACTLY COMPUTED:** positive standard, symmetric, and antisymmetric
  Hessian sectors through order twelve;
- **EXACTLY REFUTED:** termwise transverse-excursion and two-colour-word
  positivity;
- **EXACTLY REFUTED:** monotonicity of complete-ray controls in the number
  of actual-coloured updates;
- **EXACTLY REFUTED:** raw edge-monomial coefficient positivity;
- **PROVED:** exact factorial-moment stationarity recurrence;
- **EXACTLY REFUTED:** pointwise factorial domination by a complete update;
- **OPEN:** the stationary factorial-moment hierarchy;
- **OPEN:** all-order positivity of the standard and symmetric Hessian
  sectors;
- **OPEN:** positivity of every higher complete-refresh forest coefficient;
- **OPEN:** the universal transient baseline floor and its complete-ray
  Bernstein strengthening;
- **OPEN:** the standard and symmetric all-order two-colour sector signs;
- **OPEN:** an all-order variation-diminishing or positive-quotient theorem
  for the standard common-pin pencil;
- **OPEN:** the arbitrary-order active-tree coefficient.
