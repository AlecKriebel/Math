# PDF and verifier QA log

This log records the final checks on the preprint package. Times use
America/Los_Angeles.

## 2026-08-08 — final local QA

### Exact replay

`./replay.sh` completed successfully from a clean invocation.

| Log | Final result |
|---|---|
| `triangle_module.log` | exact module formulas and endpoint coefficients PASS |
| `triangle_star_independent.log` | independent triangle chains, limits, and macro identities PASS |
| `center_triangle_lumping.log` | all labelled-to-quotient comparisons under Bd and dB PASS |
| `fixed_rank_portal.log` | fixed-rank Bernstein certificates and labelled trace PASS |
| `direct_trace_exact.log` | all labelled direct-portal subset rows and parent odds PASS |
| `diffuse_growing_portal.log` | all growing diffuse-portal limit identities PASS |
| `endpoint_product_counterexample.log` | exact 318-state product and balanced-mean violations PASS |
| `endpoint_product_independent.log` | independent microscopic rational solve agrees PASS |
| `endpoint_product_audit.log` | independent lumping, zero residuals, and compact rational bounds PASS |
| `growing_endpoint_product.log` | labelled lumping and limits `32/27`, `8/9`, `256/243` PASS |
| `one_third_affine.log` | general leaf-proportion affine sharpness algebra PASS |
| `one_third_triangle.log` | 24-term positive weighted-triangle certificate PASS |
| `one_third_green.log` | Green--Poisson identity and exact affine window PASS |
| `weighted_pendant.log` | arbitrary-weight pendant activation bound PASS |
| `direct_q2_portal.log` | 7,323-monomial denominator and 11-box Bernstein cover PASS |

The replay ended with `ALL EXACT REPLAY CHECKS PASSED`.

### Build and metadata

- Compiler: Tectonic / XeTeX driver.
- Pages: 18, US Letter, no encryption or JavaScript.
- TeX log: no overfull boxes, underfull boxes, unresolved references,
  multiply defined labels, package warnings, or errors.
- Determinism: two consecutive builds with the fixed `SOURCE_DATE_EPOCH`
  produced identical SHA-256 hashes.
- Final PDF SHA-256:
  `cfd9eb2755a4f9296eae8209adff6f6b41708425a4a4f186e647184ec6617672`.

### Poppler render and page-by-page visual inspection

Every page was rendered at 150 dpi under `output/rendered/` and inspected at
original or high detail.

| Pages | Visual check |
|---:|---|
| 1--3 | title, abstract, scope box, model, baselines, and quantifiers clean |
| 4--6 | graph diagram, construction, triangle formulas, and center formulas clean |
| 7--10 | rare-edge trace, both takeover stages, initialization, and endpoint expansion clean |
| 11--12 | scoped portal limits and exact finite counterexample clean |
| 13--16 | growing product proof, post-establishment stages, affine window, and weighted-pendant proof clean |
| 17 | verifier table and conclusion clean |
| 18 | scope box, disclosure, and bibliography clean |

No clipped text, overlap, malformed equation, broken figure, unreadable table,
or accidental exact-threshold claim was found.

### Hostile mathematical audit

The post-establishment proof was re-audited after explicit repairs to the
ordinary-singleton stopping argument, the killed-branch cutoff exchange, the
Bd boundary bridge, and the dB coupon/R-extinction stage. The auditor found
no remaining incorrect equation, quantifier, proof direction, or limit
exchange. The abstract and corollary consistently say that `1/3` is the
maximal possible Bd coefficient; they do not claim the one-third separator is
universal.

### Scope audit

The paper consistently distinguishes:

- **PROVED:** `R_sim >= 3/2`;
- **PROVED:** the displayed family's exact interval is `(1,3/2)`;
- **EXACTLY REFUTED:** the normalized-product and balanced-mean endpoint
  separators;
- **PROVED:** the growing product violation, maximal affine coefficient,
  weighted-triangle theorem, and arbitrary-weight pendant obstruction;
- **OPEN:** the one-third separator for arbitrary graphs, every universal
  upper bound, endpoint impossibility, and the exact value of `R_sim`.
