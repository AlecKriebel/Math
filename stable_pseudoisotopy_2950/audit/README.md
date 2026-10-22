# Independent audit: stable pseudoisotopy, problem 2950

**Accepted unchanged as a scoped, unresolved partial result: 4/5 approaches.**
No full solution, nonexistence theorem, constructed example, novelty claim, or human peer-review claim is accepted. This is an independent AI-assisted audit of the complete eight-member author packet.

`AUDIT.md` gives the analytic assessment, limitations and all-member review. `ACCEPTANCE.json` binds acceptance to the original ZIP and external manifest, each included unchanged. The original status saying that review is pending is historical; this separate acceptance records the completed review. No derivative or repair is needed.

`SOURCE_INSPECTION.json`, `SOURCE_RETRIEVAL.json`, `SOURCE_PIN_RESULTS.json`, and `HISTORY_REVIEW.json` contain public verification metadata only. Raw PDFs, source excerpts, datasets and private coordination are excluded. The three cited source PDFs were independently downloaded and match the author pins byte for byte. All three full input corpora and the complete exact-ID record/report pair were rehashed.

Run `python replay.py AUDIT.zip AUDIT_EXTERNAL_MANIFEST.json` and repeat with `python -O`. The external manifest must be authenticated separately. For eight negative controls per packet per mode, run `python test_integrity.py AUTHOR.zip AUTHOR_MANIFEST.json AUDIT.zip AUDIT_EXTERNAL_MANIFEST.json` using the full original filenames. The accepted author archive includes its own verifier.

`verify_sources.py CATALOG PROBLEMS REPORTS PDF_DIRECTORY` independently rechecks the six full inputs when supplied separately. The PDF directory must contain `k3-author.pdf`, `gabai-v2.pdf` and `singh-v3.pdf`. No private input path is embedded in this package.

These programs check bytes, inventory, schema and disposition. There is no executable mathematical checker, formal proof certification or finite-search claim. The mathematical assessment is the written argument and the stated literature dependencies.
