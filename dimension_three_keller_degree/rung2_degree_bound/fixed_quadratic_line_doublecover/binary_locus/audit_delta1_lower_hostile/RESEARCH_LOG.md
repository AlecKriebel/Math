# Research log — hostile audit of the exact \(\delta=1\) lower equations

## 2026-07-25

- Began an independent reconstruction of the complete \(E_6,E_5,E_4\)
  calculation in the two surviving contact families.  The candidate
  verification programs are deliberately not used as input.
- Identified a scope mismatch in the candidate note: its \(\kappa=0\)
  argument proves an automorphism exit, while the theorem headline claims
  nonexistence of Keller maps.  The stated reasoning supports exclusion of
  Keller **counterexamples**, not exclusion of all Keller maps.
- Chosen independent implementation: direct construction of the full
  weighted Jacobian determinant in PARI/GP, retaining all lower
  coefficients.  Necessity of each displayed solve will be certified by
  exact affine-linear coefficient ranks/minors, not only by substitution.

