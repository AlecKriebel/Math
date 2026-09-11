# Separator proof repair review

Checked with the pinned Lean 4.19.0 project toolchain on 2026-09-10.

## Scope and semantic preservation

The original Witness, SOSAlgebra, ProjectiveSOS, and ProjectiveBound theorem statements and hypotheses are preserved. `separatorArchitecture` is now an `abbrev` with the identical structure value; this exposes concrete finite input/output sizes to numeral instance synthesis. No additional mathematical assumptions were introduced.

Witness repairs explicitly reduce complex numeral conjugation, reduce the three auxiliary Born expressions to the concrete effects, and normalize the four real correlation equalities. The witness remains an actual positive normalized complex density matrix with positive normalized local POVMs, not an assumed probability table.

SOSAlgebra repairs reorder dummy finite indices after distributing the Gram factors. This does not commute noncommuting operators: every operator product remains `(W i).conjTranspose * W j`. The weighted-square theorem uses nonnegative real pivots and positivity of state expectations.

ProjectiveSOS repairs real scalar simplification at the complex matrix-entry level. Replacing the broad `Algebra.smul_def` rewrite by `Complex.real_smul` preserves the same matrix scaling while avoiding premature expansion into matrix multiplication. Both operator certificate statements quantify over arbitrary five Hermitian involutions, including scalar involutions.

ProjectiveBound repairs distribution/reordering of weighted Born sums, concrete vector indexing, and complement equalities. All three possible zero-effect positions of a ternary qubit PVM remain represented. The CHSH sign convention groups Alice labels 0 and 2 into +1 and label 1 into -1; it therefore applies to arbitrary ternary PVMs on the first two inputs, including deterministic/zero-effect degeneracies.

## Verified artifacts

- `witness.log`: successful production build of Bell.Witness.
- `sos_algebra.log`: successful production build of Bell.SOSAlgebra.
- `sos_certificate.log`: successful production build of the unchanged exact rational 144-entry LDL factorization (independent agent).
- `projective_sos.log`: successful production build of Bell.ProjectiveSOS.
- `separator_axioms.log`: the witness and SOS theorem dependency closures contain only `propext`, `Classical.choice`, and `Quot.sound`.

The overall numerical PVM bound is 289/10, not a claim that this is the exact optimum. Its comparison against the witness and paper upper bound is proved using rational inequalities and `sqrtTwo_sq`.

ProjectiveBound production build passed (`projective_bound.log`). The final axiom report also covers `projective_strategy_rational_upper`, `projective_global_upper_bound`, `three_by_two_separation`, and `witness_margin_over_projective`; all depend only on the three standard axioms listed above. The separator branch is 100% complete at this checkpoint.
