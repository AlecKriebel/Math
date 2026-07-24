# Catalog-wide k=1 constructive screen

Date: 2026-07-23 (America/Los_Angeles)

## Outcome

**REPRODUCIBLE COMPUTATIONAL OBSERVATION, not a certified negative.**
The preregistered screen executed every one of the 13,776 labeled pairs
`(catalog line, deleted vertex)` and the generic C++ producer reported UNSAT
for every fixed core. No UNSAT proof was generated or independently replayed.

| status | count |
|---|---:|
| `OBSERVED_UNSAT_UNCHECKED` | 13,776 |
| `DUAL_VERIFIED_SAT_CONSTRUCTION` | 0 |
| `LIMIT_NO_CONCLUSION` | 0 |
| `SAT_MODEL_VERIFICATION_FAILED` | 0 |
| `SCREEN_ERROR` | 0 |

The independent coverage/status audit passed:

```text
expected pairs       13,776
actual pairs         13,776
duplicates                0
missing                   0
extra                     0
invalid records           0
negative certified        0
all pairs executed     true
all statuses precise   true
```

This says only that the producer computationally observed no two-vertex
completion of any selected induced 41-vertex core. It does not certify those
negative results and does not imply global `(5,5;43)` nonexistence. The
earlier independently replayed 16-pair pilot remains the only certified
negative subset.

## Frozen run

The amended plan was written and hash-validated before execution:

```text
results/benchmark_plans/core_completion_catalog_k1_full_screen_persistent_v1.json
SHA-256 ec187bccea440511c255a987ccac43065bd953aa8ce21bfa2f220817d7ccbecc
```

It fixed the exact Cartesian product of catalog lines `1..328` and deletion
labels `0..41`, eight persistent workers on disjoint 41-line ranges, 10
seconds and 1,000,000 nodes per instance, and no negative proof replay.

Any SAT model was to be atomically preserved before reconstruction and
checked by both the exhaustive Python verifier and the independent C++ bitset
verifier. No SAT status occurred, so that path was not invoked.

The completed run took 103.925976 wall seconds. All eight workers produced
exactly 1,722 records, returned zero, and had empty stderr. Solver statistics
over the 13,776 instances were:

| measure | minimum | median | 95th percentile | maximum | total |
|---|---:|---:|---:|---:|---:|
| internal seconds | 0.004079 | 0.010421 | 0.045666 | 0.159053 | 227.244865 |
| search nodes | 115 | 189 | 231 | 305 | 2,553,080 |
| clauses | 6,609 | 6,662 | — | 6,731 | — |

## Audited artifacts

```text
results/core_completion_catalog_k1_full_screen_persistent/
  catalog_k1_screen_summary.json
    e5ee5b08d0250a2a9117999b9735823d45651649b2108d9da807813f55918ddf
  catalog_k1_screen_coverage.json
    9b5a8832ff0389f7f84ad212f1cdab38aa54143576e005e3fa65d3a8de6ef697
  records/  (13,776 individually hashed JSON records)
```

The audit re-read every persisted record, checked its hash against the
summary, checked the catalog and solver hashes, required the exact pair and
solver-output labels, enforced the record schema and status semantics, and
required zero worker errors and zero certified negative outcomes.

Pinned implementation hashes:

| artifact | SHA-256 |
|---|---|
| `data/r55_42some.g6` | `067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb` |
| `src/core_completion_catalog_screen_solver.cpp` | `344477b1ce368110614c8052557146ed56ad7fe216f43bfdbae556a9392b202c` |
| `src/core_completion_proof_solver.cpp` | `944737d42270b381e5b302e9b38ea4421b1a9c4049d363ecfcc89150e60877e3` |
| persistent solver binary | `be4212db5e9c08a9be0d4730bf9d3f022fb758e39ace789a4c3f64d8a02d3468` |
| `src/core_completion_catalog_stream_screen.py` | `a87fa407391d31d9dd9e195aa687249c99a9363f795aa30eef80244709b4bc2a` |
| `verify/core_completion_catalog_screen_coverage.py` | `76e6513de22614e9be5e4e5f8281d038bb9d2c3f9052c9de49b71fd065323afd` |

Two targeted screen/coverage regression tests pass.

## Superseded diagnostic attempt

The original one-subprocess-per-pair attempt was intentionally terminated
after operating-system process-launch throttling. Its 1,738 partial records
remain untouched and were not resumed or combined with this run:

```text
results/core_completion_catalog_k1_full_screen/ABORTED_PARTIAL_NO_RESULT.json
SHA-256 6877a4538cd4cf07c5e85d2894597f03b601cfc43e10d289ba6add896ff48799
```
