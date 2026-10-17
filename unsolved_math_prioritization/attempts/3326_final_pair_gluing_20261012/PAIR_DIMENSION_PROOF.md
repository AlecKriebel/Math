# Two-parent edge amalgams with incidence dimension exactly three

## Result and scope

Let F have vertices 1,2,3,4,5 and maximal hyperedges

    a=12, b=23, c=34, d=14, e=135, f=245.

For k>=1, form A_k from k copies of F by identifying every copy of vertex 1, every copy of vertex 2, and the shared edge a=12. The remaining vertices of block i are 3_i,4_i,5_i, for 0<=i<k; its other edges are b_i,c_i,d_i,e_i,f_i with their original incidences. This is a genuine two-parent amalgam: two old vertices and their whole common edge are shared.

**Theorem 1.** For every k>=1, the incidence poset of A_k has dimension exactly three. The hypergraph has 3k+2 vertices and 5k+1 edges. Both shared vertices have degree 2k+1. Its incidence graph is nonplanar, 2-connected, and equal to its entire 2-core.

There is also a uniform ear extension. Adjoin t>=0 new vertices z_j to A_k and edges x_j={1,z_j}, y_j={2,z_j}, retaining a. Denote the result A_{k,t}. An ear has two distinct parents 1 and 2.

**Theorem 2.** For all k,t>=0 with k+t>=1, A_{k,t} has incidence dimension exactly three. Its counts are

    |V|=3k+t+2, |E|=5k+2t+1,
    deg(1)=deg(2)=2k+t+1,
    number of strict incidences=12k+4t+2.

Its incidence graph is 2-connected and has minimum degree at least two. If k>=1, it is nonplanar. In particular A_{1,1} has six vertices, eight edges, and both parent degrees four inside a 2-connected cyclic incidence core.

These are incidence-order statements. No geometric fact is used to infer their incidence dimension; a triangle-representation result requires its own separate proof. This report does not claim that arbitrary two-vertex identification preserves dimension three, nor that every dimension-three hypergraph admits the particular rooted order patterns below. The general triangle-representation conjecture remains unresolved here. There is no literature-novelty claim.

## 1. Exact certificate criterion and all pair types

For a finite covered clutter H, suppose vertex permutations P_1,...,P_d satisfy:

(V) Each ordered pair of distinct vertices occurs in its indicated order in at least one P_j.

(M) For every edge h and excluded vertex v, some P_j places every member of h before v.

Expand each P_j to a total order L_j of vertices and edges by putting each edge immediately after its last member, before the next vertex. Several edges with the same last member may be put in any fixed order. The following checks prove that these total orders realize the incidence poset.

* Every incident vertex precedes its edge in every expanded order.
* For distinct vertices, (V) gives both orientations.
* For a nonincident vertex v and edge h, (M) gives h<v somewhere. Choose any member w of h. By (V), some order has v<w<h, giving the other orientation.
* For distinct edges h,g, the clutter condition gives u in h\g and w in g\h. Condition (M) for (g,u) gives g<u<h; for (h,w), it gives h<w<g. Thus both edge orientations occur.

These cases exhaust every ordered pair of distinct incidence elements. Simultaneous insertion cannot invalidate an edge comparison witnessed through a vertex strictly between the edges.

Conversely, restriction of any incidence realizer to the vertices satisfies (V) and (M). For (M), an order reversing the incomparable pair h,v must put every member of h before h before v. Thus the criterion is equivalent for covered clutters. Every hypergraph used here is finite, covered, loopless, and linear; looplessness and linearity imply the clutter condition.

## 2. A sufficient three-order compatibility theorem

Consider finitely many covered linear hypergraphs H_i whose pairwise common vertices are exactly r,s. In each piece the pair {r,s} is an edge. All remaining vertices and all other edges are disjoint between pieces. Suppose each piece has three vertex permutations satisfying (V) and (M) and having the forms

    r s A_i
    r B_i s
    s C_i r,

where A_i,B_i,C_i are permutations of its nonroot vertices. Because of linearity, no other edge contains both r and s. In the union retain only one copy of the common pair edge.

The following three vertex orders satisfy the criterion:

    r s A_0 A_1 ... A_(q-1)
    r B_(q-1) ... B_1 B_0 s
    s C_(q-1) ... C_1 C_0 r.

Here q is the number of pieces. To prove this, first note that restriction to one piece is exactly its local certificate. Consequently all vertex pairs belonging to one piece, root/nonroot vertex pairs, missing incidences within a piece, and missing incidences between the common edge and a nonroot vertex already have their witnesses. The common edge specifically precedes every nonroot vertex in the first order.

For vertices from different pieces, the first and second orders have opposite piece directions, giving (V). It remains to check (M) for a noncommon edge h of piece i and a nonroot vertex v of piece j!=i.

* If h contains r, it does not contain s. Root r is before all nonroots in both the first and second orders. Their opposite piece directions put all members of h before v in at least one.
* If h contains s, use the first and third orders in the same way.
* If h contains neither root, the first and second orders suffice.

If the excluded vertex is a root, it belongs to the local piece and is already handled by the local certificate. This covers every missing incidence, so Section 1 proves a three-order realizer. No unconditional edge-gluing theorem is being assumed.

The proof also allows different kinds of compatible pieces in any fixed order. Its hypotheses can be checked locally; the global orders are explicit.

## 3. The local source block and uniform formulas

The following vertex permutations certify the required compatibility of F:

    1 2 3 5 4
    1 4 3 5 2
    2 4 5 3 1.

Every pair of nonroot vertices has both orientations: 3 precedes 4 in the first order and follows it in the other two; 3 precedes 5 in the first two and follows it in the third; 5 precedes 4 in the first and follows it in the other two. Vertex 1 precedes all others in the first two and follows them in the third. Vertex 2 is before every nonroot in the first and third and after them in the second; the pair 1,2 also occurs both ways.

The complete missing-incidence witness list is below. Order numbers are one-based.

    a before 3,4,5: order 1
    b before 1: order 3; b before 4,5: order 1
    c before 1: order 3; c before 2,5: order 2
    d before 2,3,5: order 2
    e before 2: order 2; e before 4: order 1
    f before 1,3: order 3.

There are exactly sixteen missing incidences in this list: 3+3+3+3+2+2=16, which is five vertices times six edges minus fourteen incidences. Each statement follows by reading the displayed permutations. No search result is needed.

Their expanded local incidence orders are:

    1 2 a 3 b 5 e 4 c d f
    1 4 d 3 c 5 e 2 a b f
    2 4 5 f 3 b c 1 a d e.

Apply Section 2 with r=1,s=2. For A_k the resulting vertex formulas are:

    P1 = 1,2; then (3_i,5_i,4_i) for i increasing
    P2 = 1; then (4_i,3_i,5_i) for i decreasing; then 2
    P3 = 2; then (4_i,5_i,3_i) for i decreasing; then 1.

Canonical edge expansion gives the promised full three-order realizer for every k. The explicit k=2 orders are:

    1 2 a 3_0 b_0 5_0 e_0 4_0 c_0 d_0 f_0 3_1 b_1 5_1 e_1 4_1 c_1 d_1 f_1
    1 4_1 d_1 3_1 c_1 5_1 e_1 4_0 d_0 3_0 c_0 5_0 e_0 2 a b_0 b_1 f_0 f_1
    2 4_1 5_1 f_1 3_1 b_1 c_1 4_0 5_0 f_0 3_0 b_0 c_0 1 a d_0 d_1 e_0 e_1.

They contain all nineteen elements. Their intersection is independently checked against all 342 ordered distinct pairs, with exactly 26 strict incidences. The k=3 raw fixture has 27 elements, 702 ordered pairs, and 38 strict incidences. Machine-readable fixtures include the complete vertex and full orders plus a witnessing order for every ordered vertex pair and every missing incidence.

## 4. Two-root ears and the exact lower bound

An ear piece has vertices 1,2,z and pair edges a=12, x=1z, y=2z. Its compatible vertex orders are

    1 2 z
    1 z 2
    2 z 1.

Every vertex pair occurs both ways. The only missing incidences are a<z in the first order, x<2 in the second, and y<1 in the third. Thus Section 2 applies to any mixture of F pieces and ear pieces. For A_{k,t}, take the k F pieces first, followed by the t single-vertex ear pieces, in the same concatenation rule. This proves the upper bound three in Theorem 2. In particular the t ears occur in increasing index order in P1 and decreasing order in both P2 and P3.

If k>=1, restrict the incidence poset to vertices 1,2,3_0 and edges a,b_0,e_0. This is the standard example S3: each of its three maximal elements is above exactly two of its three minimal elements. Its three absent incidences are a<3_0, b_0<1, and e_0<2. No linear extension can reverse two of them, because the corresponding two cross-incidences would give a directed cycle. Therefore every realizer needs at least three orders.

If k=0 and t>=1, the first ear on 1,2,z_0 and a,x_0,y_0 is itself S3, with the same lower-bound argument. Together with the uniform upper bound, this proves dimension exactly three in every stated case. The excluded case k=t=0 is just two incomparable vertices below their common edge and has dimension two.

## 5. Hypergraph conditions and graph structure

The inventory formulas follow by sharing two vertices and the pair edge across all pieces. An F piece contributes three fresh vertices, five fresh edges, two new incidences to each root, and twelve strict incidences overall. An ear contributes one fresh vertex, two fresh edges, one new incidence to each root, and four strict incidences. The common pair contributes one edge and two incidences. All edges have size two or three, every vertex is covered, and two distinct edges meet in at most one vertex. In particular edges from different pieces can meet only at one of the two roots; no noncommon edge contains both roots.

The incidence graph of F is a subdivision of K3,3 with branch parts {1,3,f} and {2,4,e}. Its nine internally disjoint paths are

    1-a-2, 1-d-4, 1-e;
    3-b-2, 3-c-4, 3-e;
    f-2, f-4, f-5-e.

These paths use every vertex and edge-node of the incidence graph. Thus the graph is nonplanar and 2-connected. Each ear piece has incidence graph equal to the six-cycle 1-a-2-y-z-x-1, which is 2-connected as well.

All piece graphs share the path 1-a-2. Delete any one node of their union. Each individual piece minus that node, if present there, remains connected. At least two of the three common path nodes remain, so all remaining piece graphs still have a common node. Their union after deletion is therefore connected. The original union is connected and has at least three nodes, so it is 2-connected. This proves the assertion for all k,t in the theorem, without extrapolating finite graph tests.

All incidence nodes have degree at least two: the common edge and pair edges have degree two, triple edges degree three, F nonroots degree two or three, ear vertices degree two, and roots degree at least two. Iterative deletion of nodes of degree below two therefore deletes nothing; the whole incidence graph is its 2-core. For k>=1 the union contains an unchanged copy of the displayed K3,3 subdivision, so it is nonplanar. The unbounded degrees of both roots are genuinely inside a 2-connected cyclic graph.

## 6. Verification and source credit

The dependency-free verifier checks the vertex criterion and intersects full total orders with integer suffix bitsets. It explicitly compares the result for every ordered distinct incidence-element pair, including all four vertex/edge type combinations. A separate direct-rank implementation replays the raw full-order fixtures without relying on the expansion proof. The uniform test range includes all k=1,...,40, then 64 and 100, as well as ear-only, one-block-plus-ears, and mixed examples. The universal claims follow from Sections 1-5, not from those finite tests. The k=100 pure pair example checks 644,006 ordered pairs on 803 elements.

All checks use explicit exceptions and work identically with normal Python, -O, and -OO. The controls actually corrupt an incidence orientation, remove an incidence element, remove the third order, erase either required reverse piece direction, and corrupt a local permutation. Each must reach its specific mathematical rejection. Separate source-mutation replays also check that disabled verification gates cannot pass the control harness. Private discovery searches are preserved but not used as proof, and every retained solver-produced order is independently checked exactly.

The block F, its previously known dimension-three status, and the nonplanar incidence example come from H. de Fraysseix, P. Ossona de Mendez and P. Rosenstiehl, *Representation of Planar Hypergraphs by Contacts of Triangles*, Graph Drawing 2007, LNCS 4875 (2008), pp. 125-136, printed p. 135. DOI: https://doi.org/10.1007/978-3-540-77537-9_15 . Publisher PDF: https://link.springer.com/content/pdf/10.1007/978-3-540-77537-9_15.pdf . The source's base example is credited, not claimed as new. The compatible local permutations, exact amalgam certificates, and proofs above are supplied here, with no assertion of literature priority.

This report makes no inference from a failed solver run, no geometric impossibility claim, and no claim of resolving the general conjecture. It isolates an explicit sufficient rooted-order condition and proves it for a genuinely two-parent, unbounded-degree, nonplanar, 2-connected family.
