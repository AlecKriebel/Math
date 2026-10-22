Editorial note: This is the complete authored text. Only references to undistributed operational files, their identities, locations and replay directions have been replaced. All mathematical arguments, exact finite counts, corrections and limitations are retained. The public manifest identifies the actual distributed files.

# Independent acceptance: repeated-leaf signed-core obstruction

## Verdict and exact frozen scope

**ACCEPTED, without a mathematical correction, as a separate supplement within the fifth and final substantive pass.** For every k at least four, the construction gives a connected odd-hole-free graph which is divisible, together with exactly two nonextendible prescribed colorings of its exact high-incidence core. Each bad coloring has exactly one monochromatic (k-1)-clique. The effective signed-tree component is a five-node path whose two leaf boundaries are identical.

This is not a counterexample to odd-hole-free 2-divisibility. Its bad prescriptions are not divisions of the induced core at its own clique number. At k=4 the core has nine vertices, so the example neither resolves nor excludes the unresolved eight-core boundary. No novelty, minimality or new research-pass claim is accepted or made.

The final source packet, complete proof, manifest and external pin were exactly identified and byte-checked. This acceptance uses the final pin, not the preliminary control pin. The full source identity record binds the complete exact inventory and dependencies; undistributed operational identities are omitted here.

The full proof, verifier, controls, scope, expectations and all three dependency texts were read. The accepted compression theorem was separately audited and frozen before this supplement. All originals are preserved. No repository, publication, queue or further research action was taken.

## 1. Exact graph and maximum-clique family

The four low vertices induce a diamond, with z1,z4 nonadjacent. A is a clique of size k-1 adjacent to z1,z4. The three mutually disjoint B_i cliques of size k-2 attach to their consecutive adjacent low pairs. There are no other cross-block edges. Each A vertex receives one private support k-clique, and each B vertex receives two.

A clique meeting a support-private vertex lies in its support bag. Otherwise a clique meeting B_i lies in B_i plus its low pair. A clique meeting A can use at most one of the nonadjacent z1,z4. A low-only clique has size at most three, smaller than k. Therefore the five base bags and all support bags are exactly the maximum cliques, with no larger clique. The exclusion of k=3 is essential: the diamond triangles would then be additional maximum cliques and would change original incidences.

Every A or B vertex has exactly three original maximum-clique occurrences; every low vertex has two; every support-private vertex has one. Thus X=A union B1 union B2 union B3 exactly, with |X|=4k-7. Its induced graph is K_(k-1) disjoint from three K_(k-2), so A is its unique clique of size k-1.

There are 7k-13 support bags, 7k-8 maximum cliques in total, and 4+(4k-7)+(k-1)(7k-13)=7k^2-16k+10 graph vertices. In particular, k=4 gives 58 vertices, 20 maximum cliques and nine core vertices. The graph is connected.

The original outside-X dual consists of the five-node path Q0,Q1,Q2,Q3,Q4 and marked isolated support nodes. Its leaf boundaries are both A, on the same bipartition side. Its two boundary unions S=A union B2 and T=B1 union B3 are disjoint and exhaust X. The actual graph contains the extra diamond edges z1z3 and z2z4, neither belonging to any maximum clique; deleting both changes the hole structure. No maximum-clique-shadow inheritance assumption is used.

## 2. All-size odd-hole proof

Support-private vertices are simplicial and cannot lie on an induced cycle of length at least four. After removing them, each B vertex is simplicial because its remaining neighbors are its own clique and an adjacent low pair. Removing these for hole inspection leaves exactly the diamond and A.

The vertices in A are adjacent true twins. An induced cycle of length at least four cannot use two of them: adjacency forces consecutive occurrence, and their identical other neighborhoods give a chord. With no A vertex the cycle would lie in the chordal diamond. With one A vertex, its two cycle neighbors must be z1,z4, so the remaining cycle is an induced diamond path between those tips. Every such path has exactly two edges, through z2 or z3; every three-edge alternative has a diamond chord. Hence every hole has length four, proving odd-hole-freeness of the full graph.

This is an all-size proof about the actual graph. It is not inferred from finite enumeration or from the clique shadow.

## 3. Exact failed prescriptions and remaining limitations

Color A and B2 with one color and B1 and B3 with the other. The leaf cliques force z1,z4 opposite A. Their neighboring cliques force z2,z3 to A's color. The middle clique B2+z2+z3 is then monochromatic. Thus the coloring cannot extend. Its only monochromatic (k-1)-clique is A, because A is the unique core clique of that size. There is none in the opposite color.

The independently accepted component-compression theorem applies with this exact original X. There is exactly one unmarked tree component, with disjoint boundary unions covering all X. Its complementary signed pair forbids exactly these two complete core assignments, so all other 2^(4k-7)-2 assignments extend. This exact count follows for all k from the theorem, not from fitting four test cases.

The graph itself is divisible: give both colors to A and each B_i, possible since k>=4; color low vertices arbitrarily; and in each support bag choose a private vertex opposite its attachment. Every maximum clique is mixed.

Accordingly, “at most one monochromatic (k-1)-clique guarantees extension” is false, and graph realizability does not prohibit identical same-side leaf boundaries. The established sufficient condition forbidding every monochromatic (k-1)-clique remains valid. This supplement does not strengthen the separate fourth-pass counterexample about a valid division of the induced core: here A is monochromatic, so the bad prescription is not a core division. The nine-core k=4 construction has no implication that the eight-core boundary is impossible.

## 4. Independent computational checks

The independent checker imports no authored mathematical code. It builds graph adjacency directly from the block and port rules, then reconstructs maximum cliques by increasing-vertex clique recursion rather than the source's Bron-Kerbosch routine. It checks the exact family, all original incidence counts, the unique core maximum clique, graph size formulas, and the precise two edges missing from the maximum-clique shadow.

For k=4,5,6,7 it independently reconstructs the entire dual graph and verifies the unique five-node unmarked path and repeated leaf A. A separate reverse-order Davis-Putnam elimination computes the exact existential projection from the full maximum-clique CNF and checks that precisely the complementary S/T clause pair remains. Thus the finite exact-projection check does not merely test the one displayed bad coloring.

The checker verifies every successive simplicial removal in the hole argument, then enumerates all induced cycles in the reduced graph. It finds exactly 2(k-1) induced four-cycles and no longer holes. It also exhausts all 68,636 odd base-graph subsets of size at least five at k=4,5 (3,797 and 64,839 respectively), finding none that induce a hole. No exhaustive odd-subset search of the full 58- or 105-vertex graph, or of the larger base graphs, is claimed.

Every core coloring is checked at k=4 and k=5: 512 plus 8,192, totaling 8,704. A direct oracle enumerates all sixteen low-vertex assignments and verifies full-graph completion witnesses for every successful core assignment. Exactly two colorings fail at each rank. At k=6,7 the symbolic projection and all sixteen low assignments under the bad prescription are checked; all 2^17 or 2^21 core assignments are not individually enumerated.

The independent output is byte-identical under normal Python, -O and -OO, with SHA-256 `[verified identity of undistributed artifact]`. Its case-stream hash is `[verified identity of undistributed artifact]`. The frozen author's verifier also passes in all three modes with the exact stored expected rows and stream hash. These computations supplement the proof and describe specific fixtures, not all graphs of their orders.

## 5. Fixed-byte and hostile-control audit

An independent fixed-pin checker validates all seven source members, complete inventory, nonsymlink file types and path components, exact lengths and hashes, and all three required dependencies. It is run normally and under -O/-OO. The author mathematical replay likewise uses the final source pin in each mode.

The independent mutation suite has 71 scenarios and 138 required program rejections per mode, 414 total. Disposable copies test every source member for removal, alteration, symlink and directory replacement; each dependency for removal, alteration, direct and parent symlinks; extra entries and dangling links; root and ancestor links; missing, modified, linked, internal or wrongly hashed pins; duplicate JSON keys; narrowed/typed scope; changed/missing expectations; dependency metadata; wrong origin; missing individual CLI arguments; a deliberately false author mathematical obligation; removal of both diamond diagonals; and a deliberately false independent maximum-clique obligation. Semantic mutants are re-manifested and re-pinned. All gates survive optimization.

The author's independently rehashed final terminal has (verified original byte count omitted) and SHA-256 `[verified identity of undistributed artifact]`. Its twelve final evidence files confirm 67 authored controls per mode, 201 rejections. The four separately retained preliminary receipts are also rehashed. The preliminary single-diagonal-deletion mutation was still a mathematically valid odd-hole-free obstruction; the final checker adds an exact intended-diamond identity obligation, and its final controls reject single- and double-diagonal deletion. This is an explicit control-scope correction before the final freeze; the proof and intended construction were unchanged.

The previous compression terminal and its twelve evidence files are independently rehashed as supplementary provenance: 79 authored controls per mode, alongside the separately executed compression audit's own 495 mutation rejections. No prior sealed audit is rewritten to add these late receipts.

This audit's deliverables have their own externally retained review seal and separate post-seal normal/-O/-OO checks and mutation receipts. This supports the static snapshots and tested failure modes. It does not certify concurrent hostile-race protection, coordinated replacement of all trust anchors, or exhaustive malformed-input security.

**Accepted boundary:** a graph-realizable repeated same-side leaf boundary and a nonextendible prescription with exactly one monochromatic (k-1)-clique, for every k>=4. The graph is divisible, and both the general conjecture and the k=4 eight-core frontier remain unresolved.
