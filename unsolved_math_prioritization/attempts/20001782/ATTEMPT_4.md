# Attempt 4: short-neighbor components and a failed quotient induction

3 October 2026. Outcome: rank stabilization propagates local directions,
but even globally regular examples defeat the needed covering inheritance.
General target unresolved. Discovery-goal completion estimate: 15% (subjective).

## The proposed induction

If the short-span kernel acts on fewer dimensions, one might try to apply
the lower-dimensional Delone theorem to short-neighbor components or a
quotient by them. This requires geometric inheritance, not merely an
abstract subgroup embedding in O(d-k).

First establish what rank stabilization really implies. Let X be 2R-regular,
let 0<t<=R, and suppose

    dim span(C_x(t)-x) = dim span(C_x(2t)-x) = k.

The equality then holds at every point by centered cluster equivalence.
Since the smaller span is contained in the larger one, these spans are
equal. Write V_x for that common subspace. Form the graph on X joining
distinct points at distance at most t.

### Propagation lemma

If x and y are joined, then V_y=V_x. Indeed C_y(t) is contained in C_x(2t).
Both y-x and z-x, for z in C_y(t), lie in V_x. Thus z-y lies in V_x,
so V_y is contained in V_x; the ranks are both k. Along any finite graph
path the direction remains the same, and every vertex lies in x+V_x.

Therefore each t-component lies in a k-flat and has a constant associated
short-span direction. This uses radius 2t<=2R exactly where equivalence
of ranks is needed. It does not say the component covers that flat.

## Exact counterexample to the missing covering step

For d>=2 and L>3, consider

    X = Z x (LZ + {0,1}) x (LZ)^(d-2).

This is a Delone set with exact parameters

    r=1/2,
    R=(1/2)sqrt(1+(L-1)^2+(d-2)L^2).

The shortest separation is one. For a Cartesian product, the squared
distance to the product is the sum of squared coordinate distances.
The largest gaps in the coordinates are 1, L-1, and L respectively;
their midpoints realize the covering radius displayed above.

This set is globally regular, hence 2R-regular. Integer translations in
the first coordinate, translations by L in the other coordinates, and
reflection of the second coordinate about 1/2 act transitively on X.
That reflection swaps the residues 0 and 1 modulo L.

Set t=1. At a center with second-coordinate residue 0,

    C_x(1)-x = {0, e_1, -e_1, e_2}.

At residue 1 replace e_2 by -e_2. Since L-1>2 and L>2, the 2-cluster
still lies in span(e_1,e_2). It contains the 1-cluster, so both have rank
two. Also 2t<=2R. All hypotheses of the propagation lemma hold.

Nevertheless, the t-component at the origin is exactly

    Z x {0,1} x {0}^(d-2).

An edge can change the first coordinate by +/-1 or switch the two points
in one close pair; it cannot cross the longer gaps. These moves connect
the displayed ladder and nothing else. Its affine span is a two-plane,
but it is not relatively dense there: the distances from (0,M,0,...,0)
to the component tend to infinity as M tends to infinity.

## Consequence for dimension reduction

A constant short-span direction along a component does not make that
component a Delone set in its affine span. Even all the directions may
agree globally, as here, while each component is a bounded-width ladder.
Projecting perpendicular to that direction can identify several distinct
components, so it is not automatically a faithful component quotient.

The example does not disprove the group-order conjecture. It disproves
an intermediate implication needed by this particular induction route.
Additional control of transverse gaps, component covering, and the induced
centered cluster radius is essential. None has been derived from general
2R-regularity in this attempt. We therefore cannot import the known
two- or three-dimensional bounds into Attempt 2's abstract kernel.

The propagation lemma and the product example are elementary; no novelty
claim is made. They identify the exact inheritance failure rather than
silently treating a finite orthogonal kernel as a Delone group.
