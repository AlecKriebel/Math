# Full-graph Hamming radius ten: checked formula, unresolved solve

Date: 2026-07-23 (America/Los_Angeles)

## Outcome

**CERTIFIED ENCODING; NO SAT/UNSAT CLAIM.** The formula encoding all
Ramsey(5,5;43) graphs at labeled edge-Hamming distance at most ten from
`results/best_candidates/core_kick_seed_20260731.g6` was generated and
independently reconstructed. The pinned proof-producing Glucose3 run then
reached its preregistered 300-second wall limit.

Consequently, radius ten is unresolved. No conclusion is drawn about this
Hamming ball, any larger Hamming ball, or global order-43 existence.

## Exact formula audit

The formula has:

- 903 primary edge variables;
- 9,878 auxiliary sequential-counter variables;
- 10,781 variables total;
- 1,925,196 Ramsey clauses;
- 19,746 Hamming-counter clauses; and
- 1,944,942 clauses total.

The independent structural checker regenerated the edge-variable order,
every Ramsey clause, and every counter clause. It found zero missing clauses,
matched all declared and expected counts, matched the metadata, and returned
`valid: true`.

## Solver outcome

The pinned streaming certification pipeline invoked Glucose3 with proof
logging and a 300-second wall limit. It returned:

```text
status               TIMEOUT
solver wall seconds  300.08740620799654
proof written        false
compressed LRAT      false
```

This is a resource-limit observation only. A timeout is neither SAT nor
UNSAT.

The frozen ladder rule required an immediate stop after any timeout, so
radii eleven and twelve were not generated or attempted.

## Artifact fingerprints

```text
frozen plan
3e58e6ff5cee60b309bbdd15b1dd432e56f8fb7dd75dbcbb5cf835df6f6f6580

CNF
cbe399bdce8025691609cbd5ce1cf2f966f6fe1bee38e02d45ac8ab23c0feff5

metadata
ee0805e2cf99eb61b74943c2a9a4cf3366a4d0600c98a2d670bf6f669cf9df5e

independent structural check
b525801de861033a4009e7e516eca9390373c5e4bf691f01495b5482dddc2f26

timeout result
7779e08924e6d149f0681fae9fbd6b3f83863cf3f056fc01fffab9dddf4c4e21
```

## Reproduction

From the `ramsey55` directory, the recorded proof attempt was:

```bash
python3 src/certify_cnf_glucose_streaming.py \
  certificates/core_kick_full_hamming_radius10.cnf \
  --proof certificates/core_kick_full_hamming_radius10_glucose3.drat \
  --lrat-zst certificates/core_kick_full_hamming_radius10_glucose3.lrat.zst \
  --result certificates/core_kick_full_hamming_radius10_glucose3.result.json \
  --time-limit 300 \
  --proof-check-time-limit 1800
```

The toolchain paths and hashes are embedded in the result record.
