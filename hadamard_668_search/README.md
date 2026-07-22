# Hadamard order 668 search

Status: active computational research; no exact matrix has been found yet.

This directory is a reproducible attack on the smallest unresolved Hadamard
order.  A result counts only when an explicit `668 x 668` sign matrix passes an
exact, dependency-free check of `H H^T = 668 I`.  Near solutions and solver
status are diagnostics, never discoveries.

## Current map

| Lane | Status | Scope / finish line |
|---|---|---|
| Eliahou seed verification | reproduced near matrix | published 64-modular matrix of order 668, not an exact Hadamard matrix |
| Repair with Eliahou's exact `q` | impossible | reduces to empty `TU(41)` |
| Variable `s,q` special quadruple | active | `BS(84,83)` in 288 nominal shards / 156 alternation representatives |
| Fixed-compression `LP(333)` | active restricted lane | 166 periodic equations plus conjectural factor-9 margins |
| Order-three multiplier `LP(333)` | active restricted sublane | one of four subgroups ruled out |
| Symmetric/skew `LP(333)` | impossible sublane | mod-3 norm obstruction |
| Circulant good matrices of order 167 | active | two row-sum profiles; an exact quadruple gives a skew `H(668)` |
| Unrestricted cyclic SDS of order 167 | active heuristic lane | ten row-sum profiles; an exact quadruple gives `H(668)` |

The published 64-modular seed is encoded exactly in `seed.py`.  Run its full
regression check with:

```sh
python3 verify_seed.py
```

The initially natural repair lane—hold Eliahou's
`q=(83,2,81,1)` fixed and change `s`—is now closed.  A parity telescope forces
any exact repair to decimate to a Turyn sequence in `TU(41)`, but `TU(41)` is
empty.  The new reduction has a dependency-free symbolic checker and a
self-contained explanation:

```sh
python3 verify_fixed_q_obstruction.py
```

See `FIXED_Q_OBSTRUCTION.md` for the precise scope and literature dependency.
The old fixed-q CP-SAT, CNF, and local encodings are retained as regression
artifacts, not as live searches.

## Live lane 1: variable q and `BS(84,83)`

Allowing both `s` and `q` to vary is exactly the base-sequence problem
`BS(84,83)`.  `VARIABLE_Q_LANE.md` proves the bijection, derives 288 exhaustive
nominal ordinary/alternating margin shards, and quotients them to 156 search
representatives by global coordinate alternation.  It also documents the exact
CP-SAT model:

```sh
python3 -m venv .solver-venv
.solver-venv/bin/python -m pip install -r requirements.txt
python3 variable_q_base.py
.solver-venv/bin/python search_variable_q_cp_sat.py \
  --shard 0 --workers 1 --max-memory-mb 2048 --time-limit 3600
```

`VARIABLE_Q_LOCAL_NOTES.md` documents the margin- and endpoint-parity-
preserving C++ engine and its independently rejected diagnostic checkpoints.
The tracked parity-feasible checkpoint is now in canonical shard 213; it has
half-energy 232 and 43 bad lags, so it is not a solution.  The exact CP model
uses the standard four-literal base-sequence quad parities by default; the
older endpoint telescope is an equivalent optional basis.

`VARIABLE_Q_SEED_DISTANCE.md` now gives a global raw-radius-17 exclusion around
Eliahou's published base quadruple.  A dependency-free dynamic program first
enumerates every raw margin image and proves that no quad-preserving target is
reachable through radius 13.  Exact fixed-margin CP-SAT models with table-
encoded primitive 3rd-, 4th-, and 6th-root norms then eliminate all 197
margin-plus-quad targets through radius 16 and all 276 targets in the exact
distance-17 shell.  The recorded runs used one worker, peaked below 165 MB
resident memory, and made no exact-`BS(84,83)` claim outside this finite ball.

`VARIABLE_Q_PARITY_NEIGHBORHOOD.md` gives a deterministic exact scan inside
the checkpoint's same-margin, endpoint-parity-feasible subspace.  The
checkpoint is a strict local minimum against every such change of at most six
coordinates; this bounded result says nothing about radius eight, other
margins, or parity-infeasible intermediate states.

`VARIABLE_Q_NEIGHBORHOOD.md` records a separate CP-SAT search with every
symmetry quotient disabled.  The exact finite models through raw Hamming
radius 16 are `INFEASIBLE`: no exact base sequence with the checkpoint's
shard-213 margins occurs in that ball.  This result deliberately does not
cover different-margin neighbors, the raw shard-235 partner ball, or an
unrestricted 334-sign neighborhood.

`VARIABLE_Q_COMPRESSION.md` gives an exact factor-14 signature join over all
288 nominal shards.  It eliminates no shard and proves that this compression
is Fourier-equivalent to constraints already exposed in the CP model.  The
implemented factor-12 compression to length seven adds new primitive-seventh-
root propagation relative to those exposed invariants, but it also eliminates
no shard and remained slower in a short matched benchmark, so
`--compression-7` is optional.

`VARIABLE_Q_JOINT_COMPRESSION.md` derives a bounded-memory filter that couples
the primitive-7 compression to the compression after coordinate alternation,
thereby exposing primitive-14 information.  A 30-second shard-213 run ended
`UNKNOWN` at 111 MB peak RSS; it found neither a compressed witness nor an
infeasibility result.  The all-representative scan has not been run, so no
shard-elimination claim is made.

## Live lane 2: fixed-compression `LP(333)`

`LEGENDRE_333.md` describes the exact model inside the conjecturally motivated
factor-9 compressed subfamily, its further compression constraints, local
engine, and full bordered two-circulant verification:

```sh
.solver-venv/bin/python search_legendre_333_cp_sat.py \
  --workers 1 --max-memory-mb 2048 --time-limit 3600 \
  --output output/legendre_pair_333.json
```

`LEGENDRE_MULTIPLIER.md` gives a much smaller exact order-three-multiplier
sublane.  The subgroup generated by 112 is impossible by a direct lag-111
distance contradiction; the other three subgroup searches remain open.

`LEGENDRE_SYMMETRY_OBSTRUCTION.md` rules out every pair in which each sequence
is symmetric or normalized skew under inversion.  Modulo-3 compression
reduces the three symmetry-type cases to the impossible norm equations
`x^2+y^2=668`, `x^2+y^2=222`, and `x^2+3y^2=667`.  This does not use the
conjectural factor-9 seed.  The main solver also has optional exact
`--mod111-compression energy|full` propagation; short matched trials left it
off by default.  An exact transfer DP independently proves the existing
fixed-column distance bounds have no hidden endpoint improvements or gaps.

## Live lane 3: circulant good matrices of order 167

`GOOD_167.md` describes an independent route to a skew `H(668)`.  Symmetry and
the good-matrix product theorem reduce the search to two signed row-sum
profiles.  The exact CP-SAT model and a two-stage `GF(2)` filter are both
implemented, but bounded runs and random diagnostic scans have found no
candidate and prove no nonexistence result:

```sh
.solver-venv/bin/python search_good_167_cp_sat.py \
  --profile 0 --workers 1 --max-memory-mb 2048 --time-limit 3600 \
  --output output/good_167_profile_0.json
python3 verify_good_167.py --self-test
```

## Live lane 4: unrestricted cyclic SDS of order 167

`CYCLIC_SDS_167.md` removes the good-matrix symmetry restriction and searches
all ten cyclic supplementary-difference-set row-sum profiles.  The new local
engine is single-threaded and fixed-memory; its strict verifier checks every
periodic correlation and the full order-668 Goethals-Seidel matrix.  Strict,
sanitized compilation and the exact swap-delta self-test pass.  A 60-second
portfolio run completed 184,060,343 moves using 1.4 MB peak RSS and reached
quarter-energy 76 with 46 bad lags.  Its checkpoint is nonexact and is
deliberately rejected by the strict verifier; no candidate is claimed.

## Verification

Run the dependency-free arithmetic checks and the solver-backed unit suite:

```sh
python3 verify_seed.py
python3 verify_fixed_q_obstruction.py
python3 verify_legendre_symmetry_obstruction.py
python3 variable_q_base.py
python3 variable_q_compression_7.py --self-test
python3 verify_variable_q.py --self-test
python3 verify_variable_q_seed_radius.py
python3 verify_variable_q_seed_quad_radius.py
python3 verify_variable_q_seed_frontier_artifacts.py
python3 verify_good_167.py --self-test
python3 verify_sds_167.py --self-test
.solver-venv/bin/python -m unittest -v \
  test_construction.py test_legendre_333.py test_legendre_multiplier.py \
  test_legendre_column_distance_dp.py test_variable_q_base.py \
  test_variable_q_cp_sat.py test_variable_q_compression.py \
  test_variable_q_compression_7.py \
  test_variable_q_joint_compression.py test_variable_q_parity_neighborhood.py \
  test_variable_q_seed_distance.py test_variable_q_seed_quad_radius.py \
  test_variable_q_seed_frontier.py test_variable_q_seed_ball.py \
  test_good_167.py test_sds_167.py
.solver-venv/bin/python verify_legendre_333.py --self-test
```

Any future candidate from any live lane must be expanded to the full matrix
and checked exactly before it is treated as verified.

## Resource safety

This repository is currently run on a 16 GiB host.  The live CP-SAT commands
therefore default to one worker and set `max_memory_in_mb=2048`; the shard
scheduler runs attempts sequentially.  Do not launch concurrent solvers or
increase `--workers`/`--max-memory-mb` without checking available memory.  The
OR-Tools limit applies to the solver, not all Python/model-construction memory,
so it is a guardrail rather than an operating-system hard limit.  The exact
parity-neighborhood enumerator is intentionally capped at three exchanges;
larger meet-in-the-middle tables are not safe on this machine.
The seed-frontier models use a tighter 256 MiB solver cap and have remained
below 165 MB total RSS; the cyclic-SDS engine remained below 2 MB.  Recorded
searches are still run strictly one at a time.

Primary seed source: Shalom Eliahou, [A 64-modular Hadamard matrix of order
668](https://ajc.maths.uq.edu.au/pdf/93/ajc_v93_p422.pdf), *Australasian Journal
of Combinatorics* 93(2) (2025), 422-427.
