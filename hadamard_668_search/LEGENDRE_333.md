# Fixed-compression Legendre-pair lane

This lane searches for a binary Legendre pair of length 333.  Such a pair
constructs a two-circulant-core Hadamard matrix of order 668.  It uses the
conjectural factor-9 compression proposed for `p=37`, `q=3` in
[Kotsireas--Gallardo-Cava--Gomez--Gomez-Perez](https://doi.org/10.1016/j.jsc.2026.102606):

```text
C[0] = D[0] = 1
C[j] =  3 LegendreSymbol(j,37),  1 <= j < 37
D[j] = -3 LegendreSymbol(j,37),  1 <= j < 37.
```

The compressed seed is an informed restriction, not a necessary condition
for an arbitrary `LP(333)`.  Therefore an exhaustive failure within this lane
would not prove that `LP(333)` or `H(668)` does not exist.

Status: active restricted search; no Legendre-pair candidate has been found.

## Exact model

Boolean variables encode `+1`.  The 37 CRT-column cardinalities are fixed to
the prescribed compression for each sequence, giving 74 margin equations.
For each independent lag `1 <= s <= 166`, native Boolean parity constraints
define all cyclic difference bits and one cardinality equation imposes

```text
sum_i (A[i] XOR A[i+s]) + sum_i (B[i] XOR B[i+s]) = 334.
```

This is exactly equivalent to
`PAF(A,s) + PAF(B,s) = -2`.  The default symmetry reduction chooses canonical
representatives under independent shifts by multiples of 37 and inversion;
these operations preserve the fixed seed.

The full model contains 110,556 XOR definitions and 74 column-margin
equations.  Propagation also includes:

- an exact 504-row table for the two length-3 compressions;
- the five independent PAF equations for the two length-9 compressions;
- sharp per-lag bounds derived from pairs of fixed 9-bit column weights;
- explicit even half-distances for all 166 cyclic shifts;
- optional per-cycle distance parity through `--cycle-parity`.

The separate `--mod9-profile INDEX` mode fixes one exact row-compression
profile from `legendre_333_profile_catalog.py`.  It replaces the generic
modulo-3 table and 90 nonlinear modulo-9 products by 18 row-cardinality
constraints.  This is an exact but restricted sublane: a solution is a full
`LP(333)`, while infeasibility covers only the selected compressed-profile
orbit.  Because independent row shifts and reflections change a fixed
profile's orientation, this mode deliberately requires `--symmetry none`.
The current catalog contains 21 exact, orbit-distinct sampled profiles; it is
not claimed to be exhaustive.
`search_legendre_333_profile_catalog.py` reproduces the 18-variable outer
profile search with one worker, a default 128 MiB solver cap, exact
1,944-element orbit canonicalization, and atomic streamed JSON.  The default
outer-model symmetry chooses independent dihedral maxima for both length-9
vectors and then orders the two vectors; the common multiplier is still
handled by output canonicalization.  Its output
explicitly records that compressed witnesses are not Legendre pairs or
Hadamard certificates.  The optional centered-norm shard takes one of the 37
even values from 76 through 148; these disjoint invariant shards exactly
partition the outer model.

The experimental `--mod111-compression energy` mode exposes the remaining
proper divisor compression.  Its zero-lag equation says exactly 55 of the 222
three-sign blocks are monochromatic.  `--mod111-compression full` adds the 55
nonzero compressed PAF equations as well, with combined target `-6` at each
lag.  These constraints are exact but redundant with the complete lag model;
matched short trials did not outperform the default, so they remain off.

A reproducible one-worker comparison used seed 668 and a 10-second solver
limit for each mode under the default dihedral symmetry.  All three runs
ended `UNKNOWN`:

| length-111 mode | branches | conflicts | solver wall time |
|---|---:|---:|---:|
| `off` | 612,287 | 49 | 10.156 s |
| `energy` | 626,498 | 65 | 10.041 s |
| `full` | 571,036 | 51 | 10.018 s |

These single short runs are diagnostics, not evidence that one exact model is
asymptotically better.  They support keeping the redundant compression off by
default until a longer replicated benchmark shows a consistent advantage.

The cycle-level encoding is mathematically stronger but was slower in short
matched benchmarks, so it remains off by default.  Candidate acceptance is
repeated from scratch with standard-library integer arithmetic and then on the
full bordered two-circulant matrix.

`LEGENDRE_MULTIPLIER.md` describes a smaller exact order-three-invariant
sublane.  `LEGENDRE_LOCAL_NOTES.md` documents the independent C++ local engine
and its nonexact diagnostic checkpoints.  Its current profile-4 incumbent has
half-PAF energy 2280.  An independent radius-two replay covers 17,801,598
unique states.  A direct independent replay covers all 749,359,042
alternating-six-cycle/opposite-switch states and has exact minimum 2408; an
independent connected-eight-cycle replay covers 9,549,173 states and has
minimum 2568.  Neither neighborhood lowers the 2280 center.  These are finite
local results, not global lower bounds.
`LEGENDRE_SYMMETRY_OBSTRUCTION.md` gives a finite number-theoretic proof that
two sequences which are each symmetric or normalized skew under inversion
cannot form an `LP(333)`.  This obstruction does not depend on the fixed seed.
`legendre_column_distance_dp.py` independently proves that the current
fixed-column distance intervals are globally sharp: there are no hidden
endpoint improvements or gaps to add to the model.

## Reproduction

Create a solver environment using the repository's pinned requirement:

```sh
python3 -m venv .solver-venv
.solver-venv/bin/python -m pip install -r requirements.txt
```

Run arithmetic and model regression tests:

```sh
.solver-venv/bin/python -m unittest -v \
  test_legendre_333.py test_legendre_333_eight_cycle.py \
  test_legendre_333_profile_local.py \
  test_search_legendre_333_profile_catalog.py test_legendre_multiplier.py \
  test_legendre_column_distance_dp.py
.solver-venv/bin/python verify_legendre_333.py --self-test
```

Construct and validate the full model without searching:

```sh
.solver-venv/bin/python search_legendre_333_cp_sat.py --build-only
```

Sample additional exact compressed profiles without searching the 666 signs:

```sh
.solver-venv/bin/python search_legendre_333_profile_catalog.py \
  --count 1 --time-limit 2 --max-memory-mb 128 \
  --centered-norm-shard 82 --exclude-catalog \
  --output output/legendre_333_mod9_profile_sample.json
```

`--exclude-catalog` adds one exact forbidden-assignment table containing every
oriented image of each known orbit in the selected shard.  It therefore seeks
a genuinely new orbit instead of immediately returning the catalog hint; an
`UNKNOWN` result is still not an infeasibility certificate.

Run a presolve smoke test:

```sh
.solver-venv/bin/python search_legendre_333_cp_sat.py \
  --presolve-only --workers 1 --time-limit 15
```

Exercise the optional length-111 compression and the independent inversion
obstruction checker:

```sh
.solver-venv/bin/python search_legendre_333_cp_sat.py \
  --build-only --mod111-compression energy
python3 verify_legendre_symmetry_obstruction.py
```

Launch a bounded search:

```sh
.solver-venv/bin/python search_legendre_333_cp_sat.py \
  --workers 1 --max-memory-mb 2048 --time-limit 3600 \
  --output output/legendre_pair_333.json
```

Use the best exact-profile local checkpoint as a repaired CP-SAT phase hint
without trusting it as a candidate:

```sh
.solver-venv/bin/python search_legendre_333_cp_sat.py \
  --symmetry none --mod9-profile 4 \
  --hint output/legendre_333_profile4_radius2.json \
  --repair-hint --hint-conflict-limit 100 \
  --workers 1 --max-memory-mb 320 --time-limit 3600
```

Profile-checkpoint hints are first passed through the strict checkpoint
verifier.  CP-SAT then treats their 666 signs only as a fallible phase hint;
all 166 exact equations remain constraints.  A 15-second one-worker pilot
without repaired-hint mode returned `UNKNOWN` after 493,894 branches and 155
conflicts.  Full-model construction used 254 MB peak RSS; the solve used 703
MB total RSS and zero swap despite the solver-internal 320 MiB limit.  The
corresponding 10-second repaired-hint pilot at a 128 MiB solver limit also
returned `UNKNOWN`, after 222,444 branches and no conflicts, but reached 931
MB total RSS.  The limit does not include all Python, hint-repair, and presolve
storage.  These runs remain strictly nonconcurrent and are not being enlarged
on the 16 GiB host.

Independently verify any candidate JSON.  A passing candidate is also expanded
to the full bordered two-circulant `668 x 668` matrix and checked row by row:

```sh
python3 verify_legendre_333.py output/legendre_pair_333.json
```

`--diagnostic-last-lag` can build small non-certifying models for debugging.
The CLI deliberately refuses to write candidates from such a partial model.
