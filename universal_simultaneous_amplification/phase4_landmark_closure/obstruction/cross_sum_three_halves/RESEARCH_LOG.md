# Research log: universal cross-sum at fitness 3/2

## 2026-08-02 06:40 PDT

Started an independent attack on

\[
\rho_{\rm Bd}(G,3/2)+\rho_{\rm dB}(G,3/2)
\le
\rho_{\rm Bd}(K_n,3/2)+\rho_{\rm dB}(K_n,3/2).
\]

The weighted-triangle case is already exactly proved elsewhere in the
phase-4 package.  The immediate tasks are (i) aggressive cancellation-safe
search on orders 4--7, including boundary supports and separated rational
weight scales, and (ii) discovery of a universal exact certificate or a
rational counterexample.  Numerical output is discovery evidence only.

## 2026-08-02 07:15 PDT

The unweighted atlas evaluation is complete through order seven: all 995
connected isomorphism classes, including 853 of order seven.  Neither the
cross-sum nor product comparison was violated; complete graphs attain the
maximum to floating precision.  Dense, sparse, regular-polytope, and
multistart log-weight searches likewise found no verified counterexample.
An apparent order-four violation at edge ratio about `10^25` was a double
precision absorbing-solve artifact.  Cancellation-safe evaluation at
resolvable scales converges to a strictly negative gap.

The common pointwise correction architecture was tested as an exact finite
linear feasibility problem and is false even on weighted paths.  Its
baseline-weighted (product-tangent) version is also false.  This does not
refute either fixation inequality.

## 2026-08-02 07:35 PDT

Pivoted to the weaker but decisive product conjecture
`rho_Bd rho_dB <= rho_Bd(K_n) rho_dB(K_n)`.  Proved it exactly for every
positive weighted triangle using a new 24-atom sum-of-squared-differences
certificate.  Derived the complete dB harmonic

`[n-(n+k/2)(2/3)^k]/[n(1-(2/3)^(n-1))]`

and an exact arbitrary-graph defect decomposition.  The temperature term
cancels the Bd harmonic defect; the only signed remainder is the deviation
of the row cut from `k(n-k)/(n-1)`, accompanied by two explicit nonnegative
dispersion losses.  The exact verifier passes.

Exact implicit differentiation of the complete labelled chains proves that
the log-product has zero first variation and negative Hessian on both
irreducible edge modes for `n=4,5,6,7`.  This is local only.  Numerical radial
monotonicity is false far from the complete graph, so a star-concavity proof
cannot be used.

The similarly tempting symmetric balancing step
`w_ij -> w_ij/sqrt(d_i d_j)` is locally favorable and increased the product
on all moderate tests, but it is not globally monotone.  A connected sparse
order-six separated-scale instance decreased the product from about
`0.0542035` to `0.0522807` after one step.  Both values are far below the
complete baseline, so this falsifies only the balancing proof route, not the
product conjecture.
