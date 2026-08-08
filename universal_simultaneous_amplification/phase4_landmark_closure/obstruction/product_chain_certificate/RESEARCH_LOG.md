# Research log: product-chain certificate at fitness `r=3/2`

## 2026-08-02 10:20 PDT

Started an independent attack on the finite universal conjecture

\[
\rho_{\rm Bd}(G,3/2)\rho_{\rm dB}(G,3/2)
\le
\rho_{\rm Bd}(K_n,3/2)\rho_{\rm dB}(K_n,3/2).
\]

The exact target quantifies over every finite connected undirected weighted
graph.  The intended routes are the independent product of the two exact
branching--coalescing duals, variational or matrix-tree representations, and
two-chain Lyapunov functions.  Previously falsified statewise
common-correction, radial-monotonicity, per-level, and simple batching
certificates are excluded from this attack.  Every proposed certificate will
be tested adversarially on exact rational small graphs before promotion.

Discovery status: **OPEN**.  Completion estimate for this assigned route:
`5%`.

## 2026-08-02 11:05 PDT

Formulated the independent product-dual generator
`Q=L_Bd tensor I + I tensor D_dB`.  The normalized arithmetic target

\[
 |A|/m_{\rm Bd}^K+|B|/m_{\rm dB}^K-2
\]

would imply the fixation-product conjecture by AM--GM.  Tested pointwise
Poisson corrections based on bilinear overlaps; they were already
infeasible on weighted three-paths.  This was treated only as a discovery
signal pending an exact Farkas witness.

Separately tested stationary rank-convolution and coverage-transform
strengthenings.  Exact order-four candidates showed that both global
orderings fail away from the fixation endpoint, while the endpoint product
retains the conjectured sign.

Completion estimate for the assigned route: `45%`.

## 2026-08-02 11:35 PDT

Completed a five-atom exact Farkas certificate on the **unweighted**
three-path.  Its rational pseudo-law annihilates the product generator on
every function of `(|A|,|B|,|A intersect B|)` but gives the normalized-rank
target expectation `571/852>0`.  Therefore no pointwise product-chain
Poisson/Lyapunov certificate retaining only the two ranks and their overlap
can prove the normalized arithmetic inequality.  The actual chain has
strict slack `19/504`, so this is a proof-architecture obstruction rather
than a fixation counterexample.

Also converted both transform failures to exact rational certificates:

- rank-sum stochastic domination fails at its lowest coefficient on a
  weighted order-four graph;
- the all-`z` Bernoulli-coverage product fails near `z=0` on another weighted
  order-four graph, although its `z -> 1` fixation-product endpoint is
  strictly correct.

Added an independent exact verifier which rebuilds both duals from their
atomic rules and checks all statements.  The verifier passes.  The universal
fixation-product conjecture remains **OPEN**; graph-sensitive within-rank
information is now proved necessary for the product-chain Poisson route.

Completion estimate for this assigned route: `100%` as an exact route
closure; `0%` toward a proof or refutation of the universal endpoint itself.
