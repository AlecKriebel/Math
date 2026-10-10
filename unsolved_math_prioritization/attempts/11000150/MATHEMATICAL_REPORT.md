# Bounded positive boundary-twist factorizations with pairwise intersection at most one

Target: 11000150 / AMR-109-0150. First substantive attempt, 10 October 2026 UTC.

## Result and exact remaining question

For each fixed integer genus g >= 1, positive factorizations of the boundary twist on a compact connected oriented genus-g surface with one boundary component, whose factor curves have pairwise geometric intersection at most one, have **bounded length**. In fact, there are only finitely many such ordered factorizations modulo simultaneous orientation-preserving boundary-fixing conjugation. Repeated factors are allowed.

This report gives a proof of that boundedness assertion, and obtains the credited low-genus maxima M(1) = 12 and M(2) = 40. It does **not** determine the exact maximum for every genus. Thus it answers the source's arbitrary-length subquestion negatively, while the full maximum-length question remains partially unresolved here. A separate independent audit checks the proof and its scope. No claim of historical novelty is certified by the bounded literature search.

The proof uses: (i) the absence of a nonempty positive essential Dehn-twist identity on a surface with boundary, (ii) Higman's finite-alphabet subsequence lemma, and (iii) finiteness of topological types of 1-systems on a fixed surface. The algebraic subsequence step and the requisite 1-system finiteness are proved below, as is the finite-alphabet version of Higman's lemma.

## 1. Source-faithful setup

Let S = S(g,1) be compact, connected and oriented, with genus g >= 1 and boundary delta. Let Mod(S) consist of orientation-preserving homeomorphisms fixing the boundary pointwise, modulo isotopy relative to the boundary. For an unoriented simple closed curve c, write t_c for its positive Dehn twist. Curve isotopy is taken in S. The target element is t_delta, equivalently the twist about an interior curve parallel to delta.

An admissible ordered factorization is

    t_(c1) t_(c2) ... t_(cn) = t_delta,
    i(ci,cj) <= 1 for every i,j.

Each factor curve is required to be non-null-homotopic. We allow a boundary-parallel curve in this report's broader convention; excluding peripheral curves only restricts the set and leaves the boundedness theorem valid. In particular, no identity twist about a disk-bounding curve is allowed. Isotopic repetitions contribute repeatedly to n, while the support consists of distinct isotopy classes. The intersection condition is geometric; a curve has intersection zero with a repeated copy of itself.

This is the restricted Smith question in B. Wajnryb's chapter, printed p.126 / PDF page 133 of [W]. The preceding unrestricted question is on p.125 and is a different target. The question is attributed there to Smith, and the chapter author is Wajnryb. The original PDF was inspected visually. The genus-two D6/A5 discussion and the ensuing algebraic question are motivation and a separate finer classification issue, not hypotheses or a proved classification used here.

Boundary fixing is essential. Capping delta changes t_delta to the identity and removes the positive-identity obstruction. Allowing negative factors, adding null-homotopic factors, or letting genus vary also changes the conclusion. Indeed the familiar chain construction below has lengths growing quadratically with g.

For g = 0 the surface is a disk: t_delta is the identity and there are no non-null-homotopic simple closed curves. Thus there is no admissible nonempty factorization; the empty factorization has length zero if it is permitted. The substantive theorem concerns g >= 1.

## 2. Positivity has no nonempty identity

**Lemma 2.1.** On a compact connected oriented surface with nonempty boundary, a nonempty product of positive Dehn twists about non-null-homotopic curves is not the identity.

Here and below surfaces such as a disk, on which there are no admissible curves, give the vacuous case. The annular case is also immediate from Mod(annulus) = Z.

**Justification.** We recall the arc argument so that the precise positivity hypothesis is explicit. For oriented properly embedded arcs based at the same boundary point and ending at the same prescribed boundary point, use the order obtained from their lifts starting at a fixed lift of the base point in the universal cover. A boundary-fixing orientation-preserving homeomorphism preserves this order. A homeomorphism is right-veering when it takes every such arc weakly to the right. The identity is right-veering, and the composition of two right-veering maps is right-veering: for every arc a,

    a <= h(a) <= f(h(a)).

Every positive Dehn twist is right-veering, and an essential Dehn twist is a nontrivial mapping class. The action on boundary-endpoint-relative proper arcs detects nontriviality: a homeomorphism fixing every such arc fixes a finite disjoint arc system cutting the surface into a disk, can be isotoped to fix that system pointwise, and is then isotopic to the identity on the disk relative to its boundary. Thus a nontrivial right-veering map moves some proper arc strictly right. This applies to every non-null-homotopic twist curve, including separating and boundary-parallel curves. Equivalently, a transverse proper arc in the annular twist model directly detects the displacement. Hence the inverse of a positive essential twist is not right-veering: it sends the image of that particular arc strictly left.

If t1 ... tn = 1 with n >= 1, then t1^(-1) = t2 ... tn. The right side is right-veering, including the empty product when n = 1, whereas the left side is not. This contradiction proves the lemma.

These facts are the usual right-veering argument of Honda–Kazez–Matic [HKM, Definition 2.1 and Lemma 2.5, PDF pp.2 and 4]. Their Dehn-positive monoid expressly permits homotopically nontrivial curves and includes the separating case. They are also summarized and applied in [BMVHM, Section 2.1, Propositions 3 and 5, PDF pp.5–6]. The identity obstruction is explicitly credited to Smith in [W, printed p.124]. This report does not claim that obstruction as a new theorem. We use the arc argument for all non-null-homotopic curves, rather than silently importing the narrower nonseparating convention used for the length function L in [BMVHM].

## 3. The proper-subsequence obstruction

**Lemma 3.1 (group-theoretic form).** Let G be a group, and P a conjugation-invariant subset such that no nonempty product of elements of P equals 1. Fix a finite alphabet A whose letters are assigned elements of P. For any h in G, only finitely many words over A evaluate to h.

Before proving finiteness, we prove that two distinct words with the same value cannot be comparable by the scattered-subword (subsequence) relation.

Suppose u = s1 ... sm is a subsequence of v. Write the inserted blocks as

    v = b0 s1 b1 s2 b2 ... sm bm,

where each bj is a possibly empty word. Set P0 = 1 and Pj = s1 ... sj in G for 1 <= j <= m. Direct cancellation gives

    v u^(-1) = (P0 b0 P0^(-1))(P1 b1 P1^(-1)) ... (Pm bm Pm^(-1)).

Every block conjugate on the right splits into the conjugates of its individual letters. If u is a proper subsequence, at least one inserted letter exists. Conjugation invariance therefore makes the right side a nonempty product of members of P. It cannot be 1. Consequently eval(u) != eval(v).

The case m = 0 is included: the empty word is a subsequence of every word, and a nonempty positive word cannot have its value 1.

**Finite-alphabet Higman lemma.** Every infinite sequence of finite words over a finite alphabet contains two terms u_i, u_j with i < j such that u_i is a subsequence of u_j.

For completeness, suppose a bad infinite sequence existed, meaning no such pair occurs. Construct a minimal bad sequence w0,w1,... by choosing each wi with minimum length among words that can extend the already chosen finite prefix to an infinite bad sequence. No wi is empty. Write wi = vi ai with last letter ai. Some last letter a occurs at an infinite subsequence of indices i0 < i1 < .... Consider

    w0, ..., w_(i0-1), v_(i0), v_(i1), v_(i2), ... .

If this were bad, its shorter term v_(i0) would contradict minimality at index i0. It must therefore contain a good pair. Such a pair cannot consist of two initial w terms, by the original badness. If an initial w term is a subsequence of some v_(ik), it is also a subsequence of w_(ik), again impossible. Finally, if v_(ij) is a subsequence of v_(ik) for j < k, appending their common last letter a shows that w_(ij) is a subsequence of w_(ik), also impossible. These exhaust the cases and prove the lemma. This is the classical minimal-bad-sequence proof of Higman's result [H].

Now an infinite fiber of the evaluation map would be an infinite set of distinct words. Higman's lemma would give a proper-subsequence pair in that fiber, contradicting the preceding identity. This proves Lemma 3.1.

**Corollary 3.2.** Fix any finite collection C of essential curve isotopy classes on a bordered surface and any mapping class h. There are only finitely many positive words in the letters {t_c : c in C} that equal h.

Apply Lemma 3.1 to the set of all positive essential Dehn twists: conjugation carries t_c to t_(f(c)), and preserves essentiality and twist sign. Lemma 2.1 supplies the no-positive-identity hypothesis. Notice that finite generation alone is not the argument; both conjugation invariance and the positive-identity obstruction are used explicitly. No injectivity of an Artin-group representation is assumed.

## 4. Finitely many 1-system supports up to homeomorphism

We give a direct proof including separating and peripheral curves.

**Lemma 4.1 (a coarse support bound).** A collection C of distinct non-null-homotopic curve isotopy classes on S(g,1), g >= 1, satisfying i(c,d) <= 1 has

    |C| <= N_g := 2^(2g)(3g - 2) + 1.

**Proof.** First remove the possible boundary-parallel isotopy class, of which there is at most one. Assign each remaining class c its mod-two homology class [c] in H1(S;F2), a vector space with 2^(2g) elements. If [c] = [d], then their mod-two intersection is [c] dot [c] = 0, because the intersection pairing is alternating. Geometric intersection reduced modulo two equals this pairing. Since i(c,d) is either zero or one, it must be zero.

Thus each homology fiber consists of pairwise disjoint, pairwise nonisotopic, essential nonperipheral curves. Such curves can be realized simultaneously disjointly and extended to a pants decomposition; their number is at most 3g - 3 + 1 = 3g - 2. This includes the zero homology class and therefore includes separating curves. Summing over all mod-two classes and restoring the optional peripheral class proves the stated bound. The estimate is deliberately coarse and is a bound on the number of distinct curve classes, **not** a bound on factorization length. In particular, it does not discard repetitions.

**Lemma 4.2 (support-orbit finiteness).** There are only finitely many orientation-preserving, boundary-fixing mapping-class-group orbits of such collections C.

**Proof.** Equip S with a hyperbolic metric with geodesic boundary. Represent every nonperipheral class by its simple geodesic representative; these representatives realize every pair's geometric intersection simultaneously. Put the possible peripheral curve in a collar disjoint from the others. If several geodesics pass through the same point, perturb them in a sufficiently small disk to make all intersections ordinary transverse double points. There are finitely many participating arcs, and a small generic perturbation preserving their endpoint order makes each formerly intersecting pair intersect once and creates no other pairwise intersections. Thus the total number of crossings remains at most |C|(|C|-1)/2.

The union of these representatives is an embedded graph with four-valent crossing vertices. For every component that is an isolated circle, add one two-valent auxiliary vertex. Label the constituent curve cycles by 1,...,|C|; ordering the support for this encoding costs only finitely many choices. By Lemma 4.1 the number of vertices, edges, cycle labels, crossing pairings, and cyclic orders at vertices are all bounded in terms of g. There are therefore only finitely many possible labeled ribbon graphs. Each ribbon graph determines its oriented regular neighborhood R, together with the marked curve cycles, up to orientation-preserving homeomorphism.

To recover its embedding in S, record the components of the closure of S minus R. Each is a compact oriented surface. Record which of the finitely many boundary circles of R are attached to each complementary component, which component carries the sole distinguished boundary delta, and the genus of each component. The number of these components is bounded by the number of boundary circles of R plus one, and every genus is at most g. Hence there are only finitely many such records. Empty support can be handled separately.

The classification of compact oriented surfaces shows that two embeddings with the same record are related by an orientation-preserving homeomorphism: use the ribbon-graph homeomorphism on R and homeomorphisms of the recorded complementary surfaces, and match them on each boundary circle. Orientation-compatible circle gluings do not carry an extra integer invariant; they are isotopic, and collar adjustments extend the required boundary maps. Thus annular complementary components do not create infinitely many hidden gluing choices. Finally adjust the homeomorphism in a collar of delta to fix delta pointwise, without changing any curve class. This proves finiteness of the required mapping-class orbits.

## 5. Uniform boundedness and finite ordered factorizations modulo conjugacy

**Theorem 5.1.** For every g >= 1, there are finitely many admissible ordered factorizations of t_delta modulo simultaneous conjugation by Mod(S(g,1)). Consequently their lengths have a finite maximum M(g).

**Proof.** Choose one finite support representative C_r from each of the finitely many orbits in Lemma 4.2. An admissible factorization has some support C. Choose f in Mod(S) carrying C to C_r. Conjugating its ordered factors by f gives a positive word in the fixed finite alphabet {t_c : c in C_r}. Its product is still t_delta: f fixes the boundary and f t_delta f^(-1) = t_delta. Corollary 3.2 says that only finitely many words over this alphabet evaluate to t_delta. Take the union of these finite sets over the finitely many representatives r. It is finite and contains a representative of every simultaneous-conjugacy class of admissible ordered factorizations.

The admissible set is nonempty. The standard even chain of 2g curves satisfies

    (t_(a1) ... t_(a(2g)))^(4g+2) = t_delta.

Adjacent chain curves meet once and nonadjacent ones are disjoint. Repetitions in the displayed power add no forbidden intersections. Its length is 2g(4g+2) = 4g(2g+1). This is the classical chain relation, displayed in [W, printed p.125, relation (3)]. Thus the finite set of attained lengths is nonempty and has a maximum, with

    4g(2g+1) <= M(g) < infinity.

The upper bound asserted here is existential. The proof does not identify M(g) with the coarse support bound N_g, supply a computable formula for M(g), or give an effective stopping criterion for an exhaustive search. Higman's lemma supplies finiteness of each fiber, not a numerical bound on its longest member from alphabet size alone.

## 6. Small genus and limits of the claim

For genus one, every essential nonperipheral curve is nonseparating. Abelianization of Mod(S(1,1)) is Z, taking every nonseparating positive twist to 1 and the boundary twist to 12 [BMVHM, Proposition 1]. Thus every factorization without a peripheral factor has length exactly 12. A peripheral factor can occur only as the sole factor: after commuting its occurrences to the front, an equality t_delta^m W = t_delta with m >= 1 gives t_delta^(m-1) W = 1, and Lemma 2.1 forces m = 1 and W empty. The two-curve chain realizes length 12. Hence M(1) = 12 whether or not peripheral factors are permitted.

**Lemma 6.1 (exclusion of separating factors).** An admissible factorization on S(g,1), g >= 2, is either the single peripheral twist, or all of its factor curves are nonseparating.

**Proof.** The peripheral-factor cancellation argument just given works for every g >= 1. We may therefore assume that every factor curve is nonperipheral. Suppose a separating curve c occurs. Every simple closed curve has even geometric intersection with a separating curve: every crossing into either side is paired with a crossing out. The intersection-at-most-one assumption consequently says that every factor curve is disjoint from c.

Cap delta with a disk. All the factor curves remain essential on the resulting closed genus-g surface: an essential curve that became null-homotopic after this sole capping would have been parallel to delta before capping. In particular c remains essential, since its two sides both have positive genus. The boundary-twist factorization becomes a nonempty positive identity on the closed surface. By the standard monodromy construction it gives a nontrivial genus-g Lefschetz fibration over S2; the original boundary-twist relation also supplies a section of square -1. The fibre is homologically nonzero (it intersects that section once), so the Thurston–Gompf symplectic construction for positive Lefschetz fibrations with homologically nonzero fibre applies; the symplectic construction is also summarized in [S, PDF p.1]. Its vanishing cycles are precisely the capped factor curves, all essential.

Smith's invariant-curve theorem [S, Theorem 1.3 and Proposition 4.2], equivalently its filling consequence [S, Corollary 4.3], states that such a nontrivial Lefschetz fibration in genus at least two has no essential curve disjoint from all its vanishing cycles. The capped curve c is exactly such a curve. This contradiction proves the lemma. This use of Smith's prior theorem is separate from and unnecessary for the Higman boundedness proof.

Now [BMVHM, Theorem A] gives the upper bound 40 for every nonseparating factorization of t_delta in genus two. Lemma 6.1 reduces our broader convention to that case or the singleton peripheral factor, and the four-curve chain realizes length 40 while satisfying the pairwise condition. Hence **M(2) = 40**, with or without peripheral factors. This is a deduction from credited prior results and the parity restriction, rather than an asserted classification of A5/D6 configurations or Hurwitz classes.

For g >= 3, [BMVHM, Theorem A] permits arbitrarily long unrestricted nonseparating factorizations of one boundary twist. This does not conflict with Theorem 5.1: their supports cannot all satisfy the intersection-at-most-one condition. Theorem 5.1 gives a genuine obstruction to transferring that unrestricted construction into the restricted Smith problem.

No classification up to Hurwitz moves, positive Artin equivalence, or T-moves is proved here. Finiteness of ordered factorizations modulo simultaneous conjugacy does not identify any of those equivalence classes.

## 7. Audit boundaries and remaining work

The exact remaining mathematical task is to compute M(g) for g >= 3 and to prove any asserted extremizing classification. Lemma 6.1 shows that allowing separating or peripheral essential factors does not change the maximum. This report gives no answer to the subsequent A5 Hurwitz-classification question. It also gives no fully explicit genus-dependent upper-bound formula.

The proof has four independently inspectable interfaces: the essential-twist right-veering obstruction; the exact insertion/deletion identity; finiteness of 1-system support orbits including complementary annuli and boundary fixing; and the centrality step that makes a support-normalizing conjugation preserve the target. The theorem is established by the displayed mathematical arguments.

## Review status

The accompanying [mathematical audit](MATHEMATICAL_AUDIT.md) accepts the fixed-genus boundedness and finite simultaneous-conjugacy conclusions, the separating-factor exclusion, and the credited low-genus maxima. This AI-assisted, unrefereed proof-and-audit edition is not external human peer review, journal acceptance or formal proof-assistant certification. The exact maximum for g >= 3, an explicit genus-dependent upper-bound formula and extremizer classifications remain unresolved by this work. No historical novelty or current-openness certification is claimed.

## References

[W] B. Wajnryb, *Relations in the mapping class group*, Chapter 8 in B. Farb (ed.), *Problems on Mapping Class Groups and Related Topics*, 2006; author-hosted full volume, https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf. Relevant printed pp.124–126 / PDF pp.131–133. Source question on p.126 is attributed there to Smith.

[BMVHM] R. Inanc Baykur, Naoyuki Monden, Jeremy Van Horn-Morris, *Positive factorizations of mapping classes*, arXiv:1412.0352v2 (18 August 2015), https://arxiv.org/abs/1412.0352; published in *Algebraic & Geometric Topology* 17 (2017), 1527–1555. Theorem A, Proposition 1, and Propositions 3 and 5 are the relevant statements. The retained PDF version is identified in [SOURCE_METADATA.json](SOURCE_METADATA.json).

[HKM] Ko Honda, William H. Kazez, Gordana Matic, *Right-veering diffeomorphisms of compact surfaces with boundary I*, https://arxiv.org/abs/math/0510639. The right-veering monoid and containment of positive twists are credited background.

[H] Graham Higman, *Ordering by divisibility in abstract algebras*, *Proceedings of the London Mathematical Society* (3) 2 (1952), 326–336, https://doi.org/10.1112/plms/s3-2.1.326. The finite-alphabet lemma needed here is proved in Section 3; publisher metadata was checked, with no claim that its full original article was downloaded.

[S] Ivan Smith, *Geometric monodromy and the hyperbolic disc*, arXiv:math/0011223v1 (27 November 2000), https://arxiv.org/abs/math/0011223. Theorem 1.3 is on PDF p.3; the genus-at-least-two convention is on PDF p.4; Proposition 4.2 and Corollary 4.3 are on PDF pp.10–11. The retained preprint is identified by hash; no claim of byte identity with a later published version is made.

[CT] Laura Cossu and Salvatore Tringali, *Factorization under local finiteness conditions*, arXiv:2208.05869v3 (16 March 2023), https://arxiv.org/abs/2208.05869; *Journal of Algebra* 630 (2023), 128–161, https://doi.org/10.1016/j.jalgebra.2023.04.014. Their Theorem 4.10 records Higman's lemma, and Theorem 4.11 and Lemma 5.7 illustrate its prior use in noncommutative factorization theory. Accordingly the generic Higman/factorization mechanism is not claimed as an unprecedented method here. The specific surface theorem above is proved directly rather than asserted to follow from an unchecked identification with their abstract hypotheses.
