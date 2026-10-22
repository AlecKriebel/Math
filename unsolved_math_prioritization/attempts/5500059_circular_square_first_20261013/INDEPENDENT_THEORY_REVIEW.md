# Independent review of the finite lower bound and local junction

## Accepted scope and exact inputs

The reviewed theory report, *Square circularity: rigorous boundary reduction and a non-tangent local junction*, has SHA-256 308ce4c4351b36f34495580e677c1548c6099df0cc162434243d690f288a9760. This acceptance binds those exact report bytes. The companion local rational certificate has SHA-256 6bc1bf6521fc94a1dbe7f02a199e2c13926aa687072e4c2328510bd4f800a0e1 and 282156 bytes.

Accepted conclusions:

1. Every finite positive-area convex polygonal partition of the square has worst ratio strictly greater than G=1.2886844618704579013258751580333007025952... . Therefore the finite-partition infimum is at least G. This reconstructs the known reported bound about 1.28868; it is not represented as a newly stronger global lower bound.
2. For any fixed positive integer N, the minimum among partitions into at most N such cells exists and is strictly greater than G. This does not prove a lower gap uniform in N, or prove that the finite-partition infimum equals G.
3. The report's explicit non-tangent two-disk junction has opening at least 4 atan(1/2)>90 degrees. Its finite polygon approximations and exact local certificate are valid local constructions, with no whole-square completion claim.

The exact optimum, finite attainment at that optimum, and equivalence with arbitrary infinite partitions are not settled. The restricted tangent-indisk conjecture in arXiv cs/0304023v2 is not disproved by an example outside its restriction. Source: https://arxiv.org/abs/cs/0304023v2.

## Adversarial review of the finite boundary argument

### Corner uniqueness and nonconforming boundaries

For a competitive partition of ratio at most 1.3, the elementary angle bound forces each genuine cell angle to exceed 75 degrees. In a finite polygonal partition a sufficiently small neighborhood of a boundary vertex is divided into the finitely many incident polygonal sectors. At a square corner their angles sum to 90 degrees, so exactly one positive-area cell occurs. At an interior point of a square side the angles sum to 180 degrees, so a genuine subdivision has exactly two incident cells. Three or more would require more than 225 degrees. This specifically excludes boundary T-junctions involving a third positive-angle cell. Artificial collinear vertices can be removed; subdividing one straight edge into several listed segments does not create a new cell or evade the argument.

A cell's intersection with one side is an interval by convexity. Thus the finite ordering of side cells used by the proof exists, even without assuming that every shared edge in the original representation is face-to-face. The argument does not extend this local finite-sector reasoning to infinitely accumulating cells.

### Corner support reduction

After scaling the corner cell's actual indisk to radius one, its center satisfies x,y>=1. The endpoint inequalities in the report follow from the signed distances to the two non-axis support lines. They do not assume contact with those lines or with the axes.

The positive-weight chord argument is essential: the affine lower bounds for individual endpoints could be negative far from the corner, so blindly squaring them would be invalid. The report instead uses b0 B+c0 C, whose coefficients of x and y are positive throughout the required angle range. Cauchy-Schwarz then gives the claimed chord bound. This repair is valid for arbitrary incenter location.

The same bound rules out an exit of at least 90 degrees. The special case of a cell spanning two adjacent square corners is handled with the second corner's vertical side as an artificial right-angle support. If no other exit existed, that cell would contain at least three corners, already excluded by the diagonal diameter and inradius bounds. Opposite-corner and three-corner cells have ratio at least sqrt(2). Consequently the four corner cells are distinct, and the proof's terminal side angle really is above 90 degrees.

### Crossing and strip containment

Assuming all ratios at most G, one of a corner's exits is at most theta0. Following its side reaches an exit above 90 degrees at the opposite corner. A finite ordered sequence therefore has consecutive angles alpha<=theta0<=delta. No monotonicity of the whole angle sequence is assumed. The selected crossing cell has precisely the two support inequalities used in the proof.

For an indisk centered at the origin and baseline y=-h, h>=1, the endpoint monotonicities have derivatives -(cos(theta)+h)/sin(theta)^2 and (h-cos(theta))/sin(theta)^2, respectively. They have the required signs throughout (0,pi). The actual bottom segment therefore contains the two canonical feet for theta0. This is a containment relaxation, not an assumption that a maximal indisk touches all three supports.

The minimum enclosing radius of a unit disk and these feet is convex in h by partial minimization of a jointly convex epigraph over the free circumcenter. Central inversion shows it is even. At h=1 the relevant three-contact branch gives G; at h=0 the radius is at most csc(theta0)<G. The convex secant inequality forces f(h)>G for h>1. This avoids any differentiation of an optimizer or unproved concentricity assumption.

At h=1 a circle of radius G covering the canonical data is the unique minimum circle and is internally tangent to the unit disk. A polygon cannot simultaneously contain that disk and stay within the outer circle: at the shared point every polygonal supporting edge would have to lie on the common tangent, which leaves the outer circle immediately away from the point. This establishes strictness for each finite polygonal partition. Strictness of each attained value is correctly distinguished from strictness of the infimum.

### Active branch and exact root

For the disk-plus-feet problem the one-endpoint branch changes to the two-endpoint branch at tan(theta/2)^2=(sqrt(5)-1)/2. The balancing parameter t0 is greater than 0.82 and so lies strictly in the latter branch. The circle through both feet and tangent to the disk has positive contact-balancing weights there. Each of the report's three explicit weights was independently checked symbolically: they sum identically to one and their weighted contact coordinates reconstruct the stated center in both coordinates. The contact point lies identically on both circles. Positivity follows from the displayed factors in the stated two-foot interval; it is not asserted for arbitrary t. The incorrect unrestricted use of the second branch in source Lemma 16 is therefore not inherited.

An independent rational calculation verifies the balance polynomial

t^8 - 2t^6 - 16t^5 + 3t^4 + 6t^2 + 1.

The original two positive expressions have opposite monotonicity on 0<t<1, so the isolated root is unique there and squaring adds no ambiguity in the stated interval. The independently verified brackets are

0.8224750435966752433966468926325324607092 < t0 < 0.8224750435966752433966468926325324607093,

1.2886844618704579013258751580333007025952 < G < 1.2886844618704579013258751580333007025954.

These are rigorous rational sign brackets, not confidence intervals or floating-point tolerances.

## Fixed-N compactness

The report's fixed-N conclusion is valid. Label at most N cells and take a Hausdorff-convergent subsequence in the compact square. A bounded ratio forces a cell whose inradius vanishes to have vanishing circumradius and hence diameter, so discarded degenerate limits are points. The remaining finite union of positive-area compact convex limit cells is closed. A missing relatively open subset of the square has positive area and cannot be covered by finitely many discarded points; therefore the nondegenerate cells still cover the square.

Their interiors remain disjoint under convex Hausdorff convergence. Inradius and circumradius are continuous on the nondegenerate compact convex cells. To see polygonality explicitly, choose a weak separating line for each pair of cells, and intersect the half-planes containing one chosen cell with the square. Any point in the interior of this finite half-plane intersection cannot belong to another cell. Coverage puts it in the chosen cell; taking closures gives equality. Each limit cell is thus a polygon. The minimum is attained with at most N cells and, by the strict finite theorem, is greater than G.

## Local non-tangent junction

The symbolic circle-incidence, disk-containment, and separation identities were independently recomputed. In particular the squared center-distance excess over the squared sum of indisk radii is

t^2(t-1)^2(t+1)^2/(t^2+2)^2,

which is nonnegative and is positive for t!=1. The shared support line places the disks on opposite sides. The reported q lies on both enclosing circles above both disk tangency points on that line. Taking the convex hulls with the baseline endpoints consequently gives two valid convex relaxed cells sharing exactly their common segment.

The gap-to-radius quantities x,y are positive and satisfy xy<=1/4. Hence atan(x)+atan(y)<pi/2 and the tangent-addition step uses the correct branch. Its comparison with 2 atan(1/2) reduces to the exactly verified identity

3(t^4+1)(1+t^2)-4t(1+t^2+t^4) = (t-1)^2(3t^4+2t^3+4t^2+2t+3)>=0.

Retaining the baseline, both parallel strip supports, and the upper tangent through q in finite outer polygonal approximations preserves the common edge, the opening, and the exact inradii. Uniformly close support-line approximation bounds the enclosing radii by arbitrarily small enlargements. The report does not improperly identify these local cells with a complete square partition.

## Independent exact finite local certificate

A separate rational checker accepted the frozen local certificate with 208 and 162 vertices. It verifies global support-side convexity, positive areas, containment of each stated indisk against every polygon edge, every vertex inside the ratio-64439/50000 enclosing disk, and the exact common edge [p,q]. The two cells lie in opposite closed half-planes of that separator, so their interiors do not overlap. Parallel-strip width is exactly twice the stated indisk radius, independently proving that radius maximal.

The listed upper tangent is a unit normal, is tangent to the indisk, and is the actual nonshared edge at q. The two actual edge rays have strictly negative dot product, proving the opening exceeds 90 degrees for these finite polygons. Four corruptions were rejected: altered common top point, oversized disk, reversed orientation, and changed upper tangent. The numerical bound 1.28878 here belongs only to this two-cell local patch.

The exact scalar controls also verify the source-Lemma-16 counterexample distances 1/4, 9/4, and 19/12; the earlier erroneous squared distance 5/3 was removed before acceptance. Sampled rational identities are labeled as controls, not substitutes for the universal geometric reasoning above.
