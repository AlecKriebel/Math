# Author approach 1: connected-component and extreme-rank induction

Target: construct a stratification-preserving homeomorphism from every critical closure to a convex polytope. This is an authored reduction, not a resolution of the full target.

Use the loopless bounded affine permutation convention of Galashin, arXiv:2110.08548v2, Definitions 2.1–2.5. Thus j < f(j) <= j+n, and sum_{j=1}^n (f(j)-j)=kn. A strand runs from b_j^+ to b_{f(j) mod n}^-.

## Lemma 1: a connected diagram has displacement bounds

If n>1 and the strand diagram is connected, then

    2 <= f(j)-j <= n-1  for every j.

Proof. A displacement 1 joins consecutive boundary points b_j^+ and b_{j+1}^-. Its straight chord crosses no other strand, because the open boundary arc between its endpoints is empty. A displacement n is the coloop strand joining b_j^+ to b_j^-, also consecutive boundary points. Either gives an isolated component, contrary to connectedness for n>1. All displacements are integers in [1,n], proving the bounds.

## Corollary 2: the extreme connected ranks are already top cells

For a connected diagram with k=2, every displacement equals 2: their sum is 2n and each is at least 2. Thus f=f_{2,n}. For connected k=n-1, each displacement equals n-1 by the analogous upper bound, so f=f_{n-1,n}. There are no connected diagrams with n>1 at ranks 1 or n.

Consequently every connected diagram with n<=4 is one of the top-cell cases already covered by Galashin's stratified hypersimplex theorem, apart from the trivial one-point case. This is a mathematical classification, not an inference from numerical sampling.

## Attempted induction and its precise obstruction

The known product factorization over disconnected strand components would allow induction if every larger diagram split into such components, or had extreme rank after restriction. It does not. For n=5 the permutation

    fbar = (3,1,5,2,4),  f = (3,6,5,7,9)

has k=3 and crossing pairs

    12, 13, 23, 24, 25, 45.

The crossing graph is connected (two triangles sharing vertex 2), and f is not the top shift. Thus the component induction stops already at n=5. The next author approach treats this example directly.

## Exact finite check

The accompanying `checks/enumerate_strands.py` uses integer boundary positions and the alternating-endpoint criterion for chord intersection. It enumerates all ordinary permutations and uses their unique loopless lifts. Connected counts by k for n=3,4,5,6 are respectively {2:1}, {2:1,3:1}, {2:1,3:11,4:1}, and {2:1,3:36,4:36,5:1}. The enumeration is a check of the argument and provides examples; it is not the proof of the all-n extreme-rank corollary.

## Limit

This reduction neither identifies the general face poset nor proves boundary regularity. The closure product fact quoted in the primary source must not be strengthened silently to an arbitrary new stratification claim.
