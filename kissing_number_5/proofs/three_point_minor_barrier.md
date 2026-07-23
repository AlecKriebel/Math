# An Exact Trianglewise-PSD Barrier at \(N=41\)

This note strengthens the pseudo-incidence construction in
`four_point_wedge.md`.  It gives a complete graph on 41 labeled vertices
whose edge labels have the same exact pair distribution, satisfy every
ordinary dimension-five Gegenbauer inequality and Pfender row inequality,
and make every \(3\times3\) principal Gram matrix positive definite.

It is still not a Gram matrix: the first obstruction appears in order four.
Thus this is a limitation theorem for local principal-minor tests, not a
spherical-code construction.

## Exact labels

The six labels and ordered multiplicities are
\[
\begin{array}{c|rrrrrr}
t&-157/200&-39/50&-9/20&-1/10&-19/200&99/200\\ \hline
\#\{(i,j):i\ne j,\ g_{ij}=t\}
 &32&132&264&130&522&560.
\end{array}
\tag{1}
\]
The verifier stores three nontrivial edge sets explicitly and constructs the
remaining two by lexicographic partition.

The union \(L\) of the first two classes is a 4-regular, girth-six graph on
41 vertices.  Its 16 edges labeled \(-157/200\) form a matching.  Because
\(L\) has no triangles or quadrilaterals, its unordered distance-two set has
exactly
\[
 41{4\choose2}=246
\]
members.  Every one receives the high label \(99/200\).  Another 34
explicit edges complete the 280-edge high graph.

There are only two ways, after this compulsory assignment, for a triangle
containing an edge of \(L\) to have negative determinant:

- its two other edges both have label \(99/200\);
- its two other edges both have label \(-9/20\).

The 34 extra high edges were chosen so that the endpoints of no edge of
\(L\) have a common neighbor in the high graph.  The explicit 132-edge
\(-9/20\) class has the analogous property.  Girth six is essential for the
first condition: a common distance-two neighbor of the endpoints of an
\(L\)-edge would give a 5-cycle.

The remaining 326 edges receive labels \(-1/10\) and \(-19/200\) in counts
65 and 261.  Direct rational evaluation of all \({41\choose3}=10660\)
determinants gives
\[
 \min_{|S|=3}\det G[S]
 =\frac{34771}{400000}>0.                         \tag{2}
\]
The minimum occurs for \(S=\{0,1,33\}\).

The high graph has degree multiset
\[
 12^1,\ 13^{12},\ 14^{28}.
\]
Pfender's weighted deep-row sums are, vertex by vertex, either
\[
 \frac{542}{625}\quad\hbox{or}\quad\frac{17657}{20000},
\]
so every row is strictly feasible.

## Two-point positivity

Since (1) has the same pair distribution as the exact witness in
`four_point_wedge.md`, its dimension-five Gegenbauer moments are strictly
positive in every degree.  Exact recurrence through degree 103 gives the
unnormalized minimum
\[
 41+\sum_i c_iP_2(t_i)=\frac{30261}{16000}.
\]
For the analytic tail,
\[
 1-t_i^2\geq\frac{15351}{40000},\qquad
 (1-t_i^2)^{-3/2}<\frac{17}{4}.
\]
The bound from `two_point_lp_barrier.md` therefore makes the normalized
off-diagonal tail less than \(1054/k^{3/2}<1\) for \(k\geq104\), because
\(1054^2<104^3\).

## Exact first obstruction

All principal minors through order three are positive, but order four fails
widely.  Exact enumeration of the \({41\choose4}=101270\) quadruples finds

\[
\begin{aligned}
\#\{S:|S|=4,\det G[S]<0\}&=10670,\\
\#\{S:|S|=4,\det G[S]=0\}&=0.
\end{aligned}
\]

There are 192 isomorphism types of negative edge-labeled \(K_4\)'s.  The
smallest determinant is
\[
 \det G[\{0,2,7,34\}]
 =-\frac{2436203}{3125000}.                         \tag{3}
\]
In the vertex order \(0,2,7,34\), its six off-diagonal labels are
\[
\left(
-\frac{157}{200},-\frac9{20},-\frac1{10},
-\frac1{10},-\frac9{20},-\frac{39}{50}
\right).
\]
This exact obstruction prevents any accidental claim that trianglewise PSD
or the negative-wedge family supplies a global PSD Gram matrix.

## What the certificate proves

The labeled object simultaneously satisfies:

1. all pair counts and pair parity constraints;
2. all ordinary dimension-five Gegenbauer moment inequalities;
3. Pfender's weighted inequality in every row;
4. all local deep-degree and mixed wedge constraints from
   `four_point_wedge.md`;
5. every \(2\times2\) and \(3\times3\) principal PSD constraint.

It does not satisfy all \(4\times4\) principal constraints, global PSD,
rank at most five, or Bachoc--Vallentin matrix positivity.  Any successful
upper-bound mechanism must add at least one of these genuinely stronger
compatibility conditions.

## Reproduction

Run:

```sh
python3 verifiers/verify_three_point_minor_barrier.py
python3 -m unittest tests.test_three_point_minor_barrier -v
```
