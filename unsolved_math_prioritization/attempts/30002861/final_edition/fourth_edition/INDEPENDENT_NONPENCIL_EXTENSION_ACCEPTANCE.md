# Independent acceptance of the exact nonpencil seed extension

## Decision, model and scope

**Accepted without mathematical correction.** The twelve-vertex auxiliary seed, its reflex-ear extension and its fifteen-vertex nonpencil extension are conforming straight-line triangulations of nonconvex polygonal disks. Every asserted interior balance equation holds exactly, with nonzero weights and both nonzero endpoint determinants. Their actual reduced quartic matrices have full row ranks six, seven and eight, respectively. Each of these three meshes therefore admits arbitrary prescribed vertex values and first derivatives by globally C1 piecewise quartics on its original triangles.

The accepted [manuscript](FOURTH_PASS_NONPENCIL_EXTENSION.md) needs no mathematical correction. The present report supplies the independent acceptance that was pending when the manuscript was first written.

This belongs to the **same fourth newly documented substantive pass** on row 1761 / problem 30002861 / OWR-13678-002, dated 13 October 2026 UTC. It is not a further pass; the lifetime total is unknown. The bundled row remains unsolved. See the [edition guide](README.md) and [accepted dependencies](DEPENDENCIES.md).

The model is the accepted original-mesh quartic Hermite model: finite conforming straight-line triangulations of polygonal disks, nondegenerate triangles, independent values and two first derivatives at all vertices, no refinement or imposed boundary conditions. This audit relies on the already accepted Bernstein reduction and closed-support theorem. It independently recomputes the new finite geometry and actual matrices, including the previously author-only seed. It does not treat the third-pass seed certificate as earlier independent acceptance.

The result is an internally balanced auxiliary disk that escapes the seed's color pencil. It is **not a closed balanced support, a quartic counterexample, a convex completion or a universal interpolation theorem**. Nothing here supplies missing exterior triangles. The phrase “topology-changing extension” in the original title refers to a change of triangulation incidence: the underlying topological space remains a disk throughout.

## 1. Independent seed identification and exact geometry

The seed was reconstructed from the manuscript's displayed integer vector, rational perturbations, color directions and face formulas. Its coordinates, weights, colors and faces agree exactly with the original third-pass author-only seed record. The old seed verifier and its helper modules were neither imported nor trusted to establish geometry or rank.

A newly written verifier uses Python rational arithmetic and sequential Sutherland–Hodgman clipping, independently of the manuscript verifier's supporting-line/half-plane candidate enumeration. It checks the intersection of every pair of closed triangles against their prescribed common simplex, including point and segment intersections. All vertices are distinct, all faces have positive orientation, every edge has one or two incident faces, shared edge orientations are opposite, and every vertex link is exactly a path or cycle as appropriate. Face adjacency is connected, the oriented boundary is one cycle, and V−E+T=1. Thus the lists describe embedded conforming disks, including their boundaries, rather than merely positive-area triangles.

The complete geometry totals are:

- Seed: V=12, E=27, T=16; 120 triangle-pair intersections; boundary (0,1,2,3,4,5).
- Ear: V=12, E=28, T=17; 136 triangle-pair intersections; boundary (1,2,3,4,5).
- Extension: V=15, E=35, T=21; 210 triangle-pair intersections; boundary (2,3,4,5,12,13,14).

All 466 pair checks pass. All 39 vertex-link checks pass. Every triangle is properly three-colored. Adding face (5,1,0) makes vertex 0 a degree-four interior vertex. Adding the four fan faces makes vertex 1 a degree-eight interior vertex. The extension's retained interior vertices are (0,1,6,7,8,9,10,11), with degrees (4,8,6,4,6,4,6,4).

The reported boundary turns are independently reproduced, including seed turns

    −4247750000/55914239003 at 0,
    −293000000/3867792707 at 1,

and final extension turns

    −94625/3198133656 at 12,
    −1324825/44909003592 at 14.

All three boundaries are genuinely nonconvex. The final boundary vertices 12 and 14 each have mesh degree three. In particular, they cannot be taken as the legal straight boundary vertices of a closed induced support; the accepted support classification requires degree at least five there.

## 2. Every balance equation and nonzero condition

For each interior edge vw, the two actual incident triangles determine opposite vertices u,z. The independent audit computes

    D_v = det(V_v,V_u,V_z),
    D_w = det(V_w,V_u,V_z),
    V_i = (P_i.x,P_i.y,1)^T.

It verifies D_v and D_w are both nonzero, as are every x_i, and checks separately

    x_v D_v + x_w D_w = 0,
    |x_v D_v| = |x_w D_w|,
    det(U_v+U_w,U_u,U_z) = 0.

These establish signed balance, magnitude balance and the full homogeneous identity on all 21 seed edges, all 23 ear edges and all 28 final interior edges. The exact determinant pair and weighted determinant pair for every edge are retained in the finite audit certificate. No balance condition is asserted for a disk boundary edge lacking an outside triangle.

The ear's new seams are (0,1) and (0,5). The fan's five new seams are (1,5), (1,2), (1,12), (1,13) and (1,14). Their opposite vertices are obtained from the actual face incidence; no prospective exterior vertices are invented.

The seed's homogeneous common-pencil representation in the manuscript is correct. Thus the two ear balances follow from the same-color opposite vectors. At the fan's old boundary seams, the relevant endpoint sum and opposite B-colored vectors lie in x=0. For the middle spoke, the distinct vertices 12 and 14 lie in x=0 and x_13=−2 makes U_1+U_13 lie in that same plane.

## 3. Exact construction and its restrictions

Independent slope-intercept calculations give

    l=−125/3249 < h=−200/5199 < 0.

They reproduce the stated quarter and three-quarter positions of vertices 12 and 14 and the mean side-line ordinate of vertex 13 at x=1/2. All three new points have strictly positive barycentric coordinates in the missing pocket triangle with vertices (1,5,2). The asserted angular order and four positive new triangle orientations are also verified.

The two exterior-spoke linear equations have, in the determinant order used by the manuscript, these coefficient/constant pairs:

- For x_12: coefficient 5299/90088272; constant −13499/8665000.
- For x_14: coefficient −52993/900882720; constant 13499/8664000.

Both coefficients and constants are nonzero. Solving coefficient times weight plus constant equals zero uniquely gives

    x_12=87716502/3311875,
    x_14=70181301/2649650.

Together with x_13=−2, these reproduce every new weight exactly.

For clarity, the local algebra also has an explicit general form. Write

    U_A=(1,0,a), U_C=(−1,1,c),
    P_B=(0,b), P_Z=(t,y), x_Z=−1/t.

Then, for the equation det(U_A+x_B V_B,U_C,U_Z)=0,

    coefficient of x_B = (−bct−b+t+y)/t,
    constant = (at+ay+cy−1)/t,
    x_B = (−at−ay−cy+1)/(−bct−b+t+y).

This formula requires t≠0 and −bct−b+t+y≠0. A nonzero x_B additionally requires −at−ay−cy+1≠0. Distinctness, triangle orientation, conformity and nonzero endpoint determinants are separate geometric conditions, all verified for the stated rational construction. The manuscript correctly refrains from claiming that arbitrary parameter choices or arbitrary fan lengths work.

## 4. Nonpencil conclusion

The independent computation gives exactly

    det(V_2,V_5,V_13)=−217587275/3719962464204 ≠ 0.

Vertices 2,5,13 all have color C. Thus their positions cannot belong to one projective line. Since the face adjacency graph is connected, a proper three-coloring is determined up to permutation by its values on any one triangle: traversing an adjacent triangle forces its third color. Every alternative proper coloring therefore has the same obstruction after relabeling.

Consequently the full extension leaves the globally concurrent three-color-line class. It also lies outside the precise complete nested-hexagonal-annulus incidence family of the accepted third-pass theorem. This does not contradict that theorem or enlarge its scope to arbitrary even triangulations.

## 5. Actual reduced systems and short exact rank witnesses

The audit orders neighbors by an exact rational polar-angle comparator, starting at the least angle in [0,2π). It does not import the author's oriented-link fan ordering. For every interior vertex it independently forms the cyclic corner matrix from barycentric coordinates and computes its left nullspace. The eliminated compatibility row and local jet form are then compared, under a nonzero exact row scaling, with the displayed determinant formula. All second-moment identities hold. Boundary fans contribute no compatibility rows.

The actual reduced and augmented ranks are:

- Seed: R is 6 by 27, rank(R)=rank([R H])=6.
- Ear: R is 7 by 28, rank(R)=rank([R H])=7.
- Extension: R is 8 by 35, rank(R)=rank([R H])=8.

Here is a small script-free maximal-minor certificate. Use ascending vertex order for rows and the determinant formula in the manuscript, with the polar-angle fan start just specified. Associate each applicable row with a chosen edge and raw nonzero coefficient:

    row 0:  (0,5),  615861858493/66264900000
    row 1:  (1,2), −14202877137501601237/428735535000000
    row 6:  (0,6), −503670845202777/958568000000
    row 7:  (0,7),  136828790330869/105180150000
    row 8:  (2,8),  24328858333419/20525538500000
    row 9:  (2,9),  358736854091/101252520000
    row 10: (3,10), −16614965979/7118750000
    row 11: (4,11), −2653940217/1143032000

Omit rows 0,1 for the seed and omit row 1 for the ear. Select the associated edge columns in that same row order, and divide each row by its listed coefficient. For the seed the resulting minor is the identity matrix. For the ear and extension it is upper triangular with every diagonal entry one. Its only off-diagonal entries are in row 0:

    column (0,6): −3478800947769/79201369040,
    column (0,7): −824964430784/3534754241.

Each normalized maximal minor therefore has determinant exactly one. Every normalization is nonzero. This establishes all three ranks without trusting an opaque rank routine. The [exact JSON rank certificate](EXACT_RANK_CERTIFICATES.json) records every counterclockwise fan, row and column orders, raw coefficients and the normalized matrices. It also includes lexicographically sorted selected columns; the determinant is still one, since the extension requires exactly two column swaps and the other two certificates are already sorted.

The actual row graphs are connected and have incident one-entry edge columns. They are not closed active components. The balance weights assigned to boundary vertices do not create nonexistent compatibility rows there; this is exactly why the interior balances do not imply rank deficiency.

## 6. Separate direct Bernstein-gradient verification

As a second matrix construction, the audit analytically differentiates every quartic Bernstein basis polynomial. Values and first derivatives fix the nine vertex-adjacent coefficients; edge-middle coefficients are shared and triangle-corner interior coefficients remain independent. On each interior edge it subtracts the two polynomial normal derivatives at edge parameters 1/3 and 2/3. It separately checks that the endpoint derivative differences vanish identically in every remaining-coefficient and prescribed-jet column.

This computation uses neither the reduced-row formula nor the residual Bernstein equations. Since the derivative difference is cubic along the edge and its endpoint values vanish, its two interior evaluations are equivalent to identically vanishing normal derivative. Shared edge traces supply tangential agreement.

The directly differentiated remaining-coefficient matrices are:

- Seed: 42 by 75, rank 42; adding all 36 jet columns leaves rank 42.
- Ear: 46 by 79, rank 46; adding all 36 jet columns leaves rank 46.
- Extension: 56 by 98, rank 56; adding all 45 jet columns leaves rank 56.

All 144 endpoint normal-derivative checks pass. These full systems independently confirm the reduced-matrix conclusion: every prescribed first jet is attainable on each of these three original meshes.

## 7. Reproduction and remaining question

The [finite certificates](FOURTH_PASS_CERTIFICATES.json), [compact maximal minors](EXACT_RANK_CERTIFICATES.json) and [reproduction conventions](REPRODUCTION.md) specify the exact coordinates, weights, faces, determinant tables and reduced matrices. Active negative controls detect a changed new weight, a moved middle vertex and a reversed new triangle. The mathematical acceptance rests on the exact geometry, determinant identities and rank witnesses above.

The valid new progress is a conforming, internally balanced, rational nonpencil extension of the specified seed. The remaining task is a geometrically valid closed convex support with all required exterior attachments and full balance, or a proof that the remaining configurations are impossible. This audit proves neither alternative and makes no universal negative conclusion from unsuccessful construction attempts.
