# Checking the finite two-cell local certificate

The [complete local certificate](local_patch_certificate.json) specifies two convex polygons with 208 and 162 vertices. This is a local configuration near one boundary segment. It neither covers a square nor supplies a full-square upper bound. Its ratio bound is 64439/50000=1.28878.

Every coordinate and structural parameter is a rational number stored as an integer string or a numerator/denominator string. Parse these exactly. For each cell read its ordered vertices, indisk center I, positive radius r, enclosing center C, and upper tangent normal. Read the common endpoints p and q, and the positive parameter t. The file also preserves the rational half-plane description and exact squared-ratio calculations used to produce the polygon; the listed polygon vertices are sufficient for the independent geometry checks below. Approximate ratios are diagnostic only.

## Geometry and circles

Require distinct vertices, a positive shoelace area, nonzero edges, and every vertex in the closed left half-plane of every oriented edge. This establishes the polygon's global convexity. For each edge a to b require

cross(b-a,I-a)>0,

cross(b-a,I-a)^2 >= r^2 |b-a|^2.

Thus the stated disk is contained in the polygon. Require every vertex v to satisfy

|v-C|^2 <= (64439/50000)^2 r^2.

By convexity the enclosing disk contains the polygon. These bounds establish the true circularity at most 1.28878 without presuming that the chosen circumcenter is optimal.

The strip unit normal is

n=(2t/(1+t^2), -(1-t^2)/(1+t^2)).

Check |n|^2=1. The maximum minus minimum of n dot v over the cell's vertices must equal 2r exactly. A disk contained in a width-2r strip has radius at most r, so the contained disk is maximal. Both polygons lie above the baseline.

## Shared edge and obtuse upper opening

The distinct points p and q must both occur as vertices of each cell, consecutively. Every vertex of one cell lies on one closed side of the line pq, and every vertex of the other lies on the opposite closed side. Hence interiors are disjoint, and the common segment is the exact shared edge.

At q, identify each cell's actual adjacent edge other than qp. Let u be its ray vector and n_upper its listed upper tangent normal. Check

|n_upper|^2=1,
n_upper dot (q-I)=r,
n_upper dot u=0.

Thus this actual edge is tangent to the indisk. For the two outgoing rays u1,u2, require u1 dot u2<0. Their opening is strictly larger than 90 degrees. These are exact rational comparisons.

Compare the counts, exact least enclosing slacks, common-edge verdict and strip-width verdict with [the independent local audit](EXACT_LOCAL_PATCH_AUDIT.json). Four altered-certificate controls were rejected: changing q, enlarging an indisk, reversing a polygon cycle, and replacing the upper tangent normal. The complete proof of the parametric relaxed construction, polygon approximation and universal opening estimate is in [the theory report](THEORY_REPORT.md), with [independent review](INDEPENDENT_THEORY_REVIEW.md).

## Scalar and symbolic checks

[Exact scalar controls](EXACT_THEORY_CONTROLS.json) isolate t0 and G by rational signs and verify the source-formula counterexample. [The symbolic audit](SYMBOLIC_THEORY_AUDIT.json) records universal rational identities for circle incidence, disk tangency, contact-weight normalization and center reconstruction, disk separation and the opening-polynomial factorization. The active-constraint positivity range is retained explicitly. Neither finite rational sampling nor symbolic identity simplification replaces the geometric inequalities, compactness proof or finite boundary-chain argument.
