# Hostile audit of the determinant-critical Hessian

## Status

This note independently audits the complete Hessian in
`agent_n3_determinant_critical_hessian.md`.  A determinant graph chart,
rather than Stiefel geodesics, gives the same formula, including the
factor two and the conjugation in the normal-curvature term.  The
Bell-companion Schur complement is also correct.

Two further exact conclusions are obtained.

1. Even the partial transpose of a **strictly positive** bipartite
   operator can have a negative determinant-critical rank-two point
   whose complete constrained Hessian is positive semidefinite.
   Thus positivity of the ordinary parent compression, even together
   with the full rank-two Hessian, cannot give the missing
   contradiction.  The threefold qutrit tensor form of
   \(L^{\otimes3}\) is essential.
2. The qutrit triple-Hodge construction supplies a canonical pair of
   physical leakage directions and hence a concrete specialization of
   the coupled Hessian inequality.  This specialization is not
   complete: there are full-local-support qutrit code planes for which
   the canonical triple-Hodge leakage vanishes identically.

The independent exact checker is
`verification/verify_n3_critical_hessian_hostile_audit.py`.

## 1. A determinant graph chart

Let \(A,B:\mathbb C^2\to{\cal H}\) be full-column frames satisfying
\[
 \det G_A=\det G_B=1,\qquad
 G_A=A^\dagger A,\quad G_B=B^\dagger B,
\tag{1}
\]
and put
\[
 C=A\varepsilon B^\dagger,\qquad
 \varepsilon=
 \begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\tag{2}
\]
Choose horizontal velocities
\[
 A^\dagger X=0,\qquad B^\dagger Y=0,
\tag{3}
\]
and a logical velocity \(Z\in M_2\).  The exact rank-two graph curve
\[
 F(t)=(A+tX)(\varepsilon+tZ)(B+tY)^\dagger
\tag{4}
\]
has
\[
\begin{aligned}
 F(t)&=C+tD+t^2E+O(t^3),\\
 D&=AZB^\dagger+X\varepsilon B^\dagger
     +A\varepsilon Y^\dagger,\\
 E&=XZB^\dagger+X\varepsilon Y^\dagger+AZY^\dagger .
\end{aligned}
\tag{5}
\]

The product of the two nonzero singular values is exactly
\[
\delta(F(t))
=|\det(\varepsilon+tZ)|
 \sqrt{\det(G_A+t^2X^\dagger X)
       \det(G_B+t^2Y^\dagger Y)}.
\tag{6}
\]
Set \(W=\varepsilon^{-1}Z\).  Direct logarithmic
differentiation gives
\[
\begin{aligned}
 d\log\delta&=\operatorname{Re}\operatorname{Tr}W,\\
 d^2\log\delta&=
 -\operatorname{Re}\operatorname{Tr}(W^2)
 +\operatorname{Tr}(G_A^{-1}X^\dagger X)
 +\operatorname{Tr}(G_B^{-1}Y^\dagger Y).
\end{aligned}
\tag{7}
\]
Thus the tangent constraint is
\[
 \operatorname{Re}\operatorname{Tr}W=0.
\tag{8}
\]

Let \({\cal B}(S,T)=\langle S,{\cal L}(T)\rangle\), where
\({\cal L}=L^{\otimes3}\).  At a determinant-critical point write
\[
 {\cal L}(C)=\lambda N_C+R,\qquad
 N_C=(C^+)^\dagger,\qquad
 R=(I-P_A){\cal L}(C)(I-P_B).
\tag{9}
\]
Here \(P_A,P_B\) are the orthogonal projections onto the two frame
ranges and
\[
 N_C=A\,G_A^{-1}\varepsilon G_B^{-1}B^\dagger.
\tag{10}
\]
The multiplier convention is
\[
 \lambda=\frac12Q_3(C).
\tag{11}
\]

The Hessian of the Lagrangian
\[
 Q_3-2\lambda\log\delta
\tag{12}
\]
is independent of the acceleration of a constrained curve.  Using
(5)--(10), the only part of \(E\) which pairs with \(R\) is
\(X\varepsilon Y^\dagger\), while the three parts of \(E\) are all
orthogonal to \(N_C\).  Therefore
\[
\boxed{
\begin{aligned}
\frac12\operatorname{Hess}_{C}(D,D)
={}&Q_3(D)
+2\operatorname{Re}\langle R,X\varepsilon Y^\dagger\rangle\\
&+\lambda\operatorname{Re}\operatorname{Tr}(W^2)\\
&-\lambda\left[
 \operatorname{Tr}(G_A^{-1}X^\dagger X)
+\operatorname{Tr}(G_B^{-1}Y^\dagger Y)
\right].
\end{aligned}}
\tag{13}
\]
Whitening \(A,B\) and then taking their singular frames turns (13)
exactly into equation (24) of the audited note.  In particular:

* the normal term has coefficient \(2\) in the half-Hessian;
* under \(X\mapsto\alpha X,\ Y\mapsto\beta Y\), it scales as
  \(\alpha\beta\), not as \(\overline\alpha\beta\);
* the ordinary crossed term scales as
  \(\overline\alpha\beta\).

The phase sum and phase difference are consequently independent, and
the sharp leakage condition really is
\[
 (|p|+|q|)^2\leq ab.
\tag{14}
\]

## 2. Audit of the Bell-companion Schur complement

Choose magic companion matrices so that
\[
 2\det\left(\sum_{\alpha=0}^3z_\alpha M_\alpha\right)
 =\sum_{\alpha=0}^3z_\alpha^2
\tag{15}
\]
and the critical singlet is \(z_0=1\).  If
\[
 Q_3\left(\sum_\alpha z_\alpha C_\alpha\right)
 =\sum_\alpha\lambda_\alpha|z_\alpha|^2,
\qquad \lambda_0<0,
\tag{16}
\]
then a tangent companion coordinate \(z_j=x_j+iy_j\) has core
quadratic form
\[
 (\lambda_j-\lambda_0)x_j^2
 +(\lambda_j+\lambda_0)y_j^2.
\tag{17}
\]
The second coefficient is strictly positive because
\(\lambda_j+\lambda_0\) is the energy of a physical rank-one
coefficient.  The first is positive because
\(\lambda_j>0>\lambda_0\).

If
\[
 \ell_j={\cal B}(C_j,D_{\rm out}),
\tag{18}
\]
then the mixed term is
\[
 2x_j\operatorname{Re}\ell_j
 +2y_j\operatorname{Im}\ell_j.
\tag{19}
\]
Minimizing (17)--(19) gives exactly
\[
\boxed{
\sum_{j=1}^3\left[
\frac{(\operatorname{Re}\ell_j)^2}{\lambda_j-\lambda_0}
+
\frac{(\operatorname{Im}\ell_j)^2}{\lambda_j+\lambda_0}
\right].
}
\tag{20}
\]
Thus the denominators, the real/imaginary assignment, and the absence
of an extra factor two in the audited Schur subtraction are all
correct.

## 3. A strictly positive-parent obstruction

The full Hessian still does not contradict a negative multiplier at
the level of an arbitrary positive bipartite parent.

Let the row and column spaces both be \(\mathbb C^3\), put
\[
 U=V=\operatorname{span}\{e_0,e_1\},
\qquad P=P_U\otimes P_V,
\tag{21}
\]
and let
\[
 |\Phi\rangle=\frac{|00\rangle+|11\rangle}{\sqrt2}.
\tag{22}
\]
On the two-replica space define
\[
\boxed{\qquad
 Y=P+3|\Phi\rangle\langle\Phi|+2(I-P).
\qquad}
\tag{23}
\]
Its eigenvalues are
\[
 4,\quad1,1,1,\quad2,2,2,2,2,
\tag{24}
\]
so \(Y\succ0\).  Let \({\mathscr X}=Y^\Gamma\), and use it as the
matrix of a self-adjoint quadratic form \({\mathscr Q}\) on
coefficient matrices.

On \(U\otimes V\),
\[
 {\mathscr X}=I+\frac32F,
\tag{25}
\]
while on its orthogonal complement \({\mathscr X}=2I\).  Take
\[
 C=\varepsilon=
 \begin{pmatrix}0&-1&0\\1&0&0\\0&0&0\end{pmatrix}.
\tag{26}
\]
The vectorization of \(C\) is the unnormalized singlet.  Hence
\[
 {\mathscr L}(C)=-\frac12C,\qquad
 {\mathscr Q}(C)=-1,\qquad
 \lambda=-\frac12,\qquad R=0.
\tag{27}
\]
Every rank-one matrix has the strict floor
\[
 {\mathscr Q}(uv^\dagger)
 =\langle u\otimes v,
 Y(u\otimes v)\rangle
 \geq\|u\|^2\|v\|^2.
\tag{28}
\]

The complete determinant Hessian at \(C\) is nevertheless positive
semidefinite.  The three unnormalized Bell companions have energy
\(5\), while the singlet has energy \(-1\).  Thus their six real
core Hessian coefficients are \(4\) and \(6\).  The global phase is
the sole core zero direction.  A one-sided leakage lies outside
\(U\otimes V\), so the outside half-Hessian is
\[
 2(\|X\|_2^2+\|Y\|_2^2)
 -\lambda(\|X\|_2^2+\|Y\|_2^2)
 =\frac52(\|X\|_2^2+\|Y\|_2^2).
\tag{29}
\]
All core/outside couplings and the normal residual vanish.  This
proves the claim.

The example is not physical Werner data: \(Y\) is not the fixed
threefold tensor
\((I-\tfrac12F_3)^{\otimes3}\).  Its exact role is to show
\[
\boxed{\begin{minipage}{0.88\linewidth}
Positivity before partial transpose, strict rank-one positivity,
Bell balance, determinant criticality, and the complete rank-two
Hessian can all coexist with a negative singlet.  A contradiction
must use identities tying the leakage couplings and the normal
residual to the same threefold qutrit partial traces.
\end{minipage}}
\tag{30}
\]

## 4. The physical tensor terms

For the Werner form define the canonical insertion
\[
 E_S(T)=(\operatorname{Tr}_S T)\otimes I_S
\tag{31}
\]
with tensor factors restored to their original positions.  Then
\[
 {\cal L}(T)
 =\sum_{S\subseteq\{1,2,3\}}
 \left(-\frac12\right)^{|S|}E_S(T).
\tag{32}
\]
The normal residual is therefore
\[
\boxed{
 R=\sum_{\varnothing\ne S\subseteq\{1,2,3\}}
 \left(-\frac12\right)^{|S|}
 (I-P_U)E_S(C)(I-P_V).
}
\tag{33}
\]
The empty-set term drops because it is supported between the two
singular planes.  Likewise,
\[
\begin{aligned}
 p&=\sum_S\left(-\frac12\right)^{|S|}
 \langle\operatorname{Tr}_S D_X,
        \operatorname{Tr}_S D_Y\rangle,\\
 q&=\sum_S\left(-\frac12\right)^{|S|}
 \langle\operatorname{Tr}_S C,
        \operatorname{Tr}_S(X\Sigma Z)\rangle.
\end{aligned}
\tag{34}
\]
Equations (33)--(34), and not positivity of an arbitrary parent, are
the additional physical data available for a contradiction.

## 5. A canonical triple-Hodge leakage test

Let
\[
 C=s_1u_1v_1^\dagger+s_2u_2v_2^\dagger
\tag{35}
\]
be the singular decomposition at a hypothetical negative critical
point.  With the normalized qutrit skew matrices
\[
 (A_p)_{ai}=2^{-1/2}\varepsilon_{pai},
\tag{36}
\]
put
\[
 D_t=\sum_{p,q,r}t_{pqr}A_p\otimes A_q\otimes A_r
\tag{37}
\]
and define
\[
 h_U=\overline{D_{u_1}u_2},\qquad
 h_V=\overline{D_{v_1}v_2}.
\tag{38}
\]
The triple alternating contraction has two repeated columns after
pairing with either codeword, so
\[
 h_U\perp u_1,u_2,\qquad h_V\perp v_1,v_2.
\tag{39}
\]
Moreover,
\[
 \|h_U\|^2
 =\langle u_1\otimes u_2,
 {\mathsf A}_1{\mathsf A}_2{\mathsf A}_3
 (u_1\otimes u_2)\rangle
 \leq\frac16,
\tag{40}
\]
and similarly for \(h_V\).

For \(k=1,2\), use the matched leakage which replaces the \(k\)-th
left and right singular vectors by \(h_U,h_V\).  Define
\[
\begin{aligned}
 A_k&=s_k^2Q_3(h_Uv_k^\dagger)
      -\lambda\|h_U\|^2,\\
 B_k&=s_k^2Q_3(u_kh_V^\dagger)
      -\lambda\|h_V\|^2,\\
 P_k&=s_k^2{\cal B}_3(h_Uv_k^\dagger,u_kh_V^\dagger),\\
 T_k&=s_k{\cal B}_3(C,h_Uh_V^\dagger).
\end{aligned}
\tag{41}
\]
Substitution in the exact leakage Hessian gives the concrete
qutrit-Hodge necessary condition
\[
\boxed{\qquad
 (|P_k|+|T_k|)^2\leq A_kB_k
 \qquad(k=1,2).
\qquad}
\tag{42}
\]
Thus a proof can now test the reverse-Cauchy defect against a canonical
pair of tensor-structured leakage directions, rather than arbitrary
abstract normal vectors.

### Exact obstruction to using only (42)

The canonical triple-Hodge vector can vanish even when the code plane
has full local qutrit support.  Take
\[
\begin{aligned}
 u_0&=\frac{|000\rangle+|111\rangle+|222\rangle}{\sqrt3},\\
 u_1&=\frac{|012\rangle+|120\rangle+|201\rangle}{\sqrt3}.
\end{aligned}
\tag{43}
\]
Both one-site reductions of each codeword are \(I_3/3\), so the
one-site reductions of the code projection are \(2I_3/3\), of rank
three.  Nevertheless,
\[
\boxed{\qquad D_{u_0}u_1=0.\qquad}
\tag{44}
\]
Indeed, a nonzero summand would require a diagonal label \(i\) to
differ simultaneously from all three entries of one cyclic string;
those entries are \(\{0,1,2\}\), which is impossible.

Therefore (42) becomes vacuous on a genuine full-support plane.
A complete Hodge use of the Hessian must retain the one-skew and
two-skew leakage sectors coherently with the triple-skew sector.  The
single triple-Hodge normal is not a universal bridge from the strict
reverse-Cauchy defect to (14).

## Exact status

The complete critical Hessian and its Bell Schur complement have
passed an independent complex-coordinate audit.  No contradiction
with \(\lambda<0\) is obtained.  What remains is the following
strictly physical problem:

> Combine the threefold contraction identities (33)--(34), using a
> coherent family of one-, two-, and three-skew qutrit leakage
> directions, to violate (14) whenever the singular-component
> reverse-Cauchy defect is positive.

The positive-parent example proves that the word “threefold” cannot
be removed from this target.
