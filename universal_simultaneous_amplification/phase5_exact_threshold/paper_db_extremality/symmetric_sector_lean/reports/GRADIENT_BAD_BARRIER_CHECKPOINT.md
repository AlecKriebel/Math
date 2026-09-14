# Gradient and actual bad-block barrier checkpoint

Timestamp: 2026-09-14T14:49:28Z. Implementation report, not an independent review.
Completion estimate: 100% of the assigned Poisson-gradient/A.22/A.25 obligations.
This report makes no completion claim for the rest of Stage 2 or for Stage 3.

Both `SymmetricSector/Gradients.lean` and `SymmetricSector/BadBarriers.lean`
compile. The imported `GoodPhase` and `BlockActions` modules identify the
actual good response and actual sparse block actions, respectively.

| Manuscript claim | Lean theorem | Exact domain |
| --- | --- | --- |
| A.3 recurrence, including the terminal equation | `gradient_poisson_equation` | `N ≥ 2`, `1 ≤ k ≤ N` |
| A.3a lower and upper gradient bounds | `gradient_bounds` | `N ≥ 2`, `1 ≤ k < N` |
| Positive actual gradients | `gradient_pos` | `N ≥ 3`, `1 ≤ k < N` |
| A.22 first inequality | `phaseWbar_supersolution` | `N ≥ 25`, every bad coordinate |
| A.22 second inequality | `phaseC_Wbar_le` | `N ≥ 3`, every good coordinate |
| Actual inverse comparison `W ≤ Wbar` | `phaseW_le_Wbar` | `N ≥ 25` |
| A.25 both bounds | `phaseF0_bounds` | `N ≥ 25` |
| Strict positivity of actual `f₀` | `phaseF0_pos` | `N ≥ 25`, every good coordinate |

The A.22 supersolution is proved from the actual binomial reward, not from
an independent polynomial. `phaseQ_badReward` proves the concrete Q action.
Its upper and lower binomial-ratio lemmas handle the omitted top and bottom
coordinates through the actual finite-vector zero extension. The cleared
residual is proved equal to A.23 divided by `50*k*(k+1)*(N-k)`; every factor
is positive on the physical domain. The SOS positivity theorem from
`Analytic` then supplies the required sign. This replaces the discriminant
argument for `N ≥ 25`. The separate `N = 24` matrix-barrier claim is not
included; the intended all-order proof uses the finite scalar certificates
through `N = 39`, so the large-order matrix argument only needs `N ≥ 40`.

The C action is also evaluated on the actual reward. Its exact binomial
level ratios include the factor of two from `2^(N-1) = 2*2^(N-2)` and the
absent bottom/top coordinates. `phaseC_Wbar_ratio` identifies the actual
ratio. The difference from `14/25` has a positive-denominator formula with
numerator `7*((N-3)*(2*k+1)+k*(k-1)*(2*k-1)+3)`.

Nonnegative inverse entries, already proved for the actual blocks in
`BlockBounds`, then give `W ≤ Wbar`. Applying the actual good inverse to
both reward inequalities gives `(11/25)*v ≤ f₀ ≤ v`, where `v` and `f₀`
retain their inverse-based definitions in `GoodPhase` and `PhaseConnection`.

The gradient proof derives its terminal equation from the actual binomial
normalization `c₀`. Subtracting consecutive Poisson equations yields the
second-order rank operator. A finite maximum principle proves both
reciprocal barriers, without assuming an endpoint value outside the retained
interval: the absent endpoint coefficients vanish.

## Trust and reproduction

From the project directory, run:

```text
lake build SymmetricSector.Gradients SymmetricSector.BadBarriers
lake env lean reports/GradientBarrierAxioms.lean
```

Every theorem printed by the audit depends only on `propext`,
`Classical.choice`, and `Quot.sound`. Neither implementation contains a
placeholder, project-specific axiom, `native_decide`, or compiler-trust
evaluation. The full audit output is `gradient_barrier_axioms.log`.

Remaining Stage 2 obligations belong to the phase-contraction, occupation
debt, and final scalar-comparison arguments. The physical active-chain
identification is a separate Stage 3 obligation. No result here establishes
the full fixation-Hessian theorem or biological applicability.
