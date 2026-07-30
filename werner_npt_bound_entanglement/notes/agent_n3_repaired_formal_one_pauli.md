# The repaired three-copy formal point in the one-Pauli branch

## Status

This note attacks the exact repaired formal critical table
\[
 N=\frac19I_9,\qquad
 \Beta_{pp,rr}=\frac1{36},\qquad
 \Beta_{pq,pq}=\frac1{180}\quad(p\ne q),
\tag{1}
\]
with every other entry of \(\Beta\) zero.  The table gives the formal
value \(q=-1/120\), satisfies
\[
 -\frac12N\preceq\Beta\preceq N,
\]
and satisfies all presently derived local-filter critical and Hessian
conditions.

The results below are exact necessary conditions for a common
two-column realization
\[
 C_{pq}=X_pY_q^\dagger.
\tag{2}
\]
They do not yet exclude (1) and do not construct it.  They reduce its
realizability to an explicit compact one-Pauli system and give a
nonlinear determinant floor on every off-diagonal pencil.

The dependency-free exact checker is
`verification/verify_n3_repaired_formal_one_pauli.py`.

## 1. Canonical ordinary-Gram geometry

The orthogonal common-block theorem gives, after perhaps interchanging
\(X\) and \(Y\), a logical gauge in which
\[
 X_p^\dagger X_r
 =\frac{\delta_{pr}}3I_2+h_{pr}H.
\tag{3}
\]
Here
\[
 h=h^\dagger,\qquad \operatorname{Tr}h=0,
\]
and either \(H=0\), or
\[
 H=\operatorname{diag}(1-\lambda,-\lambda),
\qquad 0<\lambda<1.
\tag{4}
\]
Write the columns as
\[
 X_p=(x_{p0},x_{p1}),\qquad
 Y_q=(y_{q0},y_{q1}).
\]
Then (3) says
\[
\begin{aligned}
 \langle x_{p0},x_{r0}\rangle
 &=\frac{\delta_{pr}}3+(1-\lambda)h_{pr},\\
 \langle x_{p1},x_{r1}\rangle
 &=\frac{\delta_{pr}}3-\lambda h_{pr},\\
 \langle x_{pa},x_{rb}\rangle&=0\quad(a\ne b).
\end{aligned}
\tag{5}
\]
The opposite triples obey
\[
\begin{aligned}
 \langle y_{s0},y_{q0}\rangle
 &=\frac{\lambda}{3}\delta_{sq},\\
 \langle y_{s1},y_{q1}\rangle
 &=\frac{1-\lambda}{3}\delta_{sq}.
\end{aligned}
\tag{6}
\]
Their crossed Gram
\[
 Z_{sq}=\langle y_{s0},y_{q1}\rangle
\tag{7}
\]
is not fixed by the ordinary block Gram.

Conversely, (5)--(6) imply
\[
 \langle C_{pq},C_{rs}\rangle_{\rm HS}
 =\frac19\delta_{pr}\delta_{qs}.
\tag{8}
\]
Indeed, only equal logical-column labels survive, and the coefficient
of \(h_{pr}\) cancels:
\[
 \lambda(1-\lambda)+(1-\lambda)(-\lambda)=0.
\]
Thus (3)--(7) are a lossless canonical parametrization of the
ordinary-Gram part of (1).

For \(a,b\in\mathbb C^3\), put
\[
 X(a)=\sum_pa_pX_p,\qquad
 Y(b)=\sum_qb_qY_q.
\]
Their logical Gram matrices are
\[
\boxed{
\begin{aligned}
 A(a):=X(a)^\dagger X(a)
 &=\frac{\|a\|^2}{3}I_2+(a^\dagger ha)H,\\
 B(b):=Y(b)^\dagger Y(b)
 &=
 \begin{pmatrix}
 \lambda\|b\|^2/3&b^\dagger Zb\\
 \overline{b^\dagger Zb}&(1-\lambda)\|b\|^2/3
 \end{pmatrix}.
\end{aligned}}
\tag{9}
\]
In particular
\[
 \|X(a)Y(b)^\dagger\|_2^2
 =\frac19\|a\|^2\|b\|^2.
\tag{10}
\]

## 2. The exact two-copy kernel equations

Identify a vector in
\(\mathbb C^3\otimes\mathbb C^3\) with its \(3\times3\)
coefficient matrix.  For such matrices \(U,V,S,T\), define
\[
 \kappa(U,V;S,T)
 ={\cal B}_2(|U\rangle\langle V|,
             |S\rangle\langle T|).
\]
Direct partial contraction gives
\[
\boxed{
\begin{aligned}
 \kappa(U,V;S,T)
={}&
 \langle U,S\rangle\langle T,V\rangle\\
 &-\frac12\operatorname{Tr}(VU^\dagger ST^\dagger)
 -\frac12\operatorname{Tr}(V^{\mathsf T}
       \overline U S^{\mathsf T}\overline T)\\
 &+\frac14\langle U,V\rangle\langle T,S\rangle .
\end{aligned}}
\tag{11}
\]
Consequently the complete realization equations for (1) are
\[
\boxed{
 \sum_{\alpha,\beta=0}^1
 \kappa(x_{p\alpha},y_{q\alpha};
        x_{r\beta},y_{s\beta})
 =
 \begin{cases}
 1/36,&p=q,\ r=s,\\
 1/180,&(p,q)=(r,s),\ p\ne q,\\
 0,&\text{otherwise}.
 \end{cases}}
\tag{12}
\]
Equations (5)--(7), positivity of the four displayed Gram matrices,
and (12) are an exact finite polynomial realization problem.  No
symmetry, reality, or tensor-product assumption has been imposed on
the two-qutrit vectors.

The product coefficients have a particularly small scalar form.
From (1),
\[
\boxed{
\begin{aligned}
Q_2(X(a)Y(b)^\dagger)
={}&\frac1{180}
 \left(
 \|a\|^2\|b\|^2
 -\sum_p|a_p|^2|b_p|^2
 \right)\\
&+\frac1{36}
\left|\sum_pa_p\overline{b_p}\right|^2 .
\end{aligned}}
\tag{13}
\]
This formula forces every nonzero \(X(a)\) and \(Y(b)\) to be
injective.  For example, if \(X(a)\) had rank at most one, choose
nonzero \(b\perp a\).  Then (13) and (10) would give
\[
 \frac{Q_2(X(a)Y(b)^\dagger)}
 {\|X(a)Y(b)^\dagger\|_2^2}\le\frac1{20},
\]
whereas the product has rank at most one and the sharp rank-one
two-copy bound gives quotient at least \(1/4\).  The argument with
\(a,b\) exchanged proves the assertion for \(Y(b)\).  Thus
\[
 A(a)\succ0,\qquad B(b)\succ0
 \quad\text{for every nonzero }a,b.
\tag{13a}
\]

The product-pencil quotient also has an exact global floor.  For unit
\(a,b\), put
\[
 D=\sum_p|a_p|^2|b_p|^2,\qquad
 O=|\langle b,a\rangle|^2.
\]
If \(z_p=a_p\overline{b_p}\), then
\[
 O=\left|\sum_pz_p\right|^2,\qquad
 D=\sum_p|z_p|^2,\qquad
 \sum_p|z_p|\le1.
\]
The triangle inequality gives
\[
 O\ge\max(0,2D-1).
\]
Substitution in (13), separately for \(D\le1/2\) and
\(D\ge1/2\), proves
\[
\boxed{
 Q_2(X(a)Y(b)^\dagger)
 \ge\frac1{40}
 \|X(a)Y(b)^\dagger\|_2^2.}
\tag{13b}
\]
The constant is sharp.  For any \(p\ne r\), take
\[
 a=\frac{e_p+e_r}{\sqrt2},\qquad
 b=\frac{e_p-e_r}{\sqrt2}.
\tag{13c}
\]
Then \(D=1/2\), \(O=0\), and equality holds in (13b).

For \(b_p=0\) and \(a=e_p\), this is exactly
\[
 Q_2(X_pY(b)^\dagger)
 =\frac1{180}\|b\|^2,
\qquad
 \|X_pY(b)^\dagger\|_2^2
 =\frac19\|b\|^2.
\tag{14}
\]
Thus every off-diagonal two-dimensional pencil has the fixed
Rayleigh quotient \(1/20\).

## 3. An exact singular-product floor at quotient \(1/20\)

We need one quantitative consequence of the proved two-copy theorem.

### Lemma 1

Let \(M\) have rank at most two and nonzero singular values
\(s_1\ge s_2\).  If
\[
 Q_2(M)=\frac1{20}\|M\|_2^2,
\tag{15}
\]
then
\[
\boxed{
\frac{s_2}{s_1}\ge
\frac{10-2\sqrt6}{19},
\qquad
s_1s_2\ge\frac14\|M\|_2^2.}
\tag{16}
\]

#### Proof

Write the singular dyads as \(E_1,E_2\), normalized in
Hilbert--Schmidt norm, and put
\[
 a=Q_2(E_1),\qquad b=Q_2(E_2),\qquad
 c={\cal B}_2(E_1,E_2).
\]
The strict rank-one theorem gives the lower bound \(1/4\), while
\(L^{\otimes2}\preceq I\) gives the upper bound.  Hence
\[
 \frac14\le a,b\le1.
\tag{17}
\]
Every linear combination of \(E_1,E_2\) has rank at most two.
The proved unrestricted two-copy theorem therefore makes
\[
 \begin{pmatrix}a&c\\\overline c&b\end{pmatrix}\succeq0.
\]
Hence
\[
\begin{aligned}
 Q_2(M)
 &\ge (s_1\sqrt a-s_2\sqrt b)^2.
\end{aligned}
\tag{18}
\]
Put \(x=s_2/s_1\).  If \(x\ge1/2\), the first inequality in
(16) is immediate.  If \(x<1/2\), minimizing the right side of
(18) over (17) gives
\[
 Q_2(M)\ge s_1^2(1/2-x)^2.
\]
Using (15) yields
\[
 \frac1{20}(1+x^2)\ge(1/2-x)^2,
\]
or
\[
 19x^2-20x+4\le0.
\]
Its smaller root is
\[
 x_0=\frac{10-2\sqrt6}{19}.
\]
Moreover \(x_0>2-\sqrt3\).  One exact way to see this is that the
quadratic on the left is decreasing below \(1/2\), while
\[
 19(2-\sqrt3)^2-20(2-\sqrt3)+4
 =97-56\sqrt3>0;
\]
the last inequality follows from \(97^2-(56\sqrt3)^2=1\).
Thus \(x\ge2-\sqrt3\).  Since \(x/(1+x^2)\) is increasing on
\([0,1]\),
\[
 \frac{x}{1+x^2}\ge
 \frac{2-\sqrt3}{1+(2-\sqrt3)^2}=\frac14.
\]
This proves (16). \(\square\)

The identical argument at the sharp quotient \(1/40\) gives
\[
\boxed{
 Q_2(M)=\frac1{40}\|M\|_2^2
 \Longrightarrow
 \frac{s_2}{s_1}\ge\frac13,\qquad
 s_1s_2\ge\frac3{10}\|M\|_2^2.}
\tag{16a}
\]
Indeed, in the \(x<1/2\) branch the scalar inequality becomes
\[
 39x^2-40x+9\le0,
\]
whose smaller root is \(1/3\), and
\[
 \frac{(1/3)}{1+(1/3)^2}=\frac3{10}.
\]

For \(M=X(a)Y(b)^\dagger\),
\[
 (s_1s_2)^2=\det A(a)\det B(b).
\tag{19}
\]
Applying Lemma 1 to (14) gives the nonlinear pencil condition
\[
\boxed{
\sqrt{\det A(e_p)\det B(b)}
\ge\frac1{36}\|b\|^2
\qquad(b_p=0).}
\tag{20}
\]
The transposed version is
\[
\boxed{
\sqrt{\det A(a)\det B(e_q)}
\ge\frac1{36}\|a\|^2
\qquad(a_q=0).}
\tag{21}
\]

Applying (16a) to the three Hadamard pairs (13c) gives, for every
\(p\ne r\),
\[
\boxed{
\begin{aligned}
 \sqrt{\det A\left(\frac{e_p+e_r}{\sqrt2}\right)
       \det B\left(\frac{e_p-e_r}{\sqrt2}\right)}
 &\ge\frac1{30},\\
 \sqrt{\det A\left(\frac{e_p-e_r}{\sqrt2}\right)
       \det B\left(\frac{e_p+e_r}{\sqrt2}\right)}
 &\ge\frac1{30}.
\end{aligned}}
\tag{21a}
\]
These six inequalities couple the off-diagonal entries of \(h\) and
\(Z\); they cannot be recovered from the nine individual block
determinants.

Write
\[
 \alpha_p=\sqrt{\det A(e_p)},\qquad
 \beta_q=\sqrt{\det B(e_q)}.
\]
Since
\[
 \beta_q\le\frac{\sqrt{\lambda(1-\lambda)}}3,
\]
(20) implies
\[
 \alpha_p\ge
 \frac1{12\sqrt{\lambda(1-\lambda)}}.
\tag{22}
\]
Minkowski's determinant inequality and
\(\sum_pA(e_p)=I_2\) give
\[
 \sum_p\alpha_p\le1.
\]
Therefore the coordinate pencils alone give the preliminary restriction
\[
\sqrt{\lambda(1-\lambda)}\ge\frac14.
\]

The Hadamard pencils improve this.  Put
\[
 \alpha_\pm^{pr}
 =\sqrt{\det A\left(\frac{e_p\pm e_r}{\sqrt2}\right)},
 \qquad
 \beta_\pm^{pr}
 =\sqrt{\det B\left(\frac{e_p\pm e_r}{\sqrt2}\right)}.
\]
Every normalized \(B(b)\) has trace \(1/3\), hence
\[
 \beta_\pm^{pr}\le
 \frac{\sqrt{\lambda(1-\lambda)}}3.
\]
The two inequalities (21a) consequently imply
\[
 \alpha_+^{pr},\alpha_-^{pr}
 \ge\frac1{10\sqrt{\lambda(1-\lambda)}}.
\]
Moreover,
\[
 A\left(\frac{e_p+e_r}{\sqrt2}\right)
 +A\left(\frac{e_p-e_r}{\sqrt2}\right)
 =A(e_p)+A(e_r).
\]
Minkowski's determinant inequality gives
\[
 \sqrt{\det(A(e_p)+A(e_r))}
 \ge\frac1{5\sqrt{\lambda(1-\lambda)}}.
\]
Sum this over the three unordered pairs.  Since
\(\sum_pA(e_p)=I_2\), the three matrices on the left are
\(I_2-A(e_s)\).  The arithmetic--geometric mean inequality gives
\[
 \sum_s\sqrt{\det(I_2-A(e_s))}
 \le\frac12\sum_s\operatorname{Tr}(I_2-A(e_s))
 =2.
\]
Thus every realization obeys the stronger exact interior restriction
\[
\boxed{
\sqrt{\lambda(1-\lambda)}\ge\frac3{10}.}
\tag{23}
\]
Equivalently,
\[
\boxed{\frac1{10}\le\lambda\le\frac9{10}.}
\]
In particular, the common Pauli direction is uniformly separated
from both rank-drop faces.  This still does not exclude the branch:
the symmetric point \(\lambda=1/2\) passes this scalar obstruction.

For comparison, the weaker coordinate-only estimate was
\[
\sqrt{\lambda(1-\lambda)}\ge\frac14.
\]

There are also explicit principal-plane inequalities.  From (9) and
(20), for every \(b\) with \(b_p=0\),
\[
\boxed{
 |b^\dagger Zb|^2
 \le
 \left[
 \frac{\lambda(1-\lambda)}9
 -\left(\frac1{36\alpha_p}\right)^2
 \right]\|b\|^4.}
\tag{24}
\]
Similarly, putting \(t=a^\dagger ha\), (21) gives
\[
\boxed{
\frac{\|a\|^4}{9}
+\frac{1-2\lambda}{3}\|a\|^2t
-\lambda(1-\lambda)t^2
\ge
\left(\frac1{36\beta_q}\right)^2\|a\|^4
\quad(a_q=0).}
\tag{25}
\]
These are genuine nonlinear restrictions: they involve the common
\(h,Z,\lambda\), not independently adjustable block energies.

## 4. Remaining explicit lemma

The repaired formal point can now be excluded by proving that no
\[
 0<\lambda<1,\quad h=h^\dagger,\quad\operatorname{Tr}h=0,
\quad Z\in M_3,
\]
and no four triples of two-qutrit vectors can satisfy simultaneously
\[
 (5),\ (6),\ (12),\ (23),\ (24),\ (25).
\]
This is strictly smaller than arbitrary rank-two factorization:

* the ordinary Gram equations have been solved completely;
* all linear combinations \(X(a)\) and \(Y(b)\) are injective;
* \(\lambda\) is bounded away from \(0,1\) by (23);
* every coordinate two-plane of \(h\) and \(Z\) obeys an explicit
  determinant/numerical-radius bound.

What is still missing is a relation coupling the two physical
qutrit partial contractions in (11).  Treating their Gram matrices
independently loses precisely the common two-qutrit tensor geometry.
