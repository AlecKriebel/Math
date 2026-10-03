# Attempt 1: testing the proposed short-witness route

3 October 2026. Outcome: a proposed sufficient route is false in general;
the group-order problem remains open. Discovery-goal completion estimate: 10%
(a subjective workflow estimate, not a probability of correctness).

## Question attacked

Could 2R-regularity force C_x(a_d r) to span R^d for a dimension-only a_d?
That would turn the elementary short-span bound into a solution. More
generally, could it force a large rank at this scale?

## Exact obstruction

Fix d >= 2 and 1 <= k < d. For L > 1 set

    X_L = Z^k x (L Z)^(d-k).

Its exact parameters are

    r = 1/2,     R = (1/2) sqrt(k + (d-k)L^2).

The packing assertion follows from the shortest coordinate vectors. Every
point of R^d has a lattice point within the half-diagonal of a rectangular
fundamental box; the center of that box realizes this distance. This proves
the covering formula, including exactness. Lattice translations prove
centered equivalence at every radius, in particular at 2R.

For any a >= 2, choose L > a/2. Every vector in C_0(ar) then has its last
d-k coordinates zero: a nonzero such coordinate alone has length at least L.
The first k coordinate vectors belong to this cluster. Consequently

    dim span(C_0(ar)) = k.

Thus no dimension-only fixed multiple of r forces full span. It does not
even force rank two. The obstruction occurs among globally regular lattices,
so adding global regularity would not rescue this proposed route. For a<2
the cluster is just its center and the failure is even more immediate.

## Why this is not a counterexample to the original problem

The group order stays bounded. In fact, for L>1,

    |S_0(2R)| = 2^d k! (d-k)!.

To prove this, the shortest shell is exactly {+/-e_1,...,+/-e_k}; its span V
is therefore preserved, and the action on V is a signed coordinate
permutation. Orthogonality preserves V-perp. Since L <= 2R, the intersection
C_0(2R) with V-perp contains its shortest shell
{+/-L e_(k+1),..., +/-L e_d}. Its symmetry on V-perp is also a signed
coordinate permutation. Conversely, every independent signed permutation
in these two blocks preserves the lattice and the ball. This proves both
directions and the exact cardinality.

## Consequence and remaining gap

Short-span estimates are valid conditional results, but cannot be made
unconditional by the proposed uniform-radius spanning assertion. An
anisotropic or rank-by-rank mechanism is necessary. The example shows why
large R/r alone is not evidence of large local symmetry: its value tends
to infinity while the group order is constant.

This elementary family is not asserted to be new. The useful correction is
to eliminate a false sufficient claim from the forward research plan.
