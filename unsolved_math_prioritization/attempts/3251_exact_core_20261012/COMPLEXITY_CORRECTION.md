Editorial note: The complete authored proof or audit is preserved below. Changes replace only operational artifact identities, byte counts, locations and original replay directions. All mathematical arguments, exact finite scopes and substantive limitations remain. This edition's public manifest identifies the distributed prose.

# Accepted correction: the exact signed-tree projection has linear input-list size

## Independent decision and precise boundary

**ACCEPTED as an all-size correction to the representation-size statement in the fourth-pass exact-core theorem.** The original propagation criterion, signed-tree characterization, certificate extraction and size bound, signed-clause soundness and completeness, and stronger core-order and core-clique consequences remain accepted at their original scopes. This correction does not settle the unrestricted odd-hole-free 2-divisibility conjecture and does not claim that the compressed signed formula is always satisfiable.

This statement concerns problem 3251 / ordered row 1753. It supersedes exactly the assertion “It can be exponentially large if explicitly enumerated” in Section 3 of the fourth-pass exact-core proof and the corresponding “can be exponentially large” assertion in Section 3 of its acceptance report. The acceptance report's opening “No mathematical correction is required” must therefore be read subject to this representation-size correction. Neither frozen original is modified.

The exact original [proof](EXACT_CORE_PROOFS.md) and [acceptance report](EXACT_CORE_AUDIT.md) were identified and byte-checked. Their original operational hashes and byte counts are omitted from this prose edition; its public manifest identifies the distributed versions. Their exact extension and extraction statements, rather than the erroneous size sentence, are used below.

## Statement and proof

Let M be the family of distinct original maximum cliques of a finite simple graph, of clique number at least three. Let P contain every vertex with incidence at least three in M. Equivalently for this argument, use any explicitly supplied finite family of distinct sets of sizes at least three, with every vertex outside P occurring in at most two original sets. Put m=|M| and L equal to the total number of original incidences.

Construct a multigraph D on the original members of M. An outside-P vertex of incidence two gives one edge between its two containing members; retain parallel edges. An outside-P vertex of incidence one marks its containing node. Incidence-zero vertices do nothing. There are no loops, because a set has no repeated membership. The construction uses the original family, not incidences recomputed after deletions.

**Claim. The P-trees in the fourth-pass definition are precisely the entire unmarked tree components of D.**

If F is a P-tree, it contains no marked node: a corresponding incidence-one vertex cannot acquire the two selected occurrences required by the definition. For every dual edge with an endpoint in F, the other endpoint must also belong to F, because its label has only those two original occurrences and must have two selected occurrences. Thus F is a union of complete connected components. Its own connectedness makes it exactly one component. All edges of that component are present in its selected multigraph, which is a tree by hypothesis. Conversely, in an unmarked tree component every outside-P vertex that occurs has incidence two, both endpoints are in the component, and its selected multigraph is exactly that tree. This proves both directions.

Consequently there are at most m P-trees. For each such component, bipartition its clique nodes and form the two unions S and T of their prescribed vertices. If S intersects T, neither signed orientation can match a prescribed coloring, and this component is discarded. Otherwise the two signed match patterns are S all zero and T all one, and their complement. Each is forbidden by one clause. By the accepted exact signed-tree theorem, the conjunction of these complementary clause pairs is equivalent to extendability of the prescribed coloring.

There are at most 2m clauses. Repeated vertices within a boundary union are included only once. Components have disjoint clique-node sets, so the sum of |S|+|T| over retained components is at most the number of original P incidences, at most L. The two complementary clauses per component therefore use at most 2L total literal occurrences.

With integer-indexed vertex and incidence lists, build D, its marks, components, edge counts, tree bipartitions, and boundary unions in O(n+L) time and space. Component-index stamps and side bits avoid scanning all P separately for each component. This is linear in the explicit incidence-list support, with an O(n) term when all graph vertices, including isolated vertices, are supplied. It makes no polynomial-time claim for obtaining the original maximum-clique list from a graph encoding.

## Edge cases and consequences

- Parallel edges give a two-cycle and exclude treehood; they must not be merged.
- A one-node unmarked tree is exactly a maximum clique wholly contained in P.
- One bipartition side may have empty boundary. Empty conditions are vacuous. Both sides cannot have empty boundary: a finite tree has a degree-at-most-one node, whose original set has at least three vertices and therefore contains a prescribed vertex.
- A prescribed vertex may recur at different clique nodes. Recurrence on one side is deduplicated; recurrence on both sides makes both signed patterns impossible, so discarding is sound.
- Distinct original clique identities are essential to the stated family; duplicate rows are not silently added to incidence counts. Residual duplicates created later by propagation are a separate matter and do not alter this construction.
- Every fourth-pass extracted failure certificate satisfies the original P-tree definition and is therefore an entire unmarked component, never a proper subtree of such a component.
- The exact O(2^|X|(n+L)) input-list decision bound remains valid. Linear formula construction does not establish polynomial-time satisfiability or a solution to the unrestricted conjecture.

The former exponential estimate overlooked closure under every outside-P incidence-two edge. It is a correction to the size assessment of the exact formula, not a change to which prescribed assignments extend.

## Independent finite checks supporting the proof

An independent checker exhausts the original selected-subfamily definition and compares it with a separately implemented complete-component construction. For every eligible prescribed assignment it also checks a whole-coloring oracle, reverse-order propagation, and the statement that the extracted obstruction is a whole matching component. It passes all 90,569 eligible partial colorings of the 1,078 rank-tagged uniform families of rank at least three on at most five vertices; all 149,013 eligible partial colorings of the 660 graphs of clique number at least three among all 1,100 labelled graphs on at most five vertices; and all 1,891 eligible partial colorings of the 37 nonuniform families of set size at least three on at most four vertices. These finite checks supplement the all-size proof above and are not its logical basis.

This standalone correction intentionally contains no additional fifth-pass realization theorem. It accompanies the complete fourth-pass proof and audit, whose public editions clearly mark this correction while preserving their full original text reversibly.
