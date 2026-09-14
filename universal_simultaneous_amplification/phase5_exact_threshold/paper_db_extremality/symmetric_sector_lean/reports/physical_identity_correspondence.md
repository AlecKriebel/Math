# General-n physical identity: correspondence and trust audit

Timestamp: 2026-09-14T14:57:34Z. Stage 3 identity completion: 100%.

The principal theorem is
`SymmetricSector.Active.R2_eq_frobeniusSq_mul_reducedScalar` in
`SymmetricSector/PhysicalIdentity.lean`:

```
{n : ℕ} → 4 ≤ n → {δ : Matrix (Fin n) (Fin n) ℝ} →
SymmetricBalanced δ →
R2 δ = frobeniusSq δ * (reducedScalar (n - 1) : ℝ)
```

`SymmetricBalanced` means zero diagonal, symmetry, and zero row sums; the
zero column sums follow by the proved `column_sums_zero`. `frobeniusSq` is
exactly `Σ i, Σ j, δ i j ^ 2`. `R2` is defined independently as the actual
labeled expression `ν₀ Δ G Δ G q`. It does not mention `reducedScalar`.
The scalar remains the exact rational `gᵀ(I−coefficientK)⁻¹s` from Appendix A.
The theorem includes `δ=0` and does not divide by its norm.

| Manuscript obligation | Checked declarations |
|---|---|
| 3.10, the two labeled moves | `Active.State`, `kernel`, `kernel_action` |
| 4.1 actual first derivative | `kernel_affine`, `perturbation` |
| A.2 actual rank transition law | `K0_rank` |
| 3.17 stationary law and normalization | `Incoming.nu0_stationary`, `nu0_sum`, `PhysicalBridge.center_eq_c₀` |
| 4.2 centered resolvent exists | `ActiveInverse.centeredMatrix_isUnit`, `centeredMatrix_det_isUnit` |
| A.3 rank Poisson source including endpoints | `Gradients.gradient_poisson_equation`, `PhysicalBridge.rankPotential_poisson`, `green_q` |
| A.11 feature insertion/erasure | `cacheX_insert`, `cacheZ_insert`, `cacheX_erase_self`, `cacheZ_erase` |
| A.12–A.14 actual coefficient action | `feature_sample_complete`, `K0_feature`, `ChannelFeatures.K0_coefficientFeature` |
| A.15 actual first perturbed Green source | `perturbation_green_q`, `coefficientFeature_source` |
| A.16 exact binomial reward | `Reward.nu0_perturbation_coeff_feature` |
| A.17a exact orbit counting | `OrbitMoments` and `Incoming.nu0_perturbation_feature_orbits` |
| A.17b labeled current | `Incoming.nu0_perturbation` |
| A.17 full general-n identity | `PhysicalIdentity.R2_eq_frobeniusSq_mul_reducedScalar` |
| n=3 absent sector | `Active.symmetricBalanced_three_eq_zero`, `R2_symmetricBalanced_three` |

The physical inverse proof uses the actual transition matrix, positive
stationary weights, finite stationary Dirichlet energy, and proved labeled
connectivity. Connectivity and invertibility are not hypotheses. Feature
coordinates are never assumed independent; the top-rank zero features and
rank-one zero bad feature enforce the absent endpoints.

The build command `lake build SymmetricSector.PhysicalIdentity` completed
successfully. Its saved output is `reports/physical_identity_build.log`.
Every printed principal dependency report contains only `propext`,
`Classical.choice`, and `Quot.sound`. No project-specific axiom, `sorryAx`,
`native_decide`, custom evaluator, or external solver result is used.

Remaining scope is explicit. The separate Stage 2 theorem `SymmetricSector.reducedScalar_pos` now compiles,
and `SymmetricSector.Active.R2_symmetricBalanced_pos` combines it with this identity
to prove strict positivity of the actual physical expression for every
nonzero symmetric balanced perturbation and every n≥4. The
coverage/collision representation, analytic stationary perturbation, other
sectors, full tangent decomposition, and the fixation/local-optimality
interpretation are outside this symmetric active-chain component. No
uniform-in-n neighborhood or open global conjecture is asserted.

Independent statement audit: `reviews/model_translation_final.md` (2026-09-14
14:59 UTC) independently compiled the principal identity and found no
translation error or unsupported assumption. It explicitly checked source
orientation, both Green applications, the non-independent features, all
endpoints, and the exact Frobenius normalization.
