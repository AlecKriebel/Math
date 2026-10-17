# Independent acceptance of unequal-angle closure of the square boundary

Problem row 1757 / 5500059 / AMR0540059. Review date: 2026-10-13.

## Exact acceptance and essential scope

Accepted within the stated boundary-only scope. For every epsilon > 0, the authored argument constructs finitely many positive-area convex polygons inside a square, with pairwise disjoint interiors, covering every square-boundary point and having circularity at most G + epsilon. It also proves that an open neighborhood of the square center remains uncovered. Thus it removes the prior four mid-side gaps but does not solve interior completion. It establishes no new whole-square upper bound, unrestricted lower bound, optimality, finite-attainment, or infinite-partition equivalence.

The separate exact example consists of 56 finite convex polygons with strict circularity bound 64439/50000 = 1.28878. It likewise covers all four sides and leaves the center and positive interior area uncovered.

Acceptance binds the complete mathematical inputs. The public proof below only normalizes dependency links; the mathematical text is unchanged, and its public-edition identity is recorded here:

- [the complete boundary proof](UNEQUAL_ANGLE_BOUNDARY_CLOSURE.md): 15,423 bytes; SHA-256 `e4b1cdc34d931d7bb403c677a5a6d63fad5f96d65d632f86cd577528953a7120`.
- [the complete boundary certificate](boundary_patch_certificate.json): 104,072 bytes; SHA-256 `197d3db0d83859d542761d0fb4b57ba9b5c34aec4f35f09169f6d458db42dc2c`.
- Complete prior authored [theory](../5500059_circular_square_first_20261013/THEORY_REPORT.md), [quantitative obstruction](../5500059_circular_square_second_20261013/QUANTITATIVE_COMPLETION_OBSTRUCTION.md), [corner-chain proof](../5500059_circular_square_second_20261013/CORNER_CHAIN_AND_BRIDGE_OBSTRUCTION.md) and their [theory](../5500059_circular_square_first_20261013/INDEPENDENT_THEORY_REVIEW.md), [quantitative](../5500059_circular_square_second_20261013/INDEPENDENT_QUANTITATIVE_REVIEW.md) and [corner-chain](../5500059_circular_square_second_20261013/INDEPENDENT_CORNER_CHAIN_REVIEW.md) independent reviews remain unchanged sibling dependencies. They supply the previously accepted balancing constant G and corner construction. They are not replaced by excerpts or hash-only placeholders.

## Independently derived envelope and branch checks

The new independent symbolic checker imports no producer code. It independently constructs the two feet and center, checks all contact distances, the relation R = 1 + y + ab/2, and the translated center. On the stated domain 41/50 <= t <= u <= 1, R > 1 and 1+y > 0, so the squared identities have the required square-root signs.

The three weights sum exactly to one, and their weighted center gradients cancel. Every weight is strictly positive on the entire stated domain: for the only potentially delicate factor, u^2(1+t^2)-1 is at least (41/50)^2(1+(41/50)^2)-1 = 778261/6250000 > 0. The other factors have the signs shown in the proof. The convex weighted sum of active distance functions therefore supports the maximum-radius objective globally at the proposed center. This is a valid sharp three-contact branch, not an unsupported continuation through a branch change.

For a baseline at height -h, the feet forced by the actual indisk and two side supports are affine in h. The weighted derivative with respect to h is independently verified as (t^2u^2+u^2+1)/(8tu) > 0. Joint convexity supplies the stated supporting-hyperplane lower bound for every h >= 1, without assuming baseline tangency or neighboring-disk tangency.

At h = 1, the minimum enclosing circle of the disk and two feet is unique. One elementary justification is that two distinct radius-R centers would give a strictly smaller radius at their midpoint by the squared-distance identity. Its internal tangency to the unit disk excludes a containing finite polygon inside the same outer circle: the unique supporting line at the common tangent point intersects the outer disk only at that point, whereas a positive-area polygon containing the inner disk must have a boundary side on that supporting line. Thus finite polygon equality is impossible, giving the strict quadratic transition obstruction. Reflection transfers the result to the reflected parameter domain via (t,u) -> (1/u,1/t); it does not assert that the original numerical domain already contains those reflected parameters.

## Complete separator segments and matching

Independent exact algebra verifies both second-intersection parameters L and U, both positive extensions beyond the indisk contact points, both opposite-support expressions, and both outer-circle equations. Consequently each compact curved cell has precisely the two claimed complete separator segments. The formula sigma' = sigma U/L matches the entire common segment, including its upper endpoint, rather than merely arranging coincident baseline feet. Opposite supporting half-planes exclude overlap of incident cells. Distinct incenter and circumcenter roles are maintained throughout.

The first cell attaches to the accepted corner through the previously proved exit parameter V and rho = V/L. No unproved mutual disk tangency enters that attachment or later joining.

## Finite angle sequence and global nonoverlap

For fixed epsilon, the stated integer n and arithmetic progression of half-angle parameters form a genuinely finite chain ending at vertical separators. The derivative bound with respect to the second parameter is uniformly below one, while F(t) decreases from G to 5/4. Hence each transition stays below G + epsilon/2, leaving room for polygonal approximation. The exact scale identity proves all scales are at most rho < 0.8, including the final match to the central K(1,1).

The stated nonincident separation estimates were checked by pair class, not inferred from a diagram:

1. A left-chain cell overshoots its right foot by less than sigma U/4. The next cell's baseline width exceeds sigma U/2. Thus every next-but-one and later cell is separated by a vertical line. The same estimate separates nonlast cells from the middle cell.
2. The last cell's right separator is vertical and its entire body lies to the left of its right foot. The symmetric middle cell and reflected half-chain therefore fit with no crossing.
3. Side-chain heights are less than 1.68, while sidewise coordinates from the adjacent corner begin at b > 1.82. This separates perpendicular chains on adjacent square sides.
4. Corner boxes have side less than 2.21; every later chain cell begins beyond 3.22. Exact exit supports handle the first neighboring cell. The square has S > 6.44, which separates distinct corner boxes and far-side patches. Opposite-side strips are disjoint by their height bounds.

These estimates exhaust the pair classes and also give a strict gap around (S/2,S/2). The middle cell plus the reflected half-chain covers the full side interval with exactly consecutive baseline intervals. Applying the square symmetries covers all four sides; corners are counted once.

## Finite polygonal approximation with fixed endpoints

Every curved compact convex cell has arbitrarily close circumscribed finite polygonal approximations. The required extra supports are compatible with that approximation:

- The baseline and separator fix each baseline endpoint.
- At an upper separator endpoint, the separator and tangent to its known outer circle are distinct supporting lines. They fix that exact endpoint because the separator ray meets the circle twice.
- Retaining the same separator for the two incident cells keeps them in opposite half-planes and preserves their entire common segment.

There are finitely many cells at every fixed epsilon. Choose the outer approximation error for each below a common sufficiently small multiple of its positive witness inradius. This preserves all finite strict nonincident, square-side, and central gaps simultaneously. It increases the available enclosing radius by an arbitrarily small multiple of that inradius while retaining the original indisk. Exact baseline intervals remain unchanged, so no square-boundary gaps are introduced. This validates an actual finite polygon family, not a substitution of curved cells or an infinite limiting family.

## Independent exact 56-polygon audit

The separate fresh boundary verifier reads exact rational strings in eight canonical types and expands all 56 specified similarities, reflections and square rotations. It imports no producer verifier. Every type's supplied cycle equals its strict convex hull. All 960 canonical edge-distance inequalities contain the unit indisk, and all 960 canonical vertex-distance inequalities lie strictly inside the proposed enclosing circle. Some indisk inequalities are equalities, which are valid tangencies; the outer inequalities are strictly positive. Exact positive similarities transfer these certificates to all 7,104 placed vertices and edges. All eight types use distinct incenter and enclosing-center locations.

All transformed vertices are in the square. Independent extraction of actual edges on each square side gives 15 exact consecutive intervals per side, starting at zero and ending at the exact side length. Their adjacency independently determines 56 expected contacts.

For every one of the 1,540 polygon pairs, the verifier recomputes all projections and independently chooses a separating axis; producer pair rows are not used to choose it. If the extremal projections coincide, it computes the exact intersection along that line. The results are 1,484 empty intersections and 56 segment intersections, with no positive-area intersections or isolated point contacts. Every segment is exactly one full polygon edge in each incident polygon, and the set of shared-edge pairs equals the adjacency induced by all consecutive square-side intervals. The producer's complete pair table is additionally checked for missing/duplicate pairs and correct vertex half-planes.

The exact sum of polygon areas is strictly below square area. Approximately 31.9451 percent of the square is covered; this numerical orientation is secondary to the retained exact rational area deficit. The center violates at least one inward supporting inequality for every polygon by a strict rational amount, so a neighborhood of the center is absent. Nothing in this calculation claims a square partition.

## Controls, modes and preservation

Thirteen hostile boundary inputs are rejected, including false ratio, negative side, floating coordinates, reversed polygon, invalid disk centers, zero scale, missing side cell, duplicate placement, false center, incomplete pair table, bad axis, and an additional slightly translated interior copy. The last control preserves the original complete boundary intervals and all copied individual disk data but creates a positive-area overlap, which is rejected by the independent pair check. One benign cyclic rotation of canonical vertex lists passes.

The geometry, controls, topology, producer-pair check and symbolic algebra are replayed in normal, -O and -OO modes, with byte-identical output required. Complete frozen inputs and independent pair data are preserved in the compact audit package. The external preservation receipt records actual archive extraction and independent per-file byte-store reconstruction, file-by-file hash agreement, and fresh checker replays from both restored trees.

The global optimization problem remains unresolved. The separately accepted 121-cell full-square witness has upper bound 1.295864; the boundary-only number 1.28878 must never replace it in the whole-square bound.
