# Sticky Cantor sets: the dimension classification

Date: 2026-10-08. Target: 3422 / OPG-37293.

## Result and attribution

For positive integers n, sticky Cantor sets in Euclidean n-space exist exactly when n >= 4. Thus every embedded Cantor set can be displaced by arbitrarily small ambient self-homeomorphisms in dimensions 1, 2 and 3; the universal displacement assertion is false in every dimension at least 4.

This is a **prior-literature resolution, not a new solution**. The high-dimensional existence theorem is Krushkal's (2016 preprint; journal publication 2018). The three-dimensional separation theorem is due to Sher (1969). Frolkina's directly inspected 2022 paper, section 3.2, explicitly gives both sides and explains the small-homeomorphism/small-isotopy bridge using Kister (1959).

Verification is deliberately asymmetric. Krushkal's six-page article, including the actual construction and argument, was inspected. Sher's original full text could not be obtained: the three-dimensional theorem is imported through Frolkina's explicit statement and reference [47, Theorem 1], **not independently reconstructed or certified here**. Kister's original text was also unavailable, but the required Euclidean bridge is proved completely below. Dimensions 1 and 2 are proved separately, without restricting an arbitrary three-dimensional homeomorphism to a plane. Standard planar Jordan-Schoenflies is used in the planar proof. The source audit records these limits.

No substantive new proof-search approach was spent: the work is source alignment, reconstruction of the elementary implications, and checking the cited prior result. No novelty claim is made for the elementary proofs or algebraic details.

## 1. Exact quantifiers

A Cantor set means a nonempty compact subset C homeomorphic to the standard Cantor space, not necessarily a subset of a straight line. In particular it is perfect and zero-dimensional. Write

    D(f) = sup {|f(x)-x| : x in R^n}.

Call C homeomorphism-displaceable at every scale if, for every epsilon > 0, there is f in Homeo(R^n) with D(f) < epsilon and f(C) intersect C empty. Stickiness is its negation: some epsilon_0 > 0 forbids all such f.

The OPG wording bounds each point strictly, rather than explicitly bounding the supremum strictly. These conventions yield the same every-scale property and the same existence of a positive obstruction scale: apply either convention with epsilon/2 to obtain the other. The distinction at a single threshold is not silently ignored.

An ambient isotopy here is a map H:R^n x [0,1] -> R^n for which (x,t) -> (H_t(x),t) is a homeomorphism, H_0 is the identity, and H_1 is the endpoint. Uniform smallness may mean sup over x,t of |H_t(x)-x|, or a bound on the diameter of each point-track. The argument below handles either convention with a factor of two margin. Only H_1(C) must miss C. The requirement H_t(C) intersect C empty for **every** t > 0 is the different instantaneous-pushing problem.

No compact-support, differentiability, piecewise-linearity, measure-preservation, or prescribed orientation assumption occurs in the target. For n=0 there is no embedded Cantor set at all; this vacuous case is separate from the positive-dimensional classification.

## 2. Complete controlled homeomorphism-to-isotopy proof

Let f be any self-homeomorphism of R^n with finite D = D(f). For 0 < t <= 1 define

    H_t(x) = t f(x/t),                  H_0(x) = x.

Each H_t is a homeomorphism, with inverse

    H_t^{-1}(x) = t f^{-1}(x/t)         (t > 0).

Because f is onto,

    D(f^{-1}) = D(f),
    sup_x |H_t(x)-x| = t D.

Both H and its displayed inverse are jointly continuous for t > 0. At t=0, if (x_j,t_j) -> (x,0), then

    |H_{t_j}(x_j)-x| <= t_j D + |x_j-x| -> 0.

The same estimate holds for the inverse. Hence (x,t) -> (H_t(x),t) really is a homeomorphism of R^n x [0,1], not merely a family of individually bijective maps. Its endpoints are the identity and f. Also

    |H_t(x)-H_s(x)| <= (t+s)D <= 2D.

Consequently an endpoint with D(f) < epsilon/3 gives an ambient isotopy whose global displacement and every track diameter are strictly less than epsilon. Conversely a small ambient isotopy gives a small endpoint. Therefore the two every-scale displacement properties are equivalent for every subset of R^n, in particular compact Cantor sets. The modulus is uniform in C: no compactness-dependent delta is needed for this global hypothesis.

This is the bounded-displacement Alexander/Kister construction. It also shows that a bounded-displacement Euclidean self-homeomorphism is orientation-preserving, since it is isotopic to the identity; orientation is a consequence, not an extra hypothesis. The formula generally does not have compact support. Nor do we claim continuity of t -> H_t in the global uniform metric for positive t: joint ambient continuity and the uniform displacement/track estimates are what was proved and what is needed. Compact-open continuity follows from joint continuity on compact parameter products.

For later comparison, small displacement only on C would not supply the finite global D used here. An arbitrary small homeomorphism C -> C' need not extend to a small ambient homeomorphism. Neither weaker condition replaces the target's global ambient assumption.

## 3. Dimension one, directly

Fix an embedded Cantor set C in R and epsilon > 0. Since C is nowhere dense, choose a finite increasing sequence of cut points outside C, from below min C to above max C, with consecutive distances less than epsilon. In a nonempty interval I=[a,b] between consecutive cuts let l=min(C intersect I) and r=max(C intersect I). Both are strictly inside I and l<r, since this nonempty clopen piece of the perfect set C has no isolated points.

Choose a closed nondegenerate interval [u,v] inside (a,b) disjoint from C. Let h_I be the increasing piecewise-linear homeomorphism of I taking a,l,r,b to a,u,v,b, respectively. It fixes the endpoints and carries C intersect I into [u,v]. On empty intervals use the identity; outside the two extreme cuts also use the identity. The resulting map h is an increasing self-homeomorphism of R, with h(C) disjoint from C. Every moved point remains in its original I, so D(h) < epsilon. Indeed finitely many intervals are used, and their maximum length is strictly below epsilon. Thus no Cantor set in R is sticky.

## 4. Dimension two, directly

We first justify the planar small-disk cover used in the proof.

### Planar small-disk-cover lemma

If C is a planar Cantor set and eta > 0, there are finitely many pairwise disjoint closed Jordan disks D_i of diameter less than eta such that C is contained in the union of their interiors.

Proof. The Cantor-cylinder partitions transported to C give a finite disjoint clopen partition into compact pieces K_j of diameter less than eta/3. Distinct pieces have positive distance. Choose r>0 so small that their 3r-neighborhoods are pairwise disjoint and each has diameter less than eta. Cover C by the interiors of finitely many closed round disks of radii between r and 2r, centered in C; first choose a finite sufficiently fine net, then perturb radii slightly. Radii may be chosen so that boundaries meet transversely, no three boundaries meet, and none are tangent. Each connected component V of their union lies in one 3r-neighborhood and has diameter less than eta.

Such a finite union is a compact planar region with finitely many piecewise-circular Jordan boundary components. Fill every bounded complementary component of each connected V. Its filled outer region is a closed Jordan disk. Filling does not increase diameter: the filled region is contained in the convex hull of V, whose diameter equals that of V. The finitely many outer Jordan curves are disjoint, so their disks are either disjoint or nested. Retain only disks not contained in another. They are pairwise disjoint, still have diameter less than eta, and their interiors cover C. Jordan-Schoenflies identifies each filled Jordan region with a closed disk. This completes the lemma.

Now apply the lemma with eta=epsilon. In each D_i choose q_i in int D_i minus C; this is possible because C has empty interior. Choose a closed-disk chart phi_i with phi_i(0)=q_i. Since C intersect D_i is compact in int D_i, it lies in phi_i(r_i B^2) for some 0<r_i<1. Since q_i is outside the closed set C, choose 0<a_i<r_i so that phi_i(a_i B^2) misses C.

Let rho_i:[0,1] -> [0,1] be the increasing piecewise-linear homeomorphism taking 0,r_i,1 to 0,a_i,1. Its radial extension R_i(0)=0 and R_i(z)=rho_i(|z|)z/|z| is a disk homeomorphism fixing the boundary. On D_i use phi_i R_i phi_i^{-1}; outside the disks use the identity. The maps glue to an ambient self-homeomorphism h, carrying each piece of C into a gap. Every moved point stays in its D_i, so D(h) is bounded by the maximum of finitely many diameters less than epsilon. Thus no planar Cantor set is sticky.

This proof uses planar topology essentially: filling cavities of a three-dimensional region does not in general turn it into a 3-ball. It therefore does not assume away wild three-dimensional embeddings.

## 5. Dimension three: precise imported theorem

The imported statement is:

    For Cantor sets A,B in R^3 and every epsilon > 0, there exists an
    ambient self-homeomorphism h of R^3, epsilon-close to the identity
    globally, such that h(A) intersect B is empty.

Frolkina, section 3.2, printed p.13, explicitly states this (indeed for N<=3) and attributes it to R. B. Sher, "Families of arcs in E^3," Theorem 1. Section 1.6, printed p.6, defines an epsilon-homeomorphism using the usual Euclidean metric and a non-strict bound at every point of the entire ambient space. The original theorem is therefore a named external dependency. We do not infer it from Wright's instantaneous-pushing result, from the existence of particular slippery examples, or from abstract zero-dimensional general position. Taking A=B=C and invoking the source theorem with epsilon/2 gives D(h)<=epsilon/2<epsilon, exactly the three-dimensional conclusion required here. There is no need for a support or orientation conclusion.

The source's stronger two-set assertion is not re-proved by this packet. In particular, Sher's other statements about uncountable arc families or possible continuum-hypothesis assumptions must not be imported into, or substituted for, the specifically cited separation theorem. Only the precise separation statement reported in section 3.2 is used. Original-source access remains an inspection limitation, not a claimed new open mathematical case.

## 6. Dimensions at least four: construction and dependency audit

The imported high-dimensional theorem is Krushkal's Theorem 1: for every d>=4 there is a Cantor set C in R^d that no sufficiently small ambient isotopy displaces from itself. Section 2 above converts this to the literal homeomorphism question with an explicit scale margin.

The paper's mechanism was checked beyond the abstract. Spun Bing defining sequences approximate two transverse codimension-two spheres. A Clifford torus in their complement supplies a commuting-meridian relation. Were the two Cantor limits separated by a small isotopy, compactness would separate sufficiently deep finite stages while retaining that relation. Alexander duality gives a complement with first homology freely generated by the stage meridians and vanishing second homology. Stallings' theorem then identifies its finite lower-central quotients with those of the meridian free group. Bing doubling expresses the original meridians as iterated commutators on disjoint sets of stage generators; their mutual commutator is detected by Magnus expansion, contradicting the torus relation. The union of the two Cantor limits gives self-stickiness. Iterated spinning supplies every d>=4.

The following precise dependencies remain imported rather than newly proved:

1. Shrinkability of the relevant iterated spun Bing decompositions and their realization as Cantor defining sequences, as used on printed p.2.
2. The geometric meridian identifications and their preservation under the small isotopy, read from the Bing slices and Clifford-torus arrangement on pp.2-5.
3. Integral Alexander duality and Stallings' homology/lower-central-series theorem.

Thus this is an audit of the published proof and its applicability, not a foundational re-proof of all geometric topology invoked by that proof. The next section supplies explicit algebra and quantifier checks so those steps are not hidden in a vague reference to commutator length.

## 7. Checkable details of the high-dimensional implication

### 7.1 From the endpoint to finite stages

Let A_j and B_j be decreasing compact defining neighborhoods with intersections A and B. If f(A) and B are disjoint, then some f(A_j) and B_j are disjoint. Otherwise the nonempty compact sets f(A_j) intersect B_j form a decreasing family inside a fixed compact set and have nonempty intersection, contradicting f(A) intersect B empty. This is an exact compactness argument, not a finite-resolution numerical assumption.

If a compact protected torus T has positive distance r from the initial defining neighborhoods, an isotopy of global displacement less than r/2 keeps the moved neighborhoods away from T. The threshold is chosen before the eventual deep stage. The additional protected meridian neighborhoods in the geometric proof are handled by taking the minimum of finitely many positive margins. A bound on the endpoint alone would not justify this; section 2 supplies the controlled path.

### 7.2 The relevant homology and the dimension boundary

For a disjoint union K of N thickened (d-2)-spheres in R^d, compactify to S^d and apply Alexander duality to K union {infinity}. For d>=4 the resulting complement Y has

    H_1(Y;Z) = Z^N,             H_2(Y;Z) = 0.

Indeed the relevant cohomology degrees are d-2 and d-3, respectively; each component of K retracts to S^{d-2}, while the extra point at infinity accounts for the Euclidean rather than spherical complement. A based wedge of N meridian circles maps to Y inducing an H_1 isomorphism and an H_2 surjection. These are exactly the hypotheses of the version of Stallings quoted in Krushkal's Theorem 2.2.

This calculation changes at d=3: for N circle components in R^3 the same duality gives H_2=Z^N, not zero. Also two 1-dimensional spheres in R^3 do not have the transverse codimension-two intersection used by the higher-dimensional construction. No three-dimensional counterexample is obtained by mechanically deleting a spin.

### 7.3 Why the specified commutator survives

Use the noncommutative power-series substitution x_i -> 1+X_i, x_i^{-1} -> 1-X_i+X_i^2-..., with [u,v]=uvu^{-1}v^{-1}. If u has first nonconstant homogeneous term P of degree p and v has first term Q of degree q, then [u,v] has degree-(p+q) term

    P Q - Q P.

Every element of the k-th lower central subgroup has no nonconstant terms below degree k: this follows inductively from the same commutator identity, and products and inverses preserve the filtration.

For a binary iterated commutator tree whose leaves are distinct generators, take the leaf order obtained by reading the left subtree before the right subtree. Its corresponding monomial occurs in the first homogeneous term with coefficient +1. Inductively it arises from P Q; it cannot arise from -Q P because the first letter of those words belongs to the disjoint right-subtree alphabet. Its degree is the number of leaves. Therefore the element is not in the next lower central subgroup. Conjugating a leaf or intermediate word preserves its first homogeneous term; inverting changes its sign. These changes do not erase this obstruction.

In Krushkal's setting the two original meridians have disjoint leaf alphabets of size l. Their commutator has a nonzero degree-2l term, so it remains nontrivial modulo gamma_(2l+1) of the meridian free group. This contradicts its being trivial on the protected Clifford torus. **Length alone is insufficient**: [u,u] is the identity. The disjoint-generator tree structure, not an arbitrary syntactically short commutator, is the verified reason for nontriviality.

### 7.4 The union and the final contradiction

A finite union of compact zero-dimensional metric spaces is zero-dimensional (the finite closed-sum theorem for covering dimension). The union A union B is compact and has no isolated points, so it is again a Cantor set. Disjointness of A and B before the displacement is not required. If f(A union B) missed A union B, then f(A) would miss B, which is already prohibited by the pair obstruction. This proves the self-displacement implication used by the construction.

Choose an isotopy obstruction scale eta for this C and let epsilon_0=eta/3. Any f with D(f)<epsilon_0 and f(C) disjoint from C would, by section 2, be the endpoint of an ambient isotopy with global displacement and track diameter below eta. That contradicts Krushkal's theorem. This proves homeomorphism-stickiness for every d>=4.

## 8. What has and has not been established

- The classification is a known result of the cited literature; it is not a proposed novel theorem.
- The small-homeomorphism/small-isotopy mismatch is closed by a fully explicit construction with stated topology and bounds.
- Dimensions 1 and 2 have direct complete proofs, using Jordan-Schoenflies only for the planar disk charts.
- Dimension 3 depends on Sher's separation theorem, explicitly stated in the inspected Frolkina paper; the original proof was not available for inspection.
- The d>=4 construction and proof were read in Krushkal, with major geometric inputs declared and the elementary quantifier, homology and Magnus implications expanded here.
- No claim concerns instantaneous pushing, all wild Cantor sets being sticky, all embeddings being tame, smooth displacement, or new low-dimensional obstructions.
- Finite code checks validate formulas and guards. They do not certify arbitrary Cantor embeddings or replace the imported topological theorems.

## References

- Open Problem Garden, "Sticky Cantor sets" (posted 2011): https://www.openproblemgarden.org/op/sticky_cantor_sets
- V. Krushkal, "Sticky Cantor Sets in R^d," arXiv:1602.01035v1 (2016), J. Topol. Anal. 10 (2018), 477-482: https://arxiv.org/abs/1602.01035 ; https://arxiv.org/pdf/1602.01035
- O. Frolkina, "On a question of B.J. Baker and M. Laidacker concerning disjoint compacta in R^N," arXiv:2203.03267v2 (2022), section 3.2, printed pp.13-14: https://arxiv.org/abs/2203.03267 ; https://arxiv.org/pdf/2203.03267v2
- R. B. Sher, "Families of arcs in E^3," Trans. Amer. Math. Soc. 143 (1969), 109-116, Theorem 1, as identified by Frolkina: https://doi.org/10.1090/S0002-9947-1969-0251705-4
- J. Kister, "Small isotopies in Euclidean spaces and 3-manifolds," Bull. Amer. Math. Soc. 65 (1959), 371-373: https://doi.org/10.1090/S0002-9904-1959-10380-3
- D. G. Wright, "Pushing a Cantor set off itself," Houston J. Math. 2 (1976), 439-447 (historical context, not the dimension-three separation input): https://www.math.uh.edu/~hjm/vol02-3.html
