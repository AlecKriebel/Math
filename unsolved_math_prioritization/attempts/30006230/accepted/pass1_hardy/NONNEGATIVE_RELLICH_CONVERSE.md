# A nonnegative-potential Hardy–Rellich converse

Authored mathematical argument, 14 October 2026. This is a theorem for the explicitly proposed remainder-free Hardy–Rellich antecedent. It is separate from both the source-faithful Hardy theorem and any counterexample with negative potential. It does not claim a full resolution of the informal Oberwolfach question, novelty, or human peer review.

## 1. Exact statement

Use the single-vertical-variable Grushin setting

\[
z=(x,t)\in\mathbb R^n\times\mathbb R,\quad
Q=n+2,\quad
\rho=(|x|^4+4t^2)^{1/4},\quad
\psi=|x|^2/\rho^2,\quad
\nabla_G=(\nabla_x,|x|\partial_t),\quad
L_G=\Delta_x+|x|^2\partial_t^2.
\]

Let $n\geq2$, equivalently $Q\geq4$, and fix $0<R\leq\infty$. Assume

\[
V\in C^2(0,R),\quad V>0,\qquad
W\in C^1(0,R),\quad W\geq0,
\]

and the source weight side condition

\[
S_Q[V](r):=(Q-5)\frac{V(r)}{r^2}
             +3\frac{V'(r)}r-V''(r)\geq0
\qquad(0<r<R).
\tag{S}
\]

For every real $u\in\mathcal T_R=C_c^\infty(B_R\setminus\{0\})$, suppose

\[
\int_{B_R} V(\rho)\frac{(L_Gu)^2}{\psi}\,dz
\geq
\int_{B_R}
\left[
W(\rho)+(Q-1)\left(\frac{V(\rho)}{\rho^2}
                         -\frac{V'(\rho)}{\rho}\right)
\right]|\nabla_Gu|^2\,dz.
\tag{HR}
\]

The left side is the nonnegative extended integral of the off-axis quotient; the axis has Lebesgue measure zero. Thus infinite-energy tests satisfy (HR) automatically. The right side is finite for each source test.

**Theorem.** These hypotheses imply a strictly positive flux-classical solution on the entire fixed interval $(0,R)$ of

\[
\bigl(r^{Q-1}V(r)f'(r)\bigr)'
       +r^{Q-1}W(r)f(r)=0.
\tag{B}
\]

The coefficient of $W$ is exactly one. There are no added endpoint assumptions, including at $R=\infty$. No boundary value, limit, integrability or boundedness condition is imposed on $f$ at either endpoint.

In fact, the proof needs (HR) only for the gauge-radial source tests; it does not replace the all-test premise by a restricted statement silently. It establishes the implication from this weaker, explicitly identified premise, so in particular establishes the displayed all-test converse.

The source GJR Theorem 1.3 has an additional remainder involving an already positive ODE solution. Removing that remainder is the proposed solution-free formulation (HR), not a newly discovered formula in the OWR paragraph. The nonnegative $W$ restriction here is explicit and excludes a general real-valued-$W$ conclusion. [GJR v3, p.7](https://arxiv.org/pdf/2404.05510v3), [OWR 14/2025, printed p.606](https://ems.press/content/serial-article-files/51358?nt=1)

## 2. Exact radial reduction, including the axis and the primitive constraint

The exact gauge-polar calculation in the [Hardy theorem, Sections 3–5](HARDY_CONVERSE_PROOF.md) gives

\[
\psi\,dz=\frac12 r^{Q-1}(\sin\theta)^{n/2}\,dr\,d\theta\,d\omega,
\qquad
c_n=\frac{|S^{n-1}|}{2}\int_0^\pi(\sin\theta)^{n/2}\,d\theta>0.
\tag{1}
\]

For any $v\in C_c^\infty(0,R)$, the test $u=v\circ\rho$ is smooth at every nonzero point, including points on $x=0,t\neq0$, and belongs to the original source class. Direct differentiation gives

\[
|\nabla_Gu|^2=\psi\,v'(\rho)^2,\qquad
L_Gu=\psi\left(v''(\rho)+\frac{Q-1}{\rho}v'(\rho)\right).
\tag{2}
\]

Consequently the quotient in the left side of (HR) agrees off the axis with

\[
\psi\left(v''(\rho)+\frac{Q-1}{\rho}v'(\rho)\right)^2,
\]

which has a bounded, zero-valued extension on the axis inside the compact supporting annulus. The weight is bounded there as well. Thus every radial test used below has finite Hardy–Rellich energy, with no removal of the axis from its support.

Set

\[
p=r^{Q-1}V,\qquad q=r^{Q-1}W,\qquad w=v'.
\]

By (1)–(2), division by the same $c_n$ reduces (HR) to

\[
\int_0^R p\left(w'+\frac{Q-1}{r}w\right)^2\,dr
\geq
\int_0^R
\left[q+(Q-1)\left(r^{Q-3}V-r^{Q-2}V'\right)\right]w^2\,dr.
\tag{3}
\]

The exact identity is

\[
\begin{aligned}
&\int_0^R p\left(w'+\frac{Q-1}{r}w\right)^2\,dr\\
&\quad-(Q-1)\int_0^R
         \left(r^{Q-3}V-r^{Q-2}V'\right)w^2\,dr
=\int_0^R p\,w'^2\,dr.
\end{aligned}
\tag{4}
\]

To verify it, integrate the cross term as

\[
2(Q-1)\int r^{Q-2}Vww'\,dr
=-(Q-1)\int
  \left((Q-2)r^{Q-3}V+r^{Q-2}V'\right)w^2\,dr.
\]

The $V'$ terms cancel, and the $V/r^2$ coefficient is
$(Q-1)[(Q-1)-(Q-2)-1]=0$. All functions in this integration are compactly supported in an interior interval, so there is no endpoint limit.

It follows that

\[
\mathfrak q[w]:=\int_0^R(pw'^2-qw^2)\,dr\geq0
\quad\text{whenever }w\in C_c^\infty(0,R)
\text{ and }\int_0^R w\,dr=0.
\tag{5}
\]

Here the zero-integral condition is essential at this stage. Conversely, every compactly supported smooth $w$ with zero ordinary integral is an allowed derivative: its primitive

\[
v(r)=\int_0^r w(s)\,ds
\]

is zero near zero and beyond the support of $w$, and belongs to $C_c^\infty(0,R)$. Thus (5) is exactly what the radial restriction supplies, rather than an inequality on an improperly enlarged test class.

## 3. The side condition forces an upper growth bound at zero

Put

\[
k=\sqrt{Q-1}>0,\qquad
U(t)=e^{-2t}V(e^t),\qquad t<\log R.
\]

When $R=\infty$, the last upper endpoint is $+\infty$. With $r=e^t$, direct differentiation yields

\[
V(r)=r^2U(t),\qquad
V'(r)=r(2U+U'),\qquad
V''(r)=2U+3U'+U''.
\]

Therefore

\[
S_Q[V](r)=(Q-1)U(t)-U''(t).
\tag{6}
\]

Hypothesis (S) is precisely $U''\leq k^2U$, and $U>0$.

Fix any $r_0\in(0,R)$ and $t_0=\log r_0$. Define

\[
Y(s)=U(t_0-s)\quad(s\geq0),\qquad
F(s)=k^2Y(s)-Y''(s)\geq0.
\]

Variation of constants for $Y''-k^2Y=-F$ gives the exact formula

\[
Y(s)=Y(0)\cosh(ks)+\frac{Y'(0)}k\sinh(ks)
     -\frac1k\int_0^s\sinh(k(s-\sigma))F(\sigma)\,d\sigma.
\tag{7}
\]

For each finite $s$, all coefficients and integrals in (7) are continuous on a compact interval. No assumption on $U$ at $-\infty$ was used. Since the kernel and $F$ are nonnegative, the final term is nonpositive. It follows that

\[
0<Y(s)\leq
\left(Y(0)+\frac{|Y'(0)|}k\right)e^{ks}
\qquad(s\geq0).
\]

Returning to $r$, we obtain

\[
V(r)\leq C r^{2-k}\qquad(0<r\leq r_0),
\quad
C=r_0^k\left(U(t_0)+\frac{|U'(t_0)|}k\right)<\infty.
\tag{8}
\]

This upper bound is a consequence of the source side condition and positivity of $V$, not an added endpoint hypothesis. In particular,

\[
p(r)=r^{Q-1}V(r)\leq C r^{Q+1-k}.
\tag{9}
\]

## 4. Unit-integral bumps with vanishing derivative energy

Choose once and for all a real nonnegative $\eta\in C_c^\infty(1,2)$ with
$\int_1^2\eta(s)\,ds=1$. For $0<2\delta<r_0$, set

\[
\eta_\delta(r)=\delta^{-1}\eta(r/\delta).
\]

Then $\eta_\delta\in C_c^\infty(\delta,2\delta)$,
$\int_0^R\eta_\delta\,dr=1$, and (9) gives

\[
\begin{aligned}
\int_0^R p(r)\eta_\delta'(r)^2\,dr
&\leq C\,\delta^{Q-2-k}
       \int_1^2 s^{Q+1-k}\eta'(s)^2\,ds\\
&=:C_\eta\,\delta^\beta,\qquad
\beta=Q-2-\sqrt{Q-1}.
\end{aligned}
\tag{10}
\]

For every integer $Q\geq4$, $\beta>0$: writing $a=Q-2\geq2$, the condition becomes $a>\sqrt{a+1}$, which follows from $a^2-a-1>0$. Hence the derivative energy in (10) tends to zero as $\delta\downarrow0$.

For each fixed $\delta$, the potential energy is finite because the bump has compact support inside $(0,R)$ and $W$ is continuous there. Its size need not be bounded uniformly in $\delta$. The only estimate needed is the one-sided inequality, using $W\geq0$,

\[
\mathfrak q[\eta_\delta]
=\int p\eta_\delta'^2\,dr-\int q\eta_\delta^2\,dr
\leq C_\eta\,\delta^\beta.
\tag{11}
\]

Thus arbitrary positive growth of $W$ at zero causes no gap in this argument. We do not claim convergence of $\mathfrak q[\eta_\delta]$ to zero from both sides.

## 5. Remove the constraint and obtain the exact positive solution

Let $h\in C_c^\infty(0,R)$ be arbitrary, and write

\[
m=\int_0^R h(r)\,dr.
\]

Choose $\delta$ small enough that $\operatorname{supp}\eta_\delta$ is disjoint from $\operatorname{supp}h$. The corrected test

\[
w_\delta=h-m\eta_\delta
\]

is smooth, compactly supported in $(0,R)$, and has zero ordinary integral. Its primitive is therefore an admissible radial test in Section 2. Disjointness of the supports, including their derivatives, gives the exact split

\[
0\leq\mathfrak q[w_\delta]
=\mathfrak q[h]+m^2\mathfrak q[\eta_\delta]
\leq\mathfrak q[h]+m^2C_\eta\delta^\beta.
\tag{12}
\]

Letting $\delta\downarrow0$ proves

\[
\mathfrak q[h]\geq0\qquad(h\in C_c^\infty(0,R)).
\tag{13}
\]

This does not assert a density theorem in a norm involving $W$; the one-sided bound (11) and exact disjoint decomposition are sufficient. If $m=0$, (13) already follows from (5).

Now apply the self-contained [one-dimensional positivity lemma in the Hardy proof, Section 4](HARDY_CONVERSE_PROOF.md), with the same
$p=r^{Q-1}V$ and $q=r^{Q-1}W$. Its hypotheses hold and it constructs a strictly positive exact solution of $(pf')'+qf=0$ on all of $(0,R)$. Briefly, form nonnegativity rules out two interior zeros by a truncated-solution polarization argument; shooting from $a_j\downarrow0$, normalizing at one interior point, and bounding the initial flux at two nearby points produce one globally consistent subsequential limit. Interior uniqueness makes the nonnegative normalized limit strictly positive. There is no loss from a solution to a supersolution, no change in the coefficient of $W$, and no shrinking of the fixed interval.

This proves (B).

## 6. Exact scope and additional consequences

1. **Nonnegative $W$ is a real restriction.** The argument uses its sign precisely in (11). With negative $W$ near zero, the potential contribution to a shrinking correction bump can be positive and arbitrarily large. Nothing here proves the same conclusion for unrestricted real $W$.
2. **A slightly stronger, explicitly identified version.** The proof actually needs $W\geq0$ only on some neighborhood $(0,\varepsilon)$ of zero, and permits real $W$ elsewhere. Similarly, it uses (S) only near zero. Thus these local sign/side-condition hypotheses suffice for the same necessity implication; they are observations about the proof, not silently added source assumptions.
3. **Historical $Q=3$ is not proved here.** In that case $\beta=1-\sqrt2<0$, so the bump estimate fails to vanish. This is a failure of this particular construction, not a counterexample and not a proof of an obstruction. The separate Hardy theorem covers $Q=3$, but it cannot repair the missing implication from the constrained form (5) to (13) in this branch.
4. **Independent positive remainder.** Any well-defined stronger premise (HR) with an additional nonnegative term on its right, including a fixed independently specified positive-function remainder, implies the core premise. Therefore the same conclusion follows under the present $Q,V,W$ hypotheses. This conclusion does not assert that the independently chosen function itself solves (B).
5. **The literal source remainder is different.** If its function is already stipulated to be a positive solution of (B), the desired property is already assumed. That circular reading is not the theorem proved here.
6. **No numerical certification.** Exact symbolic checks can verify the algebraic identities (4) and (6) and the scaling exponent; they do not replace the compact-support, sign, growth, or global positivity arguments.

The result disposes of the proposed regular-leading-weight, nonnegative-$W$, $Q\geq4$ HR core branch with the source side condition and no extra endpoint assumptions. Other branches of the informal source question retain their own precise disposition.
