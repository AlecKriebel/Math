# Exact obstruction to additive completion of the nonpencil quartic candidate

## Result and scope

This is a construction branch of the **fifth and final shared substantive pass** for row 1761 / problem 30002861 / OWR-13678-002, dated 13 October 2026 UTC. It adds no separate pass; the lifetime total is unknown. The bundled row remains unsolved. See the [final guide](README.md), [exact dependencies](DEPENDENCIES.md), [independent acceptance](INDEPENDENT_ADDITIVE_OBSTRUCTION_ACCEPTANCE.md) and [certificate](ADDITIVE_OBSTRUCTION_CERTIFICATE.json).

**The exact fifteen-vertex, twenty-one-face candidate from the accepted fourth pass has no convex balanced completion that retains its original triangles as faces.** This holds even when all its original weights may be reassigned: its interior balance equations determine them up to one common nonzero factor.

The obstruction is geometric and local. At each of the two reflex boundary vertices, both incident boundary edges force every prospective exterior opposite vertex onto a particular line. That line misses the entire available angular sector, including its boundary. Thus no conforming balanced triangle can be attached across either incident boundary edge. Arbitrarily many new vertices, arbitrary fan lengths, and arbitrary additions elsewhere cannot remove this obstruction.

This is a precise obstruction for the specified candidate, not a counterexample to quartic interpolation and not a universal interpolation theorem. It does not exclude replacing or subdividing old faces, changing old coordinates, or constructing a different nonpencil disk. The general quartic question remains unresolved.

## 1 The retained candidate and the balance model

The accepted model is a finite conforming straight-line triangulation of a polygonal disk with distinct vertices and nondegenerate triangles. For a balanced support, every vertex has a nonzero real normalized weight x_v. With

    V_v = (P_v.x, P_v.y, 1)^T,
    U_v = x_v V_v,

each interior support edge vw, with opposite vertices u,z, satisfies

    det(U_v + U_w, U_u, U_z) = 0.                 (1)

A closed active component must have convex support. No exterior triangle is introduced merely by writing (1); its location must be compatible with the retained mesh.

The exact candidate is reconstructed here without importing any earlier verifier or result file. For vertices 0,...,11, the colors are

    B,A,C,B,A,C,A,C,B,A,C,B,

and the direction vectors are

    d_A=(1,0), d_B=(0,-1), d_C=(-1,1).

Set

    q=(9,-25,-1,-1,-1,-1,-7,15,-7,3,3,3),
    x_i=q_i+(i+1)/1000,
    P_i=d_color(i)/x_i.

The three remaining vertices and weights are

    P_12=(0,-96275/2502452),          x_12=87716502/3311875,
    P_13=(1/2,-233924171/450441360), x_13=-2,
    P_14=(0,-866425/22522068),        x_14=70181301/2649650.

Their colors are B,C,B. The first twelve triangles, for i=0,...,5 and subscripts modulo six, are

    (i,i+1,6+(i+1)), (i,6+(i+1),6+i).

The remaining nine are

    (6,7,8), (8,9,10), (10,11,6), (6,8,10), (5,1,0),
    (1,5,12), (1,12,13), (1,13,14), (1,14,2).

The [independent fourth-pass audit](fourth_edition/INDEPENDENT_NONPENCIL_EXTENSION_ACCEPTANCE.md) accepted this geometry and its twenty-eight interior balance equations. The final [independent acceptance](INDEPENDENT_ADDITIVE_OBSTRUCTION_ACCEPTANCE.md) reconstructs all of them with exact rational arithmetic, together with all 210 triangle intersections, every vertex link, face-dual connectivity, edge multiplicities and Euler characteristic. The candidate is a conforming embedded disk with

    V=15, E=35, F=21,
    boundary=(2,3,4,5,12,13,14).

Only vertices 12 and 14 are reflex. The actual quartic reduced matrix, whose rows are retained only at the eight original even interior vertices, still has rank eight. The construction is therefore not a quartic counterexample.

## 2 The old weights cannot be adjusted independently

Cancel the nonzero factors x_u x_z in (1). For a fixed old edge vw and its fixed old opposite vertices u,z, the equation is

    A_e x_v + B_e x_w = 0,
    A_e=det(V_v,V_u,V_z), B_e=det(V_w,V_u,V_z).     (2)

Both coefficients are nonzero on every one of the twenty-eight original interior edges. The graph consisting of all fifteen vertices and these edges is connected. An explicit spanning tree is

    (0,1), (0,5), (0,6), (0,7), (1,2), (1,8), (1,12),
    (1,13), (1,14), (2,9), (3,9), (3,10), (4,10), (4,11).

Let x be the displayed solution and y any other solution. By (2),

    A_e x_v (y_v/x_v - y_w/x_w)=0.

Hence y_v/x_v equals y_w/x_w along every tree edge, and therefore at every old vertex. Thus y=cx for one scalar c. For nonzero normalized weights, c is nonzero.

For an explicit rank certificate, let M be the 28-by-15 matrix of (2). Multiply its v-th column by x_v and divide a tree row e=(v,w), v<w, by A_e x_v. The resulting fourteen tree rows are exactly the oriented incidence matrix with entries +1 at v and -1 at w. Deleting column 0 gives determinant -1 in the displayed row order. The original system therefore has rank at least fourteen; its known nonzero kernel vector x gives rank at most fourteen. Consequently

    rank M=14, ker M=span(x).                     (3)

This argument uses neither an optimization tolerance nor an assumption about future new vertices. The old interior edges and both their incident triangles remain unchanged in any completion retaining the old faces, so all their equations persist. A common rescaling of the U_v does not change any line used below.

## 3 A local obstruction using the entire available sector

**Lemma.** Let v be a strict reflex boundary vertex of a conforming straight-line triangulated disk, with previous and next boundary vertices a,c. Let

    C_v={P_v+alpha(P_a-P_v)+beta(P_c-P_v): alpha,beta>=0}.

Because v is reflex, C_v is the closed convex cone of the missing angular sector, whose opening is strictly less than pi. Suppose the balance equation across the boundary edge va, if that edge were made interior, would force its new opposite vertex q onto an affine line L=0. If L is strictly of one sign on C_v, then no nondegenerate conforming balanced triangle can be attached across va while retaining the old triangles.

**Proof.** Choose a sufficiently small disk around v meeting no triangle not incident to v and meeting no edge opposite v in an incident triangle. In that disk, the retained star occupies exactly the old interior angular sector. Its complement is the missing sector C_v. A newly attached nondegenerate triangle incident to v cannot have any positive angular sector inside the old star: such a sector would cause an intersection with positive area near v, violating conformity. In particular its opposite-vertex ray from v must lie in C_v, so q belongs to C_v. The balance equation also requires L(q)=0. Strict separation gives a contradiction. This uses all possible positions for q, not just points inside a chosen finite ear. ∎

An especially simple exact certificate for the strict-separation premise is

    L(P_v), L(P_a)-L(P_v), L(P_c)-L(P_v)

all strictly positive, or all strictly negative. Indeed, these are exactly the three coefficients of the affine expression for L on C_v. The parameters alpha,beta have no upper bound.

**Corollary.** If the lemma applies at a reflex vertex to either incident boundary edge, no convex triangulated disk retaining all the old triangles can satisfy the required balances.

**Proof.** A convex superset retaining the old star cannot leave v on its boundary: its retained local angle is greater than pi. Thus v must be interior. In a conforming triangulation retaining the old faces, each old boundary edge incident to v must acquire a second triangle. The prohibited attachment would be necessary. ∎

The same argument applies if several new triangles are conceptually added at once, or if the new opposite vertex is an already existing nonincident vertex. It does not require an order of additions. Subdividing an old boundary edge while leaving an old incident triangle unsplit is not a conforming completion; splitting that triangle is a change to the retained-face hypothesis.

## 4 Exact separation at vertex 12

At v=12, the boundary neighbors are a=5 and c=13. The two old incident triangles have the common third neighbor b=1. If va receives an outside triangle with opposite q, (1) implies

    V_q in span(U_12+U_5,U_1).

The two spanning vectors are independent, so this is a genuine line constraint. For the other edge vc the corresponding line is span(U_12+U_13,U_1). Exact cross products show that these lines coincide and have primitive affine equation

    L_12(X,Y)=108784934009 X+113286002040 Y+4351745500=0.

The exact evaluations are

    L_12(P_12)=-6623750,
    L_12(P_5)=-87716502000/497,
    L_12(P_1)=0,
    L_12(P_13)=-87716502.

The turn at vertex 12 is

    det(P_12-P_5,P_13-P_12)=-94625/3198133656<0.

On its whole missing sector,

    L_12(P_12+alpha(P_5-P_12)+beta(P_13-P_12))
       =-6623750-(84424498250/497)alpha-81092752 beta<0

for all alpha,beta>=0. The forced line is therefore disjoint from every legal opposite-vertex ray at 12. Neither boundary edge (5,12) nor (12,13) can receive a conforming balanced outside triangle in a retained-face completion.

In particular, the existing point P_1 is an algebraic point on the forced line, but it lies outside the available sector. Algebraic solvability of the determinant equation alone would have admitted an invalid overlapping triangle.

## 5 A second independent geometric obstruction at vertex 14

At v=14, take a=13, c=2 and b=1. The forced lines from the two boundary edges again coincide, now with primitive equation

    L_14(X,Y)=108784934009 X+112948171020 Y+4351745500=0.

Here

    L_14(P_14)=6624125,
    L_14(P_13)=350906505/4,
    L_14(P_1)=0,
    L_14(P_2)=175453252500/997,

and the reflex turn is

    det(P_14-P_13,P_2-P_14)=-1324825/44909003592<0.

For all alpha,beta>=0,

    L_14(P_14+alpha(P_13-P_14)+beta(P_2-P_14))
       =6624125+(324410005/4)alpha+(168848999875/997)beta>0.

Thus (13,14) and (14,2) are also unavailable for any conforming balanced outside attachment.

Either vertex alone proves nonextendibility. The second certificate verifies that both degree-three reflex defects have the same kind of obstruction, even though the affine separating signs are opposite.

## 6 The precise stopping theorem

**Theorem.** Let K be the exact fifteen-vertex disk of Section 1. There is no finite conforming straight-line triangulated disk K' with convex underlying region such that:

1. Every original triangle of K is also a triangle of K', with the same geometric vertices.
2. Every vertex of K' has a nonzero normalized weight.
3. Equation (1) holds on every interior edge of K'.

**Proof.** The equations on the original twenty-eight interior edges force the old weights to be c times the displayed weights by Section 2, with c nonzero. Thus both forced lines at vertex 12 remain exactly L_12=0. Convexity and the retained reflex star force vertex 12 to be interior, so the old edge (5,12) must acquire a second triangle. The local-sector lemma and the strict identity in Section 4 make that triangle impossible. ∎

The theorem does not need assumptions about the new vertices' valences or boundary degrees; it already obstructs this larger class before imposing the additional closed-support parity and activity restrictions. It also does not need to test prospective exterior collars: the required convex support cannot be reached within this fixed-candidate additive class.

The old candidate remains genuinely outside the excluded global color-pencil class, since its same-color triple 2,5,13 has nonzero homogeneous determinant. Its actual reduced matrix has full row rank eight. Neither fact is contradicted by the stopping theorem: internal balance and nonpencil geometry do not guarantee a feasible continuation.

## 7 Exact verification and remaining gap

The [exact obstruction certificate](ADDITIVE_OBSTRUCTION_CERTIFICATE.json) specifies the old interior-edge determinant pairs, spanning tree, exact row factors, normalized determinant -1 and both strict whole-cone separation identities. It uses the preserved [fourth-pass candidate](fourth_edition/FOURTH_PASS_CERTIFICATES.json) without silently altering a coordinate, weight or face. The [reproduction guide](REPRODUCTION.md) gives explicit conventions for reconstructing its matrices and lines.

The [independent acceptance](INDEPENDENT_ADDITIVE_OBSTRUCTION_ACCEPTANCE.md) reconstructs the candidate, all 210 face intersections, weight rigidity, actual reduced rank eight and the simultaneous-addition argument. Its normalized rank-eight minor, corner-elimination records, original tree minor and cone coordinates are included as separate mathematical records in the certificate. These exact nonzero minors and affine strict-sign identities are proof evidence; file identities alone are not.

Changing an old weight breaks an interior balance; a repeated tree row destroys the claimed maximal minor; a cap point in a legal reflex cone fails its forced-line equation; the algebraically valid point P_1 lies outside each permitted cone. A false convexity claim or actual reduced-rank defect is also rejected. The finite geometry checks supplement the local argument for all possible additions; they do not replace that argument by a finite search.

The exact stopping point of this construction branch is: **the specified nonpencil candidate cannot be completed by retaining its old faces and adding triangles.** A different construction would need to alter those faces or coordinates, or begin with another nonpencil configuration. The theorem does not exclude those possibilities. The fifth pass is final for this sequence; no sixth substantive pass is started. The general quartic interpolation question remains unresolved.
