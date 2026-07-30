# The sharp rank-one tangent obstruction to a \(C^2\)-defect bound

## Status

This note gives an exact counterexample to a proposed intermediate
inequality.  It is **not** a negative three-copy Werner witness and it
does not disprove the square-zero conjecture.

For a rank-at-most-two three-qutrit matrix put
\[
\begin{aligned}
 N(C)&=\|C\|_2^2,\\
 S(C)&=\sum_{i=1}^3\|\operatorname{Tr}_iC\|_2^2,\\
 P(C)&=\sum_{1\leq i<j\leq3}
       \|\operatorname{Tr}_{ij}C\|_2^2,\\
 D(C)&=s_1(C)s_2(C),
\end{aligned}
\]
and
\[
 F(C)=3N(C)-2S(C)+P(C)+2D(C).                 \tag{1}
\]
The surviving square-zero exterior conjecture is \(F(C)\geq0\) under
\(C^2=0\).

A natural defect extension is
\[
 F(C)+c\|C^2\|_2\geq0.                         \tag{2}
\]
The exact family below proves that every universal inequality of the
form (2) requires
\[
\boxed{\qquad c\geq c_*:=\frac4{\sqrt3}-2.\qquad}       \tag{3}
\]
In particular the initially proposed coefficient \(c=1/4\) is false,
because \(c_*>1/4\).

The family also shows that the obstruction is infinitesimal at a
rank-one point of the square-zero boundary.  It is not caused by any
of the previously found large nonnormal counterexamples to the
unrestricted exterior inequality.

The dependency-free exact checker is
`verification/verify_n3_csquare_tangent_obstruction.py`.

## 1. The orthogonal chain

In \((\mathbb C^3)^{\otimes3}\), define
\[
\begin{aligned}
 x&=|000\rangle,\\
 y&=\frac1{\sqrt3}
   \left(|001\rangle+|010\rangle+|100\rangle\right),\\
 z&=\frac1{\sqrt3}
   \left(|011\rangle+|101\rangle+|110\rangle\right).
\end{aligned}                                           \tag{4}
\]
The three vectors are orthonormal.  For \(t\geq0\), put
\[
\boxed{\qquad
 C_t=|x\rangle\langle y|+t|y\rangle\langle z|.
\qquad}                                                  \tag{5}
\]
The initial and final vectors in the two summands are pairwise
orthogonal.  Consequently the nonzero singular values of \(C_t\) are
\[
 s_1(C_t)=1,\qquad s_2(C_t)=t
\quad(0\leq t\leq1),                                    \tag{6}
\]
and \(C_t\) has rank two for \(t>0\).  Moreover
\[
 C_t^2=t|x\rangle\langle z|,
\qquad
\boxed{\|C_t^2\|_2=t.}                                  \tag{7}
\]

At \(t=0\), the pair \((x,y)\) is exactly a product--tangent equality
pair for the sharp rank-one pair-sector theorem: \(x\) is a product
vector and \(y\) lies in the tangent space of the product-vector
variety at \(x\).

## 2. Exact endpoint invariants

Direct simultaneous partial contraction gives
\[
\boxed{
\begin{aligned}
 N(C_t)&=1+t^2,\\
 S(C_t)&=2+\frac4{\sqrt3}t+\frac43t^2,\\
 P(C_t)&=1+\frac4{\sqrt3}t+\frac43t^2.
\end{aligned}}                                         \tag{8}
\]
Substituting (8) gives
\[
 3N(C_t)-2S(C_t)+P(C_t)
 =
 -\frac4{\sqrt3}t+\frac53t^2.                          \tag{9}
\]
Using \(D(C_t)=t\),
\[
\boxed{\qquad
 F(C_t)=
 \left(2-\frac4{\sqrt3}\right)t+\frac53t^2.
\qquad}                                                 \tag{10}
\]
Thus
\[
\begin{aligned}
 F(C_t)+c\|C_t^2\|_2
 &=
 \left(c-c_*\right)t+\frac53t^2.                       \tag{11}
\end{aligned}
\]
If \(c<c_*\), the right side is negative for every
\[
 0<t<\frac35(c_*-c).                                   \tag{12}
\]
This proves (3), and supplies an explicit exact counterexample for
every smaller coefficient.

For the specific discarded coefficient \(c=1/4\), one may choose,
for example,
\[
 t=\frac1{100}.
\]
Since \(\sqrt3<7/4\), hence \(4/\sqrt3>16/7\), equation (11) gives
\[
\begin{aligned}
 F(C_{1/100})+\frac14\|C_{1/100}^2\|_2
 &<
 \left(\frac94-\frac{16}{7}\right)\frac1{100}
 +\frac53\frac1{10000}\\
 &=-\frac1{2800}+\frac1{6000}<0.                       \tag{13}
\end{aligned}
\]
So even the failure at \(c=1/4\) has a short rational comparison
certificate; no decimal approximation is needed.

## 3. What the obstruction says

The sharp candidate suggested by this family is
\[
\boxed{\qquad
 F(C)+\left(\frac4{\sqrt3}-2\right)\|C^2\|_2\geq0
 \quad(\operatorname{rank}C\leq2).
\qquad}                                                 \tag{14}
\]
If (14) were proved, setting \(C^2=0\) would establish the stronger
square-zero exterior inequality and hence square-zero three-copy
positivity.  No proof of (14) is given here.

The constant in (14), if the inequality is true, is necessarily
sharp and is approached only as \(t\downarrow0\) along (5).  This
locates the first stability problem precisely: one needs quantitative
control transverse to the product--tangent component of the
rank-one equality variety.  A compactness or strict-gap argument that
ignores this singular-value-opening direction cannot supply a uniform
constant.
