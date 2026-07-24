# Aggregate core-radius-seven bounded attempt

Date: 2026-07-23

## Outcome

**REPRODUCIBLE COMPUTATIONAL OBSERVATION:** the strict 120-second Glucose3
run returned `TIMEOUT`. This is neither SAT nor UNSAT. No proof, LRAT, or
model was produced, and no existence or nonexistence claim follows.

The formula allows every one of the 237 edges incident to
\(\{3,4,7,38,41,42\}\) to vary and permits at most seven changes among the
other 666 core edges relative to
`results/best_candidates/exoo_seed_20260724.g6`.

## Formula and independent check

```sh
python3 src/core_radius_cnf.py \
  --base-graph results/best_candidates/exoo_seed_20260724.g6 \
  --boundary-metadata certificates/residual_lns_incident_six.metadata.json \
  --radius 7 \
  --output /tmp/ramsey55_core_radius7.cnf \
  --metadata certificates/core_radius7.metadata.json

python3 verify/core_radius_cnf_check.py \
  --cnf /tmp/ramsey55_core_radius7.cnf \
  --graph results/best_candidates/exoo_seed_20260724.g6 \
  --boundary-metadata certificates/residual_lns_incident_six.metadata.json \
  --generation-metadata certificates/core_radius7.metadata.json \
  --radius 7
```

The formula has:

- 903 primary edge variables;
- 5,300 counter auxiliaries;
- 1,925,196 direct Ramsey clauses;
- 10,593 counter clauses;
- 6,203 variables and 1,935,789 clauses total;
- 88,338,852 bytes;
- SHA-256
  `e832e9ff558085c8431f889b1daed8cae2f19ce7a5c04d2c7b4a1873f6777643`.

The independent checker reconstructed every clause in the exact order and
returned `valid=true`, with zero missing clauses.

## Strict bounded solve

```sh
python3 src/certify_cnf_glucose.py \
  /tmp/ramsey55_core_radius7.cnf \
  --proof /tmp/core_radius7_glucose3.drat \
  --lrat /tmp/core_radius7_glucose3.lrat \
  --result certificates/core_radius7_glucose3.timeout.json \
  --time-limit 120 \
  --proof-check-time-limit 1200
```

The subprocess was terminated at 120.080041 wall seconds. The pipeline
deleted its partial proof and recorded:

```text
status TIMEOUT
proof_written false
lrat_written false
```

## Retained hashes

```text
metadata
07dc0eec0653252d76a95377829c5198aa78a52cfc3c96c5f21024050abcbfe9

independent formula check
0d0508a1a077c2db38f9d6bbd7c9b41ef1c85a385c69852d218e47beb65f990b

timeout record
0ee04601eaac1f416eeee634bbcce7316d112ed2503cb0807d0030c672e7cb78
```

The 88 MB CNF is deterministic and regenerable, so it is not duplicated in
the repository.
