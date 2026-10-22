# Independent audit of equilateral polygon locking

## Verdict and scope

Accept the exact frozen author packet as a correct, explicitly limited stalled partial investigation of problem 2731, KP-1.72, rank 906. The mathematical conclusions reviewed here do not solve the open problem. The three approaches and 3/5 stopping status are accurately described. No mathematical correction is required, no corrected derivative was created, and the original author files and archive were preserved.

The accepted archive is 16,268 bytes with SHA-256 `f213feeb58b23c4c98aafb865c5965751386aba27fc64981a9aa92bebf04eca2`. Its external manifest is 1,638 bytes with SHA-256 `7b71bde678bba64192812f49058f8cc91d46fa3bfd36f725bbcda86a1f7be4d8`. Acceptance applies only to those bytes and the nine verified members, not to an unspecified later working copy. `EXACT_ACCEPTANCE.json` gives the machine-readable decision. This is an independent AI-assisted audit, not journal peer review or a novelty certification.

## Exact mathematical problem

The packet correctly studies a single closed polygonal embedding of a circle in ambient three-dimensional Euclidean space, with a fixed cyclic vertex list and all individual edge lengths equal to one. The initial ordinary knot type is the unknot. Throughout an allowed motion, nonadjacent closed edges remain disjoint and adjacent edges meet only at the designated shared vertex. Collinear forward subdivision vertices are allowed; zero edges and backtracking overlaps are excluded. The target is an embedded planar polygon. Translation can be removed by fixing the initial vertex, without restricting a physical motion.

This differs from open chains, unequal-length locked hexagons, fixed-angle linkages, thick ropes, crossings with imposed local rigidity, variable-length polygonal isotopies, and diagrammatic re-embedding. None of those models is silently used as an answer. The nearby thick-rope question in K3 is Problem 1.71, not the present Problem 1.72.

I checked the actual 436-page K3 author PDF, including the title/status page and printed pages 67–68, and visually inspected page 67. The statement in the complete pinned problem record matches after joining word-internal line-end hyphenation and collapsing whitespace. The normalized text has SHA-256 `6178d58013fe62b1c5741f52872306d568dc81f8dc1237a6415f6a1ebd410d45`. The problem attribution and scribe also agree. The inherited AIM URL is a four-page workshop summary; it is not the primary statement document. The author packet already corrects that citation. Source PDFs and their text are not part of this audit package.

Primary statement: [Baykur, Kirby, and Ruberman, K3 author version](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).

## Continuum audit of the mathematical claims

### Subdivision family

Proposition 1 is valid over the entire interval, not merely at the four checker samples. The rational functions satisfy c²+s²=1 and c≥3/5. The four slant edge vectors consequently have norm one; the two y-directed edges have norm one as well. The two pairs in y=0 and y=1 cannot intersect each other. Within either pair, strict progression through x=0,c,2c precludes overlap and leaves only the shared endpoint. The y-directed edges at the two extreme x-coordinates meet those pairs only at their prescribed endpoints. Thus the family is embedded for every parameter, including r=0 when the long rectangle sides are subdivided by collinear forward joints.

Both coarse chords have length 2c, decreasing from 2 to 6/5. This is a genuine lost constraint under free-joint subdivision. Starting at a planar rectangle also proves ordinary unknot type throughout. It neither constructs a locked polygon nor proves that subdividing an arbitrary locked polygon always unlocks it. The packet explicitly makes that distinction.

### Restricted uniform flattening

Proposition 2 is valid. Each unit spatial edge has horizontal squared length 1−h² and vertical squared length h². Scaling height by a changes every squared length to the same positive value L(a)²=1−h²+a²h². Division by L(a) therefore preserves every individual unit edge. Since h<1, the denominator never vanishes, including at a=0. The motion starts at the original polygon and ends planar.

Embeddedness follows from the injectivity of the projected polygon, considered as a map from the cyclic polygonal domain: a coincident pair of spatial points would give a coincident pair of projected points. Positive common scaling does not change that argument. Closure is automatic because all vertices are transformed by the same linear map and scalar. The case h=0 is a harmless constant planar motion. For h>0, closure forces equally many positive and negative height increments, but that is a consequence of the hypotheses, not a missing hypothesis.

The claimed obstruction to this exact formula is also correct. At a<1, equality of the flattened edge lengths is equivalent to equality of all squared height increments. A single scalar cannot repair unequal values. The supplied rotation is orthogonal with determinant one. The six projected vertices form a strictly convex polygon, as can be checked by all 24 strict left-half-plane inequalities. The height increments have squared magnitudes 1/9 and 4/9; at a=1/2 the two squared edge lengths are respectively 11/12 and 2/3. Thus the counterexample defeats the proposed common-rescaling formula while remaining an ordinary unknot.

An important framing qualification is already present: this is an elementary restricted formula, not new progress on the whole simple-projection class. The more general simple-projection convexification theorem was established by Calvo, Krizanc, Morin, Soss, and Toussaint in 2001. The packet's “unresolved step” should be read as the limitation of this attempted route toward the full problem, not an assertion that the simple-projection case remains open. The author text acknowledges the known literature and disclaims novelty, so this does not require a correction.

Bibliographic supplement: [Convexifying polygons with simple projections](https://doi.org/10.1016/S0020-0190(01)00150-8), Information Processing Letters 80(2), 81–86 (2001).

### Smooth semialgebraic configuration space

Proposition 3 has the correct dimension for based polygons: rotations have not been quotiented out. There are 3(n−1) free coordinates and n independent unit-edge equations. A linear relation among their gradients gives λ(i−1)e(i−1)=λ(i)e(i) at every free vertex, hence a common vector for all n products. If that vector were nonzero, every edge would be parallel to it. A closed polygonal circle cannot be embedded in a line. If it is zero, nonzero edge lengths force every coefficient to be zero. Thus the derivative has rank n and the local dimension is 2n−3. Forward collinearity of some consecutive edges does not invalidate this argument.

The edge-parameter formulas correctly encode all forbidden intersections, including the cyclic pair of edges 0 and n−1 and the all-adjacent n=3 case. Eliminating the real parameters gives a semialgebraic embeddedness condition. The finite intersection conditions are exact, rather than a generic-position approximation. The local stability argument below proves openness even at allowed forward-collinear vertices. Planarity of based vertices is exactly rank at most two, so vanishing of all 3-by-3 determinants is appropriate, including the vacuous n=3 instance.

Finite connected-component decomposition and path connectivity of semialgebraic components are standard real-algebraic facts. For this finite polygonal family, an embedded path preserves ordinary knot type; polygonal isotopy extension, or the local embedding neighborhoods together with a finite subdivision of the parameter interval, justifies that step. A component meets the planar locus exactly when each of its configurations has a fixed-edge embedded motion to a planar polygon. A component can therefore consist of stuck unknots only if its knot type is trivial and it misses the planar locus.

### Effective fixed n reduction and stability

The decision reduction is valid in principle. All initial formulas have rational coefficients. Component descriptions, real-algebraic sample points, and intersection tests with the planar locus are effective. It is sufficient to determine whether a remaining component's sample is an ordinary unknot, rather than classify all possible knot types. A close rational replacement is legitimate for that test even though it need not retain unit edge lengths.

Here is an explicit check of the stability constants. At every interpolation time, perturbing each vertex by less than ε moves each point on its corresponding edge by less than ε, so nonadjacent edge distances stay greater than δ−2ε. Each edge vector moves by less than 2ε and has positive length when ε<1/4. For an original unit vector e and a perturbed nonzero vector w,

\[
\left\|w/\|w\|-e\right\|\leq |1-\|w\||+\|w-e\|\leq 2\|w-e\|<4\epsilon.
\]

Thus the sum of consecutive unit directions changes by less than 8ε. The original sum has norm at least μ>0; the chosen ε<μ/16 leaves a positive margin. Consecutive segments with a common endpoint can overlap only when their oriented edge directions are exactly opposite, which this excludes. These two tests cover all possible collisions. The δ=1 convention for a triangle is valid because there are no nonadjacent pairs to control. Distances between segments and direction margins for real-algebraic input can be bounded effectively using real algebraic arithmetic and quantifier elimination. Rational approximation therefore yields the same knot type, and standard polygonal unknot recognition applies.

The cited [Basu–Pollack–Roy component algorithm](https://arxiv.org/abs/math/0603248) supports effective component descriptions. [Hass–Lagarias–Pippenger](https://arxiv.org/abs/math/9807016) supports decidability of polygonal unknot recognition. Neither result supplies the missing all-n bound. No CAD, component computation, sample knot recognition, or global search was actually performed in the packet or this audit. Enumeration over n is only a semidecision procedure for finding a counterexample, and its failure to halt cannot prove universal unlocking.

## Literature boundary checks

Calvo's author preprint explicitly defines the unit-edge space separately from the variable-edge space. PDF pages 3–4, including a visual inspection of page 4, support connectedness through five edges and the single unit-hexagon unknot component. A regular planar unit hexagon supplies a planar representative in that component. Consequently a counterexample, if one exists, needs at least seven edges. The preprint's variable-edge heptagon classification cannot be reused as a unit-edge heptagon theorem. [Geometric knot spaces and polygonal isotopy](https://arxiv.org/abs/math/9904037).

The two newer nearby titles use different deformation models. Diamantis imposes rigidity on designated diagram crossings. Cantarella–Schumacher–Shonkwiler's re-embedding procedure changes geometric layouts to simplify diagrams and does not retain each original unit edge. I inspected the latter's pinned version 2 abstract and re-embedding section. Neither is a solution of the present fixed-edge problem. [Diamantis](https://arxiv.org/abs/2602.18129), [Cantarella–Schumacher–Shonkwiler](https://arxiv.org/abs/2607.28772).

Fresh bounded searches on 2026-10-06 did not locate a general resolution. This is not a proof of absence or novelty. The author's historical repository searches and unsuccessful catalog HTTP requests remain historical provenance claims; this audit does not pretend to reconstruct every past response. The principal mathematical source, exact target identity, corpus pins, and relevant published distinctions were independently checked.

## Computational and provenance audit

All three full corpus streams were read and hashed independently, with the exact byte counts and digests recorded in `REPLAY_RESULTS.json`. The complete exact-ID problem record and its exact-key inherited report were read; the report is empty. Serializing the entire pair using Python's default `json.dumps(..., sort_keys=True)` produces `eef75cf825610172fc68ed1c073143bb6d65a5ab572b5756affadd88bdd6cc6d`. The unnormalized statement hash is `9f0678048e8c8bc1ea0ff193d5821eeb6d3ba72c4851de391190f0fe2a2f337d`. Both agree with the catalog. There was no substantive inherited attempt hidden in a truncated report.

The ZIP contains exactly nine safe relative members under its single expected prefix. Every member agrees with the external manifest, and its internal manifest binds the other eight author files. All four claimed PDF byte counts and hashes also match. Source-document page counts and statement normalization were recomputed from the actual PDFs using Poppler.

Fresh extraction to a temporary directory with spaces, with an unrelated working directory, reproduced `EXACT_CHECKS.json` byte-for-byte under normal Python and Python `-O`. Both modes rejected unexpected arguments. Six intentional checker mutations, affecting the circle bound, flattening identity, rotation, convex orientation, mixed-height length, and unit-edge condition, were rejected in both modes. Two exact-input pin mutations were rejected. Four additional malformed polygons were rejected.

An independently written cross-product segment-intersection oracle agreed with the author's coordinate-pivot routine on 61,776 unordered pairs of nondegenerate segments with endpoints in the 3-by-3-by-3 integer grid. A further 4,000 endpoint-reversal and segment-order symmetry checks passed. These are stronger finite regression checks, not a proof for arbitrary coordinates. The independent harness itself also runs under `-O`, uses explicit exceptions, and was checked for consistent output. The analytical review above, rather than this finite coverage, supports the continuum propositions.

## Safe publication boundary and remaining gap

This audit package contains authored analysis, verification code, hashes, byte counts, results, and public citations only. It contains no corpus records, third-party source documents, source-text extracts, private coordination files, or source-page images. The K3 preliminary source itself prohibits reposting without permission; it has not been redistributed here.

The accepted outcome remains unsolved, stalled partial, 3/5 approaches. There is no equilateral locked example, no universal fixed-edge unlocking theorem, and no executed component decomposition. Public presentation should retain all three limitations and the lack of novelty claim.
