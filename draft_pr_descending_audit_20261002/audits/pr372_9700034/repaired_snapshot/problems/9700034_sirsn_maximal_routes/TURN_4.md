# Author turn 4: finite exterior arcs and the remaining endpoint obstruction

**Unconditional geometric reductions; original unresolved, 4/5.**
This turn uses the ordinary SIRSN axioms and Aldous's established major-road
process, including the planted-point identity (6.4). It introduces no route-
length triangle inequality or continuum route version. The conclusions are
about countably sampled prescribed routes. Almost-sure finiteness of a
random finite union is not confused with finite expected length.

Write p=p(1)<infinity for the major-road intensity. The source's equations
(6.2),(6.4) supply a common major-road process E_r of intensity p/r, containing
the portions of sampled routes at distance at least r from both endpoints,
also when an extra point is planted at 0. Independent uniform points in a
bounded region may be coupled with successive arrivals of a space-time
Poisson process in that region. Add independent arrivals outside it to
obtain the full process; this puts all required countable routes in the
source construction. Only countably many r will be used at one time.

## 1. Exterior excursions form a finite union almost surely

Let U_i be independent uniform points in the unit disc, independent of the
SIRSN, and include the planted point 0. Consider either the rooted routes
R(0,U_i), or even all prescribed routes between pairs from {0,U_1,U_2,...}.
Every point of one of these routes on circle(0,3) is more than unit distance
from both endpoints, and hence belongs to E_1. Put

    C = E_1 intersection circle(0,3),       N=|C|.

The source's intersection-intensity formula (2.2), as applied to circles in
Proposition 6.1 and §5.5, gives

    E N ≤ 12p < infinity.                              (1)

Counting edge intersections with multiplicity only increases the number
of distinct points, so the inequality is sufficient. The expectation
excludes an infinite tangency/overlap exception as well. Thus C is finite
almost surely.

Each connected excursion of a route in the open exterior of the radius-3
ball has two distinct endpoints a,b in C. Indeed the prescribed path is
continuous, injective and has both endpoints inside the unit disc. Its
parameter intervals outside the ball have finite endpoints on the circle.
The two cannot coincide, since that would make a nontrivial closed subpath.
The closed excursion arc has finite length as a subroute of its witness.

If two excursion arcs have the same unordered pair {a,b}, their witness
routes meet at those two points. Pairwise route compatibility forces the
whole subroutes between a and b to coincide. Consequently, at most
binomial(N,2) different excursion arcs occur. Each possible arc has a
finite-length witness among the countably many prescribed routes.

**Proposition.** The union of all the sampled prescribed routes outside
B(0,3) has finite total length almost surely and is contained in some
finite random ball. In particular, there is a finite random confinement
radius for this entire countable family, even though no deterministic
confinement radius or integrable confinement bound has been proved.

The conclusion follows because the exterior is a finite union of compact
finite-length arcs. No measurable selection of witnesses is needed: the
union length and sampled maximal radius are countable suprema/limits, and
the finite-arc argument proves their finiteness pathwise.

It would be an error to infer finite mean exterior length from (1). The
lengths of the finitely many selected arcs may be biased and heavy-tailed;
(1) controls only a crossing count. Nor does the proposition control the
total length of the sampled union inside the endpoint region, which can
be infinite as the sample becomes dense.

## 2. The fixed-root end is integrably controlled

Now sample endpoints V_i uniformly from the annulus

    A={z:1/2<|z|<1},

and write M_A=sup_i len R(0,V_i). For 0<eta≤1/4 let H_eta be the union of
all portions of these rooted routes inside B(0,eta). We prove

    E len(H_eta) ≤ 3pi p eta.                           (2)

Partition the punctured ball into annuli

    A_j={eta 2^(−j−1)<|x|≤eta 2^(−j)},       j≥0.

For a route point x in A_j, its distance from 0 exceeds eta 2^(−j−1), and
its distance from any V_i is at least 1/2−eta≥eta. It therefore lies in
E_(eta 2^(−j−1)). Set inclusion and the intensity formula give

    E len(H_eta intersection A_j)
      ≤ pi eta²(4^(−j)−4^(−j−1)) · p/(eta 2^(−j−1))
      = (3pi/2) p eta 2^(−j).

Summing proves (2). Boundaries have zero expected edge length by the
intensity measure, and the origin itself has zero length; neither adds a
missing term. This bound concerns the total union at the fixed root, not
just one route. It holds even if a route returns to that neighborhood.

## 3. Exact reduction to terminal pieces and exterior maximal lengths

For fixed 0<eta≤1/4 define two countably sampled nonnegative functionals:

    J_eta = sup_i len[R(0,V_i) intersection B(V_i,eta)],
    O = sup_i len[R(0,V_i) outside B(0,3)].

The first is the largest portion near its varying destination. The second
is the largest exterior length of an individual prescribed route, as
distinguished from the total exterior union. Proposition 1 shows O is
finite almost surely; it does not show E O finite.

Every remaining route point inside B(0,3) lies outside both endpoint
eta-balls, so belongs to E_eta. Therefore, pathwise,

    M_A ≤ len(H_eta) + len(E_eta intersection B(0,3))
                         + J_eta + O.                  (3)

The first two terms have finite expected sum bounded by

    3pi p eta + 9pi p/eta.                              (4)

Conversely, J_eta≤M_A and O≤M_A. Thus for each fixed eta in this range,

    E M_A<infinity  iff  E J_eta<infinity and E O<infinity. (5)

This is a localization of the exact gap. It proves that the fixed-root
end and the bounded middle cannot themselves obstruct the expected maximum.
It does not remove the two remaining maximal estimates by renaming them.
No assertion of uniform vanishing of J_eta as eta→0 is made.

## 4. The annulus and disc questions are equivalent

Partition the unit disc, up to zero-area circles and the origin, into
2^(−k)A, k≥0. In an infinite independent uniform disc sample, each shell
contains infinitely many endpoints almost surely. Its subsequence is an
independent uniform sample on that shell, independent of the route process.
By SIRSN scale invariance, the maximal route length M_k on this subsequence
has distribution 2^(−k) M_A. The variables for different k need not be
independent. Nevertheless,

    M_disc = sup_k M_k ≤ sum_(k≥0) M_k,
    E M_disc ≤ 2 E M_A,                                (6)

whenever the right side is finite, while M_A is realized by the outer-shell
subsequence and E M_A≤E M_disc. Consequently the original disc integrability
is equivalent to annular integrability. Combining this with (5) gives the
same two-function criterion for the original target.

The countable FDD extension and measurable location kernels justify this
sampling and thinning. An uncountable geometric supremum is not substituted
for the source's iid sample.

## 5. Why a geometric counterexample remains difficult

A tempting scalar construction assigns extremely long routes to extremely
small endpoint regions. Turns 2–3 show exactly how such scalar laws can
make the maximum nonintegrable. But a valid SIRSN must also respect common
subroutes and finite major-road crossing sets. The present proposition
rules out a proposed counterexample that relies solely on infinitely many
distinct arbitrarily distant exterior arcs from one bounded endpoint set:
those arcs cannot all exist in the sampled network. Heavy lengths of a
finite random set of arcs are still possible under these estimates.

Similarly, a bounded local region with many tiny terminal pieces is not
controlled by the fixed-root estimate (2), because the centers now vary with
the endpoints. No routing construction meeting the full SIRSN axioms has
been found for either remaining failure mechanism.

The next, final turn will examine closure of the model class under mixtures
and whether the hoped-for universal finiteness statement forces a uniform
quantitative estimate. This is a different route to a legitimate network
counterexample, rather than treating the scalar examples as networks.

## Dependency and control scope

Aldous (2014), §§2.1–2.3, (6.2), Proposition 6.3 and the explicit planted-
origin consequence (6.4), plus compatibility (2.4). The source's major-road
construction and its measure-theoretic formulation are credited inputs;
their general existence theorem is not re-proved here. The finite checker
uses compatible rooted paths in finite trees and checks boundary-pair
uniqueness and dyadic constants. It neither simulates a SIRSN nor replaces
the above countable continuum argument.
