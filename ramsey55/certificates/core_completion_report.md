# k=1 fixed-core completion report

Date: 2026-07-23

## Result and exact scope

**CERTIFIED by checked custom exhaustive certificates:** for every original
vertex `d = 0,...,41` of the verified Exoo42 graph, the fixed induced
41-vertex core `G-d` cannot be completed to a `(5,5;43)` graph by adding two
new vertices while preserving every edge of that core.

All 42 original deletion labels were generated and solved separately. No
automorphism, isomorphism, or byte-identity deduplication was used.

This is not a global nonexistence result for `(5,5;43)` graphs. It rules out
only completions containing one of these particular labeled 41-vertex cores.

## Encoding

For a 41-vertex fixed core, the 83 variables are:

- 41 edges from new vertex A to the core;
- 41 edges from new vertex B to the core;
- the edge A--B.

Each homogeneous core 4-set contributes one clause for A and one for B.
Each homogeneous core triple contributes one width-7 clause involving A, B,
and A--B. The fixed core is itself checked for forbidden 5-sets.

For deletion 0:

| Clause family | Count |
|---|---:|
| A/B plus a core `K4` | 2,080 |
| A/B plus a core independent 4-set | 2,110 |
| A and B plus a core `K3` | 1,250 |
| A and B plus a core independent triple | 1,230 |
| Total | 6,670 |

The deletion-0 CNF SHA-256 is
`cca4276c280ba4fcb7fb1fd45c3add0b147522ca9de4962199f0a7d4885281fb`.

## Validation

The semantic tests exhaustively compared the CNF with direct graph checking
for every valid labeled `(3,3;m)` core through `m=5` and every assignment to
the two-new-vertex edges: 39 cores and 34,632 assignments.

An independently written formula reconstructor compared all 42 production
DIMACS files as unordered clause sets:

- 42 exact matches;
- 280,376 total unique clauses;
- zero missing clauses;
- zero extra clauses.

## Deletion 0 exact run

Commands were run from `/Users/alec/Documents/Math/ramsey55`.

```sh
/usr/bin/time -p python3 src/core_completion_sat.py \
  data/exoo42_constructed.g6 \
  --delete-vertex 0 \
  --output certificates/core_completion_delete_00.cnf \
  --metadata certificates/core_completion_delete_00.metadata.json
```

Generation wall time: 1.84 seconds.

```sh
/usr/bin/time -p python3 src/extension_sat_solver.py \
  certificates/core_completion_delete_00.cnf \
  --time-limit 60 \
  --proof certificates/core_completion_delete_00.tree
```

Outcome: `UNSAT`; internal runtime 1.347764 seconds, wall time 1.40 seconds,
163 nodes, 81 decisions, 82 conflict leaves, and 2,001 explicit unit steps.
The proof SHA-256 is
`41343ad7f4971bc419684472c57e5ccfcfda97610b4b6a0900d111bc07039885`.

```sh
/usr/bin/time -p python3 verify/extension_sat_check.py \
  certificates/core_completion_delete_00.cnf \
  certificates/core_completion_delete_00.tree
```

Outcome: `valid=true`; all 2,164 records checked in 0.008185 seconds
internally, 0.05 seconds wall.

A separate C++ solver and independently written Python checker reconstructed
the formula directly from graph6. They produced and accepted a 202-byte proof:

```sh
build/core_completion_proof_solver \
  --graph data/exoo42_constructed.g6 \
  --delete 0 \
  --proof certificates/core_completion_proof_delete0.bin \
  --node-limit 1000000 \
  --seconds-limit 60 \
  --progress 0

python3 verify/core_completion_proof_check.py \
  --graph data/exoo42_constructed.g6 \
  --delete 0 \
  --proof certificates/core_completion_proof_delete0.bin
```

This second proof has SHA-256
`5301f7a48408c90aad8940224b437a01b9bc9f6aabf64286b72984bad4ac72ed`.
The checked tree has 187 nodes, 93 branches, 94 conflict leaves, 2,408
replayed units, and maximum branch depth 13. Checker time was 1.105317
seconds.

## All-42 bounded batch

```sh
/usr/bin/time -p python3 src/core_completion_batch.py \
  data/exoo42_constructed.g6 \
  --deletions all \
  --output-dir certificates/core_completion_all42 \
  --time-limit-per-instance 60
```

Measured outcome:

- 42 UNSAT;
- 0 SAT;
- 0 timeouts;
- 84.181127 seconds internal batch runtime, 84.23 seconds wall;
- per-instance solver runtime 1.198818--2.321236 seconds;
- 7,842 total search nodes and 3,900 decisions;
- clause counts ranged from 6,652 to 6,702.

```sh
/usr/bin/time -p python3 verify/core_completion_batch_check.py \
  --input-dir certificates/core_completion_all42 \
  --expect-all-42 \
  --output certificates/core_completion_all42/core_completion_coverage_check_summary.json
```

Outcome: all 42 proofs valid. The checker replayed 104,058 records: 3,900
branches, 3,942 conflict leaves, and 96,216 unit records. Wall time was
0.44 seconds.

```sh
/usr/bin/time -p python3 verify/core_completion_cnf_check.py \
  --graph data/exoo42_constructed.g6 \
  --cnf-dir certificates/core_completion_all42 \
  --expect-all-42 \
  --output certificates/core_completion_all42/core_completion_cnf_coverage_check_summary.json
```

Outcome: all 42 DIMACS clause sets exactly matched independent reconstruction;
runtime 5.017133 seconds internally, 5.09 seconds wall.

No SAT model existed, so no candidate graph or graph-verifier invocation was
applicable.

## Summary hashes

```text
all-42 solve summary
37f277e236e1f31cec6327eb279f6bccafbdafd32b85b9809fa5735d3e92493b

all-42 proof-check summary
6b1c1caa25ddf546c104aff20bd5856f23b340dda5c6924e961fc0e8a42051e4

all-42 independent CNF-check summary
88a9b61872192a083e0068011919ea882b83e53bc4455e2f9cb31f9278b44326

coverage-enforcing proof-check summary
2e54833a541382f894c16d92b493bb40434cbbe661ac42ab77ada3b38443e14e

coverage-enforcing CNF-check summary
2e31e66986bfcdce5607983b415c27d198075e0b1556614a97c6c067d0b6c5a8
```

The all-42 directory contains 42 CNFs, 42 checked tree proofs, 42 per-instance
JSON records, the three original summaries, and two non-overwriting
coverage-enforcing recheck summaries.
