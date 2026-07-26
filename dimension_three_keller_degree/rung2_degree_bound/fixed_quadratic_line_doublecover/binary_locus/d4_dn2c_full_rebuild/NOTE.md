# D4-DN-2C: complete \(E_7\) kernel and full-lower \(E_6\) atlas

**Frozen family.** Put
\[
h=(p+q)^2,\qquad P=hp^2,\qquad Q=hq^2,\qquad
R=h(p-2q).
\]
This note concerns only this fixed binary top family.  It does **not** yet
exclude the family: the \(E_5/E_4\) descent remains to be done.

All calculations below are exact in characteristic zero.  The executable
certificate is `verify_full_e6_elimination.py`.

## 1. Complete \(E_7\) contact kernel

For
\[
H_4=(P,Q,0),\quad H_3=(U,V,R),\quad H_2=(A,B,T),
\]
the coefficient \(E_7\) of
\[
\det\!\left(L+wJH_2+w^2JH_3+w^3JH_4\right)
\]
is
\[
 E_7=\alpha\,\partial_rU+\beta\,\partial_rV+\gamma\,\partial_rT,
\]
where
\[
\begin{aligned}
\alpha&=\{Q,R\}=-6pq(p+q)^3,\\
\beta&=-\{P,R\}=6p(p+q)^3(p+2q),\\
\gamma&=\{P,Q\}=8pq(p+q)^4.
\end{aligned}
\]
After removing the common factor \(2p(p+q)^3\), the contact row is
\[
 -3q\,\partial_rU+3(p+2q)\,\partial_rV
       +4q(p+q)\,\partial_rT=0.                 \tag{1}
\]

The \(r^2,r^1,r^0\) coefficient blocks of (1) have ranks \(2,3,4\),
respectively.  Thus the \(r\)-dependent kernel has dimension \(0+2+4=6\).
The eleven binary coefficients of \(U_0,V_0,T_0\) are free.

A complete six-parameter presentation is
\[
\begin{aligned}
U&=U_0+rU_1+r^2U_2,&
V&=V_0+rV_1+r^2V_2,&
T&=T_0+rT_1+r^2T_2,\\
U_2&=\left(d+\frac43z\right)p+
       \left(2d+\frac43z\right)q,&
V_2&=dq,&T_2&=z,\\
U_1&=\left(x+\frac43a\right)p^2+
 \left(y+2x+\frac43(a+b)\right)pq+
 \left(2y+\frac43b\right)q^2,\\
V_1&=xpq+yq^2,&T_1&=ap+bq .
\end{aligned}                                      \tag{2}
\]
There are no \(r^3\) terms in \(U,V\).

## 2. The \(E_6\) contact projection

The four lower-variable-free \(r^3\) coefficients in \(E_6\) are
\[
\begin{array}{c|c}
p^3r^3&-6d^2\\
p^2qr^3&\frac{16}{3}z(3d+z)\\
pq^2r^3&\frac{2}{3}(3d+4z)(9d+4z)\\
q^3r^3&\frac{4}{3}(3d+2z)^2 .
\end{array}
\]
Consequently \(d=z=0\) set-theoretically.

At \(d=z=0\), only the \(r^2\)-coefficients \(a_{r^2},b_{r^2}\)
of \(A,B\) occur in the six \(r^1\) equations.  Exact elimination gives
\[
J=\left(f,\ (2b+3y)^2\right),                    \tag{3}
\]
where
\[
f=
8a^2-16ab+24ax-24ay-24bx
 +27x^2-54xy+9y^2.                               \tag{4}
\]
Hence the set-theoretic contact locus is
\[
2b+3y=0,\qquad f=0.                              \tag{5}
\]

Let \(\eta^2=-2\).  On \(b=-3y/2\), (4) becomes
\[
f_0=8a^2+24ax+27x^2-18xy+9y^2,
\]
and
\[
\begin{aligned}
\ell_+&=9x+(4+2\eta)a+(-3+3\eta)y,\\
\ell_-&=9x+(4-2\eta)a+(-3-3\eta)y,\\
\ell_+\ell_-&=3f_0.
\end{aligned}
\]
Thus over the algebraic closure the contact locus is the union of two
distinct planes.

## 3. Frozen full-lower atlas

The full \(E_6\) system has 13 equations and retains all 18 lower
coefficients, ordered in the certificate as
\[
\begin{split}
(&a_{pr},a_{qr},a_{r^2},
  b_{pr},b_{qr},b_{r^2},\ell_{33},\\
 &u_{p^3},u_{p^2q},u_{pq^2},u_{q^3},
  v_{p^3},v_{p^2q},v_{pq^2},v_{q^3},
  t_{p^2},t_{pq},t_{q^2}).
\end{split}
\]
No one of these columns is zero.

The two planes are parametrized by \(a=k,\ y=s,\ b=-3s/2\) and
\[
\begin{aligned}
\Pi_+:\quad
x&=\frac{-(4+2\eta)k+(3-3\eta)s}{9},\\
\Pi_-:\quad
x&=\frac{-(4-2\eta)k+(3+3\eta)s}{9}.
\end{aligned}
\]
They meet exactly when \(2k+3s=0\).  The common line is
\[
(a,b,x,y)=\left(k,k,-\frac23k,-\frac23k\right).
\]

Using zero-based row and column indices, the complete atlas is:

| chart | condition | rows | columns | pivot | rank |
|---|---|---|---|---|---:|
| `DN2C-P+` | \(\Pi_+\), \(2k+3s\ne0\) | \(0,1,2,3,4,5,7\) | \(0,1,2,3,5,7,8\) | \(93312(\eta-1)(2k+3s)^2\) | 7 |
| `DN2C-P-` | \(\Pi_-\), \(2k+3s\ne0\) | \(0,1,2,3,4,5,7\) | \(0,1,2,3,5,7,8\) | \(93312(-\eta-1)(2k+3s)^2\) | 7 |
| `DN2C-I*` | common line, \(k\ne0\) | \(0,1,2,3,4,5\) | \(0,1,2,3,5,7\) | \(186624k\) | 6 |
| `DN2C-O` | \(k=0\) | \(0,1,2,3,4\) | \(0,1,2,3,5\) | \(31104\) | 5 |

For every chart, the verifier solves on precisely the displayed pivot while
leaving every nonpivot lower variable free, then substitutes into all 13
equations.  Every residual is identically zero.  This proves both the
displayed rank and equality of coefficient and augmented ranks throughout
the stated localization.  In particular, there is no denominator-defined
contact case outside the four frozen charts.

## Scope and next step

This is a completeness result for \(E_7\) and the set-theoretic full-lower
\(E_6\) projection of `D4-DN-2C`.  It is not an exclusion theorem and makes
no statement about all quartic Keller maps.  The next calculation must start
from all four charts and retain all free lower coefficients through \(E_5\)
and \(E_4\).
