# 5300088: Convex-core ball radius from the number of generators

**Unsolved after five substantive routes.** No rank-only bound or counterexample to the full problem is claimed.

Read `PARTIAL.md` for the exact statement, five routes, full proofs of the retained controls, and the remaining gap. The strongest explicit control is a rank-two family with three-dimensional convex cores and an interior point p satisfying inj(p)=log q while its core depth is at most log((q+1)/(q-1)). This disproves a stronger pointwise-injectivity formulation, not the actual wholly-contained-ball problem. The underlying Schottky phenomenon is credited to Carol Fan; no novelty is claimed.

`SOURCE_GATE.md` records source identity, important hypothesis distinctions, and search limits. `RESEARCH_LOG.md` and `turns.jsonl` record the five routes without promoting partial evidence to a solution. `STATUS.json` gives the proposed status.

Reproduce the finite exact controls and integrity check:

    python3 verify.py
    python3 -O verify.py
    python3 verify_manifest.py

The first two outputs should equal `CONTROL_RESULTS.json`. These finite controls supplement conventional proofs and do not certify all geometric or literature claims. No external packages or source PDFs are needed for replay. Source downloads, extracted third-party text, imported corpora, and private work records are not part of this packet.

This is an AI-assisted, unrefereed research record. Independent review is pending at author freeze. No formal proof-assistant certification or priority claim is made.
