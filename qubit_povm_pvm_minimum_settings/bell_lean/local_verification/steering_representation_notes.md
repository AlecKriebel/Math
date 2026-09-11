# Mixed-state steering and full-rank pure realization audit

Checkpoint: 2026-09-11T02:01:51.525902+00:00; module verification completion estimate: 100%. All ten theorem axiom sets contain only `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`.

The actual `Bell.SteeringRepresentation` module compiles with its real ProductLocality and QuantumCompactness imports. All original definitions, hypotheses, and theorem conclusions are retained. Compatibility repairs explicitly evaluate finite sums of matrix entries and unfold State.amplitude for the Gram-row identity. The nonzero full-rank marginal proof now explicitly regroups nonsingular inverse cancellation and rotates matrix traces with the correct multiplication association.

The density matrix is decomposed into all Gram rows, so mixed states are represented without assuming a selected pure eigenstate preserves an entire behavior. Bob's steered operators are positive, have the same normalized reduced state, and reproduce every Born probability under Alice's original measurements. A singular reduced state belongs to the projective convex hull by the independently compiled product-locality theorem. A behavior outside that hull therefore has an invertible reduced state and is realized by the two-qubit purification construction, preserving the complete behavior table.

For the positive-marginal result, a nonzero PSD local effect conjugated by the full-rank coefficient matrix remains PSD and nonzero; its trace is strictly positive. Invertibility is used explicitly in both inverse cancellations. This theorem does not assert positivity for a zero effect or a rank-deficient coefficient matrix.
