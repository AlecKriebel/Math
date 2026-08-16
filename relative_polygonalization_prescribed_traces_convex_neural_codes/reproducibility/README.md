# Reproducibility package

This package performs deterministic, no-network checks for the finite exact
examples accompanying **Relative Polygonalization with Prescribed Traces for
Convex Neural Codes**.

It verifies:

1. generic crossing traces;
2. tangent closed-point contacts;
3. supporting closed-segment contacts;
4. half-open traces produced by ambient clipping;
5. simultaneous endpoints;
6. a lower-dimensional atom;
7. a covered relative carrier;
8. two face models with an identical shared-edge trace;
9. four tetrahedral face models with all six shared-edge traces.

The verifier uses exact rational arithmetic and exact Fourier--Motzkin
elimination for strict and weak affine systems. The examples test the
bookkeeping and boundary conventions. They do **not** prove the general
inclusion-minimal polygonalization theorem.

Run:

```bash
./replay.sh
```

The replay also compiles the manuscript, arXiv source, and two-page summary
from fresh temporary copies, checks the page counts and vector-figure count,
and validates this directory's manifest.
