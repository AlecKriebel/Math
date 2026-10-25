# Analytic review: Zenodo 23157237, version 1.0

**Disposition: PASS within the expressly stated smooth stationary reversible model.** No substantive mathematical defect was found in the full eight-page published note or its two mathematical supplements. This is an analytic AI review, not human peer review, a formal proof certificate, or a novelty guarantee.

The strongest checked result is almost-sure, pointwise-in-model consistency of the specified finite-rank empirical spectral-equation estimator: local uniform recovery of the symmetric tensor and a separately fitted divergence; global L² recovery after tensor clipping; C² recovery of the invariant density; and consequent local uniform covariance/drift recovery. The alternative nonlinear regularization estimator in the supplement is also justified under the stated assumptions, but is a different estimator.

## Publication and evidence binding

- Title: *Consistent spectral recovery of smooth reversible diffusion tensors at a fixed lag*.
- DOI: https://doi.org/10.5281/zenodo.23157237 ; version 1.0; publication date 2026-10-05.
- Published PDF: `spectral_tensor_consistency.pdf`, 107,695 bytes, SHA256 `8ecd8528e17260fc14ff5d9b5de9006e4d3d472ba8c5a14e2c659c399dd29162`, MD5 `4fee799f3633d990e2a6589d39bbf11d`.
- Verification ZIP: 76,086 bytes, SHA256 `66ac1726139e20493cb8179e0786eef45a624a64ec7dc46221740cdbf8df03e2`.
- Main TeX SHA256: `288b644e29cdf06ac4b0246c8f30d317ab197aa5d18d3262a26a3b7989be28ad`.
- Fresh record, acquisition receipt, every extracted member, and supplemental proof hashes are recorded in `reviewed_assets.json`. The original queue-bound PDF was checked before reading and subsequently matched to the fresh Zenodo PDF. No verdict is based only on a local historical copy.
- An isolated Tectonic rebuild succeeded. Extracted layout text of the rebuilt PDF is exactly equal to that of the published PDF; differing binary hashes are not presented as byte-identical reproduction. See `source_build_receipt.json` and `source_build.log`.

## Coverage and independence

Read all eight actual published PDF pages and the complete TeX source. Coverage: pp1–2 model and contribution boundaries; pp2–3 smoothing and empirical construction; p4 Theorem2 and pair variance; p5 Lemma3, regularity, empirical derivatives and operator convergence; p6 functional calculus and Proposition4; p7 consistency and measurability; pp7–8 verification scope, AI disclosure and references.

Read both mathematical supplemental files completely: `classical_regularization_application.md` and `independent_classical_derivation.md`. Read the full README, source-edition notes, manifest/control selections, runner, and all eight control programs. Inspected fresh primary passages for every load-bearing external analytic interface described below. The remaining bibliography was not independently read in full; it chiefly concerns historical comparison rather than an unproved step in this theorem.

**Not wholly blind:** the main proof was independently reconstructed before supplemental bodies were opened. Those required mathematical supplements embed historical audit dispositions in their proof prose. These became visible before this final verdict, as did acceptance/status language in `SOURCE_EDITIONS.md` and the README. The supplemental standalone final Verdict was read only after the current main and supplementary analytic reconstruction. No current sibling reports were read, and no findings were received from siblings. Old status text is explicitly not evidence for this decision. The new control program was written before any supplied control implementation was read, although the supplemental mathematical prose was already visible.

## Exact hypothesis boundary

The domain is known, bounded, connected, and C∞ smooth, in dimension d≥2. The unknown symmetric tensor S and density μ are C∞ up to the boundary, with known positive lower/upper ellipticity and density bounds and normalized μ. The process is stationary, reversible and conormally reflected, with generator L=μ⁻¹div(S∇). Observations are exact positions at a known fixed positive lag. The limit is increasing observation count, not decreasing lag.

The generator expansion gives interior covariance 2S/μ and drift (div S)/μ. No derivative of μ belongs in that drift under this parameterization. Ordinary normal reflection is not interchangeable with conormal reflection for an anisotropic tensor. The theorem does not require a known derivative norm or known spectral gap, but constants and conditioning may depend on the fixed truth. It does not establish a class-uniform rate, minimax result, noise tolerance, nonreversible or rough-coefficient extension, numerical accuracy, or tractable general-domain implementation. The separately fitted divergence is not claimed to equal the derivative of the tensor estimate.

## Reconstruction of the main proof

### 1. Boundary smoothing is adequate at the claimed orders

The seven reflection coefficients match normal polynomial derivatives through order six. Chart cutoffs, a sufficiently small exterior collar, and interior zero extension produce a Cʳ-bounded extension for r≤6. Convolution with a smooth mollifier then has a jointly Borel kernel, smooth in the evaluation variable. Changing reflected variables back into D gives the stated h⁻ᵈ⁻ʳ derivative envelope: fixed chart Jacobians and reflection factors only change constants. Smoothness of the kernel in its evaluation variable does not require the extension itself to be C∞.

C³-to-C² convergence suffices for the marginal, and separate-variable extension supplies the mixed C²,² pair convergence. The fifth total evaluation derivative used for net interpolation is controlled directly by the mollifier. Signed kernels and lack of exact mass preservation are harmless because the proof does not treat this smoother as a Markov kernel. The convention at sampled boundary points changes a countable collection of null events under stationarity.

The density saturation has room above and below every admissible truth. Its normalization ensures a deterministic positive lower bound even for adverse data. Eventual uniform consistency makes saturation inactive, after which normalization tends to one. The empirical pair kernel is symmetric and finite-rank, although generally indefinite and not marginally matched to the density estimate; these facts are all acknowledged and used correctly.

### 2. Dependence and derivative convergence close without hidden tuning

Weighted Poincaré, ellipticity, and the upper density bound give a positive L² spectral gap. For a centered pair observable Zᵢ, conditional means at its last and first state yield

`Cov(Z₀,Zₐ)=〈r,P^(a−1)s〉μ`, for a≥1.

The exponent a−1 is essential at the shared endpoint. Conditional Jensen and the gap give the stated variance bound for an average of n pairs. The argument applies to each bandwidth-dependent observable and assumes neither independence of pairs nor independence across dyadic prefixes.

For differentiated pair kernels with at most two derivatives in each variable, the envelope is O((j+1)^(2d+4)), the pointwise variance is O((j+1)^(4d+8)2⁻ʲ), and a mesh 2^(−j/(4d)) in 2d dimensions has O(2^(j/2)) points. Chebyshev at threshold (j+1)⁻¹ gives a summable O((j+1)^(4d+10)2^(−j/2)) bound. The extra derivative costs only a polynomial factor, so interpolation off the net vanishes. The corresponding d-dimensional state calculation gives the reported summable bound. A fixed neighborhood makes short interpolation segments legitimate for nonconvex D.

The population kernel is smooth at positive time: min–max comparison gives polynomial eigenvalue counting, elliptic graph estimates give polynomial derivative growth of normalized eigenfunctions, and the positive-time exponential weights dominate each derivative series. Bias convergence and Borel–Cantelli establish all required derivatives on one probability-one event. Unknown truth constants do not enter the dyadic or bandwidth choices.

### 3. The spectral logarithm is regularized in the actual objective

Conjugate the transition operator to L²(dx), and write W=μ⁻¹/²T. Kernel convergence controls both T in operator norm and W as a map into C² on any compact interior set. These are different controls: operator-norm convergence alone would not control the derivative rows. The paper establishes the stronger one explicitly.

The normal equations are bounded-functional expressions `Aⱼ=Bⱼg(Tⱼ)Bⱼ*` and `rⱼ=(μⱼ/Δ)Bⱼh(Tⱼ)eⱼ*`, where g(t)=t² and h(t)=t²log t on t>0 and both vanish on t≤0. Both are continuous at zero. The two outer factors contribute two further eigenvalue powers, giving exactly κ⁴ in the least-squares equations. No logarithm of a negative or zero empirical eigenvalue is evaluated.

A common bounded spectral interval and polynomial approximation imply continuous-functional-calculus convergence without matching empirical eigenvectors. Repeated eigenvalues, splits, rank changes, zero crossings and empirical eigenvalues exceeding one therefore do not break the argument. The fit includes every positive empirical eigenvalue; no fixed, unproved population truncation is substituted. This avoids falsely asserting continuity of the unbounded raw operator logarithm.

### 4. Full jet excitation is proved, including mixed derivatives

The symmetric Hessian coordinates require the factor two on off-diagonal entries. With that convention, the generator eigenfunction equations give r=Aθ. If a vector annihilates the quadratic form of A, positivity of every population transition eigenvalue implies that it annihilates every eigenfunction's full gradient/Hessian jet.

Any compactly supported smooth test function lies in every power domain of I−L: local differentiation preserves its interior support and hence all iterated conormal conditions. Spectral partial sums converge in those graph norms, and sufficiently high graph regularity and Sobolev embedding give C² convergence. Thus the vector annihilates every compactly supported test-function jet. Cutoff affine and quadratic polynomials prescribe all gradient and symmetric-Hessian components independently, forcing the vector to vanish. Continuity and compactness supply a positive minimum eigenvalue on each compact interior E. This is a truth-dependent local lower bound, not a uniform condition number over the model class.

### 5. Ridge, global tensor convergence, and measurability

The normal matrices become uniformly positive definite on each fixed compact E. The exact error identity therefore has a uniformly bounded inverse, and every positive deterministic ridge tending to zero works. No noise/ridge ratio is needed here; imposing such a requirement would ignore the proved positive definite limit.

Frobenius projection onto the known closed convex tensor interval fixes the truth and is nonexpansive. Local convergence gives interior pointwise convergence on a countable exhaustion; bounded clipping and finite domain volume give global L² convergence. This does not establish global convergence of the divergence or convergence of tensor derivatives, and neither is asserted.

The finite-feature formulas are correct even for singular Gram matrices. The identity `V*a(VCV*)V=G^(1/2)a(G^(1/2)CG^(1/2))G^(1/2)` follows for polynomials, including the constant term, and then for continuous a. No Gram inverse or measurable eigenvector selection is needed. Data-dependent feature derivatives, known-domain integrals, matrix square roots, continuous functional calculus and ridge inversion are Borel; the displayed finite formulas yield continuous spatial outputs. Separability on compact sets and bounded clipped output complete the stated random-element measurability. The latest dyadic prefix uses only observed states and tends to infinity along all sample sizes.

## Supplementary alternative estimator

The alternative argument is independently valid, but should remain distinguished from the spectral theorem. Set a fixed Sobolev index s>d/2+2 and fit all admissible Hˢ coefficients, without a known norm bound. The pointwise constraints and normalization define a closed convex, weakly closed subset. Bounded Hˢ sets are compact in C², hence in C¹.

The conjugated generators have a common H¹ form domain even though their conormal operator domains vary. C¹ coefficient convergence gives uniform form convergence and coercivity; applying the variational equation to the difference of resolvents proves norm-resolvent convergence. A continuous function of the resolvent gives semigroup operator convergence. This alone would not imply density convergence. The necessary extra step is present: min–max comparison with Neumann Laplacian eigenvalues yields a uniformly square-summable heat singular-value tail. Finite initial singular values plus this tail give Hilbert–Schmidt convergence and hence L² convergence of joint densities.

Equal joint densities first identify μ by marginalization. Equal positive-time self-adjoint semigroups identify their generators through the unbounded spectral calculus; zero is an accumulation point but has zero spectral projection. Compactly supported affine/quadratic test functions identify the tensor on the interior, and continuity extends equality to the boundary. This works on the full candidate Hˢ class and does not presume inverse continuity on an unbounded class.

An ordinary product-space kernel estimator needs only L² accuracy. The zero-extended joint density has translation squared error O(|a|): interior Lipschitz variation plus an O(|a|) boundary layer. The product domain's corners do not invalidate the finite-perimeter translation estimate. With bandwidth (j+1)⁻⁴, its bias is O((j+1)⁻²), and the same overlapping-pair variance bound gives almost-sure stochastic L² error O((j+1)⁻¹).

Choose regularization αⱼ=(j+1)⁻¹ and objective tolerance εⱼ=(j+1)⁻². A fixed countable dense subset of the admissible Hilbert-space set, and the first index within εⱼ of the countable infimum, give a measurable approximate minimizer. This is mathematical existence, with no finite search or numerical feasibility claim. Truth comparison bounds its Hˢ norm because both δⱼ²/αⱼ and εⱼ/αⱼ vanish. Compact subsequences, forward continuity and injectivity force convergence of the whole sequence in C¹. Thus this alternative also consistently estimates the divergence globally. Its stronger topology is a feature of a different, potentially intractable global optimization procedure; it does not retroactively prove the spectral estimator.

## Primary interfaces checked afresh

Primary downloads, hashes and retrieval times are in `primary_sources.json`; local third-party copies and rendered derivatives remain in the ignored reference cache.

- [Grubb, Math. Nachr. 2016](https://web.math.ku.dk/~grubb/MN16.pdf), Section2, Theorem2.2 and Corollary2.3: smooth bounded domain, strongly elliptic scalar second-order operator, suitable elliptic Neumann-type condition, power-domain Sobolev regularity. The present positive shift I−L is invertible; its conormal operator is elliptic, and positive smooth weights give equivalent L² norms. No arbitrary H²ᵃ function is silently assumed to satisfy power-domain boundary conditions.
- [Grubb's Sobolev chapter](https://web.math.ku.dk/~grubb/dist6.pdf), Corollary6.12: bounded smooth domain and strict Sobolev index exceeding derivative order plus d/2. The chosen graph power meets this threshold.
- [Hansen–Scheinkman 1993](https://www.nber.org/system/files/working_papers/t0141/t0141.pdf), printed p26/PDF p28, visually inspected because text extraction is blank: Proposition5.5 establishes identification for self-adjoint generators sharing a positive-time transition operator. The current reconstruction also verifies the logarithm domain and subsequent coefficient identification.
- [Alberti–Barnes–Jambhale–Nickl v2](https://arxiv.org/pdf/2410.19393v2), Lemma3.8 and its proof: cutoff-coordinate and spectral-Sobolev gradient excitation is prior. It concerns scalar conductivity; it is not treated as a tensor full-jet theorem. The latter is proved directly here.
- [Lenzen–Scherzer 2004](https://franklenzen.de/pdf/lenzen_scherzer_eccomas2004.pdf), Section3 and Theorem3.2: nonlinear Hilbert-space regularization for continuous weakly closed maps, with squared noise divided by regularization vanishing. The current constrained approximate-minimizer argument supplies its own application and measurability details; the citation alone does not establish them.
- [Hansen 2008](https://users.ssc.wisc.edu/~behansen/papers/et_08.pdf), Assumptions1–3 and Theorem3: bounded smooth compact kernels and sufficiently fast mixing yield centered strong uniform convergence. The joint-density condition applies only at sufficiently separated lags, permitting overlapping lag vectors. In the present setting, gap contraction gives geometric mixing; for pair separations at least two, the joint density is a product of bounded positive-time transition densities. The supplemental proof in fact uses its own weaker elementary L² estimate and does not require this stronger imported result.
- [Reiss, OWR24/2017](https://publications.mfo.de/bitstream/handle/mfo/3588/OWR_2017_24.pdf), complete contribution pp1507–1509: the final multidimensional question asks for convergence of matrix reconstruction from empirical eigenpairs and invariant density, with spectral retention to be chosen. The current result supplies one such method under its additional explicit smooth-model assumptions. It does not cover every possible reading of reflection or nonsmooth setting.

## Computational corroboration and limits

`fresh_controls.py` passes **60 fresh exact rational/symbolic assertions**. These include direct Markov path enumeration with nonsymmetric pair observables; reflection moments and failure at the next order; singular, nontrivial Gram factorizations; repeated, negative, zero, small and above-one eigenvalues; both normal-equation feature formulas; factor-four spectral bookkeeping; anisotropic variable-coefficient jet identities and a missing-factor-two negative control; full jet spanning; conormal/normal distinction; vanishing ridge much smaller than perturbation; and an operator/HS negative control. These were written before reading supplied implementations. Their finite scope is stated in the results; they do not prove statistical or elliptic limits.

All **eight published suites** replayed successfully, with fresh processes, exact package/source hash checks and expected scientific-output comparisons. Individual recorded counts are 11 author-turn1, 42 author-turn2, 1,905 historical-independent, 3,690 empirical, 43 spectral, 35 scope, and 49 mechanism assertions, plus the auxiliary suite. These counts overlap and are not eight independent theorem proofs. A few published illustrative floating diagnostics use the runner's disclosed tolerances; fresh reviewer matrix/path controls use exact arithmetic. Full receipts and scientific outputs are in `published-replay/`.

## Remaining gap and disposition

No unresolved load-bearing proof gap was identified within the theorem's hypotheses. No paper changes or repairs were made. The finite controls are corroborative, and neither they nor this review establish practical finite-sample performance. No independent general-domain numerical estimator was implemented or tested. This analytic review does not reproduce the entire historical novelty audit, resolve the explicitly uninspected CV2011 publisher-final edition, or prove worldwide priority. The paper already limits those claims.

The review is complete for its assigned mathematical scope, with the explicit non-blindness qualification above. Suitable downstream wording is “the stated consistency theorem survived this analytic review,” not “the paper has been peer reviewed” or “the method has been numerically validated.”
