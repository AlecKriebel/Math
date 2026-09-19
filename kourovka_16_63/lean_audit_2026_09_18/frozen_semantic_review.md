# Semantic review of repaired and refactored Lean sources

**Final source-review status: accepted. The final signoff below supersedes the earlier pending-freeze notes.**

## Finding

**The reviewed repairs preserve the original mathematical targets, definitions and strength. No hidden admission, custom axiom or substitution of a smaller automorphism set was found. The development still does not prove the final finite-group theorem.**

This supplements `repair_semantics_review.md` with the later frozen flag modules, integer evaluation helpers, embedding proof optimization, inner-witness refactor and integral-generation refactor. It is source review, not a fresh compilation or transitive axiom check. Build and axiom acceptance must come from the parent verification records.

The exact review snapshot is `frozen_semantics_snapshot.json`, including the original ZIP hash and hashes for 141 mathematical/root source files. `frozen_semantics_drift.json` records subsequent changes. At the parent's request, Integral, finite dependents, InnerRank and InnerScalarExtension were still permitted to receive repairs; this report requires a final addendum for those files before final release signoff.

## Preservation checks

The lightweight header comparison found 821 original explicit theorem statements and 865 current statements. Of the original 821, 815 are textually identical after whitespace normalization, including relocated declarations. The remaining six merely make previously intended types/coercions explicit:

1. inverse-unit coercion in `factor_mem_iff`;
2. scalar ring/module parameters in `fixed_iff_derivation_of_factor`;
3–5. scalar ring parameters on word spans and standard brackets in finite nilpotency;
6. `R := Int` on the adapted bracket in `diagonal_bracket`.

The 44 additional statements comprise 31 table-row lemmas, seven fast-evaluator soundness/transfer lemmas, four embedding-basis lemmas and two inner-witness helper lemmas. No original theorem was replaced by an unproved result-sized hypothesis. The header comparison is a source aid, not an elaborated theorem-equivalence checker; section variables and types were reviewed separately, particularly the scalar-kernel positivity/NeZero repair.

`frozen_data_integrity.json` confirms all of the following:

- RawCoefficients, ExportedData and Ambient.IntData remain byte-identical to the supplied ZIP.
- The scaled 199-entry sparse bracket is unchanged.
- The selected-row and rational inverse-coefficient witness data are unchanged after moving into InnerWitnessData.
- Both the finite-field generation DAG and integral generation DAG retain every original node definition exactly.
- Finite.LieAutomorphisms is byte-identical; the ordinary automorphism set is not narrowed.
- Challenge's ExactOrders and NotebookAffirmative proposition definitions are unchanged.

## Later proof mechanisms examined

### Ambient and embedding acceleration

FastBasis proves its integer evaluator equal to the actual sparse entry, then inducts over the complete term list. It preserves duplicates and zero-extended natural indices. Its generic base-change theorem derives results over an arbitrary commutative ring from `mapVec_terms` and `mapVec_unit`; it does not trust exported Python values or replace the bracket with an unconnected evaluator.

EmbeddingBasis checks the actual unimodular basis-change columns and derives the diagonal/embedding basis formulas from the existing maps. Optimized embedding shards still conclude precisely `EmbedCheck i`. They introduce every second input index, enumerate all of them, rewrite proved embedding/bilinearity/basis formulas, and finish with kernel reduction. They neither drop output coordinates nor sample a subset of basis pairs. Chunk00 retains the original direct route; the later chunks use the faster proved route.

The ambient Lie repairs expose integer cast compatibility and integer scalar simplifications. The original all-input Jacobi and Lie-structure conclusions remain unchanged.

### Inner witness and rational rank

The original 30 left-inverse row goals are now distributed across exactly 30 Row00–Row29 modules, with the same original declaration namespace and `LeftInverseCheck` propositions. `inner_entry_fast` is an equality for the actual scaled-bracket inner-column entry, obtained from FastBasis base change. Each row still quantifies over all 30 parameter columns, rewrites that equality and checks exact rational arithmetic. The aggregator imports all 30 modules and proves `leftInverse_all` by exhaustive index cases.

`extractor_innerMap` uses the same actual linear maps, with an explicit basis-vector lemma replacing a simplifier pattern that failed. Its injectivity conclusion is unchanged. Rational denominators remain in the rational field; no division was moved into a composite residue ring. The later rank/Jacobi wrappers remain subject to the final dependent-file addendum.

### Flag calculations and generation

Concrete's identities retain all original statements. Direct kernel reduction replaces unsuccessful coordinate tactic expansion for closed equalities; the two formulas with arbitrary scalar variables instead use actual bilinearity, alternating/skew identities and ring normalization.

Generation keeps its original DAG definitions, vector-value claims, fixed-vector and killed-vector claims, and final all-vector conclusions. Existing preservation/derivation predicate aliases are unfolded within proof bodies. For every field-division expression that is not kernel-computable directly, a local equality first proves the divisor nonzero and checks the equivalent modular multiplication using `div_eq_iff`. The original quotient is then rewritten to its checked residue. This is valid in the explicit field ZMod1009; it does not assume a general residue ring is a field or bypass inverse verification.

Rigidity's actual module compiles and all explicit statements match the original ZIP. Its repairs only expose predicate bodies/coercions and correct a comment. It still covers every flag-preserving linear equivalence and every flag-preserving derivation. The flag-preservation conditions remain explicit and are not conclusions of this module.

### Integral word generation

IntegralWords retains the original integral expression nodes, denominators, vector identities and nondivisibility facts in the original namespace. IntegralGeneration imports those established words, then performs the original generic scalar extension and p-adic generation arguments. Unit cancellation explicitly uses the inverse of a witnessed unit. The p-adic denominator-unit argument invokes mathlib's norm/divisibility characterization. No numerical certificate is accepted without a Lean proposition proving its required identity.

## Trust and publication limitation

The previously reviewed `decide +kernel` mechanism is ordinary Lean kernel proof reduction, distinct from native evaluation. Refactoring, serial scheduling and increased resource bounds do not introduce new mathematical assumptions. This source review found no admission/custom-axiom/native-proof bypass in the new mechanisms; the final transitive axiom report is still required to support a released trust claim.

Publication should distinguish two claims:

- If all actual project modules build and the axiom audit passes, the package is a **compiled, kernel-checked partial Lean development of the construction and supporting lemmas**.
- It is **not a full formalization of Kourovka16.63**, and its compilation does not formally verify the paper's final group-existence conclusion.

The missing work remains substantive: instantiate the complete Smith certificate/count for the actual derivation matrix; establish arbitrary quotient maps and the concrete integral exp/log correspondence; prove a finite BCH group with both directions of the ordinary group/Lie automorphism correspondence; and produce the unconditional ExactOrders/NotebookAffirmative witness. The final challenge declarations are still definitions of propositions, not proofs. The runner correctly retains `complete_formalization = false`.

## Pending final addendum

Review all mathematical-source hash changes after this snapshot, especially the permitted final dependent-module repairs. Append a final dated signoff with the final hash manifest. The source audit is complete for the frozen modules above, but final release signoff remains pending that addendum and the separate build/axiom evidence.

## Dependent-module addendum: Integral and rank wrappers

The accepted and frozen Integral/InnerRank/InnerScalarExtension/InnerScalarWitness sources were compared again with the original ZIP.

- Integral adds its direct Ambient.Lie import and specifies `R := Int` in the adapted-bracket statement. The integral embedding, Jacobi, Lie-ring structures and scalar-extension conclusions retain their original content.
- InnerRank still maps the actual 30 inner derivations, formed with the actual scaled bracket, into the full kernel of the actual derivation matrix. The generic Jacobi argument still establishes membership. Repairs expose sum expressions and subtype/map projections before applying existing linear-map laws. The dimension lower bound30 and rank upper bound931 are unchanged.
- InnerScalarWitness moves the original rational scalar-extension witnesses into a separate dependency module under the same namespace. It still requires an arbitrary field of characteristic zero and transports the checked rational left inverse itself. No modular-rank invariance is assumed.
- InnerScalarExtension imports that witness and retains the original map into the full matrix kernel and its characteristic-zero dimension/rank bounds. Only explicit subtype/coordinate reductions and the current `finrank_bot` lemma name changed.

No new mathematical hypotheses, smaller counted sets or weakened rank claims were introduced. These rank bounds alone still do not constitute acceptance of the full p-adic Smith certificate or establish the final finite kernel cardinality. Compilation success for these modules is recorded separately by their owning build agents.

Final finite-dependent freeze and final complete hash manifest are pending below.

## Finite-dependent addendum

The finite agent's frozen AdditiveLinear, BracketTrees, Coordinates, LieAutomorphisms and PadicQuotient sources preserve all original theorem statements. AdditiveLinear exposes the residue scalar cast before the original integer-linearity rewrite; BracketTrees uses the direct positivity theorem for a leaf; Coordinates normalizes the integer cast/divisibility result; PadicQuotient marks the existing p-adic functions noncomputable and normalizes the integer/natural cast in the kernel ideal.

LieAutomorphisms now factors its failed large structure literal through a private `scalarAutOfLinear` helper built with mathlib's `LieEquiv.ofBijective`. It uses the same actual `fromEntries` linear map, its original bijectivity witness and the original full bracket-preservation predicate. Its equivalences and final cardinality statement are unchanged. A local `irreducible` attribute prevents elaboration from eagerly expanding the 961-term definition of `fromEntries`; it does not change that definition, add an axiom, change the counted set or bypass kernel checking. Existing proved coordinate inverse identities still justify both inverse directions.

Accordingly, the earlier byte-identity observation for LieAutomorphisms applies only to the earlier snapshot. The final file is semantically preserved but now has the constructor repair above. The package still covers the entire Lie-ring automorphism set at this stage, while the ordinary group-automorphism correspondence remains absent.

## Final signoff: all mathematical sources frozen

Nilpotency and NearIdentity were reviewed after the parent confirmed successful actual-module compilation and the final source freeze. Nilpotency now expresses integer-power divisibility before converting it to the exact `ZMod (1009^1689)` cast statement and rewrites the vanishing scalar directly. This avoids asking for invalid no-zero-divisor scalar assumptions over the composite ring. The modulus, exponent1689, length847 bound and lower-central conclusions are unchanged. Its recursion/exponentiation limits only allow reduction of the actual large numeral. NearIdentity specifies the intended exponent when applying `pow_succ'`; its two-lattice power-divisibility statement is unchanged.

**Final semantic verdict: no weakened original theorem, changed target, hidden proof assumption, substituted automorphism subset, or altered construction/certificate data was found.** All additions are proved helper statements or definition/structure refactors linked to the original objects. The six explicit theorem-header differences remain the previously reviewed type/coercion clarifications; no further statement changes occurred. The current source has865 explicit theorem statements versus821 in the original draft.

Final evidence:

- `final_semantic_source_snapshot.json`: hashes of all142 mathematical/root Lean modules, captured after the parent's final freeze;
- `final_statement_comparison.json`: final explicit theorem-header comparison;
- `final_source_trust_scan.json`: all142 mathematical sources scanned, zero admission/bypass rejections;
- `final_mathematical_repairs.diff`: complete original-ZIP-to-final-source mathematical diff, including new and relocated modules.

A second read of every source hash immediately after generating the final audit confirmed no drift. The new private LieEquiv constructor and local irreducibility annotation were specifically reviewed and do not alter kernel trust or the final counted set. Historical “uncompiled” comments are explained by the current documentation and do not override actual build evidence.

This is final **semantic source** acceptance, conditional only on matching the recorded hashes. Root import compilation, transitive axiom inspection and reproducible build records are separate acceptance dimensions owned by the parent verification. This review does not itself certify a fresh root build.

The publication limitation is unchanged and non-negotiable: **this is a repaired partial Lean development, not a full Lean formalization of the paper or an unconditional formal solution of Kourovka16.63.** The full concrete Smith count, arbitrary-map/integral exp-log bridge, finite BCH group and both directions of ordinary group/Lie automorphism correspondence, and final group-existence theorem remain absent. Successful module builds do not discharge those missing obligations.

Final review timestamp: 2026-09-19T04:52:16.892171+00:00. Assigned semantic-repair audit:100% complete. This percentage refers only to this audit task.
