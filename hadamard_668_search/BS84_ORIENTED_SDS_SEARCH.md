# Prime-83 oriented-SDS constructor

## Exact target

`search_bs84_oriented_sds.py` implements Stage A of the adjacent cyclic-fold
program in `NOVEL_BS84_THEORY.md`.  It seeks the endpoint-folded periodic
quadruple

```text
U_0=0, V_0=2, U_i,V_i,C_i,D_i in {+1,-1}
```

whose 41 independent nonzero periodic correlations sum to zero.  This is a
strictly weaker intermediate target than `BS(84,83)`, but every solution gets
an exhaustive finite lift test against the second, modulo-84 cyclic fold.

The model is organized by cyclic distance, not by 83 aperiodic lags.  Each
unordered pair of residues occurs once in exactly one equation.  The two
blocks omitting zero contribute `2*C(82,2)` products and the two ordinary
blocks contribute `2*C(83,2)`, for **13,448 Boolean products total**.  The 41
inverse pairs of `X,Y` are eight-state variables, so the oriented parity law
is true by construction.

Valid group actions remove some easy duplication:

- a common multiplier puts a member of nonempty `X` at residue 1;
- independent translations put members of nonempty `Z,W` at residue 0;
- the 45 fixed size profiles already anchor the available block negations and
  the `C,D` exchange.

No assumption of inversion symmetry, character-template structure, or
Eliahou-seed proximity is made.

## Resumable use

From the repository root:

```sh
.venv/bin/python hadamard_668_search/search_bs84_oriented_sds.py \
  --seconds-per-profile 10 --rounds 1 \
  --checkpoint hadamard_668_search/output/bs84_oriented_sds_stage_a.json
```

The default profile order first minimizes the total inverse-pair orientation
charge `|X|-|Y|`, then balances `Z,W`.  Every `(profile,round)` attempt is
written atomically.  Repeating the command skips recorded attempts; increase
`--rounds` for new deterministic seeds.  A focused run accepts a comma list:

```sh
.venv/bin/python hadamard_668_search/search_bs84_oriented_sds.py \
  --profiles 0,7,12 --rounds 3 --seconds-per-profile 60
```

The process enforces one solver worker and rejects memory settings above
4096 MB.  The checkpoint records wall time, conflicts, branches, and peak
process RSS for each attempt.

There is also a fixed-profile annealer that preserves the inverse-pair law
after every move.  It uses one- or two-pair orientation changes and
weight-preserving exchanges in `C,D`; every accepted residual update can be
recomputed exactly.

```sh
clang++ -std=c++17 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
  hadamard_668_search/search_bs84_oriented_sds_local.cpp \
  -o tmp/search_bs84_oriented_sds_local
tmp/search_bs84_oriented_sds_local \
  --profile 20 --seconds 600 --seed 668083 \
  --output hadamard_668_search/output/bs84_oriented_sds_local_p20.json
```

Resume from the retained best state by adding
`--initial PATH_TO_THE_SAME_JSON`.  A nonzero-energy file is explicitly
tagged `h668-oriented-sds-local-checkpoint-v1` and is not a certificate.  On
energy zero the engine changes the format to `h668-oriented-sds-v1`, after
which the strict Python verifier accepts it.

For a finite exact neighborhood test around a retained state, add
`--deep-polish`.  This uses additive 128-bit fingerprints only as a
meet-in-the-middle index; every fingerprint match is replayed across all 41
integer residuals.  Thus hash collisions can add work but cannot create a
false positive or false negative.

## Certificates and lifts

Every prime-fold solution is saved below
`output/bs84_oriented_sds_candidates/`.  The search immediately verifies it
without OR-Tools, then hash-joins all

```text
82 * 83^2 = 564,898
```

common-multiplier and independent `C,D` phase choices against the 42
modulo-84 equations.  A hash match is replayed against all 83 aperiodic
base-sequence equations.  If one survives, the retained artifact contains
the explicit `BS(84,83)` lift and the independent verifier expands and checks
the complete `668 x 668` Hadamard matrix.

Verify any retained artifact directly:

```sh
python3 hadamard_668_search/verify_bs84_oriented_sds.py \
  hadamard_668_search/output/bs84_oriented_sds_candidates/CANDIDATE.json
```

The verifier checks all 82 oriented-SDS equations and all 82 periodic lags,
not only the 41 modeled representatives.  A prime-fold-only artifact exits
successfully with `lift_present=false`; that is an exact Stage-A result, not
an `H(668)` claim.

Nonexact resumable checkpoints are rejected by default.  Their internal
profile, pair parity, direct PAF vector, oriented-SDS formula, energy, bad-lag
count, and maximum residual can be replayed explicitly:

```sh
python3 hadamard_668_search/verify_bs84_oriented_sds.py \
  --allow-checkpoint \
  hadamard_668_search/output/bs84_oriented_sds_local_p19.json
```

## Bounded pilot: no Stage-A object yet

No exact prime fold, `BS(84,83)`, or `H(668)` was found.

The complete 45-profile CP-SAT sweep at two seconds per profile returned
`UNKNOWN` on every profile.  It took 109.98 seconds, peaked at 252.0 MB RSS,
and used no swap.  Two additional 60-second attempts on profile 20 also
returned `UNKNOWN`, peaking at 237.6 MB.  These timeouts are not
nonexistence results.

The parity-preserving local engine screened eight priority profiles.  The
best independent-lag quarter-energies were:

```text
profile  7: 16        profile  9: 20
profile 11: 18        profile 18: 22
profile 19: 14        profile 20: 22
profile 26: 16        profile 30: 20
```

The retained profile-19 checkpoint has size tuple

```text
(|X|,|Y|,|Z|,|W|) = (37,37,35,41)
```

and row sums `(8,10,13,1)`.  Eleven of its 41 independent residuals are
nonzero: one has quarter-magnitude 2 and ten have magnitude 1, giving exact
quarter-energy 14.  Its SHA-256 is

```text
432b9708d77c7c45001265ad5ed0938e527af08a20782f0044d14a0ad65cc39c
```

An exact deep polish around this state found no zero.  The finite scan
covered all combinations in each of these families:

- changes supported on at most two inverse-pair states, one `C` exchange,
  and one `D` exchange;
- changes supported on at most two inverse-pair states, two `C` exchanges,
  and one `D` exchange, and the exchanged `C/D` version;
- two `C` exchanges together with two `D` exchanges;
- changes supported on at most three inverse-pair states together with one
  `C` exchange and one `D` exchange.

For the retained state the largest enumerated families contained 671,161
`C` double exchanges, 706,021 `D` double exchanges, and 559,531
three-pair-state changes.  The retained deep replay took 28.34 seconds under
concurrent system load, peaked at 927,006,720 bytes RSS (under 0.9 GiB), and
used no swap.  This closes a large
structured neighborhood of one near state; it does not exclude profile 19
or any other profile globally.

## Exact status

The new contribution is an exact, resumable construction layer and a
mechanically checked near checkpoint, not a Hadamard matrix.  The strongest
next move is to use the near state as the center of a larger algebraic
meet-in-the-middle lift (or as a CP-SAT neighborhood hint), rather than
repeat the same annealing seeds indefinitely.
