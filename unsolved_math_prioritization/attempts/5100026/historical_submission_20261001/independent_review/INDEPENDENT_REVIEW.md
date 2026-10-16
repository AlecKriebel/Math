# Independent full review: k407 / 5100026

## Binding verdict

**PASS_COMPLETE_SOURCE_TARGET. No mathematical correction is required.** The unchanged proof establishes the outer focal-antipedal **vertex centroid** invariant for every primitive even period in the stated strict confocal elliptical-caustic setting, including primitive stars and the separate least-period-four case.

This verdict binds:

- `PROOF.md`: SHA256 `77afb7626fd4685b9ce7537aa2de3141df8bf087c5eff0698bb1f7834bc0ad7c`
- `FROZEN_MANIFEST.json`: SHA256 `8e1d25905cea97a67026dc9f37b9af3047a976e8a4b02431ea93de789c3d0e9d`, covering all fourteen author files

One minor bibliographic correction is recorded below. It does not change the inspected source row or mathematics. Frozen author files remain unchanged.

The reviewer had no role in this candidate's derivation. The reviewer has authored related area-invariant work using the same classical Jacobi framework, but did not supply the present focal-removal or vertex-residue cancellation argument. This is a separate adversarial AI audit, not human peer review or certification of historical novelty.

## 1. Source and construction audit

The full arXiv v11 and final paper were inspected, including rendered Table5 pages. Both list k407 as C0 prime star, even N, with M an original billiard focus. Section3.5 identifies C0 as the arithmetic vertex centroid and C2 as the signed-area centroid. A zero signed area therefore does not invalidate the object under review. The outer vertices are successive original-tangent intersections; the antipedal lines through those vertices are perpendicular to their vertex-minus-M vectors. Neither an original-polygon antipedal nor a pedal polygon is substituted.

The title in author `SOURCES.md` item1 should read **Eighty New Invariants** for arXiv2004.12497v11. **Fifty New Invariants** is the final companion's title. The URLs, Table5 identification and mathematical mapping in the frozen packet are correct. The author acknowledged this narrow title correction and will preserve it in the publication disposition. This review incorporates the correction explicitly.

Primary sources:

- [Reznik–Garcia–Koiller, arXiv v11](https://arxiv.org/pdf/2004.12497v11), Section3.5/Table5, printedpp6–7
- [Final companion](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), definitions on printedp347 and Table5 onp348
- [Stachel, On the motion of billiards in ellipses](https://doi.org/10.1007/s40879-021-00524-2), Theorem4.3 and equation(4.9), full published PDF inspected
- [DLMF periods, poles and shifts](https://dlmf.nist.gov/22.4), [addition identities](https://dlmf.nist.gov/22.8), and [derivatives](https://dlmf.nist.gov/22.13)

All three pinned PDF hashes match the author's manifest. The canonical modulus is the caustic eccentricity k; numerical software receives parameter k². The genuine source hypothesis is a nondegenerate confocal ellipse pair. Hyperbolic and collapsed caustics, moving inversion/reference points, and parity manufactured by repeating an odd primitive orbit are not asserted.

## 2. Canonical parametrization and the real domain

Stachel's parametrization covers the stated primitive turning numbers. With even N and gcd(tau,N)=1, tau is odd, and shifting N/2 vertices is exactly a central reflection. The common Euclidean normalization of the caustic's major axis preserves perpendicularity and centroid invariance; it is not an anisotropic affine normalization.

I checked the outer vertex formula against the two actual original tangent equations. Its half-step convention is consistent: R(u) is the intersection of the tangents at P(u−v), P(u+v). Consecutive R(u−v), R(u+v) therefore share the tangent at P(u). Translating the outer starting parameter changes no centroid-invariance question.

The real determinant is

`det(R(u−v)−M,R(u+v)−M)=2 B s d dn(u)(a+k sn(u))/D0`.

Every factor has the required sign for M=(k,0): s,d,B>0, dn(u)>0, D0>0, and a+k sn(u)≥a−k>0. It remains nonzero at N4. Central reflection gives the other focus. Thus all real antipedal vertices are unique and finite at every phase, including stars. No area denominator is used anywhere in the centroid proof.

## 3. Complete complex singularity audit

The common 4K,4iK' torus is valid for all coordinates. Bilinear squared norms are essential; no complex conjugation appears. Cramer's rule gives meromorphic coordinate functions. I checked each possible singularity separately rather than assuming a generic pole picture.

### dn zeros

At K+iK' and its translates, the two finite outer endpoints coincide. D0=c² is nonzero and the remaining focal determinant factor is a±1, nonzero since a>1. Hence the determinant has a simple zero, while both Cramer numerators vanish. The quotients are removable. This is not an assumption that the singular complex line pair itself determines a unique point.

### Common midpoint Jacobi poles

The endpoints at u±v are regular at a common midpoint pole. The explicit determinant has a finite nonzero limit: its numerator and denominator both have order two, with nonzero leading coefficients. Therefore the coordinate quotients are regular. No pole at this class is omitted merely because the displayed determinant has an apparent denominator.

### Focal determinant roots

At sn(u)=−a/k, both cn(u) and dn(u) are nonzero, so the zero is simple. The original tangent at P(u) passes through M and has isotropic normal: its squared norm is zero by a²−b²=k². Its orthogonal direction in the complex plane is also isotropic. Both endpoint-minus-M vectors consequently have zero bilinear norm, so the two Cramer numerators vanish.

The only possible overlap with an endpoint pole solves s²a²=1. Its admissible root is s²=1/(1+k'), hence v=K/2, and primitivity forces N4. For N≥6 the endpoints are finite and the determinant zero is simple, establishing removability. This is the step that uses the **original focus**. It would fail for a generic fixed point.

### Endpoint poles

The zeros of D0 are precisely the shifted common Jacobi poles u±v. The two endpoints cannot both be singular because 0<2v<2K. The other endpoint is regular; dn and sn at the midpoint are finite and nonzero. For N≥6 the focal factor is also nonzero by the preceding overlap calculation. Therefore the determinant has a simple pole, each Cramer numerator has order at most two, and the antipedal vertex has at most a simple pole.

The degree-two sn fiber and the explicit determinant exhaust all possibilities, including translates by2K and2iK'. This audit found no additional critical or coincident class requiring an unstated assumption.

## 4. Four incident residues and global constancy

At a possible pole of the complete cyclic sum there are precisely two singular outer vertices, separated by N/2 indices. Their leading vectors are L and−L. The Jacobi reflection around a common pole makes their finite neighbors Q and−Q. This remains true at every translated pole.

I independently derived the residue using homogeneous line coefficients. For R(z)=L/z+A+O(z), the antipedal line, multiplied by z², has first two coefficients zL+O(z²) and constant coefficient −L·L+O(z). Crossing it with the regular line at Q shows that the intersection has residue

`(L·L)(Q_y−M_y,−Q_x+M_x)/det(L,Q−M)`.

Its denominator is the nonzero leading determinant coefficient already established in the local analysis. This reproduces the two leading equations in the author proof and its sign convention. The opposite singular vertex replaces L by−L; the four actual incident residues sum to zero. The formula also handles an isotropic leading vector without division by L·L.

For N≥6 the four incident edge indices are distinct. The residue cancellation therefore neither omits an edge nor counts an edge twice. Since each local pole has order at most one, cancelling the residue removes the full singularity. Both coordinates of the sum are then holomorphic on the compact torus and hence constant.

Reflection in the original focal axis maps the family to itself with reversed order and fixes M. Endpoint-intersection symmetry shows that the constant centroid lies on that axis. Central reflection maps the two focus constructions into one another and negates the centroid. These conclusions do not assume it vanishes for N≥6.

## 5. Least period four and the circle distinction

The exceptional N4 case concerns a circular **outer-vertex locus**, even though the original ellipse may be noncircular. The half-period identities give A=B, so the antipodally paired outer quadrilateral is a rectangle circumscribed about the original ellipse.

In orthonormal rectangle axes, original focal coordinates (m,n) satisfy

`h²−m²=l²−n²=b²>0`.

I checked the four actual antipedal intersections directly and recovered the author's unrestricted rectangle mean. The support identity makes both coordinates zero. None of its denominators vanish. Independently generated rational instances also satisfy the original ellipse equation, its named tangent-line incidences, and the billiard reflection law, so these controls are genuine four-orbits rather than arbitrary rectangles.

The optional circular original billiard is a separate elementary case: the reference focus is the origin, consecutive real antipedal normals are independent for a nondegenerate primitive orbit, and opposite intersections cancel. No singular limiting argument is needed. Reversal and repeated traversal of an already even primitive orbit preserve the arithmetic mean.

## 6. Reproducibility and fresh adversarial controls

All fourteen author hashes and three source PDF hashes match. Both author receipts replay byte-for-byte: 40,797 exact assertions and 47,931 separately labeled110-digit diagnostics. Their finite scope is not confused with the all-period proof.

The independently authored checkers import no author code:

- `independent_exact.py` passes **12,906 exact assertions**. It uses homogeneous line cross-products, symbolic leading coefficients and four-edge residues, rational similarity covariance, genuine rectangle/ellipse contact and reflection controls, isotropic negative/zero controls, and translated cyclic pole bookkeeping.
- `independent_numeric.py` passes **4,083 non-interval diagnostics** at125 digits over18 primitive families, including stars and both foci. It uses actual original tangent intersections, a non-unit Euclidean scale, direct named antipedal-line incidence, both roots of the focal equation with every imaginary translate, every common midpoint and dn-zero translate, and complete sums near every translated pole type. The largest full complex-centroid residual is approximately4.09e−76.
- A generic nonfocal reference gives an explicit phase-dependent centroid in the separate negative control. Thus the tests would detect the invalid shortcut of applying the focal theorem to arbitrary M.

The finite controls corroborate the analytic proof. They are not interval certificates, a classification of all numerical configurations, or evidence of historical priority.

## Disposition

The full source target is verified within the stated primitive-even/strict-elliptical domain after one substantive author turn. The unchanged mathematical packet is suitable for a draft result PR with the full independent review and the narrow bibliography correction retained. No area-centroid result, outer-locus-focus substitution, unrestricted parity extension, or novelty guarantee is certified. The parent campaign retains publication authorization.
