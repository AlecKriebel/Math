# Universal weighted centering

This folder studies an arbitrary hypothetical 41-point kissing code
\(C=\{x_1,\ldots,x_{41}\}\subset S^4\).  It assumes no ordinary centering,
tightness, symmetry, rigidity, or finite inner-product alphabet.

The exact one-sided certificate \(B(5)\leq34\) is the imported geometric
input.  It implies that every open origin hemisphere contains at least
seven code points and
\[
0\in\operatorname{int}\operatorname{conv}(C\setminus D)
\quad\text{for every }|D|\leq6.                         \tag{1}
\]

The weighted identities below are universal.  They do not resolve the
41-point problem.  Their main value is to expose exactly what a future
weighted cap argument must control.

## 1. Full-support barycentric weights

Since \(0\) is in the interior of \(\operatorname{conv}C\), there are
weights
\[
p_i>0,\qquad \sum_i p_i=1,\qquad \sum_i p_ix_i=0.        \tag{2}
\]
Here is a direct proof retaining all points.  Put \(s=\sum_i x_i\).  For
small \(\epsilon>0\), the point
\[
-\frac{\epsilon}{1-41\epsilon}s
\]
still belongs to \(\operatorname{conv}C\).  Express it as
\(\sum_iq_ix_i\) with \(q_i\geq0\) and \(\sum_iq_i=1\), and set
\[
p_i=\epsilon+(1-41\epsilon)q_i.
\]
Then (2) holds and every \(p_i\geq\epsilon\).

This also gives an exact formula for the best minimum weight.  If
\(s\ne0\), let \(u=-s/\|s\|\) and define the radial reach
\[
\rho=\max\{r\geq0:ru\in\operatorname{conv}C\}.
\]
Then
\[
\boxed{
\max_{\substack{p\geq0,\ {\bf1}^{\mathsf T}p=1\\Xp=0}}
\min_i p_i
=\frac{\rho}{\|s\|+41\rho}.}                            \tag{3}
\]
Indeed, writing \(p_i=\mu+(1-41\mu)q_i\) shows that a given \(\mu\)
is feasible exactly when
\[
\frac{\mu\|s\|}{1-41\mu}u\in\operatorname{conv}C.
\]
If \(s=0\), the optimum is \(1/41\), attained by uniform weights.

Formula (3) identifies the quantitative gap: hemisphere counts prove
\(\rho>0\), but the current cap certificates do not provide an explicit
uniform lower bound for \(\rho\).

There is a nonconstructive uniform bound if hypothetical 41-codes exist.
The space of ordered 41-codes is compact.  Every member has the origin in
its interior by (1), so the origin-centered inradius is positive and varies
continuously.  Its minimum over this compact space is therefore positive.
This compactness statement supplies no usable rational constant and cannot
be inserted silently into a numerical inequality.

## 2. A controlled universal choice

Condition (1) gives two disjoint positive circuits.  Choose an
inclusion-minimal \(A\subset C\) with \(0\in\operatorname{conv}A\).
Carathéodory gives \(2\leq|A|\leq6\).  Delete \(A\), use (1), and choose a
second minimal circuit \(B\subset C\setminus A\), again of size at most six.
Let their normalized positive dependences be \(\alpha,\beta\).

Every coefficient in any positive dependence of unit vectors is at most
\(1/2\).  Dotting \(\sum_j\alpha_jx_j=0\) with \(x_i\) and using
\(\langle x_i,x_j\rangle\geq-1\) gives
\[
0\geq\alpha_i-\sum_{j\ne i}\alpha_j=2\alpha_i-1.
\]
Consequently
\[
p^{(0)}=\frac{\alpha+\beta}{2}
\]
is centered, is supported on at most twelve points, and satisfies
\[
\max_i p_i^{(0)}\leq\frac14.                              \tag{4}
\]

Let \(r\) be any full-support centering vector from Section 1.  The same
argument gives \(r_i\leq1/2\).  A little more care preserves the sharp
one-quarter threshold while making the support full.

Let
\[
H=\{i:p_i^{(0)}=1/4\}.
\]
Equality in the coefficient bound above forces every other point in that
circuit to be antipodal to \(x_i\).  Since a point has only one antipode, a
minimal circuit with a coefficient \(1/2\) is exactly an antipodal pair.
Each of \(A,B\) therefore contributes either zero or two indices to \(H\),
so \(|H|\leq4\).

Delete \(H\).  By (1), the origin remains in the interior of the convex
hull, so there is a centering vector \(r\) that is positive on every point
of \(C\setminus H\) and zero on \(H\).  For sufficiently small
\(\epsilon>0\),
\[
p=(1-\epsilon)p^{(0)}+\epsilon r
\]
is positive on all 41 points.  Its coordinates on \(H\) decrease strictly
below \(1/4\), while every other coordinate starts strictly below \(1/4\)
and remains so for small enough \(\epsilon\).  Thus the universal choice
can be made to satisfy
\[
\boxed{0<p_i<\frac14\quad\text{for every }i.}              \tag{5}
\]
Since \(C\) spans \(\mathbb R^5\), its weighted covariance for this choice
is positive definite.  The proof supplies no explicit common gap below
\(1/4\), and no explicit lower bound for \(p_{\min}\).

## 3. Weighted Gram and frame identities

Let \(X\) be the \(5\)-by-\(41\) coordinate matrix,
\(G=X^{\mathsf T}X\), \(D=\operatorname{diag}p\), and
\[
M=XDX^{\mathsf T},\qquad
K=D^{1/2}GD^{1/2}.
\]
Then
\[
Gp=0,\qquad K\succeq0,\qquad
\operatorname{rank}K=\operatorname{rank}M\leq5,\qquad
\operatorname{tr}M=1,\qquad K\sqrt p=0.                  \tag{6}
\]
For the full-support controlled choice, \(M\succ0\), and
\[
\operatorname{tr}M^2\geq\frac15.                         \tag{7}
\]

Put
\[
h_i=x_i^{\mathsf T}Mx_i=\sum_jp_j\langle x_i,x_j\rangle^2.
\]
The centering equation gives
\[
\sum_{j\ne i}p_j\langle x_i,x_j\rangle=-p_i.
\]
Cauchy--Schwarz and the sharp chord inequality
\[
t^2\leq\frac{1-t}{2}\qquad(-1\leq t\leq1/2)
\]
therefore yield the exact row interval
\[
\boxed{\frac{p_i}{1-p_i}\leq h_i\leq p_i+\frac12.}        \tag{8}
\]

## 4. Weighted Lorentzian and reversible chain

Define
\[
B=I+J-2G.
\]
Thus \(B_{ii}=0\), and for \(i\ne j\),
\[
B_{ij}=1-2\langle x_i,x_j\rangle\in[0,3].
\]
Weighted centering becomes the exact affine eigenvector equation
\[
\boxed{Bp={\bf1}+p.}                                     \tag{9}
\]

Set
\[
a_i=\frac{p_i}{1+p_i},\qquad A=\operatorname{diag}(a_i),
\qquad S=A^{1/2}BA^{1/2}.
\]
The rational transition matrix
\[
T_{ij}=\frac{B_{ij}p_j}{1+p_i}
\]
is row-stochastic by (9), reversible with stationary weights proportional
to \(p_i(1+p_i)\), and similar to the symmetric matrix \(S\).  Hence \(S\)
has Perron eigenvalue one and spectrum in \([-1,1]\).

Moreover,
\[
S-A=uu^{\mathsf T}
-2A^{1/2}GA^{1/2},\qquad
u=(\sqrt{a_i})_i.                                       \tag{10}
\]
For the full-support choice the rank and inertia here are exact.  Put
\(K_0=A^{1/2}GA^{1/2}\), which has rank five.  The Perron vector
\(v_i=\sqrt{p_i(1+p_i)}\) satisfies \(K_0v=0\), while
\(u^{\mathsf T}v=\sum_i p_i=1\).  Thus \(u\) has a nonzero component in
\(\ker K_0\).  Splitting off that component and taking a Schur complement
gives
\[
\operatorname{rank}(S-A)=6,\qquad
\operatorname{inertia}(S-A)=(1,5).
\]
In particular, \(S\) has at most five negative eigenvalues.
Courant--Fischer applied on the orthogonal complement of the sole positive
eigendirection in (10) gives
\[
\lambda_2(S)\leq\max_i a_i.
\]
For the controlled choice (5),
\[
\boxed{\lambda_2(S)<\frac15.}                             \tag{11}
\]

The zero diagonal and entrywise nonnegativity of \(S\) give one further
exact spectral restriction.  Write its nonzero eigenvalues as
\[
1,\quad \lambda_1,\ldots,\lambda_r,\quad
-\mu_1,\ldots,-\mu_q,
\]
where \(0<\lambda_j<1/5\), \(\mu_j>0\), and \(q\leq5\).  Put
\(P=\sum_j\lambda_j\).  Trace zero gives
\(\sum_j\mu_j=1+P\), while
\[
\operatorname{tr}S^3
=\sum_{i,j,k}S_{ij}S_{jk}S_{ki}\geq0.
\]
If \(P>0\), power mean and (11) imply
\[
\frac{(1+P)^3}{25}
\leq\sum_j\mu_j^3
\leq1+\sum_j\lambda_j^3
<1+\frac{P}{25}.
\]
The case \(P=0\) is immediate.  Since
\[
(1+P)^3-(25+P)=(P-2)(P^2+5P+12),
\]
we obtain
\[
\boxed{\sum_{\substack{\lambda\in\operatorname{Spec}S\\0<\lambda<1}}
\lambda<2.}
\]
Equivalently, the total positive spectral mass is less than three.
This sharpens the spectral description but does not contradict any lower
bound presently available.  Rank-five interlacing against the diagonal
\(A\) only controls sums of small \(a_i\)'s and cannot force the displayed
sum above two.

Since \(\operatorname{tr}S=0\), the negative eigenvalues have total
absolute value at least one.  There are at most five of them, so
\[
\boxed{\operatorname{tr}S^2\geq\frac65.}                  \tag{12}
\]
On the other hand, \(b^2\leq3b\) on \([0,3]\).  Also, with
\(a=(a_i)\),
\[
a^{\mathsf T}Bp=a^{\mathsf T}({\bf1}+p)=1,
\]
and \(0\leq a\leq p\), entrywise nonnegativity of \(B\) gives
\[
a^{\mathsf T}Ba\leq1.
\]
Consequently
\[
\boxed{
\frac65\leq
\sum_{i\ne j}
\frac{p_ip_jB_{ij}^2}{(1+p_i)(1+p_j)}
=\operatorname{tr}S^2
\leq3.}                                                   \tag{13}
\]
This is a genuine universal rank-five inequality, but its present upper
and lower bounds do not conflict.

The rank-six perturbation gives a sharper weight-sensitive form.  Put
\[
\sigma_2=\sum_i p_i^2,\qquad
\mathcal A=\sum_i a_i,\qquad
\mathcal A_2=\sum_i a_i^2,\qquad m=\max_i p_i.
\]
Let \(C_0=S-A\).  Equation (10) shows that \(C_0\) has exactly one positive
eigenvalue \(\lambda\) and at most five negative eigenvalues.  For the
Perron vector \(v_i=\sqrt{p_i(1+p_i)}\),
\[
\|v\|^2=1+\sigma_2,\qquad
v^{\mathsf T}C_0v=1.
\]
Thus \(\lambda\geq1/(1+\sigma_2)\).  Since
\(\operatorname{tr}C_0=-\mathcal A\), the absolute values of its negative
eigenvalues sum to \(\lambda+\mathcal A\).  Cauchy--Schwarz and
\(\operatorname{tr}C_0^2=\operatorname{tr}S^2+\mathcal A_2\) give
\[
\boxed{
\operatorname{tr}S^2\geq
\frac1{(1+\sigma_2)^2}
+\frac15\left(\mathcal A+\frac1{1+\sigma_2}\right)^2
-\mathcal A_2.}                                          \tag{14}
\]

There is also a sharper entrywise upper bound.  Since
\[
a\geq\frac{p}{1+m},\qquad p-a=\frac{p^2}{1+p},
\]
entrywise nonnegativity and (9) imply
\[
a^{\mathsf T}B(p-a)
=(Ba)^{\mathsf T}(p-a)
\geq\frac{\sigma_2}{1+m}.
\]
As \(a^{\mathsf T}Bp=1\),
\[
\boxed{
\operatorname{tr}S^2
\leq3a^{\mathsf T}Ba
\leq3\left(1-\frac{\sigma_2}{1+m}\right).}                \tag{15}
\]
For the controlled choice, \(m<1/4\).  The exact audit evaluates both
sides on the counterexample families below.  Even the combination of
(14)--(15) retains a substantial gap; a cap-sensitive improvement is still
needed.

## 5. Universal entrywise-quadratic transform

Define \(W_{ii}=0\) and, for \(i\ne j\),
\[
W_{ij}=B_{ij}(3-B_{ij})
=2(1-\langle x_i,x_j\rangle
-2\langle x_i,x_j\rangle^2)\in[0,9/4].
\]
Let
\[
H_2=\frac{5(G\circ G)-J}{4}.
\]
This is the degree-two harmonic Gram matrix, so
\(H_2\succeq0\) and \(\operatorname{rank}H_2\leq14\).  Exactly,
\[
\boxed{
W-4I=\frac65J-2G-\frac{16}{5}H_2.}                       \tag{16}
\]
Thus
\[
\operatorname{rank}(W-4I)\leq20,
\]
and \(W-4I\) has at most one positive eigenvalue.  For 41 points, \(4\) is
an eigenvalue of \(W\) with multiplicity at least 21.  No centering or
tightness assumption is used here.

Weighted centering additionally gives
\[
\boxed{Wp=2{\bf1}+4p-4h.}                                \tag{17}
\]
Combining (8) and (15),
\[
0\leq(Wp)_i\leq
2-\frac{4p_i^2}{1-p_i}.                                  \tag{18}
\]
Equations (16)--(18) are the most concrete surviving coupling between
rank five and positive barycentric weights.  A contradiction still needs a
lower bound on weighted mass in geometrically constrained neighborhoods.

## 6. Exact counterexamples to careless weight selection

The normalized \(D_5\) root system is a genuine rank-five 40-point kissing
code.  Its exact open-origin-hemisphere depth is eight.  Fix one antipodal
root pair \(\{\pm v\}\).

For \(0<\epsilon<1\), assign
\[
p_{\pm v}=\frac{1-\epsilon}{2},\qquad
p_x=\frac{\epsilon}{38}\quad(x\ne\pm v).                  \tag{17}
\]
These are full-support centering weights.  Since the twenty unoriented
\(D_5\) root lines satisfy
\(\sum_{\ell}v_\ell v_\ell^{\mathsf T}=4I\), the covariance is
\[
M_\epsilon=
\frac{4\epsilon}{19}I+
\left(1-\frac{20\epsilon}{19}\right)vv^{\mathsf T}.       \tag{18}
\]
Its eigenvalues are
\[
1-\frac{16\epsilon}{19},\qquad
\frac{4\epsilon}{19}\quad\text{with multiplicity four}.  \tag{19}
\]
Thus a full-support centering choice can have
\(\max p_i\to1/2\), \(\min p_i\to0\), and
\(\lambda_{\min}(M)\to0\), even at depth eight.

Reversing the masses,
\[
p_{\pm v}=\frac{\epsilon}{2},\qquad
p_x=\frac{1-\epsilon}{38},
\]
gives a full-support family with a prescribed pair of weights tending to
zero.  Finally, weights \(1/2,1/2\) on \(\{\pm v\}\) give a centered
two-point support and rank-one covariance.

These examples refute claims about **every** centering vector.  They do not
refute the controlled existence result (5), the max-min choice (3), or a
future theorem selecting weights by a new optimization principle.  They
also have 40 rather than 41 points, so a statement using a genuinely
cardinality-41 invariant remains possible.

## 7. Deletion depth alone gives no quantitative balance

There is also an exact parametric obstruction to extracting a numerical
weight bound from deletion-interiority alone.  Fix twenty distinct rational
numbers \(t\in[-1,1]\), and for \(\epsilon>0\) put
\[
v(t)=(1,t,t^2,t^3,\epsilon t^4).
\]
Take the forty normalized points
\(\{\pm v(t)/\|v(t)\|\}\) and append \(e_5\).

Any five of the twenty lines span \(\mathbb R^5\), because their determinant
is \(\epsilon\) times a nonzero Vandermonde determinant.  Consequently:

- every origin hyperplane contains at most four lines, so every open
  origin hemisphere contains at least sixteen points;
- after deleting any six points, at least fourteen antipodal pairs remain,
  and any five intact pairs span \(\mathbb R^5\); hence the origin remains
  in the interior of the remaining convex hull.

Nevertheless, the forty paired points cancel in the unweighted sum, so the
centroid sum is \(s=e_5\).  Every paired point has fifth coordinate of
absolute value at most \(\epsilon\).  The radial reach \(\rho\) of the
convex hull in direction \(-e_5\) is therefore at most \(\epsilon\).
Formula (3) now gives
\[
\max_p\min_i p_i
=\frac{\rho}{1+41\rho}
\leq\epsilon.
\]
Letting \(\epsilon\to0\) proves that even deletion-six interiority and
open-hemisphere depth sixteen supply no uniform quantitative barycentric
lower bound by themselves.

This family is deliberately **not** a kissing code: nearby moment-curve
points have inner product greater than \(1/2\).  The exact audit checks one
violating pair at \(\epsilon=1/1000\).  Thus this is a counterexample only
to a depth-only lemma; a bound that genuinely uses the kissing inequalities
remains possible.

## 8. Current bottleneck

The cap results supply strong unweighted facts: every vertex has at least
seven negative and six positive neighbors, every open hemisphere has at
least seven points, and many common-neighbor strata have bounded
cardinality.  None of those facts presently lower-bounds the total
\(p\)-mass of the corresponding set.

The controlled choice (5) bounds \(p_{\max}\), but it does not bound
\(p_{\min}\).  The compactness observation after (3) gives a qualitative
uniform lower bound but no explicit certified constant.  Therefore
substituting counts for weighted masses in (13), (15), or (16) would be an
invalid step.

A materially new continuation would need one of:

1. an explicit radial/inradius bound strong enough to quantify (3);
2. a weight-selection theorem that preserves a definite amount of mass in
   every cap-relevant neighborhood;
3. a rank inequality using (9), (10), or (14) that is independent of
   \(p_{\min}\).

## Reproduction

The exact \(D_5\) counterexamples, the deletion-depth construction, and all
rational weighted identities used by the audit are checked with

```sh
python3 \
  experiments/universal_weighted_centering/verify_weighted_centering.py
python3 -m unittest discover \
  -s experiments/universal_weighted_centering \
  -p 'test_*.py' -v
```

The verifier uses only Python's standard library.  Its imported depth-eight
certificate is hash-pinned.

Current SHA-256 values are

```text
96723982ba06defeda374cf1a0b9fe80d37bb08fe33be095ede7305541a848bd  weighted_centering_counterexamples.json
729e2d0f59f233aac07ee17a663f9a00f74245930860927814905e0669452ce6  deletion_depth_weight_counterexample.json
1fd54b16ca19794470e46eda445a279abc0893ed20fb5a5193cbec0c87c4e4c1  verify_weighted_centering.py
0cc23e145d7cf50606435b41ecc751220c1489412bca3887f1bf41c494d175fa  test_weighted_centering.py
```
