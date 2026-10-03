# Three surface fiberings on a complex surface: restricted obstructions

Problem: 2772 / KP-2.24

**Status: UNSOLVED.** No complex example with three required fiberings, and no general nonexistence theorem, is established here. The propositions below are restricted obstructions and necessary conditions. Their novelty is not claimed. Independent review is pending.

## 1. Exact source and scope

The [K3 problem list, page 105, Problem 2.24](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf) asks whether a complex surface can have at least three non-isomorphic surface-bundle structures. Its remarks identify the hyperbolic-base/hyperbolic-fiber setting, classical double Kodaira fibrations, and the distinction from smooth examples without complex structures. The bare sentence does not repeat every genus or equivalence convention. This attempt addresses the intended compact hyperbolic/Kodaira setting; it does not claim a solution based on elliptic genera or a different notion of equivalence.

The directly relevant primary reference is Claudio Llosa Isenrich and Pierre Py, [Mapping class groups, multiple Kodaira fibrations, and CAT(0) spaces](https://www-fourier.univ-grenoble-alpes.fr/~py/Documents/Articles/llosa-isenrich-py-math-annalen.pdf), Math. Ann. (2021), DOI 10.1007/s00208-020-02125-y. Its Definition 1 distinguishes fibrations by their fundamental-group kernels. For holomorphic submersions with connected fibers this agrees with distinguishing their fiber foliations. Theorem 2 forces a triple's joint fundamental-group image to have finite index in the product of the three base surface groups. Proposition 26 proves that the normalization of its product image is smooth. The same paper explicitly leaves the existence question open and asks whether the image must be ample. No later full resolution was verified in the present search.

Catanese's [Kodaira fibrations and beyond](https://www.mathe8.uni-bayreuth.de/de/team/prof-fabrizio-catanese-old/pdf/156.pdf), Question 10, is another primary formulation. Neither a complex structure on a smooth many-fibration construction nor a third fibration on a double example follows from the definitions.

Related dataset ID30003293 includes this same existence question plus a separate relative-irregularity question. The shared existence component should not be counted as a fresh independent target later; the additional irregularity question is not resolved here.

## 2. Product and finite-étale-product obstruction

**Proposition 1.** Let C and D be compact connected Riemann surfaces, and let B have genus at least two. Every holomorphic map f:C×D→B factors through one of the projections. If f is a submersion with connected fibers, its factor map is an isomorphism. Consequently a complex surface with a finite étale cover by C×D has at most two distinct holomorphic submersions with connected fibers onto hyperbolic curves, distinguished by their fibers.

**Proof.** The topological degree of f restricted to {c}×D is constant as c varies, by homotopy invariance and connectedness. If that degree is zero, every such holomorphic map is constant, so f factors through C. If it is positive, all these restrictions are nonconstant. Differentiating f in any fixed tangent direction at c gives a holomorphic section of (f|{c}×D)*TB over D. This line bundle has negative degree, because deg(TB)=2−2g(B)<0. It has no nonzero holomorphic section. Thus df vanishes in all C-directions at every point, and f factors through D.

If a factor map between compact curves has degree d>1, a regular fiber of f is a disjoint union of d copies of the other factor. Connected fibers imply d=1, hence the factor map is an isomorphism.

Now let q:C×D→X be finite étale and f:X→B a holomorphic submersion with connected fibers. The composite f∘q is also a submersion and factors through C or D. Its factor map is unramified, since its derivative is everywhere nonzero. Therefore the pullback tangent distribution of the f-fibers is one of the two product tangent distributions.

Two fibrations on X that induce the same distribution upstairs induce the same distribution downstairs, because q is a local biholomorphism and surjective. Their connected fibers are exactly the maximal connected leaves of that distribution. Equivalently, the second map is constant on every fiber of the first and descends to a map of bases; the connected-fiber condition in both directions makes the descended map an isomorphism. There are at most two distributions upstairs. ∎

This eliminates an elementary product/finite-étale-product construction, not ramified double Kodaira constructions in general. No claim that every candidate is covered étale by a product is made.

## 3. Smooth ample divisors cannot supply the triple

**Proposition 2.** Let Y=C₁×C₂×C₃, with all three curves compact of genus at least two. If S⊂Y is a smooth ample divisor, no restricted projection S→Cᵢ is a holomorphic submersion.

**Proof.** Fix i=1 and put L=O_Y(S), D=c₁(L), Kⱼ=c₁(pⱼ*Ω¹_Cⱼ). Let s be the section of L cutting out S. On its zero set, its derivative is intrinsically a bundle morphism ds:T_Y|S→L|S. Restrict to the vertical tangent bundle for p₁:

E=p₂*TC₂ ⊕ p₃*TC₃.

If p₁|S is a submersion, then ds|E is nowhere zero. Indeed, at a point of S, smoothness makes ds nonzero. If it vanished on E, its kernel T_S would equal E, making the projection derivative zero. Conversely, a nonzero restriction to E allows a vector with any prescribed C₁ component to be adjusted vertically into ker(ds).

Thus ds|E would be a nowhere-zero section of the rank-two bundle E*⊗L on S. A nowhere-zero section yields a trivial line subbundle and a line-bundle quotient, so its second Chern class must vanish. But its Chern number is

∫_S c₂(E*⊗L) = ∫_Y D(D+K₂)(D+K₃)
                 = D³ + D²(K₂+K₃) + DK₂K₃ > 0.

Here D is ample, so D³>0. Each Kⱼ is pulled back from a positive-degree line bundle on a curve and is nef; all remaining displayed intersection products are nonnegative. This contradiction proves the claim. The other two projections follow by symmetry. ∎

**Corollary.** For a hypothetical triple of Kodaira fibrations, its product image in C₁×C₂×C₃ cannot be both normal and ample.

**Proof.** The cited Proposition 26 says its normalization is smooth. If the image is normal, the image itself is smooth. The three induced projections are submersions: the original submersions factor through the image, and the derivative chain rule forces surjectivity of the induced derivatives. A normal ample image would then contradict Proposition 2. ∎

This corollary deliberately does not replace “normal and ample” by “ample.” A nonnormal image can have a smooth normalization, and the derivative/normal-bundle computation on a smooth divisor does not apply to a singular divisor by assertion. Likewise, finite-index image on π₁ alone does not establish ampleness.

For a useful exact check, if D=aH₁+bH₂+cH₃ is a product-type ample class, ∫H₁H₂H₃=1 and Hᵢ²=0, the obstructing Chern number for projection 1 equals

a[6bc+2c(2g₂−2)+2b(2g₃−2)+(2g₂−2)(2g₃−2)],

which is positive for all a,b,c>0. At a=b=c=1 and g₂=g₃=2, it is 18. The code checks this expansion in the square-zero intersection ring; it is not a search for complex surfaces.

## 4. Elementary numerical necessities

Suppose a triple exists, with base genera b₁,b₂,b₃ and fiber genera g₁,g₂,g₃. Then

b₁(X) ≥ 2(b₁+b₂+b₃),
gᵢ ≥ bⱼ+bₖ for {i,j,k}={1,2,3},
e(X)=4(bᵢ−1)(gᵢ−1) for each i.

For the first inequality, use the cited finite-index image theorem. Restriction H¹(G;Q)→H¹(H;Q) from a group to a finite-index subgroup is injective: a homomorphism to Q vanishing on H vanishes on every element after taking a positive power into H. The epimorphism π₁(X)→H also induces an injection on H¹. The target product G has first Betti number 2(b₁+b₂+b₃).

For the second inequality, the exact fundamental-group sequence of a connected surface bundle gives b₁(X)≤2bᵢ+2gᵢ. Combining yields the claim. The Euler identity follows from Euler-characteristic multiplicativity for a surface bundle. These inequalities are necessary, not sufficient, and are mutually consistent; for example bᵢ=2, gᵢ=4 gives e=12 and the same lower/upper first-Betti bound. This numerical tuple is not asserted to be geometrically realizable.

## 5. What remains unproved

The original target remains unresolved. The checked routes exclude finite-étale-product models and smooth ample product-image models. The precise surviving geometric obstruction is to construct or rule out a compact complex surface with three distinct everywhere-submersive connected-fiber maps in the hyperbolic/Kodaira setting whose product image is either nonample or nonnormal, while satisfying the cited finite-index condition. Nothing here rules out those possibilities. A proof that every such product image is simultaneously normal and ample would suffice for nonexistence, but neither property has been established here, and their conjunction is not silently assumed.

Do not promote these restrictions to a full resolution. Suggested queue status: `unsolved`, preserving this artifact and its gap.
