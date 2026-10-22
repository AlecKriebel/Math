# Independent acceptance: orientation structure and global-connectivity obstruction

## Verdict and boundaries

Accepted as structural partial results for the explicitly stated fully labeled rectangular Hamiltonian-path model:

1. Unique state-edge pinning by two neighboring labels and a direction.
2. The parity-phase projection, unique possible edge-count phase for a nontrivial rectangle, three-color characterization, exclusion of projected four-cycles, and checkerboard-area necessary condition.
3. After fixing the corner-start orientation and conditioning on the other endpoint and its orientation, sound degree/state/forced-edge propagation leaves ambiguous cells only in isolated singleton or adjacent-domino components, with no diagonal contacts.
4. The exact switch-bit plus fixed-state-edge formulation, provided selected-edge connectedness is retained.
5. The explicit 4 × 5 example showing that local orientation/degree feasibility and connectedness of the candidate graph are insufficient.

No polynomial algorithm, NP-hardness reduction, global uniqueness theorem, or main-target complexity classification follows from this acceptance. The bound does not claim an instance actually attaining surviving singleton/domino ambiguity. This review is separate from the source audit and does not certify worldwide novelty.

Public proof identities for this edition:

- [Orientation structure](ORIENTATION_STRUCTURE.md): 3b73d3489c0d25f5582faf5cf11b2710fb1fbcef08953c8d5e9534a51b5961dd
- [Connectivity obstruction](CONNECTIVITY_OBSTRUCTION.md): 316f350e848ed53e0c1007875d17d9b1007f91f21eeef9ceff49b21bd58b40f7

The review below was completed on the accepted proof texts before this edition's citation, spacing, and verification-reference edits. The proof statements and arguments are unchanged. These public identities bind the corresponding editorially normalized reports; they do not assert that the earlier computation read these newly formatted byte strings.

## Complete proof challenge

### State edges and parity

For a fixed chirality, specifying the top and one adjacent side determines a unique full orientation. A roll makes precisely one side the new top. Thus, when the two labels are distinct and nonopposite, a physical adjacency supports exactly one state edge; otherwise it supports none. The edge cannot belong to both phases.

A quarter roll transposes two of the three opposite-face axes. Its axis-permutation sign therefore flips, whereas board checkerboard parity flips at the same time. Their XOR is invariant. For each top label, either invariant phase permits precisely two orientations, separated by a half-turn about the vertical axis.

A w × h rectangle on N>1 cells has 2N−w−h < 2(N−1) physical adjacencies. Disjoint phase projections cannot both contain N−1 edges. This is a necessary-condition filter only; it does not decide Hamiltonicity. The N=1 exception is required and is stated.

The three-color rule was checked independently from vector rotations, not assumed. Its square contradiction correctly excludes projected four-cycles. The projection may still contain six-cycles, unlike an orientation-consistent rolling cycle. The area congruence follows by adding oriented elementary-square boundaries; all interior contributions cancel. It is only a necessary condition.

### Propagation soundness

Every selected nonendpoint has two distinct incident solution edges, and each endpoint has one. Consequently, deleting a state with fewer available incident edges than the required degree is sound. A forced state edge fixes its endpoint state; two different forced states at one cell are inconsistent. In a singleton state domain, exactly the required number of available edges makes all of them forced; exactly that number already forced excludes all other edges. Deleting a forced edge correctly rejects.

All deletions are monotone and forcing is monotone. Exhaustion terminates. None of these rules assumes a cycle, permits repeated cells, or needs the source papers' cutting rule. The reviewed finite implementation may retain stale adjacency information within a pass, but this only postpones deletion; forcing a singleton state's last required edges remains sound, and the next pass removes stale edges. The monotone cardinality fixed-point test is valid. The mathematical rule stated in the proof is independent of that implementation detail.

### Why surviving ambiguity has size at most two

A nonendpoint cell with two surviving states needs at least two edges at each state. Unique physical-edge pinning and grid degree four imply exactly two per state and all four physical adjacencies present. Such a cell is interior. Two diagonal ambiguous cells would supply all four edges of their elementary square, contradicting the no-four-cycle projection fact.

An ambiguous connected component cannot turn or branch: any perpendicular ambiguous neighbors of a cell would be diagonal neighbors of one another. It is therefore a straight segment.

For three consecutive ambiguous cells, the three-color rule makes the central colors alternate A,B,A and both neighboring three-cell rails uniformly the third color. The two rail cells alongside the middle cell have no usable horizontal edges in either phase (or no vertical edges for the rotated configuration). Their total usable degree is at most two.

Neither such rail cell can be the starting corner because its coordinate along the triple is strictly interior. At most one is the other endpoint. Choose the other rail cell q. It is a nonendpoint, and its edge to the central ambiguous cell survives. In a nonrejected branch, q must therefore have one surviving state carrying its two required edges: if its two physical edges used different states, both would have degree at most one and be deleted. Both edges are forced. This pins the middle cell's state, contradicting ambiguity.

This closes the only potentially delicate step in the singleton/domino proof. The corner-start condition and fixing the final endpoint state are essential to the stated argument. It must not be generalized to two arbitrary endpoints without a new proof.

### Exactness of the switch formulation

At an ambiguous cell, choosing one state chooses both of that state's two incident edges. An edge between two ambiguous cells must be chosen at both ends or at neither. This is an equivalence and gives precisely the stated XOR relation. Each domino's single relation can eliminate one bit.

At fixed-state cells, the remaining edge/literal sum must equal the required endpoint or interior degree, with propagated forced values retained. Together with selected-edge connectedness, this gives a connected finite graph of degree two except for two degree-one endpoints, hence a single spanning path. Every edge joins the selected compatible states, so rolling along the path reproduces the selected orientations from the prescribed initial state. Conversely, any valid path supplies such bits and edges. Candidate-graph connectedness alone does not supply the final implication.

### Connectivity obstruction

The independently generated physical state edges on the supplied 4 × 5 board split as claimed: one phase has 25 edges and the other none. Four candidate edges have degree-one states at both endpoints; none of those endpoints is the prescribed start. Using one would require both of its endpoints to be the two global path endpoints, which is impossible with the different fixed start. The remaining graph is exactly two 10-cycles connected by the middle bridge.

Any Hamilton path from the corner must cover the entire left cycle before crossing the bridge, because it cannot cross that bridge twice. A spanning path of a cycle must be obtained by deleting one cycle edge, and therefore has adjacent endpoints. The corner and the bridge attachment are not adjacent in that cycle. This proves nonexistence, including selectable initial orientation because the only usable start state is the displayed one.

Deleting the start-to-designated-end edge in the left cycle, and keeping the whole right cycle, does satisfy all local endpoint and interior degrees with consistent full orientations. Its disconnected selected graph is exactly the claimed obstruction. The graph proof establishes this particular counterexample independently of exhaustive search.

## Independent finite checks

The checker imports no supplied verification modules. It uses 3D integer face normals and quarter-turn rotation matrices, and computes parity from opposite-face axis permutations.

Verified in ordinary Python, Python -O, and Python -OO with byte-identical JSON output:

- 24 orientations
- 144 ordered-label/direction pinning cases
- 288 label/direction/checkerboard cases for the three-color formula
- All 1,296 six-label elementary-square assignments
- All 19,683 pair-labeled three-cell strips and rails; exactly 6 complete monochromatic-phase rail configurations, each with uniform rails
- A six-edge projected cycle with no physically valid rolling cycle
- The 4 × 5 obstruction, including all four top-compatible initial states; physical DFS visits 60 search nodes and finds zero full paths

The check coverage and outcomes are recorded in [VERIFICATION_SUMMARY.json](VERIFICATION_SUMMARY.json). Exact authored instance data are in [EXACT_AUTHORED_CERTIFICATE.json](EXACT_AUTHORED_CERTIFICATE.json); source-derived Figure 4 data are not included.

These checks corroborate the proofs. They are not exhaustive enumeration of arbitrary rectangles and do not replace the complete arguments above.

## Next mathematical gap

Global edge selection remains. Even a fully pinned orientation field can permit distinct complete cycles, as the separately replayed older Figure 4 construction demonstrates. The next investigation must retain one connected spanning selected graph and respect the corner/start-state/path conventions. Importing hardness from forbidden-cell gadgets, replacing connectedness by local degree equations, or treating a projected path as automatically orientation-consistent would leave the main gap unresolved.
