# Independent mathematical, source, and executable audit

Target: 3900016 / AMR-038-0016, distinct triangle areas in convex-polygon triangulations. Audit date: 8 October 2026 UTC.

## Verdict and exact scope

The report's mathematical partial results are accepted at the stated scope: a polygon has distinct extreme vertices; its triangulations use only those vertices and noncrossing diagonals. Acceptance is limited to the displayed elementary guarantees, small cases, and lattice arithmetic. The general optimum t(n), sharp bounded-lattice optimum t_L(n,m), and existence of unavoidable triple equal-area repetition are not resolved. No novelty, best-known bound, or global current-openness certification is given.

The final execution receipt and subject manifest bind this verdict to the exact frozen eight-file author payload. The original author payload is preserved. No mathematical correction patch is required. Its historical pending-audit field is superseded by the separate acceptance record, not silently rewritten.

## 1. Primary-source and convention audit

The [original question](https://ics.uci.edu/~eppstein/junkyard/tri-diff-areas.html) identifies Eddie Grove and the date 6 March 1990; David Eppstein is the host. It explicitly describes triangulation by n−3 mutually noncrossing chords into n−2 triangles. This excludes insertion of Steiner vertices. Its lattice interest is in coplanar integer points in a three-dimensional cube and normal directions admitting bounded integer coordinates. It is not merely an unbounded planar-lattice problem.

The report fixes an axis-aligned cube [0,m]^3, side-length parameter m, and a primitive normal with infinity norm at most m. Dividing an integer normal by its gcd preserves its direction and cannot increase this bound. The side-length versus number-of-grid-points distinction is disclosed. The report defines t_L only for nonempty classes and correctly observes that allowing arbitrary n prevents an m-only guarantee greater than one.

The source does not separately define strict versus weak convexity. The report explicitly uses extreme vertices and excludes collinear listed boundary points. The accepted results do not claim the alternative weak-boundary-point convention. This is a disclosed domain convention, not an inferred theorem covering degeneracies.

The [Geometry Junkyard open-problem index](https://ics.uci.edu/~eppstein/junkyard/open.html) still links the question. An old surviving index entry is not evidence that no later solution exists. The audit repeated focused searches by title, Grove, and distinct/equal-area triangulation terms. They produced the original posting and adjacent area literature; no full resolution was verified in this bounded pass.

The opening abstract and introduction of Dumitrescu, Sharir, and Tóth's [Extremal problems on triangle areas in two and three dimensions](https://adriandumitrescu.org/area.pdf), dated 1 October 2007, were independently inspected in the web-parsed PDF. Its spanned-triangle questions differ from coexistence of triangles in a single noncrossing triangulation. This is a scope comparison, not verification of its full proofs. The author packet accurately declines to claim a verified local PDF hash.

The abstract and history of Jin, Zhu, and Luo's [A technique for solving the polygon inclusion problems, v7](https://arxiv.org/abs/1707.04071v7) confirm the 21 April 2024 revision and individual extremal-triangle algorithmic scope. The report imports no theorem from it. An additional abstract check of [Maximum-Area Triangle in a Convex Polygon, Revisited](https://arxiv.org/abs/1705.11035) reinforces the need not to assume a particular maximum-triangle algorithm is correct; the finite checker simply enumerates triples and needs none of that literature.

All cited-source descriptions here are paraphrases. No source text or dataset contents are included. The author's public-source metadata was checked against the retained public-source bytes. Corpus metadata is acknowledged only as the supplied bounded identity check; this independent audit does not claim a new full-corpus or whole-repository no-prior-attempt search.

## 2. Mathematical proof audit

### Definitions and affine invariance

Every valid triangulation contains n−2 positive-area triangles. Thus D(P) belongs to a finite nonempty set of integers, and taking the minimum of its possible values is legitimate without a compactness argument. A nonsingular planar affine map multiplies absolute areas by one common positive determinant factor, preserving every equality and the triangulation combinatorics.

### Maximum-triangle cap lemma

With a maximum vertex triangle normalized to A=(0,0), B=(1,0), C=(0,1), comparison against ABX, ACX, and BCX gives |y|≤1, |x|≤1, and |1−x−y|≤1 for every polygon vertex and hence every point of the polygon. Below AB these imply 0≤−y≤x≤1; the cap is contained in triangle ABE with E=(1,−1). Its area cannot exceed that of ABC.

If a closed convex subset of ABE has the same area as ABE, it must equal ABE. Indeed a proper closed convex subset can be strictly separated from at least one omitted point, omitting a positive-area portion of the triangle. Equality therefore places E in the polygon. Since E has y<0, it is not a new vertex created by clipping at y=0: extremality of E in the cap implies extremality in the original polygon. Equivalently, a small segment through E witnessing nonextremality would remain below AB and contradict cap extremality.

Using E as a polygon vertex now yields |x+y|≤1 and |1−x|≤1. Together with the earlier constraints these give 0≤x≤1 and 0≤x+y≤1. That parallelogram has precisely A,E,B,C as its corners. Convexity gives containment in both directions, so the polygon has exactly four extreme vertices. This proves strictness for n≥5 and also identifies why the square/parallelogram case must be excluded. The other caps follow by permuting the triangle vertices.

### Logarithmic recursion

The three open boundary arcs contain a total of n−3 additional vertices. One resulting cap therefore has at least ceil((n−3)/3)+2=ceil((n+3)/3) vertices. A recursion inside that cap is compatible with the selected triangle and with arbitrary triangulations of the other caps. Every recursively selected area is strictly smaller than the new top area. Monotonicity and induction justify G(n), including its n=3,4 base cases. The threshold recurrence N_j=3N_(j−1)−3 with N_1=4 solves to (5·3^(j−1)+3)/2, exactly as reported. No control of collisions between different caps is claimed.

### Local flips and equal fans

A third untouched occurrence of area a ensures that flipping an adjacent equal pair cannot remove a from the old palette. Every other old area remains, so a newly appearing value increases diversity. Without a new value, or without adjacency, the argument stops. In the normalized quadrilateral the new doubled areas are h(x+y) and h(2−x−y), so their equality is equivalent to x+y=1, precisely coincidence of the diagonal midpoints. The parallelogram characterization is valid. The rational rotation fixture has positive exact orientation and equal origin-fan areas; it only obstructs a prescribed fan, not all triangulations.

### Compatible rainbow packing

Each inserted triangle lies in one convex residual face, so its sides do not cross any existing subdivision edge. Subdividing retains its nondegenerate caps. All face vertices remain original extreme vertices. The selected k triangles are distinct subdivision faces with distinct areas, and the subdivision can be completed, proving termination at k≤n−2.

With d internal edges and r residual faces, the connected disk subdivision gives k+r=d+1 and d≤3k. Boundary/interior edge incidences give 3k+Σs_i=n+2d. Eliminating d yields n=k+2+Σ(s_i−2). These formulas also cover r=0.

At termination every vertex triangle in a residual face has an area among the selected k. A fixed boundary edge of that face sees all other vertices on one side. A specified positive area places the third vertex on one parallel line; a line contains at most two extreme vertices. Therefore s_i−2≤2k. Combining this with r≤2k+1 gives n≤4k²+3k+2. Arbitrarily completing the faces preserves the selected triangles. If the completed triangulation has more than k distinct areas, the same bound remains valid for that larger count.

Solving the increasing quadratic on nonnegative k gives ceil((sqrt(16n−23)−3)/8). It is at least one for every n≥3. The proof is a universal square-root lower bound, not an extremal characterization. The independent checker uses a different minimum-new-area selection order and verifies noncrossing edges, both incidence identities, residual palette maximality, and completion.

### Three-dimensional lattice formulas

A cross product of two integer edge vectors is an integer vector parallel to the plane normal. For primitive u, Bézout coefficients show that any real scalar λ with λu integral is integral: λ=Σb_j(λu_j). Thus the cross product equals ku, k∈Z\{0}, and area=|k|·||u||₂/2. No claim that all integers k are attained is made; a chosen vertex sublattice may produce only multiples of two or another integer.

Deleting coordinate j with u_j≠0 is injective on the plane's direction space and hence on the affine plane. Its signed determinant magnitude is |ku_j|, so all areas scale by the same positive factor |u_j|/||u||₂. This preserves convexity, triangulations, and area comparisons. The projected polygon remains an integer polygon with inherited cube bounds and congruence restrictions.

For U=max|u_j|, project through a coordinate achieving U. A triangle in a square of side m has doubled area at most m²: successively maximizing the positive or negative determinant in each coordinate reduces to square corners. Hence |k|≤floor(m²/U). The entire projected polygon has area at most m², giving S≤floor(2m²/U). A triangulation expresses S as a sum of n−2 positive integer units. For q distinct units, the least possible sum of their first occurrences is 1+…+q; other triangles contribute at least one. This proves S≥(n−2)+q(q−1)/2. These are individual-polygon spectrum and mass upper constraints, not a sharp universal lower bound for t_L.

### Exact small cases and upper bounds

The triangle and unit-square cases give t(3)=t(4)=1. The cap result gives t(5),t(6)≥2. For P5 the ear doubled areas are exactly (1,1,2,2,1); the two area-two ears are adjacent and cannot coexist. The five triangulations have doubled-area profiles (1,1,3) once and (1,2,2) four times.

All twenty triples of P6 were independently checked, not inferred from an approximate regular drawing. Gap type (1,1,4) has doubled area one, type (1,2,3) has two, and type (2,2,2) has three. The fourteen triangulations have (1,1,1,3) twice and (1,1,2,2) twelve times. Therefore both witnesses have D=2. Their embeddings in z=0 lie in [0,2]^3 with primitive normal (0,0,1). The stated lattice cases for m≥1 or m≥2 follow; no claim about other feasible small lattice classes is added.

Every triangulation of a regular n-gon, n≥4, has two ears by the dual-tree leaf argument. Their common area causes a repetition among n−2 triangles, proving t(n)≤n−3. This remains intentionally weak.

The fixed-polygon area-set recurrence is exact: the triangle incident to the closing boundary edge determines the split vertex and the two independent subpolygons. Conversely the pieces glue. Exponential growth of the family is disclosed; no polynomial complexity conclusion is drawn.

## 3. Complete native-code review

The entire author check_claims.py was read, including geometric primitives, orientation/input guards, cached Catalan recursion, deduplicated ear deletion, exact spectra, threshold functions, cap recursion, packing, monotone-chain hulls, bounded suite construction, lattice cross products, mathematical tests, manifest validation, write-denial probes, and CLI/output handling.

All mathematics uses Python integers or fractions. The standard-library dependencies contain no floating-point geometry or external solver. Every required runtime guard uses explicit exceptions; AST inspection finds no assert nodes. The checker reads only its authored packet, makes no network calls, and writes only an explicitly requested external output path. Read-only probes use exclusive creation and nontruncating write-open attempts. The eight author payload files are externally bound, including the pin manifest that does not hash itself.

Native Catalan and ear-deletion generators are different recursive constructions. To strengthen independence, the audit code enumerates n−3-element diagonal subsets for n=3…7, rejects every crossing, reconstructs triangular graph faces, and checks boundary/internal incidences. For small witnesses it computes areas by the cyclic three-term determinant formula rather than the author's difference-vector formula.

The native tests exhaust a stated finite 3×3-grid-hull suite, not all polygons. Larger parabolic instances exercise only the bounded constructive mechanisms where described. The independently authored checker adds all twenty P6 triples, 36 packing runs on cyclically shifted fixtures, cap checks including the square equality, threshold checks through n=10,000, and five lattice embeddings. One embedding has cross product 2u, explicitly testing non-unit sublattice index; other normals include zeros, mixed signs, and unequal nonzero coordinates.

## 4. Executed controls and reproducibility

Final full stdout/stderr and exit status are retained for normal, -O, and -OO execution of the native checker, independent checker, and semantic-control harness. All run under real and effective UID 1000. Subject and audit-code directories have mode 0555 and files 0444. Actual directory-create and existing-file write-open attempts fail with permission errors; pre/post SHA-256 snapshots verify no payload mutation. These are permission-denied observations, not reliance on a claimed read-only flag or root's interpretation of mode bits.

Seven in-memory semantic mutations are separately rejected after unmodified native integrity passes: constant triangle areas, inflated G, inflated B, an omitted Catalan triangulation, erased ear generation, a corrupted normal cross-product component, and disabled orientation validation. Each fails a specified mathematical or guard diagnostic; a manifest hash failure does not mask these tests. The original checker bytes remain unchanged.

The independent checker also rejects eight false premises/results: diversity three for each small witness, nonprimitive or zero normals, weak convexity, a self-crossing polygon, use of a nonmaximum triangle in the cap proof, and a falsely strict cap bound for a square. These controls survive both optimization levels. Sensitivity to these faults is useful evidence, not a proof that every possible implementation error would be caught.

The source-free audit payload consists only of this audit, authored verification code, public-source descriptions, exact authored-file manifests, acceptance metadata, and full test receipts. It contains no copied source bodies, private correspondence, dataset content, or private coordination material. Final cryptographic bindings are recorded in ACCEPTANCE.json and the external audit manifest.

## Remaining mathematical gap

The accepted lower bounds do not supply matching extremal constructions for general n. Projected lattice arithmetic does not determine the sharp t_L(n,m). Local flips do not establish multiplicity at most two and do not produce a polygon forcing a triple repetition. Five research approaches are recorded as exhausted; this audit adds verification and corrections of scope, not a sixth discovery attempt. The appropriate outcome remains partial results, exhausted 5/5.
