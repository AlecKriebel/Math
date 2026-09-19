# Local Lean audit — 18 September 2026

Start with `VERIFICATION_REPORT.md` for the final verdict and checked scope.
The complete finite-group theorem is absent from this development.

## Reading the evidence

- `independent_scope_audit.md` compares the intended ordinary-automorphism
  theorem with the actual source and identifies the four missing developments.
- `intake.json`, `original_source_hashes.json`, and `data_integrity.json`
  preserve the delivered archive identity and compare its mathematical inputs.
- The module-family repair reports describe compiler changes and their scope.
- `RESEARCH_LOG.md` records checkpoints. Percentages measure this build,
  audit, and publication task, not completeness of a mathematical proof.
- Final compiled-object, elaborated-type, and axiom reports must be read with
  the trust limits stated in `VERIFICATION_REPORT.md`.

This folder intentionally retains **failed attempts**, resource benchmarks,
and successful later repairs. An empty log, source file, or isolated fragment
is not by itself evidence that a production module passed. Use the final
report's cited successful records. Early failures are retained to make the
repair history inspectable.

The standalone `.lean` files in this audit folder are development experiments
or inspection commands. They are outside the production `Kourovka` import
closure. Some test generic fragments with an abstract model that omits the
concrete bracket dependency. Their success is not counted as acceptance of
the corresponding production module; the production sources are in `../lean/`.
The download places this folder at `audit/` and the project at `lean/`.

Cached, pinned Mathlib dependencies were used. Neither an independent
implementation of Lean's kernel nor a rebuild of the entire compiler and
dependency stack is claimed. No external human peer review is claimed.

The original paper and its version 1.1.0 archives are unchanged by this
supplement. No GitHub release or new Zenodo DOI is created by this task.
