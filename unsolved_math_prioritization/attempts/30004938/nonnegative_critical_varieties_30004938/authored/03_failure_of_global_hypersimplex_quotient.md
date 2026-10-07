# Author approach 3: try to extend the top-cell hypersimplex quotient

## Proposed route

Galashin's top-cell proof forgets infinitesimal distance ratios: the cyclohedron-to-critical-closure map factors through normalized cyclic polygon side lengths, giving the second hypersimplex. An attractive all-f proof would use the same global quotient. We test this on the explicit lower-cell formula from approach 2.

## Exact obstruction

Fix fbar=(3,1,5,2,4). For t>0 sufficiently small, compare the admissible angular tuples

    θ(t)=(-t,0,t,π/3,2π/3),
    η(t)=(-2t,0,t,π/3,2π/3).

They have the same limiting configuration on the circle: labels 1,2,3 coincide, while labels 4 and 5 remain at the two other cube roots of unity. The maximum pairwise chord distance has a nonzero limit. Thus all differences among labels 1,2,3 are infinitesimal relative to that global diameter.

In approach 2's notation, both families have D=E=F=√3/2. But their first sine triples have different projective limits:

    (A:B:C) → (1:1:2) for θ(t),
    (A:B:C) → (2:1:3) for η(t).

Substituting in the exact Plücker formula gives distinct limiting points, respectively

    (0,1,1,1,1,1,2,2,2,0),
    (0,1,1,2,2,2,3,3,3,0),

in lexicographic triple order. For example, the ratio Δ134/Δ124 is 1 in the first limit and 2 in the second. All cited denominator coordinates are nonzero, so the distinction is projectively intrinsic.

Moreover both tuples are cyclically ordered around the circle. Their normalized five cyclic side-length vectors have the same limit: the first two side lengths vanish and the other three become equal. Under the normalization summing to 2 this is (0,0,2/3,2/3,2/3), up to the common convention for indexing sides.

Therefore there cannot be a continuous factorization of this lower-cell measurement map through the unmodified top-cell global side-length quotient. The two fibers that quotient identifies have different measurement limits.

## What this establishes

This is a rigorous obstruction to a particular proposed all-f proof. It is not a counterexample to the stated polytopality problem: the source does not assert global independence of infinitesimal ratios for lower cells, and a different polytope may retain the surviving local ratios. Indeed the product-of-triangles model from approach 2 retains exactly such information.

The next proof route must preserve selected nested collision data and prove that the resulting quotient has polytopal face structure.
