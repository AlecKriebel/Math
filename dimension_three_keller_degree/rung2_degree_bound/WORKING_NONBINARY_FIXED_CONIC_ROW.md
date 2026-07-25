# Working theorem: the nonbinary fixed-divisor conic strata

**Status:** proved and independently adversarially confirmed from the raw
determinant systems, including the seven-form taxonomy and combined theorem
scope.  An earlier audit caught a false homogeneous-orbit claim in the
draft, and affine translations give the stronger corrected proof.  This is
not peer reviewed.

**Recorded:** 2026-07-25T03:24:00Z.

**Promoted after combined audit:** 2026-07-25T04:03:51Z.

## 1. Setup

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have total degree four and put
\[
H_4=h(p,q,r)A(p,q),\qquad
A=(p^2,pq,q^2)^T,
\tag{1}
\]
where \(h\) is a nonzero quadratic.  Write
\[
A_p=\partial_pA,\qquad A_q=\partial_qA,\qquad
\Delta=A_p\times A_q=2(q^2,-2pq,p^2)^T.
\tag{2}
\]

The binary case \(h\in\mathbb C[p,q]_2\) is excluded in
`WORKING_FIXED_CONIC_ROW.md`.  This note begins the complementary case
\[
h\notin\mathbb C[p,q].
\tag{3}
\]

## 2. A general adjugate identity

Let \(C=J(hA)\), put \(h_r=\partial_rh\), and define
\[
k=(ph_r,\;qh_r,\;rh_r-4h)^T.
\tag{4}
\]
Direct column crosses give the rank-one identity
\[
\boxed{\operatorname{adj}C=-\frac h2\,k\Delta^T.}
\tag{5}
\]
In particular, \(Ck=0\).  The degree-eight coefficient of the Keller
determinant is
\[
E_8=\operatorname{tr}(\operatorname{adj}C\,JH_3)
   =-\frac h2\,\Delta\cdot D_k(H_3).
\tag{6}
\]
Thus \(E_8=0\) implies
\[
\Delta\cdot D_k(H_3)=0.
\tag{7}
\]

Set
\[
N=\Delta\cdot H_3.
\tag{8}
\]
Since \(\Delta\) is a binary quadratic vector,
\[
D_k\Delta=2h_r\Delta.
\tag{9}
\]
Equations (7)--(9) therefore give the scalar differential equation
\[
\boxed{D_kN=2h_rN.}
\tag{10}
\]

## 3. Logarithmic valuations force \(N=0\)

Dehomogenize on \(p\ne0\):
\[
t=\frac qp,\qquad s=\frac rp,\qquad
h=p^2H(t,s),\qquad N=p^5n(t,s).
\tag{11}
\]
The derivation (4) satisfies
\[
D_kp=p^2H_s,\qquad D_kt=0,\qquad D_ks=-4pH.
\tag{12}
\]
Substitution in (10) gives
\[
\boxed{4Hn_s=3H_sn.}
\tag{13}
\]

Suppose \(n\ne0\), and work in the PID \(\mathbb C(t)[s]\).  Let
\(\phi^m\Vert H\) be an \(s\)-dependent irreducible factor.  Characteristic
zero makes \(\phi\) separable, so the logarithmic residues of (13), after
division by \(Hn\), give
\[
\boxed{4v_\phi(n)=3m.}
\tag{14}
\]
Because \(H\) is quadratic, an \(s\)-dependent factor has multiplicity
\(m=1\) or \(m=2\).  Neither value makes the right side of (14) divisible
by four.  This contradiction proves \(n=0\), hence \(N=0\).

The Hilbert--Burch syzygy module of the components of \(\Delta\) is generated
by \(A_p,A_q\).  Since \(H_3\) is cubic, there are homogeneous quadratics
\(f,g\) such that
\[
\boxed{H_3=fA_p+gA_q.}
\tag{15}
\]

### Degree-eight theorem

For every nonbinary quadratic fixed divisor \(h\), the degree-eight Keller
identity forces (15).

This simultaneously covers all five parabolic normal forms
\[
r^2,\qquad r^2+p^2,\qquad r^2+pq,\qquad pr,\qquad pr+q^2,
\tag{16}
\]
including square and reducible cases.  No cancellation of \(h\), \(H_s\),
or a possibly zero \(N\) was used.

## 4. The first normal form \(h=r^2\)

Write
\[
\begin{aligned}
f&=f_0(p,q)+rf_1(p,q)+a_5r^2,\\
g&=g_0(p,q)+rg_1(p,q)+b_5r^2
\end{aligned}
\tag{17}
\]
and set
\[
R=qf_0-pg_0,\qquad S=qf_1-pg_1.
\tag{18}
\]
For \(H_4=r^2A\),
\[
JH_4=[\,r^2A_p\;\;r^2A_q\;\;2rA\,],
\qquad
\operatorname{adj}(JH_4)=-r^3(p,q,-r)^T\Delta^T.
\tag{19}
\]
Consequently the \(H_2\)-term in \(E_7\) is divisible by \(r^3\).
A raw expansion of the other polarization gives the division-free
certificate
\[
\boxed{
\operatorname{tr}\bigl(\operatorname{adj}(JH_3)JH_4\bigr)
\equiv12rR^2+16r^2RS\pmod {r^3}.}
\tag{20}
\]
The coefficient of \(r\) forces \(R=0\).  Since \(p,q\) are coprime,
\[
f_0=pL,\qquad g_0=qL
\tag{21}
\]
for a binary linear form \(L\).

Writing
\[
L=a_0p+a_1q,
\]
the complete degree-seven necessary form is therefore
\[
\boxed{
\begin{aligned}
f&=pL+r(a_3p+a_4q+a_5r),\\
g&=qL+r(b_3p+b_4q+b_5r).
\end{aligned}}
\tag{22}
\]
Equivalently, if the coefficients of \(f,g\) are ordered by
\((p^2,pq,q^2,pr,qr,r^2)\), then
\[
b_0=a_2=0,\qquad b_1=a_0,\qquad b_2=a_1.
\tag{23}
\]

These conditions are also sufficient for the degree-seven identity.  One
exact particular quadratic part is
\[
\begin{aligned}
(H_2)_1={}&\bigl((a_3-b_4)^2-2a_4b_3\bigr)p^2
+2a_4(a_3-b_4)pq+a_4^2q^2+a_5^2r^2,\\
(H_2)_2={}&b_3(a_3-b_4)p^2+a_5b_5r^2,\\
(H_2)_3={}&b_3^2p^2+b_5^2r^2.
\end{aligned}
\tag{24}
\]
Substitution of (22)--(24) makes \(E_7\) identically zero.

## 5. Affine normalization and the degree-six exit

Precompose \(F\) by the source translation
\[
(p,q,r)\longmapsto(p+\xi,q+\eta,r).
\tag{25}
\]
Its degree-four part remains \(r^2A(p,q)\).  The contribution of \(H_4\)
to the new cubic part is
\[
r^2(\xi A_p+\eta A_q),
\tag{26}
\]
while translating the old \(H_3\) changes only terms of degree at most two.
Choosing \((\xi,\eta)=(-a_5,-b_5)\) therefore normalizes
\[
\boxed{a_5=b_5=0}
\tag{27}
\]
without changing the Keller property or whether the map is an automorphism.
This affine normalization is essential; restricting to the homogeneous
stabilizer would leave spurious continuous parameters.

After (27), put
\[
\begin{aligned}
H_2^0={}&
\begin{pmatrix}
\bigl((a_3-b_4)^2-2a_4b_3\bigr)p^2
 +2a_4(a_3-b_4)pq+a_4^2q^2\\
b_3(a_3-b_4)p^2\\
b_3^2p^2
\end{pmatrix}.
\end{aligned}
\tag{28}
\]
The full affine space of \(H_2\) solving degree seven is
\[
\boxed{
H_2=H_2^0+\ell A_p+mA_q+
r\begin{pmatrix}
u_0p+u_1q\\u_2p+u_3q\\u_4p+u_5q
\end{pmatrix},
}
\tag{29}
\]
where \(\ell,m\) are arbitrary binary linear forms.

For completeness, the kernel statement in (29) does not come from a sample
rank.  By (19), the difference \(K\) of two degree-seven solutions satisfies
\[
\Delta\cdot D_{(p,q,-r)}K=0.
\]
On binary quadratics, \(r\) times binary linears, and constant vectors times
\(r^2\), the derivation has respective weights \(2,0,-2\).  Hence the
binary part is a quadratic syzygy of \(\Delta\), the \(r\)-linear part is
free, and the \(r^2\)-coefficient is a constant syzygy.  Hilbert--Burch
gives the \(\ell A_p+mA_q\) term, while the absence of a constant syzygy
kills the \(r^2\)-coefficient.  This proves (29).

Write \(L_0=(\lambda_{ij})_{1\le i,j\le3}\).  Substitution of the complete
families (22), (27), and (29) into degree six gives three parameter-free
coefficients:
\[
\boxed{
\begin{aligned}
[p^2r^4]E_6&=2\lambda_{33},\\
[pqr^4]E_6&=-4\lambda_{23},\\
[q^2r^4]E_6&=2\lambda_{13}.
\end{aligned}}
\tag{30}
\]
Thus \(E_6=0\) makes the entire third column of the translated linear part
zero, contradicting
\(\det L_0=\det JF(0)\ne0\).

### \(r^2\)-stratum theorem

There is no Keller map of total degree four whose leading part is
\[
H_4=r^2(p^2,pq,q^2)^T.
\tag{31}
\]

## 6. The second normal form \(h=r^2+p^2\)

Return to a general tangent cubic \(H_3=fA_p+gA_q\), with the coefficients
of \(f,g\) ordered by
\[
(p^2,pq,q^2,pr,qr,r^2)
\]
as \(a_0,\ldots,a_5\) and \(b_0,\ldots,b_5\).  The full degree-seven
\(H_2\)-coefficient matrix has rank twelve.  Seven specialization-safe
compatibilities, used successively, are
\[
\begin{gathered}
a_2^2=0,\\
a_4(a_1-b_2)=0,\qquad
(a_1-b_2)^2-a_4^2=0,\\
b_3(b_0-b_5)=0,\qquad
(b_0-b_5)^2-b_3^2=0,\\
(a_3-b_4)(a_0-a_5-b_1)=0,\\
(a_0-a_5-b_1)^2-(a_3-b_4)^2=0.
\end{gathered}
\tag{32}
\]
They force
\[
a_2=a_4=b_3=0,\quad b_2=a_1,\quad b_5=b_0,\quad
a_3=b_4,\quad a_0=a_5+b_1.
\tag{33}
\]
Substitution of (33) makes every remaining degree-seven compatibility
identically zero.  Put
\[
L=b_1p+a_1q,\qquad
\alpha=a_5,\quad\beta=b_0,\quad c=a_3.
\]
Then the exact degree-seven form is
\[
\boxed{
H_3=2(L+cr)A+(r^2+p^2)(\alpha A_p+\beta A_q).
}
\tag{34}
\]

Affine translations again remove the apparent tangent parameters.
Indeed,
\[
\begin{aligned}
\partial_pH_4&=2pA+(r^2+p^2)A_p,\\
\partial_qH_4&=(r^2+p^2)A_q,\\
\partial_rH_4&=2rA.
\end{aligned}
\tag{35}
\]
Translations in \(p,q,r\) with constants
\(-\alpha,-\beta,-c\), respectively, transform (34) to
\[
\boxed{H_3=2(xp+yq)A}
\tag{36}
\]
for a possibly changed binary linear form.

For (36), the complete degree-seven solution for \(H_2\) is
\[
\boxed{
H_2=
\begin{pmatrix}
(-u_4+2u_0)p^2+2u_1pq+2u_2pr\\
\frac{u_3}{2}p^2+u_0pq+u_1q^2+\frac{u_5}{2}pr+u_2qr\\
u_3pq+u_4q^2+u_5qr
\end{pmatrix}.
}
\tag{37}
\]
With an arbitrary row-major \(L_0=(\lambda_{ij})\), the nonzero degree-six
coefficients are scalar multiples of
\[
\lambda_{33},\quad\lambda_{23},\quad\lambda_{31},\quad
\lambda_{13},\quad2\lambda_{21}-\lambda_{32},\quad
\lambda_{11}-2\lambda_{22},\quad\lambda_{12}.
\tag{38}
\]
More explicitly, the first occurrences are
\[
\begin{array}{c|c}
p^6&4\lambda_{33}\\
p^5q&-8\lambda_{23}\\
p^5r&-2\lambda_{31}\\
p^4q^2&4\lambda_{13}\\
p^4qr&2(2\lambda_{21}-\lambda_{32})\\
p^3q^2r&-2(\lambda_{11}-2\lambda_{22})\\
p^2q^3r&-2\lambda_{12}.
\end{array}
\tag{39}
\]
In particular, \(\lambda_{13}=\lambda_{23}=\lambda_{33}=0\), so the third
column of \(L_0\) vanishes.

### \(r^2+p^2\)-stratum theorem

There is no Keller map of total degree four whose leading part is
\[
H_4=(r^2+p^2)(p^2,pq,q^2)^T.
\tag{40}
\]

## 7. The third normal form \(h=r^2+pq\)

For a general \(H_3=fA_p+gA_q\), the rank-twelve degree-seven
compatibility system has radical
\[
\boxed{
(b_0,\ b_3,\ a_2,\ a_4,\
 a_0-b_1+b_5,\ a_1-a_5-b_2,\ a_3-b_4).
}
\tag{41}
\]
A division-free forcing chain begins with
\[
b_0^2,\quad b_3^2,\quad a_2^2,\quad a_4^2.
\]
After those four vanish, put
\[
x=a_0-b_1+b_5,\quad y=a_1-a_5-b_2,\quad z=a_3-b_4.
\]
The remaining nonzero compatibilities reduce to
\[
x^2,\quad y^2,\quad zx,\quad zy,\quad2xy-z^2,
\tag{42}
\]
which force \(x=y=z=0\).  Conversely, every one of the fifteen raw
compatibilities vanishes under (41).

With
\[
L=(b_1-b_5)p+b_2q+b_4r,\qquad
\alpha=a_5,\quad\beta=b_5,
\]
the exact form is
\[
\boxed{H_3=2LA+(r^2+pq)(\alpha A_p+\beta A_q).}
\tag{43}
\]
The translation derivatives are
\[
\partial_pH_4=qA+hA_p,\qquad
\partial_qH_4=pA+hA_q,\qquad
\partial_rH_4=2rA.
\tag{44}
\]
Translations in \(p,q\) kill \(\alpha,\beta\), changing only the general
linear form \(L\).  Hence \(H_3=2(xp+yq+zr)A\).

The complete \(H_2\) solution is again (37).  A triangular subset of the
seventeen degree-six coefficients is
\[
\begin{array}{c|c}
p^4q^2&4\lambda_{33}\\
p^4qr&-2\lambda_{31}\\
p^3q^3&-8\lambda_{23}\\
p^3q^2r&2(2\lambda_{21}-\lambda_{32})\\
p^2q^4&4\lambda_{13}\\
p^2q^3r&-2(\lambda_{11}-2\lambda_{22})\\
pq^4r&-2\lambda_{12}.
\end{array}
\tag{45}
\]
Thus \(L_0\) has the singular form (53) below.

### \(r^2+pq\)-stratum theorem

There is no Keller map of total degree four whose leading part is
\[
H_4=(r^2+pq)(p^2,pq,q^2)^T.
\tag{46}
\]

## 8. The fourth normal form \(h=pr\)

The full degree-seven matrix in the eighteen coefficients of \(H_2\) again
has rank twelve.  Its thirteen nonzero compatibility quadrics have radical
\[
\boxed{
(b_0,\ a_0-b_1,\ a_1-b_2,\ a_2,\ a_4,\ a_5,\ b_5).
}
\tag{47}
\]
This radical is obtained without a generic-rank division: successive raw
compatibilities are
\[
b_0^2,\quad(a_0-b_1)^2,\quad
a_2^2,\quad a_5^2,\quad b_5^2,\quad
(a_1-b_2)^2,\quad 2a_2a_5+a_4^2.
\tag{48}
\]
After their forced vanishings, every remaining compatibility is zero.

Put
\[
L=a_0p+a_1q+b_4r,\qquad
\alpha=a_3-b_4,\qquad\beta=b_3.
\]
The exact degree-seven form becomes
\[
\boxed{H_3=2LA+pr(\alpha A_p+\beta A_q).}
\tag{49}
\]
Here
\[
\partial_pH_4=rA+prA_p,\qquad
\partial_qH_4=prA_q,\qquad
\partial_rH_4=pA.
\tag{50}
\]
Translations in \(p,q\) by \(-\alpha,-\beta\) kill the two tangent
parameters and only change \(L\).  Thus the affine-normalized cubic is
\[
\boxed{H_3=2(xp+yq+zr)A.}
\tag{51}
\]

The complete degree-seven solution for \(H_2\) is exactly (37).  Degree six
has only seven nonzero coefficients:
\[
\begin{array}{c|c}
p^5r&-\lambda_{31}\\
p^4qr&2\lambda_{21}-\lambda_{32}\\
p^4r^2&3\lambda_{33}\\
p^3q^2r&-\lambda_{11}+2\lambda_{22}\\
p^3qr^2&-6\lambda_{23}\\
p^2q^3r&-\lambda_{12}\\
p^2q^2r^2&3\lambda_{13}.
\end{array}
\tag{52}
\]
Their vanishing gives
\[
\boxed{
L_0=
\begin{pmatrix}
2\lambda_{22}&0&0\\
\lambda_{32}/2&\lambda_{22}&0\\
0&\lambda_{32}&0
\end{pmatrix},
}
\tag{53}
\]
which is singular.

### \(pr\)-stratum theorem

There is no Keller map of total degree four whose leading part is
\[
H_4=pr(p^2,pq,q^2)^T.
\tag{54}
\]

## 9. The fifth normal form \(h=pr+q^2\)

The degree-seven matrix still has rank twelve.  This time its compatibility
radical is
\[
\boxed{
(b_0,\ a_0-b_1,\ a_1-b_2+b_3,\ a_2-a_3+b_4,\
 a_4,\ a_5,\ b_5).
}
\tag{55}
\]
Indeed \(b_0^2,a_5^2,b_5^2\) first kill those three entries; the residual
system contains \((a_0-b_1)^2\) and \(3a_4^2\).  After those vanish, its
only nontrivial equations are
\[
x^2,\quad-xy,\quad y^2,\qquad
x=a_1-b_2+b_3,\quad y=a_2-a_3+b_4.
\tag{56}
\]
Conversely, (55) kills all seventeen raw compatibilities.

Put
\[
L=a_0p+a_1q+(a_3-a_2)r,\qquad
\alpha=a_2,\quad\beta=b_3.
\]
Then
\[
\boxed{H_3=2LA+(pr+q^2)(\alpha A_p+\beta A_q).}
\tag{57}
\]
The relevant translation derivatives are
\[
\partial_pH_4=rA+hA_p,\qquad
\partial_qH_4=2qA+hA_q,\qquad
\partial_rH_4=pA.
\tag{58}
\]
Translations in \(p,q\) kill \(\alpha,\beta\), again leaving a general
radial cubic \(H_3=2(xp+yq+zr)A\).

The degree-seven \(H_2\) family is (37).  Degree six has thirteen nonzero
terms, and the following ordered subset is triangular:
\[
\begin{array}{c|c}
p^5r&-\lambda_{31}\\
p^4qr&2\lambda_{21}-\lambda_{32}\\
p^4r^2&3\lambda_{33}\\
p^3qr^2&-6\lambda_{23}\\
p^2q^2r^2&3\lambda_{13}\\
p^3q^2r&-\lambda_{11}+2\lambda_{22}+7\lambda_{33}\\
p^2q^3r&-\lambda_{12}-14\lambda_{23}.
\end{array}
\tag{59}
\]
It again gives exactly (53).

### \(pr+q^2\)-stratum theorem

There is no Keller map of total degree four whose leading part is
\[
H_4=(pr+q^2)(p^2,pq,q^2)^T.
\tag{60}
\]

## 10. Combined fixed-conic theorem

Under the relative parabolic group preserving
\(W=\langle p,q\rangle\), write
\[
h=ar^2+r\ell(p,q)+b(p,q).
\]
If \(a\ne0\), completing the square in \(r\) and classifying the rank of
the residual binary quadratic gives
\[
r^2,\quad r^2+p^2,\quad r^2+pq.
\]
If \(a=0\) but \(\ell\ne0\), normalize \(\ell=p\), absorb the
\(p^2,pq\) terms into \(r\), and obtain
\[
pr,\quad pr+q^2.
\]
If \(a=\ell=0\), the binary forms are \(p^2,pq\).  These seven normal forms
are exhaustive over \(\mathbb C\), and every transformation used is an
invertible source-linear change with the induced Veronese target change.

Sections 5--9 exclude the five nonbinary forms.  The companion
`WORKING_FIXED_CONIC_ROW.md` excludes the two binary forms.  Therefore:

### Complete fixed-divisor conic theorem

Let a total-degree-four polynomial map have leading part
\[
H_4=h(p,q,r)(p^2,pq,q^2)^T
\]
for a nonzero quadratic \(h\).  If the map is Keller, then it is a
polynomial automorphism.  Equivalently, no degree-four Keller
counterexample lies anywhere in the complete taxonomy row
\[
\boxed{(e,a,b,\delta,\nu)=(2,1,2,2,1).}
\tag{61}
\]

## 11. Verification boundary and disclosure

`verify_nonbinary_fixed_conic_sympy.py` checks (5), the kernel identity,
(9), the scalar differential reduction before dehomogenization, the full
normal-term congruence (20), the exact degree-seven solution (22)--(24),
the full kernel family (29), the degree-six exit (30), the raw
\(r^2+p^2\) degree-seven rank and compatibility system, the normalized
solution (37), the degree-six coefficients (39), the three remaining raw
compatibility radicals (41), (47), (55), and their triangular degree-six
exits.
`verify_nonbinary_fixed_conic_pari.gp` independently expands the same
adjugate and the normalized degree-seven and degree-six identities.

The logarithmic-residue argument in Section 3 and the orbit classification
(16) are mathematical inputs, not computer checks.  The first adversarial
audit independently confirmed those arguments and the raw degree-seven
calculation.  It also caught and removed a false claim that a matrix modulus
survived affine equivalence: translations in \(r\) add a scalar matrix, and
translations in \(p,q\) give exactly the normalization (27).  The corrected
\(r^2\) degree-six exit is retained as an exact regression and passed a
focused second audit.  A separate raw-system audit of \(r^2+p^2\)
reconstructed the rank-twelve compatibility radical, affine translation
signs, full six-parameter \(H_2\) solution, and all seventeen degree-six
coefficients.  It found no missing specialization or algebraic correction.
Further independent raw solves reproduced the last three radicals,
translation normalizations, complete \(H_2\) kernels, and division-free
triangular exits.  A final combined audit independently reconstructed the
seven parabolic normal forms, the three remaining raw compatibility
radicals and their converses, every affine translation sign, the reused
six-parameter \(H_2\) kernel, and all four triangular degree-six tables.
It confirmed both the exhaustion and the precise theorem scope.

The two implementations are exact evidence about the encoded algebra, not
peer review.  This note was developed with AI assistance and has not been
peer reviewed.
