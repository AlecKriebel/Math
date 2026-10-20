# Scope, status, and quantifiers

## Original target

For a finite family of affine lines ell_1,...,ell_N in R^3, set

    C = [0,1]^3,
    A = C intersect (union_i ell_i),
    L = H^1(A) > 0,
    mu_A(B) = H^1(A intersect B)/L.

The proposed inequality is

    sup_{cubes Q contained in C} |mu_A(Q)-volume(Q)|
        >= c log(L)/L,

with one positive c independent of the lines, their number, directions, positions, intersections, and lengths. The logarithm is natural; changing its base only rescales c. For 0<L<=1 the right side is nonpositive, so the substantive regime is large L.

The source is Stefan Steinerberger's contribution, "Three problems for discrepancy and QMC," printed page 2891 of the 2013 Oberwolfach report. The source expressly restricts Q to cubes contained in C, but does not expressly specify their orientations or boundary convention. These notes use closed positive-side cubes and distinguish two different test classes:

- D_axis: cube edges parallel to C's axes.
- D_rot: arbitrary Euclidean orientations, still wholly contained in C.

The raw catalog formula omitted the cube-test restriction; no replacement with boxes is licensed by that omission. The identifier OWR-12723-007 is a catalog label, not a problem number printed in the source.

## Status split

1. **Axis-parallel interpretation: DISPROVED.** The exact full-chord sequence in Attempt 2, using Borda's established uniform box theorem, has L_n=sqrt(6)n and D_axis(A_n)=O(1/L_n). Its ratio to log L_n/L_n tends to zero.
2. **Arbitrary-orientation interpretation: UNSOLVED by this package.** Attempts 3–5 establish a universal 1/L baseline and logarithmic bounds for parallel families and fixed finite mixtures of specified algebraic-flow families, not for arbitrary line unions.
3. **Original unqualified statement: UNSOLVED, five attempts completed.** The source ambiguity prevents treating the restricted disproof as an unqualified resolution. This is a work-product classification, not a claim that no later published resolution exists. The bounded literature search located no inspected matching resolution; absence from that search does not prove current openness.

## Model restrictions

- Every contributing object is the complete intersection of an affine line with C. General truncated segments or rectifiable curves are different classes.
- H^1 measures the union as a set. Repeated lines do not create extra mass. Distinct noncoincident lines meet at most in points, which have zero arclength.
- L is total length, not N. Each chord is at most sqrt(3) long, but grazing chords can be arbitrarily short. No positive lower chord-length assumption is imposed.
- These are positive normalized arclength measures. No coloring, signed line weight, balancing choice, or separately normalized average of chords is present.
- The discrepancy is a supremum, not an L^2 norm, expectation, or essential supremum over orientations.
- Closed boundaries are handled within the proofs. In the explicit Borda sequence axis-parallel test boundaries have zero arclength. The universal rotating-cube jump proof uses one-sided limits of admissible translated cubes, not a degenerate cube or an assumed boundary convention change.

## Dependence and limits of the positive theorems

The parallel logarithmic bound has a universal constant independent of common direction. It uses a fixed-size inner cube aligned with that direction and a weighted planar square lower bound. The large-square transfer is proved for arbitrary finite signed Borel measures and handles boundary mass. The established ordinary planar square lower bound is an imported input, not claimed as new.

The fixed-mixture theorem fixes finitely many directions once and for all. Each direction has positive algebraic coordinates, those three coordinates are Q-linearly independent, and one coordinate equals 1. The directions are pairwise nonparallel. All constituent flows have integer duration n. The constant-error bounds for the other families and the resulting onset threshold depend on this fixed direction data. Neither a growing number of directions nor arbitrary nonparallel chord placements is covered.

Borda's axis-parallel corollary has a bound uniform over all starting points, durations, and boxes for a fixed allowed direction. Its rotated-polytope theorem instead requires algebraic facet normals with nonzero scalar product with the flow direction; its bound depends on those fixed normals. A cube with a face parallel to the direction fails that transversality condition. Density of allowed frames does not create the missing common constant.

## Computation and attribution

The script is optional exploratory floating-point work. An exact evaluation on finitely many valid cubes would produce a lower bound for a supremum, never an upper bound. The present computed values do not have certified rounding, cube containment, or clipping and therefore are not asserted as certified lower bounds either. No numerical counterexample is claimed. The asymptotic axis-parallel disproof and the positive lower bounds are mathematical arguments independent of the experiment.

No historical novelty claim is made for the authored arguments or reductions. Source theorem statements are paraphrased with citations. The source documents themselves are not redistributed.
