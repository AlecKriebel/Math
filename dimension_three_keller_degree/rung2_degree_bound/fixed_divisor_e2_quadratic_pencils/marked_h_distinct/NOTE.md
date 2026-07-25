# Six marked-\(h\)-distinct endpoint slices through \(E_6\)

## Status and scope

**Exact first-stage slice calculation; the attempted six-branch taxonomy
failed completeness.  No exclusion and no row closure are claimed.**

The all-vertical top theorem leaves a minimal pencil with unique double
member \(s=\ell^2\), while the fixed component gcd is a marked member
\(h\) of that pencil.  Earlier lower packages treated only \(h=s\).
This note begins the missing \(h\ne s\) calculation.

For each of the three marked-member orbits, this note computes the two
endpoint companions \(R=xh\) and \(R=xs=x^3\).  All six endpoint slices
survive the weighted Jacobian identities through \(E_6\).

During the completeness check, however, exact top-identity points with
\(R=x(\alpha h+\beta s)\) were found that are inequivalent to both
endpoints.  Thus these six slices are **not** an exhaustive denominator
and lower exclusion work was halted under the freeze-violation protocol.
The later clean-room reconstruction confirmed the exact companion quotient
\(3+\mathbb P^1+3\).  See `COMPANION_MODULI_GAP.md` and
`FREEZE_READINESS_COMPARISON.md`.

This is not peer reviewed.  AI systems assisted with the derivation,
case organization, exposition, and verification code.  Exact computer
checks certify the encoded algebra, not the exposition, novelty, or
worldwide priority.

## 1. The six computed endpoint slices

Put
\[
s=x^2,\qquad
H_4=(P,Q,0)=(h^2,hs,0),                              \tag{1}
\]
and write
\[
F=LX+H_2+H_3+H_4,\qquad
H_3=(U,V,R),\qquad W=(H_2)_3.                        \tag{2}
\]
The first two components of \(H_2\) are arbitrary quadratics throughout,
and \(L\) is an arbitrary \(3\times3\) matrix subject only to
\(\det L\ne0\) for a Keller map.

The three missing marked-member orbits are
\[
\begin{array}{c|c|c}
\text{label}&\langle s,r\rangle&h\\ \hline
\mathrm{RT\!-\!reducible}&\langle x^2,yz\rangle&yz\\
\mathrm{RT\!-\!smooth}&\langle x^2,yz\rangle&x^2+yz\\
\mathrm{RO\!-\!smooth}&\langle x^2,y^2+xz\rangle&y^2+xz.
\end{array}                                           \tag{3}
\]
Here `RT` and `RO` refer only to the two canonical pencil types.  The two
endpoint companions computed in this note are
\[
R=xh\quad\text{(companion \(H\))},\qquad
R=xs=x^3\quad\text{(companion \(S\))}.                \tag{4}
\]
Their factorization types distinguish these endpoints.  They do not
exhaust the projective kernel \(x\mathbb P\langle h,s\rangle\).  For
example, when \(h=yz\), the third quotient
\(s+h=x^2+yz\) has rank three, while \(s\) and \(h\) have ranks one and
two.  The complete invariant companion problem is the stabilizer quotient
formulated in `COMPANION_MODULI_GAP.md`.

Introduce a bookkeeping variable \(\tau\) and set
\[
\mathcal J(\tau)=
L+\tau JH_2+\tau^2JH_3+\tau^3JH_4,\qquad
E_j=[\tau^j]\det\mathcal J(\tau).                    \tag{5}
\]
The displayed leading forms satisfy \(E_9=E_8=0\).  The next equation is
\[
E_7=
\operatorname{Jac}(P,Q,W)+
\operatorname{Jac}(P,V,R)+
\operatorname{Jac}(U,Q,R)=0.                         \tag{6}
\]

## 2. What “legal normal form” means here

The raw variables in (6) are the twenty cubic coefficients of \(U,V\)
and the six quadratic coefficients of \(W\).  The following five kernel
directions are independent in every one of the six endpoint slices:
\[
(R,0,0),\quad(0,R,0),\quad
(\partial_iP,\partial_iQ,\partial_iR)\quad(i=x,y,z).
\tag{7}
\]
The first two are invertible target shears by the third component.  The
last three are the degree-\((3,3,2)\) effects of source translations.
They are legal equivalences and merely reparametrize the unrestricted
lower terms.  No nonlinear coordinate change, normalization of \(L\), or
division by a parameter is used.

For each endpoint slice below, the five directions (7) plus the displayed
parameter directions form the entire kernel of (6).  Thus the forms are
complete modulo legal gauges.

## 3. Complete \(E_7\) normal forms

### 3.1. Companion \(H\) for both rank-two-pencil marked orbits

For either
\[
h=yz\quad\text{or}\quad h=x^2+yz,\qquad R=xh,
\]
a complete seven-parameter complement is
\[
\begin{aligned}
U={}&Ax^3-2Cyh-2Dzh,\\
V={}&Bx^3+Cx^2y+Dx^2z+2Exy^2+2Fxz^2,\\
W={}&Tx^2+Ey^2+Fz^2.
\end{aligned}                                        \tag{8}
\]

### 3.2. Companion \(S\), reducible marked member

For \(h=yz\) and \(R=x^3\), a complete five-parameter complement is
\[
\begin{aligned}
U={}&Axyz,\\
V={}&Bxyz+\frac23Cy^2z+\frac23Dyz^2,\\
W={}&Cxy+Dxz+Tyz.
\end{aligned}                                        \tag{9}
\]

### 3.3. Companion \(S\), smooth member of the rank-two pencil

For \(h=x^2+yz\) and \(R=x^3\), a complete five-parameter complement is
\[
\begin{aligned}
U={}&Axyz-\frac43Cyh-\frac43Dzh,\\
V={}&Bxyz+\frac23Cy^2z+\frac23Dyz^2,\\
W={}&Cxy+Dxz+Tyz.
\end{aligned}                                        \tag{10}
\]
The representatives in (9) and (10) differ because the \(x^3\) target
shear has already been quotiented out.

### 3.4. Companion \(H\), smooth member of the rank-one pencil

For \(h=y^2+xz\) and \(R=xh\), a complete seven-parameter complement is
\[
\begin{aligned}
U={}&Ax^3-2Cyh-2Dzh+2Tzh,\\
V={}&Bx^3+Cx^2y+(D+T)x^2z+2Exyz+2Fxz^2,\\
W={}&Txz+Eyz+Fz^2.
\end{aligned}                                        \tag{11}
\]

### 3.5. Companion \(S\), smooth member of the rank-one pencil

For \(h=y^2+xz\) and \(R=x^3\), a complete five-parameter complement is
\[
\begin{aligned}
U={}&2Azh,\\
V={}&Ax^2z+Bxh+\frac23Cyh+\frac23Dzh,\\
W={}&Cxy+Sh+Dxz.
\end{aligned}                                        \tag{12}
\]

## 4. Exact \(E_6\) compatibility systems

Let the first two components of \(H_2\) have twelve independent
coefficients and let \(L\) have nine independent coefficients.  After
substitution of (8)--(12), \(E_6=0\) is an affine-linear system in these
twenty-one lower coefficients with twenty-eight coefficient equations.
Every computed slice has a constant maximal minor.  Hence its rank is constant on
the whole normal-parameter space, and the left-kernel residuals below are
specialization-safe necessary and sufficient conditions for solving
\(E_6\).

The exact compatibility ideals are:
\[
\begin{array}{c|c}
\text{branches}&I_6\\ \hline
\mathrm{RT\!-\!reducible/H},\
\mathrm{RT\!-\!smooth/H}
&
(AC,AD,AE,AF,CE,DF,E^2,F^2)
\\[1mm]
\mathrm{RT\!-\!reducible/S},\
\mathrm{RT\!-\!smooth/S}
&
(C^2,D^2)
\\[1mm]
\mathrm{RO\!-\!smooth/H}
&
(AC,AD,AE,AF,CF+DE,EF,2DF-E^2,F^2)
\\[1mm]
\mathrm{RO\!-\!smooth/S}
&
(CD,D^2).
\end{array}                                           \tag{13}
\]
This is a scheme-theoretic statement about the compatibility residuals,
not merely their radical.  Over a characteristic-zero field, the
field-valued solutions reduce to
\[
\begin{array}{c|c}
\text{branches}&\sqrt{I_6}\text{ as equations on points}\\ \hline
\mathrm{RT/H}&E=F=0,\quad AC=AD=0,\\
\mathrm{RT/S}&C=D=0,\\
\mathrm{RO/H}&E=F=0,\quad AC=AD=0,\\
\mathrm{RO/S}&D=0.
\end{array}                                           \tag{14}
\]
In particular, no condition forces the fixed nonzero companion \(R\) to
vanish.

## 5. Six-slice rank and survivor table

The raw \(E_7\) matrix has shape \(36\times26\).  The \(E_6\) lower-data
matrix has shape \(28\times21\).

| Branch | \(\operatorname{rank}E_7\) | Nullity \(=\) gauges + normal | \(\operatorname{rank}E_6\) | Field-valued \(E_6\) survivor | Verdict |
|---|---:|---:|---:|---|---|
| RT-reducible/H | 14 | \(12=5+7\) | 8 | \(E=F=0,\ A(C,D)=0\) | survives to \(E_5\) |
| RT-reducible/S | 16 | \(10=5+5\) | 10 | \(C=D=0\) | survives to \(E_5\) |
| RT-smooth/H | 14 | \(12=5+7\) | 8 | \(E=F=0,\ A(C,D)=0\) | survives to \(E_5\) |
| RT-smooth/S | 16 | \(10=5+5\) | 10 | \(C=D=0\) | survives to \(E_5\) |
| RO-smooth/H | 14 | \(12=5+7\) | 8 | \(E=F=0,\ A(C,D)=0\) | survives to \(E_5\) |
| RO-smooth/S | 16 | \(10=5+5\) | 10 | \(D=0\) | survives to \(E_5\) |

Thus the immediate-exclusion count **within the six computed slices** is
\[
\boxed{0/6},
\]
and the slice-survivor count after \(E_6\) is
\[
\boxed{6/6}.
\]

## 6. Pivot ledger: no hidden specialization divisors

The verification uses the following fixed nonzero minors.

| Branch | Raw \(E_7\) maximal minor | Legal-basis minor | \(E_6\) maximal minor |
|---|---:|---:|---:|
| RT-reducible/H | \(-82944\) | \(64\) | \(256\) |
| RT-reducible/S | \(25389989167104\) | \(16/3\) | \(-26873856\) |
| RT-smooth/H | \(-82944\) | \(64\) | \(256\) |
| RT-smooth/S | \(25389989167104\) | \(16/3\) | \(-26873856\) |
| RO-smooth/H | \(-13271040\) | \(-128\) | \(3072\) |
| RO-smooth/S | \(12187194800209920\) | \(64/3\) | \(1934917632\) |

Every pivot is a nonzero rational constant.  There are therefore **no
parameter pivot divisors and no omitted rank-drop charts through
\(E_6\)**.  The factors \(1/3\) are harmless in characteristic zero.  The
exact row and column indices of every pinned minor are recorded in both
verification scripts.

## 7. Sharp through-\(E_6\) witnesses

Every computed slice has the same lower-data witness:
\[
U=V=W=0,\qquad H_2=0,\qquad
L=
\begin{pmatrix}
0&1&0\\
0&0&1\\
1&0&0
\end{pmatrix},
\qquad \det L=1.                                     \tag{15}
\]
Keep the slice's fixed nonzero \(R\) in the third component of \(H_3\).
Then \(E_9=E_8=E_7=E_6=0\).  Indeed, the third row of \(L\) is \(dx\),
and
\(\operatorname{Jac}(h^2,hx^2,x)=0\).

These witnesses fail first at \(E_5\), with exact values
\[
\begin{array}{c|l}
\text{branch}&E_5\\ \hline
\mathrm{RT\!-\!reducible/H}
&-y^2z(x^2-2z^2)\\
\mathrm{RT\!-\!reducible/S}
&3x^2y(x^2+2z^2)\\
\mathrm{RT\!-\!smooth/H}
&-(x^2+yz)(x^2y-2x^2z-2yz^2)\\
\mathrm{RT\!-\!smooth/S}
&3x^2(x^2y+2x^2z+2yz^2)\\
\mathrm{RO\!-\!smooth/H}
&-(xz+y^2)(x^3-4xyz-4y^3)\\
\mathrm{RO\!-\!smooth/S}
&3x^2(x^3+4xyz+4y^3).
\end{array}                                           \tag{16}
\]
Thus (15) is sharp for the present stage: it proves that none of the six
endpoint slices can be excluded by the top identities or \(E_6\), while
making no claim about the missing companion locus or lower identities.

## 8. Freeze gate

Do **not** carry these slices to \(E_5\) yet.  The clean-room
reconstruction of
\[
\Gamma_{V,[h]}\backslash\mathbb P(V)
\]
is complete and agrees with the scope audit, but the parent freeze must
first record its stable IDs, projective parameter, and boundary charts.
The frozen row remains provisional.
