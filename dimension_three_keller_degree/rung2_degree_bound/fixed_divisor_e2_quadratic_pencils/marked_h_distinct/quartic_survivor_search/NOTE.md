# Uniform \(E_5\) obstruction on the finite nonzero smooth-secant chart

## Scope and status

This note proves an exact exclusion inside the frozen internal stratum

```text
Q2-E2-A2-B1-D1-N1-MD-P21-HSM-CTAU
```

It also covers its finite boundary `CT`.  It does **not** exclude the
parent `Q2-E2-A2-B1-D1-N1` row, the `CH` boundary, or the `CS` boundary,
and it does not improve the global degree bound by itself.

The argument uses the released complete \(E_7\) normal form and reconstructs
all subsequent determinant coefficients independently in SymPy and PARI/GP.
It was developed with substantial AI assistance, is not peer reviewed, and
its exact checks certify the encoded algebra rather than the exposition or
scope.

## Proposition

Let \(F:\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}\) have degree at
most four.  Suppose that, after the legal affine source and invertible target
changes used in the frozen taxonomy, its leading data belong to the
smooth-secant marked-pair chart
\[
 h=x^2+yz,\qquad s=x^2,\qquad
 r=h+k s,\qquad 0\ne k\in\mathbb C.
\]
Then \(\det JF\) cannot be a nonzero constant.

In particular, the proposition excludes every `CTAU` orbit
\(k\in\mathbb C\setminus\{0,-1\}\) and the finite `CT` boundary \(k=-1\).

## 1. Released \(E_7\) normal form

Write
\[
 F=F_0+LX+H_2+H_3+H_4
\]
with homogeneous \(H_i\) of degree \(i\).  Constants do not affect the
Jacobian.  The complete \(E_7\) normal form for every finite \(k\ne0\) is
\[
\begin{aligned}
H_4&=(P,Q,0)=\bigl(h^2,hx^2,0\bigr),\\
H_3&=(U,V,R)=\bigl(Ax^3,Bx^3,x(h+kx^2)\bigr),\\
(H_2)_3&=Tx^2.
\end{aligned}
\]
The first two components of \(H_2\) remain arbitrary quadratics and \(L\)
remains an arbitrary \(3\times3\) matrix.

The released normal-form proof uses two pivot charts with extra factors
\[
q=9k^2+6k-1,\qquad r=3k-1.
\]
They cover all \(k\ne0\), because
\[
\frac12q-\frac32(k+1)r=1,\qquad
\operatorname{Res}_k(q,r)=18.
\]
Thus no finite nonzero \(k\) is lost through denominator clearing.

Use the monomial order
\[
(x^2,xy,xz,y^2,yz,z^2)
\]
and write
\[
\begin{aligned}
(H_2)_1&=\sum_{i=0}^{5}a_i m_i,&
(H_2)_2&=\sum_{i=0}^{5}b_i m_i,\\
L&=(\ell_{ij})=
\begin{pmatrix}
\ell_0&\ell_1&\ell_2\\
\ell_3&\ell_4&\ell_5\\
\ell_6&\ell_7&\ell_8
\end{pmatrix}.
\end{aligned}
\]

Introduce a bookkeeping variable \(w\):
\[
\mathcal J(w)=L+wJH_2+w^2JH_3+w^3JH_4,\qquad
E_j=[w^j]\det\mathcal J(w).
\]
The normal form has \(E_9=E_8=E_7=0\).

## 2. Division-free \(E_6\) elimination

Only ten lower coefficients occur in \(E_6\):
\[
a_1,a_2,a_3,a_5,\ b_1,b_2,b_3,b_5,\ \ell_7,\ell_8.
\]
The twelve nonzero monomial coefficients are
\[
\begin{array}{c|l}
x^5y&(3k-1)a_1-(6k+2)b_1+4\ell_7\\
x^5z&-(3k-1)a_2+(6k+2)b_2-4\ell_8\\
x^4y^2&2((3k-1)a_3-(6k+2)b_3)\\
x^4z^2&-2((3k-1)a_5-(6k+2)b_5)\\
x^3y^2z&-a_1-(6k+4)b_1+8\ell_7\\
x^3yz^2&a_2+(6k+4)b_2-8\ell_8\\
x^2y^3z&-2(a_3+(6k+4)b_3)\\
x^2yz^3&2(a_5+(6k+4)b_5)\\
xy^3z^2&-2(b_1-2\ell_7)\\
xy^2z^3&2(b_2-2\ell_8)\\
y^4z^2&-4b_3\\
y^2z^4&4b_5.
\end{array}
\]

Setting these coefficients to zero first gives
\[
b_3=a_3=b_5=a_5=0.
\]
For the \(y\)-chain it gives
\[
b_1=2\ell_7,\qquad a_1=-12k\ell_7,\qquad
-36k^2\ell_7=0.
\]
The \(z\)-chain similarly gives
\[
b_2=2\ell_8,\qquad a_2=-12k\ell_8,\qquad
36k^2\ell_8=0.
\]
Because \(k\ne0\) in characteristic zero,
\[
a_1=a_2=a_3=a_5=b_1=b_2=b_3=b_5=\ell_7=\ell_8=0. \tag{1}
\]
This is a saturation certificate with sole divisor \(k=0\), already the
separate frozen `CH` boundary.  No \(q\)- or \(r\)-division is used.

## 3. \(E_5\) forces the linear part to be singular

After (1), \(E_5\) has only six nonzero monomial coefficients:
\[
\begin{array}{c|l}
x^4y&(3k-1)\ell_1-(6k+2)\ell_4\\
x^4z&-(3k-1)\ell_2+(6k+2)\ell_5\\
x^2y^2z&-\ell_1-(6k+4)\ell_4\\
x^2yz^2&\ell_2+(6k+4)\ell_5\\
y^3z^2&-2\ell_4\\
y^2z^3&2\ell_5.
\end{array}
\]
The last two coefficients force \(\ell_4=\ell_5=0\), and the preceding
two then force \(\ell_1=\ell_2=0\).  Together with
\(\ell_7=\ell_8=0\), this leaves
\[
L=
\begin{pmatrix}
\ell_0&0&0\\
\ell_3&0&0\\
\ell_6&0&0
\end{pmatrix},
\qquad \det L=0.
\]

If \(\det JF\) were a nonzero constant, evaluating it at the origin would
give \(\det L\ne0\).  This contradiction proves the proposition.  The
identities \(E_4,\ldots,E_1\) are not needed.

## 4. Verification

Run:

```sh
sh verify_strict.sh
```

The aggregate requires all of:

- an immutable-input check against the frozen taxonomy, its certificate,
  and the released \(E_7/E_6\) normal-form verifiers;
- an exact SymPy reconstruction of the weighted determinant;
- an independent exact PARI/GP reconstruction;
- a dependency-free modular scan over every \(k\ne0\) in nine prime
  fields, totaling 146 parameter values.

The modular scan is reconnaissance and regression evidence only.  The
characteristic-zero proof is the displayed division-free coefficient
elimination.
