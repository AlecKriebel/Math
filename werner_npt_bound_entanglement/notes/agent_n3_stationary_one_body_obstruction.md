# The one-body lower bound is not a local Euler--Lagrange consequence

## Status

At a hypothetical negative-depth minimizer, the shifted exterior
target would follow from
\[
 \boxed{\qquad
 a\geq \frac{2\delta}{3}+\frac49\Delta ,
 \qquad
 a=\|\Pi _1C\|_2^2,\quad
 \Delta=(s_1(C)-s_2(C))^2 ,
 \qquad}                                                   \tag{1}
\]
after the Schur normalization \(\sigma(C)=1\).

This note proves two exact limitations on a stationary proof of (1).

1.  The Hilbert--Schmidt trace of the complete left (or right)
    local-filter Hessians reduces to a manifestly positive expression;
    it supplies no lower bound on \(a\).
2.  More strongly, for every \(0<\delta<1/8\) there is an exact
    isotropic critical-data model with
    \[
      a=\Delta=0
    \]
    which satisfies the full one-site Euler equations and positive
    local Hessians for the endpoint quotient, the pair-sector
    quotient, and the negative-depth quotient simultaneously.

The model is deliberately **not** asserted to arise from one physical
rank-two coefficient matrix.  If it did, it would be a negative
three-copy witness.  What it proves is that (1) cannot be obtained
from the six local normal equations and their positive Hessians
without a new same-\(C\), cross-site compatibility relation.

The dependency-free exact checker is
`verification/verify_n3_stationary_one_body_obstruction.py`.

## 1. The negative-depth Hessian

Put
\[
 {\cal A}=L^{\otimes3},\qquad
 Q(C)=\langle C,{\cal A}C\rangle,\qquad
 c(C)=\|\Pi _2C\|_2^2
 \tag{2}
\]
and define the Schur energy
\[
 \sigma(C)=2Q(C)+3c(C).
 \tag{3}
\]
Normalize a hypothetical negative direction by
\[
 \sigma(C)=1,\qquad 2Q(C)=-\delta,\qquad \delta>0.
 \tag{4}
\]
Then
\[
 c(C)=\frac{1+\delta}{3}.
 \tag{5}
\]

For a physical site \(i\), define the two local forms
\[
\begin{aligned}
 h_i(A,B)
 &=\left\langle A_iC,{\cal A}(B_iC)\right\rangle,\\
 k_i(A,B)
 &=\left\langle\Pi _2(A_iC),\Pi _2(B_iC)\right\rangle .
\end{aligned}                                             \tag{6}
\]
If \(C\) globally minimizes the negative-depth quotient on the
rank-two variety, then every \(A_iC\) is still rank at most two and
the complete local depth Hessian is
\[
 \boxed{
 m_i(A,B)=2(1+\delta)h_i(A,B)+3\delta k_i(A,B)\succeq0 .
 }
 \tag{7}
\]
Moreover \(m_i(I,I)=0\), so positivity gives the complete local
Euler equation
\[
 m_i(A,I)=0\qquad(A\in M_3).
 \tag{8}
\]
The same statements hold for right multiplication.

## 2. Exact Hessian-trace identities

Let \(F_0,\ldots,F_8\) be any Hilbert--Schmidt orthonormal basis of
\(M_3\), and let
\[
 x=\|\Pi _0C\|_2^2,\quad
 a=\|\Pi _1C\|_2^2,\quad
 c=\|\Pi _2C\|_2^2,\quad
 d=\|\Pi _3C\|_2^2.
 \tag{9}
\]
Direct matrix-unit contraction gives
\[
\boxed{
\begin{aligned}
 \sum_{i,\mu}h_i(F_\mu,F_\mu)
 &=\frac{15}{8}(x-a)+\frac{15}{2}d,\\
 \sum_{i,\mu}k_i(F_\mu,F_\mu)
 &=\frac{16}{3}a+\frac{17}{3}c+d.
\end{aligned}}
\tag{10}
\]

Here is a short derivation.  If \({\cal T}\) acts on the other two
sites, then matrix units on site \(i\) give
\[
\begin{aligned}
 \sum_{r,s}
 \langle E_{rs}^{(i)}C,
 (I_i\otimes{\cal T})(E_{rs}^{(i)}C)\rangle
 &=3\langle C,(I_i\otimes{\cal T})C\rangle,\\
 \sum_{r,s}
 \langle E_{rs}^{(i)}C,
 (L_i\otimes{\cal T})(E_{rs}^{(i)}C)\rangle
 &=\frac52\langle C,(I_i\otimes{\cal T})C\rangle .
\end{aligned}                                             \tag{11}
\]
Since
\[
 {\cal P}_0=\frac23(I-L),\qquad {\cal P}_1=I-{\cal P}_0,
\]
the corresponding coefficients for a scalar or traceless output at
the filtered site are \(1/3\) and \(8/3\).  Summing over the three
possible filtered sites produces the four degree coefficients
\[
\begin{array}{c|rrrr}
\text{degree}&0&1&2&3\\ \hline
\sum_i L_{\widehat i}&15/8&-15/8&0&15/2\\
\sum_i\Pi _2\text{ after filtering}&0&16/3&17/3&1,
\end{array}
\]
which is (10).

Use the exact negative-depth simplex coordinate
\[
 u=4\sum_i g_i\geq0.
 \tag{12}
\]
The sector reconstruction is
\[
\begin{aligned}
 c&=\frac{1+\delta}{3},\\
 \|C\|_2^2&=4\delta+\frac34u+\frac94a,\\
 x&=\frac{32}{9}\delta-\frac49+\frac23u+\frac43a,\\
 d&=\frac{1+\delta}{9}+\frac1{12}u-\frac1{12}a.
\end{aligned}                                             \tag{13}
\]
Substitution of (10) and (13) into (7) gives
\[
\boxed{
 \sum_{i,\mu}m_i(F_\mu,F_\mu)
 =
 21\delta(1+\delta)
 \left(\frac{15}{4}+4\delta\right)u
 \frac{63}{4}\delta a .
 }
\tag{14}
\]
Thus the scalar trace of the full local Hessian is already positive
before any proposed lower bound on \(a\) is used.  Taking more local
trace averages cannot prove (1).

## 3. An exact isotropic stationary obstruction

We now retain each complete \(9\times9\) local form rather than only
its trace.  It is slightly cleaner not to rescale the following
formal data to \(\sigma=1\).  Fix
\[
 0<\delta<\frac18
 \tag{15}
\]
and assign
\[
\boxed{
\begin{aligned}
 x&=a=0,\\
 c&=\frac{2(1+\delta)}3,\\
 d&=\frac{1-2\delta}{3},\\
 N&=x+a+c+d=1,\\
 Q&=-\delta,\qquad \sigma=2.
\end{aligned}}
\tag{16}
\]
Assign equal singular values, so
\[
 \Delta=0,\qquad s_1=s_2=\frac1{\sqrt2}.
 \tag{17}
\]
The homogeneous version of (1) is
\[
 a\geq\frac{2\delta}{3}\sigma+\frac49\Delta.
 \tag{18}
\]
The data (16)--(17) violate it by \(4\delta/3\).

Let
\[
 {\cal P}_0(A)=A-\frac13\operatorname{Tr}(A)I_3
 \tag{19}
\]
denote the traceless projection and put
\[
 t=\frac{5(1-8\delta)}{48}.
 \tag{20}
\]
At every left and right site define the endpoint local form
\[
\boxed{
 h(A,B)=
 \frac{2\delta}{3}\langle A,L(B)\rangle
 t\langle A,{\cal P}_0(B)\rangle .
 }
\tag{21}
\]
Its scalar and traceless eigenvalues are
\[
 h_{\rm sc}=-\frac{\delta}{3},\qquad
 h_{\rm tr}=\frac{2\delta}{3}+t.
 \tag{22}
\]
Let
\[
 n(A,B)=\frac13\langle A,B\rangle
 \tag{23}
\]
be the balanced local norm form.  Then
\[
 h+\delta n\succeq0,\qquad
 \ker(h+\delta n)=\mathbb CI_3.
 \tag{24}
\]
Thus (21) satisfies the full one-site Euler equation and Hessian
positivity for the normalized endpoint quotient \(Q/N=-\delta\).

Define the pair-sector local form to have scalar and traceless
eigenvalues
\[
\boxed{
 k_{\rm sc}=\frac{2(1+\delta)}9,\qquad
 k_{\rm tr}=\frac{31+22\delta}{216}.
 }
\tag{25}
\]
It is positive definite and
\[
 k(I,I)=c.
 \tag{26}
\]
For
\[
 f=\frac{c}{N}=\frac{2(1+\delta)}3,
 \tag{27}
\]
one also has
\[
 fn-k\succeq0,\qquad
 \ker(fn-k)=\mathbb CI_3.
 \tag{28}
\]
Thus the same data satisfy the full local Euler equation and
second-order contraction for a local maximum of the pair-sector
quotient.

Finally, the negative-depth local form is
\[
 m=2(1+\delta)h+3\delta k.
 \tag{29}
\]
Its scalar eigenvalue vanishes exactly:
\[
 2(1+\delta)\left(-\frac\delta3\right)
 +3\delta\frac{2(1+\delta)}9=0,
 \tag{30}
\]
while its traceless eigenvalue is
\[
 2(1+\delta)\left(\frac{2\delta}{3}+t\right)
 +3\delta\frac{31+22\delta}{216}>0.
 \tag{31}
\]
Therefore
\[
\boxed{
 m\succeq0,\qquad \ker m=\mathbb CI_3,
 }
\tag{32}
\]
which is the complete local depth Euler--Lagrange and Hessian
condition, not merely its trace.

The local traces also have the exact common-sector values dictated by
(10):
\[
\begin{aligned}
 3\operatorname{Tr}_{\rm HS}h
 &=\frac52(1-2\delta),\\
 3\operatorname{Tr}_{\rm HS}k
 &=\frac{37+28\delta}{9}.
\end{aligned}
\tag{33}
\]
Hence the obstruction respects both the stationary matrix equations
and the global scalar bookkeeping.

## 4. Consequence

The proposed bound (1) may still hold at every physical negative
critical point.  What (16)--(33) prove is the sharper methodological
statement
\[
\boxed{\begin{minipage}{0.88\linewidth}
The degree-one lower bound is not a consequence of the complete
six one-site Euler equations, their endpoint, pair-sector, and
negative-depth Hessian positivity, balanced one-site norm data, and
the exact global sector traces.  Any proof must retain a compatibility
condition saying that all six local forms and the sector components
come from one common rank-two matrix \(C\).
\end{minipage}}
\tag{34}
\]

The natural next target is therefore cross-site compatibility:
commuting left filters at distinct sites, commuting right filters,
and the common rank-two normal equation must be imposed before taking
local traces.
