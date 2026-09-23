# Verification companions

The theorem is proved analytically in the paper. These small scripts make
some algebra and boundary behavior independently reproducible. **They do
not prove the complete theorem, its assertions for every dimension, the
curve-length argument, or continuity of the deformation on a mapping space.**
No computer calculation is needed to accept the paper's proof.

Run from this directory with Python 3.9 or later:

```sh
python3 verify_exact.py
python3 verify_numeric.py
```

Both scripts write JSON results next to themselves and exit nonzero on a
failed check. Supply `--output /path/to/results.json` to choose another
destination. Result timestamps and platform/version information vary across
runs; the inputs and seed are fixed.

## Exact checks (standard library only)

`verify_exact.py` expands polynomials with rational coefficients in a
central scalar `t` and **ordered, noncommuting** matrix letters. It checks
the numerator identity for the difference of two Möbius transforms, the
unitarity and resolvent Gram expansions, and the commutation of two
polynomials in the *same* matrix. A sanity check ensures that `UV - VU`
does not vanish in the formal algebra. Upper/lowercase letters denote a
unitary and its adjoint, so adjacent inverse pairs may cancel.

The check does not assert invertibility or positive semidefiniteness:
these are analytic steps in the proof. It also calculates exactly that
outside the semicircle, at `W = -1` and `t = 1/2`, the angular derivative
is `3`, exceeding both `1` and the proposed factor `q = 3/5`; the
denominator at `W = -1, t = 1` is zero. Thus the domain assumption matters.

## Optional numerical checks (NumPy)

`verify_numeric.py` requires NumPy; the recorded run uses the version shown
in `results_numeric.json`. It uses a fixed seed and 101 pairs in dimensions
1, 2, 3, 5, and 8. It includes the explicitly noncommuting boundary pair
`U = i diag(1,-1)` and `V = i [[0,1],[1,0]]`, along with generated matrices
whose eigenangles lie in the closed right semicircle. It checks:

- Unitarity, endpoints, fixed identity, and inverse-norm bounds.
- The ordered difference identity and its Hilbert–Schmidt and operator
  norm bounds, with times including `0` and `1`.
- The differential identity, obtained independently by the product rule,
  and the two corresponding tangent-norm bounds.
- Expansion and an endpoint singularity for inputs outside the semicircle.

These are ordinary floating-point checks with a tolerance documented in
the JSON, **not interval-certified bounds**. Numerical success provides
regression evidence only; the exact algebra and the written analytic
proof carry the mathematical claims. The numerical scripts do not replace
an intrinsic unitary distance with a chordal distance: their finite
difference check is explicitly chordal, and their differential check is
the local quantity used in the paper's length argument.
