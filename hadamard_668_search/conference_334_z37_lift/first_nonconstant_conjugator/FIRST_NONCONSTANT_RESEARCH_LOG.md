# First-nonconstant conjugator research log

## 2026-07-25 PDT

- Replaced the ambiguous `A0+y*A1` ansatz by the exact unitary logarithm
  normal form in `z=log(1+y)`:
  `K=z*A0+z^2*A1+...`, with alternating symmetric/skew coefficients.
- Verified over `F_37` that the first two fixed-trace orbit layers have
  dimensions 20 and 20.  The second-layer diagonal image has rank eight.
- Classified the pure rank-two skew leading coefficient into its four
  rational types and found only the Paley weight-18 pair in every safe
  diagonal function overcode.  This excludes `K=z^2*B`, `rank(B)=2`,
  across the complete quotient census.
- Parameterized a common nondegenerate two-plane pencil by
  `(t,alpha,beta)`, with decimation action
  `(t,alpha,beta)->(q*t,q^2*alpha,q^4*beta)`.
- Exhausted 76 trace-zero decimation orbits and 1,332 normalized nonzero
  scalar-gap types.  The loose entry-product code left two exceptional
  types.  Quotient profiles reduced these to `(1,19,20)` and classes
  `107,110,222,223`.
- An initial symmetry reduction incorrectly used `c+c'` for the linear
  skew term and appeared to remove both exceptions.  An independent
  direct polynomial-matrix expansion caught the error before promotion:
  for symmetric `M` and skew `B`,
  `diag(MB)=-diag(BM)`, so the correct coefficient is `c'-c`.
  The verifier and note were corrected, and the exceptions returned.
- Restored the fixed `z^18*J` contribution.  For the exceptional type,
  the ordinary and half-power function spaces form a direct `7+7` sum.
  The local `J` coefficients are forced to
  `(1,p,s,b,p^2,p*s,b*p,s^2,b*s,-b^2)`.
- Exhausted all `37^3=50,653` relaxed local triples for each of
  `eta=+1,-1`.  None matches any of the four exceptional binary words.
  This closes the entire common nondegenerate two-plane first-nonconstant
  family.
- Peak memory in the final C++ census was approximately 5 MB; runtime was
  under five seconds.  The independent quotient replay remained the
  largest check at approximately 59 MB and 46 seconds.
- No tracked files were edited, no commit or push was made, and no
  external communication occurred.
