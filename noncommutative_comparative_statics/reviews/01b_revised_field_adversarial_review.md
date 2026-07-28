# Adversarial Review 01b — Revised Field Selection

**Artifact reviewed:** `checkpoints/01_field_selection.md`

**Verdict:** narrow conditional go to Checkpoint 2; no-go as a justified new
field yet.

## Score

| Criterion | Score (0–2) | Reason |
|---|---:|---|
| Mathematical coherence | 1 | recognizable object, but category/domains were underspecified |
| Novel object or invariant | 1 | useful combination, presently an approximate path-category representation |
| Coordinate/gauge invariance | 1 | correct isometric conjugacy, but baseline |
| Theorem depth | 0 | proposed results were standard, elementary, or noncanonical |
| Nonsmooth coverage | 1 | important target without a precise transport theorem |
| Predictive utility | 1 | good falsification gates, no held-out benchmark yet |
| Cross-domain naturalness | 2 | recurring and recognizable across several fields |
| **Total** | **7/14** | conditional research-program band |

## Direct subsumption risks added

1. Quantitative and metric rewriting already supplies nonexpansive and
   Lipschitz context-amplified confluence estimates.
2. Precubical sets, higher-dimensional automata, and Mazurkiewicz traces
   already model independent actions and square-swap path equivalence.
3. Vertex spaces plus edge maps form a path-category/quiver representation;
   2-cells present a quotient category.
4. Ulam stability asks when approximate representations are close to exact
   ones.
5. Lattice gauge theory already has edge transport, plaquette curvature, gauge
   covariance, and continuum limits in the invertible sector.
6. Scattering diagrams already organize wall maps, ordered products, and
   codimension-two consistency.
7. Exit-path categories and hybrid systems already encode stratified
   transport; seam/junction behavior requires chosen protocol data.
8. Ordered and cyclic projections already study noninvertible operator
   products.

Representative leads:

- Gavazzo and Di Florio, quantitative rewriting,
  DOI `10.1145/3571256`, arXiv `2206.13610`.
- Fajstrup et al., directed/concurrent topology comparator,
  DOI `10.1016/j.tcs.2016.04.018`.
- Approximate-representation/Ulam-stability lead, arXiv `1510.04085`.
- Discrete principal connections, arXiv `math/0508338`.
- Exit paths, arXiv `0811.2580`.
- Bauschke and Borwein on projection algorithms,
  DOI `10.1137/S0036144593251710`.

## Required formal repair

- Use a finite directed 2-complex \(K\), its free path category
  \(\mathrm{Path}(K)\), and the quotient intervention category
  \(\mathcal C_K\) presented by 2-cell relations.
- Fix the deterministic target category for the first paper: extended metric
  spaces and partial nonexpansive maps.
- Define domains and failure semantics exactly.
- Interpret a response assignment as a functor on the free path category that
  need not factor through \(\mathcal C_K\).
- State that zero cell defects are exactly descent to the quotient; this is a
  baseline proposition.
- Treat gauge invariance, swap accumulation, smooth curvature limits, and
  reset/carry separation as baseline results.
- Define a **rectification constant** measuring whether small relation defects
  imply closeness to an exact response functor. Prove a positive theorem and a
  counterexample.
- Withdraw any canonical additive stratified decomposition without additional
  affine/invertible structure. In the general metric/noninvertible setting,
  use protocol-dependent route comparisons and subadditive bounds.
- Distinguish immediate order effect from persistent memory under subsequent
  continuation.

## Disposition

Accepted. Checkpoint 2 will center on approximate descent/rectification rather
than on the elementary square-defect bound. A smooth, active-set, and jump
scaling trichotomy will be used as a cross-sector diagnostic, not as a claim
that its component theories are new.

