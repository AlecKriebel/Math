# Construction Search Round 2

## Status

**NUMERICAL EVIDENCE ONLY — NOT A CONSTRUCTION CERTIFICATE OR AN UPPER
BOUND.**

No 41-, 42-, 43-, or 44-point code with maximum inner product at most
\(1/2\) was found.  Every decimal in this report was recomputed from
binary64 coordinates after row normalization.  Solver success, repeated
convergence, and small Gram eigenvalues do not prove feasibility,
nonexistence, or exact rank.

One exact theorem emerged from the construction program: an antipodal
five-dimensional kissing configuration has at most 40 points.  Its proof and
standard-library verifier are separate from these numerical experiments:

- [`../../proofs/antipodal_bound.md`](../../proofs/antipodal_bound.md);
- [`../../verifiers/verify_antipodal_bound.py`](../../verifiers/verify_antipodal_bound.py).

The resulting unrestricted negative-tail condition for hypothetical
41-codes is proved in
[`../../proofs/negative_tail_graph.md`](../../proofs/negative_tail_graph.md).

## Environment

The recorded runs used macOS arm64, Python 3.14.6, NumPy 2.5.1, and SciPy
1.18.0.  The discovery requirements are pinned in
[`requirements.txt`](requirements.txt).  NumPy's `default_rng` supplied every
random start.

The scripts test their source configurations and normalizations:

```sh
python3 -m venv /tmp/kissing5-round2-venv
/tmp/kissing5-round2-venv/bin/pip install \
  -r experiments/construction_round2/requirements.txt
/tmp/kissing5-round2-venv/bin/python -m unittest \
  experiments.construction_round2.test_numerical_tools -v
```

## Best independently generated 41-point candidate

The best new 41-point output in this round came from a rank-five linear image
of an E6-root subset.  Seed 22 deleted eight of the embedded D5 roots and
inserted nine E6 half-roots.  The program optimized the common \(6\)-to-\(5\)
linear map, released all point coordinates, performed graph-targeted
realization, and finally solved the direct minimax epigraph problem.

The recomputed result was

\[
\max_{i<j}\langle x_i,x_j\rangle
=0.5155570516153127.
\]

This is \(0.0155570516153127\) above the required threshold and is also worse
than the public \(0.514994652512\) benchmark.  It is not a construction.

Diagnostics:

- maximum squared-norm error: \(2.23\cdot10^{-16}\);
- five nonzero Gram eigenvalues:
  `7.927833788697091, 8.227612730690236, 8.232016831320697,
  8.304397752048608, 8.308138897243378`;
- largest absolute remaining Gram eigenvalue: \(3.38\cdot10^{-15}\);
- 155 pairs within \(10^{-8}\) of the maximum;
- active-degree histogram
  \(5^1,6^3,7^{14},8^{18},9^5\);
- active graph connected on all 41 vertices;
- binary64 coordinate-array SHA-256
  `d10164799035905d8bf28b74bcac41d6bcf6d8bf7f0b093641dd9414b2389b9c`.

The full coordinate and optimization log is
[`results/root_map_E6_N41_seed22.json`](results/root_map_E6_N41_seed22.json).
Its file SHA-256 is
`98d19401b228a743fbef9c1f59258a3e831990da64b350b080c5ac21ecbd9a25`.
Replay it with:

```sh
/tmp/kissing5-round2-venv/bin/python \
  experiments/construction_round2/root_map_surgery.py \
  --family E6 --n 41 --seeds 22 \
  --out /tmp/root_map_E6_N41_seed22.json
```

The final value agrees with the best pre-benchmark generic basin from round 1
to the displayed digits.  Thus the E6 seed found a known numerical basin by
a materially different route; it did not expose a new near-feasible family.

## Sharp negative-graph ansatz

The exact graph corollary forces at least 23 pairs with inner product
strictly below \(-1/2\).  The triangle-free graph
\(C_5\sqcup18K_2\) shows that 23 is sharp at the purely graph-theoretic
level; the theorem neither classifies equality graphs nor proves that this
example is spherically realizable.  It motivated the following targeted
41-point ansatz:

1. take the 20 D5 unoriented lines;
2. delete two lines;
3. retain both signs of the other 18 lines;
4. insert a regular pentagon in the span of the deleted lines;
5. perturb deterministically and optimize the 18 antipodal representatives
   and five remaining points.

Fifty pair-preserving starts, seeds 0--49, gave best constrained value

\[
0.5416720642083640
\]

at seed 27 (deleted line indices 0 and 13).  The complete compact ledger is
[`pair_cycle_seed_ledger.csv`](pair_cycle_seed_ledger.csv).  Nine
representatives of the best basin were then released into the unrestricted
41-point problem.  Their best result, after direct epigraph SQP, was seed 7:

\[
0.5205893864137946.
\]

The released candidate had 176 active pairs within \(10^{-8}\), active-degree
histogram \(5^3,6^9,8^3,9^8,10^{11},11^7\), and Gram eigenvalues

```text
7.536594285144909
8.152360407083876
8.404121960605103
8.404121960605105
8.502801386561016
```

The intended deep graph was also imposed directly through an epigraph slack:
all undesired pairs were constrained toward inner product at least \(-1/2\),
the five cycle edges toward at most \(-1/2-10^{-6}\), and all code pairs
toward the kissing upper bound.  Fourteen deterministic trials had positive
best local slack; the smallest was
`0.04272098128066848` (seeds 7 and 43 to displayed precision).  In particular,
the solver did **not** realize the target graph cell.  Positive local slack is
only a failed numerical search, not a proof that the cell is empty.

The full seed-7 log and coordinates are in
[`results/pair_cycle_seed7.json`](results/pair_cycle_seed7.json).
The file SHA-256 is
`5adc08b5bacae9e65edaa0abbff564a060e467a9982c4ca2240ee1e5f00e6e28`.
Replay:

```sh
/tmp/kissing5-round2-venv/bin/python \
  experiments/construction_round2/pair_cycle_ansatz.py \
  --seeds 7 --out /tmp/pair_cycle_seed7.json

/tmp/kissing5-round2-venv/bin/python \
  experiments/construction_round2/pair_cycle_ansatz.py \
  --no-release --seeds $(seq 0 49) \
  --out /tmp/pair_cycle_seeds_0_49.json
```

The constrained solutions with objective above \(1/2\) developed many
additional deep-negative pairs; therefore their observed deep graphs were
not \(C_5\sqcup18K_2\).  This is a diagnostic failure of the ansatz, not a
geometric obstruction theorem.

## Broken-symmetry layer mixtures

The layer search started from independent rotated blocks in \(S^3\), assigned
them distinct latitudes in \(S^4\), added pointwise tangent noise, and then
released every coordinate.  Four structurally different partitions were
tested for each cardinality.  Seed `2026072311` gave:

| \(N\) | Best starting layer sizes | epigraph-refined maximum |
|---:|:---|---:|
| 41 | \(16+8+8+8+1\) | 0.5175223212959956 |
| 42 | \(8+8+8+8+8+1+1\) | 0.5212296282474630 |
| 43 | \(5+5+5+5+5+5+5+5+3\) | 0.5262395764059031 |
| 44 | \(8+8+8+8+8+4\) | 0.5303550881204089 |

All four exceed \(1/2\), and the public numerical benchmarks are better.
The complete 16-run output is
[`results/layers_seed2026072311.json`](results/layers_seed2026072311.json).
Its file SHA-256 is
`f037b063588d43f98380c6c372fb340bb5aad7a0addffa37997d49b6ba1a1ea7`.
Replay:

```sh
/tmp/kissing5-round2-venv/bin/python \
  experiments/construction_round2/search_round2.py \
  --mode layers --n 41 42 43 44 --seeds 2026072311 \
  --output /tmp/layers_seed2026072311.json
```

## Higher-root projections and map surgery

The sources were generated internally and checked before optimization:

- 60 normalized D6 roots in \(\mathbb R^6\);
- 72 normalized E6 roots in \(\mathbb R^6\);
- 126 normalized E7 roots in \(\mathbb R^7\).

Each has source maximum inner product \(1/2\).  A preliminary scout projected
them to rank five and solved a binary maximum-compatible-subset problem for
ten directions (seeds `2026072300`--`2026072309`).  The largest subsets in
those samples were respectively 24, 27, and 25.  Coordinate projections
recover the 40-root D5 subsystem, but generic perturbations immediately split
its many boundary contacts.  This calculation uses a floating-point graph
threshold and says nothing about all projections.

The more flexible map-surgery program selects \(N\) source roots, optimizes an
arbitrary common \(6\)-to-\(5\) linear map, and then releases all \(N\)
coordinates.  For \(N=41\), 30 seeds for each of D6 and E6 were run; seed 22
gave the result described above.  Four scouting seeds for each of
\(N=42,43,44\) gave no improvement over the layer results or public
benchmarks.

## Projective-line search and exact follow-up

An independent search optimized 21 and 22 unoriented lines in
\(\mathbb R^5\), because coherence at most \(1/2\) would yield antipodal
42- or 44-point codes.  Fifty random starts for each size and eighty
D5-anchored insertion/surgery starts for each size found:

| lines | antipodal points | best observed coherence |
|---:|---:|---:|
| 21 | 42 | 0.5459083132623573 |
| 22 | 44 | 0.5574118159706004 |

As a calibration, the same pipeline recovered coherence \(1/2\) from
unperturbed and lightly perturbed 20-line D5 starts.  The numerical failures
were not used as an upper bound.  Instead, their structure suggested the
exact degree-four projective Delsarte argument in
[`../../proofs/antipodal_bound.md`](../../proofs/antipodal_bound.md), which
rigorously proves that 20 lines are maximal.

Replay:

```sh
/tmp/kissing5-round2-venv/bin/python \
  experiments/construction_round2/antipodal_lines.py \
  --line-count 21 22 --kinds random --seeds $(seq 400 449) \
  --out /tmp/antipodal_random.json

/tmp/kissing5-round2-venv/bin/python \
  experiments/construction_round2/antipodal_lines.py \
  --line-count 20 21 22 --kinds d5plus d5surgery \
  --seeds $(seq 600 639) --out /tmp/antipodal_d5_anchored.json
```

## What may and may not be inferred

- The round found no configuration of 41--44 points meeting the kissing
  threshold.
- It independently rediscovered a \(0.515557051615\) 41-point basin from an
  E6-map seed.
- The sparse deep-negative graph ansatz did not survive local realization or
  symmetry release.
- None of these failures bounds the global optimum, covers a continuous
  parameter space, or rules out any contact graph.
- The antipodal bound and forced-negative-tail lemma are exact because their
  proofs and verifiers use symbolic rational/integer arguments; they do not
  inherit validity from these numerical searches.
