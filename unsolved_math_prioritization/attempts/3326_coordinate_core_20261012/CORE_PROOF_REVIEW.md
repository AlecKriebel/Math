# Independent proof review: cyclic-core triangle extension

## Verdict and exact boundary

**Accept the cyclic-core extension theorem, its rational pendant construction, and the connected nonplanar unbounded-degree family. The separately accepted coordinate proof supplies its maximum-degree-three base, while preserving the published source credit.** No mathematical correction to the author's frozen candidate was required. Neither this theorem nor its finite tests settle a vertex of degree four entirely within the incidence graph's 2-core, or the general triangle-representation problem. No novelty or current literature-status claim is made.

The accepted statement is: a finite covered loopless linear hypergraph whose incidence poset has dimension at most three has a representation by nondegenerate closed filled rational triangles whenever every vertex-node of the incidence graph's 2-core has degree at most three in that core. Its inclusion-maximal common-intersection subfamilies are exactly the original hyperedges. Degrees outside the core, and additional tree incidences at core vertices, are unrestricted.

The author report reviewed has SHA-256 `25253aa516eb13420417296bba695ebb95c9f9986f72c926071a32f20aa0a6be` and 19,246 bytes. The distributed report is identified in the [public manifest](PUBLIC_MANIFEST.json). The review covers the entire report, including the arbitrary-parameter realizer argument, rather than only its seven-vertex example.

The base theorem is the previously reviewed degree-three reduction: the convex maximal-intersection consequence stated on p. 135 of de Fraysseix, Ossona de Mendez and Rosenstiehl, *Representation of Planar Hypergraphs by Contacts of Triangles*, followed by witness compression, finite full-nerve stability, and rational triangle inflation. That prior audit explicitly credited the convex consequence without independently reconstructing its deduction from Ossona de Mendez's *Realization of Posets*. This frozen extension proof accurately retains that dependency. The frozen author proof is preserved unchanged. Before this review was sealed, the separate explicit coordinate proof received final independent acceptance, and both its complete proof and review were read here. The complete [coordinate proof](FULL_NERVE_COORDINATE_PROOF.md) and [coordinate review](COORDINATE_PROOF_REVIEW.md) are included in this edition; their final acceptance is described in [INTEGRATION_AND_ACCEPTANCE.md](INTEGRATION_AND_ACCEPTANCE.md). That result proves the full downward-closed nerve directly from the realizer; for loopless linear input the hyperedges are Sperner, so maximal faces are exactly the original edges. With at most three incident edges per vertex, its rational planar hulls have at most three generators, and the accepted stability/inflation argument supplies the required rational nondegenerate triangles. Thus the combined theorem no longer retains the omitted-deduction dependency. This is an explicit integration of the separately accepted result, not a retrospective alteration of the frozen author report. The new boundary, grafting, combinatorial, and uniform-realizer arguments below have been independently checked. [Chapter](https://doi.org/10.1007/978-3-540-77537-9_15); [poset paper](https://jgaa.info/index.php/jgaa/article/view/paper48).

All sets are filled and all intersections are unrestricted. The result says nothing about pairwise disjoint interiors, one-sided contact representations, or triangle boundaries alone. Looplessness means hyperedges have at least two members; together with linearity it excludes proper containment among distinct hyperedges. Coverage excludes isolated vertices without edges. The empty hypergraph is treated separately.

## 1. Private boundary lemma

Let a finite family of nondegenerate compact convex polygons realize the full nerve of a covered loopless linear hypergraph. Fix an object C_v whose vertex belongs to at least two hyperedges. For each incident edge e, group its intersections with the other members of e into

    R_e = C_v intersect union of C_w over w in e minus {v}.

Each group is nonempty and compact. Nonemptiness uses both an edge witness and the fact that e has another member. Every intersection of C_v with another object belongs to exactly one such group: a nonempty intersecting pair must be contained in a hyperedge, and linearity gives uniqueness for that pair.

Distinct groups are disjoint. If a point belonged to the groups of e and f, it would belong to C_v, C_w and C_z for some w in e minus {v} and z in f minus {v}. For e different from f, linearity first gives w different from z. Full-nerve correctness then puts the triple into an edge g. Uniqueness for the pairs {v,w} and {v,z} forces e=g=f, a contradiction. Pairwise intersection-graph correctness alone would not justify this step.

Suppose the polygon boundary were covered by all groups. Some groups may not meet the boundary; discard these for this part of the argument. The remaining intersections with the boundary are a finite disjoint closed cover of a connected circle. If more than one were nonempty, any one and the finite union of the others would disconnect the boundary. Therefore a single R_e contains the whole boundary.

Let p_e be a common witness for edge e. Every point x in C_v other than p_e lies on a segment from p_e to a boundary point y, obtained by extending the ray from p_e through x to the last point of the compact polygon. This remains true when p_e itself lies on the boundary. The case x=p_e is immediate. Because y is in R_e, some C_w with w in e minus {v} contains y; it also contains p_e. Convexity puts the entire segment, including x, in C_w. Hence C_v is contained in R_e. A second nonempty group is then impossible, contradicting the degree assumption.

Thus a boundary point misses the compact union of every other object. Its distance from that union is positive. A sufficiently small open neighborhood contains side-interior points even if the original point was a polygon corner. After choosing such a point and shrinking again, the polygon in that neighborhood is exactly the intersection of the neighborhood with one closed half-plane. This supplies the private side arc required for insertion.

The degree assumption cannot simply be dropped: a degree-one object's triangle may lie strictly inside its only neighbor. The independent checker includes an exact containment control. The proof also does not assume that every neighbor group reaches the boundary; the single-covering-group argument above handles the principal adversarial case correctly.

## 2. Rational simultaneous insertion of a pendant edge

Place a private side-interior point of the existing triangle C_v at the origin in affine coordinates with the local inside half-plane y<=0. Choose a small neighborhood that contains no other old object and within which this local half-plane description is valid. For rational old triangles, a rational side point is available densely along the side; the side direction and a transverse inward direction give an invertible rational affine change of coordinates.

For a sufficiently small positive rational r, use the base points a=(-r/2,-r/2), b=(r/2,-r/2), and the common point q=(0,-r/4). For finitely many distinct rational parameters s_i in (-1/4,1/4), put

    t_i = r (2s_i/(1+s_i^2), (1-s_i^2)/(1+s_i^2)),
    T_i = conv{a,b,t_i}.

All three vertices lie in the closed radius-r disk, so all of T_i lies in the private neighborhood when r is sufficiently small. The tips lie on that circle, have positive vertical coordinate greater than r/2, and have horizontal coordinate of absolute value less than r/2. Each triangle is nondegenerate.

At height q_y the triangle's cross-section has center

    (r/4) (t_i)_x / ((t_i)_y+r/2)

and half-width

    (r/2) ((t_i)_y+r/4) / ((t_i)_y+r/2).

The latter strictly exceeds the absolute center, so q is in the interior of every T_i. It is also interior to C_v. Therefore the intended new edge {v,u_1,...,u_k} has a common interior witness, for any finite k>=1.

Every new object misses every old object except C_v. Thus any intersecting subfamily involving a new vertex is contained in the new edge; every subset of that edge intersects at q. The entire old family is unchanged. This proves the full nerve statement, including all higher intersections, and rules out unintended old/new pairs and triples automatically.

Each tip t_i is outside C_v. The tangent supporting line of the radius-r circle at t_i strictly separates t_i from every other new triangle: the other tips are distinct circle points, and the common base vertices are strictly inside the disk. All other old objects miss the whole neighborhood. Compactness again gives a private neighborhood of t_i, and then a private side-interior point near it. Rationality of the formulas and of the affine coordinate change gives rational final vertices.

The author correctly introduces all members of a new hyperedge together. Placing new triangles wholly inside their parent would not suffice: a later descendant edge would have to avoid its grandparent. Here the private tips extend across the parent's boundary, and the independently checked seven-vertex example explicitly verifies that its grandchild misses the original root.

After inserting at a root that already had at least one incident edge, its degree has become at least two, so the private-boundary lemma can be reapplied. Every newly introduced vertex initially has its own private arc, even at degree one. An insertion at a different vertex misses its entire old triangle and hence cannot remove its private arc. These observations justify arbitrary finite iteration; they do not assume one fixed private arc survives all uses of the same root.

## 3. Whole-edge backbone and finite reconstruction

The incidence graph is bipartite, with separately labeled vertex-nodes and edge-nodes. In any connected component with nonempty 2-core, every component outside the core is a tree with one attachment to the core. A cycle outside the core would itself survive pruning. A path outside the core joining two core nodes would survive together with the core, as all its internal nodes have degree at least two there. The same argument rules out two distinct attachments. Connectivity gives at least one attachment. It also shows that the nonempty core of a connected component is connected. A component with empty 2-core is a tree.

Initially select every edge whose edge-node lies in the core, retaining the whole original hyperedge and all of its vertices. At a core vertex the selected degree is exactly its core degree, at most three. A selected vertex outside the core has exactly one selected incident edge: two such core-edge neighbors would already force that vertex into the core. For an empty-core component choose one whole hyperedge as its initial connected subtree.

Whenever a selected vertex has selected degree one and an unselected incident edge, add one such whole edge and all its vertices. Its root is the only already selected vertex in that edge. A second would create a cycle in an outside tree or a path connecting that tree to the selected region twice. Therefore the root's degree changes from one to two, and every other vertex of the new edge is fresh and begins at degree one. A later selected edge cannot increase an existing degree-two or degree-three vertex indirectly, because that would give a second old vertex in the new edge. The procedure deliberately chooses only degree-one roots.

The finite procedure terminates with a whole-edge hypergraph K of maximum vertex degree at most three. Every selected vertex with an omitted incident edge has selected degree at least two, since otherwise the procedure would not have terminated. Vertices of selected degree one have no omitted branches and require no private-boundary assertion.

The omitted part is a collection of finite trees, each attached once at a selected vertex-node. It cannot attach at a selected edge-node, because every vertex of every selected edge was already included. Reading these trees away from their roots presents each omitted edge with exactly one old parent vertex and all other vertices fresh. This is precisely the pendant-edge insertion operation. No edge is truncated, subdivided, deleted, or identified with another edge during reconstruction.

The incidence poset of K is the induced subposet on its vertex and edge labels. This statement depends on keeping whole hyperedges. Restricting every order of a realizer gives a realizer of the induced subposet, so its dimension remains at most three. The credited degree-three theorem supplies rational nondegenerate filled triangles for K. Every omitted-tree root has degree at least two in K, so Section 1 supplies the initial private arc, and Section 2 reconstructs H. Separate incidence components can be translated by rational vectors into pairwise disjoint bounded boxes. The empty hypergraph uses the empty family.

The finite graph regressions independently use a leaf queue for the 2-core and reverse-label choices for selecting the backbone, rather than importing the author's round-pruning or selection code. They verify the necessary degree bound, degree-two attachment roots, and complete pendant reconstruction. Every covered loopless linear hypergraph on two through five labeled vertices was enumerated exactly: 2,290 inputs, of which 2,014 satisfy the sufficient core condition and 276 do not. The excluded inputs are reported as outside the theorem, not as failed geometric representations. Additional fixtures cover an empty graph, a branching forest, the nonplanar core with its two-level pendant chain, and an explicitly excluded degree-four cyclic core. These finite checks corroborate the universal graph argument; they do not replace it or assert that the tested inputs all have incidence dimension three.

## 4. Connected nonplanar degree-four example

The base edges are a=12, b=23, c=34, d=14, e=135, f=245. Add g=16 and h=67. The resulting seven-vertex hypergraph has maximum degree four at vertex 1, while its incidence 2-core is unchanged and has vertex degrees 3,3,3,3,2.

The displayed three orders were independently converted to complete strict total-order relation sets, whose intersection is exactly the incidence relation. This covers all 210 ordered pairs of distinct poset elements. The restriction to vertex elements 1,2,3 and edge elements a,b,e is S3: the three missing pairs (1,b),(2,e),(3,a) all need reversal, and any two reversals in a single linear extension contradict the two cross-incidences. Thus the dimension is exactly three.

For nonplanarity, the six branch nodes have bipartition {1,3,f} and {2,4,e}. The nine paths are

    1-a-2, 1-d-4, 1-e;
    3-b-2, 3-c-4, 3-e;
    f-2, f-4, f-5-e.

Their interiors are disjoint, contain no branch node, and their graph edges account for every incidence of the original core. They give a subdivision of K3,3, independently checked from the incidence lists. The pendant additions preserve that subgraph. Nonplanarity here concerns the incidence graph and is compatible with unrestricted triangle intersections.

The independent exact geometry checker reconstructs all seven rational triangles from the displayed formulas. It uses successive rational polygon clipping, including point and segment intermediate intersections, rather than the author's enumeration of active-line intersections. All 127 nonempty subfamilies were checked. There are 21 nonempty faces and exactly the eight stated maximal edges. In particular C_1 and C_7 are disjoint. Separate isolated-point, segment-contact, and disjoint-triangle controls validate closed-set and lower-dimensional clipping behavior.

## 5. Uniform unbounded-degree family and complete pair check

Attach z to vertex 1 by g={1,z}, and attach leaves u_0,...,u_k to z by h_i={z,u_i}, for any k>=0. The core remains unchanged, vertex 1 has degree four, and z has degree k+2. The original induced S3 and K3,3 subdivision remain, giving a dimension-three lower bound and nonplanarity. Neither conclusion is inferred from a general assertion that arbitrary tree attachment preserves incidence dimension.

The explicit upper bound uses the three orders in the author report. I checked their pair-type proof as follows.

- Their restrictions to the old core are the original three-order realizer. Every required new incidence u_i<h_i, z<h_i, z<g, and 1<g holds in all orders.
- The elements z,u_i,h_i precede all old core elements in the first order and follow them in the third. Hence every such old/new pair is incomparable, as required.
- The edge element g follows 1 in every order. It precedes every other old core element in the first two and follows the whole core in the third. Hence it has exactly its one required old incidence and no accidental relation with any other old vertex or edge.
- The pair u_0,z is reversed between the first and third orders. For i>=1, the pair u_i,z is reversed between the first and second. The center precedes every star-edge element in all three, as required.
- For two positive-index leaves, and for two positive-index edge elements, the first two orders use decreasing index and the third increasing index. Pairs involving index zero and one positive index reverse between the first and second orders. These cover all leaf/leaf and star-edge/star-edge pairs, including the k=0 boundary case where none exist.
- For positive indices i<j, the nonincidence u_i,h_j has u_i<h_j in the first order and h_j<u_i in the second. For positive indices j<i, the reverse h_j<u_i occurs in the third. For i>=1, the second reverses u_i,h_0 and the third reverses u_0,h_i; the first supplies the opposite orientation in both cases. The diagonal u_i,h_i is required in every order.
- Finally g follows every u_i,h_i in the first two orders and precedes them in the third. Its pair with z is already the required incidence.

These classes exhaust all distinct pairs. The orders therefore realize the full incidence poset for every k, and the retained S3 makes its dimension exactly three. Applying the accepted core-extension theorem proves the claimed triangle representation for the entire connected nonplanar unbounded-degree family. The independent implementation also checks k=0,...,30,50,100, reaching degree 102 at z; those values are regressions, not the proof of the universal quantifier.

## 6. Computational controls, preservation, and limits

Both the author's checker and the independent checker were run under normal Python, -O, and -OO. All gates are explicit exceptions. Each checker's three canonical outputs agree byte for byte. The exact canonical outputs were separately pinned; their substantive verification counts and boundaries are reported here. Raw output files and their identifiers are not distributed.

The independent rational gadget tests use one through twenty-four fresh vertices and verify strict common interior witnesses, rational circle identities and bounds, and strict tangent separation of every tip from all other triangles. The independent baseline also genuinely rejects a duplicated descendant triangle that hits the grandparent, an invalid realizer, a selected backbone with a degree-one attachment root, and a direct explicit-gate failure.

An additional disposable-copy harness performs five actual mutations under all three modes, giving fifteen required rejections: duplicate the grandchild geometry, invalidate an order, corrupt the uniform order by putting z before all leaves, retain an invalid degree-one backbone root, and duplicate a gadget tip. Each failure must be the intended explicit audit exception with a deterministic diagnostic. The author's separate harness supplies twelve additional mutation rejections. Canonical inputs remain unchanged. No timeout is counted as rejection or as evidence of a mathematical claim.

The fixed author manifest and every listed byte were independently checked before copying the full input packet. The audit preservation workflow records a complete payload manifest and external hash pin, creates an actual recovery archive and content-addressed byte store, reconstructs the complete packet separately from each, compares exact inventories and bytes, and replays both checkers and both mutation harnesses from the restored files. Preservation metadata is evidence of reproducibility and fixed scope, not a substitute for the mathematical review.

The remaining frontier is genuinely narrower than arbitrary high degree: the insertion proof cannot handle a new edge that must connect several already constrained old vertices in the cyclic core. No boundary-arc statement establishes those coordinated intersections. The accepted theorem supplies a sufficient class, including the stated unbounded-degree examples, without claiming the general problem is solved or that a fixed-neighbor obstruction rules out a different global construction.
