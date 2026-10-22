# Proof 42  Validated one phase entropy quadrature

Included dependencies: [Exact one phase integration of the entropy kernel](14_one_phase_entropy.md); [Dominant endpoint entropy and nearby power comparisons](17_dominant_endpoint_entropy.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## 1. Normalize support and integrate one phase exactly

Consider

`P(Z,theta)=a Z+b/Z+w(theta)`, `a>0`, `b` real,

with `|P|<=1`, `|w'|<=L`, and `|w''|<=L` everywhere. For a two-pair centered cross normalized by the common coefficient-sum support bound `R`, one can take

`w(theta)=[c+d exp(i theta)+e exp(-i theta)]/R`,

`L=(|d|+|e|)/R`, `a=a_0/R`.

Let `F(theta)=E_Z K(P(Z,theta))`. The exact entropy formula computes every value of `F` from the two roots of `az^2+wz+b`; its SHA-256 is `6ba4304c78cf26263996475da83e6e8f54f4258bd55a27bdecf95ad91152b534` at [Exact one phase integration of the entropy kernel](14_one_phase_entropy.md).

We will prove the composite midpoint bound

`|E_theta F(theta) - (1/N) sum_(k=0)^(N-1) F(2pi(k+1/2)/N)|`

`<= [L^2(3-2 log a)+L] pi^2/(6N^2)`. (1)

For a sign gap of two such polynomials with common `a,L`, the error is therefore at most

`[L^2(3-2 log a)+L] pi^2/(3N^2)`. (2)

In particular, this bound does not infer convergence from comparing two grids.

## 2. Proof robust to zeros and root-boundary transitions

Put `r_epsilon=(|z|^2+epsilon^2)^(1/2)` and regularize

`K_epsilon(z)=(1/2)(|z|^2+epsilon^2)log(|z|^2+epsilon^2)`.

This converges uniformly to `K` on the closed unit disk. Its gradient is `(2 log r_epsilon+1)z`. Its Hessian has tangential eigenvalue `2 log r_epsilon+1` and radial eigenvalue `2 log r_epsilon+1+2|z|^2/(|z|^2+epsilon^2)`. Consequently

`||H K_epsilon(z)|| <= 2|log r_epsilon|+3`. (3)

Jensen's polynomial formula, or the constant Fourier coefficient in the accepted root formula, gives

`E_Z log|aZ+b/Z+w|=log a+sum_roots log max(1,|r_j|)>=log a`. (4)

The logarithmic singularities are integrable because `a>0` ensures the quadratic polynomial is not identically zero. Since `r_epsilon>=|P|` and `r_epsilon<=sqrt(1+epsilon^2)`,

`E_Z |log r_epsilon| <= log(1+epsilon^2)-log a`. (5)

Indeed `|x|=2 max(x,0)-x`, the positive part here is at most `(1/2)log(1+epsilon^2)`, and (4) bounds the average of `log r_epsilon` below. Also, for sufficiently small positive epsilon,

`sup_(|z|<=1) |grad K_epsilon(z)| <= sqrt(1+epsilon^2)[1+log(1+epsilon^2)]`, (6)

because `t|2log t+1|` on `0<=t<=sqrt(1+epsilon^2)` is maximized at the upper endpoint: the negative branch's absolute maximum is `2e^(-3/2)<1`.

The smooth conditional average `F_epsilon=E_Z K_epsilon(P)` therefore satisfies, by the chain rule and (3)-(6),

`|F_epsilon''(theta)| <= L^2[3-2log a+2log(1+epsilon^2)]`

`+ L sqrt(1+epsilon^2)[1+log(1+epsilon^2)]`.

Apply the standard midpoint Taylor remainder on each angular cell: for a twice differentiable function with second derivative bounded by `M`, the cell-average error is at most `M h^2/24`, where `h=2pi/N`. Now let epsilon tend to zero. Uniform convergence of `K_epsilon` to `K` passes both the integral and every sampled value to the limit, while the displayed bound tends to `M=L^2(3-2log a)+L`. This proves (1), then the triangle inequality proves (2). No differentiability claim at an individual zero or root-regime transition is required.

## 3. Interval implementation

[certify_entropy_quadrature.py](../certificates/certify_entropy_quadrature.py) uses mpmath real interval arithmetic at 45 decimal digits for every elementary arithmetic, square-root, logarithm, sine, cosine, and pi operation. Coefficients and normalization are exact rational inputs. A complex value is represented by a rectangle of real intervals.

A quadratic square root is enclosed using real formulas

`u=sqrt((|d|+Re d)/2)`, `v=sqrt((|d|-Re d)/2)`,

with the imaginary sign determined when possible, otherwise enclosing both signs. A small negative lower endpoint introduced by interval dependence is intersected with the mathematically proved nonnegative radicand. Both roots are used, so square-root branch ordering does not matter. If a root modulus interval crosses 1, the image of `tau(r)` is enclosed by the hull of the inside expression `r` and outside expression `1/conj(r)`. The relevant cases have no division enclosure containing zero. Every final interval is rounded outward to exact rational multiples of `10^-24` in the JSON output.

The trusted numerical dependency is mpmath's real interval primitives; this is a validated interval computation using those primitives, not a formally machine-checked proof of the library. The mathematical quadrature error (2) is added to the interval midpoint average. It is larger than the floating interval widths by many orders of magnitude.

## 4. Reproducible positive tests

Run:

`python certificates/certify_entropy_quadrature.py --N 256`

The exact coefficients, rational bounds, arithmetic precision, and analytic error are saved in [quadrature_certificates.json](../certificates/quadrature_certificates.json). All examples flip only the first pair.

1. `c=9/10`, `(a_0,b_0)=(1,2/5)`, `(a_1,b_1)=(4/5,3/10)`: the entropy gap is certified inside `(0.27479,0.27584)`. This is outside both the accepted dominant-center regime and the new dominant-endpoint regime.
2. `c=1`, `(a_0,b_0)=(4,1)`, `(a_1,b_1)=(1,1/2)`: the interval contains the independently exact gap `1/2` from the dominant-endpoint theorem.
3. `c=2/5`, `(a_0,b_0)=(1,7/10)`, `(a_1,b_1)=(7/8,1/5)`: the entropy gap is certified inside `(0.22750,0.22847)`, again outside both coefficient-dominance regimes.

These intervals rigorously certify the sign of the selected comparisons under the stated interval-arithmetic dependency and analytic error proof. A positive normalized lower endpoint can be substituted for delta in the Taylor estimate of [Dominant endpoint entropy and nearby power comparisons](17_dominant_endpoint_entropy.md), yielding a certified prescribed-power neighborhood above 2 for that exact sign comparison. It does not certify the full coefficient box without separately treating every sign vertex, and it does not certify all added-circle radii.
