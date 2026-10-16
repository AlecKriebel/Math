# Independent classical priority audit — PR254 / AMR-050-0020 / k403,a

Final family conclusion, 2026-10-13 UTC: **no earlier classical proof or complete classical covering combination for the full target was located in the inspected primary corpus.** This is a bounded negative finding, not a worldwide firstness certificate. The observation, billiard parametrization, elliptic-function tools, and earlier campaign pedal mechanism are prior work and must be credited. In particular, the cyclic-dn reduction method should also acknowledge the pre-2004 cyclic-identity and generalized-Landen literature.

No classical priority obstruction to proceeding with a properly credited note was found. This family makes no conclusion about contemporary preprints being investigated by the separate current-priority family. I did not read that family's conclusions before reaching this finding.

## 1. Frozen claim and falsification standard

The reviewed input is PR254 head 73efd1fb8ba2d3039ed6692b3ad1dfa1e3085755, source PROOF.md SHA256 ff2b1d78a1b94997d366d5173243ea95b949d5ae24574471639740b35cf2c16e, from unsolved_math_prioritization/attempts/5100020. I read the entire proof, source gate, and author log. The head binds the precise original orbit constructions, not a nearby named invariant.

For a noncircular ellipse with a strictly nested nondegenerate confocal elliptical caustic, take a primitive orbit of least odd period N>=3 and any admitted coprime star winding. Its signed original-side origin-pedal area p multiplied by the signed original-vertex origin-antipedal area q is constant through the family. The antipedal line at vertex P is

    P dot X = P dot P.

All actual consecutive intersections must be finite. Signed zero areas are allowed. Reversal preserves the product. Hyperbolic and collapsed caustics and period parity obtained only by padding are outside the assertion. The circle is a separately direct regular-star extension.

The earlier credited PR204 / 5100012 proves constancy of A(P)p for odd periods. Consequently, an earlier proved all-odd statement q=R A(P), with R depending only on the fixed ellipse/caustic, would cover the full target when combined with that component. The missing classical ingredient cannot be dismissed merely because it has another title or code. Conversely, integrability, a general proof technique, or a finite list of sampled periods does not by itself supply it.

## 2. Original observation and priority boundary

The exact k403,a entry already occurs in Reznik–Garcia–Koiller's first arXiv version, Forty New Invariants, submitted 26 April 2020: Table4, printed p5, origin O, odd N, product of the unprimed pedal and antipedal areas, proof column marked unknown. I checked the definitions and signed-area convention and visually inspected that table. I also visually verified the same entry in v11 Table5 printed p7 and the published Fifty New Invariants Table5 printed p348. This firmly credits the conjectured invariant to the source authors; the present contribution cannot claim discovery of the invariant.

The frozen author log records derivation during 1 October 2026, 10:55–11:12 UTC. A fresh read-only GitHub receipt confirms PR254 was publicly created 2026-10-01T11:29:49Z and still has the assigned head. The former is an author's recorded work interval; the latter is a server-observed PR publication timestamp. Neither is a claim about the causal order of private discoveries.

## 3. Strongest classical covering candidates

### 3.1 Odd original/outer area ratio: valid theorem, different lines

Akopyan–Schwartz–Tabachnikov, Billiards in Ellipses Revisited, Theorem1.3 and the full §7 proof, establish the area ratio between an odd Poncelet polygon on concentric ellipses and the polygon made from tangents to its outer ellipse. The proof reduces to confocal ellipses and uses an affine correspondence from the Poncelet grid. This is a genuine relevant all-odd theorem; it is not simply ignored as unrelated.

For an ellipse x²/a²+y²/b²=1, the tangent at P has normal (P_x/a²,P_y/b²) and equation

    (P_x/a²,P_y/b²) dot X = 1.

The origin antipedal at P has normal P and equation P dot X=|P|². They differ at generic non-axis points when a>b. An exact check at a=2,b=1,P=(6/5,4/5) gives determinant -18/25 between the normals. Thus the theorem's polygon cannot simply be renamed q.

A fixed linear map taking each tangent at P to its origin-antipedal line at the same P would require a fixed matrix M satisfying M D^{-1}P=P/|P|², with D=diag(a²,b²). Every vertex direction would then be an eigenvector of a fixed matrix, forcing a scalar matrix; the required scalar varies with |P|² for a noncircular ellipse. This rules out that particular same-label linear bridge. It does not rule out every imaginable reindexing or transformation. No alternative proved bridge to the target was found in the theorem or grid sources inspected.

### 3.2 Even original/outer area product

Chávez-Caliz, More About Areas and Centers of Poncelet Polygons, Theorem6 and its complete §5 proof, establishes the signed area product of a Poncelet polygon and its outer tangent polygon for even N. It uses cancellation of area poles and zeros on the elliptic curve. It is relevant methodological and area-invariant precedent, but its asserted parity and derived polygon both differ. Repeating an odd walk to an even list does not establish the required identity, and a known original/outer product does not determine the origin-antipedal factor.

The paper's general treatment of algebraic area and degenerate Poncelet polygons does not state that all derived Euclidean area expressions are invariant. Its pole arguments must be reapplied to the exact expression; doing so here is precisely part of the present proof.

### 3.3 Poncelet grid, polarity, and projective integrals

Levi–Tabachnikov's Poncelet-grid theorem, Stachel's geometric grid theorem, and Stachel's A Triple of Projective Billiards describe conic families made from intersections of orbit sidelines, tangent polygons, and caustic contact polygons. I inspected their constructions, theorem inventories, and the relevant polar/inner/outer statements. None identifies the origin antipedal with one of those polygons or proves its all-odd area ratio to the original orbit.

Circular polarity clarifies the exact obstruction. With a unit circle about O, the origin-antipedal side at P is the polar of the inverted point

    I(P)=P/|P|².

The point-inverted ellipse satisfies

    X²/a² + Y²/b² = (X²+Y²)².

This is the relevant inverse-vertex locus; substituting the original ellipse's circular or elliptic polar polygon changes the construction. The envelope of the antipedal lines also does not equal the ellipse. Its squared support at normal angle pi/4 is 2a²b²/(a²+b²), whereas the ellipse's is (a²+b²)/2, different unless a=b. Reflection symmetries and the axial support values would force any elliptical envelope to have the original axes and semiaxes, so this also excludes an elliptical envelope of these same lines in the noncircular case. The exact a=2,b=1 check gives 8/5 and 5/2.

Schwartz's Pentagram Integrals for Poncelet Families, Main Theorem1.2, gives equality of projective monodromy invariants through a Poncelet family. The signed product p q depends on the Euclidean perpendicular constructions and scales as the fourth power of an overall length scale. No identification with an applicable monodromy integral was supplied by that paper. Projective constancy alone therefore does not prove this target.

These exclusions are object checks, not claims that classical projective geometry could never furnish another proof.

### 3.4 Bicentric and focal inversion mechanisms

Roitman–Garcia–Reznik's New Invariants of Poncelet–Jacobi Bicentric Polygons proves bicentric angle-sum and limiting-point pedal-perimeter invariants and transports these to focus-inversive elliptic billiard polygons. The focal and limiting-point assumptions are substantive; the origin is not an ellipse focus when a>b. The paper's area observations in its video list are explicitly experimental, including focal inverse area phenomena and a special six-periodic zero-antipedal observation.

The appendix polar-pedal transformations and the relevant conic construction formulas do not prove the requested all-odd original origin-antipedal ratio. Garcia–Reznik's later self-intersected-orbit companion likewise supplies specific inversive/parity examples rather than this theorem; I checked its complete proposition/theorem inventory and antipedal occurrences. Such examples do not justify extrapolation to every odd period or every coprime star.

## 4. Triangle and smooth-curve shortcuts

Mitrea's On the Area of Pedal and Antipedal Triangles, Theorems1.1 and1.4, express the pedal factor using the circumcircle power of the pedal point and the antipedal factor using the power of its isogonal conjugate. These are actual relevant classical formulas, but the points need not be the same. Moreover, a triangular formula has no asserted extension to arbitrary odd N.

An overly broad claim that the areas of the same-point pedal and antipedal always multiply to the reference area squared is false. For the ordered triangle (2,0),(0,2),(-1,-1) and point O=(0,0), exact supporting-line and intersection calculations give

    original area = 4,
    origin pedal area = 24/25,
    origin antipedal area = 18,
    product = 432/25, whereas original area squared = 16.

All relevant intersections are finite. This is a negative control on the generic-triangle shortcut, not a billiard counterexample. The distinction prevents using a misquoted classical triangle fact as automatic full coverage.

Gheorghe's When Euler (Circle) Meets Poncelet (Porism) concerns triangles sharing circumcircle/Euler-circle or pedal-circle data and negative pedals of circles focused at the pedal point. Its theorem scopes are triangular and tied to those conics. It does not supply the missing all-odd origin-antipedal area relation.

The smooth area-invariant pedal-like and Steiner-hat papers concern the area of complete curve envelopes/loci as the pedal point moves. Their fixed-curve or boundary-point assumptions differ from changing a finite billiard polygon at fixed O. A complete envelope area, even if known exactly, does not fix the shoelace area of its discrete cyclic tangent polygon for each N and phase. These works are useful background, not a full covering theorem.

## 5. Analytic tools that must be credited

Stachel's On the Motion of Billiards in Ellipses, Theorem4.3 and equation4.9, already supplies the exact Jacobi parametrization, coprime turning number, and relation between caustic and outer semiaxes used here. The source proof properly credits this; classical Jacobi periodicity and addition formulas are not new.

The cyclic sum S(w)=sum dn(w+j delta), reindexed onto the real subgroup, and its use as the archetypal simple-pole antiperiodic function belong to established elliptic-function theory. Khare–Lakshminarayan–Sukhatme, Cyclic Identities II, §2.1.1 equations(17)–(20), gives master reductions to derivatives of the dn cyclic sum from the summed principal parts and period characters. Its simple-pole case captures the general analytic reduction used here. Khare–Sukhatme, Generalized Landen Transformations, equations(13)–(15), expresses a uniform dn sum as a rescaled dn with transformed modulus. I read those statements and the relevant derivations, not every identity in their appendices.

Neither paper applies the reduction to the actual origin-antipedal area expression or checks its finite coincident/opposite endpoint singularities, incident double-pole cancellation, and odd-period lattice coincidence. Those construction-specific checks remain necessary. The compact-torus proof can stay self-contained; add these references as precedent, and do not describe the cyclic-dn method or pole-subtraction uniqueness as newly discovered.

Bialy–Tabachnikov's generating-function results, outer-pedal sums/centers and focal distance products were also checked in the full relevant theorem/proof sections. They do not state p q or the required all-odd q/A(P) ratio.

## 6. Exact remaining priority gap and disposition advice

The strongest candidate classical reduction is

    known odd A(P)p constancy + a proved all-odd q/A(P) constant.

No earlier classical source in this audit supplies the second factor for the actual original origin antipedal. The AST original/outer ratio cannot be substituted without an additional proved geometric or algebraic bridge. An earlier generic cyclic identity becomes a target proof only after verifying the specific area expression's hypotheses; those checks are not an already-present billiard corollary in the inspected papers.

Recommended attribution: the original authors conjectured k403,a in 2020; the candidate proves the source invariant using Stachel's canonical coordinates, classical Jacobi/elliptic-function tools, related cyclic-identity precedent, and the earlier credited PR204 origin-pedal mechanism. The antipedal-specific analysis is the candidate's useful additional argument. State that the priority search was bounded and no absolute historical-firstness claim is made.

This is a **classical-family pass with attribution recommendations**, conditional on root's mathematical acceptance and the separate recent-priority result. It is not acceptance of an unrestricted parity extension, unsigned region-area formulation, degenerate caustic extension, or unsourced claim to resolve the whole source list.

## 7. Reproducibility, independence and limits

CONSTRUCTION_CHECKS.json is generated by a portable standard-library exact-rational checker. Its scope is deliberately limited to the object and shortcut distinctions above; it does not numerically or symbolically re-prove the target theorem. Source hashes, provenance receipts, frozen input and authored output hashes are in FINAL_AUDIT_INTEGRITY.json. All external whole-source PDFs/text/images and raw web/GitHub receipts are local reading copies and must not be included in a public verification package.

Searches used exact target labels, ordinary pedal/antipedal and odd-area language, origin-antipedal/original-area ratios, bicentric/focal inversion, negative pedals, Poncelet grids, projective monodromy and cyclic Jacobi/Landen terms. QUERY_LOG.md records the query bounds. Primary sources rather than search snippets support the scope conclusions. Search-engine freshness labels were not treated as publication dates. One HTTP418 fetch failed and an alternate primary URL supplied the paper successfully.

Original Sturm/Steiner nineteenth-century treatises and all possible books or non-English literature were not exhaustively inspected. Their credited statements were read in the later primary papers; no archival completeness is claimed. General no-result searches can miss relevant work. There was no external communication, no sibling-priority conclusion borrowing, and no Git or PR mutation.
