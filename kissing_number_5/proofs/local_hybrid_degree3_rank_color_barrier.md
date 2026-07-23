# A Triple Pseudo-Measure Passing Degree-Three BV, C047, and Color Moments

## Certified barrier

On the exact five-node pair support from `local_hybrid_barrier.md`, an
integral fixed-\(41\) triple pseudo-distribution simultaneously satisfies

- strict triangle Gram feasibility and the exact fixed-\(N\) marginals;
- all proved deep-wedge, mixed-wedge, and small-color capacities;
- every Bachoc--Vallentin block through total degree three;
- the sharp rank-five spectral inequality C047;
- positive semidefiniteness of the full centered color-degree moment
  matrix; and
- basic individual-color degree-sequence and three-vertex motif
  consistency.

This is the strongest five-node triple barrier in this sequence.  It is
still not asserted to arise from one edge-colored complete graph, much less
from a rank-five Gram matrix.

The exact certificate and standard-library verifier are
`certificates/local_hybrid_degree3_rank_color_pseudodistribution.json` and
`verifiers/verify_local_hybrid_degree3_rank_color.py`.

## Counts

The pair atoms and ordered counts are
\[
\begin{array}{c|rrrrr}
\text{type}&0&1&2&3&4\\ \hline
t&-77/100&-7/10&-11/25&-9/100&499/1000\\
c_t&170&6&262&652&550.
\end{array}                                      \tag{1}
\]
The nonzero unordered triple counts are
\[
\begin{array}{c|r@{\quad}c|r@{\quad}c|r}
004&275&014&30&023&197\\
024&814&033&861&034&863\\
114&3&123&3&124&9\\
133&36&134&33&222&43\\
223&668&224&140&233&126\\
234&1967&244&248&333&848\\
334&1520&344&1353&444&623.
\end{array}                                      \tag{2}
\]
They sum to \(10660={41\choose3}\), and their edge-type incidences are
\[
(3315,117,5109,12714,10725)
=39(85,3,131,326,275).                           \tag{3}
\]
Every supported triangle has positive Gram determinant, with exact minimum
\[
\Delta(244)=\frac{278991}{3125000}.              \tag{4}
\]

## Wedge and color-degree data

Let \(W_{qr}=\sum_vd_q(v)d_r(v)\) for \(q\ne r\), and let
\(W_{qq}=\sum_v{d_q(v)\choose2}\).  The counts (2) give
\[
W=\begin{pmatrix}
275&30&1011&2782&2257\\
30&3&12&108&78\\
1011&12&937&3755&3566\\
2782&108&3755&5087&8609\\
2257&78&3566&8609&3470
\end{pmatrix}.                                   \tag{5}
\]
In particular,
\[
W_{\{0\}}=275,\qquad
W_{\{0,1\}}=275+30+3=308.                        \tag{6}
\]
The mixed value \(30\) and type-\(1\) value \(3\) attain the universal
caps
\[
\sum_vd_0(v)d_1(v)\le5\sum_vd_1(v)=30,\qquad
\sum_v{d_1(v)\choose2}\le{3\choose2}=3.           \tag{7}
\]
The verifier also checks the integer-envelope/common-center inequality at
every threshold event cell in \(3/8<q\le3/4\), including boundaries.

For a common colored graph, set
\[
S_{qq}=c_q+2W_{qq},\qquad S_{qr}=W_{qr}\quad(q\ne r),
\]
and
\[
\Sigma=S-\frac1{41}cc^{\mathsf T}.               \tag{8}
\]
This \(\Sigma\) must be positive semidefinite.  Here it is: exact evaluation
of every principal minor finds only the structurally forced zero full
determinant, while every proper principal minor is positive.  The least
positive minor is
\[
\frac{456}{41}.                                  \tag{9}
\]

The first two same-color degree moments also admit graphical degree
sequences.  One exact choice of degree multiplicities for colors
\(0,\ldots,4\) is
\[
\begin{array}{c|l}
0&2^1,\,3^2,\,4^{28},\,5^{10}\\
1&0^{37},\,1^3,\,3^1\\
2&0^8,\,1^1,\,7^1,\,8^{25},\,9^6\\
3&0^1,\,3^1,\,14^1,\,15^1,\,16^9,\,17^{28}\\
4&4^1,\,10^1,\,13^{10},\,14^{29}.
\end{array}                                      \tag{10}
\]
The verifier checks their vertex counts, degree sums, wedge sums, and every
Erdős--Gallai inequality.

For each color, the numbers of three-vertex induced subgraphs having
\(0,1,2,3\) edges are respectively
\[
\begin{array}{c|rrrr}
0&7620&2765&275&0\\
1&10546&111&3&0\\
2&6445&3364&808&43\\
3&2185&5084&2543&848\\
4&2782&5654&1601&623.
\end{array}                                      \tag{11}
\]
All are nonnegative and sum rowwise to \({41\choose3}\).  Equations
(8)--(11) are necessary consistency checks, not a simultaneous edge-coloring
construction.

## Degree-three BV and C047

Using the exact normalization of
`fixed41_three_point_formulation.md`, every principal minor of
\(H_{k,3}\) is positive for \(0\le k\le3\).  The least principal minors are
\[
\begin{array}{c|c|c}
k&\text{indices}&\text{least value}\\ \hline
0&(1,3)&
\dfrac{221539235618740811524443}
      {2101250000000000000000000}\\[2mm]
1&(1,2)&
\dfrac{621858663885311425191787767}
      {21012500000000000000000000000}\\[2mm]
2&(1)&
\dfrac{4214023039816497247}
      {12300000000000000000}\\[2mm]
3&(0)&
\dfrac{19116262265659420051}
      {4100000000000000000}.
\end{array}                                      \tag{12}
\]

For C047, the fixed-\(41\) moments are
\[
\begin{aligned}
A&=\frac{5933759}{820000},&
T&=\frac{931389435561}{20500000000},\\
\delta&=A-\frac{36}{5}=\frac{29759}{820000},&
E&=T-\frac{1116}{25}-\frac{108}{5}\delta
  =\frac{199575561}{20500000000}.
\end{aligned}                                    \tag{13}
\]
The exact rank-five residual is strictly feasible:
\[
20D^2-9V^3
=-\frac{661559877254042433}
        {25000000000000000}<0,                   \tag{14}
\]
where \(V=41\delta\) and \(D=41E\).

## Exact next obstruction

The same pseudo-measure fails at total degree four.  The \(k=4\) scalar is
\[
H_{4,4}
=-\frac{1924383662903127930296851}
        {4100000000000000000000000}<0.            \tag{15}
\]
Thus all checks above are still insufficient at the triple-measure level,
while a very simple next harmonic condition eliminates this assignment.
The remaining distinction is essential: no result here asserts a common
colored graph, a Gram matrix, or a spherical code.

## Reproduction

The discovery MILP and its floating-point eigenvalues are not trusted.
The verifier recomputes (3)--(15) with `fractions.Fraction`; the
Erdős--Gallai checks use exact integers.  Certificate SHA-256:
```
79febcf2a4d237b0dcf1d5bed839a74251b58af90d645a569f678db779bd73b3
```

Run
```
/usr/bin/python3 verifiers/verify_local_hybrid_degree3_rank_color.py
/usr/bin/python3 -m unittest tests.test_local_hybrid_degree3_rank_color -v
```
