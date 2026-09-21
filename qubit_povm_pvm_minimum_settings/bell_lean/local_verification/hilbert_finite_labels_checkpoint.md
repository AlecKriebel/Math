# Composed source Hilbert and finite-label bridge checkpoint

2026-09-21 14:37 UTC. Completion estimate: 100% for this assigned bridge and its targeted validation; package-wide fresh certification is owned by the parent task and remains separate.

`Bell/HilbertFiniteLabels.lean` defines actual local operator effects on arbitrary finite-dimensional complex Hilbert spaces, with input-dependent arbitrary finite outcome types. Positivity, normalization, idempotence, and pairwise orthogonality are conditions on those source operators. The state is the actual source tensor-product density operator, and source probabilities are its Born trace against tensor-product effects.

Encoding the labels with `Fintype.equivFin`, applying the proved source-Hilbert isometric representation, and decoding the original labels produces a fixed-qubit strategy preserving the entire behavior table. Both POVM and projective cases are proved. The reverse constructor uses the actual Hilbert space of qubit coordinate vectors and preserves the entire table as well.

The raw source behavior sets quantify over the union of complex Hilbert spaces of local dimension at most two. `rawPOVM_eq_fixed`, `rawPVM_eq_fixed`, `convexPOVM_eq_fixed`, and `convexPVM_eq_fixed` identify these with the corresponding fixed-matrix finite-label sets. `at_most_two_input_equality` proves the main convex equality for at most two inputs per party. This does not assert equality of the raw POVM and PVM sets, nor raw equality for a single fixed one-dimensional source space.

`finite_source_projective_simulation` supplies a finite probability distribution over actual Hilbert projective strategies on qubit Hilbert spaces. One common finite random variable reproduces the complete original labeled behavior table. Input-dependent arbitrary finite labels remain unchanged. No nonempty-label hypothesis is added: normalized source strategies imply nonempty measured outcome types; explicit empty-label impossibility lemmas and zero-dimensional state impossibility contracts are included.

Validation completed:

- Targeted production build `lake build Bell.HilbertFiniteLabels`: exit 0, `hilbert_finite_labels_build.log`.
- All 13 anonymous examples in `validation/HilbertFiniteLabelContracts.lean`: exit 0, `hilbert_finite_label_contracts.log` (empty output).
- All 15 endpoint and reverse-constructor axiom queries in `HilbertFiniteLabelsAudit.lean`: exit 0, `hilbert_finite_labels_axioms.log`. Only `propext`, `Classical.choice`, and `Quot.sound` occur.
- Independent semantic review by the calculus audit agent accepted source operators, source tensor Born trace, complete-table representation, source projective branches, union scope, and empty-label handling.

The first contract run required opening the standard `ComplexOrder` scope for the explicit complex positive-semidefinite target expression. This was a notation/typeclass-scope correction; no statement, hypothesis, or production definition changed. Production and contracts are frozen for the parent task's fresh full verifier run.
