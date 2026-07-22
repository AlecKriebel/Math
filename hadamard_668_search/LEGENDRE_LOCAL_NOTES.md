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
