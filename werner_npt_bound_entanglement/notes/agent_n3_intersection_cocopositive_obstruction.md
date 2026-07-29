# Exact qutrit GHZ obstruction to a copositive Schur certificate

## Status

This note records an exact **no-go for one proof route** toward the
three-copy intersection-one inequality.  It is not a counterexample to
that inequality and is not a Werner distillation witness.

For a fixed anchor \(w\), the intersection-one theorem is equivalent to
positivity of a linear map
\[
 \Phi_w(V)=a\,{\cal K}(V)-A_wVA_w,
 \qquad
 a=Q_3(P_w),\quad
 A_w={\cal L}(P_w).
 \tag{1}
\]
A natural reflection-positivity strengthening would prove that the
partially transposed Choi matrix \(J(\Phi_w)^\Gamma\) is positive, or
even merely two-block-positive.  The latter already fails for the
qutrit GHZ anchor: an explicit Schmidt-rank-two vector has expectation
\[
 \boxed{-\frac5{72}.}
 \tag{2}
\]

The independent exact checker is
`verification/verify_n3_intersection_cocopositive_obstruction.py`.

## 1. The target as positivity of one linear map

On
\[
 {\cal H}=(\mathbb C^3)^{\otimes3},
 \tag{3}
\]
put
\[
 L_i(X)=X-\frac12\operatorname{Tr}(X)I,\qquad
 M_i(X)=\operatorname{Tr}(X)I-\frac12X,
 \tag{4}
\]
and
\[
 {\cal L}=L_1\otimes L_2\otimes L_3,\qquad
 {\cal K}=M_1\otimes M_2\otimes M_3.
 \tag{5}
\]
For a unit vector \(w\), write
\[
 A_w={\cal L}(P_w),\qquad a=\langle w,A_ww\rangle.
 \tag{6}
\]
The established Schur reduction says that, for every unit \(u\), the
intersection-one inequality for all \(v\) is
\[
 aK_u-|A_wu\rangle\langle A_wu|\succeq0,
 \qquad K_u={\cal K}(P_u).
 \tag{7}
\]
Since \(A_w=A_w^\dagger\),
\[
 \Phi_w(P_u)
 =a{\cal K}(P_u)-A_wP_uA_w
 =aK_u-|A_wu\rangle\langle A_wu|.
 \tag{8}
\]
Rank-one positive operators generate the positive cone, so the
intersection-one target for this fixed \(w\) is exactly positivity of
the map \(\Phi_w\).

## 2. The tempting copositive strengthening

Use the Choi convention
\[
 J(\Lambda)=\sum_{r,s}|r\rangle\langle s|
                 \otimes\Lambda(|r\rangle\langle s|)
 \tag{9}
\]
and transpose the first Choi factor.  For one physical site,
\[
 J(M)^\Gamma=I-\frac12F.
 \tag{10}
\]
Consequently
\[
 J({\cal K})^\Gamma
 =Y:=\bigotimes_{i=1}^3\left(I-\frac12F_i\right)\succeq0.
 \tag{11}
\]
For the map \(V\mapsto A_wVA_w\), Hermiticity of \(A_w\) gives
\[
 J(V\mapsto A_wVA_w)
 =|\operatorname{vec}A_w\rangle
   \langle\operatorname{vec}A_w|.
 \tag{12}
\]
Thus
\[
 \boxed{
 H_w:=J(\Phi_w)^\Gamma
 =aY-
 \left(
 |\operatorname{vec}A_w\rangle
 \langle\operatorname{vec}A_w|
 \right)^\Gamma.}
 \tag{13}
\]
Showing \(H_w\succeq0\) would prove a complete-copositivity
strengthening of the target.  Even showing \(H_w\) two-block-positive
would be a substantial strengthening.  The next section disproves
both.

## 3. Exact GHZ calculation

Let
\[
 w=\frac1{\sqrt3}
 \left(|000\rangle+|111\rangle+|222\rangle\right),
 \qquad
 g_r=|rrr\rangle.
 \tag{14}
\]
Its one-site and two-site reductions are
\[
 \rho_i^w=\frac13I_3,\qquad
 \rho_{ij}^w=\frac13\sum_{r=0}^2|rr\rangle\langle rr|.
 \tag{15}
\]
The complementary partial-trace expansion is
\[
 A_w=P_w
 -\frac12\sum_i I_i\otimes\rho_{\bar i}^w
 +\frac14\sum_{i<j}I_{ij}\otimes\rho_{\overline{ij}}^w
 -\frac18I.
 \tag{16}
\]
On the GHZ subspace
\[
 G=\operatorname{span}\{g_0,g_1,g_2\},
 \tag{17}
\]
each of the three two-site-reduction terms in the first sum acts as
\(I_G/3\), while each of the three one-site-reduction terms in the
second sum is \(I_G/3\).  Therefore
\[
 \boxed{A_w|_G=P_w-\frac38I_G.}
 \tag{18}
\]
In the ordered basis \((g_0,g_1,g_2)\), this is
\[
 A_w|_G=
 \begin{pmatrix}
 -1/24&1/3&1/3\\
 1/3&-1/24&1/3\\
 1/3&1/3&-1/24
 \end{pmatrix}.
 \tag{19}
\]
In particular,
\[
 A_ww=\frac58w,\qquad a=\frac58.
 \tag{20}
\]

Now take the two-replica vector
\[
 q=|g_0\rangle\otimes|g_0\rangle
   +|g_1\rangle\otimes|g_1\rangle.
 \tag{21}
\]
Across the two Choi replicas its coefficient matrix is
\(\operatorname{diag}(1,1,0,\ldots,0)\), so
\[
 \operatorname{SR}(q)=2.
 \tag{22}
\]
Each displayed summand in (21) is an eigenvector of \(Y\) with
eigenvalue \(2^{-3}=1/8\), and the two summands are orthogonal.  Hence
\[
 \langle q,aYq\rangle
 =\frac58\frac28
 =\frac5{32}.
 \tag{23}
\]

Put
\[
 R=\left(
 |\operatorname{vec}A_w\rangle
 \langle\operatorname{vec}A_w|
 \right)^\Gamma.
 \tag{24}
\]
For Hermitian \(A_w\),
\[
 \langle x\otimes x|R|y\otimes y\rangle
 =|\langle x,A_wy\rangle|^2.
 \tag{25}
\]
Using the \(2\times2\) leading block of (19),
\[
 \begin{aligned}
 \langle q,Rq\rangle
 &=2\left(\frac1{24}\right)^2
   +2\left(\frac13\right)^2\\
 &=\frac{65}{288}.
 \end{aligned}
 \tag{26}
\]
Combining (13), (23), and (26) gives the announced exact obstruction:
\[
 \boxed{
 \langle q,H_wq\rangle
 =\frac5{32}-\frac{65}{288}
 =-\frac5{72}<0.}
 \tag{27}
\]

## 4. What this does and does not establish

Equation (27) proves that \(J(\Phi_w)^\Gamma\) is not positive and is
not even two-block-positive.  Therefore the intersection-one theorem
cannot be proved by establishing complete copositivity of \(\Phi_w\),
nor by the weaker proposed certificate that its partially transposed
Choi matrix is two-block-positive.

This is **not** a violation of positivity of \(\Phi_w\).  Positivity of
\(\Phi_w\), which is exactly the desired intersection-one assertion,
tests the ordinary Choi matrix \(J(\Phi_w)\) on product vectors.
The obstruction instead tests \(J(\Phi_w)^\Gamma\) on an entangled
Schmidt-rank-two vector.  Partial transpose does not preserve that
test class.  Thus (27) rules out a reflection/cocopositivity route and
leaves the original Schur inequality open.
