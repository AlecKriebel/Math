# Independent acceptance of the fixed-candidate additive-completion obstruction

## Decision and exact scope

**Accepted without mathematical correction.** The specified fifteen-vertex, twenty-one-face nonpencil disk has no finite convex, internally balanced, conforming straight-line completion that retains every old geometric triangle as a face and assigns every vertex a nonzero normalized weight. This remains true if the original weights may all be reassigned.

This audit belongs to the **same fifth and final shared substantive pass**, dated 13 October 2026 UTC, for row 1761 / problem 30002861 / OWR-13678-002. It adds no pass; the lifetime total is unknown. The bundled row remains unsolved.

The accepted [construction theorem](FIFTH_PASS_ADDITIVE_OBSTRUCTION.md) needs no mathematical correction. This independent report supplies its acceptance. The [final guide](README.md), [dependencies](DEPENDENCIES.md) and [reproduction conventions](REPRODUCTION.md) identify the exact scope and mathematical inputs.

The stopping theorem excludes the entire fixed-face additive-completion class, including simultaneous additions, arbitrarily many new vertices, arbitrary fan lengths, new triangles using old nonincident vertices, and arbitrary nonzero reassignment of the old weights. It does **not** exclude retriangulating or subdividing old faces, moving old coordinates, or starting from a different candidate. It neither constructs a quartic interpolation counterexample nor proves universal quartic interpolation. The general quartic question remains unresolved.

## 1. Independently reconstructed candidate and geometry

The independent reconstruction uses exact integer and rational arithmetic, without taking a prior construction's result as a premise. It reconstructs the first twelve points from colors

    B,A,C,B,A,C,A,C,B,A,C,B

and directions d_A=(1,0), d_B=(0,-1), d_C=(-1,1), with

    q=(9,-25,-1,-1,-1,-1,-7,15,-7,3,3,3),
    x_i=q_i+(i+1)/1000,
    P_i=d_color(i)/x_i.

It independently generates the remaining points from the preceding fan construction: the quarter and three-quarter positions between the x=0 intercepts l=-125/3249 and h=-200/5199, and the mean side-line ordinate at x=1/2. These reproduce exactly

    P_12=(0,-96275/2502452),          x_12=87716502/3311875,
    P_13=(1/2,-233924171/450441360), x_13=-2,
    P_14=(0,-866425/22522068),        x_14=70181301/2649650.

Their colors are B,C,B. The faces are the twelve annular triangles

    (i,i+1,6+(i+1)), (i,6+(i+1),6+i),  i=0,...,5,

with indices reduced modulo six before the offset 6 is added, followed by

    (6,7,8), (8,9,10), (10,11,6), (6,8,10), (5,1,0),
    (1,5,12), (1,12,13), (1,13,14), (1,14,2).

Sequential exact convex-polygon clipping independently verifies every one of the 210 triangle-pair intersections. This is a different geometric procedure from the source verifier's enumeration of edge intersections and contained vertices. Point and segment contacts are checked as well as positive-area overlap: each pair intersects in exactly its prescribed common simplex.

All points are distinct; every triangle is positively oriented and properly three-colored; edge multiplicities are one or two; both orientations on every two-face edge are opposite. Every vertex link is one path or one cycle as appropriate. The face dual is connected, the oriented boundary is one cycle, and V-E+F=1. Thus the data define an embedded conforming disk with

    V=15, E=35, F=21, interior edges=28,
    boundary=(2,3,4,5,12,13,14).

The actual interior vertices are 0,1,6,7,8,9,10,11, with respective degrees 4,8,6,4,6,4,6,4. Vertices 12 and 14 each have degree three and are the only reflex corners. Their turns are exactly

    turn_12=-94625/3198133656,
    turn_14=-1324825/44909003592.

These are boundary vertices in the retained disk. They cannot remain boundary vertices of a convex geometric superset containing their retained stars, whose local interior angles exceed pi.

## 2. Old-weight uniqueness from the actual 28-by-15 system

Write V_i=(P_i.x,P_i.y,1) and U_i=x_i V_i. The balanced-edge condition is

    det(U_v+U_w,U_u,U_z)=0,

where u,z are the actual opposite vertices across the edge vw. For all 28 old interior edges, the independent verifier obtains u,z from the incident faces, computes

    A_e=det(V_v,V_u,V_z), B_e=det(V_w,V_u,V_z),

and verifies A_e!=0, B_e!=0, A_e x_v+B_e x_w=0, and the uncancelled determinant identity separately. Every displayed weight is nonzero. The [finite certificate](ADDITIVE_OBSTRUCTION_CERTIFICATE.json) gives every coefficient pair and edge, which specify every entry of the actual 28-by-15 matrix M: the two displayed coefficients occupy its endpoint columns and all other entries are zero.

For any completion retaining the old triangles, both old triangles across each old interior edge remain present. Hence the same edge remains interior with the same opposites. If y denotes any proposed new assignment of weights to the old vertices, cancellation of the nonzero opposite-vertex factors gives

    A_e y_v+B_e y_w=0.

This cancellation uses no equation at an old boundary edge and never divides by x_v+x_w. No positivity or preassigned sign pattern is imposed on y.

Independent row reduction gives rank(M)=14 and ker(M)=span(x). A short exact certificate avoids reliance on that rank routine. In the displayed row order, take the tree

    (0,1),(0,5),(0,6),(0,7),(1,2),(1,8),(1,12),
    (1,13),(1,14),(2,9),(3,9),(3,10),(4,10),(4,11).

Every edge is an actual old interior edge. The graph is connected on all fifteen vertices, including the original boundary vertices. Multiply column i by x_i and divide row e=(v,w), v<w, by its nonzero A_e x_v. Every resulting tree row is exactly +1 at v and -1 at w. Deleting column 0 gives determinant **-1**. The independent certificate records that normalized minor, its row factors, the original nonzero minor, and their exact scaling identity.

Thus rank(M)>=14. Since Mx=0 with x nonzero, rank(M)<=14. Equivalently, each tree equation directly forces y_v/x_v=y_w/x_w, so

    y=cx

for one common scalar c. The proposed nonzero weights force c!=0. In particular, allowing arbitrary reassignment of the old weights does not free vertices 12 or 14: old interior edges (1,12) and (1,14) already tie them into the connected system.

Multiplying all old U_i by c multiplies a forced-line cross product by c^2, so every forced line below is unchanged. This argument includes negative c and does not tacitly freeze the original weights.

## 3. Independently expanded forced lines and whole-cone certificates

For a retained boundary edge vw whose old opposite is vertex 1, any newly attached opposite q must satisfy

    det(U_v+U_w,U_1,V_q)=0.

The nonzero weight at q has been canceled; the old nonzero weight at 1 could also be canceled without changing the line. Expanding directly in coordinates (X,Y,1), rather than importing the source cross products, gives a genuine affine line in each case. Its coefficient vector is nonzero, so the two spanning vectors are independent.

### Vertex 12

The exact local star consists of the faces (1,5,12) and (1,12,13). The boundary neighbors are 5 and 13. Both seams (5,12) and (12,13) independently force the same primitive line

    L_12(X,Y)=108784934009 X+113286002040 Y+4351745500=0.

The recomputed evaluations are

    L_12(P_12)=-6623750,
    L_12(P_5)=-87716502000/497,
    L_12(P_1)=0,
    L_12(P_13)=-87716502.

Every point of the closed missing angular cone has the form

    P_12+alpha(P_5-P_12)+beta(P_13-P_12), alpha,beta>=0.

The line functional there equals exactly

    -6623750-(84424498250/497)alpha-81092752 beta < 0.

All three coefficients are strictly negative. This proves separation from the whole unbounded cone, including both bounding rays, without a finite sampling argument or any bound on alpha+beta.

For an additional exact geometric check, P_1 has cone coordinates

    alpha=-958429/47308715,
    beta=-2599200/66232201.

It is an algebraic point on L_12 but is outside the permitted sector. Using P_1 as a prospective cap point would overlap the old star.

### Vertex 14

The exact local star consists of (1,13,14) and (1,14,2). The boundary neighbors are 13 and 2. Both seams (13,14) and (14,2) force the same primitive line

    L_14(X,Y)=108784934009 X+112948171020 Y+4351745500=0.

The recomputed evaluations are

    L_14(P_14)=6624125,
    L_14(P_13)=350906505/4,
    L_14(P_1)=0,
    L_14(P_2)=175453252500/997.

On the entire missing cone, the exact expression is

    L_14(P_14+alpha(P_13-P_14)+beta(P_2-P_14))
      =6624125+(324410005/4)alpha+(168848999875/997)beta > 0

for alpha,beta>=0. The three coefficients are strictly positive. Here P_1 has cone coordinates

    alpha=-25995000/662359507,
    beta=-13458503/662359507,

again excluding this algebraically valid line point from the legal sector.

Either vertex alone proves the obstruction. The independent reconstruction verifies both.

## 4. Why this excludes every simultaneous conforming additive completion

The local lemma is valid for a geometric completion as a whole; it does not assume a stepwise cap-construction process.

Let v be either retained reflex vertex. Choose a sufficiently small disk centered at v that meets no old face not incident to v and no opposite edge of an old incident face. The retained faces occupy precisely the old angular star in that disk. Its complement is the closed convex cone generated by the two boundary-neighbor rays, with angle strictly less than pi.

If a nondegenerate new triangle is incident to v and its opposite-vertex ray lies outside this missing cone, its angular sector intersects the interior of the old angular star in positive angle. Then its intersection with the retained faces has positive area arbitrarily near v. This violates conformity. This also addresses a prospective ray lying on an old interior spoke: that ray is in the interior of the old angular star, so a nondegenerate triangle on it necessarily overlaps old faces. Therefore every permissible new opposite vertex must lie in the closed missing cone.

Now suppose K' is convex and retains all old faces with their geometric vertices. Its underlying region contains the retained reflex star. A boundary point of a convex polygonal region has a local angle at most pi, so v must instead be an interior vertex of K'. Each old boundary edge incident to v is still a simplex of K'. Since v is interior, that edge must have a second incident triangle. A boundary edge of a triangulated disk cannot have an interior endpoint.

The weight-uniqueness argument forces the corresponding new opposite vertex onto the fixed line L_v=0. The cone separation proves that no permissible position on that line exists. This is a contradiction.

Nothing in this reasoning depends on the number of new faces, the ordering of their introduction, whether the new opposite is newly created or already an old nonincident vertex, or the valences of the new vertices. Subdividing an old edge while leaving its incident old triangle unchanged would violate the simplicial intersection condition; subdividing that triangle changes the retained-face hypothesis. No such operation is silently admitted and then ruled out by this theorem.

Consequently the report's all-additions conclusion is justified, not an extrapolation from a failed ear or collar search. It obstructs the larger nonzero-weight balanced class before any additional parity/activity conditions for a closed quartic support are imposed.

## 5. Independently recovered actual quartic reduced rank

The magnitude matrix M is not the actual quartic compatibility matrix. Boundary balance weights do not create compatibility rows at boundary vertices. The audit keeps these systems separate.

The independent verifier orders rays by an exact polar-angle comparator, rather than the source's directed-link traversal. At each of the eight actual interior vertices it solves the barycentric relation

    d_(i+1)=beta_i d_i+gamma_i d_(i-1),

assembles the cyclic corner matrix with row t_i-gamma_i t_(i-1), computes its left nullspace, and eliminates the corner variables. Every corner matrix has the expected rank n-1. The eliminated edge row agrees, up to an explicitly nonzero exact factor, with

    r_i=(-1)^i det(d_(i-1),d_(i+1)) /
                (det(d_(i-1),d_i) det(d_i,d_(i+1))).

All second-moment identities are independently checked. The actual R is 8 by 35, with rows 0,1,6,7,8,9,10,11. Under the independent polar-angle convention, select the edge columns

    (0,5),(1,2),(0,6),(0,7),(2,8),(2,9),(3,10),(4,11).

The respective raw diagonal coefficients are

    615861858493/66264900000,
    -14202877137501601237/428735535000000,
    -503670845202777/958568000000,
    136828790330869/105180150000,
    24328858333419/20525538500000,
    358736854091/101252520000,
    -16614965979/7118750000,
    -2653940217/1143032000.

All are nonzero. Dividing each selected-minor row by its diagonal coefficient gives an upper-triangular matrix with all diagonal entries one. Its only nonzero off-diagonal entries are in row 0, at the selected columns (0,6) and (0,7):

    -3478800947769/79201369040,
    -824964430784/3534754241.

The normalized determinant is exactly **1**, proving rank(R)=8 without an opaque rank assertion. Direct row reduction agrees. Comparing with the source R gives exact row factors (1,1,-1,1,-1,-1,1,1); these harmless signs arise from different starting rays.

The nonpencil determinant is also independently reproduced:

    det(V_2,V_5,V_13)=-217587275/3719962464204 != 0.

These three vertices have one color. A proper three-coloring of the face-connected triangulation is unique up to permutation, so recoloring cannot restore a global three-color-line pencil. This nonpencil status and full actual reduced rank are consistent with the new obstruction. The fixed disk remains interpolable in the accepted original-mesh quartic reduction, but its internal balances do not guarantee a balanced convex completion.

## 6. Exact verification and remaining gap

The independent reconstruction passes 604 exact checks with eight active controls: one changed old weight, a repeated tree row falsely offered as a full-rank minor, a legal-cone cap barycenter at each reflex vertex, the algebraically balanced but sector-illegal point P_1 at each reflex vertex, false convexity and a false actual reduced-rank defect. The author's separate reconstruction passes its 503 checks. These finite checks corroborate the geometric proof and exact determinant certificates.

The [finite certificate](ADDITIVE_OBSTRUCTION_CERTIFICATE.json) supplies the old-edge coefficient pairs, spanning tree and row factors, original and normalized tree minors, local corner-elimination records, normalized actual rank-eight minor and both cone certificates. The complete candidate and its original actual reduced matrix are preserved in the [fourth-pass certificate](fourth_edition/FOURTH_PASS_CERTIFICATES.json). The [reproduction guide](REPRODUCTION.md) explains how to reconstruct the matrices and compares the distinct row normalizations.

The proof rests on exact nonzero minors, retained-edge equations, local reflex geometry and affine strict-sign identities on the complete missing cones. The accepted stopping point is precise: this particular rational nonpencil disk cannot be completed by adding triangles while preserving its old faces and coordinates. A different construction, changed geometry or changes to the old triangulation remain outside the theorem. No broader impossibility or solution to the general quartic interpolation problem is claimed.
