# An exact global-connectivity solver parameterized by surviving cycle rank

## Status and scope

The complexity classification of the completely labeled rectangular rolling-die problem remains unresolved. This note gives an exact fixed-parameter algorithm, including the selected-edge connectivity requirement. It does not prove a polynomial-time algorithm for arbitrary rectangles and does not prove hardness.

The contraction and binary-cycle-space techniques are general graph methods. Their application here uses the die-specific unique-state-edge reduction and the sound endpoint-conditioned propagation established in the preceding pass. The necessary orientation and phase facts are restated in [FOUNDATIONS.md](FOUNDATIONS.md). No novelty or priority claim is made for the general graph methods.

The input is an explicitly labeled finite rectangle, a fixed-chirality die, a specified corner start, and exact-once cell coverage by a path. A cell's label must equal the top face after landing; the initial cell also matches. No holes, free cells, excursions, revisits, or closing return are permitted. Use the explicit reference tuple

    (top,bottom,north,south,east,west) = (1,6,2,5,3,4),

with x east and y north. The initial orientation can be fixed input or selectable among the four rotations showing the start label; these variants are handled separately below.

### Main theorem

Fix an initial orientation, a different final cell t, and its final orientation. Run the state/degree/forced-edge propagation described below to a fixed point. Let G=(V,E) be the surviving physical candidate graph, N=|V|, and F its forced edges. Reject a disconnected G, a forced cycle, or a forced s-to-t path that omits cells. A forced s-to-t path covering all cells is an immediate solution.

In every remaining branch, define the surviving cycle rank

    k = |E| - N + 1.

There is an equivalent port- and orientation-tagged multigraph K with

    |V(K)| <= 2k,       |E(K)| <= 3k-1.

It is obtained by contracting each forced path; loops and parallel edges are retained and distinguished. Its cycle rank is exactly k. A complete search requires at most 2^k parity candidates. With polynomial preprocessing and compact port summaries, each candidate can be checked in O(k) time. Thus the branch can be decided in

    polynomial(N) + O(k 2^k)

time and polynomial space, with a recoverable physical path certificate. The exponential search works when orientations are fully pinned and when the previously proved singleton/domino ambiguities remain. No orientation choices are silently omitted.

This is fixed-parameter tractability in the surviving cycle rank. The theorem supplies no constant or logarithmic bound on k for arbitrary inputs, so it supplies no general polynomial classification.

## 1. State edges and sound propagation

For adjacent cells u,v, a direction and their two labels specify at most one legal full die transition in a fixed chirality. Prescribing the current top and the side that becomes the next top fixes the entire die. Hence a physical adjacency carries at most one state edge, tagged with its required orientation at each end. It belongs to exactly one preserved die/checkerboard phase.

Fix the branch's initial and final states. At every other cell retain its two top-matching states in the chosen phase. Set desired physical degree d(v)=1 at s,t and d(v)=2 elsewhere. Maintain surviving states, edges, and a monotonically growing forced-edge set F. Repeat:

1. Delete edges whose required endpoint state was deleted.
2. A forced edge pins its endpoint state. Reject incompatible forced states.
3. Delete any state having fewer than d(v) surviving incident edges. Reject an empty domain.
4. At a cell with one state remaining, reject more than d(v) forced edges. If exactly d(v) incident edges remain, force all. If d(v) are already forced, delete its other edges.
5. Reject deletion of a forced edge.

These rules retain every completion in the branch. They have polynomially many changes. The direct implementation repeatedly scans the current finite graph; no claimed fast propagation data structure is needed for the polynomial preprocessing bound.

The first-pass residual singleton/domino theorem remains available, but the kernel bound below needs only the simpler consequence: a cell with two remaining orientations has four distinct surviving physical incident edges. Each state needs two, and one adjacency cannot support both states.

## 2. Forced paths, ports, and degenerate cases

A valid path must contain all of F. Forced degree cannot exceed the required degree, so each nontrivial connected component of F is a path or a cycle. A forced cycle cannot occur inside a Hamiltonian path, even if it covers all cells. Reject it.

If a forced path contains both s and t, it has already used their full allowed degrees. It cannot be extended. Accept if it covers all cells; reject otherwise. This handles the completed case before the kernel size argument. A one-cell board is handled directly by its matching initial state and zero moves.

Otherwise contract every connected component of F, including isolated vertices, to a node of K. Keep every edge of E minus F as a separately identified optional edge. Retain its original two cells and its required endpoint orientations. Also retain the ordered forced chain for later reconstruction.

For a nontrivial forced chain, internal cells are saturated and have no optional incidence. Its two ends are its possible external ports. If a chain contains s or t, that endpoint is saturated and only its other end is an external port. An isolated original cell is one port with required degree two, or degree one if it is s or t.

For each port v store its residual requirement

    r(v) = d(v) - degree_F(v).

This is essential: total degree two at a contracted chain does not permit using both external edges at the same end. Each chain end normally needs one. Its full orientation is already pinned by its incident forced edge. An isolated ambiguous cell must have all its selected optional edges tagged with the same retained state.

Distinct optional edges can become parallel. An optional edge can also become a loop by joining the two ends of a forced chain. Selecting such a loop would close a forced cycle and is forbidden in the path problem. Retaining the loop as a distinct, forbidden-to-select edge keeps cycle-rank bookkeeping exact. Alternatively one may delete it and repeat propagation, recomputing k; that optional optimization is not used in the stated size proof or verifier.

The two terminal components are distinct in the nontrivial case. Contraction preserves connectivity of any graph that contains F.

## 3. Proof of the linear kernel bound

Write n=|V(K)| and m=|E(K)|. Since F is a forest,

    n = N - |F|,       m = |E| - |F|,
    m - n + 1 = |E| - N + 1 = k.

Loops contribute twice to degree, as usual. No optional edge is discarded in this equality.

Every nonterminal node of K has degree at least three:

- If it is an isolated original cell with a fixed state, a surviving candidate degree of two would have forced both edges. Thus its degree is at least three.
- If it is an isolated ambiguous cell, its two states each have degree at least two on distinct physical edges, so its degree is four.
- If it is a nontrivial forced chain containing no terminal, each end already has one forced edge. If an end had only one optional edge, its two total edges would both have been forced. Each end therefore has at least two optional edges. The contracted degree is at least four, including loop incidences correctly.

Each of the two terminal nodes has degree at least two:

- An isolated terminal with only one incident edge would force that edge.
- A nontrivial terminal chain has one nonsaturated end, which needs at least two optional edges by the preceding argument.

Consequently

    2m >= 3(n-2) + 2+2 = 3n-2.

Substitute m=n-1+k to obtain n<=2k, and then m<=3k-1. In particular k=0 cannot survive as a nontrivial search kernel. A tree candidate graph either propagates to the unique complete forced path or is rejected. This explains why the k=0 case is handled before exponential search rather than by a negative edge bound.

The retained chains occupy O(N) storage for reconstruction, but the combinatorial search instance has O(k) nodes, optional edges, port incidences, and state tags. Original coordinate identifiers require O(log N) bits each; the kernel claim is a bound on combinatorial size, not a claim that original coordinate strings have constant bit length.

## 4. Exact enumeration by the binary cycle space

Let a and b be the two terminal nodes. Any valid optional-edge set X has degree one at a,b and degree two at other kernel nodes. In particular its odd-degree set is exactly {a,b}.

Choose any spanning tree T of the connected multigraph K, ignoring loops while building T. Let P be its unique a-to-b path. For each edge e outside T, let C_e consist of e and the T-path between its endpoints. A loop's T-path is empty, so C_e is that one loop. Parallel edges are treated as distinct edges; a parallel non-tree edge can yield a two-edge fundamental cycle.

There are exactly m-(n-1)=k such fundamental cycles. They form a basis over F_2 for even-degree edge sets. Here is a direct proof suitable for this multigraph setting. Given an even-degree edge set Y, XOR C_e for every non-tree edge e of Y. All non-tree edges disappear. The remainder is an even-degree subgraph of a tree, which must be empty: a nonempty forest has a leaf of odd degree. Each basis vector has its own unique non-tree edge, giving independence.

Thus every edge set with odd-degree set {a,b} is uniquely

    X = P XOR (XOR of a chosen subset of the C_e).

There are exactly 2^k candidates. This enumerates selected OPTIONAL edges in the contracted multigraph, not selected edges of a graph that has lost the forced-chain port constraints. All forced original edges are added back in every reconstruction.

For each candidate:

1. Reject a selected loop.
2. Check degree one at a,b and degree two elsewhere in K.
3. At each original port v, check precisely r(v) selected optional incidences. This enforces distinct ends of a chain separately.
4. At every isolated original cell, check that all selected incident edge tags specify one common remaining full orientation. Forced-chain endpoint tags already agree with their pinned states because propagation retained the edges.
5. Check connectedness of the SELECTED kernel edges.

These checks use O(k) data. The fundamental basis may be built in O(k^2) preprocessing. Generate subset combinations in reflected Gray-code order, so one fundamental-cycle XOR updates the candidate at a time. Even charging O(k) for a bitset XOR, the total candidate-generation and checking cost is O(k 2^k). Store a current candidate and the O(k^2)-size explicit basis rather than every candidate. For a decision search, stop at the first accepted set. A counting or full-certificate run may retain more output, which is not part of the polynomial-space decision claim.

### Soundness

An accepted X gives the physical selected graph F union X. Port checks give every original cell its exact required degree. Orientation checks choose one compatible state at each cell; every selected edge is a legal roll between those states. The selected kernel is connected, so its uncontracted graph is connected. A finite connected graph with degrees one at s,t and two elsewhere is a single spanning s-to-t path. Starting in the branch's prescribed state and rolling along this path reproduces all chosen states and labels, including the prescribed final state.

### Completeness

Any valid path survives propagation and contains F. Contract its forced chains. Its optional edge set has the stated degree parity and therefore occurs exactly once in the affine cycle-space enumeration. It satisfies every port, state, degree, and connectivity check. Consequently the solver cannot miss a solution in the branch.

### Why parity alone is insufficient

A parity candidate may have degree four at a nonterminal, the wrong port usage at a contracted chain, conflicting die states at an ambiguous cell, or multiple selected components. None of these is accepted. The cycle-space representation is a complete search space, not a substitute for the remaining tests.

## 5. Whole-instance algorithm and initial orientation variants

For a fixed initial orientation, enumerate t different from s and each of its at most two matching states in the preserved phase. This gives at most 2(N-1) endpoint/state branches. Ordinary checkerboard endpoint parity can prune them. Accept the original instance if any branch accepts.

For selectable initial orientation, enumerate the four rotations showing the start label, then the same branches. This gives at most 8(N-1) branches before phase pruning. The preceding pass's disjoint-phase edge-count test can reject one or both phases and reduce this search; no equivalence of fixed and selectable orientation is assumed.

The displayed complexity is per branch. The full algorithm multiplies preprocessing and the corresponding exponential costs by the enumerated branches, or sums their individual k values' costs. One-dimensional rectangles and N=1 can also be checked directly along their unique possible corner-rooted cell order.

## 6. Reproducibility and limits

The accepted finite verification compared complete branch solution sets against independent face-normal rotation enumeration of physical paths on small labeled rectangles. It also exhausted edge subsets of small connected multigraphs with loops and parallel edges. The comparison checked reconstructed paths, distinct original ports, full-state tags, loop rejection and selected connectedness. [VERIFICATION_SUMMARY.json](VERIFICATION_SUMMARY.json) records the scopes and aggregate outcomes. [CERTIFICATE_GUIDE.md](CERTIFICATE_GUIDE.md) supplies a program-independent validation procedure and small exact authored certificates. The complete algorithm is specified and proved above; no software implementation is part of this edition.

The older 270-cell source regression concerns the two already published witnesses in De Biasi, *Rolling a Cube can be Tricky*, May 2012 Version 0.03, Figure 4 ([public manuscript](https://www.nearly42.org/vdisk/cstheory/rollingcubenpc3.pdf)). No source board or route is reproduced here. Both published witnesses share one endpoint/initial/final-state branch. In that branch, the surviving graph has 278 edges and 259 forced edges, hence k=9. The kernel has 11 nodes and 19 optional edges, including seven edges beyond one representative per unordered node pair. Enumerating all 512 parity candidates gives exactly two complete paths in this shared branch. An independent enumeration of all 92,378 size-ten optional-edge subsets gives the same two path edge sets. These are the known source paths; no new construction or general source-board uniqueness claim is made. A fixed branch count does not count other endpoints or initial/final states.

The theorem leaves the general problem open. Full orientation pinning does not force k=0: the source regression is fully pinned with k=9. Conversely, large initial candidate cycle rank is not evidence of difficult residual search, since propagation can eliminate many edges. The parameter must be measured after the specified preprocessing. No reduction from generic connected-factor hardness to no-hole die boards is inferred.
