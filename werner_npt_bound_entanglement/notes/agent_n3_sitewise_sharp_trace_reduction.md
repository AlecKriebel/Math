# A sitewise sharp-trace reduction of the unrestricted three-copy problem

## Status

This note reduces unrestricted qutrit three-copy positivity to one
sharp inequality at any chosen physical site.  In \(3\times3\) block
notation the remaining theorem is
\[
\boxed{
 Q_2\!\left(\sum_{a=0}^2 C_{aa}\right)
 \leq
 2\sum_{a,b=0}^2 Q_2(C_{ab})
 \qquad(\operatorname{rank}C\leq2).
}                                                        \tag{1}
\]
Every block \(C_{ab}\) has rank at most two, but the common diagonal
sum can have rank six.  Thus (1) retains exactly the nonlinear
common-origin information which is absent from separate block
positivity.

The constant \(2\) is sharp.  The qutrit GHZ projection gives equality
while every two-pair face slack is strictly positive.  Consequently a
proof cannot force equality onto a coordinate face or into the kernel
of one of the established two-pair inequalities.

This is an exact reduction, not a proof of (1).  The dependency-free
checker is
`verification/verify_n3_sitewise_sharp_trace_reduction.py`.

## 1. Sitewise quantities

Fix a site \(i\), and let \(j,k\) denote the other two sites.  Put
\[
\begin{aligned}
 q_i
 &:=
 \left\langle C,
 (\operatorname{id}_i\otimes{\cal L}_j\otimes{\cal L}_k)(C)
 \right\rangle,\\
 T_i&=\operatorname{Tr}_i C,\qquad
 t_i=Q_2(T_i),
\end{aligned}                                            \tag{2}
\]
where
\[
 {\cal L}(A)=A-\frac12\operatorname{Tr}(A)I_3.
\]
Split \(T_i\) by its number of traceless factors on \(j,k\), and let
\[
 w_i=\|(T_i)_{\mathrm{traceless,traceless}}\|_2^2.
                                                               \tag{3}
\]
If \(c_i\) is the three-copy sector mass which is scalar at site
\(i\) and traceless at both other sites, then tracing the scalar
factor gives
\[
\boxed{\qquad w_i=3c_i.\qquad}                           \tag{4}
\]

Define the two exact slacks already supplied by the two-pair theorem:
\[
 r_i=\frac32w_i-t_i,\qquad
 s_i=3q_i-t_i.                                          \tag{5}
\]
The rank-six trace estimate for \(T_i\) gives \(r_i\geq0\), and the
block-Haar estimate gives \(s_i\geq0\).

## 2. The identity is sitewise

Orthogonally splitting \(C\) into its scalar and traceless parts at
site \(i\) gives the exact recursion
\[
\boxed{\qquad Q_3(C)=q_i-\frac12t_i.\qquad}              \tag{6}
\]
Using (4)--(6), direct algebra gives, for each site separately,
\[
\boxed{
 2r_i+4s_i-9c_i
 =12Q_3(C).
}                                                        \tag{7}
\]
Indeed,
\[
\begin{aligned}
2r_i+4s_i-9c_i
&=2\left(\frac92c_i-t_i\right)
  +4(3q_i-t_i)-9c_i\\
&=12q_i-6t_i.
\end{aligned}
\]

Thus summing the three sites is unnecessary.  The unrestricted
three-copy theorem is equivalent, for any one fixed site \(i\), to
\[
\boxed{\qquad t_i\leq2q_i.\qquad}                        \tag{8}
\]
The established two-pair theorem gives only
\[
2q_i-t_i+w_i\geq0,                                      \tag{9}
\]
while its two independent ingredients give
\[
t_i\leq3q_i,\qquad t_i\leq\frac32w_i.                   \tag{10}
\]
Neither inequality in (10), separately or by a nonnegative linear
combination, yields the sharp constant in (8).  The missing step must
couple their two common rank-two origins.

## 3. Intrinsic block form

Choose a basis on site \(i\) and write
\[
 C=[C_{ab}]_{a,b=0}^2,\qquad C_{ab}\in M_9.             \tag{11}
\]
Every block is a row-and-column compression of \(C\), hence
\[
 \operatorname{rank}C_{ab}\leq2.                        \tag{12}
\]
Because the two-copy endpoint superoperator acts only on sites
\(j,k\), block orthogonality gives
\[
\boxed{\qquad
 q_i=\sum_{a,b=0}^2Q_2(C_{ab}).
\qquad}                                                   \tag{13}
\]
The simultaneous trace on site \(i\) is
\[
\boxed{\qquad
 T_i=\sum_{a=0}^2C_{aa}.
\qquad}                                                   \tag{14}
\]
Substitution of (13)--(14) into (8) is exactly (1).

There is no rank bound usable directly on the right side of (14):
\[
\operatorname{rank}T_i\leq
 3\operatorname{rank}C\leq6
\]
is sharp.  The problem in (1) is therefore not another application
of two-copy positivity.  It is a common-factor inequality for the
nine blocks
\[
 C_{ab}=U_aV_b^\dagger
\]
coming from one factorization \(C=UV^\dagger\) with two columns.

## 4. Sharp strict-face equality

Let
\[
 C_{\mathrm{GHZ}}
 =
 |000\rangle\langle000|
 +|111\rangle\langle111|.                               \tag{15}
\]
It is a rank-two orthogonal projection.  Direct contraction gives,
for every site \(i\),
\[
\boxed{
 q_i=\frac12,\qquad
 t_i=1,\qquad
 w_i=\frac{10}{9},\qquad
 c_i=\frac{10}{27}.
}                                                        \tag{16}
\]
Hence
\[
 r_i=\frac23,\qquad s_i=\frac12,                        \tag{17}
\]
and (7) is an equality:
\[
 2r_i+4s_i=9c_i=\frac{10}{3}.
\]
All six numbers in (16)--(17) are strictly positive.  In particular,
each established two-pair residual has the strict value
\[
 2Q_3(C_{\mathrm{GHZ}})+w_i=\frac{10}{9}>0,             \tag{18}
\]
even though the full residual vanishes.

Thus full equality need not arise from equality in any one- or
two-component face.  A determinant proof must retain a genuine
three-way cancellation.

## 5. A nonnormal isoclinic equality model

The strict-face phenomenon is compatible with strongly nonnormal
boundary geometry.  On sites \(1,2\), put
\[
 |a\rangle=\frac{|00\rangle+|11\rangle}{\sqrt2},
 \qquad
 |b\rangle=\frac{|00\rangle+|12\rangle}{\sqrt2},
                                                               \tag{19}
\]
and on site \(3\) put
\[
 P=|0\rangle\langle0|+|1\rangle\langle1|.
\]
Then
\[
 C=|a\rangle\langle b|\otimes P                         \tag{20}
\]
has rank two and
\[
 Q_3(C)=Q_2(|a\rangle\langle b|)\,Q_1(P)=0.             \tag{21}
\]
Its two nonzero singular values are equal.  The left and right
singular planes have principal cosines \(1/2,1/2\), and every
one-site marginal of either plane has spectrum \((0,1,1)\).  Yet
\[
 \|CC^\dagger-C^\dagger C\|_2^2=3.                     \tag{22}
\]
This exact example explains why unrestricted numerical minimizers can
be highly nonnormal and have all three degree-two masses nonzero while
still lying on the local-support boundary.  It is not evidence for
the missing inequality (1).

## 6. Remaining lemma

The whole same-copy \(n=3\) endpoint is now the sharp block-trace
inequality (1).  A proof has to improve the exact Haar constant
\[
 Q_2\!\left(\sum_aC_{aa}\right)
 \leq3\sum_{a,b}Q_2(C_{ab})                             \tag{23}
\]
from \(3\) to \(2\), using the common factorization
\[
 C_{ab}=U_aV_b^\dagger.
\]
The GHZ example proves that \(2\) cannot be improved.
