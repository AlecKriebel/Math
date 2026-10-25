# Independent universal verification and exact controls

The reduction, partial-block mechanism and distinct direct-ear construction were fixed in the sealed early ledger before foreign primary bodies. The cited structural interface was subsequently checked in the actual Benchetrit–Sebő v1 body. Finite checks supplement the all-input arguments below.

## D1. Literal objective, cycle rank and completion

Graphs are loopless 2-vertex-connected multigraphs on at least 3 vertices. A complete open ear decomposition partitions every edge, starts with a circuit and thereafter uses paths with distinct old endpoints and new internal vertices. One-edge ears are permitted. The initial circuit counts and the first even ear stops the odd prefix.

The initial circuit has cycle rank 1. A path ear with l edges adds l-1 vertices, hence increases E-V+1 by1, including l=1. Thus the rank of an odd prefix equals its number of ears.

Any 2-connected subgraph H of 2-connected G admits extension of its ear decomposition to all G. If vertices remain outside, each outside component has at least two distinct old neighbors: zero would disconnect G, and a sole neighbor would separate that component from the at least two other old vertices after deletion. A path through the component between two attachment vertices supplies an open ear. Its internal vertices are new and its edges unused. Open-ear addition preserves2-connectivity, as can be checked after deleting an old vertex, an endpoint or an internal vertex. Repeat until all vertices appear, then add every unused loopless edge as a one-edge ear. Parallel edges cause no obstruction; loops would, and are excluded.

## D2. Original general factor-critical formula

The actual cited source's Theorem 3.2 says that a 2-connected graph is factor-critical iff it has an odd OPEN ear decomposition under its definitions. Its Proposition 1.13 supplies the same completion fact as D1, and its Section 3.1 already states beta as the largest number of ears of a 2-connected factor-critical subgraph. This exactly supports the manuscript's classical input; the original 1972 Lovász body was not recovered or pretended read.

An odd prefix therefore gives an eligible H with rank equal to its length. Conversely an eligible H has an all-odd open decomposition and extends by D1, giving a prefix of its rank. Adding missing edges on a fixed vertex set preserves every required perfect matching and2-connectivity, while increasing rank. Hence the maximum can be taken over induced subgraphs. If none exist the value is 0, agreeing with no odd initial circuit. This proves the original Lemma2, including its induced-subgraph clause.

## D3. Independent elementary direction: odd ears preserve factor-criticality

This was independently derived before primary reading. An odd circuit is factor-critical: deleting a vertex leaves an even path. Suppose an old factor-critical H receives the odd ear a,x1,...,x_(2q),b. After deleting an old vertex, use a perfect matching of the corresponding old deletion and pair the internal vertices consecutively. After deleting internal x_j with j odd, pair the internal segment left of it internally, pair the right segment through old endpoint b, and use an old perfect matching of H-b. If j is even, pair the left segment through a, the remaining right internal segment internally, and use H-a. All vertices are covered once. A one-edge ear merely adds an edge and preserves the property.

Thus every odd prefix is factor-critical without importing the converse structural theorem. Its union is also2-connected by D1's deletion argument. This supplies an independent upper-bound mechanism for the cone identity.

## D4. Cone identity, both original proof and a distinct direct construction

For connected bipartite B on at least2 vertices, z*B is 2-connected: delete z to get B, or delete another vertex and retain connectivity through z. A2-connected factor-critical graph has odd order and cannot be bipartite: deleting a vertex from its smaller nonempty part leaves unequal bipartition sizes.

Every eligible prefix H in z*B therefore contains z. Put S=V(H)-z. Deleting z from H gives a connected graph with a perfect matching, so B[S] is connected and perfectly matchable. Its edges bound rank(H) above, because H has at most |E(B[S])|+|S| edges on |S|+1 vertices. This proves beta(z*B)<=the objective in the original cone formula.

For a distinct direct lower-bound proof, let B[S] be connected with perfect matching M. Contract the matching edges and take a rooted spanning tree of the connected quotient. Order matching pairs so each new pair has an edge xa to an already included pair, with its mate b still new. Start with the triangle z plus the first matching pair. Add each new pair using the odd 3-ear x,a,b,z; its endpoints x,z are distinct and old, while a,b are new. Once all pairs are included, append every unused edge as a one-edge ear. This is a complete all-odd open decomposition of z*B[S], with ear count equal to its rank=|E(B[S])|. Extend to z*B by D1. It proves the reverse inequality without the deep factor-critical converse.

The original proof also works directly: deleting z requires a perfect matching of B[S]; after deleting u in S, replace its matching edge uv by zv and retain the rest. This makes the cone factor-critical, and deleting z tests connectivity. Nonempty perfectly matchable S has at least2 vertices; the feasible family exists because connected B contains an edge. All these deductions allow parallel edges; the reduction outputs simple graphs.

## D5. Complete preprocessing and polynomial encoding

Set Cover explicitly gives U, a list of sets and a signed binary budget s. Negative s is NO; empty U with nonnegative s is YES. For nonempty U, no sets, an uncovered element or s=0 is NO. If the union is U and s>=n, it is YES. Each such branch maps to a triangle with threshold1 for YES and2 for NO; its beta is1 and it is a simple cone over connected bipartite K2. Every output, including preprocessing branches, lies in the promised restricted class. Invalid encodings can be rejected before mapping; repeated element tokens can be canonicalized in polynomial time. Empty/repeated sets are permitted.

In the remaining case m,n>=1,1<=s<=n and union A_j=U. Let T=n+sum|A_j|, k=T+n+3, M=(m+1)k² and F=M-ks. Then k>T,k>s, and k-s>=T+3 gives k²-ks=k(k-s)>T. Also F>=k((m+1)k-s)>0. In particular k>=2.

For explicit input length L, n and incidence count are O(L). After the union test every universe element appears in an incidence, so m=O(L) as well; polynomial renumbering handles long labels. Thus k=O(L), B has2k(m+1)+n=O(L²) vertices and (m+1)k²+T=O(L³) edges. The cone adds only O(L²) edges. The positive threshold F has polynomial bit length. A huge binary budget is handled before construction; no pseudo-polynomial expansion, weights, implicit multiplicity or succinct graph is used.

## D6. Forward Set Cover direction with an explicit perfect matching

Choose an inclusion-minimal cover J within budget, r=|J|<=s. Each selected set has an element in no other selected set, or it could be deleted; choose p(j) accordingly. These private elements are distinct. Empty sets cannot be members of such a minimal cover of nonempty U, and duplicate sets cannot invalidate the argument.

Keep every block vertex and the selected r connectors, except one left vertex in block p(j) for each selected j. Match c_j to the distinguished right vertex q_(p(j)). The rest of that block has k-1 left and k-1 unmatched right vertices, matched internally. Match all other K_(k,k) blocks internally. These edges cover every selected vertex exactly once. Each block remains connected because k>=2. Selected connectors all meet root q0 and coverage joins every element block, so the induced graph is connected.

Exactly r left vertices in distinct blocks are removed, losing kr internal edges. Every right vertex remains, so all selected connector incidences remain. Therefore

    E(B[S])=M-kr+sum_(j in J)(1+|A_j|)>=M-ks=F.

D4 then yields beta(G)>=F. No matching algorithm or rounding assumption is hidden in this constructed witness.

## D7. Reverse direction: arbitrary partial blocks, all of them

Let connected perfectly matchable B[S] have at least F induced edges, and let r be its selected connector count. Write a_i,b_i for omitted left/right block vertices, allowing ANY integers0<=a_i,b_i<=k. Its exact internal loss is

    d_i=k²-(k-a_i)(k-b_i)=k(a_i+b_i)-a_i b_i.

If a block retains no internal edge, it loses all k² such edges. Even retaining every other internal edge and every connector edge would give at most M-k²+T<M-ks, impossible. Hence every block, including the distinct root and each element block, retains an internal edge.

A perfect matching requires equal selected bipartition sizes. Since all r connectors are left vertices,

    sum_i(k-a_i)+r=sum_i(k-b_i), so sum_i(a_i-b_i)=r.

For EACH partial block the exact identity is

    d_i-k(a_i-b_i)=b_i(2k-a_i)>=0.

It holds even when a_i-b_i is negative and does not assume a whole-block optimum. Sum to obtain loss>=kr. The entire graph has only T connector edges. Hence

    M-ks<=E(B[S])<=M-kr+T,
    k(r-s)<=T<k.

Integrality gives r<=s. Finally, a selected internal edge in element block i must have a path to the retained root block, by connectivity. The path leaves Q_i through a selected c_j, possible only if i in A_j. If q_i had been omitted no such exit could exist, so omitted distinguished vertices do not evade this argument. The selected r sets cover every element within budget. This proves the reverse implication for all feasible partial selections, not a finite list or an assumed optimum shape.

## D8. NP membership and exact threshold scope

The manuscript's certificate H plus a perfect matching of H-v for each v has polynomial length: there are at most |V(G)| matchings, each polynomial in input size. Check containment, at least 3 vertices, connectivity after each deletion, matching coverage and rank>=t. D2 proves equivalence. Binary t, including extremely large values, is compared in polynomial bit time. For t<=0 valid inputs are YES; reject invalid graphs first.

Independently, a COMPLETE open ear decomposition is itself a polynomial certificate: every edge appears once, with vertex/edge identifiers and ear delimiters. Verify the initial circuit, distinct old endpoints, new internal vertices, disjoint edge partition covering G and the actual initial consecutive odd count. This proves NP membership directly for the original objective without using a matching oracle. D5–D7 plus Set Cover NP-completeness prove the full restricted NP-hardness. No assertion is made for a fixed t; the input-dependent threshold is compatible with the cited FPT result.

## D9. Exact objective and definition negative controls

Three K33 blocks plus two left connectors give a disconnected perfectly matchable selection with27 induced edges: select just all block vertices. If a connected feasible selection retains every block edgewise, both connectors are necessary. Matching balance forces loss>=3r=6, while they contribute at most4 edges, giving at most25. If any block has no internal edge, the global bound is27-9+4=22. The25 bound is attained by omitting one left vertex in each nonroot block and matching its connector to that block's distinguished right. Both selections have18 vertices and9 matching edges. Thus induced-edge count, connectedness and matching-edge weight cannot be silently interchanged.

For K4, a triangle followed by an even2-ear introducing the fourth vertex and then the remaining one-edge ear has two odd ears in TOTAL, but initial odd count 1. No odd prefix can introduce an odd number of new vertices, so it stays on three vertices and has only the triangle; beta(K4)=1. This diagnoses the distinction from the efficiently optimized total-odd-ear parameter. For a triangle with r parallel copies of one side, the first triangle and r-1 one-edge ears give beta=r, equal to rank; this checks the importance of counting one-edge ears in the multigraph convention for every r>=1.

## D10. Reproducible finite controls, with explicit limits

The inspected own controls.py enumerates every labelled 2-connected simple graph on 3–5 vertices:249 graphs. A literal initial-circuit/open-path/one-edge search optimizes the prefix, then explicitly completes and verifies a full edge-partition decomposition. Independently enumerate induced vertex subsets and deletion perfect matchings to compare the factor-critical rank expression. Eight connected bipartite supports also compare their cone parameter against direct connected-perfectly-matchable subset optimization. All agree. These finite checks neither prove the classical theorem nor the arbitrary-size reduction.

The partial-block polynomial identity is symbolically checked exactly. Three actual-size Set Cover witnesses are constructed with the stated, unshrunk k. Their complete selected vertex sets and perfect matchings are retained, along with connectedness and exact induced-edge counts. Empty/repeated-set examples occur among them. No exponential optimization of those large beta instances is claimed. The 27/25 witnesses and triangle preprocessing value are also checked exactly. Universal encoding/preprocessing/NO-instance correctness is D5/D7, not an inference from these YES samples.

## D11. Credit, contemporary overlap and strongest result

The exact older question, open-ear convention, factor-critical formulation and structural theorem are supported by actual Sebő/Benchetrit–Sebő interfaces. Sharifov optimizes induced-edge weight without connectedness; Gomes optimizes matching-edge weight with connectedness. Havet–Nisse and Bai–Bérczi–Nalam address different ear/total-parity constraints. These distinctions were checked at their actual primary interfaces and do not establish exhaustive priority.

A separate actual five-page preprint by Alper Ferudun, Zenodo23592264, declares 23 October 2026 and was created that date, while the target declares22October2026 and has authenticated22October creation. It claims the variable-threshold classification using a different 3-SAT/multiplicity/subdivision reduction. Its complete body was read after the early seal as current primary context, not adopted as a proof of this paper or endorsed in all stronger claims. Record dates alone do not prove independence, historical firstness or the relation between the works. Its existence is explicitly recorded; no exclusive novelty/current-openness claim is approved.

The full original Theorem 1, Lemmas2–3 and Proposition4 survive this bounded falsification. No substantive defect, indispensable gap or indispensable missing attribution was established. The older Lovász original body and Gomes final journal body remain access limits; the exact needed structural statement is independently authenticated in BS v1. Historical priority remains unknown. No repair or narrower replacement was attempted.
