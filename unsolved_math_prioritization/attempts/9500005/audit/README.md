# Independent audit of synchronous reflected-Brownian partials

Disposition: accept the retained partial mathematics; neither part of Burdzy Problem 5 is resolved. The five approaches remain exhausted at 5/5. No additional proof-search approach was attempted.

- AUDIT.md is the independently authored mathematical and scope review.
- SOURCE_RECHECK.json records independent byte/hash matches and bounded primary-source inspection.
- independent_checks.py is a separately implemented finite exact checker.
- replay_audit.py runs both checkers in normal, -O and -OO modes and seven semantic mutants in every mode. It requires the original packet path and read-only modes 0555/0444, verifies actual UID 1000, probes denied writes, and prints JSON without writing files.
- REPLAY_RECEIPT.json records the actual runs and complete subprocess outputs.
- MANIFEST.json and SEAL_RECEIPT.json bind this source-free audit and record its final denied-write probes.

The original freeze was preserved. These files contain no copied source documents, dataset bodies, or private coordination material. They are mathematical auditing artifacts, not a proof assistant certificate or a stochastic simulation.
