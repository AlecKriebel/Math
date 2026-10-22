# Broad/classical priority audit — PR211 / 5100063 / k904,a

**Disposition: no exact general geometric anticipation was verified in the selected primary-source corpus. Historical novelty and first-proof priority remain undetermined.** This is a bounded coverage finding, not a novelty certificate. The root audit owns the separate mathematical-validity and promotion decisions.

The material already available in the literature is substantial. The Jacobi parametrization, Poncelet-grid affine correspondences, complex pole cancellation, cyclic principal-part reconstruction and the abstract half-period product identity are established tools. The remaining distinction is whether a prior theorem already connects those tools to **the exact outer polygon inverted about the original billiard foci**. I did not verify such a connection. No claim that a method or abstract elliptic identity is new should be made.

## Exact claim audited

For fixed real E with a>b>0 and a fixed nondegenerate confocal elliptic caustic, take any family of odd least period N>=3, including primitive coprime stars. Intersect consecutive tangents at the original billiard vertices to obtain Q_i. Invert Q_i in unit circles about the two **original** foci. Join inverted vertices by straight segments in trajectory order and compute signed shoelace areas B_+,B_-. The target is phase independence of B_+B_-. Repeating a closed list r times multiplies each signed area by r, hence the product by r².

The frozen source definition identifies this as k904,a. That identification, its October 2020 listing and its conjectural attribution are provenance, not proof of present openness or historical priority. Original-vertex inverse areas (k903,a), outer-locus own-focus inverse areas (k906), inverse arcs and unsigned filled-face areas were not substituted.

## What the broad sources establish

[AST's final Theorem 1.3 and §7](https://doi.org/10.1007/s40879-020-00426-9) establish the odd-period ratio of untransformed orbit and tangent-polygon areas for concentric ellipse pairs. The final proof expands the grid/affine argument from [v2](https://arxiv.org/abs/2001.02934v2); its conclusion does not introduce focal inversion. The same paper's polar/Minkowski and skew-hodograph constructions concern billiard and angular observables. A weighted inverse-area transformation is an additional premise, not a consequence stated in that theorem.

[Bialy–Tabachnikov](https://arxiv.org/abs/2001.08469v2) prove support-function/action identities, angular products, pedal-centroid/squared-distance invariants and certain even-period focal-distance products. These do not identify the target's product of two shoelace sums. The [Levi–Tabachnikov grid theorem](https://arxiv.org/abs/math/0511009v1) gives the fixed affine correspondence underlying AST, but its area transport does not commute with circle inversion.

The strongest analytic prior is [KLS's local arbitrary-pole reconstruction](https://arxiv.org/abs/math-ph/0306028v1), together with [Cyclic Identities II, Eq. (66)](https://arxiv.org/abs/math-ph/0207019v2). Once a cyclic function F has precisely two simple poles, a real period L and the appropriate imaginary anti-period, it is a scalar multiple of a rescaled cs function. Then F(u)F(u+L/2) is constant by an ordinary quarter-period identity. The exact normalization and proof are in `EXACT_TRANSFERS_AND_OBSTRUCTIONS.md`. This explicitly locates the classical part of the candidate's last step.

That conditional result does not settle historical anticipation. KLS's master identities require the actual principal parts and their symmetry class. The candidate's **unsummed** inverse-edge function E is generally not one fixed-sign class under real 2K. Decomposing E into its even and odd components under that shift, or first proving the reduced trace's two-pole property, still requires the target-specific inverse-distance/edge algebra and its cancellation. In particular, the N=3 coalescence is not covered merely by naming a master identity.

[Roitman–Garcia–Reznik](https://arxiv.org/abs/2103.11260v3) provide an exact polar/pedal bridge and a limiting-point **perimeter** theorem for bicentric polygons. Applying the bridge to the present Q produces a circle–ellipse Poncelet pair, with the second conic noncircular. Thus the bicentric theorem's hypothesis is absent. The explicit equation in the transfer certificate proves that obstruction, including when the outer ellipse reverses its major axis.

[Chavez-Caliz's Theorem 6](https://doi.org/10.1007/s40598-020-00154-8) supplies an important earlier complementary-zero/pole area-product argument, but for an even-period product of untransformed Poncelet/tangent areas. [Stachel's published parametrization and length identities](https://doi.org/10.1007/s40879-021-00524-2) are necessary credited inputs, not the focal inverse-area conclusion. Centroid-locus and projective self-duality results require their own observable-specific pole relations and do not assert general constancy of rational cyclic traces.

The later broad leads do not remove the object gap in their checked statements/proofs. [Glutsyuk's 2026 Theorems 1.5–1.9 and §3.8](https://arxiv.org/abs/2605.24434v1) concern a canonical weighted 2-form on dual-billiard phase space and fiber differentials. That form is not Euclidean polygon shoelace area. [Gheorghe–Garcia 2026](https://doi.org/10.1007/s12215-026-01409-7) concerns 3-Poncelet circle–ellipse construction and eccentricity/limiting-point relations; its full relevant proofs contain no focal-inverse area-product theorem. Selected classification and projective-construction statements were also checked, with the exact reading limits recorded in the ledger.

## Independently checkable obstruction results

Two exact examples rule out an overbroad transfer from concentric Poncelet geometry alone. In the homothetic pair with outer axes (2,1) and inner axes (1,1/2), inversion about the **inner** foci gives products 27/169 and 27/196 at two phases of the same Poncelet triangle family.

A second example closes the possible general-position escape: outer axes (2,1), inner axes (4/3,1/3), centers (±√15/3,0). The two explicit Poncelet triangles in the transfer certificate give products 1125/12544 and 9/128, difference 243/12544. The script checks all outer incidences, exact inner tangencies and strict segment contact. The conics have four distinct transverse complex intersections. The root independently rebuilt both examples and confirmed these checks. Neither example refutes the actual billiard target: they refute the asserted universal extension on which an automatic AST transfer would depend.

Finite 80-digit diagnostics separately confirm varying individual inverse areas, nonconfocal/axis-reversed outer loci and phase-constant products in N=3, convex N=5 and star N=5 examples. Correct phase alignment also gives a constant outer/original inverse-area ratio in those examples. These are diagnostics only. They leave the k806,a alternative route possible; they do not establish a prior general proof of that ratio or permit importing the original-vertex product as an already proved historical result.

## Route state and exact remaining gap

| Route | Current state | Reopen only for |
|---|---|---|
| AST/grid area ratio → focal inverse product | Blocked as an automatic transfer; generic inner-focus extension is false | A precise additional identity valid for this special billiard-derived outer pair |
| Bicentric polar/pedal theorem | Blocked for the stated theorem: one polar conic is noncircular; observable is perimeter | A genuine circle–ellipse weighted-area theorem or a verified new transformation preserving centers and straight edges |
| KLS master identity → target | Classical conditional mechanism, not verified geometric anticipation | A prior published identification of the exact trace and its principal-part cancellation |
| BT action/focal-distance invariants | No formula reducing the target to the established actions or distances was verified | An explicit exact reduction with signed areas and all odd windings |
| k806,a ratio plus k903,a product | Blocked as a historical proof chain when either premise lacks an established prior proof | Actual primary proof(s), with phase alignment and centers checked |
| Rational integrability / invariant area forms | Different statements and observables | A theorem explicitly identifying the target product as that first integral or an exact associated integral |

## Coverage, limitations and usable wording

The audit read primary theorem statements and relevant proofs across the grid, generating-function, cyclic-identity, polarity/pedal, centroid/area and rational-dual-billiard families. `SOURCE_TO_CLAIM_LEDGER.md` states passage-level coverage; `QUERY_ACCESS_LEDGER.json` records the actual queries, URLs, editions/dates and access failures. Some large classification/construction papers were read only at the relevant statements. Metadata-only leads are explicitly unresolved. No inference of absence is drawn from search results, and no comprehensive examination of all nineteenth-century or all later literature is claimed.

No same-family or other priority-family audit findings were read. The initial obstruction map was frozen before new full-source reading. Only root mathematical controls and source leads were exchanged. No external individual was contacted, no outreach was drafted, and no repository/provider/publication mutation was performed in this shard. Primary payloads remain excluded private reading material. After the disk-pressure notice, work continued in text and small exact controls without further large retrievals or rendering.

A defensible description, subject to the parent's independent integration, is: **“A proof of the odd-period outer focal-inverse area-product invariant conjectured as k904,a in the pinned 2020 list, using established Jacobi and meromorphic methods.”** Do not add “first”, “new general elliptic identity”, “still open”, or a claim of absolute novelty on this audit's evidence.

The bounded assigned audit is complete. The strongest verified results are the conditional classical reduction and the two exact transfer obstructions; the exact historical-priority question remains open for integration and any further literature work.
