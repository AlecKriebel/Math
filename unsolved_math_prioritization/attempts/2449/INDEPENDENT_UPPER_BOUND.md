# Independent upper bound for Erdős Problem 1038

## Conclusion and scope

Let P be the nonconstant monic real polynomials all of whose roots, including multiplicities, lie in [-1,1]. An independent exact-rational computation, combined with the argument below, establishes

    inf_{f in P} measure{x in R : |f(x)| < 1}
      <= Lambda(q_c)
      < 1.83443047576266171109075363512901884952989750747
      < 1.834430475762662,

where q_c is the exact rational number

    0.02571553686652745032257637166391965344.

This independently reproduces an upper bound from the one-cut family in Shouqiao Wang's proposed resolution, which explicitly attributes that family to Terence Tao. This is an audit and reproduction, with no novelty claim. The parameter q_c is not asserted to be stationary or optimal. Nothing here proves the matching lower bound, uniqueness of the minimum, or nonattainment of the global infimum.

Sources: [Wang's proposed resolution](https://multiscalar.ai/results/erdos-1038/paper.pdf), Sections 6 and 9; [Tao's note](https://terrytao.wordpress.com/wp-content/uploads/2025/12/erdos-1038-2.pdf), Section 4. The proof and independently developed exact-arithmetic checks do not use the source author's software. The complete mathematical formulas and rational witnesses are included here; executable checker code is outside the report.

## Parameters and the exact certificate

Set q=q_c and

    H = 2q/(1+q)^2,
    s = (1-q)/(1+q),
    a = 2s^2-1,
    A = log(H)/log(q).

The independent checker verifies 0<q<1 and q^2-6q+1>0, hence q<3-2sqrt(2). It also encloses A by exact rational logarithm bounds and verifies 0<A<s<1. Thus 0<a<1.

For u>1, u != 1/q, put

    F(u) = A log((u-q)/|1-qu|)-log(u),
    W(u) = u+1/u.

There are unique roots u_plus in (1,1/q) other than the identically present root 1, and u_minus in (1/q,infinity). Indeed, on (1,1/q),

    F'(u) = [qu^2-Bu+q]/[u(u-q)(1-qu)],
    B = 1+q^2-A(1-q^2).

Since A<s, B>2q. The numerator is negative at 1 and positive at 1/q, and its roots are positive and reciprocal. Exactly one critical point lies in (1,1/q). Consequently F first decreases from F(1)=0, then increases to infinity and has one nontrivial zero there. On u>1/q,

    F'(u) = -A(1-q^2)/[(u-q)(qu-1)]-1/u < 0.

The endpoint limits are infinity and minus infinity, giving precisely one root. The two roots are simple.

The exact checker encloses these roots between rational endpoints and proves the endpoint sign changes with Fraction arithmetic. The appendix below records every rational root endpoint, exact arithmetic rule, and acceptance inequality needed for independent arithmetic rederivation. For readability the root centers are approximately

    u_plus  = 17.861896208523519533866067426369570685214609183110...
    u_minus = 55.425602286574753476940972526137943995675399324369...

Each proposed interval has radius exactly 10^(-45), centered at a rational decimal. Floating-point calculations only propose the intervals: their acceptance relies on the exact sign checks and the uniqueness argument just given.

Since W is strictly increasing for u>1, if these root intervals are [p_l,p_h] and [m_l,m_h], then

    H(W(m_l)-W(p_h)) <= Lambda(q) <= H(W(m_h)-W(p_l)).

The exact rational enclosure, displayed here with outward decimal rounding, is

    1.8344304757626617110907536351247861430208808819614782075623140890
      <= Lambda(q) <=
    1.8344304757626617110907536351247861430208808821566781865818401394.

Both comparisons with the two upper bounds in the conclusion are performed on the underlying rational endpoints, rather than these displayed decimals.

### Why the logarithm bounds are rigorous

For rational x>0, choose an integer k so that x=2^k y with 1<=y<2. Set z=(y-1)/(y+1), so 0<=z<1/3. For N=90,

    S_N(y) = 2 sum_{j=0}^{N-1} z^(2j+1)/(2j+1),
    0 <= log(y)-S_N(y)
       <= 2 z^(2N+1)/[(2N+1)(1-z^2)].

The same formula with z=1/3 bounds log(2). Multiplication of its interval by the signed integer k and interval addition enclose log(x). All endpoints are rational. The remainder bound follows by replacing each omitted denominator by 2N+1 and summing a geometric series. The identity follows by integrating 2/(1-z^2) from 0 to z.

Interval products use all four endpoint products. Division is performed only after checking that the denominator interval excludes zero. At each proposed root endpoint the checker evaluates

    F(u) = [log(H) log((u-q)/|1-qu|)-log(q)log(u)]/log(q)

in these exact rational intervals. The plus endpoint signs are strictly negative then strictly positive; the minus signs are strictly positive then strictly negative. Their magnitudes are about 3e-47 and 5e-47 respectively. The exact log remainder is much smaller. The acceptance predicates never depend on ordinary floating-point signs.

## A probability measure realizing the candidate interval

Let omega be the arcsine probability on [a,1]:

    d omega(t) = dt/[pi sqrt((t-a)(1-t))].

For any A' in [A,s), define

    d mu_{A'}(t) = A' d delta_{-1}(t)
                  + [1-2A's/(t+1)] d omega(t).

This is a nonnegative probability. The density factor is increasing in t and has its minimum 1-A'/s>0 at t=a. Substitution t=(a+1)/2+(1-a)cos(theta)/2 gives

    integral d omega = 1,
    integral d omega(t)/(t+1) = 1/[sqrt(2(a+1))] = 1/(2s).

Thus the continuous mass is 1-A', and the atom supplies A'. All support lies in [-1,1].

We record explicitly the logarithmic potential identities needed below. In the shifted coordinate d=t+1, write

    c=1+s^2, r=1-s^2=2H,
    d(theta)=c-r cos(theta), 0<=theta<=pi,
    D0=H/q=2/(1+q)^2.

Then d(theta)=D0(1-2q cos(theta)+q^2), and the measure

    d omega_0(d) = (2s/d) d omega(d-1)

has angular density P_q(theta)/pi, where

    P_q(theta)=(1-q^2)/(1-2q cos(theta)+q^2)
             =1+2 sum_{n>=1} q^n cos(n theta).

For x_sh=c-H(u+u^(-1)), u>1,

    |x_sh-d(theta)|=Hu(1-2u^(-1)cos(theta)+u^(-2)).

Expansion of log(1-2v cos(theta)+v^2)=-2 sum_{n>=1} v^n cos(n theta)/n, first for v<1, and cosine orthogonality give

    integral log|x_sh-d| d omega = log(Hu),
    integral log|x_sh-d| d omega_0 = log(Hu)+2log(1-q/u).

On the conductor, the chord identity

    |d(theta)-d(phi)|/H
       = |exp(i theta)-exp(i phi)| |exp(i theta)-exp(-i phi)|

gives, by the same Fourier calculation with the integrable logarithmic kernel (or its Abel regularizations),

    integral log|d(theta)-d| d omega = log H,
    integral log|d(theta)-d| d omega_0 = log(d(theta))+log q.

The passage to the logarithmic kernel is valid in L1; multiplying by the bounded Poisson density preserves convergence. This also proves continuity of these potentials at the conductor endpoints.

Writing V_{A'}(x)=integral log|x-t| d mu_{A'}(t), the platform value on [a,1] is therefore

    V_{A'}(x)=log H-A' log q.

At A'=A it vanishes, and for A'>A it is strictly positive because log q<0. At A'=A the exterior formula simplifies, using

    x_sh = D0 (u-q)(1-qu)/u,
    log H=A log q,

to

    V_A(x_sh-1)=log u-Alog((u-q)/|1-qu|)=-F(u).

Thus the two crossings associated with u_minus and u_plus are

    alpha = s^2-H W(u_minus),
    beta  = s^2-H W(u_plus),

and beta-alpha=Lambda(q).

## Zero count and positive-platform recovery

The following verifies that no additional negative intervals have been omitted. Let

    S(z)=sqrt((z-a)(z-1)), chosen so S(z)~z at infinity.

The elementary arcsine transform is integral (z-t)^(-1) d omega(t)=1/S(z). It follows by the substitution above and then tan(theta/2); the sign is fixed by its asymptotic 1/z. Partial fractions give the Cauchy transform of mu_{A'}. In particular, for real x off the support and the atom, differentiation of the real logarithmic potential gives

    V'_{A'}(x) = [1-2A's/(x+1)]/S(x).

For real x<a, S(x)<0. On (-infinity,-1), the numerator is positive, so V'_{A'}<0; the potential goes from infinity to minus infinity and has exactly one simple zero. On (-1,a), it increases until x0=2A's-1 and decreases afterwards, with x0<a because A'<s. Its left limit is minus infinity. If A'>A, its limit at a is the strictly positive platform value, so it has exactly one zero on its increasing portion. If A'=A, the decrease to platform zero implies the potential is strictly positive on (x0,a), and again there is one simple crossing on the increasing portion. On (1,infinity), its derivative is positive and its value starts at the nonnegative platform, hence there is no additional negative interval. On [a,1] the potential is the platform itself. Therefore every negative set E_{mu_{A'}} is the single interval between the two crossings.

For A'>A, its zero set has exactly two points. At A'=A, the interval endpoints are the alpha and beta found above; their simplicity also follows from the signs of F' and dx_sh/du=-H(1-u^(-2)). The potentials vary jointly in C1 near these two crossings as A' tends to A, since those neighborhoods avoid the support. The implicit-function theorem therefore yields

    measure(E_{mu_{A'}}) -> Lambda(q) as A' decreases to A.

For example, take A_j=A+(s-A)/(j+1), j>=1. Every A_j lies strictly between A and s, so all the preceding positivity, probability, support, platform, and zero-count conditions hold.

## Passage to admissible finite polynomials

Fix j. Approximate mu_{A_j} weakly by equal empirical probabilities

    nu_{j,n}=(1/n) sum_{l=1}^n delta_{t_{j,n,l}},
    t_{j,n,l} in [-1,1].

One explicit choice is t_{j,n,l}=T_j((l-1/2)/n), where T_j is the generalized quantile of mu_{A_j}. For a continuous test function phi, phi composed with T_j is bounded and has discontinuities only at the countably many discontinuities of the monotone function T_j. Its midpoint Riemann sums converge to its integral, proving weak convergence. In particular, the possibly irrational atom mass A_j causes no difficulty: the approximating masses are precisely integer multiples of 1/n, and repeated roots are allowed.

Weak convergence of probabilities on [-1,1] implies L1 convergence of their logarithmic potentials on B=(-2,2). Here is a direct proof. Truncate the kernel below at -M. The truncated kernel is bounded and continuous in t for each fixed x. Weak convergence and dominated convergence on B give L1 convergence of the truncated potentials. Uniformly in t,

    integral_B [max(log|x-t|,-M)-log|x-t|] dx <= 2 exp(-M).

This follows by integrating -M-log|y| over |y|<exp(-M). Integrating the inequality against any probability gives the same error bound, so taking n to infinity and then M to infinity proves L1 convergence of the untruncated potentials.

If v_n tends to v in measure on B and the zero set of v has measure zero, then their negative-set indicators tend in L1. For every delta>0 their symmetric difference is contained, up to null sets, in

    {|v|<=delta} union {|v_n-v|>=delta}.

Take n to infinity and then delta to zero. Apply this to the positive-platform potential V_{A_j}, whose zero set has two points. Every negative set here is contained in (-2,2), since |x-t|>=1 for |x|>=2 and t in [-1,1]. Thus

    measure(E_{nu_{j,n}}) -> measure(E_{mu_{A_j}}).

The polynomial

    f_{j,n}(x)=product_{l=1}^n (x-t_{j,n,l})

is monic, nonconstant, real, and has all roots in [-1,1]. Its root potential is (1/n)log|f_{j,n}|, so its |f|<1 set is exactly E_{nu_{j,n}}.

For each j choose n_j so that the length error is below 1/j. The diagonal sequence f_{j,n_j} has lengths tending to Lambda(q). Consequently the polynomial infimum is at most Lambda(q). Together with the exact rational upper enclosure, this proves every strict upper bound asserted in the conclusion. In particular some admissible finite polynomials have sublevel-set length below 1.834430475762662. No assertion about the degree required is made.

## Verification record

The independently developed exact-rational checker was executed during the audit and replayed during report preparation. Its source code and raw output file are outside this report. The final replay uses only Python's standard library and explicit exception checks, so every proof gate remains active under normal Python, -O, and -OO. Installed mpmath was used in the initial independent run only to propose rational root boxes. The recorded rational centers are now included in the checker; exact sign tests make correctness independent of how those proposals were obtained. No code from the source author's numerical_verifier.py or Lean project was imported or executed.

The exact arithmetic checks also verify the rational constants used in the source's elementary small-k estimate; the appendix lists their positive rational margins. Those arithmetic checks are not substitutes for either global numerical certificate.

The final checker was replayed under normal Python, -O, and -OO. All three exited successfully with byte-identical output and the unchanged exact-result SHA256 b8fb956611313159f8e03f87fef65e0c8cadeb03f2117a9ed7cc4b159b6885bf. CHECK_SUMMARY.json records the aggregate replay results and implementation-only change; no exact input, acceptance inequality, or mathematical output changed. The reports are not a self-contained executable replay package, and a result hash is an integrity receipt rather than a mathematical proof. The rational formulas and witnesses below permit an independent implementation or direct exact arithmetic.

## Appendix: exact rational witnesses and rederivation instructions

Every terminating decimal in this appendix denotes an exact rational, not a floating-point input. The following witnesses are authored mathematical content, rather than a copied source dataset. Their purpose is to let a reader reconstruct the finite arithmetic from the formulas in this proof without receiving the checker implementation.

The exact parameter is

    q = 80361052707898282258051161449748917 /
        3125000000000000000000000000000000000.

Use H=2q/(1+q)^2, s=(1-q)/(1+q), and a=2s^2-1 exactly. In particular,

    s = 3044638947292101717741948838550251083 /
        3205361052707898282258051161449748917.

The two root boxes have these exact endpoints:

    plus_lower = 17861896208523519533866067426369570685214609182110155278092269729/1000000000000000000000000000000000000000000000000000000000000000
    plus_upper = 17861896208523519533866067426369570685214609184110155278092269729/1000000000000000000000000000000000000000000000000000000000000000

    minus_lower = 11085120457314950695388194505227588799135079864673862940404965203/200000000000000000000000000000000000000000000000000000000000000
    minus_upper = 11085120457314950695388194505227588799135079865073862940404965203/200000000000000000000000000000000000000000000000000000000000000

Write p_lower=plus_lower, p_upper=plus_upper, m_lower=minus_lower and m_upper=minus_upper. Their exact ordering is 1<p_lower<p_upper<1/q<m_lower<m_upper. Each box is a rational center plus or minus 1/10^45. No claim about a root is assumed in supplying these boxes: the signs below, together with the analytic uniqueness proof, establish that each contains the corresponding root.

For reproducible interval arithmetic, addition is endpointwise, negation reverses and negates endpoints, multiplication takes the minimum and maximum of the four products, and division by [b_l,b_h] multiplies by [1/b_h,1/b_l] after first proving 0 is outside that interval. For any rational x>0, choose the unique integer k with y=x/2^k in [1,2). With z=(y-1)/(y+1), define

    S(y) = 2 sum_{j=0}^{89} z^(2j+1)/(2j+1),
    R(y) = 2 z^181/[181(1-z^2)],
    J(y) = [S(y), S(y)+R(y)].

Use the same formula at y=2 for J(2), and put

    Log(x) = J(y) + [k,k] J(2).

This is a finite exact rational enclosure of log(x), including for negative k. The positive geometric-series remainder and its proof were given above. Form A_box=Log(H)/Log(q), verifying the divisor excludes zero. It lies inside the following outward decimal rational interval:

    [0.82452172925252037928523918298801833420331081464128120149456482575,
     0.82452172925252037928523918298801833420331081464128120149456482576].

Check 0<q<1, q^2-6q+1>0, 0<lower(A_box)<=upper(A_box)<s<1. These are rational comparisons. At any of the four rational root endpoints u, compute

    r = (u-q)/|1-qu|,
    F_box(u) = [Log(H) Log(r) - Log(q) Log(u)] / Log(q).

The resulting enclosures are contained in the following outward decimal rational intervals, displayed with their signs explicitly:

    F(plus_lower) in [-2.9458450844813194314710977627127973324621743464247197553363565035E-47,
        -2.9458450844813194314710977627127973324620784878129844491586479521E-47]
    F(plus_upper) in [2.9458450844813194309901879919864157365507266468006540087033357257E-47,
        2.9458450844813194309901879919864157365508225054123893148810442772E-47]
    F(minus_lower) in [5.3013477778992323153735287883735920772850413826767168716221396156E-47,
        5.3013477778992323153735287883735920772851719500441432923229665220E-47]
    F(minus_upper) in [-5.3013477778992323182982929009713663552083314182222071948142909866E-47,
        -5.3013477778992323182982929009713663552082008508547807741134640802E-47]

In particular upper(F_box(p_lower))<0<lower(F_box(p_upper)) and upper(F_box(m_upper))<0<lower(F_box(m_lower)). Decimal displays are outward bounds on exact rational enclosures; their signs do not arise from rounded floating-point evaluation.

Define, with exact rational operations,

    L_lower = H(m_lower+1/m_lower-p_upper-1/p_upper),
    L_upper = H(m_upper+1/m_upper-p_lower-1/p_lower),
    B = 1.83443047576266171109075363512901884952989750747,
    C = 1.834430475762662.

The exact acceptance inequality is L_upper<B<C. The outward decimal enclosure for [L_lower,L_upper] is the one printed in the main proof. This proves the strict upper bound, and only the upper comparator B is used. No comparison with the source's LSTAR_LO, global minimization, or stationary-point assertion is being inferred.

For the supplementary elementary-range arithmetic, put K=29/20 and z=87/392. The exact positive margins are

    1+3/8+(3/8)^2/2+(3/8)^3/6-K = 21/5120,
    (49/20)(1-z+z^2/2-z^3/6)-49/25 = 522631/245862400,
    263/240-K(1123/1620)-9/100 = 11/16200,
    2-(4/3)^2 = 2/9.

These auxiliary finite comparisons support the elementary-range audit. They do not provide either of the two unresolved global computational certificates. The strict upper theorem additionally uses the complete measure construction, zero count, positive-platform perturbation, and finite-polynomial recovery established above; the finite arithmetic alone does not replace those analytic arguments.
