# Pointwise Analysis and an Exact Barrier for the Weighted-Residual Cut

The degree-three inequality
\[
\Phi_f=\frac1N\sum_i
\left\|\sum_{j\ne i}f(g_{ij})
(x_j-g_{ij}x_i)\right\|^2\ge0,\qquad
f(u)=u-\frac83u^2,                                \tag{1}
\]
separates the degree-two BV pseudo-object in
`degree2_bv_barrier.md`.  This note asks whether (1), together with
triangle PSD, Pfender's inequality, and the deep-wedge counts, also
eliminates the exact pair distribution in `local_hybrid_barrier.md`.

It does not.  An exact integral triple pseudo-incidence survives all of
those named scalar tests and every fixed-\(N\) BV block through total
degree two.  This is a barrier result, not a spherical code.  The verifier
is `verifiers/verify_weighted_residual_barrier.py`.

## Pointwise determinant-domain bounds

For a centered triple put
\[
 u=g_{ij},\qquad v=g_{ik},\qquad t=g_{jk},\qquad
 w=t-uv.
\]
The \(3\times3\) Gram determinant condition is exactly
\[
 |w|\le s(u,v):=\sqrt{(1-u^2)(1-v^2)},             \tag{2}
\]
and the kissing constraint adds
\[
 w\le\frac12-uv.                                  \tag{3}
\]
The centered summand in (1) is
\[
 K_f(u,v,t)=f(u)f(v)(t-uv)=f(u)f(v)w.             \tag{4}
\]
Since it is affine in \(t\), its sharp lower endpoint on the determinant
interval is immediate:
\[
K_f(u,v,t)\ge
\begin{cases}
-f(u)f(v)s(u,v),&f(u)f(v)\ge0,\\
f(u)f(v)\min\{s(u,v),\,1/2-uv\},&f(u)f(v)<0.
\end{cases}                                       \tag{5}
\]
In particular,
\[
 K_f(u,v,t)\ge-|f(u)f(v)|s(u,v).                  \tag{6}
\]
This is the strongest pointwise lower bound available from only (2)--(3).
It is too weak after summation: it forgets exactly the global residual
compatibility that makes (1) useful.

The signs of \(f\) are
\[
 f(u)<0\quad(u<0\ \hbox{or}\ 3/8<u\le1/2),\qquad
 f(u)>0\quad(0<u<3/8).                            \tag{7}
\]
Every atom of the local-hybrid pair witness lies in the negative-sign
region.  Consequently (3) also gives, row by row,
\[
\begin{aligned}
0\le \Phi_{f,i}
&\le
\frac12\left[
\left(\sum_{j\ne i}f(g_{ij})\right)^2
+\sum_{j\ne i}f(g_{ij})^2\right]\\
&\hspace{35mm}
-\left(\sum_{j\ne i}g_{ij}f(g_{ij})\right)^2.
\end{aligned}                                     \tag{8}
\]
The right side of (8) is positive with a large margin at the average row
of the pair witness, so this pointwise threshold does not separate it.

## Pair data

The five atoms and ordered edge counts are
\[
\begin{array}{c|rrrrr}
\text{type}&0&1&2&3&4\\ \hline
t&-77/100&-7/10&-11/25&-9/100&499/1000\\
c_t&170&6&262&652&550.
\end{array}                                       \tag{9}
\]
Thus the unordered edge counts are
\[
(85,3,131,326,275).
\]

Let \(n_{abc}\) denote the number assigned to the unordered triple orbit
with sorted edge types \((a,b,c)\).  Every pseudo-incidence below obeys
\[
\sum_{a,b,c}\operatorname{mult}_q(a,b,c)n_{abc}
=39E_q,                                           \tag{10}
\]
where \(E_q\) is the unordered edge count.  For types \(0,\ldots,4\), the
two sides of (10) are
\[
3315,\ 117,\ 5109,\ 12714,\ 10725.                \tag{11}
\]

## Two exact directions that reject the first attempt

The first integral pseudo-incidence used the counts
\[
\begin{array}{c|r@{\qquad}c|r@{\qquad}c|r}
(0,0,4)&270&(0,1,4)&24&(0,2,4)&201\\
(0,3,3)&2550&(1,2,4)&93&(2,3,3)&546\\
(2,4,4)&4269&(3,3,3)&2174&(4,4,4)&533.
\end{array}                                       \tag{12}
\]
It passes (1), but two full degree-two blocks fail.

For \(p(u)=1/5+u-u^2\), every genuine configuration satisfies the
scalar-square inequality
\[
\frac1N\sum_i\left(\sum_jp(g_{ij})\right)^2\ge0.   \tag{13}
\]
This is the total-degree-two \(k=0\) quadratic form in direction
\((1/5,1,-1)\).  On (12), its exact value is
\[
-\frac{804424208380157}{20500000000000}<0.        \tag{14}
\]

For \(q(u)=1/5+u\), the \(k=1\) residual identity gives
\[
\frac1N\sum_i
\left\|\sum_{j\ne i}q(g_{ij})
      (x_j-g_{ij}x_i)\right\|^2\ge0.              \tag{15}
\]
The direction is \((1/5,1)\), and its value on (12) is
\[
-\frac{2007505237299643}{20500000000000}<0.       \tag{16}
\]
Equations (13) and (15) are the requested human-readable explanations of
the two negative matrices; no eigenvalue rounding is involved.

## A stronger exact integral pseudo-incidence

Reassign the same fixed triple marginals as follows:
\[
\begin{array}{c|r@{\quad}c|r@{\quad}c|r}
(0,0,4)&275&(0,1,4)&30&(0,2,4)&508\\
(0,3,4)&2227&(1,1,4)&3&(1,3,4)&81\\
(2,2,2)&7&(2,2,3)&2066&(2,2,4)&224\\
(3,3,3)&227&(3,3,4)&3313&(3,4,4)&1033\\
(4,4,4)&666&&&
\end{array}                                       \tag{17}
\]
These 13 nonnegative integers sum to
\[
\sum n_{abc}={41\choose3}=10660,                  \tag{18}
\]
and satisfy all five equations (10).

Every supported triple is strictly Gram-feasible.  The minimum is
\[
\det(0,0,4)=\frac{392283}{2500000}>0.             \tag{19}
\]
Thus (17) is an exact, boundary-safe triple pseudo-measure with orbit
mass \(6n_{abc}/41\).

## Exact wedge and Pfender compatibility

For type 0 alone, (17) has
\[
W_0=n_{004}=275.                                  \tag{20}
\]
This is compatible with the Pfender degree cap via the degree multiset
\[
3^5,\ 4^{25},\ 5^{11},
\]
because
\[
5\cdot3+25\cdot4+11\cdot5=170,\qquad
5{3\choose2}+25{4\choose2}+11{5\choose2}=275.
\tag{21}
\]
It saturates the 275 high endpoint pairs under the multiplicity-one
wedge inequality.

For types 0 and 1 together,
\[
W_{01}=n_{004}+n_{014}+n_{114}=275+30+3=308.
\tag{22}
\]
This exceeds the integer-envelope minimum 294 and is far below the
common-center capacity \(3\cdot275\) at \(a=7/10\).

The very small type-1 class is used compatibly with its edge count.  Its
three edges may form a 3-star on four type-0 degree-five vertices.  This
produces
\[
5(3+1+1+1)=30=n_{014}
\]
mixed wedges and exactly
\[
{3\choose2}=3=n_{114}
\]
type-1/type-1 wedges.  The type-0 rowwise Pfender cost remains at most
\[
5\left(2(77/100)^2-1\right)=\frac{929}{1000}<1.
\tag{23}
\]

## Full degree-two BV positivity and \(\Phi_f\)

Every principal minor of every total-degree-two block \(k=0,1,2\) is
strictly positive.  The smallest principal minors in the three blocks are
\[
\begin{array}{c|c}
k&\text{minimum exact principal minor}\\ \hline
0&3259537/2562500\\
1&3760571867797/10250000000000\\
2&3791123972203/10250000000000.
\end{array}                                       \tag{24}
\]
Since all lower-degree blocks are principal submatrices, (24) proves full
fixed-\(N\) BV feasibility through total degree two.

The degree-three weighted-residual scalar also survives:
\[
\boxed{\
\Phi_f=
\frac{35272233739927717}
     {90087890625000000}>0.
\ }                                                \tag{25}
\]
Its margin is approximately \(0.3915\).

## Exact scope boundary

The counts in (17) are not asserted to arise from one edge-colored
complete graph.  Their first BV failure is the total-degree-three \(k=0\)
block.  With
\[
r(u)=\frac15+u-u^2+u^3,
\]
the universal scalar-square inequality
\[
\frac1N\sum_i\left(\sum_jr(g_{ij})\right)^2\ge0    \tag{26}
\]
has exact pseudo-value
\[
-\frac{94089968136590201847}
       {10250000000000000000}<0.                  \tag{27}
\]

What (17) proves is precise: triangle PSD, exact integral fixed-\(41\)
marginals, the strongest obvious edge-count restrictions on the two deep
classes, the Pfender degree pattern, every full BV block through total
degree two, and the degree-three scalar (1) still do not eliminate the
local-hybrid pair distribution.  The next obstruction must use another
degree-three radial direction, a higher-order incidence condition, or
realizability by one common edge-colored graph.

## Reproduction

Run:

```sh
python3 verifiers/verify_weighted_residual_barrier.py
python3 -m unittest tests.test_weighted_residual_barrier -v
```
