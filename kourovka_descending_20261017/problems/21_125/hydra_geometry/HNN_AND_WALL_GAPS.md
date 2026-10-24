# Geometric mechanisms attempted and precise remaining gaps

This is a terminal route audit for ordinary Hydra21.125(b). None of these mechanisms produces a special model for all m>=5. Completion estimate toward that discovery:6% (uncertain, not monotone). Partial facts below do not open a publication gate.

## A. The canonical cubulation cannot be made VH by taking covers

For m>=3, the link at the vertex of the canonical square complex contains the5-cycle

    alpha_2+ — s+ — alpha_1+ — alpha_2- — alpha_3- — alpha_2+.

Each adjacency is an actual square corner: the first is from square2, the second square1, the third square2, and the last two from square3. These are five distinct germs. In a VH square complex each square alternates vertical and horizontal edges, so its vertex links are bipartite. A cover has the same local links, so **no cover of this particular cube complex admits a VH partition**. Ordinary cubical subdivision also preserves the old vertex link, so it does not remove this obstruction. Special complexes with more than two hyperplane colors are allowed; this is not a virtual-specialness obstruction.

Thus a proposed shortcut through special theorems for clean VH complexes fails a concrete local hypothesis, even after a finite cover. General special cubulations or changing the cell structure remain possible.

## B. Iterative cyclic HNN cubical combination

The alternate presentation gives a genuine hierarchy

    G_m = <G_(m-1), alpha_m | alpha_m^-1 s alpha_m=alpha_(m-1)>.

Both attaching axes are geodesic edges in the published CAT(0) model, and this accounts for its nonpositive curvature. It does not make the HNN extension special. The s-edge subgroup is not malnormal in G_(m-1) for m>=2: it is centralized by alpha_1, with <s,alpha_1> a copy of Z^2 inherited from G_1, and alpha_1 not in <s>. Therefore a theorem requiring malnormality on that attaching side cannot simply be applied. The existing hyperbolic combination theorems also require hypotheses absent here: G_m contains Z^2.

One might instead arrange a special model where both cyclic attaching subgroups are represented by suitable embedded locally convex loops, then use finite covers and wall projections to eliminate the new pathologies. No construction preserving these simultaneous conditions through arbitrary m was obtained. Replacing the desired theorem by “this cyclic HNN extension of a special group is virtually special” merely restates the unsupported central difficulty. This route is blocked until a new combination mechanism or a compatible family of special models is supplied.

### An exact normal-form check on the hyperplane subgroup

The subgroup L_m from CANONICAL_COVER_MECHANISM.md satisfies

    L_m = L_(m-1) * <alpha_m s alpha_m^-1>,
    L_m intersect G_(m-1) = L_(m-1),
    L_m intersect <s> = {1}.

Here take G_1=<s,alpha_1>=Z^2 and L_1=<alpha_1>. For the induction, abelianization of G_(m-1) sends s and its top generator alpha_(m-1) to independent generators, so <s> intersects <alpha_(m-1)> trivially. By induction L_(m-1) intersects <s> trivially. Expand a reduced word in the proposed free product into alternating factors from L_(m-1) and alpha_m <s> alpha_m^-1. The subwords alpha_m s^n alpha_m^-1 cannot pinch in the HNN extension for n!=0, since s^n is not a power of alpha_(m-1). The intervening subwords alpha_m^-1 l alpha_m cannot pinch for nonidentity l in L_(m-1), since l is not in <s>. Britton's lemma therefore proves the free-product injection and the claimed intersection with the base group; it also preserves the intersection with <s>. This establishes the induction.

In particular, s is genuinely outside L_m in the original infinite group. The rank5 class10 finite quotient's q(s) in q(L_5) is a finite-quotient collapse, not a missing infinite-group relation. Also alpha_j is outside L_m for every j>=2: the top stable-letter exponent excludes alpha_m, and the base-group intersection reduces all earlier j inductively. This agrees with the geometry of the CAT(0) universal cover and is not a finite separability theorem.

## C. Finite-vertex HNN completion attempt

A constructive approach was to find a finite quotient Q of G_(m-1) preserving the required cyclic/hyperplane separations, with equal orders for the images of s and alpha_(m-1). Their cyclic isomorphism then defines an HNN extension of the finite group Q. That extension is virtually free and has effective finite quotients available. Britton normal forms can preserve a suitably transverse graph of hyperplane groups before passing to a finite quotient.

The difficulty is the compatibility needed for the *next* level. One must prescribe the new stable letter's finite order to match the s-order while preserving all subgroup and double-coset separations required by the cube cover. A finite quotient separating finitely many elements need not preserve the required cyclic subgroup intersections or hyperplane double cosets. Simply multiplying by an abelian factor to equalize orders can introduce nontrivial powers of s into the image of the hyperplane subgroup, because all its initial generators have the same abelian s-coordinate. No general compatible completion mechanism was proved. Passing to an arbitrary finite quotient of a virtually free intermediate group does not close this gap.

The class10 rank5 certificate supplies a concrete warning: it preserves every alpha_j-versus-L separation needed to remove self-intersections, yet collapses s into L and thereby forces inter-osculation. Thus additional data are mathematically necessary.

## D. Equitable walls beyond the tubular case

Wu–Ye2504.14192v2 Theorem4.5 applies to a multiple HNN extension of one Z^2 vertex satisfying the stated CAT(0) and free-by-cyclic hypotheses. The ordinary Hydra hierarchy above has a nonabelian vertex once the first stage is passed; the displayed hierarchy is not a presentation of the theorem's required type. This does not prove that no alternative tubular presentation exists; rather, none was constructed and the missing hypothesis cannot be silently assumed.

Trying to carry balanced wall curves inductively requires control of wall projections and identifications in the nonabelian vertex space, not only two-dimensional determinants. The explicit rank3 wreath cover and rank5 nilpotent cover both remove every self-intersection and still inter-osculate. Balancing local winding data, finite quotient orders, or self-crossing counts alone cannot substitute for separating the crossing hyperplane double cosets.

Exact remaining obstruction: construct finite quotients or a different wall system that simultaneously separates the explicit L_m cosets and all crossing hyperplane double cosets, with a mechanism valid for arbitrary m>=5. This is the actual virtual-specialness difficulty; it has not been transferred to a proved simpler claim.
