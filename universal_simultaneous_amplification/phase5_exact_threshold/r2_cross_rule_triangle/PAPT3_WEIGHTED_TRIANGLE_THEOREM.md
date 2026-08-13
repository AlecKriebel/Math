# The fitness-two product inequality for every weighted triangle

Date: 2026-08-13 (America/Los_Angeles)

No literature search or external communication was used.

## 1. Theorem

Let `G` be a connected loopless undirected weighted graph on three vertices,
with nonnegative edge conductances

\[
                         (a,b,c)=(w_{01},w_{02},w_{12}).      \tag{1}
\]

At fitness two,

\[
 \boxed{
 {\rho_{Bd}(G,2)\over4/7}
 {\rho_{dB}(G,2)\over4/9}\leq1.}                           \tag{2}
\]

Equality holds exactly when `a=b=c>0`, namely when `G` is the complete
triangle up to a common conductance scale.  Thus `PAPT_3` is proved for
every connected weighted three-vertex graph, including both positive
triangles and weighted paths.

The proof is a direct exact factorization of the two absorbing systems.  It
does not use orbital symmetrization, a separate Bd or dB comparison, or a
pointwise Poisson bound.

## 2. Compact exact fixation formulas

For a partition `lambda=(i,j,k)`, let

\[
 m_\lambda(a,b,c)=\sum_{\text{distinct permutations of }(i,j,k)}
                         a^ib^jc^k.                         \tag{3}
\]

Define homogeneous symmetric polynomials `N_B,Q_B` of degree twelve by the
following coefficient table:

\[
\begin{array}{c|r|r}
\lambda &[m_\lambda]N_B &[m_\lambda]Q_B\\ \hline
(8,4,0)&20&80\\
(8,3,1)&121&484\\
(8,2,2)&222&888\\
(7,5,0)&310&700\\
(7,4,1)&2123&5067\\
(7,3,2)&5097&12593\\
(6,6,0)&600&1320\\
(6,5,1)&6042&13673\\
(6,4,2)&20467&47528\\
(6,3,3)&30130&70670\\
(5,5,2)&31264&71966\\
(5,4,3)&66586&155109\\
(4,4,4)&96564&225616
\end{array}                                                \tag{4}
\]

Define homogeneous symmetric polynomials `N_D,Q_D` of degree six by

\[
\begin{array}{c|r|r}
\lambda &[m_\lambda]N_D &[m_\lambda]Q_D\\ \hline
(4,2,0)&16&32\\
(4,1,1)&40&80\\
(3,3,0)&56&80\\
(3,2,1)&223&328\\
(2,2,2)&456&627.
\end{array}                                                \tag{5}
\]

Direct solution of the six transient subset equations for each update rule
gives

\[
 \boxed{
 \rho_{Bd}(G,2)={4N_B\over3Q_B},\qquad
 \rho_{dB}(G,2)={2N_D\over3Q_D}.}                         \tag{6}
\]

Every coefficient in `(4)--(5)` is positive.  Hence `Q_B,Q_D>0` whenever
at least two of `a,b,c` are positive, exactly the connected three-vertex
domain.

For the complete triangle, `(6)` reduces to `4/7` and `4/9`.  Consequently

\[
 {16\over63}-\rho_{Bd}(G,2)\rho_{dB}(G,2)
 ={8\mathcal N(a,b,c)\over63Q_BQ_D},                       \tag{7}
\]

where the primitive degree-eighteen numerator is

\[
                         \mathcal N=2Q_BQ_D-7N_BN_D.        \tag{8}
\]

## 3. A positive 24-circuit factorization

For nonnegative integers `i,j,k` with `i+j+k=16`, put

\[
 \mathcal A_{ijk}(a,b,c)
 =\sum_{(x,y,z)\in\operatorname{Perm}(a,b,c)}
                     x^iy^jz^k(x-y)^2,                    \tag{9}
\]

where the sum is over all six elements of `S_3`, including repeated
monomials when exponents coincide.  Every `A_ijk` is nonnegative on the
nonnegative conductance cone.

Exact coefficient comparison gives

\[
                         \boxed{\mathcal N
                         =\sum_{(i,j,k)}\gamma_{ijk}\mathcal A_{ijk},}
                                                                    \tag{10}
\]

with precisely the following positive integer coefficients:

\[
\begin{array}{c|r@{\qquad}c|r}
(i,j,k)&\gamma_{ijk}&(i,j,k)&\gamma_{ijk}\\ \hline
(0,4,12)&2880&(0,5,11)&15040\\
(0,8,8)&8720&(1,3,12)&30384\\
(1,4,11)&193060&(1,7,8)&58546\\
(1,8,7)&234046&(2,4,10)&1235746\\
(2,5,9)&41924&(2,7,7)&1462847\\
(2,9,5)&1310059&(3,4,9)&2217205\\
(3,6,7)&2475646&(3,7,6)&686879\\
(3,8,5)&11441942&(3,10,3)&27000\\
(4,7,5)&34933576&(4,8,4)&1566204\\
(4,9,3)&1169837&(4,10,2)&136296\\
(5,5,6)&2264809&(5,6,5)&58710886\\
(6,8,2)&89812&(8,8,0)&960.
\end{array}                                                \tag{11}
\]

Equations `(7)` and `(10)--(11)` prove `(2)`.

The equality statement is also immediate.  The certificate contains
`8720 A_088`, and

\[
\begin{aligned}
 \mathcal A_{088}={}&c^8(a^8+b^8)(a-b)^2
                    +b^8(a^8+c^8)(a-c)^2\\
                   &+a^8(b^8+c^8)(b-c)^2.                 \tag{12}
\end{aligned}
\]

For three positive conductances, `(12)` vanishes only at `a=b=c`.  If one
conductance is zero and the other two are positive, one term in `(12)` is
strictly positive.  This proves strictness on every connected noncomplete
weighted triangle and path.

## 4. What the factorization says structurally

Each term in `(9)` is a three-monomial exchange circuit:

\[
 x^iy^jz^k(x-y)^2
 =x^{i+2}y^jz^k-2x^{i+1}y^{j+1}z^k+x^iy^{j+2}z^k.         \tag{13}
\]

On a triangle, every pair of edges is a wedge: `x` and `y` share one
vertex, and `z` is the closing edge.  The proof therefore writes the whole
paired-tree numerator as a positive sum of local wedge-exchange circuits.
This is stronger information than mere positivity of the final symmetric
polynomial.

It identifies the only evident induction target.  After clearing the
positive row denominators in general order, one would seek

\[
 \boxed{
 \mathcal N_n(W)=
 \sum_v\sum_{\{i,j\}\subseteq V\setminus\{v\}}
 (w_{vi}-w_{vj})^2\,C_{v;i,j}(W),}                         \tag{14}
\]

where every `C_{v;i,j}` is a coefficientwise nonnegative paired-forest
completion polynomial and covariance under vertex relabelling is retained.
At order three, `(10)` is exactly `(14)`.  Such an identity would prove
`PAPT_n` directly and force complete-graph equality, because the line graph
of `K_n` is connected and all wedge differences can vanish only when all
conductances agree.

Equation `(14)` is a **named open structural target**, not a theorem in
general order.

## 5. Why the existing deletion--contraction does not yet induct

The exact two-deletion identity in
`../r2_cross_rule_determinant/FOREST_EXCHANGE_UNIT.md` reorganizes `PAPT_n`
into pairs of three-component directed forests.  Contracting the fixed
components leaves a three-sink completion problem, which initially looks
like the correct place to apply the triangle theorem.

There is a sharp obstruction.  The contracted `L` and `D` completion
systems are different directed kernels; they are not the Bd and dB systems
of one common undirected three-edge conductance vector.  Individual
three-component packets can be negative—the committed weighted-path packet
has exact value `-362/525`.  Therefore `(10)` cannot be applied packet by
packet, and naive induction by deletion--contraction is invalid.

The surviving possible induction must first sum across completion siblings
so that the common-arrow/undirected relation is restored, and only then
produce the wedge circuits `(13)`.  Equivalently, it must prove that the
global coefficients `C_{v;i,j}` in `(14)` are paired-forest polynomials with
nonnegative coefficients.  This is precisely the nonduplication problem
left by the forest-exchange branch; the triangle theorem supplies its local
algebraic endpoint but does not solve the global grouping.

Two triangle-specific coincidences also cannot be imported silently:

1. every permutation of the three edges is induced by a vertex
   permutation, while in order at least four adjacent and disjoint edge
   pairs form different orbits;
2. the triangle has only one closing edge for each wedge, while a general
   forest completion carries many directed histories with the same endpoint
   wedge.

Thus the exact next proof object is not a sum of induced-triangle gaps.  It
is the global paired-forest wedge coefficient in `(14)`.

## 6. Scope and replay

**PROVED:** `PAPT_3` for every connected nonnegative weighted three-vertex
graph, exact fixation formulas `(4)--(6)`, the degree-eighteen identity
`(7)--(8)`, and the positive 24-circuit certificate `(10)--(12)`.

**OPEN:** coefficientwise positivity of the global paired-forest wedge
coefficients `(14)`, and hence `PAPT_n` for arbitrary order.

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B verify_papt3_weighted_triangle.py
```

The verifier independently builds both symbolic absorbing chains, verifies
the compact monomial-symmetric formulas, expands all 24 exchange circuits,
checks the exact product identity, and audits the connected path boundary.
