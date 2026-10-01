# Independent full review: 5100046 / original arXiv k805

## Verdict and binding version

**PASS_COMPLETE_CREDITED_COROLLARY. No mandatory correction.**

The verdict binds the unchanged PROOF.md SHA256 bcff8a4f73aef132f9621a52eec0f853c94ffe1355cad4e2c30b84b8e63d7ac9 and FROZEN_MANIFEST.json SHA256 7f111a1d26d79414ab40e4c7d02a8a7cd9867a8cdccb1393d45b1a7e7d61498f. All thirteen author files and four source PDFs match. The complete source-target theorem, analytic proof and everywhere-defined real quotient are accepted under the stated strict elliptic-caustic assumptions.

The proposed **already_solved, 1/5** classification is appropriate as a credited shared-argument consequence of PR207, rather than a separate discovery. This does not assert that the exact all-period statement was already explicitly published by the source authors. The N=6 published result is credited separately.

This is an independent AI mathematical audit, not human peer review or certification of novelty. The reviewer has authored/reviewed other billiard packets and had read and byte-verified PR207 as an input for the separate k817 task before reading this candidate. The reviewer did not contribute to this k805 derivation. Shared prior-input knowledge is disclosed; the present source/parity/domain change and all proof steps were independently rechecked. No author file was changed.

## 1. Exact source and domain

The source target is the signed original-orbit area divided by the signed area of straight edges joining its unit focal-inverse vertices, for primitive N=2 modulo 4. It is not an outer-vertex, outer-locus-focus, elliptic-inversion, perimeter or curved-side-image assertion. Both original foci are supported.

The arXiv Table 9 row, the final companion's omission, and the later accepted-manuscript k806 row and Proposition 4.16 were checked directly. The later ratio's rho^-4 factor and simple-N=6 formula agree with the candidate. Full details and locators are in SOURCE_AUDIT.md.

A strict nested elliptical caustic has c<alpha and contains both foci and the origin in its interior. Its tangent chords therefore have strictly positive oriented edge/point determinants when traversed consistently with the caustic on the left. This orientation is available for the canonical elliptic-caustic trajectory, including stars. Independently, equation (8) proves the same sign directly: every real factor is positive for 0<v<K and 0<k<1. This avoids any implicit appeal to an unsigned star interior.

Original area is positive by summing the edge determinants about the origin. Unit inversion divides the determinant about a focus by the product of two positive squared focal distances, so every inverse edge determinant and its total area are positive. The distances have lower bound a-c>0. The denominator and the eventual proportionality constant are therefore nonzero everywhere. Reversing traversal negates both signed areas and leaves the ratio positive. Hyperbolic or degenerate caustics are not covered.

## 2. Canonical parametrization and trace factor

Stachel's theorem applies with k=c/alpha, not the numerical library parameter k². Its axes a=alpha dn(v)/cn(v), b=beta/cn(v) and step delta=4K tau/N are correct. For N=2m with m odd, primitivity forces tau odd and gcd(tau,m)=1; m delta=2K modulo 4K gives the antipodal pairing. N=2 cannot satisfy 0<tau<N/2, so the target starts at N=6.

The original edge determinant and dn addition formula reproduce A=2 C_A S for the m-term trace. The factor 2 is correct: the N-term trace consists of two identical m-term halves. The shifts j delta form all m classes modulo 2K, so S has the reduced real period ell=2K/m. At its pole representative exactly one m-term summand contributes; the residue is nonzero. Thus there are exactly two simple poles on the quotient torus with periods ell and 4iK', exchanged by the anti-period 2iK'. No unproved even-m restriction enters these facts.

## 3. Ordinary distances, inverse edges and pairing

I reconstructed both Jacobi endpoints P(u-v),P(u+v), their translated cross product and ordinary focal distances without importing the author checker. Reducing the resulting expressions by the Jacobi quadratic identities verifies equations (5), (7), (8) and (9). In particular the inverse half-edge uses the square of the product of ordinary distances, which is exactly the product of their squared lengths required by Euclidean inversion.

The real distance identity a+c sn(w) has its positive sign fixed by a-c>0. The constants U,V,W are normalized consistently. A useful independent positivity decomposition is

    U=(1-t) dn²(v)+(1-k²)t>0.

Together with U²-k²V²=(1-k²)W²>0 this proves U>|kV|, as required for real nonvanishing. The antipodal sum gives the stated rational B. Its power of alpha is correct: inverse area has inverse length-squared scaling for fixed unit inversion.

## 4. Complete generic pole analysis for odd m

V=0 is equivalent to cn(delta)=0. Since 0<delta<2K, it would force delta=K, or tau/m=1/2, impossible when m is odd. The previous N=4 exception is therefore genuinely absent, rather than overlooked.

At r=K+iK', dn has a simple zero and the other factor is U²-V²=(U-V)(U+V)>0. This gives at most a simple pole. The additional denominator factor is an affine function of sn² with one double pole in the smaller sn² torus. Its zeros are r+delta and r-delta. They are distinct because delta is not K, and neither equals r or the common Jacobi pole. Consequently they exhaust the two-zero divisor and are simple; squaring that factor gives at most double poles of B.

At the common Jacobi pole the numerator has order at most four while the denominator has order five, so B is removable. The fixed constants do not vanish in the strict domain. These checks account for every possible complex pole, not merely the real denominator.

Reflection about r leaves sn unchanged and reverses dn, so B(2r-u)=-B(u). Hence the order-two coefficients at r+delta and r-delta are opposite. In the cyclic sum, at every real pole class exactly one translate of each type contributes, and they cancel. The ordinary r-type contributes at most a simple pole. For m=3 all three types identify only after passage to the quotient; their contributors are still distinct on the base torus. The count and cancellation remain valid. Vanishing leading coefficients can only lower the order and are not excluded.

Thus R has at most the two simple poles of S(u+K), the same reduced real period and the same imaginary anti-period. Matching one residue matches the other automatically. The remaining holomorphic elliptic function is constant, and its anti-period forces zero. This proves R=C_R S(u+K) without using an even-half-period theorem outside its scope. On the real line R and S are positive, so C_R is real and positive.

## 5. Final parity, focus and published value

The sole final parity specialization is exact:

    (K+v)/ell=(m+tau)/2 is an integer.

Thus A_inverse(w)=C_R S(w), and division by its positive value gives the claimed constant 2C_A/C_R. This is precisely the change from PR207's even-m half-integer shift and product theorem. It is not a numerical extrapolation.

The half-orbit central inversion exchanges the two original foci, cyclically relabels vertices and preserves oriented area. It intertwines the two unit inversions, proving equality of their areas. Repetition claims are confined to underlying primitive families already covered; an arbitrary indexing parity is not used.

The N=6 expression matches the actual published accepted-manuscript Proposition 4.16, including rho^-4. It is a credited normalization control, not the proof for arbitrary N.

## 6. Reproduction and independent evidence

All thirteen frozen author hashes and all four pinned source hashes match. The author output replays byte-for-byte: 6,631 exact assertions and 10,947 separately labeled 80-digit diagnostics.

The independently written checker imports no author code. It passes:

- 71,664 exact assertions, including direct endpoint/distance/inversion algebra and complete pole-type multiplicity accounting for 651 primitive rotation choices
- 7,512 separate 110-digit diagnostics, covering direct Euclidean inversion, both foci, strict edge signs, the published N=6 value and 24 near-pole/removable-point cases
- Near-pole cases include r, r+delta, r-delta and the common Jacobi pole p, with the smallest m=3 case, nonconvex stars and high eccentricity
- Maximum scaled numerical discrepancy is about 1.43e-87

These finite controls corroborate the analytic audit. They are neither an exhaustive classification of all real parameters nor a substitute for the compact-torus proof.

## Publication disposition

The unchanged candidate is suitable for one source-qualified, credited-result draft at already_solved 1/5, subject to the parent publication gate. Retain the original arXiv code and exact final/later edition map, signed primitive-star scope, strict positive denominator, explicit PR207 shared credit and no-novelty qualification. No mathematical or metadata correction is required.

Portable review files are listed by REVIEW_MANIFEST.json. Exclude reading/ and all PDFs, extracted full texts and rendered pages. No merge, release or external outreach is part of this review.
