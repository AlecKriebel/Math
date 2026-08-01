# Research Log

## 2026-08-01T15:24:03-07:00 — Program initialization

- Restated the finite counterexample target as an exact diameter graph in
  \(\mathbb R^4\) with chromatic number at least six.
- Established the discovery embargo on Borsuk-specific literature and
  catalogues. General-purpose mathematics and exact computational tools remain
  allowed.
- The original checkout was on an unrelated branch with uncommitted parallel
  work, and another dirty worktree held `main`. To preserve both, initialized a
  sparse standalone checkout at `/Users/alec/Documents/Math-borsuk4`, tracking
  `origin/main`, with all new work under `borsuk_dimension4/`.
- Hardware baseline: Apple M1 Pro, 10 CPU cores, 16 GB RAM, about 23 GB free
  disk. Initial system Python has no scientific packages; the existing project
  virtual environment supplies NumPy 2.0.2, SciPy 1.13.1, and SymPy 1.14.0.
- Began three parallel tracks: symmetric exact configurations, graph-first
  low-rank diameter realizations, and structural five-partition lemmas.

Best-guess completion toward a full resolution: **0.5%**. This is an honest
uncertainty estimate for a potentially open research problem, not a schedule.

## 2026-08-01T15:46:00-07:00 — Regular-simplex pruning theorem

- Proved an exact partial positive theorem: if a diameter-one set in
  \(\mathbb R^4\) contains a diameter \(K_5\), nearest-vertex cells of that
  regular simplex partition the entire set into five pieces of squared
  diameter at most \((18-8\sqrt3)/5<1\).
- The proof embeds the simplex in the sum-zero hyperplane of
  \(\mathbb R^5\), derives exact coordinate lower bounds from the five unit
  balls, and encloses each Voronoi cell in an explicit ball.
- Consequence for the negative route: any counterexample diameter graph is
  necessarily \(K_5\)-free. This also eliminates direct Mycielski-type
  extensions of a diameter \(K_5\).
- Added an independent rational-integer verifier for all constant and radical
  comparisons in the proof.
- A bounded scan of faithful two-frequency cyclic orbits through order 200
  found no parameter at which three cyclic step classes are simultaneous
  diameter classes. With at most two classes the diameter graph has maximum
  degree at most four and is five-colorable by the elementary degree bound.
  This is evidence only, not yet a theorem about all cyclic orders.

Best-guess completion toward a full resolution: **2%**. The simplex lemma is a
real pruning result, but it does not address \(K_5\)-free obstructions.

## 2026-08-01T16:11:00-07:00 — Projected-subset orbit family eliminated

- Classified diameter relations for arbitrary unions of full radial shells on
  the 30 projected nonempty proper subsets of a five-element set in the
  standard \(S_5\) representation.
- Proved a parameter-independent five-coloring: color a subset by a cyclic
  boundary element. Every possible diameter pair is either disjoint or has
  full union, and both cases force different boundary colors.
- The theorem covers any finite number of shells with arbitrary positive
  radii, including every parameter tie; negative radii are absorbed by subset
  complementation.
- An exact 30-label verifier independently checks the inner-product formula,
  feasible minimum intersections, and coloring.

Best-guess completion toward a full resolution: **3%**. Two broad symmetric
families are now pruned, while asymmetric subsets and other group actions
remain open.
