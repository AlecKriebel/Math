# Exact corner-cut14-omino: partial results on odd rectangular tiling

**3900010 / AMR-038-0010. Original unresolved after five substantive author turns.** This frozen author packet awaits independent review. No positive odd rectangle, global impossibility, new minimum, or historical novelty is claimed.

## 1. Exact source and geometry

The source-linked shape is Reid's14omino02: a3×6 rectangle with a2×2 corner removed, with row lengths6,4,4. The exact source diagram and its66×84 tiling were visually inspected. The mathematical cell model is in [tile.json](tile.json). Copies are congruent, with rotations/reflections permitted and no independent rescaling. The target is a finite rectangle containing an odd number of copies, not a larger similar copy of the nonrectangular tile.

The similarly named14omino01 is a different T-shaped tile and has a known odd tiling; that result is not substituted here. The restored author page still describes oddness of the target as unknown, but its date is2005 and a limited literature search cannot certify current openness. The full1997 paper and2014 paper were not recovered; no unverified theorem from them is used. The exact source question and diagram were recovered fully. See [SOURCE_SCOPE.md](SOURCE_SCOPE.md) and [source_manifest.json](source_manifest.json).

## 2. Complete Euclidean-to-grid reduction and positive control

[Turn1](TURN_1.md) proves that every finite congruent tiling of a rectangle by this tile is equivalent to an integer D4 placement tiling. The positive-edge adjacency graph of the tiles is connected by generic paths avoiding finitely many junctions. A boundary tile fixes the axis directions, and adjacency propagates them. A generic horizontal or vertical line cuts each tile into integer-length intervals, so starting from the rectangle boundary forces all crossing coordinates and all tile vertices to be integral. This does not assume edge-to-edge contacts.

The credited even rectangle was transcribed from Reid's diagram into [known_even_witness.json](known_even_witness.json). A standalone checker reconstructs all396 tiles in an84×66 rectangle and verifies every cell exactly once. The coordinate certificate is mathematical data with explicit source attribution; the original image is not republished. This validates the even witness, not the source's claimed minimality search.

## 3. Odd dimensions and exact complex-character obstruction class

[Turn2](TURN_2.md) applies stripe colorings to all eight orientations. Horizontal length-six tiles have stripe sums(0,±6), and vertical ones have(±6,0). If N is odd, WH=14N has exactly one factor2. Thus the even side is6 modulo12, the odd side is odd, and **N is3 modulo6**.

It also classifies all nonzero complex pairs(x,y) for which the multiplicative cell character x^i y^j annihilates every allowed tile placement. With

    p(x,y)=S4(x)S3(y)+x^4(1+x)y^2,

comparison with reflected polynomials gives exactly the nine common zeros

    {(-1,z):z^6=1,z≠1} union {(z,-1):z^6=1,z≠1}.

A rectangle passes all these characters exactly when both sides are even, or its odd side is paired with a side divisible by6. This is complete only for this specified character class. It is not a classification of integral, finite-field, derivative, nonlinear or boundary-word invariants, and passing it does not prove tilability.

## 4. Exact all-height exclusions at fixed widths

[Turn3](TURN_3.md) defines a complete six-row frontier automaton with tile-count parity. Every legal tiling yields a path by repeatedly placing the tile covering the first unoccupied cell of the lowest unfinished row; conversely a nonempty return to the empty frontier yields a rectangle. The mask height is bounded by6 because every tile has height at most6. Complete reachable-state closure therefore addresses every height at a fixed width.

The graphs for **all widths1 through30 are exhausted**, with463,612 total reachable states and no return at either parity. No finite rectangle with a side at most30 is tileable. A second local placement enumeration checks transition coverage, and the known396-tile rectangle follows a legal positive path in the same model.

The width42 graph is **not exhausted**:300,000 states were discovered and233,511 remained queued at the explicit cap. No exclusion of width42 or all larger widths follows. Full per-width counts and deterministic state/edge hashes are in [turn_3_checks.json](turn_3_checks.json).

Combining the proved width exclusions with the stripe restriction, an odd target has odd side at least31, even side at least42, and at least93 tiles. This is a certified lower bound, not a minimum or a claim of improvement on every published search.

## 5. Odd periodic constructions and their boundary failure

[Turn4](TURN_4.md) observes that the14 cells of P represent every residue of x+4y modulo14 exactly once. Thus P is a fundamental cell domain for the translation lattice ker(x+4y mod14), and those translates tile the plane.

The14×7 rectangular torus has an exact7-tile certificate; the42×7 torus has21. Both counts are odd. The former fails the planar stripe test; the latter passes that test but its planar rectangle is excluded by the width7 graph. Several tiles wrap across each chosen seam, so these are **not congruent whole tiles in the planar rectangle**. The certificate explicitly identifies the wrapped placements.

No finite rectangle is tiled by just translations of the single unrotated orientation: the rightmost bottom-row tile would protrude two units beyond the right edge in its top row. This excludes only that fixed-orientation subclass. It explains why one cannot simply cut a rectangle out of the lattice pattern. Likewise juxtaposition/arrays of even rectangular seeds retain an even tile count; those operations on the known witness cannot alone produce an odd seed.

## 6. Final boundary-repair attempt and binary-relaxation barrier

[Turn5](TURN_5.md) attempts an actual odd target42×133, which would use399 copies. For each of14 lattice phases and two protected-interior margins, it fixes a prescribed periodic interior and searches all D4 placements in the remaining repair region. Fourteen models fail by connected-component area divisibility; nine are completely searched without a repair; five hit the10,000-node cap and remain inconclusive. These are only the stated fixed-interior models, not a complete rectangle search. All records and deterministic code are included.

A separate exact F2 relaxation tests the42×31 target. The8,452 contained placements give augmented vectors of their cell incidences and tile-count parity. The matrix rank is1,293. An explicit403-placement XOR certificate covers every cell an odd number of times and has odd placement count. Most cells overlap, with multiplicities up to19; this is **not a positive exact cover**, and is not an integer signed tiling either.

The certificate does prove a precise barrier: no F2 additive cell weighting with one fixed common weight on all permitted placements can exclude this particular odd target. Pairing any such weighting with the exact XOR identity automatically gives the required odd-count relation. Other invariants and geometric constraints remain possible.

## 7. Exact remaining gap and validation

No boundary repair or other construction has supplied a finite positive odd rectangle. No argument excludes every allowed width and height. The thin-strip exclusions, torus patterns, modular overlap cover, and capped searches must retain their respective scopes. Neither periodicity nor an additive relaxation is a substitute for an exact positive cover.

The five diagnostic receipts have11,504;40,877;2,087,728;14,880; and6,530 exact assertions. All replay byte-for-byte. The strip graphs are regenerated exactly, the known even certificate is checked independently of its source image, and the parity certificate is checked independently of the Gaussian-elimination generator. The28 boundary-model receipts replay exactly. The full proofs and completeness arguments accompany those calculations.

The ledger records five substantive attempts and the automatic exhausted state. Source retrieval, checkpoint work, and an intervening independent review of another problem do not add proof attempts. Estimated completion toward the original target:35%.

**Proposed original disposition: unsolved,5/5.** Independent adversarial source/proof/computation review is required before a PR. No sixth author search turn is being supplied by this consolidation.
