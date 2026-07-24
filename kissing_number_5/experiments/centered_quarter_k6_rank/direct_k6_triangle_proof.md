# Exact direct rank-five K6 triangle-marginal extension

## Statement

The exact centered quarter-grid pair/triple pseudodistribution has a
symmetric local realization on 51 positive-weight \(6\times6\) Gram
matrices such that every atom:

- has diagonal 1 and off-diagonal entries in
  \(\{-1,-3/4,-1/2,-1/4,0,1/4,1/2\}\);
- is positive semidefinite;
- has rank exactly five;
- has maximum off-diagonal entry at most \(1/2\).

The marginal of a uniformly chosen triangle is exactly the stored centered
triple distribution \(\nu/1560\), and the marginal of a uniformly chosen
edge is exactly \(\alpha/40\).

This is a local consistency theorem, not a spherical-code construction.
It supplies no compatibility between overlapping K6 atoms in a common
41-vertex object.

## Exact certificate

The file `direct_k6_triangle_extension.json` stores 51 edge-color vectors
and exact rational weights.  The standard-library verifier independently:

1. authenticates the centered pair/triple source;
2. rebuilds every scaled integer Gram matrix;
3. checks every principal minor of orders 1 through 6;
4. checks that every full determinant is zero and that every atom has a
   positive fifth-order principal minor, proving rank exactly five;
5. reconstructs all 20 triangle types and all 15 edge colors per atom;
6. verifies the weights are positive and sum to one;
7. verifies the exact count identities
   \[
   \mathbb E[\#\text{ triangles of type }i]=\frac{\nu_i}{78},
   \qquad
   \mathbb E[\#\text{ edges of color }j]=\frac{3\alpha_j}{8}.
   \]

Dividing by 20 and 15 respectively gives the uniform-face marginals
\(\nu_i/1560\) and \(\alpha_j/40\).

All calculations use integers or `fractions.Fraction`; no floating solver
output is trusted.

## Discovery mechanism

The K5 catalog contains one positive-semidefinite representative for each
of 105,930 attained triangle-count vectors; 101,272 stored representatives
are positive definite.  For a positive-definite scaled K5 Gram matrix \(G\)
and a grid vector \(z\), the bordered K6 matrix
\[
\begin{pmatrix}G&z\\z^{\mathsf T}&4\end{pmatrix}
\]
is PSD of rank five exactly when
\[
z^{\mathsf T}\operatorname{adj}(G)z=4\det G.               \tag{1}
\]

The discovery search sampled 5,000 evenly spaced positive-definite catalog
representatives, tested (1) exactly, and obtained 137,296 distinct K6
triangle-count vectors.  A floating LP selected 51 columns; exact rational
Gaussian elimination then reconstructed positive weights satisfying every
marginal equation.

The sampled catalog and floating LP are discovery history only.  The 51
explicit matrices and rational weights stand independently.

## Consequence for the rank program

The particular 51-orbit K5 distribution does **not** extend to K6, as shown
by `fixed_support_proof.md`.  Nevertheless, the same pair/triple marginal
does extend after changing the K5 marginal.  Therefore:

- failure of one sparse K5 support is not a rank obstruction;
- the rank-at-most-five condition at K6 does not eliminate the centered
  quarter-grid pair/triple witness;
- any successful upper-bound route must impose compatibility beyond this
  direct symmetrized K6 pair/triangle level.

## Reproduction

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/verify_direct_k6_triangle_extension.py
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.centered_quarter_k6_rank.test_direct_k6_triangle_extension -v
```
