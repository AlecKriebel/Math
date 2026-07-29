# Exact failure of the partial anchored recursion

## Status

The proposed recursion
\[
N=(2E_2-I)(2E_3-I)(P)\stackrel{?}{\succeq}0
\]
is false, even for a very simple qutrit anchor.  Here \(P\) is the
pure anchor associated with a two-dimensional code, and
\[
E_i(X)=\operatorname{Tr}_i(X)\otimes I_i
\]
is trace replacement on physical site \(i\).

The obstruction is not merely that a positive \(N\) might have
Schmidt number larger than two: \(N\) itself can have a negative
Rayleigh quotient.

## 1. Complement reversal

Let \(K=\mathbb C^2\), let
\[
U:K\longrightarrow H_1\otimes H_2\otimes H_3
\]
be an isometry with columns \(u_0,u_1\), and put
\[
|\mathcal U\rangle=\sum_{r=0}^1|r\rangle_Ku_r,
\qquad
P=|\mathcal U\rangle\langle\mathcal U|.
\]
For an arbitrary \(B:K\to H_1\otimes H_2\otimes H_3\), with columns
\(b_0,b_1\), write
\[
|\mathcal B\rangle=\sum_{r=0}^1|r\rangle_Kb_r,
\qquad
C=UB^\dagger=\sum_{r=0}^1|u_r\rangle\langle b_r|.
\]
Direct contraction gives, for every \(S\subseteq\{1,2,3\}\),
\[
\boxed{\quad
\langle\mathcal B|E_S(P)|\mathcal B\rangle
=\left\|\operatorname{Tr}_{S^c}C\right\|_2^2 .
\quad}                                                    \tag{1}
\]
Thus the anchor trace-replacement sites and the coefficient-matrix
trace sites are complements.  The full Boolean product over all
three sites reverses harmlessly after relabeling all subsets.  A
partial product does not.

Indeed, with \(D=\operatorname{Tr}_1C\),
\[
\begin{aligned}
\langle\mathcal B|N|\mathcal B\rangle
={}&4\|\operatorname{Tr}_1C\|_2^2
-2\|\operatorname{Tr}_{12}C\|_2^2
-2\|\operatorname{Tr}_{13}C\|_2^2
+|\operatorname{Tr}C|^2\\
={}&4Q_2(D).                                             \tag{2}
\end{aligned}
\]
Although \(C\) has rank at most two, \(D\) need not.  Consequently
the unrestricted rank-two two-copy theorem cannot be applied to
\(D\).

## 2. A qutrit counterexample with Rayleigh quotient \(-2/3\)

Let
\[
|\Omega\rangle_{12}
=\frac1{\sqrt3}\sum_{j=0}^2|j\,j\rangle,
\]
and choose the orthonormal codewords
\[
u_0=|\Omega\rangle_{12}|0\rangle_3,
\qquad
u_1=|\Omega\rangle_{12}|2\rangle_3.                     \tag{3}
\]
Take
\[
b_0=|\Omega\rangle_{12}|1\rangle_3,
\qquad b_1=0.                                           \tag{4}
\]
Then
\[
C=|u_0\rangle\langle b_0|
\]
has rank one, while
\[
D=\operatorname{Tr}_1C
=\frac13I_{H_2}\otimes|0\rangle\langle1|_{H_3}.          \tag{5}
\]
Its two-copy endpoint form is
\[
\begin{aligned}
Q_2(D)
&=\|D\|_2^2-\frac12\left(
\|\operatorname{Tr}_2D\|_2^2+
\|\operatorname{Tr}_3D\|_2^2\right)
+\frac14|\operatorname{Tr}D|^2\\
&=\frac13-\frac12(1+0)+0
=-\frac16.                                              \tag{6}
\end{aligned}
\]
Equations (2) and (6) therefore give the exact negative quotient
\[
\boxed{\quad
\langle\mathcal B|
(2E_2-I)(2E_3-I)(P)
|\mathcal B\rangle=-\frac23 .
\quad}                                                   \tag{7}
\]

Hence the partial-recursion route fails at its first positivity
premise.  This does not challenge the full three-copy anchored
identity or the unrestricted two-copy theorem; it isolates precisely
why neither can be iterated by leaving one physical site inside an
enlarged ancilla.
