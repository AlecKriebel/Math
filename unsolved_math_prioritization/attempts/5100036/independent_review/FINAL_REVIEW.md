# Independent adversarial review: 5100036 / arXiv k608

**Verdict: PASS_COMPLETE_SOURCE_TARGET_ON_NATURAL_DOMAIN.** The unchanged frozen proof establishes equality of the two signed areas for every primitive even elliptical-caustic billiard, including stars, and therefore the exact arXiv ratio equals 1 wherever its denominator is nonzero. It also correctly supplies a genuine finite common-zero example. No mathematical or source-scope correction is mandatory.

Reviewed `PROOF.md` SHA-256:
`4edb2dfe7be2d85ddb219bca54f661f4f6829f7667e07bd2c84fb5499726bb2b`.

Reviewed `FROZEN_MANIFEST.json` SHA-256:
`8011347b3a6f6c03a028476fb0dfa04256f2f88e73d2a196b599541fed327412`.

All eight listed author artifacts and four primary PDF hashes match. The result is a credited classical-symmetry consequence, not a certified novelty claim. The original source target is fully resolved on its natural quotient domain after one author turn; there is no reason to manufacture four further unsuccessful turns.

## 1. Independence and exact source

This reviewer has authored or reviewed other centrally symmetric derived-polygon identities, including k406,a, k607, and the distinct inner-inversion k905. That shared classical mechanism is disclosed. I did not supply the k608 six-orbit construction, antipedal formulas, or area factor to its author. Both current cross-target candidates were frozen before their independent audits. My checker reconstructs the geometry without importing the author's checker.

I visually inspected arXiv:2004.12497v11 Table 7, printed p.9. Its **k608** is the ratio of focal **outer antipedal** signed areas for even N. The original billiard foci are used, not foci of the outer vertex locus. I separately inspected the published companion Table 7, p.349: k608 is absent, while its final k607 is a different pedal-area relation. The candidate preserves the original arXiv target.

The arXiv introduction specifies confocal ellipses, Section 3.5 supplies the perpendicular-line antipedal construction, and equation (1) on p.3 supplies signed shoelace area. Stachel's Theorem 4.3 and equation (4.9), p.1614, provide the canonical Jacobi rotation for strict elliptical caustics. Coprime period and turning number are explicit there. Combined with the real 2K shifts, even primitive period gives the half-turn pairing. Orientation may be reversed without affecting area equality or its defined ratio.

Sources checked:
- Reznik–Garcia–Koiller, arXiv v11, 29 October 2020: https://arxiv.org/pdf/2004.12497v11
- Published companion, Arnold Mathematical Journal 7 (2021), 341–355: https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf
- Stachel, *On the Motion of Billiards in Ellipses*, European Journal of Mathematics 8 (2022), 1602–1622: https://doi.org/10.1007/s40879-021-00524-2
- Garcia–Reznik, *Exploring self-intersected N-periodics in the elliptic billiard*, Table 2 p.17, contextual credit for a different six-antipedal zero: https://ami.uni-eszterhazy.hu/uploads/papers/finalpdf/AMI_online_1216.pdf

The last source is credit/context, not a proof input for the present zero example. Its listed aspect-ratio-2 original-antipedal phenomenon must not be confused with the present outer-antipedal aspect ratio 1+sqrt(3).

## 2. Universal geometric regularity

### Outer vertices

Supporting tangents to an ellipse at distinct points are parallel only at antipodal points. Such a chord passes through the center and therefore cannot be tangent to a strict centered inner ellipse. This proves the consecutive outer intersections are finite.

The proof's separate exclusion of normal backtracking is correct. For a point (a cos θ,b sin θ), a line in the normal direction has perpendicular covector (sin θ/b,−cos θ/a). Applying the dual confocal-conic condition gives

    λ = a² sin² θ + b² cos² θ ≥ b².

A strict elliptical caustic requires 0<λ<b², so immediate return P_(i+2)=P_i is impossible. The canonical primitive rotation also excludes it, but the direct computation validates the written regularity proof independently.

Consequently three consecutive orbit vertices are distinct. Coincident consecutive outer intersections would supply three different tangents to one nondegenerate conic through one finite point, which is impossible. Thus T_i and T_(i+1) are distinct points on the supporting tangent at P_(i+1).

### Antipedal vertices

The original foci are strictly inside the outer ellipse. No supporting tangent contains one. Therefore the vectors T_i−F and T_(i+1)−F are independent, since otherwise the focus would lie on their shared supporting tangent. This is exactly the determinant needed to solve the two adjacent antipedal lines. Every claimed intersection is finite and unique. Convexity of the derived antipedal is not assumed.

## 3. Signed-area equality and domain

Central pairing of the orbit sends its actual ellipse tangents and outer vertices to their opposite indexed objects. Negation exchanges the two original foci and sends each corresponding antipedal line to its opposite-focus counterpart. The unique intersections satisfy Q_(i+N/2)(F−)=−Q_i(F+).

This reindexing is cyclic and preserves traversal. A half-turn in the plane has determinant +1. The two shoelace sums therefore agree, with no appeal to unsigned component areas or a positive denominator. This proves the full source equality for primitive even stars as well as convex orbits.

Division gives ratio 1 only on the common nonzero-area locus. At a common zero the literal quotient is 0/0. A selected constant extension is separate. The candidate correctly declines to assert that every exceptional fixed family has a nonempty defined ratio locus; the equality does not need that assertion. The zero certificate is a domain qualification, not a refutation of rational invariance.

## 4. Exact six-orbit and zero-area certificate

### Billiard and caustic

For a>1, C=a/(a+1), S=sqrt(2a+1)/(a+1), the six original vertices in the candidate are distinct and cyclically ordered on a strictly convex ellipse. Hence the closed physical orbit has least period six. At an off-axis vertex the incoming diagonal already has unit length, and its difference from the outgoing horizontal unit vector is precisely the outward normal. Axis reflections establish the remaining laws, with no square-root sign ambiguity. Strict convexity and distinctness exclude zero turning angles.

I checked all six chord covectors against the dual equation of the caustic with λ=C². Since 0<C²<1, the caustic is strict, nondegenerate, and confocal. Horizontal side tangencies are immediate from its minor semiaxis S; the four diagonals satisfy the same equation. These are genuine tangencies of physical billiard chords.

### Actual outer and antipedal intersections

I formed the ellipse tangent lines directly from the six original vertices and recovered every outer vertex in equation (8), rather than assuming the proposed outer hexagon. I then formed and intersected all six actual focal-antipedal lines. All six coordinate pairs agree with equation (9).

For independence from the author's half-angle substitution, I worked over Q(a)[c]/(c²−a²+1), scaling the physical y-coordinate by h=sqrt(2a+1). Thus the line inputs are rational functions of a with one quadratic radical. Projective cross products give each intersection. The scaled signed area is exactly

    h B(F+) = −4a(a+1)(a²−2a−2)/(2a+1),

and its radical coefficient is zero. This is precisely equation (10) after dividing by h. I separately checked the intermediate paired-shoelace identity in the named coordinates.

At a=1+sqrt(3), the critical quadratic vanishes and c=h. The parameter is greater than one, so the original orbit and strict caustic remain admissible. All six antipedal denominator norms and their denominator polynomials are coprime to a²−2a−2; no cancelled pole invalidates specialization. Adjacent antipedal edge lengths are also nonzero there. Hence the zero is a finite genuine signed-area cancellation, not an undefined vertex or a two-bounce artifact. The other focal area is zero by the universal equality.

The one-parameter construction changes the ellipse/caustic to select this example. It does not claim different defined ratio values within a fixed Poncelet family. No floating-point root or numerical caustic fit is used.

## 5. Reproduction and finite-control limits

- `INPUT_VERIFICATION.json`: all eight frozen author files and four primary PDF hashes match
- `AUTHOR_REPLAY.json`: the author's 11,448 exact assertions pass, with byte-identical output
- `independent_check.py`, `INDEPENDENT_CHECKS.json`: 20,376 separately authored exact assertions pass, including all six actual tangent and antipedal formulas, the field-area identity, normal-backtracking parameter, strict caustic identities, critical-root denominator checks, and 141 rational central polygon/star controls

The rational controls start from ellipse points, form their actual outer supporting-tangent polygon, and then its focal antipedals. They test derived geometry and signs; they are not asserted to be billiard orbits. The universal theorem rests on the credited classical pairing and the complete geometric argument. The exact six-orbit is separately validated analytically and symbolically.

## 6. Final scope

PASS applies to the exact arXiv k608 ratio on its natural domain and the stronger everywhere-defined signed-area equality, under the stated strict elliptical-caustic and primitive even-period hypotheses. It also applies to the explicit common-zero construction. Hyperbolic or degenerate caustics, repeated odd labels, unsigned region-area variants, universal quotient definedness, and novelty are not certified.

No author revision is required. Publication remains under the parent gate; this review does not itself create a PR or modify the queue.
