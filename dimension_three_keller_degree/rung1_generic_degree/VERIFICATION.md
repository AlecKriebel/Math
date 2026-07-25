# Verification record

The universal exclusion is checked against the following mathematical
routes:

1. Campbell's 1973 complex-analytic covering/Hartogs proof of the Galois
   case.
2. Wright's 1981 characteristic-zero algebraic proof of the Galois case.
3. Trushin's 2026 contracted/branch-divisor theorem, specialized to degree
   two.
4. The short singular-locus argument reproduced in `NOTE.md`, which uses
   only normality of a polynomial ring, quasi-finiteness of an étale map, and
   the codimension of the singular locus of a reduced hypersurface.  This is
   a self-contained specialization of Trushin's mechanism, not an independent
   prior-art route.

The two scripts are deliberately narrower.  They independently check the
encoded algebra of the weighted-lift examples used for the existence half of
the spectrum theorem:

- `verify_weighted_lift_sympy.py` uses exact symbolic differentiation and
  rational simplification for \(3\le d\le8\).
- `verify_weighted_lift_pari.gp` uses PARI/GP polynomial arithmetic at
  independently selected exact points for the same range, checking the
  Jacobian and the explicit two-point collision.

Finite computation is not a proof for all \(d\).  The uniform proof is in
`NOTE.md`; these checks are regression tests for transcription and sign
errors.  Running the same algorithm in two systems would not independently
verify the theorem, so the independent proof routes above—not the scripts—are
the verification basis.

This work is not peer reviewed.  All scripts and proofs were prepared with
substantial AI assistance and require expert scrutiny.
