# Checked 2026 deduction from older endpoint-polynomial theory

This is an implication assembled in this audit, on 2026-10-17. It is not a claim that the full convex-body SOS theorem was printed in 1990, 2012, or 2018. No originality is assigned to the quadratic upper proxy, endpoint concentration, or shell summation.

## A. Precise older ingredient

Totik-Varga, *Non-symmetric fast decreasing polynomials and applications*, JMAA 394 (2012), 378-390, Theorem 2.1, printed p.379, allows endpoint parameter a=0. Taking its function psi(v)=sqrt(v) gives real polynomials P_m of degree at most m with

    P_m(0)=1,  |P_m(t)|<=2,
    |P_m(t)|<=C exp(-c (m sqrt(t))^(1/2)),  0<t<=1.        (A1)

Here C,c are positive and independent of m,t. The hypotheses hold: psi is increasing, psi(v)=sqrt(2) psi(v/2), and integral_1^infinity psi(v)/v^2 dv=2. Its complete printed proof, pp.380-381, was read; the proof imports a symmetric fast-decrease theorem from Ivanov-Totik (1990), whose full body was not obtained. The latter dependency is explicitly retained rather than represented as independently re-proved. The direct elementary alternative in Section D below bypasses it.

## B. The normalized endpoint moment lemma

Let mu be a finite nonzero positive measure supported on [0,1]. Let F(t)=mu([0,t]), extended by F(t)=mu([0,1]) for t>1. Suppose F(h)>0 for h>0 and there are fixed A>=1,D>=0 such that

    F(t)<=A(t/s)^D F(s),  0<s<=t.                       (B1)

Then there are real polynomials P_m of degree at most m such that

    integral t P_m(t)^2 dmu / integral P_m(t)^2 dmu
       <= B(A,D)/m^2,  m>=1.                           (B2)

Proof using (A1): the classical Markov inequality on [0,1] gives

    ||P_m'||_infinity <= 2m^2 ||P_m||_infinity <=4m^2.

Set h=1/(8m^2). Since P_m(0)=1, P_m(t)>=1/2 on [0,h]. Thus

    Z_m=integral P_m^2 dmu >=F(h)/4>0.                 (B3)

The numerator on [0,h] is at most 4hF(h). On each shell

    E_j=(2^j h,2^(j+1)h], j=0,1,...,

intersected with [0,1], (A1) and (B1) imply

    integral_Ej t P_m(t)^2 dmu
      <= C^2 2^(j+1)h exp(-2c (m sqrt(2^j h))^(1/2))
         * A 2^((j+1)D) F(h)
      = A C^2 2^(D+1) hF(h) 2^(j(D+1))
         * exp(-2c 8^(-1/4) 2^(j/4)).                 (B4)

The nonnegative series in j converges for every fixed D: its successive-term ratio tends to zero. Hence numerator <=B_0(A,D) hF(h). Divide by (B3) to get <=4B_0 h=B_0/(2m^2). This proves (B2). It uses no density formula for mu, no knowledge of its orthogonal polynomials, no lower Christoffel estimate, and no interval-centered doubling.

The explicit core and numerator bounds, rather than a bare Christoffel upper bound, are what make this a normalized moment statement.

## C. Apply it to the exact convex-body hierarchy

Let K be a compact convex body in R^n with nonempty interior, f a fixed real polynomial, and a a minimizer. Write

    ell(x)=grad f(a).(x-a),
    gamma=1+(1/2) max_K ||Hess f||_op,
    g(x)=ell(x)+gamma ||x-a||^2,
    G=max_K g, u=g/G.

The one-sided derivative at a along each segment in K is nonnegative, so ell>=0 on K. Taylor's theorem gives 0<=f-f(a)<=g. Also G>0 and u is a real polynomial of degree <=2, with values in [0,1] on K. For alpha in [0,1],

    g(a+alpha(x-a))=alpha ell(x)+alpha^2 gamma||x-a||^2
                     <=alpha g(x).                   (C1)

For S_t={x in K:u(x)<=t} and F(t)=vol(S_t), the homothety

    x -> a+(s/t)(x-a)

maps S_t into S_s. Its determinant is (s/t)^n, giving

    F(t)<=(t/s)^n F(s), 0<s<=t,
    F(s)>=s^n vol(K)>0, 0<s<=1.                       (C2)

Therefore the pushforward mu=u_#(Lebesgue|K) satisfies (B1) with A=1,D=n. Applying (B2) produces

    q_m(x)=P_m(u(x))^2 / integral_K P_m(u(x))^2 dx,
    integral_K (f-f(a))q_m <=G B(1,n)/m^2.             (C3)

The square root of q_m is a real polynomial of degree <=2m; q_m is a single global square of degree <=4m. For hierarchy order r>=2 choose m=floor(r/2). Then 4m<=2r and m>=r/3. The error is at most 9GB(1,n)/r^2. At r=1 use the constant density 1/vol(K), whose error is at most G; enlarge the constant to cover it. This proves the full scoped theorem for every integer r>=1.

This establishes an actual consequence of older approximation theory plus elementary convex geometry. The final combination, including (B2) and (C2), is made here in 2026. The result is neither a claim of an older explicit printed solution nor a proof of firstness for the submitted construction.

The general-measure statement in B is conditional on (B1). It does not assert the conclusion for arbitrary reference measures in the convex-body hierarchy. The composition uses u=g/G, rather than f, and consequently does not settle the restricted original-objective hierarchy s(f) for nonconvex f. The minimizer a is an existence input, with no efficient algorithm asserted.

## D. Independent elementary fallback and degree cost

For m>=1 let N=2m+1 and

    A_m(t)=(1+2 sum_(k=1)^m T_k(1-2t))/N.

At t=sin^2(v), 0<v<=pi/2, the finite trigonometric sum is

    A_m(t)=sin(Nv)/(N sin(v)).

Thus |A_m(t)|<=min(1,1/(N sqrt(t))) and A_m(t)>=2/pi on 0<=t<=N^-2. Raising to an even, fixed power 2L with L>D+1 gives, by the same shells as above,

    integral t A_m(t)^(2L) dmu
       <=hF(h)[1+A 2^(D+1) sum_(j>=0)2^(j(D+1-L))],
    integral A_m(t)^(2L) dmu >=(2/pi)^(2L)F(h),
    h=N^-2.

Hence the moment ratio is O(m^-2). For D=n choose L=n+2. The square root A_m(u)^L has degree <=2mL, so choose m=floor(r/(2L)); the degree overhead is fixed in r. This rechecks the submitted mechanism without assuming an endpoint theorem equivalent to the desired result. The Dirichlet identity and powers of classical kernels are not new ingredients. This is not an assertion that the cited Jackson kernel is the identical polynomial A_m.

## E. What classical Christoffel and zero-spacing statements actually give

Theorem 3.2 of Totik-Varga (printed pp.383,386) supplies an endpoint Christoffel upper bound when doubling is assumed only at centers in a specified set. In particular, centers={0} is allowed. Equation (C2) gives mu([-2s,2s])<=2^n mu([-s,s]), so this weaker hypothesis really applies. The corresponding shell comparison with the same core mass is established in their proof. No interval-doubling assumption is needed for that upper result.

A Christoffel upper bound minimizes integral P^2 with P(0)=1. Our objective minimizes integral tP^2 / integral P^2. Substituting the former estimate for the latter silently loses a denominator. The construction in B supplies the missing control and thus gives a verified consequence assembled now. Theorem 3.1 and the two-sided endpoint zero-spacing result require interval doubling; their hypotheses do not follow merely from (C2).

## F. Falsification of the generic cumulative-to-interval shortcut

Here is a full-support absolutely continuous counterexample to that shortcut. It is not claimed to be the pushforward of a convex body's quadratic proxy.

For k>=1 put t_k=2^-k, delta_k=t_k/16, epsilon_k=2^(-k^2), and I_k=[t_k-delta_k,t_k+delta_k]. Define a positive measurable weight on (0,1) by w=epsilon_k on I_k and w=1 elsewhere. Its support is [0,1]. The intervals are disjoint. Let F(t)=integral_0^t w.

If I_k intersects [0,t], then t_k<=(16/15)t. The sum of lengths of all such I_k is at most (1/8)*(32/15)t=4t/15. Consequently

    11t/15<=F(t)<=t, F'(t)=w(t)<=1<=2F(t)/t a.e.

Thus F(t)/t^2 is nonincreasing, and

    F(t)<=(t/s)^2 F(s), 0<s<=t<=1.                    (F1)

For interval doubling, however, 2I_k contains I_k and an additional length 2delta_k where w=1, and it meets no other valley. Therefore

    mu(2I_k)/mu(I_k)=(1+epsilon_k)/epsilon_k ->infinity.

For any beta>0, eventually 2I_k lies in (0,beta). Hence mu fails interval-centered doubling on every [0,beta], despite (F1). A route which assumes that implication is blocked. Additional convex-body structure might support a separate argument, but no such argument is used or claimed here.

## G. Adversarial boundary checks

- The core positivity follows from a bound on all of [0,1]; tail oscillations and zeros cause no division by a vanishing polynomial.
- The outermost shell uses the extended F above 1, so no domain mass is omitted.
- Neither the old-theory deduction nor the elementary fallback uses convexity of f. Convexity enters through K and the selected proxy.
- All estimates are for fixed n,K,f; constants may depend on the geometry and objective. L is independent of r.
- Constant objectives have zero error. The interval linear example supplies worst-case sharpness rather than a positive lower rate for each objective.
- Arbitrary full-support measures without a condition such as (B1) are outside the proof.

Primary links: [Totik-Varga](https://doi.org/10.1016/j.jmaa.2012.03.006), [2018 proxy reduction](https://doi.org/10.1287/moor.2017.0906), [Slot-Laurent](https://arxiv.org/abs/1905.08142).
