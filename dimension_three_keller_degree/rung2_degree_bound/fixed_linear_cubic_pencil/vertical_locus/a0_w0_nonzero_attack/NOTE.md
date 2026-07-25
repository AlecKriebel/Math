# The zero-companion-parameter branch with \(W_0\ne0\)

**Status:** exact exclusion; independent hostile audit passed in
`../audit_a0_w0_nonzero/REPORT.md`.  This note is not peer reviewed.

**Recorded (UTC):** 2026-07-25T22:06:11Z.

## 1. Statement and scope

Work on the triple-vertical, vertical-companion row
\[
H_4=(z^4,zq,0),\qquad
H_3=(U,V,z^3),\qquad
H_2=(A,B,W),
\tag{1}
\]
where \((z^3,q)\) is a minimal cubic pencil and \(q|_{z=0}\ne0\).
After the complete legal \(E_7\) gauge, the zero value of the companion
parameter (also denoted \(s=0\) in some working files) is
\[
U=\frac43zW.                                           \tag{2}
\]
Put
\[
q_0=q|_{z=0},\qquad W_0=W|_{z=0}.
\]

### Theorem

There is no solution of \(E_6=0\) on the locus
\[
\boxed{W_0\ne0}
\tag{3}
\]
for which the cubic pencil \((z^3,q)\) is minimal.

More precisely, \(E_6=0\) and \(W_0\ne0\) force
\[
q\in\operatorname{Sym}^3\langle z,L\rangle
\tag{4}
\]
for a linear form \(L\notin\mathbb Cz\).  Thus every formal solution is
on the exact nonminimal boundary and reclassifies into the
\((a,b)=(1,3)\) row.

No hypothesis on the root multiplicity of \(q_0\) is omitted.  The proof
retains every coefficient of \(q,W,A,B,V\) and of the linear part.  It
does not use \(E_5,E_4\), invertibility of the linear part, or division by
a discriminant or a possibly zero jet coefficient.

## 2. The binary \(E_5\) family, classified without losing boundaries

The restriction of \(E_5\) to \(z=0\) is one third of
\[
4W_0\{V_0,W_0\}+3q_0\{W_0,A_0\},                     \tag{5}
\]
where
\[
\{f,g\}=f_xg_y-f_yg_x,\quad
A_0=A|_{z=0},\quad V_0=V|_{z=0}.
\]
The vanishing of (5) has the following complete elementary
classification.  It is included both to preserve all root/collision
strata requested in the attack and to show that no attractive binary
rank drop was silently discarded.  Full \(E_6\) will supersede all but
one of these rows.

### 2.1 Squarefree quadratic \(W_0\)

Normalize \(W_0=xy\), and write
\[
\begin{aligned}
q_0&=q_{30}x^3+q_{21}x^2y+q_{12}xy^2+q_{03}y^3,\\
A_0&=a x^2+bxy+c y^2,\\
V_0&=d_{30}x^3+d_{21}x^2y+d_{12}xy^2+d_{03}y^3.
\end{aligned}
\]
Then (5) vanishes if and only if
\[
\boxed{a q_{30}=0,\qquad c q_{03}=0}                 \tag{6}
\]
and
\[
\begin{aligned}
d_{30}&=\frac12a q_{21},\\
d_{21}&=\frac32(aq_{12}-cq_{30}),\\
d_{12}&=\frac32(cq_{21}-aq_{03}),\\
d_{03}&=\frac12c q_{12},
\end{aligned}                                         \tag{7}
\]
with \(b\) free.  Therefore:

| common factors of \(q_0\) and \(xy\) | free part of \(A_0\) |
|---|---|
| none | \(A_0=bxy\) |
| \(x\) only | \(A_0=bxy+cy^2\) |
| \(y\) only | \(A_0=ax^2+bxy\) |
| \(xy\) | \(A_0\) arbitrary |

Formula (7), rather than a generic-rank statement, gives \(V_0\) on
every boundary.

The root-multiplicity strata and common-factor strata are:

| root type of \(q_0\) | possible common roots with \(xy\) |
|---|---|
| squarefree | none, exactly one, or both |
| double \(L^2M\) | none; one common root which is \(L\) or \(M\); or both |
| triple \(L^3\) | none, or the triple root is \(x\) or \(y\) |

The stabilizer of \(xy\) leaves continuous root-position moduli in
several rows.  No finite-orbit claim is being made; (6)--(7) are uniform
in those moduli.

### 2.2 Double quadratic \(W_0\)

Normalize \(W_0=\gamma x^2\), with \(\gamma\ne0\).  Equation (5) becomes
\[
\boxed{4\gamma x^2(V_0)_y=3q_0(A_0)_y.}               \tag{8}
\]
Let \(m=\operatorname{ord}_x(q_0)\).

* If \(m=0\), then
  \[
  A_0=ax^2,\qquad V_0=dx^3.
  \tag{9}
  \]
* If \(m=1\), write
  \(q_0=x(rx^2+sxy+ty^2)\).  Then
  \[
  \begin{aligned}
  A_0&=ax^2+bxy,\\
  V_0&=dx^3+\frac{3b}{4\gamma}
  \left(rx^2y+\frac{s}{2}xy^2+\frac{t}{3}y^3\right).
  \end{aligned}                                       \tag{10}
  \]
* If \(m\ge2\), write \(q_0=x^2(rx+sy)\).  Then \(A_0\)
  is arbitrary and
  \[
  V_0=dx^3+\frac{3}{4\gamma}
  \left(
  brx^2y+\frac{bs+2cr}{2}xy^2+\frac{2cs}{3}y^3
  \right),
  \tag{11}
  \]
  where \(b=[xy]A_0\) and \(c=[y^2]A_0\).

This retains the complete root table:

| root type of \(q_0\) | possible \(m\) |
|---|---|
| squarefree | \(0,1\) |
| double \(L^2M\) | \(0\), \(1\) when \(x=M\), \(2\) when \(x=L\) |
| triple \(L^3\) | \(0,3\) |

Thus (5) alone has many genuine collision leaves.  None is used as a
generic proxy for another.

## 3. Compact full-\(E_6\) identity

Let \(L_3\) be the third linear row.  Row multilinearity gives
\[
\begin{aligned}
E_6={}&
\operatorname{Jac}(z^4,zq,L_3)
+\operatorname{Jac}\!\left(\tfrac43zW,zq,W\right)
+\operatorname{Jac}(z^4,V,W)\\
&+\operatorname{Jac}(A,zq,z^3)
+\operatorname{Jac}\!\left(\tfrac43zW,V,z^3\right)
+\operatorname{Jac}(z^4,B,z^3).
\end{aligned}                                         \tag{12}
\]
The last term is zero.  The two terms containing \(V\) are respectively
\(4z^3\{V,W\}\) and \(4z^3\{W,V\}\), so they cancel exactly.  Finally,
\[
\operatorname{Jac}(zW,zq,W)=zW\{q,W\}.
\]
Consequently
\[
\boxed{3E_6=z\Phi},\qquad
\boxed{\Phi=
4W\{q,W\}+9z^2\{A,q\}+12z^3\{q,L_3\}.}                \tag{13}
\]
This keeps \(B,V\) and the first two linear rows fully arbitrary: they
cancel or do not occur, rather than having been specialized.

The coefficient of the first power of \(z\) in (13) is
\[
4W_0\{q_0,W_0\}.
\]
Since \(W_0\ne0\),
\[
\boxed{\{q_0,W_0\}=0.}                                \tag{14}
\]

For completeness, if binary forms \(f,g\) of degrees three and two
satisfy \(\{f,g\}=0\), dehomogenization gives
\[
2F'G-3FG'=0,
\]
and hence \(F^2/G^3\) is constant.  Unique factorization gives
\[
f=\kappa L^3,\qquad g=\gamma L^2,\qquad
\kappa\gamma\ne0.                                     \tag{15}
\]
Thus (14) immediately excludes every squarefree and double-root
\(q_0\), every disjoint-root row, and every partial common-factor row in
Section 2.  The only binary survivor is the coincident triple/double
root.

## 4. Exact higher-\(z\) elimination on the sole survivor

Extend a binary change sending \(L\) to \(x\).  Do **not** normalize
\(\kappa\) or \(\gamma\), and retain every lower jet:
\[
\begin{aligned}
q={}&\kappa x^3
+z(\alpha x^2+\beta xy+\chi y^2)
+z^2(\delta x+\epsilon y)+\phi z^3,\\
W={}&\gamma x^2+z(ux+vy)+\omega z^2,\\
A={}&a_{20}x^2+a_{11}xy+a_{02}y^2
+z(a_{10}x+a_{01}y)+a_{00}z^2.
\end{aligned}                                         \tag{16}
\]
The six decisive raw coefficients of \(\Phi\) are
\[
\begin{aligned}
[x^3yz]\Phi={}&-16\chi\gamma^2,\\
[x^4z]\Phi={}&4\gamma(-2\beta\gamma+3\kappa v),\\
[x^2yz^2]\Phi={}&-2(27\kappa a_{02}+2\beta\gamma v
 +12\chi\gamma u-6\kappa v^2),\\
[y^2z^3]\Phi={}&-2(9a_{02}\beta-9a_{11}\chi
 -2\beta v^2+4\chi uv),\\
[x^3z^2]\Phi={}&-27\kappa a_{11}+8\alpha\gamma v
 -12\beta\gamma u-8\epsilon\gamma^2+12\kappa uv,\\
[yz^4]\Phi={}&-9a_{01}\beta-18a_{02}\delta+18a_{10}\chi
 +9a_{11}\epsilon+12\beta\ell_{32}+4\beta v\omega\\
&\quad-24\chi\ell_{31}-8\chi u\omega
 +4\delta v^2-4\epsilon uv.
\end{aligned}                                         \tag{17}
\]

Here is a parameter-division-free elimination.  The first coefficient
gives \(\chi=0\).  Put
\[
\begin{aligned}
r&=2\beta\gamma-3\kappa v,\\
f&=27\kappa a_{02}+2\beta\gamma v-6\kappa v^2,\\
g&=9a_{02}-v^2,\\
h&=9a_{02}\beta-2\beta v^2.
\end{aligned}
\]
The next three equations give \(r=f=h=0\), and the exact combinations
\[
f-vr=3\kappa g,\qquad h-\beta g=-\beta v^2             \tag{18}
\]
give \(g=0\) and \(\beta v^2=0\).  Multiplying \(r=0\) by
\(v^2\) now gives \(-3\kappa v^3=0\).  Hence
\[
v=\beta=a_{02}=0.                                     \tag{19}
\]

The last two coefficients in (17) reduce to
\[
27\kappa a_{11}+8\gamma^2\epsilon=0,\qquad
9a_{11}\epsilon=0.                                   \tag{20}
\]
If the first equation is multiplied by \(\epsilon\) and three
\(\kappa\) times the second is subtracted, the result is
\[
8\gamma^2\epsilon^2=0.
\]
Thus
\[
\epsilon=a_{11}=0.                                   \tag{21}
\]

Equations (16), (19), and (21) leave
\[
\boxed{q=\kappa x^3+\alpha x^2z+\delta xz^2+\phi z^3
\in\mathbb C[x,z]_3.}                                 \tag{22}
\]

For a cubic pencil containing \(z^3\), the nonminimal boundary is
exactly
\[
q\in\operatorname{Sym}^3\langle z,L\rangle
\quad\text{for some }L\notin\mathbb Cz.
\]
Equation (22) is precisely that boundary.  This proves the theorem.

## 5. Sharp boundary witness

Minimality is essential to the exclusion.  On the nonminimal boundary,
take
\[
q=x^3,\quad W=x^2,\quad A=B=V=0,\quad L=I.
\tag{23}
\]
Then
\[
\det\!\left(I+\tau JH_2+\tau^2JH_3+\tau^3JH_4\right)
=1+\frac{\tau^2}{3}z(8x+9z)-\frac{8\tau^3}{3}x^3.
\tag{24}
\]
Thus
\[
E_8=E_7=E_6=E_5=E_4=0
\]
with an invertible linear part, while \(E_3,E_2\) remain nonzero.
This is an exact regression witness against incorrectly extending the
minimal-pencil exclusion to the reclassification boundary.

## 6. Verification

Two exact checkers accompany this note:

* `verify_a0_w0_nonzero_sympy.py` constructs each weighted determinant
  coefficient by raw row multilinearity, independently constructs
  (12), checks (13), checks every coefficient and ideal identity above,
  checks both complete binary tables, and verifies the boundary witness;
* `verify_a0_w0_nonzero_sparse.py` uses dependency-free sparse
  multivariate arithmetic to reconstruct the full raw determinant and
  exterior expression independently, and verifies the same decisive
  algebra and boundary determinant.

`verify_strict.sh` runs both, rejects deliberate sign/coefficient
mutations, and rejects optimized Python.  At the recorded state the
hashes are:

```text
9e61daa1b3b1612f681597ee8ad69ba7f395e3027c6cedf9d445f36c6736c7c5  verify_a0_w0_nonzero_sympy.py
6cb322a9995960043c474955ec8f0a89793fca20af959ebfc160fadb37ad35cf  verify_a0_w0_nonzero_sparse.py
8e195121766ecc306ab18b99acda165a6fc1cba38f1dcdffd9231ecaa0db3a7a  verify_strict.sh
9ad87c003bc0ce00e86b8c863b53af356aeec900d487c93999981908e28528e9  ../audit_vertical_triple_yz2_gamma0_ell0/verify_vertical_triple_yz2_sparse.py
```

The hashes must be refreshed after any edit.  Exact checks are evidence
about the encoded algebra; they are not peer review.  AI systems
materially assisted the derivation, computation, and exposition.

The independent hostile reconstruction in
`../audit_a0_w0_nonzero/REPORT.md` forms the literal weighted determinant
with a separate dependency-free sparse implementation, rederives the
binary-power step and all six eliminations, and passes the strict sentinel
`A0_W0_NONZERO_INDEPENDENT_STRICT_PASS_94A60D`.
