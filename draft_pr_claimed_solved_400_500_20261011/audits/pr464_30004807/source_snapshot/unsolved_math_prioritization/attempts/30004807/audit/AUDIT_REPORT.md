# Independent adversarial audit: weak Bianchi identity and regular timelike ZAS

- Problem: 30004807 / OWR-8415343-010
- Audit date: 2026-10-03
- Verdict: **PASS_FULL_COUNTEREXAMPLE**
- Exact scope: the universal geometric conjecture on printed OWR pp. 2232–2233, interpreted with the boundary-reaching smooth test fields in BKTZ Definition 2.1.
- Blocking findings: **none**.
- Historical priority: **not established**.

The frozen construction refutes the stated universal homogeneous identity. Its integral is an ordinary absolutely convergent integral of the full contracted scalar, with value \(-8\pi\). The same geometry satisfies the inhomogeneous identity with an explicitly nonzero boundary functional. Thus the counterexample is stronger than an example where the requested integral is undefined.

This verdict does not extend to conjectures with extra energy conditions, a prescribed electromagnetic matter model, the stronger sufficient hypotheses of BKTZ's theorem, or a different test space based on smooth extension through a collapsed worldline. These are substantive distinctions already made in the frozen proof, not missing hypotheses of the audited conjecture.

## 1. Frozen input and independent verification

The six release files were checked against the supplied frozen SHA-256 manifest before and after verification. All six remain unchanged. The author's script was rerun only from an isolated temporary copy, so its generated output could not modify the frozen release. It passed all 17 listed checks.

The separate `audit_controls.py` uses a different curvature route: a proper-radial-distance orthonormal warped-product calculation, followed by independent Cartesian tensor-density differentiation. All 35 exact controls pass, including three explicitly rejected false alternatives. They include flat and negative-mass vacuum controls, the full lapse family, curvature invariants, the normal-trace coefficient, and the cancellation of individually divergent connection terms.

The geometric and source checks below are necessary mathematical arguments; the finite list of symbolic checks alone is not a proof of admissibility.

## 2. Primary-source and quantifier gate

The auditor visually inspected both rendered OWR printed pages 2232 and 2233, not merely an extraction stopping before the page break. The first page identifies admissibility through regular negative-mass ZAS on spacelike slices and presents the weak integral. The next page gives the universal conjecture for that geometric class. The immediately preceding and following discussion does not impose an independent energy condition, a specified matter theory, or the strict curvature-growth hypothesis of BKTZ Theorem 1.1. The report discusses matter models as an application and further program.

BKTZ's printed arXiv pages 6 and 9 were also inspected as rendered pages. The footnote to Theorem 1.1 permits support on the inner boundary. Definition 2.1 explicitly uses smooth compactly supported fields on the blown-up manifold with boundary. Equation (2.5) keeps a potentially nonzero normal test component at that boundary. Its optional angular-independence restriction does not exclude the rotationally invariant radial test.

Sections 1.2–1.5 and 2 were read for additional assumptions. The general geometric setting allows independent lapse and radial metric coefficients. The special relation between them used for particular electrovacuum applications and Corollary 2.3 is not a premise of the universal geometric conjecture or of Definition 2.1. The sufficient mass-expansion conditions used to produce coordinates are likewise not an extra requirement when the admissible coordinate system and regular resolution are already explicit.

The source uses the static constant-time foliation when describing ZAS slices. Requiring regular resolution on every arbitrarily tilted hypersurface would be a stronger assertion unsupported by this construction in the source. It is not silently assumed in the audit.

Sources: [OWR 40/2021, official report](https://publications.mfo.de/bitstream/handle/mfo/3893/OWR_2021_40.pdf?isAllowed=y&sequence=1), [BKTZ, arXiv:1901.00813v3](https://arxiv.org/abs/1901.00813v3), [Bray–Jauregui, arXiv:0909.0522](https://arxiv.org/abs/0909.0522). Public arXiv metadata was independently checked; the OWR DOI endpoint did not load through the browsing tool, so the report-content finding relies on the locally available official report and its inspected page images. No source-content uncertainty resulted.

## 3. Geometric admissibility

Set \(x=\rho-a>0\), \(\phi=x/(a+x)\), and
\[
g=-\phi^{-2}dt^2+\phi^4(d\rho^2+\rho^2d\Omega^2),\qquad a>0.
\]
The interior is a smooth four-dimensional Lorentzian manifold. Its underlying exterior-ball topology is diffeomorphic to the punctured-space topology used by the source. The smooth manifold with boundary, rather than the singular metric itself, extends to \(\rho=a\).

Every static slice has \(h=\phi^4\delta\). The resolution metric \(\delta\) is smooth and positive definite at the boundary. The resolution factor is smooth, nonnegative, vanishes exactly at the boundary, has inward normal derivative \(1/a>0\), and is Euclidean harmonic. Bray–Jauregui Definitions 4, 6, 7 and 10 therefore apply directly. For all their permitted \(C^1\)-approaching surfaces, Euclidean areas remain bounded and the maximum of \(\phi^4\) tends to zero, proving the full ZAS condition. The regular mass is exactly \(-2a\), not merely negative by analogy.

The area radius \(r=(\rho-a)^2/\rho\) is strictly increasing on the interior and gives
\[
h=\frac{dr^2}{1+4a/r}+r^2d\Omega^2.
\]
Thus the spatial metric, its Hawking/cumulative mass, and its standard negative-mass Schwarzschild identification are consistent. The spatial scalar curvature vanishes. The lapse is positive everywhere on the interior; no horizon is introduced. At infinity, the lapse tends to one and the spatial conformal factor tends to one with the usual inverse-radius decay.

Timelike character is not inferred solely from the sign of a singular metric component. The radial optical coordinate satisfies \(ds/d\rho=\phi^3\), so \(s\sim x^4/(4a^3)\), and the radial metric is \(\phi^{-2}(-dt^2+ds^2)\). Its limiting radial boundary \(s=0\) is timelike. All nearby constant-\(\rho\) tubes have Lorentzian induced metric, and their physical angular areas tend to zero. The lapse's inverse-linear divergence is compatible with BKTZ's explicit setting and with the negative-mass vacuum prototype.

As an additional independent check, a radial null geodesic of conserved positive energy \(E\) satisfies \(|d\rho/d\lambda|=E/\phi\). Its affine distance to the boundary is
\[
\frac1E\int_a^\rho\phi(u)du
=\frac{\rho-a-a\log(\rho/a)}E\sim\frac{x^2}{2aE},
\]
which is finite. The invariant curvature blow-up below rules out a regular extension. The singularity is genuine, incomplete and naked in the radial causal diagram.

## 4. Independent curvature route and sign checks

For the family
\[
N=A+B\frac{\rho+a}{\rho-a},\qquad A,B\ge0,\quad A+B>0,
\]
use proper spatial distance \(dl=\phi^2d\rho\) and area radius \(r=\rho\phi^2\). The independent orthonormal curvature components are
\[
R_{0101}=\frac{N_{ll}}N,\quad R_{0202}=\frac{N_l r_l}{Nr},\quad
R_{1212}=-\frac{r_{ll}}r,\quad R_{2323}=\frac{1-r_l^2}{r^2}.
\]
Contracting them with signature \((-+++)\) reproduces
\[
R_g=0,\qquad
G^\mu{}_{\nu}=\operatorname{diag}\left(0,\frac{4Aa}{N\rho^3\phi^6},
-\frac{2Aa}{N\rho^3\phi^6},-\frac{2Aa}{N\rho^3\phi^6}\right).
\]
At \(A=B=1/2\), this agrees with every component stated in the frozen proof. The Ricci-square invariant is \(6a^2/(\rho^6\phi^{10})\). Independently, the Kretschmann scalar is
\[
\frac{24a^2(a+x)^4(8a^2+12ax+5x^2)}{x^{12}},
\]
with strictly positive leading coefficient \(192a^8\). These are coordinate-invariant curvature singularities.

The vacuum endpoint \(A=0\) gives the identically zero Einstein tensor and the standard Schwarzschild Kretschmann scalar \(192a^2/r^6\). Setting \(a=0\) gives flat curvature. These controls check both sign conventions and the parameter dependence; a nonzero defect must not survive the vacuum control.

## 5. Genuine tests, full absolute integrability and exact defect

Choose smooth compactly supported \(\eta(t)\) with integral one and a smooth radial cutoff \(\chi(\rho)\) equal to one near \(a\). Then
\[
\psi=\eta\chi\,\partial_\rho
\]
is a genuine smooth compactly supported section of the tangent bundle of the blown-up manifold. In exterior Cartesian coordinates, \(\partial_\rho=\sum_i(x^i/\rho)\partial_i\), which is smooth everywhere up to the inner sphere because \(\rho\ge a>0\). Angular coordinate poles introduce no singularity in this field. It has angular-independent spherical components and is permitted by the source's explicit test convention.

The raised/lowered-index contraction in the question agrees with \(G^\mu{}_{\nu}\nabla_\mu\psi^\nu\) on the smooth interior. It is a scalar, not a coordinate-dependent collection of independently integrated summands.

In exterior Cartesian coordinates the weighted spatial mixed Einstein tensor is
\[
D^i{}_j=N\phi^6G^i{}_j
=\frac{Aa}{\rho^3}(6n_i n_j-2\delta_{ij}),\quad n_i=x_i/\rho.
\]
It extends smoothly to the inner sphere. Direct differentiation in all three Cartesian coordinates gives \(\partial_iD^i{}_j=0\). Its symmetry and zero trace give the exact all-index cancellation \(D^i{}_j\Gamma^j{}_{ik}=0\). The remaining Einstein components involving time vanish. Hence, for every smooth boundary-reaching compactly supported field,
\[
G^\mu{}_{\nu}\nabla_\mu\psi^\nu\,dV_g
=D^i{}_j\partial_i\psi^j\,dt\,d^3x.
\]
The right side is bounded on the compact support in the regular exterior coordinates. This proves absolute integrability of the complete contracted density for the entire test class. It also establishes coordinate independence under smooth changes compatible with that manifold-with-boundary structure.

The inner boundary's exterior-domain outward normal is \(-n\), giving the exact sign and coefficient
\[
I(\psi)=-\frac{4A}{a^2}\int_{\mathbb R\times S_a}\langle\psi,n\rangle_\delta\,dt\,dA_\delta.
\]
For the radial test, \(I=-16\pi A\), and at \(A=B=1/2\) this is \(-8\pi\). Independently, the spherical density is
\[
2a\eta(t)\left(\frac{\chi'}\rho-\frac\chi{\rho^2}\right)
=2a\eta(t)\frac d{d\rho}\left(\frac\chi\rho\right),
\]
which integrates to the same value. Substitution into the source's boundary expression also gives \(-4\pi a^2(2/a^2)=-8\pi\).

The individual radial and combined angular connection densities have opposite nonzero \(1/x\) terms. Integrating those terms separately is invalid. The proof does not do that: it forms the ordinary smooth scalar on the interior first, where cancellation is exact, then integrates its absolute value. Definition 2.1 requires the latter integral; the separate-summand estimates in the sufficient theorem are not additional requirements of the definition.

Compact support confined to the open punctured interior would exclude this test and make the interior identity automatic. Smoothness across a collapsed point is also a different condition. Neither convention may be substituted for the source's displayed boundary-test convention when evaluating this result.

## 6. Existing theorem and matter boundaries

Writing \(x=\rho-a\), the candidate satisfies the source's first-order conformal-factor and lapse growth bounds. However,
\[
\lim_{x\downarrow0}x^5G^\rho{}_{\rho}=2a^3\ne0.
\]
It therefore fails the strict \(O(x^{-5+\kappa})\), \(\kappa>0\), hypothesis of BKTZ Theorem 1.1. There is no contradiction with that theorem. In addition, its lapse derivative has constant correction \(1/a\), whereas Corollary 2.2 requires \(1/(2a)\); that stronger corollary does not inadvertently cover the example. Corollary 2.3's special lapse/radial-coefficient relation also fails.

With \(T=G/(8\pi)\), the static-frame energy density is zero and the angular pressures are negative. The angular null energy condition fails. This is disclosed in the frozen proof and excludes claims about NEC-restricted or specified electrovacuum conjectures. Einstein's equation alone, without a prescribed stress model or energy restriction, does not remove this geometric example. No such additional premise was found in the audited universal conjecture.

## 7. Release recommendation and limits

The frozen proof supports a full negative resolution of the literal geometric question, with its stated source-convention scope preserved prominently. There is no mathematical correction required before that scoped claim is used. Retain the explicit distinctions concerning matter restrictions, stronger sufficient theorems, and collapsed-point test spaces.

The audit has not established novelty, priority, or an exhaustive current literature search. It does not claim a canonical tensor-distribution extension of the metric through a collapsed worldline. Those issues do not undermine the stated absolutely convergent boundary-test counterexample.

Portable audit files are this report, `audit_controls.py`, `audit_controls.json`, `author_rerun.json`, `FROZEN_INPUTS.json`, and `AUDIT_MANIFEST.json`. No PDFs, full source extracts, screenshots, private catalog material, or search corpora belong in the public packet. No remote mutation was performed.
