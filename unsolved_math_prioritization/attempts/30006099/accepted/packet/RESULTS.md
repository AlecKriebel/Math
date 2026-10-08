# Data-driven maximal averages: a finite-dictionary obstruction and certified alternatives

Problem 30006099 / OWR-14298803-003; queue rank 961.
Author outcome: **partial progress, 5/5 substantive approaches**. Prepared 2026-10-07.
This is an AI-assisted, unrefereed mathematical packet. No novelty or priority claim is made. Independent review is still required.

## 1. Scope and conventions

The relevant source is Giovanni Fantuzzi's contribution, joint work with Jason Bramburger, pp. 3291–3293 of Oberwolfach Report 57/2024. The workshop occurred in December 2024; the report was published on 19 May 2025. Its unresolved requests concern non-polynomial dynamics and quantitative optimal-value errors for the EDMD replacement of an auxiliary-function program. Fixed-function generator convergence is an existing result, not a resolution of optimized-value convergence.

Let X be a compact forward-invariant subset of R^s, f a C^1 vector field on a neighborhood of X generating a forward flow Phi_t, and g continuous. Put L v = f·grad v and

    beta = sup_{x in X} limsup_{T -> infinity} T^(-1) integral_0^T g(Phi_t x) dt.

The established auxiliary-function duality and invariant-measure formulation give

    beta = max_{nu invariant probability on X} integral g dnu
         = inf_{v in C^1(X)} max_X (g + L v).                         (1)

We use the neighborhood-restriction interpretation of C^1(X). Identity (1) is credited to the established literature [TGD], not counted as an author approach. An auxiliary inequality gives an upper bound because the time average of L v is zero: its integral over [0,T] is v(Phi_T x)-v(x), bounded independently of T. Compactness and invariance are essential. Maximization is over all invariant measures, including singular ones, not merely the sampling measure or the measure observed on one attractor.

For a finite dictionary V = span{phi_1,...,phi_k}, an output dictionary W_m containing V, and exact snapshots y_j=Phi_tau(x_j), the data-driven derivative is obtained by least-squares fitting phi_i(y_j) in W_m, then subtracting phi_i(x) and dividing by tau. With a full-rank sample matrix, this is exactly the least-squares regression of

    D_tau phi_i(x_j) = [phi_i(y_j)-phi_i(x_j)]/tau

in W_m. Whenever L^2 phi_i is used below, take phi_i to be C^2 on a neighborhood and require the displayed bound to hold along the flow in X. We distinguish the auxiliary dimension k from output dimension p=dim W_m and polynomial degree m. These are not interchangeable parameters.

## 2. Approach 1: analytic non-polynomial obstruction to the unregularized program

### Theorem 1 (every finite projected degree has an unbounded-below objective)

Take X=[-1,1], f(x)=-x/(1+x^2), and g(x)=x^2. Let mu be the Chebyshev probability measure dx/(pi sqrt(1-x^2)). Let P_m be its L^2-orthogonal projection onto polynomials of degree at most m, m>=2. Then

    inf_{c in R} max_{x in X} [x^2 + c P_m(L x^2)(x)] = -infinity,    (2)

although beta=0 and the exact degree-two auxiliary program already has value 0. Moreover P_m(L x^2) converges uniformly, at an explicit geometric rate, to L x^2.

Proof. The vector field is smooth on R, globally bounded and globally Lipschitz. Every nonzero solution moves monotonically toward zero; its limit must be zero, since f has no other zero. Thus the average of x(t)^2 tends to zero. X is forward invariant and absorbs every bounded subset of R in finite time. For v=x^2,

    g+Lv = x^2 - 2x^2/(1+x^2) = x^2(x^2-1)/(1+x^2) <= 0.

At zero every exact auxiliary derivative vanishes, so the exact infimum is 0.

Write r=3-2 sqrt(2), so 0<r<1. The elementary Poisson-kernel/geometric-series identity yields the uniformly convergent Chebyshev expansion

    1/(1+x^2) = (1/sqrt(2)) [1+2 sum_{j>=1} (-r)^j T_{2j}(x)].      (3)

For verification, put x=cos(theta), use 1+x^2=(3+cos(2theta))/2 and sum the two geometric series. The coefficients in (3) are therefore exactly the orthogonal projection coefficients. With a=floor(m/2),

    q_m(x):=P_m(L x^2)(x)
           = -2+sqrt(2)+2 sqrt(2) sum_{j=1}^a (-r)^j T_{2j}(x).

Since |T_j(x)|<=1 and T_{2j}(0)=(-1)^j,

    q_m(x) <= q_m(0) = -delta_m,
    delta_m = 2 sqrt(2) r^(a+1)/(1-r) > 0.                         (4)

The equality follows either by summing the geometric progression or by evaluating (3) at zero. Its omitted tail also gives ||q_m-Lx^2||_infinity <= delta_m. Therefore max_X(x^2+c q_m)<=1-c delta_m for c>=0, proving (2). This is an analytic proof for every m, not a finite numerical extrapolation. QED.

### Corollary 1 (actual exact-snapshot EDMD, not arbitrary operator perturbations)

For each m>=2 there is tau_m>0 such that, for every fixed 0<tau<=tau_m, the snapshot EDMD program with all polynomials of degree at most two as auxiliary functions and all polynomials of degree at most m as output functions has value -infinity almost surely for all sufficiently large N of iid Chebyshev-distributed initial sites.

Proof. Set H=Lx^2. Direct differentiation gives

    L H=4x^2/(1+x^2)^3,       ||L H||_infinity=16/27<1.

The fundamental theorem of calculus along trajectories implies ||D_tau x^2-H||_infinity<=tau/2. A Chebyshev projection has ||P_m||_{infinity->infinity}<=1+2m (bound its constant coefficient by ||h|| and each other coefficient by 2||h||). Thus choose

    tau_m=delta_m/[4(1+2m)].

The population regression satisfies ||P_m D_tau x^2-q_m||_infinity<=delta_m/8. The population Gram matrix is positive definite. At fixed m,tau, the strong law for its finitely many entries and response entries, followed by continuity of matrix inversion, proves uniform convergence of the sample regression to the population regression. The sample Gram matrix is almost surely full rank once N>=m+1, since the sampling measure is atomless. Eventually its error is less than delta_m/8, leaving the approximate derivative everywhere <=-3 delta_m/4. The same scaling argument as (2) proves the claim. QED.

This also supplies a failing joint diagonal with m->infinity, tau->0 and N->infinity. For example fix the displayed tau_m, choose N_m increasing so that the probability of violating the delta_m/8 regression tolerance is at most 2^(-m), and apply Borel–Cantelli. Such N_m exist by the preceding convergence, and explicit conservative choices follow from Theorem 3. On this diagonal the selected derivative converges uniformly to the true derivative while the optimized values are eventually -infinity.

**Limits of this conclusion.** This proves a failure for the displayed order (N large at fixed m,tau, then tau small for that m), and a failing joint diagonal. It does not assert that every possible iterated order fails. The source displays a different iterated order for its fixed-observable L^2 assertion. We do not interchange that order with infima or claim to refute that assertion. The example's only invariant probability measure is the point mass at zero, so it fails the non-algebraic-support/strict-feasibility hypothesis in [BF-IM]. It does not contradict that paper's conditional theorem. Section 4.4 of [BF-IM] already explains the general instability of invariant-measure programs under perturbations; our construction realizes an explicit non-polynomial snapshot-EDMD obstruction, with no claim of priority for the phenomenon.

## 3. Approach 2: certified auxiliary optimization by weighted error penalties

### Theorem 2 (a robust replacement and consistency)

Suppose continuous functions hat L phi_i and verified numbers epsilon_i>=0 satisfy

    ||hat L phi_i-L phi_i||_infinity <= epsilon_i.

For v_c=sum_i c_i phi_i define

    B = inf_c { max_X(g+sum_i c_i hat L phi_i) + sum_i |c_i|epsilon_i }.

Then beta<=B<=max_X g. Every candidate c provides a certified upper bound, irrespective of optimizer existence. For the coefficient ball ||c||_1<=R, let J_R and hat J_R be the respective exact and approximate unpenalized minima. If epsilon=max_i epsilon_i, then

    |hat J_R-J_R|<=R epsilon,
    beta<=hat J_R+R epsilon<=J_R+2R epsilon.                        (5)

Proof. For each c, the pointwise error has absolute value at most sum_i |c_i|epsilon_i. Therefore the penalized approximate objective dominates max_X(g+Lv_c), hence beta by (1). Choosing c=0 proves the upper bound. Applying the same uniform comparison in both directions on the coefficient ball proves (5). QED.

For an asymptotic sequence, assume the dictionaries are nested, their union is dense in C^1(X), and for each fixed i the certified epsilon_{i,n} tends to zero. Then the corresponding penalized B_n tends to beta. Indeed, choose from (1) a C^1 auxiliary certificate within eta of beta, approximate it in C^1 by one fixed finite dictionary element v_c, and then hold its finitely many coefficients fixed. For all sufficiently large n it is admissible and its penalized approximate objective is at most max_X(g+Lv_c)+2 sum_i |c_i|epsilon_{i,n}. Take limsup and then eta down to zero. The lower bound beta holds for every n. No uniform bound on optimizing coefficients and no global rate for their growth is silently assumed.

For the ball version, consistency instead follows if R_n->infinity, each fixed finite vector eventually lies in the ball, and R_n max_{i<=k_n}epsilon_{i,n}->0. The two schemes must not be conflated. A finite-dimensional or SOS numerical solver introduces its own additional certified optimization/nonnegativity error; an unchecked floating output is not a rigorous certificate.

## 4. Approach 3: an explicit iid regression-to-uniform-error bound

This route gives sufficient data, dictionary, conditioning and sampling assumptions. The constants are conservative and require a priori bounds; they are not inferred from arbitrary finite trajectory data.

### Theorem 3

Let psi_1,...,psi_p be continuous real output functions with |psi_j|<=B on X, and let

    G=E_mu[psi psi^T],       lambda_min(G)>=lambda>0.

Assume each phi_i lies in their span. For iid sites, exact endpoints and a fixed tau>0, let h_i=D_tau phi_i and assume ||h_i||_infinity<=D. Put G_N=N^(-1)sum psi(x_j)psi(x_j)^T, b_i=E[psi h_i], b_{i,N}=N^(-1)sum psi(x_j)h_i(x_j). For failure probability alpha in (0,1), define

    t_G = B^2 sqrt(2 log(4p^2/alpha)/N),
    t_b = B D sqrt(2 log(4pk/alpha)/N),
    Lambda = p B^2/lambda.

If p t_G<=lambda/2, then with probability at least 1-alpha, G_N is invertible and simultaneously for i=1,...,k,

    ||hat L phi_i-P h_i||_infinity <= S_N,
    S_N = (2 sqrt(p) B/lambda)
          [sqrt(p)t_b + p t_G sqrt(p) B D/lambda],                 (6)

where P is the population least-squares projection onto the output dictionary.

Proof. Hoeffding's inequality applied to each Gram and response entry and a union bound give |(G_N-G)_{ab}|<=t_G and |(b_{i,N}-b_i)_a|<=t_b, simultaneously, with total failure probability at most alpha. Consequently ||G_N-G||_2<=p t_G, ||G_N^(-1)||_2<=2/lambda, and ||G^(-1)b_i||_2<=sqrt(p)BD/lambda. The identity

    a_{i,N}-a_i = G_N^(-1)[(b_{i,N}-b_i)-(G_N-G)a_i]

and ||psi(x)||_2<=sqrt(p)B give (6). QED.

If ||L^2 phi_i||_infinity<=M_i and E_m(Lphi_i)=inf_{w in W_m}||Lphi_i-w||_infinity, then on the same event

    epsilon_i = S_N + Lambda tau M_i/2 + (1+Lambda)E_m(Lphi_i)      (7)

is a valid uniform generator-error bound. The proof uses ||P||_{infinity->infinity}<=Lambda, the flow difference-quotient remainder, and P w=w. Smooth non-polynomial f is allowed. A sufficient diagonal makes all three terms tend to zero for each fixed phi_i; growing ill-conditioning or growing Lambda must be compensated, rather than omitted. For a finite collection of stages, split the total failure budget among them; for infinitely many stages choose summable alpha_n and apply Borel–Cantelli for eventual validity.

This result is a self-contained elementary sufficient bound, not a new claim to the general Monte Carlo rate. Existing work [BF-AF], [LLLK] and the September 2026 preprint [FMBBr] supplies broader/sharper operator approximation theory. Equation (7) also exposes why N,m,tau alone cannot specify a universal accuracy: dictionary conditioning, approximation regularity and optimization sensitivity matter. Exact initial sites and noiseless scalar responses are assumptions here. Predictor noise is not covered by (6).

## 5. Approach 4: a finite linear program using spatial coverage

This approach changes the estimator and avoids a global polynomial positivity oracle. Let Z={z_1,...,z_N} subset X have verified fill distance h: every x in X is within h of a site. Suppose g has a known modulus of continuity omega_g. At site z_j observe d_{ij}, with

    |d_{ij}-D_tau phi_i(z_j)|<=zeta_i.

Assume verified Lip_X(Lphi_i)<=ell_i and ||L^2phi_i||_infinity<=M_i. Set

    a_i=zeta_i+tau M_i/2,        e_i=a_i+ell_i h.

### Theorem 4 (finite LP upper certificate)

Minimize

    t + omega_g(h) + sum_i e_i |c_i|

subject to the N inequalities

    t >= g(z_j)+sum_i c_i d_{ij}.

Its infimum C is a finite certified upper bound on beta. Absolute values are implemented by c_i=c_i^+-c_i^- with nonnegative c_i^+,c_i^-; with nonnegative penalties this has the same infimum. Every feasible solution gives a rigorous bound.

Proof. For x choose a nearest site z_j. Then

    g(x)+sum_i c_i Lphi_i(x)
      <= g(z_j)+sum_i c_i d_{ij}+omega_g(h)+sum_i |c_i|e_i.

Take the supremum in x and use (1). The zero coefficient vector provides a finite feasible objective. For any fixed c the LP's objective at that c is at most

    max_X(g+Lv_c)+omega_g(h)+sum_i |c_i|(2a_i+ell_i h).            (8)

This follows by first replacing the data by exact Lphi_i at the sites, with error sum |c_i|a_i. QED.

Under nested C^1-dense dictionaries, fixed finite ell_i and M_i for each fixed i, h_n->0, tau_n->0, and zeta_{i,n}->0 for each fixed i, (8) and the fixed-certificate argument prove C_n->beta. This is a genuinely non-polynomial sufficient convergence theorem for a modified data-only LP with supplied regularity bounds. It does not establish convergence of the unmodified OWR optimization (2).

For a convex containing neighborhood with ||f||<=F, ||Df||<=K, ||grad phi_i||<=G_i and ||Hess phi_i||<=H_i, one may take ell_i=KG_i+FH_i and M_i=F ell_i. Only these bounds, rather than an explicit formula for f, are needed by the LP. They must be independently justified. If the recorded endpoint observable has absolute error nu_i, exact initial sites give zeta_i=nu_i/tau; thus shrinking tau with fixed observational noise does not ensure consistency.

The fill-distance requirement can be met by designed grids. Iid full-support sampling on compact X gives h_N->0 almost surely: cover X by finitely many positive-mass balls for each radius, apply the probability of missing a ball, and intersect over reciprocal integer radii. For a quantitative version, if an r/2-net has at most C r^(-s) centers in X and every ball of radius r/2 centered in X has mu-mass at least c(r/2)^s, then

    Pr(h_N>r) <= C r^(-s) exp[-Nc(r/2)^s].                        (9)

Thus a specified coverage probability is a sufficient, explicitly checkable data assumption. A single trajectory need not supply it.

## 6. Approach 5: relaxed invariant-measure LP and identification limits

The same samples support a different, primal construction that avoids unbounded auxiliary coefficients and permits singular maximizing measures.

### Theorem 5 (relaxed stationarity on grids)

With the assumptions and e_i from Theorem 4, maximize

    sum_j w_j g(z_j)+omega_g(h)

over w_j>=0, sum_j w_j=1, subject to

    |sum_j w_j d_{ij}|<=e_i       for all i.                      (10)

The LP is feasible and its maximum Q satisfies Q>=beta. Along the asymptotic sequence of Theorem 4, if the test dictionaries are nested and C^1-dense, then Q_n->beta.

Proof. Any invariant measure nu satisfies integral Lphi_i dnu=0. Push nu forward to a nearest-site map, breaking ties by smallest index. The resulting weights obey (10), since replacement of Lphi_i(x) by d_{ij} incurs error at most ell_i h+a_i. Also integral g dnu<=sum_j w_j g(z_j)+omega_g(h). Applying this to a maximizing invariant measure proves feasibility and the lower bound.

Take any subsequence of maximizers and extract a weakly convergent subsequence of their discrete probability measures, using compactness of X. For each fixed i,

    |integral Lphi_i dnu_n| <= e_{i,n}+a_{i,n} -> 0.

Continuity of Lphi_i and weak convergence imply integral Lphi_i dnu=0. C^1 density, and bounded f, extend this equality to every C^1 test function. It implies invariance: for a C^1 test psi, psi composed with Phi_t is C^1 and

    d/dt integral psi(Phi_t x)dnu(x)
      = integral L(psi composed with Phi_t)(x)dnu(x)=0.

One uses a neighborhood extension on any fixed finite time interval; compactness supplies uniform domination. Density in C(X) then yields invariance for continuous tests. The limiting objective is integral g dnu<=beta. Every subsequential limiting objective has this bound, whereas Q_n>=beta, so Q_n->beta. QED.

This finite LP is dual to Theorem 4's weighted-penalty LP by ordinary finite-dimensional linear programming duality. The independent compactness proof above explains convergence through measures and treats atomic maximizers directly; it is not an appeal to unavailable strict feasibility. These are two mathematical routes to the same computable relaxation, not two independent algorithms.

### Proposition 6 (trajectory coverage cannot be discarded)

On X=[0,1] let g(x)=x and compare f_0(x)=-x with f_1(x)=-x(1-x). Their entire trajectories started at zero, and every snapshot thereof at every sampling interval, agree identically. But beta_0=0 and beta_1=1, the latter attained by the stationary initial point x=1. Any estimator using only that trajectory receives identical data on the two systems and cannot be consistent for both maximal averages. Both systems are polynomial and smooth. Hence this is an information/coverage obstruction, not specifically a non-polynomial effect. This observation does not count as an additional turn.

## 7. What remains unresolved

1. The complete source program is not solved. We have neither necessary-and-sufficient hypotheses for unmodified EDMD optimized-value convergence nor quantitative error guarantees for all non-polynomial systems in the source's intended scope.
2. The unregularized counterexample intentionally has a singular sole invariant measure. Whether a given non-polynomial system satisfying suitable stability/strict-feasibility assumptions admits useful convergence rates for the unmodified scheme is separate.
3. The positive LP results require spatial coverage and known regularity or generator error bounds. They do not infer these globally from arbitrary finite data, solve noisy-predictor learning, or avoid dimension-dependent coverage costs.
4. C^1-dense auxiliary approximation gives qualitative consistency. A rate relative to beta additionally requires a quantitative near-optimal auxiliary-certificate approximation bound. Equations (5), (7), (8), and (9) display rather than conceal this dependence.
5. General sum-of-squares truncation errors, correlated trajectory concentration, and infinite-dimensional state spaces are not resolved here.

The legitimate outcome is partial progress: an explicit instability construction, certified alternatives with proved sufficient hypotheses, and precise remaining gaps. All finite checks supplement the analytic arguments; none proves an infinite-dimensional convergence theorem.

## References

[OWR] G. Fantuzzi, joint work with J. Bramburger, “Time averages, polynomial optimization and Koopman,” in Mini-Workshop: Data-driven Modeling, Analysis, and Control of Dynamical Systems, Oberwolfach Reports 21 (2024), pp. 3291–3293. Published 2025. https://doi.org/10.4171/OWR/2024/57 ; public report https://ems.press/content/serial-article-files/50766

[TGD] I. Tobasco, D. Goluskin, C. R. Doering, “Optimal bounds and extremal trajectories for time averages in nonlinear dynamical systems,” Physics Letters A 382 (2018), 382–386. https://doi.org/10.1016/j.physleta.2017.12.023 ; inspected author version https://arxiv.org/abs/1705.07096v3

[BF-AF] J. J. Bramburger and G. Fantuzzi, “Auxiliary Functions as Koopman Observables: Data-Driven Analysis of Dynamical Systems via Polynomial Optimization,” Journal of Nonlinear Science 34 (2024), article 8. https://doi.org/10.1007/s00332-023-09990-2 ; https://arxiv.org/abs/2303.01483v4 ; relevant results are Theorems 4.1–4.4.

[BF-IM] J. J. Bramburger and G. Fantuzzi, “Data-driven discovery of invariant measures,” Proceedings of the Royal Society A 480 (2024), 20230627. https://doi.org/10.1098/rspa.2023.0627 ; https://arxiv.org/abs/2308.15318v2 ; relevant hypotheses and limitations are in Sections 4.1–4.4.

[LLLK] L. Llamazares-Elias, S. Llamazares-Elias, J. Latz and S. Klus, “Data-driven approximation of Koopman operators and generators: Convergence rates and error bounds,” author preprint, v3 dated 24 June 2026. https://arxiv.org/abs/2405.00539v3

[FMBBr] D. Fassler, R. Morris, J. Bramburger and S. Brugiapaglia, “Finite-Data Error Bounds for Approximating the Koopman Operator: Sampling Measures, Super-Polynomial Convergence and Regularization,” author preprint, v1 dated 25 September 2026. https://arxiv.org/abs/2609.31817v1
