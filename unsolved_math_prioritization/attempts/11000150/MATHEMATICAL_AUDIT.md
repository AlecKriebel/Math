# Independent audit: bounded positive factorizations on one-boundary surfaces

Target: 11000150 / AMR-109-0150. Audit date: 10 October 2026 UTC.

## Verdict

**Accept the boundedness theorem**, with the explicit essential-curve and fixed-genus conventions below. The candidate proves that, for every fixed genus g >= 1, the positive factorizations of a single boundary twist whose factor curves have pairwise geometric intersection at most one form finitely many simultaneous-conjugacy classes. In particular, their lengths have a finite maximum M(g).

**Do not mark the entire maximum-length target solved.** The theorem answers the arbitrary-length clause negatively but does not compute M(g) for g >= 3. The small-genus conclusions M(1)=12 and M(2)=40 are supported after adding the separating-factor argument in Section 7 below. Those values use credited existing results, rather than a new independent upper-bound computation.

No counterexample or remaining logical gap was found in the boundedness proof. Historical novelty is not certified.

The distributed [mathematical report](MATHEMATICAL_REPORT.md) has 22,957 bytes and SHA-256:

`eeb44a07e7503985ef466b882f969b27485f47536c0057ea14163d4b68759db3`.

This AI-assisted, unrefereed audit retains the complete mathematical assessment and separating-factor bridge. Scoped acceptance is not external human peer review, journal acceptance or formal proof-assistant certification.

## 1. Scope and source reconciliation

The relevant source is B. Wajnryb's chapter, *Relations in the mapping class group*, in the Farb volume [W], printed p.126 / PDF133. Its restricted question requires one boundary component, a product of positive twists equal to its boundary twist, and pairwise curve intersections zero or one. It asks both for a maximal length and whether length can be arbitrarily large. Repetitions are explicitly contemplated. The preceding unrestricted question and the subsequent A5 equivalence question are distinct targets.

The proof uses isotopy classes of non-null-homotopic simple closed curves. It permits boundary-parallel factors, which only enlarges the usual essential-nonperipheral convention. Disk-bounding factors must be excluded: their twists are the identity, and arbitrary insertion would invalidate every length bound. This is an explicit mathematical convention, not an omitted hypothesis smuggled into a claim about all curves. The source's surrounding no-positive-relation discussion and Lefschetz setting support this intended convention.

Genus is fixed. There is no genus-independent bound on all lengths: the even-chain construction has length 4g(2g+1). All mapping classes fix the boundary pointwise and preserve orientation. A closed-surface argument would fail at the positivity step.

The source attributes the restricted question to Smith in Wajnryb's chapter; attribution to Penner is incorrect.

## 2. Essential twists and the positive-identity obstruction

The broad claim needed is:

> No nonempty product of positive Dehn twists about homotopically nontrivial curves on a compact oriented surface with boundary is the identity.

It is important not to infer this broad statement merely from BMVHM's notation L(1)=0: its L convention uses nonseparating factors, and its extended length convention still imposes homological essentiality. Instead, use the actual right-veering argument.

HKM defines its positive Dehn monoid using homotopically nontrivial closed curves and proves its inclusion in the right-veering monoid in Lemma 2.5 [HKM, PDF4]. Thus separating and boundary-parallel twists are included. Its endpoint-relative arc order and monoid property occur on PDF2.

Here is the additional faithfulness detail. If a boundary-fixing mapping class fixes every proper arc up to isotopy relative to endpoints, choose a disjoint cut system of proper arcs reducing the surface to a disk. The mapping class can successively be isotoped to fix those arcs pointwise, while retaining previously fixed arcs; on the resulting disk it is isotopic to the identity relative to the boundary by the Alexander trick. Therefore its action on proper arc classes is faithful.

If both f and f^(-1) are right-veering, then, for every proper arc a, right-veering of f gives a <= f(a), while right-veering of f^(-1) applied to f(a) gives f(a) <= a. Antisymmetry of the lifted-endpoint order gives equality. Faithfulness gives f=1. Every homotopically nontrivial Dehn twist is nontrivial in the relative-boundary mapping class group, including a boundary twist; an arc meeting its twisting annulus essentially detects it. Consequently a nontrivial positive twist cannot have right-veering inverse.

A hypothetical identity t1...tn=1 would imply t1^(-1)=t2...tn, a right-veering map. This contradicts the preceding paragraph. The annulus case is also immediate from its integer twist number. No separating-curve loophole remains.

## 3. Exact deletion algebra and Higman

Let u=s1...sm be a subsequence of v, so that

    v=b0 s1 b1 ... sm bm,
    P0=1, Pj=s1...sj.

In any group, with products written in the displayed order,

    v u^(-1) = product over j=0,...,m of (Pj bj Pj^(-1)).

This follows by adjacent cancellation of Pj^(-1)P(j+1)=s(j+1). Each bj is a possibly empty inserted block. Expanding a conjugated block into conjugated letters is legitimate. If the subsequence is proper, at least one inserted letter remains.

In the mapping class group every such conjugated letter is again a positive twist about a homotopically nontrivial curve. The set of all these twists, not merely the original alphabet, is conjugation invariant. Therefore equality eval(u)=eval(v) would produce a nonempty positive identity, which is impossible.

For a fixed finite curve alphabet, a fiber of evaluation is consequently an antichain for subsequence. Higman's lemma makes every such fiber finite. The report's minimal-bad-sequence proof is valid: after extracting a common last letter, any good pair in the shortened sequence lifts to a forbidden good pair of original words. Empty words and repeated letters are covered. Equal-length distinct words cannot be proper subsequences, and an infinite fiber can be enumerated without duplication.

## 4. Support-size bound and simultaneous realization

For S(g,1), H1(S;F2) has 2^(2g) elements, and its mod-two intersection pairing is alternating. If c,d have the same mod-two homology class, their geometric intersection number is even. Under i(c,d)<=1 it must be zero.

Remove the possible boundary-parallel isotopy class. Every homology fiber is then a family of pairwise nonisotopic essential nonperipheral classes of pairwise zero intersection. They can be realized simultaneously disjointly and extended to a pants decomposition, so each fiber has at most 3g-2 members. This proves

    number of distinct support classes <= 2^(2g)(3g-2)+1.

The zero homology class and separating curves are included. The estimate also holds for g=1. It is deliberately coarse and bounds the number of letters, not the number of their occurrences.

A hyperbolic metric with geodesic boundary exists because g>=1. The simple geodesic representatives of all nonperipheral classes realize minimal pairwise intersections simultaneously. Different geodesics cannot overlap along an interval. A finite multiple crossing can be locally perturbed into ordinary transverse double crossings without changing whether each pair crosses. A possible peripheral representative is placed in a disjoint boundary collar. Thus a bounded support size yields a bounded finite embedded graph.

## 5. Finite support orbits, including complementary annuli

The finite ribbon-graph argument must remember more than the intersection graph. The candidate does so correctly. Record:

1. The embedded union as a graph, with a dummy bivalent vertex on every isolated circular component.
2. Cyclic orders at vertices, the pairing through every crossing, and the constituent labeled curve cycles.
3. The partition of regular-neighborhood boundary circles among complementary components.
4. Each complementary component's genus and the component containing the original boundary circle.

All graph sizes are bounded by the support-size and intersection bounds. The regular neighborhood is determined by the ribbon graph. There are finitely many complementary-boundary partitions; each complementary genus is at most g; and the number of complement components is bounded by the number of regular-neighborhood boundary circles plus one.

Two embeddings with identical records admit compatible orientation-preserving homeomorphisms of their regular neighborhoods and complementary surfaces. Prescribed boundary circle maps extend after collar adjustments. There is no extra integer gluing parameter that creates new ambient-homeomorphism orbits: circle attachment maps of the required orientation are isotopic. This handles disconnected supports, non-filling supports, annular complement components, and isolated curve components. A final collar adjustment makes the ambient homeomorphism pointwise fixed on the original boundary without moving the support.

Hence there are finitely many support orbits for the exact boundary-fixing mapping class group used in the target.

## 6. Combining the finite statements

Choose one support representative from each finite orbit. Simultaneous conjugation carries an admissible factorization to a positive word over the corresponding fixed finite alphabet. The boundary twist remains unchanged because it is central in this relative-boundary mapping class group. Every alphabet has only finitely many words evaluating to this target, by Section 3. A finite union is finite.

This proves finite simultaneous-conjugacy classes, not merely bounded length. It does not assert finiteness of all mapping-class-group factorizations without the pairwise-intersection condition, and it does not identify Hurwitz or positive-Artin equivalence classes.

The standard even-chain relation on 2g curves gives an admissible word of length 4g(2g+1). This proves nonemptiness, so the finite upper bound is an attained maximum rather than merely a vacuous bound. Higman's lemma does not provide the maximum from the alphabet size alone. The proof does not give an effective stopping criterion for exhaustive word enumeration.

## 7. Verified additional bridge: separating factors and small genus

First handle a boundary-parallel factor. Since t_delta is central, write any factorization containing it as t_delta^m W=t_delta with m>=1. Then t_delta^(m-1)W=1. The positive-identity obstruction implies m=1 and W is empty. Such a factorization has length one.

Now assume there are no boundary-parallel factors and g>=2. Suppose one factor curve c is separating. Every closed curve crosses a separating curve an even number of times; therefore the intersection-at-most-one condition gives i(c,cj)=0 for every factor cj. Cap the sole boundary with a disk. Each factor curve, and c itself, remains essential. Indeed, let D0 be the attached disk. If an original curve bounds a disk D after capping, D0 lies entirely on one side of that curve. If D0 is outside D, D was already a disk in the original surface. If D0 is inside D, removing its interior from D gives an annulus between the curve and the original boundary. These alternatives say the curve was disk-bounding or boundary-parallel, both excluded in the present case. The capped monodromy is a nonempty positive identity whose twist factors all preserve the essential isotopy class of c.

This contradicts Smith's no-invariant-curve theorem [S, Theorem 1.3 and Proposition 4.2], equivalently the filling corollary [S, Corollary 4.3]. The cited statement applies to positive monodromy on a closed fiber of genus at least two. For completeness, the required construction starts with the fiber product over a disk and attaches the usual Lefschetz two-handles along the ordered curves with framing one less than the fiber framing. Each local singularity has the positive complex model. The identity total monodromy on the closed fiber permits closing the base by a second disk. The original lift of the monodromy to the one-boundary surface supplies a section of square -1. In particular the fiber is homologically nonzero because it intersects that section once, and the Thurston–Gompf symplectic construction for a positive Lefschetz fibration with homologically nonzero fiber applies (also summarized in [S, PDF1]). All vanishing cycles remain essential, so there are no disk-bounding vanishing cycles or relative-minimality obstruction. Only the nonempty case is used. The assertion is not applied to a trivial surface bundle or genus-one hyperbolic model.

Thus every admissible factorization other than the peripheral singleton has only nonseparating factors. BMVHM Theorem A gives the existing unrestricted upper bounds 12 in genus one and 40 in genus two. The two-curve and four-curve even chains attain those lengths under the pairwise condition. Consequently

    M(1)=12, M(2)=40,
    4g(2g+1)<=M(g)<infinity for every g>=3.

The exact values for g>=3 remain undetermined by this work. The unrestricted genus>=3 infinite-length theorem is compatible with the new restriction: its long words must eventually have some pair of factor curves with geometric intersection at least two.

## 8. Prior work and acceptance boundary

The positive-identity obstruction, right-veering theory, Higman's lemma, elementary surface classification, chain relation, Smith filling theorem, and BMVHM low-genus maxima are credited inputs. Cossu–Tringali had already applied Higman to abstract noncommutative factorization, as recorded in their Theorem 4.10, Theorem 4.11 and Lemma 5.7 [CT]; the generic mechanism is not new. The contribution assessed here is the combination for fixed-genus pairwise-intersection-constrained boundary factorizations.

Bounded primary-literature searches for the exact Smith question and for combinations of Higman, Dehn twists, finite alphabets, and positive factorizations did not locate this exact boundedness argument. Such search negatives do not certify priority. The numerical maximum and extremizer classification in higher genus are outside the established result.

## References and actually inspected primary pages

[W] B. Wajnryb, *Relations in the mapping class group*, Chapter 8 in B. Farb (ed.), *Problems on Mapping Class Groups and Related Topics* (2006). https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf . Original problem visually inspected on PDF133 / printed126; chain relation visually inspected on PDF132 / printed125.

[HKM] K. Honda, W. H. Kazez, G. Matic, *Right-veering diffeomorphisms of compact surfaces with boundary I*, arXiv:math/0510639v1 (28 October 2005). https://arxiv.org/abs/math/0510639 . PDF2 and PDF4 visually inspected for the endpoint-relative definition, monoid, and all-homotopically-essential twist inclusion.

[S] I. Smith, *Geometric monodromy and the hyperbolic disc*, arXiv:math/0011223v1 (27 November 2000); *Quarterly Journal of Mathematics* 52 (2001), 217–228. https://arxiv.org/abs/math/0011223 . PDF1, PDF3, PDF4, PDF10 and PDF11 visually inspected, including the introductory symplectic construction, Theorem1.3, genus>=2 convention, Proposition4.2 and Corollary4.3.

[BMVHM] R. I. Baykur, N. Monden, J. Van Horn-Morris, *Positive factorizations of mapping classes*, arXiv:1412.0352v2 (18 August 2015); *Algebraic & Geometric Topology* 17 (2017), 1527–1555. https://arxiv.org/abs/1412.0352 . PDF2 visually inspected for Theorem A and its nonseparating convention; Section2.1 text inspected for the right-veering argument.

[H] G. Higman, *Ordering by divisibility in abstract algebras*, *Proceedings of the London Mathematical Society* (3) 2 (1952), 326–336. https://doi.org/10.1112/plms/s3-2.1.326 . Publisher metadata checked; no original full-paper download claimed. The precise finite-alphabet lemma is independently proved in the candidate report.

[CT] L. Cossu and S. Tringali, *Factorization under local finiteness conditions*, arXiv:2208.05869v3 (16 March 2023); *Journal of Algebra* 630 (2023), 128–161. https://arxiv.org/abs/2208.05869 . Theorem 4.10, Theorem 4.11 and Lemma 5.7 text inspected in the retained primary PDF.
