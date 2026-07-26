# Exact exclusion of the six marked-distinct \(CH/CS\) endpoints

## Scope

This note independently continues the six released endpoint normal forms
past \(E_6\).  It excludes:

```text
MD-P21-HR2-CH       MD-P21-HR2-CS
MD-P21-HSM-CH       MD-P21-HSM-CS
MD-P3-HSM-CH        MD-P3-HSM-CS
```

Five endpoints force the linear part to be singular at \(E_5\).
`MD-P3-HSM-CH` has a genuine invertible family through \(E_5\); it is
excluded by two coefficients of \(E_4\).  Consequently an argument claiming
that all six die at \(E_5\) is false.

This does not address the three `C0` strata or the two outer `CO` strata.
Together with `NOTE.md`, the present package excludes eight of the thirteen
frozen marked-distinct internal strata: the six endpoints, `CT`, and the
parameterized `CTAU` stratum.

The result uses substantial AI assistance, is not peer reviewed, and claims
no global quartic-row closure or degree-bound improvement.

## 1. Common setup

Write
\[
F=F_0+LX+H_2+H_3+H_4,\qquad
L=(\ell_{ij})=
\begin{pmatrix}
\ell_0&\ell_1&\ell_2\\
\ell_3&\ell_4&\ell_5\\
\ell_6&\ell_7&\ell_8
\end{pmatrix}.
\]
As in the released normal forms, the first two components of \(H_2\) are
arbitrary quadratics in the monomial order
\((x^2,xy,xz,y^2,yz,z^2)\), with coefficients \(a_i,b_i\).

Put
\[
E_j=[w^j]\det\left(L+wJH_2+w^2JH_3+w^3JH_4\right).
\]
The released calculations give complete \(E_7\) normal forms and
constant \(E_6\) pivots.  Their field-valued \(E_6\) radicals are:

\[
\begin{array}{c|c}
\text{endpoint type}&\sqrt{I_6}\\ \hline
\mathrm{P21/CH}&E=F=0,\quad A(C,D)=0\\
\mathrm{P21/CS}&C=D=0\\
\mathrm{P3/CH}&E=F=0,\quad A(C,D)=0\\
\mathrm{P3/CS}&D=0.
\end{array}
\]

Every component of these radicals is treated below.  No division by a
normal parameter is used.

## 2. The two rank-two-pencil \(CS\) endpoints

For \(h=yz\) and \(h=x^2+yz\), the \(C=D=0\) normal form is
\[
H_3=(Axyz,Bxyz,x^3),\qquad (H_2)_3=Tyz.
\]
Solving \(E_6\) with the released constant pivot forces
\[
a_1=a_2=a_3=a_5=b_1=b_2=b_3=b_5=\ell_7=\ell_8=0.
\]
The coefficients
\[
[x^2y^2z]E_5=-6\ell_4,\qquad
[x^2yz^2]E_5=6\ell_5
\]
give \(\ell_4=\ell_5=0\).  The two \(x^4y,x^4z\) coefficients then give
\(\ell_1=\ell_2=0\).  Hence columns two and three of \(L\) vanish.

## 3. The two rank-two-pencil \(CH\) endpoints

After \(E=F=0\), the complete normal form is
\[
\begin{aligned}
U&=Ax^3-2Cyh-2Dzh,\\
V&=Bx^3+Cx^2y+Dx^2z,\qquad
W=Tx^2,\qquad R=xh.
\end{aligned}
\]

On the \(A=0\) component of \(A(C,D)=0\), exact \(E_6\) elimination gives
\[
[x^2y^3]E_5=-12C^3,\qquad
[x^2z^3]E_5=12D^3.
\]
Thus \(C=D=0\).

On the \(C=D=0\) component, four \(E_5\) equations give
\[
\ell_4=\ell_5=0,\qquad
\ell_1=(6B-8T)\ell_7,\qquad
\ell_2=(6B-8T)\ell_8.
\]
The \(2\times2\) submatrix in rows one and three and columns two and three
has proportional rows, while row two vanishes in those columns.  Therefore
\(\det L=0\), independently of \(A\).

## 4. The rank-one-pencil \(CS\) endpoint

Put \(h=y^2+xz\).  On the \(D=0\) radical, the normal form is
\[
\begin{aligned}
U&=2Azh,\\
V&=Ax^2z+Bxh+\frac23Cyh,\\
W&=Cxy+Sh,\qquad R=x^3.
\end{aligned}
\]
After the constant-pivot \(E_6\) solution,
\[
[x^2z^3]E_5=-\frac29C^3,
\]
so \(C=0\).  The remaining displayed consequences are
\[
\ell_1=0,\qquad \ell_2=Aa_3,\qquad
\ell_4=0,\qquad \ell_5=Ab_3.
\]
The \(E_6\) solution also has \(\ell_7=-BC/2=0\).  Thus the second column
of \(L\) vanishes and \(\det L=0\).

## 5. The rank-one-pencil \(CH\) endpoint

After \(E=F=0\), write
\[
\begin{aligned}
U&=Ax^3-2Cyh-2Dzh+2Tzh,\\
V&=Bx^3+Cx^2y+(D+T)x^2z,\\
W&=Txz,\qquad R=xh.
\end{aligned}
\]

### 5.1 Reduction to \(C=D=0\)

On the \(A=0\) component, put \(q=a_0-9B^2\).  Three consequences of
\(E_5=0\) are
\[
Cq=0,\qquad Dq+6BC^2=0,\qquad C(6BD-C^2)=0.
\]
If \(C\ne0\), the first gives \(q=0\), the second gives \(B=0\), and the
third gives \(C^3=0\), a contradiction.  Hence \(C=0\).

With \(C=0\), three further coefficients are
\[
\begin{aligned}
(D-T)b_3+\ell_5&=0,\\
(D-T)b_3-2D\ell_8+\ell_5&=0,\\
6D^3+(D-T)b_3-4D\ell_8+\ell_5&=0.
\end{aligned}
\]
They give \(D\ell_8=0\) and then \(D^3=0\), so \(D=0\).

### 5.2 The genuine through-\(E_5\) survivor

On \(C=D=0\), the \(E_5\) equations relevant to invertibility are
\[
\begin{gathered}
A\ell_7=A\ell_8=0,\qquad
\ell_1=6B\ell_7,\qquad
\ell_2=6B\ell_8+Ta_3,\\
\ell_4=0,\qquad \ell_5=Tb_3.
\end{gathered}
\]
They leave
\[
\det L=
T\ell_7\bigl(6Bb_3\ell_6+a_3\ell_3-b_3\ell_0\bigr).       \tag{1}
\]
Thus \(A\ne0\) is excluded, but \(A=0\) genuinely survives \(E_5\).

On that survivor, two exact \(E_4\) coefficients are
\[
\begin{aligned}
[xyz^2]E_4&=-8\ell_8^2,\\
[x^2yz]E_4&=-4\left(2(b_0-\ell_6)\ell_8-\ell_7^2\right).
\end{aligned}
\]
The first gives \(\ell_8=0\); the second then gives \(\ell_7=0\).
Equation (1) yields \(\det L=0\).

### 5.3 Sharpness witness

The necessity of \(E_4\) is certified by
\[
\begin{aligned}
h&=y^2+xz,\\
H_4&=(h^2,hx^2,0),\\
H_3&=(2zh,x^2z,xh),\\
H_2&=(z^2,\,2xy+xz+y^2,\,xz),\\
L&=\begin{pmatrix}1&0&0\\0&0&1\\0&1&0\end{pmatrix}.
\end{aligned}
\]
Here \(\det L=-1\) and \(E_9=\cdots=E_5=0\), while
\[
E_4=4xy(xz+y^2)\ne0.
\]

## 6. Verification

`derive_six_endpoints_e5_e4_sympy.py` reconstructs every constant-pivot
\(E_6\) solution and the decisive lower identities.  The separate
`verify_six_endpoints_e5_e4_pari.gp` reconstructs the determinants and
the sharpness witness independently.  Both are required by
`verify_strict.sh`.
