# Research log

## 2026-07-24 PDT

- Created this folder without changing the active
  `eliahou_global_quotient_plan/` production program or output.
- Independently rebuilt canonical cases 21 through 29 and confirmed they are
  S02 through S18 in steps of two.
- Derived 78 variables, 39 equal-syndrome reflected pairs, quotient
  dimension 18, and rank-18 \(L/S\) projections in every case.
- Repeated all four-clique coefficient checks case by case: 2,126 forced
  zeros and 686 forced nonzeros in each.
- Proved algebraically that every quotient has an odd noncentral pair.
- Located the only failures of the preferred \(L\) gauge:
  - S08 / case 24: quotient 156922;
  - S14 / case 27: quotient 6143.
- Derived the exact exceptional \(S\)-gauge surcharge of 786,432 rows and
  the all-nine total of 3,710,853,316,608 rows.
- Froze all nine model hashes and algebraic invariants in
  `SHORT_BLOCK_CERTIFICATE.json`.
- Regenerated the case-26 model independently.  Its 247,808 bytes hash to
  `21d7895441a90c83031784ce339bccedeb664c9f0312549a1a2dd0c5993a7689`,
  exactly the model used by the active case-26 production.
- Added a parameterized C++ range kernel with dynamic \(L\)-else-\(S\)
  gauge, exact integer evaluation, bit-packed physical replay, survivor
  hashing, and exact-candidate retention.
- Added case-pinned atomic runner, resume validation, RSS/output guards,
  aggregation, and an independent NumPy range replay.
- Ran one quotient in every case; all nine completed exact integer and
  physical replay without error.
- On both exceptional quotients, dynamic \(S\)-gauge and ungauged runs
  produced identical full survivor counts, best witnesses, exact candidate
  lists, and survivor-stream hashes:
  - S08: 10 survivors, stream
    `0e4fb43eea71d68bf6e4f0b26724f74e9d63efbcdaedf2b336ecea6d60286c99`;
  - S14: 28 survivors, stream
    `52a8122d700244b6d0a3288c461dac98537e51f14ce65157c66b587679a85fb1`.
- Independently replayed case-26 quotient zero and the exceptional S08
  quotient through the NumPy join and original physical equations.  Both
  passed; peak RSS stayed below 344 MB.
- Re-ran a completed one-range job and observed zero recomputation, then
  produced a validated aggregate.
- Did not launch any whole new case.  No exact repair or \(H(668)\) is
  claimed.

### Frozen resume commands

After case-26 production finishes, run or resume the remaining eight cases
sequentially with:

```text
cd /Users/alec/Documents/Math-h668-local/hadamard_668_search/eliahou_short_block_census
for case_number in 21 22 23 24 25 27 28 29; do
  env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
    VECLIB_MAXIMUM_THREADS=1 \
    /Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
    run_short_block_census.py \
    --case "${case_number}" \
    --output "output/production-case${case_number}" \
    --workers 8 --chunk-size 1024 \
    --rss-limit-mib 8192 --output-limit-mib 100
done
```

The identical command is the resume command.  Aggregate afterward:

```text
cd /Users/alec/Documents/Math-h668-local/hadamard_668_search/eliahou_short_block_census
for case_number in 21 22 23 24 25 27 28 29; do
  /Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
    aggregate_short_block_census.py \
    --output "output/production-case${case_number}"
done
```

Create and independently replay a guarded two-quotient sample with:

```text
cd /Users/alec/Documents/Math-h668-local/hadamard_668_search/eliahou_short_block_census
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 \
  /Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  run_short_block_census.py \
  --case 21 --output output/bounded-case21 \
  --start 0 --stop 2 --chunk-size 2 --workers 1 \
  --rss-limit-mib 1024 --output-limit-mib 20
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 \
  /Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  replay_short_block_range.py \
  output/bounded-case21/ranges/range_000000_000002.json
```
