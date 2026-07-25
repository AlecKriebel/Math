# Nine-case all-short-block Eliahou census

## Complete production result

Production finished on 2026-07-25 PDT.  All \(2^{18}\) quotient states in
each of cases 21 through 29 were searched, in 256 atomic ranges per case.
The complete result is:

- 9 cases and 2,304 strictly validated ranges;
- 3,710,853,316,608 exact join rows;
- 88,927,740 modular survivors;
- 88,927,740 exact integer-polynomial checks;
- 88,927,740 independent bit-packed physical replays; and
- **zero exact integer supports**.

| case | short block | join rows | modular survivors | best (nonzero, L1, Linf) | wall |
|---:|---:|---:|---:|---:|---:|
| 21 | S02 | 412,316,860,416 | 9,564,254 | (4, 72, 30) | 37.68 min |
| 22 | S04 | 412,316,860,416 | 9,796,880 | (4, 78, 36) | 36.75 min |
| 23 | S06 | 412,316,860,416 | 9,807,738 | (3, 54, 30) | 40.30 min |
| 24 | S08 | 412,317,646,848 | 9,561,296 | (4, 66, 36) | 46.63 min |
| 25 | S10 | 412,316,860,416 | 9,789,738 | (3, 72, 36) | 40.08 min |
| 26 | S12 | 412,316,860,416 | 10,533,216 | (4, 66, 36) | 73.67 min |
| 27 | S14 | 412,317,646,848 | 10,285,492 | (3, 66, 24) | 36.10 min |
| 28 | S16 | 412,316,860,416 | 9,789,970 | (4, 66, 24) | 35.17 min |
| 29 | S18 | 412,316,860,416 | 9,799,156 | (4, 66, 30) | 31.82 min |

`NINE_CASE_COMPLETION_CERTIFICATE.json` freezes the exact counts, retained
best witness, model/binary/config/aggregate/source hashes, original
survivor-stream range digest, complete raw-manifest digest, and normalized
full-semantic range digest for every case.  The semantic digest includes
every validated range field except the two nondeterministic timing-rate
fields.

The output-independent verifier requires both the original nine-model
algebra certificate and the separately frozen case-26 completion
certificate.  It regenerates all nine models, checks byte-for-byte
equivalence of the independently derived case-26 models, and independently
replays every aggregate-best quotient plus both exceptional fallback
quotients:

```text
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  /Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  verify_nine_case_completion.py
```

Add `--live` to audit all 2,304 ignored range manifests, exact path sets,
configs, aggregates, model binaries, and executables.  Live verification
also reruns both exceptional quotients in gauged and ungauged C++ modes and
requires exact agreement with the independent NumPy/physical replay.

## Exact algebraic result

Canonical cases 21 through 29 are precisely

```text
S02, S04, S06, S08, S10, S12, S14, S16, S18.
```

The independent verifier rebuilds every case from the original
anti-fold definitions.  For each case it proves:

- 78 support variables;
- 39 pairs of equal characteristic-two syndrome columns;
- affine quotient rank 21 and dimension 18;
- 20 noncentral \(L\) pairs, 18 noncentral \(S\) pairs, and the common
  central pair \(\{L_{20},S_{20}\}\);
- rank 18 for each of the \(L\), \(S\), \(L+\)central, and
  \(S+\)central quotient projections;
- the same four phase-adjusted interaction cliques;
- exactly 2,126 forced-zero and 686 forced-nonzero pair/parity coupling
  checks; and
- at least one odd noncentral reflected pair in every quotient state, so
  spatial reflection acts freely.

The frozen derivation is in `SHORT_BLOCK_CERTIFICATE.json`.  Recompute it:

```text
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 \
  /Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  verify_short_block_census.py
```

This takes about 1.3 seconds and 101 MB RSS.

## Dynamic reflection gauge

The canonical gauge fixes the orientation variable of the lowest-index
odd noncentral \(L\) pair.  Seven cases always have such a pair.

Two cases have one exceptional quotient each:

| case | short block | exceptional quotient | fallback |
|---|---:|---:|---|
| 24 | S08 | 156922 | lowest odd noncentral \(S\) pair |
| 27 | S14 | 6143 | lowest odd noncentral \(S\) pair |

There are no quotients without an odd noncentral pair.

An \(L\)-gauged quotient performs

\[
2(2^{19}+2^{18})=1,572,864
\]

join rows.  An exceptional \(S\)-gauged quotient performs

\[
2(2^{20}+2^{17})=2,359,296,
\]

an exact surcharge of 786,432 rows.  Therefore:

- each ordinary case has 412,316,860,416 rows;
- S08 and S14 each have 412,317,646,848 rows; and
- all nine cases together have exactly
  **3,710,853,316,608 rows**.

## Resumable production architecture

`short_block_census.cpp` compiles the audited packed-trit join and physical
replay from the proven case-26 implementation, then supplies an isolated
parameterized driver with the dynamic \(L\)-else-\(S\) gauge.

For every modular survivor it:

1. reconstructs all 78 support bits;
2. checks weight 39;
3. evaluates the exact 20-row integer quadratic;
4. independently reconstructs the four physical anti-fold rows;
5. evaluates all physical correlations with bit-packed signed dot
   products;
6. checks energy 334, content four, and divisibility by six;
7. retains exact candidates and the best residual witness; and
8. hashes the complete reflection-restored survivor stream.

`run_short_block_census.py` accepts any case 21 through 29.  Each output
directory is case-specific and atomically pins:

- case number and short-block index;
- exact quotient interval and chunking;
- dynamic-gauge policy and exceptional quotient list;
- generated integer model and semantic metadata hashes;
- wrapper, audited parent C++ sources, model generator, runner, and compiled
  binary hashes; and
- RSS and output-size guards.

Existing ranges are skipped only after strict validation, so the production
command is also its resume command.

Prepare a case without launching a range:

```text
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  run_short_block_census.py \
  --case 21 \
  --output output/production-case21 \
  --workers 8 --chunk-size 1024 \
  --rss-limit-mib 8192 --output-limit-mib 100 \
  --prepare-only
```

When machine capacity is available, remove `--prepare-only` to run.  A
separate output directory is required for `--ungauged`.

The other eight cases were completed with the following sequential
production command.  It remains their exact resume command:

```text
cd /Users/alec/Documents/Math-h668-local/hadamard_668_search/eliahou_short_block_census
for case_number in 21 22 23 24 25 27 28 29; do
  env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
    VECLIB_MAXIMUM_THREADS=1 \
    /Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
    run_short_block_census.py \
    --case "${case_number}" \
    --output "output/production-case${case_number}" \
    --workers 8 --chunk-size 1024 \
    --rss-limit-mib 8192 --output-limit-mib 100
done
```

The loop is sequential across cases and parallel only within one case.
Re-running exactly the same command now performs strict validation and
skips all completed atomic ranges.

Aggregate all eight completed cases:

```text
cd /Users/alec/Documents/Math-h668-local/hadamard_668_search/eliahou_short_block_census
for case_number in 21 22 23 24 25 27 28 29; do
  /Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
    aggregate_short_block_census.py \
    --output "output/production-case${case_number}"
done
```

Create and independently replay a two-quotient sample through the NumPy join
and original physical equations:

```text
cd /Users/alec/Documents/Math-h668-local/hadamard_668_search/eliahou_short_block_census
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 \
  /Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  run_short_block_census.py \
  --case 21 --output output/bounded-case21 \
  --start 0 --stop 2 --chunk-size 2 --workers 1 \
  --rss-limit-mib 1024 --output-limit-mib 20
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 \
  /Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  replay_short_block_range.py \
  output/bounded-case21/ranges/range_000000_000002.json
```

The independent replay deliberately caps itself at two quotients unless
`--allow-large` is supplied.

## Bounded controls

`BOUNDED_BENCHMARK.json` records:

- one exact C++ quotient for every one of the nine models;
- exact dynamic-gauge versus ungauged equality on both exceptional
  quotients;
- independent NumPy/physical replay of case-26 quotient zero and the S08
  exceptional quotient;
- atomic resume and aggregation; and
- byte-identical regeneration of the active case-26 model, including the
  known quotient-zero survivor count and stream hash.

These bounded controls preceded full production.  The complete nine-case
result and its stronger independent verification are now frozen in
`NINE_CASE_COMPLETION_CERTIFICATE.json`.

## Scope

These are necessary characteristic-two/three anti-fold searches inside
Eliahou's structured repair family.  The result excludes an exact repair in
these nine all-short-block cases.  It does not exclude other Eliahou repair
cases, other construction families, or \(H(668)\) itself, and it does not
construct \(H(668)\).
