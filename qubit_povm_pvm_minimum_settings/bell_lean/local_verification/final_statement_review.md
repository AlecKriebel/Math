# Independent final statement and paper-correspondence review

Checkpoint: 2026-09-11T02:10:02.650525+00:00. Statement-review subgoal: 100% inspected; whole-project certification is conditional on the root task's final clean build, contract elaboration and complete axiom audit. This review does not claim that pending assembly modules have already compiled.

## Conclusion

No added hypothesis or weakened conclusion was found in the top-level universal equality, finite complete-strategy simulation, exact separator, minimum-input result, or strengthened attainment. The definitions describe the intended complex-qubit probability model and ordinary shared-randomness convex hulls. The source-to-paper correspondence supports certifying these named mathematical conclusions after the final compiler checks succeed. It does not by itself certify every sentence, bibliographic claim, or optimality claim absent from the formal statements.

## Method and exact comparison

Reviewed the repository paper `paper/main.tex` and `paper/appendices.tex`, the original archive `/Users/alec/Downloads/bell_lean_mathematical_audit_20260910.zip`, current production modules, and `validation/Statements.lean`.

An independent script compared explicit theorem headers throughout `Bell/*.lean` against archive members, normalizing whitespace and the reserved lambda variable rename. The recorded result is `archive_statement_changes.json`. At this checkpoint its only explicit-header difference is adding the inferred types `ξ : V` and `s : ℝ` to `sameRay_of_homogeneous_inverse`. No endpoint theorem acquired an explicit assumption. This text comparison is supplemented below with a review of definitions and implicit section-variable changes; text alone is not kernel verification.

## Physical model

* `Quantum.lean` fixes `Operator = Matrix (Fin 2) (Fin 2) ℂ` and a joint `Fin 2 × Fin 2` index. State matrices are positive semidefinite with trace one. Arbitrary mixed states are permitted. No reality, purity, full-rank, or ancillary-system premise occurs in `Strategy` or the public equality theorem.
* Each POVM has all declared effects positive semidefinite and summing to the identity. A PVM adds idempotence and pairwise orthogonality while allowing zero projections. Declared output counts depend on the input and have no positivity restriction in the architecture type.
* `born` is the real part of the trace of the genuine complex density matrix against the tensor product of the two effects. `Expectation.lean` proves nonnegativity, normalization and both nonsignaling equations. Thus the behavior type is an ambient real table, but the strategy range is not an unconstrained stand-in feasible set.
* `rawPOVM` and `rawPVM` are actual ranges of complete strategies. `convexPOVM` and `convexPVM` are Mathlib's ordinary real convex hulls of those ranges. They are not defined to coincide, are not replaced with closures, and do not contain a hidden simulation premise.
* `finite_projective_simulation` quantifies one finite index type, one normalized nonnegative weight function, and one complete projective strategy per branch. The same index chooses the state and every local measurement simultaneously. Its conclusion is equality of the whole labeled behavior function. There is no per-entry or per-input choice of independent mixing distributions and no same-state simulation claim.
* The paper permits local dimensions at most two; Lean uses a fixed complex two-dimensional carrier. This is the usual embedding convention, not a larger-dimensional model. Singular qubit states and all product response tables are included, with `product_behavior_mem_convexPVM` proving the latter for arbitrary normalized finite stochastic response rows. A separately parameterized theorem for Hilbert-space dimensions 1 and 2 is not present.
* The paper includes local stochastic output postprocessing on the projective side. The formal hull permits finite mixtures of complete projective strategies; `StrategyMaps` proves closure under deterministic output maps (including merging and padding). The standard finite stochastic-map decomposition therefore has the intended interpretation. No distinct generic stochastic-channel closure theorem is named in the current inventory. This is a presentation convention to state explicitly, not an extra hypothesis of the endpoint equality.

## Paper-to-theorem map

| Paper claim | Formal endpoint | Correspondence |
|---|---|---|
| Universal two-input equality (`thm:two-input-equality`) | `two_input_convex_equality AO BO`; `universal_two_input_equality` | All finite input-dependent outputs; genuine complex-qubit convex hulls; no residual, positivity, rank, or realization assumptions. |
| Complete common-randomness projective simulation | `finite_projective_simulation AO BO s` | One finite mixture of complete strategies reproduces the full table. |
| One input on either side and all at-most-two architectures | `one_input_equality`; `at_most_two_input_equality` | Includes empty input sets and impossible empty-output architectures; no positive-alphabet condition added. |
| Exact separator, Theorem 3.1 | `witness_mem_raw`, `witness_value`, `projective_global_upper_bound`, `three_by_two_separation` | Alice has three inputs/three declared labels, Bob two inputs/two labels. The first two Alice inputs have an unused third label as in the paper. |
| Separator constants | `lower`, `upper`, `gap_identity`, `strict_gap` | Exactly L0 = 20√2 + 16/25, U = 20√2 + 3/5 + (4+3√2)/250, and L0−U = 3(2−√2)/250. |
| Stronger projective certificate | `convex_projective_rational_upper` | Proves the stronger bound 289/10 for every behavior in the actual projective hull. `rational_bound_lt_paper_upper` transfers it to the paper's U. No numerical optimization or exact-optimum claim is substituted. |
| Minimum input architecture (`cor:minimality`) | `minimum_inputs`; `minimum_inputs_attained` | Any strict separator needs at least (3,2) or (2,3); the concrete (3,2) separator attains the threshold. |
| Appendix B strengthened physical attainment | `strengthened_attainment`; `main_claims_with_strengthening` | A genuine raw POVM behavior has value (16+8√7813)/25. This is attainment, not a mere algebraic number or global POVM optimum. |

`MainClaims` is exactly the conjunction of universal two-input equality, one-input equality, the paper's actual raw-projective global bound, and physical strict separation. `main_claims` takes none of those propositions as an argument. The historical `main_claims_of_missing_theorems` remains a conditional helper, but it is not the unconditional endpoint.

## Modified helpers and possible hidden premises

1. `RankZeroSimulation.ternaryLabelMap_injective` now explicitly includes the existing section hypothesis `hπ : ∀ j, (π j).val < 2 ↔ j.val < 2`. This premise is mathematically necessary: without it the permutation swapping indices 0 and 3 maps two ternary labels to the same truncated natural-number difference. All intended callers already carry the partition-preservation premise, and it is derived by the rank-zero rigidity argument before use. No global assumption was added. The archive's uncompiled source already attempted to use `hπ` and passed it at call sites.
2. `UnnormalizedAssemblage` had the malformed grouped declaration `leftSum rightSum : Operator`; Lean interpreted the first token as a function declaration rather than two independent fields. Splitting it into `leftSum : Operator` and `rightSum : Operator` implements the structure that all original field conditions and constructions intended. Its normalization, positivity and definiteness hypotheses were neither removed nor strengthened.
3. `separatorArchitecture` and `binaryTernaryArchitecture` changed from `def` to `abbrev` with unchanged bodies, allowing the elaborator to unfold their finite input/output counts. This changes transparency rather than the mathematical model.
4. The general `matrixPair_mul_frames` lemma moved from `IncidenceDifferential` to `IncidenceAlgebra` to remove an unnecessary calculus dependency. Its statement is unchanged. Added application lemmas expose existing rank-one/steering definitions, not new assumptions.
5. Assumptions such as pure/full-rank states, nonzero null effects, invertible frames, positive multiplier weights and rank-case hypotheses remain local lemmas' explicit hypotheses. The assembled equality theorem quantifies all actual strategies, and its source obtains these conditions by reductions; they do not escape into its public type.

## Contract coverage and final execution requirement

`validation/Statements.lean` already asks Lean to elaborate, rather than merely print, the complex Hilbert-space carrier, state/PVM fields, Born tensor formula, expanded range/hull equality, finite complete-strategy mixture, zero-output and zero-input edge cases, strengthened raw attainment, projective quantitative upper bound, strict separation, and minimum-input quantifiers. That is a strong semantic guard against a vacuous top-level alias.

The supplementary `local_verification/FinalStatementContracts.lean` independently exposes POVM fields, physical nonnegativity/normalization/nonsignaling, every `MainClaims` component with the exact paper upper-bound scalar, raw simple-witness attainment, the convex rational upper bound, exact gap identity, at-most-two equality, and the conjunction with strengthened attainment. It is intentionally left for the root task's final production build and elaboration sequence. Running these contracts is still required before promoting this review to a completed certification.

Selected production physical-bridge axioms have already been queried in `IncidenceChainAxioms.lean`: all seven selected theorems report only `propext`, `Classical.choice`, and `Quot.sound`. The final complete public-dependency audit remains the root task's responsibility. Temporary isolated probes were useful during dependency repair, but their success is not counted as the final production build.
