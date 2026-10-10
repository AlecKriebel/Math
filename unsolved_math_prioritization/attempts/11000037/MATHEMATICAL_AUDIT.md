# Independent mathematical audit: Torelli density, target 11000037

Date: 2026-10-10 UTC. Target: 11000037 / AMR-109-0037, normal queue rank 1254.

## Verdict and distributed mathematical files

**PASS as rigorously proved partial results; NOT a solution of the arbitrary-generating-set Torelli density conjecture.** No required mathematical correction was found in the reviewed arguments.

This audit independently checked the complete arguments in the report and its separately reviewed logarithmic appendix. The distributed proof files are:

- [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md): 11,795 bytes; SHA-256 `889f1e0452d461bcdd99688707f3ee5bec129b4d99d5634f396b6ceb165b262e`.
- [LOGARITHMIC_APPENDIX.md](LOGARITHMIC_APPENDIX.md): 5,737 bytes; SHA-256 `8d3f1aa5a4c455da5e6d09eea3a89db1f0c2851e75102219f5dd492be49bf8c4`.

The report proves exponential negligibility after a suitable finite generating-set enlargement. The appendix proves the universal half-growth lower bound for logarithmic liminf and the sharp value 1/2 of both infima over generating sets containing any prescribed finite subset. This audit covers both complete mathematical arguments and their stated limitations.

This AI-assisted, unrefereed edition retains the complete mathematical assessments. Scoped acceptance is not external human peer review, journal acceptance or formal proof-assistant certification.

The full target remains unproved: for every finite symmetric generating set S of the closed oriented genus-g mapping class group, g >= 2, show that the proportion of Torelli elements in the distinct-element ambient ball B_S(n) tends to zero. No claim of novelty, priority, or exhaustive verification of continuing openness is accepted or made.

## 1. Source statement, object being counted, and scope

I visually inspected the retained rendering of Benson Farb's chapter, printed page 29, one-based PDF page 36. Equation (9) uses the cardinalities of the subset intersected with an ambient word ball and of that ambient ball. Conjecture 3.16 asks for Torelli density zero. The paragraph introducing logarithmic density replaces the numerator and denominator separately by their logarithms. Consequently ordinary density zero and a bound on the logarithmic ratio are different questions.

The report correctly counts group elements rather than spellings, does not use random-walk measure, and does not substitute intrinsic Torelli balls or pseudo-Anosov dilatations. Its all-generating-set target interpretation is explicitly stated. Its counterexample below establishes that the nearby generating-set discussion cannot simply be used as an unrestricted theorem for all finitely generated groups.

The closed, unmarked, orientation-preserving genus-g scope is essential. The genus-one aside is correct: the homology representation identifies the torus mapping class group with SL(2,Z), so Torelli is trivial and has zero density in the infinite ambient group. The genus-zero exclusion is correct. Punctures, boundary components, and extended mapping class groups are not covered by the asserted application. If a prescribed finite set contains the identity, allowing the identity as a harmless generator leaves every ball unchanged; the report and appendix state this convention explicitly.

Public source: https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf . Retained PDF: 2,724,624 bytes; SHA-256 `f37c6a1dbc875105c2b294196de1a03a88595b75e8705e6077e9d48f066e402a`. This was a reused retained source, not a fresh local download for this audit. Its public URL was also opened during this audit.

## 2. Free-tree adjacency estimate

For q = 2k-1, the Cayley graph of the free rank-k group is a (q+1)-regular tree. Orienting toward an end, rather than toward a root vertex, makes every vertex have exactly one parent and q children. There is no exceptional root term.

For each parent-child edge, the weighted arithmetic-geometric-mean bound is

2 |f(parent)| |f(child)| <= q^(-1/2)|f(parent)|^2 + q^(1/2)|f(child)|^2.

A vertex is counted q times in the first role and once in the second. Its total coefficient is q*q^(-1/2) + q^(1/2) = 2 sqrt(q). The absolute value of the adjacency quadratic form is bounded by the sum of the left sides; complex-valued f causes no problem, since one bounds the absolute value of the real part of each conjugate product by its modulus. The adjacency operator is bounded, being a finite sum of unitary translations, and self-adjoint. Thus the quadratic-form bound on the dense finitely supported subspace yields norm at most 2 sqrt(q). Equality is unnecessary. This part is fully elementary and sound.

## 3. Restriction of the quotient regular representation

Let K = pi(G) and H = <pi(x_1),...,pi(x_k)> be free with the displayed basis. Under left multiplication, the H-orbit of an element a of K is H a, a right coset. The map H -> H a, h -> h a, identifies its left action with H's left regular action. Hence ell^2(K) is the orthogonal direct sum of regular H-representations, with no assumption that H is normal or that K maps onto H.

The new-generator adjacency operator therefore has norm at most 2 sqrt(q). The old-generator operator has norm at most d by the triangle inequality for d unitaries. Their sum has norm at most c = d+2 sqrt(q). The proof only needs a free subgroup of the quotient image and does not assume an unavailable free quotient of a symplectic group.

## 4. Labelled-word upper bound versus distinct-element lower bound

The operator A is formed from a labelled alphabet, retaining the old labels as well as the 2k new ones even when some group elements coincide. Expansion of A^j counts each labelled word once. The coefficient at the identity is a nonnegative integer and counts precisely those words whose product has trivial image under pi. Inverses in the definition of the left regular representation do not change this identity test. The coefficient is bounded in absolute value by ||A||^j <= c^j, including j=0.

Every kernel element in B_S(n) has some word over the actual union S of length at most n. Each such word can be assigned compatible labels in the larger alphabet. Surjectivity from the collected identity-image labelled words to these kernel elements is enough for the upper bound; an injective or equimultiplicative endpoint map is neither assumed nor needed. Duplication of old and new labels, equal images of distinct labels, and identity images can only overcount the numerator, which is safe.

For the denominator, a reduced word in the x_i maps to the corresponding reduced free word in K. Distinct such words therefore represent distinct elements of G. At length n >= 1 their number is 2k q^(n-1), which is at least q^n. The identity provides the n=0 case. The fact that some elements might admit shorter spellings in S does not remove them from B_S(n). Thus the denominator lower bound is a distinct-element bound, not a count of potentially coinciding words.

For every n >= 0, the two bounds in Theorem 1 follow. Since c>1,

sum_(j=0)^n c^j = (c^(n+1)-1)/(c-1) <= [c/(c-1)]c^n.

When c<q, division gives the claimed C theta^n estimate with C=c/(c-1) and theta=c/q in (0,1), also valid at n=0. Writing y=sqrt(q)>0 shows that q>d+2sqrt(q) is equivalent to y>1+sqrt(d+1). Because k can grow without bound with d fixed, the explicit sufficient condition is achievable.

## 5. Free generators in the homology image

The matrices U and V have determinant one and lie on a rank-two symplectic summand. Cubes of the twists about a pair of curves intersecting once, with a twist inverse chosen as needed, realize the displayed signs through the homology transvection formula. Curves on the complementary summand are disjoint from their supports. This realizes both matrices in the actual homology image; full surjectivity onto Sp(2g,Z) is not needed.

For nonzero integer m, U^m sends x to x+3m and sends |x|<1 into |x|>1. The action of V^m is x -> x/(3mx+1). If |x|>1, then

|3mx+1| >= 3|m||x|-1 > |x|,

so its image has modulus less than one. Infinity is sent to 1/(3m), also in that set. To check the particular ping-pong sentence in the report, the rightmost V-power fixes 0; each subsequent alternating U- and V-power then enters the appropriate domain, ending in X for a word beginning with U and ending with V. Such a word moves 0. In the opposite pattern, the rightmost U-power fixes infinity and the same argument ends in Y, moving infinity. Pure powers are nonidentity. Cyclic reduction in the free product reduces every possible nontrivial relation to one of these cases. The asserted freeness is proved.

For the conjugates u^i v u^(-i), a reduced word in the conjugate generators can be collected into nonzero v-powers indexed by successive unequal i. Every intervening u-power is then nonzero. The resulting word in the free basis u,v cannot reduce to the identity, even when an initial or terminal u-power vanishes. Thus the rank-k conjugates are a free basis. Their lifts supply all k required in Theorem 1.

The Torelli application and its immediate extension to subgroups contained in Torelli are valid for the constructed S. They give no conclusion for an earlier arbitrary S without changing its metric.

## 6. The fixed-metric gap and explicit transfer counterexample

For a fixed finite symmetric S, the limit of b_S(n)^(1/n) exists by submultiplicativity. If the corresponding unnormalized quotient adjacency norm is strictly below that limit, choose an intermediate exponential rate if necessary, sum the return-word bounds, and obtain density zero. Thus the report's sufficient condition is correct. Nonamenability only supplies a strict bound relative to the size of the alphabet; it does not give the stronger comparison with the ambient ball growth rate used here.

For F_3 x F_2 with the union of standard factor bases, length is the sum of coordinate lengths. Direct convolution of the F_2 sphere sequence with the F_3 ball sequence gives

|B(n)| = (9*5^n - 8*3^n + 1)/2,
|F_3 x {e} intersect B(n)| = (3*5^n - 1)/2.

The ratio tends to 1/3. Both formulas include n=0. For the product generating set containing coordinate identities, coordinate projections bound length below by the maximum coordinate length. Padding a shorter factor word with identities gives the reverse inequality, proving the max metric. Its balls are products, and the subgroup ratio is 1/(2*3^n-1), tending exponentially to zero.

This is a valid example of a normal infinite-index subgroup with a nonamenable quotient whose zero-density property changes with the finite generating set. It is not a mapping-class-group counterexample. The coset-packing inequality in the report correctly keeps B_S(n+R) on the right; discarding its growth relative to B_S(n) would be invalid.

## 7. Separate audit of the logarithmic appendix

### Conjugacy counting

If h lies in a normal subgroup N, x -> x h x^(-1) maps B_S(n) to N intersect B_S(2n+ell). For any fixed y in a fiber, equality of the conjugates gives y^(-1)x in C_G(h) intersect B_S(2n). This map from the fiber is injective. Therefore the number of image elements is at least b_S(n)/[K(n+1)] under the displayed linear centralizer bound. Both the side of the quotient and the radius 2n are correct.

### Centralizer growth in the ambient metric

The existence of a Torelli pseudo-Anosov in every genus g>=2 is furnished by Farb-Leininger-Margalit's Theorem 1.1. McCarthy's theorem makes its mapping-class centralizer virtually infinite cyclic. An infinite cyclic subgroup of an infinite virtually cyclic group has finite index: intersect it with a fixed finite-index cyclic subgroup and use finite index in that cyclic group. This applies to <h> even in genus two, where finite central torsion does not alter the conclusion.

A pseudo-Anosov acts on its Teichmuller axis by a positive translation. For a fixed base point on this axis, displacement by any word is at most its S-length times the maximum generator displacement L, with L>0. This yields |h^m|_S >= |m| log(lambda(h))/L, including negative m. Finite coset representatives for <h> then show that the number of centralizer elements in an ambient radius-2n ball is at most

M [1 + 2L(2n+R)/log(lambda(h))],

hence at most K(n+1) for a fixed K. Merely knowing that the centralizer is virtually cyclic would not by itself prove ambient linear growth; the appendix correctly supplies the missing undistortion argument.

### All radii, entropy, and sharp infima

Subadditivity gives a finite entropy h_S. It is strictly positive because a fixed free rank-two subgroup has generators of some finite S-length and therefore gives exponentially many distinct elements in ambient balls. For r large, n=floor((r-ell)/2) satisfies 2n+ell<=r and n/r -> 1/2. The logarithmic correction log(K(n+1))/r tends to zero. The conjugacy inequality then gives liminf log(a_S(r))/r >= h_S/2. Dividing by log(b_S(r))/r -> h_S>0 proves D_lower(S)>=1/2. The numerator is at most the denominator, giving D_upper(S)<=1. No numerator growth-limit existence was used.

For each fixed prescribed finite subset F, choose a single finite T containing F and keep d=|T| fixed as k grows. The main theorem gives

D_upper(S_k) <= log(d+2sqrt(2k-1))/log(2k-1) -> 1/2.

This estimate does not require c<q for the finitely many small k. Combining the limiting upper estimate with the universal lower bound proves both stated infima equal 1/2. It does not prove the infima are attained, that D_lower and D_upper agree for a particular generating set, or ordinary density zero for every generating set. These limitations are stated correctly in the appendix.

## 8. Primary-source dependency checks and limitations

- Choi, *Pseudo-Anosovs are exponentially generic in mapping class groups*, arXiv:2110.06678v3: I visually inspected pages 1 and 3, including Theorem A, Corollary 1.1 and Question 1.4. These support the report's enlarged-set versus arbitrary-set distinction. The exceptional set in that work is not the Torelli group. The complete proof of Choi's theorem was not re-audited. Public record: https://arxiv.org/abs/2110.06678 . Retained PDF SHA-256 `b2e09bd3ed89d211c4dc6d8c78ef45d490e65f45f70c0398009bef4dcdaf3ba0`, 368,576 bytes.
- Farb, Leininger and Margalit, *The lower central series and pseudo-Anosov dilatations*, arXiv:math/0603675v2: I visually inspected pages 1 and 2, including the definition and Theorem 1.1. The finite upper bound establishes the required existence, for each g>=2, of a pseudo-Anosov in Torelli. Page 1 recalls the relevant Teichmuller translation property. No numerical dilatation bound is used by the audited proof. Public versioned source: https://arxiv.org/pdf/math/0603675v2 . Retained PDF SHA-256 `097a22dd9d3327b0ce4557a4bb3d7a507bb8066e5aee6fa9480f482b480f0adb`, 361,813 bytes. The public arXiv record dates v2 to 26 August 2007; the retained PDF's title-page date is not treated as a new mathematical revision.
- McCarthy, *Normalizers and centralizers of pseudo-Anosov mapping classes*: I independently read the author-hosted PDF's extracted Theorem 1 and Corollary 2, including its orientable compact negative-Euler-characteristic surface hypothesis, and the corroborating author abstract. Closed genus-g surfaces for g>=2 are covered. Source: https://users.math.msu.edu/users/mccarthy/publications/normcent.pdf ; abstract: https://users.math.msu.edu/users/mccarthy/publications/normcent.abstract.html . The manuscript is dated 8 June 1994 and states it was originally written in 1982. No local PDF bytes were obtained by this audit. The screenshot tool returned no inspectable pixels, so no visual inspection or file hash is claimed. Its established theorem is used as an attributed external input; this audit does not certify a fresh proof audit of that source.

## 9. Acceptance boundary

The accepted result is a proved enlargement theorem, its Torelli specialization, the explicit failure of general generating-set transfer, and the separately proved logarithmic lower bound and sharp infima. The original arbitrary-generating-set density-zero conclusion, any exact logarithmic density for a fixed S, and novelty remain outside acceptance.
