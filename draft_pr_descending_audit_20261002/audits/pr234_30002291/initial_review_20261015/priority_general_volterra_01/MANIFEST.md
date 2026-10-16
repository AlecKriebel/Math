# Authored release allowlist

Only the following authored files are intended for possible publication. This is an allowlist, not authorization for a Git operation.

- `.gitignore`
- `README.md`
- `SCOPE.md`
- `REPORT.md`
- `RESEARCH_LOG.md`
- `READ_EVIDENCE.md`
- `SOURCE_HASHES.json`
- `SEARCH_LEDGER.md`
- `SEARCH_LEDGER.json`
- `scope_checks.py`
- `SCOPE_CHECKS.json`
- `RESULT.json`
- `MANIFEST.md`
- `AUTHORED_MANIFEST.json`

Excluded: the entire `private/` directory, every PDF, every full extracted source, every raw publisher/arXiv/provider payload, and private build helpers. The author manifest hashes the listed files except itself to avoid self-referential hashing.
