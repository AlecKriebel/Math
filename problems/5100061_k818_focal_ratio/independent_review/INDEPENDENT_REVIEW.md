# Independent source and dependency audit: 5100061 / original k818

2026-10-02. **PASS_CREDITED_COROLLARY_WITH_ESSENTIAL_DOMAIN_QUALIFICATION.** No mathematical revision is required. The result is a credited consequence of two existing reviewed proofs, not a new general invariant mechanism. The literal assertion of a finite ratio for every admitted family is false: an allowed family has a nonzero numerator and identically zero denominator.

The verdict binds TURN_1.md SHA256 `62fb2c9a1d7d8889d4ce52a935dcf7dd1e6bc87edc273daafc0e26fba9b594e3` and FROZEN_MANIFEST.json SHA256 `ae1654925e000dc21249dde9de3df17b836e582713a0f12a373929671dcbb9c9`. All eleven manifest-bound files match. No author file was edited. This is independent AI-assisted mathematical review, not human peer review, formal verification, or a priority certificate.

## Source and exact meaning

The primary source is [arXiv:2004.12497v11](https://arxiv.org/pdf/2004.12497v11). Table 9 on printed p. 11 was inspected visually: k818 is the focal inverse area divided by the focal antipedal area, with N congruent to 2 modulo 4. The source's preliminary ensemble is a strict noncircular confocal ellipse pair. Equation (1) specifies signed shoelace areas. Sections 3.5 and 3.9 specify antipedals from original-vertex focal rays and unit inversion about an original focus. These are exactly the packet's constructions, rather than outer polygons, unsigned filled regions, or curved images of edges.

Table 11 on printed p. 14 was also inspected visually. It already records a six-periodic, aspect-ratio-two antipedal with zero signed area. The packet appropriately credits that observation and supplies its own exact geometry verification. A literal all-family finite-valued statement therefore cannot be rescued by silently assuming every denominator is nonzero. The source's ordinary quotient is not automatically a projective invariant.

## Dependency identity, scope and mathematical use

Both full dependency proofs and their full reviews were read. All four included files match exact remote bytes at the following public commits:

- [k805 / PR 257](https://github.com/AlecKriebel/Math/pull/257), head `738075a78ae8e144d8398f6ab2f507ba8ae566d2`: proof SHA256 `bcff8a4f73aef132f9621a52eec0f853c94ffe1355cad4e2c30b84b8e63d7ac9`
- [k404 / PR 255](https://github.com/AlecKriebel/Math/pull/255), head `a624d16a87c5ee67a3ab23621b891e5991794071`: proof SHA256 `b8edd78d03dac33a7be77837649eef7a8558900b3499774725174836fa54d462`

The k805 proof establishes positivity and constancy of A/V for precisely the primitive 2-modulo-4 strict elliptical family, including coprime star windings. Its odd-half-period specialization aligns the inverse-area trace with the original-area trace. Thus its reciprocal gives V = cA with c > 0. The proof explicitly credits the generic trace mechanism from PR 207; this corollary does not create a second independent version of it.

The needed k404 result is not merely its final antipedal/pedal quotient. Sections 3–5 explicitly establish B = kA for every primitive even period. The antipedal coordinates have only the stated endpoint pole classes; symmetry cancels their possible double terms, leaving the same two simple pole classes and imaginary anti-period as the original-area trace. Residue matching and the holomorphic elliptic remainder give proportionality. Crucially, neither the argument nor its review assumes the coefficient k is nonzero. The later pedal positivity result is unnecessary here.

The canonical variables, focus, trajectory ordering and strict caustic hypotheses match. Both arguments allow stars and use signed area. The standard Jacobi periods, poles and shifts are consistent with [DLMF §22.4](https://dlmf.nist.gov/22.4); the direct edge identities use [§22.8](https://dlmf.nist.gov/22.8). This audit checked the written dependency chain and its use, but did not rerun the dependencies' large historical diagnostic suites; their unchanged full review reports preserve those checks. The present independently computed evidence is listed separately below.

## Division, positivity and exceptional families

For a point F strictly inside the caustic, every oriented tangent chord has det(P_i − F, P_(i+1) − F) > 0 when the caustic is on the left. The origin and both foci meet this condition. Consequently A > 0, and inversion divides each focal determinant by a product of positive squared distances, giving V > 0. This argument uses signed edge sums and does not require a star polygon to bound a simple region.

The two antipedal line normals are independent: dependence would put the chord through the interior focus, impossible for a caustic tangent. Inverse vertices are finite since the focus lies strictly inside the outer ellipse. Thus a zero signed antipedal area is a cancellation of finite oriented terms, not a failed line intersection or an inverse singularity.

The two accepted identities immediately imply the exact dichotomy:

- If k is nonzero, B never vanishes and V/B = c/k is a finite constant at every phase
- If k is zero, B is identically zero and V is nowhere zero, so the finite quotient is undefined at every phase

No division by k or B occurs before the nonzero condition. Since A is nowhere zero, the exceptional family is not a removable 0/0 case. The separately labeled homogeneous pair [V:B] = [c:k] is defined, including its infinite projective value, but this is an extension of the source expression.

The primitive-period restriction is explicit and necessary to the cited parity argument. Distinct coprime windings are allowed. Repeating an already admitted primitive orbit multiplies all signed areas equally; repeating an odd primitive orbit does not license changing its parity classification. Reversal negates all three areas, and the even half-orbit central reflection interchanges the original foci while preserving signed areas.

## Independent exact exceptional-orbit verification

A new checker, importing no author code, reconstructs the six orbit vertices, forms antipedals by homogeneous line cross products, and computes signed areas by triangulation from one vertex. It passes **165 exact assertions** with SymPy. It verifies:

- All six outer-ellipse incidences and pairwise distinctness, proving least period six once closure is established
- Strictly positive oriented edge determinants
- A strictly nested confocal caustic with squared semiaxes 32/9 and 5/9
- Tangency with each contact point strictly inside the corresponding segment
- Specular reflection through equality of tangential components and reversal of normal components of unit velocities
- Finite antipedal intersections and incidence on both defining lines
- Both original foci, orientation reversal, and the actual signed areas

The independent values are A = 20 sqrt(5)/9, V = 15 sqrt(5)/8, B = 0. In particular A/V = 32/27, also matching the credited simple-six-period formula in the k805 packet. Six distinct vertices rule out a doubled three-periodic or other lower-period traversal. The positive caustic axes and their strict inequalities rule out degenerate or hyperbolic cases.

The author checker also replays its 66-assertion receipt exactly. Finite controls verify this specific exception, not the universal proportionality; the latter follows from the reviewed dependencies. Since B/A = k is phase independent, this exact zero at one allowed phase proves the whole family's denominator is zero.

## Disposition

The natural-domain k818 statement is proved as a credited corollary after one substantive author turn. The appropriate campaign disposition is **already_solved 1/5 as a shared-proof corollary**, with the denominator qualification prominent in the result, queue note and any draft. This label describes derivability from the existing campaign results, not a claim that the original source authors had already published the general theorem.

Do not announce a finite quotient for all families or a new independent discovery. If the imported statement is instead read as demanding an everywhere-defined finite quantity, the exact six-periodic example refutes that reading. Both conclusions should remain visible. No correction to the frozen proof is needed.
