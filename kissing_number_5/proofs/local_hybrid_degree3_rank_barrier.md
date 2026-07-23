# A Five-Node Pseudo-Measure Passing Degree-Three BV and C047

## Result and exact scope

There is an exact integral fixed-\(41\) triple pseudo-distribution on the
five-node pair support of `local_hybrid_barrier.md` which passes

- strict \(3\times3\) Gram feasibility;
- the exact pair/triple marginal equations;
- every proved deep-wedge event-cell inequality;
- the mixed-wedge and three-edge capacities;
- every fixed-\(N\) Bachoc--Vallentin block through total degree three;
  and
- the sharp rank-five spectral-moment inequality C047.

This strengthens `local_hybrid_degree3_barrier.md`, whose first degree-three
witness failed C047.  The new object is still only a triple
pseudo-distribution.  Passing one rank-five necessary inequality does not
construct a rank-five Gram matrix, and no common edge-colored complete graph
realizing these counts is asserted.  In fact, a basic color-degree covariance
test below proves that no such common graph realizes these particular counts.

The certificate is
`certificates/local_hybrid_degree3_rank_pseudodistribution.json`.
The exact verifier is
`verifiers/verify_local_hybrid_degree3_rank.py`.

## Exact counts

The pair atoms and ordered counts remain
\[
\begin{array}{c|rrrrr}
\text{type}&0&1&2&3&4\\ \hline
t&-77/100&-7/10&-11/25&-9/100&499/1000\\
c_t&170&6&262&652&550.
\end{array}                                      \tag{1}
\]
For a sorted edge-type triple \(T\), the nonzero unordered counts \(n_T\)
are
\[
\begin{array}{c|r@{\quad}c|r@{\quad}c|r}
004&275&014&30&023&30\\
024&1036&033&1032&034&637\\
114&3&124&15&133&34\\
134&32&222&266&223&39\\
224&5&233&1092&234&1616\\
244&434&333&211&334&2208\\
344&995&444&670&&
\end{array}                                      \tag{2}
\]
They obey
\[
\sum_Tn_T=10660={41\choose3}                     \tag{3}
\]
and the exact type-incidence equations
\[
\left(\sum_T\operatorname{mult}_q(T)n_T\right)_{q=0}^4
=(3315,117,5109,12714,10725)
=39(85,3,131,326,275).                           \tag{4}
\]
Every supported triangle is strictly Gram-feasible.  The least determinant
is
\[
\Delta(244)=\frac{278991}{3125000}>0.            \tag{5}
\]

## Wedge audit

The exact wedge statistics are
\[
W_{\{0\}}=275,\qquad W_{\{0,1\}}=308,\qquad
W_{0,1}^{\rm mixed}=30,\qquad W_{\{1\}}=3.       \tag{6}
\]
The verifier evaluates the integer-envelope lower bound and common-center
upper bound at every threshold event cell in \(3/8<q\le3/4\), including
all boundaries.  Every inequality holds.

The last two values in (6) attain the sharper universal capacities
\[
\sum_vd_0(v)d_1(v)
\le5\sum_vd_1(v)=30,\qquad
\sum_v{d_1(v)\choose2}\le{3\choose2}=3.           \tag{7}
\]
As in the preceding barrier, the aggregate data are compatible with
type-\(0\) degrees \(3^5,4^{25},5^{11}\) and a three-edge type-\(1\)
star on four degree-five vertices.  This checks the named local incidence
statistics only; it is not a global graph realization.

## Complete degree-three BV audit

Using the exact fixed-\(N\) normalization and transverse kernels defined in
`fixed41_three_point_formulation.md`, the verifier forms every
\(H_{k,3}\), \(0\le k\le3\), from (1)--(2).  It checks every principal
minor in rational arithmetic.  The least ones are
\[
\begin{array}{c|c|c}
k&\text{indices}&\text{least principal minor}\\ \hline
0&(1,3)&
\dfrac{258743294447584132869903}
      {4202500000000000000000000}\\[2mm]
1&(1,2)&
\dfrac{43298054454337461453155341}
      {2101250000000000000000000000}\\[2mm]
2&(0,1)&
\dfrac{2044735394554621266331271839}
      {18911250000000000000000000000}\\[2mm]
3&(0)&
\dfrac{44961384503977585143}
      {10250000000000000000}.
\end{array}                                      \tag{8}
\]
They are all strictly positive.  Hence the four total-degree-three blocks,
and therefore every lower-total-degree principal subblock, are positive
definite.

## Exact C047 audit

Let
\[
A=\int q^2\,d\alpha(q),\qquad
T=\int uvt\,d\nu(u,v,t),\qquad
\delta=A-\frac{36}{5}.
\]
In the fixed-\(41\) form of C047, define
\[
E=T-\frac{1116}{25}-\frac{108}{5}\delta.
\]
The rank-five inequality is
\[
20E^2\le369\delta^3.                              \tag{9}
\]
Exact summation from (1)--(2) gives
\[
\begin{aligned}
A&=\frac{5933759}{820000},&
T&=\frac{46569451803}{1025000000},\\
\delta&=\frac{29759}{820000},&
E&=\frac{9958803}{1025000000}.
\end{aligned}                                    \tag{10}
\]
In particular \(0<E<1/100\), but the verifier does not rely only on that
discovery band.  It evaluates (9) exactly:
\[
20E^2-369\delta^3
=-\frac{26475139223868987}
        {1681000000000000000}<0.                 \tag{11}
\]
Equivalently, in spectral variables
\[
V=41\delta=\frac{29759}{20000},\qquad
D=41E=\frac{9958803}{25000000},
\]
and
\[
20D^2-9V^3
=-\frac{26475139223868987}
        {1000000000000000}<0.                    \tag{12}
\]
Thus C047 holds with strict rational slack.

## A basic common-graph separator

For a common complete graph whose five edge colors have degrees \(d_q(v)\),
the triple counts determine
\[
S_{qq}=\sum_vd_q(v)^2=c_q+2W_{qq},\qquad
S_{qr}=\sum_vd_q(v)d_r(v)=W_{qr}\quad(q\ne r).    \tag{13}
\]
Therefore the centered color-degree matrix
\[
\Sigma=S-\frac1{41}cc^{\mathsf T}                \tag{14}
\]
must be positive semidefinite: it is the Gram matrix of the five centered
degree columns.

The counts (2) fail this elementary condition.  In the short direction
\[
a=(2,-1,0,0,1),
\]
exact evaluation gives
\[
a^{\mathsf T}\Sigma a=-\frac{570}{41}<0.          \tag{15}
\]
Equivalently, with
\[
h_v=2d_0(v)-d_1(v)+d_4(v),
\]
the pseudo-counts assign the impossible negative value
\[
\sum_vh_v^2-\frac1{41}\left(\sum_vh_v\right)^2
=-\frac{570}{41}.                                \tag{16}
\]
The least principal minor is likewise negative:
\[
\det\Sigma[\{0,1,2,3\}]
=-\frac{19857375}{41}.                            \tag{17}
\]
Thus this assignment shows that degree-three BV and C047 can have the
correct signs while common-graph degree covariance has the wrong sign.
It does not survive their full conjunction.

## A next-degree separator

This witness does not pass total degree four.  In the \(k=3\) block, the
radial direction \(p(u)=u\) has diagonal value
\[
(H_{3,4})_{1,1}
=-\frac{34232597256626759823593857}
        {10250000000000000000000000}<0.           \tag{18}
\]
The precise barrier conclusion is therefore that C047, all
total-degree-three BV blocks, and the named local-hybrid wedge inequalities
do not eliminate this pair support unless common-source compatibility is
also enforced.  This particular assignment is eliminated both by (15) and
by (18).

## Reproduction and numerical rigor

The floating-point MILP in
`experiments/search_local_hybrid_degree3.py --degree 3 --rank-five`
was used only for discovery.  The proof uses no solver status or numerical
eigenvalue.

The standard-library verifier reloads the JSON certificate and independently
checks (3)--(18) with `fractions.Fraction`.  The certificate SHA-256 is
```
84fff611607343b328a00162b299e51821238cb37bcd1e37131886404a55e7c0
```

Run
```
/usr/bin/python3 verifiers/verify_local_hybrid_degree3_rank.py
/usr/bin/python3 -m unittest tests.test_local_hybrid_degree3_rank -v
```
