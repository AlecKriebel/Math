# Negative answers to the Beurling transform annihilator questions

## Statement and conventions

Let \(D=\{z\in\mathbb C:|z|<1\}\), and let \(dA=dx\,dy\) be unnormalized planar Lebesgue measure. Define

\[
N=\left\{v\in L^\infty(D):\int_Dv(z)\phi(z)\,dA(z)=0
\text{ for every holomorphic }\phi\in L^1(D)\right\}.
\]

The pairing is bilinear: there is no complex conjugate on \(\phi\). Extend each input by zero off \(D\), and use

\[
Bv(z)=-\frac1\pi\lim_{\varepsilon\downarrow0}
\int_{D\setminus B(z,\varepsilon)}\frac{v(\zeta)}{(z-\zeta)^2}\,dA(\zeta).
\tag{1}
\]

These are the conventions in Hayman and Lingham, Problem 7.72, arXiv:1809.07200v2, printed page 183 (PDF page 184). The problem asks whether every \(v\in N\) has an essentially bounded transform, whether a universal \(L^\infty\) bound holds, and whether that bound holds at least for inputs in \(N\) that are polynomials in \(z,\bar z\). The following witnesses give negative answers. No historical priority or novelty is asserted.

**Theorem.** For each positive integer \(m\), put

\[
P_m(t)=\sum_{j=0}^{m-1}(1-t)^j,
\qquad
v_m(z)=z^2P_m(|z|^2),
\qquad
H_m=\sum_{k=1}^{m}\frac1k.
\]

Then \(v_m\in N\cap\mathbb C[z,\bar z]\),

\[
\|v_m\|_{L^\infty(D)}=1,
\qquad
\|Bv_m\|_{L^\infty(D)}=H_m.
\tag{2}
\]

Furthermore, the function

\[
v(z)=\frac z{\bar z}\quad(0<|z|<1),\qquad v(0)=0,
\]

belongs to \(N\), has norm one, and satisfies

\[
Bv(z)=1+\log|z|^2\qquad(0<|z|<1).
\tag{3}
\]

In particular, \(Bv\notin L^\infty(D)\).

## Angular annihilation for every analytic integrable test function

More generally, let \(a\) be a bounded measurable function on \((0,1)\), and define

\[
f_a(re^{i\theta})=e^{2i\theta}a(r^2)\quad(0<r<1).
\]

For every holomorphic \(\phi\in L^1(D)\), the product \(f_a\phi\) is absolutely integrable. Thus polar-coordinate Fubini is valid. For each fixed \(r<1\), the Taylor series of \(\phi\) converges uniformly on the circle of radius \(r\). Termwise angular integration gives

\[
\int_0^{2\pi}e^{2i\theta}\phi(re^{i\theta})\,d\theta
=\sum_{n=0}^{\infty}c_nr^n\int_0^{2\pi}e^{i(n+2)\theta}\,d\theta=0.
\]

Consequently \(\int_Df_a\phi\,dA=0\). This establishes annihilation for all the specified analytic \(L^1\) tests, rather than only for monomials or bounded analytic functions.

For \(v_m\), the radial factor is

\[
a_m(t)=tP_m(t)=1-(1-t)^m.
\tag{4}
\]

It is between zero and one on \((0,1)\), and approaches one as \(t\uparrow1\). Each level strictly below one is exceeded on an annulus of positive area. Hence \(\|v_m\|_\infty=1\) as an essential supremum on the open disc. The displayed definition of \(v_m\) is a finite polynomial in \(z\) and \(\bar z\); no division by \(\bar z\) is required at the origin. For \(v\), the radial factor is simply \(a(t)=1\), so \(\|v\|_\infty=1\). The preceding argument puts both kinds of input in \(N\).

## Direct calculation of the Cauchy transform

For bounded, compactly supported \(f\), define

\[
Cf(z)=\frac1\pi\int_{\mathbb C}\frac{f(\zeta)}{z-\zeta}\,dA(\zeta).
\tag{5}
\]

This is an absolutely convergent integral at every \(z\), since \(|z-\zeta|^{-1}\) is locally integrable. Thus Fubini can be used here without a principal-value interchange.

For the input \(f_a\), fix \(z\ne0\) and a radius \(r\ne|z|\). If \(r<|z|\), expand

\[
\frac1{z-re^{i\theta}}=\sum_{n\ge0}\frac{r^ne^{in\theta}}{z^{n+1}}.
\]

After multiplication by \(e^{2i\theta}\), every term has zero angular integral. If \(r>|z|\), expand instead

\[
\frac1{z-re^{i\theta}}
=-\sum_{n\ge0}\frac{z^n}{r^{n+1}}e^{-i(n+1)\theta}.
\]

Only the term \(n=1\) survives multiplication by \(e^{2i\theta}\) and angular integration; its integral is \(-2\pi z/r^2\). Both geometric series converge uniformly in \(\theta\) for the fixed, distinct radii under consideration. The single radius \(r=|z|\) can be omitted in the radial integral. It follows that

\[
Cf_a(z)=
\begin{cases}
-z\displaystyle\int_{|z|^2}^{1}\frac{a(s)}s\,ds,&0<|z|<1,\\[1ex]
0,&|z|>1.
\end{cases}
\tag{6}
\]

At \(z=0\), angular integration directly gives \(Cf_a(0)=0\). The same calculation gives zero on \(|z|=1\), or this follows from continuity of (5). Thus (6) calculates the actual full-plane Cauchy transform, with no unspecified holomorphic correction.

## Kernel differentiation and principal values

Use the Wirtinger derivatives

\[
\partial=\tfrac12(\partial_x-i\partial_y),\qquad
\bar\partial=\tfrac12(\partial_x+i\partial_y).
\]

For the locally integrable Cauchy kernel \(E(z)=1/(\pi z)\), distributional integration by parts on punctured discs gives

\[
\bar\partial E=\delta_0,
\qquad
\partial E=-\frac1\pi\operatorname{pv}\frac1{z^2}.
\tag{7}
\]

For completeness, in the \(\partial\) computation the inner boundary term is a constant multiple of
\(\int_0^{2\pi}e^{-2i\theta}\psi(\varepsilon e^{i\theta})\,d\theta\), which tends to zero for every smooth test function \(\psi\). In the \(\bar\partial\) computation the corresponding angular factor is one, producing \(\psi(0)\) after normalization by \(\pi\). The principal value in (7) exists as a distribution: the constant term of the test function has zero angular integral, and its difference from that constant is \(O(|z|)\), which is integrable against \(|z|^{-2}dA\) near zero. This also fixes the minus sign in (1).

Convolution with compactly supported \(f\) gives \(\partial Cf=Bf\) in distributions. If \(f\) is continuously differentiable near a point \(z\), the principal value in (1) exists there and agrees with that derivative. Indeed, on a small disc centered at \(z\), subtract \(f(z)\): its constant contribution vanishes by angular cancellation, while

\[
\frac{|f(\zeta)-f(z)|}{|z-\zeta|^2}\le\frac{C}{|z-\zeta|}
\]

is integrable. On a smaller compact neighborhood, the truncated local integrals converge uniformly; the remaining integral is continuous there. Therefore the principal-value representative is continuous wherever the input is locally continuously differentiable and equals the distributional derivative there.

The polynomial inputs are smooth at every point of \(D\). The single input \(v\) is smooth on \(D\setminus\{0\}\). These are precisely the pointwise regions needed below; no claim of a finite principal value at the origin is made for the single input.

## Polynomial witnesses and their exact norms

For \(a_m(t)=tP_m(t)\), formula (6) becomes

\[
Cv_m(z)=u_m(z)=zF_m(|z|^2),\qquad
F_m(t)=-\int_t^1P_m(s)\,ds
=-\sum_{k=1}^{m}\frac{(1-t)^k}{k}
\tag{8}
\]

inside \(D\), with zero extension outside. Hence, throughout \(D\),

\[
Bv_m(z)=\partial u_m(z)
=F_m(|z|^2)+|z|^2P_m(|z|^2)=G_m(|z|^2),
\tag{9}
\]

where

\[
G_m(t)=1-(1-t)^m-\sum_{k=1}^{m}\frac{(1-t)^k}{k}.
\]

In particular, \(G_m\) is continuous on \([0,1]\), with

\[
G_m(0)=-H_m,\qquad G_m(1)=1,
\qquad G_m'(t)=P_m(t)+m(1-t)^{m-1}>0\quad(0<t<1).
\tag{10}
\]

Thus \(-H_m\le G_m(t)\le1\) and \(H_m\ge1\), proving \(\|Bv_m\|_\infty\le H_m\). For every \(\eta>0\), continuity at zero makes \(|G_m(|z|^2)|>H_m-\eta\) on a sufficiently small disc, up to the vacuous case of a nonpositive threshold. This set has positive area. Therefore the essential supremum is at least \(H_m\), proving (2).

There is also an independent sign and normalization check at the origin. Except on a null set,

\[
\frac{v_m(\zeta)}{\zeta^2}=P_m(|\zeta|^2),
\]

which is bounded for fixed \(m\). The integral at zero is absolutely convergent and gives

\[
Bv_m(0)=-\frac1\pi\int_D P_m(|\zeta|^2)\,dA(\zeta)
=-\int_0^1P_m(t)\,dt=-H_m.
\]

The continuity argument above is indispensable: an isolated point value alone would not bound an essential supremum. Since \(H_m\to\infty\), no constant independent of the polynomial input can satisfy the proposed inequality.

## A single bounded input with an unbounded transform

For \(a(t)=1\), formula (6) gives

\[
Cv(z)=u(z)=z\log|z|^2\quad(0<|z|<1),
\qquad u(0)=0,
\qquad u(z)=0\quad(|z|\ge1).
\tag{11}
\]

The function is continuous at zero because \(r\log r\to0\), and it vanishes on the unit circle. Away from the origin and the unit circle,

\[
\bar\partial u(z)=\frac z{\bar z},\qquad
\partial u(z)=1+\log|z|^2\quad(0<|z|<1),
\tag{12}
\]

and both derivatives vanish outside the closed disc. These formulas also hold weakly, without additional point or boundary measures. To verify this directly, integrate by parts against a compactly supported smooth test function on \(\varepsilon<|z|<1\). The outer boundary term is zero because \(u=0\) there. The absolute value of the inner boundary term is at most a constant times

\[
\varepsilon\sup_{|z|=\varepsilon}|u(z)|
=2\varepsilon^2|\log\varepsilon|\longrightarrow0.
\]

The derivative formulas are integrable; for every \(1\le p<\infty\),

\[
\int_0^1 r|\log r|^p\,dr<\infty.
\]

Accordingly \(u\in W^{1,p}(\mathbb C)\) for every finite \(p\ge1\). The same integration-by-parts argument for (8), with its zero outer trace and no singularity at zero, shows that \(u_m\in W^{1,\infty}(\mathbb C)\), \(\bar\partial u_m=v_m1_D\), and \(\partial u_m=G_m(|z|^2)1_D\) almost everywhere. Jumps of the derivatives themselves across the unit circle do not create measures in these first derivatives of the continuous primitives.

Combining (7), (11), and (12) proves (3) at every nonzero point of \(D\). For any \(M\ge1\),

\[
\bigl|\{z\in D:|Bv(z)|>M\}\bigr|
=\pi e^{-M-1}>0.
\tag{13}
\]

Thus \(Bv\) is essentially unbounded, regardless of the value assigned to it at the origin. At zero its truncated transform is

\[
-\frac1\pi\int_{\varepsilon<|\zeta|<1}\frac{1}{|\zeta|^2}\,dA(\zeta)
=2\log\varepsilon\longrightarrow-\infty.
\]

This exceptional point is consistent with, and unnecessary for, the \(L^\infty\) conclusion.

## Scope of the conclusion

The polynomial family disproves uniform boundedness even on \(N\cap\mathbb C[z,\bar z]\). The separate input \(v=z/\bar z\) disproves the assertion that \(B\) maps all of \(N\) into \(L^\infty\). Both conclusions already hold on \(D\); the calculated transforms are zero almost everywhere outside \(D\), so the same conclusions hold if the output norm is interpreted on the whole plane.

Each individual polynomial witness has a bounded transform. The polynomial conclusion is failure of a universal constant, not a claim that one polynomial has an unbounded transform.

## Source

Walter K. Hayman and Eleanor F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2 (21 September 2018), Problem 7.72, printed p.183, PDF p.184. [Version record](https://arxiv.org/abs/1809.07200v2) and [PDF](https://arxiv.org/pdf/1809.07200v2). The proof above is an explicit verification of the two witnesses under the printed conventions; its validity does not depend on an attribution claim about subsequent literature.
