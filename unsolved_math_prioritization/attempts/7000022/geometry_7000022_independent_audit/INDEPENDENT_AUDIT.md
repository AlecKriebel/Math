# Independent adversarial audit: convex-hull surface area

Problem 7000022 / AMR-069-0022, rank 749. Audit date: 2026-10-05 UTC.

## Verdict

**PASS, scoped to the frozen partial-results package. The general target remains unresolved.**

The author freeze is a sound bounded investigation, not a proof of the sharp general inequality. No substantive mathematical correction is required for the retained claims. The five approach families are recorded as exhausted; this audit did not open a sixth proof-search route. No novelty or exhaustive current-openness certification is warranted.

Audited input: `GEOMETRY_7000022_AUTHOR_SAFE_FREEZE.zip`, 34,700 bytes, SHA-256 `5bd080b117c98900da18f44084511654b2161f9fbffc9acc9129657cff40996f`. All nine archive entries match the supplied author directory; all eight payload entries match `AUTHOR_MANIFEST.json`. The author files and original archive were left unchanged.

## Scope and independent evidence

All nine author files were reviewed: the definitions and every proof in `PROOFS.md`; README and research/status claims; both verification/manifest records; turn ledger and readiness; the complete verifier; and the saved result structure, rational certificates, counts, and diagnostic midpoints. The author verifier was executed only in an extracted replay copy. It exited successfully and reproduced its saved JSON byte for byte.

A separate standard-library verifier was written without importing the author's code. It uses decimal-grid rational radical enclosures and a different arctangent identity for pi. Its passing controls include:

- All 12 tours for the four specified noncoplanar tetrahedra
- All 60 unoriented cycles of the specified flattened octahedron, obtained by canonicalizing all permutations
- Exactly eight Euclidean minimizers, all with the interior pole-to-pole edge
- Sixteen boundary-minimizing edge cycles, with every other cycle strictly excluded by intrinsic-distance lower bounds
- Six rational heights on both sides of the stated transition threshold
- 150 exact projected-area identities, comparing a planar convex-hull/shoelace computation against the three-dimensional face formula
- An exact quadratic support-function test of the integrated Hessian/gradient identity
- The square equality control and the six-edge zero-Jacobian tree cone
- Eight rejected false surrogate claims
- Six deliberately mutated implementations rejected by the final verification suite
- Independent interval and midpoint cross-checks for all twelve saved author certificates

These are finite checks, not formal certification of the analytic arguments or a general polygonal theorem.

## Claim-by-claim mathematical review

### 1. Target, rectifiability, and lower-dimensional area: PASS

The target is `S(conv gamma) <= L^2/(2*pi)` for arbitrary continuous rectifiable closed parametrized curves in Euclidean three-space. Traversal multiplicity belongs in `L`. The source imposes no simplicity or hull-boundary restriction on the main question. For planar hulls, `S` is twice planar area, and for dimension at most one it is zero.

The continuous extension is normalized correctly: the polyhedral visibility argument gives `B(u) = (1/2) sum a_i |n_i.u|`, and spherical averaging gives `S=4 E B`. A planar body projects with area `b|n.u|`, hence `S=2b`. Projection continuity, planar convex-area continuity, and a common bounding ball justify the dominated-convergence step. There is no missing factor of two or confusion with the Hausdorff area of a planar set counted once.

The primary statement and its planar convention were checked in the author-hosted [Ghomi problem collection, printed page 14](https://ghomi.math.gatech.edu/Papers/op.pdf). The existing local target-page rendering was also visually inspected.

### 2. Polygonal equivalence and maximizer existence: PASS

Ordered polygonal interpolation of a uniformly continuous loop converges uniformly, and chord lengths do not exceed corresponding arc lengths. Convex hull is Hausdorff-continuous under this approximation. Thus an inequality for every closed polygon implies the rectifiable version without needing the polygon lengths to converge to `L`.

For existence, constant-speed reparametrization is legitimate for rectifiable loops, including curves with pauses in their original parametrization. Translated loops with length at most one form a uniformly bounded, equi-Lipschitz family after this reparametrization. Arzela-Ascoli and the area continuity above give a maximizer. Length cannot exceed one in the limit; positivity and scaling force the maximizing length to equal one. None of this proves that a maximizer is planar.

### 3. At most four hull vertices: PASS, including sharpness

Every extreme point of the convex hull of a compact curve image belongs to that image. Choosing one visit per extreme point in cyclic order produces a polygon with the same hull and no greater traversal length.

For a tetrahedron, its four faces contain the four consecutive edge pairs of any Hamiltonian cycle. The triangle bounds yield

`S <= (ab+bc+cd+da)/2 = (a+c)(b+d)/2 <= (a+b+c+d)^2/8`.

Perturbation of the four input points to noncoplanar positions is valid even when a point is interior to the planar hull or vertices repeat. Area continuity gives the doubled planar hull in the limit. A unit square attains `S=2=L^2/8`; no smaller constant works in this class. Simultaneous right-angle equality for a spatial tetrahedron would force opposite edge vectors to be negatives, which is planar. The sharpness claim does not incorrectly assert full-dimensional equality.

### 4. Projection estimates and Jensen direction: PASS

Directional total variation gives planar convex-hull perimeter at most traversal length, including degenerate projections. Fubini and the almost-everywhere arclength tangent yield `E ell=(pi/4)L`. Cauchy-Schwarz along the curve gives `E ell^2 <= (2/3)L^2`, and therefore `S <= 2L^2/(3*pi)`.

The doubly traversed segment realizes the second-moment constant `2/3`. Jensen goes in the lower-bound direction: `E ell^2 >= pi^2 L^2/16 > L^2/2`. Consequently the proposed sharp length-only second-moment bound is impossible. The averaged isoperimetric-deficit identity is algebraically correct, and is explicitly an equivalent missing estimate rather than a proof.

### 5. Mean width and support functions: PASS

For each direction, the scalar variation is at least twice the width. Averaging `|T.u|` gives `wbar <= L/4`. The support-function area identity has the correct gradient sign and coefficient:

`S = integral (h^2 - |grad h|^2/2)`.

Expanding the two-dimensional determinant and using the integrated spherical Bochner formula verifies this identity. The first nonzero spherical Laplacian eigenvalue is two, so Poincare gives `S <= pi*wbar^2`. Rotational support-function smoothing followed by addition of a small ball preserves convexity and gives the required strictly convex smooth approximation. The limiting argument is valid for all compact convex hulls, including planar ones.

Thus `S <= pi*L^2/16` is justified. The coefficient is `pi^2/8`, approximately 1.23370055, times the target. The slack threshold and its numerical value are correct; the circle has zero slack, so that condition does not settle the extremal case. The same area/mean-width inequality is independently corroborated in [Hug and Weil, printed page 95](https://users.fmf.uni-lj.si/lavric/hug%26weil.pdf). The package makes no unsupported best-known-bound claim.

### 6. Known boundary case: PASS within the stated proof/attribution split

The simple polygonal boundary-loop argument is valid. Every hull vertex lies on the loop, so neither complementary intrinsic disk has interior cone curvature; each has perimeter `L`. The imported nonpositive-curvature disk inequality gives the required two area bounds. No injective planar development of a flat disk is silently needed.

The package proves this polygonal simple case and attributes the wider boundary regime, rather than independently proving all regularity and nonsimplicity extensions. This distinction must remain visible. Ghomi's printed formulation explicitly states the simple boundary case; [Zalgaller, Section 7](https://www.mathnet.ru/eng/aa700) additionally discusses allowing multiple points. His broader statement is source attribution, not an independently checked complete technical proof in this audit.

### 7. Exact fixed-hull boundary obstruction: PASS

For six vertices at equatorial positions `(plus/minus 1,0,0),(0,plus/minus 1,0)` and poles `(0,0,plus/minus h)`, Hamiltonian cycles split exhaustively according to whether the poles are adjacent. The minimum Euclidean lengths in the two classes are

`2h+2sqrt(1+h^2)+3sqrt(2)` and `4sqrt(1+h^2)+2sqrt(2)`.

The first is shorter exactly when `h<1/(2sqrt(2))`. Selecting visits and straightening arcs proves that Hamiltonian minimization controls all closed rectifiable visiting curves, including repetitions.

A boundary path between poles must cross the equatorial square boundary. Its crossing radius is at least `1/sqrt(2)`, giving intrinsic distance `2sqrt(h^2+1/2)`; two face segments through an equatorial edge midpoint attain it. The resulting cycle lower bounds, together with an edge-cycle construction, prove the exact global boundary-tour minimum. This is not just a comparison against boundary edge tours.

At `h=1/10`, the Euclidean minimum is approximately 6.452615811343 and the boundary minimum 6.848377373195, giving a strict gap approximately 0.395761561851. Every Euclidean minimizer is simple and has a pole-to-pole segment whose open interior lies strictly inside the hull. The area is approximately 4.039801975345, and the target margin is positive, approximately 2.586813152690. The example refutes only the length-nonincreasing fixed-hull boundary-replacement mechanism.

The original geometric warning also appears in [Ghomi's October 2024 question](https://mathoverflow.net/questions/480430/shortest-loop-through-vertices-of-a-convex-polytope). The audit's exact argument and enumeration validate the authored witness independently of that warning.

### 8. Zero-area filling obstruction: PASS

The three-arm closed tree walk has traversal length six and tetrahedral hull area `(3+sqrt(3))/2`. Radial coning gives a globally Lipschitz disk map: bounded radial derivative and the angular Lipschitz bound give the usual cone-extension estimate, including the origin. On each arm interval the radial and angular derivatives are parallel, so the two-dimensional Jacobian vanishes almost everywhere. The filling area is exactly zero, not a small numerical approximation.

This is an admissible nonsimple curve for the main question and defeats any fixed-factor bound of hull area by least Lipschitz filling area in that full class. It does not disprove the target or establish anything about an additional simple-Jordan-only filling comparison.

## Source and provenance findings

The complete pinned problem and research-result corpora were independently rehashed. Both byte counts and SHA-256 hashes match a fresh read of the public repository manifest. The exact numeric problem record is unique; its AMR code is unique in the problem corpus and identifies the actual research report. That report is OPEN-TRIAGE status material with no candidate proof. It cannot be counted as an earlier solution.

The supplied two primary PDF byte streams were rehashed; their hashes match the author's metadata. Their relevant current public statements were separately inspected through the web reader. This does not claim an independent fresh binary download of those PDFs, nor a complete proof audit of either external paper.

The Ghomi-Wenk 2024 theorem controls inradius. The Bohr-Markvorsen-Raffaelli 2026 paper controls volume under additional smoothness, boundary, and torsion-zero hypotheses. Neither proves this surface-area problem; in particular its term “four vertices” is different from four extreme points of a polytope.

The returned main MathOverflow question displayed no answer text. Targeted current searches and the author's publication list yielded no verified general resolution. Search snippets, missing pages, and bounded negative searches cannot certify current openness. Two supplemental MathOverflow query variants returned reader errors; no inference of a solution or absence of a solution was drawn from those failures. Historical repository-wide negative search claims were not exhaustively repeated in this audit and are not upgraded to an exhaustive duplicate certificate.

## Corrections, release boundary, and disposition

Required mathematical corrections: none. Optional editorial clarification: retain the precise distinction between the proved simple polygonal boundary case and the source-attributed wider boundary case whenever summarizing the results. This is already present in the frozen proof and is not a release blocker.

Acceptable disposition: exhausted after five substantive approaches, with verified partial results and obstructions; `full_target_resolved=false`. Any presentation as a solved problem, a new sharp general inequality, a novelty-certified result, or a fully automated analytic proof would fail this audit.

The audit package contains only authored review, independent code and computed controls, and public verification metadata. It contains no source PDFs, extracted source text, raw source-corpus records, or private coordination material. No remote writes were performed.
