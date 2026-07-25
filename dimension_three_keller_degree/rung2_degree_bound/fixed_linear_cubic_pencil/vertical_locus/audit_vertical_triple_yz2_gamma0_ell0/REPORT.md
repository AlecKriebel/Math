# Hostile audit: the vertical \(x^3+yz^2\) chart

**Verdict:** **PASS**, only for
\[
q=x^3+yz^2,\qquad s\ne0,\qquad W=wz^2.
\]

**Completed (UTC):** 2026-07-25T21:15:54Z.

`../VERTICAL_TRIPLE_YZ2_GAMMA0_ELL0_LEMMA.md` correctly excludes this
single zero-\(\gamma\), zero-\(\ell\) chart.  I found no illegal gauge,
unrecorded chart modulus, hidden division, missing determinant equation,
or internal rank divisor.

This verdict does **not** extend to either other minimal triple-root
chart, \(W_0\ne0\), \(\ell\ne0\), or \(s=0\).  It does not close the
frozen row `Q2-E1-A3-B1-D1-N1`.

## 1. Independent chart and boundary audit

After normalizing the triple root to \(x\), the general marked cubic is
\[
q=x^3+z(Ax^2+Bxy+Cy^2)+z^2(Dx+Ey)+Fz^3.              \tag{1}
\]
The full parabolic preserving \(z=0\) and its marked triple root has
\[
x\mapsto ax+uz,\qquad
y\mapsto by+cx+vz,\qquad
z\mapsto dz,\qquad abd\ne0.                           \tag{2}
\]
The chart under audit is exactly
\[
C=B=0,\qquad E\ne0.                                   \tag{3}
\]
To see its normal form without using the candidate proof, first translate
\(x\) by a multiple of \(z\) to kill \(A\).  The resulting polynomial is
\[
x^3+z^2(D'x+Ey)+F'z^3.
\]
The \(x\)- and \(z\)-parts of the \(y\)-shear in (2) independently kill
\(D'\) and \(F'\).  Finally a nonzero scaling of \(y\) normalizes \(E\)
to one.  This gives
\[
q=x^3+yz^2                                             \tag{4}
\]
with no retained modulus.  The only chart coefficient divided by in this
normalization is \(E\), whose nonvanishing defines (3).

The adjacent conditions are genuinely different:

- \(C\ne0\) gives the \(x^3+y^2z+\alpha xz^2+\beta z^3\) chart;
- \(C=0,B\ne0\) gives the \(x^3+xyz+\beta z^3\) chart;
- \(C=B=E=0\) is binary in \(x,z\), hence lies on the nonminimal
  boundary.

Moreover, (4) is minimal: if \((z^3,q)\) were nonminimal, then
\(q\in\operatorname{Sym}^3\langle z,L\rangle\) for one linear form
\(L\).  Its restriction \(q|_{z=0}=x^3\) forces
\(L\bmod z\) to be proportional to \(x\), which cannot produce the
\(yz^2\) term.

On the triple-root branch, the plane restriction of the degree-six
identity permits
\[
W_0=\gamma x^2.
\]
The audited boundary is \(\gamma=0\), so
\[
W=z(\ell_xx+\ell_yy+wz).
\]
Its further condition \(\ell=0\) is exactly \(W=wz^2\), including
\(w=0\).  Every source transformation used above preserves \(z\) up to
scale, so it preserves this condition and only rescales the unrestricted
coefficient \(w\).

The coefficient \(s\) is the nonzero coefficient \(a\) in the
vertical-companion \(E_7\) family
\[
U=\frac43zW+a q+bz^3.                                 \tag{5}
\]
Thus \(s\ne0\) is the existing \(a\ne0\) branch, not an extra genericity
condition.  The target shear
\(F_1\mapsto F_1-bF_3\) kills the last term of (5), changing
\((A,L_1)\) by multiples of \((W,L_3)\).  A second shear
\(F_2\mapsto F_2-cF_3\) kills \(c=[z^3]V\), changing
\((B,L_2)\) by multiples of \((W,L_3)\).  Since \(A,B,L_1,L_2\) were
unrestricted, these are legal renamings; in particular they only rename
the free \(z^2\)-coefficients of \(A,B\).  The third row of \(H_4\) is
zero, so both shears preserve
\[
H_4=(z^4,zq,0)^T.
\]

There is one wording correction to the candidate note: the first shear
kills the independent summand \(bz^3\), not the literal total
\(z^3\)-coefficient of \(U\).  When \(W=wz^2\), the constrained term
\(\frac43zW=\frac43wz^3\) remains.  The displayed normal form, proof,
and all verifiers use the correct interpretation, so this does not affect
the theorem.

## 2. Independent raw determinant and \(E_6\)

The audit checker constructs
\[
\det(L+JH_2+JH_3+JH_4)
\]
from sparse polynomial arithmetic.  With
\[
\begin{aligned}
H_2&=(A,B,wz^2)^T,\\
H_3&=\left(\frac43wz^3+s(x^3+yz^2),V,z^3\right)^T,\\
H_4&=(z^4,z(x^3+yz^2),0)^T,
\end{aligned}                                         \tag{6}
\]
it first confirms \(E_8=E_7=0\) identically.

Let \(v_0,\ldots,v_8\) be the coefficients of \(V\) on
\[
x^3,x^2y,xy^2,y^3,x^2z,xyz,y^2z,xz^2,yz^2
\]
and set \(\lambda=\ell_{31}\), \(\mu=\ell_{32}\).  Every \(E_6\)
equation is jointly linear in these eleven variables.

Without receiving a row or column list from either supplied verifier,
exact elimination at \(s=1\) and all other parameters zero selects the
rows
\[
\begin{gathered}
x^4z^2,\ x^3yz^2,\ x^3z^3,\ x^2y^2z^2,\ x^2yz^3,\\
x^2z^4,\ xz^5,\ z^6                                  \tag{7}
\end{gathered}
\]
and the columns \(v_0,\ldots,v_7\).  Recomputing that minor symbolically
over the full coefficient ring gives
\[
-2^3 3^{15}s^8=-114\,791\,256s^8.                     \tag{8}
\]
Thus the rank is at least eight on \(s\ne0\), independently of
\(w,k,A,B,L\).

Direct construction with
\[
V=kq+\frac zs(A-a_5z^2)
       -\frac4{3s}z^2(\lambda x+\mu y)                 \tag{9}
\]
annihilates every \(E_6\) coefficient.  Its parameters
\((k,\lambda,\mu)\) are independent: the last two are themselves
coordinates in the eleven-variable system, while the \(k\)-direction has
nonzero \(x^3\)-coefficient.  Hence the solution space has dimension at
least three.  Together with (8), this proves rank exactly eight and
proves (9) is the complete solution.  Only \(s\) and the characteristic
zero unit \(3\) are inverted.

## 3. Complete \(E_5\) and \(E_4\) solves

After (9), there are exactly seven nonzero degree-five coefficients, on
\[
x^5,\ x^3z^2,\ x^2yz^2,\ x^2z^3,\ xz^4,\ yz^4,\ z^5.
\tag{10}
\]
They are jointly linear in
\[
b_0,b_1,b_2,b_3,b_4,\lambda,\mu.
\]
The full \(7\times7\) coefficient determinant, in these orders, is
\[
2^4 3^8s^7=104\,976s^7.                               \tag{11}
\]
There is therefore no internal \(E_5\) rank divisor.  Direct substitution
into every equation gives its unique solution:
\[
\begin{aligned}
\lambda&=\mu=0,\\
b_0&=a_0k/s,&b_1&=a_1k/s,&b_2&=a_2k/s,\\
b_3&=(a_3k+\ell_{11})/s,&
b_4&=(a_4k+\ell_{12})/s.
\end{aligned}                                         \tag{12}
\]
The two especially delicate transverse conclusions are independently
visible from
\[
[x^5]E_5=-3s\mu
\]
and
\[
[x^3z^2]E_5+3[yz^4]E_5=4s\lambda.                    \tag{13}
\]
No assumption on \(w\) or \(k\) is used.

After (12), the *entire* degree-four residual is
\[
\begin{aligned}
[x^2z^2]E_4&=9(-k\ell_{12}+s\ell_{22}),\\
[z^4]E_4&=-3(-k\ell_{11}+s\ell_{21}).                 \tag{14}
\end{aligned}
\]
There are no other surviving \(E_4\) coefficients.  In the unknowns
\((\ell_{21},\ell_{22})\), the determinant of (14) is \(27s^2\), so
\[
\ell_{21}=k\ell_{11}/s,\qquad
\ell_{22}=k\ell_{12}/s.                               \tag{15}
\]
Equations (12) and (15) give
\[
\det L
=\ell_{33}(\ell_{11}\ell_{22}-\ell_{12}\ell_{21})=0.  \tag{16}
\]
But a Keller map has
\(\det L=\det JF(0)\ne0\), even if its constant Jacobian has not been
normalized to one.  This is the required contradiction.

## 4. Independent exact certificate

`verify_vertical_triple_yz2_sparse.py` implements sparse multivariate
Laurent-polynomial arithmetic over \(\mathbb Q\) from scratch.  It
imports no computer algebra system and does not import either supplied
pivot list.  It:

- reconstructs the raw determinant and checks \(E_8,E_7\);
- independently selects and symbolically verifies (8), (11), and the
  \(27s^2\) pivot;
- asserts joint linearity before every rank argument;
- verifies all equations, including the completeness assertions in
  (9), (12), and (14);
- retains \(w,k\), all unused coefficients of \(A,B,V,L\), and \(b_5\)
  symbolically;
- includes negative controls for the \(V\)-solve, \(B\)-solve, and final
  singularity calculation.

Run:

```text
./verify_strict.sh
../verify_vertical_triple_yz2_gamma0_ell0_strict.sh
```

The new dependency-free reconstruction and the supplied SymPy and
PARI/GP implementations all pass.  They constitute three exact
implementations, with the new checker methodologically independent of
the two supplied calculations.  Exact algebra checks are not peer review.
This audit and its software were materially AI-assisted.
