# Exact finite reductions and bounded verification for OPG-388

## Status and scope

This is an authored partial mathematical/computational report, not a resolution or a counterexample to the full conjecture. No novelty is asserted. The target is the finite **simple** graph formulation: maximum degree Δ, no Δ-edge-coloring, and a Δ-edge-coloring after deletion of every edge. Every list has exactly Δ colors. A constant assignment is necessarily bad. The target asserts that every nonconstant assignment is good.

Primary formulation: [Open Problem Garden, List colorings of edge-critical graphs](https://www.openproblemgarden.org/op/list_colorings_of_edge_critical_graphs). Kaul–Mudrock, [*Criticality, The List Color Function, and List Coloring the Cartesian Product of Graphs*](https://arxiv.org/pdf/1805.02147v2), Conjecture 6 on printed page 11, formulates the same intended question using strong chromatic-choosability of the line graph. We do not exploit the reversed “if and only if” in the old Mohar page.

## 1. A nonconstant-preserving small-palette lemma

Let H be an ordinary (k+1)-vertex-critical graph on n vertices: χ(H)=k+1 and each proper induced subgraph is k-colorable. If H has a bad nonconstant k-list assignment, then it has one whose palette has at most n−1 colors.

Proof. Let L be a bad nonconstant k-list assignment. If its palette has fewer than n colors, there is nothing to prove. Otherwise let q≥n be its palette size. The family of lists has no system of distinct representatives (SDR), since such an SDR would itself be a proper H-coloring. By Hall's theorem, some nonempty S⊆V(H) has positive deficiency

    d(S)=|S|−|B(S)|, where B(S)=union of L(v) over v in S.

Choose S maximizing d(S), and write B=B(S). It is proper because d(V(H))=n−q≤0. For the vertices outside S, consider the lists L(v)\B. They have an SDR: otherwise Hall gives T⊆V(H)\S with |union_{v∈T}(L(v)\B)|<|T|, whence

    d(S∪T)=d(S)+|T|−|union_{v∈T}(L(v)\B)|>d(S),

contradicting maximality. Any proper L-coloring of H[S] would extend to H by this outside SDR: the outside colors are mutually distinct and all lie outside B, so neither outside edges nor edges crossing S create conflicts. Therefore L restricted to S is bad.

This restricted assignment is nonconstant. If it were constant, all its lists would be the same k-set; a k-coloring of the proper induced subgraph H[S], relabeled with that set, would contradict badness. Since S is nonempty, |B|≥k. Choose any k-subset A of B and give each vertex outside S the list A, retaining the original lists on S. The resulting full assignment is bad because its restriction to S is bad, and is nonconstant because the lists already differ within S. Its palette B has size |B|<|S|<n. This proves the lemma, including the nonconstancy requirement. The transformed branch actually gives at most n−2 colors, but the untouched q<n branch may have n−1 colors. ∎

For a Δ-edge-critical G with m edges, H=L(G) is (Δ+1)-vertex-critical. Indeed deletion of any vertex of H corresponds to deleting one edge of G, and further induced restrictions remain Δ-colorable; χ(H)>Δ, while coloring G−e and assigning one extra color to e proves χ(H)≤Δ+1. Thus the lemma applies with n=m and k=Δ, without requiring Vizing's theorem.

## 2. Pair-cooccurrence compression

Choose, among all bad nonconstant k-list assignments for a fixed H, one with minimum palette size q. Necessarily q≥k+1. If q≥k+2, every unordered pair of palette colors occurs together in at least one list.

Otherwise choose colors a,b which never co-occur and identify them as a single color. Every list still has size k. Every proper coloring from the merged lists lifts to a proper coloring from the original lists: at a vertex assigned the merged color, precisely one of a,b is in its original list, and two adjacent vertices cannot both use the merged color. All other color names are unchanged. Thus the merged assignment is still bad. Its palette has q−1>k colors, so it is nonconstant, contradicting minimality.

Counting co-occurring pairs now gives

    q=k+1, or binom(q,2) ≤ n·binom(k,2).

For line graphs of the target critical graphs, one may simultaneously take q≤m−1 by Section 1. Consequently any counterexample on a fixed graph has a witness within an explicitly bounded finite palette; for q≥Δ+2 that palette also satisfies q(q−1)≤mΔ(Δ−1). This is a reduction only, not a proof that the finite families are all colorable.

## 3. Exact full-list verification for K4 with one edge subdivided

Use the ordered seven edges

    e0=01, e1=02, e2=13, e3=14, e4=23, e5=24, e6=34

on vertices 0,1,2,3,4. The graph has maximum degree three and seven edges. A matching has at most two edges, so three matchings cannot cover its seven edges. It is not 3-edge-colorable.

The following explicit deletion-coloring vectors use colors 0,1,2 and -1 for the deleted edge, in the displayed edge order:

    delete e0: [-1,2,1,0,0,1,2]
    delete e1: [2,-1,0,1,1,0,2]
    delete e2: [0,1,-1,2,2,0,1]
    delete e3: [0,1,2,-1,0,2,1]
    delete e4: [1,0,2,0,-1,2,1]
    delete e5: [1,0,0,2,2,-1,1]
    delete e6: [0,1,1,2,2,0,-1]

These prove edge-criticality independently of overfullness. Every displayed deletion vector was independently checked for allowed colors and incident-edge conflicts. These seven vectors are explicit authored mathematical examples, so their criticality verification is reproducible directly from this text.

By Section 1, any bad nonconstant 3-assignment would have a witness on at most six colors. Here is a complete normalization which does not discard any assignment. Relabel the first list as {0,1,2}. Process the later edges in order. At each edge, retain the names of previously seen colors and label its fresh colors by the next consecutive unused integers, in any order. Each normalized list is therefore an arbitrary subset of previously seen colors together with a consecutive block of fresh colors, totaling three. Conversely, every list sequence generated by this rule is an actual 3-assignment. Multiple representatives of an equivalence class are harmless; uniqueness is not assumed.

The generator fixes the first list to {0,1,2}. At a later step with p colors already introduced, it chooses each old-color subset of size s≤3 and appends exactly 3−s fresh colors, rejecting only p+3−s>6. Thus it exhausts all normalized assignments with palette at most six. The independent counting recurrence is

    F(i+1,p+3−s) += F(i,p)·binom(p,s),
    F(1,3)=1, 0≤s≤min(3,p), p+3−s≤6.

For seven lists the exact counts are:

- palette 3: 1
- palette 4: 4,095
- palette 5: 662,571
- palette 6: 19,124,343
- total: 19,791,010

The completed finite search covered all 19,791,010 normalized cases. Exactly one is bad, the constant assignment. A separate seven-edge coloring witness was retained for every other case, and a designated marker represented the constant obstruction. Search exhaustion is not used to certify negative cases beyond the constant case; its impossibility follows from the matching-size argument. The raw witness collection and its storage representation are not distributed in this prose edition.

A separate checker uses no coloring search. It reconstructs each list using direct increasing triples and the first-occurrence condition, checks that every claimed color is in its list, and checks all edge intersections directly from the original graph. It verifies the sole bad record is constant, all 19,791,009 other records are proper colorings, the expected per-palette counts, and that the witness stream ended exactly at the expected boundary. This full check passed. Separate checks derived the combinatorial count and validated edge-criticality.

The checked finite witnesses together with Section 1 establish the target assertion for this one graph (and addition of isolated vertices). This is a report of completed computer-assisted verification; the omitted witness collection cannot be reconstructed from this prose alone. The published-theorem route below gives a separate mathematical justification that does not require that collection.

### Published-theorem boundary

This positive case is already implied by **Lemma 3** in the cited Kaul–Mudrock paper (printed page 8). The whole line graph is exactly the following construction from an odd cycle C5: add independent vertices u and s; join u to A={v1,v2,v3,v4} and s to B={v2,v3,v4,v5}. An exact graph isomorphism, not just a spanning-subgraph embedding, is

    (v1,v2,v3,v4,v5,u,s) ↦ (e0,e2,e6,e5,e1,e3,e4).

Equality of both edge sets was checked independently. The base C5 is strong 3-chromatic-choosable, A∪B is its whole vertex set, |A|=|B|=4>|A∩B|=3>0, and 3≤4, the intersection bound for odd k=3 in Lemma 3. The constructed graph has chromatic number 4 by the elementary edge-criticality certificate above. Lemma 3 therefore says the entire line graph is strong 4-chromatic-choosable. No unproved upward monotonicity under edge addition is used. The finite computation independently confirms this already covered special case; it is not a new conjecture resolution.

For clarity, a strong r-chromatic-choosable graph has chromatic number r and is colorable from every nonconstant assignment of (r−1)-element vertex lists. The part of Kaul–Mudrock Lemma 3 used here says the following. Starting with a strong k-chromatic-choosable graph, attach two nonadjacent new vertices to sets A and B whose union is the base vertex set, each properly larger than their nonempty intersection. If k is odd, the intersection may have at most four vertices; if k is even, at most three. Provided the resulting graph has chromatic number greater than k, it is strong (k+1)-chromatic-choosable. This is an invoked published theorem, not a reproduced proof or a novelty claim.

Here k=3. The base C5 has chromatic number three. Any nonconstant two-element vertex-list assignment on C5 has adjacent unequal lists; start at one endpoint with a color absent from the other endpoint's list and greedily proceed along the path the other way around the cycle. The last vertex cannot clash with the initial color, proving the base strong property. Under the displayed map, the base cycle corresponds in order to e0,e2,e6,e5,e1; its five consecutive intersections are 1,3,4,2,0, and its nonconsecutive pairs are disjoint. The edge e3=14 meets exactly e0,e2,e6,e5 among that cycle, and e4=23 meets exactly e2,e6,e5,e1. They do not meet each other. This verifies the entire graph equality directly. The seven-edge graph has chromatic index four: its three-color obstruction was proved above, while any displayed deletion coloring extends using a fourth color on the missing edge. Therefore the line graph has chromatic number four, all Lemma 3 hypotheses hold, and the strong four-chromatic-choosable conclusion gives every nonconstant three-edge-list coloring claimed here. No omitted computational certificate is needed for this argument.

## 4. Bounded graph and four-color-palette searches

The bounded graph census enumerated every simple labeled graph on 3≤n≤7 whose edge count lies from n to floor(3n/2), then filtered for connectedness, minimum degree at least two, and maximum degree exactly three. These are necessary conditions for a nontrivial 3-edge-critical graph: a leaf edge can be extended after its deletion using a color missing at its other endpoint, and multiple nontrivial components would permit deletion outside an obstructing component. Isolated vertices may always be discarded.

Exact backtracking and every-edge-deletion tests found one critical isomorphism type on five vertices and four on seven vertices, with none on three, four, or six vertices. The labeled counts are 30 at n=5 and 5,670 at n=7. Canonicalization considers all degree-preserving permutations. All five representative graphs are overfull by one, and deletion colorings for every edge were independently checked. Those additional witness collections are not distributed here. The classification is a computation, not an imported complete census. Only the five-vertex type received the full arbitrary-palette verification of Section 3.

A separate four-palette search exhausted all lists drawn from a fixed four-color palette, fixing the first list to {0,1,2} by a global permutation, for all five representatives and for Petersen-minus-one-vertex. This is exactly 4^(m−1) assignments per graph: 4,096 at m=7; 262,144 for each of the four m=10 graphs; and 4,194,304 at m=12. In each scan the unique bad assignment was constant. Every positive witness was checked in memory. These four-color scans do not cover arbitrary larger palettes on the m=10 or m=12 graphs.

The Petersen-minus-vertex example has nine vertices and twelve edges, ordered as

    01,05,12,16,23,27,38,46,47,57,58,68.

It is not overfull. Its non-3-colorability is certified by a full 232-node exhaustive decision tree, with 36 empty-domain leaves, checked independently in full. The decision tree itself is not distributed here. At every internal node the independent checker recomputes exactly which colors remain legal and requires a child for each. No cutoff, timeout, solver status, or unverified cubic-class-2 assumption is used. All twelve deletion-coloring witnesses are checked independently as well.

## 5. Reproduction and residual

This edition includes the complete palette-reduction proofs, the normalization rule and counting recurrence, seven explicit deletion-coloring vectors, the exact line-graph map to the published construction, all stated aggregate search counts, and the scope of the independent checks. Readers can verify the displayed vectors, recurrence, and graph isomorphism from the prose. The independent source theorem supplies the arbitrary-palette result for the subdivided-K4 graph.

The executable programs, larger coloring-witness collections, and Petersen decision tree are not distributed. Their omitted raw certificates cannot be reproduced from this prose alone. The completed census, larger-graph four-palette scans, and raw-witness acceptance are therefore reported computational results with disclosed coverage, not newly executable certificates supplied by this edition. A new implementation and generation of the omitted witnesses would be needed for an independent computational reproduction. No omitted-file names, identities, hashes, byte counts, or run commands are part of the public distribution.

All computations reported here reached completion. No incomplete search is called unsatisfiable.

Residual: arbitrary Δ≥3 critical simple graphs and arbitrary nonconstant Δ-assignments remain unproved. The small-palette and pair-cooccurrence reductions make each fixed-graph test finite but do not provide a graph-order bound. The bounded positive calculations are not evidence of full acceptance, and no intended-conjecture counterexample was found.
