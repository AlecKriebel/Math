# Final interior-completion pass: exact partial collar and restricted obstructions

Problem: row 1757 / 5500059 / AMR0540059. Fifth and final newly documented mathematical pass of this continuation, 2026-10-13. The previous lifetime count is unknown; this does not assert a lifetime total of five. No novelty or unrestricted optimum claim.

## Result

A complete finite interior at the near-critical ceiling remains unresolved. This pass supplies three narrower, rigorously testable results:

1. An exact partial extension of the pinned coarsened boundary family, retaining all 56 polygons and adding 80 convex hexagons. Every one of the resulting 136 cells has actual circumradius/inradius ratio strictly below 64439/50000 = 1.28878. Their interiors are disjoint, the square boundary remains covered, and the square center remains uncovered.
2. A sharp lower bound 1.290772978969... for arbitrary convex pentagons with two adjacent right angles, with independent incenter and circumcenter. An exact near-90.30-degree corollary rules out pentagonal caps on two specified facets of the boundary family when the separating seams bisect the unfilled sectors. This is a restricted collar obstruction, not a general completion obstruction.
3. An exact three-cell example, taken from an earlier candidate for the same strip, in which every cell is individually round enough and the interiors are disjoint, but the new uncovered angle makes any completion with ratio at most 13/10 impossible. This demonstrates a concrete failure that the accepted partial collar avoids.

None of these results improves a whole-square upper bound. The separately certified 121-cell bound below 1.295516 is unchanged. The reported lower constant G = 1.2886844618704579... remains the prior context, not a newly proved unrestricted optimum.

## 1. Frozen dependency

The complete coarsened boundary certificate is the exact [fourth-edition sibling dependency](../5500059_circular_square_fourth_20261013/coarsened_boundary_certificate.json):

    coarsened_boundary_certificate.json
    77,009 bytes
    SHA-256 6e7136b295451a6bd8c49c04440f319dce534c94f91484eac21530e53492393e

Its [independent fourth-pass boundary review](../5500059_circular_square_fourth_20261013/INDEPENDENT_BOUNDARY_REVIEW.md) and [exact checks](../5500059_circular_square_fourth_20261013/INDEPENDENT_BOUNDARY_CHECK.json) are included as exact sibling dependency evidence. They establish the 56-cell family, all square-boundary coverage and shared-edge claims, the uncovered center, and the Euler obstruction. The fifth-pass checker additionally reconstructs all original shapes and independently retests their strict convexity and disk witnesses, as well as every pair in the enlarged family.

The new partial-collar certificate is:

    PARTIAL_COLLAR_CERTIFICATE.json
    18,958 bytes
    SHA-256 d028fc1ab1cbeff1f439db04a9e1b9858f960c06a57b1cb6c0f66f7af0bbffea

Its scope string correctly labels it as a candidate accepted only after the accompanying exact checks; the certificate bytes are frozen. The exact acceptance output is [PARTIAL_COLLAR_CHECK.json](PARTIAL_COLLAR_CHECK.json).

## 2. Exact construction and what is checked

There are ten canonical hexagons along the exposed arc of the boundary type left_1, on its consecutive zero-based edges 1->2 through 10->11. They occur at each of the eight placements of that boundary type, for 80 added cells. The certificate lists every canonical rational vertex, a rational witness incenter, a positive rational squared inradius, and a rational witness circumcenter. The radius itself need not be rational. All similarities and reflections are the exact rational transformations already specified by the boundary certificate.

Adjacent added hexagons share the complete segment from the corresponding original boundary vertex to one common rational new tip. These tips were optimized jointly, rather than independently assigning different seam lengths to neighboring cells. The seam directions are allowed to tilt away from the exterior angle bisectors.

For every directed edge e from a vertex a and witness center I, the checker proves

    det(e,I-a)>0,
    det(e,I-a)^2 >= r^2 |e|^2.

These rational inequalities place the complete witness disk inside the polygon. Every vertex p satisfies

    |p-O|^2 < (64439/50000)^2 r^2.

Strict convexity is checked by positive turns and every global supporting inequality. Because the enclosing disk is convex, it contains the whole polygon. The true inradius is at least the displayed radius, and the true circumradius is at most the displayed strict upper bound; the centers need not coincide or be extremal.

All 9,180 unordered pairs among the 136 cells have exact separating-axis witnesses. Floating arithmetic is used only to select a candidate axis; all accepted separation comparisons are rational, and every pair must pass. The stored witnesses identify a cell edge giving the axis and its order, and are independently replayed against the reconstructed exact coordinates. All vertices lie inside the exact square.

The enlarged family has:

- 136 cells and 1,068 genuine sides;
- 208 complete shared edges: 56 old shared edges, 80 old/new edges, and 72 new/new edges;
- the same 60 outer-square edges;
- one simple residual inner cycle with 592 edges.

The checker confirms the full cycle and all shared orientations. Global pair separation makes the inner cycle geometrically simple. The covered area fraction increases from approximately 0.3199339167052989 to 0.3224892181598094; exact rational fractions are in the acceptance output. The square center lies strictly outside every cell, so an open neighborhood remains uncovered.

## 3. Free-angle checks, and their limits

If a convex cell contains a disk of radius r and has an interior angle alpha at a vertex, the vertex is at distance at least r csc(alpha/2) from the disk center. Any disk containing that indisk and that vertex has radius at least

    r(1+csc(alpha/2))/2.

Thus circularity at most gamma forces

    alpha >= a_gamma := 2 arcsin(1/(2gamma-1)).

This statement allows independent disk centers. At gamma=1.28878, a_gamma is about 78.675459 degrees.

At each of the nine canonical shared new tips, the checker identifies the smaller free sector using exact supporting-line signs, then proves that its angle is greater than a_gamma. Its approximate values are eight sectors near 79 degrees and one near 96.533711 degrees. The two end sectors, where a collar terminates at its parent polygon, are approximately 89.240130 and 110.525061 degrees and pass the same exact test. Rationalization causes harmless tiny deviations from 79 degrees; no claim that every rationalized sector is at least exactly 79 degrees is made.

To avoid transcendental rounding, set c_gamma=1-2/(2gamma-1)^2>0. For the two free-sector rays u,v, put D=u dot v and A=|u|^2|v|^2. When D<=0 the angle exceeds the required acute threshold. Otherwise the checker proves

    D^2 < c_gamma^2 A.

These angle checks only rule out an immediate angle contradiction. They do not prove that a polygon of the required shape fits each remaining wedge, that the wedges can be connected consistently, or that the entire residual domain admits a finite completion.

## 4. A precisely rejected collar candidate

An earlier fixed-bisector ten-hexagon optimization produced individually excellent ratios near 1.2871353, but several of its new free sectors were too acute. The exact local certificate [LOCAL_DEAD_END_CERTIFICATE.json](LOCAL_DEAD_END_CERTIFICATE.json) retains the original canonical left_1 cell and two rationalized hexagons from that candidate. All three cells have strict ratio below 1.28878 and pairwise disjoint interiors. The two hexagons share a complete edge.

At their new shared tip, the exact check identifies the remaining smaller free sector and proves

    cos(phi)>7/32.

But at a ceiling of 13/10, every positive-area convex added cell must have an angle at least

    a_(13/10)=2 arcsin(5/8),
    cos(a_(13/10))=7/32.

Hence phi<a_(13/10). No added cell can occupy this sector at the tip, and splitting it into several cells only makes their individual angles smaller. Any finite full neighborhood partition retaining these three cells is therefore impossible at that ceiling. This is an exact local rejection of this specified candidate, not a rejection of the accepted boundary patch or variable-seam collar.

This also explains the danger of appending independently scaled caps. A T-junction can leave a flat 180-degree angle from one existing cell and a large corner from another, producing an unfillable narrow remainder. Disk witnesses and nonoverlap alone are insufficient for an extendibility assertion.

## 5. Pentagon-only obstruction

The separate [public proof](ADJACENT_RIGHT_PENTAGON_OBSTRUCTION.md) proves a sharp global lower bound for arbitrary convex pentagons with two adjacent right angles. After moving the supporting lines inward to a unit indisk, it reduces the entire asymmetric family to independent diagonal and apex-triangle lower bounds. Their exact crossover is

    (1+m)^2(1-m^2)=4m^2,  0<m<1,
    rho=(1+m)/(2m)=1.290772978969... .

The proof includes an attaining tangential cyclic pentagon and a rational lower comparison rho>129077/100000. A support-perturbation estimate gives a rigorous forbidden interval around right angles.

A separate rational-angle argument covers a narrow interval around 90.30 degrees. The exact rational vertices of the pinned boundary certificate place the equal-sector half-angles at left_1 vertices 5,6,7 in that interval. Therefore whole-facet pentagonal caps on edges 5->6 and 6->7 are impossible if the new seams are the exact exterior-sector bisectors. All eight similar occurrences inherit the same restriction.

This result does not exclude variable seams, subdividing those facets, or hexagons. The accepted partial collar deliberately uses hexagons and variable seams. It does not prove a global lower bound above G.

## 6. Remaining finite-completion burden

The 80 added hexagons contribute zero to the genuine-side deficit. With N0=136 fixed cells, S0=1068 genuine sides, and B=60 outer edges, the [previously proved Euler identity](../5500059_circular_square_fourth_20261013/FIXED_PATCH_INTERIOR_OBSTRUCTION.md) gives

    sum_added(6-s_i)=S0-6N0+B-2+2X+C
                   =310+2X+C.

Every added polygon below sqrt(2) has at least five genuine sides. Thus retaining all 136 cells still requires at least 310 further pentagons and at least 446 cells in total. At a ceiling at most 13/10,

    P5=310+sum_(k>=7)(k-6)Pk+T+2V4.

The prior meanings of T and V4 remain valid; all original and new fixed interfaces are entire shared edges, and extra subdivisions can only add nonnegative terms. Hexagons do not discharge the pentagon budget. This is necessary, not sufficient, and 446 is not claimed attainable.

The remaining problem is an exact finite partition of the 592-edge residual domain with positive-radius convex cells, valid disk witnesses, compatible interfaces, complete coverage, and the required pentagon budget. A recursive collar argument would additionally need a proved finite stopping rule and a terminal core with the same ceiling. A shrinking uncovered core, an infinite limit, a numerical mesh, or the current 121-cell construction at the larger ceiling cannot supply that missing finite certificate.

No sixth mathematical pass is started. The completed scope is the exact partial collar, the specified local dead end, the restricted pentagon obstruction, and a precise statement of the still-open interior.
