# Raw coefficient table repair and validation-harness review

Date: 18 September 2026.

## Scope

Review only of `Kourovka/TableCertificate.lean`, its raw/table definitions, and the Python validation harness. No changes to mathematical data, coefficients, matrix witnesses, or the asserted table equality.

## Repair

Split the comparison into 31 exact row equalities, each proved by Lean 4.19's `decide +kernel`, then assembled the original full theorem using `List.flatMap_cons` and the row equalities. The row definitions preserve the complete range, coefficient formula, zero filtering, and list order. Exported row literals only specify the checked propositions; their correctness is established by the Lean proofs, not trusted Python generation.

The initial single full-list `decide +kernel` attempt was interrupted after approximately five minutes: kernel-reduction caching consumed about 8.5 GB of swapped memory. Row splitting bounds each kernel check. `set_option Elab.async false` also prevents concurrent theorem elaboration defeating that bound. The successful-build command and measurements will be recorded below.

This is not `native_decide` and does not introduce a compiler-evaluation axiom. The local Lean implementation (`Lean/Elab/Tactic/ElabTerm.lean`, `evalDecideCore.doKernel`) constructs the ordinary `of_decide_eq_true` proof and installs a kernel-checked auxiliary lemma.

The repaired module compiled successfully (exit 0) using:

```
lake env lean -j1 -o .lake/build/lib/lean/Kourovka/TableCertificate.olean Kourovka/TableCertificate.lean
```

The unchanged final statement elaborates as `Kourovka.Raw.reconstructedTerms = Kourovka.exportedTerms`. The actual transitive `#print axioms` result is `[propext]`, with no admission or native-evaluation axiom. See `table_certificate_build.json`, `TableCertificateAxioms.lean`, and `table_certificate_axioms.log`. The successful run took approximately one minute; sampled resident memory stayed around 1.7 GB (not an instrumented exact maximum).

## Independent harness review

- The default runner deliberately exits nonzero because the final unconditional finite-group theorem is absent. It does not equate compiling draft milestones with solving the formalization task.
- `Challenge.ExactOrders` and `Challenge.NotebookAffirmative` are proposition definitions, not closed proofs. They use standard `MulAut`, and the package explicitly forbids substituting the additive coordinate group for the required BCH group.
- An additional source scan found no executable project `axiom`, `opaque`, `unsafe`, `elab`, `run_cmd`, `initialize`, or kernel-bypass constructs. The single `ambient_calc` macro expands ordinary `simp`, `ext`, `fin_cases`, `norm_num`, and `ring` tactics; it does not manufacture unverified constants.
- The source scanner rejects admissions, project axioms, native proof evaluation, unsafe declarations, and kernel-check disabling patterns. It explicitly describes itself as a static text inventory, not a Lean parser or complete elaborated declaration inventory.
- Actual axiom reports are required for every selected named root; missing, duplicate, unexpected-root, or disallowed-axiom reports cause rejection. Allowed axioms are the standard `propext`, `Classical.choice`, and `Quot.sound`.
- `python3 scripts/check.py --self-test` passed: four source-rejection controls and four axiom-output rejection controls, plus the positive parser control. These validate runner behavior only.
- The source-hash and dependency-pin checks help provenance, but cannot replace statement review or kernel checking.
- Minor hardening limitation: dependency cleanliness uses `git status --porcelain --untracked-files=no`, so untracked source files in a dependency are not rejected. There is no evidence this was exploited, and this is not a defect in Lean's kernel. This gap was subsequently repaired and tested; see `runner_repair.md`. Publication should preserve the pinned dependency provenance and avoid claiming an independently verified compiler bootstrap.

## Completion estimate

Table proof repair and scoped audit: **100% of this bounded task**, with actual kernel acceptance and transitive axiom inspection. Full formalization: explicitly incomplete; this local repair does not discharge the absent BCH group and full automorphism count.
