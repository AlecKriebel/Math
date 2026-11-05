Editorial note: This is the complete authored text. Only references to undistributed operational files, their identities, locations and replay directions have been replaced. All mathematical arguments, exact finite counts, corrections and limitations are retained. The public manifest identifies the actual distributed files.

# Correction: the exact signed-tree projection is linear in its explicit incidence input

For problem 3251 / ordered row 1753, the fourth-pass exact-core proof and its acceptance report incorrectly describe their defined signed-tree constraint system as potentially exponentially large when explicitly enumerated. This fifth-pass correction leaves both frozen originals unchanged.

The hypotheses are finite simple G, original maximum-clique list M of clique number k>=3, and prescribed P containing every vertex of original maximum-clique incidence at least three. Make a multigraph on M using one edge for each outside-P vertex of incidence two, retaining parallel edges, and mark a node if its clique contains an outside-P vertex of incidence one.

Every P-tree defined in the fourth-pass proof is necessarily an ENTIRE unmarked tree component of that multigraph. Indeed, including one endpoint forces inclusion of the other for each low-incidence edge; a degree-one occurrence is forbidden; connectedness then leaves exactly one component. Conversely each unmarked tree component satisfies the original P-tree definition.

Thus there are at most |M| underlying obstruction trees. Each yields at most two complementary signed clauses, and the full exact projection has at most 2|M| clauses and twice the input incidence count in literal occurrences. Build it in linear incidence-list time; discard components whose bipartition boundary unions intersect because they can match no assignment.

Only the exponential-size assertion is corrected. The prior exact propagation criterion, necessary-and-sufficient obstruction theorem, failure-certificate extraction and size bound, and soundness/completeness of the core clauses remain valid. The new compression does not establish satisfiability of every formula from an odd-hole-free graph, so it does not solve the general divisibility conjecture. The standalone proof and finite verification are in this packet's the complete proof and the original checker; dependency identities are fixed by the dependency identity record.
