# Exact one-vertex-extension result for `exoo42_constructed.g6`

Date: 2026-07-23

## Result and scope

**CERTIFIED (checked custom exhaustive certificate):** the deterministic
one-vertex-extension CNF for the graph whose input-file SHA-256 is
`a7db2ac21e14b3652629d0cfc1c47bf7b65f355e1f2fcf9048a075622c5ba75a`
is UNSAT.

This proves only that this fixed 42-vertex graph cannot be extended to a
`(5,5;43)` graph while preserving every edge among the original 42 vertices.
It does not prove that no `(5,5;43)` graph exists, and it says nothing about
completions that change an edge in the 42-vertex core.

No installed DRAT/LRAT-producing solver or standard proof checker was found.
The checked artifacts instead use two small, complete DPLL tree formats:

1. A 5,339-byte textual proof whose every unit step cites an original DIMACS
   clause and whose every leaf cites a falsified original clause.
2. An independently implemented 52-byte branch tree. Its checker independently
   decodes graph6, reconstructs the clause set, replays original-clause unit
   propagation, and checks both children of all 19 branches.

Both checkers accepted their proof. The second path also independently matched
the generated DIMACS clause set exactly: 2,318 unique clauses, with zero
missing and zero extra clauses.

## Encoding

There are 42 variables. Variable `i` in DIMACS (one-based) is true exactly
when the new vertex is adjacent to base vertex `i-1`.

- Every 4-clique `C` of the base graph contributes
  `OR(i in C, NOT y_i)`.
- Every independent 4-set `I` contributes `OR(i in I, y_i)`.

The base graph was checked to contain no clique or independent set of size 5.
Therefore any new forbidden 5-set must contain the added vertex, so these
clauses are equivalent to validity of the one-vertex extension.

The generated instance contains:

| Item | Count |
|---|---:|
| Variables | 42 |
| Negative 4-clique clauses | 1,148 |
| Positive independent-4 clauses | 1,170 |
| Total clauses | 2,318 |

## Exact reproduction commands and measured outcomes

All commands below were run from `/Users/alec/Documents/Math/ramsey55`.

```sh
python3 -m unittest discover -s tests -v
```

Outcome: all 13 tests passed in 0.272 seconds. The encoding test exhaustively
compared CNF evaluation with direct graph evaluation for every extension of
all 38 valid labeled `(3,3;n)` base graphs for `2 <= n <= 5`, totaling 728
neighborhood assignments. Certificate tests also reject truncation, trailing
bytes, an invalid branch, and a corrupted unit step.

```sh
/usr/bin/time -p python3 src/extension_sat.py \
  data/exoo42_constructed.g6 \
  --output certificates/exoo42_extension_sat.cnf \
  --metadata certificates/exoo42_extension_sat.metadata.json
```

Outcome: 42 variables and 2,318 clauses. Wall time: 0.51 seconds. A repeated
generation was byte-identical.

```sh
/usr/bin/time -p python3 src/extension_sat_solver.py \
  certificates/exoo42_extension_sat.cnf \
  --time-limit 60 \
  --proof certificates/exoo42_extension_sat.tree
```

Outcome: `UNSAT` (SAT-standard exit code 20), 39 search nodes, 19 decisions,
20 conflicts, 518 explicit unit propagations, and 557 proof records. Internal
runtime: 0.131051 seconds; wall time: 0.18 seconds.

```sh
/usr/bin/time -p python3 verify/extension_sat_check.py \
  certificates/exoo42_extension_sat.cnf \
  certificates/exoo42_extension_sat.tree
```

Outcome: `valid=true`, conclusion `UNSAT`, all 557 records checked. Internal
runtime: 0.002343 seconds; wall time: 0.05 seconds.

The independent compact proof path was built and run as follows:

```sh
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic \
  src/extension_sat_proof_solver.cpp \
  -o build/extension_sat_proof_solver

/usr/bin/time -p build/extension_sat_proof_solver \
  --graph data/exoo42_constructed.g6 \
  --proof certificates/exoo42_extension_sat_proof.bin \
  --node-limit 1000000 \
  --seconds-limit 60 \
  --progress 0
```

Outcome: `UNSAT` (exit code 20), 39 tree nodes, 19 branches, 20 conflict
leaves, 469 unit assignments, maximum branch depth 5. Internal runtime:
0.000690 seconds; wall time: 0.28 seconds.

```sh
/usr/bin/time -p python3 verify/extension_sat_proof_check.py \
  --graph data/exoo42_constructed.g6 \
  --proof certificates/exoo42_extension_sat_proof.bin
```

Outcome: `VERIFIED_UNSAT_FIXED_EXTENSION_CNF`, all 39 nodes checked, 469 unit
assignments independently replayed. Checker runtime: 0.140719 seconds; wall
time: 0.20 seconds.

## Artifact hashes

```text
base graph6
a7db2ac21e14b3652629d0cfc1c47bf7b65f355e1f2fcf9048a075622c5ba75a

DIMACS CNF
ff372bd968015eb1ee027459679ba2528d0a8c566034e51f37d3f9671bb78160

DIMACS metadata
e56df8503a53a9cea756c3bf1b07017b84399afb7d8255fb2d584bba17050150

explicit-unit tree proof
e30cf3871b12322f3627ab1115d66b72078fc52d0fa30f0036ab9668f624bf66

compact independently replayed tree proof
fd8c5e9886c77ae83d604d34a35e11f7c8bde91215719dc627f95daa6e14c232
```

Relevant source hashes at execution time:

```text
src/extension_sat.py
48a84784304428049908d48bf279303812016b837516caaa666dae089d5662ab

src/extension_sat_solver.py
ee1995e2aad0cd824a30eef06a70f2127929d07e911e628db9557c6359d0df0b

verify/extension_sat_check.py
1e3928d1cda64a63fc7f02e66b479437a9587fa0340db13e7cc5683a11d4b194

src/extension_sat_proof_solver.cpp
e8c9602571385470616666b64d9de545c2b743dd66a746e155b98f1f49824325

verify/extension_sat_proof_check.py
8ff492bb13ae25dd65def7b927e3428344e95312d43b1b1531314a8afc40f063
```
