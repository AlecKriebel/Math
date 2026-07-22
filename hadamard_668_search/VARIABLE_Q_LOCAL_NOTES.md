# Variable-q `BS(84,83)` local-search lane

`search_variable_q_local.cpp` is a dependency-free C++20 heuristic for the
288 nominal exact margin shards described in `VARIABLE_Q_LANE.md`.  Global
coordinate alternation reduces these to 156 search representatives, which is
the engine's default schedule.  It is not a proof procedure.  A checkpoint
becomes a result only if all 83 residuals vanish and `verify_variable_q.py`
independently expands the resulting special quadruple to a full `668 x 668`
Hadamard matrix.

## Exact state and ordinary moves

For each positive lag the engine stores

```text
r[k] = (c_k(A)+c_k(B)+c_k(C)+c_k(D)) / 2,   1 <= k <= 83.
```

The division is exact.  Its primary objective

```text
E_half = sum_k r[k]^2
```

has the unique zero `BS(84,83)`.  A basic move exchanges a positive and a
negative sign inside one sequence and one coordinate-parity class, so both
the ordinary and alternating sums of the selected shard are invariants.
Compound moves combine up to three such swaps.  All correlation changes are
maintained incrementally in integer arithmetic and checked periodically by a
complete recomputation.

## Endpoint-parity-preserving mode

The exact lag equations imply 83 sparse endpoint product parities.  A seed
satisfying these parities can be generated with

```sh
../tmp/hadamard-env/bin/python generate_variable_q_parity_seed.py \
  --shard 213 --output ../tmp/hadamard_668_runs/parity_seed_213.json
```

For each margin-preserving swap, the engine computes its 83-bit endpoint
syndrome over `GF(2)`.  Pairing swaps with equal syndrome gives a four-flip
move in the kernel.  A swap whose syndrome is already zero is admitted by
itself; these include legal reversal-paired swaps in the odd-length
sequences.  Therefore every state visited with
`--preserve-endpoint-parity` satisfies all endpoint equations exactly.  A
full invariant check is available at any interval through `--validate-every`.

Continue the current checkpoint with, for example,

```sh
clang++ -std=c++20 -O3 -DNDEBUG -pthread \
  search_variable_q_local.cpp -o search_variable_q_local

./search_variable_q_local \
  --threads 8 --seconds 300 --shard 213 \
  --initial output/variable_q_parity_best_canonical.json \
  --preserve-endpoint-parity --validate-every 1000000 \
  --output output/variable_q_parity_best_canonical.json
```

The unperturbed `--initial` checkpoint is published before workers start and
is always considered when the final output is chosen.  Thus a continuation
cannot accidentally replace a good checkpoint by a worse perturbed state.

## Bounded diagnostic results

The best unrestricted-margin checkpoint is
`output/variable_q_local_best.json`:

```text
E_half                         = 156
sum of squared base residuals = 624
nonzero lags                  = 54 of 83
odd half-residuals            = 36
maximum absolute base residual = 6
```

The tracked parity-feasible checkpoint is
`output/variable_q_parity_best_canonical.json` in shard 213:

```text
ordinary sums                   = (14,4,11,1)
alternating sums                = (14,8,5,7)
E_half                         = 232
sum of squared base residuals = 928
nonzero lags                  = 43 of 83
odd half-residuals            = 0
maximum absolute base residual = 8
sum of absolute base residuals = 192
```

At this documentation snapshot its SHA-256 is
`9c5e69534abd8db1abf69e493dbfb7640e2457b594c3a83a5c9dd0e45d39417f`.

The second checkpoint is in a strictly stronger feasible subspace, so its
larger raw energy is not a regression.  Independent recomputation matches
every stored correlation and all 83 endpoint products.  It remains nonexact:
43 correlations are nonzero, and the full-matrix verifier correctly rejects
it.

The historical `output/variable_q_parity_best.json` lies in shard 235.  Global
coordinate alternation maps it to shard 213 without changing any squared
residual, so 213 is the canonical representative now tracked.  The two files
have the same displayed residual metrics.  Additional endpoint-preserving runs
on shards 92 and 95 ended at half-energies 280 and 264 respectively.

Djokovic's short-pair quad switch is defined on this parity-feasible state and
preserves its entire residual vector.  A bounded continuation from the
switched state, and another from the canonical state, did not improve
half-energy 232.  These runs neither prove local optimality nor construct a
base sequence.  `switch_variable_q_candidate.py` performs the checked switch;
it rejects a short pair that does not satisfy the required quad products.

An independent deterministic scan exhausts the checkpoint's endpoint-parity-
feasible, same-margin neighborhood through six flipped coordinates.  The exact
counts and minimum half-energies are

```text
Hamming distance       2       4         6
distinct vectors      34   3,646   159,558
minimum E_half       272     248       280
```

The checkpoint's half-energy 232 is strictly smaller, and no exact vector
occurs in this bounded subspace.  This is a strict local-minimum statement only
through radius six with the same margins and endpoint parities; it gives no
claim at radius eight, in another shard, or about parity-infeasible
intermediate states.  See `VARIABLE_Q_PARITY_NEIGHBORHOOD.md` and reproduce it
with:

```sh
python3 variable_q_parity_neighborhood.py \
  output/variable_q_parity_best_canonical.json --max-exchanges 3
```

An independent exact CP-SAT experiment disables all symmetry quotients and
rules out every raw labeled vector with these same shard-213 margins through
Hamming radius 16.  It is not a cross-margin or unrestricted neighborhood
claim; `VARIABLE_Q_NEIGHBORHOOD.md` states the exact scope and statistics.
