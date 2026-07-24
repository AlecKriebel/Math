# Dense-shell 729-character throughput benchmark

**Date:** 2026-07-24
**Machine:** Apple M1 Pro, one benchmark thread, 16 GB physical RAM
**Status:** validated arithmetic benchmark; not a dense-shell classifier

## Result

The exact quadratic-character kernel is **not** the computational
bottleneck suggested by the initial paper estimate.

On one M1 Pro core, the conservative median of three identical pinned
`batch=96` runs was

```text
h=1:       15,165,274 character evaluations/s/core
h=0:       10,959,890 character evaluations/s/core
combined:  12,668,666 character evaluations/s/core.
```

The six census cells in each shell are equally represented in this
microbenchmark; the rates are not reweighted by a claimed production
support distribution.  Equal weighting deliberately measures every known
dimension/radical type, including rare cells.  The margin over the gate is
large enough that this choice does not affect the go/no-go conclusion.

The combined median clears the two planning thresholds by

```text
28-day unbatched threshold, 17,641/s/core:   718.14 times
72-hour unbatched threshold, 164,650/s/core: 76.94 times.
```

Even the slowest measured shell/rate combination, the `h=0` kernel in the
single-item batch run, was `9,713,334/s/core`: 550.61 times the four-week
threshold and 58.99 times the 72-hour threshold.

This is a decisive **go** result for the narrow compiled-rate gate.  It is
not evidence that a dense profile exists and not a forecast for completing
the entire `h=1,0` classification.  Support and signed-skeleton generation,
order-24 canonicalization, positive-fiber self-reduction, upper-digit
checks, row-margin joining, and exact correlation replay are outside the
timed loop.

## What is actually timed

This is not a synthetic integer loop.  The program reconstructs the six
physical `F_37/H` polar matrices over `F_3`, then selects one legal support
from every cell of the published affine-restriction census:

```text
h=1: six representatives, dimensions 8, 9, and 10
h=0: six representatives, dimensions 11 and 12.
```

For each support it restricts all six forms to the true homogeneous kernel
of the nonempty-quartet and channel equations.  It congruence-factorizes
each of the 729 pencils once at support level.  A batch item is then built
from:

- a legal signed-medium skeleton in every quartet;
- an actual correction point `x0` and therefore a consistent affine
  right-hand side;
- all nine possible high positions in the `h=1` case;
- a varying six-coordinate target.

For every support, batch item, and character, the timed kernel:

1. combines the six affine linear forms and target offsets;
2. transforms the linear form through the stored congruence basis;
3. checks whether it vanishes on the pencil radical;
4. completes the square over `F_3`;
5. returns the exact Eisenstein Gauss sum.

The output is folded into a labelled 64-bit checksum.  The default workload
checksums are compiled assertions:

```text
factorization: 0xdcdab09cb31d00b6
h=1:           0xf21613ddea2e0b16
h=0:           0xa9ee3c575158e4d6.
```

Support factorization and batch construction are intentionally outside the
character-evaluation timer.  Factorization is measured separately; the
median rate was `882,188` support-character reductions/s/core.  Batch
construction is not yet an optimized production implementation and was
not used to claim a classifier rate.

## Correctness checks

Before timing, the compiled program independently reproduces:

```text
local unsigned-support histogram:  (1,0,6,4,1)
local legal-signed histogram:       (1,0,12,8,6)
h=1 unsigned supports:              510,384
h=0 unsigned supports:              107,476
h=1 legal signed skeletons:         59,743,488
h=0 legal signed skeletons:         47,730,304.
```

It also reproduces all twelve `(r,d,rho,nu)` cells and counts from
`LP333_ORDER3_DENSE_SHELL_QUADRATIC_ALGEBRA.md`.

The independent Python verifier does not reuse the C++ diagonalization.
It enumerates every point of:

- one real `h=1`, `d=8` affine cube;
- one real `h=0`, `d=11` affine cube;

and directly Fourier-transforms their six-coordinate output histograms.
All `2*729=1,458` exact Eisenstein character sums agree with C++.  The
canonical reference digest is

```text
58ca5a703683faf2072a5268af97ed826
2d92b91ce60f92b6fc4500f319b70fe.
```

The original dense-shell verifier was also rerun and reproduced the
published `F_27 x F_27` algebra, support counts, affine-rank histograms, and
fiber lower bounds.  An AddressSanitizer/UndefinedBehaviorSanitizer build
completed a reduced workload without a report.

## Measurements

The default workload evaluates `20,155,392` characters in each shell.
Three consecutive pinned runs gave:

| trial | factor reductions/s | `h=1` eval/s | `h=0` eval/s | combined eval/s |
|---:|---:|---:|---:|---:|
| 1 | 882,188 | 15,178,099 | 10,860,815 | 12,661,551 |
| 2 | 933,805 | 15,008,699 | 10,959,890 | 12,668,666 |
| 3 | 853,162 | 15,165,274 | 10,989,668 | 12,744,156 |

Batch-size sensitivity at approximately the same number of character
evaluations per shell was:

| batch size | combined eval/s | multiple of 17,641 | multiple of 164,650 |
|---:|---:|---:|---:|
| 1 | 11,242,184 | 637.28 | 68.28 |
| 9 | 12,192,711 | 691.16 | 74.05 |
| 96 | 13,217,530 | 749.25 | 80.28 |

The standalone optimized default run peaked at `5,095,424` bytes maximum
resident set size (`4.86 MiB`) as reported by `/usr/bin/time -l`.  The
Python reference run, including an optimizing C++ compiler subprocess,
peaked at `197,345,280` bytes (`188.20 MiB`).  Both are far below the
4 GB benchmark cap and the machine's 16 GB physical RAM.

If one performs arithmetic projection only—using the independent medians
for character evaluation and support factorization—the report's two raw
front-end totals become:

| subtotal | one core | ideal ten cores |
|---|---:|---:|
| maximal reuse, `78.35` billion characters | 1.86 hours | 0.186 hours |
| unbatched high positions, `426.77` billion characters | 9.50 hours | 0.950 hours |

Those figures include the `450,419,940` support-character factorizations,
but exclude every downstream classification cost listed above.  They
should be read only as evidence that exact character arithmetic is fast
enough, not as an end-to-end completion estimate.

## Reproduction

From this directory:

```text
clang++ -O3 -DNDEBUG -std=c++20 -mcpu=apple-m1 \
  -Wall -Wextra -Wpedantic \
  benchmark_dense_shell_characters.cpp \
  -o /tmp/h668_dense_shell_benchmark

/usr/bin/time -l /tmp/h668_dense_shell_benchmark \
  --batch 96 --rounds 48 --factor-repeats 8

python3 verify_dense_shell_benchmark.py
```

The verifier builds its own temporary optimized executable and removes it
on exit.  No benchmark result stream is written to disk.

## Interpretation for the 72-hour gate

The four-week rate gate succeeds by more than two orders of magnitude even
under the slowest measured configuration.  The earlier statement that the
729-character front end might itself take days to weeks on ten cores is
therefore too pessimistic for support-factorization reuse.

The next uncertainty is end-to-end selectivity and orchestration: how many
positive quadratic fibers survive, and what it costs to canonicalize,
self-reduce, and exact-replay them.  This checkpoint deliberately stops
before implementing that classifier.
