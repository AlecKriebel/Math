# Manuscript coverage — model values and appendix continuation

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

## Still not supplied as complete formal source endpoints

1. The general Qqa-subset-Qqc inclusion / closedness or universal GNS-style
   correlation-model argument. **The cyclic and binary value suprema themselves
   are now written** without relying on this inclusion.
2. The manuscript's canonical-polar partial-isometry/von-Neumann-algebra proof
   and computational-MUB Toeplitz/SVD intermediate formulas as individual
   theorems. Their needed conclusions have alternative proof-script routes.
3. The canonical source-Z/source-coefficient strategy identification and special
   qutrit expression in `app:attainment`. The needed attaining physical cyclic
   strategies are instead supplied through the weighted-cycle construction.
4. The standard Fourier-phase self-test tables, anchored cross-table formulas
   and asymptotic entropy comparisons in `app:settings`.
5. A full definition and supremum assembly of the *adversarial* tripartite
   guessing models in `eq:gval-model`. The existing physical trivial-Eve
   witness direction and failure of value-only privacy are written; no exact
   worst-case guessing optimization is claimed.

The paper's open questions, bibliography and priority claims are not converted
to theorem declarations. The companion is not a proof of open maximizing-face
classifications or new robustness/self-testing claims.

## Inventory and executed status

The source scanner finds **987 theorem candidates**, 319 definitions,
12 abbreviations, two named instances, 12 structures, and **75 anonymous
expanded-statement examples**. **1,332 generated `#print axioms` requests** cover
all explicitly named declarations. The standard import closure has **66 Lean
files**, including the umbrella and audits. These are text inventory counts,
not accepted-theorem counts or a measure of formal correctness.

Every earlier mathematical Lean module and every pinned dependency
configuration remains byte-for-byte unchanged from the immediate input. Only
`GeneralStatements.lean` and `AxiomAudit.lean` changed among earlier production
Lean files, to import and query the additions. The new work adds eleven Lean
files (ten mathematical modules and an expanded-statement audit).

Executed in this continuation: static import/pin/declaration checks; 34 tests
of audit machinery; 9,906 new Gaussian-rational interface assertions with
37 controls; 175 complete-permutation-determinant assertions with 19 controls;
and reruns of the earlier 392 d4 checks, 12 first-SOS checks, 8 alternate
word-reduction checks and 3,040 distinct general checks with 38 controls.

Not executed: Lean elaboration, any clean Lean rebuild, any actual axiom query,
any Lean positive/negative control, or any independent-agent correspondence
review. Every formal endpoint remains uncertified. The scanner is not a Lean
parser, and uncompiled proof scripts may need substantive mathematical repair.

Historical scope documents remain under `history/`; their earlier exclusions
and counts do not describe this source extension.
