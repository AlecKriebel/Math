# Coverage — written source versus certification

**Current formal certification: none.** Every row below has explicit Lean proof
scripts, but those scripts have not been compiled. “Written” does not mean
“kernel-accepted,” and no claim here promotes a Python check to a Lean proof.

## Requested d=4 endpoints

| Milestone | Manuscript reference | Principal source declarations | Source status |
|---|---|---|---|
| A: arbitrary-dimensional first augmented bound | `eq:Id`, `thm:exact`, `cor:first-augmented`, specialized to d=4 | `CyclicBell.first_universal_upper`, `first_upper_bound`, `first_physical_sos` | Written; no witness-module dependency; uncompiled |
| B: normalized state and ALL first-family PVMs | `eq:first-strategy`, `eq:final-swap`, `app:d4` | `D4.firstStrategy`, `D4.complete_witness_validity`, `D4.firstAlice_zero_encoding`, `D4.firstAlice_one_encoding`, `D4.firstBob_encoding`, `D4.firstBob_added_encoding` | Full witness written; uncompiled |
| C: first augmented attainment | `thm:biased`, `app:d4`, d=4 | `D4.first_reduced_attainment_complex`, `D4.first_attainment` | Actual functional evaluated; uncompiled |
| D: physical table, normalization, marginals, largest probability | `eq:target-table`, `eq:d4-table` | `D4.first_behavior_table`, `D4.first_target_normalization_and_marginals`, `D4.first_target_maximum`; parallel second-family names | Written from trace Born rule; uncompiled |
| E: maximal scalar value does not force uniformity | `sec:randomness`, d=4 Conjecture-2 discussion | `D4.first_counterexample`, `D4.first_is_maximizer`, `D4.first_scalar_value_does_not_force_uniform`, `D4.first_trivialEve_gap` | Unconditional source statements; uncompiled |
| F: complete second-family endpoint | `eq:lambda`, `lem:lambda-normalization`, `eq:second-functional`, `eq:second-sos`, `thm:second`, d=4 | `CyclicBell.second_physical_sos`, `second_universal_upper`; `D4.secondStrategy`, `D4.second_attainment`, `D4.second_counterexample` | Actual coefficients, global SOS, full witness and table written; uncompiled |

Names beginning `D4.` are in namespace `CyclicBell.D4`. The combined source
endpoint is `CyclicBell.D4.main_d4_counterexamples`.

## Physical and manuscript bridges

| Bridge | Declarations / modules |
|---|---|
| Arbitrary finite coordinate dimensions; PSD trace-one mixed states; PVMs with zero effects allowed | `Model.lean`: `State`, `PVM`, `Strategy`, `tensor`, `observable`, `born` |
| PVM encoding implies unitarity and fourth power identity | `MatrixAlgebra.lean`: `observable_unitary`, `observable_fourth_power` |
| Exact inverse measurement encoding | `Fourier4.lean`: `pvm_source_fourier_reconstruction` |
| Born reduction and density/vector agreement | `Model.lean`: `pureBorn_projectors`, `expectation_eq_trace`, `pureBorn_eq_born` |
| Generic nonnegative normalized Born probabilities | `TraceCalculus.lean`: `born_nonnegative`, `born_normalized`, marginal lemmas |
| Scalar constants and actual exponential embedding | `ScalarData.lean`: `D4.zeta_components`, `zeta_pow_exp`, `zeta_phaseTable`, `first_constant_bridge` |
| Target phases really use (0,1,3,2) | `D4.kappa_values`, `weights_are_final_swap`, `Phases.lean`: `old_weights_phase_bridge`, `old_q_phase_bridge` |
| All weighted-cycle projectors and their observable encodings | `Cycle4.lean`: `cyclePVM`, `cyclePVM_encoding`; `Witness.lean`: complete PVM tuples |
| Bob's conjugation, Alice's second-family convention | `D4.bob_manuscript_bridge`, `D4.secondAlice_manuscript_bridge` |
| Actual source coefficients, not an assumed normalized vector | `D4.sourceLambda_eq`, `lambda_normalization`, `sourceLambda_normalization` |
| Literal second-family Fourier compression | `D4.witness_source_D_compression` |
| Second-family SOS annihilation on the state | `D4.second_witness_residual_zero` |
| Trivial Eve is a physical C¹ instrument | `Guessing.lean`: positive complete guessing effects, adjoined state, sandwich and partial trace; `D4.first_physical_Eve_bridge`, `second_physical_Eve_bridge`, `trivialEve_purification` |

## Alternative proof route, not a hidden premise

A uses a new d=4 polynomial SOS supplied in `FirstSOS.lean`, not the manuscript's
all-dimensional polar/CFC argument. Its hypotheses are unitary A and U, unitary
B_y, and U B_y=B_y U. `PhysicalBounds.lean` proves all of these from the original
physical Strategy. Neither equality-phase spectra nor maximization are assumed.
The physical upper-bound import closure excludes the concrete witness modules.
The separate `SecondSOS.lean` retains the source's 1/8 normalization at d=4.

`IsFirstMaximizer` and `IsSecondMaximizer` mean comparison with ALL finite-
dimensional competitors. Their witness instances are proved using a universal
upper bound and separate exact attainment; they are not strategy-validity fields.

## Conditional helpers versus endpoints

Generic matrix lemmas appropriately assume unitarity, genuine commutation,
positive matrices, coefficient normalization, or an orthonormal basis. Those
hypotheses are explicitly discharged before either endpoint. The public
counterexamples assume none of the target conclusions and have no unproved
mathematical axiom as a written dependency. Whether the supplied scripts
successfully elaborate and whether all transitive dependencies are permitted
must still be determined by the offline audit.

## Mathematical negative controls

`Regression.lean` proves, as source candidates, that doubling Phi4 violates
normalization (the original control is in D4), restoring the canonical final
phase gives a uniform target table, the changed table differs from the swap,
dropping Bob's conjugation or replacing it by an adjoint is wrong, and an extra
factor four changes the first functional's attained value. The intentionally
false `validation/Reject*.lean` files must fail with genuine proof errors.
They are tested separately and are not production imports.

## Not written / not claimed

No source formalization is supplied for `thm:exact` at arbitrary d or on arbitrary
Hilbert spaces; q/qa/qc value equality; `thm:support-rigidity` and its support,
Schmidt, polar-kernel, invariance, and rank bridges; the all-d phase-permutation
or autocorrelation results; a complete maximizing-face classification; arbitrary
adversarial guessing optimization; canonical private randomness; robustness;
self-testing equivalences; the binary benchmark; or the low-setting obstruction.
A separate abstract-Hilbert-space basis-transport theorem is not included: the
physical model is explicitly the finite coordinate-matrix model C^nA tensor C^nB.

## Executed versus pending

Executed: compiler-free exact algebra, source/import/lock/declaration checks,
reporting-tool unit tests, local preservation, and package integrity checks.
Pending: any Lean elaboration, any clean Lean rebuild, actual axiom output,
Lean positive/negative controls, and genuinely independent statement review.
