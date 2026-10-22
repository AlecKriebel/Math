# Boundary invariance: 6200014 / AMR-061-0014

**Result:** positive, as a consequence of published theorems. Read PROOF.md.

The PL hypothesis in the main recognition theorem is not silently added: the no-square manifold obstruction forces dimension at most four, where a manifold triangulation is automatically PL. The proof also treats dimensions zero and one and disconnected manifolds.

This packet contains authored mathematical exposition, finite sanity controls, and public verification metadata. It contains no source PDFs, copied source text, corpus contents, private sources, or coordination files. It makes no novelty, human peer-review, or formal-certification claim.

## Replay

From any location with Python 3.9 or newer:

    python3 /path/to/packet/verify.py
    python3 -O /path/to/packet/verify.py

The verifier checks the exact file set, byte counts, SHA-256 hashes and finite-control output. It rejects unknown files and symlinks. It uses explicit exceptions, not assertions, so optimization does not disable validation. No network, third-party packages, writable installation, or source-corpus access is required. Run it against a separately authenticated archive hash; an internally consistent manifest alone does not prove authenticity.

Optional corpus-identity replay (the files are not included):

    python3 /path/to/packet/code/checks.py --identity PROBLEMS.json RESEARCH_RESULTS.json CATALOG.json

The full file hashes are checked before parsing. The selected record and its associated report are hashed with json.dumps([record, reports.get(problem_number, {})], sort_keys=True).encode(), using Python's default separators and ensure_ascii behavior. Absent report means an empty object.

The recorded finite checks are illustrative and regression-oriented. They cannot validate the imported manifold classification and boundary recognition results. Review their exact hypotheses in the linked scholarly sources.
