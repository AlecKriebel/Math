# Exact nonextension of the 74-orbit K6 product distribution

The exact symmetric 74-orbit K6 distribution in
`../k6_product_audit/productpool_extension.json` is not the uniform
K6-face marginal of any nonnegative quarter-grid K7 distribution.  This is
a support-specific result; it does not obstruct another K6 distribution
having the same edge, triangle, and product moments.

## Why support alone suffices

Every one of the 74 K6 orbit weights is strictly positive, and the target
K6 marginal is zero outside those orbits.  A nonnegative K7 distribution
cannot cancel off-support face mass.  Therefore every K6 face of every
positive K7 atom would have to lie in the 74-orbit support.

Expand the 74 representatives under all \(6!\) vertex permutations.  They
give 49,800 distinct labeled K6 colorings, with orbit-size histogram

\[
1\{120\}+8\{360\}+65\{720\}.
\]

Fix the K7 faces deleting vertices 6 and 5.  They overlap on the labeled
K5 with vertices \(0,\ldots,4\).  Grouping the labeled supported K6s by
this common K5 gives 40,696 keys.  The group-size histogram is

\[
\begin{array}{c|rrrrrrr}
\text{group size}&1&2&3&4&6&8&60\\
\hline
\text{number of keys}&33940&5470&600&540&130&15&1.
\end{array}
\]

Thus there are exactly

\[
\sum_{\text{keys}} |G_{\text{key}}|^2=79{,}100
\]

ordered compatible pairs of the two fixed K6 faces.  Such a pair determines
all 21 K7 edges except edge \(56\).  Trying all seven quarter-grid colors
on that edge gives exactly

\[
7\cdot79{,}100=553{,}700
\]

labeled K7 trials.  This is exhaustive: any K7 whose seven faces were
supported would occur exactly once, through its two fixed faces and its
color on edge \(56\).

The exact supported-face histogram over the trials is

\[
\{2:550820,\;3:1560,\;4:1320\}.
\]

In particular, no trial has all seven faces supported.  Repeating the
entire construction with the opposite pair of faces, deleting vertices 0
and 1, produces exactly the same counts and again no lift.

## Empty-column Farkas certificate

Let a prospective K7 orbit column record the numbers of its seven K6 faces
in each of the 74 support orbits.  The exhaustive enumeration proves that
there are no allowable columns.  The required target is
\(b_i=7w_i\).  Taking \(y=-e_0\), the column inequalities are vacuous and

\[
b^\mathsf{T}y
=-7w_0
=-\frac{
462937922730878632368908435955017028641430479
}{
6373923427690822467663452332372800000000000000
}<0.
\]

This is an exact infeasibility certificate.

## Redundant incomplete-pool scan

The existing 1,782-row rank-five K7 discovery pool has supported-K6-face
histogram

\[
\{0:1607,\;1:168,\;2:7\}.
\]

No pool row is a lift, but this scan is only a cross-check.  Completeness
comes from the 553,700 overlap-gluing trials above, which enumerate all
seven-colored K7s compatible with the target support even before Gram
positivity or rank is imposed.

## Scope

This proves only that the particular 74-orbit K6 mixture has no K7 lift.
It does not rule out:

- a different K6 mixture with the same pair and triangle marginals;
- a K7 mixture satisfying the same 560 product inequalities;
- a global 41-point code.

Indeed, the adjacent exact 53-atom K7 candidate demonstrates the first two
possibilities locally.  It cannot have the exact 74-orbit K6 face marginal
excluded here.

Reproduce with:

```sh
PYTHONPATH=. /usr/bin/python3 \
  experiments/four_point_depth_projection/k7_product_audit/verify_k6_support_no_k7_lift.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  experiments.four_point_depth_projection.k7_product_audit.test_k6_support_no_k7_lift \
  -v
```
