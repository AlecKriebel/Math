# Independent semantic referee report

Scope: `Bell/Quantum.lean`, `Expectation.lean`, `Convexity.lean`, `Assembly.lean`, `SimulationCorollaries.lean`, `OneInput.lean`, `StrategyMaps.lean`, `Targets.lean`, and both production validation files, compared directly with `paper/main.tex`. Supplementary checks included `ProductLocality.lean`, `LocalSimulation.lean`, and the declarations in `QuantumCompactness.lean`. Review date: 2026-09-11. Production files were not modified.

## Verdict within this review's scope

The public unconditional two-input equality states the correct complex two-qubit convex-hull theorem for arbitrary finite input-dependent output counts. It is not a tautological alias, an equality assumed as an argument, a scalar surrogate, a same-state claim, a real-qubit restriction, or an entry-by-entry mixture. No semantic defect undermining that theorem was identified in the reviewed model and assembly interfaces.

This conclusion is conditional on the independent fresh kernel build and axiom review coordinated by the lead referee. Reading a source proof does not establish that the checked environment accepts it. The difficult imported geometric proof is reviewed by other independent referees, not certified by this report.

“Every mathematical statement in the paper has been formalized” is stronger than the evidence here supports. In this part of the paper, stochastic postprocessing and the conversion from Hilbert-space dimension at most two to the fixed `Fin 2` matrix model are not explicitly formalized. Both conversions are valid and elementary; their omission is a coverage/documentation issue, not a counterexample to the main equality. The exact scope should be stated rather than conflating mathematical equivalence with an existing Lean theorem.

## Direct correspondence and anti-vacuity checks

| Paper item | Exact production evidence | Referee finding |
|---|---|---|
| Complex local qubits | `Bell/Quantum.lean:19–22` | `Qubit := Fin 2`, local matrices over `ℂ`, joint matrices indexed by `Fin 2 × Fin 2`. No real restriction and no ancillary quantum register. |
| Physical state | `Bell/Quantum.lean:28–31` | A full joint matrix with positive semidefiniteness and complex trace exactly one; mixed states allowed. |
| Physical POVM | `Bell/Quantum.lean:33–36` | Every effect positive semidefinite and the full finite sum exactly the identity. There is no restriction to rank one, nonzero effects, binary outputs, or extremal measurements in the definition. |
| Physical PVM | `Bell/Quantum.lean:38–40` | Extends the physical POVM with idempotence and pairwise orthogonality. Since positive semidefinite matrices are Hermitian, these are genuine orthogonal projections. Zero and identity projectors are admitted. |
| Declared alphabets | `Bell/Quantum.lean:42–50` | Output counts depend on the input, and the behavior retains every input and outcome index. |
| Born rule | `Bell/Quantum.lean:25–26,54–55,67–68` | Tensor entries are exactly `M i.1 j.1 * N i.2 j.2`; the behavior is the real part of `trace (ρ * tensor M N)`. For the Hermitian physical matrices this is the ordinary real Born probability. |
| Physical validity of probabilities | `Bell/Expectation.lean:140–169,183–205` | Positivity follows from the state matrix and tensor positivity; normalization and both nonsignaling equalities are proved for arbitrary strategies. These are not extra premises to the equality. |
| Raw images and convexification | `Bell/Quantum.lean:76–86` | Separate ranges of actual physical strategies and ordinary Mathlib real convex hulls. No custom weakened notion of hull. |
| Full arbitrary-output equality | `Bell/Assembly.lean:77–85` | The only arguments are `AO BO : Fin 2 → ℕ`. No positive-count, full-rank, optimality, realness, or residual-case premise survives in the theorem. |
| Universal architecture schema | `Bell/Targets.lean:51–53`, `Bell/Assembly.lean:89–107` | The `UniversalTwoInputEquality` alias unfolds to the requested equality for every architecture with two inputs each. At-most-two inputs, including zero-input cases, are also covered. |
| Complete-strategy finite simulation | `Bell/SimulationCorollaries.lean:24–37` | There exists one finite index type, normalized nonnegative weights, and one complete `ProjectiveStrategy` per index, with equality of entire behavior functions. The state may change by branch; every measurement is chosen by the same branch. |
| One-input boundary | `Bell/OneInput.lean:59–160` | Arbitrary numbers of settings for the other party and all dependent output counts. The conditional-response construction produces a single deterministic assignment for every setting and treats zero marginal probabilities through `ClassicalProduct`. |
| Empty outputs | `Bell/OneInput.lean:24–29`; `validation/Statements.lean:45–51` | A normalized qubit POVM cannot have zero outputs. Equality still has no nonempty-alphabet premise; it correctly includes empty physical images. This does not make the equality vacuous for ordinary alphabets. |
| Explicit nonvacuous strategies | `Bell/LocalSimulation.lean:22–40,42–68` | Deterministic identity/zero PVM strategies exist for every full label assignment, with a physical trace-one state and the expected deterministic behavior. In particular all architectures whose output counts are positive have witnesses. |
| Deterministic postprocessing | `Bell/StrategyMaps.lean:13–50,52–124` | Arbitrary output functions, including merging and unused declared labels, preserve actual POVMs and PVMs and commute with the Born behavior. Maps act on complete strategies, not isolated probability entries. |

The main assembly proceeds by genuine contradiction: an alleged hull counterexample supplies a maximizing extreme physical strategy (`Assembly.lean:81–84`); `no_two_input_extreme_separator` supplies the contradiction. Its internal strict separator and extremality hypotheses are discharged by the imported compactness/separation theorem. They are not external assumptions of the public equality.

The zero-input proof does not incorrectly manufacture a strategy when some other input has an empty outcome alphabet. It starts from an existing `Strategy`; the positive-output lemma provides the needed labels. If no strategy exists, the raw image and its hull are empty, as they should be.

## Independent contract

`../contracts/MatrixModelContract.lean` is new referee-only evidence. It defines two independent sets using existential quantifiers over explicit `Matrix (Fin 2) (Fin 2) ℂ` effects and `Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ` states. Its definitions spell out all positivity, normalization, projection, orthogonality, and tensor-entry conditions without invoking `Bell.Strategy`, `Bell.ProjectiveStrategy`, `Bell.rawPOVM`, or `Bell.rawPVM`. The two representation lemmas identify those independently written sets with the production images. The final theorem is

```
convexHull ℝ (MatrixPOVMBehaviors AO BO) =
  convexHull ℝ (MatrixPVMBehaviors AO BO)
```

for arbitrary `AO BO : Fin 2 → ℕ`, and prints its axioms. This is stronger protection against definition/alias drift than merely checking a theorem name. Its compiler status must be obtained from the lead referee's isolated run; this reviewer did not compile against existing production artifacts.

## Coverage findings

### C1. Stochastic postprocessing is not an explicit general production contract

The paper expressly includes it (`paper/main.tex:280`) and states its optimum-preservation lemma (`paper/main.tex:295–314`). The production strategy image requires literal projectors (`Quantum.lean:38–40,79–80`), while `StrategyMap` has deterministic output functions (`StrategyMaps.lean:52–56`). A search across the production `Bell` modules found no general stochastic-kernel postprocessing definition or proof that arbitrary such kernels preserve `convexPVM`. `ProductLocality.product_behavior_mem_convexPVM` (`ProductLocality.lean:17–59`) treats stochastic local response rows producing product behaviors; it does not itself state postprocessing closure for an arbitrary entangled PVM behavior.

The mathematical bridge is valid. For kernels `K_A(a|x,c)` and `K_B(b|y,d)`, sample, in advance, each function value `f_x(c)` and `g_y(d)` independently with those probabilities. The finite weight of a complete pair `(f,g)` is

```
w(f,g) = ∏_(x,c) K_A(f_x(c)|x,c) · ∏_(y,d) K_B(g_y(d)|y,d).
```

These weights are nonnegative and sum to one. Their average indicator for the pair `(f_x(c)=a,g_y(d)=b)` is exactly `K_A(a|x,c) K_B(b|y,d)`. Thus the postprocessed behavior is a finite convex mixture of the deterministic coarsenings already proved in `StrategyMaps`. This works for arbitrary input counts and is needed in particular to connect the paper's full `3×2` stochastic-PVM comparison to its literal-projector Lean model.

Recommendation: either add this general theorem and an independent contract, or identify this routine finite-kernel decomposition explicitly as a paper-to-formalization bridge outside the current Lean coverage. Do not describe it as an existing formalized theorem. This is a medium-priority scope/documentation finding for a claim of total coverage; it does not threaten the two-input hull identity.

### C2. The dimension-at-most-two embedding is implicit, not formalized

The paper quantifies over local Hilbert spaces of dimensions at most two (`paper/main.tex:251–264`); production `Quantum.lean:19–22` fixes a particular two-dimensional complex basis. There is no generic finite-dimensional Hilbert-space strategy type or theorem embedding a one-dimensional strategy into these fixed spaces among the inspected or searched production modules.

The mathematical bridge is valid. Choose an isometry `V` from each nonzero local Hilbert space into `ℂ²`, embed the joint state by `V_A ⊗ V_B`, and extend each measurement by

```
M'_a = V M_a V† + 1_(a=a₀) (I − V V†)
```

for one chosen label `a₀` at that input. The added complementary projection is positive, orthogonal to the embedded support, and has zero probability in the embedded state. It makes the effects sum to `I₂`; it also preserves projectivity and orthogonality when the original effects are projections. A valid measurement on a nonzero space has a nonempty output alphabet, so `a₀` exists. A zero-dimensional local space cannot carry a trace-one joint state. Conversely, the exactly-two-dimensional model is already one allowed case of the paper's at-most-two-dimensional model. Finite alphabets are transported to `Fin n` by choosing bijections.

Recommendation: describe fixed complex matrix coordinates as the formalized model and record this standard equivalence. A demand that every model-identification step itself be checked in Lean calls for an additional embedding theorem. This is a low-priority formal coverage finding, not a mathematical problem.

### C3. Support-value equivalence is represented by bounds, not literally all paper statements

`SimulationCorollaries.lean:49–67` establishes equality of upper-bound predicates for every two-input real linear functional. It deliberately avoids defining a support-value supremum or maximum. This is enough to transfer every linear Bell bound and, with the independently proved compactness, yields the paper's equality of support values. The general compact-convex support-function equivalence in `paper/main.tex:339–358` is not directly the statement of these corollaries. A claim that all paper lemmas were formalized should distinguish equivalent mathematical consequences from a literal theorem-by-theorem transcription.

No concern here requires changing the two-input theorem statement. None establishes that the target equality is false. The strongest supported conclusion from this semantic review is that a successful fresh kernel/axiom audit certifies the intended unconditional complex-two-qubit convex-hull equality with all finite declared outcome counts, and a finite common mixture of complete PVM strategies. The reviewed interfaces do not support the broader claim that every auxiliary mathematical sentence and every paper-to-coordinate identification already has an explicit Lean proof.
