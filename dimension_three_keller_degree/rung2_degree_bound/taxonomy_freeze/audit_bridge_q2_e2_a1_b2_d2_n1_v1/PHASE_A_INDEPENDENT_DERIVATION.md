# Phase A: independent frozen-row derivation

**Row:** `Q2-E2-A1-B2-D2-N1`
**Derivation frozen (UTC):** 2026-07-26T09:39:38Z
**Information boundary:** this file was written from
`FROZEN_TAXONOMY_v1.md` and `frozen_manifest_v1.json` before either
`WORKING_FIXED_CONIC_ROW.md`, `WORKING_NONBINARY_FIXED_CONIC_ROW.md`, or any
of their scripts was opened.

## 1. Intrinsic content of the row

The frozen tuple is
\[
(\operatorname {rank}JH_4,e,a,b,\delta,\nu)=(2,2,1,2,2,1).
\]
Thus
\[
H_4=h\,A(p,q),
\]
where:

* \(h\ne0\) is a homogeneous quadratic;
* \(p,q\) are coprime homogeneous forms of degree one, hence linearly
  independent linear forms;
* \(A=(A_1,A_2,A_3)\) is a basepoint-free binary triple of degree two whose
  reduced image is a plane conic and whose normalization map has degree one.

The last two properties say that the three \(A_i\) span
\(\operatorname {Sym}^2\langle s,t\rangle\).  Indeed, a proper subspace has
projective image contained in a line (or a point), contrary to
\(\delta=2\).  Consequently there is a target matrix \(U\in GL_3\) for which
\[
U A(s,t)=(s^2,st,t^2)^T.
\]
There is independently a source matrix \(S\in GL_3\) for which
\[
p(SX)=x,\qquad q(SX)=y.
\]

Apply these changes to a normalized candidate
\(F=X+H_2+H_3+H_4\):
\[
\widetilde F(X):=U F(SX)
 =LX+K_2+K_3+\widetilde h(x,y,z)(x^2,xy,y^2)^T,                 \tag{A.1}
\]
where \(L=US\in GL_3\), \(K_i=U H_i(SX)\), and
\(\widetilde h=h(SX)\ne0\).  The spaces of homogeneous vector maps of
degrees two and three are carried bijectively to themselves, so \(K_2\)
and \(K_3\) in (A.1) are completely arbitrary.  Also
\[
\det J\widetilde F(X)
 =\det(U)\det(S)\det JF(SX),
\]
so the nonzero-constant Jacobian property is preserved.  No relation such
as \(L=I\) may be imposed after independently normalizing the source pencil
and target conic.

This is the uniform leading normal form used by this audit:
\[
\boxed{H_4=h(x,y,z)(x^2,xy,y^2)^T,\quad
       h\in\mathbb C[x,y,z]_2\setminus\{0\}.}                  \tag{A.2}
\]
It includes every quadratic \(h\): binary or nonbinary, smooth or singular,
reduced or nonreduced.  Those are internal specializations, not new frozen
rows.

For a direct rank check, put
\[
\lambda=(y^2,-2xy,x^2)^T,\qquad
r=(xh_z,yh_z,zh_z-4h)^T.
\]
Then
\[
\lambda^T JH_4=0,\qquad JH_4\,r=0.
\]
The projective ratios of the primitive triple
\((x^2,xy,y^2)\) recover \(x/y\), and the triple spans all binary
quadratics.  Hence its image is a conic with \((a,b,\delta,\nu)=(1,2,2,1)\).
Because \(x,y\) are independent and \(h\ne0\), the generic Jacobian rank is
two.  The component gcd is exactly \(h\).

## 2. Coefficient-pivot-independent coverage

Let \(m_0,\ldots,m_{14}\) be the frozen monomial order
\[
x^4,x^3y,x^3z,x^2y^2,x^2yz,x^2z^2,xy^3,xy^2z,xyz^2,xz^3,
y^4,y^3z,y^2z^2,yz^3,z^4.
\]
For \(0\le i\le44\), write
\[
\operatorname{comp}(i)=1+\lfloor i/15\rfloor,\qquad
\operatorname{mon}(i)=m_{i\bmod15}.
\]
Because \(A_1,A_2,A_3\) are linearly independent, none of them is the zero
binary quadratic.  Since the polynomial ring is a domain and \(h\ne0\),
each original target component \(hA_j(p,q)\) is a nonzero quartic.  In
particular, some coefficient of the first component is nonzero.  The
complete coverage map is therefore
\[
\boxed{\begin{aligned}
\mathrm C_i&\longmapsto\text{the same normal form (A.1)--(A.2)}
       &&(0\le i\le14),\\
\mathrm C_i&\longmapsto\varnothing&&(15\le i\le44).
\end{aligned}}                                                \tag{A.3}
\]
On the left, \(\mathrm C_i\) records only
\[
c_0=\cdots=c_{i-1}=0,\qquad c_i\ne0,
\]
where \(c_i\) is the coefficient of
\(\operatorname{mon}(i)\) in target component
\(\operatorname{comp}(i)\).  On the right, \(S\) is chosen from the
intrinsic independent pencil \(\langle p,q\rangle\), and \(U\) from the
intrinsic isomorphism
\(\langle A_1,A_2,A_3\rangle=\operatorname {Sym}^2\langle s,t\rangle\).
Their invertibility is supplied by membership in the frozen row.  Neither
construction divides by, or even selects, \(c_i\).

In expanded form the map is:

| pivots | original component | original monomial | audit image |
|---|---:|---|---|
| `C00`--`C14` | 1 | \(m_0\)--\(m_{14}\) | (A.1)--(A.2) |
| `C15`--`C29` | 2 | \(m_0\)--\(m_{14}\) | intrinsically empty |
| `C30`--`C44` | 3 | \(m_0\)--\(m_{14}\) | intrinsically empty |

For every row point, its nonzero first target component has a unique first
nonzero entry and hence belongs to exactly one of `C00`--`C14`.
`C15`--`C44` are retained as the frozen empty intersections.  This
establishes coverage without assuming that any particular `C00`--`C14` is
nonempty and without using an original coefficient as a computational
pivot.

## 3. Audit obligations fixed before bridge access

Any proposed exclusion must retain exact checks for all of the following.

1. The linear part in (A.1) is an arbitrary \(GL_3\) matrix.
2. All 18 quadratic and all 30 cubic lower coefficients remain arbitrary
   until forced by coefficient equations; omission of lower terms is a
   fail-closed gap.
3. Both \(h_z=0\) and \(h_z\ne0\) are covered, including every factorization
   and coefficient degeneration of \(h\).
4. Any case split is exhaustive over \(\mathbb C\) and its branches retain
   their hypotheses.  Division requires a recorded nonvanishing premise.
5. The terminal contradiction must be the singularity of the arbitrary
   linear part (or an equivalent contradiction to a nonzero constant
   Jacobian), not merely failure of a chosen normal-form pivot.
6. The argument must apply uniformly to `C00`--`C14`, and must retain the
   intrinsic emptiness proof for `C15`--`C44`, through (A.3); aggregate prose
   is not a substitute for executable retained checks.
