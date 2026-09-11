# Balanced cone circuits and physical realization audit

Checkpoint: 2026-09-11T02:09:37.499655+00:00; module verification completion estimate: 100%.

Actual production `lake build Bell.CircuitRealization` succeeded, compiling both `Bell.ConeCircuits` and `Bell.CircuitRealization`. The unnecessary MeasurementSpans import in ConeCircuits was replaced by its actual dependencies StrategyMaps and DeterministicInput, with parent authorization and downstream coordination. All original mathematical statements are preserved. The axiom audit covers twenty-two cone and circuit results, including the final `circuit_section_mem_convexPVM`, and reports only `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx` occurs.

Earlier isolated sources were development checks. The successful production build and `ConeCircuitAudit.lean` establish the actual final dependency-chain outcome.

Cone proof repairs give explicit scalar-linearity algebra, closed intersections, finite subtype extensions, nonzero-factor cancellation, and two-case finite-index cardinality reasoning. Circuit realization repairs explicitly unfold output sums, instantiate equivalence sums, simplify the identity scalar homomorphism, and convert subtype cardinalities. Definitions, assumptions, and conclusions are unchanged.

Adversarial mathematical review: nonnegative normalized weights have equal side sums of time coordinate one half, so both sides have nonempty positive support. An extreme weight admits no nonzero balanced mass-zero perturbation on its support. Injecting support coefficients into H × ℝ bounds total support by dim(H)+1 ≤ 4. If one side is a singleton null ray, every opposite component lies on the same exposed ray. Two distinct opposite active indices then give an explicit nonzero balanced mass-zero perturbation, ruling out the alleged one-versus-three case. Hence each side has at most two active rays. No numerical enumeration or general-position assumption occurs.

For physical realization, singular common states are handled by the existing product-locality proof. Invertible common states are whitened using actual two-qubit purification, preserving the steered table. Null determinants and a proved bound on nonzero outcomes produce real PVMs; finite coarsening restores every original declared output label. Inactive rays may map to the fallback label because their effects are zero. The compact target is the ordinary PVM convex hull, so closed-hull transfer yields finite shared randomness rather than merely a limiting simulation.

The generic realization theorem assumes fallback labels for each input; it does not silently construct an output in an empty type. Valid uses must supply these labels from their own architecture hypotheses or normalization arguments.
