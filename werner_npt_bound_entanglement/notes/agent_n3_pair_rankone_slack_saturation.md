# A spectral gap at product saturation of the pair-sector rank-one slack

## Status

This note does **not** prove the unrestricted qutrit pair-sector
inequality
\[
 s_1(D)^2+s_2(D)^2\leq
 2\sum_{i<j}\|B_{ij}\|_2^2.                              \tag{1}
\]
It proves a sharp structural theorem at one part of the boundary of
the established rank-one estimate
\[
 s_1(D)^2\leq\frac43
 \sum_{i<j}\|B_{ij}\|_2^2.                               \tag{2}
\]

If equality in (2) is exposed by a rank-one matrix whose left vector
is a product vector, then the second singular value has a uniform
gap:
\[
 s_2(D)^2\leq\frac13
 \sum_{i<j}\|B_{ij}\|_2^2.                               \tag{3}
\]
Consequently
\[
 s_1(D)^2+s_2(D)^2\leq\frac53
 \sum_{i<j}\|B_{ij}\|_2^2,                               \tag{4}
\]
strictly stronger than (1).  In terms of the rank-one slack operator
\[
 K_D=\frac43S I-D^\dagger D,\qquad
 S=\sum_{i<j}\|B_{ij}\|_2^2,                             \tag{5}
\]
the sum of its two smallest eigenvalues is at least \(S\), rather
than merely the desired \(2S/3\).

The remaining saturation types, and especially a quantitative
version away from exact saturation, remain open.  The exact symbolic
checker is
`verification/verify_n3_pair_rankone_slack_saturation.py`.

## 1. Rank-one saturation

On \(M_3^{\otimes3}\), let \(\Pi _2\) be the orthogonal projection
onto tensors having exactly two traceless local factors.  The sharp
rank-one theorem says
\[
 \|\Pi _2(|x\rangle\langle y|)\|_2^2
 \leq\frac49\|x\|^2\|y\|^2.                              \tag{6}
\]
For unit vectors its exact slack is
\[
\begin{aligned}
4-9\|\Pi _2(|x\rangle\langle y|)\|_2^2
={}&\sum_{i<j}
\langle x\otimes y|(I-F_i)(I-F_j)|x\otimes y\rangle\\
&+\langle x\otimes y|
(I-F_1)(I-F_2)(I-F_3)|x\otimes y\rangle .
\end{aligned}                                             \tag{7}
\]
All terms on the right are nonnegative.

Assume now that \(x=x_1\otimes x_2\otimes x_3\) is a product vector
and equality holds in (6).  Simultaneous local unitaries put
\[
 x=|000\rangle.                                          \tag{8}
\]
For this \(x\), the first three zero terms in (7) say that \(y\)
has no coefficient in which two or more local indices are nonzero.
Thus
\[
 y=a|000\rangle+
 |b_1\,00\rangle+|0\,b_2\,0\rangle+|00\,b_3\rangle,
 \qquad b_i\perp|0\rangle.                               \tag{9}
\]
Unitaries fixing \(|0\rangle\) on the three sites, together with a
global phase, reduce (9) to
\[
 y=a|000\rangle+b|100\rangle+c|010\rangle+d|001\rangle,
 \quad a,b,c,d\geq0,\quad
 a^2+b^2+c^2+d^2=1.                                     \tag{10}
\]
This is the tangent space to the product-vector variety at
\(|000\rangle\).

## 2. The exact operator inequality

Put
\[
 p=\frac13I_3,\qquad q=|0\rangle\langle0|-p,\qquad
 f=|0\rangle\langle1|.
\]
For
\[
 E=\Pi _2(|000\rangle\langle y|),                        \tag{11}
\]
the four terms in (10) give
\[
\begin{aligned}
T_0={}&p\otimes q\otimes q+
       q\otimes p\otimes q+
       q\otimes q\otimes p,\\
T_1={}&f\otimes p\otimes q+
       f\otimes q\otimes p,
\end{aligned}                                             \tag{12}
\]
and \(T_2,T_3\) are the two site permutations of \(T_1\).  Hence
\[
 E=aT_0+bT_1+cT_2+dT_3.                                 \tag{13}
\]

### Theorem 2.1

For every \(a,b,c,d\) in (10),
\[
\boxed{\qquad
 E^\dagger E\preceq
 \frac4{81}I_{27}+\frac{12}{81}|y\rangle\langle y|.
\qquad}                                                   \tag{14}
\]

#### Proof

Set
\[
 H=4I_{27}+12|y\rangle\langle y|-(9E)^\dagger(9E).
                                                               \tag{15}
\]
In the computational basis, \(H\) is block diagonal.  Its only
nontrivial blocks have sizes four, three, and two.

On
\[
 \operatorname{span}\{|000\rangle,|001\rangle,
 |010\rangle,|100\rangle\},
\]
the block is
\[
 4(I_4-|t\rangle\langle t|),\qquad
 t=(a,d,c,b)^{\mathsf T},                                \tag{16}
\]
and is positive because \(\|t\|=1\).

On
\[
 \operatorname{span}\{|011\rangle,|101\rangle,
 |110\rangle,|111\rangle\},
\]
write \(r=(b,c,d)^{\mathsf T}\).  The block is
\[
\begin{pmatrix}
A&-2ar\\
-2ar^{\mathsf T}&3a^2
\end{pmatrix},
\qquad
A=3I_3+2\operatorname{diag}(b^2,c^2,d^2)-rr^{\mathsf T}.
                                                               \tag{17}
\]
Now
\[
 A\succeq3I_3-rr^{\mathsf T}>0,\qquad
 r^{\mathsf T}A^{-1}r
 \leq\frac{\|r\|^2}{3-\|r\|^2}\leq\frac12.              \tag{18}
\]
The Schur complement in (17) is therefore at least
\[
 3a^2-4a^2\left(\frac12\right)=a^2\geq0.                \tag{19}
\]

Each nontrivial three-dimensional block is, up to a permutation of
\(b,c,d\),
\[
\begin{pmatrix}
A_2&-2a(b,c)^{\mathsf T}\\
-2a(b,c)&3a^2+4d^2
\end{pmatrix},
\quad
A_2=(3+d^2)I_2+
\begin{pmatrix}b\\-c\end{pmatrix}
\begin{pmatrix}b&-c\end{pmatrix}.                        \tag{20}
\]
Thus \(A_2\succeq(3+d^2)I_2\), and its Schur complement is at least
\[
 3a^2+4d^2-
 \frac{4a^2(b^2+c^2)}{3+d^2}
 \geq\frac53a^2+4d^2\geq0.                              \tag{21}
\]

Each nontrivial two-dimensional block is, again up to permutation,
\[
\begin{pmatrix}
4-a^2&-2ab\\
-2ab&3a^2+4(c^2+d^2)
\end{pmatrix}.                                           \tag{22}
\]
Since \(4-a^2\geq3\), its Schur complement is at least
\[
 3a^2+4(c^2+d^2)-\frac43a^2b^2
 \geq\frac53a^2+4(c^2+d^2)\geq0.                        \tag{23}
\]
All remaining blocks are positive scalars, equal either to \(4\) or
to \(4-a^2\).  Hence \(H\succeq0\), which is (14). \(\square\)

The canonical formulas also give
\[
 Ey=\frac49|000\rangle,\qquad
 E^\dagger|000\rangle=\frac49y.                         \tag{24}
\]
Thus \(s_1(E)^2=16/81\), while (14) restricted to \(y^\perp\)
gives
\[
 s_2(E)^2\leq\frac4{81}.                                \tag{25}
\]

## 3. Consequence for the pair-sector slack operator

Suppose a pair-only operator \(D\) saturates (2), and equality in the
Cauchy step defining (2) is exposed by the product rank-one matrix
\(|x\rangle\langle y|\).  Equality in Cauchy implies
\[
 D=\tau\,\Pi _2(|x\rangle\langle y|)=\tau E             \tag{26}
\]
for some scalar \(\tau\).  Orthogonality of the three embedded pair
components gives
\[
 3S=\|D\|_2^2
 =|\tau|^2\|E\|_2^2=\frac49|\tau|^2,
\quad
 S=\frac4{27}|\tau|^2.                                  \tag{27}
\]
Equations (24)--(25) now yield
\[
 s_1(D)^2=\frac43S,\qquad s_2(D)^2\leq\frac13S.          \tag{28}
\]
This proves (3)--(4).
The second bound is attained in the canonical family by
\(a=c=d=0,\ b=1\), so its constant is sharp within the stated
product-saturation class.

Equivalently, the two smallest eigenvalues of \(K_D\) in (5) obey
\[
 \lambda_1(K_D)+\lambda_2(K_D)
 \geq0+\left(\frac43S-\frac13S\right)=S.                \tag{29}
\]
The desired unrestricted pair-sector theorem asks only for the lower
bound \(2S/3\).  Therefore an obstruction cannot meet the rank-one
operator-norm boundary through this product-tangent saturation
mechanism.

## 4. Remaining question

The same numerical operator inequality (14) holds on every
rank-one-saturation pair tested, including biseparable examples in
which neither \(x\) nor \(y\) is fully product.  That observation is
not used here.  A classification of all pairs in the kernel of the
three double-antisymmetrizers in (7), or a direct Pluecker proof of
(14) on that full kernel, would upgrade this note to a complete
classification of the \(s_1^2=4S/3\) boundary.
