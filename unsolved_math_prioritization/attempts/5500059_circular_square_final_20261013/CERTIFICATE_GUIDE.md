# Exact certificate guide for the final partial collar

## Coordinates and fixed dependency

The exact [coarsened boundary certificate](../5500059_circular_square_fourth_20261013/coarsened_boundary_certificate.json) is the unchanged 77,009-byte fourth-edition object with SHA-256 6e7136b295451a6bd8c49c04440f319dce534c94f91484eac21530e53492393e. Its [construction proof](../5500059_circular_square_fourth_20261013/COARSENED_BOUNDARY_REPAIR.md), [independent review](../5500059_circular_square_fourth_20261013/INDEPENDENT_BOUNDARY_REVIEW.md), and [exact audit](../5500059_circular_square_fourth_20261013/INDEPENDENT_BOUNDARY_CHECK.json) establish the fixed 56-cell family.

[PARTIAL_COLLAR_CERTIFICATE.json](PARTIAL_COLLAR_CERTIFICATE.json) is the exact 18,958-byte rational extension with SHA-256 d028fc1ab1cbeff1f439db04a9e1b9858f960c06a57b1cb6c0f66f7af0bbffea. It defines ten canonical hexagons, their centers and squared radii, 80 placements, and nine shared canonical new tips. Its historical candidate label is preserved byte-for-byte; acceptance is supplied by the accompanying exact producer checks and fresh independent audit.

For a boundary placement with scale q, offset a, reflection flag, rotation count k, and square side S, transform a canonical point (x,y) first to (a+qx,qy), then to (S-x,y) if reflected, and apply (x,y)->(S-y,x) exactly k times. Reverse the vertex order after reflection so each polygon is counterclockwise. Witness centers use the same transformation; squared radii multiply by q^2. Boundary canonical indisk radius is 1; added-cell squared radii are explicit positive rationals. These witnesses need not be extremal and their centers need not coincide.

Cell numbering is exact: indices 0 through 55 follow the boundary certificate's cells array; indices 56 through 135 follow the collar placements array. Every extension placement references its parent boundary placement and canonical cap type.

## Polygon and disk inequalities

For each directed edge a->b let e=b-a. For each other vertex p, require det(e,p-a)>0. This establishes genuine sides and strict convexity. For witness incenter I and positive squared radius r2, require

    h = det(e,I-a) > 0,
    h^2 - r2*(e dot e) >= 0.

For witness enclosing center O and every polygon vertex p, require

    (64439/50000)^2*r2 - |p-O|^2 > 0.

Convexity puts the whole polygon inside the enclosing disk. Thus the true R/r is strictly below 1.28878. [EXACT_CELL_MARGIN_TABLE.json](EXACT_CELL_MARGIN_TABLE.json) records the actual rational minimum support determinant, minimum indisk squared slack, minimum strict enclosing squared slack, positive squared witness radius, area, and genuine side count for each of all 136 placed cells. An indisk slack may be zero; the enclosing slack must be strictly positive.

## All pairs and full residual boundary

[PARTIAL_COLLAR_PAIR_WITNESSES.json](PARTIAL_COLLAR_PAIR_WITNESSES.json) has all 9,180 unordered pairs. Each row [j,i,owner,k,order] uses j<i; owner=0 means cell j supplies directed edge k and owner=1 means cell i. With that edge e=(ex,ey), use normal n=(ey,-ex). Order 1 asserts max(n dot Pj)<=min(n dot Pi); order -1 reverses the inequality. Every comparison is exact rational arithmetic. Non-strict projection separation permits shared boundary but excludes overlapping interiors.

[INDEPENDENT_PAIR_CLASSIFICATIONS.json](INDEPENDENT_PAIR_CLASSIFICATIONS.json) independently classifies every pair as empty, a point, or an entire shared edge, with its exact axis and rational intersection coordinates when applicable. Its axes x and y are coordinate axes; an axis owner:k is the perpendicular to edge k of the indicated member of that pair. This audit also independently replays every producer pair witness, rather than trusting only its own all-pair reconstruction.

The enlarged family has 1,068 genuine sides, 208 entire shared edges, 60 square-boundary edges, and one 592-edge residual inner cycle. Each outer side is tiled by 15 consecutive exact intervals. The square center is strictly outside every cell, hence an open neighborhood is missing. [PARTIAL_COLLAR_CHECK.json](PARTIAL_COLLAR_CHECK.json) and [INDEPENDENT_GEOMETRY_CHECK.json](INDEPENDENT_GEOMETRY_CHECK.json) give exact covered-area fractions; the decimal percentage is descriptive only.

## Free-sector and local-dead-end checks

A cell with circularity <=gamma must have each angle at least 2 arcsin(1/(2gamma-1)). At gamma=64439/50000, put c0=1-2/(2gamma-1)^2>0. For the two exact rays u,v of an identified smaller exterior sector, let D=u dot v and A=|u|^2|v|^2. An adequate angle follows from D<=0 or D^2<c0^2*A.

[INDEPENDENT_TIP_CHECKS.json](INDEPENDENT_TIP_CHECKS.json) stores the exact canonical tip and end tests and all 144 two-cell vertices of the residual cycle. Eight canonical shared-tip angles are near 79 degrees and one is near 96.533711 degrees. Exact rationalization does not assert that each is at least exactly 79 degrees. The successful necessary angle tests do not establish extendibility.

[LOCAL_DEAD_END_CERTIFICATE.json](LOCAL_DEAD_END_CERTIFICATE.json) describes a different three-cell patch. Its [producer check](LOCAL_DEAD_END_CHECK.json) and independent geometric audit prove that its identified exterior sector has cos(phi)>7/32, smaller than the necessary angle for ceiling 13/10. No finite completion retaining those three specified cells can fill that neighborhood. This is a local obstruction with an explicit retained-cell hypothesis.

## Sharp pentagon and arithmetic checks

The complete [pentagon proof](ADJACENT_RIGHT_PENTAGON_OBSTRUCTION.md) treats arbitrary asymmetric convex pentagons with independent disk centers. At its unique m in (0,1),

    (1+m)^2*(1-m^2)=4m^2,
    rho=(1+m)/(2m)=1.290772978969... .

The [producer exact check](EXACT_PENTAGON_OBSTRUCTION_CHECK.json) and [independent exact check](INDEPENDENT_PENTAGON_CHECK.json) verify the rational lower comparisons, equality polynomial, a strict rational root bracket, support perturbation margins, and endpoint inequalities for the two restricted equal-bisector facets. They supplement the written proof; arithmetic tests alone do not prove the geometric reductions.

## Scope and replay

The standard-library producer and independently authored exact checks pass in normal, -O, and -OO interpreter modes. Their published mode records bind the mathematical result bytes; any edition reference normalization is explicitly described in the independent replay metadata. Failed conditions use explicit exceptions, so optimization cannot remove acceptance checks. [Producer modes](MODE_REPLAY_CHECK.json) and [independent modes](INDEPENDENT_MODE_REPLAY.json) record the complete matrix.

The Euler deficit remains 310. Every completion retaining these 136 cells needs at least 310 additional pentagons and 446 cells in total below sqrt(2). This is not a sufficient completion theorem. The full-square bound stays 1.295516; neither a near-critical full partition nor an unrestricted nonexistence proof is supplied.
