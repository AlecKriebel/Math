# Independent mathematical acceptance: second labeled-die pass

## Verdict

Accepted as structural and algorithmic partial results for the fully labeled, hole-free rectangular rolling-die Hamiltonian-path problem with a specified corner start and fixed die chirality:

1. The exact forced-chain multigraph kernel with at most 2k nodes and 3k−1 optional edges, where k is the surviving candidate graph's cycle rank.
2. Complete affine cycle-space enumeration of at most 2^k optional-edge sets, with separate degree, physical-port, full-state and selected-connectivity tests; polynomial preprocessing plus O(k 2^k) time per conditioned endpoint/state branch.
3. Universal endpoint migration for a nontrivial neutral detour between physically adjacent ports.
4. The unique fully covered vertical-serpent ribbon of every even width and height congruent to 3 modulo 4, including selectable initial orientation and the neutral nonadjacent-port subfamily of widths divisible by 4.
5. The same/opposite-pair insulating-collar obstruction beside a straight rail of length at least four in the rail's intended phase.
6. The compatible eight-cycle theorem: every such cycle in a solution's simultaneously assigned orientation field is a 3-by-3 perimeter whose center is the final endpoint; hence at most one exists.

This does not classify the unrestricted problem, prove hardness, give a general polynomial algorithm, establish new global uniqueness, or certify worldwide novelty. General contraction and binary-cycle-space methods are not claimed as new. The positive ribbon has no choice mechanism, and its external boundary isolation has not been implemented in a complete no-hole reduction.

This report records the independent acceptance of the underlying second-pass mathematical results. The present editorial edition retains that proof challenge and replaces implementation and packaging references with the public proof and certificate references. The edition's [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) binds its public files. The proof challenge below is substantive; hashes alone are not the basis of acceptance.

## Exact model and dependency boundary

Coordinates increase east and north. Full orientations are `(top,bottom,north,south,east,west)` with reference `(1,6,2,5,3,4)`. Every initial and landed-on top must match its cell, every rectangle cell is used once, and no revisit or closing roll is allowed. Fixed and selectable initial orientations are distinct variants. The final endpoint and state are explicitly conditioned for the kernel.

The already accepted first-pass unique-state-edge, phase-parity, sound propagation and checkerboard-area facts were reread. The needed orientation facts are restated in [FOUNDATIONS.md](FOUNDATIONS.md); the first edition retains the [full structural theorem](../5500068_labeled_die_first_20261013/ORIENTATION_STRUCTURE.md) and its [independent review](../5500068_labeled_die_first_20261013/INDEPENDENT_STRUCTURE_REVIEW.md). The second-pass arguments do not replace full-state compatibility by phase-projection compatibility. In particular, projection six-cycles are not treated as physically closed rolling cycles.

## Complete kernel proof challenge

### Propagation and forced components

Two adjacent nonopposite face labels and a direction determine one full transition in the fixed chirality. Thus different retained states at one cell cannot share a physical candidate edge. A valid nonendpoint needs two distinct edges in one full state, and an endpoint needs one. State deletion below this quota, pinning by a forced edge, forcing all edges of a singleton state at its quota, and deleting extras when the forced quota is filled are all necessary conditions. These changes are monotone and polynomially bounded.

At a fixed point, every forced edge pins both endpoint states. Forced degree cannot exceed the required degree. Consequently each forced component is an isolated vertex, a path, or a cycle. A forced cycle is impossible in the desired open path, even if it spans the board. A forced component joining both terminals cannot be extended: it is the complete answer if spanning, and a rejection otherwise. A disconnected surviving candidate graph also rejects. These cases must precede the size theorem; they are explicitly handled.

### Contraction, ports and size

In every remaining branch the forced set is a forest and the two terminals lie in distinct components. Contracting each forced component removes one vertex and one edge per forced edge, preserving k=|E|−N+1 exactly. Every optional edge remains a distinct edge. This includes parallel edges and loops, with each loop contributing twice to contracted degree.

Internal cells of a nontrivial forced chain are saturated. Only its ends can have optional incidences; a chain containing one global terminal has only its opposite end available. A fixed-state isolated nonterminal must have at least three candidate edges, since two would already be forced. An ambiguous isolated cell has two disjoint sets of at least two state edges, hence four physical edges. Each nonsaturated chain end already has one forced edge and must have at least two optional incidences: if only one remained, that edge too would have been forced. Thus a nonterminal chain node has degree at least four. Each terminal node has degree at least two, since a single candidate continuation would be forced.

Writing n,m for kernel sizes gives 2m≥3(n−2)+4=3n−2 and m=n−1+k, so n≤2k and m≤3k−1. This is valid also when loops or parallel edges occur. A surviving search kernel with k=0 is impossible, rather than an exception to a negative edge bound: propagation and the earlier acceptance/rejection cases have already disposed of it.

The node bound alone would not justify losing chain ports. The actual solver retains the original cell of each optional incidence and checks its residual quota d(v)−deg_F(v). This prevents choosing both continuations at one end of a forced chain. It also retains state tags, so an isolated ambiguous cell cannot mix the two states. The O(k) search-size claim counts nodes, edges, incidences and tags, not coordinate bit length or the O(N) reconstruction record.

### Affine enumeration and exact selection

A spanning tree of the connected kernel has n−1 edges, ignoring loops during tree construction. Its terminal-to-terminal path has odd set exactly the two terminals. Each of the other k edges defines one fundamental even-degree edge set; a loop gives a singleton vector, and a parallel edge can give a two-edge cycle. Every even-degree edge set is a unique XOR of these vectors: eliminating its non-tree edges leaves an even-degree forest, which must be empty. This also proves independence.

Therefore every candidate with terminal odd set occurs once among the 2^k affine vectors. The algorithm does not mistake parity for the complete solution condition. It separately rejects selected loops, wrong exact node degrees, incorrect physical-port quotas, inconsistent full-state tags, and disconnected selected edges.

For an accepted vector, expand the forced chains. Every original cell has its exact endpoint/interior degree, every selected edge joins the chosen compatible states, and selected connectedness survives expansion. A finite connected graph with precisely two degree-one vertices and all others degree two is one spanning open path. Starting at the prescribed initial state physically reproduces the assigned states, including the prescribed final state. Conversely, every valid physical path survives propagation, contains every forced edge, and induces one enumerated vector passing all tests. This proves both directions.

An O(k²) explicit cycle basis and Gray-code XOR updates suffice for O(k 2^k) enumeration/checking time and polynomial decision-space use. Retaining every answer would use output-dependent space; the decision wrapper instead stops at its first certificate. A completed exhaustive enumeration with zero solutions means that branch is unsatisfiable; a propagation rejection can instead supply its particular rejection reason.

For a fixed initial orientation there are at most 2(N−1) endpoint/state branches; selectable initialization adds four choices, for at most 8(N−1). No equivalence of these variants is assumed. One cell requires zero moves and matching states. A one-dimensional corner-rooted rectangle has one possible physical cell order. These degenerate cases passed independent tests.

## Complete gadget proof challenge

### Neutral adjacent detours and the two-port principle

If a simple traversal starts at u, ends at its physical neighbor v, and ends in the direct-roll state from u to v, taking u→v first and reversing the original path except its first edge is legal. Reversibility recovers exactly the original full state at every cell. It covers the same cells and ends at the original second cell, distinct from v when the detour has more than one edge. Thus changing labels cannot remove this alternative while preserving the stated full-state-neutral traversal.

The escape from this obstruction is correctly conditional. If a proper gadget has exactly two usable external edges at distinct ports and both global endpoints are outside it, selected cut crossings are positive and even, hence exactly two. An additional internal component would be disconnected from the global path. Consequently the restriction is a single port-to-port spanning path. Neutrality alone does not establish external isolation or exclude a global endpoint.

### Ribbon for arbitrary permitted dimensions

For even columns assign N^y(q), and for odd columns N^y(W(q)). These are exactly the displayed periodic labels. Every vertical edge respects this field. Checking the four possible row residues proves that horizontal label-compatible moves occur exactly at y≡2 mod4 between an even column and the next odd column, or y≡0 mod4 between an odd column and the next even column. Each such move also produces the assigned full state. Thus the field is closed under every legal move from q; this is stronger than a projection observation.

The two bottom corners are leaves and therefore the two endpoints. Every odd-row cell has only its two vertical neighbors and is not an endpoint. Both its edges are forced. Since every vertical edge touches such an odd row, all vertical edges are forced. Intermediate even rows are then saturated. The forced top matching and bottom matching join the columns into exactly the stated serpent. This proves arbitrary-size existence and uniqueness from q.

For selectable initialization a north first move uniquely fixes q. The east first move fixes a different initial state and reaches a cell from which both possible unvisited directions have the wrong next top. It cannot cover a rectangle with at least six cells. These exhaust the initial possibilities at the corner. Each U-shaped column pair has net action W; the separating E cancels it, so the last state is W(q). When width is divisible by four, the corresponding straight displacement has this same net action. Reversal proves the specified opposite-direction traversal. Embedded exactness still requires both entry states, precisely the allowed boundary accesses, and exclusion of global endpoints from the ribbon.

### Copy-pair collar

Copying a rail cell's opposite-face pair, with either face sign, prohibits the cross-edge in every orientation. Consecutive rail pairs alternate. The parallel collar has the same pair sequence; translating an adjacency by one cell flips its checkerboard parity, while changing a label to its opposite does not change the unique edge's phase. Thus every along-collar edge is in the opposite phase from the rail. Each interior collar cell has at most its one outward edge available in the intended phase.

Length at least four supplies two such cells. Neither can be a board corner because its coordinate along the rail lies strictly between two other board cells. Both would need to be endpoints, but the specified starting corner is neither. A single free final endpoint cannot accommodate both. This establishes the claimed impossibility in the rail phase. It does not obstruct arbitrary insulating geometries or phase-selective alternatives.

### Compatible eight-cycles

A simple unit-grid polygon of perimeter eight has bounding side lengths a,b with a+b≤4 and area at most ab≤4. Pick's formula gives area I+3, so area is three or four. Area four forces a 2-by-2 unit-face square. Area three is a triomino with checkerboard imbalance ±1, contradicting the accepted phase-cycle area condition modulo three. Hence only the 3-by-3-cell perimeter can occur.

For this perimeter, the four full orientations that a center cell would need to match its four boundary neighbors are pairwise distinct. The frozen report's ordered tuples were checked with independent physical rotations. Changing the reference orientation relabels faces and preserves distinctness. A chosen center state therefore has compatible degree at most one. The no-hole rectangle includes the center; its four neighbors exclude it from being the specified starting corner. In a valid solution it must be the final endpoint. Its center identifies the perimeter uniquely, proving at most one compatible eight-cycle.

The endpoint-free gadget corollary requires the gadget to contain both the ring and its enclosed cell. An annular subset by itself could omit the center while a different part of the fully filled board contains that final endpoint. The final report makes this scope explicit. Likewise, rejection based on a pinned ring requires simultaneous full-state pinning, not merely its label-only projected edges.

## Independent finite checks

The independent audit computed rolls by rotating integer face normals using the cross-product formula for a quarter turn. Its physical-path and edge-subset enumerations were independent of the tested implementation. It compared the target algorithm's answers and affine enumeration with those independent results.

Passed:

- 24 physical orientations and all 96 directed quarter-roll comparisons
- 1,920 board/initial-state cases, including all 2-by-2 labelings with initial top 1 and all four initial yaws, thin boards, singletons, and fixed-seed arbitrary rectangles
- 40,032 endpoint/final-state branches with exact physical path-set equality; 129 returned physical paths replayed
- 3,174 connected multigraphs with loops and multiplicity, independently comparing every edge mask's odd set with the generated affine space
- Six adversarial checks separating port, state, loop and selected-connectivity requirements, including a locally valid path-plus-cycle configuration that must reject
- 504 ribbon orientation fields, including a 40-by-43 rectangle, with both directions of the exact rung formula and label-to-full-state closure
- Six exhaustively searched selectable-start ribbon boards, each with exactly one path, plus fixed-state reverse traversal
- 72 physical neutral-detour leakage instances
- 3,072 collar direction/side/orientation/sign cases
- 24 eight-ring orientation fields and all 24 possible center states in each
- Every rooted directed simple grid polygon of lengths 4, 6, 8, 10: counts 8, 24, 112, 560; full-state-closed counts 0, 0, 16, 40. The accepted closed shapes are the stated 3-by-3 and 2-by-5 cell perimeters.

Separately, the old 270-cell witnesses in De Biasi's *Rolling a Cube can be Tricky*, May 2012 Version 0.03, Figure 4 ([public manuscript](https://www.nearly42.org/vdisk/cstheory/rollingcubenpc3.pdf)), were replayed using the independent vector implementation. They have one shared endpoint/initial/final-state branch and the same full orientation field. Independent pinned-state degree propagation yields 278 candidate edges and 259 forced edges. Enumerating every one of the 92,378 ten-element subsets of the 19 optional edges gives three local degree completions, of which exactly two are connected. Those two edge sets are precisely the known witnesses and precisely the kernel solver's results. The compressed kernel has 11 nodes, 19 edges, k=9, seven parallel excess edges and 512 parity candidates.

This is a count for one branch only. It neither counts other endpoints or initial states nor creates a new nonuniqueness example. Source labels, routes, orientation tables and third-party source documents are not included in this edition.

The arbitrary-size conclusions rest on the complete proofs above. All numerical searches are bounded regression certificates. No surviving ambiguous-state rectangle is asserted. Abstract tagged-kernel tests do not claim die-board realizability.

## Resolved issues and final boundary

Two presentation issues were corrected before final acceptance:

1. The accepted algorithm distinguishes a completed satisfiable search from zero-solution unsatisfiability; a propagation rejection remains a reasoned rejection. This clarification did not alter accepted physical path sets.
2. The endpoint-free eight-cycle gadget corollary now explicitly includes the enclosed center cell in the gadget's region. The underlying global theorem was already correct.

No unresolved mathematical defect was found in the accepted scope. The unrestricted fully labeled no-hole complexity classification remains open in this work. This editorial edition does not add a research pass or enlarge the accepted mathematical conclusions.
