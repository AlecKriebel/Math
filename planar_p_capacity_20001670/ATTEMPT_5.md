# Attempt 5: the global affine-squeezing obstruction

Status after five substantive attempts: **UNRESOLVED**, with the partial
theorems in Attempts 1--4. This attempt investigates the remaining nonthin
triangles via exact bulk variation identities. It does not count review or
packaging as an additional proof turn.

Let `q=2-p`. Fix a triangle with base endpoints `(0,0),(1,0)` and third vertex
`(alpha,h)`, and set `T_t=diag(1,t)T`. Let `u_t` denote its equilibrium potential
and `C(t)=C_p(T_t)`. Pulling back to the fixed exterior of `T` gives the
variational family

\[
 C(t)=\inf_v\int t(v_x^2+t^{-2}v_y^2)^{p/2}.                 \tag{1}
\]

The trace is fixed in this formulation. Strict convexity gives a unique
minimizing gradient. The elementary envelope argument tests the nearby
functional at the old minimizer for the upper derivative, and the old
functional at the new minimizer for the lower derivative. The needed STRONG
gradient convergence follows from uniform convexity, as follows.

Write `F_t(v)` for the energy in (1). If `t_j -> t>0` and `v_j` minimizes
`F_{t_j}`, the transformed gradient norms are uniformly equivalent on a
compact positive t-interval. Comparison at the old and new minimizers gives
continuity of the minimum and `F_t(v_j) -> F_t(v_t)`. Coercivity gives weak
subsequential convergence in the homogeneous energy space; the fixed
quasi-everywhere trace class is weakly closed. Weak lower semicontinuity and
uniqueness identify every weak limit with the gradient of `v_t`.

For the FIXED linear transformation
`L_t g = t^(1/p)*(g_x,t^(-1)*g_y)`, this means that `L_t grad v_j` converges
weakly to `L_t grad v_t` in `L^p`, while its `L^p` norm converges to the norm
of that limit, because its p-th power is `F_t(v_j)`. The Radon--Riesz property
of the uniformly convex space `L^p`, valid for `1<p<infinity`, upgrades this
to strong convergence. Invertibility of `L_t` then gives strong convergence
of the original gradients. Strict convexity alone would not justify this step.
The parameter derivative of the integrand is continuous and bounded by a
constant times the p-th power of the gradient on the same t-interval; strong
`L^p` convergence and uniform integrability justify the two-sided envelope
limit. Thus

\[
 \frac{tC'(t)}{C(t)}=1-pM_y(t),\quad
 M_y(t)=\frac{\int|\nabla u_t|^{p-2}(u_t)_y^2}{C(t)}.         \tag{2}
\]

The integrand is taken as zero where the gradient is zero; it is bounded in
absolute value by `|grad u_t|^p`. In particular `0<=M_y<=1`.

## 1. Exact normalized derivative and missing inequality

Put

\[
 b_t=\sqrt{\alpha^2+t^2h^2},\quad
 d_t=\sqrt{(1-\alpha)^2+t^2h^2},\quad P(t)=1+b_t+d_t.
\]

Then

\[
 \tau(t):=\frac{tP'(t)}{P(t)}
 =\frac{t^2h^2}{P(t)}\left(\frac1{b_t}+\frac1{d_t}\right),
\]

and the scale-invariant objective satisfies

\[
 \frac{d}{d\log t}\log\frac{C(t)}{P(t)^q}
       =1-pM_y(t)-q\tau(t).                                 \tag{3}
\]

Therefore a sufficient global flattening theorem would be

\[
 M_y(t)\leq\frac{1-(2-p)\tau(t)}p                            \tag{4}
\]

for triangles whose horizontal base is a longest side. Such a theorem, integrated
from `t=0` using Hausdorff continuity, would prove the original conjecture.
Neither the capacity Brunn--Minkowski inequality nor the bound `0<=M_y<=1`
establishes (4). An upper bound on capacity obtained by transporting a trial
potential also cannot simply be differentiated into the needed derivative
inequality for the actual minimizer. Equation (4) remains an unsupported
sufficient condition, so this global route is blocked.

## 2. A nontrivial exact endpoint check

For the segment `S`, vertical stretching leaves the set exactly unchanged.
Applying the same envelope argument to `diag(1,t)S=S` makes the left side of
(2) zero. Hence its full-plane energy tensor satisfies

\[
 \int|\nabla u_S|^{p-2}(u_S)_y^2=\frac{c_p}{p},\qquad
 \int|\nabla u_S|^{p-2}(u_S)_x^2=\frac{p-1}{p}c_p.             \tag{5}
\]

This distinguishes the slit from an isotropic conductor. It is consistent with
the limiting value `tau(0)=0` in the proposed inequality, but a limiting equality
does not prove its sign away from the slit.

## 3. Why the simplest equilateral second-variation test fails

Let `T` be equilateral and use the area-preserving deformation
`A_s=diag(exp(s),exp(-s))`. Its threefold rotational symmetry makes its
equilibrium energy tensor isotropic. Transporting its ORIGINAL potential gives
the explicit upper bound

\[
 C_p(A_sT)\leq E(s):=\int(e^{-2s}u_x^2+e^{2s}u_y^2)^{p/2}.
\]

The first derivative at zero vanishes. Direct differentiation gives

\[
 E''(0)=2pC_p(T)+p(p-2)\int|\nabla u|^{p-4}(u_y^2-u_x^2)^2
       =\frac{p(p+2)}2C_p(T).                               \tag{6}
\]

The final equality uses threefold rotational symmetry: the average of the
fourth angular harmonic is zero, hence the squared directional difference
integral equals `C_p(T)/2`. These derivative integrands are dominated by a
constant times the original p-energy, so differentiation is valid.

For the perimeter, summing its three edge lengths under the same deformation
gives `P'(0)=0` and `P''(0)=3*P(0)/2`. Consequently the transported upper
comparison `E(s)/P(A_sT)^q` has second derivative, relative to its value at zero,

\[
 \frac{p(p+2)}2-\frac{3(2-p)}2
       =\frac{(p-1)(p+6)}2>0.                               \tag{7}
\]

A positive-curvature upper bound touching the true objective does not rule out
a local minimum. The relaxation of the potential under the deformation is
precisely the missing second-order information. Thus this common trial-function
shortcut cannot exclude even the equilateral triangle as a minimizer.

## Final mathematical boundary

Established in this package, subject to fresh independent review:

1. An all-convex-sets comparison with constant `rho=0.7472461733...` in place
   of the supplied `2/3`, and an explicit stronger p-dependent version.
2. A strict segment comparison for all sufficiently thin triangles, including
   third-vertex collisions with the base endpoints, for each fixed `p`.
3. The exact segment energy-tensor identities (5) and global squeezing identity
   (3), with the unproved inequality isolated in (4).

Not established: global segment minimality, exclusion of nonthin triangles,
an explicit uniform local threshold, an exact segment-capacity formula, or
priority of these partial results. The original problem must not be marked
solved.
