# Independent audit of shortest mixed round trip orientation

Problem 3000061 / AMR-029-0061, first substantive attempt. Audited 10 October 2026.

## Decision

**PASS as a scoped PARTIAL result. No mathematical correction is required to the frozen report.** The general deterministic exact polynomial-time question is not solved by this packet; no target hardness theorem or novelty claim is accepted.

The original audit authenticated the complete accepted input packet without modifying it. This public edition preserves all analytic arguments and binds the distributed report [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md): 22,268 bytes; SHA-256 `8b1a7825c65b1500018e9bc895e67c3fb533c769092a49233280bf86fb3016d1`. [ACCEPTANCE.json](ACCEPTANCE.json) records the exact distributed report and audit identities. Editorial changes remove unavailable-file references and distinguish recorded checks and source observations from edition preparation. This AI-assisted audit is unrefereed; acceptance is not external human peer review, journal acceptance, or formal proof-assistant certification. No mathematical proof correction was required.

The accepted model is an explicit finite mixed multigraph with independently orientable undirected edge identities, immutable fixed arcs, and nonnegative binary-encoded rational lengths, including zero. Only the two terminal directions are required. The same directed edge or fixed arc may occur in both component paths. Parallel edges, loops, disconnected irrelevant pieces, infinite distances, and equal terminals have the conventions stated in the report.

## Independent mathematical verification

### Shortest walks and the role of zero lengths

For a fixed orientation and distinct reachable endpoints, deleting a repeated-vertex closed subwalk never increases length. Repeated deletion produces a simple directed path. Zero-length cycles do not invalidate this argument: deletion need not strictly improve the objective. There are finitely many completions of the undirected edges, and finitely many simple paths, so every finite optimum is attained. Nonnegative loops can therefore be discarded without changing any terminal distance; fixed loops stay fixed and undirected loops can be completed arbitrarily on output. When the terminals coincide, both distances are zero independently of all other reachability.

These facts justify every subsequent simple-path argument. They do not make the concatenated outward and return paths simple or edge-disjoint.

### Articulation decomposition

The required blocks are vertex-biconnected edge sets, with each bridge its own block and a pair of parallel edges forming a two-edge cycle. They are not merely the components remaining after bridges are removed. Their block-vertex incidence graph is a forest.

Fix any orientation. A simple terminal-to-terminal path cannot enter a block attached to the block-tree route at a single vertex and later escape, because it would repeat that articulation vertex. It must visit the relevant blocks in their unique route order, and its restriction to each block connects that block's two route attachment vertices. Conversely, choosing those local paths and concatenating them gives a valid global path or walk. Thus each directed distance equals the sum of the corresponding local distances, including infinity.

The block edge sets are disjoint. Minimizing the sum of the two directional distances may therefore be done independently in each relevant block, and all local optimal orientations extend to one full orientation. This proves Theorem 1, including its feasibility assertion. A bridge cannot carry a trip in both directions. No condition is imposed on the orientations or connectivity of off-route blocks.

### The undirected lower bound

Let H be the union of the distinct underlying edge identities of two feasible directed terminal paths. Every terminal-separating cut of H has at least two physical edges. With only one edge, outward and return paths would have to traverse the same oriented edge in opposite directions. This remains impossible if the edge is fixed, and remains true when some other edge is traversed by both paths in the same direction.

The edge form of Menger's theorem supplies two edge-disjoint undirected terminal paths in H. Nonnegative weights give the chain of inequalities

- their total weight is at most the weight of all distinct edges in H;
- that distinct-edge weight is at most the weight of the original two paths, counted with multiplicity.

Hence L is a valid lower bound on every oriented round trip. An infinite L proves infeasibility. Parallel edge identities must be preserved for this statement.

### Two-unit min-cost flow and cycle extraction

Replacing each physical edge by two independent unit-capacity network arcs initially permits an apparently invalid solution that uses both directions of that physical edge. This relaxation is nevertheless exact for the undirected two-path problem. Cancel equal antiparallel units, preserving every vertex balance and lowering the cost by twice a nonnegative edge weight. Remove all remaining directed positive-support circulation cycles. Since the starting flow was globally minimum-cost at value two, these removals cannot produce a cost below that minimum. Thus the final acyclic support has the same optimum cost.

Acyclic integral support of value two decomposes into two edge-disjoint simple source-to-sink paths. After those two paths are removed, any remainder would be a nonempty balanced acyclic digraph, which is impossible. The result uses at most one orientation of each original physical edge. Conversely, any physical edge-disjoint path pair is feasible in the network, proving equality of the two optima.

Two successive shortest residual augmentations suffice. A minimum-cost integral flow of a fixed value has no negative residual cycle. The difference to a flow of one larger value decomposes into a source-to-sink residual path plus circulation cycles. The latter have nonnegative cost; a shortest residual path is therefore an optimal augmentation. This argument applies at values zero and one, including zero costs and negative-cost residual reverse arcs. Bellman–Ford is suitable; nonnegative-edge Dijkstra without suitable potentials would not be justified for the second augmentation.

The two acyclic support paths have the same order of common vertices. Opposite ordering would produce a directed closed walk, hence a directed cycle. Between consecutive common vertices, their internally disjoint segments form a simple physical cycle, including a parallel two-edge cycle. These cycles meet only at successive common vertices and have disjoint edge identities.

If each such cycle has consistent fixed directions, orient it cyclically. A directed cycle supplies both directions between its attachment vertices. Concatenating along the chain supplies an actual terminal round trip of total weight L. Completing unused edges cannot invalidate the witness and cannot lower the optimum below L, by the already proved lower bound. This establishes exact attainment, not just an upper-bound construction.

If a cycle has inconsistent fixed directions, this certificate returns unknown. No conclusion of infeasibility or suboptimality follows. In particular, the zero-weight obstruction below has OPT equal to L but does not possess a compatible edge-disjoint round trip.

### At most one fixed arc per relevant block and cacti

Every simple cycle lies in one underlying vertex-biconnected block. Every edge of the extracted cycle chain lies on a simple underlying terminal path, so its block is relevant. Under the one-fixed-arc condition, each extracted cycle has either no direction constraint or exactly one. One of its two cyclic orientations always satisfies that constraint. Disjoint edge sets make the selected orientations compatible. This proves Theorem 3 and its constructive deterministic polynomial algorithm. The restriction is per relevant block; arbitrarily many fixed arcs may occur in other blocks.

For a cactus, each relevant nonbridge block is one simple cycle. The only two simple attachment-to-attachment paths are its two sides. A feasible trip must use different sides, since using one side in both directions would contradict orientation. Consequently every cycle edge is used, the whole cycle must be cyclically oriented, and all fixed arcs must agree with that cyclic direction. This condition is sufficient as well as necessary. The cost is the sum of the weights of all relevant cycles, even when some weights vanish. An infeasible relevant block makes the whole instance infeasible. The audit records separate finite verification of this specialization on arbitrary fixed directions, bridges, and parallel two-edge cycles.

### Three-state series-parallel dynamic program

The supplied expression must genuinely realize the input graph: each edge occurs once, the prescribed terminal identifications are respected, and otherwise child vertex sets are disjoint. This is an explicit hypothesis. The checked implementation is not being certified as a validator for malformed decompositions or as a recognition algorithm for arbitrarily chosen terminals in an underlying series-parallel graph.

The three states minimize a forward distance alone, a backward distance alone, or the sum in one common orientation. The orientations realizing A, B, and C may differ. A single undirected edge has finite A and B but infinite C, even if its weight is zero.

At a series node, every simple forward or backward terminal path uses the articulation vertex and traverses both children. Each directional distance adds. A round trip requires both directions in both children. Independent child edge sets give exactly A=A1+A2, B=B1+B2, and C=C1+C2.

At a parallel node, a simple outer-terminal path stays inside one child. A switch would revisit its source or would already have reached its destination. The two directional paths consequently fall into exactly four cases: both in the first child, both in the second, forward in the first and backward in the second, or the reverse assignment. Their costs are bounded below by C1, C2, A1+B2, or A2+B1 respectively. In each finite case, independent child witnesses realize that bound. Taking the minimum therefore proves the claimed recurrence in both directions.

A witness pointer records one minimizing case for each finite state. Reconstructing the root C witness requests either one child C state or complementary one-way states in separate children, or C states in both series children. No leaf is simultaneously requested in conflicting directions. Unused free edges are completed arbitrarily and every fixed arc retains its direction. The actual distances in the reconstructed full orientation equal the state value: the constructed paths give the upper bound, and the recurrence's universal lower-bound proof rules out a better value.

There is no unrecorded Pareto frontier needed on these valid two-terminal compositions. The argument does not extend to children with additional shared boundary vertices.

### Binary-rational running time

Let q_e be the positive denominator of input length p_e/q_e. The product Q of all q_e has bit length bounded by the sum of input denominator bit lengths. Exact integer scaling by Q is a conceptual bit-complexity bound, not a subdivision of edges. Finite optimal path-pair values have denominators dividing Q and are sums of at most two simple paths, hence polynomial-size numerators and denominators. Residual path costs are signed sums of the same input lengths. Bellman–Ford performs polynomially many rational additions/comparisons, each with polynomial-size exact values; there are only two augmentations. Cancelling cycles and reconstructing paths and orientations also takes polynomial time.

The supplied series-parallel expression has three scalar values and constant many transitions per node. Stored pointers permit linear combinatorial reconstruction; exact arithmetic adds only polynomial bit overhead. The recorded demonstrator copies orientation maps and uses recursive routines, so its implementation need not realize the tight linear pointer bound or avoid Python recursion limits on arbitrarily deep inputs. Those implementation choices do not invalidate the stated polynomial algorithm or the finite check claims.

### Shared-edge obstruction

In the four-vertex graph, orienting ab from b to a leaves s and t unable to reach one another. Orienting it from a to b forces the simple paths s,a,b,t and t,a,b,s. The four unit arcs are each used once in their sum and ab is used twice, giving 4+2M. The underlying pair through a and through b costs four. Every undirected edge-disjoint terminal pair uses the two distinct incident unit edges at each terminal, so no such pair is cheaper.

For M>0 the ratio to the lower bound is 1+M/2, which is unbounded. At M=0 the lower bound is attained in value, but each feasible round trip still uses ab twice. There is no simple directed cycle through both terminals. The finite feasible orientation is strongly connected on the four vertices, so no global connectivity issue explains the gap.

The audit additionally fixed ab in the successful direction and recovered the same formula. This confirms that fixed arcs, as well as oriented undirected edges, may be used by both component paths. It is an implementation control, not an additional general tractability result.

### Arbitrary two-pair connector reduction

Fix an arbitrary orientation of the original graph H. The new s has only the outgoing connector to a, and the new t has only the incoming connector from b. Every simple s-to-t path begins and ends with those connectors. It cannot use the connector from t to c before its last vertex, and cannot use the connector from d to s without repeating its source. Its middle therefore stays inside H and connects a to b. Conversely, every such H path extends to a new terminal path with unchanged cost. The same argument, with roles exchanged, handles the return direction.

This proves the two individual distance equalities, not merely equality after minimization. It covers nonreachability, shared original terminals, and empty middle paths such as a=b. The new terminals are fresh and distinct. All four connectors are fixed directed zero-cost arcs; replacing them by freely orientable or bidirected edges would require a different argument. Completing H is the only choice, so the reduction preserves exact values and witnesses. Taking requests (s,t) and (t,s) is the reverse reduction.

The equivalence is to arbitrary **mixed** two-pair min-sum orientation. It does not transfer an undirected theorem, a feasibility result, or a separate-length-bound hardness result to the current objective.

## Primary source scope

All source retrieval and inspection statements in this section describe the recorded original audit. Edition preparation performed no new scholarly-source retrieval, source-file rehash, source inspection, or literature search.

The retained original EGRES HTML was read directly, as well as its extracted statement and discussion. Its hashes match the submitted source metadata. The original asks for minimization of the sum of the two opposed directed distances in a mixed graph with nonnegative lengths. The binary-rational model is the packet's explicit computational normalization. It does not add a demand for global strong connectivity or edge-disjoint component paths. Public source: https://oldlemon.cs.elte.hu/egres/open/Orientation_with_shortest_round_trip

Hassin–Megiddo's original PDF was checked through its abstract, Section 4's positive-length ideal-orientation hypotheses, and Section 5's distinct separately bounded and prescribed-subgraph problems. The first PDF page was visually inspected. The report's restrictions are accurate; those results are not a general mixed min-sum algorithm. Public source: https://theory.stanford.edu/~megiddo/pdf/orientat.pdf

Fenner–Lachish–Popa's retained PDF was checked through its abstract, Section 2's edge-count definition of path length, and Theorems 19–21. The first PDF page was visually inspected. The relevant input is undirected and unweighted. Its PTAS and reduction do not authorize the claimed general mixed binary-weight optimization. Public source: https://www.dcs.bbk.ac.uk/~oded/papers/MS2POP.pdf

Björklund–Husfeldt's retained PDF was checked through its abstract and Section 1.1; PDF page 2 was visually inspected. Its stated general input is loopless, unweighted, undirected, and simple, and the general algorithm is Monte Carlo. The special deterministic treatment assumes a unique optimum. Public source: https://thorehusfeldt.files.wordpress.com/2010/08/spdp-e5d5661.pdf

A fresh primary publisher result for Arkin–Hassin exposed the introduction and Theorem 2.2, confirming polynomial orientation feasibility for two prescribed pairs. It does not provide a length-minimization theorem. The report's statement that its earlier retrieval lacked a certified full proof remains an accurate limitation of that attempt; this audit does not retroactively claim a complete proof audit. Public source: https://www.sciencedirect.com/science/article/pii/S0166218X01002281

Direct web reopening of the EGRES URL and DOI resolver failed during this audit; retained source bytes and the separate publisher result supplied the relevant scope. No copied source document or source text is included in this authored audit. No exhaustive literature or current-worldwide-open conclusion is drawn.

## Recorded supplementary checks and negative controls

The audit records an unchanged replay of the original checks under ordinary and optimized Python, with byte-identical outputs matching the accepted result: 41,957 graph/terminal cases, including 600 rational multigraph cases; 23,963 arc-sparse cases; 500 series-parallel inputs with 863 finite-state witnesses; and 509 connector orientation checks. Programs and raw generated outputs are not distributed. Edition preparation did not rerun these mathematical checks.

The audit records separately implemented checks that did not use the submitted orientation oracle, distance routine, relevant-block routine, or random expression generator. They used exhaustive orientation enumeration with Floyd–Warshall, simple undirected path enumeration for L, cycle-equivalence construction of blocks, and independently generated series-parallel expressions. The recorded ordinary and optimized runs were byte-identical and passed:

- All 4,165 simple mixed graphs on one through four vertices, with slot-dependent zero/rational weights including a 198-bit numerator: 41,357 terminal cases.
- 360 further rational multigraphs with loops, parallel identities, zero weights, and larger numerators/denominators, plus a targeted irrelevant-branch graph: 45,599 terminal cases total.
- 27,039 cases satisfying the relevant-block one-arc condition.
- All 3,477 series-parallel expressions through four leaves across binary shapes, series/parallel choices, and three leaf types, plus 300 larger generated expressions: 3,777 inputs and 6,469 finite-state orientations checked.
- Every directed graph on three vertices with possible antiparallel arcs, tested at all 81 ordered two-pair requests: 5,184 requests and 10,368 separate distance equalities, including coincident terminals.
- Six zero/rational/large-weight shared-element cases, treating the shared element both as undirected and as fixed.

A separate cactus implementation was tested against its own exact orientation oracle on 420 generated mixed cacti: 213 finite orientation witnesses and 207 infeasible cases, including 95 equal-terminal cases and parallel two-edge cycles. Its normal and optimized outputs also match.

Seven concrete semantic controls reject shortcuts: replacing C by A+B; omitting cross-child parallel terms; collapsing parallel edge identities; treating fixed directions as irrelevant to orientation; calling failed certificates infeasible; demanding global strong connectivity; and treating one-way reachability as a round trip. Four independent integrity controls reject payload corruption, attacker-resealed payloads, unlisted files, and a wrong external pin. These tests use explicit exceptions, not optimization-removable assertions.

Finite checks are corroborating implementation evidence. Acceptance of the scoped partial results rests on the complete analytic proofs above and the report's matching arguments. Aggregate coverage and review limits are retained in [ACCEPTANCE.json](ACCEPTANCE.json); no omitted executable is required for the mathematical arguments.

## Accepted and unaccepted conclusions

Accepted: exact articulation decomposition; the undirected lower bound and sound cycle-chain certificate; the deterministic one-fixed-arc-per-relevant-block algorithm; the exact supplied two-terminal series-parallel dynamic program; the cactus specialization; the shared-edge obstruction; and the exact mixed two-pair equivalence.

Unaccepted because not established or not claimed: a polynomial exact solver for arbitrary mixed blocks, hardness of the target, a complete recognition theorem for arbitrary terminal placement, global novelty, or a current exhaustive literature status. The packet remains PARTIAL, attempt 1. The original audit performed no publication or queue modification; this edition likewise changes no queue entry.
