# Adversarial review of Zenodo 23157237, version 1.0

**Conclusion:** the published fixed-lag spectral-consistency theorem is supported at its stated smooth, reversible, conormal-reflection hypotheses. I found no substantive mathematical defect after reconstructing the proof, checking its load-bearing primary interfaces, replaying the published controls, and developing fresh exact controls. This is an AI-assisted mathematical review, not human peer review, a formal proof certificate, or a worldwide novelty/priority certificate.

## Publication binding and reading coverage

Title: *Consistent spectral recovery of smooth reversible diffusion tensors at a fixed lag*. Author: Alec Kriebel. Publication date: 2026-10-05. DOI: [10.5281/zenodo.23157237](https://doi.org/10.5281/zenodo.23157237).

Fresh source receipt retrieved 2026-10-25T01:14:04.782445+00:00. This review binds to:

| File | Bytes | SHA-256 |
|---|---:|---|
| `spectral_tensor_consistency.pdf` | 107695 | `8ecd8528e17260fc14ff5d9b5de9006e4d3d472ba8c5a14e2c659c399dd29162` |
| `spectral_tensor_verification.zip` | 76086 | `66ac1726139e20493cb8179e0786eef45a624a64ec7dc46221740cdbf8df03e2` |

Both SHA-256 and the Zenodo MD5 checksums were independently checked. The full eight-page actual published PDF and full mathematical TeX were read. The eight control program sources, portable runner, source-edition notes, and mathematical sections of both supplementary classical-regularization derivations were read. The source itself was not repaired or changed.

**Independence disclosure.** No current sibling report was read. The source-edition notes and the mathematical supplemental derivations embed historical acceptance/“attack disposition” statements. I encountered some of those while locating primary sources and reading proofs, and excluded them as evidence. The separate final verdict section of `independent_classical_derivation.md` was skipped. Therefore this is independently reconstructed analysis, but not a perfectly blind review. The fresh controls were independently implemented after reading the supplied control sources; they are not a blind replication.

## Exact proposition reviewed

The domain is a known bounded connected (C^\infty) domain (D\subset\mathbb R^d), (d\ge2). The truth is fixed, with symmetric (S\in C^\infty(\overline D)), invariant density (\mu\in C^\infty(\overline D)), and known fixed bounds

\[
0<\ell I\le S\le\Lambda I,\qquad 0<c\le\mu\le C,\qquad\int_D\mu=1.
\]

The generator is (L=\mu^{-1}\operatorname{div}(S\nabla)) with **conormal** boundary condition (n\cdot S\nabla u=0). The observations are stationary exact positions (Y_i=X_{i\Delta}) at one known fixed (\Delta>0). No unknown domain, sensor error, nonstationary start, nonreversible drift, or ordinary-normal replacement of anisotropic conormal reflection is included.

The specified estimator uses the first (2^j+1) observations, (j=\lfloor\log_2N\rfloor), a known-domain signed smoother of bandwidth (h_0/(j+1)), a saturated normalized density estimate, and a symmetrized finite-rank pair-density estimate. It fits **all positive** empirical eigenpairs with transition-eigenvalue weights (\kappa^4), omitting zero and negative eigenvalues. It includes a positive deterministic ridge (\lambda_j\to0). The claimed conclusions are, on one probability-one event, for **every** compact (E\Subset D):

\[
\widehat S_j\to S,\quad \widehat v_j\to\operatorname{div}S
\quad\text{uniformly on }E;\qquad
\widehat S_j^{\,c}\to S\quad\text{in }L^2(D);
\qquad \mu_j\to\mu\quad\text{in }C^2(\overline D).
\]

Here (\widehat v_j) is the separately fitted vector, **not** (\operatorname{div}\widehat S_j); the superscript (c) means projection onto the known ellipticity interval. Consequently the interior covariance (2S/\mu) and drift (\operatorname{div}S/\mu) are recovered locally uniformly. The statement is pointwise in every fixed truth, not uniform over a smoothness class. It supplies neither a statistical rate nor a practical finite-precision implementation.

## Reconstructed proof and falsification attempts

### 1. Fixed-lag identification and the logarithm

In (L^2(\mu,dx)), the closed form is (\int_D\nabla f^TS\nabla f\,dx). Its conormal realization is nonnegative after changing the sign of (L), self-adjoint, and has compact resolvent. Thus the transition eigenvalues are (e^{-\Delta\gamma_k}>0), including the constant mode at one. Zero is an accumulation point, not an eigenvalue. The real self-adjoint generator is uniquely determined by the positive transition operator through the unbounded spectral logarithm. The joint stationary density also determines (\mu) through its marginal.

This does **not** make the unweighted logarithm a continuous inverse near zero. The estimator avoids that false inference. Its stability proof applies bounded continuous functions (g(t)=t^2\mathbf1_{t>0}) and (h(t)=t^2\log(t)\mathbf1_{t>0}), both extended by zero for (t\le0), to the estimated operator. It never takes a real logarithm of a negative empirical eigenvalue. Positive eigenvalues above one are permitted in early samples and cause no analytic problem.

Fresh controls contrast (e^{-k^2}) and (e^{-2k^2}): their differences tend to zero while their logarithms differ by (k^2). They also check the weighted limit (t^2\log t\to0). An angular-drift aliasing example on a circle verifies that reversibility really matters; this deliberately lies outside the paper's hypotheses and is not a counterexample to them.

If two coefficients in the exact class gave the same joint density, their marginals, transition operators, and self-adjoint generators would agree. Applying the generators to compactly supported affine/quadratic cutoff functions then identifies the second- and first-order coefficients locally. No unobserved coordinate change is available because the domain and observation coordinates are fixed.

### 2. Conormal regularity, smoothing, and statistical convergence

The graph regularity invoked in equation (16) applies to (A=I-L), whose principal coefficient is (S/\mu), with the first-order conormal boundary operator. This is a smooth strongly elliptic Neumann-type problem; the positive shift removes the constant-mode kernel. Equivalence of the weighted and ordinary (L^2) norms identifies the same power domains and permits the ordinary Sobolev estimates. This is not an assertion that an arbitrary ordinary-normal boundary condition is equivalent to the conormal one.

The min–max quotient compares the eigenvalues with the Neumann Laplacian by constants (\ell/C) and (\Lambda/c). Polynomial counting and graph regularity give polynomial (C^r) eigenfunction bounds. Exponential positive-time damping therefore makes every fixed differentiated heat-kernel expansion absolutely and uniformly convergent on (\overline D^2). Smoothness of the stationary pair kernel, including boundary smoothness, follows at the fixed positive lag.

The extension coefficients (28,-112,210,-224,140,-48,7) satisfy the seven matching moment identities. Seven reflected chart terms match derivatives through order six; they need not define a (C^\infty) extension. Six derivatives are enough for the required tensor-product (C^{2,2}) bias argument. Convolution makes the output smooth at every fixed positive bandwidth and supplies the all-order derivative bounds on the kernel. Known chart cutoffs keep all reflected arguments inside their charts. The kernel may be signed and need not preserve mass. These facts do not invalidate the later normalization or spectral calculation.

The data argument treats adjacent observation pairs as dependent. For centered (Z_i=F(Y_i,Y_{i+1})-\mathbb EF), define the two conditional endpoint functions (r(z)=\mathbb E[Z_0\mid Y_1=z]) and (s(z)=\mathbb E[Z_0\mid Y_0=z]). Stationarity, conditional independence across the bridge, and the Markov property give

\[
\operatorname{Cov}(Z_0,Z_a)=\langle r,P^{a-1}s\rangle_{L^2(\mu)},\qquad a\ge1.
\]

The exponent is (a-1), including the overlapping case (a=1). Weighted Poincaré yields a mean-zero contraction (\rho<1); Jensen bounds both endpoint norms by (\sqrt{\operatorname{Var}F}). Summing covariances gives equation (14), with a finite constant depending on the fixed truth. Fresh exact four-state controls check these identities and enumerate entire short paths. Even when the states are independent, adjacent additive pair observables have covariance one in the chosen example; replacing (a-1) by (a) would fail. The paper uses the correct exponent.

For pair-kernel derivatives of order at most two in each variable, summands are bounded by (O((j+1)^{2d+4})). Their average variance is (O((j+1)^{4d+8}2^{-j})). A mesh (2^{-j/(4d)}) on the (2d)-dimensional domain has (O(2^{j/2})) points. At threshold ((j+1)^{-1}), the union probability is (O((j+1)^{4d+10}2^{-j/2})), which is summable. The extra kernel derivative controls interpolation from the net. The extension to a fixed neighborhood deals with short segments in a nonconvex domain. The state estimate similarly gives (O((j+1)^{2d+6}2^{-3j/4})). Borel–Cantelli applies separately to finitely many derivative indices, without independence across bandwidths or prefixes.

Uniform convergence eventually places the raw density estimate inside the region where the saturation is the identity. Its normalization tends to one, giving the claimed (C^2) density convergence. At every earlier sample, saturation gives a deterministic positive lower bound. Stationarity assigns probability zero to boundary observations; the Borel boundary convention consequently changes no almost-sure statement. Unknown smoothness norms and mixing constants are used only in the proof, not in tuning the slow logarithmic bandwidth.

### 3. Spectral stability, full jets, and coercivity

On ordinary (H=L^2(D,dx)), use the conjugated transition operator (T) and (W=\mu^{-1/2}T). The established derivative convergence gives both (T_j\to T) in operator norm and (W_j\to W) in (H\to C^2(E)) norm. The second, stronger assertion is necessary for derivative evaluation; operator convergence alone would not justify it.

Let (B_j(x)f=J(W_jf)(x)) and (e_j(x)f=(W_jf)(x)). The jet contains the diagonal Hessian, **twice** each mixed Hessian entry, and the gradient. The factor two exactly matches a symmetric tensor's off-diagonal contribution. Fresh symbolic controls in dimensions two through five verify the complete divergence and covariance/drift identities with nonconstant positive definite tensors and varying positive densities.

The normal matrix and right side are

\[
A_j=B_jg(T_j)B_j^*,\qquad
r_j=(\mu_j/\Delta)B_jh(T_j)e_j^*.
\]

Each outer factor contributes one transition eigenvalue and the middle function contributes two, reproducing the fourth-power weights exactly. Uniform polynomial approximation on a common bounded spectral interval proves continuous functional-calculus convergence. The argument accommodates multiplicities, splittings, negative modes, zero crossings, tiny positive modes and eigenvalues above one; it does not require a measurable or stable eigenvector labeling.

For every interior (x), a vector annihilating the limiting quadratic form annihilates the jet of **every** population eigenfunction, because all its weights are strictly positive. A function in (C_c^\infty(D)) lies in every power domain: the differential operator preserves compact interior support, so all iterated conormal conditions are automatic. Its spectral partial sums converge in arbitrarily high graph norms, hence in (C^2) by Sobolev embedding. Thus the same vector annihilates all compactly supported smooth jets. Affine and quadratic polynomials multiplied by a cutoff equal to one near (x) realize arbitrary gradient and symmetric Hessian. The vector must vanish.

This proves full positive definiteness; it does not assume an unverified finite-mode rank condition. Continuity and compactness give (A(x)\ge a_EI>0) on each fixed interior compact. The constant can depend arbitrarily badly on the truth, lag and compact set. A prescribed finite set of modes, or a class-uniform condition number, is not established. The empirical fit uses all its positive modes, with a count that grows with the observed prefix.

The identity

\[
\widehat\theta_j-\theta=(A_j+\lambda_jI)^{-1}
\big[(r_j-r)+(A-A_j)\theta-\lambda_j\theta\big]
\]

then proves local uniform convergence. Eventually (A_j\ge a_EI/2), so no error-to-ridge ratio is needed. This explains why any positive deterministic ridge tending to zero suffices in this particular finite-dimensional local regression. It does not justify an analogous assertion for an arbitrary ill-posed inverse problem.

The matrix projection is nonexpansive in Frobenius norm and fixes the true tensor. A countable compact exhaustion gives pointwise interior convergence on the same event; the projection supplies a uniform bounded majorant. Finite volume and dominated convergence yield global (L^2) convergence **of the clipped tensor**. There is no claimed global uniform limit, global divergence limit, or derivative consistency for the estimated tensor. The dyadic-prefix convention extends the limits to all sample sizes.

### 4. Singular features, basis invariance, and measurability

The finite-feature formulas use (G=V^*V\ge0), (H_n=G^{1/2}C_nG^{1/2}), and the identity

\[
V^*a(VC_nV^*)V=G^{1/2}a(H_n)G^{1/2}.
\]

For polynomials this follows by multiplication, including the constant term; uniform approximation extends it to continuous (a). No inverse or pseudoinverse of (G) is needed. Thus singular feature Gram matrices are admissible. All data integrals are Borel, matrix square roots and continuous matrix functions are continuous, and the positive ridge makes inversion continuous. Joint measurability plus continuity in (x), separability on compacts, and the bounded projected output give the stated random-element measurability.

The fresh Gram control uses a rational Householder change of basis, six features of rank five, and spectrum (1/4,1/4,-1/8,0,2). Rational polynomial interpolation computes (g) and (h/\log2) exactly. Direct eigenmode sums, the operator normal equations, and the singular Gram formulas agree. Rotating the repeated eigenspace by a rational orthogonal (3/5,4/5) matrix leaves the fit unchanged. The actual adjacent-edge (C_n) is also tested against the Gram identity for polynomial degrees zero through seven. These are nontrivial finite checks of the proposed mechanism, not a substitute for its continuous-functional-calculus proof.

## Primary-source interfaces

Fresh direct primary bytes, URLs, sizes and hashes are recorded in `reference_receipts.json`; downloaded PDFs and extraction/render caches are ignored locally. No browser UI or external communication was used.

| Source and location | Checked interface and scope |
|---|---|
| [Grubb, *Regularity of spectral fractional Dirichlet and Neumann problems*](https://web.math.ku.dk/~grubb/MN16.pdf), §2, Theorem 2.2 and Corollary 2.3, printed 832–834 | The setup explicitly allows a smooth strongly elliptic second-order operator and a suitable first-order Neumann-type boundary operator. The all-positive-power domain description and homeomorphism give the graph estimate used here. The shift (I-L), weighted norm equivalence, and strong ellipticity of the conormal problem meet this scope. Boundary conditions on iterated powers are respected; the proof does not pretend that every smooth function lies in all power domains. |
| [Grubb, *Distributions and Operators*, chapter 6](https://web.math.ku.dk/~grubb/dist6.pdf), Corollary 6.12 | On a bounded smooth domain, integer Sobolev order exceeding derivative order plus (d/2) controls those derivatives uniformly. This supplies (H^{2a}\to C^2) and the fixed-(r) eigenfunction bounds. |
| [Hansen–Scheinkman, NBER working paper 141](https://www.nber.org/system/files/working_papers/t0141/t0141.pdf), Proposition 5.5, printed 26/PDF page 28 | The actual scan was visually inspected. Self-adjoint generators with the same positive-lag conditional-expectation operator coincide. This is reversible fixed-lag identification, not continuity of the unbounded log, nor identification of nonreversible generators. The paper's use is correct. |
| [Reiß et al., OWR24/2017](https://content.ems.press/assets/public/full-texts/serials/owr/14/2/15432/online/10.4171-owr-2017-24.pdf), full contribution printed 1507–1509 | The multidimensional question concerns stationary bounded-domain divergence-form diffusion and estimating a matrix coefficient from empirical eigenpairs and invariant density, with retained count unspecified. The current paper selects an explicit smooth conormal model and an all-positive-mode weighted estimator. This is a convergence result in that explicit model; it does not resolve every possible interpretation or extension of the open question. “Noisy” empirical eigenpairs in the original report are not an extra sensor-noise model. |
| [Alberti–Barnes–Jambhale–Nickl, arXiv:2410.19393v2](https://arxiv.org/pdf/2410.19393v2), Lemma 3.8 and proof | The source proves scalar gradient excitation using cutoff functions, spectral truncation and Sobolev control. It is a genuine predecessor acknowledged by the manuscript, but does not by itself assert full anisotropic gradient/Hessian jet spanning. The latter is proved separately in the current paper. |
| [Lenzen–Scherzer, ECCOMAS2004](https://franklenzen.de/pdf/lenzen_scherzer_eccomas2004.pdf), §3, Theorem 3.2 | Classical nonlinear Tikhonov consistency requires forward-map hypotheses and a data-error/regularization balance. The supplementary alternative argument explicitly establishes a diffusion forward map and a suitable balance rather than using this abstract theorem as a black box for the spectral estimator. |

These checks establish the theorem interfaces actually needed. They do not constitute a new exhaustive audit of every historical citation, every original proof underlying standard elliptic theory, or every edition of prior estimation papers. In particular, this review does not remove the manuscript's stated uncertainty about the publisher-final 2011 Crommelin–Vanden-Eijnden text.

## Supplementary classical-regularization route

The two mathematical derivations describe a different estimator-existence mechanism. On a known admissible subset of a sufficiently high product (H^s) space, bounded weakly convergent sequences are compact in (C^2). The fixed-lag joint-density forward map is continuous along these sequences: conjugate weighted forms to a common ordinary (L^2) space, obtain norm-resolvent convergence, pass to the positive-time semigroup by continuous functional calculus, and upgrade operator convergence to Hilbert–Schmidt convergence using the uniform Neumann eigenvalue tail. Operator norm convergence alone would not suffice for the last step; the derivations explicitly supply the tail argument.

The forward map is injective by marginal recovery, self-adjoint logarithm, and cutoff jets. The supplementary zero-extension density estimate has a boundary-layer (L^2) bias controlled by finite perimeter and bandwidth (h_j\asymp(j+1)^{-4}); the dependent variance is exponentially dominated along the dyadic prefixes. The stated balance (\alpha_j=(j+1)^{-1}), approximate-minimization tolerance (\varepsilon_j=(j+1)^{-2}), and error (\delta_j=O((j+1)^{-1})) gives both (\delta_j^2/\alpha_j\to0) and (\varepsilon_j/\alpha_j\to0).

A countable dense admissible subset gives a measurable approximate minimizer; comparison with the fixed smooth truth bounds the Sobolev norm, forces the residual to zero, and compactness plus injectivity identifies every limit. No known bound on the true Sobolev norm is required. I found no mathematical defect in this supplied alternative derivation. It is not the same estimator as the paper's spectral fit and is not evidence of historical priority for either one.

## Computational evidence and limits

`replay/REPLAY_RECEIPT.json` records a fresh run of the unchanged published package, with Python 3.14.6 and the required SymPy 1.14.0 in an isolated ignored runtime. The runner verified its payload manifest, then all eight suites completed with exit code zero and empty stderr. Selected nonfloating scientific fields matched exactly; published floating diagnostic comparisons used relative tolerance (10^{-12}) and absolute tolerance (10^{-14}). The suite labels are retained as source labels, not endorsements of their historical provenance.

`independent_controls.py` and `independent_control_results.json` record **1,672 passing exact assertions in 26 families**. The count includes scalar entries of matrix identities; it is a coverage record, not a measure of proof strength. The main fresh tests are singular/repeated-spectrum Gram identities, tensor jets in dimensions 2–5, signed extension moments, four-state nonuniform reversible pair covariances and complete short-path enumeration, and deliberate outside-model/log-instability controls. No failed assertion was repaired into the paper; the fresh script passed on its first execution.

Neither set of controls is a simulation of the full estimator on a general smooth domain. Neither proves an infinite-dimensional PDE/statistical theorem or supplies quadrature/eigensolver error estimates. The analytic proof, with the checked elliptic interfaces, is the evidence for the asymptotic claim.

## Strongest supported result and exact remaining limits

**Strongest supported result:** the specified fourth-power-weighted empirical spectral fit is almost surely consistent for a fixed smooth reversible diffusion in the exact known-domain, known-bound, stationary fixed-lag, conormal-reflection model: local uniform tensor and separately fitted divergence recovery; global (L^2) recovery after ellipticity clipping; global (C^2) invariant-density recovery; local covariance and drift recovery; and measurability without eigenbasis selection. Any positive deterministic ridge tending to zero is allowed. All sample sizes are covered by the dyadic-prefix convention.

**Exact remaining mathematical gap for that stated theorem:** none identified by this review. This is a supported review conclusion, not a proof-assistant guarantee. The exact boundaries still matter: no rate, class-uniform conditioning, fixed prescribed retained-mode count, unknown-bound model, nonstationary start, sensor error, rough coefficients/domain, nonreversible extension, ordinary-normal anisotropic substitution, unprojected global tensor consistency, global divergence consistency, or derivative convergence of the estimated tensor is established here. Numerical implementation and exhaustive novelty/priority certification remain outside the result.

No website, spreadsheet, Git, Zenodo, or external outreach changes were made. Source bytes were only read. The review folder retains proof notes, executable controls, receipts, results and hashes; private runtime and reference caches are ignored.
