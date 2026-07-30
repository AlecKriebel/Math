# Local-similarity convexity and the balanced three-cycle core

## Status

This note proves an exact convexity theorem for the unrestricted
three-copy endpoint form.  It is different from the false
reciprocal-filter convexity statements for determinant ratios:
\(Q_3\) itself is convex along every one-site positive-similarity
geodesic.

The theorem reduces a stationary square-zero counterexample to one
explicit balanced block inequality.  That last inequality is not
proved here.  An exact rank-four block example shows that two-copy
positivity and flow balance alone do not prove it; the common global
rank-two factorization remains essential.

## 1. The recursion

Fix a physical site and write a three-copy coefficient matrix in
local blocks
\[
 C=(C_{pq})_{p,q=0}^2,\qquad C_{pq}\in M_9.
\]
The partial-trace formula gives
\[
\boxed{
 Q_3(C)
 =
 \sum_{p,q=0}^2Q_2(C_{pq})
 -\frac12Q_2\left(\sum_{p=0}^2C_{pp}\right).}
\tag{1}
\]
Indeed, subsets which do not contain the displayed site give the
first term, while subsets which contain it give the second.

Every block is a left and right compression of \(C\), so
\[
 \operatorname{rank}C_{pq}\leq\operatorname{rank}C.
\tag{2}
\]
The established unrestricted two-copy theorem therefore gives
\[
 r_{pq}:=Q_2(C_{pq})\geq0
 \quad\text{if }\operatorname{rank}C\leq2.
\tag{3}
\]

## 2. Exact geodesic convexity

Let \(K=K^\dagger\in M_3\), acting at the displayed site, and put
\[
 C(t)=e^{tK}Ce^{-tK}.
\tag{4}
\]
This path preserves matrix rank.  It also preserves \(C^2=0\), when
that condition is present.

### Theorem 1

If \(\operatorname{rank}C\leq2\), then
\[
\boxed{\frac{d^2}{dt^2}Q_3(C(t))\geq0\qquad(t\in\mathbb R).}
\tag{5}
\]
More precisely, in an eigenbasis
\[
 K=\operatorname{diag}(k_0,k_1,k_2),
\]
one has
\[
\boxed{
\begin{aligned}
 Q_3(C(t))
 &=D+\sum_{p\ne q}
 e^{2t(k_p-k_q)}r_{pq},\\
 D&=\sum_pr_{pp}
 -\frac12Q_2\left(\sum_pC_{pp}\right),
\end{aligned}}
\tag{6}
\]
and hence
\[
\boxed{
 Q_3''(C(t))
 =
 4\sum_{p\ne q}(k_p-k_q)^2
 e^{2t(k_p-k_q)}r_{pq}\geq0.}
\tag{7}
\]

### Proof

Local unitary similarities preserve all simultaneous partial-trace
norms, so diagonalize \(K\).  Then
\[
 C_{pq}(t)=e^{t(k_p-k_q)}C_{pq}.
\]
The diagonal contraction \(\sum_pC_{pp}(t)\) is independent of
\(t\).  Substitute these facts in (1) and use homogeneity of \(Q_2\)
to obtain (6).  Equations (3) and direct differentiation give
(7). \(\square\)

The same proof gives a conditional tensorization statement.  If the
\((n-1)\)-copy endpoint is nonnegative on every rank-two matrix, then
\(Q_n\) is convex along every one-site positive-similarity geodesic
on the rank-two variety.

## 3. The moment matrix and balanced flows

Let
\[
 A=L^{\otimes3}(C).
\]
Differentiating (4) invariantly gives
\[
 \left.\frac d{dt}Q_3(C(t))\right|_{t=0}
 =
 2\operatorname{Re}\operatorname{Tr}
 K\,\operatorname{Tr}_{\widehat i}
 (AC^\dagger-C^\dagger A).
\tag{8}
\]
Thus the Hermitian moment matrix at site \(i\) is
\[
\boxed{
 \mu_i(C)=
 \operatorname{Herm}\operatorname{Tr}_{\widehat i}
 (AC^\dagger-C^\dagger A).}
\tag{9}
\]
Stationarity under every one-site positive similarity is exactly
\[
 \mu_i(C)=0.
\tag{10}
\]

In an eigenbasis of a diagonal test generator, the diagonal entries
of (9) are
\[
 (\mu_i)_{pp}
 =
 \sum_q(r_{pq}-r_{qp}).
\tag{11}
\]
Consequently stationarity implies that the nonnegative directed
weights \(r_{pq}\) form a circulation:
\[
\boxed{\sum_qr_{pq}=\sum_qr_{qp}\qquad(p=0,1,2).}
\tag{12}
\]

Every circulation on three vertices is a sum of two-cycles and one
oriented three-cycle.  Explicitly, after possibly reversing all
arrows, there are
\[
 a_{01},a_{12},a_{20},\tau\geq0
\]
such that
\[
\begin{array}{lll}
 r_{01}=a_{01}+\tau,&r_{10}=a_{01},\\
 r_{12}=a_{12}+\tau,&r_{21}=a_{12},\\
 r_{20}=a_{20}+\tau,&r_{02}=a_{20}.
\end{array}
\tag{13}
\]
This follows by subtracting
\(\min(r_{pq},r_{qp})\) on every unoriented edge.  The residual
balance equations force the three surviving arrows to have the same
weight and the same cyclic orientation.

For a zero which does not generate a nearby negative witness,
(8) must vanish at all three sites.  Theorem 1 then says that the
zero is a global minimum on each individual one-parameter local
similarity geodesic.  Thus an endpoint-zero classification may
restrict immediately to the common balanced system (9)--(13).

### 3.1 Diagonal-filter capacity

The cycle decomposition has a second exact use.  For diagonal local
filters \(D_x=\operatorname{diag}(x_0,x_1,x_2)\) and
\(D_y=\operatorname{diag}(y_0,y_1,y_2)\), put
\[
 c_p=x_py_p,\qquad A_p=C_{pp}.
\]
The recursion gives
\[
\boxed{
 Q_3(D_xCD_y)
 =
 \sum_{p,q}|x_p|^2|y_q|^2r_{pq}
 -\frac12Q_2\left(\sum_pc_pA_p\right).}
\tag{13a}
\]
If the balanced flow is written as in (13), weighted arithmetic--geometric
mean on each cycle gives
\[
\boxed{
\begin{aligned}
 \sum_{p,q}|x_p|^2|y_q|^2r_{pq}
 \geq{}&
 \sum_pr_{pp}|c_p|^2
2\sum_{p<q}a_{pq}|c_pc_q|\\
&+3\tau|c_0c_1c_2|^{2/3}.
\end{aligned}}
\tag{13b}
\]
For a two-cycle this is the two-term arithmetic--geometric mean;
for the oriented three-cycle, the product of the three summands is
\(|c_0c_1c_2|^2\).  Equality holds at \(x_p=y_p=1\).

There is also a useful exact two-coordinate consequence of the
local-support boundary theorem.  Let
\[
 g_{pq}={\cal B}_2(A_p,A_q).
\]
Choose both diagonal filters to be supported on \(\{p,q\}\), and
optimize their reciprocal magnitudes while keeping \(c_p,c_q\)
fixed.  Boundary positivity and the binary copositivity criterion
give
\[
\boxed{
 |g_{pq}|
 \leq
 2\sqrt{r_{pq}r_{qp}}+\sqrt{r_{pp}r_{qq}}.}
\tag{13c}
\]
Indeed, the two crossed block terms have minimum
\(2\sqrt{r_{pq}r_{qp}}|c_pc_q|\).  After choosing the adverse
relative phase, the remaining binary quadratic has diagonal
coefficients \(r_{pp}/2,r_{qq}/2\), which proves (13c).

Summing (13c) yields the rigorous lower bound
\[
\boxed{
\begin{aligned}
 Q_3(C)\geq{}&
 \frac12\sum_pr_{pp}
 +\sum_{p<q}
 \left(\sqrt{r_{pq}}-\sqrt{r_{qp}}\right)^2\\
 &-\sum_{p<q}\sqrt{r_{pp}r_{qq}}.
\end{aligned}}
\tag{13d}
\]
In particular, a stationary block system is nonnegative whenever at
most one diagonal two-copy energy \(r_{pp}\) is nonzero.  The only
uncontrolled term in (13d) is the coherent interaction among two or
three positive diagonal block energies.  Bounding the three
\(g_{pq}\)'s independently is not expected to settle that case; their
phases and magnitudes share the factorization in (15).

## 4. The exact remaining block inequality

For a square-zero rank-two matrix write
\[
 C=XY^\dagger,\qquad X,Y:\mathbb C^2\to
 (\mathbb C^3)^{\otimes3},\qquad Y^\dagger X=0.
\tag{14}
\]
At the displayed site let \(X_p,Y_p:\mathbb C^2\to\mathbb C^9\)
be its three slices.  Then
\[
 C_{pq}=X_pY_q^\dagger,\qquad
 T=\sum_pX_pY_p^\dagger.
\tag{15}
\]
Equations (1) and (3) become
\[
 Q_3(C)=
 \sum_{p,q}Q_2(X_pY_q^\dagger)-\frac12Q_2(T).
\tag{16}
\]

After the similarity moment has been balanced, the remaining
one-site assertion is the following fully explicit lemma:
\[
\boxed{
 Q_2\left(\sum_pX_pY_p^\dagger\right)
 \leq
 2\sum_{p,q}Q_2(X_pY_q^\dagger),}
\tag{17}
\]
subject to \(Y^\dagger X=0\), the common two-column factorization
(15), and the circulation equations (12), in every local basis
selected by (9).  Equality in (17) is the stationary-zero case.

This is smaller than the original \(27\times27\) optimization:
all live quantities are two-copy endpoint values of nine matrices
sharing six \(9\times2\) factors.  It is still nonlinear, because
discarding that common factorization is invalid.

## 5. Exact obstruction to a weights-only proof

Here is a rational rank-four block system which satisfies two-copy
positivity and perfect flow balance but violates (17).

On two qutrit copies put
\[
\begin{aligned}
 P&=\operatorname{diag}(1,1,0),&
 Q&=\operatorname{diag}(0,1,1),\\
 R&=|0\rangle\langle0|,&
 S&=|1\rangle\langle1|,\\
 A&=P\otimes R,&B&=Q\otimes S.
\end{aligned}
\tag{18}
\]
Tensor factorization gives
\[
 Q_2(A)=Q_2(B)=0.
\tag{19}
\]
Moreover
\[
\begin{aligned}
 {\cal B}_1(P,Q)&=\operatorname{Tr}(PQ)
 -\frac12\operatorname{Tr}P\operatorname{Tr}Q=-1,\\
 {\cal B}_1(R,S)&=-\frac12,
\end{aligned}
\]
so
\[
 {\cal B}_2(A,B)=\frac12,\qquad Q_2(A+B)=1.
\tag{20}
\]
Take the formal local block matrix with
\[
 C_{00}=A,\qquad C_{11}=B,
\qquad C_{pq}=0\text{ otherwise}.
\tag{21}
\]
All weights \(r_{pq}\) vanish and are therefore balanced, but (1)
gives
\[
 Q_3(C)=-\frac12.
\tag{22}
\]
The global block matrix in (21) has rank four, not rank two.  Thus it
is not a Werner witness; it proves exactly that nonnegativity of the
nine coefficients and the cycle equations do not control the
constant diagonal term.  A completion of (17) must use the common
rank-two factorization (15).

## 6. Orbit geometry

For a fixed local basis, the nonconstant part of (6) is a finite
exponential circulation energy.  If its directed support graph is
strongly connected, it is coercive on
\(\{k_0+k_1+k_2=0\}\), and its unique critical point is the balanced
flow (12).  If it is not strongly connected, a separating
one-parameter subgroup sends the infimum to the orbit boundary.

For a generic one-parameter subgroup, the Grassmannian limit of a
two-plane is supported on at most two local weight spaces: a
two-plane has at most two leading independent weight components.
Hence the escaping alternative lands on the already-settled
local-support-deficient boundary.  The unsettled interior is the
balanced, or polystable, alternative represented by (9), (12), and
(17).

This orbit statement identifies the gap; it does not fill it.
Convexity controls every individual similarity orbit, but a convex
function may have a negative interior minimum even when its projective
orbit boundary is nonnegative.  Excluding precisely that balanced
minimum is the remaining common-factor problem.
