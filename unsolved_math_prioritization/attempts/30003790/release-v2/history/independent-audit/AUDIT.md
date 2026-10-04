# Independent audit of noisy curved single index consistency

Problem 30003790 / OWR-16161-003, rank 618. Audit completed 4 October 2026.

## Verdict

The frozen packet contains a correct fixed-dimensional guarded-neighbor consistency theorem, correct exact slice-loss formulas, and useful conditional lemmas. Its blanket `unsolved` disposition needs a scope correction: failure to preserve a dimension-efficient rate does not refute the literal consistency request. The defensible frozen-packet conclusion is **conditional consistency established under additional assumptions; coverage of the original, incompletely specified model not established**. The stronger efficient-geometry objective remains unresolved by this packet, but it must be identified as a separate objective.

Two qualifications are required in the deconvolution discussion: coordinate weights need stated moment assumptions, and the tangent-nullspace assertion needs interior projection and an almost-everywhere conditional-law interpretation. Neither affects the guarded-neighbor proof. Joint measurability and deterministic response-independent tie handling should also be made explicit.

A broader consistency candidate is supplied separately in `AUXILIARY_CANDIDATE.md`. It was developed during this audit and has **not** received independent review; it is not evidence that the original frozen author already proved that broader result.

## Frozen input and reproducibility

The audit binds to the following exact inputs:

- Author MANIFEST.json SHA256: a18df1c214a6ea7ed7aa14d8a038827f463a7c9ff4f069228e0eb68b247367d2
- Author RESULT.md SHA256: 0c63e1801d50434d217a8a66d16ea8bad27cac4867919f7532abc4819eb9dc16

All nine listed author files match their recorded sizes and hashes. Running the frozen `verification/check.py` reproduced `verification/result.json` byte for byte, including all 700 rational guard cases. The author files were not edited. No remote writes were performed.

The audit adds 29,160 exact guard cases, exact one-dimensional convolution-density moment integrals, independent trigonometric quadrature, exact independent-sign variance checks, a response-reuse negative control, an endpoint-cap counterexample, an unguarded prediction-risk example, and a continuous Gaussian deconvolution control satisfying the L2-density condition. These controls pass. They supplement mathematical review; none is a theorem prover or a certificate of literature completeness.

## Primary question and current sources

Klock's final paragraph on p.1194 asks for a modification yielding noisy consistency. It specifies no explicit dimension-efficient rate in that question, although surrounding discussion motivates efficiency. The underlying index is a closest-point coordinate on a smooth curve, not a fixed linear projection. The source's risk is sample-conditional integrated squared error. [S1]

Wu and Maggioni is a published JMLR article, volume 27, article 155, pages 1-75; the PDF records August 2026 publication. ArXiv v4 is dated 24 August 2026. Theorem 3, pp.17-18, gives a decaying one-dimensional estimation term plus a nondecaying term. In its notation the latter is

    C2 = [f]_(C^s)^2 ((bar_sigma_gamma C_f / reach_gamma)
                     max(sigma_zeta, omega_f))^(2s).

Remark 4(iii) leaves removal of this approximation term to later geometric work. The theorem requires specified design, noise, curve, normal-variation and coarse-monotonicity hypotheses, with s in [1/2,1]. Its bound alone neither proves actual estimator inconsistency nor an impossibility for other estimators. [S3]

The inspected Kereta-Klock-Naumova preprint is v2, 5 September 2019. Equation (23), pp.13-14, retains a noise/curvature term. The journal paper appeared online in July 2020 and in the September 2021 issue, volume 10(3), pp.987-1029. The packet's 2021 issue citation is correct. This audit does not certify that paper's proofs; the newer paper itself reports proof gaps. [S2, S3]

The publisher PDF page and relevant JMLR page were privately rendered and visually inspected after web screenshot retrieval failed. Public web metadata and current full text were also checked. Full source documents and private working inventories are excluded from this deliverable.

## Coverage of the original model

The report supplies iid sampling and discusses smooth/Hölder regression on tubular designs. It does not explicitly supply the guard theorem's uniform lower-mass assumption, bounded support, or uniform conditional noise-variance hypothesis. The centering condition is conventional for regression but must remain explicit when asserting identification. [S1]

The lower-mass omission is substantive for the *displayed rate theorem*. For example, let

    gamma(t)=(cos t,sin t), -L<=t<=L<pi/4,
    X=(1+R) gamma(T), R uniform[-r,r], 0<r<1,

with independent T having density proportional to exp(-1/t^2) for t!=0, assigned density zero at zero. This law has full annular-strip support. Its coordinate transformation is a smooth local diffeomorphism with bounded Jacobian and inverse Jacobian. Around x=gamma(0), a ball of radius delta therefore has probability at most C delta^2 exp(-c/delta^2) for fixed positive c,C and all small delta. The ratio to delta^2 tends to zero. Hence no positive uniform lower-mass constant exists, despite the smooth curve, full tube support, and nontrivial normal variation. Taking F(X)=T and independent centered bounded noise keeps the other elementary model features.

This counterexample shows an assumption gap; it does not show inconsistency of the estimator on that design. In fact, the separate candidate proof removes the lower-mass condition for consistency by changing the guard schedule. A dimension-dependent guarantee is still a consistency guarantee. General nonparametric consistency and a new geometry-adaptive rate must not be conflated, and no mathematical novelty is certified here.

## Line by line mathematical review of RESULT.md

### Route 1 and equations 1 to 3

PASS under the displayed 0<b<L<pi/4, 0<r<1 and b+h/2<L, taking h>0.

The change of variables (T,epsilon) -> (Y,epsilon) has Jacobian one. The slice rectangle is wholly within the support constraint, giving conditional independent uniforms. Thus T=Y-epsilon has support of length 2b+h and variance b^2/3+h^2/12. The polar radius is positive and all arc angles differ by less than pi/2, so the unique closest point is gamma(T).

Write m=E[a(T)|A_h]=(0,sinc(b)sinc(h/2)). Its second component is positive, so minimizing 2-2 v^T m over unit v gives equation (2). Symmetry makes E[aa^T|A_h] diagonal with entries (1-c)/2,(1+c)/2, where c=sinc(2b)sinc(h)>0. Since ||vv^T-aa^T||_F^2=2-2(v^T a)^2, its minimum is 1-c, establishing equation (3), including its constant factor.

An independently trained random vector obeys the same bound after conditioning on its training sample and averaging. The restriction to one vector per slice matters. Neither formula is a lower bound for all covariate-refined tangent estimators or for regression risk. The packet correctly says so.

### Route 2 and equations 4 to 5

PASS for each explicitly bounded scalar weight with a known independent noise law; the coordinate-moment extension needs a correction.

For finite signed measures, conditioning on X gives convolution and characteristic-function multiplication. A nowhere-zero noise characteristic function identifies the clean measure uniquely. Bounded W guarantees finite total variation. For unbounded coordinate weights, identification instead needs E|W|<infinity; E||X||^2<infinity suffices for all first and second moments. Without any such condition, the asserted second moments need not exist.

For Gaussian noise and L2 clean density, let the stochastic Fourier error on [-U,U] be

    1_{|u|<=U} exp(sigma^2 u^2/2) (L_n(u)-E L_n(u)).

Its expected squared modulus is at most 1_{|u|<=U} M^2 exp(sigma^2u^2)/n. Plancherel gives the factor 1/(2pi), and integration over a length-2U interval gives M^2 U exp(sigma^2 U^2)/(pi n). The omitted clean Fourier tail is supported on the complement, so the cross term is exactly zero, not merely bounded. The cutoff makes the stochastic bound O(sqrt(log n)/sqrt(n)); the tail vanishes by integrability. Equation (5) is correct. Independence must mean iid copies of the weighted observation, as inherited from the model.

For unbounded W the same argument works with E[W^2] in place of M^2, when finite. E||X||^4<infinity is sufficient for all second-moment weights; bounded X is the simplest single assumption. Each weighted measure used in the statistical claim must have its own L2 density.

For a fixed bounded interval of positive clean mass, L2 numerator convergence gives integral convergence, and denominator convergence in probability gives covariance convergence in probability. Define a fallback when the estimated mass is nonpositive, or use max(estimated_mass,eta_n) with eta_n down to zero. Consistency does not alone give an expectation bound for an unregularized ratio.

The last geometric sentence needs a second correction. At a unique *interior* minimizer t, first-order optimality gives (X-gamma(t))^T gamma'(t)=0. With injective g, the conditional support is in one affine normal hyperplane, for almost every clean level where the conditional law is defined. Finite second moments and a rank-(D-1) covariance then identify the tangent line. At curve endpoints, first-order orthogonality can fail. For gamma(t)=(t,0), t in [0,1], let X be uniform on [-1,0] x [-1/2,1/2]. All points project to t=0; g(t)=t is injective, but the conditional covariance is diag(1/12,1/12), with no tangent nullspace. This atomic endpoint example is outside the L2-density statistical lemma; it specifically refutes an unqualified geometric assertion based on injectivity alone. Under absolute continuity of the clean-response law, endpoint levels have zero mass, but a pointwise conditional claim still needs the almost-everywhere qualification.

None of the fixed-interval claims supplies shrinking-window convergence or a prediction theorem. The packet appropriately leaves those steps open and does not assume a known Gaussian law in the original model.

### Route 3 and equation 6

PASS. The lower-Lipschitz inequality for g and two triangle-inequality applications yield the latent diameter bound. Half-open or consistently assigned bin endpoints cause no problem. Pilot independence is not needed for this deterministic inequality, but is relevant to later statistical reuse. The packet correctly does not infer a pilot guarantee, spectral gap, bin occupancy, or prediction consistency from it.

### Route 4 and equations 7 to 12

PASS as a theorem under its explicit assumptions, with routine measurable-construction clarification.

Interpret the random field as jointly measurable in the independent training data and query. Break ties by sample index, or by auxiliary randomness independent of all regression responses conditional on their covariates. A merely marginal statement of independence is not the intended condition. Finite order statistics are then measurable, and integrated risk is well defined.

Cauchy-Schwarz yields the sandwich, regardless of nonsymmetry or failure of a triangle inequality. Comparing kth order statistics proves equation (9), including tied or repeated covariates. For r_n=(2k/(cn))^(1/D), the lower-mass bound makes the binomial mean at least 2k. The half-mean Chernoff estimate exp(-mu/8)<=exp(-k/4) is valid for all sufficiently large n.

Conditioning on training data and regression covariates preserves conditional independence of the regression noises, because the regression pairs are iid and the training part is independent. Conditional noise means are zero and their averaged variance is at most sigma^2/k. Independence of epsilon from X is unnecessary here; conditional centering and the conditional variance bound suffice. The squared bias is bounded by H^2(2r_n/lambda)^(2s) on the good radius event, and H^2 B^(2s) otherwise. The cross term vanishes conditionally. This proves equation (11).

With k=floor(sqrt(n)) and lambda=n^(-1/(4D)), the guarded radius scale is O(n^(-1/(4D))), giving the stated squared-bias order n^(-s/(2D)). The variance order is n^(-1/2), and the exponential remainder is negligible. The rate is neither claimed nor proved optimal. The sample size n is the independent regression-part size; a fixed-fraction split only changes constants in terms of the total sample size.

The conclusion is mean integrated squared-error consistency and conditional integrated risk convergence in probability by Markov. It is not an almost-sure statement and not uniform convergence of the fitted function. This is a valid response to a fixed-dimensional consistency objective under those assumptions; adverse D-dependence is a limitation of the rate, not of consistency.

An exact negative control illustrates the independence requirement. Put all covariates at one point, F=0 and iid signs epsilon=+/-1. With n=8,k=2, selecting the largest responses gives mean 123/128 and MSE 31/32, whereas sigma^2/k=1/2. Thus a response-dependent tie or neighbor rule genuinely destroys the proof. The frozen rule excludes it.

### Route 5 and the flat jet example

PASS as a local-jet obstruction. Differentiating P(1/t)exp(-1/t^2) produces another polynomial in 1/t times the same exponential, so every right derivative tends to zero and agrees with the zero left derivative. The curves are regular because their first coordinate is t. Their arclength correction has flat derivative sqrt(1+psi'(t)^2)-1; integrating and locally inverting a smooth diffeomorphism preserves the identity jet. The curves nevertheless differ at every fixed positive t. This is not a lower bound against spatially observed polynomial fitting, growing-degree approximation, or general regression, and the packet makes that distinction.

## Exact changes required before relying on the disposition

1. Replace the headline and metadata's blanket `unsolved` framing with a scoped statement that conditional consistency is proved, original-model coverage is not established, and dimension-efficient consistency is a separate unachieved objective. Remove the suggestion that adding unspecified extra assumptions is itself the literal target definition.
2. At RESULT.md lines 105-107, add finite-second-moment conditions for coordinate-moment identification. At lines 110-131, state bounded X or finite fourth moments and individual L2-density assumptions when applying the quantitative result simultaneously to X and XX^T.
3. At lines 131-134, restrict the tangent-nullspace conclusion to unique interior projections, finite covariance, and almost every clean level. Keep the positive eigengap/rank condition.
4. At lines 181-189, require joint measurability and a deterministic index tie rule, or explicitly conditionally response-independent auxiliary randomness.
5. Do not add the auxiliary candidate to the set of independently validated frozen claims. Seek a fresh review before using it to change the mathematical disposition.

These are exact scoped corrections, not allegations that equations (1)-(12) are false under their stated scalar/theorem hypotheses.

## Audit limits

The complete author arguments were checked, and all controls replayed. This audit did not prove a dimension-efficient noisy estimator, an impossibility theorem, or global literature openness. It did not independently verify all 75 pages of Wu-Maggioni or all proofs in the 2019/2021 paper. It verified the specific theorem, remark, publication metadata, and saturation claims used in this packet. A computational pass cannot settle the open scope decision.

## Sources

[S1] T. Klock, “Estimation of Nonlinear Single Index Models,” in Nonlinear Data: Theory and Algorithms, Oberwolfach Report 20/2018, pp.1192-1194. https://ems.press/content/serial-article-files/46744 ; DOI https://doi.org/10.4171/OWR/2018/20

[S2] Z. Kereta, T. Klock and V. Naumova, “Nonlinear generalization of the monotone single index model.” Inspected preprint: https://arxiv.org/abs/1902.09024v2 . Journal metadata: https://academic.oup.com/imaiai/article-abstract/10/3/987/5874628

[S3] Y. Wu and M. Maggioni, “Conditional Regression for the Nonlinear Single-Variable Model,” JMLR 27(155):1-75, 2026. https://www.jmlr.org/papers/v27/24-2004.html ; PDF https://www.jmlr.org/papers/volume27/24-2004/24-2004.pdf ; current preprint metadata https://arxiv.org/abs/2411.09686v4
