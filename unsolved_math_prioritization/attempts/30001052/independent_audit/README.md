# Independent audit deliverables

Read `AUDIT_REPORT.md` for the complete mathematical and source-scope assessment. `AUDIT_VERDICT.json` is the compact machine-readable verdict. The original author packet is preserved separately and is not replaced by these files.

- `AUDIT_CHECKS.json`: frozen-input hashes, replay modes, negative-control outcomes, source PDF fingerprints, and full-corpus fingerprints.
- `INDEPENDENT_FUSION_CHECKS.json`: a separate exhaustive enumeration including full subgroup morphism tables and every accepted homomorphism.
- `INDEPENDENT_OBSTRUCTION_CHECKS.json`: separate finite-field and finite-set controls.
- `PDF_EXTRACTION_CHECKS.json`: successful PDF parsing, page counts, and exact matching of fresh PDF text extraction to the inspected text, expressed as metadata only.
- `independent_fusion_check.py` and `independent_obstruction_check.py`: independent mathematical computation code. Both use the already installed SymPy 1.14.0; they do not import the author checkers.
- `run_audit_checks.py`: non-mutating audit runner. Mutants are confined to temporary copies. It expects the author packet in the sibling `packet` directory and the seven authorized source PDFs in the sibling `private_sources` directory. An optional command-line argument supplies the directory containing the two full corpus JSON files. Those sources and datasets are not included in these deliverables.

The public mathematical verdict remains unsolved, 5/5 approaches, with correct scoped partial results. Neither the author's original checks nor these checks formalize the homotopy theory. Current-source records and scholarly theorem inspection require reading the cited sources; offline computation does not repeat that reading.
