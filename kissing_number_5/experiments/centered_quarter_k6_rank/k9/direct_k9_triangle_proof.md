# Exact direct rank-five K9 triangle-marginal extension

## Theorem

The centered quarter-grid pair/triple pseudodistribution has a symmetric
local realization on 51 positive-weight K9 Gram matrices.  Every atom has
quarter-grid off-diagonal entries at most \(1/2\), is positive semidefinite,
and has rank exactly five.  The uniform triangle marginal is exactly
\(\nu/1560\), and the uniform edge marginal is exactly \(\alpha/40\).

This is a local marginal theorem.  It neither supplies a global 41-point
configuration nor proves compatibility between overlapping K9 atoms.

## Exact verification

`direct_k9_triangle_extension.json` stores the 51 edge-color vectors and
exact rational weights.  The standard-library verifier:

1. authenticates the exact pair/triple source and the K8 generation source;
2. rebuilds every scaled integer \(9\times9\) Gram matrix;
3. checks every principal minor of every order;
4. checks every principal determinant of orders six through nine is zero
   and every atom has a positive fifth-order minor, proving rank exactly
   five;
5. reconstructs all 84 triangle types and 36 edge colors;
6. verifies positive weights summing to one and the identities
   \[
   \mathbb E[\#\text{ triangles of type }i]
   =\frac{7\nu_i}{130},\qquad
   \mathbb E[\#\text{ edges of color }j]
   =\frac{9\alpha_j}{10}.
   \]

Dividing by 84 and 36 gives the claimed uniform-face marginals after
symmetrizing each stored atom over all vertex permutations.

## Discovery via exact range equations

Each exact K8 source atom has rank five.  Choose a positive-definite
five-vertex principal block \(B\), leaving three old vertices.  For a
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
These equations are also sufficient because the new column is the Gram
column of a vector in the span of the positive-definite basis block, with
scaled squared norm four.

The discovery search enumerated all \(7^5\) quarter-grid choices for \(w\)
for each of the 51 source atoms.  It retained exact solutions of (1) only
when all three values from (2) were grid values, obtaining 1,926 labeled K9
patterns with 1,811 distinct triangle-count vectors.  Hence it covers every
quarter-grid PSD rank-at-most-five K9 extension of each selected labeled K8
source atom.

A floating LP selected 51 columns.  Exact rational Gaussian elimination
then produced strictly positive weights satisfying every marginal
equation.  The floating LP and discovery catalog are not trusted by the
verifier.

## Numerical and boundary rigor

The grid is represented exactly by the scaled integers
\(-4,-3,-2,-1,0,1,2\).  The boundary inner product \(1/2\) is therefore
included exactly.  PSD, rank, weights, and marginals are checked with
integer or rational arithmetic.  Floating point is used only to select a
candidate basis of columns; neither a solver status nor a numerical
residual is accepted as proof.

## Interpretation

The frozen 51-orbit K8 distribution itself has no K9 extension, as proved in
`fixed_support_proof.md`.  Changing the K8 marginal preserves the same
pair/triple data and gives this exact K9 realization.  Thus neither
support-specific nonextension nor local rank-five K9 consistency removes
the centered quarter-grid pair/triple witness.

Reproduce:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k9/verify_direct_k9_triangle_extension.py
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.centered_quarter_k6_rank.k9.test_direct_k9_triangle_extension -v
```
