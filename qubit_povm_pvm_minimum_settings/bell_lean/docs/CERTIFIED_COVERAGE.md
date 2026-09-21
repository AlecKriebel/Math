# Mathematical claims and formal declarations

This map identifies the current formal statements and their source models. The dated full-run receipt, compiler checks, and verification status are recorded in [CERTIFICATION.md](../CERTIFICATION.md); this map does not substitute for that receipt. [MODEL_CONVENTIONS.md](MODEL_CONVENTIONS.md) explains the source-to-source correspondences and their boundary cases. Names in the first table are in namespace `Bell`.

## Principal conclusions

| Mathematical claim | Formal declaration | Source |
|---|---|---|
| Positive, normalized, nonsignaling Born behavior | `strategy_behavior_nonnegative`, `strategy_behavior_normalization`, `strategy_no_signaling_to_alice`, `strategy_no_signaling_to_bob` | [Expectation](../Bell/Expectation.lean) |
| Two inputs per party and arbitrary finite input-dependent output counts: equality of POVM and PVM convex hulls | `two_input_convex_equality`, `universal_two_input_equality` | [Assembly](../Bell/Assembly.lean) |
| One finite random variable selecting complete PVM strategies reproduces the entire POVM behavior | `finite_projective_simulation` | [SimulationCorollaries](../Bell/SimulationCorollaries.lean) |
| One-input equality, including empty-input and empty-output boundary cases | `one_input_equality` | [OneInput](../Bell/OneInput.lean) |
| Equality whenever each party has at most two inputs | `at_most_two_input_equality` | [Assembly](../Bell/Assembly.lean) |
| An actual 3×2 POVM witness attains `20√2 + 16/25` | `witness_mem_raw`, `witness_value` | [Witness](../Bell/Witness.lean) |
| Every projective behavior and its shared-randomness hull have score at most `289/10` | `projective_strategy_rational_upper`, `convex_projective_rational_upper` | [ProjectiveBound](../Bell/ProjectiveBound.lean) |
| The manuscript upper bound `20√2 + 3/5 + (4+3√2)/250` holds for every physical PVM strategy | `projective_global_upper_bound` | [ProjectiveBound](../Bell/ProjectiveBound.lean) |
| Exact positive witness-to-paper-bound gap `3(2−√2)/250` | `gap_identity`, `strict_gap` | [Scalars](../Bell/Scalars.lean) |
| Strict physical 3×2 separation | `three_by_two_separation` | [ProjectiveBound](../Bell/ProjectiveBound.lean) |
| A strict separator requires at least (3,2) or (2,3), and the threshold is attained | `minimum_inputs`, `minimum_inputs_attained` | [Assembly](../Bell/Assembly.lean) |
| Appendix B: a physical POVM strategy attains `(16+8√7813)/25` | `strengthened_attainment` | [StrengthenedWitness](../Bell/StrengthenedWitness.lean) |
| Unconditional main conjunction, including strengthened attainment | `main_claims`, `main_claims_with_strengthening` | [Assembly](../Bell/Assembly.lean) |

The proof route connects quantum compactness, ordinary finite convexity, extreme-measurement reductions, complex purification and steering, common-span filtering, finite cone circuits, physical incidence reconstruction, derivatives and stationarity, all required rank branches, and an exact rational sum-of-squares projective certificate. These dependencies are proved in the imported production modules, rather than supplied as top-level mathematical oracles.

## Explicit model-convention correspondences

The finite-label, Hilbert-space, and stochastic extensions below are explicit Lean declarations. They replace the earlier interpretation-only treatment of these conventions.

| Claim and independent source model | Formal declarations | Source |
|---|---|---|
| Actual matrix-valued POVMs/PVMs on arbitrary finite outcome types correspond bijectively to cardinal-indexed measurements | `Bell.FiniteLabels.POVM.encoding`, `Bell.FiniteLabels.PVM.encoding` | [FiniteLabels](../Bell/FiniteLabels.lean) |
| Entire physical strategies and their complete real Born tables correspond under relabeling | `Bell.FiniteLabels.Strategy.encoding`, `Bell.FiniteLabels.ProjectiveStrategy.encoding`, `Bell.FiniteLabels.behaviorEquiv`, `Strategy.encode_behavior`, `ProjectiveStrategy.encode_behavior` in that namespace | [FiniteLabels](../Bell/FiniteLabels.lean) |
| Relabeling transports both raw ranges and ordinary convex hulls exactly; finite mixture weights are unchanged | `Bell.FiniteLabels.rawPOVM_transport`, `rawPVM_transport`, `convexPOVM_transport`, `convexPVM_transport`, `finite_mixture_transport` | [FiniteLabels](../Bell/FiniteLabels.lean) |
| Two-input and at-most-two-input equality for arbitrary finite, input-dependent outcome types | `Bell.FiniteLabels.two_input_equality`, `Bell.FiniteLabels.at_most_two_input_equality` | [FiniteLabels](../Bell/FiniteLabels.lean) |
| Stochastic channels are finite convex combinations of complete deterministic functions, including feasible empty cases | `Bell.StochasticChannel.decomposition`, `Bell.StochasticFamily.weight_normalized`, `Bell.StochasticFamily.reconstruction` | [StochasticProcessing](../Bell/StochasticProcessing.lean) |
| One selector fixes both parties' output choices at every input and source label; stochastic processing preserves the PVM hull | `Bell.StochasticProcessing.behavior_decomposition`, `deterministic_branch_mem_rawPVM`, `mem_convexPVM` | [StochasticProcessing](../Bell/StochasticProcessing.lean) |
| The same stochastic closure holds for independently defined weighted sums on arbitrary finite source/target labels | `Bell.FiniteLabels.StochasticProcessing.encode_behavior`, `behavior_decomposition`, `deterministic_branch_mem_rawPVM`, `mem_convexPVM` | [FiniteStochastic](../Bell/FiniteStochastic.lean) |
| Source tensor inner products are basis independent and source operator positivity has the required matrix representation | `Bell.Hilbert.tensorInner_tmul`, `tensorInner_basis_independent`, `basisMatrix_positive_iff`, `operatorMatrix_positive` | [HilbertCoordinates](../Bell/HilbertCoordinates.lean) |
| Every finite-dimensional complex Hilbert space of dimension at most two has an actual linear isometry into complex C² | `Bell.Hilbert.linearIsometry`, `linearIsometry_inner`, `linearIsometry_norm`, `linearIsometry_injective` | [HilbertIsometry](../Bell/HilbertIsometry.lean) |
| Isometric embedding plus allocation of the unused orthogonal complement gives normalized POVMs/PVMs and preserves the joint Born trace | `Bell.IsometricCompression.paddedEffect_sum`, `paddedEffect_idempotent`, `paddedEffect_orthogonal`, `compress_paddedEffect`, `born_padded` | [IsometricCompression](../Bell/IsometricCompression.lean) |
| Independent source endomorphism strategies on E⊗F, with local dimensions at most two, become actual qubit strategies with exactly the same behavior | `Bell.Hilbert.born_coordinates`, `Bell.Hilbert.Strategy.toQubit_behavior`, `Bell.Hilbert.ProjectiveStrategy.toQubit_behavior` | [HilbertCorrespondence](../Bell/HilbertCorrespondence.lean) |
| Every qubit matrix strategy is also a source-Hilbert strategy on C²⊗C² | `Bell.Hilbert.ofQubitStrategy_behavior`, `Bell.Hilbert.ofQubitProjectiveStrategy_behavior` | [HilbertReverse](../Bell/HilbertReverse.lean) |
| The union over allowed local Hilbert spaces has exactly the matrix-model raw ranges and ordinary hulls; its two-input equality and finite simulation follow | `Bell.Hilbert.rawPOVM_eq_matrix`, `rawPVM_eq_matrix`, `convexPOVM_eq_matrix`, `convexPVM_eq_matrix`, `two_input_convex_equality`, `Bell.Hilbert.Strategy.finite_projective_simulation` | [HilbertSimulation](../Bell/HilbertSimulation.lean) |
| Hilbert-space and arbitrary finite-outcome conventions are removed simultaneously from one independent physical source model | `Bell.HilbertFiniteLabels.Strategy.toQubit_behavior`, `Bell.HilbertFiniteLabels.ProjectiveStrategy.toQubit_behavior`, `ofQubitStrategy_behavior`, `ofQubitProjectiveStrategy_behavior` in that namespace | [HilbertFiniteLabels](../Bell/HilbertFiniteLabels.lean) |
| The dimension-at-most-two Hilbert union with arbitrary outcome types has exactly the fixed-qubit finite-label raw ranges and hulls, and satisfies the principal at-most-two-input equality | `Bell.HilbertFiniteLabels.rawPOVM_eq_fixed`, `rawPVM_eq_fixed`, `convexPOVM_eq_fixed`, `convexPVM_eq_fixed`, `at_most_two_input_equality` | [HilbertFiniteLabels](../Bell/HilbertFiniteLabels.lean) |
| A source-Hilbert strategy with arbitrary finite outcome labels and at most two inputs per party has one finite mixture of complete labeled projective strategies, including actual Hilbert-space branches on C² | `Bell.HilbertFiniteLabels.Strategy.two_input_simulable`, `Bell.HilbertFiniteLabels.finite_projective_simulation`, `Bell.HilbertFiniteLabels.finite_source_projective_simulation` | [HilbertFiniteLabels](../Bell/HilbertFiniteLabels.lean) |

Where a table cell starts with a fully qualified namespace, subsequent short names in that cell share that namespace unless a different qualification is displayed. For the Hilbert raw-set equality, the quantifier ranges over allowed local spaces; it is not raw equality for a fixed one-dimensional carrier. For outcome labels, inputs remain `Fin m` and `Fin n`, while outcome types may vary arbitrarily with the input.

## Boundary cases and validation

No extra nonempty-output assumption is introduced in the strategy correspondence endpoints. A normalized source state excludes zero-dimensional local spaces (`Bell.Hilbert.State.alice_finrank_pos`, `bob_finrank_pos`). On the resulting nontrivial local spaces, measurement normalization supplies an existing label for complement allocation (`Bell.Hilbert.Strategy.aliceSelected`, `bobSelected`). Thus an empty declared outcome alphabet at an existing input makes the physical strategy class empty. An absent input imposes no measurement obligation. `Bell.FiniteLabels.empty_hulls_of_no_strategy` and `no_input_strategy` record the corresponding finite-label cases.

Stochastic row normalization permits an empty target precisely when there are no source rows: `Bell.StochasticChannel.nonempty_iff`, `exists_of_empty_source`, and `no_channel_to_empty`. Zero-probability selector branches have zero weight. General stochastic processing is claimed to preserve `convexPVM`, not `rawPVM`.

The [validation directory](../validation/) contains anonymous statement contracts. [Statements](../validation/Statements.lean) and [PhysicalContracts](../validation/PhysicalContracts.lean) expose the original physical endpoints; [FiniteLabelContracts](../validation/FiniteLabelContracts.lean), [StochasticContracts](../validation/StochasticContracts.lean), [FiniteStochasticContracts](../validation/FiniteStochasticContracts.lean), [HilbertContracts](../validation/HilbertContracts.lean), and [HilbertFiniteLabelContracts](../validation/HilbertFiniteLabelContracts.lean) check the additional source types, correspondence formulas, and degenerate cases. The full-run receipt records the exact files and counts actually executed.

The conclusions concern ordinary finite shared-randomness convexification. They are not same-state simulation theorems or an assertion that raw POVM and PVM ranges coincide. The strengthened value is attained without a global-optimality assertion. The formal projective proof uses an alternative stronger certificate and does not formalize every unused proof or prose statement in the manuscript.

## Auxiliary mathematics outside the certified scope

The September 11 referee review identified the following auxiliary coverage limits, retained after the model-convention extensions. The development does not claim to formalize every mathematical statement in the manuscript.

- General finite-POVM SDP dual attainment, complementary slackness, and the full determinant-pullback/KKT package are replaced by the physical deterministic-replacement route needed for multiplier positivity.
- The full smooth 14-dimensional incidence-manifold statement and full inverse-metric Hessian formula with inertia `(4,12)` are not formal endpoints; surjectivity, differentiable feasible curves, and the exact score-gap argument supply the required rank closure.
- The arbitrary pointed-cone circuit lemma, general mixed-state common-span statement, and arbitrary extremal-POVM rank-square inequality are implemented only through the specializations needed for the qubit reduction.
- The original physical-to-scalar projective-bound derivation is replaced by the stronger physical SOS bound.
- The ideal auxiliary PVM discrimination bound `3/5`, Appendix B's particular dual slacks, differentiation and unique-critical-point assertions, and some individual spectral/coordinate identities are not all separately formalized.

These are coverage limits, not findings that those auxiliary statements are false. See the [complete referee coverage matrix](../../referee_2026-09-11/reviews/coverage.md) and [response](../../referee_response_20260911/RESPONSE.md). The corrected paper explicitly retains Lorentz signature in its strict residual domain; scalar pairwise positivity alone is insufficient.
