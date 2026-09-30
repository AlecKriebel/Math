# 9900007: partial obstruction to synchronous weak-shift coupling

**Full problem: unsolved.** A concrete binary process disproves the illustrative synchronous coupling condition, even in probability. The source's broader request for another two-process characterization remains unresolved.

A fair sign flips independently from time n to n+1 with probability1/(n+2). Every fixed window converges in total variation to the stationary mixture of the two constant paths. Nevertheless, under every coupling with that limit, the probability of a mismatch at time n tends to1/2. For the stated product metric, the complete metric error converges in distribution to a fair mixture of0 and1. Finite random offsets do not repair this example.

- [Complete partial proof, assumptions and remaining question](PARTIAL.md)
- [Source/prior-work audit and access limitations](SOURCES.md)
- [Exact checker](verify_binary_process.py), [885-assertion receipt](binary_verification.json)
- [Pinned source record](source_record.json), [source manifest](source_manifest.json)
- [Readiness](readiness.json), [status](status.json), [research log](RESEARCH_LOG.md), [turn ledger](turns.jsonl)

Run `python3 verify_binary_process.py`; only Python's standard library is used. The checker covers42 finite windows and240 transition products, plus supporting identities. It does not replace the written proof for arbitrary couplings or infinite limits.

One substantive construction family was used. The unchanged proof passed a [separate adversarial review](review/REVIEW.md), with3,044 independent exact checks. The review certifies only the stated synchronous obstruction, not the broader characterization, formal verification or historical priority. Historical novelty is unestablished. This is not a counterexample to the distinct setwise-convergence problem9900005.
