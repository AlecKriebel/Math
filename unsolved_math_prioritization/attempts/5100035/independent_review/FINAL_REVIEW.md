# Independent adversarial review: 5100035 / arXiv k607

**Verdict: PASS_COMPLETE_SOURCE_TARGET_ON_NATURAL_DOMAIN.** The frozen candidate proves the original arXiv ratio invariant wherever its quotient is defined, by proving the stronger equality of the two signed focal-antipedal areas for every primitive even elliptical-caustic orbit. Its explicit primitive convex eight-orbit has both areas zero, so the natural-domain qualification is necessary. This is not a counterexample to defined-locus invariance. The proof is a credited elementary consequence of classical central symmetry; this review certifies no novelty or priority.

Reviewed frozen `PROOF.md` SHA-256:
`9c7bb0a7c2549009ab69b82fc87f07e53d259c730ddd52c008fb5a394733b736`.

Reviewed `MANIFEST.json` SHA-256:
`8f9e97e65f893682c1184287397a77e19c055d4fc934db0ca3097667ee88c39a`.

All nine listed author files and three complete primary PDFs match their recorded hashes. No mandatory correction was found. Excluded exploratory files were not used as proof inputs.

## 1. Source and exact target

I separately read the primary definitions and visually inspected arXiv v11 Table 7, printed p.9. Its **k607 is the original-orbit focal antipedal-area ratio**, value 1, N congruent to 0 modulo 4. The final companion Table 7, printed p.349, has a different **pedal** ratio relation at code k607. The candidate correctly uses the arXiv target, not the final code alone.

The arXiv introduction specifies a confocal **ellipse pair**; Section 2 specifies a>b>0 and signed shoelace areas; Section 3.5 defines perpendicular lines through the original vertices and allows self-intersecting antipedals. These details support the stated strict elliptical-caustic and signed-area scope. Hyperbolic caustics are not silently included. The manuscript's parity is the period of the actual orbit; repeating an odd orbit's vertex list does not justify the half-turn conclusion.

Primary sources checked:
- Reznik–Garcia–Koiller, arXiv:2004.12497v11, 29 October 2020: https://arxiv.org/pdf/2004.12497v11
- Published companion, Arnold Mathematical Journal 7 (2021), 341–355: https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf
- Stachel, *The geometry of billiards in ellipses and their Poncelet grids*, Journal of Geometry 112, article 40 (2021), Corollary 4.2(i) and its proof, pp.22–23: https://doi.org/10.1007/s00022-021-00606-2

The Stachel result explicitly has an elliptical caustic and even N with odd turning number. The preceding splitting discussion and canonical rotation description justify the primitive coprimality condition. Thus primitive even stars are included. The distinct hyperbolic-caustic corollary is not an input.

## 2. Universal geometry and area identity

### Finiteness

For focus F, the two antipedal normals at consecutive vertices are P_i−F and P_(i+1)−F. Dependence is equivalent to the billiard chord line containing F. Each focus lies strictly inside the nondegenerate confocal caustic, so no caustic tangent can pass through it. Both normals are nonzero, all adjacent intersections are finite and unique, and no convexity of the antipedal is needed.

### Central inversion and signs

The cited source gives P_(i+N/2)=−P_i. The half-turn exchanges foci and sends the line through P_i perpendicular to P_i−F+ to the corresponding line at index i+N/2 for F−. Unique adjacent intersections therefore satisfy Q_(i+N/2)(F−)=−Q_i(F+).

The index map is a cyclic shift. It is not an orientation reversal. The determinant in dimension two is unchanged when both endpoints are negated, so the full signed shoelace sums agree. This proves equality for all primitive even N and, in particular, the original N divisible by four target. An unsigned decomposition into regions is neither necessary nor substituted for the source's signed area.

### Quotient domain

Equality implies ratio 1 precisely when the common area is nonzero. At common zeros, the displayed quotient is undefined. Cancelling the common area as a rational invariant gives the constant extension 1, not an ordinary evaluation of 0/0. The extension should retain that label even if one restricts to a family on which the raw denominator vanishes identically. The candidate preserves this distinction and does not use the zero example to claim the invariant is false.

## 3. Independent audit of the exact eight-orbit

Let f(t)=t^4−6t^3−2t^2−2t+1. The exact endpoint signs at 3/10 and 1/3 are as stated. On (0,1/3), f'(t)<4/27−2<0, giving a unique root in the proposed interval.

For C=(1−t²)/(1+t²), S=2t/(1+t²), R=(1−t)^3(1+t)/(4t³), the root interval implies 0<S<C<1 and R>2>1. Thus the positive a=sqrt(R), b=1, c=sqrt(R−1) are genuine noncircular ellipse data. The eight listed points are distinct in counterclockwise order on a strictly convex ellipse. Consecutive sides are nonzero, and the orbit has least period eight, not merely a repeated four-orbit.

I checked the positive chord-length ratio after squaring, then used positivity to recover the unsquared ratio. The incoming-minus-outgoing unit directions have zero determinant with the ellipse normal and a positive normal multiplier. Unit length makes this exactly the specular reflection law. Axis symmetries cover the other vertices; convexity precludes zero turning angles.

I independently formed all eight chord covectors and verified their tangency to the confocal ellipse with lambda=R(1−C)^2/[R(1−C)^2+S²]. Its denominator is positive and 1−lambda=S²/[R(1−C)^2+S²]>0, so 0<lambda<1. The caustic is strict and nondegenerate and has the stated foci. This validates the configuration before the area formula is used.

For the area calculation I used scaled coordinates X=aU, Y=V and the quadratic field Q(t)[e]/(e²−(1−1/R)), where e=c/a. I formed line coefficients and projective cross products independently of the author's elimination code. The signed area divided by a reduces exactly to

    (t²−2t−1)(t⁴−6t³−2t²−2t+1)/(4t³),

with zero radical coefficient. Every antipedal intersection denominator norm is coprime to f(t), so no hidden denominator is cancelled at the selected algebraic root. The same independent calculation confirms adjacent antipedal vertices remain distinct there. Thus this is a genuine finite, nontrivial signed-area-zero antipedal. The other focal area vanishes by the universal equality.

The construction varies ellipse/caustic data to select an admissible pair. It does not purport to demonstrate variation of the quotient among phases of one fixed family. No floating-point root is used as a certificate.

## 4. Reproducibility and controls

- All frozen author and primary-source hashes verified: `INPUT_VERIFICATION.json`
- Author checker replay: 3,297 exact assertions; output matches `exact_receipt.json` byte-for-byte, saved as `AUTHOR_REPLAY.json`
- Separately written `independent_check.py`: 15,826 exact assertions, including the quadratic-field area identity, all eight dual-conic tangencies, denominator/root coprimality, nonzero derived edges, and 207 central rational polygon/star-order controls
- Independent receipt: `INDEPENDENT_CHECKS.json`

The generic rational polygons test Euclidean equivariance and signed orientation only; they are not claimed to be billiard orbits. The genuine eight-orbit is checked by the symbolic certificate and the written positivity arguments. Finite tests do not replace the source theorem or universal geometry.

## 5. Disposition

The source-aware full result is complete after the author's first substantive turn and requires no artificial additional unsuccessful turns. It may be presented as a classical-consequence proof of the exact arXiv ratio invariant on its natural domain, with the explicit 0/0 qualification retained prominently. The stronger even-period equality is also valid under the stated primitive elliptical-caustic scope.

No claim is certified for hyperbolic/degenerate caustics, repeated odd labels, unsigned region-area ratios, or the different final-edition k607. This review does not authorize publication; the parent retains that gate.
