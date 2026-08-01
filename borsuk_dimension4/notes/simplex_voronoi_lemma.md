# A regular-simplex cell lemma

## Statement in dimension four

Let \(S\subset\mathbb R^4\) have diameter one. If \(S\) contains five
points at pairwise distance one, then \(S\) has a partition into five sets,
each of squared diameter at most

\[
  \frac{18-8\sqrt 3}{5}<1.
\]

Consequently, the diameter graph of any finite counterexample to the
five-part Borsuk assertion in dimension four must be \(K_5\)-free.

This lemma applies to arbitrary sets, not just finite or compact sets, because
the displayed bound supplies a uniform strict gap.

## Proof

It is convenient to prove a slightly more general coordinate estimate. Put
\(n=d+1\), let

\[
 H=\left\{x\in\mathbb R^{d+1}:\sum_{j=0}^d x_j=0\right\},\qquad
 q_j=\frac{e_j-\frac1{d+1}{\bf1}}{\sqrt2}.
\]

The \(q_j\) form a regular \(d\)-simplex of edge length one in \(H\), and
\(\lVert q_j\rVert^2=d/(2(d+1))\). After a Euclidean isometry, the five
diameter points in the statement are these vertices with \(d=4\). Every point
of \(S\) then lies in

\[
 K=\bigcap_{j=0}^d \overline B(q_j,1).
\]

For \(x\in H\), write \(z=\sqrt2x\) and
\(T=\sum_jz_j^2\). The inequalities \(x\in K\) are exactly

\[
 z_j\ge L:=\frac T2-\frac{d+2}{2(d+1)}\quad(0\le j\le d). \tag{1}
\]

Let

\[
 C_i=\{x\in K:z_i\ge z_j\text{ for every }j\}
\]

be the closed nearest-vertex Voronoi cell, and put \(M=z_i\). Since the
coordinates sum to zero, \(M\ge0\). Summing (1) shows
\(T\le(d+2)/(d+1)\); equality would force all coordinates to be zero, so the
inequality is strict. In particular \(L\le0\).

For every \(j\ne i\), one has \(L\le z_j\le M\), hence

\[
 (z_j-L)(M-z_j)\ge0,
 \qquad
 z_j^2\le(M+L)z_j-LM.
\]

Because \(\sum_{j\ne i}z_j=-M\), summing these \(d\) inequalities and adding
\(M^2\) gives

\[
 T\le-(d+1)LM
   =\frac M2\bigl(d+2-(d+1)T\bigr). \tag{2}
\]

Specialize now to \(d=4\). From (2),

\[
 M\ge \frac{T}{3-5T/2}.
\]

When \(0\le T\le4/5\), elementary one-variable maximization gives

\[
 T-M\le T-\frac{T}{3-5T/2}
 \le \frac{8-4\sqrt3}{5}. \tag{3}
\]

Indeed, after setting \(u=3-5T/2\in[1,3]\), the unique interior maximum is
at \(u=\sqrt3\). When \(4/5\le T<6/5\), the denominator in (3) is at most
one, so (2) instead gives \(M\ge T\), and (3) remains true.

Since \(\lVert q_i\rVert^2=2/5\) and
\(\langle x,q_i\rangle=z_i/2=M/2\), (3) yields

\[
 \left\lVert x-\frac{q_i}{2}\right\rVert^2
 =\frac{T-M}{2}+\frac1{10}
 \le\frac{9-4\sqrt3}{10}=:R^2. \tag{4}
\]

Thus \(C_i\) lies in a ball of radius \(R\). The triangle inequality gives

\[
 \operatorname{diam}(C_i)^2\le4R^2
 =\frac{18-8\sqrt3}{5}<1,
\]

where the final strict inequality is equivalent to
\(13<8\sqrt3\), whose square is \(169<192\).

Assign each point of \(S\) to any cell for which its corresponding coordinate
is maximal. This produces five disjoint parts, each contained in one \(C_i\),
and proves the claim. Ties require no special treatment.

## Graph-first corollary

The five vertices of a \(K_5\) in a diameter graph in \(\mathbb R^4\) must be
the regular simplex above. The cell partition colors the entire diameter graph
with five colors and, more strongly, controls all within-color distances by a
fixed factor below the diameter. Therefore every counterexample search may
exclude graphs containing \(K_5\), rather than merely excluding \(K_6\).

There is also a local obstruction worth recording. A point at unit distance
from four vertices of this simplex lies on the line normal to their opposite
facet. The two solutions are the omitted simplex vertex and its reflection in
that facet; the reflected point has squared distance \(5/2\) from the omitted
vertex.
Hence no distinct point of a diameter-one set can be adjacent to four vertices
of a diameter \(K_5\). This independently rules out the direct Mycielski
extension of \(K_5\).
