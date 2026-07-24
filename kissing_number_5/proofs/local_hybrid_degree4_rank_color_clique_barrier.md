# A degree-four BV + rank + colored-clique pseudodistribution

## Status

This note records an exact **relaxation barrier**, not a spherical code and
not an upper-bound proof.  On the five-node support
\[
 -\frac{77}{100},\quad-\frac7{10},\quad-\frac{11}{25},
 \quad-\frac9{100},\quad\frac{499}{1000},
\]
there is an integral 41-point pair/triple pseudodistribution which
simultaneously satisfies

1. every fixed-\(N\) Bachoc--Vallentin block through total degree four;
2. the exact C047 rank-five spectral-moment consequence;
3. the complete centered covariance PSD condition for all five
   edge-color degree columns;
4. all universal threshold-wedge bounds used by the local-hybrid search;
5. the rank-forced color-\(\{0,1\}\) neighborhood-clique inequality;
6. an exact 41-row joint colored-degree moment decomposition for which
   every nonempty proper color-union degree sequence is graphical; and
7. the negative-pair graph conditions of at least 144 edges and minimum
   degree at least seven.

The exact certificate is
[`../certificates/local_hybrid_degree4_rank_color_clique_pseudodistribution.json`](../certificates/local_hybrid_degree4_rank_color_clique_pseudodistribution.json),
and the independent standard-library verifier is
[`../verifiers/verify_local_hybrid_degree4_rank_color_clique.py`](../verifiers/verify_local_hybrid_degree4_rank_color_clique.py).

The witness fails total degree five.  No simultaneous edge-coloring of
\(K_{41}\), and no rank-five Gram realization, is asserted.

## 1. Pair and triple data

The ordered pair counts are
\[
 (170,6,262,652,550).
\]
The nonzero unordered triangle-type counts are
\[
\begin{array}{c|rrrrrrrrrr}
004&275&014&17&023&302&024&789&033&774\\
034&883&114&3&123&30&133&5&134&59\\
222&25&223&397&224&242&233&629&234&1763\\
244&243&333&651&334&1564&344&1383&444&626 .
\end{array}
\]
They sum to \(\binom{41}{3}=10660\), and their five edge incidences are
\[
 (3315,117,5109,12714,10725)
 =39(85,3,131,326,275).
\]
Every used triangle has positive \(3\times3\) Gram determinant.  The
smallest is
\[
\frac{278991}{3125000}
\]
at type \(244\).

The matrix of centered color-wedge counts is
\[
W=\begin{pmatrix}
275&17&1091&2733&2239\\
17&3&30&99&82\\
1091&30&714&4147&3522\\
2733&99&4147&4925&8599\\
2239&82&3522&8599&3504
\end{pmatrix}.
\]

## 2. The support-specific neighborhood-clique lemma

Let colors \(0,1,4\) denote respectively the inner products
\(-77/100,-7/10,499/1000\).

**Lemma.**  In a rank-at-most-five Gram realization on this support,
\[
d_0(x)+d_1(x)\leq5                                      \tag{1}
\]
at every vertex \(x\).  Consequently,
\[
W_{01}+2W_{11}\leq4D_1,                                 \tag{2}
\]
where \(D_1=\sum_xd_1(x)\).

**Proof.**  Exact substitution in
\[
\Delta(u,v,t)=1+2uvt-u^2-v^2-t^2
\]
shows that, for \(u,v\in\{-77/100,-7/10\}\), all four negative support
values give \(\Delta<0\), while \(t=499/1000\) gives
\(\Delta>0\).  Thus any two color-\(\{0,1\}\) neighbors of \(x\) have
mutual color \(4\).

Those neighbors therefore have a Gram matrix with diagonal \(1\) and
constant off-diagonal entry \(s=499/1000\).  For six such vectors its
eigenvalues would be
\[
1-s\quad\text{(multiplicity five)},\qquad 1+5s,
\]
both strictly positive.  Its rank would be six, impossible in
\(\mathbb R^5\).  This proves (1).

For nonnegative integral \(d_0,d_1\) satisfying (1),
\[
d_0d_1+d_1(d_1-1)
=d_1(d_0+d_1-1)\leq4d_1.
\]
Summing over vertices gives (2). \(\square\)

For the certificate,
\[
W_{01}+2W_{11}=17+2\cdot3=23<24=4D_1.
\]
This lemma also exposes the exact defect in two earlier relaxation
witnesses: their pairs \((W_{01},W_{11})=(30,3)\) and \((24,3)\)
violate (2).

## 3. Exact analytic checks

Using the polynomial normalization documented in
[`weighted_residual_barrier.md`](weighted_residual_barrier.md), every
principal minor of every total-degree-four BV block is positive.  The
smallest principal minor in each harmonic block is printed by the
verifier; no floating eigenvalue is used.

For the rank-five moment consequence,
\[
A=\frac{5933759}{820000},\qquad
T=\frac{116433421869}{2562500000},
\]
and the fixed-rank residual is
\[
E=\frac{34689369}{2562500000}.
\]
The exact C047 expression is
\[
20(41E)^2-9\bigl(41(A-36/5)\bigr)^3
=-\frac{587191589183847267}{25000000000000000}<0.
\]

The centered covariance of the five degree columns is
\[
\frac1{41}\begin{pmatrix}
620&-323&191&1213&-1701\\
-323&456&-342&147&62\\
191&-342&646&-797&302\\
1213&147&-797&5478&-6041\\
-1701&62&302&-6041&7378
\end{pmatrix}.
\]
All principal minors are nonnegative.  The full determinant is the sole
zero principal minor, forced by \(\sum_qd_q(x)=40\); the least positive
principal minor is \(456/41\).

## 4. Exact graph-moment audit

The certificate contains eleven joint degree-vector types with total
multiplicity 41.  Every row sums to 40 and reproduces all first moments
\(D_q\), same-color wedge moments \(W_{qq}\), and mixed moments
\(W_{qr}\).

The rows satisfy \(d_0+d_1\leq5\).  Their negative-union degrees
\[
d_0+d_1+d_2+d_3=40-d_4
\]
range from 22 to 30.  Thus the negative graph has 545 edges, minimum
degree 22, and passes the independently proved requirements of at least
144 edges and minimum degree seven.

For each of the 31 nonempty color subsets \(S\), the verifier forms the
41 integers
\[
d_S(x)=\sum_{q\in S}d_q(x)
\]
and checks the exact Erdős--Gallai inequalities.  Every sequence is
graphical.  It also computes the four induced three-vertex motif counts
\((n_0,n_1,n_2,n_3)\) for every color union and verifies nonnegativity.
For the five individual colors these are
\[
\begin{array}{c|rrrr}
0&7620&2765&275&0\\
1&10546&111&3&0\\
2&6240&3756&639&25\\
3&2220&4817&2972&651\\
4&2813&5595&1626&626 .
\end{array}
\]

These checks are necessary but not sufficient for one simultaneous
five-coloring of all edges of \(K_{41}\).  In particular, separate
Erdős--Gallai witnesses cannot be superimposed without further proof.

## 5. The anchored exact cap kernel does not separate

Let \(F\) be the independently certified degree-10 one-sided cap kernel
from [`one_sided_cap_degree10_bound.md`](one_sided_cap_degree10_bound.md).
For each row \(x\), apply its positive-kernel identity to the positive
neighbors of \(x\), whose common height is \(s=499/1000\), and then sum
over \(x\).  The result is the exact linear triple functional
\[
\begin{aligned}
S={}&D_4F(s,s,1)
 +2\sum_{i=0}^3 n_{i44}F(s,s,t_i)
 +6n_{444}F(s,s,s).
\end{aligned}
\]
The verifier evaluates the 506-monomial rational polynomial exactly and
gets
\[
S=
\frac{
10900679016442230075787594834809436525730644961751705316478717975134361189524810533654029
}{
1059717120000000000000000000000000000000000000000000000000000000000000000000000000000
}>0.
\]
Thus this valid anchored cap-SDP inequality has very large slack here and
does not cut the witness.

## 6. Sharp scoped failure at the next degree

The total-degree-five, harmonic-degree-four block has the negative
diagonal entry
\[
-\frac{
894220395027688277353640397221
}{
20500000000000000000000000000000
}<0.
\]
So the witness does not pass degree five.  This is a concrete target for
the next search and prevents any accidental claim that arbitrary-degree
BV positivity has been established.

## 7. Reproduction and dependency map

Run from the repository root:

```bash
PYTHONPATH=. /usr/bin/python3 \
  verifiers/verify_local_hybrid_degree4_rank_color_clique.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  tests.test_local_hybrid_degree4_rank_color_clique -v
```

The dependency chain is
\[
\text{JSON integers/rationals}
\Longrightarrow
\begin{cases}
\text{pair/triple incidence and Gram-minor checks},\\
\text{degree-four BV principal minors},\\
\text{C047 exact residual},\\
\text{color covariance principal minors},\\
\text{rank-forced clique inequality},\\
\text{joint degree and all-union graph/motif checks}
\end{cases}
\Longrightarrow
\text{certified relaxation barrier}.
\]

The anchored-cap calculation additionally depends on the separately
verified rational Gram factors in
`one_sided_cap_degree10_bound.json`.  It is reported only as a failed
separator, not as a new theorem.
