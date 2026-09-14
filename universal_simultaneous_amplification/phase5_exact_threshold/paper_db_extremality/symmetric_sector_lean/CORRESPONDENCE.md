# Manuscript-to-Lean theorem correspondence

The table identifies checked declarations, not assumptions. Unless a namespace is stated otherwise, names below are in `SymmetricSector`; physical names are in `SymmetricSector.Active`. The full qualified audit target list is `principal_theorems.txt`.

| Manuscript claim | Lean definitions and principal theorems | Domain / status |
|---|---|---|
| 3.10 actual two-move labeled active chain | `Active.lean`: `State`, `kernel`, `kernel_action`, `kernel_affine` | Actual finite cache and target states; no assumed quotient formula |
| 3.17 complete stationary law and collision mean | `Incoming.lean`: `nu0_stationary`, `nu0_sum`; `PhysicalBridge.lean`: `center_eq_c₀` | Stationarity/normalization for n≥2; collision mean for n≥3 |
| 4.2 actual centered resolvent | `Active.lean`: `centeredMatrix`, `green`; `ActiveInverse.lean`: `centeredMatrix_isUnit`, `centeredMatrix_det_isUnit` | n≥2; proved positivity, harmonic connectivity and true inverse |
| 4.6 quadratic active-chain expression | `Active.lean`: `R2` | Defined as ν₀ΔGΔGq, independently of the scalar and norm |
| A.2 rank transition law | `Active.K0_rank` | n≥2, every physical state, both boundary ranks |
| A.3 / A.3b Poisson gradient and bounds | `Definitions.lean`: `gradient`, `c₀`; `Gradients.lean`: `gradient_terminal`, `gradient_poisson_equation`, `gradient_bounds`, `gradient_pos` | Bounds for N≥2, 1≤k<N; strict positivity for N≥3; endpoints d₀=d_N=0 |
| A.11 insertion/erasure features | `PhysicalBridge.lean`: `feature_sample_complete`, `K0_feature`; `OrbitMoments.lean`: `target_near_full_feature_relation` | General labeled identities; redundant coordinates never assumed independent |
| A.12–A.14 two-channel operator | `Definitions.lean`: `Channel`, `coefficientK`; `ChannelFeatures.lean`: `K0_coefficientFeature` | K=Hᵀ, good ranks 1…N−1, bad ranks 2…N−1; a_N=b_N=b₁=0 |
| A.15 source | `Definitions.lean`: `source`; `PhysicalBridge.lean`: `perturbation_green_q`; `ChannelFeatures.lean`: `coefficientFeature_source` | Obtained from actual ΔGq, not stipulated in R2 |
| A.16 reward | `Definitions.lean`: `reward`; `Reward.lean`: `nu0_perturbation_coeff_feature` | Actual ν₀Δ feature pairing; negative bad reward retained |
| A.17 actual reduced scalar | `Definitions.lean`: `reducedScalar`; `RowBounds.lean`: `coefficient_system_isUnit`; `Phase.witness_eq_inverse_mulVec` | Defined by true inverse; invertibility for every N≥3 gives unique coefficient solve |
| Finite lemma: S_N>0 | `Small03.lean`…`Small39.lean`: `CertN.equations`, `value`, `positive`; `SmallFinite.lean`: `finite_small_scalar_pos` | Every integer 3≤N≤39, inclusive, actual source/equations/reward |
| Finite lemma: beta_N+epsilon_N<1 | `Margins.lean`, `GeneratedMargins/Order040.lean`…`Order287.lean`; `FiniteMargins.lean`: `finite_phase_positive` | Every integer 40≤N≤287, inclusive; kernel-checked one-sided witnesses |
| Printed minimum finite margin | `GeneratedMargins/Exact40.lean`: `exact_margin_40`; `FiniteMargins.lean`: `finite_minimum_margin`, `finite_minimum_margin_strict` | Exact printed fraction, uniquely minimal at N=40 |
| A.18–A.19 Schur complement | `PhaseConnection.lean`: actual `phaseS`, `phaseC`, `phaseD`, `phaseQ`, `phaseA`, `phaseF0`, `phaseEll`, `phaseDebt`; `dualGood_schur`, `reducedScalar_schur_identity` | N≥3; true inverses and repeated excursions fully handled |
| A.20–A.21 radial recurrence and upper bound | `GoodPhase.lean`: `phaseV_eq_radialVector`, `phaseV_pos`; `RankBounds.lean`: `t_pos`, `t_upper` | Physical ranks and N≥3; actual recurrence linked to resolvent |
| A.22–A.23 bad forcing barrier | `BadBarriers.lean`: `phaseWbar_supersolution`, `phaseW_le_Wbar`, `phaseF0_bounds` | N≥25, sufficient for every N≥40 on the principal path; no claim at N=24 needed |
| A.24–A.27 contraction | `Contraction.lean`: `phaseHhat_supersolution`, `phaseC_hhat_le`, `phaseA_phaseV_le` | N≥3; concrete blocks and every boundary row |
| A.28–A.31 left occupation and debt | `LeftDebt.lean`: `leftBarrier_supersolution`, `leftOccupation_le_barrier`, `phaseEll_lower`, `phaseDebt_le_printed` | N≥4; sharper Z barrier repairs printed Y inference; same final debt bound |
| A.31 printed shortcut discrepancy | `DebtRepairExample.lean`: `printed_Y_pairing_gap_at_four` | Exact discrepancy 1/360 for the two proposed upper sums, not for actual debt |
| A.32 beta budget | `DebtBudget.lean`: `phaseDebt_le_beta_first`, `phase_first_pos` | N≥40; actual debt bounded by beta times the actual positive pairing |
| A.34 rational subsolution | `Analytic.lean`, `AnalyticTail.lean`: `rational_subsolution_step`, `t_lower_analytic` | N≥288 and 1≤k<N; SOS identity connected to actual recurrence by induction |
| A.35 analytic tail | `AnalyticTail.lean`: `betaTerm_lt_nineteen_twentieths`, `epsilon_lt_one_twentieth`, `analytic_phase_margin` | beta<19/20 for N≥288; epsilon<1/20 for N≥46; combined N≥288 |
| A.33 / A.36 all-order phase margin | `PhaseMargins.lean`: `all_phase_margin` | Every N≥40, finite range joined to analytic tail |
| A.36 all-order scalar sign | `AllOrder.lean`: `reducedScalar_pos_of_forty`, `reducedScalar_pos` | Actual S_N>0 for every N≥3; no central sign or inverse assumption |
| A.17a orbit averages | `OrbitMoments.lean`: `orbit_square_average`, `orbit_cross_average`; `Incoming.lean`: `nu0_perturbation_feature_orbits` | General finite-set counting, coincidence terms and normalizations proved |
| A.17b labeled incoming current | `Incoming.lean`: `nu0_perturbation`, `nu0_feature_zero` | Actual derivative kernel and stationary law, including endpoint caches |
| A.17 general physical identity | `PhysicalIdentity.lean`: `green_perturbation_green_q`, `R2_eq_frobeniusSq_mul_reducedScalar` | Every n≥4 and symmetric balanced real δ; no nonzero-norm assumption |
| Symmetric component sign | `SymmetricComponent.lean`: `R2_symmetricBalanced_pos`, `R2_symmetricBalanced_nonneg`, `R2_symmetricBalanced_eq_zero_iff` | Strict for n≥4 and δ≠0; nonnegative and exact zero iff δ=0 for n≥3 |
| n=3 absent symmetric sector | `Active.lean`: `symmetricBalanced_three_eq_zero`, `R2_symmetricBalanced_three` | Fully proved, distinct from scalar S₃ at physical n=4 |
| S₃=3/208 and S₄=359/26660 | `Cert3.value`, `Cert4.value`; `PhysicalChecks.lean`: `R2_four_normalization`, `R2_five_normalization` | Consistency checks supplement general theorems |

All division domains used in the proofs are discharged. Explicit public denominator theorems include `t_step_den_pos`, `lowerEll_den_pos`, `beta_den_pos`, and physical `retarget_denominator_pos`, `complete_denominator_pos`, `nu0_denominator_pos`. For N=3, `lowerEll 3 1=0`; the finite direct-solve proof covers this order without dividing by that quantity.

Coverage/collision representation as fixation, stationary perturbation expansion/analyticity, full tangent decomposition and other two sector signs remain outside this project. These are dependencies of the full local-optimality theorem, not hidden hypotheses of the proved symmetric component.
