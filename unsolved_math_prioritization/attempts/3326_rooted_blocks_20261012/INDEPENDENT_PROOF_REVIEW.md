# Independent review: rooted cyclic blocks and the exact wedge-dimension threshold

## Verdict and precise scope

**Accept both fourth-pass mathematical results:** the rational rooted-block insertion theorem and its two dimension-three families, and the exact incidence-dimension formula for the root-5 wedge. These are substantive extensions beyond a degree-three incidence-2-core sufficient condition. They do not solve the general triangle-representation problem. In particular, incidence dimension four in the second family is not geometric nonrepresentability.

The complete fixed geometry report is distributed unchanged as [ROOTED_BLOCK_PROOF.md](ROOTED_BLOCK_PROOF.md), with SHA-256 `a96576d966ac56a2d899ecb5f7f6a743e123f91068504d3da5884aea02f9f8db` and 19,046 bytes. The complete dimension report is distributed as [ROOT5_DIMENSION_PROOF.md](ROOT5_DIMENSION_PROOF.md), with only a publication-boundary metadata substitution. The complete exact realizer certificate is distributed unchanged as [EXACT_CERTIFICATES.json](EXACT_CERTIFICATES.json), with SHA-256 `a65396ff05713099a09ac76c67112c27ac3cff9e77c9c9d85462eda46157887c` and 59,923 bytes. The review covers every general proof, not merely the finite examples.

The conventions are finite covered loopless linear hypergraphs. A triangle is its closed filled convex hull; the full nerve records common intersections of every nonempty subfamily; the listed hyperedges are precisely its maximal faces. No contact, boundary-only, or disjoint-interior restriction is imposed. Linearity and looplessness ensure that distinct hyperedges cannot contain one another.

Write F for the block with vertices 1,2,3,4,5 and edges a=12, b=23, c=34, d=14, e=135, f=245. Its five-vertex example, dimension-three certificate, and nonplanar incidence graph are already in de Fraysseix, Ossona de Mendez and Rosenstiehl, *Representation of Planar Hypergraphs by Contacts of Triangles*, printed p. 135. I inspected the retained rendered page, including its displayed realizer, and verified the transcription. The new claims here concern the rooted models, block insertion, and wedge formulas; no literature novelty or current-status assertion is accepted. [Published chapter](https://doi.org/10.1007/978-3-540-77537-9_15).

The complete accepted private-boundary/core-extension review and the complete normalized-coordinate review were read. The former supplies the private-side lemma used below. The latter supplies the explicit full-nerve degree-three base, retaining credit for the rapidly increasing coordinates and radial normalization in Ossona de Mendez, *Realization of Posets*. The new insertion theorem needs only a correct starting triangle representation; it does not inherit an unproved general convex-to-triangle step. [Poset article](https://jgaa.info/index.php/jgaa/article/view/paper48).

## 1. Rooted half-plane insertion preserves the entire nerve

Let T_v be an existing nondegenerate rational triangle, and choose a side-interior point with a neighborhood meeting no other old triangle. Shrinking this neighborhood ensures that T_v agrees there with one supporting closed half-plane. A rational point can be chosen because rational points are dense along a rational side and the private neighborhood is open. A rational affine chart sends that point to the origin and the local inside to y<=0.

In a rooted model all nonroot objects are bounded rational triangles. Their finite union lies in a bounded box. A sufficiently small positive rational dilation of the model puts every nonroot triangle inside the chart neighborhood. The root remains the old triangle, whose intersection with this entire inserted family agrees exactly with the model half-plane.

The full-nerve proof has three exhaustive cases. An old-only subfamily is unchanged. A subfamily consisting of the old root and new triangles, or of new triangles alone, has exactly its model intersection behavior. A subfamily containing a new triangle and any different old triangle is empty already on that pair, because the whole inserted family lies in the private neighborhood. This excludes all unintended higher intersections, not merely unwanted edges in the pairwise intersection graph. The affine maps preserve rationality, convexity, and nondegeneracy.

Every old and new whole hyperedge is retained. An old edge and a new edge can share only the identified vertex. Internal linearity is unchanged, all edges still have at least two vertices, and all vertices remain covered. Thus no edge disappears from the maximal-edge list through containment.

The private-boundary lemma really needs full-nerve correctness. For an old vertex of degree at least two, group its intersections with other triangles according to incident hyperedge. The groups are nonempty compact and pairwise disjoint: a point in two groups would give a forbidden triple, and uniqueness of the hyperedge containing each intersecting pair forces those groups to coincide. If the polygon boundary were covered by these groups, connectedness would force one group to contain the entire boundary. Joining its common edge witness to each boundary point and using convexity then puts the entire polygon in that same group, contradicting the other nonempty group. A private point therefore exists, and a small neighborhood yields a side-interior one. This also works when some incident groups never reach the boundary.

All newly introduced vertices of F have degree at least two. They acquire private arcs from the lemma immediately after insertion. The root has degree at least two after insertion and can receive a newly chosen private arc. Any other old triangle remains disjoint from the inserted family, so it still has a private side neighborhood, possibly smaller. These facts justify arbitrary finite recursive block insertion, including attachment at a newly introduced vertex. They do not assert that a previously used neighborhood remains available unchanged.

## 2. Exact rooted geometry and the unbounded-root issue

### Root 5

With root half-plane y<=0, the four original segments have endpoints

- 1: (0,0) to (2,2)
- 2: (3,0) to (1,2)
- 3: (0,0) to (3/2,3)
- 4: (3,0) to (3/2,3)

Their six pair intersections are respectively the four pair-edge witnesses (3/2,3/2), (1,2), (3/2,3), (2,2), and the two root-edge witnesses (0,0), (3,0). These six points are distinct, so no three nonroot segments intersect. At y<=0 only the two endpoint groups remain. This gives exactly all six maximal faces, including the two triples.

### Root 1

The three segments run from (-2,0), (2,0), and (0,0), respectively, to (0,4), and the remaining triangle is conv{(-1,2),(1,2),(0,0)}. The root meets precisely the three groups prescribed by a, d, and e. The segments share (0,4), which is outside that triangle, giving f. The two sloping segments meet the triangle only at (-1,2) and (1,2), giving b and c. The vertical segment intersects it from height 0 to height 2, a subset of the intended face e. These calculations exclude all other triples and hence every larger nonface.

The rotation 1->2->3->4->1 fixes 5, permutes a,b,c,d and interchanges e,f. It is an automorphism, so the second model covers all four degree-three root choices. Together the two models cover every vertex of F.

### Thickening and strict witnesses

The displayed thin triangle around a segment is nondegenerate for eta>0, contains the entire original segment in its interior, and converges to it in Hausdorff distance. The dilation of the ordinary triangle about its centroid similarly contains it in its interior. Faces therefore persist under the outer perturbation.

The half-plane's unboundedness is not a gap in the argument. Here is a direct justification independent of the author's compact truncation. Every empty subfamily contains at least one bounded nonroot object, since the root singleton is nonempty. For that subfamily, the continuous function given by the maximum of the distances to its original closed objects is coercive because at least one object is bounded. It attains a positive minimum: a zero minimum would be a common point. There are finitely many empty subfamilies, so their positive minima have a positive minimum. A smaller uniform Hausdorff thickening of the bounded objects, leaving the root fixed, cannot create any common intersection. Equivalently, one can truncate the root inside a large compact triangle that agrees with the half-plane throughout a fixed neighborhood of all possible perturbed objects. Both approaches handle empty subfamilies containing the root rigorously.

At a root witness originally on y=0, the thickened nonroot objects contain a disk around that point. A point strictly below y=0 in this disk is interior to every participating object, including the root. The reports give explicit such rational points for eta=1/1000. My independent exact inequality check confirms all their strict slacks. With the oriented inequalities of the reports, the minimum slack is 1/125000 for root 5 and 1/62500 for root 1. Thus the particular displayed parameter is certified exactly, separately from the small-parameter existence argument.

## 3. Wedges, whole cyclic cores, and actual recursive patches

For two root-5 blocks the translated nonroot families have disjoint horizontal projections. The root triangle conv{(-4,0),(14,0),(5,-20)} agrees with y<=0 on every relevant portion of those triangles. Hence the full nerve is the wedge. It has nine vertices and twelve edges, 33 nonempty faces, and root degree four. Every incidence node has degree at least two, so the entire incidence graph is its 2-core. None of the root's degree-four contribution comes from a pendant tree.

For k root-1 blocks, translating block i by (5i,0) separates their horizontal projections: each lies in [5i-1003/500,5i+1003/500], whose length is less than 5. Below y=0 every point has depth at most 3/500. At depth d the two sides of the proposed root triangle

    conv{(-4,0),(5k+4,0),(5k/2,-5k-10)}

have horizontal coordinates -4+c_k d and 5k+4-c_k d, where c_k=(5k/2+4)/(5k+10)<1/2. At the largest possible depth they remain beyond -3.997 and 5k+3.997, strictly outside all the translated intervals. Thus its replacement of the half-plane changes no root intersection for every k>=1. All nonroot blocks remain disjoint. This verifies the universal geometry formula, including the k=1 boundary.

The root-5 family is also representable for every k, irrespective of its incidence dimension: repeatedly attach the rooted model at the common root using the insertion theorem. The same separated-translation argument works as well. Its single-block horizontal bounds are [-9/2000,6009/2000], and its maximum depth is 9/2000, which easily fits the same large-root construction.

In the root-1 wedge the common vertex has degree 3k and every other incidence node has degree at least two. Again the entire graph is its 2-core. In either family the original block contains a K3,3 subdivision with branch parts {1,3,f} and {2,4,e}, and nine paths

    1-a-2, 1-d-4, 1-e;
    3-b-2, 3-c-4, 3-e;
    f-2, f-4, f-5-e.

The interiors are pairwise disjoint and avoid all branch nodes; every consecutive pair is an incidence. This proves connected nonplanarity for each wedge. Nonplanarity of the incidence graph is compatible with unrestricted intersections of filled triangles.

I also constructed a separate recursive rational regression. Starting with one root-1 block, it finds a rational private side point on triangle 2, chooses scale 1/32, and inserts a root-5 block. It then finds a private side point on one new triangle, again uses scale 1/32, and inserts a root-1 block. Each local chart is certified by strict separation from every other old triangle and strict inclusion in the parent's other two half-planes. Every old triangle's coordinates remain identical. Full nerves were checked on all 511 subfamilies of the intermediate nine-triangle family and all 8,191 subfamilies of the final thirteen-triangle family. No incidence-dimension assertion is inferred for this extra regression.

## 4. Dimension three in the root-1 family

The three local word patterns in the geometry report realize F with root 1. The first two begin with the root, while the third has the stated B-prefix and A-suffix. I verified every ordered incidence-element pair, independently of the author's order checker.

For arbitrary k, the global first and second orders restrict to these local orders on every block and the root. Every within-block pair and every pair involving the root consequently has the required relation. For a pair of nonroot elements from distinct blocks, the first order puts the lower-index block first and the second puts the higher-index block first. Thus all cross-block pairs are incomparable, whether they are vertex/vertex, vertex/edge, edge/vertex, or edge/edge. This is the complete pair partition; it proves a three-order realizer for every k.

The restriction to vertices 1,2,3 and edges a,b,e is S3. The three missing incidences cannot have two reversals in one order because the two cross-incidences complete an alternating directed cycle. Hence three orders are necessary. The root-1 wedge therefore has dimension exactly three for all k>=1, and gives unbounded degree 3k entirely in a nonplanar cyclic incidence core.

## 5. Exact dimension threshold for the root-5 family

### Positive certificates and their expansion

The dimension report's sufficient vertex-permutation conditions are correct for covered clutters. Inserting each edge immediately after its last member yields a linear extension. The two orientations of every vertex pair are explicit. For a missing incidence, one permutation puts all edge members before the excluded vertex, giving edge-before-vertex; a permutation placing that vertex before any chosen edge member gives the opposite orientation. For two distinct edges, the clutter condition supplies a member in each difference; their missing-incidence witnesses put the edge pair in both directions. Simultaneous edge insertions do not cause a problem, because these witnesses put the relevant edge strictly before a member of the other edge.

I independently intersected the full raw orders, without using their canonical-expansion procedure. W_2 has 21 incidence elements, 420 ordered pairs, and 28 strict incidences; W_3 has 31 elements, 930 ordered pairs, and 42 strict incidences. The intersection in each case is exactly its incidence relation. Restriction supplies the k=1 case as well. Every block contains the same S3 lower bound, so the dimensions are exactly three for k=1,2,3. The search that found the orders is not used as evidence of validity.

### A block cannot have the root first in two of three realizing orders

Assume the contrary. Every nonroot vertex must precede the root in the third order. Split the nonroot vertices into A={1,3} and C={2,4}; the root edges are e=A union {r} and f=C union {r}. All missing reversals e<c and f<a must be supplied by the first two orders, because the third puts all these vertices before r and hence before e,f.

One order cannot supply a reversal of each type: a<e<c<f<a would be a cycle. Since at least one reversal of each type is required, all e-before-C reversals must be assigned to one order and all f-before-A reversals to the other. Thus the first order puts A before C and the second puts C before A.

Let q be the earlier C vertex in the first order and b its companion. For either a in A, the pair-edge {a,b} must precede q somewhere. It cannot do so in the first order because q<b, or in the second because q<a. Hence both such pair-edges precede q in the third order, forcing every other nonroot vertex before q there. The analogous argument with the earlier A vertex p in the second order forces every other nonroot vertex before p in the third. Since p and q differ, these demands contradict one another. All four required pair-edges exist because they form the complete bipartite cycle between A and C.

### Every block consumes a distinct sole-after-root order

In a three-order realizer every nonroot vertex appears both before and after r. If no vertex of one block appeared after r in exactly one order, every nonroot vertex would have a unique before-r order. Each nonroot pair-edge must precede r in some order, forcing its endpoints to have the same unique before-r order. Connectivity of the four-cycle forces all four unique orders to coincide. The remaining two orders put r before every nonroot vertex, contradicting the preceding lemma.

Choose one vertex x_i from each block that follows r in only one order t_i. Each such vertex lies in a root edge g_i. If t_i=t_j for two blocks, the missing reversal g_i<x_j must occur in that common order, since in the other two x_j<r<g_i. The reversal g_j<x_i is similarly forced there. Their required incidences then give x_i<g_i<x_j<g_j<x_i. Therefore the t_i are distinct and there can be at most three blocks. This proves dimension at least four for every k>=4. It does not depend on the private k=4 search, whose timeout is explicitly excluded from evidence.

### Uniform upper bound four: all pair types

The first three local root-first orders in the dimension report realize the induced subposet on the ten nonroot elements. Their derivation from the credited source orders is valid: moving r earlier preserves comparisons among the other vertices and can only help an edge precede an excluded nonroot vertex. Exact comparison independently confirms the local assertion, including edge/edge pairs.

The first and second global orders use opposite block concatenations. They reverse every cross-block pair of nonroot elements. The first three orders already have correct within-block nonroot relations; adding another linear extension cannot destroy required incidences or make an already incomparable pair comparable. The fourth order puts all nonroot vertices first, then all nonroot edges, then r, then root edges. It is a linear extension. It reverses every root/nonroot-vertex pair and every root/nonincident-edge pair relative to the first three, while keeping r before all incident root edges. These classes exhaust all pairs. Thus four orders suffice for every k, proving the exact formula: three for 1<=k<=3 and four for k>=4.

There is no contradiction with the geometric insertion theorem: every W_k has a triangle representation, but vertex identification need not preserve incidence dimension at most three. This distinction is essential to the accepted scope.

## 6. Independent computation and controls

My geometry implementation uses exact rational Fourier-Motzkin elimination, rather than either of the author's polygon-clipping and active-line enumeration algorithms. Every feasible subfamily returns a rational point satisfying all original inequalities. Every infeasible subfamily returns nonnegative rational multipliers whose weighted original normals sum to zero and whose weighted right side is negative. Such a certificate makes a common point impossible. A separate replay program checks these certificates directly, with no elimination procedure.

There are 26,230 retained complete subfamily certificates: both half-plane models, both wedge families for k=1,2,3, and the two recursively inserted examples. Thus all 8,191 nonempty subfamilies are checked for each of three different thirteen-triangle families. Maximal faces are explicitly compared with the original whole hyperedges; all intended edges have strict witnesses. Closed-set controls include point intersections, line/strip feasibility, parallel disjoint constraints, and inconsistent zero-normal inequalities.

The independent order checker intersects suffix bitsets for each total order and compares the resulting strict relation against the incidence list. It checks both raw W_2 and W_3 certificates, the induced ten-element nonroot local lemma, and both uniform order constructions for k=1,...,40,64,100. The k=100 tests cover 1,001 incidence elements and all 1,001,000 ordered distinct pairs each. The proofs above supply the universal quantifiers. A separate exhaustive check of 7,200 root-first/root-first/root-last vertex-order triples corroborates the root-first obstruction, but is not its proof.

All verification gates are explicit exceptions. Normal Python, -O, and -OO produce identical canonical outputs. Seeds 1,77,999 produce identical sorted outputs. Eight genuine independent source mutations are rejected with their intended diagnostics in every mode: negative thickening, colliding block translations, removal of segment reach, loss of the reverse root-1 block order, omission of the root-5 fourth order, corrupted primal and dual certificates, and disabled audit gates. These are 24 source-mutation rejections, in disposable writable copies.

The final author checkers and control harnesses are separately replayed on disposable copies under all three modes. The geometry harness tests seven actual source/order mutations in each mode; the dimension harness tests five corruptions in each mode. In addition, this audit applies three actual source mutations to the final dimension checker under every mode, removing the reversed block order, dropping the fourth order, and omitting the root from the vertex inventory. No timeout, import failure, unrelated exception, or mere nonzero exit is accepted as the intended rejection.

Exact final inputs, complete proof reviews, raw certificates, canonical diagnostics, source programs, and recovery metadata are retained in the private audit packet. A manifest binds every payload file. Both a complete archive and a content-addressed store are actually reconstructed into fresh directories and byte-checked; reconstructed verification is replayed. Preservation metadata is separate from the mathematical argument. No remote, queue, or fifth-pass action is part of this audit.

## Acceptance boundary

The accepted new geometric operation attaches an entire cyclic nonplanar block at one old vertex and preserves every old triangle. It supports finite block trees and the stated high-core-degree examples. It cannot be applied merely because an arbitrary new block has a private arc in some unrelated representation; a correct rooted half-plane model is required. It does not attach one new block simultaneously to two already constrained old vertices, and gives no representation of every high-degree indivisible cyclic core.

The root-1 wedges lie in the intended dimension-three class for every size. The root-5 wedges lie in that class precisely through three blocks, although all sizes remain geometrically representable. The general triangle-and-segment conjecture remains unresolved by these packets. Original source credit, all prior convention distinctions, and the separation between finite certificates and universal proofs are preserved.
