# Independent audit of problem 5300080

Verdict: **PASS for scoped partial results; unrestricted target UNSOLVED; 5/5 approaches used; zero original solution credit.** No required mathematical correction was found. This is AI-assisted review, not human peer review or a formal proof certificate.

- AUDIT.md: mathematical review, source applicability, provenance and limits
- CORRECTIONS.md: no required correction; provenance improvements and publication qualifications
- RESULTS.json: authenticated replay and independent exact tests
- PROVENANCE.json: public source and repository-inspection metadata
- verify_audit.py: independent standard-library checker
- AUDIT_MANIFEST.json: hashes and sizes of this audit's six payload files

Reproduce the author integrity and mathematical tests:

    python3 -B verify_audit.py /path/to/henon_boundary_5300080_author.zip

For the full provenance check, additionally supply locally available source PDFs and complete public corpora:

    python3 -B verify_audit.py /path/to/henon_boundary_5300080_author.zip --source-dir /path/to/pdf-directory --problems /path/to/problems.json --research /path/to/research_results.json --catalog /path/to/catalog.json

The optional PDF-directory filenames are milnor.pdf, lyubich_peters.pdf, hedgehogs.pdf, partially_hyperbolic.pdf, escaping2024.pdf, wandering.pdf and fatou_survey.pdf. These sources and the corpora are not distributed in this audit. Without optional inputs, provenance_checks is empty; no missing checks are claimed as passed.

The script authenticates the exact frozen ZIP before executing its inspected checker. It replays 14,006 author assertions in three configurations, rejects 14 package mutations, and runs 42,428 independently implemented exact assertions. Both normal and Python optimized execution are supported.

No source text, PDF, screenshot, raw corpus, copied source record, or private coordination is included. The original author archive is not modified or duplicated inside this audit archive. No remote writes were made.
