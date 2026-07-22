# Unrestricted cyclic SDS at order 167

This is a fourth structured construction lane for `H(668)`.  It seeks four
length-167 sign sequences with complementary periodic autocorrelation, but
does not impose the skew/symmetric conditions of the smaller good-matrix
subfamily.

Status: implementation, strict compilation, sanitizer runs, exact single- and
compound-delta self-tests, checkpoint continuation, bounded portfolio runs,
an exhaustive independent-decimation orbit, the complete fixed-profile
Hamming-radius-four audit, and an exact aligned four-window union completed;
no order-167 candidate is claimed.

## Exact target

For sequences `A,B,C,D`, require

```text
PAF_A(k)+PAF_B(k)+PAF_C(k)+PAF_D(k)
  = 668  if k=0,
  = 0    otherwise.
```

Their four circulants then fill the Goethals-Seidel array and give a Hadamard
matrix of order 668.  Independent sequence negations and permutations make
the row sums positive and sorted.  The trivial-character equation leaves ten
profiles:

```text
(1,1,15,21)   (1,9,15,19)   (3,3,5,25)    (3,3,11,23)
(3,3,17,19)   (3,7,9,23)    (3,7,13,21)   (3,9,17,17)
(5,9,11,21)   (7,13,15,15)
```

Equivalently these are the ten cyclic supplementary-difference-set parameter
sets already enumerated by `analyze_sds_167.py`.  The earlier multiplier
audit rules out only the order-83 common-orbit method; it does not rule out
unrestricted cyclic blocks.

## Low-memory local engine

`search_sds_167_local.cpp` preserves one row-sum profile by exchanging two
opposite signs within a sequence.  For a swap at positions `p,q`, every one
of the 83 independent periodic residuals is updated exactly in constant work,
so a move costs `O(83)` and the annealer stores only fixed-size arrays.  The
optional deterministic polish uses explicitly capped move pools.  A
compound move couples exchanges in two, three, or four distinct sequences;
their exact residual deltas add.  `--compound-probability` mixes these moves
with ordinary single exchanges.  The engine is single-threaded.  Simulated
annealing is a heuristic: a nonzero checkpoint is only a diagnostic, never
evidence of nonexistence.

Every zero is fully recomputed before it is written with kind
`cyclic_sds_167`.  `verify_sds_167.py` then checks strict order/metadata, all
167 periodic sums, and every row product of the resulting `668 x 668` matrix.
The generic regression fixture constructs and verifies `H(12)`.

Compile and validate with:

```sh
clang++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror \
  search_sds_167_local.cpp -o ../tmp/search_sds_167_local
../tmp/search_sds_167_local --self-test
python3 verify_sds_167.py --self-test
```

A bounded one-core portfolio run is:

```sh
../tmp/search_sds_167_local --seconds 600 --profile -1 --seed 668 \
  --output output/sds_167_local_best.json
```

The recorded 60-second validation run used seed 668 across all ten profiles.
It completed 184,060,343 exact-delta moves and 185 restarts, used 1.4 MB peak
RSS with no swaps, and reached profile `(3,7,9,23)` with quarter-energy 76 and
46 bad lags.  The output kind is deliberately
`cyclic_sds_167_checkpoint`; the strict verifier rejects that kind, so this is
only a diagnostic checkpoint and not a Hadamard candidate.

Reproduce that bounded run with:

```sh
../tmp/search_sds_167_local --seconds 60 --profile -1 --seed 668 \
  --output output/sds_167_local_best_60s.json
```

The engine can now continue a verified checkpoint and repeatedly perturb the
incumbent before annealing:

```sh
../tmp/search_sds_167_local --seconds 60 \
  --initial output/sds_167_local_best_60s.json \
  --restart-from-best --perturb-exchanges 8 \
  --move-arity 3 --compound-probability 0.05 --seed 668 \
  --output output/sds_167_local_continued.json
```

The JSON loader recomputes all residuals and energy rather than trusting
stored diagnostics.  The expanded self-test performs 10,000 single, 1,000
cross-sequence compound, and 100 same-sequence compound exact-delta checks.
Strict compilation and AddressSanitizer plus UndefinedBehaviorSanitizer runs
both pass.

Bounded continuation experiments did not improve the energy-76 incumbent:
six 10-second incumbent-restart schedules, four 10-second pure-compound
schedules, and three 20-second mixed schedules at compound probabilities
`0.01`, `0.05`, and `0.10` all returned energy 76.  A separate
10-second-per-profile screen reached quarter-energies
`84,82,88,80,82,82,82,82,88,78`; none beat the cross-profile incumbent.
These are heuristic diagnostics only.

## Energy-64 continuation and deterministic compound polish

A 600-second continuation from the energy-76 checkpoint used seed 12668,
three-sequence moves with probability `0.05`, and incumbent perturb/restart.
It evaluated 1,628,953,659 exact moves across 1,629 restart basins and found a
new profile-5 checkpoint:

```text
row sums                         = (3,7,9,23)
quarter-energy                   = 64
nonzero independent lags        = 46 of 83
maximum absolute raw residual   = 8
quarter-residual histogram      = {-2:2, -1:22, 0:37, 1:18, 2:4}
```

The run used 1.4 MB peak RSS and zero swaps.  Independent Python arithmetic
recomputed all 167 stored periodic sums and the energy.  The preserved file
is `output/sds_167_local_continued_600s.json`, with SHA-256

```text
3c4a23d1190ed74e464dc66e852dd0730c97cfd4f1d12aa4946de05aff5a8edd
```

It remains a `cyclic_sds_167_checkpoint`, not a candidate, and the strict
verifier rejects its kind.

The engine now has a deterministic compound-polish option.  It ranks every
single exchange in each sequence, keeps a bounded pool, and evaluates exact
cross-sequence combinations.  On the energy-64 checkpoint, a pool size of
8192 includes every possible opposite-sign exchange.  The resulting
14.28-second scan proves that no single exchange and no pair of exchanges in
distinct sequences lowers the energy.  A separate 219.57-second scan found
no improving triple among the best 1,024 exchanges per sequence.  Both scans
used 11.5 MB peak RSS and zero swaps.  The pair statement is exhaustive for
that move class; the triple statement is only for the displayed pools.

Reproduce the bounded scans with:

```sh
../tmp/search_sds_167_local \
  --seconds 1 --initial output/sds_167_local_continued_600s.json \
  --pair-polish-size 8192 --pair-polish-steps 1 --pair-polish-arity 2 \
  --output output/sds_167_pair_polish.json

../tmp/search_sds_167_local \
  --seconds 1 --initial output/sds_167_local_continued_600s.json \
  --pair-polish-size 1024 --pair-polish-steps 1 --pair-polish-arity 3 \
  --output output/sds_167_triple_polish.json
```

Strict compilation, the expanded delta self-test, and an ASan/UBSan
triple-polish continuation smoke test all pass.

## Exact decimation orbit and complete Hamming-radius-four audit

For a sequence `x` on `Z_167`, decimation by a nonzero multiplier `d` sends
its periodic autocorrelation to `PAF_x(d*k)`.  Since `PAF_x(-k)=PAF_x(k)`,
each sequence has 83 possible multiplier classes.  Multiplying all four
decimations by one common class only permutes the lag labels, so the first
multiplier can be fixed to one.  The `--decimation-scan` mode therefore
exhausts exactly

```text
83^3 = 571,787
```

relative decimation tuples.  On the energy-64 checkpoint, the identity tuple
is the lexicographic winner for each invariant ranking `(E,Q,max,B)`,
`(Q,E,max,B)`, and `(max,Q,E,B)`, where

```text
E = sum r_k^2 = 64
Q = sum r_k^4 = 136
B = number of nonzero r_k = 46
max |r_k| = 2
```

No decimation improves any displayed primary metric.  The optimized exhaustive
pass took 0.33 seconds and 1.4 MB peak RSS.  An independent standard-library
Python enumeration of all 571,787 tuples reproduced the energy winner in
20.08 seconds at 16.8 MB peak RSS.  A sanitized C++ pass also reproduced the
result.

The incumbent is much more strongly isolated under sign exchanges.  A state
at raw labeled Hamming distance at most four that preserves all four row sums
is necessarily one of:

```text
identity                                             1
one opposite-sign exchange                         27,722
two exchanges in one sequence                  46,884,138
one exchange in each of two sequences         288,185,440
total                                           335,097,301
```

The same-sequence scan uses the exact four-flip autocorrelation interaction
term; two deltas from the same sequence cannot merely be added.  Across all
335,097,301 states, only the incumbent attains energy 64, and only the
incumbent attains quartic value 136.  The minimum maximum residual remains 2
and is attained by 5,442 states.  In particular, no exact cyclic SDS lies in
this complete fixed-profile Hamming-radius-four neighborhood.  This is a
finite local theorem around the stored profile-5 checkpoint, not a global
nonexistence result.

The optimized same-sequence and cross-sequence passes took 6.34 and 11.88
seconds, respectively, with peak RSS 3.9 and 11.5 MB and zero swaps.  Full
ASan/UBSan repetitions took 15.13 and 28.09 seconds at under 29 MB peak RSS.
Reproduce the three exact scans with:

```sh
../tmp/search_sds_167_local --decimation-scan \
  --initial output/sds_167_local_continued_600s.json \
  --output /tmp/sds_167_decimation.json

../tmp/search_sds_167_local --same-sequence-pair-scan \
  --initial output/sds_167_local_continued_600s.json \
  --output /tmp/sds_167_same_sequence_pair.json

../tmp/search_sds_167_local --cross-sequence-pair-scan \
  --initial output/sds_167_local_continued_600s.json \
  --output /tmp/sds_167_cross_sequence_pair.json

python3 verify_sds_167_neighborhood.py \
  --engine ../tmp/search_sds_167_local
```

`--scan-objective energy|quartic|maximum` selects which independently tracked
champion is materialized.  Every materialized output is fully recomputed.  The
standard-library verifier pins the incumbent SHA-256, independently derives
all combinatorial class counts, independently re-enumerates the full relative
decimation orbit, replays both radius-four scans, and checks the combined tie
counts.  Its complete replay took 28.96 seconds at 25.5 MB peak RSS with zero
swaps.

The local annealer also accepts `--bad-lag-penalty N`, recording both its raw
energy and shaped score.  Three 60-second screens at penalties 2, 4, and 16
did not displace the energy-64 incumbent.  Bad-lag count is only a diagnostic:
a large positive penalty can favor a few concentrated residual spikes, so
future shaped runs should prioritize quartic residual scoring instead.

## Quartic shaping and exact guided-window scans

The annealer now minimizes the configurable score

```text
w_E E + w_Q Q + w_B B,
```

while exactness remains tied exclusively to `E=0`.  A 60-second pure-quartic
screen evaluated 152,303,355 proposals without lowering `Q=136`.  A separate
120-second screen proposed an exact two-plus/two-minus move within one
sequence 30% of the time; it evaluated 237,719,274 proposals across 1,189
basins and also left the incumbent unchanged.  Both remained below 1.5 MB
peak RSS with zero swaps.  These are heuristic diagnostics.

Three deterministic modes then exhaust finite domains selected by the best
single-exchange quartic scores:

- A single-block `H=12` window contains 12 incumbent plus positions and 12
  minus positions.  All `C(24,12)` row-sum-preserving assignments are visited.
  Six support-disjoint families across all four sequences cover 64,899,721
  unique states and contain no exact SDS or improvement of `E`, `Q`, or the
  maximum residual.
- A paired `H=6` window enumerates `C(12,6)^2=853,776` assignments for each
  pair of sequences.  Twelve families and all six sequence pairs give
  61,471,872 evaluations representing 61,383,193 unique states.  No exact SDS
  or metric improvement occurs.  The evaluation count includes overlaps
  between pair domains, and reported tie counts are evaluation multiplicities.
- The four-block `H=6` meet-in-the-middle mode enumerates all 924 assignments
  in each of four sequence windows.  It stores the 853,776 assignments of the
  first pair and probes all 853,776 assignments of the second pair.  The two
  unsigned 64-bit fingerprints are linear modulo `2^64`: every exact zero
  must be a fingerprint match, and every match is replayed against all 83
  residuals.  Collisions can therefore cause extra comparisons but neither a
  false exclusion nor a false solution.

Each aligned four-window family exhausts

```text
924^4 = 728,933,458,176
```

states.  The twelve supports are disjoint within every sequence, so distinct
aligned family domains intersect only at the incumbent.  Their union has

```text
1 + 12 * (924^4 - 1) = 8,747,201,498,101
```

unique states.  The exact scan found no SDS.  It took 2.36 seconds at 24.7 MB
peak RSS with zero swaps.  A one-family ASan/UBSan replay passed at 44.2 MB.
This is another finite local exclusion: it does not cover windows made by
mixing different family indices among the four sequences, nor arbitrary
fixed-profile states.

Reproduce the deterministic scans and the independent audit with:

```sh
../tmp/search_sds_167_local --window-scan-half-size 12 \
  --window-family-count 6 \
  --initial output/sds_167_local_continued_600s.json \
  --output /tmp/sds_167_window.json

../tmp/search_sds_167_local --paired-window-half-size 6 \
  --window-family-count 12 \
  --initial output/sds_167_local_continued_600s.json \
  --output /tmp/sds_167_paired_window.json

../tmp/search_sds_167_local --four-window-mitm-half-size 6 \
  --window-family-count 12 \
  --initial output/sds_167_local_continued_600s.json \
  --output /tmp/sds_167_four_window.json

python3 verify_sds_167_windows.py \
  --engine ../tmp/search_sds_167_local
```

The verifier pins the checkpoint hash, independently rebuilds and directly
enumerates a `6^4=1,296` small instance, replays the full scan, checks every
large window's signs and support disjointness, and verifies all MITM domain
counts.  It passed in 2.47 seconds at 25.4 MB peak RSS with zero swaps.

The generic checkpoint field `moves` stores a mode-specific primary counter:
unique cases for the single-window scan, raw evaluations for the paired scan,
and right-pair probes for the MITM.  The complete conceptual and unique domain
counts are printed by each deterministic mode; the MITM counts are also
checked by the independent verifier.  `moves` must not be compared across
modes as if it had one common unit.

Only an exact output should be passed to:

```sh
python3 verify_sds_167.py output/sds_167_local_best.json
```

Primary background:

- D. Z. Djokovic, O. Golubitsky, I. S. Kotsireas,
  [*Some new orders of Hadamard and skew-Hadamard matrices*](https://arxiv.org/abs/1301.3671),
  which uses cyclic SDS and the Goethals-Seidel array with a large-scale
  matching search.
- D. Z. Djokovic, I. S. Kotsireas,
  [*Goethals--Seidel difference families with symmetric or skew base blocks*](https://arxiv.org/abs/1802.00556),
  for the structured subfamilies containing the good-matrix lane.
