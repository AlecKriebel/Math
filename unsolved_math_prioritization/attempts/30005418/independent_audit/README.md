# Independent audit packet

Problem 30005418 / OWR-12697689-014, rank 797.

Decision: **PASS for scoped proofs and exact controls; universal target UNSOLVED, 5/5.** No mathematical correction was required. See AUDIT.md and CORRECTIONS.md for the exact scope and limits.

The author freeze is external and unchanged. Install/use SymPy 1.14.0 for the independent checker; the author checker uses Python's standard library.

Run from any working directory:

    python verify_audit.py AUTHOR_SAFE_DIRECTORY --author-zip AUTHOR_ZIP

Bind this audit to its independently supplied digest by adding:

    --expected-manifest AUDIT_MANIFEST_SHA256

Arithmetic alone:

    python independent_math.py AUTHOR_SAFE_DIRECTORY OUTPUT_JSON

Optional source replay, with all inputs supplied separately:

    python independent_sources.py AUTHOR_SAFE_DIRECTORY PROBLEMS_JSON REPORTS_JSON CATALOG_JSON PDF_DIRECTORY

INDEPENDENT_SOURCE_RESULTS.json records full-source hashes and exact joins. SOURCE_INSPECTION.json describes the actual 5 October 2026 source inspection; rerunning a hash script does not perform a new textual review. PRIOR_ATTEMPT_RECHECK.json distinguishes fresh remote read-only checks from inspected historical metadata.

Only authored audit discussion, scripts, deterministic arithmetic results and public verification metadata are included. No PDFs, extracted source text, images, raw corpora, private sources, credentials or coordination records are included. Extensive AI assistance is disclosed; no novelty, universal solution, formal verification, or external human peer-review claim is made.
