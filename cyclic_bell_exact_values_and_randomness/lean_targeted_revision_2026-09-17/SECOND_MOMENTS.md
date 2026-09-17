# Second-family complete first moments

2026-09-17. Completion: 100% of this bounded proof task. Target: the missing complete complex first-harmonic matrix and local moments in manuscript `thm:second`, identified by `lean_independent_review_2026-09-16/permutation_review.md` and item 1 of `REPAIR_PLAN.md`.

Only the new production file `CyclicBell/GeneralSecondMoments.lean` was added. Existing definitions, proofs, imports, root modules, inventories and reviewer documentation were not edited by this agent. The module imports the existing second-family witness and physical behavior bridge.

## Statements

All nine new theorems use namespace `CyclicBell.General`. Their only dimension hypotheses are `[NeZero d]` and `2≤d`; permutations and input labels are otherwise arbitrary.

- `secondPermutation_correlator`: the full complex expectation at every reduced input pair is `generalLambda l * chi (-(l*y))`.
- `secondPermutation_extra_correlator`: the extra Bob column is `if l=0 then 1 else 0` for every Alice row.
- `secondPermutation_local_moments_zero`: every Alice and Bob local complex first moment is zero, including the extra Bob input.
- `secondPermutation_first_harmonic_matrix`: a single formula for all d-by-(d+1) entries, explicitly using the Alice/Bob fields of `secondPermutationStrategy`.
- `secondPermutation_first_harmonic_matrix_invariant`: equality of those complete complex expectation arrays for arbitrary permutations κ and τ.
- `secondPermutation_behavior_correlator`: the same exact formula for `probabilityCorrelator (behavior (secondPermutationStrategy hd κ))`, connecting it directly to the actual Born probabilities.
- `secondPermutation_behavior_correlators_invariant`: equality of the complete physical-behavior correlator functions for κ and τ.
- `secondPermutation_physical_local_moments_zero`: the local moment statements with the actual strategy's `.state.density` and encoded measurement fields.
- `secondPermutation_complete_first_moments`: one endpoint assembling all reduced correlators, the full extra column, and every density-based Alice/Bob local first moment.

## Derivation and scope

The encoded Alice/Bob operators are rewritten as their already proved concrete weighted cycles. The maximally entangled trace identity then gives the average of products of their weights. Permutation reindexing removes κ. Conjugating `secondWeight` produces `star(secondPrefactor l) * chi(l*j)` with the positive character sign. The shift identity and exact polar Fourier compression give the remaining factor `chi(-(l*y)) * d * generalLambda l * secondPrefactor l`. Unit modulus of the prefactor and d≠0 cancel exactly; the full complex phase is retained.

For the extra Bob setting, character orthogonality gives d when l=0 and zero otherwise; the zero-input prefactor is one. This works in composite dimensions and assumes no primality. Every local encoded observable is a weighted forward cycle, whose trace vanishes for d≥2. The physical Born-correlator bridge is proved through the existing trace identity and the actual pure-state density, not by defining a new proxy probability table.

These theorems concern all entries at first harmonic order. They do not assert invariance of every Fourier order or of the full joint distribution, which is deliberately nonuniform for the swapped witnesses. They assume neither Bell maximality nor a correlator formula. No chosen reference permutation, real-part weakening, special dimension, or extra coefficient-normalization premise remains in the endpoints.

## Verification

`lake env lean CyclicBell/GeneralSecondMoments.lean` completed successfully with exit 0 and no diagnostics after the local elaboration fixes. The narrow `lake build CyclicBell.GeneralSecondMoments` also completed successfully, producing the module's olean. All nine explicit axiom queries succeeded and list only `propext`, `Classical.choice`, and `Quot.sound`. Evidence is in `second_moments_build.log`, `second_moments_axioms.lean`, and `second_moments_axioms.log`. The integration owner owns the final root import, expanded statement examples, complete inventory and clean build.
