# The normal residual as a signed Fierz--Hessian fourth moment

## Status

This note combines the norm-constrained rank-two Hessian with the
individual-label signed Fierz colligation.  It gives two exact facts
about any hypothetical normalized negative minimizer.

First, its normal residual is uniformly large.  If
\[
 q=Q_3(C)<0,\qquad
 W={\cal L}(C)-qC,\qquad {\cal L}=L^{\otimes3},
\]
then
\[
\boxed{\qquad
 \|W\|_2^2
 =
 \frac5{48}-\frac{21}{8}q
 \frac98G+\frac1{12}\Xi-q^2
 >\frac5{48}.
 \qquad}                                                   \tag{1}
\]
Here \(G=\sum_i g_i(C)\) and
\(\Xi=\|C\|_2^2+6{\cal J}_3(C)\).

Second, tangent-Hessian positivity controls that same residual by one
coherent signed fourth moment:
\[
\boxed{\qquad
 \|W\|_2^2+\sum_Tw_T|p_T|
 \leq
 \sqrt{\left(\sum_Tw_T A_T\right)
       \left(\sum_Tw_T B_T\right)}.
 \qquad}                                                   \tag{2}
\]
All quantities in (2) are defined below.  Every \(T\) is an
individual tensor-Fierz label; the parity labels are not collapsed
before applying the Hessian.

Equations (1)--(2) reduce the second-variation route to one explicit
weighted fourth-moment estimate.  The universal tight-frame bounds
alone are far too weak.  A sufficient remaining lemma is
\[
\boxed{
 \sqrt{\left(\sum_Tw_T A_T\right)
       \left(\sum_Tw_T B_T\right)}
 -\sum_Tw_T|p_T|
 \leq
 \frac5{48}+\frac98G+\frac1{12}\Xi-q^2 .
}                                                         \tag{3}
\]
At a critical point, (1)--(3) force \(q\geq0\), equivalently the
desired
\[
 204G+45\|\Pi_1C\|_2^2+16\Xi
 \geq108\|\Pi_2C\|_2^2.
\]
Inequality (3) remains unproved.  It is strictly smaller than the
original rank-two optimization: it is a scalar inequality between
two linked Fierz leakage frames at one critical point.

The exact sector arithmetic is checked by
`verification/verify_n3_normal_residual_fierz_hessian.py`.  The
Fierz block identities used here are independently checked by
`verification/verify_n3_coherent_hodge_leakage_obstruction.py`.

## 1. Norm-constrained critical representative

If a negative rank-two matrix exists, the compact set
\[
 \{C:\operatorname{rank}C\leq2,\ \|C\|_2=1\}
\]
has a negative global minimizer.  Rank-one matrices have strictly
positive endpoint energy, so the minimizer has rank exactly two and
lies on the smooth stratum.  Write
\[
 C=U\Sigma V^\dagger,\qquad
 \Sigma=\operatorname{diag}(s_1,s_2),\qquad
 s_1^2+s_2^2=1.
                                                               \tag{4}
\]
The tangent space consists of all matrices whose
\((U^\perp,V^\perp)\) block vanishes.  Lagrange multipliers for the
unit sphere therefore give
\[
\boxed{
 {\cal L}(C)=qC+W,\qquad
 W=(I-P_U){\cal L}(C)(I-P_V).
}                                                         \tag{5}
\]
The multiplier is \(q\), since taking the inner product with \(C\)
in (5) gives \(q=Q_3(C)\).  In particular
\[
 \langle C,W\rangle=0,\qquad
 \|W\|_2^2=\|{\cal L}(C)\|_2^2-q^2.                     \tag{6}
\]

## 2. Exact residual norm

Use the scalar/traceless degree masses
\[
 x=\|\Pi_0C\|_2^2,\quad
 a=\|\Pi_1C\|_2^2,\quad
 c=\|\Pi_2C\|_2^2,\quad
 d=\|\Pi_3C\|_2^2.
                                                               \tag{7}
\]
The four eigenvalues of \({\cal L}\) are
\[
 -\frac18,\quad\frac14,\quad-\frac12,\quad1.
\]
Consequently
\[
\begin{aligned}
 q&=-\frac18x+\frac14a-\frac12c+d,\\
 \|{\cal L}(C)\|_2^2
 &=\frac1{64}x+\frac1{16}a+\frac14c+d.                 \tag{8}
\end{aligned}
\]
The two nonlinear face invariants have the exact sector forms
\[
\begin{aligned}
 G&=\frac14a-c+3d,\\
 \Xi&=-5x+4a-\frac12c+\frac74d.                         \tag{9}
\end{aligned}
\]
Together with \(x+a+c+d=1\), direct elimination in (8)--(9)
gives
\[
\boxed{
 \|{\cal L}(C)\|_2^2
 =
 \frac5{48}-\frac{21}{8}q+\frac98G+\frac1{12}\Xi .
}                                                        \tag{10}
\]
Equations (6) and (10) prove the equality in (1).

For a negative minimizer, \(G>0\) by the strict Haar theorem and
\(\Xi>0\) by the classified triple-Hodge equality case.  Even without
using those strict inequalities,
\[
 -\frac{21}{8}q-q^2>0
 \qquad\left(-\frac12\leq q<0\right),
\]
so (1) follows.  Thus a counterexample cannot be a nearly reducing
two-plane for the endpoint superoperator: at least \(5/48\) of
normal-residual mass is forced.

## 3. Norm-constrained second variation

Let
\[
 X:\mathbb C^2\to U^\perp,\qquad
 Z:V^\perp\to\mathbb C^2.
\]
The one-sided tangent directions and their normal second fundamental
form are
\[
\begin{aligned}
 D_X&=X\Sigma V^\dagger,\\
 D_Z&=U\Sigma Z,\\
 N_{X,Z}&=X\Sigma Z.
\end{aligned}                                             \tag{11}
\]
The exact unit-sphere Hessian, obtained either from Stiefel geodesics
or a rank-two graph chart, gives
\[
\begin{aligned}
 A_X&:=Q_3(D_X)-q\|D_X\|_2^2\geq0,\\
 B_Z&:=Q_3(D_Z)-q\|D_Z\|_2^2\geq0,                       \tag{12}\\
 \left(
 |\langle D_X,{\cal L}(D_Z)\rangle|
 +|\langle W,N_{X,Z}\rangle|
 \right)^2
 &\leq A_XB_Z.
\end{aligned}
\]
Indeed, replacing \(X,Z\) by \(\alpha X,\beta Z\) makes the ordinary
cross term scale as \(\overline\alpha\beta\), while the normal term
scales as \(\alpha\beta\).  Their phase difference and phase sum are
independent, so both adverse phases can be attained simultaneously.

## 4. Insert the individual Fierz labels

Choose real Hilbert--Schmidt orthonormal symmetric and skew qutrit
matrix bases.  Let \(T=T_{R\mu}\) run through their threefold tensor
products and put
\[
 w_T=2^{-3}3^{|R|},\qquad
 \eta_T=(-1)^{|R|}.                                     \tag{13}
\]
Define the core and leakage blocks
\[
\begin{aligned}
 M_T&=U^\dagger T\overline V,\\
 X_T&=(I-P_U)T\overline V,\\
 Z_T&=(I-P_V)T\overline U.
\end{aligned}                                             \tag{14}
\]
The exact Fierz expansion of \({\cal L}\), followed by its
\((U^\perp,V^\perp)\) block, is
\[
\boxed{\qquad
 W=\sum_T\eta_Tw_T X_T\Sigma Z_T^\dagger .
\qquad}                                                   \tag{15}
\]
This identity is why individual labels and the parity twist must be
retained.

Specialize (11)--(12) to
\[
\begin{aligned}
 D_T^L&=X_T\Sigma V^\dagger,\\
 D_T^R&=U\Sigma Z_T^\dagger,\\
 N_T&=X_T\Sigma Z_T^\dagger,
\end{aligned}
\]
that is, take \(X=X_T\) and \(Z=Z_T^\dagger\),
and abbreviate
\[
\begin{aligned}
 A_T&=Q_3(D_T^L)-q\|D_T^L\|_2^2,\\
 B_T&=Q_3(D_T^R)-q\|D_T^R\|_2^2,\\
 p_T&=\langle D_T^L,{\cal L}(D_T^R)\rangle,\\
 r_T&=\langle W,N_T\rangle.
\end{aligned}                                             \tag{16}
\]
Then
\[
 |r_T|\leq\sqrt{A_TB_T}-|p_T|.                          \tag{17}
\]
Taking the inner product of (15) with \(W\), applying the triangle
inequality, (17), and weighted Cauchy--Schwarz gives
\[
\begin{aligned}
 \|W\|_2^2
 &\leq\sum_Tw_T|r_T|\\
 &\leq
 \sum_Tw_T\sqrt{A_TB_T}-\sum_Tw_T|p_T|\\
 &\leq
 \sqrt{\left(\sum_Tw_TA_T\right)
       \left(\sum_Tw_TB_T\right)}
 -\sum_Tw_T|p_T|.
\end{aligned}                                             \tag{18}
\]
This is (2).

## 5. Why frame norms alone do not finish

The exact weighted leakage-frame identities give
\[
 \sum_Tw_TX_T^\dagger X_T,\quad
 \sum_Tw_TZ_T^\dagger Z_T
 \preceq\frac{123}{8}I_2.                               \tag{19}
\]
Since the largest eigenvalue of \({\cal L}\) is \(1\),
\[
\begin{aligned}
 \sum_Tw_TA_T
 &\leq(1-q)\sum_Tw_T\|X_T\Sigma\|_2^2
 \leq\frac{123}{8}(1-q),\\
 \sum_Tw_TB_T
 &\leq\frac{123}{8}(1-q).                               \tag{20}
\end{aligned}
\]
Discarding the \(\sum w_T|p_T|\) correction in (2) therefore gives
only
\[
 \|W\|_2^2\leq\frac{123}{8}(1-q),                       \tag{21}
\]
which is automatic throughout \(-1/2\leq q<0\) after comparison with
(1).  Thus neither the tight-frame mass nor the normal Hessian term
alone is sufficient.

The remaining information is precisely the common signed fourth
moment in (3): the ordinary crossed responses \(p_T\), the two
one-sided Hessian energies, and the normal residual must be retained
as blocks of the same tensor-Fierz labels.  This identifies the
smallest missing second-variation lemma without introducing another
unrestricted matrix variable.
