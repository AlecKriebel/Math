# Fully covered rolling-die gadgets: an exact ribbon and three obstructions

## Status and exact model

This is the complementary no-hole investigation in the second substantive pass on TOPP Problem 68 (row 1758 / 5500068). It does **not** prove NP-hardness or a polynomial-time algorithm. No reduction from a blocked-cell or prescribed-length-cycle problem is claimed.

Every input cell of the rectangle is labeled in {1,...,6}; every cell must be visited once, including the start. Moves are unit edge-adjacent tips, with the new top face matching after landing. The start is a specified corner, and the other endpoint is unrestricted unless explicitly conditioned. There are no holes, free cells, excursions, rotations in place, or closing revisit. The die has fixed chirality represented by

    q = (T,B,N,S,E,W) = (1,6,2,5,3,4).

Coordinates increase north and east. For example,

    N(T,B,N,S,E,W) = (S,N,T,B,E,W),
    E(T,B,N,S,E,W) = (W,E,N,S,T,B).

A word denotes successive rolls in its written order. The statements below explicitly distinguish fixed and selectable initial orientations. The exact-interface conclusions for an embedded gadget are conditional on its stated external boundary accesses; merely drawing a rectangle around the gadget does not establish those accesses.

## 1. Universal endpoint leakage of neutral adjacent-port detours

**Theorem 1.** Let P=(v0,...,vL) be a legal exact-once traversal of a cell set C, where L>1, the ports v0 and vL are physically adjacent, and the terminal full orientation of P is exactly the result of the direct unit roll v0→vL from P's initial orientation. Then the same labeled set, from the same initial full orientation at v0, has the legal exact-once traversal

    v0, vL, v(L−1), ..., v1.

Its endpoint v1 is different from the designated endpoint vL. Every visited cell has exactly the same full orientation in both traversals.

**Proof.** The assumed terminal equality makes v0→vL a legal first roll with the terminal orientation of P. Every subsequent step reverses a step of P. A reversed tip is the inverse orientation update, so the orientations encountered are precisely those of P in reverse order. All L+1 cells occur once. Since P is simple and L>1, v1≠vL. Equivalently, the intended detour together with the direct return vL→v0 is a full-state closed cycle; deleting the other edge incident to v0 gives the alternative path. ∎

Thus the failure of N⁴ES⁴ is unavoidable for **every** nontrivial locally endpoint-faithful neutral replacement of a unit edge by a fully covered set. No alternative labeling can reject the second traversal while preserving the first and the stated terminal equality: they use identical full orientations at every cell.

This does not rule out a global reduction that excludes the endpoint from the gadget, that proves soundness despite endpoint migration, or that uses nonadjacent ports. It is an obstruction to a particular local interface claim, not to all no-hole reductions.

**Endpoint-conditioned two-port principle.** Suppose a proper gadget C has only two allowed external edges, one at each distinct port, and a global Hamilton path has both endpoints outside C. The path must use both external edges and restrict to a single Hamilton path through C between its ports. Indeed, the number of cut crossings is positive and even, hence two; additional internal components would be disconnected cycles. Therefore a neutral adjacent-port detour can be usable when an independent argument supplies exact boundary isolation and excludes both global endpoints. The state equality alone supplies neither condition.

## 2. A rigid full rectangular ribbon with nonadjacent neutral ports

The previous obstruction does not extend to nonadjacent ports. There is a particularly simple exact positive family.

Let w=2k≥2 and h=4r+3≥3. Label a w-by-h rectangle periodically by the following rows, starting at the bottom:

    y ≡ 0 mod 4:  1 3 1 3 ... 1 3
    y ≡ 1 mod 4:  5 5 5 5 ... 5 5
    y ≡ 2 mod 4:  6 4 6 4 ... 6 4
    y ≡ 3 mod 4:  2 2 2 2 ... 2 2.

The ports are the bottom-left and bottom-right corners.

**Theorem 2.** From the bottom-left corner there is exactly one Hamilton path on this board, even when the initial full orientation is selectable among all four states with top 1. It starts in q, follows the column-by-column vertical serpent, and ends at the bottom-right corner in W(q). Its word is

    (N^(h−1) E S^(h−1) E)^(k−1) N^(h−1) E S^(h−1).

In particular, when w is divisible by 4, the terminal state equals E^(w−1)(q), the state after the straight horizontal displacement between the ports. The smallest such neutral example is the fully labeled 4-by-3 board

    6 4 6 4
    5 5 5 5
    1 3 1 3

with the bottom-left start. Unlike an adjacent-port neutral cap, it has no wrong-endpoint completion.

**Proof.** Define an orientation field on every cell by

    Q(2i,y)   = N^y(q),
    Q(2i+1,y) = N^y(W(q)).

Its top labels are exactly the displayed board. Every vertical adjacency respects this field. Direct four-residue calculation gives all horizontal moves that match a neighbor's top label from its assigned state:

- between columns 2i and 2i+1 precisely when y≡2 mod 4;
- between columns 2i+1 and 2i+2 precisely when y≡0 mod 4.

Whenever such a move is label-compatible, its resulting full orientation is also the neighbor's assigned state. All other horizontal moves fail the next top label. Consequently every legal path starting in q remains in Q. This proves full orientation consistency, rather than merely a projection claim.

In this reachable graph the two bottom corners have degree one. Every other vertex has degree at least two. Hence a spanning path starting at the bottom-left must end at the bottom-right. Every cell in an odd-numbered row has exactly its two vertical neighbors; none is an endpoint. Both its incident edges are therefore forced. Every vertical edge is incident to an odd-numbered row, so **all vertical edges are forced**.

At every intermediate even row the two vertical edges already use the degree quota, so no horizontal edge is selected. At the top, the horizontal pairs (0,1),(2,3),... are forced. At the bottom, the horizontal pairs (1,2),(3,4),... are forced. These edges form exactly the displayed serpent. This proves existence and uniqueness for initial state q.

For selectable initial state, the first move is north or east. Matching a north move from label 1 to label 5 uniquely pins q. Matching an east move from label 1 to label 3 instead pins the initial state

    (1,6,5,2,4,3),

and reaches (3,4,5,2,1,6). Its northward next top would be 2, whereas the cell above is 5. Its eastward next top would be 6, whereas a next bottom-row cell, when present, is 1. Its other available neighbor is already visited. Thus the east-first route cannot be Hamiltonian on a rectangle with at least six cells.

Finally h−1≡2 mod 4, so the U-shaped traversal of each column pair acts on orientation as W. The east roll between pairs cancels that W, resetting q before the next pair. The last pair leaves W(q). If w≡0 mod 4, then w−1≡3 mod 4, and E^(w−1)=W. ∎

**Bidirectional and embedded interface.** Reversing the serpent gives the unique full traversal from the bottom-right with initial state W(q) to the bottom-left with state q. The same reachable-field and degree argument proves this directly. If a larger construction permits exactly one external edge at each bottom port, permits no other boundary crossing, supplies these entry states, and has its endpoints outside the ribbon, the two-port principle proves that this exact traversal is obligatory in either direction.

The ribbon is a fully covered, endpoint-faithful neutral replacement for a longer straight interface when w≡0 mod4. It is **not** a unit-edge filler, nor a complete hole-elimination reduction. It changes the labels at interior positions of the straight segment, and its interactions with neighboring compulsory tiles have not been isolated. Its internal forced-degree argument deliberately leaves no binary switch. It therefore supplies a wire/coverage building block, not a hard-choice gadget.

## 3. An all-state insulating collar can make full coverage impossible

A frequent way to prohibit a physical adjacency is to give its two cells equal or opposite labels. This forbids the edge in all orientations. Around a compulsory rolling rail, applying that rule uniformly to a parallel collar has a sharp cost.

**Theorem 3.** In a fully labeled rectangle consider a straight rail of ℓ≥4 consecutive cells whose labels are generated by consecutive rolls in that direction. Suppose the intended global phase is the phase of that rail. Place an adjacent parallel collar of ℓ cells, assigning each collar cell the same opposite-face pair as its corresponding rail cell, with either sign allowed independently. Then no corner-start Hamilton path in that phase can cover the rectangle.

**Proof.** A standard die's three opposite-face pairs define an orientation parity σ that flips at every tip. Hence σ(Q) XOR (x+y mod2) is invariant along a rolling path. A pair of adjacent nonopposite top labels determines one full state transition, whose phase depends only on their opposite-face pairs. Replacing either label by its opposite leaves this phase unchanged.

Every cross-edge between corresponding rail and collar cells is impossible, since its two labels have the same opposite-face pair. Along a straight rolling rail the top-face pairs alternate between two different pairs. The collar has the identical pair sequence. Translating an edge by one cell changes checkerboard parity, so every along-collar edge lies in the phase opposite to the corresponding rail edge, independent of the signs chosen on the collar.

An interior collar cell consequently has no cross-edge toward the rail and no edge along the collar in the intended phase. It has at most the one outward edge. There are at least two such cells because ℓ−2≥2. Neither is a board corner: its along-rail coordinate lies strictly between those of two board cells. Both would have to be path endpoints, but only the final endpoint can be a noncorner endpoint in the stipulated corner-start path. Contradiction. ∎

This rules out a same/opposite-label **all-state** insulation strip beside a length-at-least-four straight rail. It does not rule out a phase-selective collar, a more complicated interface, a side lying on the actual board boundary, or a different local geometry. Those distinctions are necessary: swapping the two alternating rail pairs, rather than copying them, can put the parallel collar edges back in the intended phase.

## 4. An eight-cycle traps the unique possible interior endpoint

For a specific solution, assign each cell the full orientation it has on that solution. Form its compatible graph by including an adjacency exactly when rolling between its assigned states is legal. This graph can contain unused edges and cycles; its edges are not all claimed to be selected.

**Theorem 4.** Every compatible simple eight-cycle in the orientation field of a corner-start Hamilton path surrounds its final endpoint. It is necessarily the perimeter of a 3-by-3 cell square. There can be at most one such eight-cycle in the solution's compatible graph. In particular, an endpoint-free fully covered gadget containing both the cycle and its enclosed center cell cannot realize such an orientation-consistent eight-cycle.

**Proof of the geometric assertion.** For a simple unit-grid polygon of length eight, let a,b be its bounding-box side lengths in unit steps. Then a+b≤4, so its area is at most ab≤4. Its eight boundary lattice points and Pick's formula give area I+3≥3. Thus the interior comprises either three or four unit faces. In the four-face case equality in the bounding-box bound forces the 2-by-2 unit-face square, whose cell-boundary vertices form the claimed 3-by-3 cell perimeter.

The three-face case is impossible for a rolling cycle. To see this without assuming a full-state girth theorem, encode opposite-face pairs by

    c(1)=c(6)=0; c(3)=c(4)=1; c(2)=c(5)=2 modulo 3.

In a fixed phase, the color change black-to-white is +1 on horizontal edges and −1 on vertical edges, or the simultaneous sign reversal in the other phase. Summing these increments around a cycle shows that the checkerboard imbalance of its enclosed unit faces is divisible by three: each elementary square contributes its checkerboard sign modulo three. A connected three-face polyomino has two faces of one color and one of the other, giving imbalance ±1, a contradiction.

**Proof of the endpoint assertion.** Start the 3-by-3 perimeter at its bottom-left corner with arbitrary orientation q0 and follow E,E,N,N,W,W,S,S. This returns to q0. For the reference q, the four possible arrivals at the center, respectively from the bottom, right, top, and left middle boundary cells, demand the following center orientations:

    (5,2,4,3,1,6),
    (4,3,6,1,2,5),
    (5,2,3,4,6,1),
    (4,3,1,6,5,2).

They are pairwise distinct. Changing the reference orientation only permutes the face labels, preserving distinctness. These are all four physical neighbors of the center, so every possible center orientation is compatible with at most one neighbor. Yet the center is compulsory. It must therefore be an endpoint of the Hamilton path. It cannot be the starting board corner, since all its four neighbors are board cells. It is the final endpoint.

The center uniquely determines this 3-by-3 square and its perimeter, so two distinct such compatible cycles would force two distinct final endpoints. ∎

**Safe propagation consequence.** If all eight ring orientations are already pinned and form this compatible cycle, a branch whose chosen endpoint is not the center can be rejected. If two distinct fully pinned compatible eight-cycles surround different centers, the instance has no corner-start Hamilton path in that pinned field. This consequence does not permit treating every cycle in a label-only phase projection as if its ring orientations had been simultaneously selected.

The deterministic checker also classifies every simple full-state closed polygon of lengths four, six, eight, and ten. It finds none of lengths four or six, the above square at eight, and the 2-by-5 cell perimeter at ten, up to translation, reflection, rotation, and reversal. Only the eight-cycle assertion is used in the analytical theorem; the ten-cycle classification is retained as a bounded finite certificate.

## 5. Exact remaining reduction obligation

These results isolate a useful construction boundary:

1. Nonadjacent rigid neutral ribbons are available with complete label-only and endpoint proofs.
2. Adjacent neutral detours necessarily permit local endpoint migration.
3. The simplest all-state collar creates compulsory low-degree cells.
4. An eight-cycle cannot provide an internal endpoint-free switch on a fully covered board.

A hardness reduction still needs a family of fully covered tiles with a genuinely selectable interface, exact permissible boundary crossings and entry states, composition that labels every remaining rectangle cell, and a proof that every globally connected Hamilton path decodes to a source solution. Conversely, no conclusion about polynomial-time solvability follows from the obstructions. The positive ribbon deliberately forces all vertical edges; it does not resolve the remaining connected edge-selection problem.

## Verification and source boundary

The accepted finite checks exhaust the stated small selectable-initial-state ribbons, all 24 center/rail orientations, every choice of opposite-label signs on a four-cell collar, and every simple rooted directed grid polygon through length ten. Larger ribbon tests verify the exact reachable orientation field and rung formulas, not merely one positive path. Their scopes and aggregate outcomes appear in [VERIFICATION_SUMMARY.json](VERIFICATION_SUMMARY.json). Small exact authored data and a program-independent checking procedure appear in [EXACT_AUTHORED_CERTIFICATE.json](EXACT_AUTHORED_CERTIFICATE.json) and [CERTIFICATE_GUIDE.md](CERTIFICATE_GUIDE.md). The arbitrary-size claims rest on the proofs above; bounded tests are regression certificates.

This work builds on the previously accepted orientation parity, unique-edge, and checkerboard-area lemmas, restated in [FOUNDATIONS.md](FOUNDATIONS.md). The parity reduction is attributed in the first-pass report to Buchin et al., *On Rolling Cube Puzzles* ([author-hosted full version](https://erikdemaine.org/papers/DiceRolling_CCCG2007/paper.pdf)). The exact target and source distinctions are documented in the [first edition's source-model audit](../5500068_labeled_die_first_20261013/SOURCE_MODEL_AUDIT.md) and [TOPP Problem 68](https://topp.openproblem.net/p68). De Biasi's blocked-cell manuscript and known nonuniqueness board are not being converted into a no-hole hardness theorem. No copied source board, source text, or third-party source document is included in this edition.
