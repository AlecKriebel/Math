# Crossingless matching Ext algebra partial results

Problem 30000930 / OWR-1790-007, rank 661. General disposition: unsolved after five substantive approaches.

The main new result is a proof of the intended associative Yoneda/arc-algebra comparison for k=2, using the published pairwise-module theorem and an explicit two-object algebra classification. The all-k comparison remains unresolved here.

The earlier f=1 nonassociativity finding is retained with the necessary ordinary-complex-orientation qualification. Its original archive and complete independent audit are preserved unchanged under history/. They do not certify the new work.

- K2_YONEDA.md: full partial theorem and proof
- LOCAL_KOSZUL.md: direct local composition and the global-filtration obstruction
- HIGHER_RANK.md: exact balance constraints and a k=4 ambiguity
- CATEGORICAL_ROUTE.md: cup-adjunction route and its missing compatibility
- SOURCE_UPDATES.md: orientation correction and current primary-literature distinctions
- RESEARCH_LOG.md: five approaches and outcomes
- LIMITATIONS.md: precise exclusions
- SOURCE_VERIFICATION.json: hashes, sizes, sources and inspection scope
- HISTORY_BINDING.json: preserved history identities
- CONTROL_RESULTS.json: exact reproducible checks

Run:

    python verify_continued.py --output /tmp/crossingless-continued.json
    cmp CONTROL_RESULTS.json /tmp/crossingless-continued.json
    python verify_manifest.py
    PYTHONDONTWRITEBYTECODE=1 python history/audit/replay_audit.py history/author-packet.zip

Python 3 and its standard library suffice. The new release requires a fresh uninvolved audit; no full-resolution or novelty claim is made.
