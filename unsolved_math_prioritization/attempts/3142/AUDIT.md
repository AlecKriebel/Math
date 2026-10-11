# Independent audit of the explicit fractional-coloring family

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The complete written proof and the complete 96-entry numerical coloring table are retained. The table, the XOR graph definition, and the four proved constraints make the positive eight-color certificate independently checkable by hand. This is not an executable computational reproduction package: code, raw exhaustive computation records and search outputs, copied source documents and images, and private coordination material are omitted. The historical exhaustive checks are reported as authenticated supporting metadata; their original executions are not rerun or supplied as an executable replay. The all-positive-t theorem and the lower bounds rest on the written arguments, not finite testing or failed searches.

The general 2 Delta + 1 conjecture remains unresolved by this work. No novelty, priority, exhaustive literature-survey, or current-openness claim is made.

The source inspection, independent checker executions and controls described below are historical audit actions. Editorial preparation authenticates their saved metadata without rerunning the mathematics or retrieving or inspecting additional scholarly sources.

## Verdict

ACCEPT the restricted mathematical theorem and its stated limitations. No mathematical correction is required.

For each positive integer t, the specified cyclic lift H_t is a connected, nonbipartite, simple, 5-regular graph with 16t vertices, and the third power of its third subdivision has chromatic number exactly 8. The singleton-incoming coloring parameter is 16 for the base and lies between 15 and 16 for every lift. These facts obstruct the singleton-incoming shortcut to the bound 2 Delta + 1; they do not refute that bound or resolve it for arbitrary graphs.

This audit certifies mathematical correctness within that scope. It does not certify novelty, current literature completeness, peer review, a proof-assistant derivation, or the truth of every theorem in the cited article.

## Authenticated input and independence

The input manifest has 6,057 bytes and SHA-256:

924d77c72f9cc74ee25142039c63ee616855ca3fe9c792cb5de50f42bafe4c5d

Its exact 25-member inventory, byte lengths, member hashes, listed directories, and external seal match. No symlinks were found. The complete original proof report was read; its digest is 4a1c1b01773f78ebc2f21062b55b506ce4aa5b4f0de611d0009bc11fb2ee259b. The complete original 96-entry table is reproduced without changes in PROOF.md of this edition.

No candidate search, verifier, seal-checking, or author program was read as source, imported, or executed. Hashing program files as opaque bytes does not execute them. A new standard-library checker was written directly from the mathematical definitions. It uses three rounds of Boolean neighbor-union reachability on an explicitly constructed subdivision, independently of the candidate's stated BFS/Floyd-Warshall implementations.

The checker parses the complete table from the authored report, independently reconstructs all labels, and establishes exact agreement with the positive eight-color JSON certificate. The unsuccessful DSATUR search and heuristic search history are not used to establish any lower bound. Their timing, pruning implementation, and historical execution are outside this audit.

## Source convention

The original public article and Open Problem Garden statement agree: subdivide every original edge into a path with exactly three edges, then join distinct subdivision vertices whose distance is at most three. The fraction is not canceled. The article assumes finite simple undirected graphs. The article's incidence identification agrees with the ordered internal vertices used here. Physical PDF pages 4, 5, and 9 were independently rendered and visually inspected; these contain the fractional-power definition, target, and incoming-color lemma. Additional source sections were read as recorded in SOURCES.json.

Sources:

- Mahsa Mozafari-Nia and Moharram Nejad Iradmusa, *Simultaneous coloring of vertices and incidences of graphs*, Australasian Journal of Combinatorics 85(3) (2023), 287-307: https://ajc.maths.uq.edu.au/pdf/85/ajc_v85_p287.pdf
- Open Problem Garden, *Chromatic number of frac 3/3 power of graph*: https://www.openproblemgarden.org/op/chromatic_number_of_frac_3_3_power_of_graph

The source PDF is authenticated within the candidate, at 206,557 bytes and SHA-256 8e451dea4019d228123844b8ad901a8c969d690c055b24aad3a958fe1d81dfc6. Public web openings independently confirmed the source identity and definitions; they did not yield a new byte-for-byte PDF retrieval comparison. The retained retrieval receipt is prior provenance, not a claim that this reviewer performed that retrieval.

## 1. Reconstructing all constraints

Write the subdivided edge as u--(u,v)--(v,u)--v. Its two ordered internal vertices are distinct.

Two terminals are at subdivision distance at most three precisely when they were adjacent in the original simple graph. A terminal and an internal vertex are at distance at most three precisely when the terminal is an endpoint of the internal vertex's original edge. A terminal on a different original edge must traverse at least one complete three-edge replacement plus at least one more edge, giving distance at least four.

For two internal vertices on distinct original edges, an available route of length at most three must pass through their common original endpoint. Distances through that endpoint are two when both internal vertices are near it, three when exactly one is near it, and four when both are far. A route using an additional complete original edge has length at least 1 + 3 + 1 = 5. Opposite internal vertices on the same original edge are adjacent. Consequently, distinct arcs (u,v) and (w,z) conflict exactly when u = w, v = w, or z = u.

These statements prove, in both directions, the four coloring constraints: adjacent terminals differ; a terminal differs from every incoming and outgoing color; outgoing colors at a vertex are pairwise distinct; and outgoing and incoming color sets at a vertex are disjoint. Incoming arcs with a common head do not thereby conflict. Omitting either endpoint's terminal constraint would change the problem.

The independently constructed 96-vertex base subdivision has 720 third-power edges. All 4,560 unordered vertex pairs agree with the criterion, and all 720 coloring inequalities are satisfied. The certificate uses all eight colors. As a further implementation check, the distance/criterion equality holds for all 1,099 labeled simple graphs of orders one through five, covering 115,851 subdivision vertex pairs. This is a finite test of the checker, not a substitute for the preceding general argument.

## 2. Base geometry and seven-color impossibility

The base vertices are four-bit vectors, with adjacency when their difference is one of the four unit vectors or the all-one vector. Nonzero differences and distinct generators imply simplicity and degree five; therefore there are 40 edges. The unit vectors generate all vertices, giving connectivity. The sequence 0,1,3,7,15,0 is a five-cycle.

A sum of two distinct generators is never a generator. The six pairs of unit vectors give the six weight-two vectors, and the four pairs involving the all-one vector give the four weight-three vectors. Each nonzero nongenerator is therefore obtained from exactly one unordered generator pair. For a nonadjacent pair x,y, ordering that pair in its two ways produces exactly two distinct common neighbors. Thus the base has diameter two, and its square is K16. Removing vertex 0 leaves at least one of those common neighbors for each nonadjacent remaining pair, so the square of the vertex-deleted base is K15.

Now suppose a d-regular graph has a coloring of its subdivided cube using at most d+2 colors. At any vertex u, its terminal and d outgoing internal vertices form a clique of size d+1. Every incoming internal vertex is adjacent to that entire clique. Since d is positive, the incoming set is nonempty and can use only the single remaining color; write it as h(u). If fewer than d+2 colors were actually available, the coloring would already be impossible.

For adjacent u,v, the two opposite arcs have colors h(v) and h(u), so these differ. For distinct u,v sharing a neighbor w, the outgoing arcs (w,u) and (w,v) have colors h(u) and h(v), so these also differ. Hence h properly colors the square using at most d+2 colors. Applying this with d=5 contradicts K16 for the base. The verified eight-color table therefore gives equality, not merely an upper bound.

This reasoning reproduces the needed incoming-color mechanism directly. It does not rely on a failed seven-color search, an uninspected reduction, or a conjecture in the source article.

## 3. Exact singleton-incoming result on the base

If singleton incoming sets are imposed directly, the same map h colors the square without any restriction on palette size. The base consequently needs at least 16 colors in that model.

For a matching upper bound, color arc (u,v) by the vertex label v and terminal v by v XOR 3. The incoming set at v is exactly {v}; the outgoing colors are the distinct neighbors of v. The vector 3 is nonzero and has weight two, so the terminal color is neither v nor a neighbor of v. Translation by 3 is injective and keeps adjacent terminal colors distinct. All four constraints hold, proving the exact singleton value 16. The independent distance checker also checks every inequality of this construction.

The eight-color witness has one incoming color at vertex 0 and two at every other base vertex. Thus the obstruction does not apply to unrestricted incoming sets or even to the two-incoming-color model.

## 4. Pullback lemma

Let f from H to G be a graph homomorphism injective on each neighborhood, with G loopless. Assign to a terminal x its base terminal color at f(x), and to arc (x,y) the base arc color at (f(x),f(y)). Adjacent terminals map to adjacent terminals; each arc remains incident to both projected endpoints. Distinct outgoing arcs remain distinct by neighborhood injectivity. Consecutive arcs remain consecutive; they cannot become the same ordered arc because that would force the images of adjacent vertices to coincide. The four constraints therefore survive.

Local injectivity is necessary for this argument: the homomorphism collapsing both leaves of a two-leaf star onto one endpoint of an edge identifies its outgoing arcs. A checker negative control confirms that pulling a proper coloring back along this map is not proper. The report correctly states the necessary hypothesis.

## 5. Every cyclic lift, including t = 1 and t = 2

For each base edge other than {0,2}, connect corresponding vertices inside each layer. For {0,2}, use (0,i)--(2,i+1), with indices modulo t.

Every base edge supplies a matching between its two different endpoint fibers. Edges from different base edges cannot coincide, and no endpoint labels coincide, so loops and repeated undirected edges are impossible. At t=1 this is exactly the base. At t=2 the two twisted edges join different pairs, namely (0,0)--(2,1) and (0,1)--(2,0); they do not become duplicate undirected edges. Every vertex has one neighbor over each of its five base neighbors. Projection is locally bijective, and the graph has 16t vertices and 40t edges.

The unit-vector cube is connected. The deleted edge 0--2 has replacement path 0--1--3--2 using other cube edges, so deleting it does not disconnect the cube. Therefore all untwisted edges connect every individual layer. The twisted edges connect consecutive layers around the cyclic index set, proving connectivity for every t. The five-cycle 0,1,3,7,15,0 uses no twisted edge and survives within every layer, proving nonbipartiteness for every t.

Projection and the pullback lemma provide eight colors. For a lower bound, the fifteen vertices with nonzero base labels in any fixed layer induce the vertex-deleted base. Every pair is joined within that layer by a path of length at most two. Hence the square of H_t contains K15, irrespective of any extra shorter paths through other layers. A seven-coloring of its subdivided cube would force a seven-coloring of that square by the regular-graph argument, which is impossible. Therefore the exact value is eight for every positive t.

The same K15 forces at least 15 colors under the singleton restriction. Pulling back the 16-color construction keeps every incoming set singleton and supplies the upper bound 16. The report correctly leaves the exact singleton value for t>1 undetermined.

## 6. Independent computation and controls

Normal, -O, and -OO executions all pass and produce byte-identical JSON results. No correctness check depends on Python assertions.

For t=1,2,...,17 and t=31, the independent checker validates:

- exact vertex/edge counts, simplicity, degree five, connectivity, and nonbipartiteness;
- local bijectivity of the projection;
- an untwisted five-cycle and square K15 in every layer;
- agreement between actual subdivision distances and all stated constraints;
- the eight-color pullback and the singleton 16-color pullback.

Across those eighteen specified graphs, each run checks 12,644,736 unordered subdivision pairs and 132,480 distance-three power edges for each of the two colorings. These finite instances corroborate implementation; the argument above is the all-t proof.

Each mode rejects thirteen deliberately incorrect controls: adjacent equal colors; a truncated vector; an undersized palette; cancellation of the fraction; omission of terminal constraints; reversal of every arc color; replacement of the subdivision cube by its square; changed, missing, or additional manifest members; changed manifest bytes; an additional empty directory; and removal of local injectivity in the star-to-edge example.

The complete numerical coloring table is retained in PROOF.md. Raw exhaustive computation records and search outputs, executable code, copied scholarly source content and images, and private coordination material are omitted from this edition. The preceding execution and control claims report the historical independent audit; no mathematical computation was rerun during editorial preparation.

## Remaining limits

The proof settles the explicitly constructed infinite family and the stated pullback upper-bound class. It supplies no locally injective homomorphism into the base for an arbitrary graph, does not prove the target for all 5-regular graphs, and does not improve the general bound. The base and every lift satisfy the target comfortably, since eight is below eleven. The correct overall outcome for the original unrestricted problem remains PARTIAL.
