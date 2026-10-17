# Independent acceptance of the finite complexity lower gap

Problem: row 1757 / 5500059 / AMR0540059. Review date: 2026-10-13.

## Verdict and exact scope

Accepted. For every positive integer N, every partition of a square into at most N positive-area compact convex cells has maximum circumradius-to-inradius ratio gamma satisfying

    gamma > G + 1/(192 * 25^(N+2)),

where G is the previously accepted balancing constant, approximately 1.288684461870457901325875. This explicitly quantifies a finite-complexity gap. The correction tends to zero with N and therefore does not improve the unrestricted finite-partition infimum lower bound G. It does not construct partitions approaching G, settle the unrestricted optimum or its attainment, or justify an infinite-partition equivalence. No literature priority claim is accepted or made.

The [complete proof](QUANTITATIVE_COMPLETION_OBSTRUCTION.md) has public-edition SHA-256 `eaef444e9a2b79020be9af28e86ac88e8ca1e58e311d48774cbc7776f319825a`. Only its dependency paths have been converted to public links; its mathematical text is unchanged from the independently reviewed proof. The accepted first-pass [theory proof](../5500059_circular_square_first_20261013/THEORY_REPORT.md) has SHA-256 `308ce4c4351b36f34495580e677c1548c6099df0cc162434243d690f288a9760`, and its full [independent acceptance](../5500059_circular_square_first_20261013/INDEPENDENT_THEORY_REVIEW.md) is also supplied in that sibling edition. The review re-read the relevant first-pass boundary and constant arguments rather than assuming the new formula from its headline.

## Finite convex cells and the side bound

The extension from polygonal to arbitrary positive-area compact convex cells in a finite partition is valid. For a fixed cell C, weakly separate it from each other full-dimensional convex cell and let Q be the intersection of C's containing half-planes and the four square half-planes. Then C is contained in Q. If Q strictly contained more than C, choose a point in Q outside closed C and interpolate slightly toward an interior point of C. This gives an interior point of Q still outside C and hence a small open disk of such points. Each other cell's interior is excluded by its separating half-plane. A finite union of boundaries of full-dimensional convex bodies cannot cover the disk, contradicting coverage.

Equivalently, the interior of the full-dimensional Q is strictly on the C side of every nonzero separating line, so it is disjoint from every other closed cell. This yields the same contradiction directly. Consequently C=Q is a polygon with at most N-1+4=N+3 sides after redundant collinear vertices are removed. This reasoning does not assume face-to-face incidence or polygonality in advance. Applying it before the boundary argument removes any apparent dependency-order issue in the report.

## Eccentric annulus lemma

Let a unit disk be inside an m-sided polygon, itself inside a disk of radius R<=13/10 with center separation d. The initial implications 0<=d<=R-1<=3/10 and delta=R-d-1>=0 hold simply by disk inclusion. Moving all supporting lines inward to tangent lines leaves a bounded polygon Q inside the original one and with k<=m sides. The boundedness follows from unchanged recession directions, and the unit disk remains included. Consecutive outward normals therefore have angular gaps strictly below pi.

For consecutive normal angles theta-h and theta+h, the vertex is sec(h)(cos(theta),sin(theta)), with 0<h<pi/2. Expanding its squared distance from (-d,0) and subtracting (d+1)^2 yields

    (sec(h)-1)(sec(h)+1+2d cos(theta))
      + 2d(cos(theta)-1) <= 2R delta-delta^2.

The report's lower estimate is sound. The first factor sec(h)-1 is at least h^2/2, for example by integrating sec(x)tan(x)>=x. The second factor is at least 2(1-d)>0. The cosine term is at least -d theta^2 for every real representative theta. Therefore

    h^2 <= (3/7)theta^2+(26/7)delta
         <= (4/9)theta^2+4delta.

This is a global trigonometric inequality; it is not a small-angle approximation or an unproved asymptotic expansion.

The gap bracketing zero has |theta|<=h. Its inequality forces delta>0 and h<3 sqrt(delta), so both bracketing normals have absolute angle below 6 sqrt(delta). This also treats zero as an endpoint of a normal gap. Boundedness ensures at least one normal outside the open right semicircle. Choose its positive or negative direction and walk from the corresponding bracketing normal to the first angle of absolute value at least pi/2. A target already reached by the initial normal requires zero steps. Otherwise the consecutive representatives along the chosen walk remain nonnegative after reflection; the walk can stop before a wrap through 2pi and uses at most k-1 steps.

For consecutive angles a<=b on that walk, substituting theta=(a+b)/2 and h=(b-a)/2 and using sqrt(x+y)<=sqrt(x)+sqrt(y) gives

    b <= 5a+12 sqrt(delta),
    b+3 sqrt(delta) <= 5(a+3 sqrt(delta)).

The initial bound is strict, so iteration gives b<9*5^(k-1)*sqrt(delta). Since b>=pi/2>3/2, it follows that delta>1/(36*25^(k-1)), and hence delta>1/(36*25^(m-1)). The exponent, number of walk steps, endpoint convention, strict inequalities and possible opposite normal are all accounted for. No near-concentric or common-center assumption enters this proof.

## Boundary crossing dependence

After the side-bound reduction, all cells are finite polygons. The accepted first-pass one-angle bound forces every genuine angle above 75 degrees when gamma<=1.3. Thus a square corner has exactly one incident positive-area cell and a side subdivision exactly two. The corner support argument excludes a cell containing two square corners and forces both neighboring exit angles below 90 degrees. Those arguments allow nonconforming representations and discard artificial collinear vertices.

For the present gamma, t=sqrt(2)*gamma-1 and theta=2 atan(t). Since gamma>G by the prior theorem, t>t0>0.82, while gamma<=1.3 gives t<1. The corner chord estimate ensures that a corner has an exit at most theta. The far corner gives a terminal separator above 90 degrees, and hence above theta. Finiteness gives one consecutive crossing alpha<=theta<=beta; there is no assumption that all separator angles are monotone.

The supporting-distance inequalities for this crossing cell, normalized by its true inradius, give baseline height h>=1 and containment of the two canonical feet (-a-hc,-h) and (a-hc,-h), with a=csc(theta), c=cot(theta). The relevant endpoint derivatives have their asserted signs for h>=1. This is a containment relaxation, not a tangency assumption about any indisk.

## Envelope sensitivity and the weights

For fixed z>=1, the function f(h,z) in the proof is convex in h by joint convexity of the epigraph and partial minimization over the outer center. It is even in h by central inversion and exchange of the feet. Thus f(h,z)>=f(1,z) for h>=1. Finite-dimensional coercivity guarantees the stated minimum exists; no unsupported differentiation of an optimizing center is needed.

At h=z=1 the candidate center is o=(-c,F-3/2). Independent exact symbolic calculation verifies its norm is F-1 and its distances to each foot are F. The displayed three positive weights sum to one. More importantly, the actual distance gradients, rather than merely the barycentric coordinates, satisfy

    w o/(F-1) + w_plus (o-p_plus)/F
      + w_minus (o-p_minus)/F = (0,0).

Both coordinates were checked as exact rational-function identities. The assignment of the plus and minus weights in the frozen report is correct. Swapping them or omitting the disk-gradient normalization fails independent negative controls. The equivalence with contact-point barycentric weights is legitimate because all three active contacts lie at the same outer radius F.

The exact identity

    w-3/8 = (t^4-1)^2/(8t^4)

proves the uniform positive sensitivity w>=3/8. The plus weight is positive already at t=41/50 and its relevant numerator factor increases; the other endpoint factor 1+t^2-t^4 is greater than one for 0<t<1. Thus no invalid extension of the source's one-foot branch is made.

A weighted sum of the three convex distance functions is minimized at o by the zero gradient. Increasing the centered disk radius from one to 1+eta adds exactly w*eta to this weighted sum. The maximum dominates that sum at every outer center, proving f(1,1+eta)>=F+w*eta for all eta>=0, not just infinitesimally.

For the crossing cell's actual outer circle, delta=R-d-1 ensures that this same circle contains the centered disk of radius 1+delta as well as both canonical feet. The enlarged disk need not be inside the polygon; the argument only requires its inclusion in the outer circle. Therefore gamma-F(t)>=3delta/8 follows correctly. Confusing these two containments would invalidate the argument, but the frozen proof does not do so.

## Final constants and controls

For D(gamma)=gamma-F(sqrt(2)gamma-1), direct differentiation gives D'=1+(sqrt(2)/2)(t^(-3)-t). On t>4/5, t<1, the second summand is smaller than (3/4)(369/320)<1, so D'<2. As D(G)=0 and gamma>G, integration gives D(gamma)<2(gamma-G).

Combining the strict annulus gap, the disk weight 3/8, this derivative factor two, and m-1<=N+2 gives precisely 1/(192*25^(N+2)). The constant arithmetic has been checked exactly. For gamma>1.3, the independently checked G<1.29 and 1/192<0.01 suffice for the remaining case.

The fresh independent algebra checker checks nine exact zero identities, rational interval and constant inequalities, and a rational sign bracket for t0. Four intentionally incorrect algebra variants are rejected. It imports no producer check code. [the exact independent algebra audit](INDEPENDENT_GAP_ALGEBRA.json) records its exact results and SymPy version. These tests support the algebra; the preceding geometric review is what validates the normal walk, finite side count and boundary crossing.

## Remaining problem

The new statement is a necessary condition for each finite N. Its correction vanishes with N, so the accepted global bracket is still the prior lower bound G together with the improved complete-square upper witness below 1.296046. A local favorable junction, annulus estimate or finite-N obstruction is not a full solution of the original optimization problem. The source context remains Damian and O'Rourke, arXiv cs/0304023v2, https://arxiv.org/abs/cs/0304023v2, and TOPP Problem 59, https://topp.openproblem.net/p59. No unrestricted completion, attainment or priority conclusion is inferred.
