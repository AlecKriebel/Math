# Exact direct rank-five K7 triangle-marginal extension

## Theorem

The centered quarter-grid pair/triple pseudodistribution has a symmetric
local realization on 51 positive-weight K7 Gram matrices.  Every atom has
quarter-grid off-diagonal entries at most \(1/2\), is positive semidefinite,
and has rank exactly five.  The uniform triangle marginal is exactly
\(\nu/1560\), and the uniform edge marginal is exactly \(\alpha/40\).

This is a local marginal theorem.  It neither supplies a global 41-point
configuration nor proves compatibility between overlapping K7 atoms.

## Exact verification

`direct_k7_triangle_extension.json` stores the 51 edge-color vectors and
exact rational weights.  The standard-library verifier:

1. authenticates the exact pair/triple source and the K6 generation source;
2. rebuilds every scaled integer \(7\times7\) Gram matrix;
3. checks every principal minor of every order;
4. checks every sixth- and seventh-order principal determinant is zero and
   every atom has a positive fifth-order minor, proving rank exactly five;
5. reconstructs all 35 triangle types and 21 edge colors;
6. verifies positive weights summing to one and the identities
   \[
   \mathbb E[\#\text{ triangles of type }i]
   =\frac{7\nu_i}{312},\qquad
   \mathbb E[\#\text{ edges of color }j]
   =\frac{21\alpha_j}{40}.
   \]

Dividing by 35 and 21 gives the claimed uniform-face marginals.

## Discovery via nullspace and Schur equations

Each exact K6 source atom has rank five.  Choose a positive-definite
five-vertex principal block \(B\), and let \(h\) be the correlations of the
omitted sixth vector with that basis.  For a proposed new-vector
correlation row \(w\) on the basis, rank-five PSD extension requires
\[
w^{\mathsf T}\operatorname{adj}(B)w=4\det B.               \tag{1}
\]
The missing correlation is forced by the nullspace/range equation:
\[
r=\frac{h^{\mathsf T}\operatorname{adj}(B)w}{\det B}.       \tag{2}
\]
The discovery search enumerated the \(7^5\) quarter-grid choices for \(w\),
retained only exact solutions of (1) whose value (2) was also on the grid,
and obtained 2,012 labeled K7 patterns with 1,782 triangle-count vectors.

A floating LP selected 51 columns, after which exact rational Gaussian
elimination produced positive weights satisfying every marginal equation.
The floating LP and search catalog are not trusted by the verifier.

## Interpretation

The frozen 51-orbit K6 distribution itself has no K7 extension, as proved in
`fixed_support_proof.md`.  But changing the K6 marginal preserves the same
pair/triple data and gives this exact K7 realization.  Therefore neither
support-specific nonextension nor the local rank-five K7 condition removes
the centered quarter-grid pair/triple witness.

Reproduce:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k7/verify_direct_k7_triangle_extension.py
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.centered_quarter_k6_rank.k7.test_direct_k7_triangle_extension -v
```
