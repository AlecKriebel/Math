# Complete independent adversarial verification

This verifies the literal finite theorem and both maximum-attainment claims. The early reconstruction was sealed before foreign/code/opinions and already derives the operator, geometry, variational estimates, scaling and all-time argument. The independent arithmetic below was authored and first executed before reading the supplied checkers. No source repair or alternative narrowed theorem is proposed.

## A single finite smooth weight

Let L=10000 and retain exactly the paper's eta, chi, q and u. The flat jets of exp(-1/x) at x=0 prove that chi is a smooth step with values in [0,1]. On the open cylinder |s|<L/2, u=1; on each far end u=sech(|s|-L/2). Near s=0 the absolute-value corner lies inside a region on which u is constant. At both q=0 and q=1, endpoint jets give smooth matching.

Stereographic radius r=exp(s) gives g0=sech²(s)(ds²+g_S²). On a pole chart rho=exp(-|s|), the far-end formula becomes

    gL = 4E/(1+E rho²)² (d rho²+rho² g_S²),
    WL = E(1+rho²)²/(1+E rho²)²,    E=exp(L).

The parenthesized polar metric is Euclidean in smooth Cartesian coordinates, and its coefficient is a positive smooth function of |x|² at x=0. The same is true for WL. Hence gL and WL are smooth and positive on the standard compact sphere. E is a finite real constant; no floating-point evaluation of E is part of the definition or proof.

The exact cylinder volume is 4pi L. In a cap transition of radial parameter q∈[0,1], u³≤1. On q≥1, u³≤8exp(-3q), so each entire cap radial integral is at most 1+8/(3e³)<2. This proves

    4pi L ≤ VL < 4pi(L+4).

VL is a fully specified positive integral. Set a=(2pi²/VL)^(2/3), h=a gL, W=a WL and t*=4a. Then a>0, t*>0 and integral W^(3/2)dV0=a^(3/2)VL=2pi². There is no unstated limiting choice of L, cap or normalization.

## The original weighted operator

The actual OWR item (16), printed 421–422, defines the same operator W^(-1/2)Y0W^(-1/2), on the same round L² space, with the same integral W^(n/2) normalization and universal n≥3 quantifier. It also explicitly identifies the geometric conformal operator. Thus the proof is not a counterexample for a substitute operator.

For n=3, Yg=Delta_g+R_g/8, with positive Laplacian. Covariance under h=Wg0 gives Yh=W^(-5/4)Y0W^(1/4). The volume is W^(3/2)dV0, so multiplication U=W^(3/4) is unitary to L²(dV0). Consequently

    UYhU^(-1)=W^(-1/2)Y0W^(-1/2)=Y_W.

All factors and inverses are smooth on a compact manifold. They preserve smooth cores and relevant Sobolev form domains, so the equality extends to the closed self-adjoint elliptic operators. The quadratic form satisfies

    <Y_W f,f> = q0(W^(-1/2)f)
              ≥ (3/4) integral W^(-1)|f|² dV0
              ≥ 3/(4 max W)||f||².

There is therefore a strictly positive spectral bottom, compact resolvent, and finite heat trace for every positive time. Negative transition scalar curvature is irrelevant to this form proof; the argument does not assume it absent.

## Dirichlet subspaces give a rigorous heat lower bound

On the product cylinder the scalar curvature is 2, hence the operator is -d²/ds²+Delta_S²+1/4. Let phi_k be the S²-constant Dirichlet sine of frequency pi k/L, with zero extension across the endpoints. The trace at each interface is zero. Integration by parts for a test function on both sides shows that the first weak derivative is the zero extension of its ordinary derivative, with no boundary delta. It lies in L², so phi_k is in the closed global H¹ form domain, even though its derivative jumps and it is not a smooth global eigenfunction.

Sine orthogonality diagonalizes both norm and form on their spans. For any vector in the first k-dimensional span, its quotient is at most mu_k=1/4+(pi k/L)². The variational characterization of the kth full eigenvalue, counted from the first eigenvalue with multiplicity, therefore gives lambda_k(gL)≤mu_k. For every finite K, summing exp(-4lambda_k)≥exp(-4mu_k) through K is legitimate. Monotone limits give

    Tr exp(-4YgL) ≥ e^(-1) sum(k≥1) exp(-4pi²k²/L²)
                 ≥ e^(-1)(L/(4sqrt(pi))-1).

The last step uses a decreasing positive Gaussian: its sum from one is at least its integral from one; its omitted integral over [0,1] is at most one. The Gaussian integral over [0,infinity) is L/(4sqrt(pi)). No numerical eigenvalue estimate or sampled trial-family optimization is used.

Under constant metric rescaling, Yh=a^(-1)YgL. At t*=4a both the time and prefactor must scale:

    t*^(3/2) Tr exp(-t*Y_W)
       = 8a^(3/2) Tr exp(-4YgL)
       = 16pi²/VL Tr exp(-4YgL)
       > sqrt(pi)/e * (L-4sqrt(pi))/(L+4).

The last inequality is strict because VL has a strict upper bound and the displayed Gaussian lower bound is positive at this L. With the independently certified strict brackets 1.772<sqrt(pi)<1.773 and e<2.719, it follows that

    weighted value > (1772/2719)(9992908/10004000)
                   = 1106714561/1700054750
                   = 13/20 + 3357947/3400109500.

This establishes the literal finite lower fraction and its strict threshold.

## An all-time upper bound for the actual round trace

On S³, degree l harmonics have eigenvalue l(l+2) and multiplicity (l+1)². With j=l+1 the Yamabe eigenvalues are j²-1/4, multiplicities j². Thus

    F0(t)=t^(3/2) sum(j≥1) j² exp[-t(j²-1/4)].

Apply Gaussian Poisson summation to sum(j in Z)exp(-tj²) and differentiate on compact positive-time intervals, where the Gaussian and its derivatives converge uniformly. The result is

    F0(t)=sqrt(pi)/4 exp(t/4)
      [1+2 sum(m≥1)(1-2pi²m²/t)exp(-pi²m²/t)].

For 0<t≤7/5 the parenthesized factors are strictly negative for all m≥1. Therefore F0(t)<(1.773/4)exp(7/20), giving the first time-region bound. This is an interval argument, not an estimate of a truncated positive spectral series near zero.

Write F0=A+B with A(t)=t^(3/2)exp(-3t/4). Its logarithmic derivative is 3/(2t)-3/4, so A increases through t=2. Each j≥2 summand of B decreases for t≥2/5. At a≥7/5, consecutive ratios in the j≥3 tail obey

    ((j+1)/j)² exp[-a(2j+1)] ≤ (16/9)exp(-7a) < 1/2.

The geometric-tail estimate is therefore

    B(a) ≤ a^(3/2)[4exp(-15a/4)+18exp(-35a/4)] = D(a).

For every a≤t≤b≤2 in this range, F0(t)≤A(b)+D(a). The six closed intervals in the original table cover [7/5,2]. For t≥2, every original spectral summand is nonincreasing, since all lambda≥3/4. Summing the pointwise inequalities proves F0(t)≤F0(2) without any derivative/sum exchange at infinity. The first small-time interval and these six intervals therefore control every t>0.

## Independent exact arithmetic certificate

`independent_rational.py` uses only integers and Fraction. It is distinct from the supplied P50 positive-series reciprocal checker:

* pi is enclosed using 16atan(1/5)-4atan(1/239). Tangent doubling gives tan(4atan(1/5))=120/119 and subtraction gives exactly tangent one. The angle lies in the first quadrant, so it is pi/4. Twenty-four alternating terms and the next-term remainder enclose each arctangent, with the subtraction reversing the needed endpoint for atan(1/239).
* For exp(-x), put q=x/32≤1. The degree-12 alternating partial sum is an upper bound; subtracting q¹³/13! gives the degree-13 lower bound. Both are strictly positive in the used range. Raising their endpoints to the 32nd power preserves the order and encloses exp(-x). Reciprocating the lower endpoint bounds exp(x) above where needed.
* Each sqrt endpoint is enclosed by integer square root on the 2^40 lattice; integer inequalities prove both endpoints. Final displayed upper fractions are rounded outward, using integer ceiling on a 10^12 lattice.

The resulting exact rational upper enclosures are:

| Time region | Independent rational upper bound | Original literal ceiling |
| --- | --- | --- |
| (0,7/5] | 314500845457/500000000000 | 629002/1000000 |
| [7/5,3/2] | 126267490127/200000000000 | 631338/1000000 |
| [3/2,8/5] | 39758931627/62500000000 | 636143/1000000 |
| [8/5,17/10] | 639463652507/1000000000000 | 639464/1000000 |
| [17/10,9/5] | 641171472209/1000000000000 | 641172/1000000 |
| [9/5,19/10] | 80150129097/125000000000 | 641202/1000000 |
| [19/10,2] | 639540520987/1000000000000 | 639541/1000000 |

Every independent expression is below the corresponding literal ceiling. Thus sup F0≤641202/1000000<321/500. The exact lower-minus-this-coarse-round-upper margin is 33272110381/3400109500000>0. This verifies all of the main theorem's quantitative constants, not only the older weaker threshold 129/200.

## Attainment and precise logical reach

The standard leading heat coefficient for the fixed smooth compact normalized metric h is vol(h)/(4pi)^(3/2)=sqrt(pi)/4. The same holds for the round metric. This coefficient depends on the principal symbol/volume, not the possibly signed lower-order curvature term. Strict positive lambda1 gives, for t≥1,

    Tr exp(-tY) ≤ exp[-(t-1)lambda1] Tr exp(-Y),

so the scaled trace tends to zero at infinity. It is continuous for positive time. The weighted lower value exceeds sqrt(pi)/4. For the round metric the first mode at t=2 gives 2sqrt(2)exp(-3/2)>sqrt(pi)/4, because 128>pi e³, independently verified from the rational constant bounds. In either case both endpoint limits are strictly below a known interior value. Outside some compact positive-time interval the trace is below that value; continuity on the compact interval proves global maximum attainment.

All theorem claims are therefore supported. A single admissible n=3 weight refutes the universal n≥3 comparison. The n≥4 restriction and the separate n≥4 monotonicity conjecture are not addressed. The metric is an explicit finite smooth example; it does not claim a closed elementary formula for VL, computed high-precision spectrum, new cylindrical geometry, new min–max principle, firstness or certified current openness. Literature/version access limits are recorded separately and do not supply or replace a mathematical step of this proof.
