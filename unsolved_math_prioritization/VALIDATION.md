# Validation record

- 15 regression tests passed: cache loss, partial-versus-solved labels, unsafe statements, source-change invalidation, retained removed entries, possible duplicates, stale verification, evidence-backed clearance, invalid scores, unknown cache provenance, deterministic exports, zero-validity bounds, stale assessment/readiness files, and retired-status display.
- Independent adversarial agent ran the first 11 tests and matched all 23 assessment hashes against SQLite and the exported catalog. Its three remaining findings were fixed and covered by four additional tests.
- Repeated full-corpus ranking produced byte-identical catalog, CSV, top queue, and individual assessment notes.
- Pinned-cache sync completed and reported no added, removed, or changed records.
- All 15,458 numeric IDs are retained. 13,174 records are eligible for further triage; 2,284 have one or more review holds. These categories are not a scientific validation of novelty or solvability.
- 23 individual desk assessments; zero ready, active, or solved research claims. No mathematical attempt was launched.
- Source downloads and SQLite are excluded from Git. Only this effort's directory was staged; pre-existing repository changes were left untouched.

Remaining limits: subjective uncalibrated scores, incomplete literature checking, incomplete semantic deduplication, possible reused numeric IDs in future upstream releases, and single-writer commands. The evidence schema records required review artifacts but cannot verify their mathematical content. Raw JSON import uses memory proportional to source size; future much larger releases may warrant a streaming parser. No claim is made that the top-ranked problem is in fact solvable in the stated budget.
