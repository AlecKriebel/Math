# Manuscript coverage — settings appendix and audit continuation

**Every result below is an UNCOMPILED proof-script candidate. There are zero
kernel-verified endpoints in this delivery.** “End-to-end candidate” describes
its written hypotheses and source dependency chain, not successful elaboration.
No result here has an executed axiom report. Offline repairs may be substantive.

Canonical manuscript: `cyclic_bell_exact_values_and_randomness/main.tex`,
Git blob `bbd0667c934d5a34dd9c8ced50df91515cb1308c`.
The source correspondence is by TeX labels, not PDF page numbering.

## Claim-to-source map

Except the retained d=4 namespace, names below have prefix `CyclicBell.General.`.
Every listed source module is in the standard `lake build` import graph.

| Manuscript label or location | Written source scope | Module and selected theorem candidates |
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

## What the strongest core candidates actually assume

`first_all_dimension_counterexample` and `second_all_dimension_counterexample`
construct complete state/PVM tuples, evaluate the actual functionals, compare
against arbitrary finite local dimensions, and prove a biased designated Born
table. They do not assume maximality or replace arbitrary competitors by the
explicit witness. There is no claim of a worst possible Eve realization.

`supported_multiplicity_rigidity` assumes an arbitrary positive trace-one mixed
state and d-outcome projective measurements attaining the actual first augmented
value. Its conclusion uses the range of the actual reduced state. Its source
chain includes purification/support cancellation, invariance, finite-spectrum
zero transfer, polar kernel handling, deriving Bob/reflection power identities,
and the rank argument. The reflection hypotheses are not caller assumptions.
The theorem does not assert a phase relation on the unused ambient complement.

`first_commuting_PVM_upper` and `second_commuting_PVM_upper` quantify over an
arbitrary complete complex Hilbert space. They are separate proof scripts, not
corollaries inferred from a finite-dimensional theorem. They concern upper
bounds; the new correlation-model supremum assembly is recorded below.

The polar-linear permutation and private-MUB criteria are intentionally
conditional in exactly the mathematical sense of their manuscript statements.
Their phase/product or private-reference hypotheses must not be advertised as
proved for arbitrary strategies.

## Newly written model, binary and appendix endpoints

All names in this table have prefix `CyclicBell.General.`. All rows are
**uncompiled proof-script candidates**, with expanded checks in
`ModelValueStatements.lean` and pending axiom requests in `AxiomAudit.lean`.

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

### The closure route and its precise limit

`continuous_bound_on_closure` extends a scalar sublevel bound to Qqa by continuity
of the actual finite Bell functional. `bellSupremum_of_attained_bound` exhibits
nonemptiness and boundedness before using real `sSup`. The selected witness and
arbitrary-model upper bounds are discharged in each named value endpoint.

**No theorem `Qqa subset Qqc` or closedness of Qqc is claimed.** Those are not
needed for the value equalities just listed. The general inclusion displayed
in the manuscript remains a separate, unwritten source endpoint. Lean's `Type`
carrier convention in these sets is a universe-size convention, not a finite
Hilbert-dimension restriction.

`BinaryPrivacyAt` is an explicitly universally quantified *property to prove or
refute*, not a validity assumption. The achievable behavior is shown to lie in
Qq, and `purifyStrategy` constructs a compatible finite purification; the privacy
statement is not vacuous. Its proof has no claim of arbitrary-Hilbert Eve privacy.

## New adversarial and source-Fourier endpoints

All new rows are **uncompiled proof-script candidates**, not formal certification.
Names below have prefix `CyclicBell.General.`. `AdversarialStatements.lean`
checks expanded definitions/quantifiers; the normal build reaches every module.

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

### Retained prior-pass source repair

The incoming `GeneralScalar.lean` referred four times to `dimension_pos`, which
was declared in `GeneralWitness.lean` outside its import closure. The unchanged
lemma has moved to the shared ancestor `GeneralFourier.lean`. Its statement and
proof are unchanged. No witness dependency was added to the universal bound.
The current conservative project-reference scan passes and its mutation tests
reproduce the incoming failure. This was found by source inspection, not Lean.

## New settings-appendix candidates

All names below have prefix `CyclicBell.General.` and all remain uncompiled.

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

## Still not supplied as complete formal source endpoints

1. General Qqa-subset-Qqc / closedness or universal GNS-style model inclusion.
   The written specific cyclic/binary value equalities and adversarial lower
   bounds do not assume this theorem.
2. The canonical-polar/von-Neumann-algebra argument and computational-MUB
   Toeplitz/SVD intermediate identities as individually translated theorems.
   The needed bounds/obstruction conclusions have alternative source routes.
3. Full canonical source-Z/source-coefficient strategy identification with its
   polar expression, including complete source PVM validity. The coefficient
   DFTs, both source Fourier sums and the qutrit formula are now written, but
   those identities alone do not close this separate endpoint.
4. The external self-testing theorem and a formal convention/isometry transport
   to its implementation are not supplied. The displayed probability tables,
   anchor formulas and observed entropy asymptotic themselves are now candidates.
5. Attainment of a fixed-realization POVM maximum for arbitrary-Hilbert Eve,
   or a maximizing realization of the worst-case value-conditioned quantity.
   The latter is not claimed by the paper's lower bound; finite-Eve fixed
   realization maxima and their finite-q nesting are now written explicitly.

The actual *adversarial* extended q/qa/qc domains and the paper's model-indexed
lower bounds are now source candidates, not just informal witness arguments.
The unknown optimal worst-case guessing value, open classifications, priority
claims and bibliography are not converted into theorems.

## Current inventory and executed status

The scanner finds **1,132 theorem candidates**, 374 definitions, 14 abbreviations,
16 structures and two named instances. **1,538 pending axiom queries**, **100
expanded statement examples**, and **81 Lean files** are in the standard build
and audit graph. The bounded settings extension adds 42 theorem candidates,
17 definitions, five Lean files and eight expanded statement examples.

Old mathematical Lean modules and all dependency pins are unchanged. Only the
existing GeneralStatements and AxiomAudit Lean files were extended for normal
build/audit integration. The runner and tests were changed to reject false
positive negative-control receipts after crashes or resource exhaustion.

Executed this pass: 7,794 new exact assertions and 48 controls for d=2..8,
55 reporting/scanning tests, retained 392 d4 checks and 12+8 SOS checks, and
static/import/reference/pin/integrity checks. Other historical suites were not
rerun in this pass; their old receipts remain explicitly historical.

No Lean process, actual axiom report, clean Lean build, independent agent or
remote push occurred. None of these finite or lexical checks proves continuity,
asymptotics, suprema, or universal statements. Whole-paper source coverage is
still incomplete and every formal endpoint is uncertified.
