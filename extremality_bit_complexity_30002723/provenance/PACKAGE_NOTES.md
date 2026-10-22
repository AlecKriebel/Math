# Package provenance and editorial notes

This package contains the full authored manuscript and mathematical audits, with no copied third-party source document. Source-gate statements are explicitly dated and identified as preceding the candidate proof. The final fresh audit is included byte-for-byte as completed.

Nonmathematical package edits normalize proof command paths to package-relative paths, replace coordination references with neutral authorship wording, and add acceptance, dependency, and replay documentation. No proof step was deleted or mathematically weakened. New packaging utilities are `replay.py`, `verify_manifest.py`, and `checks/verify_covered_nonextreme.py`; the latter rechecks the stored exact example using the existing continuous validator.

The saved-input and algebra suites were run in isolated temporary package copies. Their regenerated result JSON files matched the frozen results byte-for-byte. The original discovery programs are preserved as clearly optional programs; the replay entry point does not call discovery modes.

The manifest is a content inventory, not a cryptographic signature. Its own digest is external to the manifest to avoid circular self-reference. Cache files are not payload. No source PDFs, extracted scholarly text, original problem datasets or extracts, private source material, personal data, or coordination files are present.
