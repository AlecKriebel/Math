# An exact hard-region counterexample to the first radical-free bound

## Status

This note gives an exact counterexample to an intermediate inequality.
It is **not** a negative three-copy Werner witness and is not
square-zero.

For a rank-at-most-two matrix on three copies, write
\[
\begin{aligned}
 N&=\|C\|_2^2,\\
 S&=\sum_i\|\operatorname{Tr}_iC\|_2^2,\\
 P&=\sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2,\\
 A&=3N-2S+P,\\
 D&=s_1(C)s_2(C),\\
 T&=\|C^2\|_2.
\end{aligned}                                           \tag{1}
\]
The proposed radical-free strengthening was
\[
\boxed{\qquad A^2\leq4D^2+4T^2
       \quad\hbox{whenever }A<0.\qquad}                 \tag{2}
\]
If true, (2) would imply
\[
 A+2D\geq-2T
\]
on the hard region and hence the desired exterior inequality on
\(C^2=0\).

The Gaussian-integer construction below has rank exactly two and
satisfies
\[
\boxed{
 A<0,\qquad
 A^2-4D^2-4T^2
 =1288150978594641>0.}                                  \tag{3}
\]
Thus (2) is false even with its hard-region hypothesis.

The dependency-free exact checker is
`verification/verify_n3_radical_free_quartic_counterexample.py`.

## 1. Exact construction

Use binary-word order
\[
 000,001,010,011,100,101,110,111
\]
inside three qutrits.  Define the \(8\times2\) Gaussian-integer
matrices
\[
X=
\begin{pmatrix}
30-68i&20\\
-4-4i&-29+15i\\
18+59i&60-27i\\
21+6i&-7+17i\\
28-108i&12-33i\\
54+100i&61+54i\\
37+99i&61-60i\\
-104-73i&29+74i
\end{pmatrix},                                         \tag{4}
\]
and
\[
Y=
\begin{pmatrix}
62-80i&47-67i\\
-74+20i&-28-36i\\
-49+106i&42-61i\\
34-30i&-63-24i\\
66+47i&27+12i\\
73-74i&29+i\\
-84-9i&25+33i\\
-16+84i&66-13i
\end{pmatrix}.                                         \tag{5}
\]
Put
\[
\boxed{C=XY^\dagger.}                                  \tag{6}
\]
The two factor Grams are
\[
X^\dagger X=
\begin{pmatrix}
62517&591-19093i\\
591+19093i&27641
\end{pmatrix},                                         \tag{7}
\]
\[
Y^\dagger Y=
\begin{pmatrix}
63632&-476-7480i\\
-476+7480i&26762
\end{pmatrix}.                                         \tag{8}
\]
Their determinants are respectively
\[
1363140467,\qquad1646742608,                            \tag{9}
\]
both positive.  Hence \(X\) and \(Y\) have full column rank and
\(C=XY^\dagger\) has rank exactly two.

## 2. Exact invariant certificate

Direct simultaneous partial contraction gives
\[
\boxed{
\begin{aligned}
 N&=5002878834,\\
 S&=11103088421,\\
 P&=4142165753,
\end{aligned}}                                         \tag{10}
\]
and therefore
\[
\boxed{A=-3055374587<0.}                               \tag{11}
\]

For a full-column factorization \(C=XY^\dagger\),
\[
 D^2=\det(X^\dagger X)\det(Y^\dagger Y).
\]
Thus (9) gives
\[
\boxed{D^2=2244741487697917936.}                       \tag{12}
\]
Exact multiplication of (6) gives
\[
\boxed{T^2=\|C^2\|_2^2=88764941278788546.}              \tag{13}
\]
Finally,
\[
\begin{aligned}
 A^2-4D^2&=356347916093748825,\\
 A^2-4D^2-4T^2&=1288150978594641>0,                    \tag{14}
\end{aligned}
\]
which proves (3).

Equivalently, this exact code forces the coefficient \(k\) in any
replacement
\[
 A^2\leq4D^2+kT^2\qquad(A<0)                           \tag{15}
\]
to satisfy
\[
\boxed{\qquad
 k\geq
 \frac{356347916093748825}{88764941278788546}
 >4.
\qquad}                                                 \tag{16}
\]
The displayed rational number is approximately \(4.01451\).
Discovery optimization before rational rounding reached approximately
\(4.04103\), but that decimal is not used as evidence.

For completeness, the matrix is not a Werner witness:
\[
 8Q_3(C)=3852298452>0.                                 \tag{17}
\]
It only disproves the proposed route to square-zero positivity.

## 3. Relation to the rank-one tangent obstruction

For the exact product--tangent family
\[
 C_t=|000\rangle\langle W_1|
     +t|W_1\rangle\langle W_2|,
\]
from `agent_n3_csquare_tangent_obstruction.md`, one has
\[
 A_t=-\frac4{\sqrt3}t+\frac53t^2,\qquad
 D_t=T_t=t.
\]
Consequently
\[
\boxed{
\lim_{t\downarrow0}
\frac{A_t^2-4D_t^2}{T_t^2}
=\frac43.}                                             \tag{18}
\]
Thus the tangent family did not threaten the coefficient \(4\) in
(2); the present counterexample is a genuinely finite-distance
obstruction.

No finite universal coefficient \(k\) in (15) is established or
refuted here.  The exact conclusion is only that \(k=4\) fails on the
hard region and that any surviving coefficient must exceed the
rational lower bound (16).

