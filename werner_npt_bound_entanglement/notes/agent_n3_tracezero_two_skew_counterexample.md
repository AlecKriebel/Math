# Trace zero does not imply the coherent two-skew inequality

## Status

This note gives an exact counterexample to an intermediate
strengthening.  It is **not** a negative three-copy Werner witness.

The square-zero concurrence reduction isolates
\[
 3N-2S+P+2s_1s_2\geq0,                                  \tag{1}
\]
where
\[
\begin{aligned}
 N&=\|C\|_2^2,\\
 S&=\sum_i\|\operatorname{Tr}_iC\|_2^2,\\
 P&=\sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2.
\end{aligned}
\]
The surviving target assumes both
\(\operatorname{rank}C\leq2\) and \(C^2=0\).  Since square-zero
matrices are traceless, a tempting relaxation is to replace \(C^2=0\)
by the single equation \(\operatorname{Tr}C=0\).

That relaxation is false.  The exact matrix below has
\[
 \operatorname{rank}C=2,\qquad \operatorname{Tr}C=0,
\]
but violates (1).  It nevertheless has \(Q_3(C)>0\), and \(C^2\ne0\).
Thus any proof of the restricted exterior inequality must use the
full orthogonality of the initial and final singular planes, not only
the scalar trace consequence.

The dependency-free exact checker is
`verification/verify_n3_tracezero_two_skew_counterexample.py`.

## 1. Exact factors

Use binary-word order
\[
 000,001,010,011,100,101,110,111
\]
and embed these eight coordinates in the corresponding qutrit words.
Let \(X,Y\) be the following \(8\times2\) matrices:
\[
X=
\begin{pmatrix}
6+5i&3-3i\\
-2&-1+3i\\
2&-3i\\
11&-1-7i\\
-1-i&-2+2i\\
-7-8i&-5+6i\\
9+5i&3-7i\\
-28-9i&1-12i
\end{pmatrix},                                           \tag{2}
\]
\[
Y=
\begin{pmatrix}
(2+876i)/61&19-6i\\
-4-12i&3-i\\
7+10i&-2+2i\\
-9-8i&4-5i\\
2-12i&3\\
1+12i&-7+i\\
-4-11i&6-3i\\
2i&3-3i
\end{pmatrix}.                                           \tag{3}
\]
Put
\[
 C=XY^\dagger.                                           \tag{4}
\]

Direct Gaussian-rational contraction gives
\[
 Y^\dagger X=
\begin{pmatrix}
-207+155i&(2441+4381i)/61\\
138+186i&207-155i
\end{pmatrix}.                                           \tag{5}
\]
Hence
\[
 \operatorname{Tr}C=\operatorname{Tr}(Y^\dagger X)=0.    \tag{6}
\]
The two Gram determinants are
\[
 \det(X^\dagger X)=451794,\qquad
 \det(Y^\dagger Y)=\frac{38042244}{61}.                  \tag{7}
\]
They are strictly positive, so both factors have column rank two and
\(\operatorname{rank}C=2\).  Equation (5) is nonzero.  Since \(X\)
and \(Y\) are both injective on their two-dimensional logical spaces,
\[
 C^2=X(Y^\dagger X)Y^\dagger\ne0.                        \tag{8}
\]

## 2. Exact invariant evaluation

The partial contractions give
\[
\boxed{
\begin{aligned}
 N&=\frac{97940850}{61},\\
 S&=\frac{213490763}{61},\\
 P&=\frac{66244443}{61}.
\end{aligned}}                                           \tag{9}
\]
Therefore the rational part of (1) is
\[
 A:=3N-2S+P=-\frac{66914533}{61}<0.                      \tag{10}
\]
For a rank-two factorization \(C=XY^\dagger\),
\[
 (s_1s_2)^2
 =\det(X^\dagger X)\det(Y^\dagger Y)
 =\frac{17187257585736}{61}.                             \tag{11}
\]
There is no numerical comparison in the sign certificate:
\[
\boxed{
 A^2-4(s_1s_2)^2
 =\frac{283863875688505}{3721}>0.}                       \tag{12}
\]
Equations (10)--(12) imply
\[
 A+2s_1s_2<0,
\]
which is the promised exact violation of (1).

For comparison, trace zero makes the endpoint form
\[
 4Q_3(C)=4N-2S+P.
\]
The same exact data give
\[
\boxed{
 4Q_3(C)=\frac{31026317}{61}>0.}                         \tag{13}
\]
Thus this construction does not threaten three-copy endpoint
positivity.  Its role is to prove that the new square-zero exterior
target cannot be enlarged to all traceless rank-two matrices.

## 3. Consequence for the proof search

The logical conditions now separate sharply:
\[
\begin{array}{c|c}
\text{condition}&\text{status of (1)}\\ \hline
\operatorname{rank}C\leq2&\text{false exactly}\\
\operatorname{rank}C\leq2,\ \operatorname{Tr}C=0
  &\text{false exactly by (2)--(12)}\\
\operatorname{rank}C\leq2,\ C^2=0&\text{open}.
\end{array}
\]
Equivalently, the proof must retain the full matrix equation
\[
 Y^\dagger X=0,
\]
not merely its trace.  This rules out any argument that uses the
square-zero assumption only to delete the scalar sector
\(\Pi_0C\).
