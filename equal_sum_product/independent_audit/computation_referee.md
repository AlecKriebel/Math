# Independent computational referee report

Checkpoint: 2026-09-17 UTC. Completion estimate: **100% of the assigned code, certificate, arithmetic, and reproduction audit**. No other referee report was consulted before this conclusion. No external communication or Git operation was performed.

**Verdict:** All mathematical computations and supplied test-count claims inspected are correct. The supplied checker directly implements the stated positive-integer/global-distinctness/common-value conditions, and the complete supplied reproduction passes. No false acceptance, false rejection, arithmetic error, or mathematical correction was found. Finite tests provide implementation and transcription evidence; the unrestricted nonexistence conclusion depends on the written proof.

## Integrity and execution

The complete supplied source code was read before execution. All 39 entries in the original SHA-256 manifest matched before copying or executing the package. The original Downloads package was left unchanged and all 39 entries were rechecked afterward. Initial checks and the manifest's own hash are recorded in `computation/original_hash_audit.json`.

Execution occurred first in an isolated copy under `computation/reproduction_copy`. The copied package's logs were refreshed by its own reproducer, as the README warns; its historical manifest should consequently not be treated as a manifest of refreshed outputs. That temporary copy is excluded from publication. Replayed logs are preserved independently in `computation/reproduced_logs`, with console output in `computation/reproduction_console.txt`.

All seven reproduction stages passed under Python 3.14.6, Darwin arm64. The exact-audit stdout is byte-for-byte identical to the supplied exact-audit stdout. The original 33 unit tests passed, including positive controls, malformed values, declared-N errors, dimension guards, permutations, scaling, and arbitrary-precision arithmetic.

## Claims independently checked

The reproduced scopes agree exactly with the README, note, and progress record:

| Claim | Reproduced scope |
|---|---:|
| Checker tests | 33 |
| Ordered triples in 1 through 40 | 64,000 |
| Nonempty subsets of 1 through 12 | 4,095 |
| Telescoping checks | 512 |
| Higher-row arrays | 360 |
| Columns in those arrays | 2,340 |
| Large-number rational probe | 101-digit entries |

The 360 arrays equal 10 row counts times 12 column counts times 3 trials. Their 2,340 columns equal 10 times 3 times the sum of 1 through 12. The largest normalized sum reported as 1 reproduces exactly. All calculations use integer or rational arithmetic; no floating-point tolerances are involved.

Every matrix certificate was recomputed independently from its entries:

| Certificate | Row sums | Column products | Distinct entries | Outcome |
|---|---|---|---:|---|
| source_two_rows | 840, 840 | ten copies of 840 | 20 | Valid with minimum two rows |
| ordinary_two_rows | 26, 26 | three copies of 60 | 6 | Common sum differs from common product |
| ordinary_three_rows | 24, 24, 24 | two copies of 840 | 6 | Common sum differs from common product |
| repeated_three_rows | 8, 8, 8 | four copies of 8 | 1 | Fails global distinctness |
| scaled_source | 1680, 1680 | ten copies of 3360 | 20 | Common sum differs from common product |
| corrupted_source | 841, 840 | first 1260; remaining nine 840 | 19 | Fails multiple conditions |

The source example's reciprocal sum is exactly 2. The repeated-entry example's sum over columns of column-sum/column-product and its total inverse-square sum are both exactly 3.

## Independent checks beyond supplied tests

A separate audit implementation, `computation/independent_checks.py`, recomputes controls without importing the supplied inequality audit. It compares the submitted matrix checker against a direct definition of validity. It is portable within the published folder and can be rerun as:

```
python3 equal_sum_product/independent_audit/computation/independent_checks.py
```

Results are saved in `computation/independent_checks.json`:

- 283,932 predicate comparisons: every matrix of shapes 1 by 2, 2 by 2, 2 by 3, and 3 by 2 with entries from 0 through 5, under minimum row counts 1, 2, and 3.
- 200 accepted permutations of the valid two-row certificate, ensuring the audit is not merely testing rejections.
- 11 additional invalid entry values and 10 malformed or invalid shapes.
- 19,551 ordered positive-integer columns: every column of lengths 3 through 5 with entries from 1 through 7, verifying column-sum/product is at most its inverse-square sum using exact fractions.
- All 8,191 nonempty subsets of 1 through 13, checking the inverse-square bound.
- An independent exact polynomial identity certificate: both displayed polynomial sides have degree at most 2 in each variable, and agree at every point in the 3 by 3 by 3 grid with coordinates 0, 1, and 2. Successive univariate interpolation proves this identity universally; its use here is not an unsupported finite sampling argument.

All passed.

## Boundary and implementation assessment

The checker checks arbitrary-precision actual row sums and column products; it does not invoke nonexistence to force rejection. Python booleans and floats are correctly rejected despite their potential equality with integers. Rectangularity, positive integers, dimensions, global distinctness, declared N, equality within sums/products, and equality between sums and products are all checked. The minimum-row override is explicit and correctly enables the known two-row control. A default rejection of that control is therefore intentional. The declared-N null default in the Python function means omission; the JSON CLI correctly rejects an explicitly declared null N.

Global distinctness is essential: a 3 by 4 all-2 matrix satisfies the arithmetic equalities. The positive-integer lower bound is essential to deleting omitted factors: for four entries each equal to 1/2, normalized column sum is 32 while inverse-square sum is 16. The audit therefore does not justify a false extension to arbitrary positive reals. The selected-three-row proof and the cyclic all-row inequality correctly use positive integers at least 1, including empty-product and repeated-value diagnostic cases.

The only textual issue observed is a harmless source comment calling the additional large-number probe “100-digit entries”; its actual entries are 10^100 plus 3, 7, and 11, hence 101-digit. The output, README, and mathematical note correctly say 101-digit. This does not affect computation or mathematics, and the supplied source was not edited.

## Scope limit

This report validates computations, certificates, test-count claims, and checker logic. It is not a proof-assistant certification or an exhaustive historical-priority audit. No unproved inference from finite matrix enumeration was used. No remaining computational obligation blocks publication of the stated result, subject to the separate mathematical and source-scope reviews.
