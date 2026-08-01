# Post-solution narrow priority audit

## Scope and timing

This audit was begun only after the exact construction, proof, and standalone
verifier were complete and passing on 2026-08-01.  None of the sources below
was used in discovery or in proving the construction.  The search was narrow:
primary sources directly concerning weakly reversible systems with infinitely
many positive steady states, common-factor mechanisms, and the recent generic
geometry of steady-state varieties.  It was not an exhaustive citation or
historical survey.

## Direct published question

Boros, Craciun, and Yu constructed weakly reversible mass-action systems with
continua of positive steady states, including a reversible system with one
connected component.  Their continua are produced by a polynomial that is a
common factor of all coordinate equations.  In Section 5 they asked:

> Can a weakly reversible mass-action system have infinitely many positive
> steady states without having a common factor on the right-hand side of its
> differential equations?

The present construction gives an affirmative answer: it is reversible and
one-linkage, its only positive compatibility class contains a conic of steady
states, and its coordinate gcd is \(1\).

Primary source: B. Boros, G. Craciun, and P. Y. Yu, “Weakly Reversible
Mass-Action Systems With Infinitely Many Positive Steady States,” *SIAM
Journal on Applied Mathematics* 80 (2020), 1936–1946,
[DOI](https://doi.org/10.1137/19M1303034),
[public preprint](https://arxiv.org/abs/1912.10302).  The question occurs in
Section 5, PDF page 8; the paper also states that all of its examples use a
common factor.

## Closest later work checked

- N. Kazi Obatake and E. Walker, “Newton-Okounkov Bodies of Chemical Reaction
  Systems,” *Advances in Applied Mathematics* 155 (2024), 102672,
  [DOI](https://doi.org/10.1016/j.aam.2024.102672),
  [public preprint](https://arxiv.org/abs/2203.03840).  Example 5.4 revisits a
  Boros–Craciun–Yu system and explicitly identifies its curve as arising from
  a common factor.  It gives no common-factor-free replacement.

- S. Kothari and A. Deshpande, “Endotactic and Strongly Endotactic Networks
  With Infinitely Many Positive Steady States,” *Journal of Mathematical
  Chemistry* 62 (2024), 1454–1478,
  [DOI](https://doi.org/10.1007/s10910-024-01617-5),
  [public preprint](https://arxiv.org/abs/2303.08781).  Their examples are not
  weakly reversible, and their continua again come from a scalar polynomial
  common to the coordinate equations.

- E. Feliu, O. Henriksson, and B. Pascual-Escudero, “The Generic Geometry of
  Steady State Varieties,” *SIAM Journal on Applied Algebra and Geometry* 10
  (2026), 519–548, [DOI](https://doi.org/10.1137/25M1731289),
  [public preprint](https://arxiv.org/abs/2412.17798).  Example 3.12 describes
  the Boros–Craciun–Yu rates as fine-tuned to give a common factor.  Its generic
  finiteness results answer the separate open-set-of-rate-constants question;
  they allow exceptional parameter choices such as the exact integer rates in
  the present construction and do not resolve the no-common-factor question.

- M. Banaji and E. Feliu, “Positive Equilibria in Mass Action Networks:
  Geometry and Bounds,” [arXiv:2409.06877, v4 (2026)](https://arxiv.org/abs/2409.06877),
  gives general geometric alternatives that can include continua of
  degenerate equilibria.  It neither constructs the present weakly reversible
  case nor studies the coordinate-gcd condition.

- M. Pérez Millán, A. Dickenstein, A. Shiu, and C. Conradi, “Chemical Reaction
  Systems With Toric Steady States,” *Bulletin of Mathematical Biology* 74
  (2012), 1027–1065,
  [public preprint](https://arxiv.org/abs/1102.1590), is relevant algebraic
  background for positive-dimensional binomial steady-state varieties.  It
  does not give a continuum inside one positive compatibility class with the
  full-rank, weakly reversible, gcd-one properties required here.

## Conservative conclusion

No audited primary source supplied a weakly reversible system—much less a
three-species reversible, one-linkage, full-rank system—whose continuum in one
positive compatibility class is a height-two component while the coordinate
gcd is \(1\).  The construction therefore directly answers the explicit 2020
question and, to the extent of this targeted audit through 2026-08-01, appears
to be the first explicit example.  This is deliberately not asserted as an
exhaustive universal priority claim, and no global minimality in complexes or
reactions is claimed.
