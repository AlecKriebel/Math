# Checking the exact second edition certificates

[EXACT_AUTHORED_CERTIFICATE.json](EXACT_AUTHORED_CERTIFICATE.json) contains exact authored finite examples and abstract semantic tests. The statements for arbitrary board sizes are proved in [CYCLE_RANK_KERNEL.md](CYCLE_RANK_KERNEL.md) and [NO_HOLE_GADGETS.md](NO_HOLE_GADGETS.md). A finite check does not replace those proofs. No source-paper board, route, orientation table or copied source document occurs in the certificate.

## Conventions and elementary checking

Every coordinate is `(x,y)`, with the origin at the bottom left, x increasing east and y north. This edition uses that convention throughout its certificate. Every state has ordered entries `(top,bottom,north,south,east,west)` and belongs to the 24 rotations of `q=(1,6,2,5,3,4)`. Reflections and opposite chirality are not permitted.

For a state `(t,b,n,s,e,w)`, the four exact roll permutations are

    N: (s,n,t,b,e,w)
    S: (n,s,b,t,e,w)
    E: (w,e,n,s,t,b)
    W: (e,w,n,s,b,t).

The certificate lists all 24 states and their four successors. Starting at q, repeatedly applying these four permutations yields exactly that closed state set. Opposite faces still sum to seven. The parity of the permutation of the three opposite-face pairs among the world axes flips on each roll. XOR that parity with `(x+y) mod 2` to obtain the invariant phase, normalized to zero at q at the origin.

For every route, begin with its listed initial state and cell. Update coordinates by the indicated unit move and update the state by its permutation. Compare every resulting pair with the next listed visit. A path's visits must be distinct and cover its claimed cell set. Its top at each visit is the board label. A closed perimeter has its repeated starting cell and restored state only as the final closing entry; it is not a Hamilton path with an allowed revisit.

An independent physical check can avoid these tuple permutations: label the six coordinate unit normals by the faces of q, and rotate all normals through a right-angle tip. Read the labels at the positive vertical, negative vertical, north, south, east and west normals. The independent mathematical audit used such integer-vector rotations.

## The 4 by 3 ribbon

The three bottom-to-top label rows are `1 3 1 3`, `5 5 5 5`, and `6 4 6 4`. The certificate gives the complete 12-cell serpent and its reversal. The forward word is `NNESSENNESS`; the final state is W(q), also the state after the three east rolls of the straight port displacement. The reverse starts at `(3,0)` in W(q) and ends at `(0,0)` in q.

The certificate checks every one of the rectangle's 17 physical adjacencies. For each, compare the new top against the neighboring label, then compare the complete state against the assigned neighboring state. Exactly the eight vertical edges and three serpent rungs are compatible. Thus every edge of the reachable graph is selected by the unique path. This finite example is particularly transparent; larger ribbons can have unused compatible rungs.

The eight periodic horizontal-rule records cover each column parity and each row residue modulo four. Compare the east result with the next column's assigned state. Both label and full-state compatibility occur exactly at residue two after an even column, or residue zero after an odd column. This table supports the four-residue calculation in the general proof; the vertical roll identity is immediate from the definition of the field.

All four top-1 starting states are included. Test north against label 5 and east against label 3. The only north-compatible starting state is q. The only east-compatible starting state reaches the state displayed in Theorem 2, from which no unvisited next neighbor has the correct top. Checking just the displayed serpent would establish existence only. These first-move cases plus the forced odd-row argument establish the claimed selectable-initial uniqueness. The general ribbon theorem separately handles all even widths and heights congruent to three modulo four.

An embedded ribbon needs the exact two external accesses, the specified entry state in either direction and both global endpoints outside it. Neither this data nor the ribbon theorem establishes that such boundary isolation can be implemented in a filled larger rectangle.

## The 2 by 5 adjacent neutral cap

Replay the intended word `NNNNESSSS` and the alternate word `ENNNNWSSS` from q at `(0,0)`. Each visits all ten cells exactly once. Compare their state dictionaries by cell, disregarding visit order: the full states agree at every cell. The intended terminal state is E(q) at `(1,0)`; the alternate endpoint is `(0,1)`.

This is the authored example underlying the general endpoint-migration theorem. The theorem applies to every nontrivial adjacent-port neutral detour, by traversing its last cell first and reversing the remaining original path. Its proof does not rely on testing only this cap.

## The eight-cycle and the center

Replay `EENNWWSS` around the 3-by-3 perimeter. The final closing state equals q. Roll toward `(1,1)` from the four middle boundary cells. The certificate supplies each departure state, roll direction and demanded arrival state. These four demanded states are pairwise different. The list of all 24 possible center states therefore gives compatible degree zero or one, never two.

This proves the local state calculation used by the endpoint theorem. The independent geometric argument in Theorem 4 first rules out every other perimeter-eight polygon by the checkerboard-area condition. A compulsory center with compatible degree at most one must be the final endpoint because it is not a board corner. A gadget conclusion requires the center to be part of that same endpoint-free gadget. A ring with an omitted center does not satisfy this condition.

## A four-cell pair-copy collar

The rail is the eastward sequence of four states generated by `EEE`, at y=0. Its labels are `1 4 6 3` and its phase is zero. At y=1, the certificate lists all sixteen independent choices of retaining a rail label or replacing it by its opposite.

For each corresponding rail/collar pair, equal opposite-face pairs forbid a cross-edge in every orientation. To check this directly, examine all 24 states with the rail top and roll north; none has the collar top. For each consecutive collar pair, exactly one full east-roll transition has those labels. Its phase at its actual coordinate is one, the opposite of the rail phase. The certificate records those states and phases.

The two interior collar cells, `(1,1)` and `(2,1)`, have no railward or along-collar move in the rail phase, leaving at most one outward neighbor each. They cannot be board corners. The arbitrary-direction, arbitrary-orientation and arbitrary-length theorem follows from the phase proof, not an assumption that this particular finite rail suffices. The accepted independent audit separately checked all four rail directions, both collar sides, all 24 orientations and all sixteen sign assignments.

## Affine enumeration with loops and parallel edges

The abstract multigraph has vertices 0 and 1, three distinct parallel edges numbered 0, 1, 2, and a loop numbered 3 at vertex 0. Both vertices are terminals. Its cycle rank is `4−2+1=3`. The spanning tree and base terminal path both use edge 0. The fundamental even-degree edge sets are `{0,1}`, `{0,2}` and `{3}`.

XOR the base path with each of the eight subsets of these three basis vectors. The certificate lists all eight results and their degrees, counting a loop twice. Every odd-vertex set is `{0,1}`. Selecting a loop is rejected. Without a loop, selecting all three parallel edges has wrong exact degree; the three singleton parallel-edge selections are exactly the accepted paths.

This demonstration checks the affine mechanism, including loops and parallel edges. It is an abstract multigraph, not a claim that this multigraph is realizable as a propagated die board. The general dimension proof works for every connected multigraph by eliminating non-tree edges until an even-degree forest remains.

## Separate semantic safeguards

The final certificate section retains five small abstract records representing six accepted audit checks. Ports use letters and state tags use symbolic integers. They describe the information the contracted solver must retain; they do not supply physical die boards or claim surviving ambiguity.

1. A selected edge between two terminals plus a disjoint two-edge parallel cycle passes all local degree, port and state tests. The unselected connecting edge makes the candidate graph connected. Requiring selected connectedness rejects the selection. This is two checks: local acceptance and global rejection.
2. A three-node path can use one end of a forced chain twice and leave the other end unused. Exact contracted-node degrees alone would miss this. Check the incidence count at each named port.
3. Replacing one edge in the preceding record uses the two distinct chain ends and passes the port test.
4. Two selected edges demanding distinct symbolic states at the same singleton fail state consistency, even though their degrees and connectedness are correct.
5. A selected loop closes its contracted forced component and must reject; the displayed record also violates an exact terminal degree. It is a direct rejection example, not an assertion that loop rejection is independent of every other condition in that particular record.

For each record, count selected edge incidences at nodes and named ports, compare node and port quotas, compare tags at each port and compute connected components of the selected graph. Preserve parallel-edge identities. This reproduces every stated outcome.

## Broader verification metadata and its limits

[VERIFICATION_SUMMARY.json](VERIFICATION_SUMMARY.json) records previously accepted producer and independent checks separately. The independent audit covered 40,032 endpoint/final-state branches on 1,920 board/initial-state cases, 3,174 connected multigraphs, the listed gadget families and short polygons. These are aggregate outcomes of the accepted tests; this edition does not distribute their implementations or raw outputs.

A reader can independently reproduce bounded checks by enumerating the stated finite objects and comparing the full algorithm with physical path enumeration. On a labeled board, enumerate all nonrevisiting routes from each eligible initial state, accepting only top-matching landings. Group complete routes by endpoint and final state. Compare every group with the propagated, contracted, affine-search algorithm. For a small connected multigraph, enumerate all edge subsets and compare its exact odd-vertex sets with the affine vectors. For a polygon, enumerate unit-step simple closed routes of the stated length rooted at the origin; test whether the closing roll restores the initial full orientation.

The 270-cell source-branch aggregate requires the separate publicly cited source and is not independently reconstructible from this edition alone. Its board data are intentionally not reproduced. It counts one shared branch of two known witnesses; it does not establish new nonuniqueness or count other branches. Public-source identities are inherited from the accepted source audit; no new literature search is represented.

The manifest's byte lengths and SHA-256 values detect modified files. They do not certify mathematical correctness. The independent proof challenge, complete arguments and inspectable exact authored data provide the mathematical evidence.
