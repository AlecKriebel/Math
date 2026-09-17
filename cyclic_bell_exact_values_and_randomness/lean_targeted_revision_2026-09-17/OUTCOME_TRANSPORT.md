# Outcome-convention transport

Checkpoint: 2026-09-17T13:32:56Z. Assigned targeted scope: 100% complete.

Added only `lean_formalization/CyclicBell/GeneralOutcomeRelabeling.lean`: 6 definitions and 24 theorems. No existing physical definitions were changed. Reviewed the independent review's `REPAIR_PLAN.md` and `permutation_review.md` before implementation.

## Verified scope

- `negateMeasurement_encoded` proves that the existing outcome-negated PVM encodes the adjoint of the original observable. Measurement and strategy negation are involutive.
- `negateBobOutcomes_behavior` proves the full finite-dimensional Born table changes by `b ↦ -b`, for arbitrary input types and finite local coordinate types.
- `secondAdjointFourier_opposite_mode` identifies the alternate Fourier sum with the adjoint of the original opposite mode.
- `secondAdjointValue` explicitly adjoints Bob in every Fourier term and the extra Bob setting. `secondAdjointValue_eq_relabel` and `secondAdjointValue_negateBob` prove exact value transport. The universal upper bound and `secondAdjointPermutation_attains` give the value `d+1` for every `d≥2` and every permutation. `secondAdjointPermutation_maximal` compares this witness against every finite-dimensional competitor using the alternate functional on both sides.
- `secondAdjointPermutation_bob_encoded` and `secondAdjointPermutation_behavior` explicitly instantiate adjoint encoding and full outcome transport for the actual second-family witness, including the extra setting.
- `relabelOutcomeTable_range`, `observedMaxEntry_relabel`, and `relabelOutcomeTable_uniform_iff` prove preservation of entry sets, their supremum, and uniformity for arbitrary pairs of bijective local output relabelings. `observedMaxEntry_attained` and `le_observedMaxEntry` verify this finite supremum is the genuine attained maximum.
- `negateBob_fixedGuessSuccess`, `observedMaxEntry_eq_bestFixedGuess`, and `negateBob_bestFixedGuess` connect that maximum to the existing physical fixed-guess construction with one-dimensional Eve, and prove preservation under Bob negation. These are not claims about arbitrary quantum-Eve optimization.
- For the final-swap witness and `d≥4`, `secondAdjointSwap_nonuniform`, `secondAdjointSwap_observedMaxEntry`, and `secondAdjointSwap_quantitative` preserve target nonuniformity, the observed maximum, and the manuscript's explicit positive bias lower bound.

Changing output labels alone is not asserted to preserve an unchanged arbitrary Bell functional. The alternate functional above is explicitly transported. This targeted module makes no assertion about arbitrary-Hilbert-space optimization of that alternate functional; its maximality theorem covers every finite pair of local coordinate spaces.

## Validation

From `lean_formalization`, using the pinned toolchain:

```sh
PATH="$HOME/.elan/bin:$PATH" lake build CyclicBell.GeneralOutcomeRelabeling
```

Succeeded; the `.olean` is available. Evidence: `outcome_build.log`. Only unused-section-variable linter warnings remain.

Ran a focused `lake env lean --stdin` import and `#print axioms` on the generic encoded-adjoint theorem, the cyclic encoded-adjoint theorem, alternate maximality, attained maximum, arbitrary relabeling maximum, best fixed guess transport, nonuniformity, and quantitative target bias. All eight report exactly `propext`, `Classical.choice`, and `Quot.sound`; evidence: `outcome_axioms.log`. No root build or global axiom-inventory build was run by this subtask. Parent integration still must include the new module in the final root build and complete axiom inventory.

No placeholders, new axioms, native trust shortcuts, manuscript changes, commits, or external communications were introduced by this subtask.
