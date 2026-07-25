# Independent extension mathematical-evaluation protocol

## Scope

This checker evaluates the stable `extensions_unique.csv` artifact produced by
the completed one-vertex-extension kill test.  It does not enumerate extension
origins.  Instead, it cryptographically binds:

- the unique and provenance CSV files;
- the completed search checkpoint and SQLite database;
- the completed independent coverage-audit report and its SQLite state;
- the search runtime sources recorded by the checkpoint;
- the frozen coverage-checker sources recorded by the coverage report; and
- every source file used by this mathematical checker.

The bound coverage audit is responsible for proving that all 110,537 labeled
origins map to exactly the 54,216 canonical rows.  This checker is responsible
for independently evaluating the mathematical predicate assigned to every one
of those rows.

## Independent algorithms

The checker imports no search module and neither verifier A nor verifier B.  It
reuses only the frozen, order-at-most-12 graph6 parser in
`coverage_checker.graph`.  Configurations are ordinary Python frozen sets.
Domination and independence are tested directly from adjacency.  Negative
claims enumerate all relevant subsets.

For one-guard eternal domination at `k=3`, the initial universe is every
dominating three-set.  In simultaneous rounds, a state is deleted when some
unoccupied attacked vertex has no response obtained by moving exactly one
guard along an edge to that vertex while remaining inside the current family.
Iteration stops at the greatest fixed point.  Empty fixed points are recorded
as explicit deletion rounds and replayed after generation.

## Per-row certificates

- `gamma_below_3`: the certificate gives a dominating singleton or pair.  The
  witness size must equal the recorded domination number.
- `alpha_above_3`: the checker exhausts every pair with an undominated-vertex
  witness, gives a dominating triple and independent four-set, and exhausts
  every five-set with an internal-edge witness.  Compact certificates record
  deterministic counts and SHA-256 digests of the exhaustive witness streams.
- the two eternal-false categories: the checker similarly proves
  `gamma=alpha=3`, recomputes the presence or absence of the published private
  obstruction classification, and records a complete empty greatest-fixed-
  point deletion trace for the exact one-guard/unoccupied-attack model.

The certificate is canonical ASCII NDJSON: one header, one record per CSV row,
and one footer.  The footer hashes all exact row-record lines.  Generation
first writes a temporary file, replay-verifies it, atomically installs it, and
then replay-verifies the installed bytes again.  The JSON report is written
atomically only after all checks pass.

## Production invocation

From the campaign root:

```sh
PYTHONPATH=src python3 -m evaluation_checker
PYTHONPATH=src python3 -m evaluation_checker --verify-only
```

Any malformed graph6/CSV/JSON, duplicate JSON key, non-finite JSON value,
truncated or extra certificate line, changed source/input byte, false witness,
incorrect category count, or invalid fixed-point deletion causes a closed
failure and prevents a passing report.

## Claim boundary

Passing certifies only the delimited finite extension artifact.  It is not an
enumeration of all graphs of order 12 and does not resolve the universal
gamma–theta conjecture.
