# Exclusion of the \(c_0=0\) unmarked boundary

**Exact candidate checkpoint:** 2026-07-25T14:12:07Z  
**Status:** complete primary proof; pending independent hostile audit; not
peer reviewed.

## 1. Normal form and statement

Assume \(a_2\ne0\) and \(c_0=0\) in the unmarked chart.  First consider
the open subchart \(b_1c_2\ne0\).  The residual source and target actions
normalize
\[
a_2=b_1=c_2=1,\qquad b_2=0.
\]
Write \(a=a_3,b=b_3,d=c_3\).  Then
\[
\begin{aligned}
P&=p(pq^2+aq^3),\\
Q&=p(p^3+p^2q+bq^3),\\
R&=pq^2+dq^3.                                    \tag{1}
\end{aligned}
\]

**Candidate theorem.**  Every Keller map on the exact-\(\delta=1\)
part of (1) is an automorphism.

The endpoint subcharts \(b_1c_2=0\) are treated next.  Thus the theorem
covers the entire \(a_2\ne0,c_0=0\) boundary.

## 2. Endpoint subcharts

After normalizing \(a_2=1\) and using the target shear that sets
\(b_2=0\), the first contact coefficient on \(c_0=0\) is
\[
-6(4a_3c_2-b_1c_2-4c_3).
\]
If \(c_2=0\), contact forces \(c_3=0\), hence \(R=0\); the
quadratic-component exit gives an automorphism.

Suppose \(c_2\ne0\) but \(b_1=0\), and normalize \(c_2=1\).  The first
four contact coefficients successively give
\[
c_3=a_3,\qquad\lambda=0,\qquad b_3=0,\qquad\mu=0.
\]
At this contact point,
\[
\begin{aligned}
\alpha&=4p^3q(2p+3a_3q),\\
\beta&=-q^3(p+a_3q)(2p+3a_3q),\\
\gamma&=-4p^4q(2p+3a_3q).
\end{aligned}
\]
Thus the gcd contains \(q(2p+3a_3q)\), so this endpoint is
disjoint from exact \(\delta=1\).

It remains to treat \(b_1c_2\ne0\), which is the normal form (1).

## 3. The unique contact orbit

The first two contact coefficients give
\[
d=\frac{4a-1}{4},\qquad
\lambda=\frac{4a-1}{2}.                          \tag{2}
\]
Exact \(\delta=1\) requires \(d\ne0\): if \(d=0\), then \(q\) divides
all three already-reduced minors at \(p=0\), giving a second copy of the
chart divisor.

After (2), the remaining equations first give
\[
b=\frac{32a^2-30a+5}{16},\qquad
\mu=-\frac{192a^3-368a^2+216a-35}{32}.           \tag{3}
\]
Two residual equations factor as
\[
\begin{aligned}
(2a-1)(640a^3-1056a^2+480a-65)&=0,\\
(2a-1)(128a^3-96a^2+5)&=0.                       \tag{4}
\end{aligned}
\]
The resultant of the two cubic factors is
\(-11324620800\ne0\).  Hence
\[
a=\frac12,\qquad b=-\frac18,\qquad d=\frac14,
\qquad \lambda=\frac12,\qquad\mu=-\frac5{32}.    \tag{5}
\]
This orbit really has exact gcd degree one.  Indeed, after removing the
chart divisor \(q\), its minors factor as
\[
\begin{aligned}
\bar\alpha&=\frac1{32}(8p^2+4pq+q^2)
                         (32p^2+16pq-3q^2),\\
\bar\beta&=-\frac18q^2(16p^2+8pq+3q^2),\\
\bar\gamma&=-\frac12p^2(2p+q)^2(4p+q).           \tag{6}
\end{aligned}
\]
The quadratic in \(\bar\beta\) takes the nonzero values \(3q^2\) and
\(2q^2\) on the two nonzero linear roots of \(\bar\gamma\); the endpoints
\(p=0,q=0\) are also not common.  Thus (6) has gcd one.

## 4. Lower homogeneous identities

Let the nonzero tangent parameter be normalized to one.  The tangent is
\[
\begin{aligned}
N_1&=(16p^2+8pq-q^2)/8,\\
N_2&=-(24p^2+12pq-q^2)/32,\\
N_3&=(4p+q)/2.                                   \tag{7}
\end{aligned}
\]
Target shears by the third component set \(u_3=v_3=0\).  A source shear
in the complementary coordinate sets \(t_0=t_2=0\); the target shears
then restore \(u_3=v_3=0\).

The \(E_6\) compatibility equations and the coefficient of the
complementary variable in \(E_5\) are parametrized by \(u_0,v_2,w\):
\[
\begin{gathered}
u_1=\frac34u_0+\frac89w,\quad
u_2=\frac18u_0+\frac23w,\\
v_0=\frac{16}{9}w+8v_2,\quad
v_1=w+6v_2,\quad t_1=\frac89w,                   \tag{8}\\
x_5=-\frac14,\quad y_5=\frac5{64},\\
x_3=-\frac18u_0+\frac49w,\quad
x_4=-\frac1{32}u_0-\frac19w,\\
y_3=-\frac13w-v_2,\quad
y_4=-\frac1{72}w-\frac14v_2,\quad
\ell_{33}=-\frac49w.                             \tag{9}
\end{gathered}
\]
Keeping all free coefficients, the constant part of \(E_5\) gives
\[
\begin{aligned}
x_0&=-8\ell_{13}+\frac29u_0w+16x_2,\\
x_1&=-4\ell_{13}+\frac1{18}u_0w+\frac{16}{81}w^2+8x_2,\\
y_0&=-8\ell_{23}+\frac{16}{9}v_2w+\frac{28}{81}w^2+16y_2,\\
y_1&=-4\ell_{23}+\frac49v_2w+\frac2{81}w^2+8y_2,\\
\ell_{31}&=4\ell_{32}+\frac{64}{81}w^2.          \tag{10}
\end{aligned}
\]

Put
\[
M_1=9\ell_{11}-36\ell_{12}+16w\ell_{13},\qquad
M_2=9\ell_{21}-36\ell_{22}+16w\ell_{23}.
\]
The complete \(E_4\) identity is
\[
\begin{aligned}
E_4={}&\frac{2M_1}{9}(p^4+p^3q)
 +\frac{9M_1-8M_2}{144}p^2q^2\\
&+\frac{M_1-8M_2}{288}pq^3
 -\frac{M_1+4M_2}{384}q^4.                      \tag{11}
\end{aligned}
\]
Thus \(M_1=M_2=0\).  Equations (9)--(10) then give
\[
L\begin{pmatrix}9\\-36\\16w\end{pmatrix}
=\begin{pmatrix}M_1\\M_2\\0\end{pmatrix}=0.       \tag{12}
\]
The vector is nonzero, contradicting \(L\in\mathrm{GL}_3\).

If the tangent parameter is zero, the injective binary lower block gives
the plane-plus-shear automorphism exit.  This proves the candidate
theorem.

## 5. Verification and disclosure

`verify_c0_zero_sympy.py` reconstructs the endpoint subcharts, contact
classification, exact-gcd test, and weighted determinant through (12).
`verify_c0_zero_pari.gp` independently reconstructs them in PARI/GP.

These scripts certify the encoded algebra.  They do not replace a hostile
audit of the normalizations and zero-tangent exit, establish scholarly
priority, or constitute peer review.  AI systems materially assisted the
discovery, verification, and exposition.
