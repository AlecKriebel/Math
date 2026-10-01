# Turn 4: uniform scalar control at X log X and geometric joint-law information

**Substantive author turn4/5, scoped partial, unreviewed.** The exact X log X path-space endpoint remains unresolved. This turn proves an exact-endpoint estimate uniform in the parameter, with the order of supremum and expectation made explicit, and develops a certified bivariate continued fraction for the source's geometric coupling. It also excludes a natural independent-increment candidate that matches all one-dimensional laws and covariances. These are not a full simple description of the three source processes.

## 1. Uniform expected temporal maxima under the exact endpoint

Use the setup and generation-dependent truncation of Turn3. Fix[a,b] contained in I with1<a<b, let Y=X(b), and assume

    E[Y log(e+Y)]<infinity.

For n>=1 define deterministic quantities

    B_n=E[Y min(Y/a^n,1)],
    b_n=E[Y 1_(Y>a^n)],
    R_n=2 sqrt(B_n/[a(a-1)])+(2/a) sum_(k>=n)b_k.                 (1.1)

Then R_n tends to zero, and the following bound holds for the actual coupled process:

    sup_(lambda in[a,b]) E sup_(m>=n)
       |W_m(lambda)-W_n(lambda)| <=R_n.                         (1.2)

The parameter supremum is **outside** the expectation. Equation(1.2) does not assert an expected maximum over all parameters, and those two operations cannot be interchanged.

In particular,

    sup_lambda E|W_n(lambda)-W(lambda)| <=R_n ->0,               (1.3)

where W denotes the scalar martingale limits with the measurable convention from Turn1. This is a uniform scalar L1 statement, not a claim of convergence in the supremum-norm topology.

### Proof of the temporal estimate

Fix lambda. Write the exact increment decomposition from Turn3 as

    W_(k+1)(lambda)-W_k(lambda)=D_k(lambda)+C_k(lambda),

where D_k is the centered contribution of X_(k,i)(lambda) truncated by Y_(k,i)<=lambda^k, and C_k is the centered discarded contribution. For the fixed parameter, D_k is an F_(k+1)-measurable square-integrable martingale difference. Conditional independence of the new offspring copies gives

    E D_k(lambda)²
       <=lambda^(-k-2) E[Y² 1_(Y<=lambda^k)].                    (1.4)

The population enters only through E Z_k(lambda)=lambda^k. No variance of the untruncated offspring or population is assumed.

For any y>=0, sum the geometric series beginning at the first integer k>=n with lambda^k>=y. It gives

    sum_(k>=n) lambda^(-k) y² 1_(y<=lambda^k)
       <=[a/(a-1)] min(y²/a^n,y).                              (1.5)

To check the bound when y lies between a^n and lambda^n, observe that y²/lambda^n<=y; thus replacing lambda by a in the final minimum does not reverse the bound. From(1.4)–(1.5),

    sum_(k>=n) E D_k(lambda)² <= B_n/[a(a-1)].                   (1.6)

For finite M, orthogonality of martingale differences and Doob's L2 maximal inequality bound the expected maximum of the partial sum from k=n through M by twice the square root of(1.6). Monotone convergence extends the maximum to all finite M simultaneously. For the discarded part, centering and the triangle inequality give

    E|C_k(lambda)|
       <=(2/lambda) E[X(lambda)1_(Y>lambda^k)]
       <=(2/a)b_k.                                             (1.7)

Summing(1.7) and combining it with the martingale estimate proves(1.2), with constants independent of lambda. Integrability of Y implies B_n->0 by domination. Turn3's tail-sum bound shows sum b_k<infinity under X log X. Hence R_n->0. Scalar almost-sure martingale convergence and Fatou then give(1.3).

This argument only applies Doob to a single fixed parameter's generation filtration. It does not assume a martingale filtration in the parameter or independent parameter increments. Nor does it choose the parameter after seeing future offspring.

## 2. Consequences: uniform integrability and first-moment equicontinuity

### Uniform integrability

The family

    {W_n(lambda): n>=0, lambda in[a,b]}

is uniformly integrable. Indeed, for n>=N, (1.2) gives E|W_n(lambda)-W_N(lambda)|<=R_N uniformly. For a fixed N,

    0<=W_N(lambda)<=a^(-N)Z_N(b),

and this dominating variable is integrable. The finitely many earlier generations have analogous integrable envelopes. The elementary inequality, for x,y>=0,

    x 1_(x>2K) <=2|x-y|+2y 1_(y>K)

first lets K tend to infinity at fixed N, and then lets N tend to infinity. The same argument and(1.3) show uniform integrability of the family of limits{W(lambda)} on the compact interval.

### Equicontinuity in first moment

For a fixed generation N and a<=lambda<mu<=b, monotonicity of Z_N and its known mean imply

    E|W_N(mu)-W_N(lambda)|
       <=2[1-(lambda/mu)^N]
       <=2N(mu-lambda)/a.                                     (2.1)

This follows by adding and subtracting mu^(-N)Z_N(lambda). The two nonnegative expectation bounds are each 1-(lambda/mu)^N; no independence between parameter values is used.

Combining(1.2) with(2.1), including the finitely many n<N separately, gives

    sup_(n>=0) E|W_n(mu)-W_n(lambda)|
       <=2R_N+2N(mu-lambda)/a,                                (2.2)
    E|W(mu)-W(lambda)|
       <=2R_N+2N(mu-lambda)/a.                                (2.3)

First choose N large and then make mu-lambda small. Thus both the prelimit family and the scalar limit family are uniformly continuous on compacts in this first-moment sense. In particular the limit family is stochastically continuous at every deterministic parameter.

The distinction from path-space tightness is essential. A supremum over a random narrow parameter interval is not controlled by(2.2). The continuous-martingale countercontrol in Turn3 can also have uniformly small pointwise temporal tails and first-moment equicontinuity while its supremum diverges. It is still not a branching-process counterexample. A proof of J1 tightness must use additional branching-specific structure.

## 3. The exact geometric coupling

This section uses exactly the source's geometric process, not another monotone coupling of its marginal distributions. For1<lambda<mu, put K=X(lambda) and J=X(mu)-X(lambda). Section2.2 of Mailler–Marckert gives independence of K and J, with

    E z^K=1/[1+lambda(1-z)],
    E z^J=[1+lambda(1-z)]/[1+mu(1-z)].                         (3.1)

The same independent-increment statement holds along any finite increasing parameter list. In particular E K=lambda and E J=mu-lambda. All moments are finite. Turn2 applies to this process and gives a càdlàg limit, but the marginal law below was already identified in the source and is credited to it.

At random inverse-Bernoulli threshold times, take the right-continuous version required by the source's HReg assumption. In the displayed inverse-threshold construction this is obtained by using a strict success comparison after the decreasing change of parameter. This changes no finite-dimensional law at deterministic parameters, since the uniforms have no atoms. The formulas here concern that same geometric coupling, with its càdlàg convention specified, rather than a different coupling chosen from the marginal laws.

Let U=W(lambda), V=W(mu), and let

    phi_r(x)=E exp(-xW(r))=(r-1+x)/(r-1+r x),   x>=0.            (3.2)

Equivalently W(r) has mass1/r at zero and, on survival, is exponential of rate(r-1)/r. The standard root decomposition uses common independent descendant pairs(U_i,V_i):

    (U,V) =_law (lambda^(-1) sum_(i<=K)U_i,
                 mu^(-1) sum_(i<=K+J)V_i).                    (3.3)

The K common pairs must not be replaced by independent scalar descendants in the two coordinates.

## 4. Exact mixed moments and an excluded candidate

The source marginal law yields

    m20=E U²=2lambda/(lambda-1),
    m02=E V²=2mu/(mu-1).

Expanding(3.3) and using geometric factorial moments gives

    m11=E UV=(lambda+mu)/(mu-1).                               (4.1)

All required mixed moments exist, for example by Hölder and the finite third marginal moments. For m21=E U²V, the terms in the common K-child sum divide into: one repeated index; two distinct indices with the U² factor; two distinct indices with V paired with one of the U factors; and three distinct indices. The extra J children have mean mu-lambda and are independent. Thus

    (lambda²mu-lambda)m21
       =2lambda²(m20+2m11)+6lambda³
         +(mu-lambda)(lambda m20+2lambda²),

so

    m21 = 2lambda(2lambda²mu+lambda mu²-lambda-2mu)
           /[(lambda-1)(mu-1)(lambda mu-1)].                  (4.2)

Consider the tempting scaled process A(r)=(r-1)W(r). Its one-dimensional Laplace transform is

    E exp(-x A(r))=(1+x)/(1+r x).

There really exists a nondecreasing independent-increment process with these marginals: use a Poisson random measure in r>1 of intensity dr/r and, at a point r, an independent exponential jump of mean r. Its cumulative Laplace transform is

    exp(-integral_1^r x/(1+t x) dt)=(1+x)/(1+r x).

This candidate also matches the true covariance, since by(4.1)

    Cov(A(lambda),A(mu))=lambda²-1=Var(A(lambda)).

Nevertheless it is not the source limit process. Independent increments would force

    E U²V = 2lambda(2lambda+mu)/[(lambda-1)(mu-1)].              (4.3)

Subtracting(4.3) from(4.2) gives the strictly negative quantity

    2lambda(lambda-mu)
       /[(lambda-1)(mu-1)(lambda mu-1)].                        (4.4)

For lambda=2 and mu=3 the true moment is68/5, while the independent-increment candidate gives14. Therefore even matching every marginal and the full covariance kernel does not give the source process law. This rules out this specific subordinator description; it does not rule out every Markov representation or characterize the full process.

## 5. Certified bivariate continued fraction

There is a concrete convergent representation of the true bivariate Laplace transform

    F(s,t)=E exp(-sU-tV),    s,t>=0.

Put

    C(t)=phi_mu(t)[1+lambda(1-phi_mu(t/mu))],
    M_t(z)=C(t)/(1+lambda-lambda z).                            (5.1)

Equations(3.1)–(3.3) imply exactly

    F(s,t)=M_t(F(s/lambda,t/mu)).                               (5.2)

The factor C(t) is in(0,1], because it is

    [1+lambda(1-phi_mu(t/mu))]
       /[1+mu(1-phi_mu(t/mu))].

Consequently M_t maps[0,1] into[0,1], is increasing, and has derivative at most lambda on that interval.

Choose n sufficiently large that s/lambda^n+t/mu^n<=1, and define a rational lower terminal value

    z_n=1-s/lambda^n-t/mu^n.

Apply, from the innermost to the outermost,

    F_n^lower(s,t)
       =M_t composed with M_(t/mu) composed with ...
          composed with M_(t/mu^(n-1)), evaluated at z_n.         (5.3)

Then

    F_n^lower(s,t) <= F(s,t) <= F_n^lower(s,t)+E_n,              (5.4)
    E_n=(lambda^n/2)[s²lambda^(-2n)m20
                    +2st(lambda mu)^(-n)m11
                    +t²mu^(-2n)m02].                          (5.5)

To prove this, use 0<=exp(-x)-1+x<=x²/2 for x>=0 at the true terminal random variable sU/lambda^n+tV/mu^n. The mean-one condition gives the lower terminal z_n, and the known second moments give its error. Propagation through the n increasing maps preserves the lower bound and amplifies the error by at most lambda^n. This proves(5.4)–(5.5), whose width decays geometrically since mu>lambda>1.

For rational lambda,mu,s,t the endpoints in(5.4) are exactly computable rationals. The n=8 certificate at lambda=2,mu=3,s=t=1 already places the actual transform strictly above1/2, the value for the subordinator candidate. The checker uses exact fractions, not decimal approximations, to establish this separation.

The boundary value is important. Replacing the terminal transform by the constant1 would discard its first-order mean and can select the wrong fixed point; the derivative bound grows like lambda^n. The linear mean-corrected terminal is what makes the error in(5.5) vanish.

This continued fraction is a useful explicit bivariate law representation with a rigorous error certificate. It does not supply a simple classical representation of the entire geometric process, and it does not settle the binary and Poisson process questions.

## 6. Remaining work and controls

The exact endpoint now has uniform scalar L1 convergence, uniform integrability, first-moment equicontinuity, vanishing active-family maxima and almost-sure square-summable uniform increments. The missing implication is genuinely functional: tightness of the random paths, or a valid counterexample within the original offspring coupling. No exchange of the parameter supremum with expectation is warranted.

The geometric computations preserve the source's coupling and distinguish a proved bivariate representation from the still-missing simple full-process descriptions. The original bundle remains unresolved after4/5 substantive turns.

The finite checker verifies the scalar geometric-tail bounds, exact temporal orthogonality controls, first-moment normalization, geometric factorial expansions, mixed-moment discrepancy and rational continued-fraction enclosure arithmetic. The infinite martingale and convergence statements are established analytically above. Existing source PDFs/access qualifications and classical Kesten–Stigum/Doob credit remain unchanged; no novelty claim is made.
