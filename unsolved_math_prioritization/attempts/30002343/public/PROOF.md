# Degree-five obstructions for stable log surfaces

## Status and scope

This is a partial mathematical report, not a solution of the universal degree-five question. It supplies (a) a correction to the literal first question, (b) fully explicit model calculations, and (c) a conditional degree-five theorem with a precise remaining obstruction. Novelty of (c) is unclaimed; it is an elementary refinement of the published curve-restriction method.

Everything is over C. A stable log surface here is a connected projective demi-normal surface X with reduced boundary Δ disjoint from the generic points of the conductor, such that its normalized pair with conductor is log canonical and P=K_X+Δ is ample and Q-Cartier. Let I be the least positive integer for which L=IP is Cartier. Write D for the reduced conductor locus and T=D∪Δ. “Gorenstein pair” in this usage means I=1; it must not silently be replaced by an assertion that K_X itself is Cartier when Δ is present. A line bundle separates a length-two subscheme ξ when its evaluation onto H⁰(ξ,L|ξ) is onto. Very ampleness means a closed immersion of X, not merely a birational rational map or an embedding of its open Gorenstein locus.

## 1. The literal canonical question has no uniform answer

Let X=P² and let Δ be the smooth quartic x⁴+y⁴+z⁴=0. Smoothness follows because its three partial derivatives vanish simultaneously only at the origin of affine three-space. The pair is simple normal crossing, hence log canonical, and

K_X+Δ=−3H+4H=H.

Thus it is a stable log surface with I=1 and its entire surface is the Gorenstein locus U. For every positive r,

H⁰(U,O_U(rK_U))=H⁰(P²,O(−3r))=0,

because a nonzero homogeneous polynomial cannot have negative degree. There is no map from this complete linear system, much less a birational map or embedding. In contrast, K_X+Δ itself is very ample. Therefore one must either impose Δ=0 or explicitly replace K_U by (K_X+Δ)|U before asking for a universal positive exponent. We do not silently make that replacement in the source statement.

## 2. A smooth index-one surface for which degree four is insufficient

Let S be the hypersurface

w²=z⁵+x¹⁰+y¹⁰

in P(1,1,2,5), with the coordinates assigned those weights. The affine cone is smooth away from the origin: simultaneous vanishing of the four partial derivatives forces w=z=x=y=0. The only singular points of the weighted projective space are its weight-two and weight-five coordinate points. Neither lies on S. Thus S is smooth. Weighted adjunction gives K_S=O_S(10−1−1−2−5)=O_S(1); this is an ample line bundle because S avoids the ambient singular locus. The polynomial z⁵+x¹⁰+y¹⁰ is not a square in C(x,y,z) (it has odd valuation at infinity as a polynomial in z), so the hypersurface is integral.

Its section ring is the displayed weighted hypersurface ring. One justification is that the polynomial ring is Cohen–Macaulay, its hypersurface quotient has depth three, and the usual Proj local-cohomology sequence identifies its nonnegative graded pieces with H⁰(S,O_S(m)). For m≤4, no monomial contains w. Every m-canonical rational map therefore factors through the generically degree-two projection forgetting w. It cannot be birational.

Here degree five does embed. Sections include x⁵, y⁵, x⁴y, xy⁴, x³z, y³z, xz², yz² and w. On x≠0 their ratios to x⁵ recover y/x, z/x² and w/x⁵, which generate the affine coordinate algebra of that chart. The same holds on y≠0. The locus x=y=0 on S is a single point P: z and w are nonzero, and w²=z⁵ with coprime weights 2 and 5 has one weighted orbit. The section w is nonzero at P. No other point has both x⁵ and y⁵ zero, so P is distinguished from the two affine charts. Near P, the ratios xz²/w and yz²/w are local parameters: z,w are units, the ambient quotient action is free there, and the equation eliminates the remaining transverse coordinate. Consequently the morphism given by degree-five sections is injective on points and has injective tangent maps, and it is an immersion on the two affine charts. It is proper and quasi-finite, hence finite. At a point of its image the induced finite local algebra has the same residue field, and tangent injectivity makes the map on cotangent spaces surjective. Nakayama first gives that the target maximal ideal generates the source maximal ideal, and then that the map of local algebras is surjective. The finite morphism is therefore a closed immersion.

This shows that any uniform birational or embedding exponent for boundary-free Gorenstein stable surfaces is at least five. It is a known sharp-model phenomenon, not a new answer to the unrestricted slc question.

## 3. Exact calculation for smooth cyclic plane covers

Fix integers n≥2, d≥1 and a=(n−1)d−3>0. Let F be a smooth plane curve equation of degree nd, and let π:X→P² be the cyclic cover defined by tⁿ=F, where t is a fiber coordinate of O(d). It is smooth: in a trivialization its equation has nonzero derivative in t away from the branch divisor, while at t=0 the derivative of F is nonzero. Its cyclic algebra is

π_*O_X=⊕_{j=0}^{n−1}O(−jd).

The ramification formula gives K_X=π*O(a), so X is a smooth stable surface and I=1. For q=ma, the projection formula gives

H⁰(X,mK_X)=⊕_{j=0}^{n−1} H⁰(P²,O(q−jd))tʲ.

If q<d, only j=0 occurs, and the map factors through π. It is not birational, and hence not an embedding.

If q≥d, the complete system is very ample. To prove this rather than just count sections, choose homogeneous base coordinates u₀,u₁,u₂. The sections u_i^q show that the system is basepoint-free. On u₀≠0, ratios to u₀^q of the sections u₁u₀^(q−1), u₂u₀^(q−1) and t u₀^(q−d) recover u₁/u₀, u₂/u₀ and t/u₀^d. These generate the entire affine cover algebra, including its defining monic equation. Thus the morphism is a closed immersion on the inverse image of this target affine chart. The same argument works for u₁ and u₂, and these charts cover the image. Properness completes the closed-immersion assertion.

Both the first birational exponent and the first embedding exponent are therefore

m₀=ceil(d/((n−1)d−3)).

This never exceeds four. Indeed for n=2, positivity requires d≥4 and 4(d−3)≥d; for n≥3 the inequality 4((n−1)d−3)≥d follows at the smallest permitted d and increases with d. More explicitly n=3 needs d≥2, n=4 needs d≥2, and n≥5 permits d≥1. The maximum four occurs at n=2,d=4. Thus this natural family cannot produce failure of 5K. The claim concerns these smooth monogenic covers only, not arbitrary singular cyclic covers or arbitrary branch pairs.

## 4. The conductor is not the whole infinitesimal problem

The restriction results of Liu–Rollenske imply that H⁰(X,5L)→H⁰(T,5L|T) is onto and 5L|T is very ample (Corollary 3.5 and Proposition 4.8 of [LR]). Hence every length-two scheme ξ contained scheme-theoretically in T is separated by 5L: compose the two surjections onto T and then ξ. This includes tangent vectors along T. It does not include all length-two schemes whose support lies on T.

Here is a completely explicit local distinction. Put

R=C[x,y,z]/(xy),  p=(x,y,z),  T=V(x,y).

The map given by the functions z and x+y is an isomorphism on T. Nevertheless its tangent map at p has kernel the direction (1,−1,0), since the cotangent space m_p/m_p² has basis x,y,z. The associated length-two scheme is the quotient R→C[ε]/(ε²) sending x↦ε, y↦−ε and z↦0. This is a valid ring map because xy↦−ε²=0. It is not contained in T, and both z and x+y vanish on it. Thus the linear system {1,z,x+y} fails to separate this length-two scheme. This is a local example about linear systems, not a global counterexample involving 5K of a stable surface.

This distinction prevents the incorrect inference that very ampleness on the conductor automatically descends from very ampleness on the normalization or proves global very ampleness. The missing transverse sections must be controlled.

## 5. A degree-five obstruction theorem for index at least two

### Explicit external inputs

We use four established inputs for reduced-boundary stable log surfaces. They are mathematical dependencies, not claims proved afresh here:

A. H¹(X,O_X(kP))=0 for every integer k≥2, with reflexive interpretation when required ([LR], Proposition 3.6).
B. For I≥2, 3L is globally generated ([LR], Theorem 4.1).
C. If a globally generated mL fails to separate a length-two scheme ξ, a reduced Cartier divisor C∈|mL| contains ξ and has no component in T ([LR], Lemma 5.4(i)).
D. On such a curve C, every nonempty subcurve B satisfies (m+1/I)(L·B)≥2p_a(B)−2 ([LR], Lemma 5.6). A line bundle on a projective Cohen–Macaulay curve is very ample when its degree on every generically Gorenstein subcurve B is at least 2p_a(B)+1 (the curve-embedding theorem [CFHR]).

Reduced subcurves here are Cohen–Macaulay and generically Gorenstein. The curve C is Cohen–Macaulay because it is an effective Cartier divisor on the S₂ surface X. Positivity and integrality give L·B∈Z_{≥1}. These are essential to the argument.

### Theorem 5.1 (localization of degree-five failure)

Let (X,Δ) be as above, I≥2 and L=I(K_X+Δ). Then:

1. If |3L| fails to separate a length-two scheme ξ, |5L| separates ξ.
2. |5L| separates every length-two scheme whose support is disjoint from Bs|2L|.
3. Consequently, if 2L is globally generated, 5L is very ample.
4. Any actual failure of very ampleness of 5L must be witnessed by a length-two scheme ξ that is separated by |3L| and whose support meets Bs|2L|. It cannot be a scheme contained in T.

The theorem does not assert that Bs|2L| is empty.

Proof. For (1), apply B and C to obtain a reduced log-well-behaved Cartier curve C∈|3L| through ξ. The restriction sequence is

0→O_X(2L)→O_X(5L)→O_C(5L)→0.

Input A applies with k=2I≥2, so the map of global sections to C is onto. It remains to prove that 5L|C is very ample.

For each nonempty subcurve B⊂C put d=L·B and g=p_a(B). Input D gives

2g−2≤(3+1/I)d.

If d=1, I≥2 implies 2g−2≤7/2. Since g is an integer, g≤2, whence 5d=5≥2g+1. If d≥2, then

5d−(2g−2)≥(2−1/I)d≥(3/2)·2=3.

Thus again 5d≥2g+1. The curve-embedding theorem makes 5L|C very ample. Restricting further to ξ proves (1).

For (2), only the case where 3L separates ξ remains. If Supp(ξ) avoids Bs|2L|, choose a section s∈H⁰(X,2L) nonzero at each point of Supp(ξ). Such a section exists because at most two proper linear hyperplanes must be avoided over the infinite field C. Its restriction to the Artin scheme ξ is a unit in local trivializations, so multiplication by s gives an isomorphism between H⁰(ξ,3L|ξ) and H⁰(ξ,5L|ξ). The product of s with all sections of 3L therefore surjects onto H⁰(ξ,5L|ξ). This proves (2). Part (3) follows by the length-two criterion for very ampleness. Since 5L is globally generated by [LR], Theorem 4.1, the same criterion and (1)–(2) yield (4); the final sentence follows from Section 4. ∎

### Proposition 5.2 (the exact small-degree exceptions at index one)

Suppose I=1 and a reduced log-well-behaved C∈|3L| has been produced. The numerical estimate in D guarantees 5L|C is very ample unless C has a subcurve B with

(L·B,p_a(B))=(1,3) or (2,5).

This is a sufficient criterion, not a geometric existence statement about either pair.

Proof. Now 2g−2≤4d, or g≤2d+1. The desired inequality is 5d≥2g+1. If d≥3, then 2g+1≤4d+3≤5d. If d=1, the estimate allows g≤3, and the desired inequality fails only when g=3. If d=2, it allows g≤5, and the desired inequality fails only when g=5. This is exhaustive for integers d≥1 and g. If neither exceptional pair occurs, input D and the curve-embedding theorem prove the assertion. ∎

The obstruction at I=1 also includes the possibility that 3L is not globally generated, so the curve C cannot automatically be chosen by input C. Even when 3L is globally generated, schemes already separated by 3L still require the multiplication argument or another construction if they meet Bs|2L|. The two numerical pairs are failures of a sufficient inequality, not counterexamples to very ampleness.

## 6. What is proved and what is still missing

Proved here: the literal boundary-bearing rK_U formulation fails; the explicit smooth weighted surface requires exponent five and embeds in degree five; smooth cyclic plane covers have the stated exact threshold; conductor separation does not control all transverse jets; and Theorem 5.1 and Proposition 5.2 follow from the explicitly listed established inputs.

Not proved: an optimal exponent on the Gorenstein locus for all boundary-free stable surfaces; a uniform unindexed logarithmic exponent on the Gorenstein locus for all pairs; a stable log surface with 5I(K+Δ) not very ample; or the assertion that 5I(K+Δ) always is very ample. A theorem for the whole Cartier-index multiple is not automatically a theorem for a fixed index-independent exponent on an open locus. The hypothesis that a pair is slc alone does not give stability: ampleness is also used. No statement is made for threefolds, arbitrary rational boundary coefficients, or positive characteristic.

The concrete unresolved branch in Theorem 5.1 is separation by 5L of schemes touching Bs|2L| that already embed under |3L|. An unconditional theorem would have to handle this branch rather than omit it. At index one the two low-degree subcurve possibilities and possible degree-three base points add genuine unresolved steps in this method.

## References

[OWR] Wenfei Liu (joint work with Sönke Rollenske), “From surfaces of general type to stable (log) surfaces,” in Complex Algebraic Geometry, Oberwolfach Reports 10 (2013), report 27, contribution pp. 1598–1599; published 17 March 2014. https://doi.org/10.4171/OWR/2013/27

[LR] Wenfei Liu and Sönke Rollenske, Pluricanonical maps of stable log surfaces, Advances in Mathematics 258 (2014), 69–126. https://doi.org/10.1016/j.aim.2014.03.009 ; version inspected: https://arxiv.org/abs/1211.1291v4

[CFHR] Fabrizio Catanese, Marco Franciosi, Klaus Hulek and Miles Reid, Embeddings of curves and surfaces, Nagoya Mathematical Journal 154 (1999), 185–220. The curve theorem is also stated as [LR], Theorem 2.15. https://arxiv.org/abs/alg-geom/9607021
