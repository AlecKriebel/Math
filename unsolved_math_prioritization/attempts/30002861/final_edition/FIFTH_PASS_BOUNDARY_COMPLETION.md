# Canonical exterior completion and boundary-chord restrictions

## Status and scope

This is the theoretical branch of the fifth and final shared substantive pass for row 1761 / problem 30002861 / OWR-13678-002, dated 13 October 2026 UTC. The lifetime total is unknown. The bundled row remains unsolved. The accepted fixed model is a finite conforming straight-line triangulation of a polygonal disk, with distinct vertices, nondegenerate triangles, independently prescribed values and first derivatives at every original vertex, and globally C1 piecewise quartics on those original triangles. See the [final guide](README.md), [independent acceptance](INDEPENDENT_BOUNDARY_COMPLETION_ACCEPTANCE.md), and [exact dependencies](DEPENDENCIES.md).

The results are general exact completion and obstruction criteria, not a complete answer to the existence question:

1. The already necessary strict-corner turning inequalities are sufficient for the forced exterior vertices to form a conforming canonical collar, including all straight side subdivisions. There is no additional exterior-placement problem after these inequalities hold.
2. For a specified internally balanced convex disk with the required degree parities, finitely many nonzero-determinant and boundary-balance checks are necessary and sufficient for a closed balanced realization in that collar.
3. No interior edge of a balanced closed support touches a strict corner and another boundary vertex. All boundary-to-boundary interior edges form a noncrossing matching of straight vertices, on explicitly forced lines. Consequently every triangle incident with a boundary edge has an interior vertex opposite that edge.

These conclusions do not imply that an admissible balanced convex disk exists or cannot exist. They do not recover global color-pencil containment. The companion construction branch's obstruction to extending its fixed rational nonpencil seed is separate and seed-specific.

The [accepted dependencies](DEPENDENCIES.md#dependencies-of-the-final-theory) link the closed-support theorem, signed balance and compact quadratic construction, corrected incident-edge-segment normal form, forced exterior attachment theorem and degree/color restrictions. The arguments below do not invoke a whole-supporting-line identity for a piecewise function, a maximum principle or a signed Hessian energy.

## 1. An elementary convex-polygon lemma

Orient a strictly convex polygon counterclockwise, with strict corners A_0,...,A_(k-1), and write e_i=A_(i+1)-A_i. Indices are cyclic. Its exterior turns are delta_i in (0,pi), with sum 2 pi.

We use the following elementary fact. Suppose a closed polygonal chain has nonzero edge vectors whose directions increase through exactly one full turn, with every successive direction gap in (0,pi). Then the chain is a strictly convex embedded polygon in that order.

Here is a proof that also supplies the needed global, rather than local, conclusion. Fix an edge and rotate its direction to angle zero. For the subsequent edges, the increments in signed distance to its supporting line are a positive block, possibly one zero increment at angle pi, and a negative block. The increments sum to zero by closure. Every partial sum at a nonincident vertex is strictly positive: it first increases, and during the decreasing block its remaining sum is strictly negative until the final endpoint. Thus every nonincident vertex lies strictly in the left half-plane of every directed edge. Each listed edge is therefore an exposed edge of the convex hull of the listed vertices. The list is its embedded strictly convex boundary. This also proves distinctness; a repeated nonincident vertex would violate the strict half-plane conclusion.

## 2. Forced exterior points satisfy all side inequalities

For each side i suppose

    delta_i+delta_(i+1)<pi.                             (1)

This is equivalently the exact determinant inequality

    D_i=det(e_(i-1),e_(i+1))>0.                        (2)

Indeed the counterclockwise direction gap from e_(i-1) to e_(i+1) is delta_i+delta_(i+1), which is in (0,2 pi). Define

    t_i=det(e_i,e_(i+1))/D_i >0,
    s_i=det(e_(i-1),e_i)/D_i >0,
    Q_i=A_i+t_i e_(i-1)=A_(i+1)-s_i e_(i+1).          (3)

The equality follows by resolving e_i=t_i e_(i-1)+s_i e_(i+1). These are exactly the forced exterior attachment points from the accepted zero-ray classification.

Let H_j(X)=det(e_j,X-A_j). The polygon lies in H_j>=0 for every j. Then

    H_i(Q_i)<0;
    H_(i-1)(Q_i)=H_(i+1)(Q_i)=0;
    H_j(Q_i)>0 for every other j.                     (4)

The first inequality follows from t_i>0 and det(e_i,e_(i-1))<0. The two equalities follow from (3). To prove *all* the remaining strict inequalities, replace the boundary chain A_(i-1),A_i,A_(i+1),A_(i+2) by A_(i-1),Q_i,A_(i+2). The two new edge vectors are positive multiples (1+t_i)e_(i-1) and (1+s_i)e_(i+1). All other edge directions and turns are unchanged; the turn at Q_i is the merged turn delta_i+delta_(i+1)<pi. The direction sequence still turns exactly once. The lemma in Section 1 proves that this new polygon is strictly convex. Its sides are precisely all old side lines except i. At its vertex Q_i only sides i-1 and i+1 are incident. Every other side inequality is therefore strict. This proves (4) without an assumption about side lengths, uniform turns, or symmetry.

In particular all Q_i are distinct: Q_i violates side i whereas every Q_j for j!=i satisfies it. No Q_i is a vertex of the old polygon, and no Q_i lies in K. Summing (1) also recovers k>=5, so the cyclic indexing used above cannot have triangular or quadrilateral exceptional coincidences.

## 3. The canonical collar theorem

Permit arbitrary conforming straight subdivisions along each strict side. Write its mesh vertices in order as

    A_i=B_(i,0), B_(i,1),...,B_(i,m_i)=A_(i+1).

Adjoin the points Q_i from (3), and the triangles

    (B_(i,j),Q_i,B_(i,j+1)),   0<=j<m_i,
    (A_i,Q_(i-1),Q_i).                                (5)

Their order in (5) is counterclockwise. Together with any conforming triangulation of K, they form a conforming triangulated polygonal disk whose boundary cycle is Q_0,...,Q_(k-1). Every old vertex of K is interior to this larger disk.

**Proof.** First consider the undivided side triangle T_i=conv(A_i,Q_i,A_(i+1)) and corner triangle C_i=conv(A_i,Q_(i-1),Q_i). They are nondegenerate: T_i has one point strictly outside its side line; the rays from A_i to its two Q points lie on the two distinct adjacent side lines. Equation (4) gives precise half-plane signatures:

- The relative interior of T_i violates exactly H_i>=0 and strictly satisfies all other side inequalities.
- The relative interior of C_i violates exactly H_(i-1)>=0 and H_i>=0, and strictly satisfies all others.

These signatures make their interiors pairwise disjoint and disjoint from K. They also prove the required lower-dimensional intersections. T_i meets K in A_i A_(i+1), C_i meets K only at A_i, T_i meets C_i in A_i Q_i and C_(i+1) in A_(i+1) Q_i, and C_i meets C_(i+1) only at Q_i. Other intersections are just the vertices already dictated by these incidences, or empty. For example, a corner triangle that does not border T_i violates a side inequality strictly satisfied in the relative interior and edges of T_i except at their prescribed shared endpoint. The strictness in (4) excludes an extra contact. This can also be read directly from the sets of zero side inequalities at each of the three vertices.

The abstract faces attach as one annulus: each T_i attaches to the old side, successive T_i are joined through C_(i+1), and its sole outer boundary consists of the edges Q_(i-1)Q_i. The established geometric intersections embed that annulus. Subdividing T_i by joining Q_i to the ordered B_(i,j) gives exactly the triangles in (5); their areas are positive multiples of the area of T_i, and they intersect in their prescribed common edges. This works for arbitrarily unequal positive subedge lengths. Attaching the annulus to K gives the claimed disk and boundary. In particular simplicity of the outer Q cycle is a proved consequence of these intersections, not a presumed condition. ∎

The outer Q polygon need not be assumed convex. Only its simplicity and the exact conformity of (5) are needed.

## 4. A finite necessary-and-sufficient completion test

Let K now be a specified finite convex conforming triangulated disk, with every mesh vertex distinct. Assume:

- every interior vertex of K has even degree;
- every strict boundary corner has even induced degree at least four;
- every straight boundary vertex has odd induced degree at least five;
- all strict-side inequalities (1), equivalently (2), hold.

Construct its canonical collar. For every edge vw of K let u,z be its two actual opposite vertices in the collared mesh. For an interior edge of K both belong to K. For a boundary subedge on strict side i, one is its old opposite vertex in K and the other is the forced Q_i. Put V_v=(v_x,v_y,1)^T, and define

    a_vw=det(V_v,V_u,V_z),
    b_vw=det(V_w,V_u,V_z).                             (6)

Their simultaneous signs depend on the chosen order u,z, which will not affect either test.

**Exact completion criterion.** K admits a realization as one closed balanced active component, preserving its coordinates and triangles, if and only if

    a_vw!=0 and b_vw!=0 on every edge of K,             (7)

and there are nonzero scalars x_v satisfying

    a_vw x_v+b_vw x_w=0 on every edge of K.             (8)

For a supplied full-support weighting that already balances every interior edge, only the boundary equations of (8) remain to be tested. If the interior-edge graph is connected, those weights are unique up to one common nonzero scalar, so a failed boundary equation cannot be repaired merely by choosing another normalization.

**Necessity.** In any closed-support realization the exterior-attachment theorem forces the same Q_i and the same outside triangle at every boundary subedge. Activity gives (7); the accepted normalized balance equation gives (8). Thus using another larger exterior triangulation cannot change these necessary boundary equations.

**Sufficiency.** Section 3 supplies a legal original mesh. A strict corner gains exactly two neighbors Q_(i-1),Q_i, and a straight boundary vertex gains exactly one Q_i. The listed parity assumptions make all vertices of K even-valence interior vertices of that mesh. The Q_i lie on its boundary and contribute no retained rows.

At a strict corner each edge to a Q has, as its two neighboring rays, opposite collinear rays along an adjacent strict side. At a straight vertex the two neighbors of its single Q ray are its two opposite boundary rays. The accepted row formula therefore vanishes on every edge from K to a Q. By (7) it is nonzero at both ends of every edge of K. Hence every vertex of K is nonsingular and retained, its active graph is exactly K's connected edge graph, and that component is closed. Face-color normalization converts (8) precisely into the left-dependency equation for those retained rows. The nonzero x_v thus make it balanced. The accepted second-pass theorem then supplies an actual failure of quartic vertex Hermite interpolation, including a suitable pure-gradient datum. ∎

This criterion is an exact *finite verification or construction interface*, not an existence proof: no internally balanced convex K satisfying the boundary tests is supplied here. The graph propagation criterion already decides (8); the new point is that the canonical collar makes these finite tests sufficient for an actual original mesh, rather than merely necessary algebra with unverified outside triangles.

For completeness, interior-edge connectivity under these boundary degree assumptions follows directly. A triangle with two boundary edges would have a degree-two vertex at their common endpoint. Thus every triangle has at least two interior edges, which connect its three vertices. The connected triangle-dual graph joins these local connected subgraphs. Consequently all vertices are in one interior-edge graph. With nonzero endpoint coefficients, its balance equations determine all x_v from one nonzero root value, whenever consistent.

## 5. Boundary transfer has no hidden division by zero

For each oriented boundary subedge v to w set

    tau_vw=-a_vw/b_vw.

This is an exact projective transfer, and (8) says x_w=tau_vw x_v. Its product around the boundary must equal one. This product is a useful necessary check, but it must not replace the individual boundary checks against the internally determined weights; it alone need not enforce their agreement with the interior.

In fact x_v+x_w is nonzero for every balanced active edge of a conforming mesh. If it were zero, x_v V_v+x_w V_w would represent the point at infinity along the edge line. Equation (8) places that vector in the span of the two opposite homogeneous vertices. Their line meets the edge line at a finite point, since the opposite vertices lie strictly on opposite sides of it. This is a contradiction. Thus the affine intersection point is exactly

    P_vw=(x_v v+x_w w)/(x_v+x_w).                     (9)

For a boundary subedge its other description is the intersection of the line u Q_i with that subedge's supporting line. Section 7 below proves u is interior to K in a balanced closed support, so P_vw lies strictly within the *whole strict side* A_i A_(i+1). It need not lie in the particular subedge. No assertion that all subdivided-side transfers are positive is made. On an unsubdivided strict side, (9) gives the accepted positive transfer.

All formulas (6)-(9) use actual finite vertices and exact determinant identities; none presumes a global color pencil.

## 6. Boundary polynomials from the actual exterior triangles

Let q be the nonzero compact C1 piecewise quadratic obtained from a balanced closed component, extended by zero outside K. At every support vertex v the accepted corrected normal form is

    q_T(X)=p_v(X)+x_v s_T L_a(X)L_b(X)/det(a-v,b-v),  (10)

for each counterclockwise triangle T=(v,a,b) in its full original fan, where L_a(X)=det(a-v,X-v), x_v is nonzero, and s_T is its alternating face sign. The polynomial p_v has q's value and gradient at v. In particular at a boundary vertex these are both zero. The restrictions of q and p_v agree on each *incident edge segment*, which is all that is used below.

At a strict corner v=A_i, use its actual exterior triangle

    T_ext=(v,Q_(i-1),Q_i).

It is nondegenerate and q is zero there. Equation (10) gives the polynomial identity

    p_v(X)=-x_v s_ext
      det(Q_(i-1)-v,X-v) det(Q_i-v,X-v)
      /det(Q_(i-1)-v,Q_i-v).                         (11)

This polynomial is nonzero because x_v!=0, its denominator is nonzero, and both line forms are nonzero. Its two zero lines are precisely the two distinct strict side lines through v. This conclusion does not merely infer nonzero p_v from its boundary zeros.

At a straight vertex v on side i, choose either actual exterior triangle containing v and Q_i. Its third vertex b is the adjacent mesh vertex along that side. With the corresponding orientation and sign, (10) yields

    p_v(X)=c_v det(b-v,X-v) det(Q_i-v,X-v),            (12)

where c_v is nonzero. The two zero lines are the strict side line and the line vQ_i. They are distinct because Q_i is outside the side half-plane. Equations (11)-(12) retain the actual exterior triangles, rather than closing a missing angular sector with invented rays.

## 7. The boundary-chord theorem

Call an edge of K with two boundary endpoints that is not itself a boundary edge a boundary chord.

**Theorem.** Every boundary chord joins two straight boundary vertices. Each straight vertex is incident to at most one boundary chord. If its endpoints v,w lie on strict sides i,j, respectively, then i!=j and

    Q_i, v, w, Q_j

are collinear in exactly that order (or the reversed listed order). In particular all chords form a noncrossing matching. Every triangle of K incident with a boundary edge has its vertex opposite that edge strictly interior to K. This is the meaning of “boundary triangle” here; merely touching a boundary vertex does not suffice.

**Proof.** On an edge vw the normal form gives q(w)=p_v(w). If both vertices are on the boundary, q(w)=0. For strict v, (11) puts w on one of v's two side lines. Convexity confines the intersection of each supporting line with K to that adjacent side segment. A conforming edge along such a segment can only join consecutive mesh boundary vertices: skipping an intervening vertex would violate conformity, and its segment belongs to the boundary. Therefore a boundary chord cannot touch v.

For straight v, (12) similarly allows a boundary neighbor only on its side line or on vQ_i. The first possibility gives only the ordinary adjacent boundary edges. Since v is in the relative interior of a strict side and Q_i is on the exterior side, the line vQ_i has exactly one ray entering K, namely the ray opposite Q_i. It exits the compact convex polygon at exactly one other boundary point. There is at most one mesh vertex there, so v is incident to at most one boundary chord. Applying the same argument at its other endpoint w shows it is also straight, on a different side, with Q_j beyond w away from v. This is exactly the asserted collinear order. The absence of crossing chords follows from conformity, and the degree-at-most-one assertion gives a matching.

Finally, suppose a triangle touching boundary edge vw had its third vertex u on the boundary. No triangle has two boundary edges under the induced boundary degree-at-least-four assumption, as proved in Section 4. Thus both uv and uw would be boundary chords, contradicting the matching property at u. Hence u is interior. ∎

The chord conclusion has two deliberately separate scopes. If there are no straight boundary vertices, there are no boundary chords at all. With straight vertices, the proof allows the specified matching; it does not assert that those configurations exist or that every chord is impossible.

## 8. Exact verification and remaining question

The [exact finite collar certificate](BOUNDARY_COMPLETION_CERTIFICATE.json) gives rational polygon controls, subdivisions, forced exterior vertices, full original fans and individual boundary transfers. The [independent collar certificate](INDEPENDENT_COLLAR_CERTIFICATE.json) adds a complete 27-by-12 magnitude matrix with a nonzero maximal minor, compatible face-sign-normalized rows and common edge factors, actual exterior polynomial factorizations, and broader exact subdivision controls. The [reproduction guide](REPRODUCTION.md) specifies all geometric and normalization conventions.

The [independent acceptance](INDEPENDENT_BOUNDARY_COMPLETION_ACCEPTANCE.md) covers the universal proofs and finite controls. The existing integer support remains magnitude-unbalanced: collar existence does not convert sign balance into full balance. The local strict and straight normal forms retain nonzero boundary weights and actual exterior triangles. A false subedge positivity rule, collapsed collar, erroneous transfer or alleged dependency in the full-rank control fails its defining exact condition.

The all-polygon collar theorem and all-support chord theorem rest on the proofs above. Finite examples and symbolic checks corroborate their algebra and implementation, rather than serving as universal evidence.

The precise unresolved problem is now: find a finite conforming convex triangulated disk with the stated parity and activity requirements, outside the already excluded global color-pencil class, whose nonzero internally propagated weights also satisfy every forced-Q boundary equation; or prove that none exists. The exterior collar, once the strict-turn inequalities hold, is not a further unknown. Neither the local boundary restrictions nor the companion fixed-seed obstruction resolves this remaining global question.
