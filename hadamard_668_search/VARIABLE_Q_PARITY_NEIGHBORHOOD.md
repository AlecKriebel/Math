# Exact parity-neighborhood scan

`variable_q_parity_neighborhood.py` is a deterministic bounded search around
a parity-feasible `BS(84,83)` checkpoint.  It fixes the checkpoint's eight
sequence/parity-class sign counts, so all four ordinary and all four
alternating sums remain unchanged.

Every same-margin vector at Hamming distance `2r` can be written as `r`
disjoint exchanges of a `+1` and a `-1` in one parity class.  Each exchange
has an 83-bit syndrome: the parities of its changes to the half-correlation
residuals.  Because an exact base sequence has zero residuals, only unions
with XOR-zero syndrome can possibly be exact.  The scanner enumerates all
such unions for `r <= 3`, deduplicates their final sign vectors, and evaluates
the integer correlations directly.  Thus the scan is complete for the stated
same-margin Hamming neighborhood; it says nothing about larger distances or
other margin shards.

Run the recorded scan with:

```sh
python3 variable_q_parity_neighborhood.py \
  output/variable_q_parity_best_canonical.json --max-exchanges 3
```

For checkpoint SHA-256
`9c5e69534abd8db1abf69e493dbfb7640e2457b594c3a83a5c9dd0e45d39417f`,
the exact results are:

| Exchanges | Hamming distance | Distinct parity-feasible vectors | Minimum half-energy | Minimizers |
|---:|---:|---:|---:|---:|
| 1 | 2 | 34 | 272 | 1 |
| 2 | 4 | 3,646 | 248 | 1 |
| 3 | 6 | 159,558 | 280 | 2 |

The checkpoint itself has half-energy 232.  It is therefore a strict local
minimum against every parity-feasible, same-margin change of at most six
coordinates.  No exact candidate occurs in this bounded neighborhood.  This
does not construct or disprove `H(668)`; it gives a fast exact diagnostic for
future incumbents.  Within the endpoint-parity-feasible, same-margin subspace,
escaping this checkpoint requires either an uphill step or a move of at least
eight coordinates.  A search that permits parity-infeasible intermediate
states or changes the margins is outside this result's scope.

`test_variable_q_parity_neighborhood.py` checks the incremental correlation
formula, the complete radius-four result, and a spread of the 159,558
deduplicated six-flip vectors against independent correlation recomputation.
