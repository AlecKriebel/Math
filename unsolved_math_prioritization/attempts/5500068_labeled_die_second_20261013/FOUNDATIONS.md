# Orientation and phase foundations for the second edition

These are the accepted first-pass facts needed by the cycle-rank and gadget proofs. They are restated for readability, without a new research or priority claim. Full propagation is specified in [CYCLE_RANK_KERNEL.md](CYCLE_RANK_KERNEL.md). The [first edition](../5500068_labeled_die_first_20261013/README.md) contains the complete structural investigation.

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

Phase 1 reverses the signs. Equal pair labels give no edge in either phase. The rule follows from the parity of the permutation of the three face axes; changing either label to its opposite does not change phase. The first edition records independent finite checks of all 144 label/direction cases; the phase formula above is the mathematical rule used here.

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


The parity reduction is attributed to Buchin et al., *On Rolling Cube Puzzles*, Sections 2.1–2.3 ([author-hosted full version](https://erikdemaine.org/papers/DiceRolling_CCCG2007/paper.pdf)). These projection facts never substitute for the full orientation compatibility checks in this edition. The exact model is the fully labeled, hole-free rectangular Hamiltonian path from a specified corner, with fixed die chirality and an explicitly fixed or selectable initial orientation.
