# Exact direct rank-five K11 triangle-marginal extension

## Theorem

The centered quarter-grid pair/triple pseudodistribution has a symmetric
local realization on 51 positive-weight K11 Gram matrices.  Every atom has
quarter-grid off-diagonal entries at most \(1/2\), is positive semidefinite,
and has rank exactly five.  The uniform triangle marginal is exactly
\(\nu/1560\), and the uniform edge marginal is exactly \(\alpha/40\).

This is a local marginal theorem.  It neither supplies a global 41-point
configuration nor proves compatibility between overlapping K11 atoms.

## Exact verification

`direct_k11_triangle_extension.json` stores the 51 edge-color vectors and
exact rational weights.  The standard-library verifier:

1. authenticates the exact pair/triple source and the K10 generation source;
2. rebuilds every scaled integer \(11\times11\) Gram matrix;
3. checks all \(2^{11}-1\) nonempty principal minors of every atom;
4. checks every principal determinant of orders six through eleven is zero
   and every atom has a positive fifth-order minor, proving rank exactly
   five;
5. reconstructs all 165 triangle types and 55 edge colors;
6. verifies positive weights summing to one and
   \[
   \mathbb E[\#\text{ triangles of type }i]
   =\frac{11\nu_i}{104},\qquad
   \mathbb E[\#\text{ edges of color }j]
   =\frac{11\alpha_j}{8}.
   \]

Dividing by 165 and 55 gives the claimed uniform-face marginals after
symmetrizing each stored atom over all vertex permutations.

## Exhaustive per-source discovery

Each exact K10 source atom has rank five.  Choose a positive-definite
five-vertex principal block \(B\), leaving five old vertices.  A proposed
new-vector correlation row \(w\) on the basis must satisfy
\[
w^{\mathsf T}\operatorname{adj}(B)w=4\det B.               \tag{1}
\]
For every omitted old vertex with basis-correlation row \(h\), its
correlation with the new vector is forced by
\[
r=\frac{h^{\mathsf T}\operatorname{adj}(B)w}{\det B}.       \tag{2}
\]
The equations are sufficient because they realize the new vector in the
span of the positive-definite basis block with scaled squared norm four.

The search enumerates all \(7^5\) grid rows \(w\) for each of the 51 source
atoms, with no numerical tolerance, and retains a row precisely when (1)
and all five grid-valued instances of (2) hold.  It therefore exhausts all
quarter-grid PSD rank-at-most-five K11 extensions of each selected labeled
K10 source atom.  The result is 1,642 labeled patterns and 1,508 distinct
triangle-count vectors.

`direct_k11_all_extensions.csv` stores all 1,642 results with their source
atom indices.  The standalone catalog verifier independently regenerates
the exact candidate set for every source atom, checks equality with the
stored rows, recomputes every triangle vector, and then verifies that
`direct_k11_from_51.csv` is exactly the first-representative quotient by
triangle-count vector.

A floating LP selected 51 columns.  Exact rational Gaussian elimination
then produced strictly positive weights satisfying every marginal
equation.  The floating LP and catalog are not trusted by the final
verifier.

The exhaustive statement is deliberately scoped: the catalog contains
every extension of the 51 stored labeled K10 atoms, not every possible
quarter-grid K11 atom.

## Numerical and boundary rigor

The grid is represented by exact scaled integers
\(-4,-3,-2,-1,0,1,2\), including the boundary inner product \(1/2\).
PSD, rank, weights, and marginals are checked with integer or rational
arithmetic.  Floating point is used only for choosing a candidate column
basis.

Reproduce:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k11/verify_direct_k11_triangle_extension.py
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k11/verify_extension_catalog.py
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.centered_quarter_k6_rank.k11.test_direct_k11_triangle_extension \
  experiments.centered_quarter_k6_rank.k11.test_extension_catalog -v
```
