# Exact exclusion of frozen family `D3-BS-N1-CONTACT`

**Date:** 2026-07-26  
**Scope:** one frozen family in `Q2-E2-A1-B2-D1-N2`  
**Status:** exact full-family counterexample exclusion; no registry, ledger,
or global-row status is changed here.

## Result

There is no quartic Keller counterexample in the frozen family
\[
h=p^2,\qquad R=p(p^2+q^2),\qquad
H_4=(p^4,p^2q^2,0),\qquad (H_3)_3=R.
\]
All binary cubic and quadratic lower summands and all nine entries of the
linear part are retained.  Every nonzero \(E_7\) tangent is contradicted by
\(E_5,E_4\), or \(E_3\), or forces \(\det L=0\).  The \(E_7\)-origin contains
only the standard binary/coordinate structural exits, hence no
counterexample.  No BCW reduction is used.

The full exact replay is `verify_family_exclusion.py`; its terminal marker is

```text
D3_BS_N1_CONTACT_FULL_FAMILY_EXCLUSION_PASS
```

## Full \(E_7\) parameterization

Write
\[
\begin{aligned}
U_0&=u_0p^3+u_1p^2q+u_2pq^2+u_3q^3,\\
V_0&=v_0p^3+v_1p^2q+v_2pq^2+v_3q^3,\\
T_0&=t_0p^2+t_1pq+t_2q^2.
\end{aligned}
\]
The complete degree-one and degree-two syzygy bases of the \(E_7\)
equation are
\[
(0,p,1)
\]
and
\[
(4p^2,-3p^2+q^2,0),\quad(0,p^2,p),\quad(0,pq,q).
\]
Consequently every \(E_7\) solution is
\[
\begin{aligned}
U&=U_0+4y_0p^2r,\\
V&=V_0+r\bigl((-3y_0+y_1)p^2+y_2pq+y_0q^2\bigr)
{x\over2}pr^2,\\
T&=T_0+r(y_1p+y_2q)+{x\over2}r^2.
\end{aligned}
\]
Direct expansion verifies \(E_9=E_8=E_7=0\), with no omitted
highest-\(r\) term.

## Complete \(E_6\) compatibility

Put
\[
C=4t_1-3u_1-4v_1.
\]
Six division-free ordinary pivots leave exactly
\[
\begin{gathered}
(3y_0-y_1)C,\qquad xC,\qquad
x(-u_1+9u_3+12v_3)+16y_0y_2,\\
xy_0,\qquad u_3y_2,\qquad u_3x,\qquad u_3y_0.
\end{gathered}
\tag{1}
\]
This gives the exhaustive top split:

- \(y_0\ne0\): \(x=y_2=u_3=0\), and either \(y_1=3y_0\) or \(C=0\);
- \(y_0=0,\ x\ne0\);
- \(y_0=x=0,\ (y_1,y_2)\ne(0,0)\);
- \(x=y_0=y_1=y_2=0\), the \(E_7\)-origin.

The source change \(r\mapsto r/s\) normalizes any displayed nonzero tangent
scale without changing the frozen binary leading data and scales
\(\det L\) by a nonzero scalar.  On the \(x\ne0\) component, the additional
shear \(r\mapsto r-y_1p-y_2q\) sets \(y_1=y_2=0\) and only changes the
arbitrary binary summands.  Thus the following charts are exhaustive.

## Exact nonzero-tangent descent

### The \(x\)-chart

Normalize \(x=1,y_0=y_1=y_2=0\).  Equation (1) gives
\[
u_3=0,\qquad u_1=12v_3,\qquad t_1=9v_3+v_1.
\]
After the complete \(E_6\) solve,
\[
[p^2r^3]E_5=-6v_3.
\]
Thus \(v_3=0\).  The remaining \(E_5\) system is consistent, but the complete
\(E_4\) solve gives
\[
\ell_1=\ell_7u_2,\qquad
\ell_4=\ell_7(v_2-t_2),
\]
together with
\[
\ell_2=\ell_8u_2,\qquad
\ell_5=\ell_8(v_2-t_2),
\]
and hence \(\det L=0\).

### The \(y_2\)-chart

Normalize \(y_2=1,x=y_0=y_1=0\).  The complete \(E_5\) residual contains
\[
{C\over2},\qquad {u_1-36v_3\over2}.
\]
After \(C=0,u_1=36v_3\), two \(E_4\) coefficients are
\[
[pqr^2]E_4=12v_3,\qquad [q^3r]E_4=-144v_3^2.
\]
Thus \(v_3=0\), and the remaining \(E_4\) equations give the same two
column relations as in the \(x\)-chart, so \(\det L=0\).

### The \(y_1\)-chart

Normalize \(y_1=1,x=y_0=y_2=0\).  The complete \(E_5\) residual forces
\[
u_3=0,\qquad u_1=4v_3,\qquad t_1=3v_3+v_1.
\]
If \(v_3\ne0\), the complete \(E_4\) pivots leave
\[
[p^2r]E_3=[q^2r]E_3=-12v_3^3,
\]
a contradiction.

If \(v_3=0\), put \(d=t_2-\ell_8\).  On \(d\ne0\), \(E_4\) forces
\[
\ell_2=\ell_8u_2,\qquad \ell_5=\ell_8(v_2-t_2),
\]
and then \(\det L=0\).  On \(d=0\), put
\[
g=-\ell_7+\ell_8v_1.
\]
The two relevant \(E_3\) coefficients have common factor \(g\), and
\[
g\mid\det L.
\]
If \(g=0\), the linear part is singular.  If \(g\ne0\), the two cofactors
force
\[
\ell_2=\ell_8u_2,\qquad
\ell_5=\ell_8(v_2-\ell_8),
\]
which kills the quotient \((\det L)/g\).  Thus this boundary is also
exhausted.

### Mixed \(y_1,y_2\)-chart

Normalize \(y_1=1,y_2=s\ne0\).  The complete \(E_5\) residual contains
\[
-{3\over2}(u_1-4v_3),\qquad -s(u_1+12v_3),
\]
so \(u_1=v_3=0\).  On the generic pivot chart \(3s^2\ne1\),
\[
[p^3r]E_4=
{12s\over3s^2-1}\bigl(\ell_5+\ell_8(t_2-v_2)\bigr).
\]
After this factor vanishes, the remaining \(E_4\) equations force
\(\det L=0\).

The omitted divisor \(3s^2=1\) is checked in the exact quadratic field
\(\mathbb Q(\sqrt3)\).  A fresh pivot gives
\[
[p^3r]E_4=3\sqrt3\,(-\ell_2+\ell_8u_2),
\]
and the remaining \(E_4\) equations again force \(\det L=0\).  One field
calculation covers both conjugate roots.

### The \(y_0\)-component

Normalize \(y_0=1\) and put \(m=y_1\).  For \(m\ne3\), (1) gives \(C=0\).
The full \(E_5\) coefficient matrix has rank six, while the displayed
augmented minor is
\[
98304(m-3)\ne0.
\]
Thus this localized system is inconsistent.

At the only omitted value \(m=3\), \(C\) is unrestricted.  A fresh \(E_5\)
matrix has rank five and an augmented minor equal to
\[
12288\ne0.
\]
Hence the entire \(y_0\ne0\) component is impossible.

## The \(E_7\)-origin

At \(x=y_0=y_1=y_2=0\), the complete \(E_6\) solution is
\[
A_r=0,\qquad B_r=\ell_8p.
\]
If \(\ell_8=0\), every nonlinear term is binary; an invertible target-linear
change exhibits a triangular extension of a plane Keller map of degree at
most four, hence an automorphism.

If \(\ell_8\ne0\), then
\[
F_3=\ell_8r+B_3(p,q)
\]
is a coordinate with inverse degree at most three.  Straightening it gives
plane Keller fibres of degree at most \(3\cdot4=12<100\); the unconditional
plane bounded-degree theorem and the fibrewise injectivity/Ax argument make
the map an automorphism.  Therefore the origin contains Keller
automorphisms only, not a counterexample.

No nonzero branch reaches \(E_2\) or \(E_1\): every such branch is already
inconsistent or has singular linear part at \(E_5,E_4\), or \(E_3\).
