# Independent adversarial review: 5100063 / k904,a

**Verdict: PASS for the full stated odd-primitive-period theorem, including primitive stars. No mathematical correction is required.** This is an independent mathematical audit of the submitted proof, not a certification of novelty, minimality, historical priority, or human peer review.

Reviewed on 2026-10-01. The theorem concerns the product of the two signed straight-edge areas obtained by unit inversion of the **outer tangent-polygon vertices about the original billiard foci**, for a strictly nested nondegenerate confocal ellipse pair. Hyperbolic and collapsed caustics are not included. The circular case is a separate rigid-rotation limit argument.

## Frozen version and independence

- `PROOF.md`: SHA-256 `9640ed4bc6c6b0b56f0235c0e28513e9c3ca94c53cb75d2cb2eecee5b45b075e`.
- Final author `MANIFEST.json`: SHA-256 `385173cbcd9b0397a9da93cf35ecd65e22160e520e6ca6303e5213035bee6f8b`, binding eleven author files.
- Original supplied manifest: `038a3a852785af8bd0a1d12b1c6bd5cfd2c872221ff8adaa99e8c87a45fb1103`.
- The only change during review was a source-navigation correction in `SOURCES.md`: the own-outer-locus-focus discussion is in Section 3.9, printed p. 10, rather than Section 3.10. Corrected source-note SHA: `ce1efd2e74be4e575fc0225b9eab0216f6d52c562d67d60dd4781ed8221e700f`. The proof, author checker and author check output are unchanged. This correction is incorporated in the final manifest above.

All eleven author artifacts and all three primary PDF hashes were verified. The complete author proof, source notes and checker were read. The author's self-writing checker was not executed or used to generate the independent results. The separate checker in this review was written from the tangent equations, Euclidean inversion, Jacobi identities, and quotient-lattice argument.

The reviewer did not contribute to this candidate. Previous reviewer-authored focal-pedal work used standard Jacobi functions but supplied no lemma to this outer-inverse-area proof. The author's earlier k115 and k804,a work is transparently credited in the candidate; k903,a is not used as a black-box theorem.

## Exact source and mathematical objects

I independently rendered and inspected [Reznik–Garcia–Koiller, arXiv:2004.12497v11](https://arxiv.org/abs/2004.12497v11), Table 10, printed p. 12. Its k904,a row has the product of the two primed dagger areas, odd N, and an unproved marker. Section 3.9, printed pp. 9–10, defines unit-circle vertex inversion about the original foci and applies the primed notation to the outer polygon. The own-locus-focus operation is separately marked with a different symbol and belongs to k906. Section 2, printed p. 3, defines signed cross-product area. Thus the proof addresses the actual assigned table entry. It does not substitute original-orbit vertex inversion, chord-pedal area, or an arc-enclosed region.

The shorter published *Fifty New Invariants* companion has no 900-series table. Its omission is accurately disclosed rather than treated as an unchanged published conjecture. The canonical parametrization matches [Stachel, Theorem 4.3 and equation (4.9), printed p. 1614](https://doi.org/10.1007/s40879-021-00524-2): the modulus is the caustic eccentricity, and numerical-library parameters must be its square. The statement includes every coprime turning number in the chosen orientation. Reversing orientation changes both area signs and preserves their product. If a repeated odd-period traversal is contemplated, its signed areas simply scale by the repetition count, so no new obstruction arises; it does not change least-period parity.

## Algebraic audit

1. **Actual outer vertices.** Substituting the proposed outer point into the two tangent equations gives 1 exactly. The real tangent-line determinant is nonzero because sn(v), cn(v), dn(u), and the relevant addition denominator are positive in the stated range. The outer semiaxes exceed the corresponding billiard axes; hence every outer point lies outside the original ellipse, and no original-focus inversion is undefined. No ordering of the two outer semiaxes is assumed.

2. **Squared distance.** The factorization in equation (5) was checked by expanding the bilinear squared norm of the proposed outer point translated by the original focus. This uses the original focus coordinate alpha k. Replacing it by the eccentricity of the outer locus would change the factorization and is not permitted.

3. **Inverse edge normalization.** I independently substituted Jacobi addition expressions for sn(u±v), cn(u±v) into the translated two-point determinant and both distance factors. The three exact identities (9)–(11) and their assembly reproduce equation (8), including q^4, the positive coefficient, and the alpha scaling. The independent diagnostics also use alpha=1.37 instead of normalizing every family to one, so an omitted dimensional factor would be detected.

4. **Triple-angle factors.** Starting from the double-angle functions and one more addition, the independent symbolic checker recovers L0=Z dn(3v) and L1=Z cn(3v), and their squared gap k'^2 Z^2. Since Z>0 and dn(3v)>0 for real arguments, both denominator factors are positive on the real axis. Thus every centered inverse edge in the selected orientation is positive and the cyclic function cannot vanish identically. Odd primitivity excludes cn(3v)=0. These are strict inequalities for each nondegenerate family, with no uniform limit estimate asserted near k=0 or k=1.

## Meromorphic audit, including exceptional multiplicities

The periods and half/quarter shifts were checked against [DLMF 22.4](https://dlmf.nist.gov/22.4); addition identities against [DLMF 22.8](https://dlmf.nist.gov/22.8). The complex squared norm is bilinear, with no conjugation, as needed for meromorphic continuation.

- On the sn lattice 4K Z + 2iK' Z, the first affine sn factor has precisely the two displayed roots r0±v. They are simple: its sn value has magnitude greater than 1/k, so it is none of the four branch values ±1, ±1/k. The squared factor gives at most double poles.
- The second factor has roots r0±3v. Apart from the N=3 case these roots are distinct and simple. The possible critical value corresponds to 3v=2K, and coprimality forces exactly N=3, tau=1. Cases cn(3v)=0 are excluded by oddness and the real parameter range, so the second factor is never constant.
- In that N=3 case its factor is proportional to 1-k sn(u). At u=K+iK' it has a double zero. Indeed its second derivative there is k^2-1, nonzero, while dn has a simple zero with derivative square k^2-1, also nonzero. The remaining order is at most one. This exceptional cancellation is essential and is present in the candidate.
- The two first-factor roots cannot meet a second-factor root because that would make 2v or 4v a period 4K; the strict interval excludes it. Common poles of sn, cn, dn are removable in the reduced edge expression: numerator and denominator have the same third-order pole and the leading denominator coefficients are nonzero. This accounts for the complete pole list, not merely those seen in samples.
- Reflection about r0 preserves sn and reverses dn, so the edge function is odd under that reflection. A Laurent expansion at the reflected double poles therefore has opposite quadratic coefficients. Since their separation is the billiard step delta, the cyclic sum cancels those coefficients at every translated location. Contributions from the other factor already have at most simple order, including when its N=3 roots coincide.
- Coprimality gives real period L=4K/N. On the explicitly chosen quotient lattice L Z + 4iK' Z there are at most two simple poles, separated by 2iK'. Anti-periodicity pairs them. If both were removable, compactness and anti-periodicity would force the cyclic function to be identically zero, contradicting the strictly positive real sum. They are therefore exactly two simple poles. No claim that the displayed lattice is the maximal period lattice is needed.
- Odd reflection about the pole class forces zeros at its real half-period translates. These are distinct from the poles, distinct from each other on the stated lattice, and exhaust the zero divisor with simple multiplicity. Thus the half-period product has no poles on a compact torus and is constant.
- Central reflection of the actual outer vertices identifies opposite-focus inversion with the phase shift 2K. For odd N this is L/2 modulo the cyclic real period. Central reflection preserves oriented two-dimensional area; the phase/focus identification therefore proves exactly the required product.

These checks establish the all-period proof. They do not rely on a finite verification of many N values or on importing the original-vertex k903,a theorem.

## Independent reproducible checks

`independent_check.py` passed:

- 8,438 exact symbolic and rational-lattice assertions, including all 1,053 coprime odd rotations with N≤101;
- 5,412 separate 90-digit numerical diagnostics over 54 families, with moduli 0.07, 0.61, 0.96 and periods 3, 5, 7, 9, 11, 15, including all primitive stars in those periods;
- direct tangent intersections, actual Euclidean focal inversions, signed shoelace areas, reversed order, complex edge normalization, reflection, imaginary anti-periodicity, and both quotient zeros;
- maximum scaled diagnostic error 3.09273494625e-88;
- an exact even-period calibration: the same (4,3) billiard and (16/5,9/5) caustic yield inverse-area products 1/144 and 625/82944 for the diamond and axis-rectangle orbits. This demonstrates why the odd scope cannot be silently removed.

Numerical checks are high-precision diagnostics, not interval certificates. The finite symbolic and lattice controls supplement the universal argument audited above. Reading-copy PDFs and page renderings are excluded from the portable review package.

## Final disposition

The unchanged mathematical proof passes adversarial review for its stated scope. Preserve the exact original-focus, outer-vertex, unit-inversion, signed-area and odd-period conventions in any result summary. The only requested correction was bibliographic navigation and is already incorporated in the final source manifest. Any publication remains subject to the parent's authorized publication workflow; this review does not assert novelty or resolve neighboring invariants.
