# Verification record

**Recorded (UTC):** 2026-07-25T19:47:04Z.

The all-\(d\) theorem is proved in `NOTE.md`; finite computation is not
substituted for that proof.

Two deliberately different exact checks accompany it:

1. `verify_morse_sympy.py` checks the critical-value elimination identity,
   the seed identities, and squarefreeness of a finite branch polynomial
   for each \(3\le d\le10\).  This checks the geometric mechanism.
2. `verify_specializations_pari.gp` uses PARI/GP's exact number-field
   Galois algorithm on
   \[
   X^d-X^2-3X-5
   \]
   and obtains \(S_d\) for every \(3\le d\le10\).  These arithmetic
   specializations give independent row-by-row evidence for the generic
   group.

The weighted-lift Jacobian and collision algebra is also checked by the
existing Rung 1 SymPy and PARI/GP scripts.  The current scripts extend the
monodromy table through degree ten, as required by Track B.

Run both new checks with:

```sh
./verify_strict.sh
```

The checks are exact but do not constitute peer review.  All scripts were
prepared with substantial AI assistance.
