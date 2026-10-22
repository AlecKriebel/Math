# Exact degenerate-leading-weight addendum

14 October 2026. Authored independent audit observations within the same shared PASS1. These concern literal nonnegative leading weights and are separate from every regular \(V>0\) theorem.

## 1. Both Hardy premises can hold with a positive potential and an isolated zero of V

Fix any \(Q=n+2\ge3\), \(0<R\le\infty\), and \(a\in(0,R)\). Set
\[
V(r)=r^{1-Q}(r-a)^2,\qquad W(r)=\tfrac14r^{1-Q}.
\]
These profiles are smooth on the open interval, \(V\ge0\), and \(W>0\). Their one-dimensional form has the exact identity
\[
\int_0^R\left((r-a)^2v'^2-\tfrac14v^2\right)\,dr
=\int_0^R\left((r-a)v'+\tfrac12v\right)^2\,dr\ge0
\qquad(v\in C_c^\infty(0,R)).
\]
The cross term is integrated globally over the compact support; no boundary is introduced at \(r=a\). The already audited polar-ray calculation proves the source radial-gradient Hardy inequality for every original spatial test. Since \(V\ge0\) and \(\psi|u_\rho|^2\le|\nabla_Gu|^2\), the full-gradient Hardy inequality also follows for every test.

The target equation is
\[
((r-a)^2f')'+\tfrac14f=0.
\]
For a flux-classical solution with \(f\in C^1(0,R)\), the derivative of its flux at \(a\) equals
\[
\lim_{h\to0}h f'(a+h)=0.
\]
The equation forces \(f(a)=0\). Therefore there is no strictly positive such solution on the full interval. The positive sign of \(W\) alone does not repair the literal Hardy converse when zeros of the leading weight are admitted. This example does not satisfy the Hardy–Rellich side condition at \(a\) and makes no such claim.

## 2. The classical Hardy–Rellich side condition excludes isolated zeros

Suppose \(V\in C^2(0,R)\), \(V\ge0\), and \(S_Q[V]\ge0\). Put \(t=\log r\), \(U(t)=r^{-2}V(r)\), and \(k=\sqrt{Q-1}\). The exact transformed inequality is
\[
U''-k^2U\le0,\qquad U\ge0.
\]
If \(U(t_0)=0\), differentiability and nonnegativity imply \(U'(t_0)=0\). Variation of constants with these initial data shows \(U(t)\le0\) both to the right and left of \(t_0\): in either direction the resulting integral has a nonnegative kernel multiplying \(U''-k^2U\le0\). This holds on every finite interior interval. Hence \(U\equiv0\), and therefore \(V\equiv0\).

Consequently, in this explicitly classical side-conditioned class, either \(V>0\) everywhere or \(V\equiv0\). This claim does not assign a meaning to \(V''\) for merely \(C^1\) weights.

## 3. The identically zero leading weight is completely elementary

Use the announced off-axis extended-integral convention. If \(V\equiv0\), then both Hardy left sides, the Hardy–Rellich left side, its \(V'\) correction, and every fixed-independent-function remainder are zero. Each of the corresponding all-test premises holds if and only if \(W\le0\) pointwise:

- Sufficiency follows immediately from the sign of the right side.
- If \(W>0\) at some radius, choose a nonzero smooth spatial test supported in a small neighborhood of an off-axis point at that radius, entirely inside the region where \(W>0\). The relevant right side is strictly positive, contradicting the premise.

In contrast, the coefficient-one Bessel equation becomes \(r^{Q-1}Wf=0\). A strictly positive full-interval solution exists if and only if \(W\equiv0\). Thus \(V=0,W=-1\) is an exact obstruction for all three literal necessity readings, including a fixed independent positive remainder function, while \(V=W=0\) is not an obstruction.

These facts preserve the distinction between a degenerate branch and the regular mathematical problem. They do not alter the meaning of the literal source remainder, which already assumes its positive ODE solution, and do not by themselves resolve the source's intended formulation.
