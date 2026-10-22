# Proof 44  Two rigorously certified rational coefficient boxes

Included dependencies: [Dominant endpoint entropy and nearby power comparisons](17_dominant_endpoint_entropy.md); [Full prescribed coefficient boxes near exponent two](18_near_two_boxes.md); [Validated one phase entropy quadrature](42_validated_entropy_quadrature.md); [Validated circular Green quadrature](43_validated_green_quadrature.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

The real five-frequency polynomial is

`c+a_0 Z_0+b_0/Z_0+a_1 Z_1+b_1/Z_1`,

where the two phases are independent uniform circle variables. For each coefficient set below, all three nontrivial pair-product sign choices `(-1,+1)`, `(+1,-1)`, and `(-1,-1)` were enclosed separately by the global entropy-quadrature method. The fourth sign choice is equality. Haar phase changes and an overall sign reduce every real coefficient-box vertex to one of these four choices.

## Exact results

1. `c=9/10`, `(a_0,b_0)=(1,2/5)`, `(a_1,b_1)=(4/5,3/10)`.

   The least certified normalized entropy gap among the three patterns exceeds `0.01542318`. The full real coefficient-box majorant therefore holds for `2<p<=2.1079`.

2. `c=2/5`, `(a_0,b_0)=(1,7/10)`, `(a_1,b_1)=(7/8,1/5)`.

   The least certified normalized entropy gap among the three patterns exceeds `0.00742228`. The full real coefficient-box majorant therefore holds for `2<p<=2.0519`.

Every endpoint in these examples is nonzero and genuinely unequal to its partner. Neither example satisfies the inherited simple dominance conditions used for these certificates. The specific certified intervals remain coefficient-box results, not support classifications.

## Why the power and full-box conclusions follow

Normalize by `R=c+sum_j(a_j+b_j)`. Every sign vertex has support at most one after normalization and the same second moment. For each vertex define its power gap `D(p)`. The accepted uniform Taylor estimate is

`D(p)>=(p-2)*delta-(p-2)^2/e^2`,

where `delta` is that vertex's normalized entropy gap. The exact rational lower bound recorded for the minimum delta is strictly positive. Since `e^2>7`, this estimate is strictly positive at every nontrivial vertex whenever `0<p-2<=7*delta_min`. The displayed simpler rational interval endpoints are strictly below these exact rational bounds. For example, the positive exponential series at 2 gives `e^2>1+2+2+4/3+2/3=7`.

Convexity of the expected p-th power as a function of the full real coefficient vector, for `p>=1`, extends the common upper bound at every sign vertex to the full prescribed coefficient box. This convexity step is used only for the power test, not for the nonconvex entropy test. No assertion is made at arbitrary noise radii.

## Reproduction

Run `python certificates/certify_rational_boxes.py`.

The complete exact coefficient records, rational intervals, all three sign patterns, and safe rational power endpoints are in [rational_box_certificates.json](../certificates/rational_box_certificates.json). Each individual quadrature uses 256 angular midpoint nodes, 45-decimal real interval arithmetic, the accepted exact one-phase formula, and the proved global analytic error. The trusted numerical dependency and zero/root-transition handling are detailed in [Validated one phase entropy quadrature](42_validated_entropy_quadrature.md).
