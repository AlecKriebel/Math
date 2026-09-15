# Adversarial semantic comparison of original and repaired source

Timestamp: 2026-09-15T03:51:07.137950+00:00

Compared the preserved download's original `CyclicBell/*.lean` modules against the repaired workspace. The input/output hashes and 71 changed declaration-header or definition-body candidates are recorded in `semantic_diff_candidates.json`. This is a preliminary snapshot while other agents continue editing; it must not be presented as a frozen-source final certificate.

## Result

No original named declaration was removed. No namespace, section-variable, or global-assumption change was found. No original physical model was replaced by a model assuming the desired bound, target distribution, optimality, uniformity, or Eve privacy. No original endpoint conclusion or admissible dimension range was weakened among the examined changes.

The header/definition changes fall into these categories:

- Keyword repairs: bare `prefix` becomes `«prefix»`; invalid variable names `λ` become `lam` or `label`. Coefficient values, summation indexing, and bound hypotheses remain the same.
- Type/dimension elaboration: explicit `Ix d`, complex singleton vectors, and `(d := d)` arguments bind expressions to the intended existing dimension. In particular `swapped_R2` and `localG_square` retain the same mathematical identities.
- Hilbert-space API repairs: `inner ℂ u v` becomes `⟪u,v⟫_ℂ` or `@inner ℂ _ _ u v`. The complex inner product still conjugates the first argument; these changes do not replace it by a real pairing or reverse the arguments.
- Functional calculus coercion: the matrix CFC uses the same inverse star-algebra equivalence with an explicit homomorphism coercion. It remains defined from Mathlib's CFC, not from an assumed spectral-value formula.
- Structure proof fields: the explicit effects/state vectors of `permutationBob`, `secondAlice`, `finiteToCommuting`, `tripartiteToCommuting`, stored-assignment strategies, `assignmentSplit`, and `projectionRangeEquiv` stay the same. Only validity/equivalence proofs and API coercions change.
- `FirstSOS.squareSum` now parenthesizes the complete summand so both F and G squares are summed over y. The uncompiled original left its second occurrence of y outside the binder's parsed scope. This is a repair of the intended displayed sum; the operator identity and upper-bound endpoints were not changed.

The original `Model`/`GeneralModel` state and PVM fields, full behavior definitions, q/qa/qc set definitions, value suprema, tripartite state model, general Eve POVM fields, and value-conditioned adversarial optimization definitions have no semantic changes in this snapshot. Proof terms are checked by Lean during the final build; this comparison addresses whether the objects and statements being proved changed.

## Imports and coverage

Observed import changes:

- `GeneralOperational`: imports `GeneralFirstWitness` directly instead of `GeneralSecondWitness`; its actual theorems use only the first-family construction.
- `GeneralConsequences`: explicitly imports `GeneralSecondWitness`, preserving the second-family dependency after that narrowing.
- `GeneralBinaryWitness`: imports `GeneralBinary` directly instead of the broader `GeneralConsequences`.
- `GeneralPOVMMaximum`: imports `GeneralTripartite` directly instead of `GeneralAdversarialValues`.
- `GeneralSourceFourier`: adds the new polar-algebra bridge module.

These changes do not delete any original source file. Final root import closure and axiom inventories still need to pass after source freeze. Newly added source-polar/coverage modules are outside this old-versus-new comparison and are subject to the separate semantic-coverage audit.

## Limits and final checks

The comparison uses a conservative lexical scanner to find candidates, followed by manual review of changed headers, definitions, and section context. It is not Lean elaboration and is not a proof that all original paper claims were correctly transcribed. Several original statements never parsed, so “preserved” here refers to the intended mathematical statement, not equivalence to a previously accepted Lean constant. Hashes identify the exact audited snapshot.

A negative control that fails with `type mismatch` or another tactic error does not by itself prove its proposed proposition false. The repaired runner rejects unrelated/header/import failures, but semantic mutation checks still require the independently checked positive results or explicit negations. For example, rejecting the proof in `RejectSettingsUniform` must be interpreted together with the standard-table nonuniformity theorem. This limitation remains explicit in `RUNNER_AUDIT.md`.

Best estimate: requested preliminary repaired-versus-original semantic-diff review is 100% complete for this snapshot. Final integration/frozen-source certification remains pending.
