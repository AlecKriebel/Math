# Replay instructions

Run with Python 3, SymPy, and mpmath:

    python verification/verify_exact.py

The script writes `verification/results.json`. The frozen run used SymPy 1.14.0,
mpmath 1.3.0, and 90 decimal digits for the supplementary numerical part.

There are 37 exact symbolic/rational assertions, five finite numerical replays,
and six negative controls. The exact assertions establish the displayed
coefficient identities, rational 2×2 matrix relations, finite standardness
checks, four-coordinate rotation, strict off-diagonal sign, scalar endpoint
limit, and fixed-gap integral. The Fourier proof for arbitrary Schwartz tests
and every spatial dimension is analytical in Attempt 2; finite symbolic
dimension checks supplement it rather than replace its proof.

The high-precision numerical tests compare an explicit closed matrix formula
with eigendecomposition at four scalar shifts and replay the Fréchet derivative
at one shift. These decimal tests are not interval arithmetic and are not the
proof of the finite examples. Exact formulas provide that proof.

Negative controls drop the Yukawa residual in dimensions 1–5 and omit the
exterior-factor contribution to the mass derivative. Each defective expression
is detected. No continuum convergence, spectral-gap estimate for the field,
or nonzero continuum off-diagonal matrix element is certified.

