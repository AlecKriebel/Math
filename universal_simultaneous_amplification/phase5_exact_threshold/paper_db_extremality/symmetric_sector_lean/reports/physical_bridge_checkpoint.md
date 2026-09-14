# Active-chain bridge checkpoint

Timestamp: 2026-09-14T14:46:23Z. Stage 3 estimated completion: 55%.
This is a proof-development checkpoint, not completion of the scalar identity.

Kernel-checked in `PhysicalBridge.lean`:

- Cache insertion and erasure identities for the actual `x` and `z` features.
- `feature_sample_complete`: exact complete-kernel feature action on arbitrary
  caches, including the empty intermediate cache at the lower stop boundary.
- `K0_feature`: general-n intertwining for the actual labeled active kernel
  and the displayed two-channel coefficient formulas. It permits arbitrary
  endpoint coefficients; it does not assume feature independence.
- `rankPotential_poisson`: the recurrence-defined gradients integrate to a
  solution of the actual labeled equation `(I-K0)h = 1/rank-c₀(n-1)`, including
  both physical endpoint ranks.
- `perturbation_rankPotential`: the exact actual first perturbation of this
  rank potential equals the Appendix A gradient source.

Kernel-checked in `ActiveInverse.lean`:

- Nonnegativity and row normalization of the actual `K0`.
- Strict positivity of the actual continue and stop moves.
- `constant_of_positive_moves`: concrete connectivity of all active states,
  proved by growing each cache and connecting the maximal-cache targets.

All displayed axiom reports for these theorems contain only `propext`,
`Classical.choice`, and `Quot.sound`. No external computation is trusted.

Exact remaining bridge gaps at this timestamp:

- Compose concrete connectivity with the independently supplied stationary
  Dirichlet-energy lemma to prove the physical centered matrix invertible.
- Identify the actual centered Green application using the checked Poisson
  potential and stationary normalization.
- Link finite `Channel N` matrix coefficients to the explicit natural-rank
  coefficient formulas in `K0_feature`.
- Complete the incoming-current/orbit-moment/reward contraction and combine
  it with both genuine Green applications to identify `R2` with the scalar.

These are missing Lean infrastructure and assembly obligations. This work has
not found a mathematical gap in the corresponding manuscript identities.

## 2026-09-14T14:54:47Z — physical inverse and first Green application checked

Stage 3 estimated completion: 85%. `ActiveInverse.lean` now proves
`centeredMatrix_isUnit` and `centeredMatrix_det_isUnit` for every `n≥2`, using
proved stationarity, positive stationary weights, finite stationary Dirichlet
energy, and the actual labeled transition connectivity. No irreducibility or
matrix-invertibility hypothesis remains.

`PhysicalBridge.lean` now also proves `center_eq_c₀`, `green_q`, and
`perturbation_green_q`. The last theorem identifies the actual `Δ G q` with the
Appendix A.15 gradient source for every `n≥3`. All their axiom reports contain
only the ordinary foundational trio.

Independent incoming/reward work now provides proved normalization,
zero stationary feature means, and the exact actual-current contraction
`ν₀ Δ F = ‖δ‖² · (gᵀc)` for the zero-extended finite channel vector. The only
remaining Stage 3 assembly items are the finite-channel coefficient linkage
and the second Green application/principal identity. These are being checked
without assuming independence of feature coordinates.

## 2026-09-14T14:57:34Z — general-n principal physical identity checked

Stage 3 identity completion: 100%. The full module build
`lake build SymmetricSector.PhysicalIdentity` passed.
`R2_eq_frobeniusSq_mul_reducedScalar` proves the exact actual-chain identity
for every n≥4 and every real symmetric balanced perturbation, including zero.
The second Green application is identified by its proved centered Poisson
equation, and the finite coefficient inverse is verified independently.
There are no remaining physical-to-scalar bridge hypotheses.

All principal theorem dependencies are only `propext`, `Classical.choice`,
and `Quot.sound`. The independent model reviewer is auditing the final
statement. The integrated positivity module is written and awaits the
separate all-order scalar module's successful build.

## 2026-09-14T15:07:20Z — integrated all-order physical positivity checked

Stage 3 and the integrated symmetric component: 100% of the requested proof
statements implemented. `SymmetricComponent.lean` now compiles:

- `R2_symmetricBalanced_pos`: for every n≥4 and every nonzero real symmetric
  balanced perturbation, the actual `ν₀ Δ G Δ G q` is strictly positive.
- `R2_symmetricBalanced_nonneg`: nonnegative for every n≥3, including the
  absent sector at n=3.
- `R2_symmetricBalanced_eq_zero_iff`: within the admissible sector, the actual
  form vanishes exactly when the perturbation is zero, for every n≥3.

These compose the completed `AllOrder.reducedScalar_pos` with the independently
proved physical identity. All transitive axioms remain only `propext`,
`Classical.choice`, and `Quot.sound`. The aggregate independent clean-build and
release checkpoint are the parent's remaining validation workflow. The full
fixation Hessian/local-optimality theorem remains outside the formalized scope.
