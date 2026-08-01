# Exact certificate for the universal dB obstruction

Let `G` have `n>=3` vertices.  The proof divides according to its
positive-weight support.

## Certificate A: missing-edge gap

If `s_i` is the support degree of vertex `i`, then direct analysis of the
infinite-fitness chain gives

\[
 L_G=\frac1n\sum_i\frac{s_i}{s_i+1}.
\]

The complete-limit gap has the termwise nonnegative decomposition

\[
 \boxed{
 \frac{n-1}{n}-L_G
 =\sum_i\frac{n-1-s_i}{n^2(s_i+1)}.}
\]

Every denominator is positive.  A missing edge makes at least one numerator
strictly positive, so the gap is strict.

## Certificate B: complete-support first-order gap

Suppose every `w_ij>0`.  With `d_i=sum_{j!=i}w_ij`, direct expansion of
the absorbing equations gives

\[
 \rho_{\rm dB}(G,r)
 =\frac{n-1}{n}-\frac{a_G}{r}+O(r^{-2}),
\]

where

\[
 a_G=\frac1{n^2(n-2)}
 \sum_i\sum_{j\ne i}\frac{d_i-w_{ij}}{w_{ij}}.
\]

The difference from the complete-graph coefficient is certified by

\[
 \boxed{
 a_G-\frac{n-1}{n}
 =\frac1{n^2(n-2)}
 \sum_i\sum_{\substack{j<k\\j,k\ne i}}
 \frac{(w_{ij}-w_{ik})^2}{w_{ij}w_{ik}}.}
\]

To verify the identity at a fixed vertex, expand

\[
 \sum_{j<k}\frac{(w_{ij}-w_{ik})^2}{w_{ij}w_{ik}}
 =\left(\sum_jw_{ij}\right)
  \left(\sum_j\frac1{w_{ij}}\right)-(n-1)^2.
\]

All denominators are positive and every numerator is a square.  Equality
forces all edges incident to every vertex to have equal weight.  Symmetry and
complete support force a single global edge weight, which is exactly a scaled
copy of `K_n`.  Otherwise the coefficient gap is strict, and therefore the
fixation comparison is negative for every sufficiently large finite `r`.

For `n=2`, the only connected loopless weighted graph has one edge and dB
fixation is identically `1/2`, equal to the baseline.

