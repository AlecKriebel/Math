# An alternative consistent estimator from classical regularization

2026-10-05 UTC. Supplementary derivation of an alternative forward-kernel regularization estimator in the same smooth model. The proof was newly supplied during the present audit and independently reconstructed below; it is not a located earlier publication of this application. It does not establish convergence of the spectral-equation objective in the main note.

## Precise alternative conclusion

In exactly the submitted smooth reversible bounded-domain model, with only the stated known ellipticity/density bounds, an ordinary joint-density estimator followed by a Sobolev-penalized nonlinear inverse fit gives an almost-sure consistent estimator of S and mu in C1, hence of div S in C0. No derivative-norm bound on the truth is known to the estimator. This is a different estimator: it minimizes a mismatch with the forward stationary joint heat kernel, and may require a global infinite-dimensional minimization. It does not establish convergence of the PR's finite-rank empirical spectral-equation construction. Computational efficiency is not claimed.

The abstract ingredients substantially predate the PR. Hansen–Scheinkman, NBER technical working paper141 (1993), Proposition5.5/printed p26, proves reversible generator identification from one positive-time transition operator. Lenzen–Scherzer's author-hosted ECCOMAS2004 paper §3/Theorem3.2 states nonlinear Hilbert-space Tikhonov convergence for weakly closed continuous forward maps, with noise squared divided by the regularization parameter tending to zero; it credits Engl–Kunisch–Neubauer(1989), Seidman–Vogel(1989), and Engl–Hanke–Neubauer(1996). Bruce E. Hansen, "Uniform convergence rates for kernel estimation with dependent data," Econometric Theory24(2008),726–748, DOI10.1017/S0266466608080304 ([author-hosted published paper](https://users.ssc.wisc.edu/~behansen/papers/et_08.pdf)), Theorem3, proves strong uniform convergence of centered kernel density averages under stationary mixing conditions, including overlapping lag vectors. These are real earlier frameworks, not a prior paper explicitly claiming this particular tensor-diffusion application. The following proof checks the application rather than silently equating identification with consistency.

## Parameter space and topology

Let s be a fixed integer satisfying s>d/2+2, for example s=d+3. Let X be the Hilbert product of Hs(D) for the d(d+1)/2 independent entries of S and the density mu. The admissible subset E consists of symmetric S with ell I<=S<=Lambda I, densities c<=mu<=C, and integral_D mu=1. Include all Hs coefficients satisfying these constraints. Smooth truth belongs to E and has finite, unknown Hs norm.

E is weakly sequentially closed. A weakly convergent Hs sequence is bounded, and compact Sobolev embedding on a smooth bounded domain gives subsequences converging in C2 (the strict inequality on s is intentional). The pointwise constraints and normalization pass to the limit. A fixed Hs ball intersected with E is compact in C1, and in fact C2. The penalty controls this ball without assuming its radius is known beforehand.

For theta=(S,mu), let F(theta)=q_theta be the stationary joint Lebesgue density at the known lag Delta. This is the kernel of M_sqrt(mu) T_theta M_sqrt(mu), where T_theta is the generator semigroup conjugated to L2(D,dx). Hs coefficients have the regularity required for the uniformly elliptic reflecting realization; the weak form is sufficient for the continuity argument. The data space is Y=L2(D×D).

## Continuity despite moving conormal operator domains

Suppose theta_n is bounded in Hs and converges in C1 to theta in E. On a *common form domain* H1(D), the nonnegative conjugated generator A_theta=-sqrt(mu) L_theta /sqrt(mu) has form

    a_theta(v,w)=integral_D [grad(v/sqrt(mu))]^T S grad(w/sqrt(mu)) dx.

The conormal boundary condition is natural in this form; its operator domain need not be held fixed. Positivity and C1 convergence of mu, and C0 convergence of S, imply

    |a_n(v,w)-a(v,w)| <= epsilon_n ||v||_H1 ||w||_H1, epsilon_n→0.

The norms associated to a_n(v,v)+||v||_2² are uniformly equivalent to the H1 norm on this sequence. To see the lower bound, grad v=sqrt(mu) grad(v/sqrt(mu)) + v grad(sqrt(mu))/sqrt(mu); the second term is controlled by a uniform C1 density bound. Ellipticity controls the first term. The upper bound follows from the reverse formula. Lax–Milgram applied to a_n+I therefore gives

    R_n=(I+A_n)^(-1)→R=(I+A)^(-1) in L2 operator norm.

There is no unsupported assertion about a logarithm of a noisy operator. For fixed Delta>0, put f(z)=exp(Delta-Delta/z) on z>0, f(0)=0. This is continuous on [0,1], and T_n=exp(-Delta A_n)=f(R_n). Uniform polynomial approximation gives T_n→T in operator norm.

This convergence strengthens to Hilbert–Schmidt convergence. In the original weighted space, the Rayleigh quotient is integral grad(u)^T S grad(u) divided by integral mu u². Min–max yields lambda_k(A_n)>= (ell/C) lambda_k(Neumann Laplacian on D). Multiplication by sqrt(mu) is the relevant unitary identification of the weighted spaces and does not change eigenvalues. Thus the ordered singular values of T_n satisfy

    s_k(T_n)<=exp[-Delta(ell/C) lambda_k(Neumann Laplacian)],

uniformly in n, with a square-summable tail. Compactness and the usual Neumann eigenvalue growth suffice. The singular-value inequality

    s_(2m-1)(T_n-T)<=s_m(T_n)+s_m(T)

controls the tail of T_n-T uniformly, while each finite initial block is bounded by its operator norm. First make the common tail small, then let n→infinity for the finite block. Hence ||T_n-T||_HS→0. Uniform convergence of the density multipliers now gives F(theta_n)→F(theta) in L2(D×D). The same reasoning establishes weak sequential continuity on bounded Hs sequences by compact embedding and uniqueness of the limit, which is stronger than the weak closedness needed by the classical theorem.

## Identification on the whole admissible parameter space

If F(theta_1)=F(theta_2) as joint densities, their marginals give mu_1=mu_2. Dividing by that common density identifies the same transition operator P_Delta on the same L2(mu dx). Its generator is self-adjoint and nonpositive. Injectivity of t↦exp(Delta t) on the real line, including the unbounded spectral calculus, implies equality of the self-adjoint generators (the Hansen–Scheinkman mechanism).

Interior smooth cutoff affine and quadratic functions lie in both operator domains, including for Hs coefficients. Comparing their images recovers the first-order coefficients and the symmetric principal second-order coefficients at every interior point. Consequently S_1=S_2 and div S_1=div S_2 there. Continuity extends equality to the closure. This is coefficient identification, with no finite eigenpair rank assumption. Thus F is injective on E. It is not an assertion that the full inverse is continuous on the unbounded union E.

## A data estimator which requires no boundary correction

Let Z_i=(Y_i,Y_(i+1))∈D×D, with Y_i=X_(i Delta). Take a smooth compactly supported probability kernel K on R^(2d), and extend the true q by zero outside D×D. At n_j=2^j, choose h_j=(j+1)^(-4) times a known fixed positive scale and set

    qhat_j(z)=n_j^(-1) sum_(i=0)^(n_j-1) h_j^(-2d) K((z-Z_i)/h_j), z∈D×D.

One may symmetrize qhat_j without worsening L2 error. Positivity, an exact marginal, derivatives and finite rank are unnecessary for the alternative estimator.

The true chain has a spectral gap rho<1 on mean-zero L2(mu). For any bounded F(Z_i), conditioning on the shared chain endpoints gives

    |Cov(F(Z_0),F(Z_l))|<=rho^(l-1) Var(F(Z_0)), l>=1.

Therefore Var(n^(-1) sum F(Z_i))<=C_rho ||F||_infinity²/n. Applied to the kernel at z and integrated over the bounded product domain, it gives

    E ||qhat_j-E qhat_j||_L2² <= C h_j^(-4d) 2^(-j).

Markov's inequality at threshold1/(j+1) gives summable probabilities C(j+1)^(16d+2)2^(-j). Borel–Cantelli implies ||qhat_j-E qhat_j||_L2<=1/(j+1) eventually almost surely. Constants may depend on the fixed truth, and need not be known by the estimator.

The expectation is ordinary convolution with the zero extension of q. On D×D, q is smooth and bounded. For translations of length a, away from a boundary layer of volume O(a), smoothness gives squared L2 error O(a²). The bounded jump across the boundary contributes O(a). The boundary of D×D has finite perimeter, so these estimates remain valid at its corners. It follows by Minkowski's inequality that the convolution bias in L2 is O(sqrt(h_j))=O((j+1)^(-2)). Hence, on one probability-one event,

    delta_j:=||qhat_j-q||_L2=O(1/(j+1)).

This elementary dependent-data proof is included to avoid a hidden historical-density hypothesis. Hansen(2008) provides a stronger published stochastic ingredient: the pair sequence is stationary, geometrically strong mixing, boundedly supported, has bounded marginal density and, for l>=2, bounded joint density of two pairs. Indeed that latter density is a product of stationary density and positive-time heat densities with intervening times at least Delta. The overlap at l=1 is explicitly allowed by his Assumption2's sufficiently-large-lag condition. His bounded smooth compact kernel hypotheses and any sufficiently slow bandwidth satisfy Theorem3; its centered strong uniform error is more than enough for the L2 argument. The zero-extension bias, rather than a false global smoothness assumption at the boundary, completes this application. This is not an attribution of the entire diffusion reduction to his paper.

## Tikhonov fit and actual measurability

Put alpha_j=1/(j+1), epsilon_j=1/(j+1)^2, and define

    J_j(theta)=||F(theta)-qhat_j||_L2² + alpha_j ||theta||_Hs².

Minimize over E up to objective error epsilon_j. A countable Hs-dense subset of E exists by separability. F is norm continuous, as is the penalty. The infimum over this subset equals the infimum over E. Choose the first member whose value is at most this countable infimum plus epsilon_j. This is a measurable estimator because all costs and their countable infimum are measurable. No measurable choice from an uncountable set is being assumed. Density in E suffices even if the truth touches a known ellipticity bound.

With theta_0 the fixed truth, the approximate minimizer thetahat_j satisfies

    ||F(thetahat_j)-qhat_j||² + alpha_j ||thetahat_j||_Hs²
      <= delta_j² + alpha_j ||theta_0||_Hs² + epsilon_j.

The ratios delta_j²/alpha_j and epsilon_j/alpha_j tend to zero. This proves boundedness in Hs and a residual tending to zero. Every subsequence has a further weak-Hs, strong-C1 convergent subsequence to an admissible theta_*. Forward continuity and the vanishing residual give F(theta_*)=F(theta_0). Identification forces theta_*=theta_0. Thus the entire sequence converges in C1. This gives S and mu uniformly, div S uniformly, and global L2 S; clipping is unnecessary for this bounded admissible estimator. It also implies the weaker local uniform/clipped L2 conclusions of the submitted theorem. The unknown Hs norm is learned through coercivity of the penalty, not specified as an input. The construction along dyadic sample sizes extends to all N by reuse of the latest dyadic prefix.

## Adversarial boundary checks and priority consequence

- Varying conormal boundary domains are handled through the common weak form, not an unjustified fixed operator domain.
- Unknown mu is jointly fitted and identified by the stationary joint marginal, not assumed known or replaced with a Lamperti transform.
- All smooth truths have finite Hs norm for the one predetermined s; no countable-class selection or unknown regularity-radius tuning remains.
- A fixed positive lag is retained; the only limit is observation count plus spatial smoothing.
- No oracle eigenpairs, a logarithm of empirical negative eigenvalues, derivatives of estimated eigenfunctions, prescribed finite spectral rank, sensor model, or numerical minimizer accuracy is used.
- The qhat boundary discontinuity is permitted in L2; global uniform bias of ordinary zero-extended kernels would be false and is not claimed.
- The argument uses exact evaluations of the forward model and a global approximate minimizer. It establishes measurable mathematical existence, with no finite arithmetic or tractability claim.

The reduction demonstrates that broad estimator existence follows from a classical regularization mechanism and elementary checked application links. This materially challenges treating mere existence as an intrinsically new mechanism. Because the particular diffusion application was newly checked here, the reduction alone is not evidence of a historically earlier publication and does not refute literal chronological first publication of that application. It supplies no historical `already_solved` blocker by itself. It also does not make the source's expressly specified eigenfunction-equation convergence problem already solved: it uses a different objective and transfers no consistency to that spectral fit. No inspected earlier primary paper was found proving the submitted construction or proving convergence of arbitrary noisy spectral equations without their derivative/rank/statistical hypotheses. The defensible contribution remains the particular empirical spectral reconstruction theorem, subject to the separate mathematical gate and bounded historical audit.

There is no worldwide firstness guarantee. A published earlier application of this regularization reduction would strengthen the broad-priority objection; a published convergence theorem for the empirical spectral-equation method could also defeat the narrow problem claim. Neither was located in this bounded search.
