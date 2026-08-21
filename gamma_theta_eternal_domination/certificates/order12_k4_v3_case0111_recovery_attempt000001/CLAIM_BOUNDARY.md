# Claim boundary

## Current author-side status

```text
NO_LEAF_OR_AGGREGATE_CLAIM_PENDING_SEPARATE_HOSTILE_REVIEW
```

The author replay has passed all programmed checks, but no mathematical claim
is promoted by this package itself. The preserved production outcome remains
`RAW_FORWARD_REJECTED_NONCLAIM`, and the immutable production run is not
modified.

## What a separate hostile acceptance could support

If an independent reviewer reconstructs the exact case CNF, replays the fresh
LRAT proof with an independently controlled checker invocation, and accepts
the package and its claim boundary, the supported finite statement would be:

> The exact frozen case `0111` CNF, obtained from the order-12 parameter-4
> parent by adjoining unit clauses `-4`, `14`, `23`, and `31`, is
> unsatisfiable.

That is one leaf only. It is not an exclusion of all order-12,
parameter-4 candidates and does not resolve the γ–θ conjecture.

## Explicit exclusions

This package does not certify:

- any of the other 15 Boolean cubes;
- completeness or soundness of an aggregate result;
- the entire `(n,k)=(12,4)` slice;
- absence of counterexamples of order 12;
- any unrestricted graph class; or
- the γ–θ conjecture.

The recovery invokes no SAT solver. The retained raw solver result is treated
only as provenance for the raw proof stream; the proof checks, not the solver
exit status, are the evidentiary chain.
