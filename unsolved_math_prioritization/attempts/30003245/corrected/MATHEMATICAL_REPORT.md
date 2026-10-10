# Bounded-house finiteness: scope, partial proofs, and a local obstruction

Problem 30003245 / OWR-15170-007. Checked 6 October 2026.

## Conclusion

The full assertion is unresolved by this investigation. No verified full proof or counterexample was found. This report proves the assertion for d <= 2 and, for every fixed d, for house at most 2. It supplies a concrete counterexample to a tempting valuation step, not to the problem. These are classical-method partial results; no new solution or research priority is claimed.

A May 2026 manuscript claiming a much stronger theorem was withdrawn on 2 June 2026 because of a valuation error. An August 2026 manuscript proves a substantial result for composite rings of integers, but does not identify those rings with the full ring of integers required here. Neither establishes the requested assertion.

## 1. The exact field and question

Fix an algebraic closure of Q. Let Q^(d) be the compositum of all finite extensions of Q of degree at most d, and put

K_d = Q^(d) intersect Q_tr,

where Q_tr is the field of all totally real algebraic numbers. For an algebraic number a, write house(a) for the largest modulus of its Q-conjugates. The question asks whether

B_d(X) = {a in O_(K_d) : house(a) < X}

is finite for each fixed positive integer d and every real X >= 1. The superscript bounds the degrees of generating fields, not the degrees of all their elements. The target is Question 4 in Martin Widmer's contribution to OWR 49/2016. In the EMS version it is on printed page 2815, PDF page 23. Definitions occur on printed page 2812. The MFO-hosted version has the same PDF page positions but printed pagination shifted by two pages; no byte identity is asserted. [S1]

Both Q^(d) and K_d are Galois over Q. The first contains the normal closures of its generating fields, since it contains every conjugate of each generator field. The second is the intersection of two Galois extensions.

For nonzero algebraic integers a, the absolute multiplicative Weil height satisfies H(a) <= house(a), since house(a) >= 1 and every finite-place factor in H(a) is 1. Thus Weil-height Northcott implies the desired house finiteness; the converse is not being used.

House finiteness in O_K for a totally real K is equivalent to house finiteness in its totally positive integers. One direction is restriction. For the other, a != 0 implies a^2 is totally positive and house(a^2) = house(a)^2; every square has at most two square roots. This explains the connection to the NPI terminology in [S2], without strengthening the theorem proved there.

## 2. Coefficient compactness and the missing degree bound

**Lemma.** Given real C >= 1 and a positive integer D, there are finitely many algebraic integers a with house(a) <= C and [Q(a):Q] <= D.

**Proof.** For degree n <= D, the monic minimal polynomial has integer coefficients c_j. Each c_j is a sum of binomial(n,j) products of j conjugates, so |c_j| <= binomial(n,j) C^j. Each coefficient therefore has finitely many possible integer values. There are finitely many possible polynomials and finitely many roots of each. QED.

Consequently the original question is exactly equivalent to the existence, for every d and X, of a finite upper bound D(d,X) for the degrees of elements of B_d(X). The forward implication takes the maximum degree of a finite set; the reverse implication is the lemma. This is a reduction, not a proof of that bound.

An exponent bound on a Galois group alone is not a degree bound: the groups (C_2)^r have exponent 2 and unbounded order. Likewise, bounded local degrees cannot simply be substituted for bounded global degree. Their interaction with bounded house is the substantive unresolved step in the general case.

## 3. A self-contained proof for d <= 2

For d = 1, K_1 = Q and O_(K_1) = Z. For d = 2, K_2 is the compositum of the real quadratic fields. We give an elementary ramification proof of the house assertion; the stronger Weil-height result is due to Bombieri and Zannier [S3].

Fix X >= 1 and a in O_(K_2) with house(a) < X. If a is rational there is nothing to prove. Otherwise F = Q(a) is a finite multiquadratic Galois extension: its Galois group is elementary abelian of exponent 2.

Let p be an odd prime ramified in F. Tame inertia is cyclic, so its nontrivial inertia group has order 2. Because the Galois group is abelian, this same subgroup is the inertia subgroup at every prime of F over p. Let t be its nonidentity element and put b = a - t(a). Then b != 0, because a generates F, and b is integral. At every prime P above p one has b in P.

Write n = [F:Q], with residue degree f and g primes over p. Here the ramification index is 2, and n = 2fg. Therefore

v_p(N_(F/Q)(b)) >= fg = n/2.

Every archimedean conjugate of b has modulus less than 2X. Since its nonzero norm is an integer,

p^(n/2) <= |N_(F/Q)(b)| < (2X)^n,

and hence p < 4X^2.

Thus every odd ramified prime in F lies in the finite set S of primes at most 4X^2; include 2 in S as well. Every quadratic subfield of F is Q(sqrt(m)) for a positive squarefree integer m whose prime divisors belong to S, because ramification in a subfield forces ramification in F. A multiquadratic extension is generated by its quadratic subfields. Consequently

F is contained in Q(sqrt(p) : p in S),

a single number field depending only on X, of degree at most 2^|S|. Applying the coefficient lemma proves the required finiteness. QED.

More generally, Bombieri-Zannier's theorem gives Weil-height Northcott for the maximal abelian subfield of Q^(d), hence house finiteness for its algebraic integers. This is a credited theorem, not a new result established here. [S3]

## 4. Every fixed d: finiteness through house 2

Set E = lcm(1,2,...,d). Each normal closure of a number field of degree n <= d has Galois group a subgroup of S_n, whose exponent divides E. The Galois group of Q^(d) embeds in the product of these groups by restriction. Hence its exponent divides E. The same is true of every finite Galois subextension and quotient, including every finite Galois subfield of K_d.

**Proposition.** There are only finitely many a in O_(K_d) with house(a) <= 2. An explicit containing set is

{z + z^(-1) : z^M = 1},

where

M = 2^(v_2(2E)+2) times product over odd primes p with p-1 dividing 2E of p^(v_p(2E)+1).

In particular there are at most M/2 + 1 such a. The bound is deliberately loose and is not an exact membership classification.

**Proof.** Let a be such an integer and let z be a root of T^2 - aT + 1. It is integral by transitivity of integrality. Under every embedding, a maps to a real number in [-2,2], so both roots of this quadratic have modulus 1. Thus all Q-conjugates of z lie on the unit circle.

For completeness, the usual Kronecker argument shows z is a root of unity. Every positive power z^r is integral, of degree at most [Q(z):Q], and has all conjugates of modulus 1. The coefficient lemma puts these powers in a finite set. Two powers coincide; since z != 0, z has finite multiplicative order n.

Now a = z + z^(-1), with z a primitive nth root. If n > 2, the field Q(a) is the maximal real subfield of Q(z). Indeed z satisfies the displayed quadratic, z is nonreal, and complex conjugation has fixed field of index 2. Its Galois group is (Z/nZ)^*/{+1,-1}. Since Q(a) is contained in K_d, this quotient has exponent dividing E. For every unit u modulo n, u^E = +1 or -1 modulo n, and therefore u^(2E) = 1 modulo n. The same last conclusion is trivial for n = 1,2.

The Chinese remainder theorem now gives the claimed conductor bound. For an odd prime power p^a dividing n, the unit group has exponent p^(a-1)(p-1), so p-1 divides 2E and a <= v_p(2E)+1. For 2^a dividing n, the unit-group exponent is 2^(a-2) for a >= 3 (with the familiar smaller cases a = 1,2), so a <= v_2(2E)+2. These inequalities say precisely that n divides M. There are finitely many Mth roots of unity. Pairing z with z^(-1) gives M/2+1 values because M is even. QED.

This establishes the original strict-inequality question for every 1 <= X <= 2, and additionally establishes the endpoint house <= 2.

It also excludes the standard false counterexample. The distinct numbers 2 cos(2 pi/p), for odd primes p, are totally real algebraic integers of house less than 2 and disprove finiteness in the unrestricted ring O_(Q_tr). But membership in a fixed K_d forces p-1 to divide 2E. Only finitely many primes satisfy that condition. Unrestricted Q_tr is not the field in the question.

## 5. Why the abelian inertia proof does not extend as written

In a nonabelian Galois extension, inertia subgroups at different primes above p are conjugate, not necessarily equal. Fixing one inertia group does not make a subfield unramified at every prime above p. This is a real obstruction even inside K_3.

Here is a concrete example. Let

f(T) = T^3 - 4T + 1,

let a be a root, let U = Q(a), and let L be its splitting field. The polynomial has no rational root and has discriminant 229, which is prime. Thus U has degree 3, Z[a] is its full ring of integers, all three roots are real, and Gal(L/Q) is S_3. In particular L is contained in K_3.

Modulo 229,

f(T) = (T - 29)^2 (T - 171).

Dedekind factorization applies because the index is 1. There is a ramified prime q of U above 229 corresponding to T-29, with ramification index 2 and residue degree 1, and an unramified prime r corresponding to T-171, with both indices 1. At primes of L above 229, tame inertia has order 2: the discriminant valuation 1 gives the transposition action, equivalently the local factorization has one ramified quadratic factor and one linear factor.

At any prime w of L above 229, write D_w and I_w for decomposition and inertia. The inertia I_w is generated by a transposition. Since I_w is normal in D_w and its normalizer in S_3 is I_w itself, D_w = I_w, so the residue degree of L/Q is 1 and there are three primes of L above 229.

Choose a prime w_0 of L over r. The tower formula gives e(w_0/r) = 2 because e(w_0/229) = 2 and e(r/229) = 1. Thus its inertia group I lies in Gal(L/U), and both have order 2; they are equal and U = L^I. This choice does imply unramifiedness at r.

Put b = f'(a) = 3a^2 - 4. Multiplication by b in the basis 1,a,a^2 has matrix

[[-4,-3,0], [0,8,-3], [3,0,8]],

whose determinant is -229. Thus N_(U/Q)(b) = -229. At r, b is a unit because f'(171) is nonzero modulo 229. At q it vanishes because f'(29) is zero modulo 229. Norm factorization gives v_q(b) = 1. If w is a prime of L above q, the ramification index of L/U at w is 1, since both L/Q and U/Q have ramification index 2 there. Hence the integer-normalized valuation is

w(b) = 1,

where w and v_q are discrete additive valuations normalized to have value group Z, so w|_U = e(w/q) v_q and w(229) = 2. This is not the normalization with w(229) = 1. The value w(b) = 1 is not divisible by |I| = 2, even though b belongs to U = L^I.

This refutes the implication “membership in a field fixed by one inertia group forces valuation divisibility by its order at every prime above p.” It does not refute bounded-house finiteness. The provided verifier checks the exact polynomial, discriminant, modular factorization and norm identities; the field-theoretic deductions are proved above and are not claimed to be mechanically certified.

Castillo's arXiv:2605.27232v1 proposed finite-exponent Northcott. Its current v2 record explicitly marks it withdrawn and identifies a failed valuation-divisibility step on page 4. The example above explains why that type of step needs an additional hypothesis; no corrected proof of the withdrawn theorem is asserted. [S4]

## 6. The 2026 composite-ring result and the remaining scope gap

Man, Technau, Widmer and Yatsyna construct Q^(3) as the compositum of Q^(2) with a minimal sequence of cubic fields. Their Corollary 1 proves Weil-height Northcott for the ring generated by the component rings of integers under the stated disjointness and degree hypotheses. Their Proposition 1 also constructs, in any algebraic subring, a Northcott subring with the same fraction field. These results do not identify the constructed ring with O_(Q^(3)). [S5]

Finiteness for a subring does not imply finiteness for its integral closure. As a direct warning using the cited Proposition 1, take S = O_(Q_tr) and obtain a subring T with Northcott and fraction field Q_tr. Its integral closure in that fraction field is O_(Q_tr): every algebraic integer is integral over Z, hence over T; conversely an element integral over T is integral over Z by transitivity. But O_(Q_tr) has the bounded-house cyclotomic family displayed above. Therefore a general “pass to integral closure” rule would be false, even for totally real rings.

For the particular ring constructed inside Q^(3), the required full-ring transfer is not proved here. Likewise, total reality alone does not repair the all-primes inertia assertion, as the S_3 example shows.

## 7. Final boundary

The valid results are: the full statement for d <= 2; its restriction to abelian subfields for arbitrary d by Bombieri-Zannier; and house <= 2 for every fixed d by the elementary conductor argument. For general d >= 3 and arbitrary X > 2 this investigation supplies neither a proof nor a counterexample. The exact additional goal is a bound D(d,X) on degrees, or another argument that establishes the same finiteness without silently assuming such a bound.

The source search is dated and bounded, not a proof that no later or unlocated result exists. The withdrawn preprint is not a prior solution. The authored proofs and obstruction audit are unrefereed, with no proof-assistant certification and no novelty claim.

## References

[S1] Martin Widmer, “Northcott Number and Undecidability of Certain Algebraic Rings,” in Definability and Decidability Problems in Number Theory, Oberwolfach Report 49/2016, DOI 10.4171/OWR/2016/49. Publisher: https://ems.press/content/serial-article-files/46652 . Mirror: https://publications.mfo.de/bitstream/handle/mfo/3553/OWR_2016_49.pdf?isAllowed=y&sequence=1 .

[S2] Nicolas Daans, Vitezslav Kala, Siu Hang Man, “Universal quadratic forms and Northcott property of infinite number fields,” Journal of the London Mathematical Society 110(5) (2024), e70022. https://doi.org/10.1112/jlms.70022 . Author accepted manuscript: https://arxiv.org/pdf/2308.16721 .

[S3] Enrico Bombieri and Umberto Zannier, “A note on heights in certain infinite extensions of Q,” Rendiconti Lincei. Matematica e Applicazioni 12 (2001), 5-14. Public bibliographic/PDF source: https://www.bdim.eu/item?fmt=pdf&id=RLIN_2001_9_12_1_5_0 . The theorem was cross-checked in [S1] and [S2]; direct full-PDF retrieval through the reader was unavailable. See also Martin Widmer, “On the Northcott property for infinite extensions,” https://arxiv.org/abs/2310.11337 .

[S4] Benjamin Castillo, “The Northcott Property for Composites of Number Fields of Bounded Degree,” arXiv:2605.27232. WITHDRAWN, version 2, 2 June 2026: https://arxiv.org/abs/2605.27232v2 . Historical version 1 used only for the proof-obstruction audit: https://arxiv.org/html/2605.27232v1 .

[S5] Siu Hang Man, Niclas Technau, Martin Widmer, Pavlo Yatsyna, “Height lower bounds for elements of highly composite rings,” arXiv:2608.11904v1, submitted 12 August 2026. https://arxiv.org/abs/2608.11904 . The PDF was read through https://arxiv.org/pdf/2608.11904 . Treated as a preprint; no journal acceptance claimed.
