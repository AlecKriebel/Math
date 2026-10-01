# Author turn5: boundary-repair search and an exact binary-coloring barrier

**Final author turn. No positive odd rectangle or global obstruction found; original unresolved5/5.** 2026-10-01.

## 1. A genuine odd-rectangle boundary-repair attempt

The periodic pattern from turn4 suggests keeping a tiled interior and repairing only its boundary. The target42×133 rectangle would use399 tiles, an odd count satisfying the stripe restrictions and exceeding the396-tile even control. We tested the following precisely defined models.

For each phase c∈Z/14Z, retain every translated P whose origin obeys x+4y=c mod14 and whose cells all have distance at least m from the four rectangle sides, with m=0 or3. These retained tiles are disjoint, by the lattice proof. Their complement is the repair region. Every D4 placement lying wholly within that region is enumerated. An exact-cover depth-first search selects a tile covering the first uncovered cell, rejecting overlaps; memoization records fully exhausted uncovered masks. A fixed10,000-node cap is used and is reported when reached. No move deletes a retained interior tile.

The recorded results in boundary_repair_receipt.json are:

- All14 margin0 models fail immediately because some edge-connected component of the repair region has area not divisible by14. A connected tile cannot bridge distinct such components, so this is a rigorous obstruction for those prescribed interiors
- Nine margin3 models are exhaustively searched with no repair
- Five margin3 models reach the node cap and remain inconclusive

No model yields a positive odd rectangle. These results do not exclude another interior pattern, a wider repair region, another phase/geometry construction outside the tested model, or even the capped models. They are not a complete search of42×133 tilings. The legal-placement enumeration and the distinction between exhausted and capped searches are explicit in the reproducible code.

## 2. Testing a stronger additive coloring route

A global impossibility proof might use cell weights in F2 and tile-count parity. To test the full class of such linear constraints on one admissible candidate, take the42×31 rectangle, which would require93 tiles. Enumerate every contained D4 placement: there are8,452.

For each placement make a vector in F2^(1302+1): its1302 cell-incidence coordinates, followed by a1 recording its tile-count contribution. A positive odd tiling would express

    target=(1 at every rectangle cell,1 in the count coordinate)

as a sum of these placement vectors. Gaussian elimination over F2 is an exact relaxation, not an exact-cover solver. Its rank is1,293. The target lies in its span.

More importantly, an explicit certificate is saved in parity_42x31.json:403 distinct legal placements XOR to the target. Every cell is covered an odd number of times, and403 is odd. The standalone checker reconstructs every placement, verifies bounds and the XOR identity, and independently recomputes the matrix rank. No trust in an external solver or a claimed numerical rank is required.

The multiplicity histogram is

    1:293, 3:534, 5:200, 7:76, 9:82,
    11:53, 13:42, 15:14, 17:7, 19:1.

Thus this is emphatically **not** a positive tiling: most cells have overlaps. A positive exact cover would have93 tiles and multiplicity1 everywhere. The binary certificate is not a signed integer tiling either; cancellations here are only modulo2.

## 3. What the certificate rules out, and what it does not

Let w assign an arbitrary F2 weight to each cell of this fixed rectangle, and let c∈F2 be a common weight assigned to every permitted tile placement. If each placement has total cell weight c, then summing the403-placement certificate gives total rectangle weight403c=c. That is exactly the relation required of any odd positive tiling. Consequently **no additive F2 cell-coloring with a fixed common tile weight can exclude this42×31 target**. This conclusion covers all such cell weightings, not merely periodic stripe colorings, because the explicit linear identity is tested against every linear functional.

The certificate does not imply that a positive tiling exists. It does not classify integral colorings, other characteristics, nonlinear/boundary-word invariants or all geometric constraints. It also does not say that every rectangle passes a binary test. It only closes this particular proposed linear-obstruction route for one admissible odd candidate. The source's reported minimum, if invoked, is an independent geometric/computational statement and is not contradicted by a modular overlap cover.

## 4. Final unresolved target

The boundary-repair search did not produce a legal odd rectangle, and the binary relaxation shows why one broad parity-coloring strategy cannot by itself reject all candidates. The previous complete transfer certificates exclude only widths1–30; the width42 global graph is still capped. The periodic7/21-tile examples still wrap. Neither an actual finite odd exact cover nor an argument excluding every allowed rectangle has been obtained.

All five substantive author turns are exhausted. Retain the exact Euclidean-to-grid reduction, credited even certificate, dimension/character restrictions, fixed-width exclusions, periodic construction and scoped failed-route certificates. Proposed original status: **unsolved,5/5**. Estimated completion35%. Independent adversarial review is required before any PR, with no further author search turn hidden in packaging or review.
