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

- Proved a new bounded-set positive theorem: if two distinct points are both
  at the diameter from every other point, then the set has a five-partition
  of strictly smaller diameter. The two reference points need not themselves
  form a diameter pair.
- After normalizing the common diameter-neighbors of any two distinct points,
  they are unit vectors in R^3 with all mutual inner products at least 1/3.
  Thus every vertex pair, adjacent or not, has a three-colorable common
  neighborhood; in particular no two vertices can both be complete to a
  four-chromatic subgraph. More generally, every compact unit-vector set in
  R^3 with positive minimum inner product c admits a uniform three-partition
  above c.
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
dimension-reducing common-neighborhood theorem.

## 2026-08-01T16:59:51-07:00 — Full golden audit and Mycielski tower screen

- Exhausted every possible diameter threshold for every subset of the 120
  exact golden vectors. Five of the seven nonantipodal product levels have
  explicit full-relation five-colorings.
- At product zero, exact Bron--Kerbosch enumeration found 30,000 maximal
  admissible subsets (1,200 of size 17 and 28,800 of size 20); their threshold
  graphs are all three- or four-chromatic. At product eight, all 5,160 maximal
  admissible subsets (sizes seven and eight) are likewise at most
  four-chromatic. Exact clique-list hashes and complete DSATUR checks make the
  elimination reproducible.
- This closes all orientation, deletion, and alternative-diameter-level
  variants inside the 120-vector family, not only the previously studied
  antipodal transversals.
- Proved that the natural 47-vertex six-critical candidate M^3(C5) cannot be
  the exact diameter graph of points in R^4. A rank-five original--shadow
  slack minor forces the 23 top shadows to span a four-polytope. Their graph
  neighborhoods force exactly 23 facets, 62 polygonal ridges, and 62 edges.
  Every facet halfspace has positive constant term, which would make the
  finite polytope contain an unbounded ray.
- The Mycielski proof uses strict inequalities for graph nonedges. It does not
  rule out a diameter graph properly containing M^3(C5), so weak
  subgraph-realization remains open and is not being overstated.
- Derived a new 600-point exact orbit directly, without a catalogue, as the
  centroids of all 600 tetrahedral cliques in the positive golden relation.
  It has 30 nonantipodal inner-product levels; constrained all-threshold
  screening is now the strongest active negative route.

Best-guess completion toward a full resolution: **9%**. Two major exact
candidate families are now comprehensively screened, while the derived
600-point orbit and weak Mycielski realization remain live.

## 2026-08-01T17:04:40-07:00 — Optimized high-radius theorem

- Strengthened the positive near-Jung theorem from defect 1/100000 to the
  clean rational defect 1/728. Thus
  R^2 > (2/5 - 1/728) D^2 implies a five-partition of uniformly smaller
  diameter for every bounded set in R^4.
- Optimizing the full weighted Jung defect gives the sharp edge budget
  T <= 25 delta/(1-15 delta). The pulled affine metric then has the sharp
  asymmetric spectral interval -T I <= M-I <= (3/5) T I.
- Reworked the Voronoi pullback with separate lower and upper metric errors
  and optimized the anchor-ray center. At the rational endpoint, the exact
  squared radical comparison has positive margin
  186180822731/6547648278778880.
- Identified the exact limitation of this scalar spectral relaxation. Its
  optimized envelope crosses one at the unique algebraic defect
  delta_aff = 0.0013742502821037648302... in (1/728,1/727), certified by
  a degree-ten resultant and rational Sturm calculation. An anisotropic
  matrix analysis is required to go farther by this route.
- Hostile review caught the false intermediate comparison
  2/727 < 1/400. It was repaired with 2/727 < 9/1600, which still gives
  every contact weight above 1/8; all dependent monotonicity and admissibility
  inequalities were then re-audited and added to the exact verifier.

Best-guess completion toward a full resolution: **10%**. The certified high
band is substantially wider and its present method barrier is understood,
but it still leaves most of the circumradius interval above the low-radius
theorem unresolved.

## 2026-08-01T17:08:20-07:00 — Arbitrary-pair common-neighborhood theorem

- Removed an unnecessary hypothesis from the universal-edge argument. For
  any two distinct points at separation dD, their common diameter-neighbors
  normalize to unit vectors in R^3 with threshold
  (2-d^2)/(4-d^2) >= 1/3; the acute spherical lemma applies unchanged.
- Consequently every pair of vertices in a finite four-dimensional diameter
  graph, adjacent or not, has a three-colorable common neighborhood. No two
  vertices can both be complete to a four-chromatic subgraph.
- If two points are at the diameter from every remaining point, those common
  neighbors take three parts and the two reference points take singleton
  parts. This bounded-set five-partition does not require the reference pair
  itself to be diametral.

Best-guess completion toward a full resolution remains **10%**. The stronger
local rule materially prunes graph candidates but does not yet color a
general diameter graph.

## 2026-08-01T17:16:15-07:00 — Exact 600-point dual-orbit elimination

- Reconstructed the derived 600-point golden orbit exactly as the distinct
  scaled centroids of all tetrahedral cliques in the positive golden
  relation. Every point has squared norm 112+48 sqrt(5), and the complete
  pair-product spectrum has 30 levels.
- Exhausted every possible diameter threshold for every subset of this
  orbit. At five low thresholds, explicit full-relation five-colorings
  eliminate all subsets.
- At each of the other 25 thresholds, an exact transitivity reduction and a
  complete compatible-core recursion prove that no admissible induced graph
  has minimum degree five. Every such graph is therefore 4-degenerate and
  five-colorable. The hardest threshold required 16,176 initial neighbor
  seeds and 19,803 exact recursive states.
- The standard-library verifier rebuilds the roots, 600 tetrahedra, centroid
  coordinates, reflection action, all product and compatibility relations,
  frozen colorings, and all core searches in about four seconds. This closes
  the entire single-orbit family, while mixed golden orbits remain open.

Best-guess completion toward a full resolution: **11%**. The largest exact
single-orbit search has been closed completely, but no counterexample or
universal partition theorem is yet known.

## 2026-08-01T17:32:05-07:00 — Rank-four vector five-coloring obstruction

- Proved a new graph-first necessary condition: every finite diameter
  subgraph in R^4 has a rank-at-most-four unit Gram representation with edge
  entries at most -1/4. More generally, every finite diameter subgraph in
  R^d has a rank-d vector (d+1)-coloring with edge entries at most -1/d.
- The proof takes the minimum enclosing cap of the diameter-neighbor
  directions at each vertex. Exact active-set geometry gives squared cap
  height at least 5/8; opposite directions along an edge then force the two
  cap centers to have product at most -1/4. An independent hostile audit
  confirmed the empty-neighborhood and equality cases.
- Derived the exact regular-graph screen k <= -4 tau, where tau is the least
  adjacency eigenvalue. Applied it to the 60-vertex unsigned golden graph:
  its degree 20 and least eigenvalue -4 would require 20 <= 16. Hence that
  abstract six-chromatic graph cannot occur even as a diameter subgraph,
  giving a coordinate-independent explanation for the failed orientation
  route.
- Added a dependency-free exact checker for the sharp constants and the
  previously certified golden spectral identity. Future graph-first searches
  now reject candidates at the vector relaxation before attempting a
  rank-four Euclidean realization.

Best-guess completion toward a full resolution: **12%**. This sharply prunes
the negative route and exposes the needed chromatic-versus-vector-coloring
gap, but remains a relaxation rather than an ordinary five-coloring theorem.

## 2026-08-01T17:47:10-07:00 — Weak Mycielski realization closed globally

- Proved that the 47-vertex six-critical graph M^3(C5) cannot occur even as a
  non-induced diameter subgraph in R^4. This removes the strict-nonedge caveat
  from the earlier slack-polytope proof: arbitrary accidental diameter edges
  cannot rescue the candidate.
- Defined the probability-pair model of Hom(K2,G). Any unit-vector assignment
  with negative products on graph edges gives an explicit equivariant map
  Hom(K2,G) -> S^(r-1) by normalizing the difference of the two weighted
  shore sums; complete cross adjacency proves that this difference never
  vanishes.
- Built an explicit antipodal decagon S^1 -> Hom(K2,C5) and a three-stage
  equivariant suspension map Sigma Hom(K2,G) -> Hom(K2,M(G)). Three
  iterations give S^4 -> Hom(K2,M^3(C5)). The rank-four center-vector theorem
  would give Hom(K2,M^3(C5)) -> S^3, contradicting the mod-two projective
  cohomology form of Borsuk--Ulam.
- Added a standard-library checker for the decagon, antipodal action, and all
  Mycielski interpolation adjacencies. An independent exact slack census also
  excludes 804 of the 845 one-edge supergraphs before the global topological
  argument disposes of every augmentation at once.

Best-guess completion toward a full resolution: **14%**. The strongest
triangle-free graph-first candidate and all of its accidental-edge variants
are now eliminated, and the Hom-complex obstruction is reusable, but no
surviving six-chromatic realization or universal partition is yet known.

## 2026-08-01T17:56:47-07:00 — Mixed golden radial unions eliminated

- Derived the complete 15-level cross-product table between the 120 golden
  roots and the 600 derived tetrahedron centroids. The positive extreme
  28+12 sqrt(5) is exactly root--tetrahedron incidence, with bidegrees 20
  and 4, and the dual squared norm is four times this extreme.
- Found exact negative switching cycles in the root, dual, and cross
  maximum-absolute signed graphs, of lengths 5, 15, and 10. Consequently
  every one of the 2^360 independent projective orientation choices has the
  same three minimum products; no enumeration of switchings is required.
- Computed the exact radial upper envelopes for all four combinations of
  full antipodal or projective occupancy. Every exposed regime and tie graph
  is five-colorable; the full/full family is in fact two-colorable. The
  checker verifies exact quadratic tie equations, quartic rational norm
  polynomials, isolating intervals, and frozen transition colorings.
- This closes every full/projective radial union of the two orbits at every
  positive scale. Arbitrary vertex-deleted mixed subsets can expose lower
  product levels and remain outside the theorem.

Best-guess completion toward a full resolution: **15%**. All natural
symmetry-preserving unions of the two largest exact golden orbits are now
closed, while asymmetric deletions and graph-first deformations remain live.

## 2026-08-01T18:01:38-07:00 — Universal-vertex cap regimes

- Reduced a compact diameter set with one universal diameter vertex to an
  acute compact set X on S^3 with all pair products at least 1/2. Its closest
  cap has squared height h^2 >= 5/8.
- Proved a uniform four-partition at the sharp endpoint h^2=5/8 using the
  rigid equal-weight four-contact Gram matrix and adaptive safe-coordinate
  regions. Hausdorff hyperspace compactness upgrades this to one universal,
  though nonexplicit, interval 5/8 <= h^2 < 5/8+epsilon.
- Proved a second uniform regime h^2 > (1+sqrt(3))/4 using the exact diameter
  -1/sqrt(3) of a tetrahedral spherical Voronoi cell. A complete polynomial
  factorization certifies the cell constant and its equality cases.
- Derived weighted-polar coordinates for arbitrary four-contact supports.
  When the transverse support is regular, nearest-contact cells work across
  the entire intervening cap range, with explicit margin
  (H-1/2)(3/2-2H)/(1-H).
- Constructed an exact rational distorted support at H=17/25 and an
  algebraic threshold pair lying strictly in one nearest-contact cell. This
  rigorously falsifies the simplest adaptive extension and isolates the
  remaining target as a compact nonregular middle band.
- Expanded the dependency-free exact verifier to check all cap constants,
  polar-cell vertices, radial signs, rational support weights and scores,
  algebraic root intervals, and the strict distorted-support product bound.

Best-guess completion toward a full resolution: **17%**. A universal
diameter vertex is now handled in several robust regimes and all regular
four-contact cases, but a nonregular middle-cap theorem is still missing.
