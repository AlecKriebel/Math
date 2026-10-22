# Root mathematical review of PR #1108

Pinned head: `148130ab93ab46a3459d7bc98a11a1ca79052d65`.
Problem 30003439 / OWR-15219-008. Review checkpoint: 2026-10-17.
Mathematical-review completion estimate: 100%; full publication workflow remains pending.

## Claim, target, and success criteria

The original Tunçel OWR14/2017 p799 problem is existential: an algebraic convex cone with a negative-third-derivative-curvature normal barrier that is not a hyperbolicity cone. The author-hosted three-page contribution was opened directly, including its definitions and question. The candidate explicitly claims a full resolution of this target. It does not claim the broader all-regular-cones barrier theorem. The QUEUE row is not used to override the actual recorded outcome.

Success requires closed pointed full-dimensional convex polynomial-defined K, a genuine normal barrier on its complete interior, universal third derivative inequality for every cone direction, and exclusion of every possible homogeneous hyperbolicity representation in the original three-dimensional space. Checking only the cubic or a signed/dual/lifted cone would be insufficient.

## Direct review

The weighted-geometric-mean Hessian is a negative scalar times the outer product (y,-x)(y,-x)^T; continuity extends concavity to the axes. This establishes convexity of the actual one-sided hypograph. Strict feasibility and orthant containment establish the other regularity properties. Its finite boundary has z*p=0, so the complete extended barrier blows up, including on the extra facet and the vertex.

I checked the line derivatives of g=z³/y² and the slack form f=-log(x-g)-2log y-log z. The Hessian is the sum w²+v²+2b²+c², positive except at zero direction. Polarizing the cubic gives the displayed mixed expression without missing coefficients. Weighted Cauchy–Schwarz bounds its four groups by 2,3,3,2 times the local norms. Scaling f by25 therefore gives the standard constant2; the homogeneous degree4 gives parameter100 and the gradient bound with equality. No optimality of this parameter is asserted.

I checked the diagonal normalization using a fixed automorphism when differentiating; the invariant r is retained rather than treated as a transitive orbit. The decomposition into h(t)=(t³,1,t) and e_x has nonnegative coefficients for every h in K, with the h_y=0 case separately forced onto e_x. I checked the positivity reasoning for P,R on [0,1), at1, and above1. The square remainders are strictly positive where used. Sylvester is used only away from t=1; the exceptional block and the endpoint Gram decomposition handle both rank-two cases. The two independent reviewers separately reproduced the exact matrix, minors, and square identities, including a second logarithm-series mechanism. The analytic proof, rather than parameter sampling, establishes the universal conclusion.

For arbitrary homogeneous H defining K, positive-root continuity forces H to vanish on the curved boundary patch. Substituting x=z³/y² and clearing denominators gives an identity; primitivity of y²x-z³ and Gauss's lemma supply divisibility. For every proposed interior hyperbolicity direction e, the restriction along (0,0,1)+te factors with quadratic discriminant -3a²<0. The nonzero product cannot cancel roots. This excludes every H, not merely p, and is invariant under same-dimensional linear isomorphisms.

## Falsification and limitations

The independent families test wrong sign, forbidden t<0, omission of -log z, degenerate directions, exact scaling, and nonreal roots. In particular -s³D³(-log p)[h] has negative determinant at base(5,1,1), h=(8,1,2); dropping the added facet logarithm fails.

No mathematical repair is needed at the original stated scope. This is an AI-assisted, unrefereed review, not human peer review or formal certification. The cone is already Hildebrand's family5 member and must be credited. Full priority and publication acceptance remain separate gates; new package adversaries must review the actual preprint and distribution after those are prepared.
