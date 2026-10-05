# Independent audit for problem 30005664

The five scoped author propositions pass independent analytic and exact-algebra review. The original Aubin–Talenti critical-potential optimization problem remains unresolved after 5/5 approaches. This is independent AI review, not human peer review or formal proof-assistant certification.

Read AUDIT.md for the complete report, including domain closure, infinite angular modes, source hypotheses, and the distinction between the sharp scalar Schur-form constant and a full Dirac spectral gap. No correction to the frozen propositions was necessary. Do not shorten the result in a way that drops that distinction.

## Reproduction

Python 3 with SymPy 1.14.0 was used.

    python independent_check.py > /tmp/dirac-independent-results.json
    cmp /tmp/dirac-independent-results.json INDEPENDENT_RESULTS.json
    python verify_audit.py

The independent script reconstructs all 957 author coverage controls and adds 35 controls. Analytic arguments remain necessary for the infinite-dimensional statements.

verify_inputs.py optionally repeats the complete input verification when the reader has authorized local copies of the frozen author ZIP, catalog, two pinned dataset files, the pinned repository dataset manifest and the five public source PDFs. Pass their paths using --author-zip, --catalog, --problems, --research-results, --dataset-manifest and --source-directory. The source directory should contain owr.pdf, keller.pdf, keller_published.pdf, nice2026.pdf and ckn.pdf, as identified by INPUT_VERIFICATION.json. It emits only hashes, sizes and match metadata. These external inputs are intentionally not included in this audit ZIP.

SOURCE_REVIEW.json distinguishes fresh official-site observations, complete cached-byte verification, actual inspection scope, inherited limitations and failed live reads. INPUT_VERIFICATION.json records complete-file fingerprints and the recomputed statement/review bindings. REPLAY.json records the separate author replay and exact control-coverage comparison.

The author freeze is preserved unchanged. This ZIP contains only authored audit prose/code/results and public verification metadata. No source PDF, extract, page image, raw corpus, credentials or private coordination material is included. No repository write was performed by this audit.
