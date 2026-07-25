# The rank-one triple-companion exit

## Status and scope

**Exact audited theorem.** The full exact SymPy certificate, two
methodologically independent PARI/GP reconstructions, and the external
hostile replay pass, together with strict-transcript and fail-closed
mutation tests. The hostile audit found and repaired the hidden
\(D\ne0,a_3=0\) completeness gap and corrected the prose describing the
axis gauge; its final verdict is **PASS**. See
[`audit_hostile_external/REPORT.md`](audit_hostile_external/REPORT.md).

This note is not peer reviewed. Exact computer checks certify the algebra
encoded in the accompanying scripts; they are evidence, not peer review.
AI systems assisted with symbolic exploration, case organization, proof
drafting, and verification code.

## Theorem

Let \(K\) be a field of characteristic zero. Write a degree-four polynomial
map, after translating away its constant term, as
\[
F=LX+H_2+H_3+H_4,
\]
where \(H_j\) is homogeneous of degree \(j\). Suppose that, after invertible
linear source and target changes,
\[
H_4=\bigl(x^4,x^2(y^2+xz),0\bigr),
\qquad (H_3)_3=x^3. \tag{1}
\]
Then \(\det JF\) cannot be a nonzero constant.

Equivalently, the triple cubic companion \(R=xp=x^3\) is excluded for the
rank-one canonical fixed-divisor pencil
\[
H_4=(p^2,pq,0),\qquad
\langle p,q\rangle=\langle x^2,y^2+xz\rangle. \tag{2}
\]

Together with the separately audited mixed-companion package and the
rank-two triple-companion package, this closes the two companion orbits for
both canonical fixed-divisor \(e=2\) pencils. The present theorem by itself
is a leading-form obstruction; it is not stated as a universal degree bound.

## Weighted Jacobian identities

Put
\[
p=x^2,\qquad q=y^2+xz,\qquad
P=p^2=x^4,\qquad Q=pq=x^2(y^2+xz),\qquad R=x^3
\]
and introduce a bookkeeping variable \(\tau\):
\[
\mathcal J(\tau)
=L+\tau JH_2+\tau^2JH_3+\tau^3JH_4,\qquad
E_j=[\tau^j]\det\mathcal J(\tau). \tag{3}
\]
The Keller condition requires
\[
E_1=\cdots=E_9=0,\qquad \det L\ne0. \tag{4}
\]
The constant term is \(\det L\), so every branch below ends either in a
literal nonzero coefficient of some \(E_j\), or in \(\det L=0\).

For the quadratic first and second coordinates use the monomial order
\[
(x^2,xy,xz,y^2,yz,z^2)
\]
with coefficients \(a_0,\ldots,a_5\) and \(b_0,\ldots,b_5\). Write
\[
L=(\ell_{ij})_{1\le i,j\le3}.
\]

## Complete \(E_7\) normal form

Before gauge fixing, \(E_7=0\) is a homogeneous linear system with matrix
size \(36\times26\), rank \(8\), and nullity \(18\). An explicit maximal
minor is \(1889568\).

There are four independent legal gauge directions: the two target shears
by \(R\), and two independent source-translation directions. The
\(z\)-translation direction coincides with the second target shear at this
level. Fourteen further kernel directions give the complete normal form
\[
\begin{aligned}
W={}&w_1xy+w_2xz+w_3y^2+w_4yz+w_5z^2,\\
U={}&Axq+\frac43xW,\\
V={}&C_0x^2z+C_1xy^2+C_2xyz+C_3xz^2\\
&\quad+C_4y^3+C_5y^2z+C_6yz^2+C_7z^3,
\end{aligned} \tag{5}
\]
where \(H_3=(U,V,R)\) and \((H_2)_3=W\). The determinant of a displayed
\(18\times18\) kernel-coordinate minor is \(512/27\), proving that the
four gauges plus these fourteen directions span the entire kernel.

The \(E_6\) matrix has rank \(4\), with constant minor \(648\). Its exact
compatibility equations first give
\[
w_4=w_5=0, \tag{6}
\]
and then
\[
\begin{aligned}
9AC_4+w_1(-3A+4w_3)&=0,\\
AC_6&=0,\\
9AC_5+(w_3-w_2)(3A-4w_3)&=0,\\
AC_7&=0.
\end{aligned} \tag{7}
\]
This produces the exhaustive split \(A=0\) and \(A\ne0\).

## I. The branch \(A=0\)

### I.1. \(w_3=s\ne0\)

Equations (7) give \(w_1=0\) and \(w_2=s\), hence
\[
W=sq,\qquad U=\frac43sxq.
\]
Exact \(E_5\) compatibilities include
\[
\begin{gathered}
s^2C_6,\quad s^2(2C_2-3C_4),\quad s^2C_3,\quad
s^2C_5,\quad s^2C_7,\\
s^2C_2(C_2-C_4).
\end{gathered} \tag{8}
\]
They force \(C_2=\cdots=C_7=0\).

Put \(D=C_0-C_1\). At the freshly recomputed rank drop \(D=0\), \(E_5\)
zeros
\[
\ell_{12},\ \ell_{13},\ \ell_{32},\ \ell_{33},
\]
so \(\det L=0\).

On \(D\ne0\), put \(r=a_3\). The first complete \(E_4\) solve has pivot
\[
648r^4, \tag{9a}
\]
so it is valid only on \(r\ne0\). It gives
\[
b_1=b_4=b_5=0,\qquad b_2=C_1D+b_3,
\]
and the two displayed \(E_3\)-coefficients and the determinant are
\[
\begin{aligned}
[x^2z]E_3=[xy^2]E_3&=\frac43s^2\ell_{22},\\
\det L&=D\ell_{22}(s\ell_{11}-r\ell_{31}).
\end{aligned} \tag{9}
\]
Thus \(E_3=0\) implies \(\det L=0\).

At the hidden rank drop \(r=0\), the system is rebuilt before solving.
An alternate \(E_4\) minor is
\[
\frac{2048}{81}s^8. \tag{9b}
\]
The fresh solution again has
\[
b_1=b_4=b_5=0,\qquad b_2=C_1D+b_3,
\]
but now
\[
[x^2z]E_3=[xy^2]E_3=\frac43s^2\ell_{22},
\qquad
\det L=D\ell_{11}\ell_{22}s. \tag{9c}
\]
Hence the rank-drop chart also forces \(\det L=0\).

### I.2. The legal reduction when \(w_3=0\)

Now
\[
W=x(w_1y+w_2z).
\]
The linear source shear
\[
T_\alpha:(x,y,z)\longmapsto
(x,y+\alpha x,z-2\alpha y-\alpha^2x) \tag{10}
\]
fixes \(x\), \(q=y^2+xz\), \(H_4\), and \(R=x^3\). It sends \(W\) to
\[
x\bigl((w_1-2\alpha w_2)y+w_2z+
(\alpha w_1-\alpha^2w_2)x\bigr). \tag{11}
\]
If \(w_2\ne0\), choose \(\alpha=w_1/(2w_2)\). The \(xy\)-coefficient
vanishes and the only residue is \(w_1^2x^2/(4w_2)\).

Removing that residue uses only the already certified source-translation
gauge and a shift of the free \(V\)-coefficients:
\[
\left(\frac43x^3,0,x^2\right)
=\frac13\left(\partial_xP,\partial_xQ,\partial_xR\right)
+\left(0,-\frac23xy^2-x^2z,0\right). \tag{12}
\]
The second summand lies in the free \(C_0,C_1\) directions of (5).
Thus no nonlinear or unlisted coordinate normalization is used. The
exhaustive reduced cases are
\[
W=0,\qquad W=sxz\ (s\ne0),\qquad W=sxy\ (s\ne0). \tag{13}
\]

### I.3. The origin \(W=0\)

After the constant-pivot \(E_6\) solve, the complete nonzero part of
\(E_5\) is
\[
\begin{aligned}
E_5={}&3\ell_{12}x^5
+6((C_0-C_1)a_3-\ell_{13})x^4y
-3C_2a_3x^4z\\
&+3a_3(2C_2-3C_4)x^3y^2
+6a_3(2C_3-C_5)x^3yz
-3C_6a_3x^3z^2\\
&+6C_5a_3x^2y^3
+12C_6a_3x^2y^2z
+18C_7a_3x^2yz^2.
\end{aligned} \tag{14}
\]
This literal identity is used instead of specializing a generic solve.

If \(a_3=0\), then \(\ell_{12}=\ell_{13}=0\), and two \(E_4\)
coefficients are
\[
\frac83\ell_{33}^2,\qquad
\frac43(3a_0\ell_{33}-2\ell_{31}\ell_{33}-\ell_{32}^2).
\tag{15}
\]
They give \(\ell_{33}=\ell_{32}=0\), hence \(\det L=0\).

If \(a_3\ne0\), (14) forces \(C_2=\cdots=C_7=0\). A fresh polynomial
solve through \(E_4\), valid also at \(D=C_0-C_1=0\), gives
\[
[x^3]E_3=-3a_3\ell_{22},\qquad
3\det L=D\ell_{31}[x^3]E_3. \tag{16}
\]
Again \(E_3=0\) gives \(\det L=0\).

### I.4. The \(xz\)-axis

Take \(W=sxz\), \(U=\frac43sx^2z\). Recomputing the \(E_5\) matrix at
each rank drop gives the successive augmented minors
\[
s^6C_6,\qquad s^6(3C_5-2s),\qquad s^6C_4. \tag{17}
\]
Thus
\[
C_6=C_4=0,\qquad C_5=\frac23s.
\]
On \(C_7\ne0\), a rank-five pivot is \(s^3C_7\); after the complete
\(E_5\) solve,
\[
[yz^3]E_4=-\frac8{27}s^4\ne0. \tag{18}
\]
At the freshly recomputed rank drop \(C_7=0\), an augmented \(E_5\)
minor is already a nonzero multiple of \(s^3\). This closes both charts.

### I.5. The \(xy\)-axis

Take \(W=sxy\), \(U=\frac43sx^2y\). Fresh augmented minors successively
force
\[
C_7=C_6=C_5=C_3=0. \tag{19}
\]
Put
\[
h=2s-3C_4.
\]
At \(h=0\), a fresh \(E_5\) compatibility is \(-4s^3/9\).

Assume \(h\ne0\). After solving \(E_6,E_5\) and four independent
\(E_4\) rows, the complete remaining \(E_4\) compatibility is generated
by
\[
\begin{aligned}
\mathcal A&=C_1s^2(s-h)+(3h^2+2s^2)\ell_{32},\\
\mathcal B&=(3h+2s)(-6C_2-3h+4s).
\end{aligned} \tag{20}
\]
There are two factors in \(\mathcal B=0\).

If \(3h+2s=0\), then \(\mathcal A=0\) gives
\(\ell_{32}=-C_1s/2\), while
\[
[xz^2]E_3=-\frac29s^3(s-C_2)^2 \tag{21}
\]
forces \(C_2=s\). The remaining \(E_3\) compatibility is
\[
\frac29C_1s^3(2C_0-3C_1). \tag{22}
\]

- On \(C_1=0\), successive \(E_2,E_1\) squares force
  \(C_0=\ell_{31}=b_1=0\), after which \(\det L=0\).
- On \(2C_0=3C_1\), \(E_2\) forces
  \[
  \ell_{31}=-\frac34C_1^2,\qquad b_1=0,\qquad
  \ell_{21}=\frac{3C_1\ell_{22}}{2s},
  \]
  and the resulting \(L\) is singular.

For the second factor,
\[
C_2=\frac{4s-3h}{6},\qquad G=3h^2+2s^2. \tag{23}
\]
If \(G\ne0\), \(\mathcal A=0\) determines
\[
\ell_{32}=-\frac{C_1s^2(s-h)}G,
\]
and
\[
[xz^2]E_3=\frac{s^4(3h+2s)^2}{243h}. \tag{24}
\]
This returns to the already closed first factor.

If \(G=0\), then
\[
\operatorname{Res}_h(G,s-h)=5s^2 \tag{25}
\]
and \(\mathcal A=0\) forces \(C_1=0\). Modulo \(G\), the numerator of
the coefficient in (24) is associated to \(s^5(s-6h)\). Hence
\(s=6h\), but then \(G=75h^2\), impossible because \(s,h\ne0\).

This completes \(A=0\).

## II. The branch \(A\ne0\)

No root extraction is needed. Replace \(F\) by
\[
G(X)=\operatorname{diag}(A^{-4},A^{-4},A^{-3})F(AX). \tag{26}
\]
This fixes \(H_4\) and \(R=x^3\), sends \(Axq\) to \(xq\), and satisfies
\[
\det JG=A^{-8}\det JF.
\]
Set \(A=1\), and write
\[
w=w_1,\qquad v=w_2,\qquad s=w_3.
\]
After (7),
\[
\begin{aligned}
W&=wxy+vxz+sy^2,\\
U&=xq+\frac43xW,\\
V&=C_0x^2z+C_1xy^2+C_2xyz+C_3xz^2\\
&\quad+\frac{w(3-4s)}9y^3
+\frac{(v-s)(3-4s)}9y^2z.
\end{aligned} \tag{27}
\]
The \(y^5\)-coefficient of \(E_5\) is
\[
\frac2{27}s(v-s)(4s-3)(4s+3). \tag{28}
\]
The following four closed branches therefore cover the parameter space.

### II.1. \(s=0\)

Fresh \(E_5\) compatibilities give \(v=0\) and then \(wC_3=0\).

If \(w=0\), then \(W=0\). Three literal \(E_5\) equations give
\(\ell_{32}=\ell_{33}=0\). The third coordinate is
\[
F_3=x^3+\ell_{31}x+\text{constant},
\]
so
\[
\det JF=(3x^2+\ell_{31})
\det\begin{pmatrix}
\partial_yF_1&\partial_zF_1\\
\partial_yF_2&\partial_zF_2
\end{pmatrix}, \tag{29}
\]
which cannot be a nonzero constant.

If \(w\ne0\), then \(C_3=0\), and a fresh solve gives
\[
[y^4]E_4=\frac{w^2(w-6C_2)}3.
\]
Thus \(C_2=w/6\), after which
\[
[x^2z^2]E_4=-\frac5{12}w^3\ne0. \tag{30}
\]

### II.2. \(v=s\), away from the two resonances

Assume \(s\ne0,\pm3/4\). Exact \(E_5\) compatibilities force
\[
w=C_2=C_3=0.
\]
With \(D=C_0-C_1\), the \(D\ne0\) solve gives
\[
\ell_{32}=0,\qquad \ell_{33}=sD.
\]
Two \(E_4\) equations give
\(\ell_{12}=\ell_{22}=0\), so \(\det L=0\).
At the fresh rank drop \(D=0\), \(E_5\) gives
\(\ell_{32}=\ell_{33}=0\), and \(E_4\) gives
\(\ell_{12}=\ell_{13}=0\). Again \(\det L=0\).

### II.3. The minus resonance \(s=-3/4\)

\(E_5\) forces
\[
v=-\frac34,\qquad C_2=\frac23w,\qquad C_3=0. \tag{31}
\]
If \(w\ne0\), both the \(D\ne0\) solve and the freshly recomputed \(D=0\)
solve contain two \(E_4\) coefficients whose difference is
\[
\frac{10}{81}w^4\ne0. \tag{32}
\]
If \(w=0,D\ne0\), \(E_5\) gives
\(\ell_{32}=0,\ell_{33}=-3D/4\), and \(E_4\) gives
\(\ell_{12}=\ell_{22}=0\). If \(w=0,D=0\), the fresh solve gives
\(\ell_{32}=\ell_{33}=\ell_{12}=\ell_{13}=0\). Both leaves have
\(\det L=0\).

### II.4. The plus resonance \(s=3/4\)

\(E_5\) first forces \(v=3/4\). If \(w\ne0\), it then gives
\[
C_3=0,\qquad C_2=-\frac13w,
\]
and
\[
[y^3z]E_4=-\frac12w^2\ne0. \tag{33}
\]
Take \(w=0\). The \(C_3\ne0\) chart has
\([yz^3]E_4=3C_3^2\); after the fresh specialization \(C_3=0\), the
\(C_2\ne0\) chart has \([y^3z]E_4=3C_2^2/2\). Thus only
\(C_2=C_3=0\) remains.

Put \(D=C_0-C_1\), \(t=\ell_{32}\), \(r=\ell_{33}\), and
\(h=b_2-b_3-\ell_{13}\). On \(D\ne0\), define
\[
\begin{aligned}
\mathcal P&=-3C_1D-3D^2+4Dr+6h,\\
\mathcal Q&=-3C_1D+6D^2-8Dr+6h,\\
\mathcal H&=-C_1D+2h.
\end{aligned}
\]
Four \(E_4\) coefficients are
\[
-\frac{t\mathcal P}{3D},\quad
-\frac{t\mathcal Q}{3D},\quad
-\frac{(3D-4r)\mathcal P}{6D},\quad
-\frac{(3D-4r)\mathcal H}{2D}. \tag{34}
\]
Since \(\mathcal P-\mathcal Q=3D(4r-3D)\), these equations force
\[
r=\frac34D,\qquad t\mathcal H=0.
\]
If \(t\ne0\), then
\[
[xyz]E_3=-\frac23t^2\ne0. \tag{35}
\]
If \(t=0\), \(\det L\) has a factor \(\ell_{12}\). The
\(\ell_{12}=0\) leaf is singular; on \(\ell_{12}\ne0\), lower
identities force \(\mathcal H=0\), \(\ell_{13}=h\), and finally
\[
[xy]E_2=-\frac34\ell_{12}^2\ne0.
\]

At \(D=0\), recompute without a \(D\)-pivot and put
\(\alpha=C_1-2a_3\). Four \(E_4\) coefficients are
\[
-\frac{t(3\alpha+4r)}3,\quad
-\frac{t(3\alpha-8r)}3,\quad
\frac{2r(3\alpha+4r)}3,\quad
2r\alpha. \tag{36}
\]
They force \(r=0\) and \(t\alpha=0\). If \(t=0\), the last two columns
of \(L\) are proportional. If \(t\ne0\), then \(\alpha=0\) and the
same coefficient (35) is nonzero.

This completes \(A\ne0\), hence the theorem.

## Exhaustive branch ledger

| Top branch | Fresh subchart | Exact exit |
|---|---|---|
| \(A=0,w_3\ne0\) | \(D=0\) | \(E_5\) zeros four entries of \(L\) |
| \(A=0,w_3\ne0\) | \(D\ne0,\ a_3\ne0\) | \(648a_3^4\) pivot and (9) |
| \(A=0,w_3\ne0\) | \(D\ne0,\ a_3=0\) | \(2048s^8/81\) pivot and (9c) |
| \(A=0,W=0\) | \(a_3=0\) | two \(E_4\) squares, then \(\det L=0\) |
| \(A=0,W=0\) | \(a_3\ne0\) | determinant identity (16) |
| \(A=0,W=sxz\) | \(C_7\ne0\) | \(-8s^4/27\) in \(E_4\) |
| \(A=0,W=sxz\) | \(C_7=0\) | fresh nonzero \(E_5\) minor |
| \(A=0,W=sxy\) | \(h=0\) | \(-4s^3/9\) in \(E_5\) |
| \(A=0,W=sxy\) | \(3h+2s=0,\ C_1=0\) | \(E_2,E_1\) squares; singular \(L\) |
| \(A=0,W=sxy\) | \(3h+2s=0,\ 2C_0=3C_1\) | \(E_2\) chain; singular \(L\) |
| \(A=0,W=sxy\) | second factor, \(G\ne0\) | returns to \(3h+2s=0\) |
| \(A=0,W=sxy\) | second factor, \(G=0\) | resultant and \(G(6h,h)=75h^2\) |
| \(A\ne0,s=0\) | \(W=0\) | factorization (29) |
| \(A\ne0,s=0\) | \(W\ne0\) | residual \(-5w^3/12\) |
| \(A\ne0,v=s\) | \(D\ne0\) or \(D=0\) | proportional/zero columns in \(L\) |
| \(A\ne0,s=-3/4\) | \(w\ne0\), both \(D\)-charts | residual \(10w^4/81\) |
| \(A\ne0,s=-3/4\) | \(w=0\), both \(D\)-charts | singular \(L\) |
| \(A\ne0,s=3/4\) | \(w\ne0\) | residual \(-w^2/2\) |
| \(A\ne0,s=3/4,w=0\) | \(C_3\ne0\) or \(C_2\ne0\) | fresh \(E_4\) squares |
| plus aligned | \(D\ne0,t\ne0\) | residual \(-2t^2/3\) |
| plus aligned | \(D\ne0,t=0\) | determinant factor or \(-3\ell_{12}^2/4\) |
| plus aligned | \(D=0,t=0\) | proportional columns |
| plus aligned | \(D=0,t\ne0\) | residual \(-2t^2/3\) |

Every divisor used by a localized pivot has its zero locus recomputed
before solving. No resultant or denominator clearing is used without a
corresponding fresh rank-drop chart.

## Disclosure

This result was developed with AI assistance and has not been peer reviewed.
The exact checks are evidence about the encoded polynomial identities, not a
substitute for independent mathematical scrutiny or a guarantee of
worldwide priority.
