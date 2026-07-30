# A spectral-subspace upgrade of the explicit high-AAA radius

## Status

This note improves the explicit high-triple-skew neighborhood from
\(10^{-120}\) to \(10^{-56}\):
\[
\boxed{
 {\cal C}(Q_{(3)})>\frac8{27}-10^{-56}
 \quad\Longrightarrow\quad
 {\cal C}(Q_{(2)}+Q_{(3)})<\frac49 .
}                                                        \tag{1}
\]
It does not settle unrestricted three-copy positivity.  Its purpose is
to remove the avoidable square-root loss in the earlier compression
plane argument.

The previous proof first shows that the coherent triple-Hodge operator
\(D\) is \(O(h^{1/8})\)-close to the equality-orbit operator \(D_0\).
It then bounded compression-plane leakage from a Rayleigh quotient,
which took another square root and produced an \(O(h^{1/16})\) plane
distance.  Here a spectral-subspace argument separates the two
effects:

1. the top two-plane of \(D\) is \(O(h^{1/8})\)-close to that of
   \(D_0\);
2. determinant saturation makes the physical compression plane
   \(O(\sqrt\varepsilon)\)-close to the top plane of \(D\).

The resulting physical plane distance is \(O(\varepsilon^{1/8})\),
and \(10^{-56}\) is a conservative exact radius.

The dependency-free exact checker is
`verification/verify_n3_high_aaa_radius_upgrade.py`.

## 1. Established input

Put
\[
 \varepsilon=\frac8{27}-{\cal C}(Q_{(3)}),
 \qquad 0\leq\varepsilon<10^{-56}.
\]
The exact deficit reduction and the quantitative equality analysis
already proved the following.  There are triple-Hodge operators
\(D,D_0\) such that
\[
\begin{aligned}
 \|D-D_0\|_{\rm op}&<\eta,
 &\eta&=46\varepsilon^{1/8},\\
 \|D\|_{\rm op}&\leq r,
 &r&=\frac1{\sqrt6},                                    \tag{2}
\end{aligned}
\]
and the singular spectrum of \(D_0\) begins
\[
 r,\ r,\ \frac r2,\ldots,\frac r2.                     \tag{3}
\]
If \(U,V\) are the two physical compression planes and
\[
 M=U^{\mathsf T}DV,
\]
then
\[
 s_2(M)>r-\frac{2\varepsilon}{r}.                       \tag{4}
\]
All harmless conjugations are the same as in the established
triple-Hodge convention.

Since \(\varepsilon^{1/8}<10^{-7}\),
\[
 \eta<46\cdot10^{-7}<\frac r8.                          \tag{5}
\]

## 2. A two-step compression-plane lemma

Let \(P_0\) be the top two-dimensional right singular projection of
\(D_0\), and \(P\) the top right singular projection of \(D\).
Set
\[
 A_0=D_0^\dagger D_0,\qquad A=D^\dagger D.
\]
Then
\[
 \|A-A_0\|
 \leq(\|D\|+\|D_0\|)\eta
 \leq3r\eta=:\xi.                                       \tag{6}
\]
Here \(\eta<r\) was used in the second inequality.

Weyl's inequalities give
\[
 \lambda_2(A)\geq r^2-\xi,\qquad
 \lambda_3(A)\leq\frac{r^2}{4}+\xi.
\]
In particular \(P\) is well defined.  Choose an isometry \(W\) onto
\(\operatorname{ran}P\) with
\[
 AW=W\Lambda,\qquad \Lambda\succeq(r^2-\xi)I_2.
\]
Applying \(I-P_0\) to this equation gives the Sylvester equation
\[
 (I-P_0)A_0(I-P_0)\,(I-P_0)W
 -(I-P_0)W\Lambda
 =-(I-P_0)(A-A_0)W.                                    \tag{7}
\]
The spectra on the two sides are separated by at least
\[
 r^2-\xi-\frac{r^2}{4}
 =\frac{3r^2}{4}-\xi.
\]
Equation (5) gives \(\xi<3r^2/8\).  The elementary spectral solution
of (7) therefore gives
\[
 \|(I-P_0)P\|
 \leq\frac{\xi}{3r^2/4-\xi}
 \leq\frac{8\eta}{r}.                                   \tag{8}
\]
For completeness, the operator-norm Sylvester estimate follows from
the convergent integral solution after shifting the two Hermitian
spectra so that one is nonpositive and the other is at least the
displayed separation.  The two semigroup norms then multiply to at
most \(e^{-t\,{\rm separation}}\), and integration gives the reciprocal
of the separation.

We next compare \(V\) with \(P\).  For every unit vector
\(v\in\operatorname{ran}V\), (4) gives
\[
 \|Dv\|\geq r-\frac{2\varepsilon}{r}.
\]
On \(\operatorname{ran}(I-P)\), Weyl gives
\[
 \|D(I-P)\|\leq\frac r2+\eta,
\]
while \(\|DP\|\leq r\).  Hence
\[
\begin{aligned}
 \|(I-P)v\|^2
 &\leq
 \frac{r^2-(r-2\varepsilon/r)^2}
      {r^2-(r/2+\eta)^2}\\
 &\leq\frac{64\varepsilon}{7r^2},                       \tag{9}
\end{aligned}
\]
where (5) bounds the denominator below by \(7r^2/16\).
Thus
\[
 \|(I-P)V\|\leq\frac{8}{\sqrt7}\frac{\sqrt\varepsilon}{r}
 <\frac{4\sqrt\varepsilon}{r}.                          \tag{10}
\]

Combining (8) and (10),
\[
\boxed{
 \|(I-P_0)V\|
 <\beta:=
 \frac{8\eta+4\sqrt\varepsilon}{r}
 <930\varepsilon^{1/8}.
}                                                        \tag{11}
\]
The same proof applied to \(D^\dagger\) gives the identical bound for
the left compression plane \(\overline{\operatorname{ran}U}\).

## 3. Completion of the feature estimate

Principal-angle alignment supplies logical bases in which each
compression isometry differs from its equality-orbit isometry by at
most \(\sqrt2\beta\).  Their tensor-product isometries \(W,W_0\)
therefore obey
\[
 \|W-W_0\|_{\rm op}<2\sqrt2\beta.
\]
The physical two-skew feature operator has norm \(4/3\), so
\[
\begin{aligned}
 q&:=\|Q_{(2)}-Q_{(2),0}\|_{\rm op}\\
 &\leq2\frac43\|W-W_0\|_{\rm op}
 <\frac{16\sqrt2}{3}\beta
 <8\beta
 <7440\varepsilon^{1/8}.                               \tag{12}
\end{aligned}
\]

At the equality orbit,
\[
 \operatorname{spec}Q_{(2),0}
 =\left(\frac49,\frac4{27},\frac4{27},\frac4{27}\right),
\qquad {\cal C}(Q_{(2),0})=0.
\]
The established local concurrence perturbation lemma says that, when
\(q<2/27\),
\[
 {\cal C}(Q_{(2)})\leq18\sqrt3\,q<36q.                  \tag{13}
\]
For \(\varepsilon<10^{-56}\), equations (12)--(13) give
\[
 q<7440\cdot10^{-7}<\frac2{27}
\]
and
\[
 {\cal C}(Q_{(2)})
 <36\cdot7440\cdot10^{-7}
 <\frac4{27}.                                           \tag{14}
\]
Finally,
\[
\begin{aligned}
 {\cal C}(Q_{(2)}+Q_{(3)})
 &\leq{\cal C}(Q_{(2)})+{\cal C}(Q_{(3)})\\
 &<\frac4{27}+\frac8{27}
 =\frac49,
\end{aligned}
\]
which proves (1).

## 4. Consequence for the negative-depth fusion

The high-AAA face fusion may now use
\[
 \varepsilon_0=10^{-56}
\]
in place of \(10^{-120}\).  Its exact complementary-branch depth
bound becomes
\[
\boxed{
 \delta<
 \frac{648+2187\cdot10^{-56}}
      {5112+21141\cdot10^{-56}}
 <\frac9{71}.
}                                                        \tag{15}
\]
The exact gap below \(9/71\) is
\[
 \frac{34992\cdot10^{-56}}
 {71(5112+21141\cdot10^{-56})}.                         \tag{16}
\]
This remains far from a sign proof.  It records, however, that the
quantitative obstruction is no longer paying an artificial
square-root loss at the spectral-plane step.
