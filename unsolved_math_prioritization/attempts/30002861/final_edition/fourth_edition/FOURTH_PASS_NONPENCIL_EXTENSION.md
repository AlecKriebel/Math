# An exact incidence-changing disk extension of the rational quartic seed

## Status and scope

This is a construction branch of the **same fourth newly documented substantive pass** on row 1761 / problem 30002861 / OWR-13678-002, dated 13 October 2026 UTC. It adds no separate pass; the lifetime total is unknown. The bundled row remains unsolved. See the [edition guide](README.md), [accepted dependencies](DEPENDENCIES.md), [independent acceptance](INDEPENDENT_NONPENCIL_EXTENSION_ACCEPTANCE.md), and [exact certificate](FOURTH_PASS_CERTIFICATES.json).

**Result.** The auxiliary twelve-vertex seed from the third pass is independently recomputed and verified here. It admits an exact rational extension with a different incidence pattern that satisfies every interior signed-Ceva balance equation and genuinely leaves the original three-line pencil. The underlying topological space remains a disk; the triangulation incidence changes. The extension has 15 vertices, 35 edges and 21 faces. Its 28 interior edges all balance. It is still nonconvex, and its actual reduced quartic matrix has full row rank eight.

Thus this is **not a closed balanced support, not a quartic counterexample, and not a proof of universal interpolation**. Its substantive positive content is that the very seed supplied for this pass can escape the pencil by a local change of triangulation incidence. The accepted nested-hexagon propagation theorem cannot exclude this extension on the premise that it remains a pencil.

The original seed was explicitly not part of the independently accepted third-pass ring theorem. The seed, reflex-ear intermediate and nonpencil extension are now covered by the [fourth-pass independent acceptance](INDEPENDENT_NONPENCIL_EXTENSION_ACCEPTANCE.md). This does not retroactively enlarge the third-pass theorem.

The [companion theoretical branch](FOURTH_PASS_GLOBAL_INCIDENCE.md) handles the general concurrent-color-line obstruction. This report makes no claim that balance on arbitrary even triangulations forces a global pencil.

## 1. Model and exact necessary equations

The underlying model remains a finite conforming straight-line triangulation of a polygonal disk with nondegenerate original triangles. All vertex values and both first derivatives are independently prescribed, and the requested interpolants are globally C1 piecewise polynomials of degree at most four on the original triangles.

For a prospective closed balanced support, the accepted face normalization gives nonzero real numbers x_v and weighted homogeneous vectors

    U_v = x_v (v_x,v_y,1)^T.

If an edge vw has opposite vertices u,z, its necessary balance equation is

    det(U_v+U_w,U_u,U_z)=0.                         (1)

The equation does not require x_v+x_w to be nonzero. All equations asserted below are exact rational identities. For edges on an auxiliary disk's boundary, no outside opposite vertex is invented, and no boundary balance equation is claimed.

The actual reduced matrix is reconstructed separately. At an even interior vertex with counterclockwise neighbor vectors d_i and a_i=det(d_i,d_(i+1)), its row coefficients are

    r_i = (-1)^i det(d_(i-1),d_(i+1))/(a_(i-1)a_i).

Boundary vertices contribute no such row. This distinction explains why satisfying all internal versions of (1) does not by itself make an auxiliary disk a counterexample.

## 2. Independent verification of the supplied seed

Number the outer vertices O_i by i and the inner vertices I_i by 6+i, for i=0,...,5. Let colors A,B,C correspond to the spatial vectors

    d_A=(1,0), d_B=(0,-1), d_C=(-1,1).

The twelve colors in vertex order are

    B,A,C,B,A,C,A,C,B,A,C,B.

Define integers

    q = (9,-25,-1,-1,-1,-1,-7,15,-7,3,3,3),

and set

    x_i = q_i + (i+1)/1000,
    P_i = d_color(i)/x_i.

The 16 oriented triangles are, with indices modulo six,

    (i,i+1,6+(i+1)), (i,6+(i+1),6+i), i=0,...,5,

where i+1 in the first outer slot is reduced modulo six, together with

    (6,7,8), (8,9,10), (10,11,6), (6,8,10).

Every triangle is nondegenerate and positively oriented. All 120 pairs of triangles intersect in exactly their prescribed common simplex. All twelve vertex links are verified, the triangle adjacency graph is connected, the boundary is one simple cycle, and V−E+T=1. The complex is therefore a conforming embedded disk, rather than just an oriented list of triangles.

All 21 interior edges satisfy (1), with both endpoint determinant coefficients nonzero. The boundary cycle is (0,1,2,3,4,5), and its first two turns are negative:

    turn at 0 = −4247750000/55914239003,
    turn at 1 = −293000000/3867792707.

The retained reduced rows are precisely vertices 6,...,11. The reconstructed R has shape 6 by 27 and rank 6. Adjoining the jet matrix H leaves rank 6. Consequently the original auxiliary disk admits arbitrary quartic first jets and is not a counterexample.

These results confirm the mathematical content of the supplied seed without elevating its earlier author certificate to prior independent acceptance.

## 3. Filling one reflex ear

Add the positively oriented face

    (5,1,0).                                         (2)

It fills the reflex ear at vertex 0. Vertex 0 becomes a nonsingular degree-four interior vertex. The boundary becomes the five-cycle (1,2,3,4,5), which remains nonconvex. No vertex or coordinate is changed.

The two newly interior edges (0,1) and (0,5) balance automatically: their two opposite vertices have the same color, and the original weighted vectors have the common-pencil form. For clarity, a fixed homogeneous realization of that form is

    A=(1,0,0)^T, B=(0,-1,0)^T, C=(−1,1,1)^T,
    S=A+B+C=(0,0,1)^T.

Each original U_i is its color base plus a multiple of S. If an edge has endpoint colors A and B, its endpoint sum is in span(C,S), and both opposite C-colored vectors also lie in that plane. The other color cases are cyclic.

Exact geometry checks cover all 136 face pairs after (2). This disk has 12 vertices, 28 edges and 17 triangles, with 23 balanced interior edges. Its actual reduced matrix has shape 7 by 28 and rank 7.

## 4. A three-vertex fan that escapes the pencil

### 4.1 Coordinates, weights and faces

To the disk of Section 3, add the following vertices, colors and weights:

| Vertex | Color | Coordinate | Weight |
|---|---|---|---|
| 12 | B | (0, −96275/2502452) | 87716502/3311875 |
| 13 | C | (1/2, −233924171/450441360) | −2 |
| 14 | B | (0, −866425/22522068) | 70181301/2649650 |

Add four positively oriented triangles:

    (1,5,12), (1,12,13), (1,13,14), (1,14,2).          (3)

They fill a portion of the remaining reflex pocket at vertex 1. Vertex 1 becomes a nonsingular degree-eight interior vertex. The new boundary is

    (2,3,4,5,12,13,14).

The other original faces and all original coordinates and weights are retained exactly.

### 4.2 Direct rational construction, without optimization

The two sides of the remaining pocket run from P_1 to P_5 and P_2. Their intersections with x=0 have ordinates

    l = −125/3249, h = −200/5199, with l<h<0.

Choose P_12 and P_14 at the one-quarter and three-quarter points of this interval:

    P_12=(0,(3l+h)/4), P_14=(0,(l+3h)/4).

At x=1/2, take P_13 to have the mean ordinate of the same two side lines. This gives exactly the coordinates in the table. These three points are in increasing angular order in the missing fan at P_1, and strictly inside the pocket.

There are five newly interior edges: the former boundary edges (1,5),(1,2) and the three spokes (1,12),(1,13),(1,14).

Across (1,5) and (1,2), the known opposite vertices are respectively 0 and 8, both of color B. The endpoint sums lie in the plane x=0, so choosing P_12 and P_14 on x=0 makes both old-edge equations hold, regardless of their nonzero weights.

The opposite vertices across the middle spoke (1,13) are 12 and 14, which are distinct points on x=0. The first coordinate of U_1 is 1. Set x_13=−1/(P_13)_x=−2; the first coordinate of U_13 is then −1. Hence U_1+U_13 lies in x=0, giving the middle equation exactly.

The two remaining equations are linear in x_12 and x_14:

    det(U_1+x_12 V_12,U_5,U_13)=0,
    det(U_1+x_14 V_14,U_2,U_13)=0,

where V_i=(P_i,1)^T. Their nonzero coefficients give the unique values printed in the table. The sign difference from exchanging two determinant columns has no effect on a zero equation. This solves every newly introduced interior balance equation without numerical optimization or approximate rational reconstruction.

### 4.3 Genuine departure from the old pencil

The old color-C vertices 2 and 5 lie on y=−x. The new color-C vertex 13 does not. More explicitly,

    det(V_2,V_5,V_13)
      = −217587275/3719962464204 != 0.                (4)

Thus this coloring has no single projective line containing all its C-colored vertices. In a connected triangulated disk a proper vertex three-coloring is unique up to relabeling once one face is fixed: adjacent faces force the color of the third vertex. Therefore changing the three color names cannot restore global three-line geometry.

The extension is outside the globally concurrent three-color-line class and outside the complete nested-hexagonal-annulus incidence family. This does not contradict the accepted propagation theorem, which was proved for its explicitly specified complete annuli.

## 5. Full geometry, matrix checks and remaining obstruction

The extension has

    V=15, E=35, T=21, boundary vertices=7,
    interior edges=28.

Exact half-plane intersection checks cover all 210 triangle pairs. Every pair has exactly its specified common simplex. All vertex links, face connectivity, the single boundary cycle and Euler characteristic are checked independently. Every face has three distinct colors. All 28 equations (1) hold, and both endpoint coefficients are nonzero on every interior edge.

The eight actual even interior vertices are

    0,1,6,7,8,9,10,11,

with degrees

    4,8,6,4,6,4,6,4.

The directly reconstructed reduced matrix R has shape 8 by 35 and rank 8. The augmented matrix [R H] also has rank 8. The three quadratic moment identities are checked in every retained row. Thus arbitrary quartic vertex first jets remain interpolable on this extension.

Two new boundary turns are negative:

    turn at 12 = −94625/3198133656,
    turn at 14 = −1324825/44909003592.

In particular, the convex-support requirement has not been met. The boundary vertices 12 and 14 also have induced degree three, so they cannot simply be declared legal straight boundary vertices of a closed active support. No feasible outside attachment triangles or full closed-component equations have been supplied.

The precise progress is therefore an exact, conforming, internally balanced **nonpencil extension of the specified seed**. The missing task is to complete a convex support, retaining full balance and feasible exterior triangles, or prove that no such completion or no such support is possible. This report draws no universal negative conclusion from unsuccessful searches; no numerical optimization is used in the reported construction.

## 6. Exact reproduction

The [finite certificate](FOURTH_PASS_CERTIFICATES.json) gives the seed coordinates and weights, both exact extension steps, explicit faces and boundaries, all interior balance determinants, and nonzero maximal minors of the three actual reduced matrices. The [reproduction conventions](REPRODUCTION.md) fix indexing, rational arithmetic, determinant order, geometry tests, cyclic row normalization and the rank witnesses. The seed can also be reconstructed directly from the displayed rational formula, and the new fan from the exact line intersections and linear solves above.

The [independent acceptance](INDEPENDENT_NONPENCIL_EXTENSION_ACCEPTANCE.md) verifies each stage and its scope. Reversing a new face makes its orientation negative; changing a new weight or the middle coordinate breaks the specified balance equation. These are controls on the finite construction, not evidence that a convex completion is impossible.

The exact geometry, actual reduced ranks and noncollinearity are finite mathematical certificates. The generic fan explanation proves why these particular equations were solved; it does not claim that arbitrary geometry or arbitrary fan lengths will work.
