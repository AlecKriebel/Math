# A converse with one independently specified positive remainder function

Authored mathematical argument, 14 October 2026. This theorem addresses a separate proposed interpretation of the Hardy–Rellich remainder. The same positive function is fixed independently for every test, with no ODE assumption in the premise. It is not the literal source reading in which the function is already an ODE solution. No full informal-source resolution, novelty, or human-review claim is made.

## 1. Statement and quantifiers

Let $n\geq1$, $Q=n+2\geq3$, $0<R\leq\infty$, and use

\[
\rho=(|x|^4+4t^2)^{1/4},\quad
\psi=|x|^2/\rho^2,\quad
\nabla_G=(\nabla_x,|x|\partial_t),\quad
L_G=\Delta_x+|x|^2\partial_t^2,\quad
B_R=\{\rho<R\}.
\]

For $u\in\mathcal T_R=C_c^\infty(B_R\setminus\{0\};\mathbb R)$, the source radial derivative is

\[
u_\rho=\frac{x\cdot\nabla_xu+2t\,\partial_tu}{\rho}.
\tag{1}
\]

Suppose

\[
V\in C^1(0,R),\quad V>0,\qquad
W\in C^1(0,R;\mathbb R),
\]

and there is one fixed $g\in C^2(0,R)$ with $g>0$ such that, for every $u\in\mathcal T_R$,

\[
A_V[u]\geq D_{V,W}[u]+E_{V,g}[u],
\tag{2}
\]

where

\[
\begin{aligned}
A_V[u]&=\int_{B_R}V(\rho)\frac{(L_Gu)^2}{\psi}\,dz,\\
D_{V,W}[u]&=\int_{B_R}
\left[W(\rho)+(Q-1)
\left(\frac{V(\rho)}{\rho^2}-\frac{V'(\rho)}{\rho}\right)\right]
|\nabla_Gu|^2\,dz,\\
E_{V,g}[u]&=\int_{B_R}V(\rho)g(\rho)^2
\left|\nabla_G\left(\frac{u_\rho}{g(\rho)}\right)\right|^2\,dz.
\end{aligned}
\tag{3}
\]

Interpret $A_V$ as the nonnegative extended integral of the off-axis quotient. Both $D_{V,W}$ and $E_{V,g}$ are finite on each source test: all relevant coefficients and derivatives are bounded on its compact supporting annulus, $g$ has a positive minimum there, and $u_\rho$ is smooth away from the origin. No axis is removed from the test class.

**Theorem.** Under these assumptions:

1. The independently specified $g$ is a positive supersolution:
   \[
   (r^{Q-1}Vg')'+r^{Q-1}Wg\leq0
   \qquad(0<r<R).
   \tag{4}
   \]
2. There exists a possibly different strictly positive flux-classical solution $f$ on all of $(0,R)$ of
   \[
   (r^{Q-1}Vf')'+r^{Q-1}Wf=0.
   \tag{5}
   \]

The coefficient of $W$ is exactly one. No sign restriction on $W$, no side condition involving $V''$, and no endpoint condition are needed. Historical $Q=3$ is included. The conclusion does not assert that the given $g$ itself solves (5).

The premise must use the same $g$ for every test. A test-dependent choice $g=g_u$ is not covered.

## 2. Finite radial tests and the exact identity

Put $p=r^{Q-1}V$ and $q=r^{Q-1}W$. For a real $v\in C_c^\infty(0,R)$, let $u=v\circ\rho$ and $w=v'$. As established directly in the [Hardy proof, Section 3](HARDY_CONVERSE_PROOF.md), this is a smooth admissible source test even on the nonzero axis. The exact gauge-polar formulas are

\[
\psi\,dz=\tfrac12r^{Q-1}(\sin\theta)^{n/2}\,dr\,d\theta\,d\omega,
\qquad
c_n=\frac{|S^{n-1}|}{2}\int_0^\pi(\sin\theta)^{n/2}\,d\theta>0,
\tag{6}
\]

with counting measure on $S^0$ when $n=1$. Direct differentiation gives

\[
|\nabla_Gu|^2=\psi w^2,\qquad
L_Gu=\psi\left(w'+\frac{Q-1}{r}w\right),\qquad
u_\rho=w.
\tag{7}
\]

For these radial tests, the quotient $(L_Gu)^2/\psi$ equals
$\psi(w'+(Q-1)w/r)^2$ off the axis and has a finite, zero-valued extension there. Thus the use of (2) on these tests does not exploit an automatic inequality with infinite left side.

Expanding (7), using (6), and integrating the cross term by parts on the compact supporting interval gives the exact cancellation

\[
\frac{A_V[v\circ\rho]-D_{V,W}[v\circ\rho]}{c_n}
=\int_0^R(pw'^2-qw^2)\,dr.
\tag{8}
\]

The cancellation uses only $V\in C^1$: the cross term is
$2(Q-1)\int r^{Q-2}Vww'$, whose integral by parts cancels precisely the correction in (3). No $V''$ appears.

The remainder also reduces exactly:

\[
\frac{E_{V,g}[v\circ\rho]}{c_n}
=\int_0^R p g^2\left|\left(\frac wg\right)'\right|^2\,dr.
\tag{9}
\]

Its angular factor is the same $c_n$, so no coefficient is lost.

The derivatives of compactly supported $v$ are exactly those
$w\in C_c^\infty(0,R)$ with zero ordinary integral. Indeed, necessity is immediate, and for sufficiency the primitive $v(r)=\int_0^r w(s)\,ds$ vanishes both near zero and beyond the support of $w$.

Consequently (2) implies

\[
\int_0^R(pw'^2-qw^2)\,dr
-\int_0^Rpg^2\left|\left(\frac wg\right)'\right|^2\,dr\geq0
\tag{10}
\]

for every compactly supported smooth $w$ satisfying $\int_0^R w\,dr=0$.

## 3. Cancellation reduces the question to a multiplication coefficient

Let

\[
a(r)=\frac{g'(r)}{g(r)}.
\]

All relevant quantities are continuously differentiable locally because $p\in C^1$, $g\in C^2$, and $g>0$. Expansion of the second square gives

\[
pg^2\left|\left(\frac wg\right)'\right|^2
=p(w'-aw)^2.
\]

Using compact support to integrate the cross term,

\[
\begin{aligned}
&\int(pw'^2-qw^2)\,dr-\int p(w'-aw)^2\,dr\\
&\quad=\int\left[-q-(pa)'-pa^2\right]w^2\,dr\\
&\quad=\int\left[-q-\frac{(pg')'}g\right]w^2\,dr.
\end{aligned}
\tag{11}
\]

Define the continuous function

\[
K(r)=-q(r)-\frac{(p(r)g'(r))'}{g(r)}.
\tag{12}
\]

Thus (10) says $\int K w^2\geq0$ for all compactly supported smooth zero-mean $w$. There is no longer a derivative cost that could make localization problematic.

Suppose $K(r_*)<0$ at an interior point. By continuity there is a nonempty open interval $J\Subset(0,R)$ containing $r_*$ on which $K<0$. Choose any nonzero $\chi\in C_c^\infty(J)$ and let $w=\chi'$. Then $w\not\equiv0$, $w\in C_c^\infty(J)$, and $\int w=0$. Hence

\[
\int_0^R K(r)w(r)^2\,dr<0,
\]

contradicting (10). Therefore $K\geq0$ pointwise on all of $(0,R)$. Multiplying (12) by $g>0$ gives exactly (4).

This step preserves the zero-integral restriction rather than claiming it is irrelevant or dense in an unspecified norm. Local derivatives provide enough tests once the derivative terms have canceled.

## 4. From the supersolution to a positive exact solution

For every unrestricted $h\in C_c^\infty(0,R)$, the same integration-by-parts identity gives

\[
\int_0^R(ph'^2-qh^2)\,dr
=\int_0^Rpg^2\left|\left(\frac hg\right)'\right|^2\,dr
 +\int_0^R K h^2\,dr\geq0.
\tag{13}
\]

Now apply the self-contained one-dimensional positivity lemma proved in the [Hardy proof, Section 4](HARDY_CONVERSE_PROOF.md). Its hypotheses are $p>0$, $p\in C^1$, $q\in C$, and exactly the nonnegative form (13). It supplies a positive exact solution $f$ on the entire fixed interval $(0,R)$ of $(pf')'+qf=0$. The construction uses normalized shooting and a single convergent initial-flux subsequence across all compact interior intervals; it does not merely give a supersolution or solutions on separate annuli.

The solution is flux-classical, and in fact $C^2$ under these coefficients. Neither (11) nor (13) has an endpoint term because all tests are compactly supported inside the interval. This completes the proof.

## 5. Scope, source relationship and limits

- The argument uses only gauge-radial tests from the full antecedent. More precisely, the radial version of (2), with one fixed $g$, is equivalent to the supersolution condition (4): necessity is Sections 2–3, and sufficiency for those radial tests follows from (11). No corresponding all-test sufficiency is claimed without additional hypotheses.
- This is a proposed independent-function remainder branch. GJR's literal source theorem instead begins with $g$ already a positive ODE solution; that reading assumes the desired Bessel-pair conclusion. [GJR v1, Theorem 1.3, p.6](https://arxiv.org/pdf/2404.05510v1), [GJR v3, Theorem 1.3, p.7](https://arxiv.org/pdf/2404.05510v3)
- Unlike the remainder-free nonnegative-$W$ theorem, this proof works for every real $W$ and for historical $Q=3$, because the remainder eliminates the derivative term before the zero-integral constraint is localized.
- An independently specified positive function is not thereby an exact ODE solution. The immediate conclusion is the one-sided inequality (4); the positive exact solution (5) comes from a separate, established one-dimensional positivity theorem proved in the accompanying Hardy manuscript.
- No status of the overall informal OWR question is inferred solely from this branch. The source's intended remainder quantifier remains a formulation issue.
