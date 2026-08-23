# Physical standard-sector fitness-two phase certificate

This package proves strict positivity of the physical standard irreducible
sector of the stationary fitness-two complete-kernel Hessian in every
population order.

The load-bearing distinction is that the reward is built from the complete
rank Poisson gradient `d`, as required by

```text
R2(delta) = nu0 Delta G Delta G(H-c0).
```

It is not the distinct inverse-rank-weighted reward in the earlier standard
phase note.

The certified package launcher runs the exact certificate. For an individual
development invocation from this directory after preparing the pinned
environment, use

```bash
PAPER1_DEV_PYTHON=python3.14
"$PAPER1_DEV_PYTHON" verify_physical_standard_phase.py
```

The verifier uses exact rational arithmetic and symbolic polynomial
identities.  It also reconstructs the normalization

```text
R2(E(xi))/||xi||^2 = Phi_N(d) / [4 (N+1)^2 (N-1)].
```

This folder was intentionally kept independent of the Paper I package for a
separate hostile audit before integration.
