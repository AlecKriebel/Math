# Quantitative all-copy conjecture and exact bottlenecks

This note records conjectures only where explicitly labelled.  All
equivalences and sharpness statements below are exact.

## 1. Quantitative conjecture

Let \(s_1(C)\ge s_2(C)\ge0\) be the nonzero singular values of a matrix of
rank at most two.  The strongest candidate invariant found independently in
two proof searches is
\[
\boxed{\quad
Q_{d,n}(C)\ \ge\ 2^{-n}(s_1(C)-s_2(C))^2 .
\quad}
\tag{1}
\]
This is currently **unproved**.  It would imply all-copy two-block
positivity at the endpoint, in every \(d\), and hence (by parameter
monotonicity) throughout the full interval closer to zero.

For \(n=1\), (1) is the proved inequality
\[
\|C\|_F^2-\tfrac12|\operatorname{Tr}C|^2
\ge
s_1^2+s_2^2-\tfrac12(s_1+s_2)^2
=\tfrac12(s_1-s_2)^2.
\]

The constant is sharp at every \(n\).  Let
\[
C_0=\operatorname{diag}(s_1,s_2,0,\ldots,0),\qquad
E=|0\rangle\langle0|.
\]
Then
\[
C=C_0\otimes E^{\otimes(n-1)}
\]
has singular values \(s_1,s_2\), and tensor factorization of the quadratic
form gives
\[
Q_{d,n}(C)
=Q_{d,1}(C_0)Q_{d,1}(E)^{n-1}
=2^{-n}(s_1-s_2)^2.
\tag{2}
\]
In particular, nonzero exact zero vectors exist for every \(n\) when
\(s_1=s_2\).

## 2. Crossed-kernel scalar bottleneck

Take a singular-value decomposition
\[
C=s_1|u_1\rangle\langle v_1|
  +s_2|u_2\rangle\langle v_2|,
\]
where each displayed pair is orthonormal, and put
\[
R_n=(I-\tfrac12F)^{\otimes n},\qquad m=2^{-n}.
\]
Define
\[
\begin{aligned}
a&=\langle u_1\otimes v_1|R_n|u_1\otimes v_1\rangle,\\
b&=\langle u_2\otimes v_2|R_n|u_2\otimes v_2\rangle,\\
c&=\langle u_1\otimes v_2|R_n|u_2\otimes v_1\rangle.
\end{aligned}
\tag{3}
\]
The replica formula gives
\[
Q_{d,n}(C)=s_1^2a+s_2^2b+2s_1s_2\operatorname{Re}c,
\tag{4}
\]
and \(R_n\succeq mI\) gives \(a,b\ge m\).

Therefore the coupled estimate
\[
\boxed{\quad
|c|\le m+\sqrt{(a-m)(b-m)}
\quad}
\tag{5}
\]
would prove (1), since
\[
\begin{aligned}
Q_{d,n}(C)-m(s_1-s_2)^2
&\ge
s_1^2(a-m)+s_2^2(b-m)
-2s_1s_2(|c|-m)\\
&\ge
\left(s_1\sqrt{a-m}-s_2\sqrt{b-m}\right)^2.
\end{aligned}
\tag{6}
\]
Conversely, if (1) holds uniformly after arbitrary relative phase changes
of one singular summand, the elementary criterion for a quadratic form on
\(\mathbb R_+^2\) gives (5).  Thus (5) is the clean scalar form of the
desired tensor invariant.

The weaker bound \(|c|\le m\) is false from two copies onward.  Any proof
must retain the compensation between the crossed term and the two diagonal
terms.

## 3. Exact two-copy dual reduction for \(d=3\)

For \(n=2\),
\[
Q_{3,2}(C)
=\|C\|_F^2
-\tfrac12\left(
\|\operatorname{Tr}_1C\|_F^2+
\|\operatorname{Tr}_2C\|_F^2\right)
+\tfrac14|\operatorname{Tr}C|^2.
\tag{7}
\]
Hence two-copy positivity on rank-at-most-two matrices is equivalent to
\[
\|\operatorname{Tr}_1C\|_F^2+
\|\operatorname{Tr}_2C\|_F^2
-\tfrac12|\operatorname{Tr}C|^2
\le2\|C\|_F^2.
\tag{8}
\]

For \(M\in M_3\), write \(M_0=M-\tfrac13\operatorname{Tr}(M)I_3\), and
define the Hilbert-space-valued map
\[
\mathcal T(C)=
\left((\operatorname{Tr}_1C)_0,\,
      (\operatorname{Tr}_2C)_0,\,
      \frac{\operatorname{Tr}C}{\sqrt6}\right).
\tag{9}
\]
Because both partial traces have trace \(\operatorname{Tr}C\),
\[
\|\mathcal T(C)\|^2
=\|\operatorname{Tr}_1C\|_F^2+
  \|\operatorname{Tr}_2C\|_F^2
-\tfrac12|\operatorname{Tr}C|^2.
\tag{10}
\]
The adjoint map is
\[
\mathcal T^*(A,B,z)
=I_3\otimes A+B\otimes I_3+\frac z{\sqrt6}I_9,
\tag{11}
\]
where \(A,B\) are traceless.

For any matrix \(D\), singular-value decomposition and Cauchy--Schwarz give
\[
\sup_{\substack{\operatorname{rank}C\le2\\\|C\|_F=1}}
|\langle D,C\rangle_{HS}|
=\sqrt{s_1(D)^2+s_2(D)^2}.
\tag{12}
\]
Indeed, the upper bound is the Euclidean norm of the two largest singular
values, and equality is attained by the normalized sum of the corresponding
two singular rank-one terms.

Taking the two suprema in either order,
\[
\begin{aligned}
\sup_{\substack{\operatorname{rank}C\le2\\\|C\|_F=1}}
\|\mathcal T(C)\|
&=
\sup_{\|y\|=1}
\sup_{\substack{\operatorname{rank}C\le2\\\|C\|_F=1}}
|\langle\mathcal T^*y,C\rangle|\\
&=
\sup_{\substack{\|A\|_F^2+\|B\|_F^2+|z|^2=1\\
                 \operatorname{Tr}A=\operatorname{Tr}B=0}}
\sqrt{s_1(D)^2+s_2(D)^2},
\end{aligned}
\tag{13}
\]
with \(D\) as in (11).  Thus (8) is exactly equivalent to
\[
\boxed{\quad
s_1(D)^2+s_2(D)^2
\le
2\bigl(\|A\|_F^2+\|B\|_F^2+|z|^2\bigr)
\quad}
\tag{14}
\]
for all such \(A,B,z\).

Inequality (14) remains **unproved**.  It is already a useful exact
finite-dimensional bottleneck: no rank constraint or quantum notation
remains.  Its constant is sharp; for
\(A=|0\rangle\langle1|\), \(B=0\), \(z=0\), the operator
\(D=I_3\otimes A\) has singular value \(1\) with multiplicity three.

## 4. Discovery status

A local projected-gradient program found values numerically indistinguishable
from zero, but no reliably negative value, for real rank-two matrices at
\(d=3\), \(n=2,3\).  Independent complex and sparse exact searches have
likewise found no negative candidate through several small copy numbers.
These observations are conjecture-generation data only.
