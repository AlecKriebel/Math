# Exact compensation for every four-string square-zero completion

## Status

This note proves an exact three-copy theorem for the nonnormal
square-zero construction which repairs an inertia-\((2,2)\) Hermitian
quadrature.

Let \(p_0,p_1,n_0,n_1\) be four distinct computational-basis strings
of length three, in arbitrary local dimensions, and suppose that the
Hermitian operator \(H\) below has \(Q_3(H)<0\).  For \(U\in U(2)\), put
\[
\begin{aligned}
 H&=\frac12\left(P_{p_0}+P_{p_1}-P_{n_0}-P_{n_1}\right),\\
 B_U&=\frac12\sum_{r,s=0}^1\left(
 U_{rs}|p_r\rangle\langle n_s|
 +
 \overline{U_{rs}}|n_s\rangle\langle p_r|\right),\\
 C_U&=H+iB_U .
\end{aligned}                                             \tag{1}
\]
Then
\[
 \boxed{\quad \operatorname{rank}C_U=2,\qquad C_U^2=0,
 \qquad Q_3(C_U)\ge\frac14. \quad}                        \tag{2}
\]
The constant is sharp.

Thus the most direct way of converting a negative diagonal
inertia-\((2,2)\) direction into a rank-two nonnormal operator always
overcompensates it.  This includes the previously recorded exact
Hermitian example with \(Q_3(H)=-1/4\): every unitary square-zero
completion has \(Q_3(B_U)=1/2\) and hence \(Q_3(C_U)=1/4\).

The proof is a finite equality-pattern classification.  It is
dimension independent because four local symbols are described only
by a set partition of four labels.  The dependency-free exact checker
is
`verification/verify_n3_squarezero_string_completion.py`.

## 1. Rank and quadrature splitting

In the ordered support
\[
 (p_0,p_1,n_0,n_1),
\]
the two Hermitian quadratures are
\[
 H=\frac12
 \begin{pmatrix}I_2&0\\0&-I_2\end{pmatrix},
 \qquad
 B_U=\frac12
 \begin{pmatrix}0&U\\U^\dagger&0\end{pmatrix}.
                                                               \tag{3}
\]
Consequently
\[
 C_U=\frac12
 \begin{pmatrix}I_2&iU\\iU^\dagger&-I_2\end{pmatrix},
 \qquad C_U^2=0.                                         \tag{4}
\]
The first two block rows are independent and the last two are their
linear combinations, so \(\operatorname{rank}C_U=2\).

The endpoint form is Hermitian on operator space.  Since \(H\) and
\(B_U\) are self-adjoint,
\[
 Q_3(H+iB_U)=Q_3(H)+Q_3(B_U).                            \tag{5}
\]
It remains to prove the lower bound for these two terms jointly.

## 2. Matrix-unit kernel

For strings \(x,y,x',y'\), tensoring the one-site formula
\[
 \left\langle E_{ab},
 \left(\operatorname{id}-\frac12\operatorname{Tr}(\cdot)I\right)
 E_{cd}\right\rangle
 =\delta_{ac}\delta_{bd}-\frac12\delta_{ab}\delta_{cd}
\]
gives
\[
 \boxed{
 {\cal G}(x,y;x',y')
 =\prod_{j=1}^3\left(
 \delta_{x_jx'_j}\delta_{y_jy'_j}
 -\frac12\delta_{x_jy_j}\delta_{x'_jy'_j}\right).}
                                                               \tag{6}
\]
Every value is an integer multiple of \(1/8\).

For four fixed strings, the value of every entry in (6) depends only
on the equality partition of the four local symbols
\[
 (p_{0j},p_{1j},n_{0j},n_{1j})                           \tag{7}
\]
at each of the three sites.  There are exactly fifteen set
partitions of four labelled objects.  Hence all local dimensions are
covered by the finite set of \(15^3\) triples of partitions.  We retain
only triples for which the four resulting global strings are distinct.

## 3. The ten negative-quadrature types

Write
\[
 u=(U_{00},U_{01},U_{10},U_{11}).
\]
For the four forward dyads
\[
 |p_0\rangle\langle n_0|,\quad
 |p_0\rangle\langle n_1|,\quad
 |p_1\rangle\langle n_0|,\quad
 |p_1\rangle\langle n_1|
                                                               \tag{8}
\]
and their adjoints, let \(G_B\) be \(8{\cal G}\), so that \(G_B\)
has integral entries.

Exact enumeration of the \(15^3\) equality-pattern triples gives the
following complete statement.

* If \(Q_3(H)<0\), then \(Q_3(H)\) is either \(-1/8\) or \(-1/4\).
* There are exactly ten possible Gram types.
* In every type the forward/adjoint cross block vanishes, and both
  diagonal \(4\times4\) blocks equal one of the ten diagonal matrices
  in the table below.

\[
\begin{array}{c|c|c|c}
\text{type}&Q_3(H)&
G_B^{\rm forward}&Q_3(B_U)\\ \hline
1&-1/8&\operatorname{diag}(2,4,4,4)&(3+t)/8\\
2&-1/8&\operatorname{diag}(4,4,2,4)&(4-t)/8\\
3&-1/8&\operatorname{diag}(4,2,4,4)&(4-t)/8\\
4&-1/8&\operatorname{diag}(4,4,4,2)&(3+t)/8\\
5&-1/4&\operatorname{diag}(4,4,4,4)&1/2\\
6&-1/8&\operatorname{diag}(4,4,4,4)&1/2\\
7&-1/8&\operatorname{diag}(4,4,4,8)&(3-t)/4\\
8&-1/8&\operatorname{diag}(4,8,4,4)&(2+t)/4\\
9&-1/8&\operatorname{diag}(4,4,8,4)&(2+t)/4\\
10&-1/8&\operatorname{diag}(8,4,4,4)&(3-t)/4
\end{array}                                               \tag{9}
\]
Here
\[
 t=|U_{01}|^2=|U_{10}|^2\in[0,1],                       \tag{10}
\]
where the equality of the two moduli follows from unitarity of a
\(2\times2\) matrix.

For completeness, the last column follows directly from the diagonal
Gram profiles.  The coefficient vector of \(B_U\), in the order
forward then adjoint, is
\[
 \frac12(u,\overline u).
\]
Since the two diagonal Gram blocks agree and the cross block is zero,
\[
 Q_3(B_U)=\frac1{16}\,
 \overline u^{\,T}G_B^{\rm forward}u.                   \tag{11}
\]
The identities
\[
 |U_{00}|^2=|U_{11}|^2=1-t,\qquad
 |U_{01}|^2=|U_{10}|^2=t                                \tag{12}
\]
give the last column of (9).

The table is a finite exact certificate rather than a numerical
classification.  The checker constructs all fifteen local set
partitions, enumerates their \(15^3\) triples, evaluates (6) using
integers \(8{\cal G}\), and reproduces the ten displayed profiles.

## 4. Positivity and equality

For types \(1\)--\(4\), the last column of (9) is at least \(3/8\).
For type \(5\), it is \(1/2\).  Types \(6\)--\(10\) are also at least
\(1/2\).  Therefore
\[
\begin{aligned}
Q_3(H)=-\frac18&\quad\Longrightarrow\quad
Q_3(C_U)\ge-\frac18+\frac38=\frac14,\\
Q_3(H)=-\frac14&\quad\Longrightarrow\quad
Q_3(C_U)=-\frac14+\frac12=\frac14.
\end{aligned}                                             \tag{13}
\]
Equality occurs in type \(5\) for every \(U\), and in types \(1\)--\(4\)
at the appropriate endpoint \(t=0\) or \(t=1\).  Hence the constant
\(1/4\) is sharp.

## 5. Scope

This theorem does not prove unrestricted three-copy positivity, nor
does it assert a \(1/4\) lower bound when \(Q_3(H)\ge0\) (zero
completions occur there).  It closes a concrete falsifier mechanism:
four orthogonal product strings, a negative diagonal
inertia-\((2,2)\) quadrature, and every unitary rank-two square-zero
completion.  A negative nonnormal witness, if one exists, must use
entangled quadrature eigenvectors or a non-unitary/non-balanced
coupling not reducible to (1).
