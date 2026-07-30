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
Thus the moment matrix at site \(i\) is
\[
\boxed{
 \mu_i(C)=
 \operatorname{Tr}_{\widehat i}
 (AC^\dagger-C^\dagger A).}
\tag{9}
\]
This matrix is Hermitian.  In local blocks its complete entries are
\[
\boxed{
 (\mu_i)_{pr}
 =
 \sum_q{\cal B}_2(C_{rq},C_{pq})
 -\sum_q{\cal B}_2(C_{qp},C_{qr}).}
\tag{9a}
\]
Hermiticity follows immediately by exchanging \(p,r\) and conjugating,
since \({\cal B}_2\) is Hermitian.  Formula (9a) also follows directly
by writing the \(pr\) block of \(AC^\dagger-C^\dagger A\); the local
trace-subtraction terms in \(A=L_iL_{\widehat i}^{\otimes2}(C)\)
cancel between the two products.

Stationarity under every one-site positive similarity is exactly
\[
 \mu_i(C)=0.
\tag{10}
\]

### 3.1 Matrix-valued circulation

The off-diagonal entries of (10) have a positivity structure which is
lost if one records only the scalar weights \(r_{pq}\).  Define
\[
\begin{aligned}
 R_{pr}&=\sum_q{\cal B}_2(C_{pq},C_{rq}),\\
 S_{pr}&=\sum_q{\cal B}_2(C_{qp},C_{qr}).
\end{aligned}
\tag{10a}
\]
Then
\[
\boxed{R\succeq0,\qquad S\succeq0.}
\tag{10b}
\]
Indeed, for every \(z\in\mathbb C^3\),
\[
\begin{aligned}
 z^\dagger Rz
 &=\sum_qQ_2\left(\sum_pz_pC_{pq}\right)\geq0,\\
 z^\dagger Sz
 &=\sum_qQ_2\left(\sum_pz_pC_{qp}\right)\geq0.
\end{aligned}
\tag{10c}
\]
Each matrix inside either endpoint form is a one-sided local
compression of \(C\), and therefore has rank at most two.  The
inequalities in (10c) are precisely the unrestricted two-copy
theorem.

Formula (9a) is equivalently
\[
 \mu_i=\overline R-S.
\tag{10d}
\]
Consequently the complete stationarity equation is the
**matrix-valued circulation law**
\[
\boxed{S=\overline R,\qquad R,S\succeq0.}
\tag{10e}
\]
The diagonal part of (10e) is (12) below.  Its off-diagonal part
equates the three row coherences with the conjugate column
coherences.  Thus a weights-only argument discards six real
stationarity equations as well as the positive-semidefinite Gram
constraints (10b).

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

### 3.2 Diagonal-filter capacity

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
most two diagonal two-copy energies \(r_{pp}\) are nonzero.  Indeed,
if only \(r_{00}=a\) and \(r_{11}=b\) can be nonzero, the part of
(13d) involving the diagonal energies is
\[
 \frac12(a+b)-\sqrt{ab}
 =\frac12(\sqrt a-\sqrt b)^2\geq0.
\tag{13e}
\]
The only uncontrolled case in (13d) therefore has all three
diagonal block energies positive.  Bounding the three \(g_{pq}\)'s
independently is not expected to settle that case; their phases and
magnitudes share the factorization in (15).

There is an invariant consequence which removes the entire singular
Gram locus, without assuming stationarity.

### Theorem 2 (a negative matrix has strict row and column Grams)

For each site form the positive matrices \(R,S\) in (10a).  If
\(\operatorname{rank}C\leq2\) and either \(R\) or \(S\) is singular
at at least one site, then
\[
\boxed{Q_3(C)\geq0.}
\tag{13f}
\]
Consequently every negative rank-two matrix must satisfy
\[
\boxed{R_i\succ0,\qquad S_i\succ0\quad(i=1,2,3).}
\tag{13g}
\]
At a local-similarity stationary negative matrix, (10e) reduces these
six strict conditions to the three common positive-definite
matrix-valued circulations \(S_i=\overline{R_i}\).

### Proof

Under a local unitary similarity, \(R\) and \(S\) transform by
unitary similarity (with the harmless conjugate representation on
one of them).  Suppose first that \(R\) is singular and choose a
local basis in which it is diagonal with, say, \(R_{22}=0\).  Since
\[
 R_{22}=\sum_qQ_2(C_{2q})=\sum_qr_{2q}
\]
and every summand is nonnegative, all \(r_{2q}\) vanish.  In
particular \(r_{22}=0\), so at most two diagonal block energies are
nonzero.  Equations (13d)--(13e) give \(Q_3(C)\geq0\).

If \(S\) is singular, diagonalize it instead.  Then
\[
 S_{22}=\sum_qQ_2(C_{q2})=0,
\]
and the identical argument again gives \(r_{22}=0\) and
nonnegativity.  This proves (13f), whose contrapositive is
(13g).  Notice that neither stationarity nor \(S=\overline R\) was
used: the pair estimate (13d) is unconditional. \(\square\)

The strictness in (13g) is sharp.  The common-qubit spin-flip endpoint
zeros have, in a support-adapted basis, a matrix-valued circulation
of the form
\[
 R=S=\operatorname{diag}(a,a,0),\qquad a>0.
\tag{13h}
\]
Thus the singular boundary contains genuine non-product zeros, while
Theorem 2 says it contains no negative matrix.

### 3.3 Exclusion of the diagonal-collapse core

The formal rank-one block Gram
\[
 {\cal B}_2(C_{pq},C_{rs})
 =\gamma\,\delta_{pq}\delta_{rs}
\tag{13i}
\]
passes the matrix-valued circulation law with
\(R=S=\gamma I_3\), but gives the negative value
\(-3\gamma/2\).  It is not realizable by one rank-two matrix.  The
following theorem excludes a substantially larger diagonal-collapse
locus.

### Theorem 3

Suppose that, in some local basis at one site,
\[
 Q_2(C_{pq})=0\qquad(p\ne q).
\tag{13j}
\]
Then every rank-two \(C\) satisfies
\[
\boxed{Q_3(C)\geq0.}
\tag{13k}
\]
Consequently, in addition to (13g), a negative matrix must have a
nonzero off-diagonal block energy at every site in every local basis.

The proof uses the established exact fixed-left equality
classification for the two-qutrit endpoint:

> If a two-qutrit two-plane \(E\) has a fixed-left endpoint kernel of
> dimension at least two, then \(E\) is a factor plane
> \(a\otimes E_0\) or \(E_0\otimes a\).

We first record the alignment information contained in that kernel.

#### Lemma 4 (kernel alignment for a factor plane)

Let \(Z:\mathbb C^2\to\mathbb C^3\otimes\mathbb C^3\) be injective
with
\[
 \operatorname{ran}Z=a\otimes E,\qquad \dim E=2.
\tag{13l}
\]
If \(W:\mathbb C^2\to\mathbb C^3\otimes\mathbb C^3\) obeys
\[
 Q_2(ZW^\dagger)=0,
\tag{13m}
\]
then
\[
 \operatorname{ran}W=b\otimes E
\tag{13n}
\]
for some \(b\in\mathbb C^3\).  The analogous statement holds with
the two physical factors exchanged.

#### Proof

After a local unitary write \(a=|0\rangle\) and
\(Z=|0\rangle\otimes Z_0\), where \(Z_0:\mathbb C^2\to E\) is
injective.  Decompose
\[
 W=\sum_{\alpha=0}^2|\alpha\rangle\otimes W_\alpha.
\]
The one-copy block pairings
\[
 {\cal B}_1(|0\rangle\langle\alpha|,
            |0\rangle\langle\beta|)
 =
 \delta_{\alpha\beta}
 -\frac12\delta_{\alpha0}\delta_{\beta0}
\]
give
\[
 Q_2(ZW^\dagger)
 =
 \frac12Q_1(Z_0W_0^\dagger)
 +\sum_{\alpha=1}^2Q_1(Z_0W_\alpha^\dagger).
\tag{13o}
\]
Every summand is nonnegative.  The sharp one-copy equality
classification says that equality forces
\[
 Z_0W_\alpha^\dagger=c_\alpha P_E.
\]
Since \(Z_0\) is injective, this is equivalent to
\[
 W_\alpha=\overline{c_\alpha}\,
 Z_0(Z_0^\dagger Z_0)^{-1}.
\]
All three slices are therefore scalar multiples of one common
injective map with range \(E\), proving (13n). \(\square\)

#### Proof of Theorem 3

Rank one is already covered by the strict all-copy rank-one theorem,
so assume that \(C\) has rank exactly two.
Take a thin factorization
\[
 C=\widehat X Y^\dagger,
\qquad
 \widehat X,Y:\mathbb C^2\to(\mathbb C^3)^{\otimes3}
\tag{13p}
\]
with both maps injective, and slice it at the selected site:
\[
 C_{pq}=\widehat X_pY_q^\dagger.
\tag{13q}
\]
If either singular plane has deficient local support at any site,
the established one-sided local-support theorem already proves
(13k).  We may therefore assume full local support.  In particular,
the three maps \(\widehat X_p\) are linearly independent, as are the
three maps \(Y_q\).

We claim first that every \(\widehat X_p\) and every \(Y_q\) is
injective.  A nonzero off-diagonal block in (13q) cannot have rank
one, because the strict rank-one estimate
\[
 Q_2(M)\geq\frac14\|M\|_2^2
\]
would contradict (13j).  Hence every nonzero off-diagonal block has
rank two.

There is at least one such block.  Otherwise all six products
\(\widehat X_pY_q^\dagger\), \(p\ne q\), vanish.  No slice can then
be injective.  Write the nonzero rank-one slices as
\[
 \widehat X_p=x_p\alpha_p^\dagger,\qquad
 Y_q=y_q\beta_q^\dagger.
\]
The six vanishing products say
\[
 \alpha_p^\dagger\beta_q=0\qquad(p\ne q).
\]
Since the auxiliary space is two-dimensional, these equations force
all three \(\alpha_p\)'s to be proportional and all three
\(\beta_q\)'s to lie in the common orthogonal line.  The full map
\(\widehat X\) would then have rank one, a contradiction.

Starting from one rank-two off-diagonal block, injectivity propagates
along the connected bipartite graph on the three \(\widehat X_p\)'s
and three \(Y_q\)'s with the diagonal matching removed.  Indeed, an
injective endpoint composed with a nonzero adjacent slice gives a
nonzero block of the same rank as that slice, and rank one has just
been excluded.  This proves the claim.

Fix \(p\).  The two independent maps \(Y_q\), \(q\ne p\), lie in the
fixed-left kernel associated with \(\widehat X_p\).  Its nullity is
at least two, so the fixed-left classification makes
\(\operatorname{ran}\widehat X_p\) a factor plane.  Lemma 4 then says
that both adjacent planes \(\operatorname{ran}Y_q\), \(q\ne p\),
factor on the same one of the two remaining physical sites and share
the same two-dimensional support on the other site.

Apply this for \(p=0,1,2\).  A two-dimensional plane cannot
simultaneously be a factor plane on opposite sides: the intersection
of \(a\otimes\mathbb C^3\) and
\(\mathbb C^3\otimes b\) is only the line
\(\mathbb C(a\otimes b)\).  The overlaps of the three pairs
\(\{Y_q:q\ne p\}\) therefore force the same factor side for every
\(p\).  They also force one common two-dimensional support \(E\) on
the other physical site.  Hence the full right singular plane
\(\operatorname{ran}Y\) has local support contained in \(E\) at that
site.  This contradicts the assumed full local support.

Thus the full-support case is impossible, and the local-support
theorem proves (13k) in every remaining case. \(\square\)

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
