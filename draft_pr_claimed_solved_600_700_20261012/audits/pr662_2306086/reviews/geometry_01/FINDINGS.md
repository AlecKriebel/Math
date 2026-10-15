# Analytic and geometric adversarial findings

**PASS for the specified qualitative theorem. Mandatory changes: 0. Optional changes: 0.** This verdict does not certify priority, a quantitative sharp result, or an unqualified closure of the source problem.

Target: PR 662 / problem 2306086, exact head `e31701151c331a6eed9224fb37a75a374ea1043e`. All 24 frozen native files match the scope/snapshot sizes and SHA-256 hashes and the Git blob bytes at that head. See `BINDING_CHECK.json`. Review artifacts are confined to this `reviews/geometry_01` folder. There was no Git or remote mutation and no outreach.

## Strongest verified result

For normalized real-coefficient holomorphic injections on the unit disk,

\[
M(z)=\max_f\left|(1-|z|^2)f''(z)/f'(z)-2\bar z\right|
\]

exists and satisfies \(M(x)=4\) for \(-1<x<1\) and \(M(z)<4\) at each fixed nonreal point. A uniform strict gap also exists on every compact \(K\subset\mathbb D\setminus\mathbb R\). The original displayed quantity at zero is identically zero; the normalized auxiliary functional at zero is different.

## Attacks and outcomes

| Attack | Result and checkable reason |
| --- | --- |
| Exterior square root might be multivalued or noninjective | Resolved independently by a normalized logarithm of \(F(z)/z\) on the disk, followed by the sign/oddness/nonvanishing argument. |
| Area-theorem equality might fail to classify the map | Resolved: saturation of the \(b_1\) contribution forces every other negative coefficient to vanish; oddness removes the constant term. The limiting inequality can be taken first over finite partial sums. |
| Equality of the Koebe transform might be mistaken for equality of the original function | This shortcut is false, but the submitted proof does not use it. An exact normalized inverse-transform control attains \(A_f(i/2)=4\), is not a Koebe rotation, and is outside the real class. |
| An affine slit with a real endpoint might evade the real-class classification | A real endpoint alone is insufficient: the exact control has endpoint \(-5/12\) and oblique outgoing vector \(7/15-8i/5\). Conjugation invariance constrains both. The submitted proof does so. |
| Conformal comparison could be pointwise division, or could leave the slit endpoint free | The controlling scope note explicitly requires inverse composition. The resulting zero-fixing disk automorphism has derivative modulus \(1/(4|c|)=1\), forcing the endpoint distance \(1/4\); positive derivative then fixes the rotation. |
| Pointwise strictness might have been substituted for a strict supremum | The independent growth bound proves normality; normalization excludes constant limits; Hurwitz applied to holomorphic divided differences proves injectivity of limits. Compactness then gives an attained maximum below 4. |
| A zero derivative or moving evaluation point might invalidate continuity | Holomorphic injectivity forbids zero derivative, and the nonconstant limit stays injective. Cauchy derivative convergence on a neighborhood proves joint continuity for moving interior points. |
| Compact sets might approach the boundary or real axis | A compact subset of \(\mathbb D\setminus\mathbb R\) excludes both. No global gap on all nonreal points is inferred. Empty compact sets are vacuous. |
| Negative real normalization derivative or the original zero-point display might change the claim | Division by a nonzero real derivative, of either sign, preserves reality and the pre-Schwarzian. The original display is separately zero at the origin. |

The complete independent reconstruction is in `DERIVATION.md`. Its core proof was written before consulting the existing audit; the explicit inverse-transform control was added afterwards. The existing audit was compared and found consistent with the reconstructed mechanism. The historical wording “quotient” is corrected by the already bound scope clarification; it is not an outstanding required change.

## Exact controls and limitations

`exact_adversarial_controls.py` supplies seven exact symbolic checks of an admissible counterexample to the tempting equality shortcut. The first control run included an unjustified extra expectation that its ray endpoint would be nonreal; it failed because the endpoint is real while the direction is oblique. The harness was corrected to test the actual geometric obstruction, and all seven final checks pass. This was a check-design correction, not a defect in the target proof. Exact output is in `EXACT_CONTROLS.json`.

The native author/audit controls were not used to establish this analytic result. No floating-point computation supports the strict gap here. The binding check and exact control use the pinned interpreter at `/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python` without resolving its symlink.

## Exact remaining gap

There is no identified remaining analytic or geometric gap in the scoped qualitative theorem. An explicit or sharp formula for \(M(z)\), its general nonreal extremizers, the full variability region, historical priority, current literature, and adjudication of whether the source's intended problem demands more are not established by this review. These exclusions must remain attached to any broader disposition.
