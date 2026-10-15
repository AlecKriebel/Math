# Independent R3 reconstruction before prior verdicts

Prepared from the complete current `preprint/note.tex`, the actual OWR item,
the retained Ammann--Jammes author text, and the frozen original proof. No
package_review_01 or package_review_02 verdict was read in this reconstruction.
The target is a hypothesis, and the following checks are mathematical reasoning,
not claims made by a hash or arithmetic program.

## Exact target and scope

OWR 6/2009, printed page 421, item (16), Conjecture 1, explicitly uses a
positive smooth weight with integral W^(n/2) equal to round volume and the
operator W^(-1/2)(Delta+n(n-2)/4)W^(-1/2) on **round L2**. It quantifies over
n >= 3. The target does not require constant curvature, Yamabe minimization,
or a uniform familywise derivative bound. Printed page 422's separate
Conjecture 2 concerns n >= 4. A single admissible finite n=3 counterexample
therefore refutes the former universal assertion and settles neither the
n>=4 restriction nor the adjacent monotonicity problem.

## Finite geometry

Putting r=e^s into 4(dr^2+r^2 dOmega^2)/(1+r^2)^2 gives the stated
sech^2(s)(ds^2+dOmega^2). The two terms in eta(x)+eta(1-x) cannot both vanish.
The usual exp(-1/x) flatness proves smooth chi and all matching jets. On the
whole interval |s|<L/2 the resulting u is exactly 1; in particular |s|'s
corner is composed with a locally constant function. For q>=1, u=sech(q).
The transition is positive, smooth, and bounded above by 1.

Near either pole, set rho=e^(-|s|). Direct algebra, without evaluating
e^10000, gives

    W_L = e^L (1+rho^2)^2/(1+e^L rho^2)^2,
    g_L = 4e^L/(1+e^L rho^2)^2 (d rho^2+rho^2 dOmega^2).

In Cartesian stereographic coordinates these coefficients are smooth
strictly positive functions of |x|^2. The finite real e^10000 causes no
analytic loss. This proves admissibility on the standard sphere, including
both poles and both ends of each transition, rather than only on a punctured
or nonsmooth limit space.

Each cap contributes at most 1+integral_1^infinity 8e^(-3q)dq<2 to the
radial volume integral. Hence 4pi L<=V_L<4pi(L+4). The normalization
a=(2pi^2/V_L)^(2/3) is finite positive, and a^(3/2)V_L=2pi^2. An integral of
an explicitly specified smooth function is an exact definition; no decimal
volume calculation or limiting cylinder is needed.

## Hilbert spaces, positivity, domains, indices

For h=Wg0 in n=3, the covariance exponents are -5/4 and +1/4, the volume
factor is W^(3/2), and the L2-unitary multiplier is W^(3/4). Combining the
left exponents 3/4-5/4 and the right 1/4-3/4 yields -1/2 on both sides.
Thus the geometric operator and the exact source's round-L2 operator are
unitarily equivalent. Every multiplier and inverse is smooth and bounded
on this one compact smooth sphere. The closed form domains are H1; there
is no passage to a singular limiting domain. On the round side its form is
q0(W^(-1/2)f), which bounds (3/(4 max W))||f||^2 from below. This is a
strict, albeit small, positive spectral gap. Negative transition curvature
would not contradict this identity or invalidate the form.

The product cylinder has scalar curvature 2 and potential +1/4. The trial
sines have zero boundary trace; their zero extensions belong to H1. Their
weak first derivatives have no boundary delta because the functions,
rather than their normal derivatives, have zero trace. The quadratic form
and L2 matrices are diagonal, supported in the exact product region. The
k-dimensional span has maximum quotient 1/4+(pi k/L)^2. The **full**
closed-manifold eigenvalue lambda_k (all multiplicities, indexed from 1)
is therefore bounded above by that number. This is not an asserted
identity of cylinder and global eigenfunctions, an angular-mode count,
or an improper fixed-index spectral-limit argument.

Finite partial heat sums satisfy the comparison term by term and extend
by monotone convergence. For a decreasing Gaussian f,
sum_{k>=1}f(k)>=integral_1^infinity f>=integral_0^infinity f-1,
giving L/(4 sqrt(pi))-1. Rescaling h=a g_L multiplies eigenvalues by a^-1;
the selected normalized time is t*=4a and the scaled prefactor is
8a^(3/2)=16pi^2/V_L. Retaining both factors yields the paper's positive
lower expression sqrt(pi)/e * (L-4sqrt(pi))/(L+4). The independently
implemented Fraction calculation in INDEPENDENT_ARITHMETIC.json checks
its exact stated rational lower and positive margin over 13/20.

## Round bound at every time

Degree j-1 round S3 harmonics have multiplicity j^2 and Laplace eigenvalue
j^2-1, so the Yamabe eigenvalue is j^2-1/4. Differentiating the full
Gaussian theta identity yields exactly the paper's sqrt(pi)/4 factor
and (1-2pi^2m^2/t) corrections. Gaussian convergence locally uniformly
for t>0 justifies this step. Every correction is negative through 7/5.

For j>=2 the derivative of t^(3/2)e^(-lambda_j t) is nonpositive from
t=2/5 onward; the first mode grows until 2. Starting the remaining tail
at j=3 gives ratio bounded by (16/9)e^(-7a)<1/2 for a>=7/5, so twice
the j=3 term gives 18e^(-35a/4). Thus A(b)+D(a) bounds each closed
middle interval, with no prefactor extrapolation in the wrong direction.
The seven table enclosures have been independently rebuilt with integer
square root and rational Taylor tails. Endpoints meet at 7/5,...,2 and
have no gaps. For t>=2 all round modes decrease, so the last row controls
all remaining times. These are analytic interval bounds, not samples.

## Actual maxima

Both fixed operators are positive elliptic Laplace-type geometric
operators on smooth compact manifolds, transferred by the displayed
unitary map. The scaled small-time trace is normalized volume/(4pi)^(3/2)
=sqrt(pi)/4. A strict positive gap and finite trace at time 1 imply an
exponentially decreasing heat-trace upper bound as t grows. The scaled
trace is continuous for t>0. The weighted finite-time value is greater
than 13/20, hence greater than its endpoint limit. At time 2 the round
first mode alone is 2sqrt(2)e^(-3/2)>sqrt(pi)/4; equivalently 128>pi e^3,
which the independent arithmetic verifies. Both suprema are therefore
attained on compact subintervals of (0,infinity). No monotonicity of the
weighted heat trace, numerical maximizer, or asymptotic family argument
is needed.

## Initial conclusion and exact boundary

The argument establishes an explicit finite admissible S3 counterexample
to the universal historical assertion. I found no unsupported central
analytic transfer. It is a finite quantitative application of classical
geometry and variational tools. The reconstruction does not establish a
new mechanism, exact historical priority, firstness, or current openness.
Source-version and package-contract checks follow separately.
