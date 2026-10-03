# Final status: exhausted, unresolved WIP

ID 30001070 / OWR-2090-023. Five of five substantive author turns used. No complete proof or counterexample was found. The original unrestricted radius bound and its equality clause remain unresolved in this attempt. No independent verification or novelty clearance has been completed for the partial lemmas.

## Exact scope

For a bounded n-dimensional convex polytope with exactly 2n facets containing the origin-centered Euclidean unit ball, the target is max ||x|| >= sqrt(n), with equality exactly for circumscribed cubes. Central symmetry, volume minimization, surface-area minimization, and a freely chosen outer-ball center are not assumptions or objectives of this target. The literature-established cases and the nonsymmetric general case are kept separate.

## What was established within this attempt

- The reduction to tangent facets and polar spherical covering preserves boundedness, exact facet/vertex counts, and the equality clause.
- The cube is a strict local minimum modulo common rotations by an averaged-vertex Hessian computation; this is not claimed novel.
- Centered equal-weight tight-frame normal configurations satisfy the sharp inequality and cube-only equality. This restricted lemma is not an objective-preserving normalization of arbitrary configurations and is not claimed novel.
- Weighted active-facet mass would be sufficient under extra geometric hypotheses. A purely combinatorial version is false, as checked by an exact stacked-polytope example.
- A regular local optimizer has a necessary stationary PSD matrix identity. Its weak trace estimate does not yield the sharp bound; the missing stronger estimate is not assumed.
- An exact dimension-five anisotropic nonsymmetric example with ten normals and 34 polar vertices is not a counterexample. Finite floating-point probes likewise found none, without certifying optimality.
- Cauchy–Binet gives an all-bases determinant identity, but an exact example proves that its mean cannot be transferred to feasible vertices. The required feasible-bases inequality is unproved.

## Exact remaining gap

No global mechanism has been found for arbitrary, potentially noncentered and anisotropic configurations of exactly 2n unit normals positively spanning R^n. The global lower bound is unproved here, and the equality classification cannot be claimed without it. The five-turn budget is exhausted; these notes must not be used to reset or bypass that limit.

## Evidence and limitations

Each TURN_k.md has a corresponding exact-check script and captured result. Checks use rational SymPy arithmetic and small finite enumerations. The two scripts prefixed diagnose_ use floating-point arithmetic and have explicitly bounded, non-exhaustive scopes. No raw source PDFs, private context, or third-party correspondence are included in this WIP package.

Sources and existing credit are listed in README_WIP.md. The primary statement and a 2026 source support the continued open-status assessment, but a literature search cannot prove universal absence of an unlocated result. This package has no result PR or solved claim.
