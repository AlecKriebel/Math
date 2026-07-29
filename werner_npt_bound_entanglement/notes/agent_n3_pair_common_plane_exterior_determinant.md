# The common-plane floor as one paired-Pluecker exterior determinant

## Status

This note gives a lossless exterior-algebra formula for the determinant
of the corrected common-plane floor.  Together with the scalar
triple-Hodge trace bound, it reduces the matrix inequality to one
explicit scalar polynomial on two decomposable bivectors.

It does **not** prove either of those two scalar inequalities.
Moreover, an exact relaxed counterexample below shows that sector
occupation data, ordinary four-plane Pluecker relations, and logical
block positivity do not suffice.  The remaining input is specifically
the paired Segre--Pluecker origin
\({\cal L}=\overline U\otimes\overline V\).

The dependency-free checker is
`verification/verify_n3_pair_common_plane_exterior_determinant.py`.

## 1. Scaled common-plane floor

Retain the notation of
`agent_n3_pair_common_plane_floor.md`.  Thus
\[
 {\cal K}={\cal K}_0\oplus{\cal K}_1\oplus
          {\cal K}_2\oplus{\cal K}_3
\]
is the simultaneous sector decomposition according to the number of
local maximally-entangled projectors.  Let \(P_k\) denote its four
sector projectors and set
\[
 D=P_0-P_1+4P_3.                                        \tag{1}
\]
For the physical product four-plane
\[
 {\cal L}=\overline{\operatorname{ran}U}\otimes
          \overline{\operatorname{ran}V},
\]
put
\[
 r_k=\operatorname{Tr}(P_{\cal L}P_k),\qquad
 s=\frac12(r_1-r_2+3r_3).                               \tag{2}
\]
The corrected floor, multiplied by three, is
\[
 \boxed{\qquad
 G_{\cal L}=P_{\cal L}DP_{\cal L}+sI_{\cal L}.
 \qquad}                                                 \tag{3}
\]
The scalar inequality
\[
 s\geq0                                                  \tag{4}
\]
is exactly
\(\operatorname{Tr}Q_{(3)}\leq4/9\).  It remains unproved
for unrestricted planes.

## 2. One exterior occupation measure controls both terms

Choose orthonormal frames \(u_0,u_1\) and \(v_0,v_1\), and let
\[
 w_{ac}=\overline u_a\otimes\overline v_c,\qquad
 a,c\in\{0,1\}.
\]
The normalized Pluecker vector of \({\cal L}\) is
\[
 \Omega_{\cal L}
 =w_{00}\wedge w_{01}\wedge w_{10}\wedge w_{11}.
                                                               \tag{5}
\]
For a four-tuple
\[
 \nu=(\nu_0,\nu_1,\nu_2,\nu_3),\qquad
 \nu_k\geq0,\qquad \sum_k\nu_k=4,
\]
let \({\cal E}_\nu\) be the mutually orthogonal occupation sector
\[
 {\cal E}_\nu=
 \bigwedge^{\nu_0}{\cal K}_0\wedge
 \bigwedge^{\nu_1}{\cal K}_1\wedge
 \bigwedge^{\nu_2}{\cal K}_2\wedge
 \bigwedge^{\nu_3}{\cal K}_3,
\]
and define
\[
 m_\nu=\|\operatorname{proj}_{{\cal E}_\nu}
                  \Omega_{\cal L}\|^2.                  \tag{6}
\]
Then
\[
 m_\nu\geq0,\qquad \sum_\nu m_\nu=1.                    \tag{7}
\]

Let \(d\Gamma(P_k)\) be the number operator induced by \(P_k\) on
\(\bigwedge^4{\cal K}\).  Its eigenvalue on
\({\cal E}_\nu\) is \(\nu_k\), while its expectation in a Slater
vector is the one-particle trace.  Therefore
\[
 \boxed{\qquad
 r_k=\sum_\nu\nu_km_\nu,\qquad
 s=\frac12\sum_\nu
       (\nu_1-\nu_2+3\nu_3)m_\nu.
 \qquad}                                                 \tag{8}
\]
Thus the scalar shift and the compressed operator cannot be assigned
independent sector budgets.

The compound-operator identity gives
\[
\begin{aligned}
 \det G_{\cal L}
 &=\left\langle\Omega_{\cal L},
       \bigwedge\nolimits^4(D+sI)\Omega_{\cal L}
   \right\rangle\\
 &=\boxed{
 \sum_\nu m_\nu
 (1+s)^{\nu_0}(s-1)^{\nu_1}
 s^{\nu_2}(s+4)^{\nu_3}.}
                                                               \tag{9}
\end{aligned}
\]
No estimate enters (8) or (9).  The common-plane determinant is one
scalar polynomial in one common exterior occupation measure.

## 3. Why this determinant suffices once the scalar bound is known

The unshifted compression \(P_{\cal L}DP_{\cal L}\) equals
\(3Q_{(2)}^\Gamma\).  Since \(Q_{(2)}\succeq0\), it is block
positive on the two logical qubits.  If \(s>0\), then \(G_{\cal L}\)
is strictly block positive.

Every two-dimensional subspace of
\(\mathbb C^2\otimes\mathbb C^2\) contains a product vector: after
identifying vectors with \(2\times2\) matrices, the determinant of a
matrix pencil is a homogeneous quadratic and has a projective zero.
It follows that a strictly block-positive two-qubit Hermitian matrix
has at most one negative eigenvalue and cannot have a negative and a
zero eigenvalue simultaneously.  Hence, when \(s>0\),
\[
 \boxed{\qquad
 G_{\cal L}\succeq0
 \quad\Longleftrightarrow\quad
 \det G_{\cal L}\geq0.
 \qquad}                                                 \tag{10}
\]

There is no gap at \(s=0\) if (4) and (9) are proved globally.  The
parameter space
\(\operatorname{Gr}(2,27)\times\operatorname{Gr}(2,27)\) is
connected, and \(s\) is real analytic and not identically zero.
Under (4), every zero of \(s\) is a limit of points with \(s>0\).
Positivity at those points and closedness of the positive cone give
positivity at the limit.

Consequently the following two scalar statements suffice for the
full corrected floor:
\[
\boxed{
\begin{aligned}
 &\sum_\nu(\nu_1-\nu_2+3\nu_3)m_\nu\geq0,\\
 &\sum_\nu m_\nu
 (1+s)^{\nu_0}(s-1)^{\nu_1}
 s^{\nu_2}(s+4)^{\nu_3}\geq0,
\end{aligned}}                                           \tag{11}
\]
where \(s\) is the first moment in (8).

## 4. The paired Segre--Pluecker restriction

An arbitrary probability vector \((m_\nu)\) is not physical.  Even an
arbitrary decomposable four-vector is not enough.  The physical
four-vector has the special form
\[
\boxed{
\Omega_{\cal L}
=(\overline u_0\otimes\overline v_0)\wedge
 (\overline u_0\otimes\overline v_1)\wedge
 (\overline u_1\otimes\overline v_0)\wedge
 (\overline u_1\otimes\overline v_1).
}                                                        \tag{12}
\]
By the Cauchy decomposition of
\(\bigwedge^4({\cal H}\otimes{\cal H})\), this is the fixed
\((2,2)\)-Young-symmetrizer image of
\[
 (\overline\omega_U)^{\otimes2}\otimes
 (\overline\omega_V)^{\otimes2},\qquad
 \omega_U=u_0\wedge u_1,\quad
 \omega_V=v_0\wedge v_1.                                \tag{13}
\]
Both bivectors are decomposable and obey their own quadratic
Pluecker relations
\[
 \omega_{ij}\omega_{k\ell}
-\omega_{ik}\omega_{j\ell}
+\omega_{i\ell}\omega_{jk}=0
\qquad(i<j<k<\ell).                                     \tag{14}
\]
Equations (12)--(14), not merely the ordinary Pluecker relations for
\(\Omega_{\cal L}\), are the exact nonlinear common-code
realizability constraint.

Equivalently, choose an orthonormal basis adapted to the four physical
sectors.  For a sector basis vector \(q\), its row against the four
logical columns is the vectorization of one \(2\times2\) compression
\[
 M_q=\overline U^{\,\dagger}R_q\overline V.
 \tag{15}
\]
Each \(m_\nu\) is the sum of squared determinants of four such row
vectors with occupation pattern \(\nu\).  All matrices \(M_q\) arise
from the same two frames.  This is a completely explicit
Cauchy--Binet version of the paired Pluecker constraint.

## 5. Exact relaxed obstruction

The paired origin in (12) is essential even if logical block
positivity is retained.  In an abstract sector space choose a
four-plane whose compression of \(D\) is
\[
 P_{\cal L}DP_{\cal L}
 =I_4-2|\Phi_2\rangle\langle\Phi_2|,
\qquad
 |\Phi_2\rangle=\frac{|00\rangle+|11\rangle}{\sqrt2}.
                                                               \tag{16}
\]
This operator is block positive because a product vector has squared
overlap at most \(1/2\) with \(\Phi_2\).

Take three orthonormal directions from \({\cal K}_0\) for the
orthogonal complement of \(\Phi_2\), and one direction from
\({\cal K}_1\) for \(\Phi_2\).  Then
\[
 m_{(3,1,0,0)}=1,\qquad
 (r_0,r_1,r_2,r_3)=(3,1,0,0),\qquad s=\frac12.
                                                               \tag{17}
\]
Nevertheless
\[
 G_{\cal L}
 =\frac32I_4-2|\Phi_2\rangle\langle\Phi_2|
\]
has spectrum
\[
 \left(-\frac12,\frac32,\frac32,\frac32\right)
\]
and
\[
 \boxed{\qquad
 \det G_{\cal L}=-\frac{27}{16}.
 \qquad}                                                 \tag{18}
\]
Thus nonnegative sector masses, ordinary four-plane decomposability,
the exact first-moment coupling, and block positivity still admit a
negative formal point.  Any proof of (11) must use the two common
decomposable bivectors in (13).

## 6. Remaining exact lemma

The corrected floor is reduced to the following paired-Pluecker
problem.

> Let \(\omega_U,\omega_V\in\bigwedge^2\mathbb C^{27}\) be unit
> decomposable bivectors.  Form \(\Omega_{\cal L}\) by the fixed
> \((2,2)\) embedding (12)--(13), project it onto the four local
> maximally-entangled occupation sectors, and form \(m_\nu,s\) by
> (6)--(8).  Prove both inequalities in (11).

This has no remaining logical-vector optimization, no singular-value
ratio, and no independent sector variables.  It is still a global
quartic common-code inequality and remains unproved.
