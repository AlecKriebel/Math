# Rank-five K6 product audit, repair, and K5-lift obstruction

## Result

The exact direct rank-five K6 triangle-marginal extension does **not**
survive the pair-conditioned robust-depth/common-capacity product
inequalities.

Choose one of its 51 K6 atoms with the stored exact weight, apply a uniform
permutation in \(S_6\), and delete a uniformly chosen vertex.  The resulting
symmetric K5 marginal has:

- 306 weighted deleted faces before merging;
- 266 positive unlabeled K5 orbits after exact canonicalization;
- edge marginal exactly \(\alpha/4\);
- triangle marginal exactly \(\nu/156\).

Of the 560 distinct continuum direction/capacity rows, this induced marginal
violates exactly 41.  Every violation lies in the family

\[
(q,b,M)=(-1/4,1/2,3).
\]

The strongest violation is the elementary strict direction
\(-\!(y+z)\), not an algebraic boundary state.  With the convention that
right side minus left side must be nonnegative, its exact slack is

\[
-\frac{
34774569534004858111024638332474125643044200329
}{
2136111269073896339143576173079200000000000000
}<0.
\]

Equivalently, the left side exceeds the right side by the positive rational
obtained by removing the minus sign.

The direct-K6 form is the sum over the six deleted faces, before multiplying
by the face probability \(1/6\).  Its corresponding slack is therefore six
times the displayed induced-K5 slack:

\[
-\frac{
34774569534004858111024638332474125643044200329
}{
356018544845649389857262695513200000000000000
}.
\]

This rejects this particular symmetrized K6 distribution.  It does not rule
out a different rank-five K6 extension with the same pair/triple marginals,
and it is not an upper bound for the kissing-number problem by itself.

That distinction is decisive.  Reoptimization over the authenticated
137,296-column discovery pool produced
`productpool_extension.json`, an exact positive 74-atom mixture of
rank-exact-five Gram-PSD `K6` atoms with the same pair/triangle marginals.
It passes all 560 direction states across the seven currently proved and
encoded common-capacity families. This does not quantify over possible
future capacity theorems. Its SHA-256 is

`def805e0c73fb5a5306f230ad21866a5b0fcab1a3708f6f7daaa3b175dc54991`.

The formerly violating \((q,b,M)=(-1/4,1/2,3)\) negative-sum row is now
an exact equality. There are 113 equality state keys in total, of which
62 come from the trivial \(M=0\) family; this is not a claim that all 113
are linearly distinct cuts. The smallest strictly positive
twice-symmetrized slack is

\[
\frac{4741606889923}{12500000000000}>0.
\]

This is the direct-K6 normalization.  The induced-K5 normalization divides
it by six, giving \(4741606889923/75000000000000\).

Thus the product rows reject the original sparse distribution but do not
obstruct the symmetric local rank-five `K6` marginal problem.

## Normalization

Fix an oriented base edge in a hypothetical 41-point code.  Among its
\(39\) residual vertices, let

\[
H=\#\{\hbox{strict-tail vertices}\},\qquad
\Gamma=\#\{\hbox{common high neighbors}\},
\]

let \(I\) be the intersection count, and put
\(C=H\Gamma-I\), the number of ordered distinct tail/common pairs.  Robust
depth and the common-pair cap give

\[
C+I=H\Gamma\le MH+r\Gamma-rM.                 \tag{1}
\]

For a uniform K5 containing the base, three of the 39 residual vertices are
retained.  Thus

\[
\Pr(x\hbox{ retained})=\frac1{13},\qquad
\Pr(x,w\hbox{ retained})=\frac1{247}
\]

for distinct ordered \(x,w\).  If \(h,g,i,c\) denote the sampled counts,
(1) becomes

\[
247c+13i\le13Mh+13rg-rM.                     \tag{2}
\]

For a uniform K6 containing the base, four residual vertices are retained,
so

\[
\Pr(x\hbox{ retained})=\frac4{39},\qquad
\Pr(x,w\hbox{ retained})=\frac2{247}.
\]

The corresponding cleared row is

\[
494c+39i\le39Mh+39rg-4rM.                    \tag{3}
\]

There are six K5 faces of a K6 atom.  For every atom and every product
state, the verifier checks the exact integer identity

\[
\sum_{\text{six deleted faces}}\!
\bigl(\text{K5 form (2)}\bigr)
=\text{K6 form (3)}.
\]

It checks \(51\cdot560=28{,}560\) such identities.  Since a deleted face
has probability \(1/6\), the induced K5 slack is the weighted K6 form
divided by six.  This supplies an independent normalization path in
addition to explicitly constructing the induced marginal.

## The simple decisive row

Take a base with \(\langle y,z\rangle=-1/4\), common-neighbor threshold
\(b=1/2\), and capacity \(M=3\).  For the strict direction
\(-\!(y+z)\), neither base endpoint lies in the positive tail, so \(r=7\).
The tail and common-neighbor sets are disjoint, hence \(I=i=0\).  Row (2)
reduces to

\[
247c\le39h+91g-21E,                          \tag{4}
\]

where \(E\) is the oriented base-edge count.

For the induced K5 marginal, the exact expected oriented totals are

\[
\begin{aligned}
E&=\frac{125532493886399}{112500000000000},\\
h&=\frac{974897098487491}{650000000000000},\\
g&=\frac{656862349021}{2600000000000},\\
i&=0,\\
c&=\frac{
31755710847659641038258857541418980463254597349
}{
105523896692250479153692662950112480000000000000
}.
\end{aligned}
\]

Consequently the two sides of (4) are

\[
\begin{aligned}
\mathrm{left}
&=\frac{
31755710847659641038258857541418980463254597349
}{
427222253814779267828715234615840000000000000
},\\
\mathrm{right}
&=\frac{8707691389928497}{150000000000000},
\end{aligned}
\]

and right minus left is exactly the negative rational displayed above.

## What the verifier authenticates

`verify_induced_k5_product.py` uses only integers and
`fractions.Fraction`.  It independently:

1. authenticates the centered pair/triple source, the K6 certificate, and
   the exact direction-partition implementation by SHA-256;
2. authenticates the 137,296-column discovery catalog and its numerical
   report, while explicitly treating both as discovery provenance only;
3. reconstructs every scaled K6 Gram matrix, checks all principal minors,
   and verifies rank exactly five;
4. reconstructs exact edge and triangle marginals;
5. deletes every vertex and canonicalizes the 306 K5 faces;
6. verifies the induced K5 edge and triangle marginals;
7. regenerates all 560 exact continuum states;
8. evaluates every product row with a common integer denominator;
9. checks the K5-deletion and direct-K6 forms agree atom by atom.

The floating LP weights in the discovery report are never used.

## Reproduction

From the repository root:

```sh
PYTHONPATH=. /usr/bin/python3 \
  experiments/four_point_depth_projection/k6_product_audit/verify_induced_k5_product.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  experiments.four_point_depth_projection.k6_product_audit.test_induced_k5_product \
  -v

PYTHONPATH=. /usr/bin/python3 \
  experiments/four_point_depth_projection/k6_product_audit/productpool_verify.py

PYTHONPATH=. /usr/bin/python3 \
  experiments/four_point_depth_projection/k6_product_audit/verify_productpool_extension_independent.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  experiments.four_point_depth_projection.k6_product_audit.test_verify_productpool_extension_independent \
  -v

PYTHONPATH=. /usr/bin/python3 \
  experiments/four_point_depth_projection/k6_product_audit/verify_productpool_via_deleted_k5.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  experiments.four_point_depth_projection.k6_product_audit.test_productpool_via_deleted_k5 \
  -v

PYTHONPATH=. /usr/bin/python3 \
  experiments/four_point_depth_projection/k6_product_audit/verify_k5_support_no_k6_lift.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  experiments.four_point_depth_projection.k6_product_audit.test_k5_support_no_k6_lift \
  -v
```

The verifier prints all 41 exact violated row keys and residuals.  The test
suite also checks that a weight-tampered K6 certificate is rejected.

## Scope

The K6 certificate prescribes only a symmetric local distribution and does
not impose overlapping-subset consistency.  This audit proves that even
that specific distribution cannot be the uniform K6 marginal of a
41-point code satisfying the already-proved depth and capacity facts.

The rejection does **not** extend to every K6 distribution with the
centered pair/triple marginal.  The 74-atom replacement answers that local
feasibility question affirmatively over the available pool.  The pool is
incomplete, but that does not weaken a positive certificate: every selected
atom is checked directly.  The replacement is still not a global 41-point
Gram matrix and does not provide overlapping-subset consistency or a
six-point Lasserre moment-PSD certificate.

## The earlier 64-atom K5 witness does not lift

The exact 64-atom K5 product extension is not the K5 marginal of any
quarter-grid K6 distribution. This is stronger than failure over the
available K6 pool: a complete support join expands its 64 orbit types to
6,270 labeled K5s and tests all 104,118 possible joins of two supported
faces over a common labeled K4, including all seven choices for the final
edge. No colored K6 has all six faces in that support.

The proof is in
[`k5_support_no_k6_lift.md`](k5_support_no_k6_lift.md), with the exact
checker in `verify_k5_support_no_k6_lift.py`. There is no conflict with the
74-atom K6 replacement: its induced K5 marginal is a different
distribution.
