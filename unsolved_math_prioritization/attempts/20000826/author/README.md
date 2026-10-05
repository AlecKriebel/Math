# AIM Problem 25: three-variable multigraded connectedness

This is a partial-research package, not a solution to the general problem.

- `REPORT.md`: exact scope, five routes, later-literature update, and remaining obstruction
- `PROOFS.md`: functorial low-weight classification, a characteristic-free cubic connectedness control, and explicit boundary controls
- `verify.py`: deterministic standard-library-only exact checks
- `verification_results.json`: recorded output
- `source_metadata.json`: public bibliography, retrieval status, and inspected-source hashes
- `dataset_verification.json`: public input hashes and match results, with no dataset contents
- `SEARCH_LOG.md`: research checkpoints and bounded search scope
- `MANIFEST.json`: hashes and sizes of every other packaged file

Run from any directory with Python 3.8 or newer:

    python /path/to/verify.py --output /tmp/connected-results.json

Compare that output byte-for-byte with `verification_results.json`. The checker needs no network access, source PDFs, dataset files, or computer algebra system. Assertions are essential; do not run Python with `-O`.

The finite checks validate the displayed control examples and enumerations. They do not establish general connectedness, irreducibility, or a minimum variable count for disconnected examples. The accompanying proofs, rather than finite-point counts, establish the claimed low-weight geometric statements.

No source PDFs, extracted pages, raw imported research reports, private data, or repository coordination files are part of this package. An independent audit is required before promoting the authored claims.
