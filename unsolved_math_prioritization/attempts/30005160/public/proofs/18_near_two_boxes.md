# Proof 18  Full prescribed coefficient boxes near exponent two

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Dominant endpoint entropy and nearby power comparisons](17_dominant_endpoint_entropy.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## Input and hypotheses

Use the notation and support bound `R=c+sum_j(a_j+b_j)+rho` of [Dominant endpoint entropy and nearby power comparisons](17_dominant_endpoint_entropy.md), SHA-256 `f27f7c63d5c0c8e69ecdbafc440b9051fb0c61ac2cbbad1b813a0602f315bb30`. Suppose

`a_0>=b_0+c+sum_(j>=1)(a_j+b_j)+rho`,

with `c>0`, `a_0>0`, `b_0>0`, and independent circular noise `Y` satisfying `|Y|<=rho`. Discard a pair with both coefficients zero. A pair with only one nonzero coefficient has no effective pair-product sign and can be retained as an independent circular summand.

Let `J={j>=1:a_j b_j>0}`. Define

`eta=(b_0/a_0)*min(c^2, 2 min_(j in J) a_j b_j)` if `J` is nonempty,

and `eta=(b_0/a_0)c^2` otherwise. Put `delta_min=eta/R^2>0`.

## Statement

For every

`2<p<min(3,2+e^2 delta_min)`, (1)

the all-positive centered-cross polynomial is a full real coefficient-box majorant at these prescribed magnitudes, even after adding the same independent noise `Y`: whenever

`|x_c|<=c`, `|x_j|<=a_j`, `|y_j|<=b_j`,

one has

`E|x_c+sum_j(x_j Z_j+y_j/Z_j)+Y|^p`

`<=E|c+sum_j(a_j Z_j+b_j/Z_j)+Y|^p`. (2)

The comparison at sign vertices with a genuinely changed active pair-product sign is strict throughout (1). No strictness is asserted for all interior coefficient choices. A non-strict comparison also holds at `p=2` and at the quadratic bound's endpoint if it is at most 3.

## Proof

At sign vertices, an overall sign followed by independent phase shifts `Z_j -> -Z_j` as needed makes the center and first endpoint in every nonzero pair positive. The remaining sign `s_j` is the product of that pair's original signs. An overall sign sends `Y` to `-Y`, which has the same law by circular symmetry. These Haar-preserving changes preserve the full expectation and independence. One-sided pairs have no effective sign.

For `s_0=+1`, every nontrivial active pair-product pattern must flip some `j in J`. The exact entropy gap from the dominant endpoint proof is

`(2b_0/a_0) sum_(j in J:s_j=-1) a_j b_j >= (2b_0/a_0) min_(j in J) a_j b_j`.

For `s_0=-1`, its entropy gap is

`(b_0/a_0)[c^2+2 sum_(j in J:s_j=+1) a_j b_j] >= (b_0/a_0)c^2`.

These lower bounds are attained by the respective sign choices, so `eta` is exactly the minimum positive gap over distinct active sign patterns. If `J` is empty, only the second case occurs. All other sign patterns are distributionally identical to the positive one. Equality of the second moments at sign vertices and the normalized Taylor estimate from the dominant endpoint proof establish comparison uniformly over every sign vertex on (1).

Finally, for fixed `p>=1`, the left side of (2) is a convex function of the entire real coefficient vector: the map from coefficients to its complex value is affine for each sample, `|z|^p` is convex on the plane, and integration preserves convexity. Every point of the compact coefficient box is a convex combination of its sign vertices. The upper bound at every vertex therefore implies (2). The noise variable is unchanged in this convexity step.

## Rational example

For `c=1`, `(a_0,b_0)=(4,1)`, `(a_1,b_1)=(1,1/2)`, and `Y=0`, one has `eta=1/4`, `R=15/2`, and `delta_min=1/225`. Thus the full real coefficient-box majorant holds for

`2<p<2+e^2/225`, approximately `2<p<2.032840`.

Uniformly for independent circular noise with `|Y|<=1/2`, take `R=8`; then `delta_min=1/256` and the full box comparison holds for `2<p<2+e^2/256`, approximately `2<p<2.028864`.

This is a prescribed-magnitude neighborhood of 2 whose width depends on the smallest nonzero active pair product. It is not a uniform exponent interval over all admissible magnitudes and does not assert the complete Green cone.
