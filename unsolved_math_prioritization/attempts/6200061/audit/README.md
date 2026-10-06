# Independent audit package

Verdict: **ACCEPTED_PARTIAL_NOT_SOLVED** for Problem 6200061, rank 810.

Read `AUDIT_REPORT.md` for the mathematical, source and adversarial review. No correction of the frozen partial-result proof was necessary. The general equality and conditional existential-attainment conjectures remain unresolved by this work.

## Reproduce

Place the unchanged author archive anywhere readable, then run:

    python3 independent_checks.py PATH_TO_AUTHOR_SAFE_FREEZE.zip
    python3 -O independent_checks.py PATH_TO_AUTHOR_SAFE_FREEZE.zip

The script pins that archive's exact external SHA-256 and byte count before extracting into temporary directories. It uses no network and no third-party packages. It leaves the supplied author archive untouched.

Optional complete-input identity verification, when the authorized corpus files are available separately:

    python3 independent_checks.py PATH_TO_AUTHOR_SAFE_FREEZE.zip --corpora CATALOG_JSON PROBLEMS_JSON REPORTS_JSON

Only hashes, byte counts, record counts and match results are printed. No corpus text is exported. `CHECK_RESULTS.json` records the completed run with those optional identity checks; `HARNESS_RELOCATION.json` records normal/optimized relocated-harness tests; `SOURCE_CHECKS.json` records the bounded primary-source inspection.

Finite numerical checks do not prove the geometric result. Three intentionally rehashed semantic mutations pass the standalone author verifier and fail the archive pin; this scope limit is explicitly recorded. Read the report before relying on a PASS message.

The exact file allowlist and hashes are in `MANIFEST.json`. The external audit receipt identifies this ZIP. Neither the ZIP nor its manifest contains third-party PDFs, extracted texts, corpus records, private sources, or private coordination material. The supplied report is Markdown to match the proof/code archive format.
