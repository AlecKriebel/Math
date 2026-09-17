# Manuscript correspondence and scope

This map describes the statements encoded in the Lean companion to the [bundled manuscript](reference/manuscript/main.tex). Its SHA-256 is `82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71`; its Git blob identifier is `bbd0667c934d5a34dd9c8ced50df91515cb1308c`.

Compilation checks those statements and their proofs. Correspondence with the manuscript depends on the definitions, quantifiers, conventions, and boundaries described here. The [verification index](verification/README.md) records current execution evidence; the [claim ledger](reference/paper_claim_ledger.json) and [source inventory](reference/source_inventory.json) provide machine-readable navigation.

Unless indicated otherwise, theorem names below have prefix `CyclicBell.General.`. The earlier explicit four-dimensional modules use `CyclicBell.D4`. All-dimensional value statements assume `d≥2`; the nonuniform permutation counterexamples assume `d≥4`.

## Physical models and exact Bell values

| Manuscript claim | Source and scope |
| --- | --- |
| Finite states, measurements, encodings, and Born probabilities | [GeneralModel.lean](CyclicBell/GeneralModel.lean): actual positive trace-one mixed states and complete orthogonal PVMs, with arbitrary finite local dimensions. `encoded_unitary`, `encoded_order`, and `measurement_reconstruction` connect PVMs and observable powers. |
| `Q_q`, `Q_qa`, `Q_qc` and Bell suprema | [GeneralCorrelationValues.lean](CyclicBell/GeneralCorrelationValues.lean): `Qq`, `Qqa`, `Qqc`, `betaQ`, `betaQa`, `betaQc`. The approximate model is the product-topology closure; the commuting model uses PVMs on complete complex Hilbert spaces. |
| Finite tensor-to-commuting inclusion | [GeneralHilbertBridge.lean](CyclicBell/GeneralHilbertBridge.lean): `finiteToCommuting`, `finiteToCommuting_behavior`; the entire Born behavior is preserved. |
| `Q_qa⊆Q_qc` in finite-input scenarios | [GeneralCoverageClosureContainment.lean](CyclicBell/GeneralCoverageClosureContainment.lean): `Qqc_isClosed`, `Qqa_subset_Qqc`, `quantum_model_inclusions`. An ultralimit of actual word kernels is realized in a Hilbert completion with reconstructed commuting PVMs. Closedness or a limiting realization is not assumed. |
| `lem:scalar`: scalar maximum and equality set | [GeneralScalar.lean](CyclicBell/GeneralScalar.lean): `scalar_bound`, `scalar_equality_iff`. |
| `lem:polar`: general positive-factor identity | [GeneralCoveragePolarCanonical.lean](CyclicBell/GeneralCoveragePolarCanonical.lean): `Coverage.canonical_polar_hilbert_positive_factor_identity`, on an arbitrary complete Hilbert space, including singular operators. See the polar-decomposition boundary below. |
| First-family finite and commuting bounds | [GeneralFirstBound.lean](CyclicBell/GeneralFirstBound.lean): `first_physical_upper`; [GeneralCommuting.lean](CyclicBell/GeneralCommuting.lean): `first_commuting_hilbert_bound`, `first_augmented_commuting_hilbert_bound`. |
| `thm:exact`, `cor:first-augmented` | [GeneralCorrelationValues.lean](CyclicBell/GeneralCorrelationValues.lean): `first_reduced_values_q_qa_qc`, `first_augmented_values_q_qa_qc`. Actual three-model suprema equal `2/sin(π/(2d))` and `2/sin(π/(2d))+1`. |
| Second-family literal coefficients and normalization | [GeneralSecondCoefficients.lean](CyclicBell/GeneralSecondCoefficients.lean): `generalLambda_literal`, `generalLambda_normalization`; includes signed exponential coefficients and Fourier compression. |
| Second-family SOS and bounds | [GeneralSecondBound.lean](CyclicBell/GeneralSecondBound.lean): `second_physical_upper`; [GeneralSecondCommuting.lean](CyclicBell/GeneralSecondCommuting.lean): `second_commuting_PVM_upper`. |
| `thm:second`: reduced and augmented values | [GeneralCorrelationValues.lean](CyclicBell/GeneralCorrelationValues.lean): `second_reduced_values_q_qa_qc`, `second_augmented_values_q_qa_qc`. Actual three-model suprema equal `d` and `d+1`. |
| Exact small-dimension value table | [GeneralExactValues.lean](CyclicBell/GeneralExactValues.lean): `small_dimension_exact_value_table`, `first_four_augmented_radical_values`. Literal radical values are derived from the trigonometric formula. |

## Physical maximizers, permutation blindness, and rigidity

| Manuscript claim | Source and scope |
| --- | --- |
| Weighted cycles and physical eigenbasis | [GeneralCycles.lean](CyclicBell/GeneralCycles.lean): `weighted_full_power`; [GeneralWitness.lean](CyclicBell/GeneralWitness.lean): actual maximally entangled state, rank-one projectors, encodings, and Born/Fourier formulas. |
| General weighted-cycle characteristic polynomial | [GeneralCycleCharpoly.lean](CyclicBell/GeneralCycleCharpoly.lean): `weighted_cycle_charpoly` gives `X^d−C(∏w)` for all nonzero complex weights; `phase_cycle_charpoly` covers product-one unit phases. |
| Canonical Fourier-flat order | [GeneralChirp.lean](CyclicBell/GeneralChirp.lean): the canonical physical target table is uniform. |
| Explicit swap and quantitative nonuniformity | [GeneralSwap.lean](CyclicBell/GeneralSwap.lean): `swapped_R2`, `all_dimension_physical_nonuniformity`; [GeneralGuessing.lean](CyclicBell/GeneralGuessing.lean): the quantitative guessing gap. |
| `thm:biased` and second-family counterexample | [GeneralFirstWitness.lean](CyclicBell/GeneralFirstWitness.lean): `first_all_dimension_counterexample`; [GeneralSecondWitness.lean](CyclicBell/GeneralSecondWitness.lean): `second_all_dimension_counterexample`. These construct states and PVMs, attain the bounds, and compare with arbitrary finite competitors. |
| Same maximizer in all three models | [GeneralModelCounterexamples.lean](CyclicBell/GeneralModelCounterexamples.lean): `first_three_model_counterexample`, `second_three_model_counterexample`; actual maximizing behaviors have uniform local marginals and a nonuniform joint target. |
| `thm:permutation`: conditional theorem | [GeneralPermutation.lean](CyclicBell/GeneralPermutation.lean): `conditional_permutation_theorem`. The scalar cap, phase alignment, and cyclic products remain explicit hypotheses. |
| Arbitrary-Hilbert conditional bound and first moments (generic two-Alice-input construction) | [GeneralCoveragePermutation.lean](CyclicBell/GeneralCoveragePermutation.lean): `linear_commuting_hilbert_bound`, `linear_augmented_commuting_hilbert_bound`, `linear_permutation_local_moments_zero`, `linear_permutation_all_harmonics_invariant`. |
| Conditional simple spectra and complete first-harmonic correlator package (two Alice inputs) | [GeneralCoverageWitness.lean](CyclicBell/GeneralCoverageWitness.lean): `conditional_permutation_simple_spectra`, `conditional_permutation_complete_harmonics`. Each root eigenspace is one-dimensional. |
| Behavior nonuniqueness; small-dimension orbit exception | [GeneralOrbitConsequences.lean](CyclicBell/GeneralOrbitConsequences.lean): `first_behavior_nonuniqueness`, `second_behavior_nonuniqueness`; the `d=2,3` flatness results apply to the specified phase-permutation orbit. |
| `thm:support-rigidity` | [GeneralRigidity.lean](CyclicBell/GeneralRigidity.lean): `supported_multiplicity_rigidity`, `supported_dimension_divisible`. Physical maximality implies invariance, adjacent-reflection relations, equal multiplicities, and divisibility on the actual reduced-state support. |
| Explicit four-dimensional calculations | [Endpoints.lean](CyclicBell/Endpoints.lean): the concrete matrices, target table, and physical trivial-Eve counterexamples; these supplement the all-dimensional proofs. |

## Explicit second-family completion clauses

These endpoints concern the actual `secondPermutationStrategy`, with every Alice input in `Ix d` and every Bob input in `Option (Ix d)`. They supplement the generic two-Alice-input permutation theorem above.

| Manuscript claim | Source and scope |
| --- | --- |
| `thm:second`: complete complex first-harmonic matrix and local moments | [GeneralSecondMoments.lean](CyclicBell/GeneralSecondMoments.lean): `secondPermutation_correlator`, `secondPermutation_extra_correlator`, `secondPermutation_complete_first_moments`, `secondPermutation_behavior_correlators_invariant`. For every `d≥2` and permutation, the actual Born correlators are `λ_l χ(-ly)` and `δ_(l,0)`, all Alice/Bob local first moments vanish, and the entire `d × (d+1)` first-harmonic array is permutation-independent. This does not assert invariance of all Fourier orders or the full probability table. |
| `thm:second`, `eq:second-sos`: every residual kills the state | [GeneralSecondResiduals.lean](CyclicBell/GeneralSecondResiduals.lean): `secondPermutation_residual_zero`, `secondPermutation_aligned_residual_zero`. The literal residual `d λ_l I − A_l ⊗ Bhat_l` and the extra aligned residual `I − A_0 ⊗ B_none` annihilate `Phi_d`. The proof uses compression and unitarity, without assuming scalar attainment or maximality. |
| `thm:second`: alternate Bob-adjoint convention | [GeneralOutcomeRelabeling.lean](CyclicBell/GeneralOutcomeRelabeling.lean): `negateMeasurement_encoded`, `secondAdjointPermutation_bob_encoded`, `secondAdjointPermutation_behavior`, `secondAdjointValue_negateBob`, `secondAdjointPermutation_maximal`. Inverting Bob outcomes sends each encoded observable to its adjoint and sends the actual behavior at `b` to the original behavior at `−b`. The **functional is transported too**, using adjointed Bob observables in both its Fourier and aligned terms. No invariance of the unchanged original functional is asserted. |
| Nonuniformity and guessing under that relabeling | Same file: `secondAdjointSwap_nonuniform`, `secondAdjointSwap_observedMaxEntry`, `secondAdjointSwap_quantitative`, `negateBob_bestFixedGuess`. For `d≥4` the swapped target remains nonuniform with the same observed maximum entry and quantitative gap. Generic fixed-guess transport refers to explicit trivial-Eve guesses; it does not identify the exact worst-case Eve optimum. |

[GeneralSecondCompletionStatements.lean](CyclicBell/GeneralSecondCompletionStatements.lean) exposes expanded Born sums, local density traces, the literal residual, and the transported functional at the checking interfaces.

## Literal source strategy and polar conventions

These statements use the source positive clock `Z`, forward shift `X`, and displayed cosecant coefficients. They identify the literal strategy, beyond establishing the existence of some maximizer with the same Bell value.

| Manuscript claim | Source and entry points |
| --- | --- |
| `eq:source-fourier`, coefficient DFT, qutrit expression | [GeneralSourceFourier.lean](CyclicBell/GeneralSourceFourier.lean): `source_coefficient_DFT`, `source_fourier_zero`, `source_fourier_one`, `source_qutrit_operator`. |
| Literal coefficient polynomial and its polar interpolation | [GeneralCoverageSourceWeyl.lean](CyclicBell/GeneralCoverageSourceWeyl.lean), [GeneralCoverageSourceLiteralInterpolation.lean](CyclicBell/GeneralCoverageSourceLiteralInterpolation.lean), [GeneralCoverageSourceFactors.lean](CyclicBell/GeneralCoverageSourceFactors.lean): `sourceBob_transpose_finiteCalc`, `sourceBob_unitary`. The wraparound term and phase signs are proved for all `d≥2`. |
| Actual positive modulus and inverse | [GeneralCoverageSourceCanonical.lean](CyclicBell/GeneralCoverageSourceCanonical.lean): `sourceModulus_eq_canonical`, `sourceModulus_eq_relative_modulus`, `sourceModulus_inverse`, `sourceBob_transpose_inverse_formula`, `sourceBob_canonical_polar`. Both moduli use actual positive square roots. |
| Order and valid outcome measurements | [GeneralCoverageSourceOrder.lean](CyclicBell/GeneralCoverageSourceOrder.lean): `sourceBob_order`; [GeneralCoverageSpectralMeasurement.lean](CyclicBell/GeneralCoverageSpectralMeasurement.lean): `finiteOrderMeasurement`, `finiteOrderMeasurement_encoding`. |
| Exact full simple spectra | [GeneralCoverageSourceSpectrum.lean](CyclicBell/GeneralCoverageSourceSpectrum.lean): `source_relative_full_simple_spectrum`, `sourceBob_full_simple_spectrum`. The spectrum is exactly the stated root set, with every eigenspace one-dimensional. |
| `app:attainment`: physical source strategy | [GeneralCoverageSourceStrategy.lean](CyclicBell/GeneralCoverageSourceStrategy.lean): `sourcePhysicalStrategy`, `sourcePhysicalStrategy_encodings`, `sourcePhysicalStrategy_attains`. The source `Z/X` Alice, literal Bob matrices, extra `Z†` Bob, and normalized positive maximally entangled state attain the augmented value. |

## Adversarial quantities and binary privacy

| Manuscript claim | Source and scope |
| --- | --- |
| Actual finite adversarial model | [GeneralTripartite.lean](CyclicBell/GeneralTripartite.lean): `TripartiteOn`, `GuessPOVM`, `tripartiteBehavior_instrument`. Arbitrary finite ABE dimensions, mixed states, AB PVMs, and general Eve POVMs are included. |
| Actual commuting adversarial model | [GeneralCommutingGuessing.lean](CyclicBell/GeneralCommutingGuessing.lean): `CommutingEveOn`, `tripartiteToCommuting_behavior`; the finite embedding preserves the full extended behavior. |
| Value-conditioned guessing definitions and bounds | [GeneralAdversarialValues.lean](CyclicBell/GeneralAdversarialValues.lean): `GuessQ`, `GuessQa`, `GuessQc`, `GvalQ`, `GvalQa`, `GvalQc`, `first_value_conditioned_guessing_bounds`, `second_value_conditioned_guessing_bounds`. Closure precedes the equality slice. Quantitative lower bounds and the upper bound one are proved for `d≥4`. |
| Physical Eve witnesses, privacy criterion, and robustness obstruction | [GeneralOperational.lean](CyclicBell/GeneralOperational.lean) and [GeneralConsequences.lean](CyclicBell/GeneralConsequences.lean): actual fixed-guess instruments; `physical_private_iff_fourier`; `first_no_value_only_endpoint_robustness`, `second_no_value_only_endpoint_robustness`. Exact maximizing counterexamples rule out the stated vanishing deficit-only correction. |
| Four-dimensional entropy consequence | [GeneralConsequences.lean](CyclicBell/GeneralConsequences.lean): `d4_entropy_exact`, `d4_entropy_less_than_four`; [GeneralAdversarialEntropy.lean](CyclicBell/GeneralAdversarialEntropy.lean): `first_four_value_entropy_upper`, `second_four_value_entropy_upper`. The witness entropy is exact; the worst-case value-conditioned entropy statement is an upper bound. |
| Fixed-realization POVM maximum and nested optimization | [GeneralPOVMMaximum.lean](CyclicBell/GeneralPOVMMaximum.lean): `fixed_realization_guessing_maximum`; [GeneralNestedGuessing.lean](CyclicBell/GeneralNestedGuessing.lean): `first_GvalQ_nested`, `second_GvalQ_nested`. The inner finite-Eve maximum is attained; the outer value-conditioned optimization is a supremum. |
| One-input resource baseline, both orientations | [GeneralOneInput.lean](CyclicBell/GeneralOneInput.lean): `one_input_pure_projective_perfect_guess`; [GeneralPartySwap.lean](CyclicBell/GeneralPartySwap.lean): `right_one_input_pure_projective_perfect_guess`. Explicit local pure projective realizations permit perfect guessing. |
| Binary SOS, Hilbert bound, and three-model value | [GeneralBinaryModels.lean](CyclicBell/GeneralBinaryModels.lean): `binary_cstar_sos`, `binary_commuting_hilbert_upper`, `binary_values_q_qa_qc`. |
| Binary physical attainment and privacy | [GeneralBinaryWitness.lean](CyclicBell/GeneralBinaryWitness.lean): `binary_physical_attainment`; [GeneralBinaryCertification.lean](CyclicBell/GeneralBinaryCertification.lean): `binary_purified_saturation`, `binary_componentwise_minimality`. Privacy covers arbitrary compatible finite purifications and yields the actual conditional state `ρ_E/4`. |
| Sufficient private-MUB composition criterion | [GeneralOperational.lean](CyclicBell/GeneralOperational.lean): `privateMUB_composition`, with its stated conditional-state hypotheses. |

## Settings tables and exposure obstruction

| Manuscript claim | Source and scope |
| --- | --- |
| `eq:standard-tables`: physical tables and normalization | [GeneralPhaseTables.lean](CyclicBell/GeneralPhaseTables.lean): `phasePair_sine_formula`, `standard_behavior_formula`, `phasePair_nonnegative`, `phasePair_normalized`, `phasePair_marginals`. |
| Exact standard peaks and nonuniformity | [GeneralPhaseBounds.lean](CyclicBell/GeneralPhaseBounds.lean): `standard_tables_nonuniform`; bounds apply to every entry and include actual attaining pairs, for `d≥2`. |
| Added anchor and cross tables | [GeneralAnchoredTables.lean](CyclicBell/GeneralAnchoredTables.lean): `anchored_preserves_standard`, `anchored_matching`, `anchored_cross_formula`, `anchored_cross_nonuniform`; the cross nonuniformity result assumes `d≥3`. |
| Qubit exception | Same file: `anchored_qubit_cross_uniform`; every cross entry is exactly `1/4` when `d=2`. |
| Observed entropy and asymptotic | [GeneralPhaseEntropy.lean](CyclicBell/GeneralPhaseEntropy.lean): `standard_table_entropy_package`, `standard_entropy_exact`, `standard_entropy_asymptotic`. The asymptotic is expressed as a difference limit. |
| `prop:mub`: operator-space and coefficientwise spectral obstruction | [GeneralCoverageExposure.lean](CyclicBell/GeneralCoverageExposure.lean): `MUBSpace_representation`, `computational_MUB_spectral_obstruction`, `computational_PVM_coefficientwise_saturation`. |

The settings-table proofs describe the displayed physical implementations. Their observed entropy is distinct from entropy conditioned on an adversary. They do not depend on the Bell-bound or support-rigidity endpoints.

## Proof correspondence and limits

- **Statements versus proof steps.** This companion formalizes the mapped mathematical claims, using alternative proofs where indicated. It is not an exhaustive translation of every manuscript derivation. In particular, the computational-MUB obstruction uses a stronger constant-diagonal positivity argument instead of reproducing the Toeplitz/SVD calculation.
- **General polar decomposition.** The general polar identity assumes a supplied factor satisfying the defining factorization and initial-isometry equations. It derives the required square-root and commutation identities, including at kernels. Existence and uniqueness of arbitrary canonical polar decompositions and their strong-limit representations are not separately formalized. For the source attaining pencils, the factor and inverse are explicitly constructed.
- **Rigidity.** The result concerns the actual reduced-state support. It does not constrain an unused ambient complement, prove self-testing, or classify every maximizer.
- **Guessing optimization.** The counterexamples and quantitative bounds do not solve the unknown exact worst-case guessing optimum. Fixed-realization finite-Eve maxima are attained; no maximizing outer realization or arbitrary-infinite-Eve fixed-realization optimizer is asserted.
- **Binary privacy and conditional criteria.** Binary privacy has finite-purification scope. The private-MUB and phase-permutation results retain their stated hypotheses; they are not unconditional classification theorems.
- **External results and interpretation.** Cited self-testing theorems, isometry transport from those theorems, literature priority, and bibliographic claims are outside the formalization. The exposure obstruction concerns coefficientwise bounds, not all possible added measurements or joint Bell SOS constructions.

[AXIOMS.md](AXIOMS.md) explains the compiler, dependency, axiom, and regression checks. Inventory size and lexical scans alone are not proof evidence, and successful kernel checking alone does not settle manuscript correspondence.
