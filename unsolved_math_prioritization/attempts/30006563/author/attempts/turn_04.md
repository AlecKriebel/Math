# Attempt 4 of 5: finite seeds and a certified additive improvement

## Aim

Test whether a small seed can beat the report's displayed n-4 upper bound, and distinguish a genuine all-n improvement from a full asymptotic resolution. This uses only bounded checks on at most eight vertices, not a large search.

## A hand-provable two-color K_7

Partition the vertices as A disjoint-union B disjoint-union {z}, with |A|=|B|=3. Color every edge inside A and every edge incident to z red. Color all other edges blue.

The four possible triangle types can be checked completely:

- Three red edges: the triangle is contained in A union {z}, which has four vertices. Any two such triangles intersect.
- Two red edges and one blue edge: every such triangle contains z. They intersect there.
- One red edge and two blue edges: the triangle has two vertices in A and one in B. Any two use intersecting two-subsets of the three-element set A.
- Three blue edges: the triangle avoids z and has at most one vertex in A, so it has at least two vertices in B. Any two therefore intersect inside B.

These exhaust the types, so the coloring is admissible. One color is impossible already on six vertices. Restricting the K_7 construction to six vertices gives

    g(6)=g(7)=2.

Appending n-7 vertices by the fresh-private-star operation in Attempt 1 yields the unconditional bound

    g(n) <= n-5  for every n>=7.

This improves the numeric additive constant in the source's stated upper bound. No claim is made that the construction is new; the bounded literature search did not establish priority. It does not settle linear growth, and it is entirely consistent with g(n)=n-O(1).

## Exact eight-vertex check

For two colors, encode every edge e by a bit x_e. Two triangles have the same type precisely when their sums of x_e agree. For each unordered pair of vertex-disjoint triangles, forbid all assignments to their six edges having equal sums.

There are binom(8,6)*10=280 such triangle pairs. Each pair gives

    sum_(k=0)^3 binom(3,k)^2 = 20

forbidden assignments, hence 5,600 clauses over the 28 edge variables. Each clause has six literals and excludes exactly one of these assignments. A global interchange of colors permits the first edge to be fixed to zero without loss.

The included dependency-free exact DPLL checker finds this instance UNSAT. It writes a binary proof tree with 571 nodes and explicit unit-propagation reasons and conflict-clause indices. A separate literal-list replay routine checks every forced assignment, verifies every contradiction, and checks that each branching node covers both assignments to an unassigned variable. The proof uses integer/Boolean operations only. This is a computer-assisted finite result, not a human-only proof or an asymptotic lower bound.

The complete files are checks/small_two_color.py, checks/k8_two_color_unsat_certificate.json, checks/k8_two_color_results.json and the K_6/K_7 witness results. The n=8 run took under one second in this environment; the hard cap was 30 seconds. Replaying the certificate succeeds. By adjoining a fresh-color vertex to K_7, three colors suffice on K_8, so the finite conclusion is

    g(8)=3.

## Why the seed route does not finish the problem

Private-star extension preserves the deficit n-q. A single better seed gives a better fixed constant only. To refute n-O(1), one would need admissible seeds with n-q unbounded. To refute linear growth, one needs q/n tending to zero. Neither follows from K_7, the K_8 obstruction, or the extension operation. The uniform-product amplification route was already blocked in Attempt 3.

## Verdict

No full resolution. A rigorous explicit bound g(n)<=n-5 for n>=7 is obtained, with g(6)=g(7)=2 proved by hand and g(8)=3 supported by an exact replayable finite certificate. This counts as substantive attempt 4/5.
