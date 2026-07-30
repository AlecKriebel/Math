# The exact full-dual triangle determinant and its saturated-face boundary

## Status

This note reduces the last unrestricted three-copy dual residual to
one scalar \(3\times3\) determinant for each fixed triple of pair
directions.  It also proves a new common-origin boundary theorem:

> If a diagonal or a \(2\times2\) principal minor of that determinant
> is zero, then the complete three-component residual is already
> nonnegative.

Thus a counterexample to the unrestricted three-copy endpoint cannot
occur on the boundary detected by any of the established one- or
two-pair theorems.  It must have three positive diagonal defects and
three strictly positive \(2\times2\) principal determinants.  In
normalized variables, the only remaining issue is one strict-interior
cyclic Bargmann inequality.

This is a boundary theorem for the **full three-component residual**,
not merely a restatement of pair-only positivity.  It does not prove
the strict-interior determinant.

The dependency-free exact checker is
`verification/verify_n3_full_dual_triangle_determinant.py`.

## 1. Pair frames

Fix an isometry
\[
 V:\mathbb C^2\longrightarrow(\mathbb C^3)^{\otimes3}
\]
and use the logical-qubit vectorization of the preceding full-dual
reduction.  Let \(S=S_V\succ0\) be its low-sector Schur operator.

Index the three physical pairs by
\[
 {\cal E}=\{12,13,23\}.
\]
For \(e\in{\cal E}\), let \({\cal K}_e\) be the Hilbert space of
doubly traceless pair coefficients on \(e\), with the
Hilbert--Schmidt norm, and define
\[
 T_e:{\cal K}_e\longrightarrow
 (\mathbb C^3)^{\otimes3}\otimes\mathbb C^2,
 \qquad
 T_e(B_e)=B_e^{(e)}V.                                    \tag{1}
\]
The exact pair frame used in the primal two-face theorem is
\[
 F_e=\frac12T_eT_e^\dagger.                              \tag{2}
\]
In the notation \(P=|\boldsymbol V\rangle
\langle\boldsymbol V|/2\) and \(E_i=e_i-\operatorname{id}/3\), this
is the previously established identity
\[
 F_{ij}=E_iE_j(P).                                       \tag{3}
\]

Choose one coefficient \(B_e\in{\cal K}_e\) for every edge and put
\[
 Y_e=S^{-1/2}T_e(B_e),                                   \tag{4}
\]
\[
 d_e=2\|B_e\|_2^2-\|Y_e\|_2^2,\qquad
 c_{ef}=\langle Y_e,Y_f\rangle
 \quad(e<f).                                             \tag{5}
\]
Here and below the inner product is conjugate-linear in its first
argument.

## 2. The exact determinant

Order the edges arbitrarily as \(1,2,3\), and define
\[
 G=
 \begin{pmatrix}
 d_1&-c_{12}&-c_{13}\\
 -\overline{c_{12}}&d_2&-c_{23}\\
 -\overline{c_{13}}&-\overline{c_{23}}&d_3
 \end{pmatrix}.                                         \tag{6}
\]
For arbitrary scalars \(\lambda_1,\lambda_2,\lambda_3\), direct
expansion gives
\[
\boxed{
 \lambda^\dagger G\lambda
 =
 2\sum_e|\lambda_e|^2\|B_e\|_2^2
 -
 \left\|
 \sum_e\lambda_eY_e
 \right\|_2^2 .
}                                                        \tag{7}
\]
Because the \(B_e\)'s occupy orthogonal coefficient sectors, the
right side is exactly the full residual for the rescaled triple
\((\lambda_eB_e)_e\).

The single-pair theorem gives
\[
 d_e\geq0.                                               \tag{8}
\]
The full two-pair theorem, applied to every scalar multiple of
\(B_e,B_f\), gives
\[
 \begin{pmatrix}
 d_e&-c_{ef}\\
 -\overline{c_{ef}}&d_f
 \end{pmatrix}\succeq0,
 \qquad
 |c_{ef}|^2\leq d_ed_f.                                 \tag{9}
\]
Thus every proper principal minor of \(G\) is already nonnegative.
A Hermitian \(3\times3\) matrix is positive semidefinite exactly when
all its principal minors are nonnegative.  Consequently the
unrestricted three-copy residual is equivalent to the single
remaining condition
\[
\boxed{
 \det G
 =
 d_1d_2d_3
 -d_1|c_{23}|^2-d_2|c_{13}|^2-d_3|c_{12}|^2
 -2\operatorname{Re}
   \left(c_{12}c_{23}\overline{c_{13}}\right)
 \geq0 .
}                                                        \tag{10}
\]
This equivalence is lossless.  If (10) fails, a negative eigenvector
of \(G\) supplies scalars \(\lambda_e\) in (7), hence a violation of
the full inverse-marginal residual.  Conversely, every full residual
violation appears in this way by taking its three nonzero pair
components as the fixed directions.

If \(d_1d_2d_3>0\), put
\[
 z_{ef}=\frac{c_{ef}}{\sqrt{d_ed_f}}.                    \tag{11}
\]
Then \(|z_{ef}|\leq1\), and (10) is the normalized cyclic Bargmann
inequality
\[
\boxed{
 1-|z_{12}|^2-|z_{13}|^2-|z_{23}|^2
 -2\operatorname{Re}
 \left(z_{12}z_{23}\overline{z_{13}}\right)\geq0 .
}                                                        \tag{12}
\]
Equivalently, taking edge \(1\) as a pivot,
\[
\boxed{
 \left|z_{23}+\overline{z_{12}}z_{13}\right|^2
 \leq
 (1-|z_{12}|^2)(1-|z_{13}|^2).
}                                                        \tag{13}
\]
Equations (12)--(13) isolate both the magnitude and the cyclic phase
which are discarded by treating the three pair contributions
independently.

## 3. A complete-square equality identity

For two edges \(e,f\), write
\[
 T_{ef}(B_e,B_f)=T_eB_e+T_fB_f,\qquad
 F_{ef}=F_e+F_f=\frac12T_{ef}T_{ef}^\dagger.             \tag{14}
\]
For \(b=(B_e,B_f)\), put
\[
 y=T_{ef}b,\qquad z=S^{-1}y.
\]
The following identity is exact:
\[
\boxed{
\begin{aligned}
 2\|b\|^2-\langle y,S^{-1}y\rangle
 ={}&
 2\left\|b-\frac12T_{ef}^\dagger z\right\|^2\\
 &+\langle z,(S-F_e-F_f)z\rangle .
\end{aligned}}                                          \tag{15}
\]
Indeed, expand the square, use \(y=Sz\), and use
\(F_{ef}=T_{ef}T_{ef}^\dagger/2\).

The established two-pair theorem is precisely
\[
 S-F_e-F_f\succeq0.                                     \tag{16}
\]
It follows from (15) that equality in a two-pair dual residual forces
\[
 b=\frac12T_{ef}^\dagger z,\qquad
 (S-F_e-F_f)z=0.                                        \tag{17}
\]

Let \(g\) be the missing third edge.  The intrinsic transition matrix
\(C_z\) associated with \(z\) has rank at most two.  The exact
two-face proof identifies
\[
 \langle z,(S-F_e-F_f)z\rangle
 =
 2Q_3(C_z)+3c_g(C_z),                                   \tag{18}
\]
where
\[
 3c_g(C_z)
 =
 w_2(\operatorname{Tr}_{i(g)}C_z)
 =
 \langle z,F_gz\rangle.                                 \tag{19}
\]
Here \(i(g)\) is the physical site complementary to the pair \(g\).
More importantly, the equality classification in that proof is
\[
 \langle z,(S-F_e-F_f)z\rangle=0
 \quad\Longrightarrow\quad
 w_2(\operatorname{Tr}_{i(g)}C_z)=0.                    \tag{20}
\]
Combining (19)--(20) and \(F_g=T_gT_g^\dagger/2\) gives the
common-origin phase constraint
\[
\boxed{
 T_g^\dagger z=0.
}                                                        \tag{21}
\]
This is the information which is invisible in the three isolated
\(2\times2\) principal-minor inequalities.

## 4. Saturated faces are globally safe

### Theorem 4.1

For fixed \(V\) and fixed directions \(B_1,B_2,B_3\), suppose that
at least one diagonal entry or one \(2\times2\) principal determinant
of \(G\) vanishes.  Then
\[
 G\succeq0.
 \tag{22}
\]
In particular, the full three-component residual is nonnegative for
every scalar combination of these directions.

### Proof

If \(d_e=0\), (9) gives \(c_{ef}=0\) for both other edges.  Thus the
\(e\)-th row and column of \(G\) vanish, and the remaining
\(2\times2\) principal block is positive semidefinite by (9).

Now suppose \(d_e,d_f>0\) and
\[
 d_ed_f-|c_{ef}|^2=0.                                   \tag{23}
\]
The positive semidefinite \(ef\)-principal block has a nonzero kernel
vector \(\lambda=(\lambda_e,\lambda_f)\).  Apply (15) to
\[
 b=(\lambda_eB_e,\lambda_fB_f).
\]
Its left side is zero by (23), so (17) holds.  Equation (21) then
gives \(T_g^\dagger z=0\).  For every \(B_g\),
\[
\begin{aligned}
 \sum_{h=e,f}\overline{\lambda_h}G_{hg}
 &=
 -\left\langle
 S^{-1/2}\sum_{h=e,f}\lambda_hT_hB_h,\,
 S^{-1/2}T_gB_g
 \right\rangle\\
 &=-\langle z,T_gB_g\rangle
 =-\langle T_g^\dagger z,B_g\rangle
 =0.                                                     \tag{24}
\end{aligned}
\]
Thus the kernel of the saturated \(ef\)-block is also annihilated by
the full third column.  Hence \(G\) has a nonzero kernel and
\(\det G=0\).  All its proper principal minors are nonnegative by
(8)--(9), so \(G\succeq0\).
\(\square\)

In the normalized variables, saturation
\(|z_{12}|=1\) therefore forces the exact phase transport
\[
\boxed{
 z_{23}=-\overline{z_{12}}z_{13},
}                                                        \tag{25}
\]
and (13) is an equality.  This is not a generic consequence of three
pairwise positive \(2\times2\) matrices; it uses the vanishing
\(w_2\)-term in the common two-face equality classification.

## 5. Strict-interior frontier

The only remaining case has
\[
\boxed{
 d_1d_2d_3>0,\qquad |z_{12}|,|z_{13}|,|z_{23}|<1.
}                                                        \tag{26}
\]
There the complete unrestricted problem is exactly (13).  A negative
determinant would have to violate the common Gram-disc condition
\[
 z_{23}\in
 -\overline{z_{12}}z_{13}
 +
 \sqrt{(1-|z_{12}|^2)(1-|z_{13}|^2)}\,\overline{\mathbb D}.
 \tag{27}
\]
The center in (27) is fixed by the same phase transport which becomes
exact on a saturated face.  The remaining task is quantitative:
control the displacement from that center by the two strict
two-face slacks without discarding their common rank-two transition
matrix.
