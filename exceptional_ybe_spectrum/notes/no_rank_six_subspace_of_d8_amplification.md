# No codimension-two square restriction of the identity-amplified witness

**Date:** 2026-07-29

**Status:** PROVED

**Scope:** all identity amplifications of the published four-dimensional
witness.  This is a no-go theorem for extracting an unresolved dimension
\(4m-2\) from the neighboring dimension \(4m\) amplification; it is not an
unrestricted nonexistence theorem in dimension \(4m-2\).

## 1. Statement

Let \(H^{(4)}\) be the published exceptional involution on
\(\mathbb C^4\otimes\mathbb C^4\).  For \(m\ge2\), put
\[
V_m=\mathbb C^4\otimes\mathbb C^m\cong
\mathbb C^2_a\otimes\mathbb C^2_b\otimes\mathbb C^m_c
\]
and let \(H^{(4m)}=H^{(4)}\boxtimes I_m\), with the factors reordered so
that it acts on \(V_m\otimes V_m\).

> **Theorem 1.**
> If \(Q\in\operatorname{End}(V_m)\) is an orthogonal projection and
> \[
> [H^{(4m)},Q\otimes Q]=0,
> \]
> then \(\operatorname{rank}Q\ne4m-2\).

Thus no identity stabilization of the published witness can be cut down
by codimension two to enter the unresolved congruence class.  In
particular, the known dimension-eight amplification has no
six-dimensional square-invariant local subspace, so the most direct
``amplify to eight and cut down to six'' construction cannot produce a
dimension-six exceptional matrix.

The proof is exact and uses neither the Yang--Baxter relation nor a
numerical optimizer after the explicit form of \(H^{(4m)}\) is inserted.
It is an operator-Schmidt and low-rank-pencil argument.

## 2. A three-term operator-Schmidt form

Use the Hermitian Pauli matrices \(X,Y,Z\), and put
\(J=-iY\).  On the first local site define
\[
A_X=X_a\otimes I_b\otimes I_c,\qquad
A_Y=Y_a\otimes I_b\otimes I_c,\qquad
A_Z=Z_a\otimes I_b\otimes I_c.
\]
On the second local site define
\[
\begin{aligned}
B_X&=-\frac1{\sqrt3}X_aX_b\otimes I_c,\\
B_Y&=\frac1{\sqrt6}(Z_aY_b-Y_aZ_b)\otimes I_c,\\
B_Z&=\frac1{\sqrt6}(Y_aY_b-Z_aZ_b)\otimes I_c.
\end{aligned} \tag{1}
\]
Direct expansion of the five Pauli words in the published formula gives
\[
H^{(4m)}=A_X\otimes B_X+A_Y\otimes B_Y+A_Z\otimes B_Z. \tag{2}
\]
All six displayed coefficient operators are Hermitian.

## 3. The low-rank pencil

Suppress the spectator \(c\)-qubit and write
\[
\widetilde B(x,y,z)=x\widetilde B_Z+y\widetilde B_Y+z\widetilde B_X
\quad\text{on }\mathbb C^2_a\otimes\mathbb C^2_b. \tag{3}
\]
Order the Bell basis as
\[
\Phi_+,\ \Psi_+,\ \Phi_-,\ \Psi_-.
\]
An exact change of basis gives
\[
\widetilde B(x,y,z)\sim
\begin{pmatrix}
-z/\sqrt3-\sqrt{2/3}\,x&0&0&0\\
0&-z/\sqrt3+\sqrt{2/3}\,x&0&0\\
0&0&z/\sqrt3&-i\sqrt{2/3}\,y\\
0&0&i\sqrt{2/3}\,y&z/\sqrt3
\end{pmatrix}. \tag{4}
\]
The determinants of its two \(2\times2\) blocks are
\[
\frac{z^2-2x^2}{3},
\qquad
\frac{z^2-2y^2}{3}. \tag{5}
\]

For real \(x,y,z\), (4) shows that
\(\operatorname{rank}\widetilde B(x,y,z)\le2\) precisely on the union of
the following six real lines:
\[
\begin{aligned}
&\mathbb R(1,0,0),\qquad \mathbb R(0,1,0),\\
&\mathbb R(1,1,\sqrt2),\quad
\mathbb R(1,-1,\sqrt2),\quad
\mathbb R(1,1,-\sqrt2),\quad
\mathbb R(1,-1,-\sqrt2).
\end{aligned} \tag{6}
\]
Indeed, a total rank at most two occurs only when one block is zero and
the other has rank at most two, or when both blocks have rank one.
Equation (4) gives exactly the two axes in the first case and the four
remaining lines in the second.  In particular:

> **Lemma 2.**
> The real low-rank cone
> \[
> \{(x,y,z)\in\mathbb R^3:
> \operatorname{rank}\widetilde B(x,y,z)\le2\}
> \]
> contains no two-dimensional real linear subspace.

## 4. Leakage forces a full qubit algebra

Assume for contradiction that \(\operatorname{rank}Q=4m-2\), and put
\(E=I-Q\), so \(\operatorname{rank}E=2\).  Since \(H^{(4m)}\) and
\(Q\otimes Q\) commute,
\[
0=(E\otimes Q)H^{(4m)}(Q\otimes Q)
=\sum_{\nu=X,Y,Z}(EA_\nu Q)\otimes(QB_\nu Q). \tag{7}
\]

Let
\[
\mathcal D=\operatorname{span}_{\mathbb R}
\{QB_XQ,QB_YQ,QB_ZQ\}.
\]
We first prove
\[
\dim_{\mathbb R}\mathcal D\ge2. \tag{8}
\]
If not, the real-linear map
\[
(x,y,z)\longmapsto Q B(x,y,z)Q
\]
would have a kernel of real dimension at least two.  For every vector in
that kernel, the block matrix of the Hermitian operator \(B(x,y,z)\)
relative to \(QV\oplus EV\) has the form
\[
B(x,y,z)=
\begin{pmatrix}
0&C\\ C^*&D
\end{pmatrix}.
\]
Because \(\dim EV_m=2\), its rank is at most four.  But
\[
B(x,y,z)=\widetilde B(x,y,z)\otimes I_m,
\]
so
\[
m\,\operatorname{rank}\widetilde B(x,y,z)\le4. \tag{8a}
\]
For \(m=2\), this puts the kernel plane inside the rank-at-most-two cone
(6), contradicting Lemma 2.  For \(m\ge3\), (8a) is even stronger:
every member of the plane has rank at most one.  Formula (4) shows that
the only pencil element of rank at most one is zero, another
contradiction.

Choose a real basis of \(\mathcal D\) and expand the three Hermitian
compressions \(QB_\nu Q\) in it.  Linear independence of tensor
coefficients in (7), together with (8), gives two linearly independent
real vectors \(u,v\in\mathbb R^3\) for which
\[
EA(u)Q=EA(v)Q=0. \tag{9}
\]
Here the coordinates are ordered compatibly with (3), so
\(A(u)=u_xA_Z+u_yA_Y+u_zA_X\).  Taking adjoints in (9) shows that
\(Q\) commutes with both Hermitian operators \(A(u)\) and \(A(v)\).
Independent Pauli directions have a nonzero commutator, so these two
operators generate the full \(M_2(\mathbb C)\) acting on qubit \(a\).
Consequently
\[
[Q,A_X]=[Q,A_Y]=[Q,A_Z]=0. \tag{10}
\]
Equivalently, \(Q=I_a\otimes Q_{bc}\) for a nonzero operator
\(Q_{bc}\).

Using (10) in the full commutator and (2) gives
\[
0=[H^{(4m)},Q\otimes Q]
=\sum_{\nu=X,Y,Z}A_\nu Q\otimes[B_\nu,Q]. \tag{11}
\]
The three operators \(A_\nu Q=A_\nu\otimes Q_{bc}\) are therefore
linearly independent.  Hence
\[
[Q,B_X]=[Q,B_Y]=[Q,B_Z]=0. \tag{12}
\]

Finally, the \(A_\nu\) generate the full matrix algebra on qubit \(a\).
The product of \(A_X\) with \(B_X\) supplies \(I_a\otimes X_b\), and the
commutator of \(A_Z\) with \(B_Z\), followed by multiplication by
\(A_X\), supplies \(I_a\otimes Y_b\).  Their product supplies
\(I_a\otimes Z_b\).  Thus the joint algebra generated by the six
operators in (1)--(2) is
\[
M_4(\mathbb C)_{ab}\otimes I_m. \tag{13}
\]
Equations (10) and (12) imply that
\[
Q\in I_{ab}\otimes M_m(\mathbb C)_c.
\]
Every projection in this commutant has rank divisible by four, contrary
to \(\operatorname{rank}Q=4m-2\).  This proves Theorem 1.

## 5. Numerical discovery trace and limitations

The exact proof was prompted by a predeclared Grassmannian search for a
rank-six projection \(Q\).  Four rank-four calibration runs reached the
known zero-commutator locus, while all 32 rank-six production runs
converged to the same positive normalized squared commutator
\[
\frac{\|[H^{(8)},Q\otimes Q]\|_F^2}{64}
=0.239583333333\ldots=\frac{23}{96}.
\]
That repeated endpoint is numerical evidence only; neither its apparent
optimality nor the value \(23/96\) is used in the proof.

The theorem excludes only codimension-two subspace extraction from
identity amplifications of this particular witness.  A solution in
dimension \(4m-2\), if one exists, could be genuinely new and need not
embed into the neighboring known \(4m\)-dimensional solution.
