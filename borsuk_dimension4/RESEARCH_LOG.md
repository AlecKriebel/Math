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

## 2026-08-01T16:11:35-07:00 — Graph-first and positive-route checkpoint

- Proved three reusable exact diameter-realization obstructions:
  `K_6-e` cannot occur; after a universal `K_2` the remainder has no `C_4`;
  and two completely cross-joined blocks cannot each contain two diameter
  edges. The last statement follows from orthogonal affine spans and an exact
  circle-radius bound.
- Applied these screens to multiple explicit six-chromatic joins, Mycielski
  graphs, a Hajós graph, and the 28-vertex disjoint-pair graph on two-subsets
  of an eight-element set. All were ruled out globally, not merely within a
  symmetric realization ansatz. Exact diagnostics reconstruct the graphs and
  their small obstruction subgraphs.
- Established the correct compactness target for a universal positive proof:
  exact diameter-graph coloring alone is insufficient, while a universal
  positive theorem would automatically imply one dimension-wide contraction
  factor below one and is equivalent to a uniform finite near-diameter
  theorem.
- Proved five-partition theorems for convex hulls whose actual diameter
  endpoints have unique outward normals, for circumradius
  `R^2 < 3 D^2 / 10`, and for a nonzero (currently nonexplicit) band below the
  Jung endpoint `R^2 = 2 D^2 / 5`. Exact examples expose the failure of the
  naive limiting, fan-boundary, and arbitrary-normal extensions.
- Independently reran all exact Route B diagnostics and the short Route A
  envelope/transversal checks successfully.

Best-guess completion toward a full resolution: **5%**. The remaining positive
case includes a middle circumradius shell with nonsmooth diameter endpoints;
the remaining negative case requires a K5-free graph surviving the new rank
and cross-block screens.

## 2026-08-01T16:11:35-07:00 — Symmetric-orbit checkpoint

- Proved a conceptual five-coloring theorem for every finite
  `A_5`-invariant set in the four-dimensional sum-zero representation. The
  color is the first cyclic minimum-to-ascent coordinate, and an exact weak
  order verifier checks all ordinary and parity-forced rearrangement cases.
- Exhaustively generated 133,303 distinct exact signed-permutation point
  orbits from all at-most-two-generated signed-permutation subgroups and
  primitive canonical integer seeds of height at most six. Their exact
  chromatic distribution was 161 one-color, 130,418 two-color, 2,584
  three-color, and 140 four-color; none required five.
- Checked 1,560,423 aligned radial two-orbit pairs, including 5,017 exact
  triple upper-envelope ties, and 1,805 fully tied three-orbit events at the
  next bounded level. Every surviving graph was at most four-colorable.
- Eliminated all 4,096 transversals of the signed two-support roots and, by a
  signed-cycle plus explicit projective coloring argument over
  `Q(sqrt(5))`, all `2^60` transversals of a 120-vector golden-ratio family.
- Reran all seven exact verifier modes, including the two approximately
  22-second large enumerations, with the reported counts reproduced.

Best-guess completion toward a full resolution: **6%**. Full simplex symmetry,
broad bounded signed orbits, and whole antipodal transversals are now strongly
disfavored. Partially symmetry-broken subsets and noncanonical multi-orbit
alignments remain live.

## 2026-08-01T16:26:00-07:00 — Explicit high-circumradius band

- Quantified the compactness-only near-Jung argument: if the minimum enclosing
  radius satisfies
  `R^2 > (2/5 - 1/100000) D^2`, five nearest-contact-anchor cells all have
  diameter strictly below `D`.
- The Jung defect forces five positive contact weights and all ten normalized
  squared anchor distances above `999/1000`. An entrywise Gram estimate then
  gives a linear identification with the regular simplex having squared-norm
  distortion below `1/125`.
- Pulled the actual Voronoi cells back through that identification and enclosed
  each in an explicit ball. The resulting certified contraction is
  `Gamma^2 = (504/125)(12997/15500 - (4/5)sqrt(377/620)) < 1`.
- An independent rational-arithmetic verifier checks every endpoint constant;
  the decisive squared radical comparison has positive margin
  `154363852991/3814209000000`.
- A separate hostile audit found no hidden affine-independence, strictness,
  compactness, or Voronoi tie-breaking assumption.

Best-guess completion toward a full resolution: **7%**. The positive route now
has exact low- and high-circumradius regimes, but a substantial middle shell
and nonsmooth diameter-endpoint configurations remain unresolved.

## 2026-08-01T16:41:49-07:00 — Universal-edge theorem and golden lead closed

- Proved a new bounded-set positive theorem: if a diameter pair is universal
  (both endpoints are at the diameter from every other point), then the set
  has a five-partition of strictly smaller diameter.
- After normalizing the common neighbors of any diameter edge, they are unit
  vectors in R^3 with all mutual inner products at least 1/3. Thus every edge
  has a three-colorable common neighborhood; in particular no diameter
  subgraph can contain K2 join H with chi(H) at least four. More generally,
  every compact unit-vector set in R^3 with positive minimum inner product c
  admits a uniform three-partition above c.
- The proof encloses the spherical set in a closest cap and colors three
  half-open longitude sectors. At the sharp cap bound, equality forces a
  regular support triangle; its opposite support point excludes every
  dangerous sector-boundary limit. Exact arithmetic and an independent
  hostile audit verified the constants and strictness.
- Decisively eliminated the strongest golden-symmetry negative lead. On all
  120 oriented vectors, the exact dot = -8 graph is 20-regular with 1,200
  edges and has an explicit five-coloring with five classes of size 24.
  Every switching of the 60 antipodal lines and every admissible deletion is
  an induced subgraph and inherits that coloring.
- Independently certified why the unsigned lead looked promising: its
  60-vertex absolute-8 graph has exact spectrum
  {20^1, 5^16, 0^18, (-4)^25}, clique number four, and chromatic number
  exactly six. The obstruction is therefore genuinely in the edge signs,
  not an earlier chromatic miscalculation.

Best-guess completion toward a full resolution: **8%**. The negative search
lost its strongest exact candidate, while the positive route gained a
dimension-reducing theorem that may generalize to nonuniversal diameter
edges.
