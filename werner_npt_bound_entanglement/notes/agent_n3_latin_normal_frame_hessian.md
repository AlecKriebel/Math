# The Latin-minor normal frame and the quotient-critical Hessian

## Status

This note audits the infinitesimal use of the complete Latin--Segre
minor orbit at a matrix of rank exactly two.  There are two exact
conclusions.

First, the differentials of the Latin minors form a quantitatively
complete frame for the normal space of the rank-two determinantal
manifold.  If
\[
 C=U\Sigma V^\dagger,\qquad
 \Sigma=\operatorname{diag}(s_1,s_2),\qquad
 \delta=s_1s_2>0,
\tag{1}
\]
then, for every ambient variation \(Z\),
\[
\boxed{
 \frac{\delta^2}{5760^2}\|Z_\perp\|_2^2
 \leq
 {\mathbb E}_{\mathsf U,\mathsf V}
 \left|d\Delta_{\mathsf U,\mathsf V}|_C[Z]\right|^2
 \leq
 \frac{\delta^2}{36^2}\|Z_\perp\|_2^2,
}
\tag{2}
\]
where
\[
 Z_\perp=(I-UU^\dagger)Z(I-VV^\dagger).
\tag{3}
\]
Thus their common differential kernel is exactly the tangent space,
not a larger frame-dependent relaxation.

Second, at a critical point of the pair-sector quotient
\[
 \lambda(C)=\frac{Q_3(C)}{\|\Pi _2C\|_2^2},
\tag{4}
\]
the normal residual has a canonical coherent representation by these
minor differentials.  Substitution into the Lagrange Hessian gives
exactly the determinant-manifold curvature term, with its sign,
factor two, and complex-bilinear phase dependence fixed:
\[
\boxed{
\begin{aligned}
 \frac{\|\Pi _2C\|_2^2}{2}
 \frac{d^2}{dt^2}\lambda(C(t))\bigg|_{t=0}
 ={}&
 \langle Z,({\cal L}-\lambda\Pi _2)Z\rangle\\
 &+2\operatorname{Re}
 \left\langle
 R,\,
 U_\perp D\Sigma^{-1}B V_\perp^\dagger
 \right\rangle .
\end{aligned}}
\tag{5}
\]
Here \({\cal L}=L^{\otimes3}\), \(C(t)\) is the exact rank-two graph
curve constructed below, \(Z=C'(0)\), and, in the singular-frame
block decomposition,
\[
 Z=
 \begin{pmatrix}A&B\\D&0\end{pmatrix},
\qquad
 R=({\cal L}-\lambda\Pi _2)C
 =
 \begin{pmatrix}0&0\\0&R_\perp\end{pmatrix}.
\tag{6}
\]

Equations (2) and (5) do not by themselves prove \(Q_3(C)\geq0\).
They give a lossless way to insert the complete nonlinear rank-two
relations into a critical Hessian argument.  The remaining lemma
must use the special tensor structure of \({\cal L}\) to rule out a
negative quotient-critical point; ordinary determinantal geometry
alone does not do so.

The dependency-free exact checker is
`verification/verify_n3_latin_normal_frame_hessian.py`.

## 1. Exterior derivative at rank two

Let \({\cal H}=(\mathbb C^3)^{\otimes3}\), although the statements in
this section hold in any finite dimension.  Use normalized exterior
products, so that wedges of distinct vectors from an orthonormal
basis are orthonormal.

For a linear map \(C\), the first derivative
\[
 J_C(Z):=d(\wedge^3)_C[Z]
\tag{7}
\]
is
\[
\begin{aligned}
J_C(Z)(x_1\wedge x_2\wedge x_3)
={}&Zx_1\wedge Cx_2\wedge Cx_3\\
&+Cx_1\wedge Zx_2\wedge Cx_3\\
&+Cx_1\wedge Cx_2\wedge Zx_3.
\end{aligned}
\tag{8}
\]
Choose singular vectors \(u_1,u_2,v_1,v_2\) in (1), and put
\[
 P_U=UU^\dagger,\qquad P_V=VV^\dagger.
\tag{9}
\]
For \(w\in V^\perp\), equation (8) gives
\[
\boxed{
 J_C(Z)(v_1\wedge v_2\wedge w)
 =
 \delta\,
 u_1\wedge u_2\wedge Z_\perp w.
}
\tag{10}
\]
The derivative vanishes on the orthogonal complement of
\[
 (v_1\wedge v_2)\wedge V^\perp.
\tag{11}
\]
Indeed two of the three copies of \(C\) in (8) require two input
directions in \(V\), and their nonzero wedge already fills the
two-dimensional output space \(U\).  The remaining output therefore
retains only its \(U^\perp\) component.

The maps
\[
 w\longmapsto v_1\wedge v_2\wedge w,\qquad
 z\longmapsto u_1\wedge u_2\wedge z
\tag{12}
\]
are isometries on the respective orthogonal complements.  Hence
\[
\boxed{
 \|J_C(Z)\|_2^2
 =
 \delta^2\|Z_\perp\|_2^2.
}
\tag{13}
\]
This also proves directly that the common kernel of all third-minor
differentials is the tangent space
\[
\boxed{
 T_C{\cal D}_2
 =
 \{Z:(I-P_U)Z(I-P_V)=0\}
}
\tag{14}
\]
of the smooth rank-two stratum \({\cal D}_2\).

## 2. The Latin orbit is a complete normal frame

For three independent local qutrit unitaries
\(\mathsf U=(\mathsf U_1,\mathsf U_2,\mathsf U_3)\), set
\[
 p_r(\mathsf U)
 =
 \mathsf U_1|r\rangle\otimes
 \mathsf U_2|r\rangle\otimes
 \mathsf U_3|r\rangle
\tag{15}
\]
and
\[
 \eta_{\mathsf U}
 =
 p_0(\mathsf U)\wedge p_1(\mathsf U)\wedge p_2(\mathsf U).
\tag{16}
\]
For independent left and right frames, define
\[
 \Delta_{\mathsf U,\mathsf V}(X)
 =
 \langle\eta_{\mathsf U},(\wedge^3X)\eta_{\mathsf V}\rangle.
\tag{17}
\]
Let
\[
 K={\mathbb E}_{\mathsf U}
 |\eta_{\mathsf U}\rangle\langle\eta_{\mathsf U}|.
\tag{18}
\]
The exact Schur--Weyl calculation in
`agent_n3_latin_segre_minor_orbit.md` gives
\[
 \boxed{
 \frac1{5760}I\preceq K\preceq\frac1{36}I
 \quad\hbox{on }\wedge^3{\cal H}.
 }
\tag{19}
\]

Define the analysis operator
\[
\begin{aligned}
 {\cal A}_C:\operatorname{End}({\cal H})
 &\longrightarrow
 L^2\!\left(U(3)^3\times U(3)^3\right),\\
 ({\cal A}_CZ)(\mathsf U,\mathsf V)
 &=d\Delta_{\mathsf U,\mathsf V}|_C[Z].
\end{aligned}
\tag{20}
\]
Equations (7) and (17) imply
\[
 ({\cal A}_CZ)(\mathsf U,\mathsf V)
 =
 \langle\eta_{\mathsf U},J_C(Z)\eta_{\mathsf V}\rangle.
\tag{21}
\]
Independence of the two Haar frames therefore gives the exact identity
\[
\boxed{
 \|{\cal A}_CZ\|_{L^2}^2
 =
 \operatorname{Tr}\!\left[
 J_C(Z)^\dagger KJ_C(Z)K
 \right].
}
\tag{22}
\]
Diagonalizing \(K\) shows that its left-right action in (22) has
eigenvalues between \(5760^{-2}\) and \(36^{-2}\).
Combining (13), (19), and (22) proves (2).

Let
\[
 {\cal N}_C
 =
 \{(I-P_U)Z(I-P_V):Z\in\operatorname{End}({\cal H})\}
\tag{23}
\]
be the normal space, and let
\[
 S_C={\cal A}_C^\dagger{\cal A}_C\big|_{{\cal N}_C}.
\tag{24}
\]
Then
\[
\boxed{
 \frac{\delta^2}{5760^2}I_{{\cal N}_C}
 \preceq S_C\preceq
 \frac{\delta^2}{36^2}I_{{\cal N}_C}.
}
\tag{25}
\]
In particular \(S_C\) is invertible.  This is the exact regularity
statement needed to use the redundant continuum of Latin minors as
Lagrange constraints.

## 3. Quotient criticality and the canonical multiplier

Put
\[
 q(X)=\langle X,{\cal L}X\rangle,\qquad
 c(X)=\|\Pi _2X\|_2^2
 =\langle X,\Pi _2X\rangle,
\tag{26}
\]
and suppose \(c(C)>0\).  Set
\[
 \lambda=\frac{q(C)}{c(C)},\qquad
 {\cal T}={\cal L}-\lambda\Pi _2,\qquad
 R={\cal T}C.
\tag{27}
\]
The first variation of the quotient is
\[
 d(q/c)_C[Z]
 =
 \frac{2}{c(C)}\operatorname{Re}\langle Z,R\rangle.
\tag{28}
\]
If \(C\) is critical on the rank-two stratum, (28) vanishes on the
complex tangent space (14).  Applying it to both \(Z\) and \(iZ\)
shows complex, not merely real, orthogonality.  Thus
\[
\boxed{
 U^\dagger R=0,\qquad RV=0,\qquad R\in{\cal N}_C.
}
\tag{29}
\]

Because of (25), the function
\[
\boxed{
 \mu_C={\cal A}_CS_C^{-1}R
}
\tag{30}
\]
is well-defined and obeys
\[
 {\cal A}_C^\dagger\mu_C=R.
\tag{31}
\]
It is the minimum-\(L^2\)-norm solution of (31).  Moreover
\[
\boxed{
 \frac{36^2}{\delta^2}\|R\|_2^2
 \leq
 \|\mu_C\|_{L^2}^2
 \leq
 \frac{5760^2}{\delta^2}\|R\|_2^2.
}
\tag{32}
\]

Write
\[
 \Delta(X)(\mathsf U,\mathsf V)
 =\Delta_{\mathsf U,\mathsf V}(X).
\tag{33}
\]
With Hilbert-space inner products conjugate-linear in their first
entry, the real Lagrangian is
\[
 {\mathfrak L}(X)
 =
 \langle X,{\cal T}X\rangle
 -
 2\operatorname{Re}\langle\mu_C,\Delta(X)\rangle_{L^2}.
\tag{34}
\]
Equations (29)--(31) show that \(d{\mathfrak L}_C=0\) in every
ambient direction.  Its half-Hessian is
\[
\boxed{
 \frac12d^2{\mathfrak L}_C[Z,Z]
 =
 \langle Z,{\cal T}Z\rangle
 -
 \operatorname{Re}
 \left\langle
 \mu_C,D^2\Delta_C[Z,Z]
 \right\rangle_{L^2}.
}
\tag{35}
\]
This fixes the multiplier sign without choosing individual minors.

## 4. Graph curvature and the factor two

Use the orthogonal row and column decompositions
\[
 {\cal H}=U\oplus U^\perp,\qquad
 {\cal H}=V\oplus V^\perp.
\tag{36}
\]
Every tangent \(Z\) has a unique block form
\[
 Z=
 \begin{pmatrix}
 A&B\\D&0
 \end{pmatrix}.
\tag{37}
\]
For sufficiently small \(t\), the exact graph curve
\[
\boxed{
 C_Z(t)=
 \begin{pmatrix}
 \Sigma+tA&tB\\
 tD&t^2D(\Sigma+tA)^{-1}B
 \end{pmatrix}
}
\tag{38}
\]
has rank exactly two.  Indeed it factors as
\[
 \begin{pmatrix}I\\tD(\Sigma+tA)^{-1}\end{pmatrix}
 (\Sigma+tA)
 \begin{pmatrix}I&(\Sigma+tA)^{-1}tB\end{pmatrix}.
\tag{39}
\]
It has
\[
 C_Z'(0)=Z,\qquad
 \left(C_Z''(0)\right)_\perp
 =
 2D\Sigma^{-1}B.
\tag{40}
\]
Since every Latin minor vanishes identically on (38),
\[
\boxed{
 D^2\Delta_C[Z,Z]
 =
 -{\cal A}_C
 \left(
 2U_\perp D\Sigma^{-1}B V_\perp^\dagger
 \right).
}
\tag{41}
\]
The minus sign can also be seen from the Schur complement:
the determinant of
\(\left(\begin{smallmatrix}\Sigma+tA&tB\\tD&0\end{smallmatrix}\right)\)
starts with
\(-t^2\det(\Sigma)D\Sigma^{-1}B\).

Substituting (31) and (41) into (35) yields
\[
\boxed{
\begin{aligned}
 \frac12d^2{\mathfrak L}_C[Z,Z]
 ={}&
 \langle Z,{\cal T}Z\rangle\\
 &+
 2\operatorname{Re}
 \left\langle
 R,\,
 U_\perp D\Sigma^{-1}B V_\perp^\dagger
 \right\rangle .
\end{aligned}}
\tag{42}
\]
Finally, along a critical curve,
\[
 \frac{c(C)}2(q/c)''(0)
 =
 \frac12(q-\lambda c)''(0),
\tag{43}
\]
because both \(q-\lambda c\) and its first derivative vanish at
\(t=0\).  Equations (42)--(43) prove (5).

The curvature term in (42) is complex-bilinear in the two leakage
blocks: under
\[
 B\mapsto\alpha B,\qquad D\mapsto\beta D
\tag{44}
\]
it scales inside the real part as \(\alpha\beta\), not
\(\overline\alpha\beta\).  This is precisely the phase convention
which produces the sharp coupled leakage condition in the earlier
determinant-Hessian analysis.

If \(C\) is a local quotient minimizer, the right side of (42) is
nonnegative for every tangent \(Z\).  At a point which is merely
critical, (42) remains an identity but nonnegativity need not hold.

## 5. Caveats

1. **Rank one is singular.**  If \(s_2=0\), then \(J_C=0\);
   third-minor differentials do not frame a normal space, and
   \(S_C^{-1}\) does not exist.  This is unavoidable because the
   rank-at-most-two variety is singular at rank at most one.  The
   strict all-copy rank-one bound excludes rank one from a negative
   endpoint minimizer, but that fact is external to the differential
   theorem proved here.
2. **The quotient denominator must be nonzero.**  Equations
   (26)--(43) concern critical points with
   \(\|\Pi _2C\|_2>0\).  A use of this quotient must separately
   dispose of any locus on which \(\Pi _2C=0\).
3. **The multiplier convention is quotient-specific.**  Here
   \(\lambda=Q_3(C)/\|\Pi _2C\|_2^2\).  It is not the multiplier
   \(\lambda=Q_3(C)/2\) used in determinant-normalized notes.
4. **Independent frames are essential.**  The bounds (2) use
   independent left and right Latin frames.  Diagonal or
   symmetric-cube minors have a nontrivial blind subspace and do not
   furnish (25).
5. **There is no dimension reduction in (2).**  The constants
   \(5760\) and \(36\) are the qutrit-three-copy Haar-frame constants.
   The exterior differential formula (13) is dimension-independent,
   but another physical dimension requires its own complete frame
   estimate.

