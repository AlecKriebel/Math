# Attempt 3: local stability for non-colliding thin triangles

Status: a qualitative local theorem with a quantitative proof in terms of a
positive potential-gradient constant. It does not cover all degenerating
triangles and does not resolve the conjecture.

Use the unit segment `S=[0,1] x {0}` and its p-capacitary potential `u` in the
homogeneous Sobolev class, with value one on `S` and zero at infinity. Write
`c_p=C_p(S)`, `q=2-p`, `r=p-1`. The potential, unlike the smooth compactly
supported test functions in the definition, is an equilibrium minimizer in the
completed energy space. This distinction is important.

## 1. An energy defect under enlargement

For a compact set `K` containing `S`, let `v` be its capacitary potential,
extended by one on `K`. The standard capacitary measure identity is

\[
 \int |\nabla u|^{p-2}\nabla u\cdot\nabla\phi=\int\phi\,d\mu_S,
\]

where `mu_S` is supported on `S`, and does not charge sets of zero p-capacity.
Both potentials equal one quasi-everywhere on `S`, so testing with `v-u`
(by finite-energy approximation) gives zero. Consequently

\[
 C_p(K)-c_p=\int D_p(\nabla v,\nabla u),
\quad D_p(a,b)=|a|^p-|b|^p-p|b|^{p-2}b\cdot(a-b).             \tag{1}
\]

Convexity gives `D_p>=0`; on the interior of `K`, `grad v=0`, so
`D_p(0,grad u)=(p-1)|grad u|^p`. Thus

\[
 C_p(K)-c_p\geq(p-1)\int_K|\nabla u|^p.                       \tag{2}
\]

This is stronger than bare monotonicity. It does not assume uniform convexity
with a false p-power lower bound when `p<2`.

For completeness, the measure identity used here follows from the Euler
inequality for the capacitary obstacle problem: `-div(|grad u|^(p-2)grad u)`
is a nonnegative distribution supported on `S`, hence a measure, and the
finite-energy pairing extends to differences with zero quasi-everywhere trace
on `S`. The identity is for the full homogeneous Sobolev energy space, not for
an assertion that the infimum has a minimizer in `C_c^1`.

## 2. A fixed strip with positive gradient

There are constants `eta_p>0` and `m_p>0` such that

\[
 |\nabla u(x,y)|\geq m_p
 \quad\text{for }1/4\leq x\leq3/4,\quad0<y<\eta_p.           \tag{3}
\]

Here are the standard local ingredients, stated explicitly. The segment is
regular for the p-Dirichlet problem for `p>1`. On either open flat side, `1-u`
has zero boundary value and positive interior value. Odd reflection across the
line gives local `C^{1,alpha}` regularity for the reflected p-harmonic function.
The Hopf boundary lemma gives a strictly positive inward derivative of `1-u`
at every point of the open segment. It can also be obtained by a radial
p-harmonic annular barrier in an exterior disk tangent to the segment.
Compactness of `[1/4,3/4]` and continuity of the gradient prove (3).
No endpoint regularity or endpoint asymptotic is needed.

## 3. Compare thin triangles with their same-perimeter segments

Let

\[
 T_{\alpha,h}=\operatorname{conv}\{(0,0),(1,0),(\alpha,h)\},
 \quad\delta\leq\alpha\leq1-\delta,
 \quad0<\delta\leq1/2.
\]

For every `alpha` in `[0,1]`, the roof over `x` has height at least
`h*min(x,1-x)`. In particular the rectangle

`[1/4,3/4] x [0,h/4]`

lies in the triangle and has area `h/8`. If `h/4<=eta_p`, equations (2)--(3)
give

\[
 C_p(T_{\alpha,h})-c_p\geq\frac{(p-1)m_p^p}{8}\,h.            \tag{4}
\]

On the other hand, its perimeter is

\[
 P=1+\sqrt{\alpha^2+h^2}+\sqrt{(1-\alpha)^2+h^2}.
\]

Using `sqrt(x^2+h^2)<=x+h^2/(2x)` and the concavity of `t^q`,

\[
 C_p(I_P)-c_p=c_p[(P/2)^q-1]
 \leq\frac{c_pq}{4\delta(1-\delta)}h^2.                      \tag{5}
\]

Therefore

\[
 C_p(T_{\alpha,h})>C_p(I_{P(T_{\alpha,h})})
\]

whenever

\[
 0<h<\min\left\{4\eta_p,
 \frac{(p-1)m_p^p\delta(1-\delta)}{2c_p(2-p)}\right\}.        \tag{6}
\]

This proves strict segment comparison for all sufficiently thin triangles
whose third-vertex projection stays a fixed positive fraction away from both
endpoints. Scaling and rigid motions give the analogous statement for an
arbitrary base.

## Scope and exact unresolved regimes

The result is local, and its threshold is implicit in the segment potential.
It does not give an explicit numerical uniform neighborhood of all segments.
When `alpha` tends to zero with `h`, the quadratic perimeter bound in (5)
deteriorates; the perimeter increment can be order `h`. The proof above must
not be extended to that regime by silently holding `delta` fixed. It also says
nothing about triangles bounded away from degeneration. Both regimes remain
part of the original conjecture.
