# Turn 2 — Local switches, four-seam surgery, and a disconnected finite locus

AI-assisted mathematical proof candidate; independent review pending. Original question unresolved, 2/5 author turns completed. No identification of the OWR tile-rotation equivalence is claimed.

## 1. Credited local-choice structure

Fix a finite monomial string algebra A=kQ/I. A quadratic cover is B=kQ/J, J⊆I, locally gentle. At each vertex let p,q≤2 be the numbers of incoming/outgoing arrows. Mark the p×q matrix entry (a,b) when ab belongs to I. The unmarked entries have at most one per row and column. A locally gentle J is precisely a choice of marked entries such that both the chosen entries and their complement have at most one per row and column. Distinct vertices constrain disjoint length-two paths, even when a loop is present.

For saturated covers (no larger quadratic J inside I still locally gentle), the possibilities are:
- p=0 or q=0: unique empty table;
- p=q=1: retain the entry if available, otherwise empty;
- (p,q)=(1,2) or (2,1): one retained entry; two choices exactly when both entries belong to I;
- p=q=2: the retained entries must be a permutation matrix, whose complement is the other permutation matrix. There are two choices exactly when all four entries belong to I, otherwise one supported permutation matrix.

The last assertion follows because I's complement is a partial matching: with three available entries, exactly one of the two permutation matrices is supported; with two, they themselves form a permutation matrix. These cases exhaust the string condition. Maximality is local because the quadratic generators at distinct vertices are disjoint. Thus the set of saturated covers on a fixed labelled quiver is a product of binary choices, a hypercube. Isomorphisms may identify its vertices.

This structure is already explicit in Xin–Zhang, arXiv:2608.14360, Definition 2.1 and Remark 2.2. It is credited background here, not a new classification claim. In particular their count is up to 2^(n1+n3) models after identifications. For acyclic Q every quadratic cover is finite-dimensional, so changing the local coordinates one at a time connects all saturated covers through finite covers. For cyclic Q the last conclusion fails, as Section 3 shows.

## 2. What the turn-1 topology-changing switch actually does

In the turn-1 quiver, change J0={ac,be} to J1={ac,ce}. This is a single switch at vertex 2, with incoming arrows b,c and outgoing e. Complete this vertex with an outgoing blossom f. The two completed relation tables are

J0 at 2: be, cf forbidden; bf, ce permitted.
J1 at 2: bf, ce forbidden; be, cf permitted.

In the Palu–Pilaud–Plamondon lozenge construction (Definition 4.6), each arrow has corners s,v,t,f and sides 0=s-v, 1=v-t, 2=t-f, 3=f-s. A permitted pair glues the incoming lozenge's side 1 to the outgoing one's side 0; a forbidden pair glues incoming side 2 to outgoing side 3. The old four seams are therefore red(b,e), red(c,f), green(b,f), green(c,e). Cut exactly these seams and reconnect them as red(b,f), red(c,e), green(b,e), green(c,f). The same eight boundary sides are paired once each. All other lozenges and seams are unchanged. Endpoint identifications are those of the credited construction, so this is an explicit oriented cell-complex cut/reglue operation, not merely a comparison of invariants.

In the deterministic checker's blossoming order, b=1,c=2,e=4,f=8. The complete old/new seam table is in turn2/verification.json. Reassembling the whole complex gives respectively (g,b,χ)=(0,3,-1) and (1,1,-1), agreeing with the independently written ribbon calculation in turn 1. The operation changes topology despite preserving the polygon pieces and Euler characteristic.

Consequently genus is not invariant under this particular natural local reglue. This is a decisive warning against equating 'rotation of tiles' with a homeomorphism without a source definition. We have not proved that this four-seam operation is an allowed OWR rotation, nor that it is forbidden. The conjecture's exact quotient remains unpinned.

## 3. Finite-dimensionality obstructs successive single-vertex switches

Take vertices 0,1, arrows a,b:0→1 and c:1→0, and let I consist of all four composable length-two paths ac,bc,ca,cb. A=kQ/I has dimension 5 and is a finite-dimensional string algebra. Both vertices are degree-three non-gentle vertices with two choices. A saturated gentle cover chooses one permitted pair from {ca,cb} and one from {ac,bc}. Its four states are:

1. permitted ca,ac: a↔c is a directed transition cycle, so B is infinite-dimensional;
2. permitted ca,bc: the sole maximal permitted arrow path is bca, so B is finite-dimensional;
3. permitted cb,ac: the sole maximal permitted arrow path is acb, so B is finite-dimensional;
4. permitted cb,bc: b↔c is a directed transition cycle, so B is infinite-dimensional.

In each finite case, a basis consists of two idempotents, three arrows, two length-two paths and one length-three path, hence dimension 8. No longer path is permitted. Switching only one vertex in either finite state reaches an infinite state. Thus the subgraph induced by finite-dimensional covers in the local-choice hypercube has two isolated vertices. This disproves a general proof strategy that connects any two finite covers by successive one-vertex switches while keeping every intermediate cover finite.

This is not a counterexample to the OWR conjecture. The two finite covers are exchanged by swapping a and b, and a move involving both vertices at once connects their labelled relation tables. The source explicitly mentions collections of tiles, so simultaneous moves are especially relevant. No minimality assertion about this obstruction is needed.

## 4. Exact decision criterion and controls

For any quadratic locally gentle B, form the finite directed graph whose vertices are quiver arrows and whose edges a→b are the permitted length-two paths. Every vertex has in/out-degree at most one. B is finite-dimensional iff this graph has no directed cycle: a cycle supplies arbitrarily long distinct monomial basis paths, while an acyclic finite transition graph bounds their length by |Q1|. This proves the criterion used above, including loops and parallel arrows. Equivalently no permitted walk with |Q1| transitions exists.

Run `python turn2/verify_switches.py` from the packet. Its stdout must match turn2/verification.json. It exhausts all 20 string-compatible local tables with p,q≤2; checks the finite-locus obstruction; independently compares the cycle criterion with bounded walk propagation for 913 states from all 283 degree-constrained simple directed quivers on at most three vertices; and checks the full four-seam topology change. There are 972 exact assertions. The supplementary seeded search found the two-vertex obstruction after 18 examples; it is not used as a proof of completeness or minimality.

## 5. Status and sources

The local completion description is credited to Xin–Zhang (2026), https://arxiv.org/abs/2608.14360, Remark 2.2. The lozenge construction is credited to Palu–Pilaud–Plamondon (2019), https://arxiv.org/abs/1807.04730v2, Definition 4.6 and Theorem 4.10. The OWR source is Baur's printed pp.441–444, especially443, https://ems.press/content/serial-article-files/47001; the expanded Baur–Coelho Simões paper is https://arxiv.org/abs/2403.07810. None of the retrieved sources defines the OWR tile-collection rotation sufficiently to transfer either scoped obstruction to the original conjecture.

Informal completion estimate: 40%. The substantive gain is an explicit topology-changing surgery and an exact obstruction to a finite single-switch connectivity proof. Original unresolved 2/5; no full solution or novelty claim.
