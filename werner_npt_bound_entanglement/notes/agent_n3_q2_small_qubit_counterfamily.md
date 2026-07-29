# A small qubit-supported counterpencil and exact triple-skew compensation

## Status

This note replaces the earlier dense \(27\)-coordinate counterexample
to the standalone coherent two-skew bound by a much smaller exact
family.  It has binary support on the eight words in
\(\{0,1\}^3\subset\{0,1,2\}^3\), Gaussian-integer coefficients of
modulus at most \(3\sqrt {10}\), and one real parameter.

Let
\[
\begin{aligned}
 {\cal J}_2(C)
 &=\frac34N-\frac12S+\frac14P,\\
 {\cal J}_3(C)
 &=\frac18(N-S+P-T),
\end{aligned}                                             \tag{1}
\]
where
\[
\begin{aligned}
 N&=\|C\|_2^2,&
 S&=\sum_i\|\operatorname{Tr}_iC\|_2^2,\\
 P&=\sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2,&
 T&=|\operatorname{Tr}C|^2 .
\end{aligned}
\]
The standalone coherent two-skew assertion is equivalent to
\[
 {\cal J}_2(C)+\frac12s_1(C)s_2(C)\geq0.                 \tag{2}
\]
The family below violates (2).  Nevertheless, it obeys the exact
coupled compensation inequality
\[
\boxed{
 {\cal J}_2(C_t)+2{\cal J}_3(C_t)+s_1(C_t)s_2(C_t)>0
 \qquad(t\in\mathbb R).
}                                                        \tag{3}
\]
Thus the triple-skew sector repairs the smaller counterexample
pointwise along the whole pencil.

This does not prove the unrestricted coupled feature theorem: (3)
only treats the displayed one-parameter pencil, not every logical
\(SL(2,\mathbb C)\) filter between its two fixed physical planes.

The dependency-free exact checker is
`verification/verify_n3_q2_small_qubit_counterfamily.py`.

## 1. The rank-two pencil

Order the binary words as
\[
 000,001,010,011,100,101,110,111.
\]
Define
\[
\begin{aligned}
x={}&(4+3i,0,0,5,0,-3-3i,4+2i,-9-3i)^{\mathsf T},\\
y={}&(1+7i,-2-7i,4+6i,-5-5i,1-7i,7i,-2-7i,3+6i)^{\mathsf T},\\
z={}&(1-i,0,0,-2i,0,-1+i,1-i,-2i)^{\mathsf T},\\
e={}&(1,0,0,0,0,0,0,0)^{\mathsf T}.
\end{aligned}                                             \tag{4}
\]
Embed these vectors into \((\mathbb C^3)^{\otimes3}\) by putting
zero on every word containing the digit \(2\), and put
\[
\boxed{\qquad C_t=xy^\dagger+tze^\dagger,\qquad t\in\mathbb R.\qquad}
                                                               \tag{5}
\]
Plainly \(\operatorname{rank}C_t\leq2\).  For \(t\ne0\), its two
nonzero singular values satisfy
\[
\begin{aligned}
 \bigl(s_1(C_t)s_2(C_t)\bigr)^2
 &=\det[(x,tz)^\dagger(x,tz)]\,
   \det[(y,e)^\dagger(y,e)]\\
 &=t^2(2290)(352)=806080\,t^2.
\end{aligned}                                             \tag{6}
\]
Consequently
\[
 s_1(C_t)s_2(C_t)=|t|\sqrt{806080}.                       \tag{7}
\]

## 2. Exact invariant polynomials

Direct Gaussian-integer contraction gives
\[
\begin{aligned}
 N(t)&=14t^2+172t+71556,\\
 S(t)&=14t^2+1260t+158820,\\
 P(t)&=6t^2+24t+103113,\\
 T(t)&=2t^2-356t+15844.
\end{aligned}                                             \tag{8}
\]
Substitution in (1) gives
\[
\boxed{
\begin{aligned}
 4{\cal J}_2(C_t)&=20t^2-1980t+141,\\
 8{\cal J}_3(C_t)&=4t^2-708t+5.
\end{aligned}}                                            \tag{9}
\]

At \(t=1\),
\[
 4{\cal J}_2(C_1)=-1819,\qquad
 \bigl(s_1(C_1)s_2(C_1)\bigr)^2=806080.
\]
The radical-free comparison is
\[
 1819^2-4(806080)=84441>0.                               \tag{10}
\]
Since \({\cal J}_2(C_1)<0\), equation (10) proves exactly that
\[
 {\cal J}_2(C_1)+\frac12s_1(C_1)s_2(C_1)<0.              \tag{11}
\]
This is therefore an exact counterexample to the standalone
two-skew exterior inequality.

## 3. Exact compensation by the triple-skew sector

Combining (7) and (9) yields the identity
\[
\boxed{
\begin{aligned}
4\bigl({\cal J}_2(C_t)+2{\cal J}_3(C_t)
        +s_1(C_t)s_2(C_t)\bigr)
={}&24t^2-2688t+146\\
&+4|t|\sqrt{806080}.
\end{aligned}}                                            \tag{12}
\]
This is strictly positive for every real \(t\).  If \(t\leq0\), every
term after \(24t^2+146\) combines as
\[
 -2688t+4|t|\sqrt{806080}
 =|t|\bigl(2688+4\sqrt{806080}\bigr)>0.
\]
If \(t\geq0\), the coefficient of \(t\) in (12) is positive because
\[
 806080>672^2=451584.
\]
This proves (3).

At the violating point \(t=1\), the compensation can be checked
without radicals in either direction:
\[
\begin{aligned}
 1819^2-4(806080)&=84441>0,\\
 16(806080)-2518^2&=6556956>0.
\end{aligned}                                             \tag{13}
\]
The first line says the standalone expression is negative; the
second says the coupled expression
\((-2518+4\sqrt{806080})/4\) is positive.

For comparison, the original three-copy endpoint form itself is
positive on the whole pencil:
\[
\begin{aligned}
8Q_3(C_t)
 &=8N(t)-4S(t)+2P(t)-T(t)\\
 &=66t^2-3260t+127550\\
 &=66\left(t-\frac{815}{33}\right)^2+\frac{2880700}{33}>0.
\end{aligned}                                             \tag{14}
\]
Equation (12) is the more relevant statement for the shifted
two-/three-skew program, because it displays the precise nonlinear
compensation that the failed standalone split discarded.

## 4. What this resolves and what it does not

The pencil proves three exact facts:

1. failure of the standalone coherent bound already occurs inside a
   common local qubit support and does not require a dense qutrit
   construction;
2. the failure persists in a one-parameter rank-two algebraic family,
   rather than at an isolated rounded point;
3. the triple-skew term supplies an exact pointwise repair throughout
   that family.

It does not prove unrestricted three-copy positivity, and it does not
establish the coupled concurrence bound for all filters of the two
physical planes.  A global argument must still control arbitrary
nonnormal rank-two companions with genuinely qutrit local geometry.
