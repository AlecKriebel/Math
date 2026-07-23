# Quantitative audit of the root-system zero-slack obstruction

Status: **PROVED**, conditional only on the standard ADE classification of
finite crystallographic simply-laced root systems.

This note audits Lemma 6 of `sparse_deep_graph_stability.md` and makes its
compactness step effective.  It does not finish the five-dimensional
kissing-number problem: the explicit constant obtained here is much too
small for the remaining global energy margin.

## 1. A hypothesis that must be explicit

The phrase “distinct code points” in Lemma 6 must mean that the core points
also satisfy

\[
 \langle z_a,z_b\rangle\leq \frac12\qquad(a\ne b).       \tag{1}
\]

This is true in the intended application, where all the vectors come from
one spherical code.  Merely saying that the \(z_a\)'s are distinct does not
describe a compact constraint set: the complement of the collision
diagonals is open.  Thus the compactness sentence in the original proof is
valid only after (1), or another closed separation condition, is included
explicitly.

The zero-slack root-system argument itself is otherwise correct.  In
particular, for \(v_i=\sqrt2u_i\), the integral Gram matrix makes the
integer span a genuine lattice: every squared norm in that span is an
integer, so nonzero vectors have norm bounded away from zero.  The set of
norm-two lattice vectors is therefore finite and is closed under the
corresponding reflections.

## 2. An effective separation theorem

Put

\[
 {\cal Z}=\{-1,0,1\},\qquad
 d(x)=\min_{k\in{\cal Z}}|x-k|,
\]

and set

\[
 \eta=\frac1{7200}.                                   \tag{2}
\]

### Theorem 1

Let \(r\in\{16,17,18\}\), let \(q=41-2r\), and let
\(u_1,\ldots,u_r,z_1,\ldots,z_q\in S^4\).  Assume only the core code
condition (1).  Define the root-alphabet defect

\[
 Q=
 \sum_{i<j}d(2\langle u_i,u_j\rangle)^2+
 \sum_{i,a}d(2\langle u_i,z_a\rangle)^2.              \tag{3}
\]

Then

\[
 Q>\eta^2=\frac1{51840000}.                            \tag{4}
\]

#### Proof

Suppose instead that \(Q\leq\eta^2\).  Round every controlled scaled inner
product in (3) to a nearest member of \({\cal Z}\).  Thus every rounded
entry differs from the corresponding entry by at most \(\eta\).

We use the following elementary determinant estimate.  Under the present
contradictory assumption, every controlled off-diagonal entry of the
actual scaled Gram matrix has absolute value at most \(1+\eta\), and every
rounded off-diagonal entry has absolute value at most one.  Thus every
column of any submatrix of order at most six has Euclidean norm less than
\(3001/1000\).  A difference column has norm at most
\(\sqrt6\eta<(49/20)\eta\).  Multilinearity in the columns and Hadamard's
inequality therefore give, for \(k\leq6\),

\[
\begin{split}
 |\det M-\det N|
 &\leq k\,\frac{49}{20}
       \left(\frac{3001}{1000}\right)^{k-1}\eta\\
 &\leq 6\,\frac{49}{20}
       \left(\frac{3001}{1000}\right)^5\eta
 <3600\eta=\frac12.                                  \tag{5}
\end{split}
\]

Consider first the scaled Gram matrix of the \(u_i\)'s, with diagonal two,
and its rounded integral matrix \(R\).  Every \(6\times6\) minor of the
actual Gram matrix vanishes, since the vectors lie in dimension five.
Equation (5) and integrality show that every \(6\times6\) minor of \(R\)
vanishes.  Hence
\(\operatorname{rank}R\leq5\).  For every principal minor of order at most
five, (5) gives an error strictly smaller than \(1/2\); the corresponding
actual principal minor is nonnegative.  The rounded principal minor is an
integer, so it is nonnegative.  All larger principal minors vanish by the
rank bound.  The principal-minor criterion therefore gives

\[
 R\succeq0,\qquad \operatorname{rank}R\leq5.           \tag{6}
\]

The same argument applies to the rounded scaled Gram matrix \(R_a\) of
\(u_1,\ldots,u_r,z_a\), separately for every \(a\).

Realize \(R\) as the Gram matrix of vectors
\(v_1,\ldots,v_r\) of norm squared two.  Their mutual inner products are in
\(\{0,\pm1\}\).  Their integral span has at least \(2r\geq32\) distinct
norm-two roots.  By the ADE classification, a simply-laced root system of
rank at most five with at least 32 roots must have rank five and type
\(D_5\).  In particular, \(R\) has rank five and its norm-two root system
has exactly 40 oriented roots.

Each \(R_a\) adjoins one more norm-two root to this \(D_5\) system.  Its
norm-two root system is still simply laced and has rank at most five.
The ADE classification again forces it to be the same \(D_5\) root system.
The adjoined root cannot be one of \(\pm v_i\), because all of its rounded
inner products with the base roots belong to \(\{0,\pm1\}\), whereas its
inner product with \(v_i\) would then be \(\pm2\).  Thus every \(z_a\)
receives one of only

\[
 40-2r
\]

oriented root labels.  Since \(q=41-2r\), two core points, say \(z_a,z_b\),
receive the same label.  Equivalently, their rounded inner products with
all the spanning base roots are identical.

It remains to transfer that collision back to the actual vectors.  Choose
five base roots whose \(5\times5\) principal submatrix \(R_I\) is positive
definite.  It has integral determinant at least one.  Every eigenvalue is
at most six by the absolute row-sum bound, hence

\[
 \lambda_{\min}(R_I)\geq 6^{-4}=\frac1{1296}.          \tag{7}
\]

Let \(P_I\) be the actual scaled Gram matrix on the same five indices.
Its off-diagonal entrywise distance from \(R_I\) is at most \(\eta\), so
its operator-norm distance is at most \(4\eta\).  Weyl's inequality gives

\[
 \lambda_{\min}(P_I)
 \geq\frac1{1296}-\frac4{7200}
 =\frac7{32400}>\frac1{5000}.                         \tag{8}
\]

Write \(v_i^*=\sqrt2u_i\), \(w_a=\sqrt2z_a\), and
\(w_b=\sqrt2z_b\).  The common rounded label implies, for each \(i\in I\),

\[
 |\langle v_i^*,w_a-w_b\rangle|\leq2\eta.
\]

Using the five-vector frame operator and (8),

\[
 \|w_a-w_b\|^2
 < 5000\sum_{i\in I}
       \langle v_i^*,w_a-w_b\rangle^2
 \leq100000\eta^2=\frac5{2592}<2.                     \tag{9}
\]

Since both \(w_a,w_b\) have norm squared two, (9) yields

\[
 \langle z_a,z_b\rangle
 =1-\frac14\|w_a-w_b\|^2>\frac12,
\]

contrary to (1).  This proves (4). \(\square\)

## 3. An explicit value for the gap in Lemma 6

Let

\[
 h(t)=t^2(t^2-\tfrac14).
\]

For \(|t|\leq1/2\), put

\[
 \delta(t)=\operatorname{dist}
 \bigl(t,\{0,\tfrac12,-\tfrac12\}\bigr).
\]

A direct split into \(|t|\leq1/4\) and \(1/4\leq|t|\leq1/2\) gives

\[
 -h(t)\geq\frac{\delta(t)^2}{8}.                       \tag{10}
\]

Consequently

\[
 d(2t)^2=4\delta(t)^2\leq32[-h(t)].                   \tag{11}
\]

### Corollary 2

Under the hypotheses of Lemma 6, with the core code condition (1) stated
explicitly,

\[
 A+B<-\varepsilon,\qquad
 \varepsilon=\frac{\eta^2}{32}
 =\frac1{1658880000}.                                 \tag{12}
\]

Thus one may take

\[
 \boxed{\varepsilon_{16}=\varepsilon_{17}
 =\varepsilon_{18}=\frac1{1658880000}}.
\]

Indeed, summing (11) over all terms of \(A+B\) gives
\(Q\leq32[-(A+B)]\), and Theorem 1 gives (12).

The constant is intentionally crude.  Its role is to replace qualitative
compactness with an independently checkable rational separation, not to
claim that the true maximum is close to this value.

## 4. Robust form for near-antipodal matching pairs

The same proof gives a stability statement even when some relevant
absolute inner products slightly exceed \(1/2\).  For every relevant
inner product \(t\), put

\[
 e(t)=(|t|-\tfrac12)_+,\qquad
 T_1=\sum e(t),\qquad T_2=\sum e(t)^2.                 \tag{13}
\]

For \(|t|>1/2\),

\[
 d(2t)^2=4e(t)^2,\qquad
 0<h(t)\leq\frac72e(t),                               \tag{14}
\]

where the second inequality follows from
\(\max_{[1/2,1]}h'(t)=7/2\).  Combining (4), (11), and
(14) gives the robust estimate

\[
 A+B<
 \frac72T_1+\frac18T_2-\varepsilon.                   \tag{15}
\]

For matching-edge parameters
\(\langle a_i,b_i\rangle=-p_i\), put
\(s_i=1-p_i\) and \(S=\sum_i s_i\).  The projection estimates (17)--(18)
of `sparse_deep_graph_stability.md` imply

\[
 e(\langle u_i,u_j\rangle)
 \leq\frac{s_i+s_j}{2},\qquad
 e(\langle u_i,z_a\rangle)\leq\frac{s_i}{3}.           \tag{16}
\]

Here \(0\leq s_i\leq1/2\) was used.  Hence, with \(q=41-2r\),

\[
 T_1\leq\kappa_r S,\qquad
 T_2\leq\kappa_r^2S^2,\qquad
 \kappa_r=\frac{r-1}{2}+\frac{q}{3},                  \tag{17}
\]

and therefore

\[
 A+B<
 \frac72\kappa_rS+\frac18\kappa_r^2S^2-\varepsilon,   \tag{18}
\]

where

\[
 \kappa_{16}=\frac{21}{2},\qquad
 \kappa_{17}=\frac{31}{3},\qquad
 \kappa_{18}=\frac{61}{6}.
\]

Equation (18) is a fully explicit robust version of the root-system
obstruction.  Numerically, however,
\(\varepsilon\approx6.0282\cdot10^{-10}\), so this crude estimate is far
too weak when combined with the present total midpoint bound.  A useful
completion of the sparse-deep-graph route still requires a substantially
stronger projective stability inequality or a finite exact optimization
around the \(D_5\) root system.

## 5. Dependency map

The proof uses:

1. the elementary determinant perturbation estimate (5);
2. the rank-five vanishing of all \(6\times6\) Gram minors;
3. the principal-minor characterization of positive semidefiniteness;
4. the ADE root-system classification in ranks at most five;
5. the closed core separation condition (1);
6. the elementary scalar estimates (10) and (14).

No numerical optimizer, root-system uniqueness assumption about the
40-point kissing configuration, or unverified finite enumeration is used.
