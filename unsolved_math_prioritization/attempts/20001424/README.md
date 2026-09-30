# 20001424: a graph-defined PCF descent counterexample candidate

**Complete candidate, awaiting independent adversarial review.**

A ten-edge decorated four-cycle defines a degree11 critically fixed rational-map class through the established graph realization theorem. The proposed proof gives trivial holomorphic automorphisms and a unique fixed-point-free antiholomorphic involution. It then proves that the class is algebraic with real field of moduli but has no real model.

- [Complete candidate and verification boundary](CANDIDATE.md)
- [Exact embedded graph](graph.svg)
- [Graph verifier](verify_graph.py) and [receipt](graph_verification.json)
- [Source/prior-art audit](SOURCES.md), [source hashes](source_manifest.json), [pinned record and prior report](source_record.json)
- [Research log](RESEARCH_LOG.md), [turn ledger](turns.jsonl), [status](status.json)

Run `python3 verify_graph.py`; only Python's standard library is required. It exhausts1,152 possible degree-compatible vertex permutations. It does not replace the written realization, naturality, algebraicity, or descent arguments.

The class is specified combinatorially; its coefficients and exact number field are not computed. General graph realization and pseudo-real dynamics are prior work. Historical novelty and minimal degree remain unestablished. No independent-resolution claim is made before review.
