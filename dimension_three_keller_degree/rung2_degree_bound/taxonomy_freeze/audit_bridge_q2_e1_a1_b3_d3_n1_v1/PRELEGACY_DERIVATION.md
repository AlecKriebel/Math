# Frozen-only derivation for `Q2-E1-A1-B3-D3-N1`

This note was derived before opening any legacy exclusion note.  Its only
inputs were `FROZEN_TAXONOMY_v1.md` and `frozen_manifest_v1.json`.

## 1. Intrinsic leading form

The frozen tuple is
\[
(e,a,b,\delta,\nu)=(1,1,3,3,1).
\]
Consequently, and without a choice of coordinates,
\[
H_4=\ell A(p,q),                                      \tag{1}
\]
where:

- \(\ell\) is a nonzero linear form and is the exact component gcd;
- \(p,q\) are independent linear forms and
  \(U=\langle p,q\rangle\) is the canonical pencil;
- \(A=(A_1,A_2,A_3)\) is a basepoint-free, linearly independent triple of
  binary cubics;
- \([A_1:A_2:A_3]\) is birational onto a reduced irreducible plane cubic.

Regard \(A\) as a hyperplane \(W\) in
\(\operatorname{Sym}^3(\mathbb C^2)^*\).  The induced map is the projection
of the rational normal cubic in \(\mathbb P^3\) from the point \(W^\perp\).
A centre on the rational normal cubic is exactly the common-basepoint case
and is forbidden.  A centre on its tangent developable but not on the curve
gives a cusp.  A centre off the tangent developable gives a node.  Over
\(\mathbb C\), the resulting two normal forms are
\[
\begin{aligned}
B_{\rm cusp}(u,v)&=(u^3,\;uv^2,\;v^3),\\
B_{\rm node}(u,v)&=(u^2v,\;uv^2,\;u^3-v^3).
\end{aligned}                                          \tag{2}
\]
They satisfy respectively
\[
Y^3-XZ^2=0,\qquad X^3-Y^3-XYZ=0.
\]
The first has its cusp at \([1:0:0]\); the second has a node at
\([0:0:1]\), with normalization preimages \([1:0]\) and \([0:1]\).

Thus there are \(M\in\operatorname{GL}_3(\mathbb C)\) and independent
linear \(p,q\) such that the intrinsic normal form is
\[
H_4=\ell\,M B_\tau(p,q),\qquad
\tau\in\{\mathrm{cusp},\mathrm{node}\}.                 \tag{3}
\]
The factor incidence is the invariant, exhaustive split
\[
\begin{array}{ll}
\text{aligned:}&\ell=\alpha p+\beta q,\quad
                 (\alpha,\beta)\ne(0,0),\\
\text{transverse:}&\ell,p,q\text{ are linearly independent}.
\end{array}                                             \tag{4}
\]
In the transverse case a source basis makes \((p,q,\ell)=(x,y,z)\).  In
the aligned case the marked binary linear form
\(\alpha u+\beta v\) is retained: setting it to a preferred point would
require a separate proof about the stabilizer of the nodal or cuspidal
system and is not part of (3).

This gives four inclusive internal regimes: nodal/cuspidal crossed with
aligned/transverse.  Arbitrary lower terms \(H_2,H_3\) do not enter this
leading classification.

## 2. Division-free coefficient map

Put
\[
\ell=L_xx+L_yy+L_zz,\qquad
g=\sum_{|\gamma|=3}g_\gamma x^{\gamma_x}y^{\gamma_y}z^{\gamma_z},
\]
where \(g\) is the first component of \(M B_\tau(p,q)\).  Order its ten
coefficients as
\[
(g_{300},g_{210},g_{201},g_{120},g_{111},
  g_{102},g_{030},g_{021},g_{012},g_{003}).
\]
The first fifteen frozen coefficients \(d_i=c_i\) are exactly
\[
\begin{array}{rcl}
d_0&=&L_xg_{300},\\
d_1&=&L_yg_{300}+L_xg_{210},\\
d_2&=&L_zg_{300}+L_xg_{201},\\
d_3&=&L_yg_{210}+L_xg_{120},\\
d_4&=&L_zg_{210}+L_yg_{201}+L_xg_{111},\\
d_5&=&L_zg_{201}+L_xg_{102},\\
d_6&=&L_yg_{120}+L_xg_{030},\\
d_7&=&L_zg_{120}+L_yg_{111}+L_xg_{021},\\
d_8&=&L_zg_{111}+L_yg_{102}+L_xg_{012},\\
d_9&=&L_zg_{102}+L_xg_{003},\\
d_{10}&=&L_yg_{030},\\
d_{11}&=&L_zg_{030}+L_yg_{021},\\
d_{12}&=&L_zg_{021}+L_yg_{012},\\
d_{13}&=&L_zg_{012}+L_yg_{003},\\
d_{14}&=&L_zg_{003}.
\end{array}                                             \tag{5}
\]

There is also an exact integer formula for the \(g_\gamma\).  Write
\(p=P_xx+P_yy+P_zz\), \(q=Q_xx+Q_yy+Q_zz\), and
\[
g=\sum_{r=0}^3 a_rp^{3-r}q^r.
\]
Then
\[
g_\gamma=
\sum_{r=0}^3a_r
\sum_{\substack{\mu+\nu=\gamma\\|\mu|=3-r,\ |\nu|=r}}
\binom{3-r}{\mu}\binom r\nu P^\mu Q^\nu.                \tag{6}
\]
For first row \((m_1,m_2,m_3)\) of \(M\),
\[
(a_0,a_1,a_2,a_3)=
\begin{cases}
(m_1,0,m_2,m_3),&\tau=\mathrm{cusp},\\
(m_3,m_1,m_2,-m_3),&\tau=\mathrm{node}.
\end{cases}                                             \tag{7}
\]
Equations (5)--(7) use only addition and multiplication.

## 3. Exact `C00`--`C44` routing

Because \(M\) is invertible, its first row is nonzero.  Because the three
entries in either triple (2) are linearly independent, \(g\ne0\).
The polynomial ring is a domain and \(\ell\ne0\), so
\(\ell g\ne0\).  Therefore some \(d_i\), \(0\le i\le14\), is nonzero.

For \(0\le i\le14\), the exact route is
\[
\boxed{\mathrm C_{i}\iff
d_0=\cdots=d_{i-1}=0\ \text{and}\ d_i\ne0}.             \tag{8}
\]
Here the ID is zero-padded (`C00`, ..., `C14`) and each \(d_i\) is the
polynomial (5), with (6)--(7) substituted.  For every \(15\le i\le44\),
\[
\boxed{R/\mathrm C_i=\varnothing}.                      \tag{9}
\]
Indeed, reaching component two would require all coefficients of the
nonzero first component to vanish.  This is a coverage map to every frozen
pivot stratum and contains no division or unrecorded pivot.
