# Exact fixed-support K6 obstruction

## Statement

Let \(\mu_5\) be the particular symmetric probability distribution on 51
quarter-grid, Gram-PSD K5 orbits stored in
`certificates/centered_quarter_k5_extension.json` with SHA-256
```
133e8b502653b3bb1e1c4c3eb6c0452705020f65128959dc9d0cb34a8c0645ef.
```
There is no symmetric probability distribution \(\mu_6\) on quarter-grid
\(6\times6\) Gram matrices such that:

1. every matrix is positive semidefinite and has rank at most five; and
2. the marginal of a uniformly chosen five-vertex face is exactly \(\mu_5\).

This theorem is finite and exact, but its scope is narrow.  It does not
exclude a different K5 distribution having the same pair/triple marginals,
a direct K6 triangle-marginal distribution, or a 41-point spherical code.

## Complete finite reduction

The 51 K5 representatives expand under \(S_5\) to 2,940 distinct labeled
matrices.  Any K6 atom with K5 marginal supported on these 51 orbits must
have **every** one of its six K5 faces in this labeled support: a face
outside the support would contribute a strictly positive mass outside the
claimed marginal and cannot be canceled by nonnegative weights.

To enumerate all such K6 matrices, take its faces obtained by deleting
vertices 5 and 4.  They overlap in the labeled K4 on vertices
\(\{0,1,2,3\}\).  Conversely, two supported labeled K5 faces with the same
K4 restriction determine every K6 edge except \(45\); trying its seven
quarter-grid colors covers all possibilities.

There are 1,938 K4 keys and 6,942 compatible ordered pairs of supported K5
faces.  Thus the complete search has only
\[
7\cdot6942=48\,594
\]
color trials.  Exact checking of the other four faces leaves 240 labeled
K6 matrices.

Every one of the 240 matrices has exact determinant zero.  Since all proper
principal submatrices occur inside a Gram-PSD K5 face, all proper principal
minors are nonnegative; with the zero full determinant, every principal
minor is nonnegative.  Hence all 240 matrices are PSD and have rank at most
five.  Canonicalization under \(S_6\) gives four orbits, each of size 60.

Their K5 face-count vectors are
\[
6e_0,\qquad6e_{21},\qquad6e_{39},\qquad6e_{46}.             \tag{1}
\]

## Exact Farkas certificate

Let \(A\) be the \(51\times4\) matrix whose columns are (1), and let
\[
b_i=6w_i
\]
where \(w_i\) is the exact weight of K5 orbit \(i\) in \(\mu_5\).  A K6
extension would give \(z\geq0\) satisfying \(Az=b\).

The row for orbit 1 vanishes in every column of \(A\), whereas
\[
w_1=\frac{193319639973}{2080000000000}>0.
\]
With \(y=-e_1\),
\[
A^{\mathsf T}y=0\geq0,\qquad
b^{\mathsf T}y=-6w_1
=-\frac{579958919919}{1040000000000}<0.                   \tag{2}
\]
Equation (2) is an exact Farkas contradiction.

## Independent verification

`enumerate_k6.cpp` performs a 49,412,580-row sixth-vertex search.  The
standard-library verifier `verify_fixed_support_obstruction.py` instead
uses the 48,594-case K4 gluing reduction, a Leibniz determinant independent
of the discovery code's Bareiss determinant, and independently recomputes
all principal minors and group orbits.

Run:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/verify_fixed_support_obstruction.py
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.centered_quarter_k6_rank.test_fixed_support_obstruction -v
```

The verifier authenticates both source certificate hashes, rebuilds the
entire enumeration, and checks the rational Farkas pairing.  No floating
arithmetic is used.
