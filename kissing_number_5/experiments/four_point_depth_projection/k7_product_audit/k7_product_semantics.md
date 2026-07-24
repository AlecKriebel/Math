# Exact K7 product normalization

Fix an oriented base edge in a hypothetical 41-point code.  There are 39
vertices outside the base.  Let \(H\) be the strict robust-depth tail,
\(\Gamma\) the common high-neighbor set, \(I=|H\cap\Gamma|\), and
\(C=|H||\Gamma|-I\), the number of ordered distinct pairs in
\(H\times\Gamma\).  If robust depth gives \(|H|\ge r\) and the applicable
common-neighbor theorem gives \(|\Gamma|\le M\), then

\[
C+I=|H||\Gamma|
\le M|H|+r|\Gamma|-rM. \tag{1}
\]

A uniformly sampled K7 containing the base keeps five of the 39 residual
vertices.  A specified residual vertex and a specified ordered pair of
distinct residual vertices are retained with probabilities

\[
p_1=\frac{\binom{38}{4}}{\binom{39}{5}}=\frac5{39},
\qquad
p_2=\frac{\binom{37}{3}}{\binom{39}{5}}=\frac{10}{741}.
\]

Writing \(h,g,i,c\) for the sampled counts and \(E\) for the base-edge
event, the expectation of (1), cleared by the smallest convenient integer
factor, is

\[
\boxed{
741c+78i\le 78Mh+78rg-10rM E.
} \tag{2}
\]

Equivalently, since \(c=hg-i\),

\[
78Mh+78rg-10rME-741hg+663i\ge0. \tag{3}
\]

The seven currently proved capacity families specialize (2) as follows.
The variable \(r\) is the exact strict-tail requirement supplied by the
direction state.

| base \(q\) | threshold \(b\) | \(M\) | cleared K7 row |
|---:|---:|---:|---|
| \(-3/4\) | \(1/4\) | 6 | \(741c+78i\le468h+78rg-60rE\) |
| \(-3/4\) | \(1/2\) | 0 | \(741c+78i\le78rg\) |
| \(-1/2\) | \(1/2\) | 1 | \(741c+78i\le78h+78rg-10rE\) |
| \(-1/4\) | \(1/2\) | 3 | \(741c+78i\le234h+78rg-30rE\) |
| \(0\) | \(1/2\) | 6 | \(741c+78i\le468h+78rg-60rE\) |
| \(1/4\) | \(1/2\) | 7 | \(741c+78i\le546h+78rg-70rE\) |
| \(1/2\) | \(1/2\) | 7 | \(741c+78i\le546h+78rg-70rE\) |

## Independent deletion normalization

For a fixed K7 base, sum the K6 product form

\[
39Mh+39rg-4rME-494c-39i
\]

over the five deleted-vertex faces that retain the base.  Every individual
residual membership is retained four times and every ordered distinct pair
is retained three times.  The sum is therefore

\[
156Mh+156rg-20rME-1482c-156i,
\]

which is exactly twice (2)'s slack.  The other two of the seven K6 faces
delete a base endpoint and contribute nothing to that fixed base.
Consequently, after summing over every base edge,

\[
\sum_{\text{seven deleted K6 faces}}F_6=2F_7. \tag{4}
\]

Uniform deletion gives an induced-K6 expected slack equal to \(2/7\) of
the primitive K7 slack.  The verifier checks (4) both for all
\(7\cdot8\cdot2^5\cdot2^5=57{,}344\) abstract set-membership patterns and
for every selected atom/state pair in the exact 53-atom candidate:

\[
53\cdot560=29{,}680
\]

exact identities.

## Audit of the frozen direct K7 extension

The earlier 51-atom direct K7 triangle extension does not satisfy the
product rows.  Exact evaluation of all 560 direction/capacity states finds
45 negative rows, all in

\[
(q,b,M)=(-1/4,1/2,3).
\]

The strongest primitive K7 slack is

\[
-\frac{
1326789388591936214665268422759803340516316873153
}{
24412017416989651166186925880736000000000000000
}.
\]

It occurs at required depth \(r=5\).  One exact rational direction
representing its open direction cell is

\[
(\lambda,\mu)=
\left(1,\frac{2726079748655}{4665300484096}\right).
\]

This rejects only the frozen 51-atom distribution.  It is not a universal
K7 obstruction: the separate exact 53-atom candidate passes the same 560
rows.

Reproduce with:

```sh
PYTHONPATH=. /usr/bin/python3 \
  experiments/four_point_depth_projection/k7_product_audit/verify_k7_product_semantics.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  experiments.four_point_depth_projection.k7_product_audit.test_k7_product_semantics \
  -v
```
