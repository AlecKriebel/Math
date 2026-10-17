# Exact reproduction conventions for the fourth spline edition

The [certificate](FOURTH_PASS_CERTIFICATES.json) contains authored rational constructions. Every fraction is exact, with no floating-point tolerance. The global arguments are proofs in the two manuscripts and their independent acceptances; checking finitely many disks does not prove the universal or conditional theorems.

## Labels and finite records

The eight-vertex control uses the ordered names (v,a,b,c,d,z1,z2,z3), corresponding to indices 0 through 7. Its coordinate, weight, color and face arrays follow that order. The explicit named endpoint-determinant list from the proof is retained as author_opposite_order_records. The exact_checks record uses the deterministic convention below; an opposite-order reversal changes both coefficients' signs and does not change balance.

The seed uses indices 0 through 11. Its twelve coordinates and weights are also reconstructed by x_i=q_i+(i+1)/1000, P_i=d_color(i)/x_i, with

    q=(9,-25,-1,-1,-1,-1,-7,15,-7,3,3,3),
    d_A=(1,0), d_B=(0,-1), d_C=(-1,1),
    colors=(B,A,C,B,A,C,A,C,B,A,C,B).

The reflex-ear step retains the seed unchanged and appends the face (5,1,0). The final step retains that intermediate unchanged and appends the three displayed vertices 12,13,14, their weights and four faces. Thus no coordinate or face is silently replaced. Each exact_checks record contains complete stage-specific edge incidence, boundary, fan, balance, area and reduced-matrix information; coordinates are stored once for the seed and once for the new vertices.

## Oriented determinant and incidence conventions

For planar columns a,b, define det(a,b)=a_x b_y-a_y b_x. For a face (v,w,u), doubled area is det(P_w-P_v,P_u-P_v), and it must be strictly positive. For homogeneous columns, det(A,B,C) is the determinant with those vectors as columns. Put V_i=(P_ix,P_iy,1)^T and U_i=x_i V_i.

Process faces in their displayed order. For each face (v,w,u), add opposite u to the unordered edge {v,w}, opposite v to {w,u} and opposite w to {u,v}. Store edge endpoints increasingly. Sort the final distinct edge list lexicographically. A boundary edge occurs once and an interior edge twice. For an interior edge (v,w), let (u,z) be its two opposite vertices in their first-face, second-face encounter order. Define

    D_v=det(P_z-P_v,P_u-P_v),
    D_w=det(P_u-P_w,P_z-P_w).

Every recorded coefficient is nonzero and

    x_v D_v=x_w D_w.

Independently check det(U_v+U_w,U_u,U_z)=0. Multiplication by the nonzero opposite weights relates this equation to the preceding one. No step divides by x_v+x_w; its possible vanishing is harmless. The common_weighted_value in the certificate records the two equal rational values.

Only interior edges of each auxiliary disk are included. No outside opposite vertex, exterior attachment or boundary equation is supplied for them.

## Exact embedded disk checks

Check all coordinates are pairwise distinct. Every face must have distinct indices and positive doubled area. Every edge has one or two incident faces. The face-dual graph must be connected. The once-incident edges must form the stated single boundary cycle; orient this cycle with the faces to its left. For each vertex, construct its link from the opposite edge in each incident triangle. An interior link is one simple cycle; a boundary link is one simple path. Verify V-E+T=1.

These combinatorial checks are supplemented by geometric intersection tests for every pair of faces: 28 pairs for the eight-vertex disk, 120 for the seed, 136 for the reflex-ear intermediate and 210 for the final extension. The exact geometric intersection must be precisely the simplex named by their common vertex indices.

One reproducible test intersects two closed, positively oriented triangles as six half-planes. Enumerate intersections of all pairs of their supporting edge lines whose 2-by-2 determinant is nonzero. Retain a point exactly when it lies in all six closed half-planes. For two bounded convex polygons the retained points are the vertices of the intersection, including its segment and point degeneracies. For no common index require the set to be empty. For one common index require exactly that point. For two common indices require both common endpoints and require every retained point to lie on their segment. More than two common indices indicates a duplicate face and is rejected.

An alternative exact test collects triangle vertices lying in the other triangle and all closed segment-segment intersections. Parallel collinear edges require endpoint-in-segment tests. The same common-simplex conditions apply. Positive face orientation alone never substitutes for the complete pairwise tests.

For a counterclockwise boundary b_0,...,b_(n-1), the turn at b_i is

    det(P_bi-P_b(i-1),P_b(i+1)-P_bi).

The certificate includes every turn. The eight-vertex control has turn -7/4 at z3. The seed has negative turns at 0 and 1. The final extension has turns -94625/3198133656 at 12 and -1324825/44909003592 at 14. Their nonconvexity is exact.

## Actual reduced quartic matrices and rank witnesses

Use all lexicographically sorted mesh edges as columns. Use interior vertices in increasing index order as rows. Boundary vertices contribute no row. For each interior vertex v, orient its neighbor cycle counterclockwise and start at its smallest-index neighbor. A positively oriented incident face (v,w,u) maps neighbor w to the next neighbor u, independently of the cyclic rotation used to write the face. Repeatedly follow this map to recover the full fan w_0,...,w_(d-1).

Set d_i=P_wi-P_v and a_i=det(d_i,d_(i+1)). All a_i are positive. The row entry in column {v,w_i} is

    r_(v,i)=(-1)^i det(d_(i-1),d_(i+1))/(a_(i-1) a_i).

All other entries are zero. This divides the first-edition row by its nonzero initial area a_0, so it preserves row rank and has the correspondingly scaled right-hand side. A different cyclic start may negate a row; the certificate's exact maximal-minor determinant uses the specified start.

Every interior vertex in these four finite disks has even degree. Each retained row is nonzero; no singular zero row is mistakenly retained. The exact shapes and ranks are

    eight-vertex control: 2 by 15, rank 2;
    twelve-vertex seed: 6 by 27, rank 6;
    reflex-ear intermediate: 7 by 28, rank 7;
    fifteen-vertex extension: 8 by 35, rank 8.

The sparse_rows records specify every nonzero entry. Each nonzero_maximal_minor record selects exactly as many columns as rows, lists their edge labels and zero-based indices, and gives its exact rational determinant. Reconstruct the corresponding square matrix from the coordinates and the formula and verify that determinant. A nonzero maximal minor proves full row rank without relying on numerical rank thresholds or a particular elimination program.

For example, the independent audit starts the a-fan at b, one cyclic step before this certificate's start at v, so its a-row is the negative of this certificate's row. With those audit rows ordered (v,a), columns vb and ab form diag(1,-1), with determinant -1. With this certificate's starts the same columns form diag(1,1). The stored maximal minor uses columns va and vb and has determinant -1. All conventions certify the same full row rank. The interior weight-balance matrix on all eight vertex weights is a different matrix; its one-dimensional kernel does not create a dependency among these two actual reduced rows.

For each row also verify the three quadratic moments

    sum_i r_i d_ix^2=0,
    sum_i r_i d_ix d_iy=0,
    sum_i r_i d_iy^2=0.

The local right-hand side in this scaling is

    H_v=(sum_i r_i) f_v+(1/2)(sum_i r_i d_i) dot g_v.

If desired build H with columns (f_v,g_vx,g_vy) for all vertices and zeros away from row v. Since R already has full row rank, rank([R H]) equals rank(R). The accepted exact reduction therefore gives arbitrary vertex first-jet interpolation on every displayed auxiliary disk. The finite rank witnesses say nothing about an unspecified convex exterior completion.

The independent [short rank certificates](EXACT_RANK_CERTIFICATES.json) use a different specified fan start, at the least polar angle in [0,2π), and divide each row by its explicitly listed nonzero selected coefficient. Their displayed selected minors are identity or upper triangular with unit diagonal, hence determinant one. These independent conventions are not substituted into the sparse rows above; each certificate must be reproduced with its own stated starts and scalings.

## The new fan and pencil escape

Intersect the lines P_1P_5 and P_1P_2 with x=0 to get

    l=-125/3249, h=-200/5199, l<h<0.

The new points 12 and 14 have ordinates (3l+h)/4 and (l+3h)/4. At x=1/2, point 13 has the mean ordinate of those two side lines. The weights are x_13=-2 and the unique nonzero solutions x_12,x_14 of

    det(U_1+x_12 V_12,U_5,U_13)=0,
    det(U_1+x_14 V_14,U_2,U_13)=0.

Check each linear coefficient is nonzero before solving. Across the middle spoke (1,13), both opposite vertices lie on x=0 and the first coordinates of U_1 and U_13 cancel. Across the old seams, all needed vectors already lie in x=0. This reconstructs all five newly interior equations exactly.

The homogeneous determinant det(V_2,V_5,V_13) is -217587275/3719962464204. The color-C triple is therefore noncollinear. In the eight-vertex disk, det(P_d-P_b,P_z2-P_b)=21/4. Check every face is tricolored; connected face transport makes any proper coloring unique up to a global permutation. Thus relabeling cannot restore color-pencil containment.

## Global proof qualifications and algebraic checks

Transport three vertex colors across interior dual edges. Bounded dual facial walks correspond to interior primal vertices, and even degree makes their transport trivial. Boundary vertices give link paths, not additional dual faces. The bounded facial walks and immediate edge reversals generate all loops, so the coloring is well defined globally.

At a boundary vertex of degree d, the previous and next boundary colors agree exactly when d is odd. If epsilon_i is the signed color increment, it is preserved at a strict even corner and reversed at a straight odd vertex. Hence the number s of straight vertices is even. If s=0, the number k of corners is divisible by three. Use the accepted k>=5, not an assumption that every convex polygon must have at least five corners.

Euler's disk degree identity gives

    2 N4 = 6 + sum_(interior degree>=8)(degree-6)
               + sum_(strict boundary)(degree-4)
               + sum_(straight boundary)(degree-4).

All interior support degrees are even and at least four; every straight boundary vertex contributes at least one. This proves N4>=3+s/2. These are necessary conditions on an actual closed support, not the auxiliary disks with illegal boundary degrees.

For independent A,B,C and S=A+B+C, the exact local identities in that basis are

    det(A+aS,B+bS,C+cS)=(1+a+b+c) det(A,B,C),
    det(A+aS+B+bS,C+cS,(u,v,w))
        =(u-v)(1+a+b+c) det(A,B,C),
    det(alpha A+beta B+(p+q)S,gamma C+rS,delta C+tS)
        =(alpha-beta)(r delta-t gamma) det(A,B,C).

The line rule divides only by the nonzero triangle determinant. The base rule uses distinct opposite vertices with nonzero weights: their homogeneous vectors are independent and the final factor is nonzero. A provisional zero base coefficient is allowed until connectivity forces a common coefficient, which nondegeneracy forces to be nonzero. A projective common point at infinity is allowed initially and is ruled out only by the convex boundary-diagonal argument. No affine division precedes that argument.

The boundary positivity lemma is used only after proving exactly six strict corners and no straight subdivisions. It uses genuine original exterior vertices and activity at both endpoints. No formula is extrapolated to boundary subedges with straight vertices.

## Rejection controls and evidence limits

Useful exact negative controls include a wrong sign in the line-forcing identity, unequal base coefficients with independent opposites, an odd-valence interior wheel claimed to be three-colorable, a changed dependency weight, a perturbed middle fan coordinate, a reversed added face, a false convexity assertion and a false same-color collinearity assertion. Each must fail its own defining exact equation or inequality.

The finite constructions and checks do not establish that arbitrary even triangulations collapse to a pencil, that sufficient propagation rules are complete, that any nonpencil seed can be completed convexly, or that the whole quartic question is decided. The independent acceptances state the exact positive conclusions and exclusions.
