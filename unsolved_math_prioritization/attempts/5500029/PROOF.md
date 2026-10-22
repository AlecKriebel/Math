# Hamiltonian-path tetrahedralizations: a degeneration-safe reduction

Problem identity: 5500029 / AMR-054-0029 / TOPP 29.

## Status and exact scope

The unrestricted problem is **not solved here**. The target is a full-dimensional convex polytope in R^3, decomposed face-to-face into positive-volume tetrahedra whose vertices are vertices of the original polytope, with a Hamiltonian **path** in the triangular-face-adjacency dual. No Steiner vertices are allowed. Nontriangular facets and coplanar original vertices are allowed. “Vertices” means extreme points of the polytope; a separately prescribed set of additional points on edges or facets would be an additional input requirement.

This note proves a reduction valid in that scope, gives explicit geometric examples explaining two failed proof shortcuts, and records the remaining gap. The reduction is a degeneracy-safe extension of the degree-three reinsertion argument in Escalona–Fabila-Monroy–Urrutia, rather than a claimed new resolution of TOPP 29. The accompanying independent AI-assisted mathematical audit accepts these partial results. The manuscript and audit are unrefereed; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed.

## 1. Degree-three reinsertion without general position

**Theorem 1.** Let P be a convex three-dimensional polytope, and let v be a vertex of degree three. Suppose P has at least five vertices, and put Q = conv(V(P) \ {v}). If Q has a no-Steiner Hamiltonian-path tetrahedralization, then P has one. No general-position or simplicial-boundary assumption is needed.

### Geometry of deleting v

Let a,b,c be the three neighbors of v. The tangent cone at v has exactly the three incident edge rays. It is a full-dimensional pointed cone, so these rays are linearly independent. After an invertible affine coordinate change, take

- v = (0,0,0),
- a = (1,0,0), b = (0,1,0), c = (0,0,1),
- P contained in the nonnegative orthant.

The tangent-cone assertion can also be seen by cutting off a sufficiently small neighborhood of v: its vertex figure has three vertices and is a triangle. Every ray from v into P intersects this triangle, and is therefore a nonnegative combination of the three edge rays.

Write s(x)=x_1+x_2+x_3. Every other vertex w of P has s(w)>1: otherwise it would lie in conv(v,a,b,c), and, being distinct from those four vertices, would not be an extreme point of P. Also, every such w has at least two positive coordinates. A w on a single positive coordinate axis would lie farther along an incident edge ray than the named neighbor, making that neighbor non-extreme.

Consequently F=conv(a,b,c) is a triangular facet of Q. Moreover

P = Q union conv(v,a,b,c), with intersection F.

For completeness, any point of conv(v,Q) lies on a segment from v to some x in Q. That segment meets the plane s=1 at x/s(x), a point of F. The part below the plane belongs to conv(v,F), and the part above belongs to Q. This proves the displayed decomposition. Q is three-dimensional: if all vertices other than v were coplanar, P would be a pyramid and v would have degree |V(P)|−1, contrary to degree three and |V(P)|≥5.

### Replacing the tetrahedron incident with F

Let T be the assumed tetrahedralization of Q, and let tau=conv(a,b,c,q) be its unique tetrahedron incident with F. The opposite vertex q is an original vertex, with nonnegative coordinates, s(q)>1, and at least two positive coordinates.

Let I={i:q_i>0}. For each i in I put

T_i = conv(v,q,e_j,e_k), where {i,j,k}={1,2,3}.

These are positive-volume tetrahedra. They partition

U = tau union conv(v,a,b,c) = conv(v,a,b,c,q).

Here is a direct verification that also handles zero coordinates. Write an arbitrary x in U as

x = beta q + sum_i gamma_i e_i,

with alpha,beta,gamma_i≥0 and alpha+beta+sum gamma_i=1, where alpha is the coefficient of v. Set r=min_{i in I}(gamma_i/q_i). Replace beta by beta+r, gamma_i by gamma_i−r q_i, and alpha by alpha+r(s(q)−1). The coefficients remain nonnegative and sum to one, and at least one active gamma_i becomes zero. Thus x belongs to some T_i. For two active indices i and j, membership in both T_i and T_j forces x_i/q_i=x_j/q_j to be the minimum active ratio, and their intersection is exactly conv(v,q,e_k). Thus the pieces intersect in common faces and their interiors are disjoint.

Every pair of the T_i shares a nondegenerate triangle. Their dual is K_3 if all coordinates of q are positive, and K_2 if exactly two are positive.

The three possible external faces of tau, other than F, are

F_i = conv(q,e_j,e_k).

For q_i>0, F_i survives as a face of T_i. If q_i=0, the prospective tetrahedron T_i is flat and is omitted. Crucially, that omitted port F_i lies in x_i=0, a supporting plane of P and Q. It is therefore a boundary face, and has no neighboring tetrahedron of T across it. The zero-volume omission cannot remove a used edge of the old dual path.

There is no mismatch with tetrahedra outside U. Nonboundary ports are preserved exactly. In the flat case the only changed triangulation is inside a supporting boundary plane, where the old two triangles are replaced by the other diagonal of the convex boundary quadrilateral. There is no outside tetrahedron across that plane. The four boundary edges of that quadrilateral are unchanged. The removed diagonal is e_j e_k. In Q, the two supporting facets meeting along that edge are F and the facet containing F_i; tau contains a neighborhood of the relative interior of the edge inside their full dihedral wedge. Thus no other tetrahedron of T can contain that edge without overlapping tau in its interior. Removing that diagonal consequently creates no lower-dimensional mismatch with an outside tetrahedron. This also covers face-to-face conformity, rather than checking only interior disjointness.

### Splicing the Hamiltonian path

The old Hamiltonian path uses at most two edges incident with tau. Each used edge belongs to a distinct surviving external port and therefore to a distinct vertex of the replacement K_2 or K_3. A complete graph on two or three vertices has a spanning path between any two distinct specified vertices. Replace tau in the old path by such a path. If tau was an endpoint, choose a spanning path ending at its single required port; if it was the only tetrahedron, use any spanning path of the replacement graph. All other path adjacencies remain unchanged. This proves Theorem 1.

**Corollary 1.1 (reduction).** Repeated degree-three deletion reduces the question to a tetrahedron or a polytope of minimum vertex degree at least four. If the reduced core admits a Hamiltonian-path tetrahedralization, reversing the deletions supplies one for the original polytope. In particular, a vertex-minimal counterexample, if one exists, has minimum degree at least four.

This is a sufficient reduction. It does not assert the converse for an arbitrary deletion, does not establish that every core is small, and does not handle general degree-four or degree-five deletion.

## 2. Credited positive core classes

### Simplicial boundary with Hamiltonian boundary dual

Suppose P is simplicial and the dual G of its boundary graph has a Hamiltonian cycle C. The face-deletion observation of Escalona–Fabila-Monroy–Urrutia yields a face F of G such that G−V(F) has a Hamiltonian path. One proof chooses an edge outside C with shortest cyclic endpoint distance. Its shorter C-arc and that edge bound a face: a chord inside this region would have shorter cyclic endpoint distance. Deleting that face’s vertices leaves the complementary C-arc as the required path.

The face F of G corresponds to a vertex v of P. Cone v to every triangular facet not incident with v. Every resulting tetrahedron has positive volume because its base is a supporting facet not containing v. The tetrahedra partition P, and their dual is G−V(F). This argument uses the simplicial boundary, but it does **not** need the stronger condition that no four vertices anywhere are coplanar.

Using the published Holton–McKay theorem that every 3-connected cubic planar graph with at most 36 vertices is Hamiltonian, Euler’s formula gives the following credited consequence:

**Corollary 2.1.** Every simplicial convex 3-polytope with at most 20 vertices admits such a tetrahedralization, including those with nonfacial coplanar vertex quadruples. The same holds for any polytope reducible to one of these by degree-three deletions, by Theorem 1.

The finite graph-classification theorem is a literature input, not independently re-enumerated in this work. We do not upgrade this statement to every nonsimplicial polytope with at most 20 vertices.

### Pyramids, including nonsimplicial bases

Every convex pyramid over an r-gon has a Hamiltonian-path tetrahedralization: triangulate the base by a fan from one base vertex and cone its r−2 triangles to the apex. The dual is a path. This also establishes that the limiting pyramid in Section 3 is not a counterexample to the original question.

Theorem 1 therefore applies to pyramidal cores of arbitrary size as well. No claim of novelty is made for the elementary pyramid construction.

## 3. A rigorous obstruction to naive general-position specialization

The statement “take a Hamiltonian tetrahedralization of a small generic perturbation, let the perturbation go to zero, and discard flat tetrahedra” does **not** preserve the conclusion.

For 0<t≤1, define seven vertices by

0=(0,0,t), 1=(4,0,0), 2=(6,2,t), 3=(3,5,0),
4=(0,4,t), 5=(−2,1,0), 6=(1,1,10).

Let P_t be their convex hull. All seven points are extreme: the six projected base points form a strictly convex hexagon, and point 6 is the upper apex. For t>0 the first six points form a thin convex octahedron Q_t. Its upper facets are 024,012,234,450 and its lower facets are 135,123,345,501. These supporting-face descriptions follow directly from the alternating heights and convexity of the projected hexagon; the recorded independent audit also checked their exact supporting orientations.

Take the following tetrahedra, with labels in brackets:

- [0] 6024
- [1] 6012
- [2] 6234
- [3] 6450
- [4] 0135
- [5] 0123
- [6] 0345
- [7] 0234

The first four cone the upper boundary of Q_t to vertex 6. The last four are the pulling tetrahedralization of Q_t from vertex 0. Together they tetrahedralize P_t. A Hamiltonian path is

[1], [0], [2], [7], [5], [4], [6], [3].

Every consecutive pair shares exactly three vertex labels, hence a triangular face. All tetrahedra are positive-volume for 0<t≤1. In fact all 35 four-vertex orientation determinants are nonzero throughout that interval, so P_t is a general-position instance. Each determinant is affine in t; none changes sign or vanishes in the stated interval. The recorded audit independently checked these facts symbolically. The coordinates and geometric construction above specify the example without any omitted program or generated certificate.

At t=0 the last four tetrahedra become flat. The first four remain positive and still tetrahedralize P_0, the hexagonal pyramid. Their dual is K_1,3: tetrahedron [0] is adjacent to each of [1],[2],[3], and the leaves have no mutual face adjacency. A Hamiltonian path cannot cover three degree-one vertices. In particular, deleting the flat entries from the displayed path produces [1],[0],[2],[3], whose last pair shares only an edge.

Thus even starting from genuine general-position polytopes, a perfectly valid Hamiltonian tetrahedralization may specialize to a non-Hamiltonian positive-volume tetrahedralization. This rules out that specific argument; it does not rule out choosing different perturbation tetrahedralizations, retriangulating the limit, or proving a separate specialization theorem with extra hypotheses.

## 4. Why the degree-three proof does not automatically cover degree four

An explicit convex example shows that pairing each cap tetrahedron independently with the old tetrahedron behind its face can fail.

Take a=(2,0,0), b=(0,2,0), c=(−2,0,0), d=(0,−2,0),
v=(0,0,2), q=(1,1,−2), and P=conv(a,b,c,d,v,q).

Vertex v has degree four. The square interface is split along ac. On triangle acd, the old tetrahedron is qacd and the cap tetrahedron is vacd. The segment vq meets z=0 at (1/2,1/2,0), which lies outside triangle acd. Accordingly their union is not the convex bipyramid needed for a 2→3 replacement.

The sum of their six-times-volumes is 32. The three proposed tetrahedra vqac,vqcd,vqda have total six-times-volume 48, so they cannot replace that pair. The degree-three proof’s crucial convex-patch assertion is false for this degree-four attempt.

The full polytope nevertheless has a valid Hamiltonian cycle tetrahedralization, namely vqab,vqbc,vqcd,vqda around the interior edge vq. Hence this is an obstruction to a proposed induction step, not a counterexample to TOPP 29.

## 5. Recorded verification and remaining gap

During the original proof review, an exact checker used rational arithmetic and explicit exceptions, never Python assertions. Its recorded checks covered:

1. The seven-vertex family at t=1, including all pairwise tetrahedral intersections and exact equality of covered volume and convex-hull volume.
2. All 35 affine orientation certificates for general position on 0<t≤1.
3. The positive limiting complex, its K_1,3 dual, and exhaustive absence of a four-vertex Hamiltonian path.
4. 54 nonnegative integer degree-three patches, including 27 flat-boundary-port cases, with all 216 ordered endpoint-port tests.
5. A complete exact cube deletion/reinsertion example, including its intermediate convex hulls and final Hamiltonian path.
6. The degree-four failed patch and the valid global repair.
7. Nine controls rejecting false target substitutions or failed shortcut claims.

The recorded finite computations support and guard the proofs; they are not a substitute for the general argument in Section 1 and do not establish the unrestricted conjecture. Their aggregate results are retained in ACCEPTANCE.json and MATHEMATICAL_AUDIT.md. Programs, generated certificates, and raw outputs are excluded from this proof-only edition. Edition preparation reran no mathematical computation and performed no new scholarly-source retrieval, visual inspection, or literature search.

What remains is a no-Steiner Hamiltonian-path construction, or a counterexample applying to **every** tetrahedralization, for the remaining degree-at-least-four cores. General position cannot simply be removed using the failed limiting argument. The 84-point example in the existing literature obstructs common-vertex/pulling tetrahedralizations only and does not fill this gap.

## References and recorded source boundaries

The following retrieval and inspection statements are history from the proof review and audit on 10 October 2026; they are not new source work for this edition. They do not certify exhaustive literature coverage, novelty, bibliographic priority, or worldwide current openness.

- TOPP, Problem 29: https://topp.openproblem.net/p29. Retrieved again on 2026-10-10; still explicitly open. The source is about convex polytopes and paths.
- F. Escalona, R. Fabila-Monroy, J. Urrutia, *Hamiltonian Tetrahedralizations with Steiner Points*, arXiv:1210.5484: https://arxiv.org/abs/1210.5484 and https://arxiv.org/pdf/1210.5484. Full supplied PDF inspected in text. Lemma 3 supplies the general-position predecessor of Section 1; Theorem 4 and Corollary 5 supply the boundary-dual route in Section 2. The arXiv file bears a 2012 v1 marker and an internal 2021 date; this note does not invent a separate arXiv version from that internal date.
- Same authors, *Hamiltonian tetrahedralizations with Steiner points*, Bol. Soc. Mat. Mex. 23 (2017), 537–547; published online 25 November 2015, DOI https://doi.org/10.1007/s40590-015-0080-8. The accessible publisher abstract states the improved Steiner bound floor((m−2)/2)−1, whereas the supplied arXiv PDF states floor((m−2)/2). The journal’s bound is credited as a published statement; its subscription-only full proof was not inspected here. Both retain general-position and no-Steiner small-hull qualifications.
- F. Chin, Q.-H. Ding, C. A. Wang, *On Hamiltonian Tetrahedralizations of Convex Polyhedra*, ISORA 2005, pp. 206–216: https://www.aporc.org/LNOR/5/ISORA2005F16.pdf. The 92-vertex construction concerns pulling, not all tetrahedralizations.
- D. A. Holton and B. D. McKay, *The smallest non-Hamiltonian 3-connected cubic planar graphs have 38 vertices*, J. Combin. Theory Ser. B 45 (1988), 305–319, with appended 1989 erratum: https://users.cecs.anu.edu.au/~bdm/papers/HoltonCubic38.pdf; erratum DOI https://doi.org/10.1016/0095-8956(89)90025-7. The recorded audit visually inspected physical pages 1–3 and 16. Theorem 1.1 gives the at-most-36-vertex Hamiltonicity input. The erratum adds a case to Theorem 1.2 at orders 38, 40, and 42; it does not alter Theorem 1.1. The classification is a credited literature input, not independently re-enumerated or fully re-audited here.
