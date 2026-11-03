# Independent adversarial review: theta invariants and MRD codes

Reviewed 21 October 2026. This is an authored scope and verification audit, not a claim of a new MRD construction, a complete classification, or a current openness certificate.

## Verdict

The principal source-gate conclusion is sound: the known obstruction concerns a fixed generator, whereas the original research question permits substantially broader interpretations. The concrete length-seven experiment correctly demonstrates that the familiar fixed-generator collision is separated by other generators. It does not show that all-generator profiles characterize twisted Gabidulin codes or are complete equivalence invariants.

There is a source-transcription caution in the printed Giuzzi–Zullo characterization: its displayed membership and indexing must not be used literally without qualification. The intended augmented normal-form result remains established prior work.

## Source scope

1. The original Oberwolfach report asks whether the invariants can identify other MRD families or help produce constructions. It does not specify a universal completeness assertion, a particular additional family, or that only one generator must be used. Source: A. Neri, *Identifying rank-metric codes using Galois group action*, in [Contemporary Coding Theory, OWR 13/2019](https://ems.press/journals/owr/articles/16775), pp. 828–830.

2. Neri–Puchinger–Horlemann-Trautmann, [*Equivalence and Characterizations of Linear Rank-Metric Codes Based on Invariants*](https://arxiv.org/abs/1911.13059v2), Remark 6.8, compares the sum and intersection sequences for the same fixed generator. Its monomial code uses the exponent set obtained from a consecutive interval by deleting an interior exponent. The cited dimension-three MRD examples have exponent set {0,1,3}, length seven for odd q, and length eight for q congruent to 1 modulo 3. Unequal right idealizers establish inequivalence. The remark itself leaves comparisons involving different generators as a further possibility. It cannot support an all-generators impossibility theorem.

3. In Neri–Puchinger–Horlemann-Trautmann, equivalence is the semilinear vector rank-isometry relation. For extension-field-linear codes it has the form D = tau(C)A, with A invertible over the base field and tau an absolute finite-field automorphism. The Galois automorphism theta commutes with tau and fixes A. Consequently each labeled theta profile, not only the unordered collection of profiles, is invariant. Linear vector equivalence is a subcase. A counterexample to completeness for linear equivalence alone would not automatically establish a counterexample for semilinear equivalence; the right-idealizer argument used here supplies the stronger inequivalence.

4. General matrix equivalence and equivalence permitting transposition must be distinguished from that vector convention. The cited polynomial papers permit invertible compositions on both sides and field automorphisms. Their equivalence arguments for the extension-field-linear MRD examples are compatible with the usual normalizer reduction. Transposition is not part of Neri–Puchinger–Horlemann-Trautmann's stated vector equivalence, and theta-profile invariance under transposition should not be asserted. For the known monomial-versus-twisted pair, even allowing transposition does not rescue equivalence: the monomial code has both idealizers of order q^n, whereas a nontrivial twisted code has only one such idealizer. The unordered pair of idealizer orders differs.

5. Giuzzi–Zullo, [*Identifiers for MRD-codes*](https://arxiv.org/abs/1807.09476v3), Theorem 3.9, gives prior augmented characterization, not a dimensions-only characterization. Its additional invertibility and twisted-combination conditions carry substantive information. Theorem 3.10 also gives a sufficient MRD criterion starting from a rank-metric code with no rank-one element, rather than assuming MRD at the outset. Neither result constructs an unknown family solely from a dimension sequence.

6. Neri–Santonastaso–Zullo, [*Extending two families of maximum rank distance codes*](https://arxiv.org/abs/2104.07602v1), Theorem 3.8, gives the stated odd-q construction at length 2t, t at least three, with relative norm minus one. Proposition 4.2 and Theorem 4.3 use the profiles to exclude equivalence to Gabidulin codes and, for t at least five, extension-field-linear twisted Gabidulin codes. Remark 4.4 handles the remaining coefficient-twisted codes through idealizers. Theorem 4.6 and Corollary 4.9 additionally describe equivalence within the constructed family. Those are stronger positive results than merely computing a few invariant values, but are not a characterization by theta dimensions alone. The source gate is appropriately conservative about the role of the invariants in the construction.

## Giuzzi–Zullo printed-statement caution

The inspected rendered page, not only the extracted text, places p and q in C while simultaneously displaying the chain p^[s], ..., p^[s(k-1)] and requiring p invertible. Literal use is inconsistent in the intended nontrivial range: p together with that chain gives k independent consecutive Frobenius iterates, so their span is a generalized Gabidulin code of dimension k, with intersection dimension k-1, rather than the asserted k-2. The normal-form argument in Lemma 3.8 explains the intended shift; one must not additionally impose membership of the unshifted invertible p in C in that displayed version.

The printed hypothesis k > 2 also should not be advertised as an unrestricted boundary-case theorem. At k = n-1, two such subspaces of an n-dimensional space intersect in dimension at least n-2, making the claimed k-2 value impossible; full dimension is similarly excluded. Safe use in this audit is the nontrivial range 2 < k < n-1. No claim is made that these printed issues overturn the established intended characterization, or that an erratum has been checked.

An unambiguous sufficient normal form is the span of p^[s], ..., p^[s(k-1)] and p + eta p^[sk], for invertible p and admissible nonzero eta. Composition on the right by p inverse gives the standard twisted code. This formulation avoids the erroneous extra membership condition and shows explicitly why the information is more than intersection dimensions.

## Independent verification of the length-seven test

Let F = F_(3^7), theta(a) = a^3, and identify linearized polynomials with their length-seven evaluations on an F_3-basis. In exponent-coordinate notation let e_j represent x^(3^j). The tested codes are

- C = span_F(e_0, e_1, e_3).
- H = span_F(e_0 + e_3, e_1, e_2).

The parameter of H is eta = 1; its norm is 1, different from (-1)^(3 times 7) in F_3. Thus it is an admissible twisted code.

For C, direct unions and intersections of the shifted support sets {0,1,3} independently reproduce every entry in the profile output. All six generators give the sum profile (3,5,6,7,...) and intersection profile (3,1,0,...).

For H, the generators theta and theta inverse give the same two profiles. At theta squared, the sum contains e_0 through e_5 individually and therefore has dimension six. Adding the next conjugate introduces e_6. At theta cubed, the six generating vectors are independent and the next conjugate fills the remaining dimension. Inverse-generator symmetry covers theta to the fourth and fifth powers. Consequently those four generators give sum profile (3,6,7,...) and intersection profile (3,0,...). The all-generator collection separates C from H even if its labels are discarded.

The profile program computes ranks over F_3. This is exact here, not an approximation: all coefficient matrices lie in F_3, so scalar extension to F preserves their rank. Frobenius fixes their coefficients, and cyclic exponent shifts correctly implement conjugation. The coefficient-space orthogonal complement is used only to compute intersection dimensions via elementary linear algebra; it need not be identified with the evaluation code's named rank-metric dual.

## Finite-field certificate audit

The exhaustive program uses the quotient F_3[z]/(z^7+z^2+2). Its multiplication reduction implements z^7 = 1 + 2z^2 correctly. Its check that each nonzero quotient element has a multiplicative inverse certifies a field. An independent polynomial-arithmetic implementation also verified the Rabin irreducibility conditions: z^(3^7) reduces to z, and gcd(z^3-z, z^7+z^2+2) is one.

The rank routine is Gaussian elimination over F_3 on the seven field-coordinate columns of the evaluation vector. Pivot normalization is correct because the nonzero elements 1 and 2 of F_3 are their own inverses. The coefficient enumeration selects exactly one representative from each nonzero F-projective class: (1,a,b), (0,1,b), or (0,0,1). There are 2187^2 + 2187 + 1 = 4,785,157 representatives for each three-dimensional code, and nonzero F-scaling preserves F_3-rank.

The completed output for each code has projective counts 99,463 at rank five, 1,993,632 at rank six, and 2,692,062 at rank seven, with no lower-rank representatives. The counts sum to 4,785,157. Independence of the three polynomial generators is immediate from their distinct exponent coordinates, and evaluation is injective on the seven-dimensional space of linearized polynomials of q-degree below seven. Thus the exhaustive check covers every nonzero codeword up to rank-preserving scaling and certifies minimum rank distance five. This attains the Singleton bound for length seven and dimension three.

This is a finite certificate for the explicit q=3 example, not a proof for every odd q, and it does not certify general all-generator completeness. The final hardened C++ program was independently recompiled with C++17, optimization, and compiler warnings enabled, then rerun exhaustively. It exited successfully and its output matched FINITE_TEST.json byte for byte. The algorithm was also reviewed and its mathematical coverage checked. Independent polynomial arithmetic, support-profile checks, and histogram-total checks are reproducible with independent_check.py; INDEPENDENT_CHECK.json records that program's successful result.

The completed AUDIT.md was read separately. Its source scope, finite certificate, profile calculations, and explicit right-idealizer computations agree with this review. The latter correctly give orders 3^7 and 3, certifying inequivalence even under ordinary two-sided polynomial equivalence independently of the vector theta-profile argument.

## Acceptance boundaries

- Accept the fixed-generator collision and the concrete MRD verification as correct.
- Accept the demonstrated separation by additional generators.
- Preserve the distinction between sum-only, sum-and-intersection, all-generator, all-automorphism, arbitrary-subset, and augmented invariants. At degree seven all six nonidentity automorphisms are generators, but this coincidence is special to prime extension degree.
- Do not call the known monomial or twisted codes new, call this a full solution of the Oberwolfach question, or infer a classification from one finite example.
- Qualify the Giuzzi–Zullo quotation as the intended nontrivial-range augmented result rather than a literal fully audited transcription of its printed statement.

No publication or external-state mutation was performed for this review.
