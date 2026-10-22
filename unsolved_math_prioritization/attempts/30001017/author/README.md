# Rank 662: first Voronoi intersection numbers

**Disposition: unresolved after five approaches. Fresh independent audit required.**

The exact all-genus conjecture is retained. The packet proves support, abelian-weight, and birational-comparison lemmas; reproduces known low-genus finite sums with exact rational arithmetic; and isolates the first zero not covered by the cited EGH theorem as genus-five degree L^2 D^13. No new global vanishing theorem, geometric counterexample, or novelty claim is made.

- PROOF.md: full authored partial arguments, formula derivations, and exact remaining gap
- RESEARCH_LOG.md and turns.jsonl: five substantive approaches and completion estimates
- SOURCE_VERIFICATION.json: public source identifiers, hashes, sizes, retrieval and inspection scope
- SOURCE_ISSUES.md: normalization, typographical, and preprint arithmetic cautions
- CONTROL_RESULTS.json: deterministic output of python3 verify.py
- STATUS.json, LIMITATIONS.md, REPOSITORY_GATE.json: disposition and verified scope
- MANIFEST.json and verify_manifest.py: exact allowlist and integrity verification

Run from this directory:

    python3 verify.py
    python3 verify_manifest.py

Only Python's standard library is needed. The arithmetic run performs no network activity and consumes no external datasets or PDFs. Source files are not redistributed. Formula evaluations for g>=6 are diagnostic calculations pending reconciliation with the published paper, not certified new geometric values.
