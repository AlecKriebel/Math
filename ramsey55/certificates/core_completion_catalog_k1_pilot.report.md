# Catalog-wide k=1 core-completion preparation and timing pilot

Date: 2026-07-23 (America/Los_Angeles)

## Result and exact scope

**CERTIFIED, fixed-core scope only.** Sixteen preregistered pairs
`(catalog line, deleted vertex)` were solved UNSAT and each exhaustive tree
was independently replayed against the selected induced 41-vertex core.
There were no SAT models, limits, or checker failures in this sample.

This certifies only those 16 fixed cores. It does not classify the other
13,760 catalog/deletion pairs and is not global `(5,5;43)` nonexistence.

**REPRODUCIBLE COMPUTATIONAL OBSERVATION.** At four-worker concurrency the
complete generate/solve/check pilot took 33.548254 seconds. Linear projection
to all 13,776 pairs is approximately 8.02 wall hours under the measured
machine load. This projection is a scheduling estimate, not a mathematical
claim and not a guarantee against harder outliers.

## Catalog and generic selection

The input catalog is `data/r55_42some.g6`:

```text
328 graph6 data lines
SHA-256 067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb
328 * 42 = 13,776 labeled fixed 41-vertex cores
```

The pre-existing dual catalog audit says all 328 entries are valid
`(5,5;42)` graphs:

```text
results/verification/r55_42some_catalog_dual_check.json
SHA-256 6fe9186d25b16efe98029f60b11f4a5f5f8559c7150380cb3dc45b09833c0931
```

The C++ exact solver now accepts both:

```text
--line    one-based nonempty, noncomment graph6 catalog data line
--delete  original vertex label 0..41
```

The independent checker has the same line/deletion interface but retains its
own graph6 parser, core reconstruction, formula builder, and tree replay.
Tests compare its selections on lines 1, 2, and 328 with the project graph
reader.

New proofs use `CORE2DP2`. The header binds:

- input graph order;
- one-based catalog data-line number;
- deleted original vertex;
- variable count;
- clause count.

The checker still accepts legacy `CORE2DP1` proofs only as line-1 artifacts.
It rejects a version-2 proof when checked under a different line number.

## Exact per-core problem

For each selected 42-vertex catalog graph `H` and label `v`, retain the fixed
induced core `H-v` on 41 vertices and add two new vertices A and B. The 83
variables are:

- 41 A-to-core edges;
- 41 B-to-core edges;
- the A--B edge.

Homogeneous core 4-sets give the one-new-vertex clauses and homogeneous core
triples give the two-new-vertex clauses. An exhaustive UNSAT tree proves only
that this particular fixed core has no such completion.

## Preregistered pilot

The plan was written before execution:

```text
results/benchmark_plans/core_completion_catalog_k1_pilot_v1.json
SHA-256 2f8a14b9107f3cfacbfee7bc9e535ef287a75774ff2d89619aafc7192fce9542
```

It fixed 16 pairs across eight approximately equally spaced catalog lines,
10 seconds and 1,000,000 nodes per instance, and four concurrent workers. Its
acceptance rules required independent tree checking for UNSAT and immediate
model preservation plus both graph verifiers for SAT.

Measured results:

| measure | minimum | median | maximum |
|---|---:|---:|---:|
| solver internal seconds | 0.007214 | 0.018749 | 0.054423 |
| search nodes | 131 | 192 | 211 |
| proof bytes | 150 | 211 | 230 |
| independent checker wall seconds | — | 7.554053 | 9.171399 |

Totals:

```text
checked UNSAT fixed cores   16
dual-verified SAT            0
limits                       0
verification failures        0
solver internal time         0.402695 s
batch wall time             33.548254 s
proof bytes                  3,324
```

The exact solver is not the scheduling bottleneck. Independent Python core
reconstruction and proof replay dominate wall time.

The batch summary is:

```text
results/core_completion_catalog_k1_pilot/catalog_k1_batch_summary.json
SHA-256 f7856f5a4808c6d5b152458f5c624f6a2762aa1d2bdbb56e3697d5af89c1cb88
```

An additional coverage guard independently checked that all and only the 16
preregistered pairs occur, every proof and recorded hash still exists, every
solver/checker pair label agrees, and every classification is conclusive:

```text
results/core_completion_catalog_k1_pilot/catalog_k1_coverage_check.json
SHA-256 55ba2272b975bb8d6616e6862f13fc8bba9e1ccc3fbdc37f7ce0f0116f038963
valid=true
complete_checked_classification=true
```

## SAT preservation and verification policy

The batch runner treats SAT as the primary constructive outcome:

1. Atomically preserve the raw zero-based true-variable list before further
   processing.
2. Reconstruct the 43-vertex completion and write graph6 plus the canonical
   representation-rich JSON artifact.
3. Run the exhaustive Python five-subset verifier.
4. Run the independently implemented C++ recursive bitset clique verifier on
   the graph and complement.
5. Report `DUAL_VERIFIED_SAT_CONSTRUCTION` only if all checks agree.

This path was exercised in code and semantic tests, but no pilot instance was
SAT, so no candidate artifact was created.

## Production decision

The full classification was **not launched** from this bounded task. The
selected production schedule uses 21 nonoverlapping, resumable-by-chunk line
blocks:

- 20 chunks of 16 catalog lines = 672 cores each;
- one final chunk of 8 lines = 336 cores;
- four workers;
- 10-second and 1,000,000-node limits per core;
- projected 23.48 minutes per full chunk and 8.02 hours total;
- projected proof storage about 2.9 MB at the pilot mean.

The machine-readable schedule, exact chunks, hashes, acceptance rules, and
scope warning are in:

```text
results/benchmark_plans/core_completion_catalog_k1_production_schedule_v1.json
SHA-256 3ddd4ae32a363718870bc674dc9b92e55e4fab503e237f46cde7e63a5623924d
status READY_NOT_LAUNCHED
```

Any `LIMIT` remains unclassified and moves to a separately planned escalation
queue. Any SAT result stops ordinary classification long enough to preserve
and dual-verify the construction. A catalog-wide fixed-core statement is
permitted only after the coverage checker sees the exact Cartesian product
of lines `1..328` and deletions `0..41`, with every pair conclusive.

Even that future statement would mean only:

```text
None of these 13,776 selected fixed 41-vertex cores has a two-vertex
completion.
```

It would not imply that no `(5,5;43)` graph exists.

## Reproduction

Compile the line-aware solver:

```bash
clang++ -O3 -std=c++17 -Wall -Wextra -pedantic \
  src/core_completion_proof_solver.cpp \
  -o /tmp/core_completion_proof_solver_catalog
```

Run the tests:

```bash
/opt/homebrew/opt/python@3.11/bin/python3.11 \
  tests/core_completion_catalog_tests.py -v

/opt/homebrew/opt/python@3.11/bin/python3.11 \
  tests/core_completion_catalog_coverage_tests.py -v

/opt/homebrew/opt/python@3.11/bin/python3.11 \
  tests/core_completion_proof_tests.py -v

/opt/homebrew/opt/python@3.11/bin/python3.11 \
  tests/core_completion_sat_tests.py -v
```

Thirteen targeted tests pass: four catalog selection/proof tests, two
coverage-guard tests, three legacy proof regressions, and four semantic CNF
tests.

Run the frozen pilot:

```bash
/opt/homebrew/opt/python@3.11/bin/python3.11 \
  src/core_completion_catalog_batch.py \
  --catalog data/r55_42some.g6 \
  --solver /tmp/core_completion_proof_solver_catalog \
  --pairs-plan \
    results/benchmark_plans/core_completion_catalog_k1_pilot_v1.json \
  --output-dir results/core_completion_catalog_k1_pilot \
  --seconds-limit-per-instance 10 \
  --node-limit-per-instance 1000000 \
  --jobs 4
```

Recheck exact pilot coverage:

```bash
/opt/homebrew/opt/python@3.11/bin/python3.11 \
  verify/core_completion_catalog_coverage_check.py \
  --summary \
    results/core_completion_catalog_k1_pilot/catalog_k1_batch_summary.json \
  --pairs-plan \
    results/benchmark_plans/core_completion_catalog_k1_pilot_v1.json \
  --require-conclusive \
  --output \
    results/core_completion_catalog_k1_pilot/catalog_k1_coverage_check.json
```

## Source and tool hashes

| artifact | SHA-256 |
|---|---|
| `src/core_completion_proof_solver.cpp` | `944737d42270b381e5b302e9b38ea4421b1a9c4049d363ecfcc89150e60877e3` |
| pilot solver binary | `e05393a3dac9094752be60d3eab5991ee47d3dbd8c5551bfd0799fe5baea6ac6` |
| `src/core_completion_catalog_batch.py` | `6d935f71cea7e8863c401cb997ec4cd2e017b7165c9a41df84900d4f6bf76290` |
| `verify/core_completion_proof_check.py` | `8e4f2f9cfd429ddac89142e0765a50d2504ad4513874a66e46f59550724443c6` |
| `verify/core_completion_catalog_coverage_check.py` | `a8f93bccfe6abfc8333e35456614b4cf8c2a8bf8a1c0ee959efb7e553404ba83` |
| `tests/core_completion_catalog_tests.py` | `13603c0032d76e36ed4f812d94f50460daa55e472f4c4626533e39420ded648b` |
| `tests/core_completion_catalog_coverage_tests.py` | `539fcb5503a095eaac97f6e37e8fe0c4d6b53d0f8cd2e9f26b05a7bc3e627883` |
