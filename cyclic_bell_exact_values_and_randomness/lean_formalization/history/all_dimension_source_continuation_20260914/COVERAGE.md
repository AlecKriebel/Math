# Manuscript coverage — all-dimensional source continuation

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
bounds; the correlation-model supremum wrappers below are still absent.

The polar-linear permutation and private-MUB criteria are intentionally
conditional in exactly the mathematical sense of their manuscript statements.
Their phase/product or private-reference hypotheses must not be advertised as
proved for arbitrary strategies.

## Still not supplied as complete formal source endpoints

1. The full definitions of Q_q, Q_qa, Q_qc and their embedding/closure/supremum
   assembly into the literal three-model value equality. Finite physical
   attaining strategies and separate arbitrary-Hilbert PVM upper bounds are
   written, but they are not silently promoted to that complete model theorem.
2. The manuscript's canonical polar partial-isometry/von Neumann algebra proof
   itself. The bound uses a different continuous-factor proof that handles zeros.
   Likewise the computational-MUB block/Toeplitz/SVD intermediate identities
   are replaced, not individually formalized.
3. The canonical Z/source-coefficient strategy identification, source Fourier
   sums and special qutrit expression in the attainment appendix; the weighted
   cycle characteristic polynomial for general nonunit weights. The companion
   instead constructs all needed unit-phase PVMs and proves their encodings.
4. The standard Fourier-phase self-test tables, anchored cross-table formulas,
   asymptotic entropy comparison and some low-dimensional exact-value entries.
5. A separate arbitrary-Hilbert binary benchmark proof and full q/qa/qc binary
   value wrappers. The finite arbitrary-dimension binary SOS, physical
   attainment and arbitrary finite purifying-Eve privacy chain are written.
6. Some transport/assembly corollaries, notably explicitly swapping parties in
   the one-input theorem and bundling its conclusion with the binary benchmark
   as a named componentwise-minimality endpoint.

The manuscript's open questions, bibliography, priority statements, complete
maximizing-face classification, optimal worst-case adversarial guessing, and
approximate/self-testing claims are not converted to theorems here.

## Inventory and its limits

The current scanner finds **851 theorem candidates**, 273 definitions,
11 abbreviations, two named instances, nine structures, and 50 anonymous
expanded-statement examples. **1,146 generated `#print axioms` requests** cover
all explicitly named declarations, including proof-bearing constructors and
named finite-spectrum instances. The standard closure has **55 Lean files**.

These are source counts, not proof-quality measurements or accepted-theorem
counts. The scanner is not a Lean parser. Actual compiler output must confirm
that all declarations elaborate and that every transitive axiom set is allowed.

The previous detailed d=4 coverage register is preserved under
`history/d4_source_continuation_20260914/COVERAGE.md`. It is historical; its
321-theorem count and exclusions do not describe the current extension.
