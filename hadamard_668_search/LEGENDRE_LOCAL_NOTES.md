# Fixed-compression LP(333) local-search lane

`search_legendre_333_local.cpp` is a dependency-free C++17 heuristic for the
fixed length-37 compression described in `LEGENDRE_333.md`.  It is a search
lane, not a proof procedure.  Every emitted state has the prescribed
compression, but only an independently verified zero-energy state would be a
Legendre pair and hence yield a Hadamard matrix of order 668.

## Exact state and moves

The two sign sequences are stored in the same `Z/9 x Z/37` CRT convention as
`legendre_333.py`.  In column `j`, the number of positive signs is fixed to

```text
j = 0:                  A = 5, B = 5
chi_37(j) = +1:         A = 6, B = 3
chi_37(j) = -1:         A = 3, B = 6.
```

A basic move exchanges a positive and a negative sign in one column of one
sequence.  Compound moves perform two or three disjoint exchanges.  Thus all
74 column margins, both total sign sums, and the fixed compression are
invariants rather than penalty terms.

For each independent cyclic lag `k=1,...,166`, the engine stores the exact
integer residual

```text
e[k] = (PAF_A(k) + PAF_B(k) + 2) / 2.
```

The primary energy is `sum(e[k]^2)`.  It is zero exactly when every Legendre
equation holds.  Several optional objectives have the same unique zero and
diversify parallel workers.

For a sign at position `p`, the engine caches its single-flip delta

```text
-s[p] * (s[p+k] + s[p-k])
```

at every independent lag.  Deltas for a multi-flip move are the sum of these
cached rows plus the exact correction for pairs whose two endpoints flip.
This scores a column swap in `O(166)`.  Accepted moves update both the
residuals and the cache in integer arithmetic.  Periodic full recomputation
checks abort on any discrepancy.

The search combines parallel restarts, geometric simulated annealing or
late acceptance, random compound moves, exact best-improvement descent over
all basic swaps, and sampled four-/six-flip polishing at basic local minima.

## Build and run

```sh
clang++ -O3 -DNDEBUG -std=c++17 -pthread \
  search_legendre_333_local.cpp -o search_legendre_333_local

./search_legendre_333_local \
  --threads 8 --seconds 15 \
  --epoch 150000 --polish-steps 64 \
  --compound-polish-samples 8192 \
  --mode anneal --objective 0 \
  --temperature-start 48 --temperature-end 0.2 \
  --validate-every 1000000 --seed 5668 \
  --output output/legendre_333_local_compound.json
```

Using `--iterations` instead of `--seconds` gives a per-worker deterministic
budget.  The program exits with status 0 only at zero energy; status 2 means
that it wrote a nonexact diagnostic checkpoint.

## Bounded diagnostic run

The command above evaluated 94,571,158 exact margin-preserving moves across
eight workers in 15.001 seconds, including 626 restart/polish epochs.  Its
preserved checkpoint is `output/legendre_333_local_compound.json`:

```text
sum(e[k]^2)                    = 1608
sum((PAF_A+PAF_B+2)^2)        = 6432
nonzero residual lags         = 126 of 166
max |PAF_A+PAF_B+2|           = 20
sum |PAF_A+PAF_B+2|           = 808
```

Independent verification was run with

```sh
python verify_legendre_333.py \
  output/legendre_333_local_compound.json
```

It recomputed `sum(A)=sum(B)=1`, both prescribed compressions, and all 166
integer correlation sums.  It reported `valid=false` with 126 bad lags, as
expected.  A separate arithmetic comparison also matched every correlation
and the recorded energy.  This checkpoint is **not** an LP(333) solution and
does not construct a Hadamard matrix of order 668.

If a later run reaches zero, the JSON must still pass
`verify_legendre_333.py` before it is treated as a discovery.

## Exact row-and-column profile engine

`search_legendre_333_profile_local.cpp` searches smaller fibers in which both
the 37 CRT-column sums and one exact nine-row compression profile are fixed.
The 21 currently catalogued profiles all have sequence sums one and combined
length-9 PAF `(594,-74,...,-74)`; they are orbit-distinct samples, not an
exhaustive list of all compressed profiles.

Every legal move is a `2 x 2` checkerboard switch in the `9 x 37` CRT matrix.
It preserves all row and column margins.  The same exact half-PAF residual
energy is updated in fixed-size integer arrays.  An optional compound proposal
atomically takes one legal switch in each sequence, so their PAF changes can
cancel while both margin fibers remain exact.

```sh
clang++ -std=c++17 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
  search_legendre_333_profile_local.cpp \
  -o ../tmp/search_legendre_333_profile_local
../tmp/search_legendre_333_profile_local --self-test
../tmp/search_legendre_333_profile_local \
  --profile 6 --seconds 60 --seed 677 \
  --mode anneal --temperature-start 128 --temperature-end 0.5 \
  --output output/legendre_333_profile6_local_60s.json
python3 verify_legendre_333_profile_local.py \
  output/legendre_333_profile6_local_60s.json
../tmp/search_legendre_333_profile_local \
  --initial-checkpoint output/legendre_333_profile6_local_60s.json \
  --cross-pair-polish --same-sequence-pair-polish \
  --six-cycle-polish --polish-only --seconds 60 \
  --output output/legendre_333_profile6_radius2.json
clang++ -std=c++17 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
  verify_legendre_333_profile_radius2.cpp \
  -o ../tmp/verify_legendre_333_profile_radius2
../tmp/verify_legendre_333_profile_radius2 \
  output/legendre_333_profile6_radius2.json
../tmp/search_legendre_333_profile_local \
  --initial-checkpoint output/legendre_333_profile4_radius2.json \
  --cross-pair-polish --same-sequence-pair-polish \
  --six-cycle-polish --mixed-six-cycle-polish --polish-only --seconds 360 \
  --output output/legendre_333_profile4_mixed.json
../tmp/search_legendre_333_profile_local \
  --initial-checkpoint output/legendre_333_profile4_mixed.json \
  --eight-cycle-polish --polish-only --seconds 30 \
  --output output/legendre_333_profile4_eight.json
clang++ -std=c++17 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
  verify_legendre_333_profile_mixed.cpp \
  -o ../tmp/verify_legendre_333_profile_mixed
../tmp/verify_legendre_333_profile_mixed \
  output/legendre_333_profile4_mixed.json
../tmp/verify_legendre_333_profile_mixed --eight \
  output/legendre_333_profile4_eight.json
```

The strict verifier owns the profile table and recomputes every row and
column margin, every stored correlation, both energy forms, the compression-
lift identity, and all redundant plus-count metadata.  It has a hard
zero-energy firewall: exact states may be accepted only by
`verify_legendre_333.py`, which constructs and checks the full matrix.

A four-second screen of the initial profiles 1 through 11 found profile 6 best at energy
2352.  Its 60-second run improved to energy 2320, with 135 bad lags, maximum
absolute raw PAF residual 20, and L1 residual 976.  Profile 0's retained
60-second checkpoint has energy 2416.  All were independently replayed and
are nonexact.  The production engine used at most 2.1 MB RSS with zero swap.

At the profile-6 checkpoint there are exactly 2,939 legal switches in `A` and
3,053 in `B`.  A complete rescore proves it is a strict one-switch local
minimum: the best neighbor raises energy from 2320 to 2400.  The exhaustive
cross-sequence polish then scored all `2,939 * 3,053 = 8,972,767` A/B switch
pairs, while the same-sequence polish scored 4,109,262 disjoint A pairs and
4,438,151 disjoint B pairs.  None improves E2320.  The combined production
scan also scored all 120,553 valid A and 126,980 valid B alternating
six-cycles.  It finished in 1.38 seconds at 4.42 MB RSS with zero swap.

`verify_legendre_333_profile_radius2.cpp` independently reconstructs and
collision-free deduplicates the complete product switch-graph ball through
radius two.  Two same-sequence switches are either disjoint, share one cell
and reduce to an alternating six-cycle, share an edge and reduce to one
checkerboard switch, or coincide and return to the center.  The verifier
counts exactly 17,661,680 unique states including E2320 and finds no lower
energy.  Its independent replay took 0.92 seconds at 72.4 MB RSS with zero
swap.  This finite theorem is not a lower bound on the whole profile fiber.

A subsequent 60-second continuation from the verified center used a 5%
coordinated A/B proposal mixture.  It evaluated 213,783,033 proposals over
855 restart basins and retained E2320 unchanged.  The run used 2.44 MB RSS and
zero swap.  This bounded heuristic outcome adds no nonexistence claim.

Centered-norm sharding subsequently found five additional exact compressed
orbits, now profiles 12 through 16, in invariant shards 82, 116, 130, 134, and
86.
They pass the same startup margin/PAF validation.  Ten-second screens reached
energies 2528, 2400, 2488, 2560, and 2480, respectively.  A 60-second profile-13
run then reached E2344 with 133 bad lags, maximum raw residual 20, and L1
residual 984.  Its complete radius-two engine polish found no improvement.
The generalized independent verifier confirms all 17,676,364 unique states in
that ball have energy at least 2344.  All five searches used at most 2.3 MB
RSS and zero swap; the independent audit used 72.6 MB.  None displaced the
then-current E2320 incumbent.

A later 60-second depth run on original profile 4 produced the current global
incumbent E2280, with 120 bad lags, maximum raw residual 20, and L1 residual
928 after 221,282,503 proposals.  The complete single/pair/six-cycle engine
polish found no improvement.  The generalized independent verifier then
enumerated 17,801,598 unique states in its product switch-graph radius-two
ball and confirmed that none has lower energy.  The search used 2.12 MB RSS;
the independent audit used 73.0 MB; both used zero swap.  The checkpoint is
still a nonexact near miss and constructs no Hadamard matrix.

The profile-4 incumbent was then scanned against the larger exact mixed
neighborhood that pairs an alternating six-cycle in either sequence with one
legal checkerboard switch in the other.  One complete pass processed
7,832,160 raw cycle patterns, 249,233 legal cycles, and all 749,359,042
possible cycle/switch pair distances.  Exact bounding-box pruning reduced the
number of point distances evaluated to 486,717,630 without approximation.
No move lowered E2280.  The pass completed in 285.28 seconds at 8.52 MB RSS
with zero swap, and its output signs are identical to the independently
verified radius-two center.  This closes one additional finite neighborhood;
it is not a lower bound on the full profile-4 fiber.

The separate direct verifier does not use the engine's KD tree or its pruning.
It evaluated all 749,359,042 mixed states, found unique minimum energy 2408,
and found no state tying or lowering E2280.  The minimum witness replay
preserved every margin and reproduced the energy.  This audit took 8.51
seconds at 4.03 MB RSS with zero swap.

The engine also streamed every connected simple alternating eight-cycle in one
sequence.  At profile 4 there are 9,549,173 such moves.  None improves E2280.
An independent DFS enumeration found exact minimum 2568 with multiplicity two
and replayed its first witness from scratch.  The audit took 0.97 seconds at
1.85 MB RSS with zero swap.  Disconnected two-four-cycle supports belong to
the separately audited pair neighborhood; this result does not cover arbitrary
eight-flip margin-preserving moves.

Exact outer-model orbit exclusion and a constructive 648-element subgroup
symmetry subsequently expanded the sampled catalog from 17 to 21 profiles.
Profiles 17 through 20 lie in centered-norm shards 82, 102, 108, and 130.
Their ten-second screens reached E2480, E2544, E2336, and E2408 respectively.
A 60-second continuation of profile 19 evaluated 214,957,700 proposals and
retained E2336.  The independent radius-two verifier covered 17,708,876 states
including the center without a descent.  Its independent eight-cycle replay
covered 9,526,800 states and found exact minimum 2448.  Profile 4 therefore
remains the catalog incumbent.  Every retained checkpoint is nonexact.
