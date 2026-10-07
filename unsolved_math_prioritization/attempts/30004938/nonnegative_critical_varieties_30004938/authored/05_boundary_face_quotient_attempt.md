# Author approach 5: enumerate the boundary quotient and test its face structure

Status: exact finite tube enumeration and an explicitly bounded exploratory face calculation. This is a substantive attempt to finish the missing stratification step for the bowtie example, not a proof of all-f polytopality.

## The combinatorial model

For fbar=(3,1,5,2,4), the affine poset is generated, with period 5, by the circular chains

    1 < 2 < 3 < 6,
    2 < 4 < 5 < 7.

Its infinite Hasse diagram consists of two cyclic three-label chains meeting at the shared strand label 2 modulo 5. A proper tube is a finite convex connected subset containing at most one representative of each residue class. Every tube class has a unique translate whose minimum belongs to {1,...,5}.

## Exact tube enumeration

The script `checks/enumerate_bowtie_tubes.py` uses the transitive closure of the generating relations and tests residue uniqueness, order convexity and connectedness with integer arithmetic. The search is complete for tubes: every tube has at most five elements; its induced connected Hasse diagram has a spanning tree; each Hasse edge is among the generating edges, whose integer jump is at most four. Hence its total span is at most 4(5−1)=16, which is the enumerated bound. All elements relevant to convexity lie between the minimum and maximum, since every generating relation increases the integer label.

The result is 37 tube classes, distributed by size as follows:

    size 2: 6; size 3: 10; size 4: 12; size 5: 9.

These are precisely the candidate facets of the four-dimensional affine poset cyclohedron under the source's tube-face theorem.

## Image mechanism

Restrict any compactified angular configuration to either triple {1,2,3} or {2,4,5}.

- If its three points are distinct at the circle scale, its normalized sine triple lies in the interior of T.
- If all three first separate at a common finite linear scale with three distinct positions, its side triple lies in the relative interior of an edge of T: the largest side equals the sum of the other two.
- If two of the three points remain together at their first separating scale, the normalized side triple is a vertex of T, with one zero side and the other two equal.

Thus a tubing predicts a pair of product-face types. The exact measurement formula from approach 2 determines the critical limit from those two normalized triples.

## Exploratory full-face calculation

The script `checks/enumerate_bowtie_faces.py` enumerates compatible collections of at most four tube classes, tests nesting/disjointness against translates, and uses a finite window of translates for the acyclicity test. It reports codimension counts

    1, 37, 189, 304, 152

and 49 predicted product-face types. The counts obey Euler's identity 1−37+189−304+152=1 and the simple-four-polytope relation 304=2×152. There are exactly 49 nonempty faces of T×T, since a triangle has 7 nonempty faces.

These agreements are useful checks, not certification. In particular, finite-window acyclicity is explicitly marked exploratory in the output; it is not substituted for a proof of acyclicity of the entire periodic graph. More importantly, assigning a face type establishes at most containment of the image in that product stratum, not surjectivity onto the stratum.

## Attempted completion and exact remaining gap

A promising argument for surjectivity is to build each face chart recursively. A mixed connected tube must contain the shared strand 2 at some translate; after fixing its position, the two three-point shape parameters seem freely rescalable. When the two triples first separate in distinct nested tubes, their ratios should vary independently. When they first separate at the same tube, the local poset is the union of two chains meeting at that shared element.

To finish, one must prove, for every tubing, that these local choices are simultaneously compatible with the specified child-tube collisions and all induced order constraints, for every pair of points of the predicted product-face interiors. This universal surjectivity assertion is not proved by the enumeration, by one sample per face, or by the product topology already established. No stratified-homeomorphism claim is made without it.

If it were proved, the image of every open cyclohedron face would be a product-face interior. Surjectivity of the whole compactification and coverage of T×T would then imply that every product stratum occurs, so the common refinement in Definition 4.9 would be exactly the product face stratification. This would settle the bowtie example only. Arbitrary connected f would still require a new construction.
