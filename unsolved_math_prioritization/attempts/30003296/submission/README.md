# Complete surfaces in the genus four moduli space

Problem 30003296 / OWR-15177-013. Research checked on 4 October 2026.

**Unsolved after five approach families.** This packet does not prove existence or nonexistence of a complete complex surface in the moduli space of smooth genus-four curves. It records exact scope, known constraints, failed construction mechanisms, and remaining gaps.

Read `PARTIAL.md` for the mathematical work and references. The five routes are affine stratification and positivity; Satake and Schottky sections; covering spaces and automorphisms; Prym compression; and smoothing a compact-type boundary surface.

The strongest conclusions are restrictions on hypothetical surfaces and rejections of particular constructions. In particular, such a surface must meet the hyperelliptic locus in finitely many points; it cannot lie wholly in the automorphism locus. Neither statement settles the question or is claimed as a new discovery.

`SOURCE_GATE.md` explains source identity, current literature, and the related genus-four target. `turns.jsonl` and `RESEARCH_LOG.md` record the five substantive routes. `verify.py` checks modest exact arithmetic and negative controls. It is not a formal proof checker. `VALIDATION_LIMITS.md` states the limits.

Run `python3 verify.py` and `python3 verify_manifest.py` from this directory. Both are offline and use only Python's standard library. `CONTROL_RESULTS.json` contains the expected arithmetic results.

Only the author-written files listed in `SHA256SUMS.json` belong to this packet. No downloaded source, source-image reproduction, full-text extraction, raw catalogue, or private coordination record is included.
