# Independent reconstruction of the revised PR302 theorem

This reconstruction is about the explicit smooth model and estimator in the second candidate. I performed the derivation before opening the first-review verdict or ROOT acceptance. The candidate's own supplementary derivations were read as material under review, not as independent acceptance evidence. This is mathematical AI review, not human refereeing or formal certification.

## 1. Target and observation law

Reiss's complete contribution, printed1507–1509, goes from one-dimensional low-frequency inference to an unknown general positive definite matrix S on a bounded reflecting domain. Its last paragraph asks for convergence of reconstruction from empirical generator eigenpairs and invariant density, with K still to be selected. It does not prescribe a specific objective, a convergence rate, or an added measurement-noise model. The revised theorem selects a nonparametric smooth bounded connected domain and smooth unknown S and mu with known pointwise bounds. These are substantive explicit model assumptions; the claim is not all possible rough coefficient classes.

The interior operator is L=mu^-1 div(S grad), so the second-order coefficient is S/mu and the covariance convention is Sigma=2S/mu; drift is divS/mu. Symmetry and integration by parts give energy integral grad f^T S grad g and natural boundary n.S.grad f=0. Ordinary normal reflection with anisotropy would give a different operator model. Conormal reflection, unknown mu, general matrix S, and exact stationary positions at fixed positive Delta all match the stated source interpretation.

The weighted Poincare argument is valid despite different Lebesgue and mu means: min_a integral(f-a)^2 mu <= C min_a integral(f-a)^2 <= C C_D integral|grad f|^2. With ellipticity this gives an actual population gap ell/(C C_D) and a contraction rho<1. The estimator does not need its numerical value. Disconnected D would invalidate a one-dimensional stationary nullspace and the gap argument, but is explicitly excluded. Delta=0, unbounded D, degenerate S or vanishing mu are likewise outside the theorem.

## 2. Boundary smoothing and density safety

In each flattened chart the extension coefficients satisfy sum alpha_a(-a)^k=1 for k=0,...,6. This matches all normal derivatives through6; tangential derivatives commute with the finite reflection sum. Cutoff supports and a sufficiently thin known collar prevent exiting a chart. Interior cutoff pieces have a zero extension. The partition of unity gives E f=f on D. Exterior cutoffs preserve matching at t=0. This is a bounded linear extension on C^r for r<=6.

Convolution with eta_h is smooth in x even when an arbitrary high derivative of E f is unavailable. Rewriting the extension integrals in z in D gives a finite kernel with bounded Jacobian factors. Each x derivative acts on the mollifier and has sup bound A_r h^-d-r for every fixed r. C^3 extension gives C^2 bias convergence. Applying the extension in each variable supplies the mixed C^{2,2} convergence used below. The construction uses no unknown truth field. Its signs and possible failure of exact mass preservation do not enter any positivity assumption.

The explicit definition K_h(x,z)=0 for z on the boundary makes every sample-to-estimator map defined. Each stationary Y_i has the Lebesgue density mu, so the countable union of boundary-sample events has probability zero. This convention fixes a definition; it does not assume a new probabilistic hypothesis.

For every data tuple, psi takes values in [c/2,2C]. Consequently Z_j is between (c/2)volD and 2C volD, and mu_j is at least c/(4C volD). It is smooth in x and normalized. Once tilde-mu converges uniformly to mu, its values are eventually inside the identity interval [3c/4,3C/2]; normalization then converges to1 and C^2 convergence is preserved. Tight truth bounds c and C cause no problem because that identity interval strictly contains [c,C].

## 3. Derivative consistency with overlapping pairs

For centered Z_i=F(Y_i,Y_{i+1})-E F, set r(z)=E[Z_0|Y_1=z] and s(z)=E[Z_0|Y_0=z]. Conditional Jensen gives their L^2(mu) norms at most sqrt(Var F) and zero means. Conditioning from Y_1 to Y_a gives Cov(Z_0,Z_a)=<r,P^{a-1}s>, including a=1. Therefore |Cov|<=rho^{a-1} VarF. Summing the stationary covariance series yields variance of the average <=(1+2/(1-rho))||F||_infinity^2/n. A rho^a bound would mishandle overlap; independent pair observations are not needed and not assumed.

For a pair derivative with orders at most2 in each variable, the summand bound is A h^-(2d+4)=A(j+1)^(2d+4); its variance is at most A(j+1)^(4d+8)2^-j. A 2d-dimensional epsilon-net with epsilon=2^-j/(4d) has A2^(j/2) points. Chebyshev at threshold1/(j+1) supplies summable A(j+1)^(4d+10)2^-j/2. A further derivative supplies Lipschitz bound A(j+1)^(2d+5), whose product with epsilon tends to0. Straight interpolation segments are legal in the fixed neighborhood for all sufficiently fine nets, without convexity of D. Finite many derivative indices give one probability-one event. The state calculation has pointwise variance A(j+1)^(2d+4)2^-j, net size A2^(j/4), hence the claimed A(j+1)^(2d+6)2^-3j/4 probability bound. Deterministic extension bias then yields the full C^2 and C^{2,2} limits.

Population smoothness is not an empirical-eigenvector assumption. The smooth strongly elliptic conormal realization has compact resolvent. Uniform comparison to the Neumann Laplacian gives polynomial eigenvalue counting. Iterated elliptic estimates bound eigenfunction derivatives polynomially in the population eigenvalue. At a fixed strictly positive Delta the exponentially decaying semigroup factors dominate every such polynomial. Hence all fixed differentiated series for q converge absolutely uniformly on the closed product domain. This also justifies differentiation of the true kernel and its endpoint behavior.

## 4. Continuous operator reconstruction

On H=L^2(dx), T has kernel q/(sqrtmu_x sqrtmu_y), and phi_k=sqrtmu u_k has eigenvalue kappa_k=e^-Delta gamma_k>0. T_j is real self-adjoint finite rank, not necessarily positive. Uniform mu convergence and the common lower bound give T_j->T in Hilbert-Schmidt and operator norm. Differentiating the W_j=mu_j^-1/2 T_j kernel twice and using Cauchy-Schwarz in its second variable gives W_j->W as bounded maps H->C^2(E). Thus the bounded evaluation operators B_j=J W_j and e_j=W_j|_x converge uniformly on every interior compact E.

In the spectral basis, B_j phi= kappa Ju and e_j phi=kappa u. Multiplication by g(t)=t^2 for t>0 and0 otherwise supplies the remaining two powers in the quadratic normal matrix. The h(t)=t^2 logt extension by0 for t<=0 similarly supplies kappa^4 logkappa in the linear term. Therefore A_j=B_j g(T_j) B_j* and r_j=(mu_j/Delta)B_j h(T_j)e_j* are exactly the stated normal equations, including eigenvalues>1 and repeated eigenspaces. Negative modes never acquire a logarithm.

Both g and h are continuous on a common bounded spectral interval, especially at0. Uniform polynomial approximation and telescoping bounded operator powers imply norm continuity of g(T_j) and h(T_j), without any commutation or individual eigenvector convergence. This proves uniform A_j->A and r_j->r on E. A fixed number of empirical modes need not excite full jets; using every positive finite-rank mode is an essential part of the specified estimator, with rank at mostn+1.

## 5. Full excitation and ridge stability

The population series A=sum kappa^4 Ju Ju^T and r=sum kappa^4 nu mu u Ju converge by the smoothing/operator arguments. The population PDE gives r=A theta with theta comprising the independent symmetric S entries and div S. The coefficient2 on mixed Hessians accounts for both symmetric off-diagonal entries.

If xi^T A xi=0, nonnegativity and strictly positive weights imply xi.Ju_k(x)=0 for allk. Every interior compactly supported smooth f lies in all powers of I-L: repeated applications are local and retain compact support, so all iterated natural boundary conditions hold. Spectral partial sums converge in every graph norm. Choosing 2a>d/2+2 in the smooth elliptic estimate and Sobolev embedding gives convergence in C^2. Thus xi.Jf(x)=0 for every f in C_c^infinity(D). Cutoff affine and quadratic polynomials realize arbitrary gradient and symmetric Hessian atx, so xi=0. Continuous A and compactness give a_E>0, not a uniform over all truths or boundary points constant.

Eventually A_j>=a_E I/2 on E. The exact error equation is

    thetahat-theta=(A_j+lambda I)^-1[(r_j-r)+(A-A_j)theta-lambda theta].

The inverse is uniformly bounded on E and theta is bounded there. Any positive deterministic lambda_j->0 therefore suffices; no delta/lambda rate is needed. A heuristic inverse bounded by1/lambda would miss this crucial population excitation. The separately fitted divergence estimates div S, without claiming that differentiating the fitted tensor recovers it.

Projection onto ellI<=M<=LambdaI is nonexpansive in Frobenius norm and fixes S. Interior pointwise convergence on a countable compact exhaustion and a deterministic global bound imply global L^2 convergence by dominated convergence. A global unprojected tensor bound, global divergence error, or derivative error is not inferred. This handles deterioration of excitation near the boundary. All sample sizes use a dyadic prefix with j->infinity, so no omitted subsequence of observations remains.

## 6. Measurability without eigenvector selection

Writing V columns f_i=K_i/sqrtmu_j gives T_j=V C_n V*, G=V*V and H_n=G^1/2 C_n G^1/2. The columns of mu_j^-1/2 V are v_i=K_i/mu_j. Hence B_j=D_x C_n V* and e_j=v(x)^T C_n V*. For a polynomial a, V* a(V C_n V*) V=G^1/2 a(H_n)G^1/2 follows by multiplying each power, including the constant power. Uniform approximation extends this to continuous functions. This produces exactly the two finite Gram formulas in the note.

No inverse of G is present. Duplicate observations, singular G, zero rank, repeated eigenvalues, and no positive modes are allowed. Kernel derivatives and their fixed-domain integrals are Borel in the data; finite matrix square root and continuous functional calculus are continuous, and the ridge matrix is invertible. Joint Borel measurability and continuous x paths imply C(E)-valued measurability on every compact E by countable dense evaluations; bounded projected output gives L^2-valued measurability on D. The empirical eigenbasis may be arbitrary without appearing in the actual measurable definition.

## 7. Supplementary alternative regularization theorem

For fixed integer s>d/2+2, the Hilbert coefficient space is separable and bounded balls compact in C^2 (choose0<eta<min{1,s-d/2-2}). E is a norm-closed convex subset and weakly closed; normalization is linear and pointwise inequalities pass via compact embedding. The smooth truth has finite unknown norm, but no norm radius is used by the estimator.

The natural form integral grad u^T S grad w on H^1 in weighted L^2 defines every H^s candidate. Its Markov semigroup preserves1 and yields a nonnegative symmetric stationary pair kernel. Conjugation by sqrtmu changes the form to a(v,w)=integral grad(v/sqrtmu)^T S grad(w/sqrtmu) on the common H^1 domain. For bounded H^s sequences with C^1 coefficient convergence, the form coefficients converge uniformly and a+I is uniformly coercive. Lax-Milgram gives norm-resolvent convergence. The continuous f(r)=exp(Delta-Delta/r), f(0)=0 on[0,1], transfers it to operator-norm heat convergence.

Operator norm alone would not give kernel L^2 convergence. Min-max supplies uniform singular-value tails beta_k=exp[-Delta(ell/C)nu_k] with sum beta_k^2 finite by Neumann eigenvalue growth. The inequality s_(2m-1)(T_n-T)<=s_m(T_n)+s_m(T) yields HS^2 <=2M opnorm^2+8sum_(m>M)beta_m^2. Taking the tail small first closes the kernel continuity link. The density multipliers then give F(theta_n)->F(theta) in L^2(DxD).

Equal joint kernels give equal marginals mu, and equal self-adjoint positive-time operators determine equal generators via the unbounded real logarithm. Zero is a spectral accumulation point but has zero projection, so it creates no ambiguity in the log domain. Interior cutoff affine/quadratic functions lie in both generator domains and recover divS and S by comparing their local images. Thus F is injective throughout E, including nonsmooth H^s weak limits and fields touching their pointwise constraints.

Ordinary pair KDE with h~j^-4 has integrated stochastic variance O(j^(16d)2^-j) from the correct overlapping covariance calculation. Markov/Borel-Cantelli gives L^2 stochastic error eventually<=1/(j+1). For a zero-extended smooth true q, the product domain has finite perimeter; its translation symmetric difference has volumeO(|v|), while interior differences are Lipschitz. The squared translation L^2 error isO(|v|+|v|^2). Minkowski gives smoothing biasO(sqrth)=O(j^-2), not global uniform bias. Thus delta_j=O(j^-1) almost surely.

Choose a fixed countable dense subset of E and the first point with cost <=countable infimum+epsilon_j for J=||F(theta)-qhat||^2+alpha_j||theta||^2. The positive epsilon and cost continuity make this measurable and an approximate global minimizer; no finite numerical search is promised. With alpha_j=1/(j+1), epsilon_j=1/(j+1)^2, comparison to the truth gives bounded H^s norm and residual->0 because delta_j^2/alpha_j and epsilon_j/alpha_j vanish. Every subsequence has a weak-H^s/strong-C^1 cluster point in E; forward continuity and identification force the truth. Compactness yields full C^1 convergence, including divS. This is a genuine current alternative deduction, not an earlier paper or a proof for the spectral-equation objective.

## Disposition after independent analytic reconstruction

No mathematical gap or counterexample was found within the explicit model. The theorem supplies an actual data construction, all-positive empirical-mode selection, derivative convergence, interior rank/excitation, stable continuous weighting, any vanishing positive ridge, and measurable finite-feature formulas. The supplementary estimator links also close. The argument makes a scoped consistency claim and supplies neither rates nor computational implementation. Primary-source comparison, provenance, archived/source/PDF consistency, and earlier-review reconciliation are additional review tasks recorded separately.
