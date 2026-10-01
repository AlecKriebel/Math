# Independent review: exact corner-cut 14-omino, problem 3900010

## Verdict and binding scope

**PASS_SCOPED_PARTIALS_ORIGINAL_UNSOLVED_5_OF_5.** No mandatory mathematical
correction was identified. This is a pass for the precise partial claims and
their limitations, not a resolution of the original odd-rectangle question.

The reviewed author snapshot is bound by:

* `FROZEN_MANIFEST.json` SHA-256
  `e557dd21dc1738440fda6948d36a2e5966217af3d55fa781f5dbc473e1a8e06b`,
  listing 34 files;
* `RESULT.md` SHA-256
  `bc7bf5c765afffaca44384a4b156c4f3f0e424bcad24ff0b5fff4231fff26cab`;
* the five unchanged turn files, all checkers, coordinate certificates, and
  source manifest included in that frozen snapshot.

All 34 author hashes and seven primary-input hashes match. The five supplied
receipts replay byte-for-byte. Three separately authored reviewer checkers,
which import no author module, pass **535,005 exact assertions** in total.
The author files were not edited. The reviewer did not contribute a new author
search turn or extend the five explicitly inconclusive boundary-repair cases.

The original target remains: does this exact tile admit a finite rectangle
tiled by an odd number of congruent copies, allowing reflections and rotations?
Neither a positive witness nor an obstruction for all rectangle dimensions is
present. The appropriate original status remains **unsolved, 5/5**. Publication
requires the parent's separate gate; this review does not create a PR or
modify the queue. No novelty or priority is certified.

## 1. Exact source and shape

The live [Eppstein source item](https://ics.uci.edu/~eppstein/junkyard/open.html)
specifies a 3-by-6 rectangle with a 2-by-2 bite removed and links to the exact
Reid `14omino02` item. The complete
[restored Reid item](https://sicherman.net/mikereid/14omino02_rect.html)
states the odd-number-of-copies question and displays the 66-by-84 even example.
Its date is 2005. The
[restoration provenance](https://sicherman.net/mikereid/index.html) explains the
archive's relationship to Reid's former website; it does not turn the 2005
open-status sentence into a modern resolution check.

I visually inspected the exact tile and even-rectangle images. Independent
pixel checks recover six white cell centers in the top row and four in each
of the next two rows. The source's different `14omino01` is not the target.
Every one of the 10,938 internal unit-cell adjacency edges in the source's
even-witness bitmap agrees with the supplied coordinate certificate, including
which adjacencies are separated by a tile boundary. Thus the coordinate data
are verified against the actual credited diagram, not merely against its
reported dimensions.

The complete Reid 2008 paper's definitions permit congruent copies and explain
how rotations and reflections are represented by including all orientations.
Its example concerning the other 14-omino is not substituted for this one.
The inaccessible full 1997 and 2014 texts are not claimed to have been read or
used. The author's statement that limited searching found no verified newer
resolution is retained as a retrieval report, not a proof of current openness.
The source's minimality assertion is likewise not re-proved by this packet.

## 2. Euclidean-to-grid reduction

The reduction is sound without assuming edge-to-edge matching. In a finite
tiling, a generic interior path can avoid all arrangement vertices and cross
tile boundaries transversely. It therefore connects tiles through positive
boundary segments. At least one tile shares a segment with the rectangle
boundary; its orthogonal edge frame is aligned with the rectangle. Segment
adjacency propagates that frame throughout the tiling. Reflections are
included, so all eight D4 orientations are allowed.

Once the frames are aligned, a generic horizontal line cuts a tile into
intervals with integer lengths, since their endpoints are differences of
integer coordinates in that tile's translated local frame. Starting at the
rectangle's left boundary forces every successive crossing coordinate to be
integral. Every vertical tile edge is crossed by some such generic line.
Repeating vertically proves the corresponding assertion for horizontal edges.
This establishes integral vertices and dimensions even with partial-edge
contacts and T-junctions. Finiteness and genuine interior-disjoint positive
tiling are essential hypotheses and are correctly present.

The 396-copy, 84-by-66 positive control independently has one and only one
copy covering every cell. It is even and gives no odd-case result.

## 3. Stripe and complex-character claims

The stripe sums of the eight oriented tiles are exactly the stated pairs:
one coordinate is zero, and the other is positive or negative six. Odd tile
count makes the rectangle area have 2-adic valuation one. Hence one side is
odd, its even partner is 6 modulo 12, and the tile count is 3 modulo 6.

The reflection comparison in Turn 2 exhausts the possibilities for nonzero
complex characters. As a separate algebraic check, computing the Gröbner
basis over the rationals of the eight oriented tile polynomials gives exactly

\[
 S_6(x),\qquad (x+1)(y+1),\qquad S_6(y).
\]

Their common zero set is precisely the nine stated points. This exact
polynomial check uses no floating-point root test. The associated rectangle
conditions follow from finite geometric sums and agree with the author's
formula. Both the proof and the disposition appropriately restrict
completeness to this multiplicative-character class. Neither claims a complete
classification of all additive invariants or a sufficient tiling criterion.

## 4. Frontier completeness and all-height exclusions

The crucial finite-state argument passes an independent reconstruction.

At the first empty cell of the lowest unfinished row, the tile covering that
cell in a genuine completion cannot extend below the row: every lower cell
is already occupied. It therefore has minimum height zero relative to the
frontier. Enumerating all contained horizontal translations of every oriented
tile enumerates every possible move. A tile has height at most six, so a
six-row state is sufficient. Stripping only full bottom rows preserves all
unresolved occupancy. The parity coordinate is retained.

Every rectangular tiling determines a path by repeatedly taking its tile at
the first gap. Conversely each nonempty path returning to the empty frontier
specifies pairwise disjoint legal tiles filling a rectangle. Area conservation
forces the total number of stripped rows to be positive on such a return.
Thus complete reachable-state closure at a fixed width covers every height,
rather than just a finite height range.

My implementation uses a six-entry tuple of row masks, a depth-first stack,
and a direct column scan. It does not import the author's single-mask
breadth-first search or its transition generator. For every width 1 through
30 it recovers the same entire state-set hash, state count, and transition
count. The sum is **463,612 states**, with **468,603 transitions**, and no
return at either parity. This verifies the all-height nonexistence result for
these thirty widths. The known even certificate is also checked as a legal
positive path by the replayed author verifier.

The width-42 computation is capped. Its nonempty unprocessed queue is
explicitly retained and no exclusion at width 42 is approved. The width
exclusions plus the stripe restrictions do imply odd side at least 31, even
side at least 42, and at least 93 tiles. They do not imply that 93 is attained
or that the source's stronger reported minimum was independently reproduced.

## 5. Periodic and fixed-orientation arguments

The residue map (x+4y\pmod {14}) is bijective on the fourteen tile cells.
Consequently the translates by its kernel give a genuine plane tiling. The
finite torus partitions follow because the displayed rectangular period
lattices lie inside that kernel. My checker independently verifies all four
recorded torus partitions, their odd counts, injectivity of each projected
tile, and seam-crossing placements.

These projections do not yield positive planar rectangle tilings. In
particular, the 14-by-7 rectangle fails the stripe test, and the 42-by-7
rectangle is excluded by the width-seven exhaustive graph even though it
passes the tested characters. This directly confirms the scope distinction.

For translations of the single fixed orientation, the rightmost tile meeting
the bottom boundary has its four-cell bottom row ending at the rectangle's
right edge. Its six-cell top row then exits the rectangle. This proves the
stated impossibility for that subclass and does not exclude rotated or
reflected repairs. The even-seed juxtaposition argument is simply induction
on addition of even tile counts; its narrow scope is correctly stated.

## 6. Boundary-repair and binary certificates

All 28 fixed-interior models were reconstructed independently. The retained
tiles are disjoint because their origins lie in one coset of the residue
kernel. The independently enumerated repair-placement counts and connected
component sizes match the author's data. A connected tile cannot cover cells
from distinct edge-connected components of the available region, so the
fourteen component-area obstructions are valid.

The nine claimed complete negative cases were additionally checked with a
separate, uncapped exact-cover search selecting a cell with the fewest
currently available placements. All nine exhaust with no repair. This
differs from the author's first-cell rule and confirms that the conclusion
does not depend on treating a capped search as complete. The five author
models marked inconclusive were not extended by the reviewer. Their status
remains inconclusive, and all twenty-eight conclusions apply only to their
specified frozen interiors.

For the 42-by-31 binary test, the 403 selected placements are distinct,
contained, and congruent to the tile. Their multiplicities match the complete
reported histogram; every cell has odd multiplicity, with maximum 19. A
separately implemented low-pivot Gaussian elimination, with a different
placement ordering, confirms 8,452 columns, rank 1,293, and membership of the
augmented target vector. This is an F2 overlap certificate, not a positive
tiling or an integer signed tiling.

The stated coloring barrier follows by pairing that exact vector identity
with an arbitrary linear functional on the cell coordinates and the count
coordinate. Therefore no F2 cell weighting giving every allowed placement
the same common weight can obstruct this particular odd target. Other
characteristics, integral or nonlinear obstructions, and geometric positivity
remain outside that conclusion.

## 7. Reproducibility and disposition

The author receipts reproduce exactly with assertion totals 11,504; 40,877;
2,087,728; 14,880; and 6,530. The separate reviewer receipts contain:

* `independent_checks.json`: 509,627 exact assertions, including every closed
  frontier state set and the independently computed character ideal;
* `independent_boundary_checks.json`: 8,834 exact assertions, including the
  nine uncapped negative reconstructions;
* `source_checks.json`: 16,544 exact assertions, including all hashes and
  pixel-boundary comparisons.

One disposable reviewer polynomial diagnostic initially had a Python argument
unpacking typo; it was corrected before any result was recorded. All final
review checkers pass. No author mathematical correction was requested.

The five substantive author events are present and consistently counted.
Historical completion percentages in the author packet are subjective author
estimates, not calibrated probabilities, theorem evidence, or part of this
review's verdict. They should not be promoted into a result summary.

The review approves publication of these scoped partials as an **unsolved
five-turn attempt**, subject to the parent's publication gate. It does not
approve a claimed solution, unrestricted oddness obstruction, new minimum,
or a statement that periodic/modular tilings solve the positive rectangle
problem. The full original gap is explicit and remains open within this work.

Portable review files are the report, three reviewer scripts, three reviewer
receipts, the author-replay receipt, and `REVIEW_MANIFEST.json`. Reading copies
and replay directories are excluded from publication.
