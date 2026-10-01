# Author turn 1: the exact finite-support structure and endpoint invariants

**Partial; the eta_C question remains unresolved.** 2026-10-01.

This turn investigates the construction itself before applying the known Countryman epimorphism theorem. It shows directly that eta_C is normal for every Countryman input C, and that the published stationary-endpoint necessary condition cannot obstruct an epimorphism *from* eta_C. Normality alone is not enough to prove strong surjectivity.

## 1. The object and its convex copies

Write D=C*+{0}+C and let L=E(D) be all functions x:omega→D that are eventually zero, ordered lexicographically by the first different coordinate. This is Moore's exact eta_C construction. Every x has finite support. If u is any finite word in D, the set

    [u]={u concatenated with x : x in L}

is convex and isomorphic to L by prefix removal. The cylinders of a fixed length n partition L, in the lexicographic order of D^n. Thus

    L is isomorphic to D^n × L                          (1)

with the first coordinate primary. This is an actual order isomorphism, not a assertion that either product projection is a monotone epimorphism.

The order has no endpoints: append a positive or a negative element after the support of x to find points on either side. Moreover every open interval has size aleph1. Given x<y, let j be their first difference. Choose N larger than j and both support lengths. For each c in the positive C copy, change only x(N) from zero to c. The resulting point is strictly between x and y, and different c give different points. Cardinality is aleph1 because it is a countable union of finite powers of the aleph1-sized alphabet.

## 2. Aronszajn preservation and a direct normality witness

Countryman lines are Aronszajn and have cardinality aleph1; these are credited standard facts, recorded in Moore and in Polymeris–Martinez-Ranero Lemma2.6. Finite sums and finite lexicographic products of Aronszajn/countable orders remain short and have no uncountable separable suborder. For the product assertion, an alleged uncountable forbidden suborder either has uncountably many first coordinates, giving a forbidden suborder in the first factor by taking one representative per fiber, or has an uncountable fiber in the second factor. The same argument handles omega1 and its reverse; any uncountable subset of omega1 has type omega1. A countable union of such suborders also cannot contain an uncountable forbidden suborder, since one piece would contain an uncountable part of it. Applying this to the padded finite powers D^n proves that L is Aronszajn. This reproduces the elementary construction property, not Moore's PFA universality theorem.

Choose an increasing continuous sequence (C_xi)_(xi<omega1) of countable subsets covering C. Put

    D_xi=C_xi*+{0}+C_xi,
    E_xi=E(D_xi).

Each E_xi is countable, the sequence is increasing and continuous, and its union is L. Continuity uses finite support: finitely many symbols that appear at a limit stage already all occur at one earlier stage.

Fix x outside E_xi. There is a coordinate j whose nonzero symbol lies outside D_xi. Choose N larger than j and the support of x, and choose fixed negative and positive symbols d_-<0<d_+ in D. Let x^- and x^+ be obtained by placing d_- or d_+ at coordinate N. Then

    x^- < x < x^+.

For every z in E_xi, the first coordinate at which z differs from x is at most j, because z(j) cannot equal x(j). That comparison is unchanged when passing to x^- or x^+. Therefore z is never strictly between x^- and x^+. The three points belong to the same complementary interval of L\E_xi. Every point in every such complementary interval has another point below and above it in the same interval; none of these intervals has an endpoint.

Consequently (E_xi) witnesses non-stationarity of L. Combined with the aleph1-density above, **eta_C is a normal Aronszajn line for every Countryman C**, with no extra normality hypothesis on the input C and no use of PFA in this structural calculation.

## 3. The stationary-endpoint obstruction is vacuous at this domain

Polymeris–Martinez-Ranero Theorem1.9 supplies a necessary condition for an epimorphism A→B in terms of stationary sets of levels at which all complementary intervals have an endpoint. For the displayed decomposition of L, every complementary interval is nonempty and has neither endpoint. Hence each of the four endpoint sets L(D), R(D), Lhat(D), Rhat(D) is empty (where the first two use “some” and the latter “every”).

Thus the necessary differences Lhat(L)\Lhat(B) and Rhat(L)\Rhat(B) are empty for every target B. This published invariant cannot produce the desired negative example with eta_C as domain. It does not follow that all other obstacles vanish, that the sufficient Countryman forcing theorem applies to L, or that L has an epimorphism onto B. In particular, L contains copies of both C and C*, so it is not itself Countryman.

## 4. Why normality is not a solution

The known countercontrol is a normal Countryman line C0 together with its reverse: A=C0+C0* is normal but not strongly surjective. This example is already noted after Corollary3.2 of Polymeris–Martinez-Ranero, and is credited here.

For completeness, suppose f:A→C0 were a monotone surjection. The image of the final summand C0* must be countable: otherwise choosing one preimage for each value would give an uncountable order embedding into both C0 and C0*, impossible for a Countryman line. On the other hand, choose any y in that final summand. Surjectivity and monotonicity imply that every target point above f(y) also lies in its image. That final ray of the aleph1-dense C0 is uncountable, a contradiction. The normality of the sum follows by combining the two normal decompositions; crossing the joining cut cannot introduce a first or last point into a complementary interval.

Therefore proving eta_C normal closes no strong-surjectivity gap by itself. It only identifies why normal-input facts and stationary endpoint obstructions have to be used carefully.

## Remaining mechanism

The finite-support construction gives many convex copies of eta_C and arbitrarily long tails, but a monotone quotient onto an arbitrary suborder must place all points into the correct ordered convex fibers. PFA universality supplies an embedding, not those fibers. The next attempt will make this gap exact through a retraction/cut criterion, including why a chosen embedding can fail even when an epimorphism of the abstract orders exists.

Substantive author turns: 1/5. Estimated completion15%. All quoted general results are credited; no novelty claim, no full epimorphism theorem and no counterexample to the target.
