# Turn 2: conditional renormalization of the excursion-layer width functional

**Substantive author turn 2 of 5. Original flat-disk area limit unresolved.** The source's conjectural continuum boundary suggests a layer-width area functional. This turn rigorously constructs its Gaussian fluctuation part, with a uniform small-component bound. The finite excursion-to-disk area identity and the divergent conditional-mean term are still missing; the theorem below is not silently substituted for the original polygon theorem.

## 1. A measurable layer functional

Let e:[0,1]→[0,infinity) be continuous with e(0)=e(1)=0, and write H=sup e. At level y>0 let I_y be the countable family of connected components I=(g,d) of {t:e(t)>y}. Put s(I)=d−g. Define the sigma-finite measure nu_e on such level/component pairs by integrating counting measure over y. Components can be enumerated measurably by their first rational point in a fixed enumeration, so all integrals below are ordinary measurable integrals. The elementary layer-cake identity is

    integral s(I) nu_e(dI)=integral_0^1 e(t)dt=:T≤H.         (1)

The intervals at different levels form a laminar family: any two are nested or disjoint. For a fixed component I, there is at most one component containing it at each lower level. Consequently its set of ancestors has nu_e-measure at most H.

Let X be a standard real Brownian bridge on [0,1], independent of e if e is random. For epsilon>0 set

    W_epsilon(e,X)=integral_(s(I)>epsilon)
                          |X(d)−X(g)| nu_e(dI).             (2)

For each y there are at most 1/epsilon such disjoint components. Thus the cutoff measure is at most H/epsilon, and W_epsilon is a well-defined nonnegative random variable bounded by (2H/epsilon)sup|X|. In particular it has finite moments of order two for each fixed e and epsilon.

Conditionally on e, the increment X(d)−X(g) is centered Gaussian with variance s(1−s). Therefore its exact conditional mean is

    M_epsilon(e)=sqrt(2/pi) integral_(s(I)>epsilon)
                                  sqrt(s(I)(1−s(I))) nu_e(dI). (3)

Write Z_epsilon=W_epsilon−M_epsilon. No replacement of the random mean (3) by a deterministic logarithm has been justified at this point.

## 2. A Gaussian covariance estimate

If U,V are centered jointly Gaussian real variables, then

    |Cov(|U|,|V|)|≤|Cov(U,V)|.                              (4)

One proof is Gaussian interpolation. After scaling to unit variances and writing rho for their correlation, let F(rho)=E[f(U)g(V)] for smooth approximations f,g to absolute value with derivatives bounded by one. Differentiating the bivariate Gaussian density and integrating by parts gives F'(rho)=E[f'(U)g'(V)], so |F'(rho)|≤1. Subtract F(0), integrate from zero to rho, then remove the smooth approximation by dominated convergence. Scaling back proves (4). Degenerate variances follow by continuity.

For Brownian-bridge increments over intervals I,J, the exact covariance is

    c(I,J)=|I intersect J|−s(I)s(J).                        (5)

If I is contained in J with lengths s≤t, this is s(1−t), whose absolute value is at most s. If they are disjoint, it is −st. These two simple bounds suffice; independence of different component widths is not assumed and would be false for a bridge.

## 3. Uniform L2 control of the small-component tail

For epsilon>0 define

    T_epsilon(e)=integral_(s(I)≤epsilon) s(I) nu_e(dI).

By (1), T_epsilon≤T and T_epsilon→0 as epsilon decreases to zero, by dominated convergence. For 0<delta<epsilon, the difference Z_delta−Z_epsilon is the integral of the centered widths over delta<s(I)≤epsilon. Expanding its conditional variance and applying (4)–(5), split interval pairs into nested and disjoint ones.

For nested pairs, assign the smaller interval I first. Its contribution is bounded by s(I) times the total measure of its ancestors, which is at most H. The two possible orders cost at most a factor of two. For disjoint pairs the bound is s(I)s(J), so the double integral is at most T_epsilon². Hence

    E_X[(Z_delta−Z_epsilon)² | e]
                    ≤2H T_epsilon+T_epsilon².              (6)

This is an upper bound; counting a diagonal twice would only enlarge it. The cutoff integrals have finite measure, so the covariance/Fubini calculation is justified by their finite second moments. The resulting bound is uniform in the lower cutoff delta.

Thus Z_epsilon is Cauchy in L2 of the bridge X for every fixed continuous e. It has a mean-zero limit Z(e,X), and

    E_X[(Z−Z_epsilon)² | e]≤2H T_epsilon+T_epsilon²,
    E_X[Z² | e]≤2HT+T²≤3H².                                (7)

The arbitrary-cutoff limit, rather than only a subsequence, follows from the uniform Cauchy estimate. This constructs the Gaussian fluctuation component of (2) completely.

## 4. A deterministic modulus-of-continuity bound

Let

    omega_e(epsilon)=sup{|e(t)−e(u)|:|t−u|≤epsilon}.

For t in a component I=(g,d) at level y with length at most epsilon, continuity gives e(g)=y and |t−g|≤epsilon. Thus e(t)−y≤omega_e(epsilon). For each fixed t the levels at which it belongs to such a small component therefore occupy a subset of [max(0,e(t)−omega_e(epsilon)),e(t)], of length at most omega_e(epsilon). Tonelli's theorem gives the stronger bound

    T_epsilon(e)≤omega_e(epsilon).                          (8)

Combining (7)–(8),

    E_X[(Z−Z_epsilon)² | e]
        ≤2H omega_e(epsilon)+omega_e(epsilon)².              (9)

For a Holder-continuous excursion of exponent gamma and constant C_e, this gives a conditional mean-square error at most
2H C_e epsilon^gamma+C_e² epsilon^(2gamma). In particular there is no conditional Gaussian variance divergence hidden at small excursion components.

There is also a useful stability form. If e_j→e uniformly, then

    H_j≤H+||e_j−e||_infinity,
    omega_(e_j)(epsilon)≤omega_e(epsilon)+2||e_j−e||_infinity.

The right-hand side of (9) consequently gives uniform small-component centered-tail control along such a convergent sequence. This by itself does not prove convergence of the large-component integrals when the excursion changes; that separate continuity issue must be addressed before transferring a discrete approximation.

## 5. Random excursions and the Brownian case

For any random continuous e independent of X with E[H²]<infinity, integrating (7)–(9) and using domination by 3H² proves joint L2 convergence and E[Z²]≤3E[H²]. If only H<infinity almost surely is known, the same limit can be constructed by localizing to H≤R, where the preceding argument is L2; the consistent limits yield convergence in probability as R tends to infinity.

For a standard Brownian excursion, E[H²]<infinity follows, for example, from its classical representation as the norm of three independent Brownian bridges. This representation is recorded in S. Janson, *Brownian excursion area, Wright's constants in graph enumeration, and other Brownian areas*, [arXiv:0704.2289](https://arxiv.org/abs/0704.2289), Section 2. Each bridge can be represented as B(t)=W(t)−tW(1). Doob's inequality gives E sup|W|²≤4 and hence E sup|B|²≤10. Therefore the crude bound E[H²]≤30 suffices, and the limit here has E[Z²]≤90. These coarse constants are only existence bounds, not estimates of the desired flat-disk limiting variance.

Thus for an independent Brownian excursion e and Brownian bridge X,

    W_epsilon(e,X)−E[W_epsilon(e,X)|e] -> Z(e,X) in L2.      (10)

The remaining conditional mean (3) can still fluctuate with e and diverge as epsilon tends to zero. Equation (10) does not state that subtraction of (log(1/epsilon))/(2pi) is enough.

## 6. Why this is a natural area functional, and the precise limitation

For continuous bounded-variation X and e, define the cutoff folded height

    Y_epsilon(t)=integral_0^(e(t))
          sign(X(d_y(t))−X(g_y(t)))
          1_{d_y(t)−g_y(t)>epsilon} dy,

where (g_y(t),d_y(t)) is the component containing t. The same component is used for all points of its interior at a fixed level. Below min_(s≤u≤t)e(u), the signs and cutoff indicators for s,t agree. It follows that

    |Y_epsilon(t)−Y_epsilon(s)|
          ≤e(s)+e(t)−2 min_(s≤u≤t)e(u).

Hence Y_epsilon is continuous. If e has bounded variation, summing over a partition also bounds the variation of Y_epsilon by that of e. Fubini for the finite signed measure dX then gives the exact identity

    integral_0^1 Y_epsilon dX
      =integral_(s(I)>epsilon) sign(X(d)−X(g))
                                      [X(d)−X(g)] nu_e(dI)
      =W_epsilon(e,X).                                     (11)

The closed curve (X,Y_epsilon), when X(0)=X(1), has signed area
one-half integral(X dY_epsilon−Y_epsilon dX)=−W_epsilon under this time orientation. Reversing orientation makes it positive. This sign is explicitly retained; no orientation convention is suppressed. It is an algebraic area identity, not a proof that every such curve admits a flat-disk filling.

For fixed e and epsilon, (2) obeys

    |W_epsilon(e,X)−W_epsilon(e,X')|
                 ≤(2H/epsilon)||X−X'||_infinity.            (12)

Thus polygonal approximation of X gives the same finite-cutoff functional. Brownian X is not of bounded variation, and (11) is not used as an unqualified pathwise Stokes integral in that case; (2) supplies the rigorous cutoff definition.

The source's continuum boundary formula has the same layer sign structure and is explicitly conjectural. No finite source bijection has been proved here to preserve (11) with the correct cutoff and deterministic correction. Therefore (10) is a theorem for a natural candidate continuum functional, not a completed theorem about A_n.

## 7. Next obstruction

Two steps remain before this route can prove the original claim: renormalize the random conditional mean (3) by the deterministic logarithm, and prove a quantitative transfer between finite uniform disks and this functional at a shrinking cutoff. Known additive-functionals results for Brownian trees may help with the first, but their centering and normalization have to be checked. Even a complete continuum theorem would not justify omitting the finite-model transfer.

**Original unresolved, author count 2/5.** The Gaussian width fluctuations are now controlled rigorously; the conditional mean and finite disk identification remain open. No original counterexample or novelty certification is claimed. Uncalibrated completion estimate: 25%.
