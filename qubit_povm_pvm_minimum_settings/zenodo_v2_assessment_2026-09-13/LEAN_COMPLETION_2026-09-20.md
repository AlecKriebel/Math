# Lean completion decision

Assessment date: 20 September 2026 Pacific. Scope: assess the supplied 11 September coverage report against current formal endpoints; no new formal proofs or release were requested or performed.

## Decision

The existing development supports “the principal results are formalized in Lean in the explicit complex-qubit matrix model.” It does not support “every mathematical statement or every argument in the manuscript is formalized.” The unconditional equality in `Bell/Assembly.lean`, explicit whole-strategy mixture in `Bell/SimulationCorollaries.lean`, and expanded `validation/Statements.lean` contracts match the former claim. Missing general lemmas are not missing assumptions of those endpoints when the compiled proof uses replacements.

Before advertising complete machine-checked correspondence with every model convention in the manuscript, prioritize the following explicit bridges:

1. **Stochastic output processing.** Define arbitrary finite local stochastic channels and prove their decomposition into deterministic output maps. Prove that processing preserves the projective convex hull, with a single random selector for complete strategies across all inputs and both parties. Existing deterministic coarsening is a foundation, not this theorem. Handle zero channel probabilities, unused labels, and degenerate alphabets explicitly.
2. **Dimension and basis conventions.** Transfer physical behaviors from local complex Hilbert spaces of dimension at most two to the fixed matrix carrier while preserving positivity, trace, Born probabilities, measurement normalization, and projectivity. Extending effects by zero alone is insufficient: assign the unused orthogonal complement to a chosen outcome. Treat nonempty outputs and impossible normalized states/measurements in degenerate cases correctly. A generic Hilbert-space formulation also needs the basis/isometry correspondence, not only a concrete one-dimensional example.
3. **Finite label conventions.** Prove behavior and hull transport under finite-type equivalences to `Fin n`, allowing input-dependent alphabets. This is primarily representation bookkeeping; `Fin n` already covers every finite cardinality.

These are recommendations for eliminating external interpretation steps, not repairs to an identified false central theorem. They are not prerequisites to describing the present fixed-matrix theorem accurately.

## Manuscript and release completion

Version 2 should explain that the formal proof replaces parts of the original route, and map the principal claims to exact declarations. In particular, deterministic score gaps replace the general POVM-duality/KKT argument; feasible curves and an exact score-gap identity replace full manifold/Hessian/inertia statements; an operator SOS certificate supplies the global projective bound. Formal endpoint validity does not validate every intermediate assertion in an unused manuscript proof. Retained manuscript-only assertions still require mathematical review, or the exposition should be revised around the certified route.

There is no need to formalize general SDP duality, the full 14-dimensional manifold, full Hessian inertia, or every appendix calculation solely to certify the principal results. Literal whole-manuscript certification would require addressing every partial/absent entry in the coverage audit, a substantially larger scope.

Before a new immutable release, stage a consistent package, remove stale active-source status wording (for example `SimulationCorollaries.lean` currently says proofs await compilation), refresh shipment hashes and manuscript correspondence, and execute the advertised complete check from the extracted archive. Preserve historical receipts as historical. If proof or verifier inputs change, generate fresh verification evidence. Include compiled contracts for any added bridges and retain the precise axiom/trust statement. See `VERSION_2_PLAN.md` for the previously identified publication corrections and archive issues.

## Evidence and limits

This assessment read the supplied coverage report and current definitions, assembly, simulation endpoints, contracts, certificate and prior referee response. An independent follow-up audit agreed with the completion distinction and rehashed all 88 original protected proof/verifier inputs: unchanged. No new full compiler run is claimed. The existing fixed successful run remains the compilation evidence; source inspection and matching hashes are not a new compilation.

The earlier Zenodo comparison was made directly against archived files on 13 September Pacific. This assessment does not claim a new remote-version check on 20 September. No production proof/manuscript files, external records, or correspondence were modified.

Completion: 100% of this bounded assessment. The suggested bridge formalizations and version 2 release remain future work; no percentage for those unfinished tasks is inferred from the size of the existing library.
