# Commentary/citation audit package

REPORT.md and VERDICT.json give the complete bounded disposition. INDEPENDENT_MECHANISM.md preserves the derivation written before old priority reports were read. SOURCE_COVERAGE.json and ACCESS_LEDGER.json separate complete primary texts from public metadata/access failures.

Run `python3 exact_checks.py` from this directory to reproduce the ten exact algebra and rational checks. Run `python3 seal.py` to verify the authored manifest. To intentionally reseal changed authored files, run `python3 seal.py --write`, then `python3 seal.py`.

MANIFEST.json includes every inner authored file, including .gitignore, and explicitly identifies its two self-referential control files. Raw copyrighted PDFs, OCR, HTML and page renderings are ignored under .cache and are not publication artifacts. The preexisting user-supplied PDFs are referenced by their identity/hash receipts and not copied into the authored package. The parent integrates the authored results; this subtask does not mutate Git index, canonical material or remote publication state.
