# Independent re-review: Bob outcome inversion and transported second functional

Date: 2026-09-17. Scope completion estimate: 100% of the assigned source/statement audit. Compilation and axiom replay belong to the coordinating reviewer.

Snapshot reviewed: `snapshot/lean_formalization` in this review directory. No snapshot files were edited and no builds were run by this reviewer.

## Verdict

**Pass, conditional on the separate clean build and axiom audit.** I found no incorrect sign, nonphysical relabeling, circular maximality assumption, improper supremum use, or overclaim about Eve optimization. The previously identified Bob-adjoint outcome-inversion coverage gap is now closed by explicit theorems on actual PVMs and Born probabilities. The manuscript sentence at `reference/manuscript/main.tex:1014` is covered directly by `secondAdjointPermutation_bob_encoded` and `secondAdjointPermutation_behavior`.

The added value/maximality statements correctly transport the Bell functional as well as the realization. They do **not** claim that replacing Bob by his adjoints leaves the original, unchanged Bell functional invariant. This distinction is mathematically necessary.

## Concrete checks

All source references below are relative to `snapshot/lean_formalization`.

### Actual measurement and Born definitions

- `CyclicBell/GeneralModel.lean:14` requires a positive trace-one state; `:19` requires positive, complete, idempotent, orthogonal effects; `:26` encodes positive-character outcomes. Its `:34` and `:46` are the actual tensor Born expectation and behavior.
- `CyclicBell/GeneralPhaseTables.lean:23` defines `negateMeasurement M` by effects `M.effect (-b)`. Positivity, completeness, projectivity, and orthogonality are discharged from the original PVM and the bijectivity of negation. There is no change of physical state, complex conjugation of effects, or extra restriction on ranks/dimensions.
- `CyclicBell/GeneralOutcomeRelabeling.lean:16` proves the encoded observable of that PVM equals the original observable's conjugate transpose. The proof uses the Hermitian PVM effects through `measurement_spectral_star`, the character identity `chi_star`, and finite-sum reindexing. Thus the adjoint claim is derived, not included as a field defining the relabeling.
- `:31` applies the PVM transformation to **every** Bob input, including `none`; `:36` proves actual Born probabilities satisfy `p_new(a,b|x,y)=p_old(a,-b|x,y)`. `:40` proves involutivity. The cyclic specialization at `:82` and `:88` has the same physical meaning for every Alice/Bob input and every permutation.

I compared the foundational `GeneralModel.lean`, `GeneralPhaseTables.lean`, `GeneralOperational.lean`, `GeneralSecondBound.lean`, and `GeneralSecondWitness.lean` against the previously audited delivered package; all five are byte-identical. The new bridge has not silently weakened their definitions or changed the original second-family functional.

### Conjugation and Fourier signs

- `GeneralOutcomeRelabeling.lean:47` defines the new Fourier combination as `sum_y chi(l*y) B_y†`, retaining the plus character. `:50` correctly identifies this as the adjoint of the **opposite** original Fourier mode, `Bhat(-l)†`, rather than `Bhat(l)†`. This accounts for coefficient conjugation under adjoint.
- `:57` defines the transported second functional with the original `star (generalLambda l)` coefficients, adjointed Bob observables inside the Fourier terms, and an adjoint on the added Bob observable as well. Alice observables and the state are unchanged. This is exactly the pullback of the original functional under Bob-output negation.
- `:62` proves `secondAdjointValue s = secondValue (negateBobOutcomes s)`. `:68` then proves the correct joint transport law `secondAdjointValue (negateBobOutcomes s) = secondValue s` using involutivity. There is no theorem claiming `secondValue (negateBobOutcomes s) = secondValue s`.
- As an adversarial sanity check on the distinction, for the displayed forward weighted-cycle witnesses in dimensions greater than two, blindly adjointing Bob and retaining the original positive-character functional changes the operator products' shift support. There is no reason for the unchanged score to remain maximal. The new theorem's explicitly transported functional avoids precisely that incorrect assertion.

### Universal finite-dimensional upper bound and attaining witness

- `:72` applies the already proved universal `second_physical_upper` to the relabeled physical strategy. It quantifies arbitrary finite Alice and Bob coordinate types; no fixed-dimension or witness-class assumption is introduced.
- `:78` defines the alternate witness by the actual relabeling operation. `:93` proves its score is d+1 from the original witness's proved attainment and the transport law.
- `:99` compares **the transported functional on both sides** against every finite-dimensional competing strategy. The proof combines the unconditional upper bound with the explicit witness score. Neither attainment nor maximality is an assumption of the strategy constructor.
- These new maximality endpoints are finite tensor statements. The module does not assert or prove a new literal q/qa/qc supremum equality for the alternate convention. That stronger claim is unnecessary for the manuscript's outcome-inversion sentence and is not advertised in the new coverage row. It should not be inferred as an additional formally checked endpoint merely from the theorem name.

### Maximum entries and guessing claims

- `:105` defines a plain bijective relabeling of any real table. `:109` proves equality of its value ranges using both permutations and their inverses, so this is a general reindexing theorem rather than a probability-specific assumption.
- `:122` defines `observedMaxEntry` as `sSup` of that finite range. `[NeZero d]` ensures the index type is nonempty; `:124` explicitly proves attainment by finite-range membership, and `:130` supplies boundedness for each lower comparison. This avoids relying on default values of real suprema of empty or unbounded sets.
- `:133` and `:146` correctly prove observed-maximum preservation. `:138` independently proves equivalence of uniformity under bijective relabeling.
- `:152` transports the **fixed deterministic guess** `(a,b)` to `(a,-b)`. Its `fixedGuessSuccess` is not an invented score: `GeneralOperational.lean:141` is the trace pairing with an explicit one-dimensional Eve instrument, and `:154` derives the Born-entry identity. I also inspected `CyclicBell/Guessing.lean:82`, where that conditional state is genuinely defined by adjoining a trivial Eve, sandwiching with the joint projector, and tracing AB.
- `GeneralOutcomeRelabeling.lean:162` equates the observed maximum only with the best deterministic fixed guess, and `:173` transports that quantity. Neither theorem identifies this with a general Eve POVM optimum or with the value-conditioned adversarial optimum across all realizations. The module comments and `COVERAGE.md:52` maintain that distinction.
- `:181`, `:190`, and `:199` transfer nonuniformity, the observed maximum, and the quantitative lower-bound witness respectively. The last theorem explicitly chooses `(a,-b)` from the original witness and uses double negation to recover the old table entry. It asserts existence of a biased outcome, not that the displayed lower bound is the exact maximum.

### Import and statement visibility

`CyclicBell.lean:1` imports `GeneralSecondCompletionStatements`. That module imports `GeneralOutcomeRelabeling` and exposes expanded observable and Born statements at lines 52–71, including the full transported functional with its added term. `CyclicBell/AxiomAudit.lean:1238` onward contains entries for the new relabeling definitions/theorems; the coordinator should confirm these are actually checked in the clean replay. The updated claim ledger and `COVERAGE.md:51` describe the same scoped transport claims as the code.

## Remaining boundaries

No repair is requested for this assigned module. This review certifies statement correspondence and proof mechanism, subject to the independent build; it does not replace the other reviewers' checks of second-family moment formulas, canonical polar existence, or the rest of the paper. The module proves the explicit mathematical outcome convention in the bundled manuscript; it does not independently establish the bibliographic claim that a particular external source appendix uses that convention.
