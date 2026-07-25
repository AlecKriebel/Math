# Exact direct rank-five K8 triangle-marginal extension

## Theorem

The centered quarter-grid pair/triple pseudodistribution has a symmetric
local realization on 51 positive-weight K8 Gram matrices.  Every atom has
quarter-grid off-diagonal entries at most \(1/2\), is positive semidefinite,
and has rank exactly five.  The uniform triangle marginal is exactly
\(\nu/1560\), and the uniform edge marginal is exactly \(\alpha/40\).

This is a local marginal theorem.  It neither supplies a global 41-point
configuration nor proves compatibility between overlapping K8 atoms.

## Exact verification

`direct_k8_triangle_extension.json` stores the 51 edge-color vectors and
exact rational weights.  The standard-library verifier:

1. authenticates the exact pair/triple source and the K7 generation source;
2. rebuilds every scaled integer \(8\times8\) Gram matrix;
3. checks every principal minor of every order;
4. checks every principal determinant of orders six through eight is zero
   and every atom has a positive fifth-order minor, proving rank exactly
   five;
5. reconstructs all 56 triangle types and 28 edge colors;
6. verifies positive weights summing to one and the identities
   \[
   \mathbb E[\#\text{ triangles of type }i]
   =\frac{7\nu_i}{195},\qquad
   \mathbb E[\#\text{ edges of color }j]
   =\frac{7\alpha_j}{10}.
   \]

Dividing by 56 and 28 gives the claimed uniform-face marginals after
symmetrizing each stored atom over all vertex permutations.

## Discovery via exact range equations

Each exact K7 source atom has rank five.  Choose a positive-definite
five-vertex principal block \(B\), leaving two old vertices.  For a proposed
new-vector correlation row \(w\) on the basis, a rank-five PSD extension
requires
\[
w^{\mathsf T}\operatorname{adj}(B)w=4\det B.               \tag{1}
\]
For either omitted old vertex with basis-correlation row \(h\), its
correlation with the new vector is forced by the range equation
\[
r=\frac{h^{\mathsf T}\operatorname{adj}(B)w}{\det B}.       \tag{2}
\]
These equations are also sufficient: the new column lies in the span of
the positive-definite basis block with scaled squared norm four.

The discovery search enumerated all \(7^5\) quarter-grid choices for \(w\)
for each of the 51 source atoms, retained only exact solutions of (1) whose
two values from (2) were grid values, and obtained 2,064 labeled K8
patterns with 1,908 distinct triangle-count vectors.  Thus it covers every
quarter-grid PSD rank-at-most-five K8 extension of each selected labeled K7
source atom.

A floating LP selected 51 columns.  Exact rational Gaussian elimination
then produced strictly positive weights satisfying every marginal
equation.  The floating LP and discovery catalog are not trusted by the
verifier.

## Numerical and boundary rigor

The seven off-diagonal grid values are stored as exact rationals and scaled
to the integers \(-4,-3,-2,-1,0,1,2\).  Thus the kissing constraint includes
the boundary value \(1/2\) exactly; no strict inequality or tolerance is
used.  PSD and rank are decided from integer principal determinants, and
all marginal identities use rational arithmetic.  Floating point is used
only to choose a candidate 51-column basis.  A solver status, residual, or
near-PSD matrix is never accepted by the verifier.

## Interpretation

The frozen 51-orbit K7 distribution itself has no K8 extension, as proved in
`fixed_support_proof.md`.  But changing the K7 marginal preserves the same
pair/triple data and gives this exact K8 realization.  Therefore neither
support-specific nonextension nor the local rank-five K8 condition removes
the centered quarter-grid pair/triple witness.

Reproduce:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k8/verify_direct_k8_triangle_extension.py
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.centered_quarter_k6_rank.k8.test_direct_k8_triangle_extension -v
```
