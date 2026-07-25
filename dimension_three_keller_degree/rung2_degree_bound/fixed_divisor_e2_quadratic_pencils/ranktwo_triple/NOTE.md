# The rank-two triple-companion exit

## Status

**Exact audited theorem.**  The corrected SymPy certificate and a
methodologically independent PARI/GP reconstruction both pass, together
with fail-closed injection tests.

This note is not peer reviewed.  Exact computer checks certify the encoded
algebra, not the mathematical exposition or worldwide priority.  AI systems
assisted with symbolic exploration, case organization, proof drafting, and
verification code.

## Theorem

Let \(K\) be a field of characteristic zero and write
\[
F=LX+H_2+H_3+H_4
\]
with \(H_j\) homogeneous of degree \(j\).  Suppose that, after linear source
and target changes,
\[
H_4=(x^4,x^2yz,0),\qquad (H_3)_3=x^3.
\tag{1}
\]
Then \(\det JF\) cannot be a nonzero constant.

Thus the triple cubic companion is excluded for the rank-two canonical
fixed-divisor pencil
\[
H_4=(p^2,pq,0),\qquad
\langle p,q\rangle=\langle x^2,yz\rangle.
\tag{2}
\]
Together with the separately audited mixed-companion package, this
close the rank-two half of the fixed-divisor \(e=2\) lower frontier.  It does
not address the rank-one pencil \(\langle x^2,y^2+xz\rangle\).

## Weighted identities and the complete top kernel

Put
\[
\mathcal J(s)=L+sJH_2+s^2JH_3+s^3JH_4,\qquad
E_j=[s^j]\det\mathcal J(s).
\]
The Keller condition requires
\[
E_1=\cdots=E_9=0,\qquad \det L\ne0.
\tag{3}
\]

The raw \(E_7\) coefficient matrix has size \(36\times26\), rank \(8\),
and nullity \(18\).  Five directions are legal gauges: two target shears
by \(x^3\), and three source translations.  A complete thirteen-parameter
normal complement gives
\[
\begin{aligned}
U={}&Axyz+\frac43\left(
w_1x^2y+w_2x^2z+w_3xy^2+w_5xz^2
\right),\\
V={}&B_1xy^2+B_2xyz+B_3xz^2+B_4y^3+B_5y^2z
+B_6yz^2+B_7z^3,\\
W={}&w_1xy+w_2xz+w_3y^2+w_4yz+w_5z^2,
\end{aligned}
\tag{4}
\]
where \(H_3=(U,V,x^3)\) and \((H_2)_3=W\).

The fractions in (4) follow directly from the \(y/z\)-weight equation
\[
3(yU_y-zU_z)-4x(yW_y-zW_z)=0.
\tag{5}
\]

## The degree-six split

Two square compatibility equations in \(E_6\) give
\[
w_3=w_5=0.
\tag{6}
\]
Set
\[
K=9A-12w_4,\qquad M=-3A+8w_4.
\tag{7}
\]
The remaining compatibility equations are exactly
\[
KB_4=KB_7=0,\qquad
KB_5+Mw_1=KB_6+Mw_2=0.
\tag{8}
\]

### Case 1: \(K\ne0\)

Equations (8) eliminate \(B_4,B_7,B_5,B_6\).  Reparametrize
\[
w_4=\frac{9A-K}{12}.
\]
The exact \(E_5\) left kernel gives, for \(i=1,2\), the paired equations
\[
\begin{aligned}
w_i(3C_iK+4w_i^2)&=0,\\
-C_i(9A-2K)(9A-K)+4Kw_i^2&=0,
\end{aligned}
\tag{9}
\]
where \(C_1=B_1,C_2=B_3\), together with
\[
Aw_i(9A-2K)(9A-K)=0.
\tag{10}
\]
If \(w_i\ne0\), eliminating \(C_i\) from (9) gives
\[
81A^2-27AK+5K^2=0.
\tag{11}
\]
Equation (10) leaves \(A=0\), \(9A=2K\), or \(9A=K\).  The left side of
(11) is respectively \(5K^2,3K^2,3K^2\), impossible because \(K\ne0\).
Hence
\[
w_1=w_2=0.
\tag{12}
\]

Put \(S=(9A-2K)(9A-K)\).  The remaining equations are
\(SB_1=SB_3=0\).

If \(S\ne0\), then \(B_1=B_3=0\), and the surviving form is aligned:
\[
U=Axyz,\qquad V=B_2xyz,\qquad W=w_4yz.
\tag{13}
\]
Since \(-3A+4w_4=-K/3\ne0\), the complete \(E_5\) solve makes the last
two entries of the third row of \(L\) zero.  A fixed pivot for this solve
is proportional to
\[
(3A-8w_4)^2(3A-4w_4)^4,
\]
which is nonzero on the \(S\ne0\) chart.  Two \(E_4\) coefficients have
the form
\[
\begin{aligned}
D^2\ell_{22}+T\ell_{12}&=0,\\
D^2\ell_{23}+T\ell_{13}&=0,
\end{aligned}
\qquad D=-3A+4w_4\ne0,
\tag{14}
\]
with the same scalar \(T\).  Thus
\(\ell_{12}\ell_{23}-\ell_{13}\ell_{22}=0\), and \(\det L=0\).

There are two resonances.

- If \(9A=2K\), then \(A\ne0\) and \(w_4=3A/8\).  If
  \((B_1,B_3)\ne(0,0)\), the involution \(y\leftrightarrow z\) lets us
  take \(B_3\ne0\).  On that chart the complete \(E_6,E_5\) solve has
  \[
  [z^4]E_4=\frac38A^2B_3^2,
  \]
  a contradiction.  The zero pair is aligned, but it is not covered
  by the preceding generic aligned solve: its \(E_5\) pivot contains
  \((3A-8w_4)^2\), which vanishes here.  A fresh solve at
  \(B_1=B_3=0,\ w_4=3A/8\) has \(E_5\)-rank \(4\).  Two square
  coefficients are
  \[
  [x^2y^2]E_4=-\frac43\ell_{32}^2,\qquad
  [x^2z^2]E_4=\frac43\ell_{33}^2,
  \]
  so \(\ell_{32}=\ell_{33}=0\).  The remaining \(x^3y,x^3z\)
  equations have the form
  \[
  T\ell_{12}-\frac32A\ell_{22}=0,\qquad
  -T\ell_{13}+\frac32A\ell_{23}=0
  \]
  with the same scalar \(T\).  Since \(A\ne0\), they force
  \(\ell_{12}\ell_{23}-\ell_{13}\ell_{22}=0\); the third row of
  \(L\) is now \((\ell_{31},0,0)\), and hence \(\det L=0\).
- If \(9A=K\), then \(A\ne0\) and \(w_4=0\).  On the same
  \(B_3\ne0\) chart, \(E_5\) again zeros the last two entries of the
  third row of \(L\), while two \(E_4\) equations are
  \[
  AB_3\ell_{22}-b_5\ell_{12}=0,\qquad
  AB_3\ell_{23}-b_5\ell_{13}=0.
  \]
  They force the same \(2\times2\) minor, hence \(\det L\), to vanish.
  If \((B_1,B_3)=(0,0)\), the form is aligned and the aligned pivot
  above is nonzero because both \(3A-8w_4\) and \(3A-4w_4\) equal
  \(3A\).

### Case 2: \(K=0,\ A\ne0\)

Now \(w_4=3A/4\), and (8) gives \(w_1=w_2=0\).  Six literal
\(E_5\) compatibility equations are nonzero scalar multiples of
\[
A^2B_1,\ A^2B_3,\ A^2B_4,\ A^2B_5,\ A^2B_6,\ A^2B_7.
\tag{15}
\]
Only \(B_2\) remains.  The fresh aligned solve at \(K=0\) must be done
separately: \(E_5\) gives
\[
\ell_{12}=\ell_{13}=\ell_{32}=\ell_{33}=0,
\]
so \(\det L=0\).

### Case 3: \(K=A=0\)

Here \(w_4=0\).  Suppose first that \((w_1,w_2)\ne(0,0)\).  By the
\(y/z\) involution take \(w_1=s\ne0\) and write \(w_2=rs\).  Three
cross-multiplied polynomial \(E_5\) syzygies necessarily give
\[
\begin{aligned}
B_5&=3B_4r+\frac23s,\\
B_6&=3B_4r^2+\frac23rs,\\
B_7&=B_4r^3.
\end{aligned}
\tag{16}
\]
If \(B_4rs\ne0\), the complete localized solve yields the literal
coefficient
\[
[y^4]E_4=\frac4{27}s^4,
\]
impossible.  On the rank-drop chart \(B_4=0\), a division-free
\(E_5\) left relation has right side \(-4s^3/9\), again impossible.

The chart \(r=0\) requires one further split.  If \(B_3\ne0\), the
\(E_5\) matrix has the explicit pivot \(-96B_3s^2\), and its localized
left relation has right side \(-4s^3/9\).  This relation cannot be
specialized to \(B_3=0\).  On the fresh chart
\(r=0,\ B_4\ne0,\ B_3=0\), the \(E_5\) matrix instead has rank \(4\)
with pivot \(144B_4s^2\) and no compatibility obstruction.  After its
complete solve, the literal coefficient is
\[
[y^4]E_4=\frac4{27}s^4,
\]
which is impossible.  Thus \(w_1=w_2=0\).

Finally \(U=W=0\) and \(V\) is arbitrary in its seven displayed
monomials.  A generic \(E_5\) pivot is proportional to \(B_1\), so it
cannot be specialized globally.  Instead, after the constant
\(E_6\) solve, two literal coefficients are
\[
[x^4y]E_5=3\ell_{12},\qquad
[x^4z]E_5=-3\ell_{13},
\]
and hence \(\ell_{12}=\ell_{13}=0\) on every chart.  The six remaining
nonzero \(E_5\) rows are
\[
-6B_1a_4,\quad 6B_3a_4,\quad -9B_4a_4,\quad
-3B_5a_4,\quad 3B_6a_4,\quad 9B_7a_4.                \tag{17}
\]

If \(a_4=0\), two literal \(E_4\) coefficients are
\[
[x^2y^2]E_4=-\frac43\ell_{32}^2,\qquad
[x^2z^2]E_4=\frac43\ell_{33}^2.
\tag{18}
\]
If \(a_4\ne0\), (17) kills
\(B_1,B_3,B_4,B_5,B_6,B_7\), leaving only \(V=B_2xyz\).  On that
fresh leaf,
\[
[xy^2z]E_4=2a_4\ell_{32},\qquad
[xyz^2]E_4=-2a_4\ell_{33}.                            \tag{19}
\]
Thus in both cases \(\ell_{32}=\ell_{33}=0\), so \(\det L=0\).

Every branch contradicts (3), proving the theorem.
