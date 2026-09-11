# Mathematical claims and formal declarations

This map describes the fixed complex-qubit model and named mathematical conclusions. The successful-run requirement and precise verification status are in [CERTIFICATION.md](../CERTIFICATION.md). The independent manuscript comparison is in [the final statement review](../local_verification/final_statement_review.md).

| Mathematical claim | Formal declaration | Source |
|---|---|---|
| Positive, normalized, nonsignaling Born behavior | `strategy_behavior_nonnegative`, `strategy_behavior_normalization`, `strategy_no_signaling_to_alice`, `strategy_no_signaling_to_bob` | [Expectation](../Bell/Expectation.lean) |
| Two inputs per party, arbitrary finite input-dependent outputs: equality of POVM and PVM convex hulls | `two_input_convex_equality`, `universal_two_input_equality` | [Assembly](../Bell/Assembly.lean) |
| One finite random variable selecting complete PVM strategies reproduces a whole POVM behavior | `finite_projective_simulation` | [SimulationCorollaries](../Bell/SimulationCorollaries.lean) |
| One-input equality, including empty-input and empty-output boundary cases | `one_input_equality` | [OneInput](../Bell/OneInput.lean) |
| Equality whenever each party has at most two inputs | `at_most_two_input_equality` | [Assembly](../Bell/Assembly.lean) |
| An actual 3×2 POVM witness attains `20√2 + 16/25` | `witness_mem_raw`, `witness_value` | [Witness](../Bell/Witness.lean) |
| Every projective behavior, and its shared-randomness hull, has score at most `289/10` | `projective_strategy_rational_upper`, `convex_projective_rational_upper` | [ProjectiveBound](../Bell/ProjectiveBound.lean) |
| The manuscript upper bound `20√2 + 3/5 + (4+3√2)/250` holds for every physical PVM strategy | `projective_global_upper_bound` | [ProjectiveBound](../Bell/ProjectiveBound.lean) |
| Exact positive witness-to-paper-bound gap `3(2−√2)/250` | `gap_identity`, `strict_gap` | [Scalars](../Bell/Scalars.lean) |
| Strict physical 3×2 separation | `three_by_two_separation` | [ProjectiveBound](../Bell/ProjectiveBound.lean) |
| Any strict separator requires at least (3,2) or (2,3); the threshold is attained | `minimum_inputs`, `minimum_inputs_attained` | [Assembly](../Bell/Assembly.lean) |
| Appendix B: a physical POVM strategy attains `(16+8√7813)/25` | `strengthened_attainment` | [StrengthenedWitness](../Bell/StrengthenedWitness.lean) |
| Unconditional main conjunction, including strengthened attainment | `main_claims`, `main_claims_with_strengthening` | [Assembly](../Bell/Assembly.lean) |

The complete proof route connects quantum compactness, finite convexity, extreme-measurement reductions, complex purification and steering, common-span filtering, finite cone circuits, physical incidence reconstruction, derivatives and stationarity, all rank branches, and an exact rational sum-of-squares projective certificate. These dependencies are proved within the imported production modules; none is supplied as a top-level mathematical oracle.

[Statements.lean](../validation/Statements.lean) and [PhysicalContracts.lean](../validation/PhysicalContracts.lean) independently elaborate 25 examples spelling out the model and endpoints. They check complete-strategy mixing, actual PSD matrices and Born probabilities, the finite alphabets, exact constants, and minimum-input quantifiers.

The conclusion concerns ordinary finite shared-randomness convexification. It is not a same-state simulation theorem or an equality of the unconvexified strategy ranges. The strengthened value is attained, with no assertion that it is the global POVM optimum. The formal proof uses an alternative, stronger projective certificate; it does not formalize every unused alternative proof or every prose statement in the manuscript.

The manuscript's dimensions-at-most-two and stochastic-output conventions are represented by the fixed two-dimensional ambient carrier and finite convexification. Explicit generic theorems parameterizing all smaller Hilbert spaces or all stochastic output channels are not separate endpoints of this development. The independent review explains the embedding and finite deterministic-map interpretation.
