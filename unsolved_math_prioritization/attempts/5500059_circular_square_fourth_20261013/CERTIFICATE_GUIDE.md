# Exact checking guide for the fourth edition

This guide explains how to reconstruct every displayed mathematical witness using arbitrary-precision integers and rational arithmetic. The [full-square proof](FOURTH_PASS_CONSTRUCTIVE_UPPER_BOUND.md), [fixed-patch proof](FIXED_PATCH_INTERIOR_OBSTRUCTION.md), and [coarsened-patch proof](COARSENED_BOUNDARY_REPAIR.md) give the complete arguments and their scope.

## Full-square certificate

The [rational certificate](rational_partition_certificate.json) lists 240 integer vertex pairs, 121 counterclockwise face cycles, and 121 disk-witness records. Divide every vertex, incenter, enclosing center and radius numerator by D=10^12. Use the displayed independent disk centers without assuming either is extremal.

For every directed face edge V to W and every other face vertex Z, verify det(W-V,Z-V)>0. There are 2,884 such support tests, and their minimum is 160383401566530772. This tests all vertices against each edge, rather than only consecutive turns.

Each unordered pair has an entry in [the producer separators](pair_separation_witnesses.json) and [the independently reconstructed separators](INDEPENDENT_PAIR_SEPARATIONS.json). The producer table gives face indices and global edge-vertex labels. The independent table gives the supporting face and its local edge position. Verify the indicated edge belongs to its face and that every vertex of the other face is on the nonpositive side. There are exactly 7,260 unordered pairs, each occurring once. Separating half-planes prove disjoint interiors.

The doubled shoelace areas are positive and sum to 8000000000000000000000000 = 8 D^2. Containment inside [-D,D]^2, disjoint interiors, and equality of areas prove full closed coverage as detailed in the proof. Incidence is a redundant check: 336 internal edges have opposite orientations; 24 boundary edges tile all four sides; 240-360+121=1.

For edge vector E, incenter numerator A and radius numerator q, verify det(E,A-V)>0 and

(det(E,A-V))^2 - q^2 ||E||^2 > 0.

All 696 comparisons are strict. The smallest q is 29350614583, and the minimum squared slack is 11903868602776199771750141753138239.

For every vertex V and enclosing-center numerator B, verify

1295516^2 q^2 - 1000000^2 ||V-B||^2 > 0.

All 696 comparisons are strict. Their minimum is 823068242597106816174189584. A convex disk containing all vertices contains the polygon, so the true ratio is strictly below 1295516/1000000. Strictness follows from the finite positive margin; decimal optimizer scores do not certify it.

The [face-margin table](exact_face_margin_table.json) records exact results for every cell. Recompute the entire table and [summary](exact_verification_summary.json), rather than trusting aggregate minima alone. Reconstruct all eight listed [edge flips](topology_operations.json) from the [third-edition certificate](../5500059_circular_square_third_20261013/rational_partition_certificate.json) if checking provenance. The geometric theorem does not require this history.

## Original fixed-patch side budget

The original [56-cell certificate](../5500059_circular_square_third_20261013/boundary_patch_certificate.json) is a sibling dependency and is not the new coarsened certificate. Reconstruct the eight canonical polygons under the listed positive rational similarities, reflections and rotations.

Count 7,104 genuine sides, 56 shared fixed-fixed edges, 60 outer-square segments, and 6,932 exposed inner edges. The exposed edges form one simple cycle. There are 6,876 one-fixed-cell vertices with cell angle in (150,180) degrees and 56 two-fixed-cell endpoints with free sector in (90,135) degrees. The proof gives exact dot-product tests and checks which sector is free.

For any finite completion, subdivide sides at every partition vertex. Euler and edge-incidence counting yield

sum(6-s_i) = B-2+2X+C.

B=60, X is the nonnegative sum of interior vertex degrees minus three, and C counts additional side incidences at collinear subdivision points. A cell of ratio below sqrt(2) has at least five genuine sides, by the complete independent-center perimeter argument in the proof. Substitution gives at least 6,826 added pentagons. At ratio at most 13/10, all angles exceed 72 degrees, X=V4 and C=T, producing the displayed refined identity.

## Coarsened boundary witness

The [new exact certificate](coarsened_boundary_certificate.json) specifies 56 convex polygons with 588 genuine sides. Its canonical vertex counts are 6,13,15,13,11,8,7,7. Reconstruct all rational similarities, verify strict convexity, unit-disk inclusion in canonical coordinates, and strict enclosure at radius 64439/50000. Verify all 1,540 unordered cell pairs have supporting-line separators, all four sides have gap-free consecutive boundary intervals, and all 56 shared segments match in both orientations.

There are 416 exposed inner edges, 360 one-cell inner vertices and 56 two-cell endpoints. For the one-cell angle test, with D=u dot v and A=|u|^2|v|^2, verify D<0 and 10000 D^2>6561 A. This gives angle greater than 144 degrees. The free sectors force the same trivalent local incidence at ceiling at most 13/10. The necessary pentagon count becomes 588-6*56+60-2=310.

Check that the square center is strictly outside every cell and that the exact covered area is less than the square area. These checks prevent this boundary-only example being mistaken for a whole-square partition. The passive illustration rounds coordinates only for display. Its uncovered-center label is part of its stated scope.

## Audit and interpretation

Complete rational witnesses and the written arguments carry the claims. Programs, raw solver streams and discovery records are not premises of the public mathematical proofs. Normal, -O and -OO computational replays and hostile/benign controls are regression evidence in the accompanying audits. Exact dependencies are identified in the [public manifest](PUBLIC_MANIFEST.json); prior-edition claims remain unchanged.

The current complete-square upper bound is 1.295516. The boundary-only ceiling 1.28878 proves no interior completion. Neither 6,882 nor 366 is claimed sufficient, and the unrestricted optimum and attainment remain open.
