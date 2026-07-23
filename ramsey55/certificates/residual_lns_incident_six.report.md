# Six-residual-vertex incident-edge exact neighborhood

Date: 2026-07-23

## Result and scope

**REPRODUCIBLE COMPUTATIONAL OBSERVATION:** the deterministic exact solver
reached its strict 60-second limit on the 237-variable CNF. The outcome is
`TIMEOUT`, not `SAT` and not `UNSAT`.

No proof was produced, no candidate was exported, and this run supports no
existence or nonexistence conclusion. In particular, it does not establish
local minimality or global `(5,5;43)` nonexistence.

The neighborhood frees every edge with at least one endpoint in the residual
conflict union `{3,4,7,38,41,42}`:

- 15 edges within those six vertices;
- 222 edges from them to the other 37 vertices;
- 237 variables in total.

The other 666 edges remain fixed as in
`results/best_candidates/exoo_seed_20260724.g6`, whose SHA-256 is
`f5adf13e5791bb8fe4c58941e3d797c283223013290a2376935f1e1eef4ef31a`.

## Explicit incident-edge mode

The generator and independent checker now accept the clearly named option:

```text
--free-incident-vertices 3,4,7,38,41,42
```

It means that every pair having at least one listed endpoint is a Boolean
variable. The pre-existing `--free-vertices` mode continues to mean only
pairs induced within the listed vertex set. Both modes and explicit
`--free-edge` pairs can be combined; their union is deduplicated and sorted
lexicographically.

## Tests

```sh
python3 -m unittest -v tests/residual_lns_tests.py
```

All seven tests passed in 2.368 seconds. New coverage includes:

- exhaustive CNF/direct-graph equivalence over all 512 assignments of a
  small two-incident-vertex neighborhood;
- exact and deduplicated edge-set construction when induced, incident, and
  explicit modes are combined;
- independent-checker agreement on the same combined edge set;
- rejection of out-of-range incident vertices in both implementations;
- exact production coverage of all and only the 237 incident edges.

## Generation and independent formula reconstruction

Commands were run from `/Users/alec/Documents/Math/ramsey55`.

```sh
python3 src/residual_lns_sat.py \
  results/best_candidates/exoo_seed_20260724.g6 \
  --free-incident-vertices 3,4,7,38,41,42 \
  --output certificates/residual_lns_incident_six.cnf \
  --metadata certificates/residual_lns_incident_six.metadata.json
```

Generation took 2.50 seconds wall time. The formula contains:

| Variables | Clique-prevention clauses | Independent-prevention clauses | Total |
|---:|---:|---:|---:|
| 237 | 23,483 | 25,978 | 49,461 |

The generator was rerun and both the CNF and metadata were byte-identical.

```sh
python3 verify/residual_lns_cnf_check.py \
  --graph results/best_candidates/exoo_seed_20260724.g6 \
  --cnf certificates/residual_lns_incident_six.cnf \
  --free-incident-vertices 3,4,7,38,41,42
```

The independent checker directly decoded graph6 and reconstructed every
relevant 5-subset clause without importing the generator or graph-I/O module.
It returned `valid=true`, exact clause-order agreement, 49,461 reconstructed
clauses, zero missing clauses, and zero extra clauses. Internal runtime was
1.195414 seconds; wall time was 1.25 seconds.

## Strict bounded solve

```sh
python3 src/extension_sat_solver.py \
  certificates/residual_lns_incident_six.cnf \
  --time-limit 60 \
  --proof certificates/residual_lns_incident_six.tree
```

The solver returned:

```text
status TIMEOUT
runtime_seconds 60.0031763329971
wall_seconds 60.10
nodes 659
decisions 338
conflicts 320
propagations 11080
maximum_depth 38
```

The small internal overrun is the deadline-check granularity; the requested
budget was not extended. Because the outcome was `TIMEOUT`, the solver did
not write `certificates/residual_lns_incident_six.tree`. There is therefore
no proof to check. Candidate export and the two full-graph verifiers were
also inapplicable.

The exact timeout record is retained as
`certificates/residual_lns_incident_six.timeout.json`.

## SHA-256 hashes

```text
candidate graph6
f5adf13e5791bb8fe4c58941e3d797c283223013290a2376935f1e1eef4ef31a

CNF
bfa9d9e3edea9a5ac332614fc76984c9d287b1e8bf39d282199a09aab2b9c014

metadata
6377935d48dcebb4e7c402a6c39a8f1e73a1eeb58cc6918fc489d34e1f21c1fe

timeout record
f804d7bfe7ce5f1afc2d6224a297a314105fbb96c8d64e22417937a2e3fdd192

generator source
8a2d43317130d1002684b11491f488738e1bbfa0c0aa08bb8e6b00aeb9d35d37

independent CNF checker source
974b97774da888bdaadbe3ceda7373e5f5d17313462a9c57571d6b4e60a1d672

semantic/adversarial tests
372207d64e43b4014b04a6d673ac1fbdeac9c650252bab62bed2e734900ede1e
```

The retained CNF and metadata occupy 1,522,911 bytes.
