# Research log: characteristic-two profile quotient

## 2026-07-24 14:03 PDT

- Derived the characteristic-two necessary quotient
  `F_4[C_37]^H ~= F_4 x F_(4^6) x F_(4^6)` for the order-three
  `LP(333)` profile equation.
- Proved the semilinear star formula
  `(a,X,Y)^*=(a^2,Y^32,X^128)` and the resulting single nontrivial norm
  equation.
- Completed the exhaustive `2^24`-word channel census for all five reduced
  aggregate types and all three dense shells.  Every one of the fifteen
  cells survives; the measured reduction is approximately `2^11`.
- Added an assignment-level verifier for use by the dense classifier.
- Independent audit confirmed the factorization, trace dependency, and all
  fifteen census values.  It also found that the first API version checked
  only the six nonzero-lag conditions when optional shell/aggregate pins
  were omitted.  The API now checks the zero-lag and trivial-character
  factors unconditionally, with the auditor's counterexample retained as a
  regression test.
- This is a sieve and algebraic localization result, not a Legendre pair or
  an `H(668)` construction.  No external priority claim has been made.
