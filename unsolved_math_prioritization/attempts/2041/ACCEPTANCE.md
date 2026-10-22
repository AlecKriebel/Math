# Acceptance report: EP-312 / problem 2041

## Publication and review scope

This is an unrefereed AI-assisted prose-only edition. “Accepted” means an independent internal AI audit of the explicitly stated partial result; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The complete substantive candidate proof and independent mathematical audit are retained. No mathematical correction was required. Historical finite tests are described for context; their programs, detailed receipts, and certificate contents are not distributed, and this edition is not an executable reproduction package. Publication preparation did not rerun those mathematical tests or newly inspect scholarly sources.

## Decision and exact limits

ACCEPT AS AN ELEMENTARY PARTIAL RESULT. The universal arbitrary-multiset exponential approximation target remains unresolved. The independent audit required no mathematical correction.

Accepted statements are:

- Removing the sufficiently-large-cardinality threshold is equivalent with the same fixed constant c to the uniform finite-multiset bound epsilon(A) <= exp(-c R(A)).
- Existence of an absolute positive target exponent is equivalent, up to an absolute change of constants, to the stated logarithmic-mass bound for stable gap-avoiding multisets. That logarithmic-mass assertion is still unproved here.
- For each fixed occurrence multiplicity bound M, the target holds for every K > 1 with c_M = 1/(M+1/log 2), without a cardinality threshold. This does not give a uniform exponent as M grows.
- Every admissible universal exponent must satisfy c <= (30/59) log 15. Arbitrary-cardinality padding excludes each strictly larger c. This neither refutes existence of a smaller positive exponent nor establishes optimality.
- The finite counts and exact arithmetic checks identified in the historical verification section were independently confirmed. They do not prove an infinite-range assertion.

Compression preserves mass and permits one-way lifting of compressed subsets to original occurrence subsets. It need not preserve the entire subset-sum set. Exact unit sum is allowed, the target error bound is strict at K, and the uniform bound is non-strict at R(A).

Korsky's optimal-complement and divisibility-compression reductions are prior related work. His stretched-exponential analytic theorem is an attributed manuscript claim, not an independently accepted dependency. The PDF displays July 7, 2026, whereas the HTML displays August 24, 2026; both identify arXiv v1 / July 5. No equality of their bytes, external referee approval, novelty, optimal constant, or complete literature coverage is asserted.

## Exact edition identities

- RESULT.md: 15,292 bytes; SHA-256 f5bfaf2c8d3c18973afe5c4ed9c4b4c0ebc36c063cf5f306c2aa1db5556252df.
- AUDIT.md: 17,801 bytes; SHA-256 4d1db8a66983e19706311d44a822d1dcbe31c8d53124213a7dea9dd9ea90d49e.

The original candidate and audit were preserved unchanged. Editorial changes add review/distribution framing, describe omitted tests historically, and remove nonmathematical coordination details. All substantive proofs, audit arguments, acceptance qualifications, and mathematical limitations remain. Public source/verification metadata contains no source bodies, datasets, executable programs, or detailed certificate contents.
