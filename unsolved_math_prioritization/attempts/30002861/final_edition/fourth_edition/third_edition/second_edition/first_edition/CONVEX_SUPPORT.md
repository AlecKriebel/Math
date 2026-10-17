# Convex-support restrictions for quartic vertex Hermite interpolation

## Scope and result

**Review status:** the structural theorem and interpolation corollary below are independently accepted; see [the mathematical audit](QUARTIC_AUDIT.md). The acceptance includes the precise simplex-labelled-chain proof in Lemma 4. These remain partial quartic results. No novelty or priority claim is made.

The exact setting is a finite conforming straight-line triangulation of a polygonal disk, with nondegenerate triangles. Splines are globally C1 and have total degree at most 4 on each triangle. Values and both gradient components at all vertices, including boundary vertices, are arbitrary. There are no imposed boundary conditions, subdivisions, or moved vertices.

The main result below is a necessary geometric restriction on every closed component of the reduced quartic interpolation matrix:

**Convex-support theorem.** A nonempty closed component induces a triangulation of a convex polygon. Its strict boundary corners have even induced degree at least 4; its straight boundary vertices have odd induced degree at least 5; its interior vertices have their original even mesh degrees, at least 4. In particular the component contains at least three nonsingular degree-4 interior mesh vertices.

Consequently, if the entire mesh has at most two nonsingular degree-4 interior vertices, the quartic vertex-jet map is surjective. This includes meshes with legal collinearities and requires no generic-position assumption.

This does not settle the existential quartic conjecture. Closed components with the required geometry do exist, as the [eighteen-vertex family](QUARTIC_REDUCTION.md#5-a-collinear-eighteen-vertex-family) demonstrates; cycle balance remains necessary. This argument supplies no cycle-balanced counterexample and no universal surjectivity theorem.

## 1. Independent local algebra

For a triangle with vertices v,w,u, degree-4 Bernstein coefficients at and immediately beside v are fixed by the prescribed jet:

c400=f_v,  c310=f_v+(g_v dot (w-v))/4,

with analogous formulas around all three corners. Of the 15 coefficients, nine are fixed. The six remaining coefficients consist of three edge coefficients c220 and three triangle-corner coefficients c211. Give each mesh edge a single shared coefficient m_vw=c220. This guarantees polynomial trace agreement across each shared edge.

For adjacent triangles (v,w,u) and (v,w,z), write z=alpha v+beta w+gamma u, alpha+beta+gamma=1. The two nonautomatic first-row Bernstein continuity equations, one at each endpoint of vw, are

t_(v,w,z),v - gamma t_(v,w,u),v - beta m_vw
    = alpha [f_v + g_v dot (w-v)/4],

and the corresponding equation at w with alpha and beta exchanged. The two endpoint equations are already satisfied by the prescribed common gradients. Therefore these equations are necessary and sufficient for C1 smoothness.

At an interior vertex v, write its distinct outgoing rays d_i=w_i-v in counterclockwise order, with indices modulo n. The gaps theta_i between successive rays lie strictly between 0 and pi: each is the angle of one nondegenerate incident triangle. Put

a_i=det(d_i,d_(i+1))>0,

beta_i=det(d_(i-1),d_(i+1))/a_(i-1),
gamma_i=-a_i/a_(i-1),
alpha_i=1-beta_i-gamma_i.

The cyclic corner-coefficient equations are

t_i-gamma_i t_(i-1)-beta_i m_vw_i
    =alpha_i [f_v+g_v dot d_i/4].

For odd n, their corner matrix is invertible because the product of all gamma_i is -1. For even n, its rank is n-1 and a left null vector is

lambda_i=(-1)^i a_0/a_i.

Thus its sole compatibility condition is

sum_i r_vi m_vw_i = H_v(f_v,g_v),

r_vi=lambda_i beta_i
     =a_0 (-1)^i det(d_(i-1),d_(i+1))/(a_(i-1) a_i),

H_v=-sum_i lambda_i alpha_i [f_v+g_v dot d_i/4].

Boundary stars are paths, so their corner equations have no compatibility condition. An identically zero row occurs exactly at a singular degree-4 interior star, whose rays form two opposite pairs; its H_v is also zero. Discard those zero rows and all vertices producing no row. Denote the remaining edge-coefficient matrix by R and the local jet matrix by H. The exact problem is Rm=Hj.

The criterion and this elimination agree with the separately assembled full BB matrix in the [quartic reduction](QUARTIC_REDUCTION.md). The structural arguments below are symbolic and do not depend on any finite collection of rank tests.

## 2. Useful moment identity

Let r_i=lambda_i beta_i. Since lambda_i gamma_i=lambda_(i-1),

sum_i lambda_i alpha_i = -sum_i r_i.

The barycentric relation d_(i+1)=beta_i d_i+gamma_i d_(i-1) also yields

sum_i r_i d_i = sum_i (lambda_(i-1)-lambda_i) d_i,

and consequently

sum_i lambda_i alpha_i d_i=-2 sum_i r_i d_i.

Therefore the compatibility equation can be written without the alpha coefficients:

sum_i r_i [m_vw_i-f_v-(g_v dot (w_i-v))/2]=0.

In particular,

H_v=(sum_i r_i)f_v + (sum_i r_i(w_i-v)) dot g_v/2.

The rows of H have disjoint jet supports. A nonzero left dependency z of R obstructs arbitrary jets exactly when at least one vertex in its support has a nonzero zeroth or first edge moment. There is no cancellation between jets assigned at distinct vertices. This argument retains the nonzero-moment qualification and does not import an external spline-dimension theorem.

For reference, the second homogeneous moments also vanish:

sum_i r_i d_i d_i^T=0.

One direct proof inserts a global quadratic with zero first jet at v: its edge c220 coefficient is d_i^T Q d_i/12 when its Hessian is Q. The exact compatibility relation holds for every symmetric Q. This identity is not used in the convex-support proof.

## 3. Closed row components

An edge column of R has at most two nonzero entries, one at each endpoint. Join two row vertices when their mesh edge has nonzero coefficients at both ends. A column with just one nonzero entry is a half-edge. A connected component is called closed if no half-edge is incident to it.

Along a two-entry edge vw, a left dependency satisfies

z_w=-(r_vw/r_wv) z_v.

Thus a dependency is nonzero on an entire connected component or vanishes on all of it. Any component containing a half-edge forces zero. A closed component admits a nonzero dependency precisely when these ratios have product 1 around every cycle. A closed component alone is not a counterexample.

In the remainder, S is the vertex set of any nonempty closed component. No cycle-balance assumption is needed for the geometric theorem.

### Lemma 1: no double-zero edge

For an interior mesh edge vw, let u and z be its opposite triangle vertices. The reduced coefficient at v vanishes exactly when u,v,z are collinear; at w it vanishes exactly when u,w,z are collinear. Both cannot hold, because u and z are distinct and it would put v,w,u,z on one line, making both incident triangles degenerate.

This statement applies when both endpoints produce rows. In particular, if v,w are both in S and r_vw=0, the other coefficient cannot also be zero. It would then be a half-edge at w, contradicting closedness. Hence every mesh edge whose endpoints lie in S has nonzero coefficients at both endpoints.

Conversely, if v is in S and r_vw is nonzero, closedness forces a nonzero row coefficient at w, placing w in the same component S. Therefore, for each v in S:

- its neighbors in S are exactly its nonzero-coefficient rays;
- its neighbors outside S are exactly its zero-coefficient rays;
- the active graph on S is the full induced mesh graph.

These conclusions do not assume that a zero-coefficient edge is absent merely because it is not an active graph edge; the no-double-zero argument is essential.

### Lemma 2: the zero-ray classification

For a ray i in an even interior fan, r_i=0 exactly when

theta_(i-1)+theta_i=pi.

For n at least 6, there are at most two such indices, and if there are two they are cyclically adjacent. Indeed two nonadjacent zero indices use disjoint pairs of positive gaps, whose sums already exhaust 2pi; at least one further positive gap remains, a contradiction. Three zero indices cannot be pairwise adjacent in a cycle of length at least 6.

For n=4, a zero index always comes with its opposite zero index, because the complementary two gaps also sum to pi. Either there are no zeros, there are exactly two opposite zeros, or all four coefficients vanish. The last case is singular and has been removed from R.

### Lemma 3: local shape of the induced complex

Let K consist of every mesh simplex all of whose vertices lie in S. It is finite, compact and connected because its induced edge graph is the connected component S. A sufficiently small neighborhood of each v in S has one of the following intersections with K:

1. No zero ray: the whole disk about v lies in K.
2. One zero ray, necessarily n at least 6: the two bounding supported rays are opposite. The supported fan is a half-disk; v is straight on the boundary.
3. Two adjacent zero rays, necessarily n at least 6: write the four consecutive bounding rays p,a,b,q, with a and b zero. The relations are p opposite b and a opposite q. If their successive angular gaps are x,y,z, then x+y=y+z=pi. The missing sector has angle x+y+z=2pi-y>pi, so the supported sector has angle y<pi. This is a strictly convex boundary corner.
4. Two opposite zero rays in a nonsingular n=4 star: the two supported rays are opposite. Locally K is a straight line segment, with no supported triangles at v.

Every listed local intersection is convex. The interior of an induced edge has either one or two incident induced triangles, or none; locally it is respectively a half-disk, a disk or a line segment, again convex. Triangle interiors are locally convex. Thus K is locally convex everywhere.

### Lemma 4: compact connected locally convex finite complexes are convex

Here is an elementary finite-complex argument, included to avoid importing a local-to-global convexity theorem. Any two points p,q of K can be joined by a polygonal path in K: connect them to vertices of simplices containing them, then use the connected edge graph. Subdivide a polygonal path into finitely many segments, each carried by one closed maximal simplex, and label each segment by that simplex. This subdivision exists because the intersection of a segment with any simplex is an interval or a point, and the complex is finite.

If a simplex label occurs more than once, replace the chain from the start of its first labelled segment to the end of its last labelled segment by the straight segment in that convex simplex. This never increases length and reduces the number of labels. Repetition gives a labelled polygonal chain with distinct simplex labels. Incidental intersections of that chain with other simplices need not receive additional labels.

There are only finitely many ordered lists of distinct maximal simplices. For a fixed feasible list, the successive junctions range over the compact intersections of consecutive closed simplices, with p in the first and q in the last. Every resulting segment lies in its labelled convex simplex. Length is a continuous function on this finite product of compact sets, so it attains a minimum. Taking the least over the finitely many feasible lists gives a globally shortest polygonal path in K.

If that path bends, take nearby points on the two sides of a bend inside a neighborhood on which K is convex. The joining segment lies in K and strictly shortens the path. Consequently a shortest path has no bend and is the straight segment pq. Thus every pq lies in K, proving convexity.

### Theorem: S induces a convex polygon triangulation

Apply Lemma 4 to K. It cannot be zero-dimensional because each retained row has at least two nonzero coefficients. If K were one-dimensional, its embedded graph would be a finite segment with an endpoint of degree 1, again impossible: Lemma 2 gives at least two supported neighbors at every vertex.

Thus K has nonempty planar interior and is a convex polygon. In particular, the line-star case in Lemma 3 cannot occur: the convex hull of any such vertex and a triangle in K would give a two-dimensional sector there. This explicitly excludes a valence-4 chain joining or touching a two-dimensional component, including attachment at a common vertex.

All its faces come from the original induced conforming complex, so K is triangulated by the supported triangles. The boundary cases are now exactly (2) and (3):

- at a straight boundary vertex, exactly one mesh neighbor is outside S, so the induced degree is n-1, odd and at least 5;
- at a strict corner, exactly two mesh neighbors are outside S, so the induced degree is n-2, even and at least 4;
- at an interior vertex no mesh neighbor lies outside S, so induced degree equals the original even degree, at least 4.

There are no holes, pinched attachments or extra zero-coefficient induced edges.

## 4. Euler restriction and a positive interpolation corollary

For any triangulation of a polygonal disk, write d(v) for its edge degree. Euler's formula and edge-face incidence give

sum_(interior v) [6-d(v)] + sum_(boundary v) [4-d(v)] = 6.

Apply this to the convex induced submesh K. Every boundary summand is nonpositive. Every interior degree is even and at least 4, so the only positive summands are +2 at degree-4 vertices. It follows that K contains at least three interior degree-4 vertices.

Those vertices are nonsingular in the original mesh: S contains only nonzero rows. Their original and induced stars coincide because they are interior to K. Therefore every closed component contains at least three original nonsingular degree-4 interior vertices.

**Corollary.** If the whole original mesh has at most two nonsingular degree-4 interior vertices, R has no closed component. Every component is then forced to zero in the left-nullspace by a half-edge and propagation, so R has full row rank. Hence every prescribed collection of vertex values and gradients has a globally C1 piecewise quartic interpolant on that same fixed mesh.

No external dimension formula or generic-position theorem is needed for this corollary.

## 5. What remains unresolved

The convex-support theorem does not prove cycle imbalance. The exactly verified eighteen-vertex family has a closed convex 12-vertex support and therefore passes this necessary geometric test, but has full row rank because its cycles are unbalanced.

The exact remaining task is either to construct an admissible mesh with a closed cycle-balanced component and a nonzero local jet form, or to prove that cycle balance cannot occur under the geometric restrictions above. No claim in this report treats failure of a sequential extension algorithm, local construction, stability, approximation order, or interpolation after refinement as a counterexample to the fixed-mesh question.

## Bounded algebraic cross-check

For the rational t=3 member of the closed-support family, all 12 rows were recomputed from its exact rational reduced matrix. Both displayed first-moment identities and the homogeneous second-moment identity held exactly. The induced core degrees were 4 at its six outer-core vertices and 6,4,6,4,6,4 around its inner hexagon. Thus precisely three interior degree-4 vertices contribute +6 in the Euler formula, with every other summand zero. This is a consistency check of the proved identities and the necessary restriction, not a proof of the general theorem.

## Primary-source scope references

The original question and model were checked in the primary sources. See [SOURCES.md](SOURCES.md) for exact versions and inspection limits. The principal references are:

- Peter Alfeld, Multivariate splines and the Bernstein-Bezier form of a polynomial, in Oberwolfach Report 21/2015, printed p.1146, items 16-18: https://publications.mfo.de/handle/mfo/3469 ; DOI https://doi.org/10.4171/OWR/2015/21 .
- Expanded author copy, Definition 1 and Section 9, Theorem 4 and Conjecture 2: https://peteralfeld.github.io/home/mfo.pdf ; DOI https://doi.org/10.1016/j.cagd.2015.11.007 .

The structural claims in Sections 1–4 are proved here. The bounded literature review did not establish a complete resolution or worldwide openness. This is authored mathematical exposition; copied source documents and source arrays are not included.
