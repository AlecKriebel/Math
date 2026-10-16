# Five centers in an alpha=16 cube move

**Status: complete exact counterexample candidate; separate adversarial review pending.**
This is a computer-assisted mathematical certificate using only rational arithmetic and integer root bounds. The floating-point search that found the example is not used to certify it.

## 1. Claim and source scope

The question on printed p.1785 of [Oberwolfach Report35/2020](https://ems.press/content/serial-article-files/46871?nt=1) asks whether three is the maximal number of potential central points for alpha-immersions when alpha>1. The precise realization setting is given in [Melotti–Ramassamy–Thévenin](https://arxiv.org/abs/2003.08941v2), Definitions2.1/2.4/2.5, Remark2.8, Theorem4.7 and Remark4.8; the [published version](https://ems.press/content/serial-article-files/39488) retains the expectation in Remark4.8. Crossings are allowed. The six boundary points must be distinct, and each alternating triple must be noncollinear.

**Proposition.** There is an admissible alpha=16 realization of the three quads before a cube move whose fixed six boundary points admit at least **five distinct** new central points afterward. The new centers are distinct from every boundary point. Thus the proposed upper bound of three is false.

No bound on the actual maximum is asserted, and “at least five” is not replaced by “exactly five.” The conclusion concerns realizations/immersions, not proper embedded tilings.

## 2. Rational foci and levels

Set
\[
A=(0,0),\quad B=(2073/10000,0),\quad
C=(4719/10000,64/10000),
\]
\[
\lambda=27/1250,\qquad\mu=1.
\tag{1}
\]
We first construct five distinct points X satisfying
\[
|X-B|^{16}-|X-A|^{16}=\lambda,
\qquad |X-C|^{16}-|X-A|^{16}=\mu.
\tag{2}
\]
These foci are noncollinear: det(B,C)=0.00132672>0.

Write b=2073/10000, c=4719/10000, d=64/10000. For s>=0 put
\[
u=s^{1/8},\quad v=(s+\lambda)^{1/8},\quad w=(s+1)^{1/8},
\]
\[
x(s)=\frac{b^2+u-v}{2b},\qquad
y(s)=\frac{c^2+d^2+u-w-2cx(s)}{2d},
\]
\[
G(s)=x(s)^2+y(s)^2-u.
\tag{3}
\]
All roots are positive real eighth roots. G is continuous on [0,infinity).

**Exact equivalence.** A zero s of G gives X=(x(s),y(s)) solving (2), because the defining linear equations imply
\[
|X-A|^2=u,
\quad |X-B|^2=v,
\quad |X-C|^2=w.
\]
Raising these nonnegative equalities to the eighth power gives (2). Conversely every solution of (2) has s=|X-A|^{16}, and its coordinates must satisfy the two invertible linear equations in (3), hence G(s)=0. Different s values give different points because s=|X-A|^{16}. There are no extraneous roots introduced by the reduction.

## 3. Five disjoint intermediate-value intervals

Exact rational interval arithmetic gives the following strict bounds:

| s | certified interval containing G(s) |
|---|---|
| 9/10000 | (38/100,39/100) |
| 11/10000 | (-28/100,-27/100) |
| 13/10000 | (51/100,52/100) |
| 1/2 | (-91/100,-90/100) |
| 1 | (9,10) |
| 10^17 | (-39,-38) |

Thus each of the five disjoint open intervals between successive listed s values contains a zero of G. By the equivalence above these supply five distinct points solving (2).

Here is the exact arithmetic behind the table. For rational q>=0, take D=2^200 and
\[
k=\left\lfloor\sqrt{\left\lfloor\sqrt{\left\lfloor\sqrt{
\lfloor qD^8\rfloor}\right\rfloor}\right\rfloor}\right\rfloor.
\]
Equivalently k is obtained by applying integer square root three times to floor(qD^8). Then
\[
(k/D)^8\leq q<((k+1)/D)^8,
\quad q^{1/8}\in[k/D,(k+1)/D].
\tag{4}
\]
For q=0 the exact interval [0,0] is used. Substitute these intervals into (3), using ordinary outward rational interval operations. Every decision in the accompanying `certify_five_centers.py` is an integer or Fraction comparison. The full rational endpoints of the resulting residual intervals are stored in `turn2_exact_certificate.json`; the table above is a deliberately coarser enclosure.

As an explanatory approximation only, the five certified points are near
\[
\begin{split}
&(-0.3864062930,\ 0.5196541287),\\
&(-0.3589856359,-0.5501782938),\\
&( 0.0896235465,-0.9408699996),\\
&( 0.0936742413,\ 0.9643898289),\\
&( 0.1036500000,\ 9.7582578125).
\end{split}
\tag{5}
\]
The proof uses the sign intervals, not these rounded positions. A sign-preserving rational bisection refines each of the five intervals 100 times. It never assumes that a root is unique. The resulting coordinate boxes are pairwise disjoint and are included in the exact certificate.

## 4. Six fixed admissible boundary vertices

Let J(a,b)=(-b,a). For a nonzero vector q, real h, and real level L, define T(q,h,L) as the unique real root t of
\[
|q|^{16}\left(((t-1)^2+h^2)^8-(t^2+h^2)^8\right)=L.
\tag{6}
\]
This is an algebraic specification with rational coefficients for every parameter used below. Existence and uniqueness are elementary: g(t)=(t^2+h^2)^8 is strictly convex, so g(t-1)-g(t) is strictly decreasing; its limits at negative and positive infinity are respectively positive and negative infinity. For h=0 strict convexity still holds, though our boundary choices use nonzero h.

Put
\[
t_1=T(C,10,\mu),\quad t_3=T(B,1,\lambda),\quad
t_5=T(C-B,-10,\mu-\lambda),
\]
and define, in the source's combinatorial order,
\[
\begin{array}{lll}
A_1=t_1C+10JC,& A_2=A,& A_3=t_3B+JB,\\
A_4=B,& A_5=B+t_5(C-B)-10J(C-B),& A_6=C.
\end{array}
\tag{7}
\]
The definitions give the **exact** identities
\[
|A_1-C|^{16}-|A_1-A|^{16}=\mu,
\quad |A_3-B|^{16}-|A_3-A|^{16}=\lambda,
\]
\[
|A_5-C|^{16}-|A_5-B|^{16}=\mu-\lambda.
\tag{8}
\]

Each parameter in (6) is enclosed by 160 steps of rational bisection, with its endpoint polynomial signs checked exactly. The resulting coordinate boxes certify
\[
\begin{array}{ll}
A_1:&x\in(0.17194,0.17196),\quad y\in(4.72219,4.72221),\\
A_3:&x\in(-0.55229,-0.55227),\quad y=0.2073,\\
A_5:&x\in(0.40359,0.40361),\quad y\in(-2.64281,-2.64279).
\end{array}
\tag{9}
\]
All terminating decimals in these coarse enclosures denote exact rationals. Together with (1), the boxes establish six distinct boundary points. The even determinant is the positive rational stated after (2); the odd determinant det(A3-A1,A5-A1) lies strictly between 6.37 and 6.39. The checker also verifies the stronger condition that no three boundary points are collinear.

For every X from Section3, equations (2) and (8) imply that all three quads
\[
A_2A_3A_4X,\qquad A_4A_5A_6X,\qquad A_6A_1A_2X
\tag{10}
\]
are 16-quads. For example the first condition is
\(|A_2-A_3|^{16}+|A_4-X|^{16}=|A_2-X|^{16}+|A_3-A_4|^{16}\),
which is exactly the lambda equation; the other two use mu-lambda and mu.

No potential center is one of the boundary points. Positive lambda and mu exclude B and C, and b^16!=lambda excludes A. Equation(2) forces x<b/2; the certified x coordinates of A1 and A5 exceed b/2. Finally
\[
|A_3-C|^{16}-|A_3-A|^{16}-1\in(0.98,0.99),
\]
so A3 is not a common-focus solution. The independently refined center boxes also verify these exclusions directly, and verify that none of the five centers lies on a line through any pair of boundary points.

## 5. An incoming center, also certified without a flip assumption

We certify an incoming point Z so that this is an actual instance of the original cube move, not merely the right-hand arrangement. Define the positive algebraic levels
\[
L=|A_4-A_5|^{16}-|A_4-A_3|^{16},\qquad
M=|A_2-A_1|^{16}-|A_2-A_3|^{16}.
\tag{11}
\]
Apply the scalar construction to common focus A3, other foci A5,A1, and levels L,M. More explicitly, put b'=A5-A3, c'=A1-A3, D'=det(b',c'), and
\[
u'=s^{1/8},\quad v'=(s+L)^{1/8},\quad w'=(s+M)^{1/8},
\]
\[
R_1=|b'|^2+u'-v',\quad R_2=|c'|^2+u'-w',
\]
\[
Y_x=(R_1c'_y-R_2b'_y)/(2D'),\quad
Y_y=(b'_xR_2-c'_xR_1)/(2D'),
\quad H(s)=Y_x^2+Y_y^2-u'.
\tag{12}
\]
Noncollinearity gives D'!=0. Exact interval arithmetic, retaining the algebraic boundary-point boxes, yields
\[
H(1/100)\in(0.00037,0.00038),\quad
H(11/1000)\in(-0.00081,-0.00080).
\]
Hence H has a root in (1/100,11/1000). At that root Z=A3+Y satisfies
\[
|Z-A_5|^{16}-|Z-A_3|^{16}=L,
\qquad |Z-A_1|^{16}-|Z-A_3|^{16}=M.
\tag{13}
\]
The coordinate box for the whole retained s interval is contained in
\[
Z_x\in(0.1677,0.1717),\qquad Z_y\in(-0.0036,-0.0026).
\]
It is disjoint from all six boundary boxes. The checker further excludes every line through a boundary pair.

Equations(11)–(13) establish the first two old quads A1A2A3Z and A3A4A5Z. For the third, subtract the two equations in (13). The exact boundary identities (8) give
\[
M-L=|A_6-A_1|^{16}-|A_6-A_5|^{16},
\]
so A5A6A1Z is a 16-quad as well. All three old and all three new quad conditions are therefore satisfied. The incoming realization was certified directly and does not depend on assuming the conjectured count or even importing the published existence theorem.

## 6. Verification and limits

`certify_five_centers.py` passes 6,987 exact checks. It uses no floating-point values in a branch deciding validity. Eighth-root bounds are checked by integer eighth powers; boundary parameters are algebraic roots bracketed with exact polynomial signs; all interval operations have rational endpoints. The certificate records all full rational enclosures. It depends only on elementary real algebra, strict convexity, and the intermediate value theorem.

This is a complete disproof candidate of the proposed bound of three, under the source's crossing-allowed realization hypotheses. It does not assert a bound for proper embeddings or determine the maximum possible number of centers. Separate review, source-scope checking, and historical-priority assessment remain necessary before publication claims.
