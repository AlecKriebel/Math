# Independent review of the Schubert-curve partial (20000236)

**Verdict: PASS_SCOPED_DEGREE_THREE_SMOOTHNESS_AND_FAMILY.** No mandatory correction. The full original problem remains **unsolved, 2/5 approaches**.

The reviewed `PARTIAL_RESULT.md` has SHA256 `03232d129ce64ae4ed60f4bd38c47a18ee392fdf84c38937f4e62a33ddadb1fe`. This is an independent adversarial AI review, using gpt-6-astra at xhigh, and is not human peer review or a priority certification.

## Source and precise scope

I read the original AIM discussion on printed pages 5–6 and visually checked page 6. Problem 10.4 asks whether a one-dimensional intersection of osculating Schubert varieties at distinct real points is smooth over the complex numbers. Its preceding Theorem 10.3 already supplies smoothness at every real point. The following Osserman question, Problem 10.6, is separate. The submitted statement retains this distinction and does not turn real smoothness into the conclusion by definition.

The complete Levinson preprint supplies the needed inputs: Theorem 1.1 gives dimensional transversality for distinct osculation points; Theorem 1.2 records the zero-dimensional Mukhin–Tarasov–Varchenko total-reality theorem; Theorem 1.5 and Corollaries 2.9–2.10 supply real smoothness and the real structure on every component. The preprint explicitly records reducedness, and its normalization calculation in Lemma 5.5 is consistent with the calculation used here. Conjecture 4.4 is the broader complex-smoothness question. I checked these statements, their relevant proofs and surrounding hypotheses in the full primary preprint. Its published Canadian Journal of Mathematics metadata is corroborated, but this review does not claim a line-by-line comparison with the final journal version.

The earlier imported degree-two, Richardson and Wronskian-kernel results are expressly credited. This review accepts no new discovery claim and does not independently certify every claim in that imported report.

## Components and the moving-box argument

The assertion that every complex irreducible component is defined over R is justified. Here is an independent reconstruction of the submitted moving-box proof.

Fix an irreducible component C. Every additional box condition is a Plucker hyperplane section. For real y away from the finitely many marked points, properness makes the full intersection zero-dimensional; in particular the hyperplane cannot contain C. Since O_C(1) has positive degree, its section has a zero, so C meets that hyperplane. Total reality makes all such intersection points real.

A fixed Grassmannian point U can occur at only finitely many values of y: the added box says its Wronskian vanishes at y, and that Wronskian is nonzero. To check the last statement, choose a basis with distinct polynomial degrees d_1<...<d_k. The coefficient of degree sum(d_i)−k(k−1)/2 in its Wronskian is the product of the leading coefficients times the nonzero Vandermonde product over d_j−d_i. This remains valid when some differentiated low-degree terms are zero. The homogeneous Wronskian has only finitely many zeros on P¹, including a possible zero at infinity.

Consequently C contains infinitely many real points. Those points belong to both C and its conjugate, so the irreducible curves coincide. This uses arbitrary initial partitions and only one additional box; it does not replace the original problem by an all-box problem. It also agrees with Levinson's componentwise Corollary 2.10.

## The conditional degree-three theorem

For a reduced projective curve, normalization is finite and the quotient in

    0 → O_S → nu_* O_tilde(S) → Q → 0

has finite length delta. A projective irreducible component of the normalization is a smooth connected curve, so its Euler characteristic is 1−g_j. Additivity gives exactly

    delta = r − sum(g_j) − chi(O_S).

This calculation permits disconnected S; no connected arithmetic-genus substitution is needed. Every singular point is nonreal because the real locus is smooth. Conjugation acts freely on the singular support and preserves the complex lengths of the corresponding normalization defects. Thus delta is even, rather than merely the number of singular points being even.

The Plucker degree is the sum of the positive integer component degrees because the curve is reduced and pure. Hence degree at most three implies r≤3. If r≤2 and chi≥1, then 0≤delta≤1, forcing delta=0. If r=3, each component is an embedded projective line. Each is defined over R by the preceding argument. Two distinct projective lines meet in at most one point; if both are real, that intersection is conjugation-fixed and therefore real. Such an intersection would be a singular point of their reduced union, contradicting real smoothness. Thus the three lines are disjoint and smooth. Finally delta=0 means the normalization is an isomorphism, and a normal curve over C is smooth.

No gap was found. The example consisting of a real line and a real conic meeting at two conjugate nonreal points explains why the chi assumption matters. It is a diagnostic for the general curve argument, not a Schubert counterexample.

## The explicit family and scheme structure

For k=2 and lambda=(n−3,n−5), the ordinary Schubert incidence indices are

    n−1−lambda_1=2,     n−lambda_2=5.

Thus the variety is exactly the four-dimensional locus U⊂F_5 with dim(U∩F_2)≥1. This works for n=5, including the zero second part, and for every larger n.

Setting p_34=p_35=p_45=0 in the five Plucker relations for G(2,5) leaves the three minors of the displayed 2-by-3 matrix and no additional equation involving p_12. The homogeneous ideal is prime: the rank-one parametrization u_i=a c_i, v_i=b c_i has these minors as its kernel, with the standard monomial/row-and-column-margin description. Its height is two. Hence the stated Hilbert–Burch resolution is exact, and adjoining the free cone coordinate gives the Cohen–Macaulay ring of dimension five and series (1+2t)/(1−t)^5.

The three remaining box conditions are homogeneous linear equations. Dimensional transversality at every distinct real configuration gives their joint height three. In this Cohen–Macaulay ring they form a regular sequence. There is no appeal to a generic-hyperplane Bertini theorem: the actual osculating hyperplanes satisfy the height condition. Their quotient has Hilbert series (1+2t)/(1−t)^2. Its Hilbert polynomial is 3m+1, so the projective curve has degree three and chi(O_S)=1. This is a scheme-theoretic calculation; degree alone would not determine chi.

Reducedness and real smoothness are the credited Schubert inputs. The preceding degree-three theorem then proves the asserted all-distinct-real-configuration family. Independent four-step Pieri growth from lambda to the ambient rectangle gives multiplicity three, confirming the degree. The result does not cover arbitrary larger-degree Schubert curves, arbitrary complex or colliding osculation points, or the stable boundary.

## Reproduction and independent diagnostics

All **3,373** submitted assertions reproduce with a byte-identical receipt. The independent script passes **1,330** exact checks using SymPy, including:

- a Groebner/initial-ideal count compared with the monomial-image margin count for the rank-one ring
- the cone Hilbert function and its third finite difference, independently recovering 3m+1
- direct Pieri growth for 71 ambient dimensions and the exact flag indices
- 189 polynomial Wronskians with nontrivial lower coefficients, checked by differentiation
- normalization-defect parity, rational intersections of real lines, and the conjugate-node diagnostic

Reproduce from this review directory with `python independent_checks.py`; reproduce the submitted receipt with `cd author_replay && python verify.py`. These bounded controls do not establish the imported Schubert theorems or enumerate all real configurations. The written geometric and commutative-algebra arguments provide the universal steps.

The package is ready as a reviewed partial. Preserve **unsolved 2/5**, the chi hypothesis, distinct real osculation points, and the attribution of earlier work.

## Primary references

- [Original AIM problems, pages 5–6](https://aimath.org/pastworkshops/degenalggeomproblems.pdf)
- [Levinson, full primary preprint](https://arxiv.org/abs/1504.06542v1), especially Theorems 1.1–1.5, Corollaries 2.9–2.10 and Lemma 5.5
- [Published Levinson article](https://doi.org/10.4153/CJM-2015-061-1), Canadian Journal of Mathematics 69 (2017), 143–185
- [Mukhin–Tarasov–Varchenko, Annals of Mathematics 170 (2009)](https://doi.org/10.4007/annals.2009.170.863), used through its precise total-reality statement in Levinson
