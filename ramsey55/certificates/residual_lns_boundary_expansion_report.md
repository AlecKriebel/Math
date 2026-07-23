# Proof-guided residual boundary expansion

Date: 2026-07-23

## Result and scope

**CERTIFIED by independently reconstructed CNFs and checked exhaustive tree
certificates:** two proof-guided expansions of the 66-edge residual
neighborhood are UNSAT under their exact fixed boundaries.

The base graph is
`results/best_candidates/exoo_seed_20260724.g6`, SHA-256
`f5adf13e5791bb8fe4c58941e3d797c283223013290a2376935f1e1eef4ef31a`.
It is the invalid 43-vertex candidate with \(C_5=0\) and \(I_5=2\).

The first expansion releases:

- all 66 edges induced by
  `{3,4,7,10,21,22,30,31,32,38,41,42}`; and
- the 14 edges of the observed 43-cycle that cross that vertex-set boundary:
  `{0,42}`, `{2,3}`, `{4,5}`, `{6,7}`, `{7,8}`, `{9,10}`,
  `{10,11}`, `{20,21}`, `{22,23}`, `{29,30}`, `{32,33}`,
  `{37,38}`, `{38,39}`, `{40,41}`.

The second expansion also releases six fixed edges selected to disrupt the
largest number of unit-proof reason clauses:
`{3,15}`, `{2,21}`, `{0,30}`, `{2,4}`, `{25,41}`, `{9,42}`.

All unlisted edges remain exactly as in the base candidate. These are
fixed-boundary results only. They are not global nonexistence, unrestricted
local minimality, or an improved Ramsey bound.

## Exact outcomes

| Neighborhood | Variables | Negative clauses | Positive clauses | Total | Solve |
|---|---:|---:|---:|---:|---:|
| 66 internal + 14 cycle-cut edges | 80 | 3,299 | 2,109 | 5,408 | 0.030573 s |
| previous 80 + 6 trace-selected edges | 86 | 3,367 | 2,408 | 5,775 | 0.037582 s |

Both deterministic solves ended in UNSAT by unit propagation alone:

- 80-variable proof: 76 unit records, zero branches, one conflict;
- 86-variable proof: 82 unit records, zero branches, one conflict.

The independent direct-subset checker reconstructed the two clause sequences
exactly, with zero missing or extra clauses. The independent tree checker
accepted all 77 and 83 proof records, respectively. No SAT model existed, so
candidate export and graph verification were not applicable.

Machine-readable rechecks are retained as
`results/verification/residual_lns_80_formula_check.json`,
`results/verification/residual_lns_80_proof_check.json`,
`results/verification/residual_lns_86_formula_check.json`, and
`results/verification/residual_lns_86_proof_check.json`.

## Exact commands

```sh
python3 src/residual_lns_sat.py \
  results/best_candidates/exoo_seed_20260724.g6 \
  --free-vertices 3,4,7,10,21,22,30,31,32,38,41,42 \
  --free-edge 2,3 --free-edge 4,5 \
  --free-edge 6,7 --free-edge 7,8 \
  --free-edge 9,10 --free-edge 10,11 \
  --free-edge 20,21 --free-edge 22,23 \
  --free-edge 29,30 --free-edge 32,33 \
  --free-edge 37,38 --free-edge 38,39 \
  --free-edge 40,41 --free-edge 0,42 \
  --output certificates/residual_lns_twelve_plus_cycle_cut.cnf \
  --metadata certificates/residual_lns_twelve_plus_cycle_cut.metadata.json

python3 src/residual_lns_sat.py \
  results/best_candidates/exoo_seed_20260724.g6 \
  --free-vertices 3,4,7,10,21,22,30,31,32,38,41,42 \
  --free-edge 2,3 --free-edge 4,5 \
  --free-edge 6,7 --free-edge 7,8 \
  --free-edge 9,10 --free-edge 10,11 \
  --free-edge 20,21 --free-edge 22,23 \
  --free-edge 29,30 --free-edge 32,33 \
  --free-edge 37,38 --free-edge 38,39 \
  --free-edge 40,41 --free-edge 0,42 \
  --free-edge 3,15 --free-edge 2,21 \
  --free-edge 0,30 --free-edge 2,4 \
  --free-edge 25,41 --free-edge 9,42 \
  --output certificates/residual_lns_twelve_plus_trace_chords.cnf \
  --metadata certificates/residual_lns_twelve_plus_trace_chords.metadata.json
```

The retained exact free-edge sequences are also recorded in each metadata
file.

```sh
python3 src/extension_sat_solver.py \
  certificates/residual_lns_twelve_plus_cycle_cut.cnf \
  --time-limit 60 \
  --proof certificates/residual_lns_twelve_plus_cycle_cut.tree

python3 verify/extension_sat_check.py \
  certificates/residual_lns_twelve_plus_cycle_cut.cnf \
  certificates/residual_lns_twelve_plus_cycle_cut.tree

python3 src/extension_sat_solver.py \
  certificates/residual_lns_twelve_plus_trace_chords.cnf \
  --time-limit 60 \
  --proof certificates/residual_lns_twelve_plus_trace_chords.tree

python3 verify/extension_sat_check.py \
  certificates/residual_lns_twelve_plus_trace_chords.cnf \
  certificates/residual_lns_twelve_plus_trace_chords.tree
```

The independent formula checks use
`verify/residual_lns_cnf_check.py`, the base graph, and the exact
`--free-vertices`/`--free-edge` lists above.

## SHA-256 hashes

```text
80-variable CNF
29331d96769546f9ca3a8090b42c7d59f506cf86fe97e341ce5189bf4860467f

80-variable metadata
52fda74870f720671eb2d99b38aaff2e49fa8a8c0cf15065042dc69846f7922c

80-variable proof
76fe3fae159dbc03e0a0f76591be3b63f62b11ccaa55a3c8a770131c0b299350

86-variable CNF
7e1ea8f550b431dbef4857a181d24a867c43659c6bb97d6d605425eba072ea0f

86-variable metadata
eb3225c5bb1c1ae16ecfec9be58cd5602b07b10c068cc431777c1dcf0a8392a8

86-variable proof
7c1d8272dd16b92225e750223ca93339a0d6a8015fbfcd3dddf7dd38831a83f1
```

The six new CNF, metadata, and proof files occupy 276,415 bytes.

The later incident-edge extension is backward-compatible with these explicit
free-edge modes. Current source hashes are recorded in
`residual_lns_incident_six.report.md`; the exact free-edge sequences in the
retained metadata make regeneration independent of this report prose.
