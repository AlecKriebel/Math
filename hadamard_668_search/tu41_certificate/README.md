# Independent certificate that `TU(41)` is empty

This directory contains a completed, low-memory, deterministic enumeration of
normalized Turyn sequences with short length 41 (long length 42).  The result is

```text
461 / 461 canonical shards complete
57,543,021 search nodes
0 solutions
```

The recorded run took 362.92 seconds summed over the serial shards on an Apple
M1 Pro.  The slowest shard took 10.70 seconds.  A separate timed replay of that
shard used 1,376,256 bytes maximum RSS as reported by macOS `/usr/bin/time -l`.
Raw per-shard reports are intentionally not in the repository; the strict,
compact result index and its hashes are in `shard_results.json` and
`certificate.json`.

This computation is disjoint from the fixed-`q` reduction in the parent
repository.  It establishes only `TU(41) = empty`.  Connecting that fact to a
particular Hadamard-668 search lane requires a separate reduction.

## Exact search space

For odd `n=41=2m+1`, `m=20`, Definition 7(i) of
Edmondson--Seberry--Anderson gives the normalized forms

```text
A = (1,1,a2,...,a20,-a20,...,-a2,-1,-1)
B = (1,1,b2,...,b20,-b20,...,-b2,-1, 1)
C = (1,c1,...,c19,c20,c19,...,c1,1)
D = (1,d1,...,d19,d20,d19,...,d1,1).
```

There are `19+19+20+20=78` free signs.  The required equations are

```text
N_A(j) + N_B(j) + N_C(j) + N_D(j) = 0,   1 <= j <= 41,
```

where `N_S(j) = sum_i S_i S_(i+j)` is aperiodic autocorrelation.

The enumeration uses these exact, elementary consequences:

1. `C` and `D` are interchangeable, so their free sign vectors are restricted
   to lexicographic order, with `+1` before `-1`.
2. Evaluating the complementary polynomial identity at `z=1` gives

   ```text
   sum(A)^2 + sum(B)^2 + sum(C)^2 + sum(D)^2 = 166.
   ```

   The displayed normal forms have `sum(A)=0` and `sum(B)=2`, hence
   `sum(C)^2+sum(D)^2=162`.  The only integral possibility is
   `|sum(C)|=|sum(D)|=9`.  Each short sequence therefore has 16 or 25 negative
   entries.
3. After symbolic cancellation, the equations at lags 39 down to 20 introduce
   all variables in blocks of 3, eighteen blocks of 4, and a final block of 3.
   A branch is retained only when the newly complete high-lag equation is
   exactly zero.
4. A partial lower-lag bound with fixed contribution `F` and `U` unresolved
   product terms rejects only if `|F|>U` or `F+U` is odd.  This is a necessary
   condition even when unresolved products are dependent, so it cannot remove
   a solution.
5. At every leaf, all 41 positive-lag equations are evaluated directly.

After the first five recursive steps, 19 signs have been assigned.  Exactly 461
prefixes survive.  `verify_cube_cover.py` independently rebuilds the first five
correlation polynomials in Python, exhausts all `2^19` assignments, and verifies
that `cubes_depth5.txt` is exactly this feasible canonical set.

## Certificate files

- `enumerate_tu.cpp` — dependency-free C++17 exhaustive enumerator.
- `cubes_depth5.txt` — the deterministic 461-prefix cover.
- `verify_cube_cover.py` — independent Python exhaustion of the cube cover.
- `run_shards.py` — serial, atomic, resumable shard runner.
- `summarize_shards.py` — strict validator/aggregator for raw shard reports.
- `shard_results.json` — compact result and node-count index for all shards.
- `certificate.json` — top-level hashes, totals, and `UNSAT` result.
- `verify_manifest.py` — checks the committed source/cube/index/summary chain.
- `test_regressions.py` — ASan/UBSan build and known small-case regressions.
- `generate_tu_cnf.py` — an independent experimental SAT encoding; it is not
  needed by the completed certificate.
- `add_dimacs_units.py` — helper for reproducible SAT subinstances.

## Quick verification

From this directory:

```sh
python3 verify_manifest.py
python3 verify_cube_cover.py cubes_depth5.txt
python3 test_regressions.py
```

Expected output includes:

```text
PASS TU(41) certificate manifest: 461/461 empty shards
PASS independent depth-5 cube cover: 461 prefixes
PASS n=3: solutions=1
PASS n=7: solutions=1
PASS n=9: solutions=0
PASS sanitized TU(41) cube generation: 461 prefixes
```

The small cases correspond to known long lengths 4 and 8 (present) and 10
(absent).  They test the same sequence construction and recursive path used at
41.

## Full replay

The replay is single-process.  Valid completed reports are skipped on a later
invocation only when their cube, source hash, executable hash, and parsed result
all match.

```sh
clang++ -std=c++17 -O3 -DNDEBUG -Wall -Wextra -pedantic \
  enumerate_tu.cpp -o /tmp/tu41-enumerate

python3 run_shards.py \
  --enumerator /tmp/tu41-enumerate \
  --source enumerate_tu.cpp \
  --cubes cubes_depth5.txt \
  --output-dir /tmp/tu41-replay-reports \
  --bounds-depth 14

python3 summarize_shards.py \
  --enumerator /tmp/tu41-enumerate \
  --source enumerate_tu.cpp \
  --cubes cubes_depth5.txt \
  --reports /tmp/tu41-replay-reports \
  --output /tmp/tu41-replay-certificate.json \
  --index-output /tmp/tu41-replay-index.json
```

The recorded executable was built with Apple clang 21.0.0 on arm64 macOS 26.2,
so its binary hash is platform-specific.  The source and cube hashes are
portable.  A full replay should reproduce `0` solutions and the deterministic
node counts; wall times and the executable hash may differ.

## Proof dependencies and limits

The certificate depends on the displayed normalized definition, the elementary
row-sum identity, C/D interchange, and correctness of the small C++/Python
programs and compiler.  It does **not** depend on OR-Tools, a SAT solver, or
trusting the 1994 enumeration result.  It is an auditable exhaustive
computation, not a proof-assistant kernel or an LRAT proof.

The algorithm independently reconstructs the outside-in recursion outlined in:

- G. M. Edmondson, Jennifer Seberry, and M. R. Anderson,
  [On the existence of Turyn sequences of length less than 43](https://documents.uow.edu.au/~jennie/WEBPDF/1994_03.pdf),
  *Mathematics of Computation* 62 (1994), 351–362,
  [doi:10.1090/S0025-5718-1994-1203733-8](https://doi.org/10.1090/S0025-5718-1994-1203733-8).

That paper reports the same nonexistence result through long length 42, but no
code or output from it is used here.  This repository has not established a
priority claim that the present artifact is the first modern open certificate.
