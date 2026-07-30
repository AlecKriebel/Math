# The square-zero equation cannot be replaced by nilpotence

## Status

This note gives an exact counterexample to a tempting relaxation of
the square-zero exterior target.  It is not a Werner endpoint
counterexample: its endpoint value is positive.

For a rank-at-most-two matrix \(C\), put
\[
\begin{aligned}
 N&=\|C\|_2^2,&
 S&=\sum_i\|\operatorname{Tr}_iC\|_2^2,\\
 P&=\sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2,&
 D&=s_1(C)s_2(C).
\end{aligned}
\]
The proposed square-zero inequality is
\[
 3N-2S+P+2D\geq0.                                      \tag{1}
\]
There is an exact rank-two matrix \(C\) on three binary local
supports, embedded in the qutrit triple, such that
\[
 C^3=0,\qquad C^2\ne0,
\]
but
\[
 \boxed{3N-2S+P+2D<0.}                                 \tag{2}
\]
Thus neither \(\operatorname{Tr}C=0\), the vanishing of the second
spectral coefficient, nor even nilpotence of \(C\) suffices for (1).
Any proof of the square-zero theorem must use the full equation
\(C^2=0\), equivalently the vanishing of the complete logical overlap
matrix below.

The dependency-free exact checker is
`verification/verify_n3_nilpotent_two_skew_counterexample.py`.

## Construction

Use the ordered binary strings
\[
 000,001,010,011,100,101,110,111
\]
inside \((\mathbb C^3)^{\otimes3}\).  Let
\[
Y=\begin{pmatrix}
1+7i&8-4i\\
-2-6i&1-i\\
4+6i&i\\
-4-4i&1-2i\\
1-7i&1\\
6i&-3+i\\
-2-5i&2-i\\
1+3i&-i
\end{pmatrix}
\]
and
\[
X_0=\begin{pmatrix}
5+4i&1-i\\
-2&i\\
2&-1-i\\
5&-1-4i\\
-1-i&i\\
-3-4i&-2+3i\\
4+3i&1-4i\\
-13-4i&-6i
\end{pmatrix}.
\]
Direct multiplication gives
\[
 H=Y^\dagger Y=
 \begin{pmatrix}299&-1\\-1&105\end{pmatrix},
 \qquad \det H=31394,
\]
and
\[
 K=Y^\dagger X_0=
 \begin{pmatrix}
-41+24i&9+24i\\
40+69i&38-21i
\end{pmatrix}.
\]
Choose the nonzero square-zero logical matrix
\[
 G=
 \begin{pmatrix}
-40+20i&10+20i\\
40+80i&40-20i
\end{pmatrix},
\qquad
\operatorname{Tr}G=\det G=0,\qquad G^2=0.               \tag{3}
\]
Define the Gaussian-integer matrix
\[
 X=(\det H)X_0+
 Y\,\operatorname{adj}(H)(G-K).                         \tag{4}
\]
Then
\[
 Y^\dagger X=(\det H)G.                                 \tag{5}
\]
Embed \(X,Y\) on the displayed eight binary strings and put
\[
 C=XY^\dagger.                                          \tag{6}
\]

Both \(X\) and \(Y\) have full column rank.  In fact,
\[
\det(X^\dagger X)
=28330741506297369413120,\qquad
\det(Y^\dagger Y)=31394.                                \tag{7}
\]
Consequently \(\operatorname{rank}C=2\).  Equations (3), (5), and
(6) give
\[
 C^3=X(Y^\dagger X)^2Y^\dagger=0.
\]
Since \(Y^\dagger X\ne0\) and both thin factors have full column
rank,
\[
 C^2=X(Y^\dagger X)Y^\dagger\ne0.                       \tag{8}
\]

## Exact violation

Exact contraction gives
\[
\begin{aligned}
N&=105262033353136,\\
S&=230674647423880,\\
P&=84535625654192.
\end{aligned}                                           \tag{9}
\]
Hence
\[
 A:=3N-2S+P=-61027569134160.                            \tag{10}
\]
The product of the two nonzero singular values obeys
\[
 D^2
=\det(X^\dagger X)\det(Y^\dagger Y)
=889415298848699615355489280.                           \tag{11}
\]
Finally,
\[
 A^2-4D^2
=166702999029879870656948480>0.                         \tag{12}
\]
Since \(A<0\), equation (12) proves \(-A>2D\), which is exactly
(2).

The matrix is not a negative endpoint witness.  Its trace vanishes
and
\[
 8Q_3(C)=8N-4S+2P
=88468928437952>0.                                      \tag{13}
\]

## Consequence

For a full-column factorization \(C=XY^\dagger\), the two nonzero
eigenvalues of \(C\) are the eigenvalues of the \(2\times2\) overlap
\(Y^\dagger X\).  The example makes both characteristic invariants
of this overlap vanish while retaining a nonzero nilpotent overlap.
Therefore scalar corrections depending only on
\(\operatorname{Tr}(Y^\dagger X)\) and
\(\det(Y^\dagger X)\) cannot bridge the false unrestricted exterior
inequality to the square-zero case.  The missing datum is the matrix
equation
\[
 Y^\dagger X=0,
\]
not merely its characteristic polynomial.
