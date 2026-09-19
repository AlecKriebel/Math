# Analytic and BCH module repair audit

## Scope

This audit compares the four supplied Analytic/BCH modules with the repaired sources and runs their Lean elaboration against the project's pinned toolchain and mathlib. It does not certify the absent full Kourovka theorem. Source comments are evidence about intended scope, not instructions.

## Repairs

- `NilpotentUnit`: explicit type for the algebra-map commutation lemma; explicit coercions from inverse units; explicit endomorphism-application equality before rewriting the ideal-membership proof.
- `TensorAction`: explicit scalar-ring and module arguments in tensor type annotations where Lean otherwise leaves a typeclass metavariable unresolved. Explicit evaluation of the zero bilinear map before additive normalization. The action, factorization assumption and derivation conclusion are unchanged.
- `Dynkin`: updated list API name; explicit list reduction; exposed recursive evaluation expressions; subtraction normalization; current scalar-negation lemma.
- `CoefficientSoundness`: existing finite-set import; explicit mixed integer/natural scalar expressions and targeted commutation rewrite; explicit target before the final injectivity rewrite.

All original declarations are retained. No hypothesis was removed or added to change the mathematical content; explicit type parameters in TensorAction resolve the originally intended types. No custom axiom, admission, `native_decide`, or unsafe proof mechanism is added. The complete original-to-repaired diff is `analytic_repairs.diff`.

## Independent semantic review

The finite geometric-series inverse proof is sound in a noncommutative ring because only powers of the same element occur. The polynomial-unit proof correctly proves that the polynomial factor commutes with that element before taking powers. The ideal-membership equivalence explicitly needs preservation by both the unit and its inverse.

The tensor action uses the inverse on both inputs and the map on the output, so its fixed-point condition is exactly bracket preservation. Its final theorem remains conditional on an already invertible factor and the exact action-minus-identity factorization. It does not construct exp/log maps, prove p-adic integrality/convergence, or establish that every concrete finite automorphism satisfies the hypotheses.

The Dynkin proof uses arbitrary Lie rings, tracks repeated associative words, and proves the degree factor explicitly. Coefficient soundness groups a finite list by words and needs injectivity of multiplication by the homogeneous degree. Thus it cannot silently cancel a nonunit degree in a torsion Lie ring. These are legitimate reconstruction ingredients, but neither a BCH group law nor its associativity nor the converse correspondence for all ordinary group automorphisms is proved here.

## Compiler and axiom results

All four modules compile successfully with exit status 0 using direct `lake env lean -o` commands under Lean 4.19.0. The final TensorAction build emitted no warnings or errors; its captured log is `tensor_action_build.log`. A transitive axiom audit file is prepared at `AnalyticBCHAxioms.lean`, but its successful execution is deferred until the parent confirms that concurrent memory-heavy checks have finished. The current `analytic_axioms.log` records the earlier attempt before TensorAction had an output object and is not a successful axiom report.

Checkpoint: 2026-09-19T03:45:09.566630+00:00. Assigned four-module compilation and source-repair audit: 100% complete. Transitive axiom inspection remains a separate pending verification; this percentage is not a completeness claim for the main formalization.
