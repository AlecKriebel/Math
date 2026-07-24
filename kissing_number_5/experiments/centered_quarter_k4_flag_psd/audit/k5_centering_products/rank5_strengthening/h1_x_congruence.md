# Exact H1 quarter-grid congruence

## Lemma

Let \(C=\{x_1,\ldots,x_{41}\}\) be a centered spherical code whose
off-diagonal inner products lie in

\[
 \left\{\frac a4:a\in\{-4,-3,-2,-1,0,1,2\}\right\}.
\]

For each \(a\), let \(m_a\) be the number of unordered pairs
\(\{i,j\}\) with \(i<j\) and
\(\langle x_i,x_j\rangle=a/4\).  Put

\[
 Q=\sum_a a^2m_a,\qquad
 V=\operatorname{tr}(G^2)-\frac{41^2}{5},\qquad X=40V,
\]

where \(G\) is the Gram matrix of \(C\).  Then

\[
 X=5Q-11808\quad\hbox{and}\quad X\equiv2\pmod {10}.
\]

In particular, the branch \(X=13\) contains no centered 41-point
quarter-grid code.

## Proof

Centering means \(\sum_i x_i=0\), hence

\[
 0=\left\|\sum_i x_i\right\|^2
   =41+2\sum_{i<j}\langle x_i,x_j\rangle
   =41+\frac12\sum_a a m_a.
\]

Therefore

\[
 \sum_a a m_a=-82.
\]

Since \(a^2\equiv a\pmod2\),

\[
 Q=\sum_a a^2m_a
   \equiv\sum_a a m_a
   \equiv0\pmod2.
\]

The squared Gram trace is

\[
 \operatorname{tr}(G^2)
 =41+2\sum_a m_a\left(\frac a4\right)^2
 =41+\frac Q8.
\]

Consequently

\[
 X
 =40\left(41+\frac Q8-\frac{1681}{5}\right)
 =5Q-11808.
\]

Because \(Q\) is even, \(5Q\equiv0\pmod {10}\), while
\(-11808\equiv2\pmod {10}\).  This proves the congruence and excludes
\(X=13\).  No PSD, rigidity, contact-graph, or solver assumption is used.

## Scope

This lemma uses both exact quarter-grid multiplicities and exact centering.
It does not apply to a continuous pseudodistribution whose pair masses are
not empirical multiples of \(2/41\).  Such a relaxation may therefore
contain an \(X=13\) witness without contradicting the lemma.
