# Research log: endpoint-spine order obstruction

## 2026-08-13 — exact two-cycle stopping certificate

- Started from the full linked-spine identity
  `G=<A,K(x-1)>_m=<A,x-1>_m-cross_K(A,x)`.
- Used the symbolic deterministic two-cycle endpoint family; no graph,
  kernel, or parameter search was performed.
- Proved uniformly for `3/2<=r<=151/100` and every `kappa>0`,
  `kappa!=1`, that `x-1` has one positive and one negative coordinate.
- Proved that `A` and `x` are strictly comonotone, so the cross-Dirichlet
  correction is positive rather than discardable.
- The Doob spine is the deterministic swap, hence `KA` reverses the
  `A`-order and is strictly antimonotone in `x`.
- Factored the true endpoint gap and proved it remains strictly positive
  throughout the family using two coefficient-positive polynomials in
  `r-3/2`.
- Conclusion: the endpoint equations do not force the qualitative
  one-crossing/order-preservation condition needed by this proposed proof
  architecture.  This is a route obstruction only; the universal endpoint
  sign remains open.
