# An Integral Five-Node Pseudo-Measure Passing Degree-Three BV

This note strengthens `weighted_residual_barrier.md`.  On the same exact
five-node pair support, there is an integral fixed-\(41\) triple
pseudo-distribution which simultaneously satisfies

1. strict \(3\times3\) Gram feasibility on every supported triple;
2. the exact fixed-cardinality pair/triple marginal equations;
3. every universal deep-wedge event-cell inequality used in the local
   hybrid audit;
4. the sharper mixed-wedge capacities forced by the type-\(0\) degree
   cap and the fact that there are only three type-\(1\) edges; and
5. every fixed-\(N\) Bachoc--Vallentin block through total degree three.

This is a method barrier, not a spherical code.  No common edge-colored
complete graph realizing the triple counts is asserted.

The exact certificate is
`certificates/local_hybrid_degree3_triple_pseudodistribution.json`, and
the standard-library verifier is
`verifiers/verify_local_hybrid_degree3.py`.

## Pair and triple data

The pair atoms, ordered counts, and unordered edge counts are
\[
\begin{array}{c|rrrrr}
\text{type}&0&1&2&3&4\\ \hline
t&-77/100&-7/10&-11/25&-9/100&499/1000\\
c_t&170&6&262&652&550\\
E_t&85&3&131&326&275.
\end{array}                                      \tag{1}
\]

For a sorted edge-type triple \(T\), let \(n_T\) be its unordered
triple count.  The nonzero counts are
\[
\begin{array}{c|r@{\quad}c|r@{\quad}c|r}
004&275&014&30&023&70\\
024&1021&033&990&034&654\\
114&3&123&22&124&5\\
133&12&134&42&222&242\\
224&63&233&1126&234&1601\\
244&412&333&290&334&2068\\
344&1063&444&671&&
\end{array}                                      \tag{2}
\]
where, for example, \(023\) means \(T=(0,2,3)\).

All counts are nonnegative integers and
\[
\sum_T n_T=10660={41\choose3}.                   \tag{3}
\]
Their five edge incidences are
\[
\left(
\sum_T\operatorname{mult}_q(T)n_T
\right)_{q=0}^4
=(3315,117,5109,12714,10725)
=39(85,3,131,326,275).                           \tag{4}
\]
Thus the full-permutation-orbit masses
\[
\nu_T=\frac{6n_T}{41}
\]
obey the exact fixed-\(N\) marginal equations.

For every supported \(T\), direct rational evaluation gives
\[
\Delta(T)=1+2uvt-u^2-v^2-t^2>0.
\]
The minimum is
\[
\Delta(244)=\frac{278991}{3125000}>0.            \tag{5}
\]
Consequently no determinant boundary or numerical tolerance is involved.

## Universal wedge checks

Let \(W_A\) count centered wedges whose two incident edge types lie in
\(A\).  Exact evaluation of (2) gives
\[
W_{\{0\}}=275,\qquad
W_{\{0,1\}}=308.                                 \tag{6}
\]
For every event cell \(3/8<q\le3/4\), the verifier forms
\[
A_q=\{r:t_r<0,\ t_r^2\ge q\},\qquad
B_q=\{r:t_r\ge2q-1\}
\]
and checks exactly
\[
F_{41}\!\left(\sum_{r\in A_q}c_r\right)
\le W_{A_q}
\le L(q)\sum_{r\in B_q}E_r,                      \tag{7}
\]
where \(F_{41}\) is the integer degree-envelope minimum and
\[
L(q)=\min\!\left(5,\left\lfloor
\frac3{8q-3}\right\rfloor\right)
\]
is the proved common-center multiplicity bound.  The event list contains
all support, high-threshold, and floor-change boundaries, so (7) covers
the whole continuous interval rather than a sampled grid.

There are two additional incidence capacities which an aggregate
\(W_{\{0,1\}}\) check can miss.  Pfender's row inequality gives
\(d_0(v)\le5\).  Since \(E_1=3\),
\[
W_{0,1}^{\rm mixed}
=\sum_vd_0(v)d_1(v)
\le5\sum_vd_1(v)=5(2E_1)=30.                    \tag{8}
\]
Also any three-edge graph has
\[
W_{\{1\}}=\sum_v{d_1(v)\choose2}\le{3\choose2}=3. \tag{9}
\]
The counts (2) attain both bounds:
\[
W_{0,1}^{\rm mixed}=n_{014}=30,\qquad
W_{\{1\}}=n_{114}=3.                             \tag{10}
\]
The aggregate data are locally compatible: type-\(0\) degrees may be
\[
3^5,\ 4^{25},\ 5^{11},
\]
which have degree sum \(170\) and wedge count \(275\).  Placing the three
type-\(1\) edges as a star on four of the degree-five vertices realizes
the two numbers in (10).  This is only a check of these degree and wedge
statistics, not a claim that all of (2) has a graph realization.

## Exact degree-three BV verification

Use the normalization and polynomialized transverse kernels from
`fixed41_three_point_formulation.md`.  Thus
\[
Q_0=1,\qquad Q_1=t-uv,
\]
\[
Q_{k+1}
=\frac{2(k+1)}{k+2}(t-uv)Q_k
-\frac{k}{k+2}(1-u^2)(1-v^2)Q_{k-1},
\]
and
\[
Z_{k,3}(u,v,t)
=\left(u^iv^jQ_k(u,v,t)\right)_{0\le i,j\le3-k}.
\]
For \(k=0,1,2,3\), the fixed-\(N\) matrix is
\[
\begin{split}
H_{k,3}={}&Z_{k,3}(1,1,1)\\
&+\sum_q\frac{c_q}{41}\left[
Z_{k,3}(1,q,q)+Z_{k,3}(q,1,q)+Z_{k,3}(q,q,1)
\right]\\
&+\sum_T\frac{6n_T}{41|\operatorname{Orb}(T)|}
\sum_{(u,v,t)\in\operatorname{Orb}(T)}
Z_{k,3}(u,v,t).                                  \tag{11}
\end{split}
\]
The addition formula makes \(H_{k,3}\succeq0\) necessary for every
genuine spherical code.

The verifier constructs (11) in exact rational arithmetic and checks
every principal minor, not floating-point eigenvalues.  The least
principal minors are
\[
\begin{array}{c|c|c}
k&\text{indices}&\text{least principal minor}\\ \hline
0&(1,3)&
\dfrac{84333109360856935209633}
      {1050625000000000000000000}\\[2mm]
1&(1,2)&
\dfrac{3449723259474261817946435877}
      {42025000000000000000000000000}\\[2mm]
2&(0,1)&
\dfrac{31248817301127972207531453743}
      {378225000000000000000000000000}\\[2mm]
3&(0)&
\dfrac{106047122208949126237}
      {20500000000000000000}.
\end{array}                                      \tag{12}
\]
Every entry in (12) is strictly positive.  Hence every \(H_{k,3}\) is
positive definite.  Since every lower-total-degree block is a principal
submatrix, all BV constraints through total degree three hold.

## The independent rank-five cut separates it

Claim C047 in `rank_five_spectral_moment.md` applies to any positive
semidefinite Gram matrix of rank at most five.  With
\[
p_j=\operatorname{tr}(G^j),\qquad
V=p_2-\frac{p_1^2}{5},\qquad
D=p_3-\frac{p_1^3}{25}-\frac{3p_1}{5}V,
\]
it states
\[
20D^2\le9V^3.                                    \tag{13}
\]
For a fixed-\(41\) triple measure, put
\[
A=\int q^2\,d\alpha(q),\qquad
T=\int uvt\,d\nu(u,v,t).
\]
The exact trace expansions are
\[
p_2=41(1+A),\qquad p_3=41(1+3A+T).
\]
For (1)--(2), rational summation gives
\[
\begin{aligned}
A&=\frac{5933759}{820000},&
T&=\frac{942439107537}{20500000000},\\
V&=\frac{29759}{20000},&
D&=\frac{11249247537}{500000000}.
\end{aligned}                                    \tag{14}
\]
Consequently
\[
20D^2-9V^3
=\frac{252349919611050160863}
        {25000000000000000}>0.                   \tag{15}
\]
Thus C047 rigorously excludes this triple pseudo-measure from coming from
one rank-five Gram matrix.  This also shows that the rank cut contains
information not recovered by all total-degree-three BV blocks.

## Basic color-degree covariance does not separate it

There is another necessary common-source condition at the level of an
edge-colored complete graph.  If \(d_q(v)\) is the degree of vertex \(v\)
in color \(q\), the triple counts determine
\[
S_{qq}=\sum_vd_q(v)^2=c_q+2W_{qq},\qquad
S_{qr}=\sum_vd_q(v)d_r(v)=W_{qr}\quad(q\ne r).
\]
Hence
\[
\Sigma=S-\frac1{41}cc^{\mathsf T}\succeq0        \tag{16}
\]
is necessary.

For this first degree-three witness, (16) holds exactly.  The verifier checks
every principal minor of \(\Sigma\); the full determinant is zero, as forced
by \(\sum_qd_q(v)=40\), and every proper principal minor is positive.  The
least positive one is
\[
\frac{456}{41}.                                  \tag{17}
\]
Thus the rank-five failure in (15) is not merely the same obstruction as
the basic color-degree covariance test.  Conversely, the rank-aware
reassignment in `local_hybrid_degree3_rank_barrier.md` passes C047 but fails
(16), giving an exact independence witness in the other direction.

## Exact scope boundary

The same counts do not pass total degree four.  In the \(k=3\) block,
the radial direction \(p(u)=u\) has the negative diagonal value
\[
(H_{3,4})_{1,1}
=-\frac{65176795992375100476726763}
        {20500000000000000000000000}<0.           \tag{18}
\]
Thus (2) is not an all-degree pseudo-distribution.  Its rigorous lesson is
precise: degree-three BV, triangle PSD, the local-hybrid pair cuts, and all
named universal wedge capacities do not by themselves eliminate this
five-node fixed-\(41\) support, while the independent rank-five inequality
does eliminate this particular triple assignment.

## Discovery versus verification

`experiments/search_local_hybrid_degree3.py` found (2) by a
floating-point MILP with iteratively separated eigenvector cuts.  Neither
the MILP status nor its eigenvalues are used in the proof.

The verifier independently reloads the rational JSON data and checks
(3)--(18) using only Python's standard library.  The certificate SHA-256
is
```
305719113ef9be62b2185084ffbea6f9e3241accfb98a4b81c2aef2aa5b07632
```

From the repository root, run
```
/usr/bin/python3 verifiers/verify_local_hybrid_degree3.py
/usr/bin/python3 -m unittest tests.test_local_hybrid_degree3 -v
```
