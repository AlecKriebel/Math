# Independent adversarial review: Dol'nikov packet 30005804

## Verdict and scope

**PASS_SCOPED. No blocking mathematical or computational correction found in the five written turns. Original problem unresolved after the five-turn author budget.**

This passes the packet as a rigorously limited research checkpoint. It does not certify a proof or counterexample to the original conjecture, novelty, priority, exhaustive current literature status, or readiness for publication. No sixth author search, remote write, pull request, merge, or queue/status mutation was performed by this reviewer.

Reviewed in order: README, TURN_1 through TURN_5, supporting Python, certificates, state/checkpoint records, and source gate. All author claims below are assessed under their exact written hypotheses. The primary source was independently downloaded, rendered, and read at printed pages 172–174. Its four cited packet PDFs match the author's source hashes exactly.

## Frozen identity and integrity

- Repository supplied for review: `AlecKriebel/Math`
- Branch supplied for review: `math/30005804-dolnikov-wip`
- Frozen commit recorded in the supplied receipt: `08e3f30b26bb9cd7487ad7f6db8373a4e796a343`
- Research path: `problems/30005804_dolnikov`
- SHA-256 of TURN_5_MANIFEST.json: `4c77bd766217a50903162ab441416b2a3d5f003f1af6b13ca3db982d82d33b1d`

All 37 entries in that manifest match both byte length and SHA-256. Including the manifest itself gives the stated 38 checkpoint files. The local directory has a 39th file, the later TURN_5_REMOTE_RECEIPT.json, which is correctly outside the manifest it describes. All 38 Git blob hashes and sizes in that receipt were independently recomputed locally and match. The present remote ref was not newly fetched by this reviewer: these are checks of the supplied frozen bytes and receipt, not a claim about a changing branch tip. The author packet was left unchanged.

## Exact target and primary literature

The imported problem is the finite, planar, three-color problem for translates of **one fixed compact convex K**. Every cross-color pair must intersect, including boundary contacts. The conclusion asks for at most three piercing points for at least one color. Rotations, homothets, varying bodies, and the preceding projection-theory contribution are outside this target. I visually checked the contribution boundary and typeset conjecture in [OWR 3/2024, printed pages 172–174](https://ems.press/content/serial-article-files/48651). An empty color is trivially pierced by zero points; this reconciles OWR with the explicit nonempty-family convention of the original formulation.

Attributions and limitations were checked against these primary sources:

1. [Jerónimo-Castro–Magazinov–Soberón, arXiv:1310.4714v3](https://arxiv.org/abs/1310.4714v3): Theorems 1.2–1.4 are the centrally symmetric, triangle, and stronger equal-disk results; Theorem 1.6 is the four-color variant. Lemma 2.1 already gives the standard translation-space duality. Lemma 6.2 contains the familiar two-family projected-width inequality. These ingredients cannot support a novelty claim by themselves. The PDF's 2018 front-page compilation date does not change its 2015 arXiv version marker or published citation.
2. [Gomez-Navarro–Roldán-Pensado, arXiv:2305.16760](https://arxiv.org/abs/2305.16760): Theorem 2.1 states the two-color three-point result for constant-width bodies or Banach–Mazur distance at most 1.1178 from a disk. Corollary 2.2 is the older eight-point bound; Theorem 2.5(a) is the three-point-union versus one-line alternative. The relevant statements and proof sections were checked. The [publisher record](https://link.springer.com/article/10.1007/s00454-024-00669-3) confirms online publication on 27 June 2024 and volume 73 (2025), pages 1079–1096.
3. [Martínez-Sandoval–Roldán-Pensado, arXiv:2307.07714v2](https://arxiv.org/abs/2307.07714v2): Theorem 3 gives four-point piercing of the union of all but one color, for n≥2. The manuscript's full six pages were inspected, including its fixed-direction inscribed-parallelogram lemma and proof of the four-point conclusion. This result is stronger than a one-color four-point bound and is accurately credited in the packet. It supplies no three-point resolution of the unrestricted source target.

This audit verifies the cited statements and their use. It is not a fresh exhaustive survey of all subsequent literature or a second independent proof audit of every published theorem. None of the packet's new restricted proofs requires assuming an unverified general three-point result.

## Turn 1: rational reduction and finite decision certificates

**Accepted under the written finite-family hypotheses.**

The failure-of-three-piercing condition is stable under sufficiently small outer thickening. The proof has the necessary compact bound on used points: for thicknesses at most 1, every useful piercing point belongs to the finite union of K+B translates. Unused points can be placed in that same compact set. A convergent subsequence in its third Cartesian power, followed by a constant assignment subsequence, yields a piercing triple at the limit if stability were false. Finiteness is essential and present.

The rational polygon approximation is valid. Uniform support-function approximation of K+(3ε/8)B within ε/16 lies strictly between the ε/4 and ε/2 offsets. Rational vertices can be obtained from a sufficiently fine rational approximation of a finite convex hull; full dimension is preserved by the positive inner offset. Perturbing centers by less than ε/8 gives the claimed ε/8 inner buffer and 5ε/8 outer inclusion. Thus every original cross contact becomes a positive-area overlap while every color still fails three-piercing. The argument accommodates originally lower-dimensional K. Empty K cannot support a nontrivial counterexample.

The arrangement candidate set is complete for full-dimensional polygon translates, including segment and singleton intersections. Any nonempty common intersection is a bounded polygonal set. An extreme point activates two nonparallel constraints, or is already a polygon vertex; overlapping parallel edges do not create an unlisted endpoint. This is the step that makes the finite mask search exact, rather than a point-grid test. Its completeness proof is not circularly inferred from test output.

The Helly formulation is also correct: bad pairs and bad triples, together with nonempty singletons, characterize which auxiliary color classes can share one point. Pairwise intersection alone is insufficient. The saved checker obtains its bad edges from the same arrangement masks, so its combinatorial comparison is not an independent geometry oracle. The reviewer supplies that missing independence as a control: a direct supporting-half-plane feasibility implementation and exhaustive feasible-class partitioning agree with both author methods on 1,270 nonempty subsets, including duplicate translates, coincident edges, segment contacts, singleton contacts, rational offsets, and affine shears.

The enumeration consequence is exactly a counterexample semidecision procedure. It has no bounded denominator, vertex count, family size, or termination guarantee when the conjecture is true. There is no implemented full unbounded search claimed by this audit.

## Turn 2: collinear and single-strip results

**Accepted with the dimensional and configuration restrictions stated in the text.**

The identity t∈q−K iff q∈K+t and the cross-intersection condition t−s∈K−K have correct signs. For a fixed direction, the maximum parallel chord length ℓ equals the radial extent of D=K−K along that direction. Every cover of collinear centers by translates of −K induces intervals of length at most ℓ, and a longest chord can be translated to realize any interval of length ℓ. Hence the interval-cover formula and greedy strict-gap convention are exact, including endpoints.

If the center set is also in s+D, its collinear span is at most 2ℓ: averaging the difference of two points of symmetric convex D gives half that horizontal difference in D. Two closed intervals cover the span. For ℓ=0, each such D section has at most one point. The sharpness example proves two may be needed for the designated color; it does not show the original existential conclusion needs two.

The positive-width strip theorem requires nonempty interior of K. At (ℓ,0), a supporting functional can be normalized to x+βy because its x coefficient is strictly positive: zero is interior to D and the support value is positive. Contracting a longest chord toward an interior point gives positive slack on the entire compact segment. A small transverse thickening therefore lies in −K. In the sheared coordinates, three width-3ℓ/4 rectangles cover the width-at-most-2ℓ box; the strip height b depends on K and the chosen direction. No uniform b over all bodies, nor implication from an arbitrary physical line transversal to such a small center strip, has been established or used.

## Turn 3: exhaustive lattice certificates

**Accepted for exactly K₂ and K₃ with integer centers, including their jointly affine-transformed lattice versions.**

The normalization by a second-family integer center places every first-family center in U=D∩Z². If that first family is not three-pierceable, a minimal obstruction T exists and has piercing number exactly four. A second-family center v satisfies t−v∈D for every t∈T. Choosing any t gives v∈D−D=2D, so the search over V=2D∩Z² is complete. Restriction to U at that step would be invalid; the packet correctly uses V.

The reviewer rebuilt the certificate without importing the author hull, point-in-polygon, edge-arrangement, or cover routines. For K_m+t the direct inequalities are:

    x ≥ t_x,
    t_y ≤ y ≤ t_y+1,
    x+(m−1)y ≤ m+t_x+(m−1)t_y.

Because m≥1, a common intersection, if nonempty, contains (max t_x,max t_y). Thus Cartesian products of center x- and y-coordinates are a complete independent piercing candidate set. Direct inequalities also give U, V, and all common-neighbor lists. Bottom-up cover dynamic programming verifies every subset and all recorded minimal cores:

- m=2: |U|=13, |V|=39, 8,192 subsets, 576 non-three-pierceable subsets, 3 minimal cores.
- m=3: |U|=17, |V|=53, 131,072 subsets, 31,052 non-three-pierceable subsets, 113 minimal cores.
- All 116 cores have exactly the neighbor set {(0,0)}.

Every bad subset was checked to contain a recorded core. Every one-point state was independently checked against direct common-intersection feasibility. These are complete finite certificates under a proven infinite-to-finite reduction, not bounded-window evidence extrapolated to all real centers.

The affine invariance requires moving the body and lattice together. Clearing center denominators without maintaining the body/lattice relationship does not extend the result to arbitrary real translations of the original K.

## Turn 4: all-body parallel-row theorem

**Accepted for every nonempty compact convex planar K.**

For each A row and B row, the two opposite cross extrema lie in one horizontal section of D. Their separation is the sum of the two row spans. Every section of D has length at most 2ℓ, so w(A_i)+w(B_j)≤2ℓ. This statement involves no smoothness, strict convexity, interior, integrality, or shared row-offset assumption.

If every A row has span ≤ℓ, one translate of a longest chord of −K covers each row. Otherwise one A row has span >ℓ, forcing every B row to have span <ℓ. The selected family consequently needs at most its number of rows. At ℓ=0 the inequality forces zero span in every row, so the proof remains valid. The explicit point q=(x−u,h−v) has the correct translation-space sign. Equality uses closed chords and causes no gap.

Exact accepted statement: if A uses at most r rows and B at most s rows, all parallel to the same direction, and every cross pair intersects, then τ(A)≤r or τ(B)≤s. In particular, the three-point conclusion follows if two colors each occupy at most three such rows. These are lines of translation vectors; lines meeting the physical translates are a different condition.

For the widely spaced variant H>0 is the perpendicular width of K, and distinct row heights **within each family** must differ by at least H. One-row families have span at most 2ℓ and hence need at most two points. If both families have multiple rows, the cross-height inequalities give span_y(A)+span_y(B)≤2H. Each term is at least H, hence both equal H and both families have exactly two rows. Applying the row theorem is sound even at spacing exactly H. The square sharpness example has only boundary cross contacts and correctly gives two required points in each of its two colors.

Thus the R×Z result for every real m≥1 follows because K_m has vertical width 1. It strengthens the existential lattice conclusion, without pretending to recover its stronger singleton-neighbor assertion. A horizontal segment has H=0 and is outside this variant's stated premise; lower-dimensional cases of the underlying row theorem and original problem are separately valid.

## Turn 5: determinant normalization, margin theorem, and obstruction

**Accepted under the exact margin hypotheses; no extension to factor one.**

For full-dimensional K, compactness gives a maximizer (u,v) of |det(u,v)| and interior gives a positive maximum Δ. Replacing either vector by any w∈D bounds both Cramer coordinates of w by 1 in absolute value. Symmetry and convexity give the inner unit diamond. The unit coordinate vectors belong to D, so each coordinate direction has an attaining chord of K of length 1; the square containment prevents longer chords. The same bounds show each coordinate projection width of K is exactly 1. This distinguishes chord lengths from projection widths rather than conflating them.

For polygonal D, optimizing the bilinear determinant successively in each argument reaches vertices. The implemented basis is exact and rational. The reviewer separately maximized over all original vertex differences for 10 translated/sheared polygons and found the returned determinant equal to the true extremum, with exact inverse maps and projection widths.

For longest perpendicular chords C and I of L=−K, λC+(1−λ)I is a genuine λ-by-(1−λ) rectangle inside L by convexity. The two chords need not intersect; this does not invalidate the Minkowski convex combination. The independent half-plane checks also verify all rectangle corners at λ=1/100, 1/2, 3/4 and 99/100.

Under the two-family margin condition a−b∈λD, the sum of x-spans is ≤2λ, so one family has x-span ≤λ. If both families' y-coordinates can each be covered by r closed intervals of length 1−λ, the selected family is r-pierceable. The strip widths refer to the normalized coordinates and λ must satisfy 0<λ<1 here.

For three colors, at most one color can have x-span >λ and at most one can have y-span >λ. At least one therefore fits a λ-square. Three copies of the inscribed rectangle cover it when 3(1−λ)≥λ, exactly λ≤3/4. At λ=3/4 the coverage meets on closed boundaries; no strict inequality is required. The conclusion still uses the fixed original K, not a scaled replacement. The small λ=0 case is unnecessary to the stated theorem and would be trivial.

For segment K, any cross-intersection forces equal parallel supporting lines. With two nonempty colors fixing one such line, every remaining translate has that same line. The problem becomes equal-length intervals. The pairwise cross extrema show that at least one color has center span at most the interval length and hence a common point. Point K and empty colors are immediate; empty K cannot satisfy a nontrivial cross premise. Thus no determinant normalization is improperly applied to Δ=0.

Strict cross-interior intersections do imply membership in some λD with λ<1 for a fixed finite full-dimensional configuration. The proof using a common interior anchor to move endpoints inward is correct. It supplies no uniform λ≤3/4. This is the exact obstruction to composing the result with Turn 1; strictness and a quantitative universal margin are different hypotheses.

### The square-cover barrier

The half-unit L1 diamond is a valid maximum-determinant-normalized body: D is the unit L1 diamond, the coordinate axes attain determinant 1, and no pair in D has larger determinant. The direct boundary proof correctly forces a ball pairing adjacent square corners, excludes opposite-corner pairing, and handles both remaining arrangements of the top corners. Its use of closedness to include side endpoints is legitimate.

The independent computational verification uses u=x+y and v=x−y. An L1 ball of radius 1/2 becomes a closed axis-aligned square of side 1. Every nonempty subset that fits such a square can be covered by one whose lower-left coordinates are the respective coordinate minima of that subset. Consequently the Cartesian candidate set is complete. This independently reproduces all 21 maximal masks in the saved 16-point witness. All 1,330 distinct triples of maximal masks fail to cover it; a four-cover is verified. The exact minimum is four.

This falsifies only the proposed universal square-cover relaxation. It is not a colorful counterexample: for example (1,1)∉D, so copying the full square witness into two colors violates the cross premise. The centrally symmetric case is already known to satisfy the original conclusion. No failed-lemma evidence may be upgraded to failed-conjecture evidence.

## Replay and reproducibility

The original scripts were run unchanged with ordinary Python 3 and bytecode writing disabled. Every stdout JSON equals the corresponding saved TURN_N_CHECKS.json. Reported author check counts are 2,832; 5,196; 177,229; 7,691; and 2,522. The third and fifth certificates regenerate exactly. Assertion counters are operational audit metadata, not a formal proof-size measurement.

Independent commands, from this review directory:

    python -B reviewer_checks.py > rerun.json
    python -c "import json; assert json.load(open('rerun.json')) == json.load(open('REVIEWER_CHECKS.json'))"
    python -B replay_author_checks.py

`reviewer_checks.py` uses explicit exception checks, so its checks are not removed by Python optimization. The author checkers require running without `-O`, as their README states. The reviewer certificate algorithms depend only on Python's standard library and rational/integer arithmetic. The source PDFs and renders are retained only as local audit evidence.

Extra implementation controls are 150 cross-valid row configurations with both choices exercised (73/77), and 30 cross-valid margin configurations. The premises and returned piercing incidences are checked by independent half-plane inequalities. These are finite controls. The proofs above, not the tests, justify the statements for arbitrary K and arbitrary real centers.

## Remaining gap and disposition

The full source condition is a−b∈K−K, with no center-row restriction, body-relative row-spacing condition, or positive uniform margin. Rational approximation does not force a three-row representation and does not turn arbitrary fine rows into spacing at least the body's width. The margin theorem stops at 3/4. The factor-one coordinate bounding box discards constraints that cannot be recovered from width pigeonholing alone; the diamond witness proves the suggested three-cover completion false.

The checkpoint therefore remains **original unresolved, five author turns consumed**. Its valid output is a collection of exact restricted theorems, finite-instance/counterexample-semidecision reductions, two complete lattice certificates, and a sharply delimited failed-relaxation certificate. I recommend accepting those claims with their present scope. No mathematical correction is required to do so. Any public summary must preserve the factor 3/4, center-line hypotheses, fixed-body/lattice coupling, and the explicit absence of a solution or novelty certificate.
