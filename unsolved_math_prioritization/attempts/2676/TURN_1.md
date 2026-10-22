# Turn 1: the hyperbolic involution route and a homology-sphere obstruction

**2676 / KP-1.17. Scoped partial results, author turn 1/5. The original question is unresolved.**

## 1. Aim and precise scope

The target asks for an alternating/non-alternating pair of links in S^3 with homeomorphic double branched covers, or a proof that none exists. This turn attacks the distinct-covering-involution construction on a fixed hyperbolic manifold. It establishes conditional exclusion criteria and explains why an existing large class of common-cover constructions cannot yield a mixed pair. It does not assume that every cover is hyperbolic or that two branching involutions commute.

All links and actions are smooth, equivalently tame in the usual three-dimensional setting. Alternation is invariant under ambient homeomorphisms, including reflection. Accordingly, equivalence up to mirror is sufficient for an exclusion result. If a cover homeomorphism reverses orientation, one can mirror the second branch link before identifying oriented covers; mirroring does not change whether it is alternating.

The geometric input is classical: Dinkelbach–Leeb, Geometry & Topology 13 (2009), Theorem H, printed p.1129, states that a smooth finite-group action on a closed hyperbolic three-manifold is smoothly conjugate to an isometric action. The fixed hyperbolic metric can be used for all individual actions by Mostow rigidity. Mecchia–Reni (2002), pp.430–431, already uses this involution/isometry approach for common branched covers. No novelty is claimed for that approach or the elementary group consequences below.

## 2. Branching involutions and a fixed finite group

Let Y be a closed oriented hyperbolic three-manifold, and let G=Isom^+(Y). It is a finite group. A double branched covering Y→S^3 gives a nontrivial orientation-preserving smooth involution tau, with nonempty one-dimensional fixed locus and quotient S^3. Geometrization conjugates it to an element of G. Different conjugating diffeomorphisms do not change the quotient branch link except by an ambient homeomorphism.

If two such involutions tau and sigma are conjugate by a homeomorphism h of Y, then h induces a homeomorphism

    Y/<tau> → Y/<sigma>,    [x] ↦ [h(x)],

carrying the projected fixed sets to one another. Thus their branch links have the same alternation status. In particular, conjugacy in G is sufficient; there is no need to presume that an arbitrary homeomorphism is itself an isometry.

**Proposition 1.** If G has a single conjugacy class of involutions, all links in S^3 with double branched cover Y have the same alternation status. In fact the argument identifies their link types up to ambient homeomorphism and possibly mirror.

For this proposition it is unnecessary that every involution of G be a branching involution. The criterion is sufficient, not a characterization: G may have several involution classes but only one class with quotient S^3, or several branch classes all producing alternating links.

## 3. A centralizer criterion, proved without a classification of 2-groups

An involution means an element of order exactly two. Write C_G(t) for a centralizer.

**Lemma 2.** Let G be a finite group and t an involution. If t is the only involution in C_G(t), every involution of G is conjugate to t.

**Proof.** Choose a Sylow 2-subgroup P containing t. The center of the nontrivial finite 2-group P has even order and therefore contains an involution z. Since z commutes with t, the assumption implies z=t. Thus t is central in P, and P is contained in C_G(t). Consequently t is the only involution of P. Every involution of G lies in a Sylow 2-subgroup, and Sylow conjugacy carries that subgroup to P. Its involution must then be t. ∎

**Corollary 3.** If a fixed branching involution tau of a closed hyperbolic Y has no distinct commuting involution in G, no mixed-alternation pair can have cover Y.

The contrapositive is useful for a counterexample search: if any second branch link has different alternation, there must be an involution z≠tau commuting with tau. They generate a Klein four group. This statement holds for each branching involution in the mixed pair. It does **not** assert that z is free or nonfree, or that Y/<z> is S^3.

**Corollary 4.** A hyperbolic mixed-pair cover must have a Klein four subgroup in its orientation-preserving isometry group. In particular, it cannot have a cyclic or generalized-quaternion Sylow 2-subgroup.

For the first conclusion, apply Corollary 3. Conversely, if G contains no Klein four subgroup, two distinct commuting involutions are impossible, so Lemma 2 applies. For the explicitly named Sylow examples, a cyclic 2-group has one involution, and a generalized quaternion 2-group also has exactly one: in the presentation

    <x,y | x^(2n)=1, y^2=x^n, yxy^(-1)=x^(-1)>, n a power of two,

all elements outside <x> square to x^n and x^n is the sole order-two element. Sylow conjugacy again gives one involution class in G. No converse classification of finite 2-groups is needed.

A topological consequence is also available. A distinct commuting z descends to a nonidentity order-two diffeomorphism of (S^3,L_tau): it preserves the projected fixed set of tau, and it cannot descend to the identity because the deck group on the unbranched complement is exactly <tau>. Hence a hyperbolic mixed pair requires a nontrivial order-two symmetry of each branch pair (S^3,L). This assertion does not classify whether that quotient symmetry is free, periodic or strongly inverting.

## 4. An exact dihedral reduction and its limitation

Suppose a mixed pair has hyperbolic cover Y. Realize its two branching involutions as tau,sigma in G. They cannot be conjugate, since conjugacy would identify the branch links up to mirror. Choose a Sylow 2-subgroup P containing tau and conjugate sigma into P; this preserves its quotient branch link type. The group D generated by these two involutions is a finite dihedral 2-group. More explicitly, let r=tau*sigma have order m, necessarily a power of two. Since the two involutions are distinct, m>=2. The relations

    tau^2=1, r^m=1, tau*r*tau=r^(-1)

give the dihedral group of order 2m. Its two reflection quotients are still S^3 and retain the respective alternation statuses. Conversely, any such smooth dihedral action on a closed hyperbolic Y with the two stated quotient/branch properties supplies a counterexample. Thus this is an exact reduction of the **hyperbolic-cover subproblem** to finite 2-group actions with geometric quotient data.

The reduction does not make m equal to two. In the dihedral group D_8 of order eight, with r of order four, the reflection classes {s,r^2*s} and {r*s,r^3*s} are not conjugate, and no representative of the first commutes with a representative of the second. Their central commuting partner r^2 is a different conjugacy class. For general rotation order 2^j, j>=2, reflections r^a*s and r^b*s commute precisely when

    2(a-b)=0 modulo 2^j,

whereas the two reflection classes have different exponent parity. The conditions are incompatible across the classes. This elementary example blocks an unjustified reduction from two branch classes to a commuting pair of those same classes. It is a group-theoretic negative control, not a constructed mixed link pair.

Mecchia's 2001 Theorem 2.5, pp.169–170, classifies the geometric dihedral possibilities for common hyperbolic covers of **knots** into three constructions. That knot-specific classification is not promoted here to an arbitrary-link classification, and it does not determine which branch sets are alternating. The unresolved input remains geometric information about the branch sets, not just the abstract group D.

## 5. A determinant-one exclusion, including split links

**Proposition 5.** If the double branched cover of a link L in S^3 is an integral homology sphere, and L is alternating, then L is the unknot and the cover is S^3.

**Proof.** If L is split into two nonempty sublinks, cutting along a splitting sphere gives the standard connected-sum formula

    Sigma(L_1 disjoint-union L_2)
       = Sigma(L_1) # Sigma(L_2) # (S^1 x S^2).

The relevant H1 obstruction can also be seen directly: the two branched covers of the complementary balls are connected and have two spherical boundary components each. Gluing them along both boundary spheres has a two-edge, two-vertex graph of spaces, whose cycle contributes a free Z summand to H1 by Mayer–Vietoris. Thus a split link cannot have an integral-homology-sphere cover. We can therefore choose a connected reduced alternating diagram for L.

The classical Goeritz presentation identifies the order of first homology of its branched double cover with the determinant of a reduced graph Laplacian for either Tait graph, hence with its number of spanning trees by the matrix-tree theorem. For a reduced alternating diagram the Tait graph is connected and has no loops or bridges: either would be a nugatory crossing. If there is at least one edge, choose a spanning tree T. Since there are no bridges, there is an edge outside T, and replacing an edge on its fundamental cycle gives another spanning tree. Thus the number of spanning trees is at least two. If there are no edges, the connected diagram is the unknot. An integral homology sphere has homology order one, so only this last case is possible. The double cover of the unknot is S^3. ∎

This uses the standard Goeritz/matrix-tree determinant formula, not an attempted sufficiency test for general alternation. Greene's complete arXiv paper explains the Tait/Goeritz and branched-cover lattice correspondence in Section 1.1 and Theorem 4.7. The proof above only needs its elementary determinant aspect.

**Corollary 6.** No closed hyperbolic integral homology sphere is the double branched cover of any alternating link. Hence all of its branch links are non-alternating, whether or not they are mutants.

This rules out the particular construction in Mecchia 2001 Section 3, pp.171–172. It starts with a strongly invertible hyperbolic knot J and sufficiently long 1/a-surgeries that give hyperbolic manifolds, then obtains common-cover branch knots from distinct strong inversions. In standard meridian-longitude coordinates, the first homology of p/q-surgery on a knot is Z/|p|, because the longitude is nullhomologous in the exterior and filling adds the relation p*meridian=0. At p=1 the covers are integral homology spheres. Corollary 6 certifies that every one of the constructed branch knots is non-alternating. Choosing a different strong inversion in this family cannot produce the alternating half of a mixed pair.

The exclusion is limited to determinant-one covers. It does not say that every nontrivial surgery is incompatible with an alternating branch link, and it does not exclude dihedral constructions with other homology.

## 6. Outcome and remaining gap

This turn tried to exploit different involutions on a common cover. It establishes a usable finite-group exclusion and a precise dihedral reduction, and it eliminates the long 1/a-surgery examples as a potential counterexample family. These are classical-consequence partials, not a solution or a novelty claim.

The hyperbolic sector still requires proving that every admissible branching class has the same alternation status, or giving one fully specified action with two verified S^3 quotients and opposite alternation. The existence of a Klein four subgroup, multiple involution classes, matching homology or matching Floer data supplies none of that missing branch geometry. Nonhyperbolic covers also remain in the original question.

Next route: examine definite spanning surfaces/fillings and whether an alternating presentation can be transported across a different deck involution. A mere nonequivariant definite filling must not be treated as a spanning surface for the new branch link. One of five substantive turns has been used.
