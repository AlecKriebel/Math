# A compact maximum-volume-basis reduction for a hypothetical 41-code

This note gives an exact, classification-free semialgebraic formulation of the
existence of a 41-point spherical code in \(S^4\) with maximal inner product
\(1/2\).  It neither assumes nor guesses a contact graph.

## 1. An exact four-dimensional auxiliary bound

Let \(P_k=P_k^{(4)}\) denote the normalized Gegenbauer polynomials for
\(S^3\):
\[
P_0(t)=1,\qquad P_1(t)=t,\qquad
(k+2)P_{k+1}(t)=2(k+1)tP_k(t)-kP_{k-1}(t).
\]
Consider
\[
f(t)=(t+1)(t-\tfrac9{16})(t+\tfrac{11}{16})^2
      (t+\tfrac3{32})^2.
\]
Its exact Gegenbauer expansion is
\[
\begin{aligned}
f(t)={}&\frac{383475}{4194304}P_0(t)
+\frac{1437735}{4194304}P_1(t)
+\frac{660717}{1048576}P_2(t)\\
&+\frac{25317}{32768}P_3(t)
+\frac{10805}{16384}P_4(t)
+\frac38P_5(t)+\frac7{64}P_6(t).
\end{aligned}
\]
All coefficients are positive.  Moreover \(f(t)\leq0\) on
\([-1,9/16]\): the first two linear factors have opposite signs there,
and the other factors are squares.  The Delsarte argument therefore gives
\[
A(4,\tfrac9{16})\leq
\frac{f(1)}{f_0}=\frac{166698}{5113}<33.
\]
Since code cardinalities are integral,
\[
\boxed{A(4,\tfrac9{16})\leq32.}
\]

For completeness, the Delsarte step uses only that each matrix
\((P_k(\langle u_i,u_j\rangle))_{i,j}\) is positive semidefinite.
Consequently
\[
\sum_{i,j}f(\langle u_i,u_j\rangle)\geq f_0N^2,
\]
while the sign of \(f\) off the diagonal gives an upper bound \(Nf(1)\).

## 2. A strict frame lower bound

Let \(C=\{x_1,\ldots,x_{41}\}\subset S^4\) be a hypothetical code and put
\[
S=\sum_{i=1}^{41}x_ix_i^T.
\]
Fix a unit vector \(v\), write \(z_i=\langle v,x_i\rangle\), and consider
the indices with \(|z_i|\leq1/5\).  Orthogonally project those points onto
\(v^\perp\) and renormalize:
\[
y_i=\frac{x_i-z_iv}{\sqrt{1-z_i^2}}\in S^3.
\]
For distinct selected indices,
\[
\langle y_i,y_j\rangle
=\frac{\langle x_i,x_j\rangle-z_iz_j}
       {\sqrt{(1-z_i^2)(1-z_j^2)}}
\leq
\frac{\frac12+\frac1{25}}{1-\frac1{25}}
=\frac9{16}.
\]
The denominator is positive, and the displayed weak inequality includes
all boundary cases \(z_i=\pm1/5\).  The projected points are distinct,
since equality of two normalized projections would give inner product
\(1>9/16\).

By the auxiliary bound, at most 32 indices have \(|z_i|\leq1/5\).
Therefore at least nine have \(|z_i|>1/5\), and hence
\[
v^TSv=\sum_i z_i^2>\frac9{25}.
\]
This holds for every unit \(v\), so
\[
\boxed{S\succ\frac9{25}I_5.}
\]
The strictness comes from the strict inequalities \(|z_i|>1/5\) for the
nine indices outside the closed slab.

Let the eigenvalues of \(S\) be \(\lambda_1,\ldots,\lambda_5\).  They
satisfy \(\lambda_i>9/25\) and
\(\sum_i\lambda_i=\operatorname{tr}S=41\).  For positive numbers bounded
below by \(m\) with fixed sum, their product is minimized by putting four
of them at \(m\) and the remaining one at the residual sum.  This follows
iteratively from the fact that, for fixed \(a+b\), the product \(ab\) is
minimized on \(a,b\geq m\) at an endpoint.  Thus, with \(m=9/25\),
\[
\det S>
\left(\frac9{25}\right)^4
\left(41-\frac{36}{25}\right).
\]

## 3. A uniformly nonsingular five-point basis

Let \(X\) be the \(5\times41\) matrix whose columns are the points of
\(C\).  Cauchy--Binet gives
\[
\det S=\det(XX^T)
=\sum_{\substack{I\subset\{1,\ldots,41\}\\|I|=5}}
 \det(X_I)^2.
\]
There are
\(\binom{41}{5}=749398\) summands.  Therefore some five-point subset
\(B\) satisfies
\[
\det(X_B)^2>
q:=
\frac{(9/25)^4(41-36/25)}{\binom{41}{5}}
=\boxed{\frac{6488829}{7318339843750}}.
\]
Choose \(B\) to have maximum absolute determinant among all five-point
subsets and relabel its points as \(x_1,\ldots,x_5\).  Its Gram matrix
\[
H=(\langle x_i,x_j\rangle)_{i,j=1}^5
\]
is positive definite and satisfies \(\det H=\det(X_B)^2>q\).
Since \(\operatorname{tr}H=5\), the other four eigenvalues have product at
most \((5/4)^4\) by arithmetic--geometric mean.  It follows that
\[
\lambda_{\min}(H)\geq \frac{256q}{625}
=\frac{830570112}{2286981201171875}.
\]
Thus the gauge is not merely nonsingular: it has an explicit rational spectral
conditioning bound.

Every remaining point has a unique coefficient vector
\(\alpha_p\in\mathbb R^5\) such that
\[
x_p=\sum_{i=1}^5\alpha_{pi}x_i.
\]
Replacing \(x_i\) in \(B\) by \(x_p\) changes the determinant by the
factor \(\alpha_{pi}\).  Maximality of \(B\) therefore gives
\[
|\alpha_{pi}|\leq1.
\]

There is a stronger hierarchy.  Form the \(5\times41\) coefficient
matrix
\[
D=[\,I_5\mid\alpha_6\mid\cdots\mid\alpha_{41}\,].
\]
Every \(5\times5\) minor of \(D\) is the determinant ratio between a
five-point subset and \(B\).  Hence
\[
\boxed{|\det D_I|\leq1\quad\text{for every }|I|=5.}
\]
Equivalently, for \(k=1,\ldots,5\), every \(k\times k\) minor made from
\(k\) nonbasis coefficient columns and the corresponding \(k\) replaced
basis positions has absolute value at most one.  The counts by \(k\) are
\[
180,\ 6300,\ 71400,\ 294525,\ 376992,
\]
and together with the unchanged basis minor they total \(749398\).
The \(k=2\) constraints, for example, are the exact quadratic pruning
inequalities
\[
|\alpha_{pi}\alpha_{qj}-\alpha_{pj}\alpha_{qi}|\leq1.
\]

## 4. Exact compact semialgebraic system

Use the ten off-diagonal entries of a symmetric \(5\times5\) matrix \(H\)
with diagonal one, and the \(36\cdot5=180\) entries of
\(\alpha_6,\ldots,\alpha_{41}\), as variables.  Impose:

1. every principal minor of \(H\) is nonnegative, and
   \(\det H\geq q\);
2. \(H_{ij}\leq1/2\) for \(i\ne j\);
3. \(-1\leq\alpha_{pi}\leq1\);
4. \(\alpha_p^TH\alpha_p=1\) for \(6\leq p\leq41\);
5. \((H\alpha_p)_i\leq1/2\) for all basis/nonbasis pairs;
6. \(\alpha_p^TH\alpha_q\leq1/2\) for \(6\leq p<q\leq41\);
7. optionally, all maximum-volume minor inequalities
   \(|\det D_I|\leq1\).

All constants are rational.  The code inequalities have degree at most
three; only the fixed \(5\times5\) principal-minor conditions and the
optional coefficient-minor hierarchy have higher degree, at most five.
The domain is compact because
\[
H_{ij}\in[-1,1],\qquad \alpha_{pi}\in[-1,1].
\]
The lower bound on \(\det H\) removes the singular-basis boundary.

There are exactly
\[
\binom52+36\cdot5=10+180=190
\]
variables and 36 unit-norm equalities, leaving an intrinsic
154-dimensional variety before active code inequalities.

Two further symmetry reductions are boundary-safe.  The 36 nonbasis points may
be relabeled so that
\[
\alpha_{6,1}\leq\alpha_{7,1}\leq\cdots\leq\alpha_{41,1}.
\]
The five basis vectors may be permuted so that their Gram row sums are
nondecreasing.  Ties are allowed, so neither ordering discards a boundary
configuration.

### Forward direction

Given a hypothetical code, Sections 2 and 3 supply a maximum-volume
basis satisfying \(\det H>q\), all coefficient bounds, and every
maximum-volume minor inequality.  Norms and pairwise inner products
translate directly into conditions 4--6.

### Reverse direction

Suppose the semialgebraic system is feasible.  The principal-minor
conditions make \(H\succeq0\), while \(\det H\geq q>0\) makes \(H\)
positive definite.  Hence there exist linearly independent unit vectors
\(x_1,\ldots,x_5\in\mathbb R^5\) with Gram matrix \(H\).  Define
\[
x_p=\sum_i\alpha_{pi}x_i,\qquad 6\leq p\leq41.
\]
Condition 4 gives \(\|x_p\|=1\).  Conditions 2, 5, and 6 give every
pairwise inner product bound.  Thus these vectors form a 41-point code.
Distinctness is automatic, because equal unit vectors would have inner
product \(1>1/2\).

Therefore feasibility of this compact rational semialgebraic system is
equivalent to existence of the forbidden 41-point code.

## 5. A global polynomial-matrix pruning constraint

Let
\[
M=DD^T=I_5+\sum_{p=6}^{41}\alpha_p\alpha_p^T.
\]
If \(B\) is a realization of the basis, then
\[
S=BMB^T,\qquad H=B^TB.
\]
The frame inequality \(S\succeq(9/25)I\) is equivalently
\[
M\succeq\frac9{25}H^{-1},
\]
or, by the Schur complement,
\[
\boxed{
\begin{pmatrix}
M & \frac35 I_5\\
\frac35 I_5 & H
\end{pmatrix}\succeq0.}
\]
This exact \(10\times10\) polynomial-matrix inequality couples all 36
nonbasis points and is a safe additional pruning condition.

There is also a useful distance form of every pair constraint.  Conditions 4
and 6 imply
\[
(\alpha_p-\alpha_q)^TH(\alpha_p-\alpha_q)
=2-2\alpha_p^TH\alpha_q\geq1.
\]
For a basis point, the same identity gives
\[
(\alpha_p-e_i)^TH(\alpha_p-e_i)\geq1.
\]
Unlike an interval evaluation of the bilinear inner product, these forms expose
nonnegative squared differences and often give a sharper box enclosure.

The norm equations also admit a safe local elimination pivot.  From
\(|\alpha_{pi}|\leq1\) and \(\alpha_p^TH\alpha_p=1\),
\[
1\leq 5\max_i |(H\alpha_p)_i|.
\]
Hence some coordinate satisfies
\[
\left|\frac{\partial}{\partial\alpha_{pi}}
(\alpha_p^TH\alpha_p-1)\right|
=2|(H\alpha_p)_i|\geq\frac25.
\]
The ten closed cases obtained by choosing the coordinate and its sign cover
the whole norm surface.  Within such a case, interval Newton or exact
quadratic elimination can remove one coefficient variable without a
singular-derivative boundary.  Applying this independently to all 36 points
explains the intrinsic dimension 154, although an explicit naive split would
have \(10^{36}\) cases.

Together with the full coefficient-minor hierarchy, this yields a safe nested
finite reduction.  Fix a rational interval box for the ten entries of \(H\)
and cover \([-1,1]^5\) by rational coefficient boxes.  Discard a coefficient
box if its norm form cannot equal one.  Two retained boxes are incompatible if
an exact Bernstein or directed interval upper bound shows
\[
(u-v)^TH(u-v)<1
\]
throughout their product and throughout the \(H\)-box.  A box is
self-incompatible under the same test and can then contain at most one code
point.  For tuples of two through five boxes, discard the tuple if a
coefficient minor is everywhere greater than one in absolute value.  Every
actual 36-point coefficient set maps to a feasible capacitated
clique/hypergraph object satisfying all these tuple constraints.  If the cover
is refined until every retained cell is self-incompatible, the 36 images are
distinct and give an ordinary 36-clique.  Thus a certified computation with no
such object safely eliminates the whole \(H\)-box.  The cells may be taken
half-open for a deterministic assignment, while all interval tests use their
closed hulls, so boundary points are retained.

There is a concrete universal resolution at which self-incompatibility is
automatic, before \(H\) is subdivided.  Since \(H\succeq0\) and
\(\operatorname{tr}H=5\), one has \(H\preceq5I\).  Partition each coordinate
interval \([-1,1]\) into 11 half-open intervals of width \(2/11\), using a
closed last interval, and use closed hulls for verification.  Two coefficient
vectors in the same five-dimensional cell satisfy
\[
(\alpha-\beta)^TH(\alpha-\beta)
\leq5\|\alpha-\beta\|^2
\leq5\cdot5\left(\frac2{11}\right)^2
=\frac{100}{121}<1.
\]
Thus every one of the \(11^5=161051\) cells has capacity at most one for every
admissible \(H\).  Any hypothetical code therefore produces an ordinary
36-clique on distinct cells.  This is a genuine finite, boundary-safe
reduction, but its compatibility relation still depends continuously on the
ten entries of \(H\).

## 6. Exhaustive-certificate format and present blocker

A boundary-safe interval proof can start from the compact box above,
bisect only at rational midpoints, and retain closed children whose union
covers the parent.  A terminal box is certifiably infeasible if exact
Bernstein or directed-rational interval bounds show:

- a norm equality cannot contain zero;
- a code inequality is everywhere violated;
- a required principal minor is everywhere negative;
- \(\det H<q\) throughout;
- a maximum-volume minor exceeds one in absolute value; or
- the global block matrix has a rigorously negative quadratic form.

A verifier need only check the rational tree coverage and the recorded
polynomial enclosures.  No strict/weak boundary case is discarded.

The obstruction is scale, not formulation.  Even after the 36 norm
equalities, the search has dimension 154.  A dense SOS relaxation in 190
variables has
\[
\binom{192}{2}=18336
\]
monomials through degree two and
\[
\binom{193}{3}=1179616
\]
through degree three.  Direct CAD is doubly exponential, and uniform
interval subdivision is correspondingly intractable.  The formulation
is therefore a certified reduction and a source of exact pruning
lemmas, not yet a nonexistence certificate.
