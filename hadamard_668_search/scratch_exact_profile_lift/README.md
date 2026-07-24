# Experimental exact lift of the first shell-two profile

## Status

This directory contains a resumable CP-SAT diagnostic for the first of the
five exact `n_9=2` profile-zero representatives.  It is secondary to the
quadratic-algebra work and carries **no negative result**.

`search_exact_profile_lift_xor.py` fixes all 24 profile IDs in the exact
216-sign order-three quotient, enforces the rank-18 first Hensel layer, and
retains all 58 exact quotient correlation equations.  A returned assignment
is expanded to two length-333 sign sequences and must pass a solver-free
check of all 166 nonzero periodic correlations before it can be saved.

The current exact model has 11,916 variables and 11,801 constraints on a
fixed row-margin shard.  A five-minute four-worker union run ended
`UNKNOWN`, after 1,674,513 branches, without a candidate.  Its peak resident
memory was about 604 MB and it used no swap.

`run_row_sum_shards.py` splits the exact row-margin join into the 72 compatible
catalog rows.  Attempt zero gave each shard five seconds with one worker:

```text
72 UNKNOWN, 0 feasible, 0 infeasible
```

This is a solver checkpoint only.  `UNKNOWN` proves nothing about any shard,
the fixed profile, `LP(333)`, or `H(668)`.

## Resume

Run from `hadamard_668_search` using a Python environment that contains
OR-Tools:

```text
python scratch_exact_profile_lift/run_row_sum_shards.py \
  --attempt 1 \
  --seconds-per-shard 60 \
  --jobs 4 \
  --memory-per-shard-mb 2500
```

The driver defaults to the current Python interpreter, refuses an aggregate
declared memory cap above 12 GB, writes one log per row-margin shard, and
atomically updates `output/row_sum_shards/checkpoint.json`.  Reusing an
attempt number skips completed `(row,attempt)` pairs; increasing `--attempt`
starts a new deterministic seed round.

The alternative `search_exact_profile_lift.py` is an earlier table-heavy
prototype.  It is retained locally for architectural comparison but is not
part of the resumable checkpoint.
