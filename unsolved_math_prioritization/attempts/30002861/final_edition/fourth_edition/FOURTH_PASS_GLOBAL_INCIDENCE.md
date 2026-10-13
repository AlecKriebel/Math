# Global color propagation, pencil normalization, and an exact nonpencil control

## Status and scope

This is a theoretical branch of the fourth newly documented substantive pass for row 1761 / problem 30002861 / OWR-13678-002, dated 13 October 2026 UTC. All branches and audits belong to the same fourth pass; the lifetime total is unknown. The bundled row remains unsolved. See the [edition guide](README.md), [accepted dependencies](DEPENDENCIES.md), [independent acceptance](INDEPENDENT_GLOBAL_INCIDENCE_ACCEPTANCE.md), and [exact certificate](FOURTH_PASS_CERTIFICATES.json).

The accepted fixed model is a finite conforming straight-line triangulation of a polygonal disk, with distinct mesh vertices and nondegenerate original triangles. A closed active component induces a convex triangulated support K. Its interior degrees are even; its strict boundary corners have even induced degree at least four; its straight boundary vertices have odd induced degree at least five. Every induced edge is active. The original exterior triangles are retained when boundary balance or exterior attachment is used.

For a balanced component, the accepted normalized nonzero dependency weights x_v give homogeneous vectors

    U_v = x_v (v_x,v_y,1)^T.

An interior support edge vw, with opposite vertices u,z, satisfies exactly

    det(U_v+U_w,U_u,U_z)=0.                              (B)

The accepted exterior-attachment theorem also supplies at least five strict boundary corners and the boundary positivity lemma on an unsubdivided side.

The results here are:

1. Even interior valence gives a globally consistent vertex three-coloring on the entire disk, including its boundary. The boundary color word has precise parity restrictions.
2. On a closed support, containment of each color class in one of three distinct concurrent projective lines, together with (B), forces the fixed-base normalization. Thus the previously established fixed-base pencil obstruction excludes every global color-pencil support, regardless of topology or subdivisions.
3. A constructive line/base propagation rule is valid beyond the ring incidence. It is a sufficient certificate, not a claim that it always reaches every vertex.
4. An exact eight-vertex conforming disk, with one nonsingular degree-four interior vertex and one degree-six interior vertex, satisfies every interior balance equation but is not a color pencil. It has a reflex boundary corner and is not a closed-support candidate. This demonstrates the essential missing step in any attempt to infer pencil collapse merely from even valence, degree-four defects, and interior balance.

No universal quartic interpolation theorem or quartic counterexample is claimed. No literature novelty or worldwide openness claim is made. The corrected incident-edge-segment normal form is not strengthened or used as a whole-line identity for the piecewise function.

## 1. Vertex three-coloring on an even triangulated disk

**Lemma 1.** A triangulated topological disk whose interior vertices all have even degree admits a proper vertex three-coloring. Each triangle has all three colors. The coloring is unique up to a global permutation of the colors.

**Proof.** Label the three vertices of one triangle A,B,C. When crossing an interior edge into the adjacent triangle, its two shared vertices keep their labels and the new opposite vertex receives the missing label. This transport is uniquely determined and invertible.

The embedded triangle-dual graph is connected. Its bounded faces correspond to interior primal vertices; boundary vertices do not create bounded dual faces. Traversing the dual facial walk around an interior vertex fixes the color of that vertex and successively alternates its two remaining neighbor colors. Its transport is the identity exactly when the interior degree is even, as assumed.

Every loop in a connected plane graph is a product of conjugates of its bounded facial walks and immediate edge reversals. One can see this by successively removing enclosed bounded faces from a simple loop, then splitting a general loop at repetitions. Transport around every generator is the identity. Hence transport is path-independent, including for triangles adjacent to the boundary.

The transported triangle labels therefore agree on shared vertices. All triangles incident to any one primal vertex form a connected cycle or path, so the resulting label of that vertex is globally unambiguous. Every edge belongs to a triangle, so its endpoints have different colors. Finally, any two proper three-colorings agreeing on one triangle agree across every dual edge, proving uniqueness up to the initial color permutation. No condition on boundary degree was needed for this lemma. ∎

This is a vertex-coloring proof. The accepted two-coloring of faces alone is not being treated as an automatic substitute.

## 2. The boundary word and a sharper defect count

List the boundary vertices counterclockwise as v_0,...,v_(b-1), with colors c_i in Z/3Z. Adjacent colors differ, so write

    c_(i+1)-c_i = epsilon_i modulo 3,
    epsilon_i in {+1,-1}.

At a boundary vertex of induced degree d, its link is a path on d neighbors. Along this path the other two colors alternate. The two endpoint neighbors are the previous and next boundary vertices. Their colors are equal exactly when d is odd.

For a closed support this gives

    epsilon_i =  epsilon_(i-1) at a strict corner,
    epsilon_i = -epsilon_(i-1) at a straight vertex.      (1)

**Corollary 2.** The number s of straight boundary vertices is even. If s=0, the number k=b of strict corners is divisible by three and is at least six. If k=5, then s>=2 and b>=7.

**Proof.** Following the nonzero epsilon around its cycle returns it to its starting value, so the number of sign reversals in (1) is even. With no reversal all increments agree; closing the color word forces 3 to divide b. The accepted exterior-attachment theorem gives k>=5. The remaining conclusions follow. ∎

Let N4 count interior support vertices of degree four. Euler's disk identity gives the exact refinement

    2 N4 = 6
      + sum_(interior degree >=8) (degree-6)
      + sum_(strict boundary) (degree-4)
      + sum_(straight boundary) (degree-4).              (2)

All sums on the right are nonnegative, and each straight boundary vertex contributes at least one. Since s is even,

    N4 >= 3+s/2.                                       (3)

In particular, a closed support with only three degree-four interior vertices has no straight subdivision vertex. It then has a multiple of three strict corners, at least six. A five-strict-corner support requires at least four degree-four interior vertices. The previously accepted degree restrictions and Euler identity are the inputs; (1)-(3) record their combined consequences.

## 3. Mere color-pencil containment forces a common base coefficient

The following normalization result separates geometric line containment from the stronger vector statement that was essential in the ring proof.

**Lemma 3 (interior-edge connectivity).** In a triangulated disk with no boundary vertex of degree two, the graph consisting of all vertices and all interior edges is connected.

**Proof.** A triangle with two boundary edges would have, at their common boundary endpoint, a link path containing the edge joining both endpoints of that path. This forces the path to have just that one edge, giving degree two. Thus each triangle has at least two interior edges. Those edges connect all three triangle vertices. Adjacent triangles share an interior edge, and the triangle-dual graph is connected. Their connected three-vertex subgraphs therefore join to give the claim. ∎

**Lemma 4 (pencil normalization).** Let a triangulated disk have no degree-two boundary vertex, distinct geometric vertices, a proper vertex three-coloring, nonzero weights, and balance (B) on all its interior edges. Suppose the vertices of each color lie on the corresponding member of three distinct concurrent projective lines. Then there are linearly independent homogeneous vectors A,B,C, with S=A+B+C representing the common point, such that

    U_v = D_color(v) + t_v S,                           (4)

where D_A=A, D_B=B, and D_C=C. In particular no vertex is the common point.

**Proof.** First choose a nonzero representative S of the common projective point. In the two-dimensional quotient space R^3/<S>, the three distinct color lines become three distinct one-dimensional subspaces. Their representatives have a linear relation with three nonzero coefficients. Scaling representatives on the first two lines and choosing the representative on the third yields vectors A_0,B_0,C_0 on their respective planes with

    A_0+B_0+C_0=S.

For clarity, choose independent quotient vectors a,b for the first two lines so that -(a+b) spans the third, lift them to A_0,B_0, and put C_0=S-A_0-B_0. Then A_0,B_0,S are independent, so A_0,B_0,C_0 are independent. Each color plane is span(D_c,S).

Write the actual weighted vectors, without rescaling them separately, as

    U_v=alpha_v D_color(v)+t_v S.

Zero alpha is provisionally allowed; it would mean the vertex is the common point.

Across an interior edge with endpoint colors A,B, both opposite vertices have color C. Those vertices are distinct and their weights are nonzero, so their two homogeneous vectors are linearly independent. Since both lie in the two-dimensional C plane, they span that entire plane. Balance (B) therefore says

    alpha_v A_0+alpha_w B_0+(t_v+t_w)S
        belongs to span(C_0,S).

In the quotient, [C_0]=-[A_0]-[B_0], and [A_0],[B_0] are independent. Thus alpha_v=alpha_w. The same argument applies to every interior edge, irrespective of its colors.

Lemma 3 now forces every alpha_v to be a single constant alpha. It cannot be zero, since then every vertex would represent the common point, contradicting distinctness and nondegenerate triangles. Replace A_0,B_0,C_0,S by alpha times themselves and replace t_v by t_v/alpha. This gives (4). This is one common change of basis, not an independent renormalization of the already fixed dependency coordinates. ∎

This proof covers an initially permitted vertex at the common point, a common point at infinity, and arbitrary signs of all weights. Their exclusions, where appropriate, follow from the argument rather than being generic-position assumptions.

## 4. A global color-pencil exclusion

**Theorem 5.** No balanced closed active support can have all vertices of each of its three color classes on one of three distinct concurrent projective lines.

**Proof.** A closed support has no degree-two boundary vertices. Lemma 4 supplies the fixed-base form (4), and in particular no vertex represents S. Two different color lines meet only at S. Consequently any mesh vertex lying on one of these lines has exactly that line's color.

Each color line is an actual affine line, since it contains finite mesh vertices. If it is not supporting for the convex polygon K, it meets the boundary of K in at most two points. If it is supporting and contained two boundary mesh vertices, the entire boundary chain between them along the corresponding straight side would lie on that line. Every vertex in that chain would have the same color, including the endpoints of at least one boundary mesh edge. This contradicts proper coloring. Hence a supporting color line contains at most one boundary mesh vertex. This handles possible straight boundary segments explicitly.

There are three color lines, so the total number of boundary vertices satisfies b<=6. The exterior-attachment theorem gives at least five strict corners. By Corollary 2 any straight vertices would occur at least twice and would give b>=7. Therefore there are no straight vertices. The remaining strict-corner count is a positive multiple of three between five and six, hence exactly six.

The boundary colors repeat A,B,C,A,B,C, up to reversal and permutation. Each opposite pair lies on its color line. Thus the three opposite diagonals of the strictly convex hexagon meet at S. Two such diagonals have alternating boundary endpoints and intersect in the relative interiors of both segments. It follows that S is a finite point P in the interior of K. This establishes finiteness and interiority before using any affine coordinate for S; it also rules out the cases of S at infinity or on the boundary.

Translate P to the affine origin. The first two coordinates of S are now zero. In (4), two opposite boundary vertices of one color therefore have the same planar numerator, namely the first two coordinates of that color's base vector. That numerator is nonzero: otherwise the base vector and S would be proportional, contrary to independence of A,B,C. Since P lies strictly between these boundary vertices, their geometric displacement vectors are oppositely directed. Their weights must therefore have opposite signs.

Every boundary side is unsubdivided. The accepted boundary positivity lemma, applied to its actual exterior opposite vertex, gives the same sign for the weights at its two endpoints. Propagating around the boundary makes all six signs equal. This is the contradiction. ∎

The theorem is independent of the interior combinatorial pattern, interior degree distribution, and symmetry. Its additional hypothesis is global color-pencil containment. No claim that arbitrary balanced supports satisfy that hypothesis is made.

## 5. Exact propagation certificates without a ring assumption

Fix independent A,B,C and S=A+B+C. A vertex is *line-certified* when its actual U vector has a proved representation alpha D_color+tS; it is *base-certified* when alpha is proved to be one. These terms describe a proof procedure only.

Two local rules follow directly from (B).

**Line rule.** Suppose a triangle of colors A,B,C is base-certified, with vectors A+aS, B+bS, C+cS. Across its AB edge, the other opposite vertex Z of color C is line-certified. Indeed nondegeneracy gives

    det(A+aS,B+bS,C+cS)
      = (1+a+b+c) det(A,B,C) != 0.

Writing Z=(u,v,w) in the A,B,C basis, edge balance becomes

    (u-v)(1+a+b+c) det(A,B,C)=0.

Thus u=v, exactly the C-plane condition.

**Base rule.** If all four vertices around an interior edge are line-certified, its endpoints have equal base coefficients. This is the quotient-space calculation in Lemma 4. If either endpoint is already base-certified, the other becomes base-certified. The two opposite vertices are distinct, so they span their color plane even if one coefficient was provisionally zero.

The rules can be applied in any order and on any triangulated incidence pattern. Each successful application adds a proved assertion; no assumption of geometric genericity is used. If they certify all vertices as line-contained in the same three planes, Theorem 5 rules out the proposed balanced closed support. If they stall, no impossibility conclusion follows. The rules do not claim that every degree-four star or every even triangulation generates a globally exhaustive certificate.

A finite closure witness consists of the initial exact fixed-base patch, its reference A,B,C,S, and an ordered list of rule applications naming their edges and vertices. Every application can be independently checked against the actual face incidences, the nondegeneracy and distinctness hypotheses, and the displayed identities. This extends the available certification interface beyond uniform hexagonal annuli, without presuming that a new topology has actually passed it.

## 6. Exact nonpencil control with an interior four-star

Consider the eight rational vertices, in the listed order:

    v=(0,0), a=(1,0), b=(0,1), c=(-1,-1),
    d=(1,-1), z1=(3,-1), z2=(4,-7/4), z3=(2,-2/3).

Take the following eight counterclockwise triangles:

    (v,a,b), (v,b,c), (v,c,d), (v,d,a),
    (a,d,z3), (a,z3,z2), (a,z2,z1), (a,z1,b).

Their doubled areas, in this order, are

    1, 1, 2, 1, 1, 1/4, 1/2, 1.

The boundary cycle is

    b,c,d,z3,z2,z1.

The only interior vertices are v and a, of degrees four and six respectively. The four rays at v have four distinct supporting lines, so its degree-four star is nonsingular.

Use these nonzero weights in the same vertex order:

    x=(1, 1, -1/3, -1/4, 1/2, 5, 4/5, -12/7).          (5)

For each interior edge vw, choose the two opposite vertices u,z in the explicit opposite-vertex order of the [finite certificate](FOURTH_PASS_CERTIFICATES.json) and put

    D_v=det(z-v,u-v),  D_w=det(u-w,z-w).

The exact list is:

    edge va:   D_v=1,     D_a=1;
    edge ab:   D_a=-1,    D_b=3;
    edge vb:   D_v=1,     D_b=-3;
    edge vc:   D_v=1,     D_c=-4;
    edge vd:   D_v=-1,    D_d=-2;
    edge ad:   D_a=-2/3,  D_d=-4/3;
    edge az3:  D_a=-3,    D_z3=7/4;
    edge az2:  D_a=-1/3,  D_z2=-5/12;
    edge az1:  D_a=-5/4,  D_z1=-1/4.

Every entry is nonzero, and (5) satisfies x_v D_v=x_w D_w on all nine edges. Thus every interior edge is active and satisfies the full magnitude equation (B), not merely its sign.

A proper three-coloring is

    A: a,c;
    B: b,d,z2;
    C: v,z1,z3.

The three B vertices are not collinear:

    det(d-b,z2-b)=21/4 != 0.

By Lemma 1 all proper three-colorings differ only by a color permutation, so the disk has no alternative proper coloring that turns it into a color pencil. In particular its vectors cannot have the fixed-base pencil form.

It is not a convex support. At z3 the counterclockwise boundary turn is

    det(z3-d,z2-z3)=-7/4 < 0.

Therefore it cannot be a closed active component under the accepted support theorem. Its boundary equations against genuine exterior triangles have not been asserted or supplied. The example is a sharp control against the implication

    even interior degrees + an interior nonsingular four-star
      + all interior magnitude balances => global pencil.

It is not a counterexample to an implication that also assumes the entire closed-support geometry.

## 7. Exact verification and remaining obstruction

The [finite certificate](FOURTH_PASS_CERTIFICATES.json) gives the eight-vertex disk, exact opposite-vertex orders, endpoint determinants, rational weights, boundary and coloring, together with a nonzero maximal minor of its actual reduced quartic matrix. Its two retained rows are independent. Thus this auxiliary disk admits arbitrary quartic vertex first jets; the interior balanced weights are not a left dependency of its actual reduced matrix.

The [reproduction conventions](REPRODUCTION.md) specify exact reconstruction of face incidence, vertex links, all 28 triangle-pair intersections, the boundary cycle, connectivity, degree parity, Euler characteristic, all nine normalized and homogeneous edge balances, and the noncollinear color triple and reflex turn. The [independent acceptance](INDEPENDENT_GLOBAL_INCIDENCE_ACCEPTANCE.md) checks the global arguments and local algebra, including nonzero factors and the point at infinity.

The global proofs of coloring, boundary restrictions, interior-edge connectivity, and convex-pencil exclusion are not conclusions from finite testing. The finite checks corroborate their local algebra and the explicit control.

The remaining task is a balanced closed support outside the global color-pencil class, or a proof that the convex closed-support hypotheses force that class or another contradiction. The control above shows precisely why a purely interior, single-four-star propagation argument is insufficient. The three-coloring itself is now justified globally; projective color-pencil containment remains a genuinely additional geometric condition.
