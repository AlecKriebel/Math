# Exact direct rank-five K10 triangle-marginal extension

## Theorem

The centered quarter-grid pair/triple pseudodistribution has a symmetric
local realization on 51 positive-weight K10 Gram matrices.  Every atom has
quarter-grid off-diagonal entries at most \(1/2\), is positive semidefinite,
and has rank exactly five.  The uniform triangle marginal is exactly
\(\nu/1560\), and the uniform edge marginal is exactly \(\alpha/40\).

This is a local marginal theorem.  It neither supplies a global 41-point
configuration nor proves compatibility between overlapping K10 atoms.

## Exact verification

`direct_k10_triangle_extension.json` stores the 51 edge-color vectors and
exact rational weights.  The standard-library verifier:

1. authenticates the exact pair/triple source and the K9 generation source;
2. rebuilds every scaled integer \(10\times10\) Gram matrix;
3. checks every principal minor of every order;
4. checks every principal determinant of orders six through ten is zero and
   every atom has a positive fifth-order minor, proving rank exactly five;
5. reconstructs all 120 triangle types and 45 edge colors;
6. verifies positive weights summing to one and
   \[
   \mathbb E[\#\text{ triangles of type }i]
   =\frac{\nu_i}{13},\qquad
   \mathbb E[\#\text{ edges of color }j]
   =\frac{9\alpha_j}{8}.
   \]

Dividing by 120 and 45 gives the claimed uniform-face marginals after
symmetrizing each stored atom over all vertex permutations.

## Discovery via exact range equations

Each exact K9 source atom has rank five.  Choose a positive-definite
five-vertex principal block \(B\), leaving four old vertices.  For a
proposed new-vector correlation row \(w\) on the basis, a rank-five PSD
extension requires
\[
w^{\mathsf T}\operatorname{adj}(B)w=4\det B.               \tag{1}
\]
For any omitted old vertex with basis-correlation row \(h\), its correlation
with the new vector is forced by
\[
r=\frac{h^{\mathsf T}\operatorname{adj}(B)w}{\det B}.       \tag{2}
\]
These equations are sufficient because the new column represents a vector
in the span of the positive-definite basis block with scaled squared norm
four.

Enumerating all \(7^5\) grid choices for \(w\) for each of the 51 source
atoms, and requiring all four forced values to lie on the grid, gives 1,783
labeled K10 patterns and 1,650 distinct triangle-count vectors.  This
covers every quarter-grid PSD rank-at-most-five K10 extension of each
selected labeled K9 atom.

A floating LP selected 51 columns.  Exact rational Gaussian elimination
then produced strictly positive weights satisfying every marginal
equation.  The floating LP and discovery catalog are not trusted by the
verifier.

## Numerical and boundary rigor

The grid is represented by the exact scaled integers
\(-4,-3,-2,-1,0,1,2\), including the boundary inner product \(1/2\).
PSD, rank, weights, and marginals are checked with integer or rational
arithmetic.  Floating point is used only for choosing a candidate column
basis and supplies no trusted proof step.

## Frozen-support branch

The preceding levels exhaustively disproved extension of each frozen
distribution.  At K10, the exact size audit in `frozen_support_note.md`
finds 16,057,440 labeled K9 support matrices and a lower bound of
112,402,080 missing-edge color trials.  The full frozen-support enumeration
was deliberately skipped under the task's growth-control instruction.  No
claim about that frozen K9 distribution's extendibility is made.

Reproduce:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k10/verify_direct_k10_triangle_extension.py
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.centered_quarter_k6_rank.k10.test_direct_k10_triangle_extension -v
```
