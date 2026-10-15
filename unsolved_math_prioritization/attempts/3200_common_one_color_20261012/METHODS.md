# Common-color matching reduction: exact scope and independent checks

## 1. Result and scope

Let G be a finite simple graph with maximum degree at most three. Assume G is not three-edge-colorable but G-e is three-edge-colorable for every edge e. Let L assign an exact three-element color list to every edge.

This supplementary note proves the exact matching-selection criterion below, supplies a short critical-cycle construction, and independently corroborates the resulting theorem:

**Theorem.** If the total intersection of the edge lists is nonempty, then G is L-edge-colorable if and only if L is nonconstant.

The proof is symbolic; the finite checks are corroboration, not hypotheses. The total palette and number of exceptional edges are unrestricted. The empty-total-intersection case is not settled here. No priority or historical-novelty claim is made.

Two explicit critical-graph examples delimit the method: arbitrary degree-three-covering matchings need not leave just one odd cycle, and even a matching leaving one odd cycle can fail for a particular nonconstant list assignment. Both limitations are compatible with the theorem, which selects a suitable matching.

## 2. Exact fixed-matching criterion

Fix a common color c and write B(e)=L(e) minus {c}; each B(e) has two elements. Let M be a matching. The following are equivalent:

1. M covers every vertex of degree three in G.
2. G-M has maximum degree at most two.

Indeed, deleting a matching reduces each vertex degree by at most one. A degree-three vertex must lose one incident edge, while all other vertices already have degree at most two.

For such a matching M, the strategy of coloring every edge of M with c and every edge outside M from its reduced list B succeeds **if and only if no odd-cycle component of G-M has a constant B-list assignment**.

To prove this, every nontrivial component of G-M is a path or cycle. Paths are greedily edge-colorable from two-element lists. A cycle with nonconstant two-element lists is also colorable: order its edges h1,...,hk so that B(h1) differs from B(hk); put on h1 a color in B(h1) minus B(hk), then color successively while avoiding the previous color. The last edge automatically avoids the first color. Constant two-element lists color a cycle exactly when its length is even. Components are independent, and none of their colors is c, so they do not conflict with M.

This is a criterion for the stated fixed-M strategy. It does not assert that every full list coloring has a common-color class covering every degree-three vertex, or that failure for one M implies failure of the assignment.

## 3. A critical-cycle matching through any specified edge

**Lemma.** For any edge e and any proper three-edge-coloring phi of G-e, there is a color class M of phi that covers all original degree-three vertices. Its complement G-M has exactly one odd cycle C, and C contains e.

**Proof.** At a degree-three endpoint of e, precisely two labels occur under phi, so exactly one of the three labels is excluded from the choice of a covering color class. There are at most two such endpoints. Choose a label gamma that occurs at each degree-three endpoint; at least one choice exists. Every other degree-three vertex sees all three labels. Therefore M=phi inverse(gamma) is a matching covering every degree-three vertex. Endpoints of degree at most two require no coverage.

The graph G-M has maximum degree at most two. After deleting e, phi uses only the other two labels on its remaining edges. Thus any odd cycle in G-M contains e, so at most one exists. If none existed, all components of G-M could be two-edge-colored, and coloring M with gamma would three-edge-color G, a contradiction. Hence there is exactly one odd cycle and it contains e. QED.

This proof needs no Kempe-chain assertion or perfect-matching theorem. It also proves the statement for every ordinary deletion coloring and every label satisfying the coverage condition.

## 4. Local overlap and family connectivity

Criticality implies that all edges lie in one connected component: an uncolorable component would persist after deleting an edge from any other edge-containing component. Consequently a nonconstant edge assignment has two incident edges with different values.

Choose incident edges e,f with B(e) different from B(f), and apply Section 3 to obtain cycles Ce,Cf. At their common endpoint each cycle uses two of at most three incident edges. They therefore share an incident edge g. The two cycles cannot both have constant B-lists, since then B(e)=B(g)=B(f). At least one has nonconstant reduced lists.

Apply the fixed-matching criterion to that cycle's matching. Every other component is a path or even cycle, and the unique odd cycle is nonconstant. This proves sufficiency of nonconstancy. A constant three-list assignment would give an ordinary three-edge-coloring, proving necessity of nonconstancy.

For completeness, there is a valid global connectivity statement. Consider the family of all unique odd cycles arising as complements of degree-three-covering matchings with exactly one odd-cycle component. This family covers every edge by Section 3, and its edge-intersection graph is connected. To see this, choose one cycle Ce through each edge e using Section 3. Whenever e,f are incident, Ce,Cf share an edge by the local overlap argument. The line graph of the edge-containing component is connected, so this selected family is connected under edge intersection. Any additional family member contains some edge e and meets Ce there. This argument proves connectivity, not pairwise intersection of all cycles.

The construction of a list coloring uses ordinary deletion colorings for at most two incident edges. This does not claim an efficient algorithm for obtaining the ordinary deletion colorings from an arbitrary graph representation.

## 5. An actual critical graph with three odd cycles after another matching

The following construction gives a 25-vertex, 37-edge finite simple critical graph and a matching covering all 24 degree-three vertices whose complement consists of cycles of lengths 3,3,19.

A compact deterministic construction is as follows. Start with the nine-vertex graph having edge set

    02, 13, 14, 23, 24, 34, 06, 57, 58, 67, 68, 78, 15.

Keep vertex 0. For each vertex v in {1,...,8}, replace v by a triangle whose three vertices are ports p(v,w), one for each neighbor w. Replace each original edge vw by p(v,w)p(w,v), with p(0,w)=0. The generator labels ports consecutively in increasing v and then increasing w.

For the path 2,3,1,5,7,6 in the base graph, take every external edge between triangle blocks except its five path edges. In each of the six path blocks, also take the internal edge joining its predecessor and successor ports; at the two ends use the port toward 0. These twelve edges form the specified matching. Direct decomposition gives residual cycles of lengths 3,3,19.

The graph is not three-edge-colorable because each color class has at most floor(25/2)=12 edges, whereas there are 37 edges. Every one of its 37 single-edge deletions has an explicit proper ordinary three-coloring in the original checked certificate collection. All these certificates are directly checked; the raw certificate collection is not distributed in this prose edition. Thus this is an actual critical graph, not merely an arbitrary support or boundary signature.

The example disproves the stronger assertion that **every** degree-three-covering matching leaves exactly one odd cycle. It does not conflict with Section 3, which constructs a special matching from a deletion coloring. The complete deletion-color-class scan for this graph finds four critical triangles and four critical Hamilton cycles. Distinct triangles are edge-disjoint, while the full family remains connected under edge intersection.

## 6. Exactly one common color: one matching fails, another succeeds

Use the critical seven-edge graph with ordered edges

    e0=01, e1=02, e2=13, e3=14, e4=23, e5=24, e6=34.

Assign {0,1,2} to every edge except L(e2)={0,1,3} and L(e5)={0,2,3}. The total intersection is exactly {0}.

There are precisely two matchings covering the degree-three vertices:

- Mbad={e2,e5}. Its residual five-cycle has the constant reduced list {1,2}, so the fixed-Mbad strategy fails.
- Mgood={e3,e4}. The full coloring (2,1,1,0,0,3,2), in the displayed edge order, respects every list and is proper. Its zero-color class is exactly Mgood.

This is an explicit failure of arbitrary matching selection in a critical graph and a four-color palette. It is not an uncolorable list assignment.

The exact finite census for this graph uses all three list types containing 0 in the palette {0,1,2,3}, independently on each edge. Among the 3^7=2,187 assignments:

- 3 assignments have no successful covering matching; they are exactly the constant assignments.
- 48 assignments have exactly one successful covering matching.
- 2,136 assignments have both matchings successful.

For all 4,374 assignment/matching pairs, an exhaustive direct list-coloring solver agrees with the criterion in Section 2.

## 7. Complete bounded checks and certificate provenance

Seven actual critical fixtures were used: the seven-edge graph; four ten-edge graphs on seven vertices; Petersen-minus-one-vertex on nine vertices and twelve edges; and the new 25-vertex graph above. The first six came from the preceding exact graph-search fixtures. Their complete edge sets were copied into the original packet, which therefore had no execution dependency on prior folders. Those raw fixture collections are not distributed here.

All fixtures except Petersen-minus-one-vertex are overfull, proving ordinary noncolorability by the matching bound. For Petersen-minus-one-vertex, an authored exhaustive decision-tree certificate was copied from the preceding graph-search packet. The independent verifier checks that every node branches over exactly all legal colors and every leaf is a dead end: 232 nodes and 36 dead ends. Each fixture has directly checked ordinary deletion-coloring witnesses for every edge.

The complete MRV search enumerates every labeled proper ordinary three-coloring of every single-edge deletion, without a node/time cutoff. For every color class covering all original degree-three vertices it checks the unique-odd-cycle conclusion. Counts are:

| Fixture | Vertices | Edges | Deletion colorings | Covering color classes | Distinct critical cycles |
|---|---:|---:|---:|---:|---:|
| 0 | 5 | 7 | 48 | 60 | 2 |
| 1 | 7 | 10 | 96 | 120 | 3 |
| 2 | 7 | 10 | 108 | 120 | 3 |
| 3 | 7 | 10 | 72 | 84 | 2 |
| 4 | 7 | 10 | 144 | 168 | 4 |
| 5 | 9 | 12 | 360 | 468 | 8 |
| 6 | 25 | 37 | 864 | 888 | 8 |
| Total | | | 1,692 | 1,908 | 30 |

The original result collection stores a full deletion-coloring/color-class witness for each of the 30 distinct critical cycles; those raw records are not distributed here. A separately written verifier checks these witnesses using a different component-decomposition implementation, checks edge coverage and family connectivity, and checks every pair of stored cycles through incident edges for edge overlap. It also validates the ordinary noncolorability/deletion certificates, the three-odd-cycle negative control, and the positive/negative matching-selection example. The independent certificate verifier does not itself re-enumerate all ordinary colorings; completeness of the numerical census comes from the exhaustive scanner. Neither the theorem nor its proof depends on that census.

## 8. Stopping boundary

The bounded round ends with the exact fixed-matching criterion, the symbolic common-one-color theorem, and the two explicit method limitations above. An arbitrary three-list assignment with empty total intersection remains outside this theorem. For a fixed four-color palette, assignments using only two or three of its four possible three-element list types have a common color and are covered; assignments using all four types have empty intersection and are not settled by this argument. No bad-list counterexample is asserted.

## 9. Distribution and computational reproduction

The complete authored symbolic arguments and explicit construction and list-coloring examples are preserved. Programs, raw fixture/certificate/coloring collections and completed-run records are not distributed. Their computational suites cannot be rerun or omitted records reconstructed from this prose alone; fresh implementation and fresh input generation are required. The 25-vertex example's criticality was verified by its overfull bound and checked certificates for every edge deletion; those deletion certificates are not printed here. The independent audit independently reconstructs and re-enumerates the claimed bounded domains, as described in [AUDIT_METHODS.md](AUDIT_METHODS.md). Neither census is a premise of the common-one-color symbolic theorem. This complement belongs to the same fifth and final research round.
