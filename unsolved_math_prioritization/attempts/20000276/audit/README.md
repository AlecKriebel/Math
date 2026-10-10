# Independent audit of problem 20000276

Verdict: PASS for the frozen regular-local theorem and singular F-pure
counterexample, with no fatal mathematical gap found. The intended original
AIM scope remains unverified, so an unqualified original-target solved label
is not supported. Historical novelty is not established.

- `AUDIT_REPORT.md`: complete scoped mathematical review and independent
  Fedder/pair-definition verification of the singular example
- `VERDICT.json`: machine-readable acceptance boundaries
- `verify_independent.py`, `INDEPENDENT_CHECKS.json`: independent exact finite
  controls, supplementary to the general mathematical audit
- `AUTHOR_CHECKS_REPLAY.json`, `AUTHOR_FREEZE_VERIFICATION.json`: author test
  replay and unchanged snapshot verification
- `verify_source_metadata.py`, `SOURCE_METADATA_VERIFICATION.json`: public
  dataset, selected-record join, hash-recipe, and scholarly PDF byte checks
- `SOURCE_INSPECTION.json`: retrieval history and limits of literature review
- `verify_manifest.py`, `AUDIT_MANIFEST.json`: integrity verification

Run `python3 verify_independent.py` and `python3 verify_manifest.py` from
this directory. The source verifier takes explicit paths for the two public
dataset files, public catalog, and separately supplied scholarly PDFs; these
source materials are deliberately not included.

The archive contains audit writing, verifiers, and public verification
metadata only. It contains no papers, extracted source text, raw dataset
contents, or private coordination material. No remote writes were made.
