# Exact dense-shell classifier pilot and production runner

## Status

This package is the first **truthful end-to-end** classifier pilot for the
two unclassified order-three profile shells

```text
h=1: (n_9,n_3,n_0)=(1,15,8),
h=0: (n_9,n_3,n_0)=(0,18,6).
```

It replaces the synthetic right-hand sides in the earlier arithmetic
microbenchmark with the actual Eisenstein profile equations.  Every selected
decorated skeleton is completed exhaustively through the bounded profile
layers described below.  Every modulo-nine hit is reconstructed as a
24-letter profile assignment and replayed independently on all 37 physical
positions.

The initial pinned census is:

| shell shard | canonical decorations | primitive-flag phase leaves | affine aggregate hits | exact aggregate hits | characteristic-two hits | modulo-nine hits | following lambda-digit hits | joint char2/mod9 | exact profiles |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `h1 --skip 0 --limit 100` | 100 | 7,440,174 | 3,897,234 | 159,116 | 82 | 220 | 1 | 0 | 0 |
| `h0 --skip 0 --limit 10` | 10 | 3,188,646 | 3,188,646 | 105,954 | 50 | 141 | 1 | 0 | 0 |

These are bounded shard counts, not shell-wide estimates.  In particular,
zero joint characteristic-two/modulo-nine hits in this small, early,
lexicographic sample is a useful measurement but not an exclusion or an
independence theorem.

## 1. Exact streamed state space

A local signed medium skeleton is

```text
(A_j,A_(j+6),B_j,B_(j+6)) in {0,+1,-1}^4
```

subject to the certified local equation

```text
-A_j+A_(j+6)+B_j-B_(j+6)=0 mod 3.
```

The C++ driver streams the 27 legal local states across six quartets in
deterministic lexicographic order.  For `h=1`, every zero position is
considered as the unique high position.  The complete decorated object—not
its support alone—is canonicalized under

```text
G = C_6 x C_(2,A) x C_(2,B).
```

The stabilizer is counted directly from all 24 images and every displayed
raw-weighted decoration count uses `24/|Stab_G|`.  The complete profile-ID
action is also evaluated on modulo-nine hits.  Its two
`diagnostic_*_idlex_*` fields record only whether the representative reached
through a canonical decoration happens to be ID-lexicographically canonical.
They are **not** full-assignment orbit counts: ID order does not refine
decoration order.  They are not aggregated or used scientifically.  An
exact-zero candidate, unlike those diagnostics, is transformed to a
canonical full assignment and replayed before it is emitted.

An independent complete Burnside pass gives the exact decorated workload:

| shell | raw signed skeletons | raw decorations | canonical decorations |
|---|---:|---:|---:|
| `h=1` | 59,743,488 | 537,691,392 | 22,426,752 |
| `h=0` | 47,730,304 | 47,730,304 | 1,999,128 |

Here an `h=1` decoration includes its high position but not its three high
phases; those are exhausted inside the decoration.  The Burnside fixed
vectors are pinned by the independent verifier, so the full canonical
workload is known exactly rather than estimated by dividing raw counts by
24.

`--skip` and `--limit` count canonical decorated objects.  Therefore the
next deterministic shard after

```text
--skip S --limit L
```

is

```text
--skip S+L --limit ...
```

No search state or survivor table is retained between decorations.
The current `--skip` implementation reaches a later canonical index by
rescanning the earlier prefix.  It gives deterministic bounded recovery,
but large collections of skip-based shards would repeat work.

Production mode avoids this defect.  `--prefix i j --complete-shard
--enumerate-exact-orbits` fixes the first two local-state indices **before**
decoration canonicalization and phase restoration.  The 729 ordered pairs
partition every raw skeleton exactly once.  Every canonical decoration
consequently belongs to exactly one shard, and summing its exact orbit
weight over all shards recovers the raw decoration census.  A successful
shard prints `shard_complete=1`; no bounded limit or skip is accepted in
this mode.

## 2. Actual equations

For a fixed decorated skeleton the driver uses exact pairs

```text
a+b*omega,             omega^2+omega+1=0.
```

It builds the real `F_37/H` transition table and the exact correlations

```text
D_t = sum_c (A_(c+t) A_c^* + B_(c+t) B_c^*).
```

Medium phases are restored quartet by quartet.  A local phase choice is
kept only when the exact primitive flag

```text
ell(D_t/3)=0 mod 3
```

holds.  The product of the six local tables is streamed; no phase cube is
stored.  At each leaf the exact class aggregates must equal one of the 22
certified targets.

The affine aggregate count tests equality modulo `lambda^3` with at least
one exact aggregate target.  The 22 targets occupy one, two, or three
distinct right-hand-side residue pairs depending on the skeleton aggregate
type.  It is therefore a union-of-targets count, not the earlier
one-right-hand-side `3^d` count.

The subsequent gates are evaluated on the actual correlations:

1. `mod9`: every coordinate of every independent `D_t` is divisible by 9;
2. `post_mod9_lambda`: after division by 9, `a+b=0 mod 3` in every row;
3. `mod27`: both integer coordinates are divisible by 27;
4. `exact`: all correlations vanish.

The second gate is the first post-modulo-nine lambda digit and is the
quadratic dense-shell layer.  The pilot checks it by exact enumeration,
making this package a small reference oracle.  The connected audit in
`../dense_shell_e2e_audit/` now evaluates and inverts all 729 characters
for one actual affine target fiber, recovers its following-digit witness,
and replays it exactly.  Complete production shards reconstruct exact upper
correlations only on the actual `char2 && mod9` intersection.  Thus
`post_mod9_lambda_hits`, `mod27_hits`, and `exact_zero_hits` in production
are explicitly scoped to that intersection.  This is exhaustive for exact
profiles because exact zero implies both necessary gates; the bounded pilot
continues to evaluate the upper exact gates on every modulo-nine hit.

## 3. Independent characteristic-two intersection

Every exact aggregate-compatible assignment is also reduced through the
tracked package

```text
../char2_profile_quotient/
```

and tested against

```text
A A^* + B B^* = e in F_4[C_37]^H.
```

The C++ implementation derives the six physical `F_4` correlations
directly.  The Python verifier independently calls the public
`check_eisenstein_profile` API and checks the same assignment, aggregate,
and shell support.  This measures the real intersection with the ternary
layers; it does not multiply marginal densities.

## 4. Witness recovery and detached replay

The first witness at each available gate is emitted as the two twelve-ID
class words, exact aggregate target, six compact Eisenstein correlations,
and a semantic digest.  In bounded pilot mode, every modulo-nine survivor is
sent to a detached routine that:

1. expands both invariant class words to all 37 physical positions;
2. recomputes all 37 cyclic correlations directly;
3. checks the six representatives and their six conjugate reversals;
4. rechecks the exact aggregate; and
5. computes the exact full-assignment stabilizer and orbit size.

The independent Python verifier repeats this physical replay without using
the C++ transition code.  It also verifies every emitted prefix flag and
semantic digest.

The default classifier behavior remains stop-on-first: an exact-zero hit is
canonicalized, detached-replayed, emitted with `shard_complete=0`, and
returns candidate status.  This is useful for bounded discovery work.

The production runner instead always supplies
`--enumerate-exact-orbits`.  Every exact hit is transformed to the
lexicographically canonical 24-ID representative, paired with its exact
target index, and inserted into a sorted per-shard map.  Duplicate
representatives do not create duplicate records.  Each retained orbit is
recomputed and replayed on all 37 physical lags, then emitted as
`exact_orbit_000000`, `exact_orbit_000001`, and so on.  Exact hits do not
stop the shard in this mode.

The runner and strict aggregator independently check canonicality, target
consistency, ordering, deduplication, semantic digests, all exact flags, and
all 37 correlations for every retained orbit.  The aggregator also performs
a second deterministic deduplication across prefix shards and writes the
complete orbit list with source-shard provenance.  Thus 729
`shard_complete=1` records now certify an exhaustive shell census while
preserving every exact profile they contain; completion no longer means
that the shell had no exact hit.

## 5. Reproduction

Build and run a bounded shard:

```text
clang++ -O3 -DNDEBUG -std=c++20 \
  -Wall -Wextra -Wpedantic -Werror \
  dense_shell_classifier_pilot.cpp \
  -o /tmp/h668_dense_shell_classifier_pilot

/tmp/h668_dense_shell_classifier_pilot \
  --shell h1 --skip 0 --limit 100

/tmp/h668_dense_shell_classifier_pilot \
  --shell h0 --skip 0 --limit 10

/tmp/h668_dense_shell_classifier_pilot \
  --shell h1 --count-decorations

/tmp/h668_dense_shell_classifier_pilot \
  --shell h0 --count-decorations

# Reproduce the certified exact profile through the census path:
/tmp/h668_dense_shell_classifier_pilot \
  --shell h0 --prefix 0 5 --skip 35879 --limit 2 \
  --enumerate-exact-orbits
```

Run the detached verifier and regression test from the repository root:

```text
python3 \
  hadamard_668_search/dense_shell_classifier_pilot/verify_dense_shell_classifier_pilot.py

python3 -m unittest -v \
  hadamard_668_search/dense_shell_classifier_pilot/test_dense_shell_classifier_pilot.py

python3 -m unittest -v \
  hadamard_668_search/dense_shell_classifier_pilot/test_dense_shell_production.py
```

The verifier also compares the unsplit first 100 `h=1` decorations with
the additive union of

```text
--skip 0  --limit 40
--skip 40 --limit 60.
```

Prepare and execute the deliberately zero-work production smoke:

```text
python3 \
  hadamard_668_search/dense_shell_classifier_pilot/run_dense_shell_production.py \
  --shell h0 --prefix 13 13 --workers 1
```

A complete v2 `h=0` launch, when authorized, is:

```text
python3 \
  hadamard_668_search/dense_shell_classifier_pilot/run_dense_shell_production.py \
  --output \
  hadamard_668_search/dense_shell_classifier_pilot/output/production-v2 \
  --shell h0 --workers 8 --aggregate-rss-limit-mib 3072

python3 \
  hadamard_668_search/dense_shell_classifier_pilot/aggregate_dense_shell_production.py \
  --output \
  hadamard_668_search/dense_shell_classifier_pilot/output/production-v2 \
  --shell h0
```

The same runner command is the resume command.  It validates every existing
result, including every retained exact orbit, and launches only missing
shards.  The v2 manifest pins the source, binary, compiler, flags,
enumeration command, exact-orbit policy, both Burnside fixed vectors, and
all 1,458 prefix cells.  Results are written by atomic rename.  A v1
stop-on-candidate output cannot be silently resumed as v2: its manifest,
source hash, command, and result schema all fail validation.  Work is
ordered by descending raw-decoration count to avoid a single large final
wave.  At most eight children run, while the parent polls their aggregate
resident memory and stops the pool above 3,072 MiB.  Darwin `RLIMIT_AS` is
not used because it prevents process startup on the reference Mac.

### v1 discovery-output migration boundary

The existing directory

```text
hadamard_668_search/dense_shell_classifier_pilot/output/production
```

is a frozen v1 discovery artifact.  Its manifest pins source hash
`cf48f07cf1c69b2df1adc9f5f48ffd96c4b3daccc747bcab5a9852d9138e2025`,
and its raw `candidates/h0-p00-p05.json` record pins the stopped second
exact-profile discovery.  Leave that directory unchanged.

There is deliberately no in-place conversion.  Do not copy its manifest,
candidate, binary, temporary files, or partial counters into v2.  The v1
prefix stopped after the hit and is not a complete prefix result.  The
explicit `output/production-v2` command above creates a fresh v2 manifest
with the new source and binary hashes, restarts `h0-p00-p05` from the
beginning, rediscovers and retains its certified orbit, and then continues
to the end of that prefix.  Repeating exactly that command safely resumes
only hash-matching v2 results.  Pointing the v2 runner at the old default
directory fails its read-only provenance preflight before compilation, so
it neither adds a new binary nor overwrites or mixes the two provenance
lines.

## 6. Historical pilot rate and complete-prefix correction

Three consecutive optimized bounded runs gave the following median
single-core
rates.  “Raw-equivalent” means that every processed canonical decoration
and every phase leaf is weighted by its **measured** `24/|Stab_G|`; it does
not divide by an assumed free orbit of size 24.

| shell shard | canonical primitive leaves/s | raw-equivalent primitive leaves/s | raw-equivalent affine points/s |
|---|---:|---:|---:|
| first 100 `h=1` decorations | 16,388,674 | 393,328,180 | 206,029,046 |
| first 10 `h=0` decorations | 20,807,951 | 499,390,832 | 499,390,832 |

The earlier 25.20-core-hour calculation is **superseded and invalid**.  It
treated the one-right-hand-side totals

```text
h=1: 15,012,043,331,328,
h=0:  8,914,445,186,688
```

as the workload entering `affine_aggregate_compatible`, but that gate is a
union of as many as three distinct target residue classes.  A detached
six-quartet dynamic program now tracks the two aggregate scalar types and
derives the exact residue-stratified union upper bounds

```text
h=1: 30,006,842,465,088,
h=0: 17,848,209,316,608,
total: 47,855,051,781,696.
```

Because the current driver generates every primitive-compatible leaf before
testing that union, the honest pre-gate workload bounds are larger:

```text
h=1: 45,036,129,993,984,
h=0: 26,743,335,560,064,
total: 71,779,465,554,048.
```

Applying those early bounded **primitive-leaf** rates to the bounds gave:

```text
h=1: 31.806 single-core hours,
h=0: 14.876 single-core hours,
total: 46.681 single-core hours (now superseded).
```

The connected audit superseded that estimate with the first complete
positive-work production prefix, `h0-p01-p13`. It contains 1,296 legal
signed skeletons and 42 canonical decorations.  A diagnostic-witness
fallback had caused 554,008 redundant all-37-lag replays in complete mode;
restricting that fallback to bounded mode changed the prefix from
2.615347 seconds to 0.771325 seconds, with every lower counter unchanged
and zero production replays because the prefix has no `char2 && mod9`
point.

Those values are the historical v1 post-fix measurement. The exhaustive v2
source was then measured with `--enumerate-exact-orbits` on the same prefix.
Its five-run median is 0.744369 seconds and 385,532,181 raw-equivalent
primitive leaves per second. Applying the current v2 rate to the rigorous
upper bounds gives:

```text
h=1: 32.45 single-core hours,
h=0: 19.27 single-core hours,
total: 51.72 single-core hours.
```

This is still not a runtime certificate: the prefix belongs to the rare
`(r,d,rho,nu)=(5,12,12,0)` cell, the `h=1` shell has high-position work,
and the remaining prefixes have different support, survivor, and
canonicalization distributions.

The earlier 12.7-million-character/second microbenchmark also cannot be
used unchanged as a production projection.  On the connected actual
modulo-nine fiber, 459 of 864 restricted polar entries differ from that
benchmark's synthetic/theoretical family.  The same factorization code runs
at a three-run median 15,641,863 characters/second on the actual fitted
representative family, but support-level reuse and shell-wide rate
distribution remain unmeasured.  See `../dense_shell_e2e_audit/README.md`.

No actual char2/mod9 intersection occurs in the pinned sample.  The earlier
neutral-intersection figures `622,743` and `3,304` were scaled from the
invalid one-right-hand-side workload and are also superseded.  They are not
replaced here: neutrality between these algebraic gates is unproved, and the
production run can measure the intersection directly.

## 7. Resource boundary and interpretation

Each production child keeps only six local option tables, one phase vector,
the current witnesses, and the retained canonical exact-orbit map.  The map
grows only with distinct exact profiles, not raw exact hits.  The pinned
standalone C++ runs use roughly 1.5 MB maximum resident memory.  The
independent Python verifier, including temporary compilation, four bounded
C++ runs, and both complete Burnside censuses, completes in about eleven
seconds and stays below 170 MB on the reference machine.

The resource-safe default is one canonical `h=1` decoration:

```text
--shell h1 --skip 0 --limit 1.
```

The first lexicographic decoration has no primitive-flag lift for any high
phase, so validation uses larger pinned shards to exercise every implemented
gate.

This is now production-resumable infrastructure, but it is not a completed
shell classification until all 729 results for that shell pass the strict
aggregator.  The verified 729-character count/self-reduction kernel remains
an available architecture, but it must use the actual production polynomial
and be validated across representative support cells before a shell-wide
character-cost projection is claimed.
