# An explicit analytic closure criterion for ellipsoid null chains

**600008 / AMR-005-0008. Analytic classification candidate; separate review pending.** One substantive approach. The result below gives an explicit condition involving a complete one-dimensional integral of the parameters. It does not provide a polynomial Cayley determinant or establish historical priority. The original source's Cayley-style motivation and its step-count convention must be kept distinct from the precise analytic statements proved here.

## 1. Source, conventions and the criterion

Tabachnikov's *A Baker's Dozen of Problems*, Section7, printed p.62, asks for conditions on \(a,b,c>0\) for closed chains on
\[
 M:\quad x^2/a+y^2/b+z^2/c=1
\]
with the induced metric \(dx^2+dy^2-dz^2\). The surface is analytic, but its metric is Lorentzian only between the two tropics and degenerates on them. A chain alternates the two null foliations at the tropics. It is not a future-directed null geodesic in a globally nonsingular spacetime.

The foundational Genin–Khesin–Tabachnikov paper (GKT), Section5, defines an unambiguous equator map \(T\): follow one null family from the equator to the Northern tropic, then the other family back to the equator. Its Problem5.2 asks for the parameters for which \(T^n\) closes with winding \(r\). The later problem describes tropic-to-tropic chains without explicitly reconciling the counting of individual arcs and return-map steps. We give both conventions below.

Define
\[
 f(t)^2=a\sin^2t+b\cos^2t,\qquad
 {\cal M}(a,b,c)=\frac1{2\pi}\int_0^{2\pi}
 \sqrt{\frac{f(t)^2}{c+f(t)^2}}\,dt. \tag{1}
\]
Thus \(0<{\cal M}<1\). The integral is smooth, explicit, nonsingular on its interval, and uses only \(a,b,c\), with no geodesic endpoint or unknown shift left to determine.

**Theorem.** Choose the direction that advances positively around the equator. The lift of GKT's map \(T\), normalized by that actual null path rather than modulo one, has rotation number
\[
 \rho(a,b,c)=\frac{1-{\cal M}(a,b,c)}{2{\cal M}(a,b,c)}. \tag{2}
\]
Consequently, for positive integers \(n,r\), \(T^n\) closes after winding \(r\) if and only if
\[
 \boxed{\quad {\cal M}(a,b,c)=\frac{n}{n+2r}.\quad} \tag{3}
\]
A literal chain of \(n\) full tropic-to-tropic arcs closes with winding \(r\) if and only if (3) holds **and \(n\) is even**. The reverse orientation changes the sign of the winding; the criterion then uses \(|r|\). No positively advancing nontrivial chain has zero winding.

If “after \(n\)” means least period, an additional minimality condition is needed. For \(T\), it is \(\gcd(n,r)=1\). For a full chain, write \(\rho=p/q\) in lowest positive terms; the least number of full arcs is \(\operatorname{lcm}(2,q)\), with the corresponding winding. These statements also specify closures that are iterates of a shorter one.

For fixed \(a,b>0\), every positive rational \(r/n\) determines exactly one \(c>0\) in (3). If \(a=b=A\), the condition is elementary:
\[
 c=A\left[\left(1+\frac{2r}{n}\right)^2-1\right]. \tag{4}
\]
When \(a>b\), the unique \(c\) satisfies the strict bounds
\[
 b\left[\left(1+\frac{2r}{n}\right)^2-1\right]
 <c<
 a\left[\left(1+\frac{2r}{n}\right)^2-1\right]. \tag{5}
\]
Interchanging \(a,b\) covers the other ordering.

## 2. A global conformal cylinder for the belt

Set \(D=(a+c)(b+c)\). On the Northern half of the belt introduce \(t\in\mathbb R/(2\pi\mathbb Z)\) and \(0\le v\le c\) by
\[
\begin{split}
x&=\sqrt{\frac{a(a+v)}{a+c}}\cos t,\\
y&=\sqrt{\frac{b(b+v)}{b+c}}\sin t,\\
z&=\sqrt{\frac{c(c+f(t)^2)(c-v)}{D}}.
\end{split} \tag{6}
\]
The Southern half has the opposite sign of \(z\). Direct substitution verifies the ellipsoid equation. Here \(v=c\) is the equator and \(v=0\) is the tropic.

To see that no part of the belt is omitted or duplicated, \(v\) at a given point is the unique solution of
\[
 \frac{(a+c)x^2}{a(a+v)}
 +\frac{(b+c)y^2}{b(b+v)}=1. \tag{7}
\]
Its left side is strictly decreasing in \(v\). At \(v=c\) it is at most one, by the ellipsoid equation. At \(v=0\) it is at least one exactly when
\(x^2/a^2+y^2/b^2-z^2/c^2\ge0\), the closed-belt condition. Since \(x,y\) do not both vanish there, strict monotonicity applies. The signed cosine and sine in (6) then determine \(t\) modulo \(2\pi\).

The induced metric is
\[
 g=(v+f(t)^2)
 \left[
 \frac{f(t)^2}{c+f(t)^2}\,dt^2
 -\frac{v}{4(a+v)(b+v)(c-v)}\,dv^2
 \right]. \tag{8}
\]
The cross term vanishes. One way to verify (8), for \(a\ne b\), is to put \(u=-f(t)^2\) in the pseudo-confocal formulas
\[
 x^2=\frac{a(a+u)(a+v)}{(a-b)(a+c)},\quad
 y^2=\frac{b(b+u)(b+v)}{(b-a)(b+c)},\quad
 z^2=\frac{c(c-u)(c-v)}{(a+c)(b+c)}.
\]
Differentiation gives
\[
 g=\frac{v-u}{4}\left[
 \frac{u\,du^2}{(a+u)(b+u)(c-u)}
 -\frac{v\,dv^2}{(a+v)(b+v)(c-v)}
 \right].
\]
The formula (8) extends directly to \(a=b\), either by substitution in (6) or by continuity.

Define
\[
 S(t)=\int_0^t\sqrt{\frac{f(s)^2}{c+f(s)^2}}\,ds,\qquad
 L=S(2\pi)=2\pi{\cal M},
\]
and
\[
 \tau(v)=\frac12\int_0^v
 \sqrt{\frac{w}{(a+w)(b+w)(c-w)}}\,dw,\qquad H=\tau(c). \tag{9}
\]
On the Northern half let \(Y=H-\tau(v)\); on the Southern half let \(Y=-H+\tau(v)\). This identifies the open belt with
\[
 (\mathbb R/L\mathbb Z)\times(-H,H)
\]
and transforms the metric to
\[
 g=(v+f(t)^2)(dS^2-dY^2). \tag{10}
\]
The equator is \(Y=0\), and the tropics are \(Y=\pm H\).

The coordinates are smooth across the equator: \(H-\tau(v)\) is a positive constant times \(\sqrt{c-v}\), times a function analytic and nonzero near \(v=c\). Equation (6) expresses \(z\) in the same form, so the signed definition of \(Y\) glues smoothly. At the tropics this change of coordinates extends continuously and bijectively; its normal dependence is of order \(v^{3/2}\), as expected from the null-chain cusp. We do not assert a nonsingular Lorentz metric beyond the tropics.

In a Lorentzian surface, any integral curve of a null line field is a geodesic after reparameterization: the covariant derivative of its null tangent is orthogonal to that tangent, whose orthogonal complement is its own span. Thus in (10) the unparameterized null geodesics are exactly the straight lines of slopes \(dS/dY=\pm1\). Switching to the other family at a tropic is the reflected straight-line continuation, retaining positive \(S\)-advance.

An equator-to-North-to-equator passage advances \(S\) by \(2H\). A full tropic-to-tropic arc has the same advance, since its vertical extent is \(2H\). Hence
\[
 \rho=\frac{2H}{L}=\frac{I_v}{L},\qquad
 I_v=\int_0^c\sqrt{\frac{v}{(a+v)(b+v)(c-v)}}\,dv. \tag{11}
\]
The remaining calculation eliminates this second integral.

## 3. The period identity

For \(a>b\), put
\[
 I_u=\int_{-a}^{-b}
 \sqrt{\frac{u}{(a+u)(b+u)(c-u)}}\,du.
\]
The quotient inside the square root is positive on this interval. Substituting \(u=-f(t)^2\) on a quadrant gives
\[
 I_u=\frac L2. \tag{12}
\]
We claim
\[
 I_u+I_v=\pi. \tag{13}
\]

Here is a contour proof with the signs fixed. On the plane cut along
\([-a,-b]\cup[0,c]\), let
\[
 R(z)=\sqrt{z(z+a)(z+b)(z-c)},\qquad R(z)\sim z^2
 \quad(z\to\infty),
\]
and consider \(z\,dz/R(z)\). It is holomorphic off the cuts and behaves as \(dz/z+O(dz/z^2)\) at infinity. Its integral around a large counterclockwise circle tends to \(2\pi i\).

On the upper bank of either cut, its value is \(-i\) times the corresponding positive integrand in \(I_u\) or \(I_v\); the lower-bank value has the opposite sign. A counterclockwise loop around a cut traverses its upper bank from right to left, so the two cut integrals are \(2iI_u\) and \(2iI_v\). Shrinking the outer contour proves (13). Endpoint singularities are integrable and contribute no small-circle residues.

Equations (11)–(13) give
\[
 \rho=\frac{\pi-L/2}{L}=\frac{\pi}{L}-\frac12,
\]
which is (2). Continuity in \(a,b>0\) gives the same identity at \(a=b\); alternatively the rotational case is evaluated directly below.

## 4. Closure, uniqueness and the rotational case

The cylinder description proves the return-map criterion: each \(T\)-step adds \(2H\) in the lifted \(S\)-coordinate, so \(T^n\) returns after winding \(r\) exactly when \(n(2H)=rL\). Because \(S(t+2\pi)=S(t)+L\), this is the ordinary winding about the equator, not a redefined topological index.

For full arcs, the boundary coordinate changes from \(H\) to \(-H\) at every step. Returning to the starting point therefore also requires an even number of arcs. Conversely these two conditions suffice. The least-period assertions follow by reducing the rational number \(\rho\). In particular an odd period of the folded equator map is not silently counted as an odd closed sequence of full boundary-to-boundary arcs.

Differentiating (1) under its smooth positive integrand gives
\[
 \partial_c{\cal M}
 =-\frac1{4\pi}\int_0^{2\pi}
 \frac{f(t)}{(c+f(t)^2)^{3/2}}\,dt<0. \tag{14}
\]
Also \({\cal M}\to1\) as \(c\downarrow0\) and \({\cal M}\to0\) as \(c\to\infty\). Thus (3) has exactly one positive solution \(c\) for any positive \(r/n\). It depends real-analytically on \(a,b\), by the implicit function theorem. Common scaling of \(a,b,c\) leaves the criterion unchanged.

If \(a=b=A\), then \({\cal M}=\sqrt{A/(A+c)}\), giving (4). For \(a>b\),
\[
 \sqrt{\frac b{b+c}}
 <{\cal M}<
 \sqrt{\frac a{a+c}},
\]
because the integrand lies between these values and is nonconstant. Solving these inequalities at the target value in (3) proves (5).

## 5. Correction to the imported elliptic-torsion argument

GKT's invariant one-form is precisely the integrand defining \(dS\), up to a constant. The imported prior report correctly uses its invariant-coordinate translation, but then claims that this translation is automatically an ordinary elliptic-curve group translation and hence can be tested by a division polynomial. That additional step is not justified.

For example, write \(p=(a+b)/2\), \(q=(a-b)/2>0\), and \(w=\cos2t\). The imported quartic model is
\[
 y^2=(p-qw)(c+p-qw)(1-w^2),\qquad
 dS=-\frac{p-qw}{2y}\,dw. \tag{15}
\]
At the two points above infinity, \(y\sim\pm iqw^2\). Thus \(dS\) has simple poles with nonzero opposite residues, namely \(\pm i/2\) in a local coordinate \(1/w\). It is a differential of the **third kind**, not the claimed second kind and not the holomorphic differential used for the ordinary Abel–Jacobi map.

A translation in the real coordinate obtained by integrating (15) therefore cannot be identified with algebraic elliptic-group translation by that argument. An abstract circle conjugacy is not an identification of the divisor or an algebraic torsion test. The present proof uses the real integrals and an elementary contour identity; it makes no unsupported division-polynomial claim.

## 6. Literature and unresolved stronger interpretation

GKT proves the Poncelet closure theorem and supplies the invariant density, but does not write the parameter-only shift (2) in the inspected Sections4–5. Tabachnikov's2015 problem invokes Cayley's classical algebraic condition as the motivating model. Wüstholz's2017 workshop slides announce an arithmetic result over number fields, using additional period and Jacobian conditions; the slides do not contain a complete proof or explicit parameters for every \((n,r)\), and no available full proof was verified in this bounded search. No equivalence with that announcement is claimed.

The theorem here is a complete analytic criterion for the precisely defined equator map and for literal full-arc chains, including the axisymmetric case. If the intended requirement is specifically a finite algebraic Cayley-type condition in the axes, that stronger request remains unresolved by this work. Neither the elementary integral criterion nor the imported torsion inference should be represented as a verified algebraic solution or as an established novel contribution.

The exact checker verifies the metric identities, signs on rational samples, pole orders/residues, rotational parameter formulas and period-count arithmetic. Optional numerical quadrature checks are diagnostic only. Global coordinate, contour and closure arguments are supplied in the proof above.
