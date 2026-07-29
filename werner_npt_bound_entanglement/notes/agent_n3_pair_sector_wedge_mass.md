# The pair-sector determinant as one common-origin wedge-mass inequality

## Status

This note gives an exact exterior-algebra reduction of the remaining
qutrit three-copy pair-sector lemma.  It does **not** prove that lemma.
It shows that the shifted \(2\times2\) Gram determinant is equivalent
to one sharp inequality among three orthogonal wedge masses, and then
records the additional two-term Pluecker form forced by the common
left and right singular planes.

The independent dependency-free checker is
`verification/verify_n3_pair_sector_wedge_mass.py`.

## 1. Abstract shifted-projection identity

Let \({\cal K}\) be a finite-dimensional Hilbert space, let
\(\Pi:{\cal K}\to{\cal K}\) be an orthogonal projection, and let
\(E_1,E_2\in{\cal K}\) be orthonormal.  Put
\[
 G_{rs}=\langle E_r,\Pi E_s\rangle,\qquad
 W=\frac23I-\Pi,
 \tag{1}
\]
and use the normalized exterior vector
\[
 \omega=E_1\wedge E_2
 =\frac{E_1\otimes E_2-E_2\otimes E_1}{\sqrt2}.
 \tag{2}
\]
The compound-operator identity gives
\[
 \boxed{\quad
 \det\!\left(\frac23I_2-G\right)
 =
 \left\langle\omega,
 (\mathop{\bigwedge}\nolimits^2W)\omega\right\rangle.
 \quad}
 \tag{3}
\]
Indeed, expansion of the right side gives
\[
 \langle E_1,WE_1\rangle\langle E_2,WE_2\rangle
 -
 \langle E_1,WE_2\rangle\langle E_2,WE_1\rangle.
 \]

Decompose
\[
 {\cal K}={\cal K}_1\oplus{\cal K}_0,\qquad
 {\cal K}_1=\operatorname{Ran}\Pi,\quad
 {\cal K}_0=\ker\Pi.
 \tag{4}
\]
Let \(A_k\) be the squared norm of the component of \(\omega\) having
exactly \(k\) of its two exterior factors in \({\cal K}_1\).  Thus
\[
 A_0+A_1+A_2=1,\qquad A_k\geq0.
 \tag{5}
\]
The eigenvalues of \(W\) are \(2/3\) on \({\cal K}_0\) and \(-1/3\)
on \({\cal K}_1\).  Therefore
\[
 \boxed{\quad
 \det\!\left(\frac23I_2-G\right)
 =\frac19\left(4A_0-2A_1+A_2\right).
 \quad}
 \tag{6}
\]
Consequently the entire shifted Gram problem is exactly
\[
 \boxed{\qquad
 4A_0+A_2\geq2A_1,
 \qquad}
 \tag{7}
\]
or, using (5),
\[
 \boxed{\qquad
 6A_0+3A_2\geq2.
 \qquad}
 \tag{8}
\]

The masses can also be read directly from \(G\):
\[
\begin{aligned}
 A_2&=G_{11}G_{22}-|G_{12}|^2,\\
 A_0&=(1-G_{11})(1-G_{22})-|G_{12}|^2,\\
 A_1&=1-A_0-A_2.
\end{aligned}
\tag{9}
\]
Thus (6) is not a relaxation; it is the original determinant in
orthogonal exterior coordinates.

## 2. The common singular-plane Pluecker restriction

For the pair-sector problem,
\[
 {\cal K}=M_3^{\otimes3}
 \simeq {\cal H}_{L}\otimes\overline{{\cal H}_{R}},
 \qquad
 \Pi=\Pi_2.
 \tag{10}
\]
The two orthonormal vectors in (1) are not arbitrary:
\[
 E_r=u_r\otimes\overline v_r,\qquad r=1,2,
 \tag{11}
\]
where \(u_1,u_2\) and \(v_1,v_2\) are separately orthonormal.  Define
\[
\begin{aligned}
 u_\wedge&=\frac{u_1\otimes u_2-u_2\otimes u_1}{\sqrt2},&
 u_\odot&=\frac{u_1\otimes u_2+u_2\otimes u_1}{\sqrt2},\\
 v_\wedge&=\frac{v_1\otimes v_2-v_2\otimes v_1}{\sqrt2},&
 v_\odot&=\frac{v_1\otimes v_2+v_2\otimes v_1}{\sqrt2}.
\end{aligned}
\tag{12}
\]
Regrouping the left replicas and the right replicas gives the exact
common-origin identity
\[
 \boxed{\quad
 \omega
 =\frac1{\sqrt2}\left(
 u_\wedge\otimes\overline v_\odot
 +
 u_\odot\otimes\overline v_\wedge
 \right).
 \quad}
 \tag{13}
\]
The two displayed summands are orthogonal and have equal squared norm
\(1/2\).  Equivalently,
\[
 \omega\in
 \left(\mathop{\bigwedge}\nolimits^2U\otimes
       \operatorname{Sym}^2\overline V\right)
 \oplus
 \left(\operatorname{Sym}^2U\otimes
       \mathop{\bigwedge}\nolimits^2\overline V\right),
 \tag{14}
\]
and its two components arise from the **same** two planes \(U,V\).
This is the nonlinear Pluecker restriction absent from arbitrary
sector-mass arithmetic.

For local dimension three,
\(\bigwedge^2\mathbb C^3\simeq\overline{\mathbb C^3}\) by the Hodge
map.  Hence every local antisymmetric factor in (13) can be replaced
by one conjugate qutrit index.  The unresolved statement is therefore
the following explicit Hodge--Pluecker inequality:

> If \(\omega\) has the common-origin form (13), and \(A_k\) are its
> masses according to whether zero, one, or two operator replicas lie
> in the exact degree-two sector \(\operatorname{Ran}\Pi_2\), then
> \(6A_0+3A_2\geq2\).

This is strictly smaller than the original partial-trace inequality:
all dependence on the singular values has disappeared, arbitrary
bivectors have been excluded, and the only remaining negative spectral
sector is the mixed mass \(A_1\).

## 3. Sharpness

Take
\[
 E_1=E_{01}\otimes E_{01}\otimes P_0,\qquad
 E_2=E_{01}\otimes E_{01}\otimes P_1.
 \tag{15}
\]
As recorded in the shifted-Gram note,
\[
 G=\frac13
 \begin{pmatrix}1&1\\1&1\end{pmatrix}.
 \tag{16}
\]
Equation (9) gives
\[
 A_0=\frac13,\qquad A_1=\frac23,\qquad A_2=0.
 \tag{17}
\]
Thus
\[
 6A_0+3A_2=2,
 \tag{18}
\]
so both the wedge-mass inequality and the original shifted determinant
would be sharp.

## 4. Remaining exact task

A proof must expand the two masses \(A_0,A_2\) on the correlated
two-term vector (13), use the qutrit Hodge identifications at the three
physical sites, and establish
\[
 6A_0+3A_2-2\geq0.
 \tag{19}
\]
No inequality valid for an arbitrary unit bivector can suffice:
putting all mass in \(A_1\) makes (19) negative.  The needed input is
exactly the shared decomposable origin of the two summands in (13).
