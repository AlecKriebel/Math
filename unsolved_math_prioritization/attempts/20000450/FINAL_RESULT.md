# Full torsion computation: pentagonal quintic

**20000450 / AIM-ALGEBRAIC_NUMBER_THEORY-0102. Complete candidate, 1/5 substantive author turns, independent review pending.**

For the explicitly normalized regular-pentagon pencil in TURN_1.md over K=Q(sqrt(5)), set phi=(1+sqrt(5))/2. Every finite parameter except 0, -5sqrt(5), -phi^5 has an elliptic normalization. With origin [0:1:0], its full 5-division field is

K(sqrt(5+2sqrt(5)), zeta_5, (lambda+phi^5)^(1/5)).

An explicit cubic model and birational plane maps are given in equations (9)–(12). The precise modular parameter is beta=(11-5sqrt(5))lambda/[2(lambda+5sqrt(5))], and equation (17) is an actual isomorphism to the quadratic twist of Tate normal form. Equations (19)–(22) give every geometric 5-torsion point, including the twenty omitted by the prior infinity-line computation. Sections 6–7 supply the extension data, specialization criterion and Galois representation.

For lambda in K, the division field has degree four exactly when lambda+phi^5 is a fifth power in K; otherwise its degree is twenty with Galois group D10 times C2. Generically it has degree twenty. There is no nonzero K-rational 5-torsion, and the torsion over the real quadratic extension K(sqrt(5+2sqrt(5))) is exactly the infinity subgroup.

The source's equation did not specify a ground field, origin or scaling. This answer states each convention and computes the regular pencil. It does not manufacture a nontrivial Tate–Shafarevich class from a curve having a rational origin, or answer separate nonregular-pentagon variants. A plane fiber with cusps may still have smooth elliptic normalization; the proof checks this distinction rather than inheriting an unnecessary ordinary-node restriction.

The imported July 2026 partial report is credited for its infinity-line and conic reductions, which are independently checked. Fisher's classical Tate and full-level X(5) maps are the essential primary-theory input. The candidate's contribution is their explicit identification with this fixed plane pencil and the resulting complete computation. Historical novelty is not established.

The verifier passes 88,918 exact assertions, combining symbolic identities with 388 separately labeled finite-field fibers, including 30,012 enumerated affine points. These controls supplement the written universal proof and primary-theory dependency. Final status remains pending independent source and proof review.
