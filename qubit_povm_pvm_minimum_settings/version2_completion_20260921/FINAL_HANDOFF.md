# Version 2 completion and local handoff

**The principal results, including the stated model conventions, have complete formal proofs in Lean.**

The independently reviewed mathematical scope is complete. This does not certify every auxiliary assertion or alternative manuscript proof. No unresolved mathematical or reproduction blocker remains within the requested scope. The package is local; no GitHub/Zenodo release, package upload, or new DOI was created.

## New formal scope

- `Bell.StochasticChannel` and `Bell.StochasticFamily` give nonnegative normalized product weights over deterministic functions, with exact channel reconstruction. `Bell.StochasticProcessing.behavior_decomposition` and `mem_convexPVM` use one common selector over both parties and every input. `Bell.FiniteLabels.StochasticProcessing` gives the same physical weighted-table operation for arbitrary input-dependent finite source/target labels. Deterministic merging preserves PVMs; stochastic processing preserves their ordinary convex hull. Empty-source/target existence conditions and zero weights are explicit.
- `Bell.Hilbert.Strategy.toQubit_behavior` and the projective counterpart preserve actual tensor Born probabilities from independent endomorphism-valued strategies on arbitrary complex inner-product spaces of local dimension at most two. Positivity, actual source trace, basis-independent tensor form, isometries, tensor transport, and selected-outcome complement allocation are proved. Reverse representation and `Bell.Hilbert.rawPOVM_eq_matrix` / `rawPVM_eq_matrix` identify the union of allowed dimensions with the fixed matrix model. Zero-dimensional normalized states are impossible; existing outcome labels are derived from valid strategies.
- `Bell.FiniteLabels.behaviorEquiv`, encoding behavior theorems and finite-mixture transport preserve independent arbitrary finite outcome types, normalized POVMs/PVMs, actual Born tables and ordinary convex hulls. `Bell.FiniteLabels.two_input_equality` transports the principal equality.
- `Bell.HilbertFiniteLabels.at_most_two_input_equality` and `finite_source_projective_simulation` combine both conventions in an independent source model, returning finite mixtures of actual Hilbert-space projective branches on the original labels. Each branch includes its state. No same-state simulation, raw POVM/PVM equality, closure substitution, or global POVM optimum is claimed.

Exact declarations, quantifiers and boundary cases: [coverage map](../bell_lean/docs/CERTIFIED_COVERAGE.md), [model conventions](../bell_lean/docs/MODEL_CONVENTIONS.md), [semantic review](reviews/semantic_review.md).

## Verification evidence

The packaged certificate records successful clean run `20260921T145457Z-083d0c3b`. A further clean extraction of the exact final ZIP passed the entire advertised reproduction, ending `2026-09-21T15:22:57.094376+00:00`, with Lean run `20260921T150935Z-9ebb22fc`.

Both runs rebuilt all 68 production modules, compiled 78 statement examples in seven contracts, audited all 826 public theorem dependency closures, and checked 104 protected proof/verifier inputs unchanged. All exact artifact checks and all 14 preflight stages passed. Both PDFs rebuilt warning-free. The final shipped/rebuilt publication and review PDFs each have 37 identical rendered pages; their byte hashes differ because PDF byte determinism is not promised. All ten LaTeX source-archive member contents match the staged source.

The first failed integrated certification is also preserved: its required-declaration inventory contained an incorrect theorem name. The name and early guard were repaired before both successful clean runs. No failed receipt is represented as success.

Authoritative records:

- [Certificate for the exact protected snapshot](../bell_lean/CERTIFICATION.md)
- [Final complete reproduction receipt](evidence/final_clean_reproduction_receipt.json)
- [Final kernel report](../bell_lean/reports/runs/20260921T150935Z-9ebb22fc/kernel_report.json)
- [Final axiom audit](../bell_lean/reports/runs/20260921T150935Z-9ebb22fc/axiom_audit.json)
- [Final statement audit](../bell_lean/reports/runs/20260921T150935Z-9ebb22fc/statement_audit.json)
- [Final artifact bindings, including all page comparison hashes](evidence/final_artifact_bindings.json)
- [Final independent package review](reviews/final_package_review.md)

The actual final-extraction command was:

```sh
PATH=/Users/alec/.elan/bin:$PATH bell_lean/.venv/bin/python \
  version2_completion_20260921/extracted/final/qubit-povm-pvm-v2.0.0/reproduce.py \
  --dependency-cache /Users/alec/Documents/Math/qubit_povm_pvm_minimum_settings/bell_lean/.lake/packages
```

For another machine, use a clean extraction and the instructions in [VERSION_2.md](../VERSION_2.md): `python reproduce.py --bootstrap`, or its prepared-cache variant. The tested path reused the separately provisioned dependency cache and rebuilt every project proof. Lean 4.19.0, the pinned compiler/runtime and the dependency-cache producer remain trust assumptions. All nine dependency source commits and tracked-file cleanliness were checked; this is not an independent Mathlib rebuild or authentication of compiled cache objects. Audited dependencies use only `propext`, `Classical.choice`, and `Quot.sound`, with no admitted proofs or custom mathematical axioms.

## Manuscript and local outputs

Revised sources are in [paper/](../paper/). The manuscript identifies the replacement formal routes: deterministic physical score gaps, feasible curves with an exact score-gap identity, and an operator sum-of-squares global projective bound. General SDP duality/KKT and pullback, the full manifold/Hessian/inertia development, broader cone/rank statements, and selected discrimination/spectral/Appendix B calculations remain manuscript-only, as itemized in the coverage map. Current public archive claims were checked against directly downloaded Zenodo files and latest-version metadata; see [archive comparison](ARCHIVE_COMPARISON.md).

The local [output directory](output/) contains:

- `qubit-povm-pvm-v2.0.0.zip` — complete reproduction package, 11,427,095 bytes.
- `Minimum_Bell_Setting_Complexity_v2.0.0.pdf` and `Minimum_Bell_Setting_Complexity_review_v2.0.0.pdf`.
- `qubit-povm-pvm-latex-v2.0.0.tar.gz` — matching source.
- `proof_source_snapshot.json`, `final_reproduction_receipt.json`, `BINDINGS.json`, and `SHA256SUMS.txt`.

ZIP SHA-256: `b301f82654bbebfdc3d91c3b0c7569d7a83e9cff9ffd0eb2b420cf6e82b52104`.

Protected snapshot JSON SHA-256: `5f65a3b6d423f525b9e55e905d517d5be2011bddda19e3094dae7071098934c9`.

The final ZIP contains the first successful certificate and is frozen. Its second complete reproduction receipt is outside the ZIP to avoid self-reference. Local output archives are intentionally ignored by Git; source, public evidence and final verification logs are checkpointed on `main`. Historical required input archives and receipts are retained, while build caches and private correspondence are excluded.
