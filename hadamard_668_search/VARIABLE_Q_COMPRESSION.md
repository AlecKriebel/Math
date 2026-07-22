# Periodic compression of `BS(84,83)`

## Exact factor-14 reduction

Pad each length-83 sequence with a trailing zero.  A base sequence then gives
four periodic length-84 vectors whose summed periodic autocorrelation is

```text
(334,0,0,...,0).
```

Compress modulo six:

```text
X_j = sum_(t=0)^13 x_(j+6t),   0 <= j < 6.
```

The periodic compression theorem gives the exact necessary condition

```text
sum_X (PAF_X(0),PAF_X(1),PAF_X(2),PAF_X(3)) = (334,0,0,0).
```

For `A,B`, every compressed cell is even and lies in `[-14,14]`.  For
padded `C,D`, cells 0 through 4 have the same alphabet, while cell 5 contains
13 signs and the distinguished zero and is odd in `[-13,13]`.  Compression
preserves both selected margins because the step six is even:

```text
sum_j X_j = S,                 sum_j (-1)^j X_j = T.
```

`variable_q_compression.py` enumerates these integer vectors exactly, applies
the individual energy/Fourier bounds, groups them by their four-value PAF
signature, and performs a two-pair hash join against `(334,0,0,0)`.  The
implementation also checks the compression theorem directly on both source
lengths.

## Exhaustive result on all 288 nominal shards

All 288 nominal margin shards survive factor 14.  Global coordinate
alternation groups them into 156 orbits, but all nominal shards were evaluated
here as an independent regression.  There are 378 to 392 compatible `AB`
pair-signature sums per shard and 124,940 to 1,042,220 compatible
four-signature combinations.  The strongest individual pruning occurs on the
short sequences in shards 50, 51, 68, 69, 78, 79, 180, and 181, where 392
signatures fall to 362 (about 7.65%).  Survival of this compressed relaxation
does not assert that a shard contains an exact base sequence.

For the historical local-search focus shard 235 the exact counts are

```text
compressed vectors:       (2580, 2604, 2500, 2500)
distinct PAF signatures:  ( 205,  205,  832,  832)
surviving signatures:     ( 205,  205,  789,  789)
matched AB pair sums:       391
signature quadruples:       1,041,152
compressed-vector quadruples: 752,231,412
```

Shard 235 is the global-alternation partner of the currently tracked canonical
shard 213.  The displayed counts and reproduction command remain labeled 235
because that is the nominal shard on which they were measured.

Reproduce one shard or the exhaustive report with

```sh
python3 variable_q_compression.py --self-test --shard 235
python3 variable_q_compression.py --all-shards \
  --output ../tmp/hadamard_668_runs/factor14_all_shards.json
```

## Why this does not strengthen the current CP model

For a length-six PAF signature `(p0,p1,p2,p3)`, the four distinct Fourier
powers are

```text
p0+2p1+2p2+p3,   p0+p1-p2-p3,
p0-p1-p2+p3,      p0-2p1+2p2-p3.
```

The first and fourth are `S^2` and `T^2`, already fixed by the shard margins.
The middle two are precisely the primitive sixth- and third-root norm
constraints already present in `search_variable_q_cp_sat.py`.  Inverting the
length-six Fourier transform recovers `(334,0,0,0)`.  Thus factor 14 is a
useful independent regression and signature filter, but adding its 96
quadratic products to CP-SAT would add no new mathematical information.

## Exact factor-12 reduction to length seven

The next small compression is new relative to the margin and primitive-root
constraints already exposed in the CP model.  Like every compression
condition here, it remains a logical consequence of the full exact base-
sequence equations.  Compress the same padded length-84 vectors modulo seven:

```text
X_j = sum_(t=0)^11 x_(j+7t),   0 <= j < 7.
```

The periodic compression theorem now gives

```text
sum_X (PAF_X(0),PAF_X(1),PAF_X(2),PAF_X(3)) = (334,0,0,0).
```

For `A,B`, all seven cells contain 12 signs and therefore are even integers
in `[-12,12]`.  For padded `C,D`, cells 0 through 5 have that alphabet.  The
appended zero is index 83, which is residue 6 modulo 7, so the last cell
contains 11 signs and one zero and is odd in `[-11,11]`.

Unlike factor 14, the compression step is odd and does not directly preserve
the alternating margin.  This causes no ambiguity in the exact engine.  If a
12-sign cell has compressed sum `x`, its possible internal alternating sums
form

```text
-(12-|x|), -(12-|x|)+4, ..., 12-|x|.
```

The last short cell uses the analogous exact 6-versus-5-sign table.
`variable_q_compression_7.py` propagates these tables by finite-set dynamic
programming, so liftability to each selected alternating margin is checked
without a relaxation.

There is also a useful uniform explanation for why all compatible margins
lift.  An exact compressed quadruple has individual energy at most 334.
Cauchy--Schwarz therefore leaves at least

```text
84 - floor(sqrt(7*334)) = 36
```

units of alternating slack in a long vector, and at least 28 units in the
first six cells of a short vector.  The required alternating magnitudes are
at most 18 and 17.  The margin-shard congruences select exactly the attainable
class modulo four.

## Exact factor-12 result

Factor 12 eliminates no margin shard.  The module contains one explicit
compressed four-vector PAF witness for each of the 12 ordinary row-sum profiles
and independently checks that those witnesses lift to all 288 nominal
ordinary/alternating shards (156 representatives after global-alternation
symmetry).  The witness table, cell alphabets, four compressed PAF equations,
and all alternating-margin lifts are rechecked from integers.  These witnesses
certify survival of the compressed relaxation; they are not exact
`BS(84,83)` sequences.

Primitive-seventh-root bounds nevertheless prune individual compressed PAF
signatures substantially.  The following exact counts first impose
`PAF(0) <= 334`; the right column additionally requires every primitive-seven
PSD to lie in `[0,334]`:

```text
A/B ordinary sum S
 0:  27,173 ->  4,388       2:  50,128 ->  7,764
 4:  47,698 ->  7,785       6:  47,989 ->  7,764
 8:  44,530 ->  7,749      10:  43,828 ->  7,722
12:  39,801 ->  7,704      14:  23,261 ->  4,397
16:  33,399 ->  7,650      18:  31,212 ->  7,563

C/D ordinary sum S
 1: 338,355 -> 52,429       3: 333,837 -> 52,467
 5: 326,970 -> 52,343       7: 180,578 -> 28,485
 9: 301,098 -> 52,202      11: 283,933 -> 52,059
13: 264,701 -> 51,628      15: 241,762 -> 51,412
17: 220,068 -> 51,159
```

The PSD test is exact.  For `t = 2*cos(2*pi/7)`, reduce a compressed PSD to
`a+b*t+c*t^2` modulo

```text
t^3+t^2-2t-1.
```

All three real conjugates lie in `[0,334]` exactly when the elementary
symmetric functions of the PSD and of `334-PSD` are nonnegative.  The module
computes those integer traces, pair sums, and norms; it uses no floating-point
cutoff.

Reproduce the theorem checks and selected full signature enumerations with

```sh
python3 variable_q_compression_7.py --self-test
python3 variable_q_compression_7.py --count-length 84 --ordinary-sum 14
python3 variable_q_compression_7.py --count-length 83 --ordinary-sum 7
```

The exhaustive count commands return `(23261, 4397)` and
`(180578, 28485)`, respectively.

## CP-SAT integration and benchmark

`search_variable_q_cp_sat.py --compression-7` adds the 28 residue sums and
the four exact compressed PAF equations.  Relative to the historical
shard-235 benchmark model this costs 140 integer variables and 144 constraints,
including 112 integer products.  It is opt-in because that matched short
benchmark did not show a throughput benefit:

```text
shard 235, parity-preserving hint, 1 worker, seed 668

                              default       --compression-7
15-second status              UNKNOWN       UNKNOWN
conflicts                     194,774       162,996
branches                    1,092,260       992,491

fixed 100,000-conflict run
wall time                       6.757 s        9.011 s
branches                      544,448       712,897
```

The fixed-wall branch reduction is outweighed by product-propagation cost in
the conflict-capped comparison.  This does not rule out a long-run tree-size
benefit, but it supports keeping the new invariant optional until a broader
portfolio benchmark says otherwise.
