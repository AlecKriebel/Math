# Verification record

**Recorded (UTC):** 2026-07-25T19:47:04Z.

The family-wide theorem is proved in `NOTE.md` by combining Gallagher's
general weighted-lift identities, exact rational recovery, and Brink's
Theorem 13.  Finite computation is not substituted for that proof.

Three exact checks accompany it:

1. `verify_general_seed_sympy.py` leaves all unconstrained seed coefficients
   symbolic and checks the endpoint, integral, divisibility, elimination, and
   recovery identities for generic degrees \(3\) through \(10\).
2. `verify_morse_sympy.py` checks the critical-value elimination identity,
   the seed identities, and squarefreeness of a finite branch polynomial
   for each \(3\le d\le10\).  This checks the geometric mechanism.
3. `verify_specializations_pari.gp` uses PARI/GP's exact number-field
   Galois algorithm on
   \[
   X^d-X^2-3X-5
   \]
   and obtains \(S_d\) for every \(3\le d\le10\).  These are arithmetic
   consistency checks only: an arithmetic specialization does not by
   itself distinguish geometric \(S_d\) from a possible geometric
   \(A_d\).

The hostile audit independently reconstructed the function fields and
branch cycles.  Its separate PARI resultant check certifies that at
\(U=1\) the finite branch polynomial has degree \(d-1\) and is squarefree
for \(3\le d\le20\).  Together with the classical Morse-polynomial theorem,
this is independent exact evidence for the geometric mechanism.

The weighted-lift Jacobian and collision algebra is also checked by the
existing Rung 1 SymPy and PARI/GP scripts.  The current scripts extend the
monodromy table through degree ten, as required by Track B.

Run both new checks with:

```sh
./verify_strict.sh
```

The checks are exact but do not constitute peer review.  All scripts were
prepared with substantial AI assistance.
