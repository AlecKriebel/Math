# Independent adversarial reconstruction, before code, foreign bodies or opinions

The whole actual four-page PDF and the entire 13,427-byte controlling `published-source/note.tex` have been read. No inventory triage, archived audit narrative, current/historical scientific review, foreign primary body or source mathematical program has been read. The target conclusions below are hypotheses to check, not assumed results. This early object is to remain immutable.

## Literal assertion and scope

On the unit round S³ with positive Laplacian, Y0=Delta+3/4 and the operator in question is Y_W=W^(-1/2)Y0W^(-1/2) on L²(dV0). The weight is smooth and strictly positive with integral W^(3/2)=2pi². The paper claims a fully specified finite weight and t*>0 with

    t*^(3/2) Tr(exp(-t*Y_W)) > 1106714561/1700054750 > 13/20,
    max(t>0) t^(3/2) Tr(exp(-tY0)) < 321/500.

Both maxima are asserted to be attained at finite positive times. This would refute the universal comparison over dimensions n≥3 by its n=3 case. It does not settle the comparison restricted to n≥4 or the separate source monotonicity question. The original Morpurgo operator, normalization and quantifiers still require direct authentication after this seal. The manuscript explicitly denies firstness/current-openness certification and credits cylindrical geometry and the spectral mechanism as classical.

API version is 1.0.0, declared 13 October 2026; the actual reader prints that date/version. API creation is 15 October 2026, 04:00:37.039113 UTC. Those are different facts. The exact actual reader and controlling source hashes are sealed separately with this reconstruction.

## Construction: smoothness rather than a limiting singular metric

The cylinder coordinate has r=exp(s), and the round metric equals sech²(s)(ds²+g_S²). This follows directly from the stereographic round factor 4/(1+r²)² after dr=r ds. The proposed L is the finite integer 10000. With q=|s|-L/2, the cutoff is chi(q)=eta(q)/(eta(q)+eta(1-q)), eta(x)=0 for x≤0 and exp(-1/x) otherwise. Its denominator is positive, its endpoint jets match constants, and u=exp(-chi(q)log cosh(q)).

For q≤0, u=1, so the cylinder is exactly a product of unit S² with an interval of length L. The corner of |s| occurs where u is locally constant and is harmless. For q≥1, u=sech(q). At either pole take rho=exp(-|s|). Then

    u=2 exp(L/2)rho/(1+exp(L)rho²),
    g_L=4 exp(L)/(1+exp(L)rho²)² (d rho²+rho²g_S²),
    W_L=exp(L)(1+rho²)²/(1+exp(L)rho²)².

These are positive smooth radial functions of rho² at the pole in a Cartesian stereographic chart. Thus the construction is a single smooth compact conformal metric, not merely an infinite-cylinder limit. exp(10000) need not be evaluated numerically; finiteness, positivity and smoothness suffice. Every multiplier and its reciprocal is bounded for this fixed compact example, even though the bounds are large.

The cylinder contributes 4pi L to V_L. Each cap contributes radial integral at most 1+integral(1,infinity)8exp(-3q)dq <2, since u≤1 on [0,1] and sech(q)≤2exp(-q) afterwards. Hence 4pi L≤V_L<4pi(L+4). Define a=(2pi²/V_L)^(2/3), h=a g_L, W=a W_L, t*=4a. Then a^(3/2)V_L=2pi². This checks the normalization exponent; an exponent 2/3 used in the wrong place would materially change the comparison.

## Exact operator identity and positivity

For h=Wg0 in dimension three, conformal covariance gives Y_h=W^(-5/4)Y0W^(1/4). The unitary L²(dV_h)→L²(dV0) is multiplication by W^(3/4). Left exponent 3/4-5/4 and right exponent 1/4-3/4 both equal -1/2. Therefore the weighted operator's spectrum and trace are exactly those of Y_h. This must be checked against the actual historical weighted operator, not an unweighted Laplacian or a differently normalized conjugate.

The weighted quadratic form is the round positive form applied to W^(-1/2)f, and is at least 3/(4 max W) times ||f||². This establishes strict positivity despite possible negative scalar curvature on the transitions. No unproved nonnegative-curvature condition is necessary. Smooth positive coefficients on a compact manifold imply closed elliptic forms, compact resolvent and finite positive-time heat traces.

## Trial subspaces and multiplicities

On the exact cylinder scalar curvature is 2, so Y_gL=-d²/ds²+Delta_S²+1/4. The S²-constant sine modes with Dirichlet endpoints have norm and form matrices diagonal and Rayleigh values mu_k=1/4+(pi k/L)². Zero extension is in global H¹ because the boundary value is zero. A derivative jump only affects the second derivative distribution; it does not put a delta in the first weak derivative or violate the form-domain calculation. No claim that the modes are smooth global eigenfunctions is needed.

The span of the first k modes gives lambda_k≤mu_k for the full closed-manifold spectrum counted with multiplicity, including the first eigenvalue. Thus all finite partial heat sums at time 4 dominate the sine-mode sums; monotone limits yield the full trace lower bound. The decreasing Gaussian gives

    sum(k≥1) exp(-4pi² k²/L²) ≥ integral(1,infinity) ...
                                 ≥ L/(4sqrt(pi))-1.

This direction of the sum/integral comparison is important. The omitted [0,1] integral is at most one.

## Scaling and the finite numerical gap

Constant scaling gives Y_h=a^(-1)Y_gL, so at t*=4a,

    t*^(3/2) Tr(exp(-t*Y_W))
       =8 a^(3/2) Tr(exp(-4Y_gL))
       =16pi²/V_L Tr(exp(-4Y_gL))
       >sqrt(pi)/e * (L-4sqrt(pi))/(L+4).

The last inequality uses the strict volume upper bound and a positive numerator. Separating the two occurrences of sqrt(pi), one may lower-bound its outer factor by 1.772, upper-bound its negative occurrence by 1.773, and upper-bound e by 2.719. This gives the claimed rational candidate. Its exact equality and margin must be recomputed independently, without floating-point acceptance. The bound is finite at L=10000, so an asymptotic argument alone is insufficient.

## All-time round trace, not a sampled maximum

Round eigenvalues are j²-1/4 with multiplicities j², j≥1. Hence F0(t)=t^(3/2)exp(t/4) sum(j≥1)j²exp(-tj²). Gaussian Poisson summation and differentiation give

    F0(t)=sqrt(pi)/4 exp(t/4)
        [1+2 sum(m≥1)(1-2pi²m²/t)exp(-pi²m²/t)].

The sign is correct by differentiating the t^(-1/2) factor and exp(-pi²m²/t) together. On (0,7/5] every correction is negative, so the stated single small-time bound follows. Local uniform Gaussian convergence justifies the differentiation; it is not an exchange at t=0.

For t≥7/5, split off A(t)=t^(3/2)exp(-3t/4). It increases up to t=2. All terms with j≥2 decrease for t≥2/5, since their logarithmic derivative is 3/(2t)-(j²-1/4). The j≥3 consecutive ratio is at most (16/9)exp(-7a)<1/2 for a≥7/5, giving the tail majorant 18exp(-35a/4). The factor 18 is twice the first tail multiplicity 9, and must not be mistaken for a multiplicity of 18 in the original spectrum.

Therefore each interval [a,b]⊂[7/5,2] has the universal bound A(b)+a^(3/2)[4exp(-15a/4)+18exp(-35a/4)]. Six specified intervals cover this entire range. For t≥2 all summands decrease, so F0(t)≤F0(2). Recomputing exact rational upper enclosures for the seven time regions will establish an all-time bound. A mesh of actual function samples alone would not do so.

## Distinct adversarial arithmetic plan

Without opening the supplied certificate code, independently author an exact Fraction certificate with a different exponential enclosure: range-reduce x to x/32, use alternating Taylor bounds for exp(-x/32), then raise the positive lower/upper endpoints to the 32nd power. Invert the lower endpoint for needed positive exponentials. Odd and even alternating partial sums bound exp(-q) for q in a suitably small positive interval. This avoids copying the manuscript's positive-series P50 reciprocal implementation.

Obtain pi bounds independently by the Machin identity pi=16atan(1/5)-4atan(1/239), using alternating rational remainders. Tangent doubling gives tan(4atan(1/5))=120/119, and subtracting atan(1/239) gives tangent one with the first-quadrant branch. Rational square bounds or integer bisection certify endpoint square roots. Compare every interval expression to the paper's literal table and to 321/500, and recompute the lower fraction and positive gaps. This computation supports the finite arithmetic; smoothness, min–max and Poisson summation remain written mathematical obligations.

Controls should challenge the weighted-operator exponents, missing volume/time prefactors, omitted constant cylinder curvature, illegitimate smooth-eigenfunction treatment of zero-extended modes, false monotonicity ranges, a too-small tail factor, and incorrect rational thresholds. Some controls require algebraic or logical proof rather than a floating-point failure. A source checker must be read before any source execution; source builders/finalizers will not be executed.

## Maxima and remaining obligations

The normalized heat leading term at t down to zero is (4pi)^(-3/2)2pi²=sqrt(pi)/4. Strict positivity gives trace decay at infinity via the time-one trace and the first eigenvalue. The finite weighted lower value is above the zero-time limit. The first round mode at t=2 is 2sqrt(2)exp(-3/2), also above that limit because 128>pi e³. Continuity and both endpoint limits then put each supremum inside a compact positive-time interval, where it is attained. Thus the word maximum in the original comparison is addressed.

No central defect is apparent in the reconstructed mechanism. This is not yet a final verdict: exact arithmetic, actual historical operator/normalization, imported primary interfaces, source preservation and code boundaries remain to be checked. The contribution cannot be credited as a new cylindrical construction or min–max method. Novelty/current-openness claims do not follow from this derivation or a bounded negative search.
