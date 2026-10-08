# 3. Quantitative boundary regularity and dimension

## Attempt

Instead of finding a compact leaf or an explicit halfspace, force one leaf limit set to have zero two-dimensional area. The sufficient numerical threshold below is elementary and makes the missing estimate precise.

## Lemma 3: Hölder threshold

Give S^1 its arc metric and S^2 a round metric. Suppose f:S^1 -> S^2 satisfies d(f(x),f(y)) <= C d(x,y)^alpha for all x,y, with C finite and alpha>1/2. Then f(S^1) has zero two-dimensional Hausdorff measure, so is not S^2.

Proof. Cover S^1 by n equal closed arcs of length 2*pi/n. Their images cover f(S^1), have diameter at most C(2*pi/n)^alpha, and the sum of squared diameters is at most C^2(2*pi)^(2*alpha)n^(1-2*alpha), which tends to zero. The maximal diameter tends to zero too. This is precisely the defining upper bound for two-dimensional Hausdorff measure. The round sphere has positive such measure, proving properness. The same calculation gives dim_H f(S^1)<=1/alpha, by replacing 2 with any s>1/alpha.

If the continuous extension of an inclusion L -> H^3 to the closed intrinsic disk is available, its boundary image equals Lambda(L). For inclusion in one direction, approach any intrinsic boundary point from inside. For the reverse direction, take a sequence in L approaching ambient infinity and extract an intrinsic compactification subsequence. It cannot converge to an interior point, by continuity of the inclusion and properness of L. Its boundary limit maps to the prescribed ambient point.

Hence in the closed taut two-sided setting a single extension with alpha>1/2 yields a proper leaf limit set and, through Calegari's alternative, an asymptotically separated leaf.

## Endpoint and continuity obstructions

At alpha=1/2 the displayed covering bound is constant, not tending to zero. For alpha<1/2 it grows. Thus this particular proof establishes no boundary case. It does not assert that every map at or below the threshold fills the sphere.

Mere continuity cannot replace the estimate. The standard Peano phenomenon already allows a continuous map of a circle onto a sphere. More concretely, the credited Cannon–Thurston surface-bundle example has sphere-filling leaf boundary maps. Its foliation is R-covered and is not a target counterexample, but it rejects the proposed general inference from continuity to proper image.

Fenley's continuous-extension results and Buckminster's 2026 universal-circle map must consequently be kept separate from quantitative proper-image estimates. In particular a surjective map from the global universal circle is not a statement that an individual leaf's boundary map is or is not surjective.

Remaining gap: produce this Hölder bound, a substitute Hausdorff-dimension bound, or a missing boundary point for some leaf of every target foliation. No such bound is obtained from two-sided branching. Choosing a different arbitrary circle metric cannot be used to claim the round/intrinsic visual-metric estimate above.
