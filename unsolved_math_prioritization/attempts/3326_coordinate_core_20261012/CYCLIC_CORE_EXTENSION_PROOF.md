# A cyclic-core extension of the degree-three triangle-representation reduction

## Result and limits

Let H be a finite covered loopless linear hypergraph. Its incidence graph B(H) is the bipartite graph with one node for every vertex and one node for every hyperedge, and an adjacency for every incidence. Its graph 2-core is obtained by repeatedly deleting nodes of degree less than two. Degrees in this core are measured in the remaining graph, not in H.

**Theorem.** Suppose the incidence poset of H has dimension at most three. If every surviving vertex-node in the graph 2-core of B(H) has degree at most three, then H has a representation by nondegenerate closed filled rational triangles in the plane whose inclusion-maximal common-intersection subfamilies are exactly its hyperedges.

The condition is vacuous when the 2-core is empty. There is no bound on vertex degrees outside the core, or on degrees contributed by tree branches attached to core vertices. This extends the previously reviewed maximum-vertex-degree-three result. It does not treat a vertex having four incident edges that all remain in the incidence 2-core. No general solution, counterexample, novelty claim, or current literature-status claim is made.

The base case used here is the degree-three corollary in the accepted prior report: the credited convex-representation theorem, witness compression, and finite-nerve inflation give rational nondegenerate triangles when all vertex degrees are at most three. A concurrent investigation supplies a proposed explicit coordinate proof of that convex-representation consequence; the present theorem does not assume its acceptance. The underlying credited sources are de Fraysseix, Ossona de Mendez and Rosenstiehl, *Representation of Planar Hypergraphs by Contacts of Triangles*, LNCS 4875 (2008), pp. 125–136, especially p. 135, and Ossona de Mendez, *Realization of Posets*, JGAA 6(1) (2002), pp. 149–153. [Chapter](https://doi.org/10.1007/978-3-540-77537-9_15); [poset paper](https://jgaa.info/index.php/jgaa/article/view/paper48).

All geometry below concerns unrestricted intersections of filled sets. It does not claim to preserve disjoint interiors or contact representations.

## 1. A private boundary arc is forced by two incident hyperedges

Consider a finite family of nondegenerate compact convex polygons C_v realizing the full nerve of a covered loopless linear hypergraph H. Fix a vertex v incident with at least two different edges. A point is private to v if it belongs to C_v and to no other C_w.

**Lemma 1.** The boundary of C_v contains a private point. For a polygon, a point can be chosen in the relative interior of one of its sides, in an open boundary arc avoiding all other objects.

**Proof.** For each incident edge e define

    R_e = C_v intersect union{C_w : w in e minus {v}}.

These are nonempty compact subsets of C_v: an edge witness belongs to every member indexed by e. They account for every point where C_v meets another object. Indeed, a pair with nonempty intersection must belong to an edge, and linearity makes that edge unique.

The sets R_e for distinct incident edges are disjoint. Otherwise a point lies in C_v, C_w and C_z for w in e minus {v} and z in f minus {v}. Linearity gives w different from z. Full-nerve correctness puts {v,w,z} in an edge g. Uniqueness of the edges containing {v,w} and {v,z} then gives e=g=f, a contradiction.

Suppose the boundary were covered by the R_e. Discard groups whose intersection with the boundary is empty. The remaining intersections are disjoint closed subsets of the connected boundary. A finite disjoint closed cover of a connected space has exactly one nonempty member. Consequently the whole boundary belongs to one group R_e.

Choose a common witness p_e of e. Every C_w with w in e contains p_e. Every x in C_v lies on a segment from p_e to some boundary point y, with the trivial case x=p_e included. Since y belongs to R_e, it lies in C_w for at least one w in e minus {v}; convexity gives x in C_w. Hence all of C_v belongs to R_e. But another incident edge f has a nonempty R_f contained in C_v and disjoint from R_e, a contradiction.

Thus some boundary point is outside the finite compact union of all other objects. An open neighborhood avoids that union. A polygon side-interior point can be chosen in this neighborhood even if the initial private point was a corner. A still smaller neighborhood meets the polygon exactly in the closed half-plane on the inside of that side. This yields the claimed private boundary arc. QED.

The argument does not assert that every edge group touches the boundary. The covering assumption itself forces a single group to cover the boundary; star-shapedness about its common witness then yields the contradiction. Degree one alone does not force a private boundary point: one triangle may be contained in another.

## 2. Exact local construction for adding a pendant hyperedge

A pendant-edge addition means adding one hyperedge

    g = {v,u_1,...,u_k}, k >= 1,

where v is already present and all u_i are new vertices. All other hyperedges and all old representing triangles are unchanged.

**Lemma 2.** If the triangle of v has a private side-interior point, this addition can be realized by nondegenerate triangles. Every new triangle has a private exposed vertex and therefore a private side-interior arc. If the old triangles have rational vertices, the new ones can be chosen rational. All old faces and nonfaces are preserved, and all new faces are exactly the subsets of g containing at least one new vertex.

**Construction.** Take affine coordinates with the private side-interior point at the origin and the old triangle locally in y<=0. Choose a sufficiently small neighborhood that avoids every old triangle other than C_v and within which C_v is exactly the lower closed half-plane. With rational old triangles, choose a rational point on the side and rational coordinate basis, so these affine coordinates and their inverse have rational coefficients.

Choose a sufficiently small positive rational r. Set

    a = (-r/2,-r/2), b = (r/2,-r/2), q = (0,-r/4).

For distinct rational parameters s_i in (-1/4,1/4), set

    t_i = r*(2*s_i/(1+s_i^2), (1-s_i^2)/(1+s_i^2)),
    C_(u_i) = conv{a,b,t_i}.

Choose r small enough that the closed radius-r disk, and hence all these triangles, lies in the private neighborhood. Each t_i is on the radius-r circle, with |(t_i)_x|<r/2 and (t_i)_y>r/2. Thus each triangle is nondegenerate and q is strictly inside it. For example, the horizontal cross-section at q_y has center

    (r/4)*(t_i)_x / ((t_i)_y+r/2)

and half-width

    (r/2)*((t_i)_y+r/4) / ((t_i)_y+r/2),

and the half-width strictly exceeds the absolute center. The point q is also strictly inside the old triangle C_v. Therefore g has a common interior witness.

Every new triangle misses every old triangle other than C_v, by the choice of neighborhood. Any intersecting subfamily involving a new object is consequently contained in g; conversely all subsets of g meet at q. This proves full-nerve correctness, not just pairwise correctness.

The point t_i lies outside C_v because it has positive y coordinate. It is private among the new triangles as well: all their vertices lie in the radius-r disk, and its tangent line at t_i strictly separates t_i from every other new triangle. The two common base vertices lie strictly inside the disk, and the other distinct tips are different points of its strictly convex boundary. All other old triangles miss the entire neighborhood. Compactness gives a neighborhood of t_i avoiding every other object, so a nearby side-interior point is private. Rationality follows directly from the displayed formula and the rational affine coordinates. QED.

This is a coordinated construction: all vertices of a new hyperedge are introduced together. It uses the ability to cross an existing object's private boundary. Putting a new triangle entirely inside its parent would obstruct adding a subsequent descendant edge that must avoid the grandparent; that incorrect shortcut is not used.

**Corollary 2.1.** Starting with a triangle representation, one may attach any finite rooted hypergraph tree by successive pendant-edge additions, provided each initial attachment vertex has a private boundary arc. In particular it is enough that each initial attachment vertex has degree at least two. Newly introduced vertices have their private arcs by Lemma 2, whether or not their current degree is one. Further insertions never destroy an old vertex's private property unless that vertex is the attachment root: new triangles avoid every other old triangle. An attachment root whose degree has increased to at least two has a private arc again by Lemma 1.

## 3. Selecting a degree-three whole-edge backbone

We now prove the theorem's combinatorial reduction. All edges selected below are whole original hyperedges; their members are never truncated. Consequently the incidence poset of the selected hypergraph is an induced subposet of the original incidence poset.

Work component by component in B(H). Standard elementary 2-core properties used here are as follows. Every component outside a nonempty 2-core is a tree and attaches to the core at exactly one node. A cycle outside the core would itself have minimum degree two and would survive pruning. A path joining two core nodes would survive together with the core, so no outside component can have two attachments. Connectivity supplies one attachment. If a connected component has empty 2-core, it is a tree. These observations also show that a nonempty core of a connected component is connected.

In a component with nonempty 2-core, initially select every hyperedge whose edge-node is in the core. Include all vertices of every selected edge, including those whose vertex-nodes were removed in core pruning. Core vertex-nodes have selected degree equal to their core degree, at most three. Every included noncore vertex has selected degree one: two core-edge neighbors would put that vertex in the core.

In a component with empty core, select one arbitrary hyperedge, together with all its vertices. All initial selected vertex degrees are then one.

Perform the following finite procedure. Whenever a selected vertex has selected degree one and has an incident hyperedge not yet selected, select exactly one such edge and include all its vertices. Repeat until no such vertex remains.

Every newly selected edge contains exactly one previously selected vertex. In a tree component this follows from the absence of cycles and the connectedness of the selected subtree. In a component with core it follows from the same fact in each tree attached to the core; a second old vertex would create an outside cycle or a second attachment to the core. Thus the chosen old vertex's selected degree changes from one to two, and all other vertices brought in by that edge are new and have selected degree one. No later step increases an already selected degree-two vertex: the procedure chooses only degree-one roots, and the tree property prevents its being a second old vertex of a later edge.

The resulting whole-edge hypergraph K therefore has maximum vertex degree at most three. Every selected vertex incident with an omitted edge has selected degree at least two, by termination. Terminal selected degree-one vertices have no omitted incident edges, so no private-arc assertion is required for them.

The omitted portion is a disjoint collection of finite incidence trees attached to selected vertex-nodes. It cannot attach at a selected edge-node, since every vertex of that edge was already included. It cannot attach to two selected nodes, by the same outside-tree argument. Reading each omitted tree away from its root reconstructs H through pendant-edge additions: each new edge contains its unique already-present parent vertex and all its other vertices are fresh. This reconstructs the original whole hyperedges, including their sizes, with nothing deleted or identified.

Restricting the incidence poset gives dim P(K)<=3. Apply the reviewed degree-three corollary to represent K by rational nondegenerate triangles. Each root for the omitted trees has degree at least two in K, so Lemma 1 supplies its private arc. Apply Lemma 2 and Corollary 2.1 along all omitted trees. This gives the claimed representation of H. Separate connected components can be translated to pairwise disjoint rational boxes. Empty H is represented by the empty family. QED.

## 4. A connected nonplanar degree-four certificate

The class is not confined to hypergraphs with planar incidence graphs. Start with the chapter's five-vertex example

    a=12, b=23, c=34, d=14, e=135, f=245,

and attach g=16 and h=67. The resulting H has seven vertices, eight edges, and maximum vertex degree four at vertex 1. Its incidence 2-core is the original example, whose vertex degrees are 3,3,3,3,2. Its incidence graph remains nonplanar: it contains the original subdivision of K_(3,3).

Here are three explicit linear extensions of its incidence poset:

    7 6 h 1 g 2 a 3 b 5 e 4 c d f
    7 6 h 1 g 4 d 3 c 5 e 2 a b f
    2 4 5 f 3 b c 1 a d e 6 g 7 h

Their intersection is precisely the incidence order, as verified on all 210 ordered pairs of distinct elements. The restriction to minimal elements 1,2,3 and maximal elements a,b,e is the standard six-element example S3. Its missing-incidence pairs are (1,b),(2,e),(3,a); two of these reversals cannot occur in one linear extension because the two cross-incidences would create a cycle. Thus the dimension is exactly three.

An explicit rational triangle representation is also checked. For the five previously reviewed segments

    1: [(0,-2),(0,4)], 2: [(0,4),(4,0)], 3: [(0,0),(4,0)],
    4: [(0,-2),(4,2)], 5: [(0,0),(3,1)],

replace [a,b] by the triangle with vertices

    a-eta*(b-a)-eta*J(b-a), a-eta*(b-a)+eta*J(b-a), b+eta*(b-a),

where eta=1/1000 and J is counterclockwise quarter-turn. Add

    C6 = conv{(0,99/100),(0,101/100),(3/100,1)},
    C7 = conv{(29/1000,9999/10000),(29/1000,10001/10000),(3/50,1)}.

The exact checker tests all 127 nonempty subfamilies and finds precisely the eight asserted maximal edges. In particular C7 misses C1, so the two-level attachment does not accidentally create a grandparent incidence. All objects are nondegenerate rational triangles. This example is an explicit certificate of the degree-four extension, not a geometric obstruction or a new claim about the source's original example.

## 5. A connected nonplanar family with unbounded degree

The dimension hypothesis is verified uniformly for a larger family, rather than assumed to survive arbitrary tree attachment. Start with the same five-vertex core. Add a new vertex z, an edge g={1,z}, and, for any integer k>=0, new vertices u_0,...,u_k and edges h_i={z,u_i}. The 2-core stays the original nonplanar core. Vertex 1 has degree four, while z has degree k+2, which is unbounded.

Write

    R1 = 2 a 3 b 5 e 4 c d f,
    R2 = 4 d 3 c 5 e 2 a b f,
    L3 = 2 4 5 f 3 b c 1 a d e.

A uniform three-order realizer is

    u_k ... u_0 z h_k ... h_0 1 g R1;
    u_0 z h_0 u_k h_k ... u_1 h_1 1 g R2;
    L3 z g u_1 h_1 ... u_k h_k u_0 h_0.

When k=0 the blocks indexed 1,...,k are empty. These specialize to the previous seven-vertex certificate after renaming z=6 and u_0=7.

Here is a direct verification by pair types. The old restrictions are the accepted core realizer. Each u_i precedes its h_i in all three orders; z precedes every h_i and g; and 1 precedes g. Every new element precedes every old core element except where its forced incidence with 1 intervenes, in at least one of the first two orders; the third order puts all old elements before z, g, u_i and h_i. Specifically g is after 1 but before every other old vertex and every old edge in the first two orders, whereas it is after the whole core in the third. This gives exactly its required old incidence and reverses all other old/new incomparable pairs. The vertex z and all u_i,h_i precede the entire old core in the first order and follow it in the third, giving their remaining cross-block incomparabilities.

Among the star elements, u_0 precedes z in the first two orders and follows it in the third. Each u_i for i>=1 precedes z in the first order and follows it in the second and third. For i,j>=1, distinct leaves and distinct edge nodes are in descending index order in the first two orders and ascending index order in the third. An incomparable u_i,h_j with 1<=i<j is reversed by the second order's h_j<u_i, while for 1<=j<i the third order has h_j<u_i; the first order always has u_i<h_j. For i>=1 the second order has h_0<u_i and the first has u_i<h_0; the third has h_i<u_0 and the first has u_0<h_i. Pairs involving u_0 and another leaf, or h_0 and another edge node, are reversed between the first and second orders. Finally g precedes all star leaves and h_i in the third order and follows all of them in the first two. These cases exhaust all distinct pairs. Thus the orders realize the incidence poset.

The original S3 remains an induced subposet, so every family member has dimension exactly three. The theorem therefore gives rational triangle representations for this connected nonplanar family with arbitrarily high vertex degree. This is a concrete nontrivial class covered by the sufficient condition; it is not a claim that arbitrary pendant attachment preserves incidence dimension three. The private checker independently verifies the orders for k=0,...,20 as finite regressions, while the displayed pair-type argument proves all k.

## 6. Verification boundary and remaining problem

The private checker uses rational half-plane intersections. Each tested intersection is bounded. If nonempty, it has a vertex, possibly a degenerate isolated point, at two independent active boundary lines; enumerating line intersections and checking every inequality therefore decides these finite intersection tests exactly. Every acceptance gate is an explicit exception, not a Python assertion. Diagnostics are sorted and are required to agree byte for byte under normal Python, -O and -OO. Negative controls genuinely alter geometry, an edge, or a realizer and require rejection; no timeout is accepted as mathematical evidence.

Finite regressions additionally exercise the whole-edge backbone procedure on an empty core, a single edge, a disconnected forest-plus-nonplanar-core example, a branch beginning at a vertex of a core edge, a deep branch, and a degree-four cyclic core. The last is deliberately outside the sufficient theorem and is not mistaken for a covered case. These regressions supplement the general proof; they do not replace it.

The theorem isolates a sharper unresolved frontier: degree four arising entirely within the incidence 2-core. The pendant insertion works because a new hyperedge has one old vertex and all other vertices are fresh. At a cyclic-core edge, several vertices already carry constraints elsewhere; the construction cannot connect them using disjoint private neighborhoods. Neither a private boundary arc nor the earlier fixed-neighbor obstruction settles that coordinated problem.
