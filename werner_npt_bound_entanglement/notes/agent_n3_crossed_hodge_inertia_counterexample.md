# A positive-definite crossed-Hodge inertia counterexample

## Status

This note gives an exact obstruction to a proposed same-\(C\)
compatibility route for the unrestricted three-copy problem.

For a rank-two coefficient matrix \(C\), fix one qutrit site, write
its environment blocks as \(C_{ap}\in M_9\), and define
\[
 \beta_{ap,bq}={\cal B}_2(C_{ap},C_{bq}),\qquad
 {\cal B}_2(D,E)=\langle D,{\cal L}^{\otimes2}(E)\rangle,
 \quad
 {\cal L}(D)=D-\frac12\operatorname{Tr}(D)I_3.             \tag{1}
\]
Let \(\Gamma\) transpose the second qutrit index of \(\beta\), and
let \(P_-\) project onto
\(\bigwedge^2\mathbb C^3\subset\mathbb C^3\otimes\mathbb C^3\).

The tempting conjecture
\[
 \operatorname{ind}_-\!\left(P_-\beta^\Gamma P_-\right)\leq1
 \tag{2}
\]
is false, even under the additional assumption \(\beta\succ0\).
Thus neither rank two alone nor rank two together with positivity of
the complete block Gram can exclude the isotropic large-slack model.
Exact isotropy, the critical equations, or another genuinely global
condition must be used.

This is a counterexample only to the intermediate inertia claim.  Its
three-copy endpoint value is positive, so it is not a Werner
distillation witness.

The dependency-free checker is
`verification/verify_n3_crossed_hodge_inertia_counterexample.py`.

## 1. Exact rank-two matrix

Use the computational basis \(\{|abc\rangle:0\leq a,b,c\leq2\}\).
Define
\[
\begin{aligned}
 x_0&=|211\rangle-|212\rangle,\\
 x_1&=-|012\rangle-|100\rangle+\frac12|201\rangle,\\
 y_0&=-|011\rangle-|211\rangle,\\
 y_1&=-|011\rangle+|100\rangle-\frac14|221\rangle,
\end{aligned}                                             \tag{3}
\]
and
\[
 C=x_0y_0^\dagger+x_1y_1^\dagger.                        \tag{4}
\]
The pairs \(x_0,x_1\) and \(y_0,y_1\) are each linearly independent.
Hence \(C=XY^\dagger\), with both \(X\) and \(Y\) of column rank two,
has
\[
 \operatorname{rank}C=2.                                 \tag{5}
\]

We take the first qutrit as the displayed block site.  Direct use of
(1) gives the following exact matrix:
\[
128\beta=
\begin{pmatrix}
64&0&0&0&0&0&64&0&64\\
0&128&0&0&0&0&0&0&0\\
0&0&8&0&0&0&0&0&0\\
0&0&0&128&0&0&0&0&0\\
0&0&0&0&32&0&32&0&32\\
0&0&0&0&0&8&0&0&0\\
64&0&0&0&32&0&112&0&96\\
0&0&0&0&0&0&0&16&0\\
64&0&0&0&32&0&96&0&97
\end{pmatrix}.                                            \tag{6}
\]
The ordered indices are
\[
 (00),(01),(02),(10),(11),(12),(20),(21),(22).
\]

## 2. Strict positivity of the block Gram

The nine leading principal minors of \(\beta\) are
\[
 \frac12,\ \frac12,\ \frac1{32},\ \frac1{32},\
 \frac1{128},\ \frac1{2048},\ \frac1{16384},\
 \frac1{131072},\ \frac1{16777216}.                       \tag{7}
\]
They are all strictly positive.  Sylvester's criterion therefore
proves
\[
 \boxed{\beta\succ0.}                                     \tag{8}
\]
In particular, the failure below cannot be attributed to the
indefiniteness of the two-copy block Gram.

## 3. Two negative antisymmetric directions

Use the orthonormal Hodge basis
\[
\begin{aligned}
 z_1&=\frac{|01\rangle-|10\rangle}{\sqrt2},\\
 z_2&=\frac{|02\rangle-|20\rangle}{\sqrt2},\\
 z_3&=\frac{|12\rangle-|21\rangle}{\sqrt2}.
\end{aligned}                                             \tag{9}
\]
On this basis the crossed compression is
\[
\boxed{
 K:=P_-\beta^\Gamma P_-
 =
 \begin{pmatrix}
 1&0&1/8\\
 0&-1/32&0\\
 1/8&0&-5/32
 \end{pmatrix}.}                                         \tag{10}
\]
The middle coordinate is a negative eigenvector.  The determinant of
the remaining \(2\times2\) block is
\[
 -\frac5{32}-\frac1{64}=-\frac{11}{64}<0,                \tag{11}
\]
so that block has one negative and one positive eigenvalue.  Hence
\[
 \boxed{\operatorname{ind}_-(K)=2.}                       \tag{12}
\]
For reference, the three eigenvalues are
\[
 -\frac1{32},\qquad
 \frac{27-\sqrt{1433}}{64},\qquad
 \frac{27+\sqrt{1433}}{64}.                              \tag{13}
\]
Equivalently, its characteristic and minimal polynomial is
\[
 \left(\lambda+\frac1{32}\right)
 \left(\lambda^2-\frac{27}{32}\lambda-\frac{11}{64}\right).
 \tag{14}
\]
The three roots are distinct, so the displayed product is indeed
minimal as well as characteristic.

## 4. Exact scope of the obstruction

The block identity
\[
 Q_3(C)=\operatorname{Tr}\beta
 -\frac12\langle\operatorname{vec}I,\beta
 \operatorname{vec}I\rangle                              \tag{15}
\]
gives here
\[
 \operatorname{Tr}\beta=\frac{593}{128},\qquad
 \langle\operatorname{vec}I,\beta\operatorname{vec}I\rangle
 =\frac{385}{128},
\qquad
 Q_3(C)=\frac{801}{256}>0.                               \tag{16}
\]
Therefore (4) does not decide unrestricted three-copy positivity.
It proves the narrower and useful negative result:

\[
\boxed{\begin{minipage}{0.87\linewidth}
The Hodge/logical-\(\epsilon\) decomposition cannot end in a universal
``positive semidefinite minus one square'' formula for
\(P_-\beta^\Gamma P_-\), even when the structured block Gram
\(\beta\) is positive definite.  Any valid exclusion of the
large-slack isotropic target must retain more of the exact stationary
or multi-site common-\(C\) structure.
\end{minipage}}                                           \tag{17}
\]

In particular, this calculation does **not** decide whether the exact
stationary isotropic family
\[
 \beta=A|\operatorname{vec}I\rangle\langle\operatorname{vec}I|+BI_9
 \tag{18}
\]
is realizable.  It rules out only the proposed route that tried to
exclude that family from positivity and rank two through a universal
inertia-one theorem.
