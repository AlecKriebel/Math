# KP-2.28 / 2776: type-preserving RAAG embeddings

**Partial results; general question unresolved.** Five distinct mathematical routes are documented, with complete proofs of the partial statements and exact descriptions of the remaining gaps. No novelty claim or full resolution is made.

- `RESEARCH_REPORT.md`: normalized scope, mathematical arguments, and dependencies.
- `LITERATURE_AND_SCOPE.md`: current bounded literature check and important source/convention limitations.
- `verify_exact.py`: source-free Python 3 standard-library checks.
- `VERIFICATION_RESULTS.json`: output from the checked edition.
- `SOURCE_MANIFEST.json`: public titles, URLs, inspected versions, retrieval outcomes, hashes, and byte counts only.
- `EDITION_MANIFEST.json`: pinned hashes and byte counts for every preceding file.

Reproduce the checks with `python3 verify_exact.py`. The script writes its results next to itself. The proofs, rather than finite testing, establish the unbounded claims.

The packet contains no source PDFs, page images, source extracts, datasets, private sources, private personal information, or coordination material.
