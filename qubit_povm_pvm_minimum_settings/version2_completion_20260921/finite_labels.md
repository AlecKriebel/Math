# Finite-label physical model completion

Checkpoint 2026-09-21T14:29:12.110262+00:00: **100%** of the assigned finite-label and stochastic-integration goal complete.

## Checked production artifacts

- `Bell/FiniteLabels.lean`: independent POVM/PVM effect records over arbitrary finite outcome types, whole source strategies with actual matrices and Born probabilities, measurement/strategy encoding and decoding equivalences, full-table real linear equivalence, finite-mixture transport with unchanged weights, exact raw-range and ordinary convex-hull transport, membership equivalences, and principal two-input/at-most-two-input equality.
- `Bell/FiniteStochastic.lean`: independent weighted behavior processing over arbitrary input-dependent finite source/target labels; exact commuting square with cardinal encoding; one finite selector decomposition of the entire table; physically realized raw-PVM deterministic branches; stochastic preservation of the source model's convex PVM hull.
- `validation/FiniteLabelContracts.lean`: 12 anonymous contracts.
- `validation/FiniteStochasticContracts.lean`: 5 anonymous contracts.

Pinned Lean 4.19.0 production build of `Bell.FiniteStochastic` succeeded, including `Bell.FiniteLabels`. Both contract files independently completed successfully. Local compiler logs are `bell_lean/local_verification/finite_stochastic.log`, `finite_label_contracts.log`, and `finite_stochastic_contracts.log`. A 25-declaration axiom check (`finite_label_axioms.log`) reports only `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx` or custom axiom.

## Mathematical scope and boundaries

The source measurement definitions are independent matrix-valued families, not aliases for Fin-indexed Bell measurements. The source strategy's state is unchanged by encoding, every effect is transported by an explicit finite equivalence, and the entire Born table is preserved. Normalization is proved by equivalence invariance of finite sums; positivity, idempotence, and orthogonality transport directly. Inverse laws certify that every target strategy also comes from a source strategy. Convex-hull statements use ordinary convex hulls, not closures or limits, and preserve finite shared-randomness weights.

The scope is arbitrary input-dependent finite **outcome** types; inputs remain `Fin m` and `Fin n`, as authorized. No nonempty outcome assumption is introduced. Empty declared outcomes at an existing input preclude a source strategy and yield empty raw models/hulls; empty input sets impose no measurement constraints. Contracts cover Bool, Option Bool, explicitly input-dependent Option/Bool-product alphabets, Empty, zero inputs, and empty-to-empty stochastic channels. Existing source rows cannot have empty target channel alphabets because row normalization rules that out.

Stochastic processing is defined by actual finite weighted sums on source labels before relating it to the existing cardinal model. The same global selector and weights reconstruct all input pairs and both parties simultaneously. Only convex PVM closure is claimed for general stochastic processing; raw PVM membership is proved for each deterministic selector branch. Output merger maps need not be injective.

## Independent review

The repair_calculus reviewer independently accepted both source designs. For FiniteLabels they checked independent effect/state records, two-sided strategy and raw-range correspondence, exact hull directions, and lack of hidden Nonempty/DecidableEq premises. For FiniteStochastic they checked the independently defined weighted map, exact commuting square, actual physical PVM branches, and unchanged global selector weights. Final production compilation and contracts subsequently passed.

## Integration

Root should import `Bell.FiniteStochastic` in the aggregate module (it imports `Bell.FiniteLabels`) and include both anonymous contract files in the shared runner. No shared aggregate, audit, or script files were edited by this subtask. No commits, releases, or external communications were performed.
