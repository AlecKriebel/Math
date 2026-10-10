# Independent audit of the squared pole exceptional set bound

## Verdict

**ACCEPTED as a complete affirmative deduction for Hayman–Lingham Problem 7.37, ID 2307037 / AMR-022-7037. No mathematical correction is required in the frozen proof.**

For every finite positive squared-pole sum
\[
g(z)=\sum_j\frac{\lambda_j}{(z-z_j)^2},\qquad \lambda_j>0,\quad\sum_j\lambda_j=1,
\]
the candidate constructs one compact set \(S\), depending on \(g\) but not on \(R\), of area exactly \(\pi\), and proves
\[
\int_{\{|z|<R\}\setminus S}|g(z)|\,dA(z)
\le 2\pi\log R+\pi(\log 2+e^{-1})\qquad(R>1).
\]
All poles may be arbitrary complex numbers. Repeated poles, overlap in the construction, disconnected sets and bounded components of the complement are covered. The logarithmic coefficient \(2\pi\) is optimal among bounds with a finite additive constant. No optimality claim is made for the additive constant.

This is an independent AI-assisted mathematical audit of a specified argument, not human peer review, formal verification, or a priority determination. The result is a deduction from the cited established theorems together with the candidate's localization argument. Nothing in this audit establishes historical novelty or certifies that the question remained globally open before this deduction.

## Frozen text and exact target

The reviewed proof has SHA-256 `4030345880f7ea137e61ab49c79f5ffd4b897d9fd363dd43e83c730eaec1326d` (9,102 bytes). Its source-hypothesis companion has SHA-256 `ab608002221d1edbcaa34962532bae964db3de333024e1a7b3051cd164c24133` (5,051 bytes). These are the audited original identities. This edition updates only nonmathematical status and publication wrappers; ACCEPTANCE.json separately identifies the original and distributed documents. Public source identities and inspection history are recorded in SOURCE_DEPENDENCIES.json and SOURCE_METADATA.json.

The original statement was checked on the rendered pages 172–173 of the Hayman–Lingham v2 PDF, printed pages 171–172. Its quantifiers require a single exceptional set of exact area \(\pi\), an absolute additive constant, and every real \(R>1\). The statement does not confine the poles to the unit disk. The proposed theorem satisfies these quantifiers and strengthens measurability of the exceptional set to compactness. The target integral is an ordinary nonnegative Lebesgue integral, not a principal value.

The nearby Problem 7.36 and the source's update concerning it are not taken as a proof of 7.37. The additional quadrature-set construction and localization estimate are essential to the deduction.

## Eremenko–Hamilton input

The actual primary PDF was read, including all five pages and the displays on printed pages 2794 and 2796–2797. Its transform is
\[
Tf(\zeta)=-\frac1\pi\operatorname{pv}\int \frac{f(z)}{(z-\zeta)^2}\,dA(z).
\]
The displayed indicator estimate has precisely the coefficient and integration region used in the candidate:
\[
\int_{\Delta\setminus E}|T\mathbf1_E|\,dA
\le |E|\log\frac\pi{|E|}.
\]
Here \(\Delta\) can be the closed unit disk. There is no restriction that \(E\) be connected or a quadrature set. No extra additive term occurs. Null disk boundaries permit use of the open disk. The proof varies a bounded complex dilatation supported on \(\Delta\setminus E\); its final dual estimate yields the displayed absolute-value integral. This is a statement about measurable indicators, not a theorem restricted to finitely many poles. Its use here is on an indicator.

Under \(z=L\zeta\), \(w=L\eta\), the kernel contributes \(L^{-2}\) and the area element contributes \(L^2\). Thus
\[
T\mathbf1_E(L\zeta)=T\mathbf1_{E/L}(\zeta),
\]
and the integral estimate becomes \(a\log(\pi L^2/a)\), with \(a=|E|\). The scale factor and both occurrences of \(\pi\) are correct. When \(a=0\), the indicator vanishes almost everywhere and the continuous endpoint value is zero.

## Levine–Peres input and its hypotheses

The inspected source is the May 1, 2009 author manuscript, not an asserted byte-identical copy of arXiv v2. Definition (4), the superharmonic convention in section 2.1, Proposition 2.12, Corollary 2.13, Lemmas 2.14–2.15 and 6.1, and Proposition 6.6 with its proof and Theorem 6.7 interface were read. Relevant source displays were visually checked. The boundary-regularity proofs in section 7.2 were also read. The entire 74-page article and every ancestral theorem in its bibliography are not claimed to have been independently reproved.

### Existence, containment, boundedness and exact area

At a binary stage the inputs are bounded open sets \(A,B\) with null boundaries. The density \(\sigma=\mathbf1_A+\mathbf1_B\) is bounded, nonnegative, compactly supported, and continuous away from \(\partial A\cup\partial B\). It takes values in \(\{0,1,2\}\), so the density-gap hypothesis (24) holds with any fixed number strictly between zero and one. The set \(\{\sigma\ge1\}\) is exactly the open union \(A\cup B\). Consequently the enlarged noncoincidence set in Proposition 2.12 is exactly the smash sum in definition (4).

Proposition 2.12 gives its null boundary, and Corollary 2.13 gives additive area, including when the inputs overlap. Lemma 2.15 bounds the noncoincidence set; adjoining the bounded input sets preserves boundedness. Openness follows from continuity of the obstacle and majorant and the open union in definition (4). All these properties therefore hold again at the next binary stage. Lemma 6.1 makes reassociation legitimate under exactly these hypotheses. There is no separation, disjointness, integer-volume or unit-disk condition.

Take input disks with areas \(m_j=\pi\lambda_j\), hence radii \(\sqrt{\lambda_j}\). The final open smash sum \(\Omega\) contains every input disk and has area \(\pi\) and null boundary. Therefore \(S=\overline\Omega\) is compact and has the same exact area. Each pole has an open neighborhood in \(S\). The factor \(\pi\) belongs in the masses; using masses \(\lambda_j\) instead would have produced the wrong area and exterior-field normalization.

### The admissible test class

Proposition 6.6 fixes arbitrary finitely many centers and positive real volumes and gives a quadrature inequality for every integrable superharmonic function on the whole smash sum. It does not require nonnegative test functions, entire-plane superharmonicity, connectedness, or distinct centers. The source's definition of superharmonicity is the lower-semicontinuous mean-value inequality on balls lying in the open set. Both signs of a real harmonic function satisfy it.

The proof of Proposition 6.6 addresses the potentially troublesome value \(\sigma=1\): it doubles the indicators of concentric disks of half the target volumes. Their union is bounded and open, and the doubled density is at least two there and supported in its closure. This meets the strict-density hypothesis of Theorem 6.7. The mean-value inequality on the smaller disks, Lemma 2.7, associativity, and the ball-doubling identity then recover the desired smash sum. Neither the test class nor the source centers acquire an additional restriction during this argument.

Applying Proposition 6.6 separately to \(h\) and \(-h\) gives exact harmonic quadrature. For the kernel needed here the tests are smoother and better behaved than required: if \(z\notin S\), the real and imaginary parts of \((w-z)^{-2}\) are bounded and harmonic on a neighborhood of \(S\). The distance from this fixed \(z\) to the compact \(S\) is positive. This remains true when \(z\) is in a bounded complementary component. No analytic continuation from infinity, exterior connectedness or simply connectedness is being assumed.

## Exterior field and measure theoretic checks

Harmonic quadrature gives
\[
\int_\Omega\frac{dA(w)}{(w-z)^2}
=\sum_j\frac{\pi\lambda_j}{(z_j-z)^2}=\pi g(z).
\]
Squaring removes the sign change in the denominator, and the transform has its separate minus sign. Hence \(T\mathbf1_\Omega(z)=-g(z)\) for every \(z\notin S\).

This is a pointwise absolutely convergent integral at each such \(z\). The \(L^2\) realization or almost-everywhere principal-value convention for the transform elsewhere does not turn the target integral into a principal value. The exterior ordinary-integral representative agrees with the singular-integral representative almost everywhere, which suffices when applying Eremenko–Hamilton. Indicators and their transforms have measurable representatives. The rational function is continuous away from its poles, all of which lie inside \(S\).

At any fixed exterior point, both near and far pieces have positive distance from that point and finite area, so splitting the exterior integral is valid before using any integral bound. The comparison of regions in the near estimate is in the correct direction. In the far estimate all integrands are nonnegative after taking the absolute kernel, so Tonelli requires no prior integrability assumption. It then proves the asserted integrability. Independently, \(S\) contains the disk of radius \(\sqrt{\lambda_j}\) at each pole, so each summand has absolute value at most one outside \(S\); finiteness on any bounded integration region is also immediate for fixed finite \(n\).

## Localization and the absolute constant

For a fixed \(R>1\), let \(L=\sqrt2R\), \(E=\Omega\cap D_L\), \(F=\Omega\setminus D_L\), and \(a=|E|\). Then \(0\le a\le\pi\), \(|F|=\pi-a\), and
\[
D_R\setminus S\subset D_L\setminus E.
\]
The near integral is at most \(a\log(2\pi R^2/a)\).

For \(|w|=\rho>R\), direct integration of the angular Poisson kernel gives
\[
\int_0^{2\pi}\frac{d\theta}{\rho^2+r^2-2\rho r\cos\theta}
=\frac{2\pi}{\rho^2-r^2}.
\]
Integrating \(r\,dr\) from zero to \(R\) gives
\[
\int_{D_R}|z-w|^{-2}\,dA(z)
=\pi\log\frac{\rho^2}{\rho^2-R^2}.
\]
For \(w\in F\), \(\rho\ge\sqrt2R\); the logarithm is at most \(\log2\). The prefactor \(1/\pi\) in the Beurling transform cancels the \(\pi\) in the last integral. Thus the far contribution is at most \((\pi-a)\log2\), not \(\pi(\pi-a)\log2\) or half that value.

The combined expression is exactly
\[
2a\log R+\pi\log2+a\log(\pi/a).
\]
Since \(\log R>0\), replacing \(a\) by \(\pi\) in the first term is legitimate. The remaining entropy term is at most \(\pi/e\): \(-t\log t\) has derivative \(-\log t-1\), second derivative \(-1/t\), and maximum \(1/e\) at \(t=1/e\), with both endpoint values understood correctly. This proves the announced constant, approximately 3.333313440094524. No number of poles, location, separation or diameter enters it.

The set \(S\) was already selected before this argument. Only the auxiliary split changes with \(R\). The argument is deterministic for each real \(R>1\), with no probability-one event or radius-dependent exceptional set whose intersections must be managed. Therefore the single-set, all-radii quantifier is fully established.

## Adversarial cases and sharpness

- Coincident poles can be combined by adding positive coefficients, preserving the rational function and mass. The source would also permit repeated centers directly.
- A single pole at the origin gives the closed unit disk as an admissible exceptional set and the exact integral \(2\pi\log R\).
- Arbitrarily translated poles do not enter a prohibited ambient-disk hypothesis: localization is applied to the truncated quadrature set, not to all its poles.
- Widely separated disks can give a disconnected smash sum. The local harmonic test condition still applies componentwise and the theorem is stated for their whole union.
- Overlap is precisely what the smash sum handles; replacing it by the plain disk union would generally lose exact area and is not the candidate's construction.
- Tangent disks can give a closed exceptional set with a bounded hole. The quadrature kernel remains an admissible test at every point in that hole. Independent complex-kernel checks included three tangent equal disks around a noncentral hole point.
- The extreme near masses \(a=0\) and \(a=\pi\), radii arbitrarily close to one, and large radii cause no endpoint or sign failure.

For sharpness, set \(g(z)=z^{-2}\). The part of any area-\(\pi\) set \(S\) removed from \(D_R\setminus D_1\) has area at most that of \(D_1\setminus S\). The weight is at most one in that annulus and at least one in the unit disk. Thus the finite weighted annular loss is no larger than the weighted gain in the unit disk. The latter may be infinite; no invalid subtraction of two infinities is needed. It follows that every measurable such \(S\) has integral at least \(2\pi\log R\). Letting \(R\) increase excludes every smaller leading coefficient with any finite additive constant.

## Verification scope

Independent symbolic differentiation and algebra checks, angular and radial numerical integration, scalar boundary controls, and complex disk-kernel checks supplement the analytic review. They were replayed in ordinary and optimized Python, with the same mathematical results. The programs and raw outputs are not distributed in this edition. These finite diagnostics are supplementary: they do not prove the imported potential-theory or quasiconformal theorems, are not substitutes for checking their hypotheses, and are not hidden computational dependencies of the analytic proof.

Required corrections: **none**. Remaining limitations concern the nature of the review and historical attribution, not an identified mathematical gap. The audited original proof and source-hypothesis companion remain unchanged. Separately identified distributed editions preserve all mathematical content. The manuscript and audit are unrefereed.

## Public sources

1. A. Eremenko and D. H. Hamilton, *On the area distortion by quasiconformal mappings*, Proceedings of the American Mathematical Society 123 (1995), 2793–2797. [Primary PDF](https://www.math.purdue.edu/~eremenko/dvi/hamilt.pdf), [DOI](https://doi.org/10.1090/S0002-9939-1995-1283548-8).
2. Lionel Levine and Yuval Peres, *Scaling Limits for Internal Aggregation Models with Multiple Sources*, Journal d'Analyse Mathématique 111 (2010), 151–219. The inspected page numbering is that of the May 1, 2009 [author manuscript](https://lionellevine.github.io/scalinglimit.pdf); [arXiv v2](https://arxiv.org/abs/0712.3378v2) independently identifies the journal publication and is separately hashed. [DOI](https://doi.org/10.1007/s11854-010-0015-2).
3. W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory*, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), Problem 7.37.
