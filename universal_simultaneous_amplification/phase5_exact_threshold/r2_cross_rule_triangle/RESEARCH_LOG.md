# Research log: fitness-two cross-rule triangle

## 2026-08-13 -- exact all-weight `PAPT_3`

- Derived both six-state fitness-two fixation probabilities symbolically for
  conductances `(a,b,c)`.
- Compressed the degree-twelve Bd and degree-six dB numerator/denominator
  polynomials into monomial-symmetric tables with positive coefficients.
- Cleared the complete product baseline `16/63`; the primitive numerator is
  the degree-eighteen polynomial `2 Q_B Q_D-7 N_B N_D`.
- Found and exactly verified a 24-term positive decomposition into
  `sum_perm x^i y^j z^k (x-y)^2`.  The certificate proves strictness away
  from the equal positive triangle and remains strict on every path
  boundary.
- Interpreted each atom as a wedge-exchange circuit.  A subsequent exact
  order-four Hessian audit refuted the initially proposed one-orbit
  covariant wedge-square extension: adjacent and disjoint edge pairs must
  both be retained.  See the complete-ray companion package.
- The existing two-deletion identity does not prove that target packetwise:
  contracted `L` and `D` completions are not one common undirected triangle,
  and an exact three-component packet is negative.  Global sibling grouping
  remains necessary.
- Best-guess completion: **100% for `PAPT_3`** and **25% for identifying the
  algebraic form of a possible all-order induction**.  The surviving form
  is fixed-colour paired-forest positivity; the all-order sign remains open.
