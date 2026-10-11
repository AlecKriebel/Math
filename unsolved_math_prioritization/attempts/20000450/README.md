# Full 5-torsion of the normalized pentagonal quintic

**20000450 / AIM-ALGEBRAIC_NUMBER_THEORY-0102: claimed_solved, 1/5 substantive author turns. Independent full source and proof review: PASS.**

For the regular-pentagon pencil, this packet gives an explicit Weierstrass model, all twenty-five geometric 5-torsion points, its exact division field and Galois action. Classical Tate, division-polynomial and full-level modular machinery is credited; historical novelty is unestablished.

## Field, scaling and elliptic locus

Write r=sqrt(5), K=Q(r), phi=(1+r)/2. The precise homogeneous normalization is

P=2(X^5-10X^3Y^2+5XY^4)+5phi(X^2+Y^2)^2T-5phi^3(X^2+Y^2)T^3+phi^5T^5,

Q=X^2+Y^2-T^2, and the plane pencil is P+lambda TQ^2=0. Its origin is [0:1:0] on the smooth projective normalization. In the arithmetic specializations lambda belongs to K; the generic base field is K(lambda).

The elliptic locus is exactly the finite parameters lambda different from 0, -5sqrt(5), and -phi^5. A cuspidal plane vertex need not make the normalization nonelliptic; the proof includes that distinction.

On this locus,

K(E_lambda[5]) = K(sqrt(5+2sqrt(5)), zeta_5, (lambda+phi^5)^(1/5)).

For lambda in K the degree is four when lambda+phi^5 is a fifth power in K, and twenty otherwise. In the latter case the group is D10 times C2, where D10 has order ten. The generic degree is twenty. There is no nonzero K-rational 5-torsion; the five infinity points constitute the torsion over K(sqrt(5+2sqrt(5))).

## Explicit computation and proof

[TURN_1.md](TURN_1.md) gives:

- A birational cubic model and inverse plane maps, with the original infinity origin identified
- The full exceptional-parameter calculation
- An actual quadratic-twist isomorphism to Tate normal form with beta=(11-5sqrt(5))lambda/[2(lambda+5sqrt(5))]
- The degree-ten division-polynomial remainder and both y-values for every root, specifying the other twenty torsion points
- Both inclusions in the exact division-field equality, valid under each allowed specialization
- The Kummer extension data and explicit Galois matrices

The primary question is [AIM Question 17, printed p.51](https://www.aimath.org/WWN/qptsurface2/qptsurface2.pdf). The full-level cover is credited to [Fisher, JEMS 3 (2001), Lemma 3.4](https://ems.press/content/serial-article-files/31488). The imported July 2026 partial report's infinity-line and conic reductions are credited and checked.

The source leaves its arithmetic field and equation scaling implicit; they are explicit here. The model has a rational origin and is not a nontrivial Tate–Shafarevich torsor. No local-solubility claim or solution of nonregular-pentagon variants is made.

## Validation and integrity

- [Independent full review](review/ADVERSARIAL_REVIEW.md): PASS, no mandatory correction
- Run `python verify_turn1.py`: 88,918 exact assertions, including separately labeled finite-field controls
- Run `python review/independent_checks.py`: 29 independently written symbolic checks
- All twelve frozen author files and six review files are preserved byte-for-byte
- [CURRENT_STATUS.json](CURRENT_STATUS.json) is the reviewed disposition; historical pending-review files are unchanged

Finite controls support the written universal proof and primary-theory dependency. AI-assisted review is not formal verification or human peer review. Downloaded source PDFs, screenshots and raw imports are not redistributed. No historical-priority claim is made.
