# Working Plan

## Common normalization

For a finite spherical set, normalize every point to squared norm one and let
\(m=\min_{i<j}\langle p_i,p_j\rangle\). Diameter edges are precisely pairs
with inner product \(m\), because
\(\lVert p_i-p_j\rVert^2=2-2\langle p_i,p_j\rangle\). A candidate therefore
needs a rank-at-most-four positive semidefinite Gram matrix whose minimum-entry
graph is not 5-colorable.

Non-spherical candidates are retained through centered Euclidean distance
matrices: \(B=-\tfrac12 J\Delta J\) must be positive semidefinite of rank at
most four.

## Route A — symmetric exact families

1. Generate explicit signed-permutation and small reflection orbits from seed
   vectors with rational or low-degree algebraic coordinates.
2. Classify inner products by orbit invariants rather than pair enumeration.
3. Compute exact chromatic numbers of minimum-inner-product graphs.
4. Explore carefully chosen unions and symmetry-preserving deformations.
5. Reject immediately on five-colorability, rank, or a hidden larger distance.

## Route B — graph first

1. Construct six-chromatic graphs from explicit combinatorial rules, including
   joins, products, incidence graphs, and critical subgraphs.
2. Solve symmetry-reduced Gram equalities for a common edge distance, PSD rank
   at most four, and strict nonedge inequalities.
3. Use numerical nonlinear/semidefinite optimization only to suggest exact
   parameters; recognize and re-check every candidate symbolically.
4. When a candidate survives, emit CNF, proof, and a tiny independent checker.

## Route C — positive theorem

1. Derive reductions from arbitrary bounded sets to compact sets and finite
   obstructions without losing the strict inequality.
2. Analyze diameter-pair geometry, antipodal structure, and supporting cones in
   dimension four.
3. Seek a canonical simplex/cone/Voronoi partition into five classes.
4. Separate genuine universal lemmas from statements needing symmetry,
   smoothness, or bounded facial complexity.

## Decision gates

- No broad random coordinate search.
- No computation expected to exceed 4 GB RAM or 2 GB output without a logged
  justification and a smaller pilot.
- A floating-point near-candidate is evidence only; it cannot advance beyond
  discovery until exact reconstruction.
- Literature audit is prohibited during discovery and starts only after an
  exact result passes independent checks.
