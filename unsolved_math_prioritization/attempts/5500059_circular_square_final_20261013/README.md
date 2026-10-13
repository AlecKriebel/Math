# Circular partitions of a square: fifth and final edition

Problem: row 1757 / 5500059 / AMR0540059. Date: 2026-10-13.

**Status: unresolved.** This is the fifth and final newly documented substantive pass of this continuation. The prior lifetime attempt count is unknown. There are at least five newly documented passes; no sixth pass is started or claimed.

## What this edition establishes

- The original 56-cell coarsened boundary family is retained exactly and extended by 80 strictly convex hexagons. All 136 cells have independent inscribed/enclosing-disk witnesses proving actual circularity strictly below 64439/50000 = 1.28878.
- All 9,180 unordered pairs have exact separating witnesses. The independent audit additionally classifies each intersection and checks the full 592-edge residual cycle and all 144 two-cell residual angles. The square boundary is covered and an open neighborhood of its center remains uncovered.
- The covered area is approximately 32.24892181598094% of the square. This is a partial collar, not a finite partition of the square. The collar number 1.28878 cannot replace the full-square upper bound 1.295516.
- A sharp theorem for arbitrary convex pentagons with two adjacent right angles gives R/r >= rho = 1.290772978969... . The proof allows independent incenter and circumcenter and constructs an attaining tangential cyclic pentagon.
- A separate exact perturbation argument forbids pentagonal caps on two specified full facets with exact equal-unfilled-sector-bisector seams. It does not exclude other seam directions, facet subdivisions, hexagons, or general completions.
- A different, explicitly specified three-cell dead-end collar cannot be completed at ceiling 13/10 because its residual angle is too small. That local obstruction is not asserted for the accepted 136-cell partial collar.

Retaining this 136-cell family requires at least 310 further pentagons and at least 446 cells in any completion below sqrt(2). At a ceiling at most 13/10 the exact deficit identity is

    P5 = 310 + sum_{k>=7}(k-6)Pk + T + 2V4.

These are necessary conditions. Neither a 446-cell completion nor any finite completion of this partial collar at 1.28878 is proved. The exact optimum and unrestricted finite attainment remain unresolved.

## Unchanged whole-square bounds

The [fourth-edition complete construction](../5500059_circular_square_fourth_20261013/FOURTH_PASS_CONSTRUCTIVE_UPPER_BOUND.md) partitions the square into 121 positive-area strictly convex polygons and proves the strict upper bound 1295516/1000000 = 1.295516. Its [certificate](../5500059_circular_square_fourth_20261013/rational_partition_certificate.json), full pair data, strict margins, and independent audit remain unchanged.

Together with the [previously audited source context](../5500059_circular_square_first_20261013/SOURCE_BOUND_AUDIT.md), the statement remains

    G <= Gamma_fin < 1.295516,
    G = 1.2886844618704579... .

The value G is prior context, not a new lower-bound theorem or a demonstrated optimum. No literature-priority or novelty assertion is made.

## Read the complete arguments and exact data

- [Final interior-completion report](FINAL_INTERIOR_COMPLETION_STATUS.md): the construction, angle argument, exact local dead end, and remaining finite-completion burden.
- [Sharp and stable pentagon obstruction](ADJACENT_RIGHT_PENTAGON_OBSTRUCTION.md): full proof, attaining pentagon, explicit stability constants, and the restricted near-90.30-degree facet argument.
- [Certificate guide](CERTIFICATE_GUIDE.md): coordinate conventions, all-pair records, margin equations, exact angle tests, and independent verification.
- [Integration and acceptance](INTEGRATION_AND_ACCEPTANCE.md): scope, evidence, historical count, and unresolved questions.
- [Independent geometry review](INDEPENDENT_GEOMETRY_REVIEW.md) and [independent pentagon review](INDEPENDENT_PENTAGON_REVIEW.md).
- [Full partial-collar illustration](partial_collar.svg) and [one canonical collar](canonical_collar.svg). Both are passive rounded illustrations; exact rational certificates control the claims.

The [public manifest](PUBLIC_MANIFEST.json) binds every file in this edition and the complete transitive public sibling dependencies. The first four editions are preserved unchanged.
