# Calculus and stationarity verification checkpoint

Timestamp: 2026-09-11T02:00:35.239964+00:00. Estimated completion of this assigned calculus chain: 100%; this is not an estimate or certification of the full paper.

## Exact checked claims

The pinned Lean 4.19.0 / pinned Mathlib build checks `Bell.ImplicitCurve`, `Bell.IncidenceDifferential`, and `Bell.IncidenceStationarity`. The statements are unchanged. Generic `exists_level_curve` and `exists_normalized_lagrange` also check in independent small import files. No `sorry`, new axiom, or assumed stationarity was introduced.

The derivative is the genuine strict derivative of the six polynomial constraints. Invertibility of the probability block and feasibility imply its surjectivity. The ordinary constrained local maximum yields normalized Lagrange multipliers, then both metric and frame stationarity identities. A kernel vector integrates to a differentiable level-set curve, and the exact quadratic gap produces an uphill curve contradicting local maximality when its coefficient is positive.

## Adversarial mechanism checks

- The five-null-constraint right inverse uses `Z = (Pᵀ)⁻¹ S(c)`, where `P = gY`. Since `g` is symmetric, `Yᵀg=Pᵀ`, so `YᵀgZ=S(c)`. The finite seed has diagonal entries `cᵢ/2` and off-diagonal `(c₄-c₀-c₁-c₂-c₃)/4`; its quadratic values on all five fixed rays are exactly half their prescribed values. This is now checked by Lean, including the signed fifth ray.
- The radial direction `(0,Y)` differentiates each null quadratic to twice its value, which is zero only at feasible points. Its mass derivative is exactly one because the normalization is one. Subtracting the unwanted mass component therefore preserves every prescribed null derivative. Both hypotheses are essential and explicit.
- The implicit-curve theorem assumes actual strict differentiability, derivative surjectivity and a kernel vector. Finite-dimensional codomain supplies the complemented-kernel mechanism through Mathlib. It asserts feasibility only eventually near zero, matching the subsequent local-maximum argument.
- The quadratic limit uses only first differentiability; division occurs on the punctured neighborhood. The score-improvement argument needs a strictly positive limiting form. Zero directions or zero quadratic values provide no conclusion and are not silently promoted.
- The Lagrange functional is normalized only after proving its scalar coefficient nonzero from derivative surjectivity. Metric stationarity is derived by comparing frame and metric variations; it is not an input premise to the main stationarity theorem.

## Scope and remaining gap

These files prove statements about the explicitly defined finite-dimensional real incidence chart. Establishing that the paper's physical complex-qubit POVM data reduce to that chart, and assembling the complete global equality/separation result, remains the responsibility of the other dependency chains and final theorem-contract review. This checkpoint alone does not certify those correspondences.

## Repairs

Current Mathlib derivative imports and names; explicit point equality in derivative composition; scalar-coordinate continuity; explicit continuous-linear-map extensionality; finite vector-entry simplification; removal of invalid doc-comment/set-option placement; and separating elaboration of derivative or limit compositions from their expected goals. The last change avoids expensive definitional unfolding of bilinear forms and does not change proof content. The algebraic frame-congruence lemma was moved to `IncidenceAlgebra` in coordination with its owner, allowing geometric modules to depend on algebra alone.

Axiom audit command: `lake env lean local_verification/CalculusAudit.lean`; output in `local_verification/calculus_axioms.log`.

## 2026-09-11T02:06:01.030482+00:00 — physical extremality/filtering checkpoint

Estimated completion of the expanded assigned module set: 100%. `Bell.ExtremeMeasurement` and `Bell.CommonSpanFiltering` now build as production modules under the pinned compiler. Their theorem contracts are unchanged.

Adversarial checks: scalar dependence is converted into an actual pair of positive measurement perturbations whose midpoint is the *complete* behavior. Extremality identifies each branch behavior with the original, and a nonzero full-Schmidt-rank marginal detects each active coefficient. Zero effects are explicitly excluded by `EffectSupport`, and full-rank effects can coexist with no other nonzero effect. The full-rank-effect deterministic conclusion uses normalization to identify its sole effect with the identity. No extremal measurement selection assumption is introduced.

Common-span filtering constructs a physical normalized assemblage for each sign. The left sum is `I ± εH` and the right sum is `reduced/(1 ± ετ)`, with `τ = localTrace H reduced`. The scalar denominator is positive by the simultaneous perturbation lemma. Branch weights are `(1 ± ετ)/2`, their sum is one, and the complete weighted behavior equals the original. Equal weights would generally be incorrect; the Lean proof uses the displayed unequal weights. Strict marginal positivity then forces every active coefficient to equal τ. Zero effects contribute zero, giving the scalar-identity common-span conclusion.

Repairs: unfolding the pure-state density before applying the Born identity; correctly reducing marginal behavior sums; replacing nonexistent subtype-sum APIs by a filter/subtype equality; explicit real-to-complex scalar multiplication; trace cyclicity applied only to the intended factors; and avoiding a rewrite that changed H inside the scalar coefficient when proving the final span identity.
