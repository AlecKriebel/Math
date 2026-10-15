# Turn 1: a basis-invariant deterministic consistency theorem

2026-10-02. First substantive author turn for target30003508. This is a scoped deterministic result for general smooth anisotropic tensors and unknown invariant density. It does not yet prove that the required empirical kernel estimates can be constructed with the stated convergence from low-frequency observations. The original statistical target remains unresolved after1/5 turns.

## 1. Setting and estimator

Let D be a bounded connected smooth domain in R^d, d>=2. Let S and μ be smooth on its closure, with S symmetric uniformly positive definite, μ bounded above and below by positive constants, and integral_D μ=1. The reflecting generator is

    Lu=μ^(-1) div(S grad u),   n·S grad u=0 on the boundary.

Fix an observation lag Δ>0. On L²(μ dx), P=exp(ΔL) is positive, compact, self-adjoint and injective. Its real orthonormal eigenfunctions u_k have eigenvalues κ_k=exp(Δν_k)>0, where ν_k<=0 are the generator eigenvalues. The stationary constant eigenfunction is included; its gradient and Hessian vanish.

Let p(x,y) be the transition density with respect to Lebesgue measure and q(x,y)=μ(x)p(x,y) its stationary joint density. Reversibility makes q symmetric. On H=L²(D,dx), define the conjugated operator T by kernel

    T(x,y)=q(x,y)/sqrt(μ(x)μ(y)).

It is compact positive self-adjoint with orthonormal eigenfunctions φ_k=sqrt(μ)u_k and eigenvalues κ_k.

Suppose q_n is a real symmetric finite-rank kernel, μ_n is positive, and Δ is known. Define T_n by the same conjugation with q_n and μ_n. For each positive nonzero eigenvalue κ_(n,k) of T_n, take an orthonormal real eigenbasis φ_(n,k), put u_(n,k)=φ_(n,k)/sqrt(μ_n), and ν_(n,k)=Δ^(-1)log κ_(n,k). Negative empirical eigenvalues are discarded. No labeling or matching of empirical eigenvectors to true ones is assumed.

For a smooth scalar function u define its differential jet J u in R^m, m=d(d+1)/2+d, by listing

    (∂_ii u)_i, (2∂_ij u)_(i<j), (∂_j u)_j.

The matching unknown vector θ lists (S_ii)_i, (S_ij)_(i<j), and (div S)_j. Thus

    (J u)·θ=div(S grad u).

At every interior point x, define the ridge spectral estimator θ_n(x) as the unique minimizer over z∈R^m of

    Σ_(κ_(n,k)>0) κ_(n,k)^4
       [(J u_(n,k))(x)·z−ν_(n,k) μ_n(x)u_(n,k)(x)]²
       +λ_n |z|²,

where λ_n>0 and λ_n→0. The sum is finite. Write its normal equation as

    θ_n=(A_n+λ_n I)^(-1)b_n.

This is an explicit weighted fit of the source's eigenfunction equations. Its local unknowns temporarily treat S and div S as independent; consistency below recovers their correct common limit. No finite-K identifiability assumption is inserted.

## 2. Precise conditional convergence hypotheses

Assume a common positive lower bound for μ_n and μ, and

1. μ_n→μ uniformly on D and in C²(E) for every compact E contained in D
2. q_n→q in L²(D×D)
3. For every such E and each multi-index |α|<=2,

    sup_(x∈E) ||∂_x^α(q_n−q)(x,·)||_(L²(D)) →0.

The kernels and derivatives are continuous in the displayed Hilbert-valued sense. These are deterministic assumptions. They may hold on a probability-one event or in probability for statistical estimators, but this turn does not prove that they do.

**Theorem.** Under these hypotheses, θ_n→θ uniformly on every compact interior set E. In particular the reconstructed tensor entries converge uniformly there. If known fixed ellipticity and norm bounds contain S, clipping the estimated symmetric tensor to the corresponding closed convex matrix set also gives convergence in L²(D), provided the above local convergences hold simultaneously on a compact exhaustion.

The class is anisotropic and μ is unknown. The theorem does not require simple eigenvalues, individual empirical eigenvector convergence, a prescribed finite number of eigenpairs, or an unproved pointwise excitation condition.

## 3. Operator form and eigenvalue collisions

Let M_n be multiplication by μ_n^(-1/2), and set W_n=M_n T_n, W=M T. The hypotheses imply

    ||T_n−T||_(H→H)→0,
    ||W_n−W||_(H→C²(E))→0.

For the first assertion, the Hilbert–Schmidt kernel norm suffices. For the second, differentiate the multiplier and apply Cauchy–Schwarz to the kernel in its y variable. Uniform positive lower bounds and C²(E) convergence control each multiplier derivative. Global uniform convergence of μ_n controls the y multiplier.

For x∈E define bounded linear functionals

    B_n(x):H→R^m,   B_n(x)f=J(W_n f)(x),
    e_n(x):H→R,     e_n(x)f=(W_n f)(x),

and their true counterparts B,e. Their operator norms converge uniformly in x. Define continuous real functions, including their values at zero, by

    g(t)=t² if t>0, and 0 if t<=0,
    h(t)=t² log t if t>0, and 0 if t<=0.

Spectral expansion gives the exact identities

    A_n(x)=B_n(x) g(T_n) B_n(x)*,
    b_n(x)=μ_n(x)/Δ · B_n(x) h(T_n) e_n(x)*.             (3.1)

Indeed W_n φ_(n,k)=κ_(n,k)u_(n,k), so the two outer factors contribute κ², and the middle factors contribute κ² or κ² log κ. These formulas also explain why the power4 is useful: h is continuous at zero despite the logarithm. It suppresses small empirical eigenvalues without estimating their eigenvectors separately.

The spectra of the self-adjoint T_n lie in a common bounded interval because T_n→T in operator norm. Continuous functional calculus therefore gives g(T_n)→g(T) and h(T_n)→h(T) in operator norm. One elementary proof approximates g and h uniformly on that interval by polynomials and uses the telescoping formula for powers of bounded operators. Applying this to (3.1) proves

    A_n→A and b_n→b uniformly on E.                    (3.2)

This includes arbitrary multiplicities and empirical splits of true repeated eigenvalues. The weighted sums are invariant under orthogonal basis changes inside any eigenspace. Positivity of A_n follows directly from g>=0.

## 4. Identification from the full spectral jet family

True spectral expansion gives

    A(x)=Σ_k κ_k^4 J u_k(x) J u_k(x)^T,
    b(x)=Σ_k κ_k^4 ν_k μ(x)u_k(x) J u_k(x).

The eigenfunction PDE shows b(x)=A(x)θ(x). The series and differentiated kernels are legitimate because the fixed positive-time elliptic semigroup is smoothing; equivalently the bounded-functional identities in section3 define their convergent sums.

We prove A(x) is positive definite at every interior point, rather than assume excitation. If ξ^T A(x)ξ=0, every nonnegative term forces ξ·J u_k(x)=0, since κ_k>0.

For any f∈C_c^∞(D), the eigenfunction partial sums converge to f in C². Here is the standard elliptic argument with its relevant hypotheses: f belongs to the domain of every power of the smooth conormal Neumann operator, because it vanishes near the boundary; spectral partial sums converge in every such graph norm. Iterated elliptic regularity turns a sufficiently high graph norm into H^(2j), and Sobolev embedding for 2j>d/2+2 gives C² convergence. Thus ξ·J f(x)=0 for every such test function.

Multiplying arbitrary affine and quadratic polynomials centered at x by a cutoff equal to one near x realizes every possible gradient and symmetric Hessian at x. Their jets fill R^m, so ξ=0. This proves positivity.

The matrix A is continuous in x, as follows from the continuous evaluation functionals in section3. Therefore on each compact E there is an α_E>0 such that A(x)>=α_E I. Notice that this constant may be small and depends on the true coefficients and E; no uniform rate or practical conditioning claim is made.

## 5. Consistency and boundary handling

By (3.2), eventually A_n>=α_E I/2 on E. Since b=Aθ,

    θ_n−θ=(A_n+λ_n I)^(-1)
       [(b_n−b)+(A−A_n)θ−λ_n θ].

Consequently

    ||θ_n−θ||_(∞,E)
    <=(2/α_E)[||b_n−b||_(∞,E)
         +(||A_n−A||_(∞,E)+λ_n)||θ||_(∞,E)] →0.

This proves the stated interior result. For a probabilistic version on a common almost-sure event, the same proof applies pathwise. Convergence in probability follows from the corresponding probability versions of the assumptions and the same fixed α_E bound.

For the L² assertion, fix constants 0<ell<=Lambda such that ell I<=S(x)<=Lambda I on D, and project the reconstructed symmetric tensor pointwise in Frobenius norm onto this closed convex set. Projection is nonexpansive and leaves S fixed. Interior pointwise convergence holds on a countable compact exhaustion. The projected error is uniformly bounded on the finite-volume domain. Dominated convergence proves L² convergence. This is not a claim of uniform convergence of derivative estimates at the reflecting boundary.

## 6. What remains for the original target

The theorem is a deterministic reconstruction step conditional on convergence of empirical joint-density and invariant-density estimates in the specified norms. It does not assume individual eigenpair consistency, and it proves the previously unverified spectral-jet identification rather than hiding it in a rank hypothesis. The number of retained empirical positive eigenpairs is the finite rank of the chosen empirical kernel and may grow with sample size.

The next necessary task is to construct q_n and μ_n from the actual stationary low-frequency Markov observations, choose deterministic smoothing/sieve schedules, prove these strong local kernel and density convergences, and check their finite-rank symmetry/positivity requirements. Additional observational sensor noise is outside the source model. Generic least-squares continuity without that statistical step is not a full source solution.

The hypotheses used here are smooth bounded-domain, smooth anisotropic uniformly elliptic S and smooth positive μ. They are explicit restrictions on regularity, not inferred from the source's unspecified numerical estimator. No optimal rate, universal finite-K guarantee or historical novelty claim is made.

Substantive author count1/5. Original unresolved. Completion estimate30%, subjective and uncalibrated. The next turn should address empirical operator estimation, not restate the conditional theorem as complete.
