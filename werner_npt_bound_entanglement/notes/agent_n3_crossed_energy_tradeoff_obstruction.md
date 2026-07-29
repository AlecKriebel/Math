# Exact obstruction to a crossed rank-one energy bridge

## Status

This note gives an exact counterexample to a tempting intermediate
inequality.  It is not a negative Werner witness.

Let
\[
 Y=\bigotimes_{i=1}^3\left(I-\frac12F_i\right),\qquad
 m=\frac18.
\]
For two orthonormal frames \(U=(u_0,u_1)\) and \(V=(v_0,v_1)\), put
\[
 e_{ab}
 =\langle u_a\otimes v_b,Y(u_a\otimes v_b)\rangle
 =Q_3(|u_a\rangle\langle v_b|).                         \tag{1}
\]
Ordinary Cauchy--Schwarz for \(Y-mI\succeq0\) bounds the true
rank-two interference \(c\) by
\[
 |c|
 \leq\sqrt{(e_{01}-m)(e_{10}-m)}.                       \tag{2}
\]
It is natural to try to replace the crossed diagonal energies on the
right by the two matched diagonal energies:
\[
 (e_{01}-m)(e_{10}-m)
 \stackrel{?}{\leq}
 \left(m+\sqrt{(e_{00}-m)(e_{11}-m)}\right)^2.           \tag{3}
\]
If true, (2)--(3) would prove the desired coupled scalar bound.
Equation (3) is false, even for real qutrit codewords.

The dependency-free exact checker is
`verification/verify_n3_crossed_energy_tradeoff_obstruction.py`.

## Exact counterexample

On three qutrits, define
\[
\begin{aligned}
u_0&=\frac{|000\rangle+|011\rangle}{\sqrt2},&
u_1&=\frac{|100\rangle+|112\rangle}{\sqrt2},\\
v_0&=\frac{|000\rangle+|012\rangle}{\sqrt2},&
v_1&=\frac{|100\rangle+|111\rangle}{\sqrt2}.
\end{aligned}                                             \tag{4}
\]
The supports in each displayed pair are disjoint, so \(U\) and \(V\)
are orthonormal frames.

Direct matrix-unit contraction gives
\[
 e_{00}=e_{11}=\frac{11}{32},\qquad
 e_{01}=e_{10}=\frac34.                                  \tag{5}
\]
Since \(m=1/8\), the right side minus the left side of (3) is
\[
 \left(\frac{11}{32}\right)^2
 -\left(\frac34-\frac18\right)^2
 =\boxed{-\frac{279}{1024}}.                             \tag{6}
\]
Thus (3) fails by a large exact margin.

The failure is not a distillation witness.  For
\[
 E_0=|u_0\rangle\langle v_0|,\qquad
 E_1=|u_1\rangle\langle v_1|,
\]
the actual interference is
\[
 c=\langle E_0,L^{\otimes3}(E_1)\rangle=-\frac1{32},     \tag{7}
\]
far smaller than the Cauchy--Schwarz upper bound \(5/8\).  In fact,
\[
 Q_3(E_0+E_1)
 =e_{00}+e_{11}+2\operatorname{Re}c
 =\frac58>0.                                             \tag{8}
\]

## A one-parameter exact family

The obstruction is not isolated.  Replace the coefficient \(1\) of
the second basis string in each vector in (4) by \(t\in\mathbb R\),
and normalize by \(\sqrt{1+t^2}\).  Then
\[
\begin{aligned}
e_{00}=e_{11}
 &=\frac{2t^4+8t^2+1}{8(1+t^2)^2},\\
e_{01}=e_{10}
 &=\frac{t^4+10t^2+1}{4(1+t^2)^2},\\
c&=-\frac1{8(1+t^2)^2}.                                 \tag{9}
\end{aligned}
\]
Since
\[
 e_{00}-m=\frac{t^2(t^2+6)}{8(1+t^2)^2}\geq0,
\]
the defect in (3) factors exactly as
\[
\boxed{
\left(m+\sqrt{(e_{00}-m)(e_{11}-m)}\right)^2
-(e_{01}-m)(e_{10}-m)
=
\frac{t^2(t^2-10)(3t^4+26t^2+2)}
     {64(1+t^2)^4}.}                                    \tag{10}
\]
It is strictly negative for \(0<t^2<10\).

Meanwhile the actual matched rank-two energy is
\[
 Q_3(E_0+E_1)
 =\frac{t^2(t^2+4)}{2(1+t^2)^2}\geq0.                   \tag{11}
\]

## Consequence

The four diagonal rank-one energies do not contain enough information
to turn the shifted Cauchy--Schwarz inequality (2) into the desired
matched bound.  Any successful argument must control the actual
interference \(c\) using the common two-plane Pluecker geometry; it
cannot pass only through \(e_{00},e_{01},e_{10},e_{11}\).
