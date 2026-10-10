# Audit of the Gaussian Lipschitz Brenier claim

## Verdict

**PASS for the exact Gaussian target, with preprint status retained.** The proof route in Maja Gwóźdź, *Caffarelli Estimates under Lipschitz Perturbations*, arXiv:2609.04052v1, supports the original Gaussian conjecture after the substitution (B=-f). This is a source-credit finding, not a new proof or an independent discovery. No essential unresolved gap was found in the route needed for that target.

The distinction between mathematical review and publication status is important. The primary arXiv record retrieved on 10 October 2026 lists a single version, submitted 3 September 2026 at 16:24:45 UTC. It does not provide a journal reference or acceptance statement. This audit does **not** establish peer review, journal acceptance, community consensus, or priority over every other work. Appropriate wording is “independently checked full-target proof in a September 2026 preprint, credited to Gwóźdź.” An unqualified “published resolution” would exceed the evidence.

The acceptance here concerns the original Gaussian upper Lipschitz estimate for all dimensions and all globally Lipschitz perturbations. The reverse estimate and the optimization appearing with Theorem 1.1 were also checked. The broader noncommuting anisotropic theorem and the subsequent displacement and compact-mixture applications are not all certified by this bounded audit.

## Target identity and original context

- Numeric identifier: 30005263.
- Source alias: OWR-11695859-006.
- Curated title: *Dimension-Free Lipschitz Optimal Transport Maps*.
- Original primary source: Max Fathi, *Globally Lipschitz transport maps*, joint work with Dan Mikulincer and Yair Shenfeld, in *Heat Kernels, Stochastic Processes and Functional Inequalities*, Oberwolfach Report 49/2022.
- Original locator: Conjecture 1, PDF page 35, printed page 2845. The talk begins on PDF page 34, printed page 2844. Pages 33 and 36 contain neighboring talks; they are context, not additional hypotheses on this conjecture.
- Report DOI: https://doi.org/10.4171/owr/2022/49
- Publisher record: https://ems.press/journals/owr/articles/11695859
- Publisher PDF: https://ems.press/content/serial-article-files/46987

In the original problem, (gamma) is the standard Gaussian measure on Euclidean (mathbb R^n), and (mu=e^fgamma) is already a probability measure. The function (f) is globally Lipschitz. The requested conclusion is that the quadratic optimal transport map from (gamma) to (mu) admits a global Lipschitz bound depending only on the Lipschitz seminorm of (f), uniformly in (n).

The immediately following OWR Theorem 1 concerns a transport which need not be optimal. It is not itself a resolution of Conjecture 1. Likewise, an additive bound on (|T(x)-T(y)|), even one with a dimension-free additive error, does not control the difference quotient as (y) approaches (x).

Bounded source discovery does not establish exhaustive literature coverage, priority or absence of historical work.

## Exact comparison of hypotheses and conclusion

| Feature | Original target | Checked source specialization | Result |
|---|---|---|---|
| Dimension | Every finite (n), dimension-free bound | Paper fixes arbitrary (d\geq1); set (d=n) | Exact |
| Domain | Entire Euclidean space | (mathbb R^d), with full-support marginals | Exact |
| Source | Standard Gaussian | (gamma_d) | Exact |
| Target | Probability (e^fgamma_d) | (Z_B^{-1}e^{-B}gamma_d) | (B=-f) gives (Z_B=1) |
| Regularity of perturbation | Global Lipschitz only | Global (L)-Lipschitz (B); smoothness removed in Section 4.4 | Exact |
| Convexity | No convexity requirement on (f) | No convexity or semiconvexity requirement on (B) | Exact |
| Size | No smallness restriction | Every (L\geq0) | Exact |
| Boundedness | (f) may be unbounded | (B) may grow linearly and be unbounded | Exact |
| Symmetry or centering | None | None in Theorem 1.1 or its proof route | Exact |
| Map | Quadratic-cost optimal map | Brenier map (T=\nabla\Phi) | Exact |
| Sense of global map | Optimal maps initially defined almost everywhere | Globally defined Lipschitz representative, identified by uniqueness | Meets target |
| Constant | Depends only on (operatorname{Lip}(f)) | (mathfrak C(0,L)) | Exact |
| Uniformity | Uniform over functions and dimensions at fixed (L) | Same scalar expression for every (d,B) with (operatorname{Lip}(B)\leq L) | Exact |
| Extra moment hypothesis | Not separately stated | Finite second moments in Theorem 3.2 | Automatic here |
| Boundary assumptions | None | No boundary; both supports are (mathbb R^d) | Exact |

The automatic moment check is substantive: (|B(x)-B(0)|\leq L|x|), so a Gaussian density multiplied by (e^{-B(x)}) has an integrable Gaussian-times-linear-exponential majorant, even after multiplication by any fixed polynomial. Thus normalization is finite and positive, and the second moment required by the transport and approximation results is finite. Adding a normalization constant to (B) changes neither its Lipschitz seminorm nor the resulting probability measure.

The paper's constant is

\[
\mathfrak C(0,L)=\inf_{0<\beta<1}\beta^{-1}
\exp\!\left(\frac{4L^2}{1-\beta^2}\right).
\]

This is finite for every (L\geq0), for example by fixing (\beta=1/2). For (L=0), the target is the source and the limiting value is 1. Neither the dimension nor an additive value such as (B(0)) occurs in the constant.

## Main proof dependency map

The indispensable forward route is:

1. Brenier existence/uniqueness and full-space smooth regularity for smooth positive densities.
2. Lemma 3.9, importing the large-scale estimate of Gozlan and Sylvestre.
3. Lemma 3.10, giving supercoercivity of the smooth Brenier potential from surjectivity of its gradient.
4. Lemma 4.1, the translated Monge–Ampère identity.
5. Lemmas 4.2–4.5 and Appendix A.1, the compatible Schur and log-determinant inequalities.
6. Lemmas 4.6–4.8, construction and strict certificate for the radial penalty.
7. Proposition 4.9, the genuinely noncompact joint-maximum argument.
8. Section 4.4 together with Lemmas 3.11 and 3.13, passage from smooth perturbations to all globally Lipschitz perturbations.
9. Corollaries 3.4 and 3.6, or directly the scalar choices (Q=P=G=\mathsf R=S=I), for the claimed constant.
10. Corollary 5.5 and Theorem 1.1, taking source perturbation (a=0) and target perturbation (b=B).

For the additional lower Hessian estimate in Theorem 1.1, apply the same upper estimate to the reverse transport and use Lemma 5.1. Proposition 5.6 supplies optimization of the scalar constant. These additions are not required to answer the original one-sided question, but their applications were checked.

The earlier Gwóźdź manuscript arXiv:2608.15906 is cited as a methodological predecessor. It is not needed as an uninspected black box in the Gaussian proof route: the relevant identities, Schur inequality, penalty construction, maximum argument, and approximation argument are given again in the inspected 2609.04052v1. This audit does not claim to verify the earlier manuscript independently.

## Checks of the genuinely necessary argument

### Smooth full-space regularity

Proposition 3.8 uses positive smooth densities on all of (mathbb R^d). On each bounded ball, each density and its reciprocal are bounded. Thus the stronger bounded-ball assumptions in the Cordero-Erausquin–Figalli result are met; there is no substitution of the weaker interior-only condition at a boundary. Their full-space case gives a global homeomorphism and local smooth regularity of all orders. The Monge–Ampère determinant is positive everywhere by continuity of the density identity, so the gradient is a smooth diffeomorphism with positive-definite Hessian. Dimension one follows directly from the distribution-function formula.

The inspected author/arXiv copies label the relevant consequence Corollary 5, while Gwóźdź cites “Corollary 1” of the published paper. The mathematical result and its hypotheses were matched by content, rather than assuming matching numbers across versions. The primary publisher confirms the 2019 article, volume 39(12), pages 7101–7112, DOI 10.3934/dcds.2019297. No result was inferred solely from the mismatching label.

### Large-scale control and absence of circularity

In the Gaussian case the Gozlan–Sylvestre estimate is

\[
|T_{a,b}(x)-T_{a,b}(y)|\leq |x-y|+8\max\{\operatorname{Lip}(a),\operatorname{Lip}(b)\}.
\]

Theorem 5.15, Theorem 5.16 and equation (31) in v5 were inspected, including their proof from Theorem 4.2 and Corollary 4.3. The smoothness and convexity moduli used there are of the form (r^2/2+2L_a r) and (r^2/2-2L_b r). Their monotone conjugate and inverse calculations give the stated additive modulus. Its extension from almost every pair to every pair uses the already established continuous Brenier representative.

For the target here one can take (c_0=8L,c_1=1) in Lemma 3.9. Integration along the translation yields

\[
0\leq\mathcal B_m(x)\leq 8L|m|+|m|^2/2,
\quad
\mathcal B_m(x)=\Phi(x+m)-\Phi(x)-m\cdot T(x).
\]

This is independent of the base point (x). It controls the auxiliary maximization without assuming the differential Lipschitz estimate to be proved. Accordingly, the use of this imported result is not circular.

The underlying entropic argument in Gozlan–Sylvestre was checked at its required links: the Prékopa–Leindler inequality gives the upper modulus for the entropic transform; translation and Hölder give its lower modulus; the paired Schrödinger equations imply the infimal-convolution inequality for the smoothness modulus; convexity of that modulus gives the differential inequality integrated in Theorem 4.2. Corollary 4.3 passes to the Brenier potential using Nutz–Wiesel Theorem 1.1. That imported theorem requires a nonnegative continuous cost integrable against the product marginals, which the quadratic cost satisfies because both second moments are finite. The author's primary PDF was inspected for the complete statement and normalization. No finite-support or extra entropy assumption was silently introduced here.

### The translated identity and Schur term

Direct differentiation of the Monge–Ampère identity gives equation (4.8). The signs of the source and target Bregman terms were checked. In the Gaussian specialization the curvature terms become (-|m|^2/2+|\delta_m|^2/2), while the perturbation errors are bounded by gradient widths, at most (2L|\delta_m|) for the target perturbation.

At the joint maximum the block Hessian has lower-right block (C-\Pi\preceq0). Its negative-semidefiniteness forces the kernel compatibility ((C-A)\ker(\Pi-C)=0). This is essential: the proof does not replace an inverse by a pseudoinverse without a compatibility condition. Completing the square on the range of (Pi-C) gives the generalized Schur inequality; the compatible congruence in Lemma 4.3 preserves its quadratic form.

Appendix A.1 was checked algebraically, including noncommuting matrices. After normalization to (P=I), its functional is

\[
\operatorname{tr}((A+A^{-1}-2I)(I-C)^{-1})
-\log\det C+d-\operatorname{tr}A^{-1}+\log\det A.
\]

For positive (A+A^{-1}-2I), strict convexity and boundary divergence reduce the minimization to (C+C^{-1}-2I=A+A^{-1}-2I). The unique solution with spectrum in ((0,1)) is the spectral function (C=\min(A,A^{-1})). Reciprocal eigenvalues cause no ambiguity. The scalar contribution is zero below 1 and (t+2\log t-t^{-1}) above 1. Adding (delta I) and taking the infimum limit handles eigenvalue 1. Lemma 4.4 then handles (C\preceq P) by perturbing only the kernel of (P-C), using the established compatibility. The Rayleigh-quotient lower bound is in the correct direction.

### Penalty and noncompact maximum

For the Gaussian specialization choose (S=I) and any (0<\beta<1). The positive curvature gap is (1-\beta^2); the perturbation width numerator is bounded by (2L). The action is consequently bounded by (4L^2/(1-\beta^2)), as claimed.

The construction in equations (4.32)–(4.44) produces a strictly increasing (C^1) radial derivative (p), a (C^2) strictly convex penalty (Theta), and (D^2\Theta(0)=KS). The eventual cubic addition in (p) gives superquadratic growth of (Theta). It is joined where the unmodified derivative is already exactly linear, so the required derivatives match. A supremum over the compact sphere makes the auxiliary function continuous; differentiability of the supremum is not assumed.

The strict certificate (4.52) was checked in both ranges. In the inner range its lower bound contains ((1/2-\lambda)q^2d_{\beta,S}>0). In the outer range the chosen threshold makes (q^2d_0/2-qn_0>0). Thus strict positivity holds even when the positive-part expression in the penalty construction vanishes.

The noncompact step is more than a formal invocation of a maximum principle. Surjectivity makes (Phi) supercoercive by the finite Fenchel-conjugate argument in Lemma 3.10. After an additive normalization (Phi\geq0), the function

\[
J_\varepsilon(x,m)=\mathcal B_m(x)-\Theta(m)-\varepsilon\Phi(x)
\]

attains a maximum. If a positive violation exists, the large-scale corrector bound and superquadratic penalty keep the maximizing translations in a compact annulus. The same estimates bound (\varepsilon\Phi(x_\varepsilon)). Supercoercivity then gives (\varepsilon|x_\varepsilon|\to0), and the affine growth of (T) gives (\varepsilon T(x_\varepsilon)\to0). This justifies the limit in the Rayleigh quotient of equation (4.69).

The error (\varepsilon(d+L^2/4)) tends to zero with fixed (d). No dimension-dependent quantity survives into the final bound. Passing to a subsequence in the compact annulus gives a contradiction with the strict certificate. Taking the small-translation limit then yields (D^2\Phi\preceq KS), followed by the stated limits in (K) and (lambda). The order of these limits is legitimate; their parameters need not be uniform over dimensions to leave a dimension-free final expression.

### Removal of smoothness

The relevant part of Section 4.4 preserves the perturbation Lipschitz bounds and gradient widths under convolution. In the Gaussian specialization the reference potentials stay Gaussian, up to a harmless additive source constant in the paper's general construction. The smoothed (B_j) converge uniformly to (B) because (B) is globally Lipschitz and the mollifiers have shrinking compact support. Gaussian-times-linear-exponential domination gives weighted (L^1) convergence of the normalized densities and convergence in (W_2).

The smooth estimates are uniform in the smoothing parameter. The displayed first-moment estimate bounds (T_j(0)). Arzelà–Ascoli gives locally uniform subsequential convergence; the segment identities preserve convexity and identify the limiting map as a gradient. Tightness and local uniform convergence identify its pushforward. The usual Brenier uniqueness identifies it with the original quadratic optimal map, and positivity of the source density identifies continuous representatives everywhere. Second differences pass to the limit and Lemma 3.11 turns the distributional Hessian bound into a (C^{1,1}) potential and global Lipschitz gradient.

Lemma 3.13 additionally cites Villani's stability theorem. In this route the convex-gradient pushforward criterion already identifies the limit once the displayed convergence steps are in place. Thus the use of stability is consistent and introduces no stronger hypothesis than the verified finite second moments. Foundational Brenier existence/uniqueness and classical local Monge–Ampère regularity are used as published theorems; this bounded audit is not a reproof of those theories.

### Reverse bound and scalar optimization

For the reverse map the same hypotheses hold with the perturbations exchanged. The two continuous Brenier maps compose to the identity almost everywhere by uniqueness, hence everywhere because both densities are strictly positive. The conjugate-potential inequality in Lemma 5.1 correctly reverses the upper Hessian bound and gives the lower bound (mathfrak C(L,0)^{-1}I).

For (L>0), differentiating the logarithm of the scalar expression gives the critical equation stated in Proposition 5.6. Its unique solution for the forward case satisfies

\[
\beta_*^{-1}=\frac{2L+\sqrt{4L^2+2}}{\sqrt2},
\]

and substitution gives the formula on page 25. Expansion yields (4L^2+\log L+O(1)) for the logarithm. The accompanying one-dimensional example (B(t)=-L|t|) has derivative at zero equal to its normalizing constant, which is at least (e^{L^2/2}). This checks the stated order comparison, but sharp leading asymptotics are not part of the original target.

## Nonblocking editorial observations and scope limits

1. PDF cross-references often call lemmas and corollaries “Theorem”; the HTML presentation uses the more appropriate types. The theorem/equation numbers and actual mathematical content were checked in the PDF. The bibliography numbering also differs between the rendered HTML and PDF. The PDF and exact titles are the audit authority.
2. The cited full-space regularity consequence has different numbering in the inspected author copies. Its content and domain assumptions match, as explained above.
3. Lemma 3.12 writes an integral of an almost-everywhere Hessian along every line segment without explicitly handling exceptional segments. The standard proof uses mollification, or first proves the estimate for almost every parallel segment and then uses continuity. This is an exposition omission, not a counterexample to the lemma. It is not an essential obstruction for the original Euclidean bound: smooth maps are bounded before passage to the limit, and locally uniform limits preserve that bound; Lemma 3.11 also directly supplies the globally Lipschitz gradient. No new target argument was pursued to repair a failed claim.
4. No acceptance is given here to all of Section 6 or to every application of the full anisotropic theorem. The derivative lower bound and scalar optimization were checked only to accurately describe Theorem 1.1.
5. No absence-of-history, exhaustive-novelty, journal-acceptance, or scholarly-consensus claim follows from the bounded searches.

## Source identities and inspection record

All page references are one-based PDF page numbers. [SOURCE_METADATA.json](SOURCE_METADATA.json) records the public URLs, historical retrieval timestamps, byte counts, hashes and successful HTTP status. The primary PDF matched the earlier retrieved copy byte-for-byte.

| Source | Identity | Bytes | SHA-256 |
|---|---|---:|---|
| Claim | arXiv:2609.04052v1, 38 pages | 630541 | 1077982c0ecae8d89b231058b6b2485fe317ce8b0eee8777f9bcef58d78b0086 |
| Original OWR report | DOI 10.4171/owr/2022/49 | 3096049 | 635cc191b74e58cd4c126d6426c8d49de28a1b2c5e9db35070519466e9c95f46 |
| Gozlan–Sylvestre | arXiv:2501.11382v5, 43 pages | 572104 | 235df4756f82e595c345935e01aae91a03cfddc8c6112a355cd2cec59b279bfe |
| Cordero-Erausquin–Figalli | author-hosted current PDF, 13 pages | 362734 | cc9d73e836dffc9b3daca8105af90a9f8b911fc89b23259351b55322612aa1bd |
| Cordero-Erausquin–Figalli | arXiv:1902.07621v1 | 208800 | 1a07fe3bdbb9de5535e3e8c4b32a109581af40e326cbe6feea178b9cf5b7fadd |
| Nutz–Wiesel | author PDF dated 30 October 2021, 22 pages | 375604 | f4a72f158fe19291ebd2d4effd1d8735779ec1e015db2aebbf90b1302110b79b |

Primary links:

- Claim version and full text: https://arxiv.org/abs/2609.04052 and https://arxiv.org/pdf/2609.04052v1
- Large-scale estimate and version history: https://arxiv.org/abs/2501.11382 and https://arxiv.org/pdf/2501.11382v5
- Full-space regularity, author record and PDF: https://cvgmt.sns.it/paper/4317/ and https://cvgmt.sns.it/media/doc/paper/4317/regularity_transport_final-addition.pdf
- Published regularity article: https://www.aimsciences.org/article/doi/10.3934/dcds.2019297
- Entropic convergence theorem: https://www.math.columbia.edu/~mnutz/docs/potentialConv.pdf and https://doi.org/10.1007/s00440-021-01096-8

Text inspection covered the original OWR conjecture and neighboring context; the claim's Sections 1–4.4, pages 22–25 of Section 5 and the one-dimensional witness continuing onto page 26, including every proof on the Gaussian dependency route, Appendix A, and bibliography; Gozlan–Sylvestre Sections 2.1, the relevant subgradient-modulus proof in 2.2, Sections 3.1–3.2, 4.1, and 5.5; the Cordero-Erausquin–Figalli full-space theorem and its proof through the full-space case; and Nutz–Wiesel pages 1–3 for cost assumptions, normalization, and Theorem 1.1. These are mathematical-reading records, not an assertion that every imported foundational proof was recursively reproved. The later displacement proof inside Section 5.1 is outside the accepted scope.

The visual-inspection metadata lists the pages actually opened as images: 28 of 35 rendered pages. Rendered but unopened pages are not counted as visually inspected. Copied source documents, extracted source text, screenshots, raw retrieval captures and private coordination material are excluded from this edition.

## Recommended use of this audit

Credit the exact Gaussian result to Gwóźdź's September 2026 preprint, with the verified version and status qualifier. Preserve the original authors' conjecture attribution. This authored audit is AI-assisted and unrefereed; its acceptance verdict is a bounded proof-level review, not external human peer review, journal acceptance or proof-assistant certification. No new proof, novelty or priority is claimed.

Edition preparation preserves the complete substantive proof-route audit, exceptions and imported foundations. Five control-character corruptions were corrected to the intended beta and epsilon notation as editorial rendering only; no mathematical correction is introduced. Existing input bytes and publication integrity were rechecked. No new source retrieval, substantive proof-source inspection, literature search or mathematical computation was performed for this edition.
