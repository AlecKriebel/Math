# Hostile endpoint optimization at fitness `3/2`

This directory is an independent Gate-2 falsification branch.  It asks for
counterexamples to the two endpoint statements

\[
 P(G)=\frac{\rho_{\rm Bd}(G)\rho_{\rm dB}(G)}
 {\rho_{\rm Bd}(K_n)\rho_{\rm dB}(K_n)}\le 1,
 \qquad
 M(G)=\min\!\left\{\frac{\rho_{\rm Bd}(G)}{\rho_{\rm Bd}(K_n)},
 \frac{\rho_{\rm dB}(G)}{\rho_{\rm dB}(K_n)}\right\}\le1.
\]

`search_endpoint.py` builds both effective subset chains directly from the
two update definitions.  It optimizes `P`, `M`, the normalized arithmetic
mean, and weighted Pareto scalarizations on fixed supports.  Floating-point
results are discovery data only.

`verify_endpoint_candidates.py` is a separate exact-rational implementation.
It is used to recheck any apparently positive candidate and a deterministic
hostile corpus.  Passing its finite tests is not a universal proof.

`verify_balanced_poisson.py` proves and checks the exact Green--Poisson
reduction in `BALANCED_POISSON_REDUCTION.md`.  It isolates the remaining
balanced-separator sign as one coupled cross-rule, cross-rank occupation
inequality and exactly refutes all separate state/rank/mismatch shortcuts.

`verify_vertex_bilinear_farkas.py` is an exact rational LP-dual certificate.
On a weighted three-path it proves that no arbitrary vertex-labelled
bilinear correction to the complete radial product-chain Poisson potential
can satisfy the desired pointwise drift inequality.  The same script checks
that this graph is a proof barrier, not a fixation counterexample.

## Current classification

- **OPEN:** the universal product inequality and the weaker endpoint
  disjunction.
- **NO COUNTEREXAMPLE FOUND:** direct nonsmooth optimization of `M`, product,
  and normalized arithmetic objectives on the finite supports described in
  `HOSTILE_ENDPOINT_REPORT.md`.
- **EXACTLY REFUTED AS NUMERICAL ARTIFACT:** an extreme separated star whose
  double-precision Bd solve returned an impossible normalized ratio larger
  than `10^5`; rational reconstruction gives `x~0.66575`, `y~0.45617`.
- **PROVED FOR ONE HOSTILE ONE-PARAMETER FAMILY:** on `K_{2,2}` plus one
  chord of arbitrary weight `a>=0`, the dB ratio is strictly below one and
  both the normalized-arithmetic and product gaps have coefficient-positive
  numerators.
- **EXACT DUAL GUIDANCE:** if a graph-independent affine separator
  `lambda*x+(1-lambda)*y<=1` exists, two exact witnesses force
  `lambda>177/2000` and `lambda<7/12`.  The balanced candidate `lambda=1/2`
  survives; this does not prove it.
- **PROVED REFORMULATION / OPEN SIGN:** the balanced separator is exactly
  `T+C<=E` for explicit Green occupation, signed-cut, and dispersion terms.
  Neither term is separately signed, even after aggregation by rank.  The
  remaining minimal obstruction is a coupled Green-flow inequality.
- **EXACTLY REFUTED PROOF ANSATZ:** an exact ten-atom Farkas law excludes
  every radial-plus-vertex-bilinear pointwise product-chain Poisson
  certificate on the rational weighted path with edge ratio `17`.  A
  successful certificate must use nonlinear/higher-order vertex data or an
  aggregate rather than pointwise inequality.

No literature search or external contact is used in this branch.
