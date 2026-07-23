# k=2 core completion: delete original vertices 0 and 1

Date: 2026-07-23

## Result and scope

**CERTIFIED by a checked exhaustive tree certificate:** the fixed 40-vertex
induced core obtained by deleting original vertices 0 and 1 from the verified
Exoo42 graph cannot be completed to a `(5,5;43)` graph by adding three
vertices while preserving every core edge.

This result applies only to this fixed 40-vertex core. It is not a global
`(5,5;43)` nonexistence result and does not cover any of the other 860
two-vertex deletion pairs.

## Deterministic instance

The 123 variables encode:

- 120 edges from three new vertices to the 40 core vertices;
- 3 edges among the new vertices.

| Forbidden-set family | Negative | Positive |
|---|---:|---:|
| One new vertex plus four core vertices | 2,853 | 2,811 |
| Two new vertices plus three core vertices | 3,492 | 3,402 |
| Three new vertices plus two core vertices | 394 | 386 |
| Total | 6,739 | 6,599 |

Total clauses: 13,338. Clause widths are 4, 7, and 9.

The generator was rerun and produced a byte-identical CNF.

## Tests and independent formula audit

```sh
python3 -m unittest -v tests/core_completion_k2_tests.py
```

All four tests passed. The semantic test compared direct graph validity with
CNF evaluation for every extension of 10 valid small labeled cores, totaling
25,672 assignments. A separate target-5 test exhaustively covered the
nine-literal, three-new-vertex clause family.

```sh
/usr/bin/time -p python3 verify/core_completion_k2_cnf_check.py \
  --graph data/exoo42_constructed.g6 \
  --cnf certificates/core_completion_k2_delete_00_01.cnf
```

The checker independently decoded graph6 and directly enumerated every
relevant 5-subset. It reconstructed 13,338 unique clauses with zero missing
and zero extra clauses. Internal runtime was 0.373789 seconds; wall time was
0.45 seconds.

Retained machine-readable recheck:
`results/verification/k2_delete_00_01_formula_check.json`.

## Generation and bounded solve

Commands were run from `/Users/alec/Documents/Math/ramsey55`.

```sh
/usr/bin/time -p python3 src/core_completion_k2_sat.py \
  data/exoo42_constructed.g6 \
  --delete-vertices 0,1 \
  --output certificates/core_completion_k2_delete_00_01.cnf \
  --metadata certificates/core_completion_k2_delete_00_01.metadata.json
```

Generation wall time: 2.00 seconds.

```sh
/usr/bin/time -p python3 src/extension_sat_solver.py \
  certificates/core_completion_k2_delete_00_01.cnf \
  --time-limit 60 \
  --proof certificates/core_completion_k2_delete_00_01.tree
```

Outcome: `UNSAT` within the strict cap.

- Internal solver runtime: 25.195826 seconds
- Wall time: 25.29 seconds
- Search nodes: 1,483
- Decisions: 741
- Conflict leaves: 742
- Explicit unit steps: 18,251
- Proof records: 19,734

```sh
/usr/bin/time -p python3 verify/extension_sat_check.py \
  certificates/core_completion_k2_delete_00_01.cnf \
  certificates/core_completion_k2_delete_00_01.tree
```

Outcome: `valid=true`, conclusion `UNSAT`. All 19,734 proof records were
checked. Internal checker runtime was 0.033912 seconds; wall time was 0.09
seconds.

Retained machine-readable recheck:
`results/verification/k2_delete_00_01_proof_check.json`.

No SAT model existed, so candidate export and the two graph verifiers were not
applicable.

## Hashes and storage

```text
base graph6
a7db2ac21e14b3652629d0cfc1c47bf7b65f355e1f2fcf9048a075622c5ba75a

CNF (323,474 bytes)
d0678b8c71edeaa5a9e3e99170d6d35fb655a1da2873355eda4116208d03488c

metadata (1,300 bytes)
01442e908a53e1ec6027e69ba628d120827380252bef502cb9eb657894ab12fb

checked tree proof (197,034 bytes)
a469ea000c190c7b639a819ffdaec81a191ba5f2f037a86fbe4f814ba03887a0

generator source
4df7613c6544c34b72e4cb1c303451de1feac3400b31249a8c45c48187719ae5

independent CNF checker source
7e283652a447b1e4eea1a242d1a56d87d490bf8866467899461e7e380579aeec

semantic tests
55ad4b3ac03cf4938f0b54810474e08d4393e1e3ec0de1d230dea878374cd46c

deterministic proof-capable solver
ee1995e2aad0cd824a30eef06a70f2127929d07e911e628db9557c6359d0df0b

independent tree checker
1e3928d1cda64a63fc7f02e66b479437a9587fa0340db13e7cc5683a11d4b194
```

Total CNF, metadata, and proof storage: 521,808 bytes.
