# Attempt 2: an explicit elliptic-coordinate segment bound

Status: a second proved partial bound, not a solution of segment minimality.
We improve the segment upper comparison entering Attempt 1. No assertion of
novelty for the elliptic test-function method is made.

Let `q=2-p`, `r=p-1`, and `b_p=2*pi*(q/r)^r`. For the unit segment with endpoints
`(-1/2,0)` and `(1/2,0)`, use elliptic coordinates

\[
 x=\tfrac12\cosh\mu\cos\nu,\qquad
 y=\tfrac12\sinh\mu\sin\nu,
 \quad \mu>0,\ 0\leq\nu<2\pi.
\]

The common scale factor is
`h=(1/2)*sqrt(sinh(mu)^2+sin(nu)^2)`. The map covers the exterior of the segment
once up to the harmless angular seam. A function `U(mu)` has energy

\[
 \int_0^\infty |U'(\mu)|^p A_q(\mu)\,d\mu,\quad
 A_q(\mu)=2^{-q}\int_0^{2\pi}
       (\sinh^2\mu+\sin^2\nu)^{q/2}\,d\nu.                  \tag{1}
\]

Hölder's inequality, or direct one-dimensional minimization, shows that the
infimum of this restricted energy with `U(0)=1` and `U(infinity)=0` is

\[
 U_p^{\rm exact\ trial}
  =\left[\int_0^\infty A_q(\mu)^{-1/r}\,d\mu\right]^{-r}.
                                                               \tag{2}
\]

This is an UPPER bound on the true capacity `c_p`, not an exact capacity formula.
The integral is finite: `A_q(0)>0` and `A_q(mu)` grows like a positive constant
times `exp(q*mu)` at infinity. To ensure admissibility, keep the function equal
to one on an inner ellipse `mu<=epsilon`, truncate at `mu=M`, and minimize on
`[epsilon,M]`. The coordinates are regular on that annulus. Smooth transitions
preserve the limiting energy; then let `epsilon` tend to zero and `M` to infinity.
Thus endpoint singularities of elliptic coordinates create no assumption about
an unattained minimizer in the original compactly supported smooth class.

## 1. Remove the angular integral rigorously

Because `0<q/2<1`, Jensen's inequality for the concave power gives

\[
 A_q(\mu)\leq2\pi\,2^{-q}(\sinh^2\mu+\tfrac12)^{q/2}
 =2\pi\,2^{-3q/2}\cosh(2\mu)^{q/2}.                         \tag{3}
\]

The exponent `-1/r` reverses this bound inside the integral in (2), and the
outer power `-r` reverses it again. Therefore

\[
 c_p\leq U_p^{\rm ell}:=2\pi\,2^{-3q/2}J(q/(2r))^{-r},
 \quad J(k)=\int_0^\infty\cosh(2\mu)^{-k}\,d\mu
 =\frac{\sqrt\pi\,\Gamma(k/2)}{4\Gamma((k+1)/2)}.              \tag{4}
\]

The beta-integral identity follows by `t=tanh(2*mu)`, then `s=t^2`.
Retain the better of this and the distance-to-segment bound:

\[
 U_p=\min\{b_p\pi^{-q},\ U_p^{\rm ell}\},\qquad
 \kappa_p=\frac1\pi\left(\frac{b_p}{U_p}\right)^{2/q}\geq\pi.
                                                               \tag{5}
\]

There is no need to assume that (4) beats the distance bound for every `p`;
indeed it does not near `p=1`.

## 2. The resulting all-shapes comparison

For a perimeter-two triangle of area `A` and longest side `a`, precisely the
same division as in Attempt 1 gives

\[
 C_p(T)/c_p\geq\max\{a,\sqrt{\kappa_p A}\}^{q}.               \tag{6}
\]

Define `rho_p` as the unique root in `(2/3,1)` of

\[
 \rho_p^2=\kappa_p(1-\rho_p)\sqrt{2\rho_p-1}.                 \tag{7}
\]

The root exists because `kappa_p>=pi` and is unique by monotonicity. The Heron
minimax proof in Attempt 1 now yields

\[
 \boxed{C_p(K)\geq\rho_p^{2-p}C_p(I_{P(K)})}.                 \tag{8}
\]

This is an exact formula involving gamma functions and a one-variable root.
Floating-point evaluation is optional and is not part of its proof.

## 3. An elementary special exponent

At `p=4/3`, `q=2/3`, `r=1/3` and `J(1)=pi/4`. Thus

\[
 U_{4/3}^{\rm ell}=(4\pi^2)^{1/3},\qquad \kappa_{4/3}=4.
\]

The latter uses `4>pi`, so the elliptic bound is the smaller choice in (5).
Consequently the original conjecture at this exponent has the proved partial
factor `rho_{4/3}^{2/3}`, where `rho_{4/3}` is the unique root of

\[
 \rho^4=16(1-\rho)^2(2\rho-1),\qquad 2/3<\rho<1.
\]

Squaring is legitimate because both sides of (7) are positive. This quartic
provides an algebraic, independently checkable special case.

## Remaining gap

Even the strengthened factor is below one. The elliptic test function is not
claimed to satisfy the nonlinear p-Laplace equation, and the geometric minimax
does not imply a capacitary equality case. The exact segment value, exclusion
of nondegenerate minimizing triangles, and full conjecture remain unresolved.
