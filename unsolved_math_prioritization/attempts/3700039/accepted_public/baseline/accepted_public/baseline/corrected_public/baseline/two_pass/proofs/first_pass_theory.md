# First substantive pass: median inequality for three subharmonic functions

## Disposition and scope

**The general normalized-supremum conjecture is not resolved.** This report gives a precise denominator convention, a sharp universal fixed-radius bound, an exact harmonic diagnostic showing why the supremum cannot be replaced by an attained nonnegative value, and a finite-jet reduction. These results do not provide a counterexample to the conjecture.

The primary source is A. Eremenko, *Conjectured inequality for subharmonic functions*, 4 April 2015, https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. Both pages were read and visually inspected. The source's intended middle ordered value is used despite its notation slips. It credits the homogeneous and harmonic cases and separately asks for a stronger small-radius statement. Its power-growth condition concerns an application, not the general target. The finite-jet corollary below explicitly uses the credited homogeneous mechanism; no claim of priority is made for that corollary or the elementary inequalities here.

Throughout, `u_1,u_2,u_3` are subharmonic on the whole plane and `u_j(0)=0`. Set

- `v_2(z)=med(u_1(z),u_2(z),u_3(z))`;
- `I(r,v)=integral_0^(2*pi) v(r exp(i theta)) dtheta`, without averaging by `2*pi`;
- `B(r)=max_{|z|=r} max_j u_j(z)`.

## 1. Denominator classification and an explicit convention

### Proposition 1

For every `r>0`, `B(r)` is finite and nonnegative. Moreover,

`B(r)=0` if and only if all three functions vanish identically on the closed disk `|z|<=r`.

The function `B` is nondecreasing, continuous on `(0,infinity)`, and tends to zero as `r` decreases to zero. Consequently either all three functions vanish everywhere, or there is a finite `R_0>=0` such that

`D={r>0:B(r)>0}=(R_0,infinity)`.

When `R_0>0`, all three functions vanish on the closed disk of radius `R_0`.

**Proof.** Local upper bounds and upper semicontinuity give a finite maximum on each circle. The submean inequality at zero gives `0<=I(r,u_j)<=2*pi*B(r)`, hence `B(r)>=0`. If `B(r)=0`, the maximum principle gives `u_j<=0` in the disk. Each attains this maximum at zero, so the strong maximum principle gives `u_j=0` throughout the open disk. Upper semicontinuity at its boundary, together with the boundary upper bound zero, gives zero on the closed disk. The converse is immediate.

The maximum principle also proves monotonicity. Harmonic comparison with the function affine in `log|z|` on an annulus proves that `B(exp(t))` is a finite convex function of `t`, so `B` is continuous for positive radii. Upper semicontinuity at zero gives `limsup B(r)<=0`, and nonnegativity gives the limit zero. The stated alternatives follow from monotonicity, continuity, and the first assertion. QED.

### Convention used in this report

For every triple other than the globally zero triple, take the supremum of the actual quotient over its domain `D`, the positive-denominator radii. Treat the globally zero triple separately as a zero equality. This makes no arbitrary numerical assignment to `0/0` at the other radii.

The source does not specify a convention. This positive-denominator interpretation is a precise conservative formulation, not a claim that the source explicitly selected it. If one instead assigns quotient zero whenever `B=0`, any nontrivial flat-disk triple automatically satisfies the resulting supremum statement. That extension is weaker on such triples; equivalence to the positive-denominator formulation has **not** been proved here. Flat-disk triples remain genuine unresolved cases under the convention used here.

Under this convention, for a nonzero triple the exact denominator-free equivalent is

`for every epsilon>0 there exists r in D such that I(r,v_2)>=-epsilon*B(r)`.

The requirement `r in D` must not be dropped. Nor may this be replaced by the existence of a radius with `I(r,v_2)>=0`; Section 3 supplies an explicit counterexample to that reformulation. If `R_0>0`, the stronger small-radius limsup over `D` has no radii approaching zero; any assertion about it needs a separate convention.

## 2. The sharp universal fixed-radius bound

### Proposition 2

For every positive-denominator radius,

`-pi <= I(r,v_2)/B(r) <= 2*pi`.

The lower constant `-pi` is optimal, even among triples of entire harmonic polynomials with value zero at the origin. The upper constant is attained, for example, by `u_1=u_2=u_3=|z|^2`.

**Proof of the bounds.** Each `u_j` is bounded above on the circle. Its submean inequality excludes circle integral `-infinity`; hence it is integrable there and has nonnegative integral. For three finite numbers `a<=b<=c<=B`,

`a+b+c<=2*b+B`, hence `b>=(a+b+c-B)/2`.

Apply this almost everywhere on the circle and integrate:

`I(r,v_2)>=(I(r,u_1)+I(r,u_2)+I(r,u_3)-2*pi*B(r))/2>=-pi*B(r)`.

This inequality also proves integrability of the median. Its upper bound by `B(r)` proves the other endpoint. QED.

### Exact sharpness construction

Partition the circle, up to endpoints, into the three rotated arcs

`E_j={theta: |theta-2*pi*j/3|<pi/3 modulo 2*pi}`, `j=0,1,2`.

Let `g_j=1` on `E_j` and `g_j=-1/2` on its complement. At almost every angle the triple consists of `(1,-1/2,-1/2)` in some order. Thus each `g_j` has integral zero, their pointwise sum is zero, and their median is `-1/2`.

For `N>=1`, put `n=N+1` and use the nonnegative Fejer kernel

`F_N(t)=(1/n)*(sin(n*t/2)/sin(t/2))^2`, with integral `2*pi`.

Let `f_{j,N}=F_N*g_j`, with circular convolution normalized by `1/(2*pi)`. Its exact trigonometric polynomial is

`f_{j,N}(theta)=sum_{k=1}^N (1-k/n)*(3*sin(k*pi/3)/(pi*k))*cos(k*(theta-2*pi*j/3))`.

The corresponding entire harmonic polynomial is

`U_{j,N}(z)=sum_{k=1}^N (1-k/n)*(3*sin(k*pi/3)/(pi*k))*Re(exp(-2*pi*i*j*k/3)*z^k)`.

It has value zero at zero and restricts to `f_{j,N}` on the unit circle. Positivity and normalization of the kernel give `-1/2<=f_{j,N}<=1`. Its nonzero first Fourier coefficient gives `B_N=max_j max_theta f_{j,N}(theta)>0`, and `B_N<=1`.

Here is a quantitative proof requiring no unverified angular quadrature. For `|t|<=pi`,

`||g_j(. -t)-g_j||_1<=3*|t|`.

For `|t|<=2*pi/3`, this is the symmetric-difference length of two translated arcs multiplied by the jump `3/2`; beyond that range the bound follows from the maximum possible symmetric difference. Also,

`F_N(t)<=min(n, pi^2/(n*t^2))` for `0<|t|<=pi`.

The first bound follows from the geometric-sum expression of `F_N`; the second uses `sin(|t|/2)>=|t|/pi`. Splitting at `|t|=pi/n` gives

`integral_{-pi}^pi |t|*F_N(t) dt <= (pi^2/n)*(1+2*log n)`.

Consequently

`||f_{j,N}-g_j||_1 <= (3*pi/(2*n))*(1+2*log n)`.

The median is 1-Lipschitz for the maximum norm on triples, so

`|I(1,med U_{j,N})+pi| <= (9*pi/(2*n))*(1+2*log n)`.

As `N` tends to infinity, the integral tends to `-pi`. Because `0<B_N<=1`, for all sufficiently large `N` its negative quotient is no greater than its negative integral. Proposition 2 sandwiches that quotient between `-pi` and a sequence tending to `-pi`. This proves sharpness.

For an explicit finite certificate, take `N=9999`, `n=10000`. The positive exponential series gives

`exp(10) > sum_{k=0}^9 10^k/k! = 5719087/567 > 10000`,

so `log(10000)<10`. The relative error above is strictly less than

`9*(1+20)/(2*10000)=189/20000<1/100`.

It follows rigorously that this explicit degree-9999 harmonic triple satisfies

`I(1,med U_{j,9999})/B_9999 < -(99/100)*pi`.

This is a sharpness witness at one radius, **not a counterexample to the supremum conjecture**. Harmonic triples are a credited affirmative class.

## 3. Exact harmonic diagnostic: a negative integral at every radius

### Proposition 3

Let `omega=exp(2*pi*i/3)` and, for `j=0,1,2`, set

`u_j(z)=Re(omega^j*z+omega^(2*j)*z^2)`.

These entire harmonic functions have value zero at zero. For every `r>0`,

`B(r)=r+r^2`,

and their median has the exact integral

- `-3*sqrt(3)*r^2`, for `0<r<=1/2`;
- `3*sqrt(3)*(r^2-2*r+1/2)`, for `1/2<=r<=1`;
- `-3*sqrt(3)/2`, for `r>=1`.

Thus the integral is strictly negative at every positive radius, whereas the supremum of its normalized quotient is zero, not attained. Both the small-radius and large-radius normalized limits are zero. This example satisfies the conjecture; its role is to exclude an incorrect strengthening/reformulation.

### Complete sector and ordering derivation

On a circle, write `f_r(s)=r*s+r^2*(2*s^2-1)`. The three values are `f_r(cos(theta+2*pi*j/3))`. Their median is invariant under `theta -> theta+2*pi/3` and `theta -> -theta`, so its integral is six times its integral on `0<=theta<=pi/3`.

On that sector put

`x=cos theta`, `y=cos(theta-2*pi/3)`, `z=cos(theta+2*pi/3)`.

Then `x>=y>=z`, `x+y+z=0`, `1/2<=x<=1`, `-1/2<=y<=1/2`, and `-1<=z<=-1/2`. For any pair, the remaining coordinate controls the ordering:

`f_r(x)-f_r(y)=r*(x-y)*(1-2*r*z)`,

`f_r(y)-f_r(z)=r*(y-z)*(1-2*r*x)`,

`f_r(x)-f_r(z)=r*(x-z)*(1-2*r*y)`.

In particular `f_r(x)>=f_r(y)` throughout this sector. Let `c=1/(2*r)`.

1. If `r<=1/2`, then `c>=1` and the median is `f_r(y)` throughout the sector.
2. If `1/2<=r<=1`, put `alpha=arccos c`, so `0<=alpha<=pi/3`. The median is `f_r(z)` on `[0,alpha]` and `f_r(y)` on `[alpha,pi/3]`.
3. If `r>=1`, put `alpha=arccos c` and `beta=2*pi/3-alpha`, so `pi/6<beta<=pi/3`. The median is `f_r(z)` on `[0,beta]` and `f_r(x)` on `[beta,pi/3]`.

The formulas agree at equality boundaries, so ties cause no ambiguity.

Use the antiderivative

`integral [r*cos(theta+d)+r^2*cos(2*(theta+d))] dtheta = r*sin(theta+d)+(r^2/2)*sin(2*(theta+d))`.

For the three regimes the full circle integrals are, respectively,

`6*integral_0^(pi/3) f_r(y) dtheta = -3*sqrt(3)*r^2`,

`6*(integral_0^alpha f_r(z) dtheta + integral_alpha^(pi/3) f_r(y) dtheta)`

`=3*sqrt(3)*r*(-2*r*cos(alpha)^2+r+2*cos(alpha)-2)`

`=3*sqrt(3)*(r^2-2*r+1/2)`,

and

`6*(integral_0^beta f_r(z) dtheta + integral_beta^(pi/3) f_r(x) dtheta)`

`=3*sqrt(3)*r*(-r*sin(2*beta+pi/6)+r+2*cos(beta+pi/3))`

`=-3*sqrt(3)/2`.

For the last simplification, `beta=2*pi/3-alpha` gives `sin(2*beta+pi/6)=-cos(2*alpha)` and `cos(beta+pi/3)=-cos alpha`; substitute `cos alpha=1/(2*r)`.

Finally each value is at most `r+r^2`, with equality for `j=0,theta=0`, proving the formula for `B`. The middle quadratic decreases from `-1/4` to `-1/2` on `[1/2,1]`, so all three integrals are negative. Dividing the first and last formulas by `r+r^2` gives the claimed endpoint limits. QED.

## 4. A finite-jet reduction, using the credited homogeneous case

### Proposition 4

Suppose the three functions have a common finite-order Taylor expansion at zero, with the first nonzero homogeneous terms of their joint collection occurring at degree `m>=1`:

`u_j(z)=P_j(z)+o(|z|^m)` as `z->0`, uniformly in direction,

where each `P_j` is a homogeneous real polynomial of degree `m`, some possibly zero, and at least one nonzero. Then the normalized median quotient has a finite nonnegative limit as `r->0`.

In particular, any counterexample consisting of functions smooth near zero must have all three functions flat at zero. This is a necessary condition, not an existence claim or a solution of the flat case.

**Proof.** The locally uniform limit of `u_j(r*z)/r^m` is `P_j`; passing the submean inequality to that limit proves that each `P_j` is subharmonic. On the unit circle put `h_j(theta)=P_j(exp(i*theta))`. The polar Laplacian gives `h_j''+m^2*h_j>=0`. With `T=pi/m`, variation of constants yields

`h_j(theta+T)+h_j(theta)=(1/m)*integral_0^T sin(m*(T-s))*(h_j''+m^2*h_j)(theta+s) ds>=0`.

If `a_j+b_j>=0` for all three indices, then `med(b)>=med(-a)=-med(a)` by coordinatewise monotonicity. Apply this with the two angular triples and integrate to obtain a nonnegative median integral for the `P_j`. This is the source's credited homogeneous argument, specialized to polynomial leading terms.

Let `C=max_{|z|=1}max_j P_j(z)`. It is strictly positive: otherwise the maximum/strong maximum principle would force all `P_j` to vanish in the unit disk, contradicting the nonzero choice. Uniform expansion and the maximum-norm Lipschitz property of the median give

`B(r)/r^m -> C`,

`I(r,v_2)/r^m -> I(1,med P_j)`.

Their quotient tends to a nonnegative number. QED.

This includes every triple smooth near zero for which at least one function has a nonzero finite Taylor coefficient. It does not apply to arbitrary subharmonic functions, all-flat smooth triples, or nontrivial flat-disk triples.

## 5. Verification and remaining frontier

The exact sector integrals, two junctions, ordering-difference identities, exponential-series bound, and finite sharpness bound are stated in the [finite certificate](../certificates/first_pass_exact.json) and independently reconstructed in the [theory audit](../audits/first_theory_acceptance.md). Exact calculation checks supplement the analytic proofs; they do not certify the unresolved general assertion.

The companion construction work proves exclusions for common rotating-separable triples and for certain compact positive logarithmic potentials and records a log-periodic search reduction. Those are separate authored files; this report does not duplicate or silently strengthen them.

The unresolved target remains the general positive-denominator supremum assertion, with no finite-growth restriction. The exact harmonic diagnostic shows that persistent strict negativity of the unnormalized integral alone is insufficient for a counterexample. A counterexample needs one uniform `epsilon>0` for which `I(r,v_2)<=-epsilon*B(r)` on every positive-denominator radius. No such triple has been produced here, and no full proof has been claimed.
