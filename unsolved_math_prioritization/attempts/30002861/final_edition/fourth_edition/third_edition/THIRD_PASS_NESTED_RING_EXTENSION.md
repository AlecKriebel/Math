# Pencil propagation excludes closed nested hexagonal rings of every size

## Status and dependency

This is an additive result within the same third documented substantive pass for row 1761. It depends on the [twelve-vertex proof](THIRD_PASS_CEVA_OBSTRUCTION.md)'s algebraic pencil-collapse lemma and its boundary positivity lemma, and on the accepted fixed conforming-disk model. The [independent extension audit](INDEPENDENT_NESTED_RING_ACCEPTANCE.md) accepts this result.

Every geometric vertex mentioned below is distinct from every other vertex, as required by a conforming realization. This makes explicit the distinctness hypothesis already used in the pencil-collapse proof when excluding projectively coincident vertices. All listed triangles are nondegenerate.

**Result.** There is no balanced closed active core consisting of the central six-vertex pattern and any positive number of successive six-vertex triangulated annuli of the types described below. Coordinates and each intermediate ring may be nonsymmetric; no convexity of intermediate rings or of the initial inner hexagon is assumed. The terminal boundary is convex because it is the boundary of a closed active component. The number of support vertices is unbounded.

This is a theorem about a specified family of closed core topologies. It is not a universal theorem about every even triangulation, and does not by itself exclude differently shaped proper components in arbitrary larger full meshes.

## 1. Ring topology and number of vertices

Start with the six vertices I_0,...,I_5 and the four faces

    (I_0,I_1,I_2), (I_2,I_3,I_4),
    (I_4,I_5,I_0), (I_0,I_2,I_4).

Add n>=1 successive rings, each with six vertices. Between an inner ring V_0,...,V_5 and a new outer ring W_0,...,W_5, use either of these triangulations, with indices modulo six:

Forward:

    (W_i,W_(i+1),V_(i+1)),
    (W_i,V_(i+1),V_i).

Reverse:

    (W_i,W_(i+1),V_i),
    (W_(i+1),V_(i+1),V_i).

The choice may be made independently for each annulus. The two versions are related by reversing cyclic indices. There are 6(n+1) core vertices and 12n+4 faces. The terminal boundary vertices have induced degree four. In a closed component they are consequently strict convex corners, and the boundary has no straight subdivision vertices.

The colors of the initial inner vertices, in cyclic order, are A,C,B,A,C,B. These extend to each new ring: the new opposite vertex across an old boundary edge receives the missing third color. Each ring again has a three-periodic color sequence, so opposite terminal vertices W_i,W_(i+3) have the same color. Every triangle has all three colors.

As in the preceding report, use the normalized nonzero weights x_v and their homogeneous weighted vectors U_v=x_v(v_x,v_y,1)^T. Balanced edges obey

    det(U_v+U_w,U_u,U_z)=0

for their opposite vertices u,z.

## 2. Exact propagation through one annulus

**Lemma.** Let A,B,C be linearly independent homogeneous vectors and put S=A+B+C. Suppose the known inner triangulated region has

    U_v=D_color(v)+t_v S,

where D_A=A, D_B=B, and D_C=C. In particular, this holds for each edge of its six-vertex boundary and for the known opposite vertex across that boundary edge. If all the new annulus's relevant edge balances hold, all six new outer vertices also have exactly this form with the same A,B,C,S.

**Proof for the forward annulus.** First take a boundary edge of the known region with endpoint colors A,B, and known inside opposite vertex of color C. Rename its scalar coefficients as a,b,c, so its vectors are

    A+aS,    B+bS,    C+cS.

Its triangle is nondegenerate. The determinant in the basis A,B,C is

    det(A+aS,B+bS,C+cS)=1+a+b+c != 0.                  (1)

Let Z=(u,v,w)^T be the unknown weighted vector of the new opposite vertex, expressed in that basis. Edge balance is

    det(A+aS+B+bS,C+cS,Z)
      =(u-v)(1+a+b+c)=0.                               (2)

By (1), u=v. Thus Z lies in span(C,S), and can be written uniquely as

    Z=gamma C+pS.                                      (3)

Doing this around the old boundary places all six new vectors on the appropriate color lines. This step does not assume gamma is one or nonzero.

Now inspect the annulus edge joining this new vertex to the old endpoint of color B. Its two opposite vertices are the old endpoint of color A and the next new outer vertex, also of color A. Write the latter as

    Z_next=delta A+qS.

The two opposite geometric vertices are distinct. Their homogeneous vectors A+aS and delta A+qS are therefore linearly independent, so

    q-a delta != 0.                                   (4)

The edge balance expands exactly as

    det(gamma C+pS+B+bS,A+aS,delta A+qS)
      =(gamma-1)(q-a delta)=0.                         (5)

Equations (4)-(5) give gamma=1. Every new vertex appears as the first endpoint in such an annulus edge, so its base coefficient is one. This establishes the claimed form around the whole new ring.

All determinant expansions above have the common additional nonzero factor det(A,B,C) when expressed in the original homogeneous coordinates. No affine coordinate for the point S, or division by its last coordinate, has been used.

For the reverse annulus, reverse the cyclic indices in the same argument. ∎

The distinctness factor in (4) is essential and is an explicit model hypothesis, rather than an assumption of generic position. If delta=0, the two vectors are still independent whenever the two vertices are distinct, so this case is covered without special division by delta.

## 3. Induction and the terminal-boundary contradiction

**Theorem.** No balanced closed active core has one of the nested ring topologies in Section 1, for any n>=1.

**Proof.** For n=1, the initial central pattern plus first annulus is exactly the twelve-vertex pattern of the preceding report. Its pencil-collapse lemma uses only its 21 interior edges, not the six boundary-edge balances. It therefore applies unchanged when further rings are present. If the first annulus is reverse, use the opposite cyclic orientation and the same lemma.

Thus the first twelve weighted vectors have the form base_color+t_v S. For each further annulus, all known inside opposite vertices lie in the already constructed region. The propagation lemma therefore applies successively and forces the same form throughout all n rings.

In particular each opposite pair of terminal boundary vertices belongs to one of the three distinct lines span(A,S), span(B,S), span(C,S). Their opposite diagonals concur at the projective point S. As the boundary is a strictly convex hexagon, these diagonals intersect in their relative interiors. Hence S is finite and its affine point P is in the interior of the terminal hexagon.

Translate P to the affine origin. Then S has zero first two coordinates, so the two terminal weighted vectors in each same-color opposite pair share the same nonzero first-two-coordinate vector. Since P lies strictly between that pair of geometric vertices, their normalized weights must have opposite signs.

On the other hand, all six terminal boundary vertices are strict corners, and the boundary positivity lemma applies to every side using its actual exterior opposite vertex. All six terminal weights must have the same sign. This is a contradiction. ∎

## 4. Scope of the new restriction

This excludes balanced cores with 12,18,24,... vertices in these nested annular incidence patterns, irrespective of geometric symmetry or the admissible shape of intermediate rings. It excludes a countably infinite family of complete closed-core topologies, rather than a fixed-dimensional radial parameter family.

The proof does not claim that every closed component in a larger mesh is such a nested ring. It does not settle different layouts of the degree-four vertices, higher interior valences, other boundary sizes, or straight subdivided boundary sides. It also does not assert full row rank on every larger full triangulation merely because its complete vertex set can be arranged in such rings: a differently shaped proper closed component would need its own analysis.

Equations (1), (2), and (5), their nonzero-factor meanings, and the forward/reverse color propagation can be checked by the exact conventions in [REPRODUCTION.md](REPRODUCTION.md). The induction itself is the proof for all n.
