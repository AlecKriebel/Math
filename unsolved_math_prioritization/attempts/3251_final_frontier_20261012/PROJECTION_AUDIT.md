Editorial note: This is the complete authored text. Only references to undistributed operational files, their identities, locations and replay directions have been replaced. All mathematical arguments, exact finite counts, corrections and limitations are retained. The public manifest identifies the actual distributed files.

# Independent acceptance: linear signed-core compression and chordal tree realization

## Decision and fixed scope

**ACCEPTED as all-size partial structural results, with an explicit correction of the prior exponential-size assertion. The unrestricted odd-hole-free 2-divisibility conjecture remains unresolved.**

This audit reviews the fifth/final-pass proof for problem 3251 / ordered row 1753. The exact original proof, external pin, manifest and complete source identity record were independently verified. Their undistributed operational identities are omitted here; the public manifest identifies this distributed edition.

The full proof, standalone correction, verifier, controls, mandatory scope, exact expected data, tree fixtures, and all four identified dependency texts were read. The four dependencies are the unchanged fourth-pass exact propagation/signed-tree proof and its acceptance report, and the unchanged fourth-pass chordal core-division counterexample and its acceptance report. The mathematical use of the first pair explicitly excludes their incorrect exponential-size sentence. No original source or dependency was modified. No remote repository, queue, publication or additional research round was initiated.

## 1. Exact component closure and linear projection

Every outside-P vertex has at most two occurrences in the original distinct maximum-clique family because P contains all vertices of original incidence at least three. A selected P-tree cannot contain a clique with an incidence-one outside vertex. If it contains one endpoint of an incidence-two dual edge, the selected-occurrence condition forces the other endpoint into the selected family. Consequently its node set is a union of entire dual components. Connectedness forces exactly one component, whose full multigraph equals the selected tree. Conversely an unmarked tree component has exactly the selected-occurrence property. This proves equality with the original definition, not merely a sufficient list of certificates.

Important boundary checks are all satisfied:

- Incidence is in the original maximum-cardinality clique family, not a residual family, a maximal-clique list, or the induced core.
- Distinct original sets and repetition-free set membership prevent loops. Parallel edges are retained, and a connected component with two parallel edges is cyclic rather than a tree.
- Incidence-one marks exclude the entire component. Incidence-zero vertices make no dual nodes or edges.
- One-node unmarked components are exactly cliques wholly contained in P.
- Prescribed vertices may appear in several clique nodes or components. Same-side repetitions are deduplicated; occurrence on both sides makes both signed match conditions impossible and warrants discarding that component.
- One boundary side may be empty, including a star with a boundary-free center. Both sides cannot be empty: a finite tree has a node of degree at most one, whereas its original set has size at least three.
- The proof works for disconnected graphs and for nonuniform original distinct sets of size at least three. It does not require odd-hole-freeness.

The accepted fourth-pass signed-tree theorem then makes the complementary signed clause pairs exactly equivalent to extendability of every prescribed coloring. At most m components give at most 2m clauses. The disjoint node sets of the components charge their deduplicated boundary sizes to original P incidences, yielding at most 2L literal occurrences. Components, edge counts, tree bipartitions, and component-index/side stamps give O(n+L) construction in an integer-indexed incidence-list representation. The O(n) term includes isolated graph vertices. Obtaining the original maximum-clique list from a graph encoding is not claimed polynomial.

Every fourth-pass propagation extraction is a P-tree by its accepted theorem, and hence must equal one whole matching component. No proper subtree can serve under the original occurrence condition. The constructive extension theorem still supplies completions, and the O(2^|X|(n+L)) decision bound remains valid after building the projection once. Formula compression alone does not prove satisfiability for all odd-hole-free inputs or a polynomial-time algorithm for that question.

The empty-formula corollary is sound: when every component is marked, cyclic, or has overlapping boundary unions, every prescribed coloring extends. The k-uniform tree incidence identity is kt-2(t-1)=(k-2)t+2; it counts prescribed incidences, not necessarily distinct prescribed vertices.

## 2. The explicit correction and unaffected fourth-pass conclusions

The fourth proof's Section 3 sentence “It can be exponentially large if explicitly enumerated” is false for the system it defines. The corresponding sentence in Section 3 of its acceptance report is also false. Its opening “No mathematical correction is required” is qualified by this correction. Both historical originals are preserved byte-for-byte.

The complete accepted complexity correction is separately fixed and suitable for attaching beside the unchanged originals. Its exact source and separate correction pin were verified. It intentionally contains none of the new realization theorem.

The previous exact propagation theorem, complete obstruction characterization, extraction bound, and signed-clause soundness/completeness remain valid. The stronger core-order bound and k=4 core-clique consequence use independent arguments and remain valid at their stated dependency scope. The separate chordal counterexample to extending every division of the induced core is also unaffected. The correction improves the size assessment without changing the set of extendible prescribed colorings. No unconditional conjecture, clique-cutset closure, graph-shadow inheritance, novelty, or minimality claim follows.

## 3. Arbitrary bounded-degree-tree realization

For k at least three and any nonempty tree T of maximum degree at most k, place one vertex on each tree edge. Fill the bag at each node a with k-deg(a) fresh distinct prescribed vertices. Attach two support k-bags at each such fresh vertex, each with its own k-1 private vertices. The auxiliary bag tree consists of T with these support leaves.

A graph vertex's containing bags form a connected subtree: an edge vertex uses its two endpoint bags; a prescribed vertex uses its base bag and two support leaves; a private vertex uses one bag. Adjacent bags intersect in exactly one vertex. Leaf-bag elimination therefore removes simplicial vertices and supplies a perfect elimination order. At the first eliminated vertex of any graph clique, all later members of that clique lie in its elimination bag; thus every clique is contained in a displayed bag. The displayed k-bags are distinct and therefore exactly the maximum cliques. These arguments prove chordality and exactness for all sizes, rather than assuming an arbitrary bag family is an exact graph clique family.

Original incidences are precisely three for the fresh prescribed vertices, two for tree-edge vertices, and one for support-private vertices. Therefore the exact high-incidence set is the prescribed set C. Its size is c=kt-2(t-1)=(k-2)t+2. The dual has T as its unique unmarked component and 2c marked isolated support components. The boundary groups C_a are disjoint, so its complementary pair forbids exactly two full colorings of X=C. Exactly 2^c-2 core colorings extend. This includes the one-node case and stars with an empty center group.

The counts n=t-1+(2k-1)c, m=t+2c and |E|=(t+2c)binom(k,2) are correct. No graph edge is counted twice because two distinct bags share at most one vertex. The induced core is the disjoint union of the groups C_a. For t at least two its clique number is k-1, attained at the leaves. The two bad core prescriptions make these leaf cliques monochromatic, so they are not divisions of the induced core at its own clique number. The realization is therefore not an additional counterexample to arbitrary core-division extension.

The graph is connected, chordal and divisible. A direct division follows by coloring a root bag with both colors and extending over each one-vertex bag separator with an opposite-colored new vertex. Consequently arbitrary order, long paths and degree-bounded branching of an obstruction component are compatible with chordality, without suggesting an indivisible chordal graph.

## 4. Independent mathematical computation

The independent checker imports no authored mathematics. It enumerates families by combinations of edges, prescribed subsets by descending submasks, full-coloring models directly, selected-subfamily trees with an independent disjoint-set forest test, and complete dual components by a separate breadth-first traversal. It reconstructs graph maximum cliques by descending subset size and direct adjacency tests. For each partial coloring, a reverse-order propagator extracts its own certificate and checks that it is an entire matching component.

The three independent exact universes agree with the source totals:

- 1,078 rank-tagged uniform families on at most five vertices, 7,694 prescribed sets and 90,569 partial colorings, with 35,334 failures.
- All 1,100 labelled graphs on at most five vertices, including 660 eligible graphs, 19,288 prescribed sets and 149,013 partial colorings, with 15,402 failures.
- 37 nonuniform families on at most four vertices, 341 prescribed sets and 1,891 partial colorings, with 280 failures.

Thus 241,473 partial colorings and all 51,016 extracted failures are checked independently. Raw definition trees and component trees agree for every prescribed set, including the 4,014 tree instances discarded for overlapping boundary unions. Nine targeted fixtures cover parallel edges, a mark-poisoned pair, opposite-side prescribed sharing, same-side prescribed sharing with a boundary-free star center, a simple cycle, a component with no prescribed vertices, a singleton, disconnected trees, and the empty family. Three out-of-scope inputs reject duplicate original sets, uncovered high-incidence vertices, and rank-two sets.

A separate independent Prüfer-tree realization checker constructs all 433 labelled-tree/rank fixtures of orders one through five for ranks three, four and five with maximum degree at most the rank, plus longer paths through twelve nodes and rank-sized stars: 457 graphs in total. It reconstructs maximal cliques from adjacency, independently verifies chordality by maximum-cardinality-search elimination, and checks all incidences and size formulas. It checks 43,514 graph vertices in aggregate. All 7,400 core assignments on its fixtures of at most three tree nodes are tested by direct enumeration of free base-edge colors.

A further independent exact-source fixture check reconstructs the author's 19 path/star/broom graphs and tests all 79,016 core assignments by free-edge enumeration. Its 38 failures and full deterministic case-stream SHA-256 `[verified identity of undistributed artifact]` agree exactly with the authored expectation. The frozen authored checker additionally computes the exact projection by Davis-Putnam elimination and verifies full graph witnesses for every successful realization coloring. None of these bounded checks substitutes for the all-size proofs.

## 5. Optimization, identity, and tested hostile controls

The frozen author replay, independent compression/extraction oracle, independent realization universe, and independent exact-author-fixture oracle pass under normal Python, -O and -OO, with byte-identical mathematical outputs in each family. All acceptance gates use explicit exceptions. An independent fixed-pin source checker verifies every packet member, complete inventory, native nonsymlink file types and path components, and the four exact dependencies in all modes.

The independent disposable-copy mutation suite checks removal, alteration, symbolic-link substitution, and directory substitution for all nine packet members; removal, alteration, direct and parent symbolic links for all four dependencies; extra files/directories/links; dangling and ancestor symlinks; missing, altered, linked, interior and wrong-hash pins; duplicate JSON keys; narrowed or wrongly typed mandatory scope; altered/missing expected values; dependency metadata; altered/missing fixtures; wrong executable origin; missing individual CLI arguments; and explicitly false mathematical obligations in the author and both independent mathematical checkers. Semantic mutants are re-manifested and re-pinned to reach semantic gates instead of only stale-hash rejection.

The independent suite requires 85 mutation scenarios and 165 program rejections per interpreter mode, 495 rejections total. The original source and dependencies are checked again afterward. External author-control receipts are independently rehashed when supplied; this audit's own mutation suite is the independently executed control evidence.

The audit inventory is fixed by a separate externally retained review seal. Post-seal normal/-O/-OO checks and seal-hostile-control receipts are kept outside the sealed directory. This is static-snapshot integrity and evidence for the declared controls, not protection against hostile concurrent filesystem races, coordinated replacement of all trust anchors, or every malformed representation.

**Final scope:** the exact linear projection, its correction of the historical complexity assessment, and the stated all-size chordal realization are accepted. The unrestricted target remains unresolved; no new global satisfiability theorem is inferred.
