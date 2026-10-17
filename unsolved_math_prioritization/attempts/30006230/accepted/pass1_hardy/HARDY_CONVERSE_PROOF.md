# The regular-weight Hardy converse for the Grushin gauge

Authored mathematical argument, 14 October 2026. This document addresses the two Hardy displays in GJR Corollary 3.1. It does not decide a Hardy–Rellich converse or claim a full resolution of the informal Oberwolfach question. The one-dimensional positivity argument is classical Sturm/Allegretto–Piepenbrink theory, proved here to fix its exact hypotheses and conclusion. No novelty or human-review claim is made.

## 1. Precise result

Let $n\geq1$, $Q=n+2$, and $0<R\leq\infty$. For $z=(x,t)\in\mathbb R^n\times\mathbb R$, set

\[
\rho=(|x|^4+4t^2)^{1/4},\qquad
\psi=|\nabla_G\rho|^2=\frac{|x|^2}{\rho^2},\qquad
\nabla_G=(\nabla_x,|x|\partial_t),\qquad
B_R=\{\rho<R\}.
\]

All spatial tests below are real elements of

\[
\mathcal T_R=C_c^\infty(B_R\setminus\{0\}).
\]

The radial derivative is the derivative along the source's gauge-polar rays:

\[
u_\rho=\frac{x\cdot\nabla_xu+2t\partial_tu}{\rho}.
\tag{1}
\]

In particular, it is not the ordinary derivative with respect to $|x|$. The source radial gradient has squared norm $|\nabla_{\rho,G}u|^2=\psi|u_\rho|^2$.

**Theorem.** Suppose $V\in C^1(0,R)$ is strictly positive and $W\in C^1(0,R)$ is real-valued. The following four assertions are equivalent:

1. For every $u\in\mathcal T_R$,
   \[
   \int_{B_R}V(\rho)|\nabla_Gu|^2\,dz
   \geq\int_{B_R}W(\rho)\psi u^2\,dz.
   \tag{H_G}
   \]
2. For every $u\in\mathcal T_R$,
   \[
   \int_{B_R}V(\rho)\psi|u_\rho|^2\,dz
   \geq\int_{B_R}W(\rho)\psi u^2\,dz.
   \tag{H_\rho}
   \]
   This assertion quantifies over all source tests, not just gauge-radial ones.
3. For every real $v\in C_c^\infty(0,R)$,
   \[
   \int_0^R r^{Q-1}\bigl(V(r)|v'(r)|^2-W(r)|v(r)|^2\bigr)\,dr\geq0.
   \tag{H_1}
   \]
4. There is a strictly positive flux-classical solution on the entire fixed interval $(0,R)$ of
   \[
   \bigl(r^{Q-1}V(r)f'(r)\bigr)'+r^{Q-1}W(r)f(r)=0.
   \tag{B_Q}
   \]
   Here flux-classical means $f\in C^1(0,R)$ and $r^{Q-1}Vf'\in C^1(0,R)$, with the equation pointwise. Under the displayed hypotheses $f\in C^2(0,R)$.

The coefficient of $W$ is exactly one. There is no sign assumption on $W$, and no condition on $V,W,f$ at either endpoint. In particular $f$ need not extend continuously, remain bounded, or satisfy an integrability or boundary-value condition at $0$, at a finite $R$, or at infinity. The proof works for the historical $n=1,Q=3$ case as well as the newer $n\geq2,Q\geq4$ range. It does not use spherical harmonics or a dimension-dependent spectral formula.

In fact, the same proof permits real $W\in C(0,R)$. We state the main theorem with the source's $C^1$ weight class. No stronger regularity of $V$ is used.

## 2. Source alignment

Ganguly–Jotsaroop–Roychowdhury (GJR), arXiv:2404.05510v1, Definition 2.2 and Corollary 3.1, use the $Q$-dimensional equation and the two displays above, with $Q\geq3$. The corresponding v3 statements use $Q\geq4$. Both source corollaries assume $V\geq0$ and the Bessel-pair property to obtain the inequalities. The theorem here reverses both displays in the explicitly restricted regular-leading-weight class $V>0$, and also re-establishes sufficiency without importing endpoint assumptions. [GJR v1, pp.13–14](https://arxiv.org/pdf/2404.05510v1), [GJR v3, pp.14–16](https://arxiv.org/pdf/2404.05510v3)

The OWR question is an informal converse question for both Hardy and Hardy–Rellich inequalities, not one fully quantified theorem. Its cited Hardy–Rellich display contains a positive ODE solution in its remainder. The present theorem says nothing about how that second antecedent should be formulated. [OWR 14/2025, printed p.606](https://ems.press/content/serial-article-files/51358?nt=1)

## 3. Exact polar integration and admissible radial tests

Write $\theta\in(0,\pi)$, $\omega\in S^{n-1}$, and use

\[
x=r\sqrt{\sin\theta}\,\omega,\qquad
t=\frac{r^2}{2}\cos\theta.
\tag{2}
\]

Then $\rho=r$ and $\psi=\sin\theta$. For $n=1$, $S^0=\{-1,1\}$ has counting measure, so the same formula consists of two coordinate sheets. It covers the complement of the axis $x=0$, a Lebesgue null set. This is only a coordinate omission, not a deletion from the test class.

For $s=|x|=r\sqrt{\sin\theta}$, direct differentiation gives

\[
\left|\frac{\partial(s,t)}{\partial(r,\theta)}\right|
=\frac{r^2}{2\sqrt{\sin\theta}}.
\]

Multiplication by the Euclidean radial factor $s^{n-1}$ yields the exact measure

\[
dz=\frac12 r^{n+1}(\sin\theta)^{(n-2)/2}\,dr\,d\theta\,d\omega
=\frac12 r^{Q-1}(\sin\theta)^{(n-2)/2}\,dr\,d\theta\,d\omega.
\tag{3}
\]

Thus

\[
\psi\,dz=\frac12r^{Q-1}(\sin\theta)^{n/2}\,dr\,d\theta\,d\omega.
\tag{4}
\]

These are precisely the source polar measure and its weighted version, derived here also for $n=1$. The unweighted angular exponent is then $-1/2$, which is integrable; the weighted exponent is $1/2$. The factor $1/2$ is retained throughout. [GJR v1, pp.9–10](https://arxiv.org/pdf/2404.05510v1)

For $v\in C_c^\infty(0,R)$, let $u(z)=v(\rho(z))$. The function $\rho$ is smooth at every nonzero point, including $x=0,t\neq0$, since $|x|^4+4t^2>0$ there. If $\operatorname{supp}v\subset[a,b]\Subset(0,R)$, then $u$ is smooth, vanishes near the origin and outside the compact gauge annulus $a\leq\rho\leq b$, and hence belongs to the original $\mathcal T_R$. In particular, we have not restricted tests away from the axis.

The gauge is homogeneous for $\delta_s(x,t)=(sx,s^2t)$. Differentiating along (2) proves (1), and gives $u_\rho=v'(\rho)$. The ordinary chain rule gives

\[
|\nabla_Gu|^2=\psi|v'(\rho)|^2.
\tag{5}
\]

Define the finite, strictly positive constant

\[
c_n=\frac{|S^{n-1}|}{2}\int_0^\pi(\sin\theta)^{n/2}\,d\theta
=\frac{\pi^{(n+1)/2}\Gamma((n+2)/4)}{\Gamma(n/2)\Gamma((n+4)/4)}.
\tag{6}
\]

Equations (4)–(6) imply the exact identities

\[
\begin{aligned}
\int V(\rho)|\nabla_G(v\circ\rho)|^2\,dz
&=\int V(\rho)\psi|(v\circ\rho)_\rho|^2\,dz
=c_n\int_0^Rr^{Q-1}V|v'|^2\,dr,\\
\int W(\rho)\psi(v\circ\rho)^2\,dz
&=c_n\int_0^Rr^{Q-1}Wv^2\,dr.
\end{aligned}
\tag{7}
\]

Every integral is finite because the supports lie in an interior compact annulus. Consequently either $H_G$ or $H_\rho$, separately, implies $H_1$ after cancelling the same positive $c_n$. There is no altered coefficient in front of $W$.

## 4. A self-contained one-dimensional positivity lemma

**Lemma.** Let $I=(0,R)$, $0<R\leq\infty$, $p\in C^1(I)$ with $p>0$, and $q\in C(I;\mathbb R)$. If

\[
\mathfrak q[v]:=\int_I(pv'^2-qv^2)\,dr\geq0
\qquad(v\in C_c^\infty(I;\mathbb R)),
\tag{8}
\]

then there exists $f>0$ on all of $I$ with

\[
(pf')'+qf=0.
\tag{9}
\]

The solution is $C^2(I)$, and may be normalized to $f(r_0)=1$ at any prescribed $r_0\in I$.

### 4.1 Compactly supported Sobolev tests

On any compact subinterval of $I$, $p,q$ are bounded and $p$ has a positive lower bound. By ordinary mollification inside a slightly larger compact subinterval, (8) extends to every $H^1$ function compactly supported in $I$. The associated bilinear form

\[
\mathfrak b[v,h]=\int_I(pv'h'-qvh)\,dr
\]

is continuous on that local $H^1$ space. If such a $v$ satisfies $\mathfrak q[v]=0$, positivity of

\[
\mathfrak q[v+\varepsilon h]=2\varepsilon\mathfrak b[v,h]+\varepsilon^2\mathfrak q[h]
\]

for both signs of arbitrarily small $\varepsilon$ proves $\mathfrak b[v,h]=0$ for every compactly supported $H^1$ test $h$.

### 4.2 No nonzero solution has two interior zeros

Suppose a nonzero solution $y$ of (9) has $y(a)=y(b)=0$ with $0<a<b<R$. Extend its restriction to $[a,b]$ by zero outside $[a,b]$, obtaining $v\in H^1_c(I)$. Integration by parts gives

\[
\mathfrak q[v]=\int_a^b(py'^2-qy^2)\,dr
=[py'y]_a^b=0.
\]

The preceding polarization argument implies $\mathfrak b[v,\eta]=0$ for every $\eta\in C_c^\infty(I)$. But integration by parts in $[a,b]$ gives

\[
\mathfrak b[v,\eta]=[py'\eta]_a^b.
\]

Choose $\eta(a)=1$, $\eta(b)=0$. It follows that $p(a)y'(a)=0$. The initial data $y(a)=y'(a)=0$ force $y\equiv0$, a contradiction. Thus any nonzero solution has at most one zero in $I$. This step rules out the possibly zero Dirichlet energy on a smaller subinterval; mere nonnegativity on that subinterval would not by itself rule it out.

Existence and uniqueness used here are elementary for the linear first-order system

\[
\binom{y}{h}'=\begin{pmatrix}0&1/p\\-q&0\end{pmatrix}\binom{y}{h},
\qquad h=py'.
\tag{10}
\]

Its coefficient matrix is continuous and bounded on each compact interior interval. Local solutions extend uniquely across every such interval, by the usual integral equation and Gronwall bound, and hence throughout the open interval $I$. No extension to either endpoint is asserted or needed.

### 4.3 Positive solutions on an exhaustion

Fix $r_0\in I$, and choose $a_k\downarrow0$ with $a_k<r_0$. Let $y_k$ be the global solution of (9) with

\[
y_k(a_k)=0,\qquad p(a_k)y_k'(a_k)=1.
\]

Its derivative at $a_k$ is positive, so $y_k>0$ immediately to the right. It cannot vanish again, by Section 4.2. Therefore

\[
y_k>0\quad\text{throughout }(a_k,R).
\tag{11}
\]

Normalize $f_k=y_k/y_k(r_0)$, so $f_k(r_0)=1$. These functions are positive on the nested intervals $(a_k,R)$, whose union is the entire desired $I$. Each right-hand interval really reaches every $r<R$: it is not a fixed small neighborhood of $r_0$, and it does not stop at an unspecified first zero. For a conventional two-sided compact exhaustion, choose any $b_j\uparrow R$ (or $b_j\uparrow\infty$); every $[a_j,b_j]\Subset I$ eventually lies in the positivity region of every sufficiently large $f_k$.

### 4.4 A single convergent initial-data subsequence works on all intervals

Let $C,S$ be the global fundamental solutions of (9) specified by

\[
C(r_0)=1,\quad p(r_0)C'(r_0)=0,
\qquad
S(r_0)=0,\quad p(r_0)S'(r_0)=1.
\]

Every normalized $f_k$ has the form

\[
f_k=C+d_kS,\qquad d_k=p(r_0)f_k'(r_0).
\tag{12}
\]

Since $S'(r_0)>0$, choose fixed interior points $r_-<r_0<r_+$ close enough to $r_0$ that $S(r_-)<0<S(r_+)$. For all sufficiently large $k$, (11) holds at both points. Consequently

\[
-\frac{C(r_+)}{S(r_+)}<d_k<-\frac{C(r_-)}{S(r_-)}.
\tag{13}
\]

Thus the initial fluxes have a convergent subsequence, $d_{k_j}\to d$. Set $f=C+dS$. Equation (12) implies convergence to $f$ in $C^2$ on every compact subinterval, along this same subsequence; no compatibility problem between separate annular limits remains. In particular, $f$ solves the exact equation (9), not a supersolution inequality or a shifted spectral equation, and $f(r_0)=1$.

For every $r\in I$, eventually $a_{k_j}<r$, so $f_{k_j}(r)>0$. Hence $f(r)\geq0$ for every $r\in I$. If $f(s)=0$ at an interior point, nonnegativity and differentiability give $f'(s)=0$, and uniqueness in (10) would force $f\equiv0$, contradicting $f(r_0)=1$. Thus $f>0$ throughout $I$, proving the lemma.

**Why no endpoint hypothesis appears.** Every integral, density argument, comparison point and ODE uniqueness statement in the proof occurs in a compact subset of $I$. The moving $a_k$ are interior zero initial data for approximating solutions, not a boundary condition imposed on the limit. A common initial-data limit provides the global solution even if coefficients or the resulting solution are singular at either endpoint.

## 5. Apply the lemma and recover both all-test inequalities

Set

\[
p(r)=r^{Q-1}V(r),\qquad q(r)=r^{Q-1}W(r).
\]

Then $p>0$, $p\in C^1(I)$, and $q\in C(I)$. Assertion $H_1$ is exactly (8), so the lemma proves $B_Q$ with coefficient one and positivity on all of $(0,R)$.

For completeness the reverse implication follows from the ground-state identity. If $f>0$ solves $(pf')'+qf=0$, direct expansion and compact-support integration by parts give, for $v\in C_c^\infty(I)$,

\[
\int_I(pv'^2-qv^2)\,dr
=\int_Ipf^2\left|\left(\frac vf\right)'\right|^2\,dr\geq0.
\tag{14}
\]

Indeed, writing $v=fh$, the cross term and the remaining $h^2$ term are the total derivative $(pff'h^2)'$, which integrates to zero. All terms are supported in a compact interior interval, so no endpoint boundary term has been discarded by an unproved limit.

Now take any $u\in\mathcal T_R$. Its support is contained in one gauge annulus $[a,b]\Subset(0,R)$. For each fixed $(\theta,\omega)\in(0,\pi)\times S^{n-1}$,

\[
v_{\theta,\omega}(r)
=u\left(r\sqrt{\sin\theta}\,\omega,\frac{r^2}{2}\cos\theta\right)
\]

is a smooth compactly supported one-variable test with support inside that same $[a,b]$, and $v_{\theta,\omega}'=u_\rho$. Apply $H_1$, or (14), on every ray, then integrate against $\tfrac12(\sin\theta)^{n/2}d\theta d\omega$. Formula (4) and Fubini give $H_\rho$ for all $u\in\mathcal T_R$, and in fact

\[
\int_{B_R}\left(V(\rho)\psi|u_\rho|^2-W(\rho)\psi u^2\right)dz
=\int_{B_R}V(\rho)f(\rho)^2\psi
\left|\partial_\rho\!\left(\frac{u}{f(\rho)}\right)\right|^2dz.
\tag{15}
\]

Fubini applies without an improper-energy qualification: $V,W,f,1/f,f'$ are bounded on the supporting radial interval, and $u,u_\rho$ are bounded there; all angular measures in (3)–(4) are finite for $n\geq1$. In particular the axis does not create an infinite-energy Hardy test.

Finally, a pointwise calculation away from $x=0$ gives

\[
\nabla_Gu\cdot\nabla_G\rho=\psi u_\rho.
\]

Cauchy–Schwarz and $|\nabla_G\rho|^2=\psi$ imply

\[
\psi|u_\rho|^2\leq|\nabla_Gu|^2.
\tag{16}
\]

At $x=0,t\neq0$ the left side is zero, so the same inequality holds there directly. Since $V>0$, integrating (16) proves $H_G$ from $H_\rho$. Together with (7), the lemma and (14), this completes every implication in the theorem.

One can also recover the full-gradient identity directly, but it is unnecessary for necessity: radial restriction, the one-dimensional lemma, and raywise integration already establish equivalence of both source premises.

## 6. Literal nonnegative leading weights: a separate obstruction

If the source's printed $V\geq0$ class is interpreted literally without regularity or nondegeneracy conventions beyond $C^1$, the unconditional converse is false. For any $n\geq1$ and any fixed $0<R\leq\infty$, choose

\[
V(r)=0,\qquad W(r)=-1.
\]

Both Hardy inequalities hold for every source test: their left sides are zero and their right sides are nonpositive. But the desired equation becomes

\[
-r^{Q-1}f(r)=0,
\]

which has no strictly positive solution under any classical, flux-classical, or distributional interpretation compatible with multiplication by this smooth nonzero coefficient.

The issue is not confined to an identically zero coefficient. Under the explicit $C^1$, flux-classical convention used above, choose an interior $a\in(0,R)$ and

\[
V(r)=r^{1-Q}(r-a)^2,\qquad W(r)=-r^{1-Q}.
\tag{17}
\]

These are smooth on $(0,R)$, $V\geq0$, and $V>0$ except at one radius. Again both Hardy displays hold for all tests simply because $W<0$. The target equation is

\[
\bigl((r-a)^2f'(r)\bigr)'-f(r)=0.
\]

For $f\in C^1$, the derivative of the flux at $a$ is zero:

\[
\lim_{h\to0}\frac{h^2f'(a+h)-0}{h}=0.
\]

The equation at $a$ therefore forces $f(a)=0$. It cannot have a strictly positive flux-classical solution on the whole interval. This second example uses the stated solution convention; the $V\equiv0$ example is independent of that subtlety.

These examples settle only that literal degenerate branch. They are not obstructions to the regular theorem and are not presented as the intended full solution of the OWR question. They also use negative $W$; no conclusion about an independently imposed $W>0$ degenerate branch is inferred from them.

## 7. Known theory, inspection record and boundaries

The one-dimensional equivalence between nonnegative quadratic form and positive solution is classical disconjugacy/Allegretto–Piepenbrink theory. Section 4 supplies all details needed here rather than invoking a general theorem whose closure, global form bounds or endpoint conventions might differ. The ground-state transformation (14) is likewise standard. Thus the contribution of the argument here is an explicit source-matched reduction and a complete proof under the announced hypotheses, not a claim of a new abstract positivity principle.

For contextual attribution, Lenz–Stollmann–Veselić, *The Allegretto–Piepenbrink Theorem for Strongly Local Dirichlet Forms*, Theorem 2.3, gives a ground-state representation. Their Theorem 3.3 gives positive weak solutions below the spectral bottom under irreducibility, local compactness, noncompactness and a Harnack principle; Theorem 3.7 handles the spectral bottom under a uniform Harnack principle. Those statements were inspected directly. They are background, not black-box inputs to Section 4, and no assertion is made that all of their global form hypotheses have been verified for every present weight. [Versioned primary manuscript](https://arxiv.org/pdf/0811.2135v2)

Theorem 2.1 of the inspected Ghoussoub–Moradifam author manuscript treats a Euclidean Hardy equivalence with positive $V,W$, specific endpoint integral assumptions and an unpunctured-ball test class. It is an important cited precedent, but those are not the assumptions of the source punctured Grushin tests. The proof above neither imports their endpoint assumptions nor uses their Bessel scale convention to replace coefficient one. The inspected 2007 manuscript is not asserted identical to the eventual journal version. [Ghoussoub–Moradifam, arXiv:0709.1954v1, p.5](https://arxiv.org/pdf/0709.1954v1), [journal DOI](https://doi.org/10.1007/s00208-010-0510-x)

Primary statements inspected for this argument:

- GJR v1: polar coordinates and measure, pp.9–10; Definition 2.2, p.13; both Corollary 3.1 displays, p.14.
- GJR v3: both Corollary 3.1 displays, p.16, checked against the recovered version-specific statement map.
- Ghoussoub–Moradifam v1: Theorem 2.1, p.5, and the following endpoint lemma, to verify why it should not be imported wholesale.
- Lenz–Stollmann–Veselić v2: Theorems 2.3, 3.3 and 3.7, as contextual attribution rather than an unproved implication used here.

**Exact outcome:** both regular-leading-weight Hardy necessity branches are proved for all historical dimensions and the complete fixed open interval, with real $W$, exact normalization and no endpoint assumptions. A separate literal-degenerate counterexample is supplied. Hardy–Rellich formulations and the overall informal question are outside this theorem's resolution claim.
