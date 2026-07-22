# Unrestricted cyclic SDS at order 167

This is a fourth structured construction lane for `H(668)`.  It seeks four
length-167 sign sequences with complementary periodic autocorrelation, but
does not impose the skew/symmetric conditions of the smaller good-matrix
subfamily.

Status: implementation, strict compilation, sanitizer runs, exact single- and
compound-delta self-tests, checkpoint continuation, and bounded portfolio
runs completed; no order-167 candidate is claimed.

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
stored diagnostics.  The expanded self-test performs 10,000 single and 1,000
compound exact-delta checks.  Strict compilation and an AddressSanitizer plus
UndefinedBehaviorSanitizer continuation smoke test both pass.

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
