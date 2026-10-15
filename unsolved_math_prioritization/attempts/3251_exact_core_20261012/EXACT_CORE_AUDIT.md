Editorial note: The complete authored proof or audit is preserved below. The clearly labeled representation-size correction supersedes two false historical complexity sentences and qualifies the earlier acceptance. Other changes replace only operational artifact identities, byte counts, locations and original replay directions. All mathematical arguments, exact finite scopes and substantive limitations remain. This edition's public manifest identifies the distributed prose.

# Independent audit: exact high-incidence-core propagation and signed trees

## Decision and scope

**ACCEPTED as all-size structural partial results at the frozen scope. The original no-correction verdict is qualified by the [accepted representation-size correction](COMPLEXITY_CORRECTION.md); all other conclusions remain accepted at their stated scopes. The unrestricted odd-hole-free 2-divisibility conjecture remains unresolved.**

This audit concerns the fourth-pass [exact-core proof](EXACT_CORE_PROOFS.md), for problem 3251 / ordered row 1753. The complete original proof was checked against its externally retained pin and exact manifest. Original operational identities are omitted from this prose edition; its public manifest identifies the actual distributed files.

All graphs are finite and simple. A division means a two-coloring with no monochromatic maximum-cardinality clique. The original maximum-clique family, not the maximal-clique family or an induced-core recomputation, defines incidence and X. Throughout the extension and tree theorems, k is at least three and P contains X. Odd-hole-freeness is used only in the stated core-order and K4-core consequences. The nonuniform set-family variant assumes original set sizes at least three and outside-P occurrence incidence at most two.

The five mandatory dependency texts were read in full and their exact bytes verified: the accepted boundary-flexibility audit, its original boundary-extension proof, the separately accepted high-incidence-core addendum, the accepted sharp-chromatic-order audit, and the accepted maximum-clique-hypergraph audit. The frozen source files were preserved. This review makes no remote or queue change and initiates no further research round.

## 1. Exact singleton propagation: accepted

Every singleton assignment is logically necessary in any extension of the current assignments. A fully assigned monochromatic maximum clique therefore proves failure. A clique becomes permanently satisfied immediately after it creates its last vertex, so it cannot create another vertex.

At a conflict-free fixed point, discard satisfied cliques and remove assigned vertices from each remaining occurrence. A residual of size zero would have caused a conflict, and a residual of size one would permit another rule. Every residual has size at least two. If no original vertex of that clique was assigned, its demand remains bichromatic B and its original size is at least three; otherwise its assigned vertices all have one color, whose monochromatic residual is forbidden. Consequently every residual two-set is one-sided.

The accepted mixed-constraint lemma applies to labelled residual occurrences, including repetitions produced by different original cliques. Every remaining vertex lies outside P, and its incidence in these occurrences is at most its original incidence, hence at most two. The only unsatisfiable mixed component is a pure odd cycle of two-sets all demanding B. Such a component cannot occur here. The residual coloring supplied by that lemma completes the prescribed coloring.

This proves necessity and sufficiency for every exhaustive legal propagation order. It also handles opposite demands on one currently free vertex: executing either demand makes the opposing clique an ordinary monochromatic conflict. There is no need to impose an extra arbitrary conflict convention. Repeated residual two-sets with opposite one-sided demands can be simultaneously satisfied by coloring their two vertices differently and do not constitute an omitted exception.

The claimed linear-incidence implementation is valid with a queue, per-clique assigned-color counts, and incidence lists. Each vertex is assigned once, each incidence is updated once, and the mixed completion is an Euler-traversal construction on a linear-sized dual representation. This is conditional on receiving the explicit original maximum-clique list. The O(2^|X| (n+L)) decision bound does not claim efficient maximum-clique enumeration from an arbitrary graph encoding.

## 2. Extraction and complete tree converse: accepted

Start with the final conflict clique R. For every nonprescribed vertex used as an input to a selected clique, select its earlier creator. A selected creator is never R, because a creator is subsequently satisfied whereas R is monochromatic. Every selected creator contributes exactly one created vertex, and this vertex is consumed in one later selected clique. Incidence at most two rules out a second consumer. Conversely every outside-P vertex in a selected clique is already assigned at that clique's creation or conflict time, or is the clique's own created output. Closing backward over all inputs selects its creator.

Thus every represented outside-P vertex has exactly two selected occurrences. Orient its edge from its creator to its consumer. Every selected node except R has exactly one outgoing edge, R has none, and creation times strictly increase along edges. The selected graph is connected to R by construction. It has one edge per nonroot node and no directed cycle; equivalently, connectedness and the edge count make its underlying multigraph a tree. This explicitly rules out an undirected cycle and parallel edges. Merely invoking directed acyclicity without the outdegree and connectivity facts would not have sufficed, but those facts are all present in the frozen proof.

Label a creator by the common color of its inputs and label R by its conflict color. An output has the opposite color to its creator's label and the same color as its consumer's label. Labels therefore alternate across every tree edge. Every prescribed vertex at a selected node has that node's label, which gives the matching signed P-tree. Since its t-1 edges are distinct outside-P vertices, t is at most |V minus P|+1. Distinct selected clique identities also give t at most |M|.

For the converse, root any matching tree arbitrarily. A nonroot leaf has exactly one outside-P vertex, its parent edge; every other vertex lies in P and has the leaf's label. Its parent edge is consequently forced to the parent's label. At an internal node, all child-edge vertices have already acquired its label, as have all its prescribed vertices, so its parent edge is forced. The root finally becomes monochromatic. This works even when internal nodes have no prescribed vertices, including the tested stars whose centers have none. It uses the occurrence condition on every outside-P vertex in the selected subfamily, not an unstated absence of other graph edges.

The one-node case is exactly a maximum clique contained in P and already monochromatic. Different selected nodes may share multiple prescribed vertices; matching is possible only if each such shared vertex occurs on a single bipartition side. The discussion of leaves is correctly qualified: opposite-side leaf boundary cliques are differently colored and therefore disjoint, but same-side leaf cliques may overlap.

## 3. Exact signed core clauses: accepted

For P=X, each tree bipartition produces two unions S and T of prescribed vertices. If they overlap, the tree matches no coloring and can be discarded. Otherwise its two complementary monochromatic-side patterns are precisely the two match conditions. Empty unions have their usual vacuous meaning. The extracted obstruction establishes completeness of these clauses, and the inward forcing argument establishes soundness. One-node trees retain maximum cliques wholly in X.

This is an exact constraint system on the original core. Editorial correction: the earlier exponential-size assessment is superseded by the [accepted complexity correction](COMPLEXITY_CORRECTION.md), which proves at most 2|M| clauses and at most 2L literal occurrences. It is not generally the maximum-clique constraint system of the induced graph G[X]. The packet correctly separates that limitation and does not rely on the companion fourth-pass example as a premise or runtime dependency.

## 4. Stronger core conditions: accepted

The accepted addendum supplies q=chi(G[X]) at least 2k-3 and r=omega(G[X]) at least k-1 in every indivisible graph, with r at most k. When k is at least four, q>r. For odd-hole-free G, the induced graph G[X] is C5-free. Applying the accepted sharp bound |X| at least 2q-r+2 gives |X| at least 3k-4, and |X| at least 3k-3 when r=k-1. In particular, k=4 requires at least eight high-incidence vertices. These are necessary conditions, with no existence or sharpness conclusion at this frontier.

At k=4, if G[X] were K4-free, the Chudnovsky–Robertson–Seymour–Thomas four-colorability theorem for K4-free odd-hole-free graphs would give chi(G[X]) at most four, contradicting chi(G[X]) at least five. Thus X contains a maximum K4 without any induced-minimality hypothesis.

This final implication explicitly uses an external theorem, whose statement and source were checked in the pinned accepted maximum-clique-hypergraph audit. The cited author PDF is *K4-free graphs with no odd holes*, JCTB 100 (2010), 313–331, Theorem 1.3, https://thomas.math.gatech.edu/PAP/k4free.pdf, 217,207 bytes, SHA-256 `2e57b496d24fbc04db44d9efc900f3eb5af4843c9f42adadc5e376837be4b504`. This audit does not claim a fresh complete verification of that external proof.

The Hu–Xu–Zhuang preprint is appropriately treated as prior-credit context. Restricted minimal-nonperfect-divisibility statements are not substituted for unrestricted 2-divisibility or clique-cutset closure. No novelty claim is made.

## 5. Independent exact finite verification

The independent checker generates uniform families by cardinality and combinations of edges, rather than by the author's edge-mask traversal. It generates partial colorings by choosing the prescribed subset and then assigning its colors, rather than filtering all ternary words. It reconstructs graph maximum cliques by descending subset cardinality and direct pair containment. Rank-tagged empty hypergraph families and isolated vertices remain distinct within their stated labelled universes.

Instrumentation identifies the author's actual object and partial-coloring calls. The independent object set and case set agree exactly, with no missing or repeated calls:

- 1,078 rank-tagged simple uniform hypergraphs with 3<=r<=n<=5, yielding 90,569 eligible partial colorings.
- All 1,100 labelled simple graphs of orders zero through five, including 660 with clique number at least three, yielding 149,013 eligible partial colorings.
- A combined exact case set of 239,582 records, with the exact serialized case-set identity independently verified. The undistributed raw case-set byte count and hash are omitted from this prose edition.

For every case, a separately implemented full-coloring oracle checks extendability. A separately implemented reverse-order propagator agrees. An independent union-find tree test enumerates all possible selected-subfamily tree clauses, and the existence of a matching clause agrees exactly with nonextendability. Thus the finite check verifies the full obstruction converse, not merely the validity of returned failures.

Every one of the 50,736 returned failure certificates is independently checked. Their combined node-size distribution is 50,086 of size one, 510 of size two, 120 of size three, and 20 of size four. Every successful propagated assignment is checked for an actual full-coloring extension. The successful cases include 3,188 with repeated residual sets.

An independently generated path/star fixture universe agrees exactly with the author's 54 failures and 700 one-prescribed-vertex-flip repairs. Every fixture and repair is checked by independent enumeration over its free edge vertices, and every failed fixture's certificate is checked. Paths reach nine nodes; rank-r stars have r leaves and test branching nodes with no prescribed vertices. These remain abstract hypergraph fixtures, not claims of graph maximum-clique realizability.

Supplemental tests cover all 1,891 eligible partial colorings of simple nonuniform families with original edge sizes at least three on orders zero through four. Seven malformed certificates are rejected by both independent and authored validators: a missing consumer, repeated nodes, unordered nodes, a foreign node, an empty certificate, wrong signs, and two shared outside vertices creating parallel edges. An explicit opposite-singleton-demand example is rejected, while repeated two-vertex residual constraints with opposite demands are satisfied. A rank-two triangle and an unprescribed Fano family demonstrate the necessity of the excluded rank and core-coverage hypotheses.

The author's exact stream hashes and all 54 arithmetic instances are reproduced. These are bounded regressions supplementing the all-size arguments; they neither prove the unrestricted conjecture nor imply that an indivisible odd-hole-free graph exists.

## 6. Optimization resistance, integrity, and sealing

The independent mathematical replay and the exact authored executable both pass under normal Python, -O, and -OO, with byte-identical output within each family. Exact independent and authored output identities were verified; those undistributed replay-output hashes are omitted from this prose edition. No acceptance gate uses an assertion. All five mandatory dependency files, the external pin, manifest, complete packet inventory, regular-file types, and native symlink-free path components are checked before mathematics.

The independent hostile-control harness mutates only disposable copies. It tests every packet member for removal, tampering, symlink substitution and replacement by a directory; every dependency for removal, tampering, direct symlink substitution and parent-directory symlinks; extra files, directories and symlinks; dangling symlinks; missing, changed, symlinked and internal pins; root, ancestor, dependency-root and pin-parent symlinks; duplicate JSON keys; narrowed and missing mandatory scope; missing counts, altered counts and altered stream hashes; changed dependency metadata; wrong executable origin; missing mandatory arguments; and explicitly false mathematical obligations in both the authored and independent checkers. Semantic author mutants are re-manifested and re-pinned to test their semantic gates beyond stale hashes.

There are 73 independent mutation scenarios and 143 required program rejections per interpreter mode, for 429 successful rejections across the three modes. Mode-by-mode outputs and script identities are recorded in the sealed JSON evidence. The author's terminal receipt is verified, and every named evidence member is independently rehashed, including its 56 negative controls per interpreter mode. Original source and dependency bytes are rechecked after the tests.

A separate external review seal fixes the complete review inventory and every file's size and hash. Post-seal verification and seal-hostile-control receipts remain outside the sealed review directory. This certifies a pinned static snapshot and the tested failure modes; it does not claim protection against concurrent hostile filesystem races, every malformed representation, or coordinated replacement of all external trust anchors.

**The exact propagation criterion, complete signed-tree obstruction theorem, exact core clauses, stronger core-order bound, and k=4 core-clique consequence are accepted at their stated scopes. No unrestricted conjecture, clique-cutset closure, graph-shadow odd-hole inheritance, or novelty claim follows.**
