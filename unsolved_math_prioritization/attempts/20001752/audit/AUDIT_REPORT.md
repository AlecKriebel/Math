# Independent audit: E8 and Leech midpoint Mellin identities

Problem 20001752 / AIM-GEOMETRY-0090; rank 513. Audited 3 October 2026.

## Verdict

**PASS_PARTIAL.** The frozen proof establishes the entire normalized E8 subproblem:

\[
\int_0^\infty f_8(r)r^3\,dr
=\int_0^\infty\widehat f_8(r)r^3\,dr=\frac1{15}.
\]

The summation theorem holds for every radial Schwartz function in dimension eight, not merely for the tested Gaussians. The dimension-24 summation theorem and its exact weighted-tail value \(20/91\) also pass. The modular-period representations, their signs and constants, and the stated narrow polynomial-ansatz obstruction pass.

**The original combined problem remains unresolved here, because the Leech midpoint value is not identified.** The number \(20/91\) is not that value. Preserve the five completed approaches and the partial/exhausted disposition. No global impossibility, novelty, historical priority, comprehensive literature clearance, or human peer-review claim is supported by this audit.

No blocking mathematical defect or required correction to the frozen formulas was found. The detailed convergence bounds below make explicit some estimates that the author states briefly. The source-version and numerical qualifications below must accompany the result.

The audited proof SHA-256 is

`405a9f91ea3cc437e55e55e63bdcf7151b8b8187f2659394f1ea3d0a07a1440f`.

All eight files listed in the author manifest still match their frozen hashes and byte counts. This audit did not modify them or publish anything remotely.

## 1. Target, sources, and versions

The relevant mathematical target is the radial Mellin evaluation, rather than reconstructing the 2016 sphere-packing functions. Cohn and Miller define \(M_f(s)=\int_0^\infty f(r)r^{s-1}\,dr\), state the Fourier/Mellin relation in (5.2), and give the E8 conjecture and the Leech numerical value on PDF page 18. These are the normalization and question checked here. Their numerical-sequence convergence conjectures are not proved by this packet and are not needed for its theorem about the constructed Schwartz magic function. [Cohn--Miller, version 1](https://arxiv.org/abs/1603.04759v1).

The four principal source files were inspected at the claimed statements, and their hashes were checked against the supplied source inventory:

- **Viazovska, arXiv:1603.04246v2**, revised 4 April 2017. Equations (28), (35), (38), (41), Propositions 1--4, and Theorem 4 supply the E8 modular form, Schwartz/eigenfunction property, contour, normalization, and root data. The rendered pages 13--14 were also inspected to remove OCR ambiguity in the rational terms and the first-root derivative. [Pinned version](https://arxiv.org/abs/1603.04246v2).
- **Cohn--Kumar--Miller--Radchenko--Viazovska, arXiv:1603.06518v4**, revised 6 September 2026. Although the bibliographic citation is to the 2017 Annals paper, the supplied PDF is this later version. Section 2, particularly (2.1), (2.6), (2.9)--(2.10), and printed page 1023, supplies the Leech positive eigenfunction data. Rendered printed pages 1022--1023 were checked. Section 4 gives its normalization in the magic function. The corresponding formula, contour, and normalized-data passages were additionally compared with the 2017 version 3 and agree. The current arXiv record notes corrections to the ancillary positivity-verification file; this audit does not claim to revalidate that entire appendix. [Version 4 record](https://arxiv.org/abs/1603.06518v4), [version 3 PDF](https://arxiv.org/pdf/1603.06518v3).
- **Cohn--Kumar--Miller--Radchenko--Viazovska, arXiv:1902.05438v3**, revised 10 June 2022. Lemma 2.2 is exactly the density statement needed, in the radial Schwartz topology and in every dimension. Its proof includes the necessary seminorm estimates and Riemann-sum convergence. Theorem 1.7 and Corollary 1.8 provide the stated uniqueness background. [Pinned version](https://arxiv.org/abs/1902.05438v3).
- **Cohn--Miller, arXiv:1603.04759v1**, 15 March 2016. Equation (5.2), Conjecture 5.3, and its following paragraph were read directly. [Pinned version](https://arxiv.org/abs/1603.04759v1).

The 2025 Alfes--Kiefer--Mazáč paper's publisher text was checked at Lemma 2.2: it explicitly invokes the same Gaussian-density result for radial distributions. Its bibliographic date and article number agree with the author packet. This is contextual support, not a prior evaluation of this E8 moment. [Publisher article](https://link.springer.com/article/10.1007/s00220-025-05313-6).

The supplied text of Seewoo Lee's 2026 thesis was checked for the targeted Mellin/midpoint/decimal strings and `1/15`; no matching passage was found. Its title and date agree with the supplied source. A new fetch of its landing page encountered a verification page. This limited text search is not a review of the entire thesis and cannot certify absence of an equivalent result. [Thesis record](https://escholarship.org/uc/item/2j65b950).

The live AIM and problem-catalog pages were not independently retrievable in this audit. The pinned problem record was used only to recover scope; Cohn--Miller independently verifies the mathematical target. The corrupted decimal \(0.17786094729650\ldots\) is present in that pinned record, whereas Cohn--Miller print \(0.177860964729650276645646126241\ldots\). It is appropriate to flag the discrepancy, rather than call an unspecified ellipsis an exact target. No stronger claim about the currently live AIM text is made. [AIM source location](http://aimpl.org/discreteaf/1/).

No exhaustive new repository-history or priority search was undertaken. The author's search reports remain bounded reports.

## 2. Fourier, Mellin, and origin conventions

The Fourier kernel is \(e^{-2\pi i x\cdot y}\). Thus, for \(\operatorname{Im}\tau>0\),

\[
\widehat G_\tau=(-i\tau)^{-d/2}G_{-1/\tau},
\qquad G_\tau(r)=e^{\pi i\tau r^2}.
\]

For \(d=8,24\), the prefactors reduce to \(\tau^{-4}\) and \(\tau^{-12}\), respectively. There is no missing phase. Differentiation of the radial profile gives \(\mathcal DG_\tau=2\pi i\tau G_\tau\), also at zero.

For a smooth radial function, the restriction to a coordinate line is smooth and even. Consequently \(f'(0)=0\), \(f'(r)/r\to f''(0)\), and this origin value is a continuous functional of the Schwartz function. It is the radial second derivative, not its quadratic Taylor coefficient and not its Laplacian. These distinctions matter to the final constants.

The Mellin integrals use \(dr\), not the radial volume measure on \(\mathbb R^d\); no sphere-area factor belongs in the answer. The Gaussian identity is

\[
M_{G_\tau}(s)=\tfrac12\Gamma(s/2)(-\pi i\tau)^{-s/2}.
\]

In particular \(M_{G_\tau}(4)=-1/(2\pi^2\tau^2)\). The stated general Fourier/Mellin equation agrees with Cohn--Miller (5.2); as an ordinary integral relation it holds for \(0<\Re s<d\), which includes both midpoints. Elsewhere it is interpreted meromorphically. At the midpoint its scalar is one.

There is also a proof of midpoint equality avoiding this general equation: the right side of the proved E8 sampling formula is unchanged by Fourier transform, since \(\widehat{\widehat f}=f\) for radial functions. Thus the E8 conclusion does not depend on using analytic continuation of Mellin transforms.

## 3. Absolute convergence and Gaussian density

Write \(e_0=1\) and \(e_n=-24\sigma_1(n)\). The elementary bound \(|e_n|\le24(n+1)^2\) yields

\[
|a_n|\le576(n+1)^5,\qquad |b_n|\le13824(n+1)^8.
\]

For \(n\ge1\), \(r_n=\sqrt{2n}\). Therefore a sufficiently high weighted supremum seminorm of \(f\), and of its first radial derivative, bounds both series absolutely. For example, weight 20 suffices. Division by \(r_n\) causes no problem away from zero; the origin is separately controlled by the second derivative. Fourier transform is continuous on Schwartz space, so the same bounds apply to \(\widehat f\). The Mellin functional at 4 is continuous by bounding \([0,1]\) with a supremum norm and using decay of order greater than 4 for the tail.

In the Leech lift, \(h_0=1\) and \(h_n=480\sigma_7(n)=O((n+1)^8)\). Convolution gives \(A_n=O((n+1)^{14})\) and \(B_n=O((n+1)^{17})\). Weight 40 radial Schwartz seminorms suffice for those sampling series.

For the left side of the lifted theorem, the sum of absolute kernels satisfies

\[
\sum_{2n\le r^2}|h_n|\,r(r^2-2n)
\le C(1+r)^{21}.
\]

Indeed, \(\sum_{n\le r^2/2}|h_n|=O((1+r)^{18})\) and \(r(r^2-2n)\le r^3\). A decay seminorm of order 24 now proves absolute integrability, continuity, and legitimacy of interchanging the sum and integral, including after absolute values are taken. The \(n=0\) term is included.

Lemma 2.2 of CKMRV applies to these continuous functionals. Its Gaussians have arbitrary positive imaginary part; even a fixed imaginary part suffices. The proof starts with compactly supported smooth radial functions, writes them as \(g(|x|^2)e^{-\pi y|x|^2}\), extends \(g\) smoothly to a compactly supported function on the real line, and uses Fourier inversion. The rapid decay of its one-dimensional Fourier transform controls every required Schwartz seminorm; bounded-interval Riemann sums then give finite Gaussian combinations. A diagonal sequence handles the countable seminorms. Therefore no unjustified passage from Gaussian tests to all Schwartz functions occurs.

The defining Eisenstein series converge absolutely in the upper half-plane. Their products are consequently the coefficient convolutions used in the proof. The proof never uses polynomial growth for the different weakly holomorphic forms \(\Phi_8,\Phi_{24}\); their cusp estimates are handled separately below.

## 4. The universal E8 summation identity

Put \(X=E_2(\tau)\), \(c=6/(\pi i)\), and \(y=c/\tau\). The sign in

\[
E_2(-1/\tau)=\tau^2(X+c/\tau)
\]

agrees with the source transformation formula. The Gaussian value of the proposed sampling functional is exactly

\[
\frac{X^2+(X+y)^2}{24}
+\frac{X^3-(X+y)^3}{36y}
=\frac{y^2}{72}
=-\frac1{2\pi^2\tau^2}.
\]

The coefficient of \(X^2\) is \(2/24-3/36=0\), that of \(Xy\) is also zero, and that of \(y^2\) is \(1/24-1/36=1/72\). This is an exact polynomial cancellation for every \(\tau\) in the upper half-plane, not an inference from sample values. The convergence and density argument then proves the theorem with its exact constants \(1/24\) and \(1/432\).

## 5. E8 magic-function evaluation

The normalization in Viazovska's Theorem 4 makes the positive Fourier eigencomponent

\[
h_8=\frac{\pi i}{8640}a.
\]

In her regularized expression (38), the analytic integral has a factor \(\sin^2(\pi r^2/2)=O(r^4)\). It cannot affect the constant or quadratic terms. The singular rational terms give

\[
a(r)=-\frac{8640i}{\pi}+\frac{18144i}{\pi}r^2+O(r^4).
\]

Thus \(h_8(0)=1\), its quadratic coefficient is \(-21/10\), and \(\mathcal Dh_8(0)=h_8''(0)=-21/5\). Proposition 4 gives \(a'(\sqrt2)=72\sqrt2 i/\pi\), hence \(\mathcal Dh_8(\sqrt2)=-1/120\). The value at that radius is zero. The sine-squared factor and regularity at the remaining lattice radii give the required double zeros for every \(n\ge2\).

Accordingly the positive-eigenfunction version of the sampling identity reduces to

\[
\frac1{12}+\frac1{216}\left(-\frac{21}{5}+\frac35\right)
=\frac1{15}.
\]

The negative component is annihilated by the midpoint functional. All signs, the factor of two from projection, and the radial-derivative division have been checked independently. Uniqueness among radial Schwartz magic functions is appropriate background, but is not being substituted for an evaluation.

## 6. Leech weighted-tail theorem

The weight-eight transformation of \(H=E_4^2\) cancels the extra \(\tau^{-8}\) in the dimension-24 Fourier factor. The same Gaussian calculation yields

\[
-\frac{H(\tau)}{2\pi^2\tau^2}.
\]

Directly, setting \(u=r^2-2n\) gives

\[
\int_{\sqrt{2n}}^\infty e^{\pi i\tau r^2}r(r^2-2n)\,dr
=\frac{q^n}{2}\int_0^\infty u e^{\pi i\tau u}\,du
=-\frac{q^n}{2\pi^2\tau^2}.
\]

The estimates in Section 3 justify the sum, and density proves the lifted identity universally.

The Leech positive component is \(-\pi i a/113218560\). The unnormalized source values independently produce

\[
h_{24}(0)=1,\quad h_{24}(\sqrt2)=\frac1{156},\quad
\mathcal Dh_{24}(0)=-\frac{3587}{910},\quad
\mathcal Dh_{24}(\sqrt2)=-\frac{107}{2730},\quad
\mathcal Dh_{24}(2)=-\frac1{65520}.
\]

In particular, the source's derivative at 2 is \(-1/32760\), so dividing by the radius is essential. The remaining samples vanish as claimed. Direct convolution gives \(A_1=432\), \(B_1=408\), \(B_2=28872\), and exact rational evaluation gives \(20/91\).

The distinction from the Leech midpoint is rigorous at the level of kernels. On \(0<r<\sqrt2\), only \(n=0\) contributes to \(J_H\), so its kernel is \(r^3\); the midpoint kernel is \(r^{11}\). These differ, for example near \(r=1/2\), and a smooth radial bump supported there separates the functionals. Thus even their universal identities cannot be conflated.

## 7. Modular periods, contour directions, and Fubini

The E8 form equals Viazovska's \(\phi_0\), since \(j-1728=E_6^2/\Delta\). The dimension-24 form is the positive-eigenfunction form (2.1), not the negative-eigenfunction ingredient (3.1). Their numerators cancel all nonpositive powers in their quotients at the cusp, and the published expansions start at \(q\). Their real coefficients make both real-line integrands real at the two displayed nomes.

Set \(p=d/4\), so \(p=2\) or 6. In the first contour, \(z=-1-1/w\) and \(dz=w^{-2}dw\); its kernel becomes

\[
\frac{\Phi_d(w)}{w^p(w+1)^p}\,dw.
\]

It runs downward from the cusp to \((-1+i)/2\). In the second, \(z=1-1/w\); the kernel is \(\Phi_d(w)/(w^p(w-1)^p)\). Translating \(w\) by one and using periodicity makes it identical to the first. Vertical representatives give \(w(w+1)=-(t^2+1/4)\). Because \(p\) is even, the combined contribution is \(-2iI_d\), with the minus sign from downward orientation.

For the third contour, \(w=-1/z\) transforms its kernel to \(\Phi_d(w)w^{-p}dw\), again downward. Multiplication by its original \(-2\) and parameterization of the imaginary axis contributes \(-2iK_d\); the fourth term contributes another \(-2iK_d\), since \(i^{-p}=-1\) for both values of \(p\). Thus \(P_d=-2iI_d-4iK_d\).

These deformations stay in the upper half-plane, where \(\Delta\) is nonzero and the integrands are holomorphic. At transformed infinity, \(\Phi_d\) decays exponentially, uniformly in the real part by periodicity. Truncated versions of the published straight paths and the chosen vertical paths can be joined by horizontal segments of length \(O(t)\); their connecting integrals tend to zero. The mapped first two vertical contours approach their original endpoints within the upper half-plane, with imaginary part comparable to \(1/t\). After integrating the absolute radial Gaussian, the added factor is a power of \((\operatorname{Im}z)^{-1}\), hence only a power of \(t\). It is dominated by the exponential decay of \(\Phi_d\). The same reasoning handles the third endpoint at zero; the fourth is directly exponentially convergent. Compact segments pose no Fubini difficulty. This proves the needed absolute integral interchange, rather than only a formal contour substitution.

The Gaussian Mellin multiplier before the contour period is \(-1/(2\pi^2)\) for \(p=2\) and \(-60/\pi^6\) for \(p=6\). Combining these with the source normalizations gives

\[
M_{f_8}(4)=\frac{-iP_8}{17280\pi},\qquad
M_{f_{24}}(12)=\frac{60iP_{24}}{113218560\pi^5},
\]

which are exactly (15). The E8 theorem therefore yields \(P_8=1152\pi i\) and \(I_8+2K_8=-576\pi\). The Leech expression is an exact convergent integral representation, but remains unevaluated as a simpler identified constant.

## 8. Scope of the higher-depth obstruction

Expanding the proposed sixth/seventh-power response gives all of the author's coefficients \(35,70,63,28,5\); the two leading canceled coefficients are zero. For the formal matching equation (17), the constant term yields \(A=6B'\). After that substitution, the coefficient of \(y^j\), for \(j\ge1\), is

\[
\frac{6(j-1)}{(j+1)!}B^{(j+1)}(X).
\]

The \(y^2\) coefficient is exactly \(B'''\). In characteristic zero it vanishes only when \(\deg B\le2\), at which point the entire left side vanishes. Thus \(C=0\). This is a valid coefficientwise obstruction for polynomials \(A,B\) in the formal variable \(X\); it does not establish independence of modular-function values along an analytic locus and makes no claim excluding other constructions.

## 9. Reproduction and diagnostic limits

The author scripts were copied before execution so their output-writing behavior could not alter the frozen packet. Both reruns exited successfully and reproduced their recorded JSON outputs byte for byte. Their floating-point assertions remain diagnostics.

`audit_controls.py` is a separate implementation. Its default mode uses only the standard library, checks all eight frozen input hashes and the unchanged author manifest against the audit's independent snapshot, performs 80 coefficient comparisons for each of three independent divisor formulas, verifies the exact covariance coefficients and normalized source data, checks the polynomial obstruction and contour Jacobian algebra, and rejects eight specific wrong-normalization or scope mutations. It passes **331 assertions**. Run:

`python audit_controls.py --public ../public`

The optional `--numeric` mode additionally requires mpmath and passes **344 assertions**. It checks ten Gaussian cases across dimensions 8 and 24, including eight oscillatory complex Gaussians, at 120 working decimal digits; their maximum observed absolute residual is below \(10^{-116}\). Its quadrature is independent of the author's quotient-series routine: it directly evaluates Eisenstein series and the product formula for \(\Delta\). Integration to 16 gives

\[
M_{f_8}(4)\approx0.0666666666666666666666666666666666667,
\]
\[
M_{f_{24}}(12)\approx0.1778609647296502766456461262418773568.
\]

It also rejects the reversed first-contour sign, bringing the mutation count to nine in this mode. These are non-interval checks with finite truncations, not certified error enclosures. In particular, the number of working digits is not a claim that every printed digit is correct. The infinite claims are supported by the analytic arguments above.

The initial audit-only E8 quadrature cutoff at 12 was too short for its deliberately strict \(10^{-38}\) diagnostic threshold. Extending the cutoff to 16 resolved that diagnostic issue; no author formula was changed. Both final modes were rerun against the final control implementation.

## 10. Portable release boundary

The separate audit deliverables are this report, `audit_controls.py`, `exact_controls.json`, `numeric_controls.json`, `author_rerun.json`, `FROZEN_INPUTS.json`, `SOURCE_VERSIONS.json`, and `AUDIT_MANIFEST.json`. They contain no full source papers, source PDFs, catalog dumps, cached research reports, credentials, or local coordination paths. The manifest covers the final audit artifacts and the frozen inputs.

Any publication should retain the qualified **PASS_PARTIAL** verdict: E8 evaluated exactly; Leech weighted-tail theorem valid; Leech midpoint identification unresolved; five approaches completed; no priority claim.
