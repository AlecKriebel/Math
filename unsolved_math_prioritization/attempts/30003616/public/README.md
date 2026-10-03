# Spectral rays for continuum Fibonacci operators

**Problem:** 30003616 / OWR-15951-003, queue rank 505.

**Disposition:** `unsolved 5/5`. No proof or counterexample settles the full question. This package records five substantive approaches, rigorous partial deductions, and exact obstructions to several insufficient arguments. It makes no priority or novelty claim.

The operator acts on **the full plane** `L²(R²)`. “Half-line” means an energy interval `[E*, infinity)` contained in its spectrum. This is not a Schrödinger operator on a spatial half-line, and there is no boundary-condition parameter.

The source allows arbitrary real tile functions `f0,f1 in L²([0,1))`, concatenated by the Fibonacci word, and asks about every pair of positive couplings. The established constant-tile, equal-coupling theorem is a special case, not a resolution of that target.

## Contents

- [RESULT.md](RESULT.md): exact formulation, five approaches, proofs, and remaining gaps
- [SOURCE_AUDIT.md](SOURCE_AUDIT.md): original source, checked literature, and duplicate scope
- [RESEARCH_LOG.md](RESEARCH_LOG.md): dated approach record and completion estimates
- [checks/check.py](checks/check.py): small exact algebra and finite-residue checks
- [checks/results.json](checks/results.json): recorded check output

The strongest analytic deduction here is an elementary bound for the Fricke–Vogt invariant,

`|I(E)| <= (exp((||q0||_1 + ||q1||_1)/sqrt(E)) - 1)^2`,

valid for arbitrary real integrable tile functions and `E>0`. With the established dimension theorem, it gives a `1 - O(E^(-1/2))` lower bound for local Hausdorff dimension in the aperiodic case. It does not establish thickness or an energy ray.

All mathematical claims are frozen for fresh independent audit. The original reports, PDFs, downloaded text, and dataset records are not part of this public package.

