# A 41-Point Pseudo-Object Surviving All Degree-Two BV Blocks

This note gives an exact strengthening of
`three_point_minor_barrier.md`.  It is a labeled complete graph on 41
vertices, not a spherical code.  It has the same six-point pair distribution,
satisfies every \(3\times3\) principal Gram condition, and satisfies every
fixed-\(N\) Bachoc--Vallentin block of total degree at most two.  Its first BV
failure is an elementary degree-three weighted-residual inequality.

The exact verifier is
`verifiers/verify_degree2_bv_barrier.py`.

## Data retained from the trianglewise barrier

The labels and ordered multiplicities are
\[
\begin{array}{c|rrrrrr}
t&-157/200&-39/50&-9/20&-1/10&-19/200&99/200\\ \hline
c_t&32&132&264&130&522&560.
\end{array}
\tag{1}
\]
The 82 edges in the first two classes are the same 4-regular girth-six
graph \(L\), and its 16 edges in the first class are the same matching.
All 246 distance-two pairs in \(L\) retain label \(99/200\).  The verifier
stores new exact choices of

- 34 additional \(99/200\) edges;
- 132 edges labeled \(-9/20\);
- 65 edges labeled \(-1/10\).

The remaining 261 edges receive \(-19/200\).

The endpoints of an edge of \(L\) have neither a common \(99/200\)-neighbor
nor a common \(-9/20\)-neighbor.  Thus the negative-wedge multiplicity and
triangle restrictions remain valid.  Exact enumeration gives
\[
 \min_{|S|=3}\det G[S]
 =\frac{34771}{400000}>0.                         \tag{2}
\]

## The degree-two BV audit

For a sorted label triple \(T\), let \(n_T\) be its number of unordered
vertex triples.  The corresponding full-permutation-orbit mass in the
fixed-\(N\) normalization is
\[
 \nu_T=\frac{6n_T}{41}.
\]
There are 38 nonzero triple orbits.  The verifier checks exactly
\[
 \sum_T\nu_T=40\cdot39
\]
and, for every label \(q\),
\[
 \sum_T\frac{\operatorname{mult}_q(T)}3\nu_T
 =39\alpha_q,\qquad \alpha_q=\frac{c_q}{41}.       \tag{3}
\]

For each total-degree-two harmonic block \(k=0,1,2\), every principal
minor is strictly positive.  In particular, the scalar \(k=2\) block is
\[
 \frac{8701609923}{16400000000}>0.                \tag{4}
\]
Since lower-total-degree blocks are principal submatrices of these blocks,
(4) and the exact minor checks prove feasibility through total degree two.

This matters because the preceding trianglewise pseudo-object fails the
same \(k=2\) scalar.  Thus trianglewise PSD can coexist with either sign,
and the degree-two harmonic obstruction can be repaired without changing
the pair distribution or the deep-wedge graph.

## Human-readable form of the harmonic inequalities

For a genuine spherical code with Gram entries \(g_{ij}\), fix \(i\) and
write
\[
 r_{ij}=x_j-g_{ij}x_i\in x_i^\perp.
\]
For any polynomial \(p\), define
\[
 R_{i,p}=\sum_{j\ne i}p(g_{ij})r_{ij}.
\]
Then the \(k=1\) BV block is simply the Gram matrix, in the direct sum of
the tangent spaces \(x_i^\perp\), of the vectors \(R_{i,p}\):
\[
 B(p,q)=\frac1N\sum_i\langle R_{i,p},R_{i,q}\rangle
 =\frac1N\sum_{i,j,k}
 p(g_{ij})q(g_{ik})(g_{jk}-g_{ij}g_{ik}).          \tag{5}
\]
Consequently \(B\succeq0\) for every genuine code.

Taking \(p(u)=1,u,u^2\), the pseudo-object's total-degree-three \(k=1\)
matrix is
\[
\begin{pmatrix}
\frac{1636251}{205000}&
-\frac{172747923}{164000000}&
\frac{52884578739}{32800000000}\\
-\frac{172747923}{164000000}&
\frac{8600664577}{16400000000}&
\frac{9151184465761}{3280000000000}\\
\frac{52884578739}{32800000000}&
\frac{9151184465761}{3280000000000}&
\frac{694136547054399}{656000000000000}
\end{pmatrix}.                                    \tag{6}
\]
Its \(u,u^2\) principal minor is
\[
-\frac{38887070757266787904992449}
       {5379200000000000000000000}<0,              \tag{7}
\]
and its full determinant is
\[
-\frac{615018788827907136219533721201153}
       {8821888000000000000000000000000}<0.        \tag{8}
\]
The preceding total-degree-three \(k=0\) block is positive definite, so
this is the first failed BV block in increasing total degree and then
harmonic degree.

There is an even shorter scalar witness.  Put
\[
 f(u)=u-\frac83u^2.
\]
Equation (5) implies the universal inequality
\[
\Phi_f:=
\frac1N\sum_i
\left\|\sum_{j\ne i}f(g_{ij})
      (x_j-g_{ij}x_i)\right\|^2
\ge0.                                               \tag{9}
\]
The exact value on the pseudo-object is
\[
 \Phi_f
 =-\frac{105027064094021}{15375000000000}<0.       \tag{10}
\]
Thus (9), rather than the less transparent determinant (8), is the
human-readable separator.

For comparison, the degree-two \(k=2\) scalar also has a direct form.
Let
\[
 A_i=\sum_{j\ne i}r_{ij}r_{ij}^{\mathsf T}
\]
on the four-dimensional tangent space.  Its centered contribution is
\[
\frac13\left(4\operatorname{tr}(A_i^2)
             -\operatorname{tr}(A_i)^2\right)
=\frac43\left\|A_i-\frac{\operatorname{tr}A_i}{4}I\right\|_F^2.
\tag{11}
\]
This proves nonnegativity for a real configuration and explains precisely
what the earlier pseudo-object violated.

## Colored-wedge incidence explanation

The negativity in (10) is not diffuse.  A deep edge and a
\(-9/20\)-edge sharing a vertex determine a colored wedge.  Triangle PSD
forbids its third edge from also having label \(-9/20\).  Since \(L\) is
4-regular, the number of these wedges is forced:
\[
 \sum_v d_L(v)d_{-9/20}(v)
 =4\sum_vd_{-9/20}(v)
 =4\cdot2\cdot132=1056.                             \tag{12}
\]
They split as follows:
\[
\begin{array}{c|rrr}
\text{deep label}\backslash\text{closing label}
 &-1/10&-19/200&99/200\\ \hline
-157/200&9&79&118\\
-39/50&73&308&469.
\end{array}
\tag{13}
\]

For an unordered triangle with labels \(a,b,c\), define its coefficient
\[
 \gamma(a,b,c)=
 \sum_{\sigma\in S_3}
 f(t_{\sigma(1)})f(t_{\sigma(2)})
 \bigl(t_{\sigma(3)}
       -t_{\sigma(1)}t_{\sigma(2)}\bigr),           \tag{14}
\]
where repeated permutations are counted.  The six wedge classes in (13)
have coefficients
\[
\begin{array}{c|r}
(-157/200,-9/20,-1/10)&-3051549029/1125000000\\
(-157/200,-9/20,-19/200)&-1492678977689/562500000000\\
(-157/200,-9/20,99/200)&1788817041/3906250000\\
(-39/50,-9/20,-1/10)&-83548443/31250000\\
(-39/50,-9/20,-19/200)&-163456844727/62500000000\\
(-39/50,-9/20,99/200)&7211997243/15625000000.
\end{array}
\tag{15}
\]
Thus a high closing edge contributes positively, whereas either shallow
closing label contributes about \(-2.6\) per wedge.

Before division by \(N=41\), the exact decomposition of (10) is
\[
\begin{array}{c|r}
\text{repeated-pair contribution}
 &223915208247977/375000000000\\
\text{the 1056 deep--middle wedges}
 &-542375696941691/562500000000\\
\text{all other distinct triples}
 &24481144214347/281250000000.
\end{array}
\tag{16}
\]
The three entries sum to
\[
-\frac{105027064094021}{375000000000},
\]
which becomes (10) after division by 41.  The failed degree-three block is
therefore explained primarily by insufficient high-label closure of the
forced deep--middle wedges, not by four-cycles or a large collection of
unrelated motifs.

Equation (14) yields an exact labeled-triangle count inequality
\[
 2\sum_{\{i,j\}}f(g_{ij})^2(1-g_{ij}^2)
 +\sum_{a\le b\le c}\gamma(a,b,c)n_{abc}\ge0       \tag{17}
\]
for any genuine code supported on these labels.  A possible hybrid route is
to combine (12), a universal upper bound on high closures in (13), and
bounds on the compensating terms in (17).  No such universal closure bound
has yet been proved, so this is a candidate mechanism rather than an upper
bound for arbitrary spherical codes.

## Four-local audit

The relabeling is not four-locally PSD.  Exact enumeration gives
\[
\#\{S:|S|=4,\det G[S]<0\}=14608,
\]
with minimum
\[
 \det G[\{1,15,16,39\}]=-\frac{712327}{500000}.
\tag{18}
\]
This prevents interpreting it as a Gram matrix and shows that survival of
all degree-two BV blocks is still substantially weaker than four-local
positive semidefiniteness.

## Reproduction

Run:

```sh
python3 verifiers/verify_degree2_bv_barrier.py
python3 -m unittest tests.test_degree2_bv_barrier -v
```
