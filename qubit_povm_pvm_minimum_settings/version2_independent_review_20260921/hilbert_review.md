# Independent review: Hilbert-space and dimension correspondence

Checkpoint: 2026-09-22 00:49 UTC / 2026-09-21 Pacific. Completion estimate: **100% of this bounded audit**, not a mathematical probability of correctness. Reviewed source at HEAD `5ec53ad703c0aa6834f7b1f1b409a83c9c332eea`; all seven reviewed production modules match that commit. Production source was not edited. No earlier review reports were used to reach this assessment.

## Verdict

**No actionable correctness finding.** The new source model is genuinely a finite-dimensional complex Hilbert-space operator model. Its connection to the fixed-qubit matrix model is proved in both directions, with the dimension bound, tensor-product Born rule, outcome labels, and edge cases preserved. The combined finite-label simulation supplies a single finite random variable selecting a complete projective strategy on both sides. I found no circular definition, hidden same-state hypothesis, real-coordinate restriction, or substitution of scalar data for the physical model.

## Source-model audit

`Bell/HilbertCorrespondence.lean:16–58` defines source states as endomorphisms of the actual algebraic tensor product `E ⊗[ℂ] F`, positive for the source tensor Hermitian form and normalized by the linear-map trace. Local POVMs are positive endomorphisms summing to the identity; PVMs additionally have idempotent and pairwise orthogonal effects. The source Born rule is explicitly the real part of `trace(ρ * TensorProduct.map M N)`. None of those definitions invokes target qubit matrices or assumes a desired correlation-set equality.

The tensor Hermitian form is a legitimate finite-dimensional Hilbert tensor product construction. `HilbertCoordinates.lean:17–82` establishes the relevant Hermitian-form and definiteness properties in basis coordinates. `:88–112` identifies orthonormal coordinates with the given local inner products and proves the usual pure-tensor product formula. `:114–127` proves independence of both chosen orthonormal bases by tensor induction. Because the local spaces are finite-dimensional over complex numbers, use of the algebraic tensor product introduces no missing completion or infinite-dimensional trace assumption.

Positivity includes self-adjointness and nonnegative quadratic forms (`HilbertCoordinates.lean:32–63`), and is equivalent to matrix positive semidefiniteness. `HilbertCorrespondence.lean:70–115` separately proves state positivity, trace one, local normalization, idempotence, orthogonality, and the tensor Born-coordinate identity. Taking the real part in the source definition matches the existing matrix model exactly; it is not used to discard a problematic imaginary coordinate from a different physical rule.

## Embedding and unused complement

`IsometricCompression.lean:13–82` uses the rectangular isometry condition `V†V = I`, congruence `V A V†`, and complement `I − VV†`. It proves trace preservation, preservation of products on the embedded support, positivity/idempotence of the complement, and its annihilation of the embedded operators.

`IsometricCompression.lean:86–134` assigns that complement to exactly one declared outcome of each measurement. The explicit sum proof restores the full target identity; the idempotence and orthogonality proofs show this also works for PVMs. It does not add an undeclared output. In a one-dimensional source, the extra qubit direction may change projector ranks but has zero weight in the embedded state, so the existing outcome probabilities remain unchanged.

The product embedding is proved isometric, and its compression factors into the two local compressions (`IsometricCompression.lean:144–175`). The state and Born-rule constructions at `:191–209` therefore preserve every joint probability at once. `HilbertIsometry.lean:15–55` additionally constructs an actual complex linear isometry from the source space to complex two-dimensional Euclidean space and checks its coordinates, inner products, norms and injectivity. No real-state or real-measurement restriction appears.

## Reverse correspondence and the union over dimensions

`HilbertReverse.lean:11–85` reconstructs physical operators and states on `QubitSpace = EuclideanSpace ℂ (Fin 2)` by inverse basis-coordinate maps, proving the physical positivity, normalization and PVM conditions. `:95–112` proves equality of the Born tables and verifies dimension two.

`HilbertSimulation.lean:16–63` defines the independent raw behavior sets by existential quantification over allowed local spaces and source strategies. The forward inclusion uses the dimension-bounded embedding; the reverse inclusion chooses the actual two-dimensional qubit space. This proves equality for the **union of local dimensions at most two**. It does not incorrectly claim that every fixed one-dimensional carrier realizes all qubit behaviors. The corresponding convex-hull theorem follows at `:66–69` without an extra equality premise.

## Combined arbitrary finite labels and one shared mixture

`HilbertFiniteLabels.lean:19–176` defines arbitrary-label effects and strategies directly on the source Hilbert spaces. Encoding and decoding use the equivalence between each finite label type and its cardinality, with normalization and projectivity preserved. The forward composed embedding and reverse Hilbert reconstruction preserve the same labeled Born table (`:127–203`), rather than proving unrelated cardinal and Hilbert-space results without a combined bridge.

The endpoint `finite_source_projective_simulation` at `:232–242` returns one finite index type, one common nonnegative weight function summing to one, and one complete source projective strategy per index. Its equality is of the whole behavior function. The branch states may change, and their Hilbert spaces are complex qubit spaces, exactly as permitted by the paper's simulation claim. The raw-set correspondences and equality at `:244–290` retain both arbitrary finite label types and the independent Hilbert source model.

## Boundary cases

- Zero-dimensional local spaces are not excluded by a concealed hypothesis. `HilbertCorrespondence.lean:120–134` proves that a normalized source state forces each local finrank to be positive, since otherwise the joint trace is zero.
- Empty outcome types cannot carry a normalized measurement on the nontrivial spaces forced by the state. The selected output used for padding is derived from this fact (`HilbertCorrespondence.lean:136–181`). The combined model proves strategy emptiness explicitly for either party's empty outcome type (`HilbertFiniteLabels.lean:292–302`).
- A one-dimensional source is allowed and embeds correctly; the reverse correspondence is a union statement, not a fixed-one-dimensional surjectivity claim.
- Zero, identity, and repeated zero-probability effects are not discarded. A selected complement can alter an effect on unused space while leaving every observable probability unchanged.
- The combined simulation carries explicit `m ≤ 2` and `n ≤ 2` hypotheses. Its Hilbert embedding and raw-set equivalence themselves do not incorrectly require two inputs; only the Bell equality uses the setting restriction.

## Fresh independently written contract

I wrote and compiled `contracts/HilbertModelProbe.lean`, without copying the production contract files or earlier reviews. It checks:

1. Each zero-local-dimension hypothesis implies the source state type is empty.
2. The combined theorem yields an entrywise mixture whose two sides are expanded into the actual source **linear-map trace and tensor-map formulas**, rather than relying only on the name `behavior`.
3. Each branch is an actual Hilbert-space projective strategy with the original arbitrary output types; one common weight list reconstructs all input/output combinations.

Fresh command, executed from `bell_lean`:

```text
lake env lean ../version2_independent_review_20260921/contracts/HilbertModelProbe.lean
```

Result: exit code 0. All three probe declarations report only `propext`, `Classical.choice`, and `Quot.sound`. Exact output is preserved in `evidence/hilbert_probe.log`.

This contract imports the existing compiled modules and therefore is not a new clean rebuild of the entire proof development or Mathlib. The independent work here consists of source-level semantic review and a fresh expanded endpoint/boundary contract. Full-build provenance and the unchanged original equality proof are separate review scopes. No claim that every sentence of the physical exposition is individually formalized is needed for this verdict.
