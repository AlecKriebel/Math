# Independent analytic reconstruction of the alternative regularization estimator

The alternative consistency conclusion stated in the bundled classical_regularization_application.md survives the attacks below. This is a newly checked application of classical identification, compactness and quadratic regularization. It is not a proof about the PR's empirical spectral-equation estimator, and not a located historical theorem about this exact application.

## 1. Parameter space, truth membership and unknown radius

Fix an integer s>d/2+2 before observing data. Let X be the real Hilbert product of H^s(D) for the independent symmetric entries of S and mu, with a fixed product Hilbert norm. Let E be the pointwise constrained set in the note. The smooth truth theta0 belongs to E, and has a finite norm M=||theta0||_X. M is never an estimator input.

A smooth bounded domain admits bounded Sobolev extension to Euclidean space. Choose 0<eta<min{1,s-d/2-2}. The Sobolev embedding H^s(D) into C^{2,eta}(D-bar), followed by the compact inclusion into C^2(D-bar), gives compactness of bounded H^s sets in C^2. A smaller eta can be used when needed. In particular there is compactness in C^1. If theta_n converges weakly in X, it is bounded; any C^2 subsequential limit equals its weak X limit as a distribution. Thus a weakly convergent sequence actually converges in C^2 after identifying its unique possible compact limit, and the full sequence does so by the subsequence criterion.

E is weakly sequentially closed: the compact-limit argument passes the matrix inequalities, density bounds and normalization to the limit. There is also a direct check: E is a norm-closed convex subset of X (point evaluations are continuous since s>d/2); a norm-closed convex set in a Hilbert space is weakly closed. The normalizing integral is a continuous linear functional. Neither argument imposes a bound on the unknown M. Touching ell, Lambda, c or C is permitted. The average 1/vol(D) lies in [c,C] whenever E is nonempty, so (ell I,1/vol(D)) is one explicit admissible initial output.

Attack disposition: no unknown-radius or admissible-boundary gap. Compact C^2 does require the strict s>d/2+2 used in the note. Equality at the critical exponent would not suffice.

## 2. A forward density on the entire candidate class

For every theta=(S,mu) in E, use the form

    e_theta(u,w)=integral_D grad(u)^T S grad(w) dx

on V=H^1(D), in H_mu=L^2(mu dx). Ellipticity and c<=mu<=C make the form plus the weighted L^2 norm equivalent to the H^1 norm. It is a densely defined closed nonnegative symmetric form. Its associated nonnegative self-adjoint operator B_theta realizes -L_theta with natural conormal boundary condition. The contraction property under normal scalar contractions makes its semigroup Markov. Constants have zero energy, so P_theta(t)1=1. No choice of a classical operator domain common to all candidates is required.

Let U_mu:H_mu->L^2(dx), U_mu u=sqrt(mu)u, a unitary map. Multiplication by sqrt(mu) and its reciprocal are automorphisms of H^1 since mu is C^1 and positive. The conjugated A_theta=U_mu B_theta U_mu^{-1} has the common form domain H^1 and form

    a_theta(v,w)=integral_D grad(v/sqrt(mu))^T S grad(w/sqrt(mu)) dx.

The semigroup T_theta=exp(-Delta A_theta) is Hilbert-Schmidt by the eigenvalue argument below. Consequently Q_theta=M_sqrt(mu) T_theta M_sqrt(mu) has a unique L^2(DxD) kernel q_theta. Positivity of the semigroup and the positive multipliers imply q_theta>=0 almost everywhere. T_theta sqrt(mu)=sqrt(mu), so Q_theta 1=mu; symmetry gives both marginals mu and total integral one. This defines F(theta)=q_theta throughout E even without invoking a smooth heat kernel for every candidate. For a smooth truth it agrees with mu(x)p_Delta(x,y), the observed stationary pair density.

Attack disposition: candidate H^s regularity is enough; no illicit C^infinity requirement on weak limits or candidate operator domains enters the construction.

## 3. Common-form coercivity and norm resolvents

Consider a bounded X sequence theta_n converging in C^1 to theta in E. Put b_n=a_n+<.,.>_2 and b=a+<.,.>_2. On this sequence c,C,ell,Lambda and sup||mu_n||_{C^1} are uniformly bounded. The identity

    grad v=sqrt(mu_n) grad(v/sqrt(mu_n))
           + v grad(sqrt(mu_n))/sqrt(mu_n)

gives ||v||_{H^1}^2 <= C0 (a_n(v,v)+||v||_2^2). Its reverse identity gives the upper bound. Thus b_n(v,v)>=eta0||v||_{H^1}^2 for one eta0>0, and the forms are uniformly bounded on H^1.

Expand grad(v/sqrt(mu_n)) into mu_n^{-1/2}grad v plus v grad(mu_n^{-1/2}). The coefficients of the resulting grad-v/grad-w, grad-v/w, v/grad-w and v/w terms converge uniformly. Hence

    |a_n(v,w)-a(v,w)| <= epsilon_n ||v||_{H^1}||w||_{H^1}, epsilon_n->0.

For f in L^2, set v_n=(I+A_n)^{-1}f and v=(I+A)^{-1}f. Lax-Milgram gives ||v||_{H^1}<=eta0^{-1}||f||_2, and

    b_n(v_n-v,w)=(a-a_n)(v,w).

Taking w=v_n-v yields ||v_n-v||_{H^1}<=epsilon_n eta0^{-2}||f||_2. Therefore R_n=(I+A_n)^{-1}->R=(I+A)^{-1} in operator norm on L^2. This proof explicitly handles changing conormal operator domains; it only fixes their form domain.

Attack disposition: norm resolvent convergence is proved, not inferred from pointwise coefficient convergence across changing operator domains.

## 4. Semigroups and the indispensable uniform trace tail

Each R_n is a self-adjoint contraction with spectrum in [0,1]. Define f(0)=0 and f(r)=exp(Delta-Delta/r) for r>0. This is continuous on [0,1], including at zero. Spectral calculus gives T_n=f(R_n). Approximate f uniformly by polynomials. For each fixed polynomial p, p(R_n)->p(R) in norm by telescoping powers; uniform approximation then proves T_n->T in operator norm. Neither a logarithm of noisy data nor commutation between R_n and R is used.

Let nu_k be the nondecreasing Neumann Laplacian eigenvalues, including nu_1=0. On the same vector space H^1, the original weighted Rayleigh quotient satisfies

    e_n(u,u)/integral mu_n u^2 >= (ell/C) integral |grad u|^2/integral u^2.

Min-max over finite-dimensional subspaces therefore gives lambda_k(A_n)>=a nu_k, a=ell/C. The unitary U_mu does not change eigenvalues. The domain is connected, so nu_2>0, also proving the required spectral gap. The heat singular values obey s_k(T_n)<=beta_k=exp(-Delta a nu_k).

For completeness, the needed eigenvalue-growth bound does not follow from compactness alone. Extend H^1(D) boundedly into a fixed ambient torus, with a collar cutoff. Fourier truncation at radius R has rank O(R^d) and restricted L^2 approximation error <=C/R times ||u||_{H^1}. If a Neumann eigenspace spanned by k low modes has dimension greater than that rank, some unit L^2 vector in it has zero truncation. Its H^1 norm is at most sqrt(1+nu_k), so 1<=C/R sqrt(1+nu_k). Taking R comparable to k^{1/d} proves nu_k>=c0 k^{2/d}-C1. In particular sum beta_k^2<infinity.

For B_n=T_n-T the approximation-number inequality

    s_{2m-1}(B_n)<=s_m(T_n)+s_m(T)<=2 beta_m

follows by subtracting rank-(m-1) approximants of the two compact operators. Monotonicity gives the same bound for s_{2m}(B_n). Thus

    ||B_n||_HS^2 <= 2M ||B_n||_op^2 + 8 sum_{m>M} beta_m^2.

First send M to infinity to control the common tail, then n to infinity for the finite part. Hence T_n->T in Hilbert-Schmidt norm. Uniform convergence of sqrt(mu_n), the multiplier bound sqrt(C), and the uniform HS bound sum beta_k^2 give Q_n->Q in HS norm. The HS-kernel isometry is exactly F(theta_n)->F(theta) in L^2(DxD).

Combining this with section 1 establishes weak sequential continuity of F on E (weak sequences in X are bounded), and norm continuity. The negative control B_n=n^{-1/2}I on n-dimensional orthogonal blocks has operator norm tending to zero and HS norm one: omitting the uniform tail would be fatal. The note supplies that tail correctly.

Attack disposition: no operator-to-density gap; the critical uniform summability step survives independently.

## 5. Identification, including the unbounded logarithm

Suppose F(theta1)=F(theta2). Their marginals give mu1=mu2 almost everywhere, hence everywhere by continuity. With common mu, the stationary density determines P_Delta on H_mu by division by mu(x), equivalently Q and T by multiplication with mu^{-1/2}. Both underlying generators are self-adjoint.

If T=exp(-Delta A), then T is injective: its spectral measure at the singleton {0} is zero, since exp(-Delta lambda)>0 for every finite lambda in the spectral measure of A. Zero may still be in the spectrum as an accumulation point. The Borel functional calculus recovers

    A=-(1/Delta) log T,
    Dom(A)={v: integral_(0,1] |log r|^2 d<v,E_T(r)v> < infinity}.

The value assigned to log at r=0 is irrelevant because its spectral projection is zero. Equal T gives equal spectral measures, domains and generators. This is the exact distinction from taking a logarithm of an empirical operator with negative or zero eigenvalues.

Every compactly supported smooth test function belongs to both weighted generator domains: integration by parts has no boundary term, and mu^{-1}div(S grad phi) is continuous and L^2 since the coefficients are C^1. Equality of the generators gives equality of these continuous expressions at every interior point. At x0, a cutoff affine function with gradient v and Hessian zero recovers (div S)/mu through its value of L. A cutoff quadratic function centered at x0 with gradient zero and arbitrary symmetric Hessian H gives Lphi(x0)=S(x0):H/mu(x0). Equality for all H recovers S(x0). Equality on the closure follows from continuity. The argument works across the entire H^s class, including candidates touching pointwise bounds; it needs neither finitely many eigenpairs nor an inverse continuous on an unbounded parameter class.

Attack disposition: no aliasing, candidate regularity or logarithm-domain gap.

## 6. Truth heat-kernel regularity and zero-extension bias

Only the true smooth coefficients require smooth spatial heat-kernel regularity. The conormal elliptic eigenproblem for the smooth truth has smooth eigenfunctions on D-bar. Iterated elliptic estimates applied to -div(S grad u_k)=lambda_k mu u_k bound every fixed Sobolev norm, and then every fixed C^r norm, by a polynomial in 1+lambda_k. Combining this with the eigenvalue-growth bound and exp(-Delta lambda_k) gives absolute uniform convergence of the differentiated expansion

    q(x,y)=mu(x)mu(y) sum_k exp(-Delta lambda_k) u_k(x)u_k(y),

where u_k are orthonormal in L^2(mu). Thus q is smooth on D-bar x D-bar; C^1 boundedness already suffices below. This avoids applying a boundary-biased Euclidean density theorem to a globally smooth zero extension, which is false.

Let Omega=DxD and tilde q=q 1_Omega. A C^1 extension of q to an ambient neighborhood exists by separate extensions in the two D variables; after cutoff it is bounded and globally Lipschitz. For a translation vector v=(v_x,v_y), smooth boundary finite perimeter gives

    |Omega triangle (Omega+v)| <= vol(D) Per(D)(|v_x|+|v_y|) <= C|v|.

This also follows by telescoping the translations in the two factors and does not require the cornered product boundary to be smooth. On the common interior the Lipschitz extension controls differences by C|v|; on the symmetric difference boundedness controls the jump. Consequently

    ||tilde q(. - v)-tilde q||_2^2 <= C(|v|^2+|v|).

For a fixed smooth compactly supported probability kernel K in R^{2d}, Minkowski gives

    ||K_h*tilde q-tilde q||_2 <= integral K(w) C sqrt(h|w|+h^2|w|^2) dw
                              <= C sqrt(h).

Restriction to Omega cannot increase this error. With h_j=h0(j+1)^{-4} the bias is O((j+1)^{-2}). No uniform boundary consistency is claimed. As an exact stress example, for the unit m-cube and a product uniform kernel, the squared L^2 bias is (1-5h/6)^m-2(1-h/2)^m+1=m h/6+O(h^2), while the corner value stays 2^{-m}. Smooth even kernels retain the same nonvanishing flat-boundary phenomenon. The nonsmooth control kernel is illustrative only; it is not used in the estimator's theorem.

Attack disposition: the note's L^2 boundary argument is valid; replacing it with global uniform bias would fail.

## 7. Overlapping pairs and almost-sure KDE error

Let Y_i=X_{iDelta}, P=P_Delta and Z_i=(Y_i,Y_{i+1}). Reversibility, connectedness and the spectral bound give ||P|| on mean-zero L^2(mu) equal to rho<1. For bounded real F of a pair, write H=F-EF, r(z)=E[H(Y0,Y1)|Y1=z] and s(z)=E[H(Y0,Y1)|Y0=z]. Conditional Jensen bounds both L^2 norms by sqrt(Var F), and both means are zero. The Markov property, including at the shared endpoint when lag=1, gives

    Cov(F(Z0),F(Z_l))=<r,P^{l-1}s>_mu,
    |Cov|<=rho^{l-1} Var F, l>=1.

Therefore

    Var(n^{-1} sum_i F(Z_i)) <= [1+2/(1-rho)] ||F||_infinity^2/n.

There is no independence assumption on the pairs. An exact two-state Markov control with F(a,b)=a+b and eigenvalue rho=7/10 has Var F=2(1+rho), Cov_l=(1+rho)^2 rho^{l-1}; it violates the stronger incorrect rho^l Var bound, while satisfying the note's bound. The genuine exponent in the note passes this adversarial test.

At n_j=2^j, each KDE summand F_z= h_j^{-2d} K((z-Z_i)/h_j) is bounded by ||K||_infinity h_j^{-2d}. Tonelli and the finite volume of Omega imply

    E ||qhat_j-E qhat_j||_2^2 <= C h_j^{-4d} 2^{-j}
                               <= C (j+1)^{16d}2^{-j}.

Markov at squared threshold (j+1)^{-2} gives a bound C(j+1)^{16d+2}2^{-j}; its sum is finite for each fixed d. Borel-Cantelli requires no independence across j and gives stochastic error <=(j+1)^{-1} eventually almost surely. Stationarity gives E qhat_j=K_{h_j}*tilde q restricted to Omega. With section 6,

    delta_j=||qhat_j-F(theta0)||_2=O((j+1)^{-1}) almost surely.

All constants may depend on the fixed truth; the bandwidth and regularization schedule do not. Symmetrization is an orthogonal projection in L^2 onto symmetric kernels and cannot worsen error to the symmetric truth.

Attack disposition: variance, overlap, bandwidth dependence, boundary rate and Borel-Cantelli all close.

## 8. Measurable approximate global minimization

E as a metric subspace of the separable Hilbert space X has a countable dense set {e_k}, fixed using only the known E. One explicit existence construction is to take a fixed dense sequence in X and project it onto the closed convex E; metric projection is nonexpansive and its projected sequence is dense in E. This does not presume rational coefficient fields stay feasible at a tight bound.

For alpha_j=(j+1)^{-1}, epsilon_j=(j+1)^{-2}, let

    J_j(e)=||F(e)-qhat_j||_2^2+alpha_j||e||_X^2,
    g_j=inf_{k>=1} J_j(e_k).

F and the penalty are norm continuous, so g_j=inf_E J_j. It is finite and nonnegative since E is nonempty. The map from finitely many positions to qhat_j is continuous in L^2 (translations of smooth K), hence Borel measurable. Each J_j(e_k) and their countable infimum are measurable. Choose k_j as the smallest index with J_j(e_k)<=g_j+epsilon_j, which exists since epsilon_j>0. Its event at index k is that inequality at k intersected with its failures at all earlier indices, a measurable event. Then thetahat_j=e_{k_j} is a measurable X-valued estimator. No measurable selection over an uncountable argmin, no exact minimizer, and no numerical search termination claim is needed.

Attack disposition: measurable mathematical existence holds. Computational effectiveness and finite arithmetic are separate, unclaimed requirements.

## 9. Pathwise convergence and every sample size

On the single probability-one event in section 7, comparison with the fixed truth gives

    ||F(thetahat_j)-qhat_j||_2^2+alpha_j||thetahat_j||_X^2
      <=delta_j^2+alpha_j M^2+epsilon_j.

Here delta_j^2/alpha_j=O(1/(j+1))->0 and epsilon_j/alpha_j=1/(j+1)->0. Thus limsup ||thetahat_j||_X^2<=M^2 and the residual tends to zero. The estimates have a bounded tail in X, whose bound follows from comparison and does not use M as input. Every subsequence has a further weak-X/strong-C^1 subsequence converging to some theta* in E. Sections 3–4 and the residual imply F(theta*)=F(theta0). Section 5 forces theta*=theta0. The compact subsequence criterion now gives convergence of the full sequence in C^1(D-bar).

For each observed N>=2, j=floor(log2 N) permits the first n_j+1 states among the N+1 observations. Reuse the jth output. As N tends to infinity j does too, so this full-N estimator converges on the same event. Assign the explicit admissible initial value for N<2. C^1 convergence of S implies uniform convergence of div S componentwise, since (div S)_b=sum_a partial_a S_ab. Uniform convergence also implies global L^2 convergence on bounded D. No clipping is needed because every output is already in E.

Attack disposition: all-N extension and divergence conclusion hold. The proof does not promote pointwise-in-truth consistency into an uncontrolled uniform rate.

## Verdict

All nine analytic/statistical links pass. No fatal gap or mandatory mathematical repair was found in the frozen note. The detailed derivations here make its implicit classical steps checkable. Historical and estimator-specific limitations are recorded in the bundled SOURCE_EDITIONS.md. This reconstruction used an independent AI adversary and is not human peer review.
