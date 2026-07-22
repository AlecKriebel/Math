# Exact same-margin neighborhood search

This experiment asks a narrowly defined repair question around the best
parity-feasible variable-`q` checkpoint.  It does **not** search every nearby
334-sign vector: all four ordinary and all four alternating margins are fixed
to shard 213 throughout.

The checkpoint is
`output/variable_q_parity_best_canonical.json`, with SHA-256

```text
9c5e69534abd8db1abf69e493dbfb7640e2457b594c3a83a5c9dd0e45d39417f
```

and margins

```text
ordinary    = (14, 4, 11, 1)
alternating = (14, 8, 5, 7).
```

Its half-correlation energy is 232, with 43 nonzero lags and no odd
half-residual.  Hamming distance below means ordinary coordinate distance on
the four raw, labeled sequences `A,B,C,D`, whose lengths total 334.  The model
constraint is `distance <= R`, not merely equality at the outer shell.

## Exact model and symmetry scope

`search_variable_q_cp_sat.py` imposes all 83 integer base-sequence
correlation equations, the eight selected margins, and exact redundant
spectral/parity propagation.  For this experiment it uses both equivalent
quad and endpoint parity bases.  Crucially, `--no-symmetry-breaking` removes
every reversal, negated-reversal, fixed-bit, and global-alternation lex
quotient.  A symmetry quotient is unsafe for this purpose because moving a
vector to its canonical representative can change its distance from the
fixed checkpoint.

The completed historical runs used OR-Tools 9.14.6206, four workers, and
random seed 1668.  Subsequent searches use the safer one-worker, 2,048 MiB
defaults on the 16 GiB host:

| Radius `R` | Status | Solver wall time | Conflicts | Branches | Limit |
|---:|---|---:|---:|---:|---:|
| 4 | `INFEASIBLE` | 1.318 s | 3,119 | 96,662 | 300 s |
| 6 | `INFEASIBLE` | 1.741 s | 4,813 | 222,919 | 300 s |
| 8 | `INFEASIBLE` | 8.201 s | 34,216 | 1,032,687 | 300 s |
| 10 | `INFEASIBLE` | 25.491 s | 127,486 | 2,599,675 | 600 s |
| 12 | `INFEASIBLE` | 114.924 s | 557,127 | 8,826,046 | 1,200 s |
| 14 | `INFEASIBLE` | 399.601 s | 2,307,319 | 24,643,747 | 2,400 s |
| 16 | `INFEASIBLE` | 1,487.746 s | 9,725,924 | 59,741,208 | 3,600 s |

Thus CP-SAT found the exact finite radius-16 model infeasible: no exact
`BS(84,83)` **with these shard-213 margins** occurs within raw Hamming
distance 16 of this checkpoint.  Fixed ordinary and alternating margins fix
the sign counts separately in each sequence/parity class, so every such
distance is even; the recorded radius-16 ball also covers the intervening odd
radii.  The radius-16 run used the resource-safe one-worker, 2,048 MiB
configuration and remained near 112 MiB resident memory.

This is not a general neighborhood claim.  It excludes neither a nearby
vector with different margins, nor the raw radius-14 ball around the
historical shard-235 representative, nor any unrestricted base sequence.
Shard 235 is globally alternation-equivalent to shard 213, but that
equivalence does not preserve distance to this particular labeled
checkpoint.  OR-Tools reports exact finite-model infeasibility but does not
emit a separately replayable SAT proof transcript here.

Reproduce the largest row with:

```sh
../tmp/hadamard-env/bin/python search_variable_q_cp_sat.py \
  --shard 213 \
  --hint output/variable_q_parity_best_canonical.json \
  --hint-distance 16 \
  --no-symmetry-breaking \
  --parity-basis both \
  --workers 1 --max-memory-mb 2048 \
  --random-seed 1668 --time-limit 3600
```

`VARIABLE_Q_PARITY_NEIGHBORHOOD.md` records a complementary deterministic
enumeration of every endpoint-parity-feasible same-margin vector through
distance six, including the minimum correlation energy at each exact even
distance.
