# Residual orientation ambiguity is confined to singleton and domino switches

## Scope and result

The instance is an entirely labeled m-by-n rectangle, a fixed-chirality standard die with opposite faces summing to 7, matching the board label on top **after landing**, and a Hamiltonian **path** starting at a specified corner. The initial orientation may be fixed or selectable; these variants are kept separate. No free cells, holes, revisits, rotations in place, or closing return to the start are used.

**Residual ambiguity theorem.** Fix the initial orientation, enumerate the other endpoint and its final orientation, and exhaust the sound state/degree/forced-edge propagation below. In every nonrejected branch, every cell retaining two possible orientations is an interior nonendpoint cell. Such cells form disjoint singleton cells and side-adjacent dominoes. Distinct components have no diagonal contacts. Their orientation choices admit an exact one-Boolean-variable-per-component formulation, with local degree equations at the other cells and one remaining global connectedness condition.

This is a structural reduction, **not** a polynomial-time algorithm for the complete problem, nor an NP-hardness proof. The bound is proved; attainment by a solvable full rectangle was not established. Finite checks below found no surviving ambiguity on the tested generated instances.

## 1. Die convention and parity

Use coordinates (x,y), with y increasing north. Write an orientation as

    (top, bottom, north, south, east, west).

The reference die is (1,6,2,5,3,4). Its 24 rotations are the fixed-chirality states. A quarter roll changes the sign of the permutation of the three opposite-face axes among the world axes. Equivalently, the usual cube-rotation parity changes on every move. Let sigma be 0 at the reference orientation and flip on a roll. Then

    phase = sigma(orientation) XOR ((x+y) mod 2)

is preserved. At a cell with a prescribed top label, each phase has exactly two orientations, related by a 180-degree yaw. This is the familiar parity reduction of Buchin et al., Sections 2.1–2.3; it is not claimed as new.

### Unique-edge lemma

For adjacent labels a,b and a specified direction, a legal transition exists precisely when b is neither a nor 7-a. If it exists, prescribing top a and the side which becomes top b specifies exactly one orientation of the fixed-chirality die. Its successor orientation is unique too. Thus a physical board adjacency contributes exactly one state edge in total, in exactly one phase. In particular, the two phase-projected edge sets are disjoint.

This does not mean a projected path is rollable: consecutive projected edges may demand different orientations at their shared cell.

For N>1 cells in a rectangle, the total number of physical edges is

    E = 2N - m - n < 2(N-1).

A spanning path in a phase needs at least N-1 edges in that phase's projected graph. Hence **at most one phase can even satisfy this edge-count necessary condition**. This permits a phase rejection test for selectable initial orientations; it does not imply that a surviving phase is feasible. A one-cell board is handled directly.

## 2. A three-color description of the projected graph

Let p(a)=min(a,7-a), and encode opposite-face pairs cyclically by

    c(1)=c(6)=0; c(3)=c(4)=1; c(2)=c(5)=2   in Z/3Z.

Call x+y even cells black and odd cells white. In phase 0:

- A horizontal adjacency is present exactly when c(white)-c(black)=+1.
- A vertical adjacency is present exactly when c(white)-c(black)=-1.

Phase 1 reverses the signs. Equal pair labels give no edge in either phase. The rule follows from the parity of the permutation of the three face axes; changing either label to its opposite does not change phase. Independent finite checks also cover all 144 label/direction cases; their scope is recorded in [VERIFICATION_SUMMARY.json](VERIFICATION_SUMMARY.json).

### No projected 4-cycle

Suppose a square's lower-left black cell has color a, and all four edges belong to phase 0. Its right neighbor has color a+1, and its upper neighbor has color a-1. The upper-right black cell would then need color a-1 from the right edge and a+1 from the upper edge, a contradiction modulo 3. The other phase and square colors are symmetric.

More precisely, exhaustive square color reasoning gives only the following edge-count triples, counting phase 0, phase 1, and unavailable edges:

    (2,2,0), (3,0,1), (0,3,1), (1,1,2), (0,0,4).

Thus every phase-projected graph is planar and bipartite with girth at least 6. For a connected projected graph on N>=4 vertices, the usual planar girth bound is E <= 3(N-2)/2. Do not substitute girth 8 here: the original state graph and this projection are different graphs.

**Explicit projected 6-cycle:** pair-label rows

    1 3 1
    2 3 2

have a phase-0 perimeter 6-cycle. The middle vertical edge is unavailable because both labels belong to pair 3. No orientation-consistent rolling cycle follows this six-edge perimeter. This is only a projected witness, not a valid puzzle solution.

### Checkerboard-area obstruction

Orient each geometric horizontal edge black-to-white with weight +1 and each vertical edge black-to-white with weight -1; reversing an edge negates its weight. In phase 0 every projected edge satisfies c(v)-c(u)=weight(u,v) modulo 3; phase 1 reverses it. Around a counterclockwise elementary square with lower-left cell (x,y), the weight sum is 4(-1)^(x+y), congruent to (-1)^(x+y) modulo 3. Therefore every simple projected cycle satisfies

    sum over enclosed elementary squares of (-1)^(x+y) = 0 modulo 3.

This is necessary, not sufficient for the cycle to occur in a particular label assignment, and not sufficient for actual die-state continuity. It follows by summing the elementary face boundaries; interior edges cancel.

## 3. Endpoint-conditioned propagation

For N>1, the initial state is fixed in a branch. Enumerate an endpoint t distinct from the corner s, and one of its two phase-compatible orientations. There are at most 2(N-1) such branches for a fixed initial state. Ordinary bipartite endpoint parity can prune them. With a selectable initial orientation, additionally enumerate the four top-compatible initial orientations, or first use the unique candidate-phase test above. One-dimensional boards can instead be checked directly along their unique corner-rooted Hamiltonian path.

For each cell v let D(v) contain the remaining phase-compatible orientations showing its label. Initially D(s) and D(t) are the prescribed singletons; every other D(v) has two states. Let k(v)=1 at s,t and k(v)=2 elsewhere. The graph consists of legal state edges whose endpoint states remain. Maintain a set F of forced state edges.

Repeat to a fixed point:

1. Delete edges incident to a deleted state.
2. A forced edge at v pins its state. Delete any other state of v. If forced edges demand two distinct states of v, reject.
3. Delete any state of v with fewer than k(v) remaining incident edges. Reject if D(v) becomes empty.
4. If D(v) is a singleton with state q, reject if more than k(v) incident edges are forced. If q has exactly k(v) remaining incident edges, force all of them. If exactly k(v) incident edges are already forced, delete its other incident edges.
5. Reject if a forced edge is deleted.

Each deletion/forcing step is sound for any completion to a Hamiltonian s-t path. All domains and edge sets only decrease, while F only increases, so a straightforward implementation terminates in polynomial time. Premature-cycle and other connectivity pruning may be added, but are not needed for the theorem.

## 4. Proof of singleton/domino structure

Call a surviving cell ambiguous if |D(v)|=2. Endpoints are not ambiguous because they were explicitly fixed.

### Lemma A: all four physical edges occur at an ambiguous cell

Each of its two states has remaining degree at least 2, by Step 3. There is at most one state edge over each of the four physical adjacencies, by the unique-edge lemma. Therefore both states have degree exactly 2, and all four physical adjacencies remain in the current phase. The cell is consequently interior.

### Lemma B: no two ambiguous cells are diagonal neighbors

If two opposite corners of an elementary square were ambiguous, their four incident edges on that square would all belong to the same phase, by Lemma A. This would be a projected 4-cycle, which is impossible.

Hence a cell cannot have two perpendicular ambiguous neighbors, because those neighbors would be diagonal to each other. Every connected component of ambiguous cells is consequently a straight horizontal or vertical segment (including a singleton).

### Lemma C: uniform rails along a three-cell segment

Suppose three horizontally consecutive cells v_-,v,v_+ are ambiguous. Their colors alternate A,B,A, since both horizontal edges are in one phase. The three cells immediately above them all have the third color C; the three immediately below them also all have color C. This follows directly from the three-color rule. Thus both three-cell rails are uniform in opposite-face pair, regardless of the six individual face-label signs.

The two rail cells immediately above and below v have no horizontal legal edges at all: both horizontal neighbors have their own face pair. Each rail cell therefore has total physical usable degree at most 2, counting both phases and all orientations.

### Lemma D: no ambiguous segment has length at least three

Neither rail cell next to v can be the starting corner. For a horizontal triple, their x coordinate is strictly between the rectangle's left and right boundaries; for a vertical triple the analogous y statement holds. At most one can be the other endpoint t. Choose a rail cell q which is not an endpoint.

The edge q-v still exists because v is ambiguous (Lemma A). Since q has total usable degree at most 2, and is a nonendpoint, it can retain only one orientation with two available edges; both edges are forced by Step 4. In particular q-v is forced. Step 2 then pins v's state, contradicting ambiguity.

Thus every component has at most two cells. Together with Lemma B, this proves the theorem.

The corner hypothesis is used precisely in excluding s from the two flanking rail cells. For two arbitrary prescribed endpoints, both could occupy these rails, so this argument alone does not exclude a length-three segment. It should not be generalized to that setting without further work.

## 5. Exact Boolean switch formulation

Assign arbitrary names 0 and 1 to the two states at each ambiguous cell v, with bit z_v selecting its state. Every such state has exactly two incident edges, so **both** must be selected whenever that state is chosen. For an incident edge e, write a(v,e) for the unique state index supporting e. Then

    e is selected  iff  z_v = a(v,e).

If both endpoints u,v are ambiguous, consistency requires

    (z_u=a(u,e)) iff (z_v=a(v,e)),

or equivalently

    z_u XOR z_v = a(u,e) XOR a(v,e).

These are exact equivalences, not merely implications. Each domino has one such relation; eliminate it to retain one bit per singleton/domino component. Since components have at most two cells, no nontrivial internal XOR cycle remains.

- A singleton exposes four ports and selects one of two complementary pairs.
- A domino exposes six ports. In the choice using its internal edge, it selects two external ports, one at each cell. In the other choice it selects the remaining four external ports, two at each cell. The internal pairings are fixed by the cells.

Every other cell has a fixed orientation. Introduce a free edge bit y_e for each remaining edge joining two such fixed-orientation cells. Each edge from a switch component to a fixed cell is already a literal in that switch's bit. At a fixed cell v impose

    sum of its incident edge bits/literals = k(v).

Keep forced-edge values from propagation. Finally require the selected physical graph to be connected.

**Exactness.** A solution path supplies all bits and satisfies every condition. Conversely, bits satisfying the degree equations define exactly one compatible orientation per cell; every selected edge is a legal transition; all cells have degree 2 except s,t, which have degree 1. A finite connected graph with this degree sequence is a single Hamiltonian s-t path. Initial and final orientations are the fixed branch states. Without the connectedness condition, the constraints may admit an s-t path plus disjoint cycles; this relaxation is not claimed to solve the original problem.

The result leaves a bounded-local-choice Boolean degree/connectivity problem. It does not establish tractability of that remaining problem or allow importing hardness for boards with blocked cells.

## 6. Verification and limitations

The deterministic finite verification checks all 24 orientations, all 144 label/direction cases, all 1,296 six-label elementary squares, all 19,683 pair-labeled three-cell strips and rails, and all 1,968 combinations of corner-rooted Hamiltonian paths and initial die orientations on the rectangles 2-by-2, 2-by-3, 3-by-3, 3-by-4, and 4-by-4. It checks propagation never removes the generated witness and that the residual ambiguity bound holds.

A separate bounded randomized probe generated 2,000 6-by-6 and 4,000 12-by-12 corner-rooted Hamiltonian paths by fixed-root backbite moves, then labeled them by actual rolls and ran propagation with their actual endpoint orientations. It found no residual ambiguous cell. These negative searches establish neither a stronger theorem nor sharpness. No claim of a surviving singleton/domino witness is made.

## Source boundary

Sources are distinguished in the [source and model audit](SOURCE_MODEL_AUDIT.md):

- Kevin Buchin, Maike Buchin, Erik D. Demaine, Martin L. Demaine, Dania El-Khechen, Sándor Fekete, Christian Knauer, André Schulz, and Perouz Taslakian, [*On Rolling Cube Puzzles*, full version](https://erikdemaine.org/papers/DiceRolling_CCCG2007/paper.pdf), Sections 2.1–2.4 and 4.1. Its parity reduction and degree reasoning are acknowledged above; its fully oriented state-graph girth statement must not be applied to the phase projection. The author-hosted 30-page full version is distinguished from the four-page CCCG 2007 proceedings version. The author BibTeX field `unrefereed = 1` is reported in the audit; this edition does not identify the full version as a refereed journal publication.
- Marzio De Biasi, [*Rolling a Cube can be Tricky*](https://www.nearly42.org/vdisk/cstheory/rollingcubenpc3.pdf), May 2012, Version 0.03. The source contains the older fully labeled nonuniqueness example and claims hardness with blocked cells. Its independently checked Figure 4 construction and its unverified complete hardness interfaces have different evidentiary status. Neither settles the fully labeled no-hole target.

The structural reduction and proofs here are authored derivations from the stated model. No worldwide novelty or priority claim is made. The [independent acceptance report](INDEPENDENT_STRUCTURE_REVIEW.md) challenges the complete proof, including the rail-cell forcing argument. The general theorem does not depend on an external program or on Figure 4.
