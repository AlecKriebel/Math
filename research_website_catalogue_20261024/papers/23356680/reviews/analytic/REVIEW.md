# Independent analytic review: Zenodo 23356680

**Verdict: PASS within the stated mathematical scope.** No blocking mathematical defect was identified in either theorem or the full-comparison construction. This is an independent AI-assisted mathematical review, not formal proof verification or independent human peer review. First priority, present-day openness of the motivating question, and journal acceptance are not established.

Reviewed title: *A smooth Reshetnyak-harmonic sphere with unbounded distortion*, Alec Kriebel, version 1.0, 13 October 2026, DOI [10.5281/zenodo.23356680](https://doi.org/10.5281/zenodo.23356680). Review completed 2026-10-25 UTC (24 October locally).

## Identity and coverage

- Published six-page PDF SHA256: `a35dae6189ec49ed00e90ac38eeeda3f72a9e6737221de62554e913ed1157125`.
- Published `note.tex` SHA256: `6007845a15f67e4cf454a555e76f9ae7713b77b23caa210cf3df62c9b3a94480`.
- Source/verification ZIP SHA256: `956dfbc0366eae1122ef00f0a7a8535841101f84a46234659bd0476dfa1e7968`.
- Every page of the main PDF and the entire 372-line mathematical source were read. There is no separate mathematical supplement PDF for this record. The source contains the full written proofs. Page 5 was additionally rendered and visually inspected for the stress, transformation, and constants formulas.
- A fresh cached Tectonic build succeeds. Its six pagewise extracted texts are identical to the published PDF. Rebuilt PDF SHA256 is `12d78f46cbef5c3a9be3afef7a4f1492efe0b161aa432c27d85596616c39a440`; binary identity is **not** claimed. See `source_binding.json` and `source_build.log`.
- Historical package audit verdicts, archived analytic/computational reviews, priority reviews, and sibling reviewer opinions were not read before this verdict and are not evidence for it. Their advertised check counts were not adopted as validation. Fresh controls were written independently in this review folder.

Page coverage: p.1 abstract, definitions and Theorem 1; p.2 Theorem 2, Lemma 3 and start of Lemma 4; p.3 critical Sobolev exact-form argument, target and source construction; p.4 global construction, distortion, admissibility and non-minimizing distinctions, start of angular identity; p.5 stress, sphere argument, both bounds; p.6 attribution, limitations, AI disclosure and bibliography. All substantive claims on those pages were assessed.

## Exact claims and assumptions

Theorem 1 concerns a smooth homeomorphism from the **round** sphere into a specially constructed compact smooth Riemannian sphere. “Reshetnyak harmonic” means neighborhoodwise minimization of the squared operator-norm energy against every same-trace W¹,² map into the entire target, on every Lipschitz domain relatively compact in a suitable neighborhood. It does not mean merely stationarity, nor minimization within an image patch, continuous class, or homotopy class. The distortion is essentially unbounded, a stronger failure than a single degenerate equator. The target also has all the geometric hypotheses used for the pinned motivating question.

Theorem 2 concerns a different energy: the circular average of the squared metric differential, agreeing with Dirichlet energy for smooth targets. The target is only required to be complete; the map belongs to the standard essentially separably valued metric W¹,² space and has the same neighborhoodwise local minimization property. The conclusion is infinitesimal quasiconformality, allowing zero seminorms. The paper proves Q = 4 + √17 directly and derives applicability of the older bound 2√2 + √6. Neither constant is presented as new or sharp.

These are mathematical deductions under explicit definitions. No empirical model, numerical fit, or physical assumption is involved.

## Reconstruction of the counterexample

### 1. Flat-belt comparison, Lemma 3, p.2

The essential premise is a coordinate y that is 1-Lipschitz for **ambient target distance**, not just the intrinsic metric of a chart. A sufficiently small strongly convex metric ball inside the flat belt satisfies that premise: its globally minimizing geodesic between any two points remains in the ball and has the Euclidean coordinate length bound. Angular coordinates are lifted on the chosen ball, so winding is not silently ignored.

The infimum extension F(q) = inf[y(p) + d(p,q)] is finite and globally 1-Lipschitz, and F = y on the ball. This follows directly from the triangle inequality and the ambient Lipschitz premise. For any competitor v, Lipschitz composition and trace compatibility give f = F∘v with trace x, and |∇f|² bounded by the squared operator norm of dv. Writing f = x + w with w in W¹,²₀ gives the exact scalar identity

    ∫|∇f|² = |Ω| + 2∫∂xw + ∫|∇w|² = |Ω| + ∫|∇w|².

The cross term vanishes by approximation by compactly supported scalar smooth functions. The reference derivative diag(h′,1) has operator norm one when |h′| ≤ 1. This proves the complete competitor inequality. A competitor leaving the flat ball or winding elsewhere in the sphere still composes with the global F, so those cases are covered.

### 2. Conformal caps and critical Sobolev comparison, Lemma 4, pp.2–3

For a sufficiently small source neighborhood, a cutoff η equal to one near the compact reference image can have mass a less than half the total target area A. Then b = a/(A−a) lies in (0,1), and the multiplier (1+b)η−b stays in [−b,1]. Hence ω has comass at most one, equals the area form near the reference image, and has zero integral. Since the target is a connected oriented sphere, the top-degree cohomology criterion supplies a global smooth primitive α.

The exactness is crucial. An area form itself is not globally exact on a sphere and would not justify arbitrary bubbles. Here the pointwise bound v*ω ≤ |Jac v| ≤ ||dv||op² is valid even where the competitor reverses orientation. The smooth orientation-preserving conformal reference attains equality.

I checked the claimed critical W¹,² Stokes argument rather than presuming smooth target-valued density. A partition of unity and cutoffs express α as a finite sum f_j dg_j of globally smooth scalar functions. On the compact target, these functions and derivatives are bounded. Their compositions with a Sobolev map satisfy the scalar chain rule. For bounded F,G in W¹,², bounded mollification of F and strong L² convergence of the gradients give F_n dG_n → F dG in L² after taking an almost-everywhere convergent subsequence; dF_n∧dG_n → dF∧dG in L¹. Thus d(v*α) = v*ω holds distributionally.

Matching traces permit gluing v to the smooth reference outside Ω. The difference β of pulled-back primitives is L² and supported in the compact closure of Ω. Testing dβ against a cutoff identically one there yields zero; the derivatives outside Ω cancel. This proves equality of the ω integrals without assumptions about a continuous representative, degree, image containment, or homotopy. There is no missing smooth-density or no-bubble hypothesis.

### 3. Smoothness, coverage and distortion, pp.3–4

B is the usual smooth flat cutoff; its denominator in H is always positive. The apparent |s| singularity in ρ is harmless because H(|s|−2) is identically zero near s = 0. The belt is exactly flat for |s| ≤ 2. For s ≤ −3, z = exp(s+iθ) converts ρ²(ds²+dθ²) exactly to |dz|²; for s ≥ 3 the corresponding coordinate is ζ = exp(−s−iθ). The metric therefore extends positively and smoothly at both added poles.

In the source profile, η₀ transitions only where 1/4 < |t| < 1/2. On that interval a is a convex combination of t² and one, hence 0 < a ≤ 1; elsewhere the stated exact formulas apply. It vanishes only at t = 0. Its integral h is strictly increasing despite h′(0)=0, is odd, and is affine with slope one outside the transition. At both poles the induced map is multiplication by e^c in the corresponding complex coordinates. Thus u is a smooth homeomorphism of compact surfaces; it need not be a diffeomorphism.

For |t| < 1 the image lies in the flat belt and the scalar comparison applies in sufficiently small neighborhoods. For |t| > 1/2 and at both poles the map is conformal and the cap comparison applies. These are open sets with overlap; neither seam circle is omitted. Compact smooth geometry supplies geodesicity and a uniform contractible normal-ball radius. Nested uniformly bilipschitz charts also give the stated short-loop cone filling estimate with the original Lipschitz boundary parametrization. The cone has finite W¹,² energy, and its area is bounded by a uniform constant times length squared.

On 0 < |t| < 1/4, h′(t) = t² and the singular values have ratio t⁻². The source conformal factor cancels in the ratio. For any finite Q, a sufficiently narrow band has ratio greater than Q and positive round area 4π tanh δ. This establishes essential unboundedness independently of the derivative degeneracy on the measure-zero equator.

The operator-norm-squared energy satisfies the required admissibility properties. Its properness follows from uniform boundedness and equicontinuity of seminorms on the unit circle, with a closed limit class. Convexity of the squared operator norm and the affine-boundary average derivative identity give quasiconvexity even for maps into arbitrary finite-dimensional normed spaces.

### 4. Local minimization is not global homotopy minimization, p.4

The conformal coordinate identity has energy equal to target area. Substitution s=h(t) is legitimate for the monotone smooth h (the isolated zero derivative causes no issue). Since ρ=1 on the support of 1−a, the energy difference is exactly 4πc > 0. The two maps have degree one and are homotopic; therefore u fails global homotopy minimization.

For the KS energy, a nonnegative compactly supported first-coordinate variation inside 0<t<1/4 has first variation −4∫tψ < 0. Small variations remain in the flat patch and keep the trace. Thus the counterexample is genuinely not locally KS-minimizing. No inference identifying minimizers of comparable energies is made.

## Reconstruction of the separate KS theorem, pp.4–5

For fixed seminorm s, set F_s(A)=I(s∘A)/det A. The circle map w=Av/|Av| has angular Jacobian det A/|Av|². Using |Av|=1/|A⁻¹w| gives two powers of det A in the denominator and four powers of |A⁻¹w|. This avoids differentiating s itself, so nonsmooth and rank-deficient seminorms are covered. On a compact matrix neighborhood, derivatives of the smooth kernel are bounded times M(s)². That bound is integrable for the metric Sobolev map.

After changing variables in a domain variation, the seminorm is held at the new source point. Differentiating the matrix factor gives precisely

    T(s) = (1/π)∫s(w)²(4w⊗w − 2Id) dw.

Both signs of each compactly supported smooth domain variation are admissible same-trace competitors inside a minimizing chart. Local minimality therefore implies ∫T:DV=0. This step uses only domain stationarity, which is a valid consequence of the stronger hypothesis. It does not presume that arbitrary stationarity implies minimizing behavior.

T is symmetric, trace-free and locally L¹. Its divergence equations are a_x+b_y=0 and b_x−a_y=0 for entries (a,b;b,−a), the distributional Cauchy–Riemann equations for q=a−ib. Weyl regularity gives a holomorphic coefficient. Direct rotation/scaling of the integral confirms q_w=(dz/dw)²q_z under holomorphic source coordinate changes. Every point, including each pole, has its own minimizing chart, so this is a global holomorphic quadratic differential. The sphere has none: in a plane coordinate the coefficient is entire and decays as O(|z|⁻⁴) at infinity. Hence T=0 almost everywhere.

To check the elementary bound, normalize M=1 and put a minimizing direction along e₂. If L=s(e₁), triangle inequality gives 1≤L²+m². The rank-one comparison r(v)=L|v₁| satisfies |s−r|≤m and |s²−r²|≤2m on the circle. The matrix kernel has operator norm two, so ||T(s)−T(r)||≤8m. The exact rank-one stress is L² diag(1,−1). Balance gives 1−m²≤8m, hence m≥√17−4 and M/m≤4+√17. The zero seminorm is allowed; a nonzero rank-one seminorm cannot be balanced.

Finally J(A)=I(s∘A) is convex on the full matrix space. Balance implies DJ(Id)[D]=I(s)tr D. For positive symmetric S of determinant one, the supporting-hyperplane inequality and tr S≥2 show J(S)≥J(Id). The polar decomposition A=SR and rotation invariance then yield SL(2)-minimality. This is exactly the pointwise hypothesis of the older sharper bound. For inner-product seminorms, fourth angular moments give T=2G−tr(G)Id; balance yields weak conformality. Fourfold symmetry also balances non-Euclidean norms, so roundness is correctly not claimed in general.

## Primary-source checks

Primary PDFs were acquired independently; URLs, hashes, sizes, timestamps and failed access are retained in `reference_acquisition.json`. Downloaded PDFs and extracted reference text are ignored cache material.

- [MVW, arXiv:2503.08553v1](https://arxiv.org/pdf/2503.08553v1): checked the fixed general-energy convention, target hypotheses, Question 1.9, metric-Sobolev definitions and exact Definition 6.1. These agree with the note. The v1 PDF, rather than a potentially later HTML rendering, is the source of this conclusion.
- [Oberwolfach Report 30/2025](https://ems.press/content/serial-article-files/52249?nt=1), printed pp.1624–1626: checked the contribution and its Question 1. It fixes a suitable energy and asks the harmonic-sphere distortion question under the stated target assumptions.
- [Korevaar–Schoen 1993](https://intlpress.com/site/pub/files/_fulltext/journals/cag/1993/0001/0004/CAG-1993-0001-0004-a004.pdf): checked scalar Lipschitz composition and trace/gluing framework, particularly Theorems 1.12.2–1.12.3. The latter applies to Lipschitz domains, p>1 and matching traces; the present p=2 comparison meets these hypotheses. No NPC hypothesis from the paper’s later harmonic-map theory is imported.
- [Lytchak–Wenger, Energy and area minimizers, arXiv v2](https://arxiv.org/pdf/1507.02670v2): checked the definition of energy-minimal seminorm and Lemma 3.1/§3.3. The author-hosted September 2015 PDF URL timed out, so exact identity with that manuscript is not claimed.
- [Lytchak–Wenger, Area minimizing discs, arXiv v2](https://arxiv.org/pdf/1502.06571v2): checked the metric-differential chain rule in Lemma 4.9, energy comparability, and original pointwise Lemma 6.9. Completeness, p>1, biLipschitz precomposition and SL(2)-minimality are the relevant hypotheses; they are met. This directly verifies the older constant independently of the inaccessible author URL.

McShane extension and the elementary comass comparison were reconstructed directly. The general calibration citation is not used to import an unstated Sobolev theorem. The critical Sobolev identity is proved in the note and checked above. Classical de Rham cohomology, scalar Sobolev calculus, strongly convex neighborhoods and the sphere’s holomorphic quadratic-differential fact are standard ingredients used with their required hypotheses.

## Independent finite controls

`independent_controls.py` uses exact rational polynomial integration and a separate angular quadrature/finite-difference implementation. It does not import historical package verification code.

1. A zero-trace polynomial scalar competitor gives cross term exactly zero and positive energy excess exactly 1/45.
2. On t∈[1/16,1/8], x∈[0,1], a nonnegative zero-trace polynomial first-coordinate variation gives KS first variation exactly −1/2516582400, agreeing exactly with integration by parts. It is an admissible W¹,² control; the universal argument separately uses smooth compactly supported variations.
3. Exact fourth-circle moments verify T=2G−tr(G)Id for anisotropic, rank-one and isotropic Gram matrices.
4. With 262144 shifted angular samples, direct and changed-variable energy formulas agree within 2.08×10⁻¹⁰ across six seminorms and two nonsingular matrices. Seminorms include Euclidean anisotropic, rank-one, ℓ¹, ℓ∞, skew polyhedral and zero cases.
5. Finite differences of direct energy agree with the integrated stress within 4.77×10⁻⁷. Fourfold norms balance, rank-one stress remains nonzero, and the zero seminorm is handled.
6. A deliberate omission of one determinant power fails for every nonzero test seminorm, confirming the check detects this consequential formula error.

An initial finer finite-difference step than the angular grid spacing produced a 3.15×10⁻⁵ corner-integration artifact for ℓ¹. Increasing angular resolution and using a step larger than that spacing resolved it. This sensitivity is recorded rather than treated as a theorem defect. All floating-point checks are diagnostics, not rigorous error enclosures or substitutes for the written universal proofs.

## Strongest verified conclusion and remaining gaps

The full Theorem 1 construction is supported: a smooth homeomorphism from round S² to a compact smooth Riemannian sphere is locally Reshetnyak-minimizing against unrestricted same-trace Sobolev competitors, yet has essentially unbounded infinitesimal distortion. Its target meets the pinned 2025 metric-space hypotheses. The separate KS theorem and applicability of the older sharper bound are also supported.

**No unresolved mathematical gap was identified in these claims.** Scope limits remain: no proof-assistant formalization; no exhaustive replay of historical audit counts; no independent human peer review; no exhaustive priority search; no assertion that the final 2026 journal text retained identical question wording or that the question remained open then. The paper already states the relevant historical and review-status limitations. The failed author-hosted reference access is covered for the load-bearing statements by accessible primary arXiv sources. No correction or replacement construction was attempted because no defect requiring deferral was found.
