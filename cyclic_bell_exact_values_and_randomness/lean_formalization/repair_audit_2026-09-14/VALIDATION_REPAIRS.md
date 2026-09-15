# Validation repair audit

Checkpoint: 2026-09-15T04:02:23.149811+00:00. Assigned scope approximately 75% complete: all 25 controls inspected and preflighted; seven proof repairs are being rechecked; actual root-import run remains pending the umbrella olean.

## Method

Only validation/*.lean source files were edited. No theorem targets changed. No validation scripts were modified. The umbrella `CyclicBell.olean` was not yet available, so temporary copies in validation_preflight replaced only `import CyclicBell` with compiled GeneralStatements, AdversarialStatements, Regression and GeneralCoverageSourceWeyl imports. These logs are explicitly preliminary and are not presented as actual umbrella-import validation. Other existing direct module imports were preserved.

## Repairs

- AcceptGeneral: its second-family upper bound needed explicit conversion/normalization of real 5+1 to 6.
- AcceptModels: the qa second-augmented value similarly needed explicit cast/numeral normalization.
- RejectConjugation and RejectFirstNormalization: replaced mismatched uses of the correct bridge/attainment theorem with simplification by an already proved negation of the exact target.
- RejectGeneralSwap and RejectSettingsUniform: replaced a contradiction attempt containing duplicate negations / an attempted proof by the negation itself with simplification by the exact checked negation. The revised diagnostic should be the false goal itself, not an unrelated term-type mismatch.
- RejectClosureSliceOrder: aesop reached its maximum rule-application depth. This is not valid mathematical rejection evidence. Replaced the search with direct simplification by closure_before_slice_control.2, which is the checked negation of this exact topological example.

## Meaning of rejection controls

Every rejection file intentionally states a false mathematical target. Failure of a proposed proof is only a mutation smoke test, and is not by itself a proof of falsity. The source library provides the mathematical evidence: actual value/normalization theorems, proved nonuniformity and nonprojectivity, essential conjugation, the wrong-factor negation, or the explicit source coefficient formula with nonzero unit phase.

The closure-order control is a simple topological counterexample, not itself a theorem about quantum model closure. The actual quantum closure-before-slice definition is checked independently by the exact `rfl` contract in AdversarialStatements. No type mismatch here is being represented as an independent proof that a mathematical target is false.

## Initial preflight

Five acceptance files: AcceptPhysical, AcceptAdversarial and AcceptSettings passed; AcceptGeneral and AcceptModels reported the two normalization errors above.

Twenty rejection files: all rejected, with no missing identifiers/imports in the completed compiled-module preflight. The aesop rule-depth warning in RejectClosureSliceOrder was identified and repaired, so that original run is explicitly invalid as final negative-control evidence. Initial logs for the five strengthened rejection proofs are superseded by their repair reruns.

## Repaired preflight and direct-import checkpoint

2026-09-15T04:05:02.823109+00:00 — assigned scope approximately 90% complete. Repaired preflight: 5/5 accepts compile and 20/20 rejects fail for intended proof reasons, with no remaining resource warning. The five rewritten negative proofs all reduce their exact targets to `False`.

Actual `lake env lean validation/<file>.lean` runs have now passed for all nine files that directly import their required modules: AcceptSettings plus RejectAnchorQubitGap, RejectGeneralCoefficients, RejectGeneralNormalization, RejectGeneralSwap, RejectNormalization, RejectSettingsNormalization, RejectSettingsUniform and RejectUniform. Each negative run was checked with the existing `check.Runner`, including exit code, resource/API rejection rules and error location inside the sole example proof. Exact commands, hashes and logs are in validation_actual/<stem>/result.json and 001.log.

All 49 example statements across the 25 files remain identical to the downloaded originals, ignoring whitespace. The comparison is recorded in validation_statement_preservation.json. Actual runs of the remaining sixteen root-import controls await CyclicBell.olean; their repaired temporary-import preflight has passed.

## Final actual-file result — 100% assigned validation scope

2026-09-15T04:11:00.568138+00:00 — all **5 acceptance files compile**, and all **20 rejection files fail for permitted proof diagnostics inside their sole example proof** under the existing fail-closed Runner. Every tested file's SHA-256 still matches its current source. Exact per-file commands, statuses and hashes are consolidated in validation_actual/SUMMARY.json; individual compiler output is in each stem's 001.log.

To avoid coupling these controls to unfinished additional coverage, the sixteen blanket umbrella imports were narrowed to the compiled modules that supply the same declarations. Parent explicitly agreed. This changes no test target and no mathematical assumption. The official check.py still independently builds the entire CyclicBell umbrella before running the controls, and the static import graph includes its coverage modules.

Four final negative controls (adversarial uniform bound, closure value, reduced model value, purification norm) initially emitted Lean's bare `linarith failed to find a contradiction`, which the diagnostic validator does not recognize. The validator was preserved. Each proof now derives the exact target's negation from the library's positive bound/value/normalization theorem and then simplifies the false target to `False`. All four reruns passed the intended-rejection checks. Their rejected initial diagnostic records remain in validation_actual/<stem>/initial_diagnostic.

Final statement-preservation comparison again confirms all 49 example signatures are unchanged from the downloaded package. No source targets were weakened, no tests deleted, and no scripts edited. Benign unnecessary-sequence-focus lint warnings remain in the two repaired acceptance proofs; no resource/API/syntax errors or depth warnings remain in final logs.
