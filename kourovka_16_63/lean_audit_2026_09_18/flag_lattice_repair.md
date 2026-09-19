# Flag and lattice repair audit

Final checkpoint: 2026-09-19T04:42:40.594127+00:00. **100% of this bounded repair/checking assignment completed.** This percentage does not describe progress toward a complete formalization of Kourovka 16.63.

## Final result

All 43 Flag/Lattice modules in this inventory compile under Lean 4.19.0, including every one of the 31 embedding certificate shards. `NearIdentity` is assigned to the finite-module agent. `Flag/Rigidity` was independently repaired and checked by the analytic agent. No original theorem statement was weakened; no admissions, new axioms, or native decision procedures were introduced.

Final source/object hashes and freshness checks are recorded in `flag_lattice_final_inventory.json`. Parent's `embedding_rows/summary.json` records all 29 remaining shard checks passing, with per-row source/import hashes. Shards 00 and 01 passed separately before that batch. The final logs `flag_concrete_build.log`, `flag_generation_build.log`, and `lattice_integral_build.log` are empty successful compiler logs.

## Repairs

- **Expressions:** retained and checked the repaired integral-expression induction proofs.
- **Precision:** restricted two rewrites to the domain side of a submodule inclusion; the original rewrite also altered the target submodule and invalidated the membership proof.
- **AdaptedBasis:** explicitly exposed the pointwise multiplication equation in `embed_divisible_two` to avoid an unresolved linear-map coercion.
- **WeightedFlags:** restricted the exponent decomposition rewrite to its intended occurrence; the original rewrite altered inner occurrences of the same exponent.
- **ScaledData:** expanded the bracket's type abbreviation to its definitionally equal linear-map type, resolving polymorphic function coercion. All 199 scaled structure coefficients are unchanged.
- **IntegralWords / IntegralGeneration:** separated finite expression certificates from generic coefficient-ring arguments without changing namespaces, node definitions, denominators, or theorem statements. Repaired the coefficient-casting naturality proof using explicit evaluation unfolding, a typed target bracket, and additive-map integer-scalar normalization. The actual p-adic generation theorem compiles.
- **Concrete:** repaired malformed tactic quotation syntax and a finite-index reduction issue in the nonzero-vector proof. Closed bracket and projector identities are checked by kernel reduction. The two parameterized identities use bilinearity and scalar ring normalization.
- **Generation:** explicitly unfolded the bracket-preservation and derivation predicates before simplifying with their hypotheses. The field division operation was not reducible by kernel computation; all 42 scalar quotient values are therefore proved via `div_eq_iff` and exact modular multiplication, after which the vector equalities are kernel reducible. Original node definitions, target values, fixed-vector and vanishing-vector statements remain unchanged.
- **EmbeddingBasis / certificate shards:** added proved formulas for diagonal and embedded basis vectors and a bridge to the independent integer coefficient evaluator. These speed proof reduction while preserving the original `EmbedCheck` proposition. Shard 00 uses direct kernel computation; shards 01–30 use these proved reductions followed by kernel computation.
- **Integral:** explicitly imported the ambient Lie module after narrowing unused imports elsewhere and annotated the scalar ring in the adapted-bracket application. After all shards passed, the full integer embedding theorem, transported Jacobi identity, arbitrary-ring Lie structures, and adapted-coordinate relationship compiled successfully.

## Checking and trust

Finite checks use `decide +kernel`, which runs reduction in Lean's trusted kernel. This is not `native_decide`. Expensive files disable asynchronous elaboration and were checked with one Lean worker per process. Initial resource failures, failed elaboration attempts, and an initial missing output-directory error were repaired; the final successful checks supersede those attempts.

## Exact remaining mathematical scope gap

These modules prove algebraic components and conditional general lemmas. They do not supply the final theorem constructing a finite group with the claimed automorphism cardinality.

Specifically, `approximate_lift_preserves` and `approximate_derivation_lift_preserves` take the ambient module, expression-span generation equality, and error/integrality hypotheses as arguments. `Weighted.reduction_preserves_level` takes a map already known to preserve the weighted lattice. No theorem in these modules instantiates all those arguments for every automorphism of the concrete finite quotient. `Flag.full_flag_rigidity` quantifies over the full finite-field linear-equivalence type once bracket and flag preservation are supplied; it does not itself prove that all quotient automorphisms reduce to that situation. Those bridges and the remaining BCH/group and cardinality arguments are necessary for a complete formalization.
