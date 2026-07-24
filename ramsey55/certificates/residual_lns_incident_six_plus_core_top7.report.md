# Proof-core-guided seven-core-edge cut

Date: 2026-07-23

## Result and exact scope

**CERTIFIED:** no \((5,5;43)\)-graph agrees with
`results/best_candidates/exoo_seed_20260724.g6` on all core edges except
possibly

```text
(0,32), (18,33), (18,20), (24,26), (1,10), (9,29), (27,29)
```

while every one of the 237 edges incident to
`\{3,4,7,38,41,42\}` is unrestricted.

The other 659 core edges remain fixed. This closes one deterministic cut
through the radius-seven shell. It does not close other choices of seven core
edges and is not global order-43 nonexistence.

## Preregistration and selection

The configuration and outcome policy were fixed before formula generation in
`results/benchmark_plans/proof_core_top7_cut_v1.json`, SHA-256
`85794252bf8c014a94cb69a31545be5245fc926f5bf42f94ea211c62eed2aab4`.

The seven edges are ranks 1–7 in the independently reproduced occurrence
ranking of fixed edges in the accepted 6,335-clause DRAT input core. Their
scores are \(104,102,101,101,100,96,94\). The ranking audit independently
reconstructed every source clause and found a unique ordered mapping for
every retained core clause:

- script SHA-256:
  `32d14b3e9aad496f9e3ea63a08f6271b0e7404c7b956f1008789b00bf95e91f9`
- result SHA-256:
  `3cd52e8c6f60e7d1923bc53c449a09ca93541eb27593a3f9e840ab76f60e4f65`

## Formula generation and independent reconstruction

```sh
python3 src/residual_lns_sat.py \
  results/best_candidates/exoo_seed_20260724.g6 \
  --free-incident-vertices 3,4,7,38,41,42 \
  --free-edge 0,32 --free-edge 18,33 --free-edge 18,20 \
  --free-edge 24,26 --free-edge 1,10 --free-edge 9,29 \
  --free-edge 27,29 \
  --output certificates/residual_lns_incident_six_plus_core_top7.cnf \
  --metadata certificates/residual_lns_incident_six_plus_core_top7.metadata.json
```

The formula has 244 variables and 52,148 clauses: 24,597
clique-prevention clauses and 27,551 independent-set-prevention clauses.

```sh
python3 verify/residual_lns_cnf_check.py \
  --graph results/best_candidates/exoo_seed_20260724.g6 \
  --cnf certificates/residual_lns_incident_six_plus_core_top7.cnf \
  --free-incident-vertices 3,4,7,38,41,42 \
  --free-edge 0,32 --free-edge 18,33 --free-edge 18,20 \
  --free-edge 24,26 --free-edge 1,10 --free-edge 9,29 \
  --free-edge 27,29
```

The independent checker reconstructed all 52,148 clauses in the exact order,
with zero missing or extra clauses.

## Proof production and verification

```sh
python3 src/certify_cnf_glucose.py \
  certificates/residual_lns_incident_six_plus_core_top7.cnf \
  --proof certificates/residual_lns_incident_six_plus_core_top7_glucose3.drat \
  --lrat certificates/residual_lns_incident_six_plus_core_top7_glucose3.lrat \
  --result certificates/residual_lns_incident_six_plus_core_top7_glucose3.result.json \
  --time-limit 300 \
  --proof-check-time-limit 1200
```

Glucose3 returned UNSAT in 0.458771 internal seconds (0.667263 wall):
14,441 conflicts, 20,480 decisions, and 234,062 propagations.

`drat-trim` accepted the ASCII DRAT. Its accepted core contains 7,449 of
52,148 input clauses and 7,921 of 14,442 lemmas, with 264,611 resolution
steps and zero RAT lemmas. Nonfatal deletion warnings are preserved in the
result transcript. The generated LRAT was independently accepted by
`lrat-check`.

## Artifact hashes

```text
CNF
cfbf69f7bb7646235ba195dae92aae38532ee7d869ef4f1b653c074c05cd4b42

metadata
190f6bbe19c2eb9f8a6bc187199064258d8d25e7caeb4e660ca288877a389af3

DRAT, 1,980,297 bytes
c1f75abad12de12f2db0e8fa30d3840320f54212a20679f22f42b1f5228ffeae

LRAT, 2,570,552 bytes
8e4c2ed3f44a55ee205a97015ac9d8a1d405927747bb4b97ffa22b9b9f1d07cc

result JSON
1576ca20a3fe9bd8d32ba39c69b950dbeb51c6e9ddb8770a4b62d072f6efd3c3
```
