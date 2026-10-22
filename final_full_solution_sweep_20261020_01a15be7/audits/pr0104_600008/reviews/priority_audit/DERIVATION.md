# Independent reconstruction of the antecedent analytic criterion

This derivation was written before consulting historical PR104 audit verdicts. It is an independent calculation, not a claim that the following exact notation or every convention is printed in one source.

## Prior differential and its surface specialization

[Dragović–Radnović (2019), arXiv:1909.08154v1](https://arxiv.org/pdf/1909.08154v1), proof of Theorem 3.1, printed p.5, supplies separated differentials and the integrated relation (3.2). It identifies coordinate-plane crossings; p.7 explicitly relates its final count to crossings of the plane $x_2=0$. Remark 4.4 on p.13 names the geodesic limit and the original open problem. I use these specific formulas, not its general assertion of having solved the problem, as evidence. No assertion about the validity of its finite algebraic Cayley conditions is required here.

Set its $(a_1,a_2,a_3)=(a,b,c)$, with $a>b>0$. The lightlike specialization removes the infinite caustic, and the surface specialization fixes the remaining caustic at zero. The surviving $k=1$ differential has

\[
 P_0(x)=-x(a-x)(b-x)(c+x).
\]

On the belt write the two variable confocal coordinates as $\lambda_1=-v$, $\lambda_3=u$, with $0<v<c$, $b<u<a$. Its two positive magnitudes are

\[
 R_u(u)^{1/2}du=\sqrt{\frac{u}{(a-u)(u-b)(c+u)}}du,
 \qquad
 R_v(v)^{1/2}dv=\sqrt{\frac{v}{(a+v)(b+v)(c-v)}}dv.
\]

This specialization can be checked without assuming any convergence theorem for closed billiard orbits. The standard confocal squared coordinate formulas are

\[
 X^2=\frac{a(a+v)(a-u)}{(a-b)(a+c)},\quad
 Y^2=\frac{b(b+v)(u-b)}{(a-b)(b+c)},\quad
 Z^2=\frac{c(c-v)(c+u)}{(a+c)(b+c)}.
\]

Differentiation, with Lorentz signs $(+,+,-)$, gives exactly

\[
 g=\frac{u+v}{4}\bigl(R_u(u)du^2-R_v(v)dv^2\bigr).
\]

The supplied checker verifies the ellipsoid identity, both metric coefficients, the vanishing cross term, and equality with $x^2/P_0(x)$ exactly. Thus the local null equation is precisely equality of the two positive differential magnitudes. This avoids the invalid inference that a limit of billiard periodicity conditions at a fixed reflection count necessarily gives a geodesic period.

Indeed, near a small positive caustic $\varepsilon$, the disappearing interval contributes $A_\varepsilon=O(\sqrt\varepsilon)$ to the $k=0$ differential, and $B_\varepsilon\le\varepsilon A_\varepsilon$ to $k=1$. The number of grazing reflections can diverge. If the total $k=0$ contribution stays bounded, its $k=1$ contribution still vanishes, by this inequality. Simply setting all reflection counts equal, or retaining a fixed total billiard period, is unwarranted.

## The actual winding lift and parity

Define the positive periods

\[
 I_u=\int_b^a\sqrt{R_u(u)}du,\qquad
 I_v=\int_0^c\sqrt{R_v(v)}dv.
\]

The angular parametrization $u=a\sin^2t+b\cos^2t$ crosses the interval $[b,a]$ four times for one full physical turn of $t$. After unfolding quadrants, the horizontal coordinate therefore has circumference $4I_u$. The signed vertical coordinate has range $(-I_v,I_v)$, with the equator at zero and the two tropics at the endpoints. A full tropic-to-tropic arc, or an equator-to-North-to-equator excursion, has positive horizontal advance $2I_v$. Hence the unreduced winding lift is

\[
 \rho=\frac{I_v}{2I_u}.
\]

For full physical arcs, $n$ arcs close with $r$ turns exactly when $nI_v=2rI_u$ and $n$ is even. The second condition records which boundary circle is occupied, independently of the angular period. For the folded equator map there is no boundary-circle parity restriction. Its closure equation is the same without the evenness condition. These are actual positive coordinate advances, so no integer is lost by reducing a rotation number modulo one.

This also explains the integrated antecedent's counts: the number of $Y=0$ plane crossings is $2r$, not $r$ and not $4r$. The two integrals in (3.2) have the common half-oscillation factor cancelled. Our direct unfolded calculation fixes that factor even if the phrase about tracing a segment is read ambiguously.

## Exact classical connection formula

Put

\[
 n_0=\frac{a-b}{a},\quad m_0=\frac{c}{b+c},\quad k^2=n_0m_0,\quad C=\frac{2b}{\sqrt{a(b+c)}}.
\]

All parameters obey $0<k^2<n_0,m_0<1$. With $s=\sin^2\theta$, use $u=b/(1-n_0s)$ in the right interval and $v=bm_0s/(1-m_0s)$ in the vertical interval. Direct substitution gives

\[
 I_u=C\Pi(n_0,k),\qquad
 I_v=C\bigl(\Pi(m_0,k)-K(k)\bigr).
\]

Here \(\Pi(n,k)=\int_0^{\pi/2}[(1-n\sin^2\theta)\sqrt{1-k^2\sin^2\theta}]^{-1}d\theta\). This explicitly fixes the distinction between the characteristic $n$ and the modulus $k$. Both substitutions preserve positivity, so verifying squared pullbacks does not introduce a sign ambiguity.

The complete specialization of [DLMF 19.7.8](https://dlmf.nist.gov/19.7.E8) is

\[
 \Pi(n_0,k)+\Pi(m_0,k)-K(k)
 =\frac{\pi}{2\sqrt{(1-n_0)(1-m_0)}},\qquad n_0m_0=k^2.
\]

Since $C=2\sqrt{(1-n_0)(1-m_0)}$, the result is $I_u+I_v=\pi$. No new elliptic-integral identity is needed.

Finally, $I_u=\pi\mathcal M$ by the same angular substitution. Thus

\[
 \rho=\frac{1-\mathcal M}{2\mathcal M},\qquad
 \rho=r/n\iff\mathcal M=\frac{n}{n+2r}.
\]

At $a=b=A$, direct evaluation gives $\mathcal M=\sqrt{A/(A+c)}$; equivalently this is the continuous distinct-axis limit. Strict monotonicity in $c$, endpoint limits, uniqueness, analytic dependence and the bounds follow by differentiation or elementary pointwise comparison of this explicit positive integrand. They do not provide a separate new closure mechanism.

## What this proves about priority

The exact analytic closure theorem, with winding and physical parity, follows from an already published separation mechanism plus a classical connection formula and elementary unfolding. It is not enough to assert that an unrelated ambient billiard theorem solves the surface problem; the calculation above supplies the missing equivalence. Conversely, this calculation does not validate any unsupported ordinary elliptic-torsion shortcut or finite polynomial Cayley characterization. No categorical assertion of the first author to print every formula is made.
