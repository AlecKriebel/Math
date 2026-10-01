# Author turn3: finite-state exclusion of every rectangle with a side at most30

**Exact fixed-width computational proof, not a global impossibility theorem.** 2026-10-01.

The character restrictions narrow odd candidates but do not settle existence. This turn builds a finite frontier automaton whose exhaustive closure excludes every height at specified widths. It does not confuse a capped search with closure.

## 1. State definition and complete transitions

Fix width W and process a rectangle upward from its bottom edge. A state(s,p) consists of a bit mask s in the next six rows and the parity p of the number of tiles already placed. A bit at x+Wy marks an occupied cell. All rows strictly below the frontier are completely occupied and have been removed. The lowest row is not full; after every placement all newly completed lowest rows are immediately removed by right-shifting the mask W bits. The empty start state is(0,0).

Take the leftmost unoccupied cell in the lowest row. The tile covering it in any completion cannot have a cell below that row, because all lower cells are already occupied by previous tiles. Thus its minimum y-coordinate is0 and it is an allowed orientation of P with an integer horizontal offset. Enumerate every orientation and every bottom-row cell which could cover the selected gap, reject offsets outside the width and reject occupied-cell overlap. Add the resulting mask, strip completed rows, and toggle p. The tile height is at most6, so no transition needs a seventh row. Hence the state space is finite, bounded by2^(6W+1).

Every real tiling determines a path in this graph: repeatedly select its tile covering the current first gap. Conversely every path returning to an empty mask corresponds to disjoint legal placements, and the stripped full rows give a rectangle. For a nonempty return path, the height is positive by area conservation

    popcount(s_next)=popcount(s)+14-W*(rows stripped).

The original problem's arbitrary congruent placements are covered by turn1's grid theorem. No edge-to-edge assumption, search heuristic, boundary symmetry reduction, or height cutoff is introduced here.

A positive rectangle exists at width W exactly when a nonempty reachable path returns to an empty mask. An odd rectangle returns with p=1. Tracking both parity states prevents an invalid identification of paths with different tile counts.

## 2. Exhaustive results and reproducible certificates

Breadth-first search exhausts the entire reachable graph for every width W=1,...,30. None of these thirty graphs has any transition returning to an empty mask, of either parity. Therefore **no finite rectangle with a side at most30 can be tiled by P**, regardless of the other side's size.

The complete state and edge counts and their deterministic SHA-256 digests are in turn_3_checks.json. The exact program regenerates every state and checks every outgoing legal move; no external SAT/ILP solver or uncheckable oracle is used. Selected counts are:

- W=6:21 reachable states,20 transitions
- W=18:2,216 reachable states,2,226 transitions
- W=30:188,423 reachable states,189,975 transitions

The sum over all thirty complete graphs is463,612 reachable states. The program also independently compares the gap-anchored placement list with a list built from every orientation's permitted bounding-box translation, so it checks coverage of the local move enumeration.

The graph model has a positive control: the complete396-tile84×66 witness is followed tile by tile through exactly these legal frontier transitions and returns to the empty mask at height66. This guards against a transition rule that wrongly rejects all rectangular tilings.

## 3. Explicit incomplete search

At W=42, the search was stopped at the declared cap of300,000 discovered states, with233,511 states still queued. It is **inconclusive**. There was no odd return among the explored transitions, but the graph was not exhausted; no statement about all width42 rectangles follows. Widths31 and above are not excluded by this turn.

The height-uniform negative claims for widths1–30 come from complete finite-state closure, not merely testing finitely many target heights. Nevertheless only those widths are covered. There is no inference to all widths.

## 4. Consequence for an odd target

Combine the complete strip exclusion with turn2. An odd rectangle would have an odd side at least31 and an even side congruent to6 modulo12, hence at least42. Its tile count is therefore at least(31*42)/14=93 and congruent to3 modulo6. This is a proved lower bound, not a claimed minimum or a claim of improvement on all published searches. Reid's source reports a stronger minimum for any rectangle; this packet has independently checked the even witness, not reproduced that source's full minimality computation.

## Remaining route

A large-width odd rectangle remains possible. To avoid only increasing search caps, the next turn explores an explicit periodic lattice construction and identifies its boundary obstruction. Periodic or signed tilings will not be mistaken for positive rectangular witnesses.

Substantive author turns:3/5. Estimated completion30%. Original unresolved; no novelty claim.
