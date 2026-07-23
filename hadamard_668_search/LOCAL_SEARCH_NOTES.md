# Fixed-q local-search lane

`search_special_local.cpp` is a dependency-free C++17 heuristic for the
reduced fixed-q equations.  It stores all 81 residual correlations exactly and
updates them in integer arithmetic after every move.

## Lossless normalization

The search fixes

```text
sum(X)=9, alt(X)=-9, x[0]=+1, x[82]=-1,
sum(Y)=9, alt(Y)=+9.
```

The signs of the ordinary sums are normalized by reversal/global-negation for
`X` and global negation for `Y`.  No endpoint of `Y` is fixed: after choosing
`sum(Y)=9`, fixing `y[0]` as well would not follow from the global-sign
symmetry.

Parity forces the displayed alternating sums.  For `X`, the even and odd
index sets have sizes 42 and 41; for `Y` they have sizes 41 and 40.  Thus the
four mutable parity groups have fixed positive populations

```text
X-even (endpoints excluded): 20 of 40
X-odd:                       25 of 41
Y-even:                      25 of 41
Y-odd:                       20 of 40
```

Every basic move swaps a positive and a negative sign inside one group.
Compound moves perform two such swaps in distinct groups.  Therefore every
visited state obeys all forced sums and endpoints without penalty terms.

## Build and run

```sh
clang++ -O3 -DNDEBUG -std=c++17 -pthread \
  search_special_local.cpp -o search_special_local

./search_special_local \
  --threads 8 --iterations 20000000 \
  --epoch 300000 --polish-steps 120 \
  --mode anneal --objective 0 --seed 668 \
  --output output/special_local_best.json
```

`--iterations` is a per-worker deterministic budget.  With it, fixed thread
count, seed, and options give reproducible independent walks.  Without it,
`--seconds` sets a wall-clock budget.  Exit status is zero only for energy
zero; a nonexact checkpoint exits with status 2.

The engine supports simulated annealing and sampled tabu search, four exact
objectives with the same zero set, projected starts from Eliahou's modular
seed, random feasible restarts, compound swaps, and exact exhaustive
best-swap polishing.

## Diagnostic result

The preserved checkpoint is `output/special_local_best.json`:

```text
energy = sum(R_k^2) = 576
nonzero residual lags = 60 of 81
max |R_k| = 6
sum |R_k| = 168
```

It was independently recomputed from the saved signs, including all sums,
endpoints, and 81 aperiodic correlations.  It is **not** an exact solution.

Search on this lane was stopped after the fixed-q problem was separately
reduced to the classified empty family `TU(41)`.  The checkpoint and engine
remain useful as regression diagnostics, but further heuristic effort on this
particular fixed-q system cannot produce an exact pair.
