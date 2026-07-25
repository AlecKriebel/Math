# Whole-case-26 quotient census: completed exact computation

This folder turns the fixed-quotient contraction in
`../eliahou_defect2_math/` into a rigorously sized whole-case computation.
The complete gauged census has now been run over all \(2^{18}=262,144\)
quotient states and both central values.  Every retained modular survivor was
replayed through both the exact integer polynomial and the independent
bit-packed physical rows.  The computation found **zero exact supports** in
this case.

This closes the defined case-26 global-quotient search.  It does not exclude
other cases, other construction families, or \(H(668)\).

## Completion result and tracked certificate

The tracked `COMPLETION_CERTIFICATE.json` freezes the result without requiring
the ignored production directory:

```
quotient states                 262,144
atomic ranges                       256
gauged join rows          412,316,860,416
mod-6 survivors              10,533,216
exact integer replays        10,533,216
bit-packed physical replays  10,533,216
exact supports                        0
```

The canonical range-stream digest is
`c566eef9154ebefb13bca52c5e3e931c622e7d930619e2d3f35bec09d9e27fc7`.
The exact aggregate JSON has SHA-256
`268adc90d99e7a045c60879fd9367910c78a3b0b93e11aab47589e743d5a5253`;
the run configuration has SHA-256
`e47a5d236701aca230308a30c2739a3b7835d1e9d7bfb9b2ca0957025395280c`.

The best nonexact witness occurs at quotient `123143`, central value `1`,
pair state `369546495487`, with normalized residual vector

```
[0,0,0,-36,0,0,0,18,6,0,0,0,0,0,-6,0,0,0,0,0].
```

An independent NumPy replay of that quotient found 46 survivors, zero exact
supports, and exactly the same best witness.

The central structural fact is universal, not special to the pinned
quotient.  Write each reflected characteristic-two syndrome pair in one
of the two pair coordinates

```
parity 0:  x = (y,y),       substitution column (+1,+1),
parity 1:  x = (1-y,y),     substitution column (-1,+1).
```

Modulo three, after conditioning the central pair
`{("L",20),("S",20)}`, every quadratic coupling

- between the `L` and `S` blocks, or
- between parity-0 and parity-1 pair coordinates

vanishes unless the two pair coordinates have the same
**phase-adjusted parity**.  The fixed phase is the alternating phase of
the reflected pair position.  The four components are therefore always

```
L-color-0, L-color-1, S-color-0, S-color-1.
```

Their sizes vary with the quotient state, but their identities do not.
`verify_global_quotient_plan.py` checks this directly for every physical
pair-pair coefficient and every parity choice.

More explicitly, for noncentral reflected pairs `i,j`, let `p_i` be raw
pair parity and let `epsilon_i` be the fixed alternating phase.  The
twenty-vector quadratic coefficient satisfies

```
Q_ij(p_i,p_j) = 0                         if blocks differ,
Q_ij(p_i,p_j) = 0                         if p_i+epsilon_i != p_j+epsilon_j,
Q_ij(p_i,p_j) != 0 as a twenty-vector     otherwise.
```

All additions in the color condition are modulo two.  The verifier checks
2,126 forced-zero coefficient/parity cases and 686 forced-nonzero cases.
Thus every one of the four induced interaction graphs is a clique, even
though its vertex set changes with the quotient.

## Why quotient-table caching alone does not work

The 18-dimensional quotient projects bijectively onto all `2^18` parity
patterns of the 18 noncentral `S` pairs.  Its projection to the 20
noncentral `L` pairs is injective as well.  Thus no two quotient states
have the same `S` component mask or the same `L` component mask.

Across all quotient states, independently materializing every component
row would require exactly

```
L-color-0   871,563,240
L-color-1   871,563,240
S-color-0   387,420,489 = 3^18
S-color-1   387,420,489 = 3^18
total 2,517,967,458 component rows.
```

At even 12 bytes per row this is over 30 GB, and this machine currently
has much less free disk than that.  A global external-sort cache is
therefore the wrong architecture.

## Streaming exact architecture

For each quotient state:

1. substitute its 39 pair parities into the mod-3 quadratic;
2. condition the central pair to zero and one;
3. choose the lowest-index odd noncentral `L` pair and fix its
   orientation bit to zero using the certified free reflection gauge in
   `../eliahou_global_reuse_math/`;
4. enumerate the four small component tables using packed 20-trit
   signatures, tracking full-even weight inside every component;
5. put the `2^18` `S-color-0 + S-color-1` sums in a persistent timestamped hash
   table, keyed by `(signature, full-even weight)`;
6. stream the remaining `2^19` `L-color-0 + L-color-1` sums and probe the complementary
   key;
7. reconstruct the reflected mate of every representative, restoring
   the complete ungauged survivor set;
8. for every full survivor, reconstruct all 78 support bits, evaluate
   the exact integer quadratic, and independently replay the four
   physical anti-fold rows with bit-packed signed dot products;
9. retain exact candidates and range minima, and hash the complete
   canonical survivor/residual stream with SHA-256.

The tables are fixed-cardinality even though their component sizes vary:
after gauge fixing their Cartesian products always have `2^19` and
`2^18` rows.  Including both central values, the whole case has the exact
principal work count

```
right-side hash insertions:  137,438,953,472
left-side hash probes:       274,877,906,944
total:                       412,316,860,416
```

The ungauged validation control retains the old
`687,194,767,360`-row count.  The gauge saves exactly
`274,877,906,944` rows, or 40%, while preserving the complete output by
orbit reconstruction.  At the independently certified pinned quotient,
31 joined representatives reconstruct to the original 62 survivors.

The kernel uses five 2-bit packed trit bytes in one `uint64_t`,
carry-free mod-3 addition, a `2^20`-bucket hash table, and generation
stamps so the bucket array is never cleared between quotient states.
The measured production resident set is only 17.5 MB for one worker.
No survivor table is written: every survivor is replayed inline and
folded into the range digest.  Atomic range manifests contain all exact
candidates, a best witness, counts, hashes, and timing.

## Historical production and resume command

The census is complete; there is no reason to rerun it during ordinary
verification.  If the ignored live artifacts are retained, the original
command remains a strict resume command:

```
cd /Users/alec/Documents/Math-h668-local/hadamard_668_search/eliahou_global_quotient_plan
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 \
  /Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  run_global_quotient_census.py \
  --output output/production \
  --workers 8 \
  --chunk-size 1024 \
  --rss-limit-mib 8192 \
  --output-limit-mib 100
```

The command is its own resume command.  It validates every existing
manifest and skips only ranges whose schema, exact boundaries, source
hash, model hash, replay counts, gauge counts, and digest shape all pass.
The runner atomically pins:

- both C++ sources and their combined SHA-256;
- the exact integer binary model and SHA-256;
- the compiled binary SHA-256;
- the runner and model-generator SHA-256;
- the quotient interval, chunking, and gauge mode.

The 256 completed ranges were aggregated with:

```
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  aggregate_global_quotient_census.py \
  --output output/production
```

Preparation without launching a range remains available for reproducibility:

```
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  run_global_quotient_census.py \
  --output output/production \
  --workers 8 --chunk-size 1024 \
  --rss-limit-mib 8192 --output-limit-mib 100 \
  --prepare-only
```

The `--ungauged` option retains the complete `20+18` join as a
validation control.  It must use a separate output directory because
gauge mode is pinned in `RUN_CONFIG.json`.

## Verification

The default completion verifier does not read ignored output.  It checks the
certificate arithmetic, all pinned tracked-source hashes, the artifact
inventory, and regenerates the binary model from the mathematical derivation:

```
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  verify_completion_certificate.py
```

When the ignored `output/production` tree is present, `--live` additionally
hashes the run configuration, aggregate, binary, and model, then independently
validates all 256 range manifests and reconstructs the aggregate range digest:

```
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  verify_completion_certificate.py --live
```

The underlying quotient algebra and exact work-count verifier remains:

```
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  verify_global_quotient_plan.py
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  ../eliahou_global_reuse_math/verify_global_reuse_math.py
```

Verify the three separated ungauged reference quotients:

```
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 \
  /Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  verify_reference_quotients.py
```

They recompute quotient indices `0`, `131071`, and `262143` using the
original NumPy polynomial substitution and join.  Their survivor counts
are respectively `50`, `70`, and `56`, exactly matching the C++ kernel.

Independently replay any small production range, rebuilding every
support through the original NumPy substitution and physical replay:

```
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  replay_global_quotient_range.py \
  output/production/ranges/range_000000_001024.json \
  --allow-large
```

Without `--allow-large`, this deliberately caps itself at eight
quotients.  The bounded validation used two-quotient ranges.

`BENCHMARK.json` records all hard controls:

- quotient `0`: 25 gauge representatives, 50 full survivors;
- quotient `131071`: 35 representatives, 70 full survivors;
- quotient `262143`: 28 representatives, 56 full survivors;
- pinned quotient `260914`: 31 representatives, 62 full survivors.

For every one, gauged and ungauged mode have the same full survivor
count, best witness, exact-candidate list, and canonical full-stream
SHA-256.  A four-quotient atomic run was resumed without recomputation,
aggregated successfully, and independently replayed in Python.

## Production performance record

`BENCHMARK.json` records a 2,048-quotient single-core run of the complete
production path: reflection reconstruction, exact integer evaluation,
and bit-packed physical replay for all 78,998 full survivors.  It
processed `3,221,225,472` join rows in 47.99 seconds, about 67.1 million
rows/second, with 17.5 MB maximum resident set.

The completed 256-range aggregate records `15,574.577026539` summed kernel
seconds across workers.  The earlier literal projection was useful for
resource planning but is no longer evidence for completeness; completeness
is pinned by the range count, aggregate counters, digest, and certificate.

Eight measured-size workers use roughly 140 MB; even a very conservative
overhead allowance is far below the explicit 8 GB aggregate RSS guard.
The four-quotient test output, including model and binary, was 344 KB.
The completed run recorded 680,031 bytes before writing the aggregate, far
below the 100 MB guard.
No external table store or survivor stream is required.

## Character-transform and caching audit

A dense transform on the full signature group has `3^20 =
3,486,784,401` cells.  One four-byte array already occupies about
13.0 GiB, before transform workspace or weight channels, so it is not
safe on this 16 GB machine.  Complex transform storage is much larger.

Caching component rows across quotient states also fails cleanly: both
block projections are injective, the exact aggregate is 2.52 billion
rows per central value, and a minimal practical row store exceeds the
currently available disk.  The phase-adjusted four-clique identity is
the useful reuse: it compiles the decomposition and packed arithmetic
once while streaming quotient states with a fixed small working set.
