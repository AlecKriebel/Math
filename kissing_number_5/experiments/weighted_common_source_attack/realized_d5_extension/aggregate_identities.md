# Exact aggregate identities for realized profiles

## Setup

Let \(x_i=r_i/\sqrt2\) be the twelve support vectors in `support.py`, let
\(P=\operatorname{diag}(p_1,\ldots,p_{12})\), and let
\(S=(\langle x_i,x_j\rangle)_{ij}\).  Direct exact calculation gives
\[
\sum_i p_i x_i=0,\qquad \sum_i p_i x_ix_i^{\mathsf T}=\frac15I_5.
\tag{1}
\]

Let \(y_1,\ldots,y_m\) be realized extension points and put
\[
H_{ai}=\langle y_a,x_i\rangle,\quad
G_{ab}=\langle y_a,y_b\rangle,\quad
B=\sum_{a=1}^m y_ay_a^{\mathsf T},\quad
c=\sum_{a=1}^m y_a.
\]

## Profile and rank identities

Writing \(X\) for the matrix with rows \(x_i^{\mathsf T}\) and \(Y\) for the
matrix with rows \(y_a^{\mathsf T}\), we have \(H=YX^{\mathsf T}\),
\(S=XX^{\mathsf T}\), and (1) says \(X^{\mathsf T}PX=I_5/5\).  Consequently
\[
\boxed{HPH^{\mathsf T}=\frac15G},\qquad
\boxed{HPSPH^{\mathsf T}=\frac1{25}G}.
\tag{2}
\]
In particular,
\[
\operatorname{rank}H=\operatorname{rank}G\le5,
\quad h_a^{\mathsf T}Ph_a=\frac15,
\quad h_a^{\mathsf T}PSPh_a=\frac1{25},
\tag{3}
\]
and the extension kissing constraints are exactly
\[
h_a^{\mathsf T}Ph_b\le\frac1{10}\qquad(a\ne b).
\tag{4}
\]
This is the aggregate form of the projection-membership equalities; no
relaxation of the rank condition has occurred.

Taking traces and Frobenius norms in (2) gives
\[
\sum_a h_a^{\mathsf T}Ph_a=\frac m5,
\qquad
\sum_{a,b}(h_a^{\mathsf T}Ph_b)^2
 =\frac1{25}\operatorname{tr}(G^2)
 \ge\frac{m^2}{125}.
\tag{5}
\]
The final inequality uses \(\operatorname{rank}G\le5\) and
\(\operatorname{tr}G=m\).  Also,
\[
\sum_{a,b}h_a^{\mathsf T}Ph_b
=\frac15\|c\|^2\ge0.
\tag{6}
\]
Equations (2), (5), and (6) remain true after restricting to any subset of
the extension points.

If
\[
e_i=\sum_a H_{ai}^2,
\]
then the column-energy identity is
\[
\sum_i p_i e_i=\frac m5.
\tag{7}
\]
For every support row, the scalar bound
\(-1\le H_{ai}\le1/2\) also gives the exact valid inequality
\[
e_i+\frac12\sum_a H_{ai}\le\frac m2,
\tag{8}
\]
by summing
\((1/2-t)(1+t)=1/2-t/2-t^2\ge0\).

## The exact polar region

Set \(z=\sqrt2y\), so \(\|z\|^2=2\).  The twelve support inequalities
\(r_i\cdot z\le1\) are equivalent to
\[
\begin{aligned}
z_4+|z_1|&\le1,&
-z_2+|z_3|&\le1,\\
z_2+|z_5|&\le1,&
-z_4+|z_3|&\le1,\\
|z_1|+|z_5|&\le1.
\end{aligned}
\tag{9}
\]
This is an exact equivalence, obtained simply by taking the maximum in each
pair or quadruple of signed linear inequalities.

The last inequality in (9) yields
\[
y_1^2+y_5^2
=\frac{z_1^2+z_5^2}{2}
\le\frac{(|z_1|+|z_5|)^2}{2}
\le\frac12.
\tag{10}
\]

## A \(3+2\) block frame inequality

For a whole extension code put
\[
R=\sum_a(y_{a1}^2+y_{a5}^2).
\]
Equation (10) gives \(0\le R\le m/2\).  Decompose
\(\mathbb R^5=U\oplus V\), where
\[
U=\operatorname{span}(e_2,e_3,e_4),\qquad
V=\operatorname{span}(e_1,e_5).
\]
The diagonal blocks \(B_U,B_V\) of the positive semidefinite frame operator
\(B\) have traces \(m-R,R\).  The off-diagonal block contributes a
nonnegative quantity to the Frobenius norm.  Cauchy--Schwarz on the three and
two eigenvalues therefore proves
\[
\boxed{\operatorname{tr}(G^2)=\operatorname{tr}(B^2)
\ge \frac{(m-R)^2}{3}+\frac{R^2}{2}.}
\tag{11}
\]
Equality requires the cross block to vanish and
\(B_U=(m-R)I_U/3,\ B_V=RI_V/2\).

This inequality is exact and uses the fixed polar region, but it does **not**
prove \(m\le28\).  Indeed, its right side is minimized at
\(R=2m/5\), which lies inside \(0\le R\le m/2\), and the resulting lower
bound is only \(m^2/5\), the ordinary rank-five frame-potential bound.

## Calibration on the known 28-point completion

For the other 28 normalized \(D_5\) roots, exact calculation gives
\[
c=0,\qquad B=\operatorname{diag}(5,6,6,6,5),\qquad R=10,
\qquad \operatorname{tr}(G^2)=158.
\tag{12}
\]
Thus (11) is an equality:
\[
\frac{(28-10)^2}{3}+\frac{10^2}{2}=108+50=158.
\]
This equality is a calibration datum, not a rigidity hypothesis.

## Precise remaining gap

To deduce \(m\le28\), an additional inequality must couple the off-diagonal
kissing restrictions (4) to the polar information (9).  Identities
(2)--(11) alone do not supply such a coupling.  In particular, minimizing
the block-frame bound over its rigorously available range silently discards
all improvement over the generic rank-five relaxation.
