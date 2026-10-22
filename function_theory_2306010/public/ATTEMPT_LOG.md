# Substantive approach record

Target: 2306010 / AMR-022-6010, Function Theory 6.10. Date: 2026-10-04 UTC.

## Turn 1 of 5: complete reconstruction of a prior negative resolution

**09:18–09:28 UTC.** The source gate began at the catalogue URL. Its failed fetch was followed by the exact Hayman–Lingham source and current-literature searches. These immediately identified the September 2026 Guo–Hu preprint. The complete imported statement and previous OPEN-TRIAGE report were read; neither was substituted for the primary mathematics.

The substantive work in this turn was one connected complete-verification approach:

1. Matched the target, exterior domain, and zero-constant Laurent normalization.
2. Reconstructed the single-valued binomial-series primitive G and its derivative branch.
3. Proved the weighted Laurent-tail injectivity inequality on the closed exterior, including a uniform derivative lower bound, using a telescoping majorant for the absolute binomial coefficients.
4. Reconstructed the geometric bridge from regular Jordan boundary to the omitted set, positive tangent turning to convexity, and convexity to nonnegative exterior pre-Schwarzian real part. This fills the interpretation boundary between an analytic predicate and actual geometric convexity.
5. Verified convexity of F,G and the exact negative rational certificate for their 3/5–2/5 combination H.
6. Wrote and ran 438 standard-library exact checks with six negative controls; a second run reproduced CHECKS.json byte for byte. No floating-point or exhaustive parameter search was used.
7. Inspected the prior author's analytic and geometric Lean entry points at a pinned commit, while explicitly declining to claim an unperformed Lean build or a full formal audit.

**Outcome:** complete candidate reconstruction of a known counterexample, credited to Guo–Hu. Suggested status `already_solved`, turns `1/5`. No novelty claimed. A fresh independent audit is pending.

**Why turns 2–5 were not used:** the whole exact target has a complete prior-resolution reconstruction in turn1. Spending further turns on alternative attempted solutions would obscure that outcome and risk misattributing a known result. The sections above are components of one verification approach, not five artificially relabeled turns.

**Completion estimate:** the conventional proof and reproducible controls are complete. The remaining gate is independent adversarial review of this frozen packet. If that review finds a genuine mathematical gap, it must be recorded explicitly rather than ignored or relabeled as verified.
