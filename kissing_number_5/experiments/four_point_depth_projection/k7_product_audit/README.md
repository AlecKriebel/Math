# Rank-five K7 product audit, repair, and K6-lift obstruction

## Results

This folder advances the edge-conditioned robust-depth/common-capacity
hierarchy from K6 to K7.

For five residual vertices sampled from the 39 vertices outside an oriented
base edge,

\[
p_1=\frac5{39},\qquad p_2=\frac{10}{741}.
\]

If \(h,g,i,c\) are the sampled depth count, common-neighbor count,
intersection count, and ordered distinct-pair count, the primitive cleared
K7 row is

\[
\boxed{741c+78i\le78Mh+78rg-10rME.}
\]

The conclusions are:

1. The stored 51-atom direct K7 triangle extension fails 45 of the 560
   direction states in the seven currently proved capacity families. All
   failures occur for \((q,b,M)=(-1/4,1/2,3)\).
2. The exact 74-orbit K6 product distribution has no K7 lift. A complete
   support gluing checks 553,700 colored K7 trials and finds none with all
   seven K6 faces supported.
3. Changing the K6 marginal repairs the obstruction. The exact certificate
   `candidate_k7_product_extension.json` gives a positive 53-atom mixture
   of quarter-grid Gram matrices. Every atom is PSD of rank exactly five,
   its uniform edge and triangle marginals are exactly \(\alpha/40\) and
   \(\nu/1560\), and all 560 currently proved product states pass.

The 53-atom certificate has SHA-256

`1b5e262592e1872cfe9f26b344d82da5066d8332efc5104a34a433d9d5564b00`.

It has 65 equality state keys: 62 from the trivial \(M=0\) family and
three from the \(q=-1/4\) family. These are state keys, not a claim of 65
linearly independent cuts. Its smallest strictly positive
twice-symmetrized K7 slack is

\[
\frac{
621356053751757820879468470110075171035859371
}{
30090524476568270576550820092000000000000000
}>0.
\]

## Exact normalization and the frozen witness

The full derivation is in
[`k7_product_semantics.md`](k7_product_semantics.md). The independent
deletion identity is

\[
\sum_{\text{seven deleted K6 faces}}F_6=2F_7.
\]

It holds because a residual singleton appears in four of the five
base-preserving K6 faces, while an ordered distinct pair appears in three.
The exact semantics verifier checks this first on all 57,344 abstract
set-membership patterns and then on every candidate atom/state pair:

\[
53\cdot560=29{,}680
\]

exact identities.

The stored 51-atom K7 extension has strongest primitive slack

\[
-\frac{
1326789388591936214665268422759803340516316873153
}{
24412017416989651166186925880736000000000000000
}.
\]

This rejects only that frozen local distribution.

## Exact nonextension of the 74-atom K6 distribution

[`k6_support_no_k7_lift.md`](k6_support_no_k7_lift.md) gives the complete
finite proof. The 74 K6 orbits expand to 49,800 labeled K6s. Gluing two
supported faces over their common labeled K5 gives:

- 40,696 common-K5 keys;
- 79,100 compatible ordered face pairs;
- 553,700 trials after all seven colors of the missing edge are tried;
- supported-face histogram \(\{2:550820,3:1560,4:1320\}\);
- zero trials with all seven K6 faces supported.

The exact enumeration/Farkas manifest
`k6_support_no_k7_lift.json` has SHA-256

`f1810d2b00d7456bc360bbba40df1202e9c41b0fad4ce02db76d95548539eaa1`.

The verifier repeats the enumeration using the opposite pair of K7 faces
and obtains the same counts. It also includes a synthetic constant-color
support that has exactly one lift, guarding against an implementation that
would reject every input support.

Because the target K6 distribution has zero mass outside its 74 positive
orbits, a nonnegative K7 lift could not cancel an off-support K6 face.
Thus the support enumeration is sufficient and does not require Gram
positivity or rank.

## The 53-atom replacement

The discovery pool contains 1,782 rank-five K7 rows generated from 51 K6
bases. It is not a complete enumeration. This does not weaken the positive
certificate: both exact verifiers authenticate every selected row and
rebuild its geometry directly.

Two verification paths are provided:

- `verify_candidate_k7_product.py` checks every principal minor and
  evaluates the primitive K7 row by direct membership counts.
- `verify_candidate_k7_via_k6_faces.py` uses an exact
  \(LDL^\mathsf T\)/zero-Schur-complement factorization and evaluates every
  row through the seven deleted K6 faces.

Both reconstruct the exact weights, edge and triangle marginals, and all
560 direction states. The direction-state partition includes every
relevant open projective cell, exact strict boundary, and projective
infinity, modulo color pairs that cannot occur in a supported incident
triangle. Every incidence in every authenticated atom is checked to lie
in that feasible set.

## Reproduction

The exact verifiers require only Python 3.10 or later and the standard
library. They were run with Python 3.14.6. From the repository root:

```sh
PYTHONPATH=. python3 \
  experiments/four_point_depth_projection/k7_product_audit/verify_k7_product_semantics.py

PYTHONPATH=. python3 \
  experiments/four_point_depth_projection/k7_product_audit/verify_k6_support_no_k7_lift.py

PYTHONPATH=. python3 \
  experiments/four_point_depth_projection/k7_product_audit/verify_candidate_k7_product.py

PYTHONPATH=. python3 \
  experiments/four_point_depth_projection/k7_product_audit/verify_candidate_k7_via_k6_faces.py

PYTHONPATH=. python3 -m unittest \
  experiments.four_point_depth_projection.k7_product_audit.test_k7_product_semantics \
  experiments.four_point_depth_projection.k7_product_audit.test_k6_support_no_k7_lift \
  experiments.four_point_depth_projection.k7_product_audit.verify_candidate_k7_test \
  -v
```

The discovery program `search_k7_product_mixture.py` used Python 3.14.6,
NumPy 2.5.1, and SciPy 1.18.0. Solver output is used only to select an
active set; weights are reconstructed as exact fractions and the separate
standard-library verifiers do not trust the solver.

## Scope

“All 560 rows” means every direction state in the seven currently proved
and encoded common-capacity families. It does not quantify over future
capacity theorems.

The 53-atom object is a symmetric local K7 distribution. It is not:

- a global 41-point Gram matrix;
- an overlapping-subset-consistent K7 marginal;
- a seven-point Lasserre or moment-PSD certificate; or
- a resolution of the five-dimensional kissing-number problem.

Thus local rank-exact-five K7 consistency plus the present product rows
still does not separate the centered pair/triple witness.
