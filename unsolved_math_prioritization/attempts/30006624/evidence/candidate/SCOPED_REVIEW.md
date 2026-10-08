# Adversarial review: PARTIAL_REPORT Propositions 4.1 and 5.1–5.3

Scope: metric and topology hypotheses in those four propositions only. No additional proof family was introduced. Outcome: PASS, with an exposition clarification incorporated into the report. None of the four examples is a counterexample to the full target, as the report explicitly states.

## Proposition 4.1

- The bounds d_1<=d_w<=2d_1 imply completeness and preservation of the topology of the closed strip. The strip is contractible, hence simply connected.
- The formula for |y-v|<2 is valid: for any connecting continuous rectifiable path, the minimum horizontal coordinate z is attained. The lower bound on horizontal weighted variation is F(x)+F(u)-2F(z), and on vertical weighted variation is (1+z)|y-v|. Its derivative in z is strictly negative throughout the allowed interval, so the direct horizontal-plus-vertical path attains the displayed minimum.
- All uses of the formula in the right-angle triple have vertical separation either zero or k<2. No application outside its stated range occurs.
- The I(A,B) claim remains valid despite possible nonattainment of arbitrary path infima. Independently of the short-vertical-separation formula, for any W=(x,y), the sum d_w(A,W)+d_w(W,B) is at least |F(a)-F(x)|+|F(b)-F(x)|+2|y|. This is strictly greater than F(b)-F(a) if y is nonzero or x is outside [a,b]. Equality is attained on the horizontal segment. This explicit lower-bound justification has been incorporated into the report.
- The factor 2+b+x-k is strictly positive because x,b>=0 and k<2. The final defect is (b-a)k>0. Arbitrarily small translated versions fit all interior and relative boundary neighborhoods.

## Proposition 5.1

- Each branch has its compact inherited path metric; paths through another branch cannot shorten it. Points from different branches have distance equal to the sum of their distances to the root. This proves both geodesicity and the stated Cauchy argument.
- In the case not eventually contained in a finite union of branches, each tail has points from arbitrarily many branches. Thus the use of a second tail point in a different branch is justified, and every tail point is forced toward the root.
- The proposed local neighborhoods are ambient-good, not merely intrinsically trees. At attachment vertices the radius less than one eighth of the circumference makes going around the remaining circle strictly longer. Away from attachment vertices one also shrinks to avoid vertices. At the root all excursions to a circle require reaching distance 1 first.
- The equally spaced circle triple has three pairwise short arcs with empty common intersection. Off-circle excursions add length and cannot create ambient interval points.
- The indicated retraction onto any circle is continuous (indeed distance-nonincreasing with the circle's inherited distance). It sends all spokes and all other circles to the chosen attachment vertex. Composing with the circle inclusion is the identity, so its fundamental group injects into that of the full space. Simple connectivity therefore fails.

## Proposition 5.2

- The same branch distance formula proves completeness. Each spoke-plus-square is compact.
- At each fixed time, the first contraction is distance-nonincreasing within every square and fixes spokes. Cross-branch distances go through the root. Its displacement is uniformly bounded by a constant times the time change because square diameters are uniformly bounded. The spoke contraction has the same properties. These observations justify joint continuity, including at the infinite-valence root.
- The point-wedge median proof checks ambient interval membership and uniqueness. A point strictly outside one factor cannot lie on an interval whose endpoints are in that factor, since its excursion from the wedge point adds twice its positive distance to that point. This covers the potentially omitted uniqueness case.
- Filling a circle changes its boundary distances. The report explicitly states this and does not identify the old and new boundary metrics.

## Proposition 5.3

- Every point of the slit plane has an ordinary coordinate rectangle avoiding the slit. For two points in such a rectangle, the coordinate rectangle between them is contained in the neighborhood; hence the intrinsic distance is ordinary l1. Any ambient interval point must be coordinatewise between the endpoints, since intrinsic distances dominate l1 distance. Thus the asserted local ambient medianity is valid.
- These local identifications also verify that the intrinsic metric topology is the usual slit-plane topology. Polar coordinates with radius in (0,infinity) and angle in (0,2*pi) therefore prove simple connectivity for the relevant topology.
- Every path from B to C crosses y=0 at some x<0, giving the strict lower length bound 4-2x>4. Paths crossing at x=-epsilon show that the distance infimum is 4. No minimizing path is assumed.
- The coordinatewise interval argument forces any common point of I(A,B) and I(A,C) onto y=0 with -1<=x<0. Its B-to-C two-leg distance is 4-2x>4, excluding it from I(B,C).
- The negative-axis sequence is Cauchy in the intrinsic metric. Any intrinsic limit would also be its Euclidean limit, the deleted origin, which is impossible. Incompleteness is fully verified.

No substantive correction to these propositions is required.
