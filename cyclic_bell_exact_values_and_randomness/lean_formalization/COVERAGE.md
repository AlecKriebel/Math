# Manuscript correspondence and formalization scope

Canonical source: `../main.tex`, merged v1.1.0, Git blob
`bbd0667c934d5a34dd9c8ced50df91515cb1308c`, SHA-256
`82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71`.
The original downloaded handoff was uncompiled and has been preserved. This
map describes the repaired statements; it is not itself a compiler receipt.
See `logs/latest_run.json` for the frozen clean build, controls and complete
axiom audit, and `repair_audit_2026-09-14/` for independent semantic reviews.

Every original named theorem is retained. Repairs correct elaboration, imports,
coercions and proof steps; they do not replace arbitrary physical strategies
with the explicit witness or introduce assumed Bell maxima. New `GeneralCoverage*`
modules fill the mathematical correspondence gaps identified during review.

## Claim-to-source map

Except the retained d=4 namespace, names below have prefix `CyclicBell.General.`.
Every listed source module is in the standard `lake build` import graph.

| Manuscript label or location | Written source scope | Module and selected theorems |
|---|---|---|
| `eq:Id; cor:first-augmented` | First augmented upper bound, any finite local dimensions and any positive trace-one mixed state | [GeneralFirstBound.lean](CyclicBell/GeneralFirstBound.lean) — `first_physical_upper` |
| `lem:scalar` | Roots-of-unity maximum and exact equality phases in every d>=2 | [GeneralScalar.lean](CyclicBell/GeneralScalar.lean) — `scalar_bound`, `scalar_equality_iff` |
| `eq:weighted-cycle` | Arbitrary weighted cycle d-th power; unit-phase physical spectral construction | [GeneralCycles.lean](CyclicBell/GeneralCycles.lean) — `weighted_full_power` |
| `eq:q-sequence; eq:target-table` | Actual maximally entangled state, rank-one projectors, encoding and Born/Fourier bridge | [GeneralWitness.lean](CyclicBell/GeneralWitness.lean) |
| `sec:biased canonical calculation` | Fourier flatness and uniform physical target for canonical order | [GeneralChirp.lean](CyclicBell/GeneralChirp.lean) |
| `eq:R2; eq:guessing-gap` | Literal final-two swap; exact lag-two autocorrelation, nonuniformity and quantitative guessing gap | [GeneralSwap.lean](CyclicBell/GeneralSwap.lean) — `swapped_R2`, `all_dimension_physical_nonuniformity` |
| `thm:biased` | Full first-family physical counterexample for every d>=4, with comparison to arbitrary finite competitors | [GeneralFirstWitness.lean](CyclicBell/GeneralFirstWitness.lean) — `first_all_dimension_counterexample` |
| `eq:lambda; lem:lambda-normalization` | Actual signed/exponential source coefficients, Fourier compression and normalization | [GeneralSecondCoefficients.lean](CyclicBell/GeneralSecondCoefficients.lean) — `generalLambda_literal`, `generalLambda_normalization` |
| `eq:second-sos` | General second-family SOS and arbitrary-dimensional mixed-state upper bound | [GeneralSecondBound.lean](CyclicBell/GeneralSecondBound.lean) — `second_physical_upper` |
| `thm:second` | Full second-family strategy, attainment d+1, shared target and nonuniform counterexample for d>=4 | [GeneralSecondWitness.lean](CyclicBell/GeneralSecondWitness.lean) — `second_all_dimension_counterexample` |
| `thm:permutation` | Polar-linear conditional theorem with the manuscript phase/product and scalar-cap hypotheses | [GeneralPermutation.lean](CyclicBell/GeneralPermutation.lean) — `conditional_permutation_theorem` |
| `thm:support-rigidity` | Physical maximality to actual Alice support, invariance, kernel-safe cancellation, adjacent reflections, equal eigenspace multiplicities and divisibility | [GeneralRigidity.lean](CyclicBell/GeneralRigidity.lean) — `supported_multiplicity_rigidity`, `supported_dimension_divisible` |
| `thm:exact operator-inequality part` | Arbitrary complete complex Hilbert-space first-family upper bound, separately proved without finite dimension | [GeneralCommuting.lean](CyclicBell/GeneralCommuting.lean) — `first_commuting_hilbert_bound`, `first_augmented_commuting_hilbert_bound` |
| `thm:exact; eq:second-sos commuting reading` | Actual arbitrary-Hilbert PVM encodings and first/second augmented operator upper bounds | [GeneralSecondCommuting.lean](CyclicBell/GeneralSecondCommuting.lean) — `first_commuting_PVM_upper`, `second_commuting_PVM_upper` |
| `sec:randomness; eq:value-conditioned witness direction` | Explicit one-dimensional Eve instrument and fixed-guess success above uniform for both families | [GeneralConsequences.lean](CyclicBell/GeneralConsequences.lean) — `second_all_dimension_physical_Eve_gap` |
| `cor:behavior-nonunique` | Explicit canonical and swapped maximizers inequivalent under target output relabelings | [GeneralOrbitConsequences.lean](CyclicBell/GeneralOrbitConsequences.lean) — `first_behavior_nonuniqueness`, `second_behavior_nonuniqueness` |
| `sec:biased d=2,3 paragraph` | All phase orderings in the particular permutation orbit are Fourier flat for d=2,3 | [GeneralOrbitConsequences.lean](CyclicBell/GeneralOrbitConsequences.lean) |
| `No value-only endpoint robustness corollary` | Actual exact maximizing physical witness contradicts a vanishing deficit-only guessing correction | [GeneralConsequences.lean](CyclicBell/GeneralConsequences.lean) — `first_no_value_only_endpoint_robustness`, `second_no_value_only_endpoint_robustness` |
| `eq:d4-entropy` | Exact d=4 entropy 5-log(3)/log(2), below four | [GeneralConsequences.lean](CyclicBell/GeneralConsequences.lean) — `d4_entropy_exact`, `d4_entropy_less_than_four` |
| `prop:one-input` | First-party one-input nonsignalling behavior has explicit local and pure projective perfectly guessable realization | [GeneralOneInput.lean](CyclicBell/GeneralOneInput.lean) — `one_input_pure_projective_perfect_guess` |
| `thm:binary-benchmark finite-dimensional part` | Binary operator SOS, saturation to operator-valued privacy for arbitrary finite purifying Eve; actual guessing success | [GeneralBinary.lean](CyclicBell/GeneralBinary.lean) — `binary_saturation_privacy` |
| `app:binary attainment` | Literal binary source observables, projectors and Phi2 attained value 3 sqrt(3) | [GeneralBinaryWitness.lean](CyclicBell/GeneralBinaryWitness.lean) — `binary_physical_attainment`, `binary_physical_measurement_package` |
| `lem:private-mub` | Actual post-measurement conditional states satisfy the sufficient private-MUB composition criterion | [GeneralOperational.lean](CyclicBell/GeneralOperational.lean) — `privateMUB_composition` |
| `sec:settings operator-valued Fourier criterion` | Physical conditional instrument privacy iff all nontrivial operator-valued Fourier coefficients vanish | [GeneralConsequences.lean](CyclicBell/GeneralConsequences.lean) — `physical_private_iff_fourier` |
| `prop:mub` | Source computational-MUB coefficientwise spectral exposure obstruction, via a stronger constant-diagonal positivity proof | [GeneralExposure.lean](CyclicBell/GeneralExposure.lean) — `source_computational_MUB_exposure` |
| `app:d4; eq:d4-table` | All earlier d=4 milestones A-F and physical trivial-Eve counterexamples retained | [Endpoints.lean](CyclicBell/Endpoints.lean) |

The separate `GeneralGuessing.lean` module gives the manuscript's quantitative
bound, and `first_all_dimension_physical_Eve_gap` in `GeneralOperational.lean` handles the first-family physical Eve
instrument. `GeneralConsequences.binary_private_guess_success` converts binary
operator privacy to every complete guessing POVM's success 1/4.

## Correlation models, binary benchmark and algebraic appendices

| Manuscript claim | New source endpoint and actual scope |
|---|---|
| `sec:framework` definitions of Q_q/Q_qa/Q_qc | `GeneralCorrelationValues.lean`: `Qq`, `Qqa`, `Qqc` are actual real behavior sets. Qq uses arbitrary finite local types and mixed states; Qqa is the product-topology closure; Qqc uses complete complex Hilbert spaces and commuting PVMs. |
| Finite tensor-to-commuting inclusion | `GeneralHilbertBridge.lean`: `finiteToCommuting`, `finiteToCommuting_behavior`; `Qq_subset_Qqc` constructs normalization, projectors, cross-party commutation and the entire Born behavior, not merely the Bell value. |
| `thm:exact` complete reduced value | `first_reduced_values_q_qa_qc`: actual three-model real suprema equal `2 / sin(pi/(2*d))` for every d>=2. |
| `cor:first-augmented` complete value | `first_augmented_values_q_qa_qc`: actual three-model suprema equal `2 / sin(pi/(2*d)) + 1`. |
| `eq:second-sos` reduced value | `second_reduced_values_q_qa_qc`: actual three-model suprema equal d. |
| `thm:second` augmented value | `second_augmented_values_q_qa_qc`: actual three-model suprema equal d+1. |
| `sec:randomness` common maximizing witness | `first_three_model_counterexample`, `second_three_model_counterexample`: one valid finite strategy belongs to all three models, has value equal to all three literal suprema, uniform local marginals and a nonuniform target table. |
| Same witness, actual trivial Eve | `first_three_model_physical_guessing_gap`, `second_three_model_physical_guessing_gap`: fixed-guess success of the existing actual finite instrument exceeds 1/d^2. No adversarial optimizer is asserted. |
| `thm:binary-benchmark` arbitrary-Hilbert upper bound | `GeneralBinaryModels.lean`: `binary_cstar_sos`, `binary_commuting_hilbert_upper` separately handle complete complex Hilbert spaces, without finite dimension or same-party commutation. |
| `thm:binary-benchmark` complete value | `binary_values_q_qa_qc`: actual binary PVM behavior-model suprema all equal 3 sqrt(3). |
| `thm:binary-benchmark` physical purification/privacy | `GeneralBinaryCertification.lean`: `binary_purified_saturation` starts with arbitrary finite local and Eve dimensions, actual PVMs and the actual Bell score. Its conclusion is the post-measurement conditional matrix `rho_E/4` for every target outcome. |
| `prop:one-input`, opposite party orientation | `GeneralPartySwap.lean`: `right_one_input_pure_projective_perfect_guess` explicitly constructs Alice input-dependent PVMs, Bob's one-input PVM, the stored pure state and Eve's perfect-guess effects. |
| `cor:binary-minimality` | `binary_componentwise_minimality`: a physically attainable two-input-per-party behavior is private against all finite compatible purifications; every left/right one-input binary nonsignalling behavior has a perfectly guessable compatible purification and cannot satisfy that privacy property. |
| `tab:exact-values`, d=2,3,4,5,6 | `GeneralExactValues.lean`: `small_dimension_exact_value_table` proves the five literal radical values from the trigonometric definition; `first_four_augmented_radical_values` instantiates all three model suprema. |
| Characteristic polynomial following `eq:weighted-cycle` | `GeneralCycleCharpoly.lean`: `weighted_cycle_charpoly` proves `X^d - C(product w)` for every nonzero complex weight tuple. Nonunit weights and non-product-one tuples are included. `phase_cycle_charpoly` specializes to the physical unit-phase case. |

## Adversarial quantities and source Fourier conventions

| Manuscript claim | New source endpoint and scope |
|---|---|
| `sec:framework`, actual finite adversarial model | `GeneralTripartite.lean`: `TripartiteOn`, `GuessPOVM`, `tripartiteBehavior_instrument`. Arbitrary finite local dimensions, mixed state, AB PVMs, general Eve POVM; actual sandwich/partial trace. |
| Actual three-party commuting model | `GeneralCommutingGuessing.lean`: `CommutingEveOn`, `tripartiteToCommuting_behavior`. Arbitrary complete Hilbert space; all cross-party commutations; full finite extended-behavior embedding. |
| `eq:gval-model` | `GeneralAdversarialValues.lean`: `GuessQ`, `GuessQa`, `GuessQc`, `GvalQ`, `GvalQa`, `GvalQc`. The approximate domain is closure of FULL extended correlations before the score-equality slice. |
| `eq:value-conditioned` | `first_value_conditioned_guessing_bounds`, `second_value_conditioned_guessing_bounds`: the literal quantitative lower bound and upper bound one in every model, for all d>=4. |
| `eq:d4-entropy` | `GeneralAdversarialEntropy.lean`: `first_four_Gval_three32`, `second_four_Gval_three32`, `first_four_value_entropy_upper`, `second_four_value_entropy_upper`. These are bounds, not an exact worst-case optimum. |
| Fixed-realization definition of G | `GeneralPOVMMaximum.lean`: `finitePOVM_maximum_exists`, `finitePOVMValue_attained`, `fixed_realization_guessing_maximum`. Arbitrary finite Eve dimension; complete general POVMs parameterized by Gram factors. |
| Nested optimization bridge | `GeneralNestedGuessing.lean`: `first_GvalQ_nested`, `second_GvalQ_nested`. Actual finite-q outer suprema of fixed-realization attained maxima equal the flattened definitions. Physical saturators discharge nonemptiness. |
| `eq:source-fourier` | `GeneralSourceFourier.lean`: `source_coefficient_DFT`, `source_fourier_zero`, `source_fourier_one`. Actual integer triangular exponent, positive clock, forward shift and source normalization. |
| `app:attainment` qutrit formula | `source_qutrit_operator`. This is the explicit coefficient/matrix identity, not a complete source-polar strategy identification. |

## Settings appendix

| Manuscript claim | New source endpoint and scope |
|---|---|
| `eq:standard-tables` | `phasePair_sine_formula`, `standard_behavior_formula`: explicit phase PVMs and actual Phi_d trace Born probabilities; signed ordinary lifts and nonzero sine denominators are proved. |
| Standard table physical validity | `phasePair_nonnegative`, `phasePair_normalized`, `phasePair_marginals`: valid PVMs, normalized probabilities and both uniform local marginals, independently of the claimed joint table. |
| `app:settings` standard maximum/nonuniformity | `standard_tables_nonuniform`: upper bound for every entry, actual attaining pair, peak strictly greater than 1/d^2 for d>=2, and nonuniformity. |
| `app:settings` perfect anchor | `anchored_preserves_standard`, `anchored_matching`: actual third Bob measurement, unchanged old tables, same-label matching. |
| Anchor cross table | `anchored_cross_formula`, `anchored_cross_nonuniform`: physical numerator-one table, attained maximum and strict nonuniformity for d>=3. |
| Qubit exception | `anchored_qubit_cross_uniform`: each d=2 cross entry is exactly 1/4. |
| Observed entropy/asymptotic | `standard_table_entropy_package`, `standard_entropy_exact`, `standard_entropy_asymptotic`: actual attained peak, logarithmic formula, and difference-limit o(1) claim. Not adversarial conditional entropy. |

These modules do not depend on the scalar extremum or Bell/rigidity endpoints.
They realize the displayed source tables, not the external cited self-testing
theorem itself or a formal isometry transport to every convention in that paper.

## Additional coverage supplied during local repair

Names in this section use `CyclicBell.General.`; generic analytic helpers also
use its `Coverage` namespace.

| Manuscript claim | Repaired correspondence |
|---|---|
| `lem:polar` | `GeneralCoveragePolarCanonical`: `canonical_polar_hilbert_positive_factor_identity` proves the actual nested-positive-square-root identity on arbitrary complete Hilbert spaces, including singular C. Given a polar factor, it uses the defining factorization and initial-isometry equations. |
| `thm:permutation`, arbitrary-Hilbert bound | `GeneralCoveragePermutation`: `linear_commuting_hilbert_bound`, `linear_augmented_commuting_hilbert_bound`; scalar cap is the explicit conditional hypothesis in the paper. |
| `thm:permutation`, full spectrum and moments | `GeneralCoverageWitness`: `conditional_permutation_simple_spectra` proves every root eigenspace has dimension one; `conditional_permutation_complete_harmonics` covers all local/first-harmonic moments. |
| `prop:mub`, literal operator system and eigenvalue obstruction | `GeneralCoverageExposure`: `MUBSpace_representation`, `computational_MUB_spectral_obstruction`, `computational_PVM_coefficientwise_saturation`; the matrices are exactly the Fourier/circulant operator system and the conclusion concerns real eigenvalues and physical Phi expectation. |
| `app:attainment`, literal source coefficients and polar factor | `GeneralCoverageSourceLiteralInterpolation`, `GeneralCoverageSourceWeyl`, `GeneralCoverageSourceFactors`, `GeneralCoverageSourceCanonical`: actual cosecant coefficient polynomial equals the polar function on the actual relative-unitary spectrum; source Bob is unitary and gives the canonical positive-modulus factorization. The modulus inverse is constructed and verified. |
| `app:attainment`, source Bob order and measurement validity | `GeneralCoverageSourceOrbit`, `GeneralCoverageTwistedPower`, `GeneralCoverageSourceOrder`, `GeneralCoverageSpectralMeasurement`: noncommutative ordered products prove `sourceBob_order`; finite spectral calculus constructs actual PVMs and proves their exact encoding. |
| `app:attainment`, full simple source spectra | `GeneralCoverageSourceSpectrum`: `source_relative_eigenspace_finrank`, `source_relative_charpoly`, `sourceBob_eigenspace_finrank`. A concrete unitary eigenbasis puts the literal Bob transpose into a unit-phase product-one weighted-cycle form. |
| `app:attainment`, actual canonical source attainment | `GeneralCoverageSourceStrategy`: `sourcePhysicalStrategy`, `sourcePhysicalStrategy_encodings`, `sourcePhysicalStrategy_attains`. The normalized positive Phi state, source Z/X Alice, literal source Bob matrices, and extra Z-adjoint Bob attain the actual first value `2/sin(pi/(2*d))+1`. |
| `sec:framework`, Qqa inclusion in Qqc | `GeneralCoverageClosureContainment`: `Qqc_isSeqClosed`, `Qqc_isClosed`, `Qqa_subset_Qqc`, `quantum_model_inclusions`. Closedness/inclusion is for finite input alphabets, including every scenario in the paper. |

The closure proof constructs an actual complete Hilbert space and commuting
PVMs. `GeneralCoverageUltralimit` gives bounded scalar limits along one common
ultrafilter; `GeneralCoverageMomentModel` derives a positive word kernel and all
PVM/cross-party relations from actual varying-Hilbert realizations.
`GeneralCoverageGNS` realizes that kernel in the completion of its possibly
degenerate coefficient space. `GeneralCoverageCompletionOperators` and
`GeneralCoverageReconstruction` extend contractive word actions and recover
all limiting behavior coordinates. No closedness, limiting strategy or
universal embedding is assumed. The original value proofs remain independent
of this additional background theorem.

## Reading the quantified claims correctly

- The first/second counterexamples include actual states, complete PVMs and Born
  probabilities, and compare against arbitrary competitors. Their biased target
  tables give lower bounds on adversarial guessing, not an exact optimal adversary.
- Supported rigidity concerns the range of the actual reduced state and derives
  the invariance and reflection relations. It makes no claim on an unused
  ambient complement and does not assert self-testing or a complete classification.
- Qqa is the topological closure of the actual finite behavior set. The
  adversarial approximate model takes closure of full extended behaviors before
  imposing the exact Bell-score slice. It is not closure of that slice.
- Finite-Eve fixed-realization POVM maxima are genuinely attained. The outer
  value-conditioned quantity is a supremum; a maximizing global realization or
  arbitrary-infinite-Eve fixed-realization maximum is not asserted.
- Binary privacy is quantified over compatible finite purifications and complete
  Eve guessing POVMs. It is not restricted to a selected adversary.
- The conditional permutation and private-MUB criteria retain their stated
  hypotheses. Settings-table entropy is observed entropy, separately from
  adversarial conditional entropy.

## Proof correspondence and external boundaries

This is a formalization of the paper's mathematical claims, not a literal
translation of every prose proof step. In particular, the computational-MUB
obstruction uses a stronger constant-diagonal positivity argument instead of
reproducing its Toeplitz-block/SVD calculation. The general polar identity uses
C*-algebraic square-root identities instead of a strong-limit/von Neumann
algebra construction. It assumes the supplied polar decomposition's defining
properties; existence/uniqueness of arbitrary polar decompositions and their
strong-limit representations are not separately formalized here. The source
attaining pencil's factor and inverse are explicitly constructed.

External cited self-testing results, literature priority, bibliography, open
classification questions and unknown optimal guessing values are not theorem
claims of this companion. The standard probability/anchor tables and entropy
asymptotic are proved directly for the displayed physical implementations;
there is no formal isometry transport of an external self-testing theorem.

The complete declaration list is generated in `reference/source_inventory.json`
and every name is queried in `CyclicBell/AxiomAudit.lean`. Inventory counts and
lexical checks alone are not proof evidence. The final actual axiom receipt
allows only `propext`, `Classical.choice`, and `Quot.sound` and rejects missing
queries, admissions, custom axioms and native proof-evaluation trust.
