# Subsampled-SDP clustering: readiness hold

**30003758 / OWR-15999-007 · queue row 1768 · 13 October 2026**

**Recommendation: DEFERRED (`deferred` in the queue lifecycle).** The historical
question asks how a clustering of the full dataset can be obtained from an SDP
on a subsample. It does not specify a unique quantified residual problem.
Conditional sketch-and-lift and sketch-and-solve guarantees are already known.

This is a source-scope assessment, not a proof, counterexample, theorem correction,
or finding that the entire question is already solved. It adds **zero substantive
proof-attempt passes**. The lifetime proof-attempt count is **unknown**; an old
queue display of `0/5` does not certify that count.

Read the [scope audit](SCOPE_AUDIT.md) for the preserved historical question,
existing results, and the choices needed before any new proof attempt. In
particular, the source uses a uniformly selected fixed-size subset, while the
later theoretical guarantees discussed here use independent Bernoulli sampling.
Neither sampling laws nor their probability guarantees are silently transferred.

The [source inspection record](SOURCE_INSPECTION.json) identifies public sources,
retrieved-byte hashes, inspected locations, and limits. Statements and selected
source pages were inspected; the cited papers' proofs were not independently
audited. The [scope record](SCOPE_RECORD.json) makes those limits machine-readable.
The [research log](RESEARCH_LOG.md) records this assessment's checkpoints.

## Reproduce the package checks

From this directory, run `python3 verify.py`, `python3 -O verify.py`, and
`python3 -OO verify.py`. Each command must print a JSON result with `ok: true`.
The verifier uses explicit checks rather than optimization-removable assertions.
[MANIFEST.json](MANIFEST.json) inventories every other file in this package.

These checks establish package consistency and declared scope safeguards. They
do not prove a theorem, authenticate a remote source, certify an exhaustive
literature search, establish global openness, or audit the published proofs.
No source documents or dataset contents are redistributed.
