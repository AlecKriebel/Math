# Independent review: 5100033 / arXiv k605,a

**Verdict: PASS_COMPLETE_SOURCE_TARGET.** The unchanged mathematical candidate proves the product invariance for the two signed focal-pedal areas of the outer tangent polygon, for every odd primitive period and turning number in the stated nondegenerate confocal-ellipse scope. No mathematical revision is required. This verdict does not certify historical novelty.

## Exact version and independence

- `PROOF.md` SHA-256: `5a78b9d2fb1f7a0a80e556f2e2b759875bdbba055a454c148524eb44879add7e`
- Current author `MANIFEST.json` SHA-256: `d6878cde56ffa2b0233826c15a99adfa643746a73c91ca826b00ea3f8f8a28ca`
- Initial author manifest SHA-256: `94df61c022921db05dc80bd53b9c823d6b13afc6fc6e704baf6dba2507d3227d`

All 13 current manifest entries and all three source PDF hashes were independently checked. The sole correction requested during review was bibliographic: the precise arXiv v11 PDF is dated **29 October 2020**, not 2021. The published companion remains 2021. The correction has been verified; `MANIFEST_V1.json` and `METADATA_CORRECTION.md` preserve its provenance. The proof and checker were not changed.

The reviewer did not contribute to this candidate before its freeze. The reviewer has worked on distinct nearby billiard invariants; this is therefore an independent audit of this exact construction, not a claim that the reviewer had never encountered elliptic-function invariant methods. The author's disclosed use of the general two-pole framework is appropriately credited.

## Source identity and scope

The [arXiv v11 source](https://arxiv.org/pdf/2004.12497v11), Table 7, p. 9, has the primed-area product under k605,a. The [published companion](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Table 7, p. 349, has that same product under **k606**. Published k605 is the different original-orbit pedal product. Both tables were read and visually checked. Section 3.7 identifies the primed polygon, and Section 2 specifies signed cross-product area and the confocal-ellipse setting with a>b>0.

[Stachel's published canonical theorem](https://doi.org/10.1007/s40879-021-00524-2), Theorem 4.3 and equation (4.9), p. 1614, was read and independently rendered. Its modulus convention, semiaxes, factor of two in the phase increment, and coprime turning-number condition agree with the candidate. The checker correctly passes k squared as the numerical Jacobi parameter.

The ordinary feet are projections onto outer side **lines**, with the original billiard foci as centers. The finite outer side segments do not impose a clamping operation. The proof concerns signed areas even for star orbits. It never substitutes unsigned enclosed-region area, original chord projections, antipedal vertices, or the foci of a different derived ellipse.

The theorem is stated for least period. If the source's notation is also read to allow an odd repeated traversal, its extension is immediate: both area sums multiply by the odd repetition count, so their product multiplies by its square. This does not supply an independent new target. The circular comment is valid because the two foci coincide with the rotation center; hyperbolic and collapsed caustics remain outside the claim.

## Adversarial mathematical checks

### Real geometry and meromorphic map

The reviewer recomputed the perpendicular projection from the tangent normal. Canceling the common factor gives precisely equation (3). The real denominator is positive because a>c. The auxiliary-circle identity is an algebraic identity, not a numerical observation. Negating the original point and switching the focus gives equation (4). Consecutive outer intersections have the original tangents as their side lines in the same cyclic order, up to a harmless cyclic shift. The canonical phase increment is not a half-period, so those intersections remain finite on the real family.

### Exhaustive complex poles and their orders

The classical period/shift identities were checked against [DLMF 22.4](https://dlmf.nist.gov/22.4), with the derivative rule checked against [DLMF 22.13](https://dlmf.nist.gov/22.13). The common poles of sn and cn are removable in the projected foot. The two roots of the remaining denominator on the sn torus are exactly K+iK' minus/plus v. Both are simple: neither cn nor dn vanishes at either point when 0<v<K and 0<k<1. The degree-two count excludes unlisted roots. Doubling the imaginary period introduces only their indicated translates.

The numerator vectors at the adjacent poles agree; their denominator derivatives differ by a sign. Therefore the residues are opposite and collinear. This is the decisive audit point: adjacent singular vertices actually occur, so a termwise assertion that only one endpoint is singular would fail. The determinant's nominal double-pole coefficient vanishes exactly. Primitivity ensures that there are precisely two such singular vertices in each pole orbit, including N=3 and the edge across the cyclic index cut. All remaining terms have at most simple poles.

### Reduced lattice, signs, and cancellation

The area sum is invariant under both the billiard step and the true real period. Their integer gcd yields the reduced period L=4K/N. On the torus with periods L and 4iK', there are at most two simple poles. The imaginary half-shift reverses one coordinate and hence the area sign. Reflection reverses both the cyclic order and the planar orientation, giving an even area function rather than an odd one. The shift of its reflection center from K to K-v is justified by the actual step period.

For the centered function F, evenness and the imaginary anti-period force zeros at the real-half-period translates of both possible poles. These points are distinct and are not poles. If poles disappear, compactness and the anti-period force F to vanish identically. Otherwise both poles are simple, the zero count is exactly two, and the translated product has no poles anywhere. Compactness makes it constant. This uses no division by an area or nonzero residue of the area sum. Odd N makes focus switching precisely the required half-period modulo L. Every coprime star turning number is covered.

## Independent checks

`independent_check.py` and `INDEPENDENT_CHECKS.json` record:

- 9,303 exact assertions: rational projection/auxiliary-circle identities and cyclic-divisor checks covering 1,104 primitive rotations through period 103
- 4,941 numerical comparisons at 85 decimal digits, across 27 real families and 27 complex pole cases
- Real vertices advanced by direct Euclidean ray/ellipse intersection and reflection after initialization; actual outer intersections followed by direct Euclidean side projection
- Complex checks of both characters, the predicted zero, opposite residues, cancellation of the potential double pole, and continuation of the product near a pole

The reported maximum scaled numerical residual, about 1.19e-39, includes a finite-epsilon Laurent comparison; it is not an error bound on the universal theorem. The separate finite-epsilon residue residual is about 6.49e-19. All tolerances and precision are explicit in the checker. These are non-interval diagnostics, not a proof by numerical sampling.

The author program was inspected before replay. Its exact and numerical controls, including wrong-parity tests, complement the independent checks. The replay is byte-identical to the frozen author receipt: 20,718 exact assertions and 15,076 numerical comparisons, including eight complex pole cases and eight wrong-parity controls. Its output is preserved separately in `author_replay.json`; these counts are not part of the independent counts and are not universal certification.

## Disposition and publication limits

The exact frozen mathematical proof passes. A fresh exact-ID repository search found no earlier matching PR. The original source marks the row as conjectural, but neither that historical mark nor a limited current search establishes novelty. Preserve the Stachel and classical-input credits and the source-edition distinction.

The portable review package contains this report, the independent checker and receipt, the author replay, and the review manifest. Source PDFs, extracted full texts, and rendered pages are excluded. Publication remains the coordinator's gate; this review made no external write to the candidate branch or queue.
