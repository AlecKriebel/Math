# Final statement-contract follow-up

Checkpoint: 2026-09-11T02:26:49.895954+00:00. Assigned final read-only statement review: 100% complete. The parent task's final clean serial verification run remains in progress; this note does not report its completion.

The two elaboration repairs in `validation/Statements.lean` preserve the intended mathematical contracts:

1. The Born formula now wraps the entry function in `Matrix.of` and explicitly types both indices as `Fin 2 × Fin 2`. In the pinned Mathlib, `Matrix.of` is `Equiv.refl _`, and `Matrix.of_apply` is proved by `rfl`. Thus the tensor entries remain exactly `M i.1 j.1 * N i.2 j.2`, with the intended matrix multiplication inside the trace. The wrapper disambiguates matrix instances from function instances; it neither changes the physical tensor nor introduces a hypothesis. The repaired contract still has proof `rfl` against the actual Born definition. The original uncompiled expression is compared at the level of its intended statement, not presented as a previously accepted Lean theorem.
2. The zero-input case now uses `change (0 : ℕ) ≤ 1; decide`. This exposes the definitionally equal input-count inequality for architecture `⟨0,5,AO,BO⟩`. The equality conclusion, arbitrary output functions and absence of alphabet-positivity assumptions are unchanged.

Reviewed every declaration name and source-file location in `docs/CERTIFIED_COVERAGE.md`; all correspond to current production declarations. The physical model, finite complete-strategy mixture, arbitrary-output convex-hull equality, exact separator constants, stronger rational projective bound, threshold, and strengthened raw attainment are described accurately. `main_claims` denotes the basic conjunction and `main_claims_with_strengthening` adds the separate attainment claim, as reflected by the paired declaration names. The stated exclusions—no same-state simulation, no raw-range equality, no global POVM optimum, and no claim to formalize every unused manuscript argument—are appropriate.

The contract count is correct: 14 examples in `Statements.lean` plus 11 in `PhysicalContracts.lean`, totaling 25. The parent reports successful elaboration of both repaired production contracts; the final clean run still needs to finish and publish its own success result.

Packaging observation sent to the parent: the coverage document links `../CERTIFICATION.md`, which was absent at the time of this read. That certificate should exist before final delivery. No production source, contract, script or generated report was edited during this follow-up.
