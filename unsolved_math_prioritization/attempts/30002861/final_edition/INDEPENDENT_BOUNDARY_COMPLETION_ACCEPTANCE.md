# Independent acceptance of canonical exterior completion

## Decision and exact scope

**Accepted without mandatory mathematical correction.** The global exterior-collar theorem, finite necessary-and-sufficient completion criterion, nonzero balanced-edge weight-sum, actual exterior-polynomial formulas, boundary-chord matching theorem, and interior-opposite-vertex conclusion are valid under their exact stated hypotheses.

This audit belongs to the same fifth and final shared substantive pass for row 1761 / problem 30002861 / OWR-13678-002, dated 13 October 2026 UTC. It adds no pass; the lifetime total is unknown. The bundled row remains unsolved.

The reviewed [boundary-completion report](FIFTH_PASS_BOUNDARY_COMPLETION.md) needs no mathematical correction. Its public edition explicitly defines a boundary triangle as one incident with a boundary edge, which is the exact scope verified below. The [final guide](README.md) and [dependencies](DEPENDENCIES.md) identify the preceding accepted proofs.

The fixed model remains a finite conforming straight-line triangulation of a polygonal disk, with distinct vertices and nondegenerate triangles. Values and both first derivatives are independently prescribed at every original vertex. Interpolants are globally C1 and quartic on the original triangles. The collar constructs a legal original mesh for an existence implication; it does not refine an already specified interpolation problem and silently change its model.

The mathematical dependencies are the accepted closed-support and zero-ray classification, face-normalized row formula, compact quadratic construction, corrected incident-edge-segment normal form, and degree restrictions. Their exact statements are linked in the [dependency guide](DEPENDENCIES.md). The new universal arguments are audited below, and a separate exact reconstruction verifies the algebra and geometry without using a prior computational result as a premise.

This acceptance proves neither existence nor impossibility of an admissible balanced convex support. It proves no new global color-pencil containment, no quartic counterexample, no universal interpolation theorem, and no historical or present-day literature-openness claim.

## 1. The full-turn polygon lemma is global and length-independent

Fix one directed edge of the closed chain and take its direction to be zero. In the specified cyclic order, the later edge directions lie strictly increasingly between zero and 2 pi. Because both neighboring gaps are less than pi, the first later direction lies in (0,pi) and the last lies in (pi,2 pi). The signed increments of distance to the fixed supporting line consequently consist of a nonempty positive block, at most one zero increment at pi, and a nonempty negative block.

Closure makes the sum zero. During the positive block every nonincident partial sum is positive. During the negative block, any partial sum before the final endpoint equals the negative of the remaining strictly negative sum and is positive. Thus every nonincident vertex is strictly to the left of every listed directed edge. There is no assumption about edge lengths. Each edge is an exposed edge of the convex hull, the vertices are distinct, and the listed order is the embedded strictly convex hull boundary. This rules out a locally turning but globally self-intersecting chain.

For the polygon in the manuscript, positivity of

    D_i = det(e_(i-1), e_(i+1))

is equivalent to delta_i + delta_(i+1) < pi, because this sum lies in (0,2 pi). The displayed t_i and s_i are positive, and their determinant identities give the two identical affine descriptions of Q_i.

Deleting the old edge i replaces the adjacent two edge vectors by the positive multiples (1+t_i)e_(i-1) and (1+s_i)e_(i+1). The intervening new turn is the sum of the deleted two turns and remains below pi. Every other turn is unchanged, and the total turn remains 2 pi. The preceding lemma therefore applies to this closed reduced polygon. Its exposed side inequalities prove, for every old side j,

    H_i(Q_i) < 0,
    H_(i-1)(Q_i) = H_(i+1)(Q_i) = 0,
    H_j(Q_i) > 0 otherwise.

These are global side inequalities, including sides far from i. No metric comparability, lower bound on lengths, symmetry, or near-parallel exclusion beyond D_i > 0 is used. Summing all turn inequalities gives k >= 5. For different indices i and j, Q_i violates H_i >= 0 whereas Q_j satisfies it; hence all exterior points are distinct. They are also distinct from and outside every old vertex and from K itself.

## 2. Complete face-intersection table and genuine embedded collar

Let S_i be the old whole strict side A_i A_(i+1), T_i its exterior side triangle, and C_i the exterior corner triangle at A_i. All are closed sets below. The half-plane signatures give the following complete table for distinct indices, interpreted cyclically:

- T_i intersect K = S_i.
- C_i intersect K = {A_i}.
- T_i intersect T_(i-1) = {A_i}, and T_i intersect T_(i+1) = {A_(i+1)}; other distinct T intersections are empty.
- T_i intersect C_i = [A_i,Q_i], and T_i intersect C_(i+1) = [A_(i+1),Q_i]; all other T_i/C_j intersections are empty.
- C_i intersect C_(i-1) = {Q_(i-1)}, and C_i intersect C_(i+1) = {Q_i}; all other distinct C intersections are empty.

Here is a direct verification covering lower-dimensional contacts, not just disjoint interiors. Throughout T_i, H_i <= 0 and every other H_j >= 0, while T_i intersect {H_i=0} is exactly S_i. Throughout C_i, H_(i-1),H_i <= 0 and the other H_j >= 0. Imposing both nonnegative inequalities on C_i leaves only A_i, which proves its intersection with K. These observations settle all T/T intersections and all nonincident T/C intersections by restricting their intersection to old sides in K.

For T_i/C_i, C_i must satisfy H_(i-1)=0 at an intersection, and this zero set in C_i is exactly [A_i,Q_i], already a side of T_i. The analogous argument handles C_(i+1). If C_i and C_j are nonadjacent, their two negative-side index sets are disjoint because k >= 5. On their intersection both negative forms of C_i must be zero, leaving A_i; this does not lie in C_j. For adjacent C_i and C_(i+1), their intersection is confined to [A_i,Q_i] and [A_(i+1),Q_i], respectively. These lie on the two distinct adjacent supporting lines that meet at Q_i. The intersection is exactly that point. Thus there is no unlisted edge contact, vertex contact, overlap, crossing, or exterior-point coincidence.

The side triangles and corner triangles attach combinatorially as an annulus with inner boundary the old polygon and outer boundary Q_0,...,Q_(k-1). The exact intersection table embeds this annulus. An exterior boundary edge cannot cross another or touch a nonincident vertex without contradicting that table. The outer boundary is therefore simple, regardless of whether it is convex or has a straight vertex.

Joining Q_i to arbitrary strictly ordered straight subdivision vertices partitions T_i into nondegenerate triangles. Each new doubled area is the positive subedge-length ratio times the original doubled area; there is no lower bound on that ratio. Their intersections are exactly the prescribed subedges and vertices. Any old triangulation of K meets these triangles only through the prescribed subdivided old boundary. Every old vertex becomes interior in the completed disk, and all Q_i lie on its boundary. This proves the required geometric original mesh, not merely a formal abstract annulus.

## 3. Completion criterion, activity, and actual normalized dependencies

At a strict old corner the collar adds exactly two neighbors, and at a straight boundary vertex it adds exactly one. The stipulated induced degree parities make every old vertex even-valence in the full original mesh. The old interior vertices retain their complete even fans. Each Q_i is a boundary vertex of the full mesh and supplies no retained row.

For the spoke A_i Q_i, the two neighboring rays at A_i point along opposite directions of side i: one reaches the next old side vertex and the other reaches Q_(i-1). For the spoke A_i Q_(i-1), the two neighboring rays point along opposite directions of side i-1. At a straight old vertex, the two neighbors of its one exterior spoke are its opposite boundary rays. Thus the row formula vanishes on all old-to-Q spokes, including arbitrary side subdivisions. The determinant tests (7) make the coefficient nonzero at both ends of every old edge. Consequently every old vertex has a nonzero retained row, the active graph is precisely the connected edge graph of K, and no one-entry column leaves it. It is an actual closed component.

The precise normalization can be checked without relying on terminology. Orient an old edge v to w, and take its actual opposite vertices u on the left and z on the right. Put

    A = det(w-v,u-v) > 0,
    B = -det(w-v,z-v) > 0,
    a = det(u-v,z-v),
    b = det(u-w,z-w).

If s is the sign of the left triangle, the accepted face-sign-normalized fan formula gives

    rho_vw = -s a/(AB),
    rho_wv = -s b/(AB).

The common multiplier is finite and nonzero. Hence the actual retained-row dependency condition at this column is exactly a x_v + b x_w = 0. The exterior columns are already zero. Reversing the chosen opposite-vertex order changes both a and b by the same sign and does not change the equation. These x_v are coordinates for the specific normalized rows; arbitrary independent rescalings are not being mixed into the boundary equations.

A consistent face coloring exists because the supported disk has even interior degrees, as in the accepted normalization theorem. The even completed fans extend these signs around boundary vertices. Equivalently, in the constructed full disk all interior vertices are even, so its whole triangle dual is bipartite. Thus all displayed edge equations refer to one compatible system of normalized rows.

Necessity follows from the accepted zero-ray/exterior-attachment theorem: any larger original mesh realizing the same closed support has the same forced opposite Q_i at each boundary subedge. It cannot change a failed forced-Q equation. Sufficiency follows from the embedded collar, the preceding parity/activity argument, and the exact normalized dependency identity. The accepted second-pass theorem then turns a balanced closed component into failure for an appropriate pure-gradient datum. This last implication is expressly conditional on successfully passing every determinant and balance check; no successful balanced input is provided here.

The connectivity and uniqueness statement is also valid. A triangle having two boundary edges would join the two endpoints of their common vertex's link path by one link edge, exhausting the path and forcing boundary degree two. The stipulated degrees exclude this. Every triangle therefore has at least two interior edges connecting its three vertices, and the connected face dual joins these subgraphs. The graph of all vertices and interior edges is connected. With nonzero endpoint coefficients, any one nonzero root weight determines every other weight. Thus internally consistent weights are unique up to a common factor, and one cannot repair a failed boundary equation by changing only their normalization. More generally, on the connected full edge graph any nonzero kernel vector is automatically full-support and the kernel has dimension at most one.

## 4. Nonzero weight sum and exact scope of boundary transfer

Choose coordinates v=(0,0), w=(L,0), u=(P,H), z=(R,-J), where L,H,J > 0. Direct determinant calculation gives

    a = -(PJ+HR),
    b = L(H+J) - (PJ+HR),
    b-a = L(H+J) > 0.

The activity conditions are a,b != 0. For a nonzero solution of a x_v + b x_w = 0,

    x_v+x_w = x_v (b-a)/b != 0.

Thus the affine weighted point is always defined, and its edge coordinate is

    L x_w/(x_v+x_w) = (PJ+HR)/(H+J),

the exact finite intersection of the opposite-vertex line with the edge's supporting line. This proves the statement for all balanced active edges, including transfers of negative sign. It is not restricted to a generic intersection.

For a boundary subedge, Section 7 of the manuscript supplies a strictly interior opposite vertex u. Since u has every strict-side inequality positive and Q_i has all inequalities except i nonnegative, the intersection of their segment with H_i=0 has all other inequalities strictly positive. Hence it lies strictly inside the whole strict side. It need not lie inside the selected subedge.

An explicit legal local geometry confirms the distinction: the whole side runs from (0,0) to (4,0), Q=(2,-6), u=(2,1), while the subedge runs from v=(0,0) to w=(1,0). Then a=-14, b=-7, tau=-2, and weights (1,-2) give the finite crossing (2,0). This is a local transfer control, not an asserted balanced support. Positivity follows for an unsubdivided strict side because the crossing lies strictly between its endpoints; it does not extend to every subdivided subedge.

The product of boundary transfers must be one. It is only a necessary check when internal weights are already fixed: a cyclic collection of ratios may close while differing from those weights on individual edges. The manuscript correctly requires all individual boundary equations.

## 5. Exterior normal forms use genuine original triangles

In an arbitrary closed support, the accepted zero-ray classification gives exactly two adjacent omitted rays at each strict corner. Their intervening original triangle is precisely (A_i,Q_(i-1),Q_i). In the canonical collar it is the explicitly constructed C_i. There is no invented angular sector. Since the compact quadratic equals zero on this actual exterior triangle, the local normal form yields the displayed polynomial identity (11).

The two exterior directions are independent; x_v and the face sign are nonzero. Thus p_v is a genuinely nonzero product of the two adjacent supporting-line equations, with nonzero denominator. The conclusion does not infer nonzero p_v merely from zeros along two lines. On the model exterior rays (-l,0),(0,-h), its form is a nonzero signed multiple of X Y. The exact generic Hessian determinant is -x_v^2, although no signed-Hessian argument for the entire spline is inferred from that fact.

At a straight vertex, the unique omitted ray goes to Q_i. Either adjacent original exterior triangle has its other ray on the strict side. Formula (12) follows with nonzero coefficient and distinct factors. The independent symbolic calculation uses both genuine exterior triangles, with opposite face signs, and obtains the same p_v from each. With side neighbors (-l,0),(r,0) and exterior Q=(k,-h), the common polynomial is, up to the chosen face sign,

    x_v Y(h X+k Y)/h.

Its zero lines are exactly the strict side and vQ_i. The actual exterior coefficients vanish because the two boundary-neighbor rays are opposite. For a strict corner, the independently checked three genuine exterior triangles likewise all give the same local polynomial with their alternating signs.

On the reconstructed integer control, all three actual exterior triangles at each of its six strict corners produce the identical nonzero local p_v for x_v=1. Their factorizations are retained in the exact certificate. This verifies the exterior algebra locally; it does not manufacture a global compact spline on that magnitude-unbalanced control.

The sole use of the corrected incident-segment assertion is q(w)=p_v(w) for an actual edge vw. No identity for the entire piecewise function on an extended supporting line is invoked. Zero sets of the polynomial p_v itself may of course be discussed globally.

## 6. Boundary chords and every edge-boundary triangle

Let vw be a non-boundary edge whose endpoints lie on the boundary. Since q(w)=0, the incident-segment formula gives p_v(w)=0. If v is strict, the nonzero exterior polynomial forces w onto one of its two supporting side lines. Convexity confines K on that line to the corresponding old strict side. A conforming edge on that segment cannot skip a subdivision vertex and is a boundary edge. This contradicts the chord assumption.

If v is straight, the only additional zero line is vQ_i. Because Q_i is strictly outside side i and v is in that side's relative interior, exactly one ray along this line enters K: the ray away from Q_i. Its intersection with K is a segment ending at a unique other boundary point. Distinct mesh vertices give at most one chord incident at v. Applying the same argument at w shows that it too is straight, lies on a different strict side, and has its own Q_j beyond w away from v. Thus the order is exactly Q_i,v,w,Q_j, or its reversal. Conformity supplies noncrossing, while the degree-at-most-one statement supplies matching. The theorem does not assert that such a matching is realizable by a balanced support or that all straight-vertex chords are impossible.

Finally fix an actual boundary edge vw and its triangle uvw in K. If u were on the boundary, neither uv nor uw could be a boundary edge, because that would give a triangle with two boundary edges and a degree-two boundary vertex. Both would be chords, contradicting the matching property at u. Therefore u is strictly interior to K. The precise scope is triangles incident with a boundary edge and the vertex opposite that edge, not all triangles that merely touch a boundary vertex.

## 7. Independent exact certificates and remaining question

The independent reconstruction has 3,272 successful exact checks and 11 active negative controls. Its triangle-intersection algorithm differs from the author's: it enumerates intersections of pairs of independent supporting lines from the six closed half-planes of each triangle pair and retains the feasible points. Every extreme point of the bounded intersection is obtained this way. Equality with the prescribed common-simplex vertex set checks empty, point, segment and area intersections exactly. The [independent finite certificate](INDEPENDENT_COLLAR_CERTIFICATE.json) and [reproduction guide](REPRODUCTION.md) give the mathematical inputs and conventions.

The exact polygon samples include a rational circle pentagon, a rational octagon, extreme affine shear and anisotropy, and side subdivisions as small as 10^-15 of a strict side. The mesh sizes (V,E,T) are (11,25,15), (15,37,23), (15,37,23), and (21,52,32). Together these check 1,107 triangle pairs. The reconstructed integer control adds all 378 triangle pairs of its (18,45,28) full mesh. Every link, boundary, positive orientation, total area, and relevant half-plane signature is checked exactly. These samples corroborate the proofs; they are not offered as all-polygon evidence.

For the integer control, the independently polar-sorted full fans are even, all twelve exterior-spoke endpoint coefficients vanish, all 54 old-edge endpoint coefficients are nonzero, and the explicit actual row/determinant common factor is checked on every one of its 27 old edges. The actual retained matrix R and the formal normalized balance matrix M both have rank 12. A 12-by-12 minor of M, in the certificate's vertex order, is

    -6624693947958945585230391966837094249267200 / 402018373,

using row edges

    (0,1), (0,5), (1,2), (2,3), (3,4), (1,7),
    (0,6), (0,7), (2,8), (2,9), (3,10), (4,11).

Its cyclic boundary-transfer product is exactly

    585991946946275 / 301150964543077,

which is not one. This reinforces the necessary distinction between a perfectly legal closed active geometry and a balanced component. The certificate includes the entire 27-by-12 M matrix, all full normalized fan rows, common column factors, Q coordinates, and boundary transfers, so the rank and activity statements are reproducible rather than opaque rank numbers.

Negative controls include a collapsed Q detected by the full mesh validator, an altered endpoint determinant detected by the actual normalized row, a zero merged-turn determinant, false positivity on a subedge, omission of a nonzero boundary weight, and conflating legal closed geometry with a nontrivial dependency. The author's separate reconstruction passes its stated 1,872 checks and eight controls. Its agreement is secondary to the independent reconstruction and universal proofs.

The [finite certificate](INDEPENDENT_COLLAR_CERTIFICATE.json) records authored rational geometry, exact matrices and factors. The preserved [integer control](fourth_edition/third_edition/second_edition/SECOND_PASS_CERTIFICATE.json) supplies its coordinates without a parallel baseline copy. Mathematical validity rests on the arguments and exact identities above, not on file identities.

The final remaining question is exactly the manuscript's: produce a finite conforming convex triangulated disk with the required parity and nonzero activity, outside the already excluded global color-pencil class, whose internally propagated nonzero weights satisfy every forced-Q boundary equation; or rule out all such disks. The exterior collar is no longer an additional geometric unknown once the strict-turn conditions hold. Neither this accepted completion interface nor the boundary-chord restrictions settle that global balance problem.
