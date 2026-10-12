# Fifth and final pass on the odd hole free divisibility frontier

Problem 3251, ordered queue row 1753. Status: unsolved. Five substantive passes in the recorded sequence are confirmed; the lifetime attempt count is unknown. The main investigations and the separately audited repeated-leaf supplement belong to this same fifth and final pass. No sixth research pass is included.

The target asks whether every finite simple odd-hole-free graph with at least one edge admits a two-coloring avoiding monochromatic maximum-cardinality cliques. Maximum means maximum cardinality, not inclusionwise maximal. This is different from perfect divisibility. No full solution, counterexample to the target, novelty, minimality, latest-best bound or human-review claim is made.

## Accepted frontier

- [Exact linear projection and chordal realization](PROJECTION_PROOFS.md), with its [complete independent audit](PROJECTION_AUDIT.md): every obstruction tree is a whole unmarked component of the original low-incidence dual multigraph. For m original maximum cliques and L original incidences, the exact signed projection has at most 2m clauses and at most 2L literal occurrences, constructed in O(n+L) time and space from the supplied incidence list. This does not prove satisfiability. Every bounded-degree tree is realizable as the unique effective obstruction component of a connected chordal, divisible graph.
- [Structural bounds and critical joins](STRUCTURAL_PROOFS.md), with its [complete independent audit](STRUCTURAL_AUDIT.md): for k>=5 an odd-hole-free indivisible graph has at least 3k-3 original high-incidence core vertices, or at least 3k-2 if the core clique number is k-1. Equality has the stated critical-join form. At k=4 an eight-vertex core would be K1 joined to a seven-vertex 4-critical odd-hole-free graph with clique number three and connected complement. This narrows the boundary and does not exclude it.
- [Separate repeated-leaf supplement](REPEATED_LEAF_PROOFS.md), with its [complete independent audit](REPEATED_LEAF_AUDIT.md): for each k>=4, a connected odd-hole-free, divisible graph has exactly two bad prescribed core colorings, each with exactly one monochromatic (k-1)-clique. At k=4 it has nine core vertices and 58 graph vertices. These bad prescriptions are not divisions of the induced core and do not address the eight-core frontier.

The [authored correction](AUTHOR_CORRECTION.md) and [complete accepted complexity correction](COMPLEXITY_CORRECTION.md) openly supersede the fourth proof and audit's false exponential-size assertion. The original propagation, signed-tree equivalence, extraction bounds and extension statements remain valid. The frozen originals have not been rewritten. Linear representation size is not a satisfiability theorem or a polynomial-time claim for enumerating maximum cliques from graph input.

The structural proof imports the published Bikov–Nenov Theorem 5.2, F_v(4,4;5)>=19. Thus every k=4 indivisible graph has at least 19 vertices, without an odd-hole assumption. Its large external enumeration was not replayed. The elementary n>=4k-3 deduction is not presented as a best-known numerical Folkman bound. Gallai and CRST are also external theorem dependencies; see [source credit and limits](SOURCES.md).

For a minimal odd-hole-free indivisible graph, clique-cutset sides have at least 13 vertices when k=4 and at least 3k+2 when k>=5. Accordingly, k=4 clique and edge cutsets require at least 22 and 24 vertices in total; for k>=5 the corresponding bounds are 5k+4 and 6k+2. These are necessary bounds and do not prove cutset exclusion or gluing.

General odd-hole-free 2-divisibility and the k=4 eight-core case remain open within this work. All constructed chordal and repeated-leaf examples are divisible. Universalness inside the core is not universalness in the whole graph.

## Complete texts and verification

This edition distributes all complete fifth-pass proofs and acceptance reports, both necessary correction texts, and the [complete scholarly source audit](SCHOLARLY_SOURCE_AUDIT.json). Operational references are transformed reversibly without abridging mathematics. It includes [exact finite coverage](VERIFICATION_SCOPE.md), [small authored examples](SMALL_EXAMPLES.md), [dependencies](DEPENDENCIES.md), and [acceptance boundaries](ACCEPTANCE_AND_SCOPE.md).

Only the distributed prose and public scholarly PDFs receive public identities. No original code, raw datasets, control files, replay receipts, private coordination material or copied third-party source documents are distributed. The reported original computations were independently audited in their frozen setting; this is a prose edition, not a standalone exhaustive replay package.

Earlier companion texts are the [initial edition](../3251_divisibility_partials_20261012/README.md), [third-pass edition](../3251_boundary_core_20261012/README.md), and [corrected fourth-pass edition](../3251_exact_core_20261012/README.md). These links specify the repository layout; this preparation does not claim any new remote publication or integration.
