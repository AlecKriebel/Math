# Clique--pendant endpoint-product audit

This folder independently exactifies an unweighted counterexample to the
normalized product inequality at `r=3/2`.

- `CLIQUE_PENDANT_PRODUCT_AUDIT.md` gives the derivation and scope.
- `verify_clique_pendant_product.py` rebuilds the exact quotient chain,
  checks strong lumping against a labelled implementation, and certifies
  `G(31,4)` over `QQ`.
- `certify_minimality.py` exhaustively proves that `G(31,4)` is the first
  product witness by vertex count within this unweighted family.

The witness suppresses dB, so it refutes a proof route but is not a
simultaneous amplifier.
