# 2912 / Kirby 4.36: unresolved obstruction audit

**Status: unsolved / stalled after two substantive approaches.** No proof or counterexample to the original question was obtained.

The target is whether the complete homotopy 2-type, including the first k-invariant, determines the homotopy type of an actual 2-knot complement. The source does not mark the meridian or boundary inclusion.

- [Complete deductions, stopped routes and exact gaps](OBSTRUCTION.md)
- [Primary-source audit and retrieval limitations](SOURCES.md)
- [Finite integral block verifier](verify_group_block.py) and [receipt](group_block_verification.json)
- [Pinned source record](source_record.json), [source hashes](source_manifest.json)
- [Readiness](readiness.json), [status](status.json), [research log](RESEARCH_LOG.md), [two-turn ledger](turns.jsonl)

The first route identifies third universal-cover homology through meridional group cohomology and proves a sufficient degree-one pair-map criterion. It does not construct such a map from unmarked 2-type data. The second computes a nonzero obstruction module for an explicit infinite-ended group pair; it does not construct two actual exteriors with the same full 2-type.

Run `python3 verify_group_block.py` with the Python standard library. All 507 exact finite algebra assertions pass. The checker does not establish knot realization or homotopy classification. The unchanged mathematical deductions passed a [separate adversarial review](review/REVIEW.md), with29,933 independent exact controls. This AI review does not certify a solution, novelty, formal verification or human peer review. No novel theorem is claimed.
