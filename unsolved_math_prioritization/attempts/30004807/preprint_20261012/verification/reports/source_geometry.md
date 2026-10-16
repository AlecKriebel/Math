# Independent source and geometry review of PR464

## Verdict and exact scope

**PASS for the qualified geometric counterexample in the frozen proof. Mandatory issues: 0. Optional improvement: 1. Unresolved mathematical gaps in this qualified claim: 0.**

The metric
\[
g=-\phi^{-2}dt^2+\phi^4\delta,\qquad \phi=1-a/\rho,\quad a>0,\quad \rho\geq a,
\]
has harmonically regular, negative-mass ZAS on its natural static, totally geodesic slices. Under the BKTZ smooth boundary-reaching test convention, the displayed radial test gives an absolutely convergent Einstein-tensor contraction with integral \(-8\pi\). It therefore disproves the universal implication from this slice geometry to the homogeneous weak identity. The fixed-boundary smooth structure, static foliation, and absence of an energy/matter restriction must remain visible in any publication.

The short OWR conjecture does not formally define admissibility for every arbitrary nonsymmetric spacetime or expressly quantify over every tilted hypersurface. Its cited static construction supports the foliation interpretation used by the proof. This review cannot certify an unstated stronger author-intended version. That limitation is interpretive, not an unsupported step in the explicit counterexample theorem. Historical priority and a complete preprint package are outside this independent geometry review.

## Independence and inspected inputs

The initial hypothesis and independent source conclusion were recorded before reading the frozen proof, source gate, any earlier audit, any peer report, or root conclusions. No earlier mathematical audit or peer report has been used in this review. The only frozen mathematical inputs subsequently read were `release/PROOF.md` and `release/SOURCE_GATE.md` at head `97b2ed225574ca61bd03cb8db021a533e04938dc`.

Primary PDF scans inspected visually, including complete page breaks:

- Burtscher, OWR40/2021, PDF pages 75-77, printed 2231-2233. The conjecture begins on printed 2233; its geometric description and displayed identity are on 2232.
- BKTZ, arXiv:1901.00813v3, printed/PDF pages 4-12. These include Sections 1.3-1.4, Theorem 1.1 and its boundary-support footnote, Definition 2.1, equation (2.5), angular-independence footnote 7, and the normal-orientation calculation on page 10.
- Bray-Jauregui, arXiv:0909.0522v2, printed/PDF pages 3, 5-8, and 32. These cover the time-symmetric setting, Definitions 4, 6, 7, 10, and the discussion of future arbitrary-slice extensions in Section 6.6.

Total visually inspected primary pages: 18. Foreign PDFs, text extractions, and images remain private and are excluded from the public whitelist. Public receipts retain provenance and hashes, not source reproductions.

## Source reconstruction

The [OWR report](https://doi.org/10.4171/OWR/2021/40) describes admissibility by regular negative-mass ZAS on spacelike slices and proposes the weak identity for that geometric class. It gives no explicit energy condition, prescribed matter law, or lapse bound. [BKTZ](https://arxiv.org/abs/1901.00813v3), Sections 1.3-1.4, makes the construction on constant-time slices; its theorem adds sufficient growth assumptions separately. Definition 2.1 tests vector fields smooth on the blown-up manifold including its boundary. The radial component need not vanish; equation (2.5) displays it. Angular independence in that equation is a convenient restriction, satisfied by the proposed radial test.

[Bray-Jauregui](https://arxiv.org/abs/0909.0522v2) defines ZAS through areas of approaching graphs converging in **C1**, not merely C0. A regular resolution is a smooth positive Riemannian metric and a smooth conformal factor vanishing at the boundary with positive inward normal derivative. The paper's spacetime motivation is time-symmetric; arbitrary spacelike-slice extensions are discussed separately in Section 6.6.

## Direct geometric checks

For the constant-time slices, \(h=\phi^4\delta\), with resolution \((\delta,\phi)\). On \(S_a\), the inward resolution normal is \(+\partial_\rho\), and its derivative of \(\phi\) is \(1/a>0\). The Euclidean Laplacian vanishes. A C1-convergent family of boundary graphs has bounded Euclidean area, whereas the supremum of \(\phi^4\) on it tends to zero. Consequently the full ZAS definition holds; coordinate spheres alone are not being substituted for that definition.

The resolution mass is
\[
-\frac14\left(\pi^{-1}4\pi a^2(a^{-1})^{4/3}\right)^{3/2}=-2a.
\]
The area-radius relation \(r=(\rho-a)^2/\rho\) gives
\[
h=(1+4a/r)^{-1}dr^2+r^2d\Omega^2.
\]
Thus the spatial geometry is exactly the negative-mass Schwarzschild slice. The static shift vanishes and \(\partial_t h=0\), so its second fundamental form is zero. This also meets the time-symmetric motivation of the cited Riemannian framework. As \(\rho\to\infty\), the spatial coefficients differ from Euclidean ones by order \(\rho^{-1}\), their first two derivatives have orders \(\rho^{-2}\), \(\rho^{-3}\), and the spatial scalar curvature is zero. The lapse tends to one. The asymptotic-flatness statement is valid.

The limiting singularity is timelike in the radial causal sense used for the naked singularity prototype. Every \(\rho\)-tube has spacelike normal and Lorentzian induced metric. With \(s'=\phi^3\), the radial metric is \(\phi^{-2}(-dt^2+ds^2)\), and \(s\sim(\rho-a)^4/(4a^3)\); hence the radial conformal boundary \(s=0\) is timelike. Radial null geodesics of conserved energy \(E>0\) satisfy \(|d\rho/d\lambda|=E/\phi\). Their remaining affine length is proportional to \(\int_a^\rho\phi(u)du\), which is finite. The computed invariant \(\operatorname{Ric}_{\mu\nu}\operatorname{Ric}^{\mu\nu}=6a^2/(\rho^6\phi^{10})\) diverges. The singularity is not a removable coordinate artifact. This is not a claim of a nondegenerate smooth extension of the four-dimensional physical metric to the cylinder.

## Tilted-slice falsification controls

For a local graph \(t=f(\rho,\omega)\), the induced metric is
\[
h_f=\phi^4\bigl(\delta-\phi^{-6}df\otimes df\bigr),
\]
and it is spacelike exactly when \(|df|_\delta<\phi^3\). This explicitly describes the issue that a foliation-only check could hide.

First take \(f=t_0+q s(\rho)\), where \(s'=\phi^3\) and \(|q|<1\). Then
\[
h_f=\phi^4\bigl((1-q^2)d\rho^2+\rho^2d\Omega^2\bigr).
\]
The parenthesized resolution metric is smooth and positive at the boundary; its inward derivative of \(\phi\) is \(1/(a\sqrt{1-q^2})\). Its regular mass is \(-2a/(1-q^2)<0\). Thus the counterexample is not confined to literally horizontal slices.

For a smooth angular function \(q(\omega)\) with \(\sup|q|<1\), take \(f=t_0+q(\omega)s(\rho)\) locally. Since \(s/\phi^3=(\rho-a)/4+O((\rho-a)^2)\) extends smoothly, the one-form
\[
\phi^{-3}df=q\,d\rho+(s/\phi^3)dq
\]
extends smoothly and has boundary value \(q\,d\rho\). The resulting resolution is positive on a sufficiently small collar. Its normal derivative is positive and its regular mass remains negative. These local graphs can be continued to static slices away from the collar; no asymptotic non-flat tilted slice is needed.

By contrast, a smooth nearly-null radial graph defined near the boundary by
\[
f'=\phi^3\sqrt{1-\phi^2}
\]
is strictly spacelike in the interior but has
\[
h_f=\phi^6d\rho^2+\phi^4\rho^2d\Omega^2.
\]
It has **no regular resolution in the fixed cylinder boundary smooth structure**. Indeed any regular defining factor \(u\) must vanish to first order, \(u=c(\omega)(\rho-a)+O((\rho-a)^2)\) with \(c>0\). Dividing the radial metric by \(u^4\) gives a coefficient tending to zero, while the angular coefficients have positive limits. A purported resolution metric would therefore be degenerate on the nonzero radial tangent direction. This contradicts positive definiteness.

The same test also fails regularity for the cited vacuum negative-Schwarzschild spacetime: replace the graph derivative by \(f'=(\phi^2/N_v)\sqrt{1-\phi^2}\), where \(N_v=(\rho+a)/(\rho-a)\). It yields exactly the same \(h_f\). Thus requiring regular ZAS for **every** interior-spacelike graph approaching a null direction would also exclude the primary prototype. Neither the proof nor this review promotes that substantially stronger all-tilted-slice assertion. This control is a scope test, not a new proposed resolution of that different conjecture.

## Boundary tests and defect

On the exterior cylinder, \(\partial_\rho=x^i\partial_{x^i}/\rho\) is smooth because \(\rho\geq a>0\). Therefore \(\psi=\eta(t)\chi(\rho)\partial_\rho\) is a permitted smooth section with compact support in the manifold-with-boundary topology. Its spherical components are angular independent. It has a nonzero normal component; the primary test convention expressly permits that. A vector-field section need not be tangent to the boundary. Replacing this class by fields smooth after collapsing the sphere, or fields supported entirely in the punctured interior, changes the weak problem.

Independent conformal differentiation gives the mixed spatial Ricci eigenvalues \(4a/(\rho^3\phi^6),-2a/(\rho^3\phi^6),-2a/(\rho^3\phi^6)\). The vacuum lapse obeys \(\operatorname{Hess}_hN_v=N_v\operatorname{Ric}_h\) and \(\Delta_hN_v=0\). For \(N=(1+N_v)/2=\phi^{-1}\), the mixed Einstein eigenvalues are \(0,2a/(\rho^3\phi^5),-a/(\rho^3\phi^5),-a/(\rho^3\phi^5)\). With volume density \(\phi^5\rho^2\), the full contracted test density reduces to
\[
2a\eta(t)\,\partial_\rho(\chi(\rho)/\rho)\,dt\,d\rho\,d\Omega.
\]
It is absolutely integrable, and its integral is \(8\pi a(0-1/a)=-8\pi\) when \(\int\eta=1\) and \(\chi(a)=1\). The algebraic cancellation must occur before integration; the separate singular connection summands need not be integrable. The original proof handles this correctly. Its Cartesian symmetric-traceless density argument also gives absolute integrability for every source-convention test, and the outward domain normal at the inner boundary is minus the Euclidean radial normal, giving the displayed defect sign.

The example meets BKTZ's first two sufficient growth hypotheses but has a nonzero order \((\rho-a)^{-5}\) Einstein coefficient, without their required strict improvement. There is no contradiction with the established theorem. If matter is defined by \(T=G/(8\pi)\), the static energy density is zero while angular pressure is negative; the angular null energy condition fails. Consequently NEC, DEC, electrovacuum, or specified admissible electromagnetic matter models are not solved here. The static initial data still have \(R_h=0\), \(K=0\), energy density and momentum density zero; that distinction does not restore spacetime NEC.

## Reproducible evidence, counts, and remaining limit

The independent standard-library `check_geometry.py` uses second-order rational automatic differentiation and imports no frozen checker. It reproduces Ricci eigenvalues, vacuum Hessian identities, scalar flatness, area-radius conversion, the half-vacuum lapse relation, defect-density cancellation, Euclidean density divergence, and positivity controls. It passes **396 exact checks over 18 rational parameter cases** under both ordinary Python and optimized Python; the two result files are byte-identical. These bounded checks corroborate the analytic deductions above and are not a universal proof by sampling.

The source-binding receipt confirms that the frozen proof and source gate still match the original capture. No original source, earlier audit, root note, Git state, remote branch, or external record was changed. No outreach occurred. Outside input could clarify the intended admissibility beyond the report's informal wording; this observation is recorded without preparing contact.

**Exact remaining limit:** absence of a fully specified arbitrary-spacetime admissibility definition in the short OWR report prevents certification of every possible unstated author-intended strengthening. The strongest independently verified theorem is the explicit counterexample with regular negative-mass ZAS in the natural static foliation and BKTZ boundary-reaching tests, also robust under uniformly spacelike nearby graph tilts. That theorem has no mathematical gap found in this review.

**Optional improvement (1):** in the preprint, support the existing foliation qualification with Bray-Jauregui page 3 and Section 6.6/page 32, and consider a short uniformly-spacelike-tilt observation. This improves clarity but is not needed to repair the already-qualified frozen theorem. Do not claim all arbitrary tilted slices, Einstein matter admissibility, first priority, formal verification, or human peer review.
