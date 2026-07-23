# Residual-focused fixed-boundary exact completion

Date: 2026-07-23

## Result and exact scope

**CERTIFIED by independently reconstructed CNFs and checked exhaustive tree
certificates:** neither of the following two free-edge neighborhoods of the
current 43-vertex `E=2` candidate contains a `(5,5;43)` graph:

1. the 19 edges consisting of all 15 pairs within residual-conflict union
   `{3,4,7,38,41,42}` plus the four previously changed core edges
   `{10,31}`, `{21,22}`, `{30,31}`, `{31,32}`;
2. all 66 pairs within the 12-vertex union
   `{3,4,7,10,21,22,30,31,32,38,41,42}`.

All 884 edges outside the first neighborhood, or all 837 edges outside the
second neighborhood, are fixed exactly as in
`results/best_candidates/exoo_seed_20260724.g6`.

These are fixed-boundary neighborhood results only. They are not a global
`(5,5;43)` nonexistence result, do not establish local minimality under a
different free-edge set, and do not improve a Ramsey-number bound.

The base graph6 SHA-256 is
`f5adf13e5791bb8fe4c58941e3d797c283223013290a2376935f1e1eef4ef31a`.
It has zero 5-cliques and two independent 5-sets:
`{3,4,7,41,42}` and `{3,4,38,41,42}`.

## Exact encoding

One variable represents each free edge; true means the edge is present.
For every 5-subset, the generator directly inspects its fixed pairs:

- if no fixed pair is a nonedge, it emits a negative clause preventing all
  free pairs of the subset from becoming edges;
- if no fixed pair is an edge, it emits a positive clause preventing all
  free pairs of the subset from becoming nonedges.

Therefore a complete assignment satisfies the CNF exactly when the completed
graph has neither a 5-clique nor an independent 5-set, subject to the stated
fixed boundary.

| Neighborhood | Variables | Negative clauses | Positive clauses | Total |
|---|---:|---:|---:|---:|
| Six residual vertices plus four edges | 19 | 322 | 34 | 356 |
| Induced 12-vertex neighborhood | 66 | 2,907 | 1,961 | 4,868 |

Both CNFs and metadata files were regenerated and compared byte for byte with
the retained artifacts.

## Semantic tests and independent formula audit

```sh
python3 -m unittest -v tests/residual_lns_tests.py
```

All four tests passed in 2.245 seconds. The tests include exhaustive
assignment/CNF/direct-graph equivalence for a small instance and 768
deterministic random-assignment comparisons over 12 random small graphs.

The production CNFs were independently reconstructed by a checker that does
not import the generator or graph-I/O implementation:

```sh
python3 verify/residual_lns_cnf_check.py \
  --graph results/best_candidates/exoo_seed_20260724.g6 \
  --cnf certificates/residual_lns_six_plus_four.cnf \
  --free-vertices 3,4,7,38,41,42 \
  --free-edge 10,31 --free-edge 21,22 \
  --free-edge 30,31 --free-edge 31,32

python3 verify/residual_lns_cnf_check.py \
  --graph results/best_candidates/exoo_seed_20260724.g6 \
  --cnf certificates/residual_lns_twelve_vertex.cnf \
  --free-vertices 3,4,7,10,21,22,30,31,32,38,41,42
```

Both returned `valid=true` and exact clause-order matches, with zero missing
and zero extra clauses. Checker runtimes were 1.148382 and 1.208199 seconds.

## Bounded solves and proof checks

Commands were run from `/Users/alec/Documents/Math/ramsey55`.

```sh
python3 src/extension_sat_solver.py \
  certificates/residual_lns_six_plus_four.cnf \
  --time-limit 60 \
  --proof certificates/residual_lns_six_plus_four.tree

python3 verify/extension_sat_check.py \
  certificates/residual_lns_six_plus_four.cnf \
  certificates/residual_lns_six_plus_four.tree
```

The 19-variable formula was `UNSAT` in 0.000292 seconds. The proof checker
accepted all 17 records: 16 unit steps, zero branches, and one conflict.
The forced assignments make every edge of `{3,4,7,41,42}` absent, falsifying
the exact positive clause for that residual independent 5-set.

```sh
python3 src/extension_sat_solver.py \
  certificates/residual_lns_twelve_vertex.cnf \
  --time-limit 60 \
  --proof certificates/residual_lns_twelve_vertex.tree

python3 verify/extension_sat_check.py \
  certificates/residual_lns_twelve_vertex.cnf \
  certificates/residual_lns_twelve_vertex.tree
```

The 66-variable formula was `UNSAT` in 0.011881 seconds. The proof checker
accepted all 47 records: 46 unit steps, zero branches, and one conflict.
Again the final conflict is the positive clause for
`{3,4,7,41,42}`. Thus the expanded neighborhood exposes the same
fixed-boundary obstruction, not merely a search timeout.

No SAT model exists in either stated neighborhood, so candidate export and
the two graph verifiers were not applicable.

## SHA-256 hashes

```text
generator source
b1e4c1b5af23bf4b642dcc02562b001d80db5e6f93c5201d1f15d85689caa61a

independent CNF checker source
5d58f048688a7b42e0c582fe541d656722f82ac4a60b41636590263f7b375d70

semantic tests
1a659d7d44c621710bd54b37d8a276dfc8be8a1bfd6a15db288a4e839def5ab8

deterministic proof-capable solver
ee1995e2aad0cd824a30eef06a70f2127929d07e911e628db9557c6359d0df0b

independent tree checker
1e3928d1cda64a63fc7f02e66b479437a9587fa0340db13e7cc5683a11d4b194

19-edge CNF
e055d5ae68b321d4343d5c1966d8a06a740482b5390e8f4443674b2301587462

19-edge metadata
3d9a3634da120abb33f055772dfcb7a15a648b0cb118e96e1df2c0cc70cf00e7

19-edge checked tree proof
5645c314f478a59ac5daf7de314c0b4930526a1573b5b3246a184b3f863d32e1

66-edge CNF
bb6a8166fa530f511a1d99860a8ed3028e8aa91d5c5204d819fa5fda899426da

66-edge metadata
94554415fd70ccd64320920cf79a46edead52ec067a4e9ef0ae04dfdafd163a1

66-edge checked tree proof
5f646f3a6aeb8049728ed7f6f046ca32581d5458b3160d38ee170f92442e7f6c
```

The six retained CNF, metadata, and proof artifacts occupy 125,106 bytes.

## Current-source recovery note

The generator and checker were later extended with a backward-compatible
incident-edge option. Current generator SHA-256
`8a2d43317130d1002684b11491f488738e1bbfa0c0aa08bb8e6b00aeb9d35d37`
regenerated both retained CNFs with the same hashes shown above, and current
independent checker SHA-256
`974b97774da888bdaadbe3ceda7373e5f5d17313462a9c57571d6b4e60a1d672`
again matched all 356 and 4,868 clauses exactly. The original source hashes
remain recorded above as historical provenance.
