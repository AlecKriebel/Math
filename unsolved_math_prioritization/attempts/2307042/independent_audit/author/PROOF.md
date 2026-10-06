# An annular Martin kernel with isolated contact at the base point

## Result and scope

Let

\[
D=\{z\in\mathbb C:1<|z|<e\},\qquad a=e^{1/2},\qquad \xi=-1.
\]

Let \(K_\xi\) be the minimal Martin kernel of \(D\) at the inner-boundary point \(\xi\), normalized by \(K_\xi(a)=1\), and let

\[
H_a(z)=\sup\{h(z):h>0\text{ harmonic on }D,\ h(a)\leq1\}.
\]

**Theorem.** There is a neighborhood \(U\) of \(a\) such that

\[
K_\xi(z)<H_a(z)\qquad(z\in U\setminus\{a\}).
\tag{1}
\]

Consequently there is no nonconstant continuous curve issuing from \(a\) on which \(K_\xi=H_a\), even for an initial segment. In particular there is no such Green line. This gives a negative answer to the extension asked in Hayman--Lingham, Problem 7.42, with “along a Green line issuing from the base point” understood as the equality-along-the-line property explicitly exhibited there for a disc radius. Equality just at the base point is automatic for every normalized kernel and is not the property being tested. The theorem does not assert absence of contact farther away from \(a\).

This is an authored candidate proof, requiring independent review. No assertion of historical novelty or priority is made.

## 1. Cylinder coordinates and the kernel

Use logarithmic coordinates

\[
z=e^{x+iy},\qquad 0<x<1,\quad y\in\mathbb R/(2\pi\mathbb Z).
\]

The resulting cylinder \(C\) is conformally equivalent to \(D\); locally, harmonicity is equivalent to \(\partial_x^2h+\partial_y^2h=0\). The base point is \(a_C=(1/2,0)\), and the chosen boundary point is \((0,\pi)\).

The Poisson density, with respect to the boundary coordinate \(t\), on the \(x=0\) side of the infinite strip \(0<x<1\) is

\[
p(x,t)=\frac{\sin(\pi x)}{2\bigl(\cosh(\pi t)-\cos(\pi x)\bigr)}.
\tag{2}
\]

For example, (2) follows by sending \(w=t+ix\) to \(e^{\pi w}\) in the upper half-plane and transforming its Poisson density. The periodized density for the cylinder at \((0,\pi)\) is

\[
P(x,y)=\sum_{k\in\mathbb Z}p(x,y-\pi+2\pi k).
\tag{3}
\]

Every term is positive. On each compact subset of the open cylinder, the summands and each fixed finite order of their derivatives have exponentially summable bounds in \(|k|\). Thus (3) defines a positive, periodic, smooth harmonic function and can be differentiated term by term. Set

\[
K(x,y)=\frac{P(x,y)}{P(1/2,0)}.
\tag{4}
\]

Here and below, a function on the cylinder is also regarded as the corresponding single-valued function on the annulus.

### Why (4) is a minimal Martin kernel

This identification can be checked directly, without assuming that an arbitrary positive harmonic function is a Martin kernel.

Write the strip Green function in the coordinates \(w=y+ix\), \(w'=\eta+is\) as

\[
g_S(w,w')=
\log\left|\frac{e^{\pi w}-e^{\pi\overline{w'}}}
{e^{\pi w}-e^{\pi w'}}\right|.
\tag{5}
\]

The normalization in (5) has logarithmic singularity \(-\log|w-w'|\). It is positive inside the strip and zero on its two sides. The series

\[
g_C(w,w')=\sum_{k\in\mathbb Z}g_S(w,w'+2\pi k)
\tag{6}
\]

converges locally with derivatives away from the pole, by exponential decay in the horizontal separation. It is periodic, has the required single logarithmic singularity on the cylinder, and vanishes on the boundary. Uniqueness of the Dirichlet Green function identifies (6) with the cylinder Green function.

Differentiating (5) at \(s=0\) gives

\[
\left.\frac{\partial}{\partial s}g_S(y+ix,\eta+is)\right|_{s=0}
=2\pi p(x,y-\eta).
\]

The exponentially convergent sum permits the same differentiation in (6). For \(w'\to\pi\) through the strip, its normal distance \(s\) tends to zero, and on compact subsets of the open cylinder,

\[
\frac{g_C(w,w')}{g_C(a_C,w')}\longrightarrow
\frac{P(x,y)}{P(1/2,0)}.
\tag{7}
\]

Indeed the Green function is smooth in its second variable up to this boundary segment away from its pole, vanishes when \(s=0\), and has the displayed positive normal derivative. The Taylor expansion is uniform for the first variable in such compact subsets and for \(\eta\) near \(\pi\). Thus (7) is a Martin boundary limit.

For completeness, this limit is minimal. Suppose \(v\) is harmonic on the cylinder and \(0\leq v\leq P\). Away from \((0,\pi)\), (3) extends continuously to the boundary with value zero, so the same is true of \(v\). Near the exceptional point put \(t=y-\pi\) and \(r=(x^2+t^2)^{1/2}\). Formula (2), its Taylor expansion, and the smooth remaining terms in (3) give

\[
P(x,\pi+t)=\frac{x}{\pi(x^2+t^2)}+O(x).
\tag{8}
\]

Odd reflection of \(v\) across \(x=0\) is harmonic in a punctured disc and is \(O(r^{-1})\). The real harmonic Laurent expansion in a punctured disc has a logarithmic term, first-order dipole terms, and a regular harmonic part when this growth bound holds. Oddness under \(x\mapsto-x\) eliminates the logarithmic and tangential-dipole terms. Therefore

\[
v(x,\pi+t)=A\frac{x}{x^2+t^2}+v_0(x,t),
\tag{9}
\]

where \(v_0\) extends harmonically across the origin and is odd in \(x\). This elementary Laurent statement follows equally by expanding in Fourier modes on concentric circles: the bound \(O(r^{-1})\) excludes all negative-power modes of degree at least two. Along \(t=0\), the inequalities \(0\leq v\leq P\) and (8) imply \(0\leq A\leq1/\pi\).

Subtracting \(\pi A P\) from \(v\) cancels the dipole. By (8)--(9), the difference extends continuously with value zero at the exceptional boundary point as well as at all other boundary points. It is harmonic on the annulus and continuous on its compact closure. The maximum principle applied to it and its negative gives \(v=\pi A P\). Hence \(P\), and therefore \(K\), is minimal. Equations (4) and (7) establish that this is precisely an admissible normalized minimal Martin kernel.

## 2. The gradient at the base point

For \(k\in\mathbb Z\), define

\[
q_k=\operatorname{sech}\bigl((2k-1)\pi^2\bigr)>0,
\quad S_1=\sum_kq_k,\quad S_2=\sum_kq_k^2.
\]

At \((1/2,0)\), differentiating (2)--(3) yields

\[
P=\frac12S_1,\qquad P_x=-\frac\pi2S_2,\qquad P_y=0.
\tag{10}
\]

The last equality also follows by pairing indices \(k\) and \(1-k\). Thus

\[
\nabla K(a_C)=(-c,0),\qquad c=\pi\frac{S_2}{S_1}.
\tag{11}
\]

Since every \(|2k-1|\geq1\), the ratio \(S_2/S_1\) is a weighted average of numbers at most \(\operatorname{sech}(\pi^2)\). Consequently

\[
0<c\leq\pi\operatorname{sech}(\pi^2)<\frac8{83}<\frac1{10}.
\tag{12}
\]

The rational bound uses only \(3<\pi<4\) and
\(\cosh(\pi^2)>1+\pi^4/2>83/2\). No numerical truncation of the kernel is involved.

## 3. Four admissible competitors

Put \(b=1/(2\cosh(1/2))\) and define

\[
h_{x,\pm}(x,y)=1\pm(x-1/2),
\qquad
h_{y,\pm}(x,y)=1\pm b\sin y\cosh(x-1/2).
\tag{13}
\]

These are periodic and harmonic: the \(x\)- and \(y\)-second derivatives of \(\sin y\cosh(x-1/2)\) cancel. The first pair lies strictly between \(1/2\) and \(3/2\), while the second pair is at least \(1/2\), because \(|x-1/2|<1/2\). They all equal one at \(a_C\), so each is admissible in the definition of \(H_a\).

Their gradients at the base point are

\[
(1,0),\quad(-1,0),\quad(0,b),\quad(0,-b).
\tag{14}
\]

In particular, \((-c,0)\) is strictly inside their convex hull. We use a quantitative version to cover every direction simultaneously. Since \(\cosh(1/2)<2\), we have \(1/4<b<1\). The upper bound on the hyperbolic cosine also follows from its series: \(\cosh(1/2)\leq\sum_{n\geq0}(1/4)^n=4/3<2\).

For \(d=(u,v)\neq0\), write \(\rho=\sqrt{u^2+v^2}\) and \(M=\max\{|u|,b|v|\}\). By (11) and (14),

\[
\begin{aligned}
\max_j(\nabla h_j(a_C)-\nabla K(a_C))\cdot d
&=M+cu\\
&\geq(1-c)M\\
&>\frac{75}{83}\,\frac\rho8
=\frac{75}{664}\rho
>\frac\rho{10}.
\end{aligned}
\tag{15}
\]

Here \(M\geq(|u|+b|v|)/2\geq b(|u|+|v|)/2>\rho/8\).

All five functions in (13) and (4) are smooth near \(a_C\). Taylor's theorem for the finite list \(h_j-K\) supplies a common constant \(C_0\geq1\) and a radius \(r_0>0\) such that their remainders have absolute value at most \(C_0\rho^2\) whenever \(\rho<r_0\). Therefore (15) gives

\[
\max_jh_j(a_C+d)-K(a_C+d)
>\frac\rho{10}-C_0\rho^2>0
\]

for \(0<\rho<\min\{r_0,1/(20C_0)\}\). Since \(H_a\geq\max_jh_j\), this proves (1).

## 4. Consequence for Green lines

A nonconstant Green line issuing from \(a\) has points distinct from \(a\) arbitrarily close to \(a\). If its kernel equalled the Harnack envelope along that line, those points would contradict (1). In fact (1) excludes every nontrivial equality curve approaching \(a\), with no need to calculate the Green trajectories or make assumptions about their initial direction. All normalized functions equal one at the base point itself, so the surviving equality there is correctly retained.

The annulus is a bounded smooth doubly connected Green domain. A single minimal Martin boundary point violating the proposed property disproves its universal extension to multiply connected domains.

## Reference for the question

W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2 (2018), Problem 7.42 and Update 7.42, printed pp. 173--174: https://arxiv.org/abs/1809.07200v2 . The source statement, provenance limitations, and related literature are discussed in SOURCE_STATUS.md.
