# 20001424: a graph-defined PCF descent counterexample

**Complete negative answer to the pinned canonical question; independent adversarial review: PASS.**

A ten-edge decorated four-cycle defines a degree-11 critically fixed rational-map class through the established graph realization theorem. The proof gives trivial holomorphic automorphisms and a unique fixed-point-free antiholomorphic involution. The class is algebraic, its field of moduli lies in the reals in the chosen embedding, and it has no real model. Thus it cannot be defined over its field of moduli.

- [Complete proof and verification boundary](CANDIDATE.md)
- [Independent review](review/REVIEW.md), including the algebraic-conjugator clarification in Section 6
- [Review summary](review/review_summary.json) and [independent exact checks](review/independent_checks.py)
- [Exact embedded graph](graph.svg)
- [Graph verifier](verify_graph.py) and [receipt](graph_verification.json)
- [Source/prior-art audit](SOURCES.md), [source hashes](source_manifest.json), [pinned record and prior report](source_record.json)
- [Research log](RESEARCH_LOG.md), [turn ledger](turns.jsonl), [status](status.json)

Run `python3 verify_graph.py`; only Python's standard library is required. It exhausts 1,152 possible degree-compatible vertex permutations. From `review/`, run `python3 independent_checks.py`; all 183 independent assertions pass. These finite checks do not replace the written realization, naturality, algebraicity, or descent arguments. The separate AI review is not formal verification or peer review.

The class is specified combinatorially; its coefficients and exact number field are not computed. General graph realization and pseudo-real dynamics are prior work. Historical novelty and minimal degree remain unestablished. The live original AIM problem page could not be recovered; its wording is preserved in the authorized pinned record, with the source-access boundary detailed in the audit and review.
