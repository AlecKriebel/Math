# Second analytic review of the weighted Yamabe counterexample

Problem 30001168 / OWR-3389-021, ranked record 821  
Review date: 6 October 2026  
Disposition: **ACCEPT the dimension-three counterexample.**

The stated smooth positive weight satisfies every hypothesis of the original
comparison, and its scaled heat trace is strictly larger than the entire
round-sphere comparison trace. No correction to the frozen proof is needed.
This review additionally supplies a four-region proof of the round upper
bound, independent of either earlier interval-grid certificate.

This is an independent AI mathematical review. It is not human peer review,
formal proof-assistant verification, publication, or a claim of historical
priority. The conclusion refutes the universal assertion over n>=3 by its
n=3 instance. Neither the comparison restricted to n>=4 nor the separate
monotonicity problem 30001169 is resolved here.

## Source and frozen inputs

The original item (16), Conjecture 1, was checked in printed pages 421-422 of
*Low Eigenvalues of Laplace and Schrödinger Operators*, Oberwolfach Reports
6 (2009), 355-428, [DOI 10.4171/OWR/2009/06](https://doi.org/10.4171/OWR/2009/06).
The [official EMS PDF](https://ems.press/content/serial-article-files/46205)
was opened anew; its relevant text and locally rendered source pages were
inspected. The hypotheses are smooth strict positivity and the normalized
integral with round volume, with the weighted operator acting on round L².
There is no Yamabe-minimizer, constant-scalar-curvature, scalar-curvature-sign,
or upper-weight-bound hypothesis. The adjacent monotonicity question has
n>=4 scope. The unrelated half-line inequality is not the target question.

Both supplied frozen ZIP hashes were independently recomputed and match
their receipts. The complete authored proof, the first analytic audit, both
arithmetic implementations, and both replay verifiers were read. Both
replay verifiers passed in normal and optimized isolated Python. Their
original files and ZIPs remain unchanged. This second review did not repeat
the earlier full-corpus parsing or literature/repository searches and makes
no new claim based on those searches. Public input hashes and review history
are recorded in INPUTS.json.

## Smooth admissibility and positivity

Put g_c=ds²+g_S² on R x S². Stereographic radius r=e^s gives

    g_round = sech²(s) g_c.

With L=10000 and q=|s|-L/2, the author's flat step chi produces
u=exp(-chi(q) log cosh(q)). The apparent absolute-value singularity is
irrelevant because u=1 on an open neighborhood of s=0. At q=0 and q=1,
flatness of chi and 1-chi matches all derivatives to the adjoining constant
and sech pieces. Thus g_L=u²g_c is smooth on the twice-punctured sphere and
contains the exact length-L product cylinder.

Near either pole, in the appropriate small stereographic radius rho,

    W_L = u² cosh²(s) = e^L (1+rho²)²/(1+e^L rho²)².

This is a smooth function of the squared Cartesian radius with value e^L>0
at the pole. The value is mathematically finite for the fixed L=10000.
Consequently the extension is a smooth positive conformal weight on the
original smooth S³, not a singular limit or another topology.

In dimension three the conformal Laplacian is Y_g=Delta_g+R_g/8 with positive
Laplacian convention. For h=Wg_round,

    Y_h = W^(-5/4) Y_round W^(1/4),
    U f = W^(3/4)f,
    U Y_h U^(-1) = W^(-1/2)Y_round W^(-1/2).

The multiplier U is unitary between the two volume-measure L² spaces.
All the multipliers are smooth and boundedly invertible for this fixed
weight, so the smooth-function identities extend to the self-adjoint
operators via their closed quadratic forms. Moreover the weighted form
is bounded below by (3/(4 max W))||f||². Thus the spectrum is strictly
positive. Compact smooth ellipticity ensures compact resolvent and a
trace-class heat operator at every positive time. Any possibly negative
cap scalar curvature creates no difficulty.

## The closed-manifold spectral lower bound

Inside the exact cylinder R=2, hence Y=-d²/ds²+Delta_S²+1/4. The functions
sin(pi k(s+L/2)/L), constant on S² and extended by zero outside the cylinder,
have zero boundary traces. Their extensions therefore belong to H¹ on the
closed sphere. A normal-derivative jump affects the distributional second
derivative, but no delta enters the first derivative or the quadratic form.
Equivalently, H¹_0 cylinder approximants extend by zero continuously in H¹.

These functions are mutually orthogonal for both the form and L² norm.
Their first k span has largest Rayleigh quotient

    mu_k = 1/4 + (pi k/L)².

The min-max principle compares the k-th full closed-manifold eigenvalue,
with its actual multiplicity, to this k-dimensional subspace. Thus
lambda_k<=mu_k and

    Tr exp(-4Y_gL) >= e^(-1) sum_{k>=1} exp(-4 pi² k²/L²).

No spectral decoupling assertion, boundary condition on the closed operator,
missing transverse multiplicity, or large-L convergence is used. Other
modes can only strengthen the trace lower bound.

## Volume and time scaling

The exact middle has volume 4 pi L. Each cap has radial volume at most
1+8/(3e³)<2, so V_L<=4 pi(L+4). The decreasing Gaussian satisfies

    sum_{k>=1} exp(-4 pi² k²/L²) >= L/(4 sqrt(pi))-1.

The right side is positive for the specified L. Set

    a=(2 pi²/V_L)^(2/3), h=a g_L, W=a W_L, t_*=4a.

Then integral W^(3/2) dv_round=2 pi², and Y_h=a^(-1)Y_gL. Direct substitution,
including the prefactor, gives

    t_*^(3/2) Tr exp(-t_*Y_W)
      = (16 pi²/V_L) Tr exp(-4Y_gL)
      >= (sqrt(pi)/e)(L-4 sqrt(pi))/(L+4)
      > (1772/2719)(10000000-7092)/10004000
      = 1106714561/1700054750 > 13/20.

The bounds 1.772<sqrt(pi)<1.773 and e<2.719 are applied to separate positive
factors in the correct direction. This is a finite-L inequality at one
explicitly defined positive time, not an asymptotic existence argument.

## A separate four-region round bound

The round eigenvalues and multiplicities are j²-1/4 and j² for j>=1. Write

    F(t) = sum_{j>=1} j² t^(3/2) exp(-(j²-1/4)t),
    A(t) = t^(3/2) exp(-3t/4),
    B(t) = sum_{j>=2} j² t^(3/2) exp(-(j²-1/4)t).

A increases through t=2 and decreases afterwards. Every term of B decreases
for t>=2/5, because the smallest eigenvalue in B is 15/4. These statements
follow by differentiating each individual term. Summing their pointwise
inequalities requires no derivative/series interchange.

For 0<t<=3/2, the Gaussian Poisson identity and its derivative give

    F(t) = (sqrt(pi)/4)e^(t/4)
           [1+2 sum_{m>=1}(1-2 pi²m²/t)e^(-pi²m²/t)].

Every correction is negative on this interval. Hence

    F(t) < (1.773/4)e^(3/8) < 0.644924944529518 < 129/200.

For a>=3/2, the ratio of consecutive summands of the j>=3 tail is at most
(16/9)e^(-7a), which is less than 1/2 since e^(7a)>1+7a. Therefore

    B(a) <= a^(3/2)[4e^(-15a/4)+18e^(-35a/4)] = T(a).

It remains to use three elementary bounds:

    3/2 <= t <= 13/8:  F(t) <= A(13/8)+T(3/2),
    13/8 <= t <= 7/4:  F(t) <= A(7/4)+T(13/8),
    7/4 <= t < infinity: F(t) <= A(2)+T(7/4).

The separate monotonicity of A and B proves all three, including the
unbounded final interval. Their certified rational upper bounds, rounded
upward to the displayed decimals, are respectively

    0.638896077738840,
    0.641808301650495,
    0.644195469901180.

All four ranges together prove F(t)<129/200 for every t>0. This bound is
weaker than the first audit's bound but suffices for the strict separation.
It is not an estimate of the exact maximum. It uses four analytic regions
rather than either earlier 100-cell or 200-cell discretization.

### Elementary arithmetic implementation

The accompanying four_region_certificate.py imports no previous certificate.
For positive x, let P_N(x)=sum_{k=0}^N x^k/k!. It uses

    P_N(x) < e^x <= P_N(x) + [x^(N+1)/(N+1)!]/[1-x/(N+2)]

whenever 0<x<N+2. The upper tail follows because all subsequent term ratios
are bounded by x/(N+2). Reciprocal degree-40 lower sums bound negative
exponentials from above. Degree-12 sums and their geometric tails bound
e^(3/8) and e. Four explicit square-root brackets are checked by exact
squaring. The bounds for pi use the direct alternating Gregory series for
pi/4 through 2000 terms and its next positive term; no Machin or other
angle-addition formula is needed.

Every acceptance calculation is rational, and checks use explicit
exceptions rather than assert. The report's analytic steps, including
Poisson summation, smooth extension, conformal covariance, ellipticity,
and min-max, remain mathematical review obligations rather than code tests.

## Literal maxima and final disposition

The normalized leading heat coefficient is sqrt(pi)/4 for both metrics.
The scaled traces tend to that value as t decreases to zero. At infinity,
strict positivity and the finite heat trace at, for example, time 1 imply
exponential decay: for t>=1,

    Tr exp(-tY) <= exp(-(t-1)lambda_1) Tr exp(-Y).

Multiplication by t^(3/2) does not alter the zero limit. Continuity holds at
positive time. The constructed trace exceeds its zero-time limit. The
round first mode at time 2 also exceeds this limit, so both suprema are
attained at positive finite times. Thus the source's literal maxima do not
introduce an exception.

All specified analytic objections were checked and none invalidates the
construction. The proof establishes a full negative answer to the universal
comparison through n=3. It does not establish its historical novelty or
settle any n>=4 statement.

This package contains authored review, arithmetic code, replay results, and
public verification metadata only. It excludes copied source documents,
source extracts, dataset contents, and private coordination material. No
remote mutation or external outreach was performed.
