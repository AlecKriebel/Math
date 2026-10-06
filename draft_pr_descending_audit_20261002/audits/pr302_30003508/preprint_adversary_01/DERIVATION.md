# Independent reconstruction of the first candidate

This is the analytic record of the first fresh whole-package reviewer. The target is the theorem in the frozen `preprint_package_v01/spectral_tensor_consistency.tex`, not an unrestricted claim that every multidimensional diffusion can be estimated, and not a deduction from successful finite controls. The reconstruction below was made before consulting the earlier acceptance verdicts. Symbols use the candidate's conventions.

## 1. Exact statistical and mathematical target

The original three-page Reiss contribution, printed 1507–1509 in OWR24/2017, starts with general SDEs, reviews scalar inference, and finally specifies a stationary bounded-domain divergence-form model. Its final question asks for convergence of reconstruction of the matrix S from empirical eigenpairs and invariant density, with retained K to be determined. The word “noisy” there qualifies empirical spectral estimates; it does not supply a sensor-noise observation law. The source's final scalar-to-matrix passage states covariance Σ=2S/μ and drift β=(div S)/μ. It does not fix one multidimensional estimator or a convergence rate. Its report year is 2017, and the official publication date is 28 April 2018.

The candidate chooses a known bounded connected C∞ domain D⊂R^d, d≥2, known Δ>0, unknown smooth symmetric S and smooth μ on D-bar, with known 0<ell I≤S≤Lambda I and 0<c≤μ≤C, ∫μ=1. Its operator is L=μ^{-1}div(S grad), with the natural conormal boundary condition n·S grad u=0. Exact stationary positions Y_i=X_{iΔ} are observed. These explicit assumptions are sufficient to prove a scoped answer to the final question. They are stronger than the unspecified “sufficiently regular” opening model; the abstract correctly calls this an answer in the explicit smooth model. Ordinary normal reflection, a rough domain, nonreversibility, sensor noise and rates are outside the deduction.

At N≥2, j=floor(log2 N), n=2^j, h=h0/(j+1). The first n+1 states supply a density smoother and a symmetrized pair smoother. The chosen spectral fit retains every strictly positive empirical eigenvalue; its finite number is determined by the data feature rank, at most n+1. Thus it does specify the retained count rather than assuming a fixed K already excites all jets.

## 2. Known-domain smoothing and its precise boundary role

In a flattened boundary chart, extending a cutoff piece through the boundary by Σ_{a=1}^7 α_a f(x',-at), with α=(28,-112,210,-224,140,-48,7), matches normal derivatives through order six because Σα_a(-a)^k=1 for k=0,...,6. The finite Vandermonde identities are checkable algebra; the argument needs the corresponding extension operator, not merely those numbers. A small enough collar keeps every reflected point in its chart, and an exterior cutoff preserves the matched boundary jets. Interior pieces extend by zero after their supported cutoff. Finite partitions and smooth chart changes give a bounded extension in each C^r norm r≤6, equal to f on D. Convolution with an ordinary compact smooth mollifier therefore converges in C^2 for C^3 input.

After changing each reflected integral back to the interior variable z, bounded chart Jacobians and finite supports give a real Borel kernel K_h(x,z). Every x derivative can be placed on the mollifier, so |∂_x^α K_h|≤A_r h^{-d-|α|} for each fixed r, despite the finite order of the extension. Separately extending each variable gives the asserted mixed C^{2,2} convergence: mixed derivatives through those orders are controlled by the available six matching orders in each variable. The x neighborhood is fixed. For small net distances, the entire line segment lies in that neighborhood even if D is not convex.

The kernel is signed. It need not integrate to one for a point mass, preserve positivity, or make the joint estimate a transition kernel. None of those properties is used below. The raw density converges uniformly, so a smooth saturation equal to the identity on [3c/4,3C/2] is eventually inactive. For every interior-valued sample, saturation and normalization give c/(4C vol D)≤μ_j≤4C/(c vol D). Its C^2 convergence follows from the raw C^2 convergence and Z_j→1.

One minor formal clarification remains in the first candidate: Lemma 1 defines K_h for z∈D whereas a reflected process has state space D-bar. At each deterministic observation time, stationarity gives the absolutely continuous law μ dx, so P(Y_i∈∂D)=0. A countable union shows that all observations lie in D on one event of probability one. Consequently this omission does not defeat the almost-sure theorem. Assigning K_h(x,z)=0 for z∈∂D makes the statistics explicit Borel functions on the entire sample space and justifies the text's “every sample” wording without relying on completion. This is a definition on a null set, not a further model assumption.

## 3. Dependent consecutive pairs, including lag one

The energy form of -L in L^2(μ dx) is ∫grad f^T S grad f. For a μ-centered f,

    ||f||_μ² = min_a ∫(f-a)² μ
              ≤ C min_a ∫(f-a)²
              ≤ C C_D ∫|grad f|²
              ≤ C C_D/ell · energy(f,f).

Connectedness supplies the Neumann Poincaré constant C_D. Therefore the fixed-lag semigroup P contracts the mean-zero subspace by rho≤exp[-Δ ell/(C C_D)]<1. The estimator does not use rho or an unknown smoothness bound.

For a real bounded pair observable F(Y_i,Y_{i+1}), center it to Z_i, and put r(z)=E[Z_0|Y_1=z], s(z)=E[Z_0|Y_0=z]. Both are centered and have norm at most sqrt(Var F). The Markov property gives, for a≥1,

    Cov(Z_0,Z_a) = <r,P^{a-1}s>_μ,
    |Cov| ≤ rho^{a-1} Var F.

At a=1 the two pairs share exactly one endpoint; P^0 appears, so no independence of adjacent pairs is inserted. Summing the diagonal and both covariance triangles gives

    Var(n^{-1}Σ F(Y_i,Y_{i+1}))
       ≤ [1+2/(1-rho)] ||F||_∞²/n.

The state analogue uses P^a. This bound applies anew to each bandwidth-dependent differentiated summand. It does not require independent dyadic prefixes. As a falsification of a tempting stronger statement, the stationary two-state chain with eigenvalue rho and F(a,b)=a+b has Var F=2(1+rho) and Cov_a=(1+rho)^2 rho^{a-1}; a generic rho^a Var F bound fails already at lag one. The actual candidate uses the correct exponent.

## 4. Population graph regularity and empirical C^{2,2} convergence

The smooth uniformly elliptic conormal realization has compact resolvent. Comparison of Rayleigh quotients by the pointwise bounds and min-max compares eigenvalues gamma_k of -L with those of the Neumann Laplacian. Bounded smooth domains have polynomial eigenvalue counting. The cited smooth Neumann graph-domain theorem supplies, after a positive shift, ||f||_{H^{2a}}≤B_a||(I-L)^a f||_{L²(μ)} on its power domain. Sobolev embedding then bounds each eigenfunction's fixed C^r norm by a polynomial in 1+gamma_k. Weighted and unweighted L² norms are equivalent.

Since Δ>0 is fixed, the exponential factor beats every such polynomial. The population expansion

    q(x,y)=μ(x)μ(y)Σ_k exp(-Δ gamma_k)u_k(x)u_k(y)

converges absolutely and uniformly after every fixed derivative on D-bar×D-bar. This proves population smoothness including the boundary. It uses neither estimated eigenvector regularity nor a uniform bound over all possible truths. The zero eigenvalue of -L contributes the constant mode and causes no difficulty with I-L.

For pair derivatives with |α|,|β|≤2, the individual smoothed summand is at most B(j+1)^{2d+4}. Section 3 gives its average variance at a fixed (x,y) at most B(j+1)^{4d+8}2^{-j}. A net in the 2d-dimensional compact product at spacing ε_j=2^{-j/(4d)} has cardinality at most B2^{j/2}. Chebyshev at threshold (j+1)^{-1}, followed by a union bound, gives

    P(max_net |∂_x^α ∂_y^β(q_j-Eq_j)|>(j+1)^{-1})
       ≤ B(j+1)^{4d+10}2^{-j/2}.

This is summable in j. One further derivative bounds the interpolation error by B(j+1)^{2d+5}ε_j→0. Finitely many derivative indices and Borel–Cantelli give uniform centered convergence. Symmetry and stationarity yield Eq_j=(R_h⊗R_h)q, whose bias converges in the same mixed norm. The state estimate uses a d-dimensional net of cardinality B2^{j/4}, giving probability B(j+1)^{2d+6}2^{-3j/4}, again summable. Thus μ_j→μ in C²(D-bar) and q_j→q in C^{2,2}(D-bar×D-bar) on one event of probability one. Every later compact E uses that same event; no intersection over uncountably many probability-one statements occurs.

## 5. The spectral fit survives all spectral collisions

On H=L²(dx), let T_j have kernel q_j/√(μ_j μ_j), and T the analogous population kernel. T_j is self-adjoint and finite rank because the symmetrized adjacent-pair matrix uses n+1 kernel sections. Its positive eigenvalues need not be ≤1, its top mode need not equal one, and its negative and zero spectrum are allowed. Nonzero eigenfunctions are smooth because they are in the feature span. The density and pair convergence imply T_j→T in Hilbert–Schmidt and operator norm. For W_j=μ_j^{-1/2}T_j, derivatives of the kernel in its first variable and Cauchy–Schwarz imply W_j→W as H→C²(E), for each interior compact E.

Set B_j(x)=J eval_x W_j and e_j(x)=eval_x W_j. Define

    g(t)=t² for t>0, else 0;
    h(t)=t² log t for t>0, else 0.

Both are continuous on the real line, including zero. For an empirical positive mode, W_j φ_{j,k}=kappa_{j,k}u_{j,k}. Therefore two outer powers and two middle powers give exactly the normal matrix and right-hand side for the kappa^4-weighted objective:

    A_j=B_j g(T_j) B_j*,
    r_j=μ_j/Δ · B_j h(T_j) e_j*,
    θhat_j=(A_j+lambda_j I)^{-1}r_j.

The logarithm is evaluated only at positive empirical modes. The continuous function h, rather than the discontinuous naked logarithm, governs convergence. Uniform operator bounds put all spectra in one compact interval. Uniform polynomial approximation of g and h there, and telescoping polynomial powers, prove g(T_j)→g(T) and h(T_j)→h(T). Combining with the outer H→C² convergence gives uniform convergence of A_j and r_j on E. This is invariant under multiplicities and eigenbasis changes, and handles positive modes crossing zero, spurious negative modes, lost rank, and empirical eigenvalues above one. No convergence of an individually labeled eigenvector or differentiability of a noisy logarithm is assumed.

## 6. Full-jet excitation is proved, not an unverified identifiability condition

The vector J uses diagonal Hessians, twice the off-diagonal Hessians, and gradients. Its dimension is m=d(d+1)/2+d, and θ stacks symmetric S entries and div S. Symmetry ensures J(u)^T θ=div(S grad u), with the factor two correct. The population PDE gives r=Aθ. The matrix A is the absolutely convergent nonnegative sum Σ kappa_k^4 Ju_k Ju_k^T.

Suppose ξ^T A(x)ξ=0 at an interior point. All kappa_k are strictly positive, so ξ^T Ju_k(x)=0 for every k. If f∈C_c∞(D), each application of the local differential operator preserves support away from the boundary. Such f belongs to every power domain and satisfies every iterated conormal condition. Spectral partial sums converge in all graph norms; choose 2a>d/2+2 to obtain C² convergence. Therefore ξ annihilates Jf(x) for every compactly supported smooth f. A cutoff equal to one near x times affine and quadratic polynomials prescribes gradient and symmetric Hessian independently. These jets span R^m, forcing ξ=0. The constant eigenfunction has zero jet, but the full remaining spectrum still spans.

Continuity of the evaluation operators gives continuity of A. Compactness of E gives min_{x∈E}lambda_min A(x)=a_E>0. This is a truth-dependent local lower bound. It is not a uniform estimate at the conormal boundary or across all smooth parameters. Finite controls of some mode families are illustrations; the power-domain/cutoff argument is the proof of the general assertion.

## 7. Ridge, clipping and the strongest proved topology

Eventually A_j≥a_E I/2. The exact error identity is

    θhat_j-θ=(A_j+lambda_j I)^{-1}
       [(r_j-r)+(A-A_j)θ-lambda_j θ].

Each bracket term tends uniformly to zero, and the inverse stays bounded. Any deterministic positive lambda_j→0 is sufficient. A noise-to-ridge rate is unnecessary because the limiting matrix is already locally positive definite. The tensor part and separately fitted vhat_j converge locally uniformly to S and div S. Nothing permits replacing vhat_j by div Shat_j: no convergence of estimator derivatives has been proved.

Pointwise Frobenius projection onto the known closed convex matrix interval is nonexpansive, fixes the true S, and bounds the projected output by a fixed finite constant. Interior convergence on a countable compact exhaustion plus dominated convergence gives the global L² tensor limit, since D has finite volume and its boundary has Lebesgue measure zero. There is no corresponding global divergence or boundary-uniform conclusion. Density convergence and positivity give covariance 2Shat_j/μ_j and drift vhat_j/μ_j locally uniformly. Reusing the dyadic prefix gives the same event and convergence for all N→∞.

## 8. Eigenvector-free measurable statistics, including singular feature Gram matrices

Let f_i=K_h(·,Y_i)/√μ_j, v_i=K_h(·,Y_i)/μ_j, V have columns f_i, and C_n be the adjacent symmetric matrix with entries 1/(2n). Then T_j=VC_nV*, G=V*V≥0, H_n=G^{1/2}C_nG^{1/2}. With D_x having columns Jv_i(x), B_j=D_x C_n V* and e_j=v(x)^T C_n V*. For polynomials a, including a constant term,

    V* a(VC_nV*) V = G^{1/2} a(H_n) G^{1/2}.

The identity extends to continuous a by uniform approximation. It uses no inverse of G, so duplicate positions and singular features are allowed. Applying g and h yields exactly the finite formulas printed in the manuscript. Kernels, their derivatives, positive saturation, and integrals over a fixed known domain are Borel in the positions. Finite positive square roots and continuous functional calculus are continuous, and ridge makes the final inverse nonsingular. The outputs are continuous in x. Separability then gives C(E)-valued measurability; bounded projected output gives L²(D)-valued measurability. With the harmless boundary convention in Section 2, this is a fully explicit statistic on all D-bar samples. No measurable choice of empirical eigenbases is required.

## 9. Independent reconstruction of the classical alternative

This supplement solves a different objective; it cannot substitute for Sections 2–8. Fix s>d/2+2, let X be the Hilbert product of H^s components, and E its closed convex pointwise admissible subset with normalized density. Smooth truth has finite unknown X norm M. E is nonempty, separable, norm-closed and weakly closed. Bounded H^s sequences are compact in C² and C¹. The conventional Hölder exponent should be explicitly chosen as 0<eta<min(1,s-d/2-2); the first candidate omits the min(1,·). There always is such an exponent under its strict s assumption, so this precision cleanup changes no compactness conclusion.

For each candidate, use the weighted H¹ energy form to define the conormal self-adjoint generator. Conjugation by √μ puts it on L²(dx) with common form domain H¹ and form a(v,w)=∫grad(v/√μ)^T S grad(w/√μ). On any bounded X sequence converging in C¹, the form coefficients converge uniformly and the shifted forms are uniformly H¹-coercive. The identity for grad v in terms of grad(v/√μ) and v, with uniform C¹ density bounds, proves the latter. Lax–Milgram on the common form domain gives norm resolvent convergence, handling moving conormal operator domains explicitly.

If R_n=(I+A_n)^{-1}, then exp(-ΔA_n)=f(R_n), where f(0)=0 and f(r)=exp(Δ-Δ/r). Continuous functional calculus gives operator norm semigroup convergence. This alone would not imply density convergence. Min-max supplies singular-value bounds s_k(T_n)≤beta_k=exp[-Δ(ell/C)nu_k] from Neumann Laplacian eigenvalues. Polynomial counting gives Σbeta_k²<∞ uniformly. The approximation-number inequality s_{2m-1}(T_n-T)≤s_m(T_n)+s_m(T)≤2beta_m, and monotonicity, give

    ||T_n-T||_HS² ≤ 2M0 ||T_n-T||_op² + 8Σ_{m>M0} beta_m².

Tail control followed by the norm limit proves Hilbert–Schmidt convergence. Multiplication by √μ_n then yields L² convergence of joint kernels F(θ_n). A diagonal operator with n entries n^{-1/2} has norm→0 but HS norm one; that invalid shortcut is avoided by the actual trace tail.

Equal joint kernels have equal marginals μ, hence equal fixed-lag self-adjoint semigroups on one weighted space. The exponential is strictly positive at each finite generator spectral value; zero is only an accumulation spectral point with zero spectral projection. The unbounded Borel logarithm reconstructs both generator and its domain. Compactly supported smooth tests are in its domain for all H^s candidates. A cutoff quadratic jet at x, with zero gradient, recovers S(x):H/μ(x), and affine jets recover div S. Thus the forward map is injective on the entire class, including parameters that touch the allowed bounds.

For statistical input, ordinary ambient KDE of the zero-extended joint truth is sufficient in L², even though it is boundary biased uniformly. Put Omega=D×D. A bounded C¹ extension of q and the finite-perimeter bound |Omega triangle (Omega+v)|≤B|v| give ||q1_Omega(·-v)-q1_Omega||²_2≤B(|v|²+|v|). Convolution bias is therefore O(√h). With h=(j+1)^{-4}, bias is O((j+1)^{-2}). The pair covariance bound above gives E||qhat-Eqhat||²_2≤B h^{-4d}2^{-j}. Markov at squared threshold (j+1)^{-2} is summable, so δ_j=||qhat-F(θ0)||_2=O((j+1)^{-1}) almost surely. Product D×D need not have a smooth cornered boundary for the finite-perimeter argument.

Take a fixed countable dense feasible set, for example the metric projections into E of a dense X sequence. Select the first index with objective ≤its countable infimum+epsilon_j. Continuity and countability prove measurability; tight pointwise constraints do not require feasible rational coefficient fields. With alpha_j=(j+1)^{-1}, epsilon_j=(j+1)^{-2}, comparison against truth gives

    residual²+alpha_j||θhat_j||²_X
       ≤δ_j²+alpha_j M²+epsilon_j.

Both δ_j²/alpha_j and epsilon_j/alpha_j tend to zero. The estimator has a bounded X tail and residual→0. Every subsequence has a weak-X/strong-C¹ further subsequence; forward continuity and injectivity force its limit to truth. Thus the whole sequence converges in C¹(D-bar), recovering μ, S and actual div S uniformly, and S in global L². This estimator requires neither a known M nor computational access to an exact minimizer. Its mathematical existence and stronger convergence topology do not establish efficiency or the spectral fit's consistency.

## 10. Stronger statements tested and rejected

No part of this reconstruction proves finite-mode jet excitation on every domain, uniform conditioning at the boundary, a class-uniform rate, stable naked empirical logarithms, generator identification without self-adjointness, positive empirical kernels, empirical eigenvector convergence, derivative convergence of Shat, or consistency under ordinary normal rather than conormal reflection. The existing exact/floating controls test specific falsifications of these shortcuts; they are not proofs of the infinite-dimensional result. The scoped analytic chain above supplies the actual theorem. No material missing mathematical link was found in that chain or in the separate classical chain. The four low-severity presentation/definition clarifications are recorded in the verdict and report.
