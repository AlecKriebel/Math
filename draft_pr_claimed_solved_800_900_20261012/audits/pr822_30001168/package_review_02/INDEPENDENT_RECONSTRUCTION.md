# Independent reconstruction before consulting prior verdicts

Written during package review 02 on 2026-10-15 UTC. Inputs at this stage were the current note, its code, and actual OWR/Ammann–Jammes passages, not previous review conclusions.

## Exact claim and falsification criteria

The target is Morpurgo's Conjecture 1, item (16), printed pages 421–422 of OWR 6/2009: for every integer n >= 3 and every smooth positive W with integral W^(n/2) equal to round volume, the maximum of t^(n/2) Tr exp(-t W^(-1/2)Y_0 W^(-1/2)) is at most its round value. The underlying Hilbert space is round L2 and Y_0 = Delta + n(n-2)/4 has the positive-Laplacian convention. A single admissible n=3 example exceeding a valid all-time round bound disproves the universal statement. It need not settle n>=4 or Conjecture 2. Main attacks: non-smooth or vanishing W, wrong conformal/unitary powers, unbounded cap volume, omitted normalization/time prefactor, reversed or fixed-index-only min–max, a finite-time-only round bound, and unjustified literal maxima.

## Geometry reconstructed

Under r=e^s, the round metric is sech(s)^2(ds^2+g_S2), directly from 4(dr^2+r^2g_S2)/(1+r^2)^2. The step chi has a positive denominator for all real arguments. Its endpoint jets agree to all orders with constants 0 and 1. The expression involving |s| is constant near s=0, so that apparent corner never enters a derivative. At q=0 its jets agree with u=1; at q=1 they agree with sech(q). Thus there is an exact cylinder of length L, two smooth transitions, and two exact sech tails.

For the positive tail, rho=e^(-s) gives cosh(s)/cosh(s-L/2) = e^(L/2)(1+rho^2)/(1+e^L rho^2); the negative tail is identical with rho=e^s. Squaring gives the note's W_L formula. Both W_L and the metric coefficient are positive smooth functions of |x|^2 at each stereographic origin. L=10000 is finite, so e^L is a legitimate finite real constant, irrespective of machine overflow. Compactness then gives finite positive upper and lower bounds for W_L and W.

The cylinder volume is 4 pi L. For each cap q>=0, u<=1 on [0,1] and u=sech(q)<=2e^(-q) thereafter; its integral of u^3 is <=1+8/(3e^3)<2. Therefore 4 pi L<=V_L<4 pi(L+4). The fixed prescribed tails are essential: an arbitrary pointwise F_L<=1/r cap condition alone would not imply a uniform finite cap volume. a=(2pi^2/V_L)^(2/3) is strictly positive and a^(3/2)V_L=2pi^2, so W=aW_L has exactly the required normalization.

## Operator, form domain, and spectral mass

In n=3, Y_g=Delta_g+R_g/8. Conformal covariance under h=Wg_0 gives Y_h=W^(-5/4)Y_0 W^(1/4). The volume relation is dV_h=W^(3/2)dV_0, hence multiplication by W^(3/4) is unitary from L2(h) to round L2. Conjugation yields W^(-1/2)Y_0W^(-1/2) exactly. Smooth positive compact multipliers and their inverses preserve H1 and the closed forms. The displayed lower bound >=3/(4 max W) follows by applying Y_0>=3/4 to W^(-1/2)f. Thus no sign assumption on cap scalar curvature is required; there is a positive gap and compact elliptic resolvent.

On the exact cylinder scalar curvature is 2, giving -d_s^2+Delta_S2+1/4. The k-dimensional span of constant-angular sine functions has zero boundary trace, so its zero extension is in global H1. A jump of first normal derivatives obstructs H2, but does not obstruct H1; there is no jump in the function itself. All form and L2 matrices are diagonal on this span. The maximal Rayleigh quotient is mu_k=1/4+(pi k/L)^2. The full global k-th eigenvalue is <=mu_k for every k, including multiplicity; this uses all k-dimensional trial spaces rather than an unsupported transfer from an asymptotic fixed-index theorem. It implies each finite heat sum inequality and hence the full trace inequality by monotone limits.

The decreasing Gaussian f(x)=exp(-4pi^2 x^2/L^2) satisfies sum_{k>=1} f(k)>=integral_1^infinity f >= L/(4sqrt(pi))-1. Thus Tr exp(-4Y_gL)>=e^(-1)(L/(4sqrt(pi))-1). Since Y_h=a^(-1)Y_gL, the time must be 4a, and t_*^(3/2)=8a^(3/2)=16pi^2/V_L. Substitution and the strict volume upper bound give >sqrt(pi)/e * (L-4sqrt(pi))/(L+4). Substituting sqrt(pi)>1.772 in the leading factor and sqrt(pi)<1.773 in the positive numerator, and e<2.719, gives precisely 1106714561/1700054750. Its excess over 13/20 is 3357947/3400109500>0.

## Round all-time bound and attainment

The round spectrum is lambda_j=j^2-1/4 with multiplicity j^2, j>=1. Differentiating the Gaussian theta identity gives the printed Poisson formula. Every correction term is strictly negative when t<=7/5 because 2pi^2>7/5. Thus the small-time bound is (1.773/4)e^(7/20).

A(t)=t^(3/2)e^(-3t/4) increases to t=2. For j>=2 each other summand decreases for t>=2/5, since its maximum is at 3/[2(j^2-1/4)]<=2/5. For j>=3 the consecutive ratio at t>=a is <=(16/9)e^(-7a)<1/2. Their sum is <=18a^(3/2)e^(-35a/4); j=2 contributes 4a^(3/2)e^(-15a/4). Therefore A(b)+D(a) bounds each entire interval [a,b] listed, not just its endpoints. All modes are nonincreasing after 2, so the final interval also bounds the infinite-time ray. Six intervals plus the Poisson small-time region cover every positive time without a gap.

The Taylor lower polynomial gives an upper reciprocal bound for each negative exponential. Its geometric upper remainder is valid because subsequent positive-term ratios are <=x/(N+2)<1. Integer square-root enclosures give the specified rational endpoint formulas. The table's largest displayed enclosure is 641202/10^6<321/500, strictly separated from 13/20. These arithmetic inequalities are independently reconstructed in independent_arithmetic.py.

The leading heat coefficient for h and g_0 is volume/(4pi)^(3/2)=sqrt(pi)/4. The positive gap forces the scaled traces to zero at infinity. The cylinder witness exceeds the zero-time limit. The round first mode at 2 is 2sqrt(2)e^(-3/2), which exceeds sqrt(pi)/4 because 128>pi e^3. Positive-time continuity plus these strict witnesses puts both suprema inside compact positive-time intervals. The word 'maximum' is therefore justified.

## Attribution and remaining limits

The actual Ammann–Jammes author manuscript, section 3.2, constructs smooth conformal Pinocchio metrics with growing cylindrical noses; its introduction credits earlier Pinocchio sources. Its Theorem 4.1 is a fixed-index statement and alone is not an all-index trace bound. The present explicitly chosen cap and elementary all-k trial-mode deduction supply the needed application. The mechanism is classical as the current note explicitly says. This reconstruction certifies no historical priority, exhaustive literature absence, or worldwide current openness. It does not prove anything about n>=4 or the adjacent monotonicity conjecture. Arithmetic and package checks cannot mechanically certify smoothness, covariance, min–max, Poisson summation, or heat asymptotics; those remain imported standard analytic results applied here with stated hypotheses.
