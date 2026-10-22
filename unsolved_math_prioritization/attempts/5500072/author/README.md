# Regular-pentagon polyhedral surfaces

This is an authored partial investigation of 5500072 / AMR-054-0072, queue rank 929. The full problem is unresolved by this work. No novelty is claimed. Independent audit is pending.

- `proof_note.md`: hypotheses, curvature identities, trivalent rigidity, the four-valent obstruction, and the remaining global gap
- `research_report.md`: source reconciliation, inherited-work gate, and bounded search outcome
- `status.json`: machine-readable conservative disposition, three approaches used
- `diagnostics.py`: exact standard-library algebra and optional complete-corpus/source-byte verification
- `validation_results.json`: recorded full-input diagnostic output
- `verification_metadata.json`: public source retrieval metadata and bounded repository search observations
- `replay_results.json`: normal/optimized relocated replay and rejection tests

Run `python diagnostics.py` or `python -O diagnostics.py` for the exact algebra and frozen-status checks. Without supplied inputs, this explicitly reports corpus and source-byte verification as not performed. To reproduce the complete input check, provide all of `--catalog PATH --problems PATH --reports PATH`; optionally provide `--source-dir DIRECTORY` containing the independently obtained public files listed in the metadata. No network access is required by the diagnostic.

The pair digest is over the complete two-element list `[record, reports.get(problem_number,{})]` serialized with `json.dumps(...,sort_keys=True)` and all other JSON options left at Python defaults. It is not a digest of a selected-field summary.

The external archive manifest pins each member and the ZIP by size and SHA-256. The separately frozen bootstrap checks these before extraction and runs the diagnostic from a newly created unrelated directory under both normal and optimized Python. The bootstrap is a packaging check; it does not replace independent mathematical review. A manifest is an integrity reference, not a digital signature.

The local four-pentagon stars do not constitute a closed-surface counterexample. Incidence fixtures likewise are algebraic test inputs and are not asserted to have geometric realizations. Source PDFs, their extracted text, dataset contents, and private coordination material are excluded.
