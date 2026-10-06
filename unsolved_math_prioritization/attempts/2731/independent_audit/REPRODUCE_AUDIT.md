# Reproduce the independent audit checks

The analytical verdict is in `INDEPENDENT_AUDIT.md`. The script verifies only exact-input provenance and finite regression tests; it cannot replace the written mathematical audit.

Run `python replay_audit.py AUTHOR.zip AUTHOR_MANIFEST.json` with the exact author freeze and its external manifest. The archive and manifest are hard-pinned; later or modified copies are rejected. The script extracts only the verified nine member basenames into a temporary directory, performs normal and optimized author-checker replays from another working directory, checks an independent exact segment oracle, and tests failure fixtures and mutations.

To reproduce the complete corpus and source verification, add `--catalog CATALOG_FILE --problems PROBLEMS_FILE --reports REPORTS_FILE --source-dir SOURCE_DIRECTORY`. Supply the authorized original full inputs. This optional mode prints only public verification metadata and never emits their contents. The source directory must contain the four PDF basenames listed in the script. Source page-count and normalized-statement inspection additionally require Poppler's `pdfinfo` and `pdftotext`; all other operations use Python's standard library. No network is used.

The complete invocation produces `REPLAY_RESULTS.json`. Running the same invocation with `python -O` must produce identical output on the same Python version. On another Python release the recorded version field may differ. `SOURCE_RECHECK.json` separately records human-readable source-inspection scope and the bounded literature review.

`EXACT_ACCEPTANCE.json` specifies what was accepted and what was not claimed. The audit's inner manifest binds all other audit files; its external manifest binds every file and the exact audit ZIP. No author correction was required, and no corrected derivative exists.
