# Independent audit: problem 30004620

Read AUDIT.md and CORRECTIONS.md. The result remains **UNSOLVED, five of five author approaches used**. This is a fresh independent AI-assisted audit, not human peer review.

The author freeze is unchanged. All 8,800 author controls were replayed byte-for-byte. `python3 -B verify_independently.py` runs a separately implemented exact-rational audit without importing or executing the author's verifier. Compare its output to independent_results.json.

`python3 -B verify_evidence.py --help` describes optional local input verification. It accepts externally supplied author archive, catalog, problems, research-results, and primary PDF paths. None of those source PDFs or raw corpora is redistributed here.

AUDIT_MANIFEST.json binds the audit payload. The separate archive receipt binds the archive itself. Public metadata, original mathematical analysis, executable audit code, and results are included. Scholarly-source text, PDFs, extracts, images, raw corpus records, and private coordination are excluded. No remote write was made.
