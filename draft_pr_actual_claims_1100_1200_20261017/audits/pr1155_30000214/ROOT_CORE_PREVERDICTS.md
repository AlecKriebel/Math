# Root mathematical analysis before old verdicts

This is an adversarial supplied-candidate review, not independent rediscovery.
The prior body/outline and speculative approach exposures are recorded in
ROOT_TARGET_PREPROOF.md. This analysis follows full PROOF.md and Nevo's nine-page
v2 text, OWR target/context and LSV PDF pages1–14, before reading the candidate's
old audits, validation or acceptance reports.

## Construction and exact imported hypotheses

Put d=3 and q=11 in LSV. Section2 supplies the building vertices as homothety
classes of O-lattices; neighbors of [L] are exactly subspaces strictly between
yL and L. The dimension1 and dimension2 subspaces of F11^3 give the two neighbor
types. A link edge is exactly a flag of those two types, hence each link is the
point-line incidence graph of PG(2,11). The building is connected (composition
series of lattices), locally finite, and pure2dimensional, with no larger cells.

LSV's Section3 construction embeds the cyclic algebra modulo its central units
in PGL3(F), and conjugation on its nine-dimensional algebra gives an injective
linear representation; its kernel consists of central elements, already removed
in the projective group. Section4, Proposition4.8 proves a simply transitive
vertex action without invoking Section6's spectral assertion. Definition4.7 and
Equation9 place every generator in GL9(F11[t]) with matrix entries of degree at
most1. Corollary4.6 writes any neighbor of the base vertex by one generator if
the lattice index is11, and by two if the index is11^2. This covers the entire
undirected neighbor set, including steps that might otherwise be misrepresented
as single inverse generators. Their inverses also have polynomial entries since
this is a subgroup of GL9 of the polynomial ring. No reduction at an inadmissible
ideal of the original localized algebra is used: the reduction is of the faithful
polynomial matrix representation itself.

For a graph path from o to gamma o of length r<=4, identify its successive vertices
with their unique group elements. Consecutive quotients are base-neighbor
elements. Therefore gamma has matrix degree at most2r<=8. Reduction modulo t^9
is a group homomorphism to a finite general linear group, so its kernel is normal
and finite index. If gamma is in that kernel, degree<9 and divisibility by t^9
force its matrix to be I, then faithfulness forces gamma=1. Normality and
transitivity conjugate the displacement estimate to every vertex. This is not
merely an assertion of torsion-freeness; it is the required geometric separation.

The orbit vertex set is finite by finite index and simple transitivity. Faces
are images of existing building faces, not newly completed cliques. No face
identifies vertices since its diameter is1. Distinct neighbors of a given lift x
have distance<=2, so their quotient images are distinct. Every quotient edge or
triangle incident with [x] can be translated by a kernel element to a lift
incident with x. Its other vertices are uniquely determined among neighbors of
x. Thus the link is an isomorphic abstract graph, both on vertices and edges.
Every face extends to a triangle, and connectedness is inherited. The claimed
finite simplicial quotient and unchanged links follow with no global Ramanujan
input. The existence and simply transitive action are substantial credited
external inputs, not re-proved foundational building theory.

## Spectral inequality and cocycle identity

There are133 points and133 lines, each degree12. M M^T=11I+J: diagonal12,
off-diagonal1. Thus singular values of M are12 once and sqrt11 with multiplicity
132, and the bipartite adjacency spectrum is +/-12 and +/-sqrt11. The
unnormalized Laplacian has smallest positive eigenvalue12-sqrt11. The unique
zero eigenspace is constants, proving connectedness. Bipartiteness and unique
point-pair lines exclude cycles shorter than6.

For H=G-w, extend any unweighted-mean-zero function by0 at w. Its squared norm
and mean are unchanged; subtracting the deleted incident-edge energies costs at
most the squared norm. The resulting bound is E_H >= (11-sqrt11)||x||^2.
It is positive, so H is connected. For any nonconstant f subtract its unweighted
mean c0. Weighted variance is the minimum over c, hence at most
sum d_H(v)(f(v)-c0)^2 <=12||f-c0||^2. Dividing gives the normalized gap at least
(11-sqrt11)/12>7/12>1/2. This argument has the correct inequality direction
despite irregular degrees11 and12. The same regular calculation gives G's gap.

For a pure finite2complex X, m(e)>0 is its number of incident triangles. Choose
the minimum weighted-norm cocycle in any cohomology class, using closedness of
the finite-dimensional subspace of coboundaries. Differentiating along a
vertex-supported coboundary gives sum_u m(vu)a_vu=0, irrespective of orientation
convention. At v, the function f_v(u)=a_vu is therefore mean zero for the actual
link-degree weights, since deg_link(v)(u)=m(vu). The cocycle equation gives
f_v(u)-f_v(w)=-a_uw. Summing link Poincare inequalities gives E(a)>=2lambda E(a):
each opposite edge occurs once per incident triangle on the left and at its two
endpoints on the right. Lambda>1/2 forces E=0. This is a complete finite linear
algebra argument, including existence of the minimizer and the factor2, not an
unsupported appeal to a global cohomology/spectral theorem.

## Deletions and all Reisner cases

Each edge of K lies in12 triangles, since a vertex in the corresponding link
has degree12. Deleting one vertex removes at most one triangle on any surviving
edge, leaving at least11. Each remaining vertex originally has266 neighbors
and loses at most1. Thus every remaining face extends to a2face and the
deletion is nonempty, pure and still dimension2. K is connected; bypass any
deleted vertex in a path through its connected link, using edges of that link
as actual surviving edges. Vertex links of the deletion are G or G minus one
vertex, with precisely the triangles/weights of the deleted complex. The cocycle
argument gives H^1 overR, and duality gives H1 overR. Integer boundary matrices
have the same rank overQ and any characteristic-zero field, proving the claimed
Q and characteristic-zero statements without using F11 as a coefficient field.

For the empty face, connectedness and H1=0 are exactly the below-top reduced
homology requirements in dimension2 (nonemptiness covers negative degree).
Vertex links are nonempty connected1complexes, edge links are nonempty
0complexes, and facet links are {empty}, of dimension-1. These are all face
cases, before and after every vertex deletion. Hence K is2-CM in the exact
same-dimension sense of Nevo's Definition3.1. Top H2 need not vanish, and the
proof does not accidentally require it.

## Sphere exclusion and target resolution

Use the standard link-inclusive homology-sphere convention: every face link has
the homology of the sphere in the prescribed complementary dimension. In a
2sphere subcomplex S, each edge link is0dimensional with reduced H0 of dimension1,
hence contains exactly2 vertices. Thus each edge lies in2 triangles. At each
vertex the link is a connected graph whose vertices all have degree2; as a
finite simple graph it is a cycle. It embeds as a subgraph of a G link, so has
length>=6. Consequently 2f1>=6f0 and 3f2=2f1. Euler characteristic is
f0-f1+f2=f0-f1/3<=0. But the global sphere homology over any field gives Euler
characteristic2. The combinatorial contradiction uses no orientability
assumption, universal-cover lifting or topological-sphere classification.
It does require the standard local-link definition; a complex with only global
sphere homology is not excluded and is outside that definition. Thus no sphere
piece can appear at all, defeating the exact cover question and a fortiori the
overlap/reordering requirements. No field-uniform CM or subdivision claim is
needed.

## Independent diagnostics and remaining limits

The independent standard-library finite_incidence_and_threshold.py constructs
all133 projective points and133 dual lines overF11, checks all17689 exact Gram
entries, verifies degrees, no4cycles, all266 single deletions connected and all
deleted degrees11/12. It also constructs a7vertex triangulated torus with all
links C6 and exactly computes rational H1 dimension2: gap=1/2 is genuinely a
boundary where the strict lemma cannot be weakened. A nonzero exact cocycle
checks both energy double counts. These are finite, falsifiable supporting
checks; they do not enumerate the huge quotient or establish lattice existence.
The universal proof rests on the checked symbolic arguments and explicitly
credited LSV inputs. Priority/novelty is a separate unresolved audit at this
checkpoint. No mathematical gap or repair is currently identified.
