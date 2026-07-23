# Unrestricted projective common-type five-comb exhaustion

## Status

No Hadamard matrix of order 668 is claimed here.

This note closes one exact, explicitly delimited five-comb family. For each
of the 48 normalized complementary length-five quartets, all of the following
were retained simultaneously:

- every permutation of its eight polarized carrier types;
- every projective row-sign labeling allowed by the complete modulo-four
  quotient, including repeated labels;
- every carrier orientation;
- every physical hole completion; and
- all 83 aperiodic base-sequence equations and the exact row-square identity.

The family splits into 32 structural cores. All

```text
48 * 32 = 1,536
```

models terminated `INFEASIBLE`. These are recorded CP-SAT conclusions, not
independently replayable UNSAT certificates. The result excludes the
common-type polarized five-comb family, not all five-comb packings and not
`BS(84,83)`.

## 1. Exact projective quotient

The eight carrier slots are at shifts

```text
0,1,2,3,20,21,22,23.
```

Their four-row signs are the eight projective columns from two real mutually
unbiased `H4` bases. Write each slot label as three bits. The complete
modulo-four syndrome is affine-linear in the 24 label bits and has rank nine.
After translating all labels so that slot zero is labeled zero, the RREF is

```text
l00 xor l50 = 0
l02 xor l42 = 0
l10 xor l50 = 0
l12 xor l50 xor l70 xor l72 = 0
l20 xor l70 = 0
l22 xor l60 xor l62 xor l70 = 0
l30 xor l60 = 0
l32 xor l50 xor l52 xor l60 = 0
l40 xor l50 = 0.
```

It leaves exactly twelve free bits

```text
alpha,beta,u5,u6,u7,y1,...,y7
```

and hence exactly 4,096 normalized projective maps. Their labels are

```text
low    = (0,0,beta,alpha,0,0,alpha,beta)
middle = (0,y1,y2,y3,y4,y5,y6,y7)
high   = (0,beta xor u7,
            alpha xor beta xor u6,
            alpha xor u5,
            0,u5,u6,u7).
```

Swapping the two long rows and/or the two short rows translates the seven
middle bits by the low, high, or low-XOR-high masks. Exact lex leaders reduce
the 4,096 maps to 1,440 row-pair orbits. The five structural bits
`alpha,beta,u5,u6,u7` define the 32 solver cores.

## 2. The complete physical hole fiber

Number the fourteen hole entries in row order at

```text
long rows:  40,41,82,83
short rows: 40,41,82.
```

Write `h_i in {0,1}` for the negative-sign bit of entry `i`, so its physical
sign is `(-1)^h_i`. After row-sign normalization and the rank-nine label
equations, the complete modulo-four fiber is label-independent:

```text
h0 = h4
h1 = h5
h2 = h6
h3 != h7
h8 = h11
h10 = h13.
```

These six relations give exactly 256 physical completions. Lag 82 adds

```text
h2 + h10 = 1.
```

Thus the four signs at position 82 are, up to one scalar `eta`, the fixed
projective direction

```text
V_2 = (+,+,-,-),
```

and the two signs at position 83 are `f,-f`.

## 3. Exact high-lag boundary theorem

Let

```text
Phi(label) = sum of the four entries of V_label
           = (4,0,0,0,2,2,2,-2).
```

Carrier inner products satisfy

```text
V_l dot V_m = Phi(l xor m).
```

After gauging out `eta` and `f`, lags 81 through 78 depend only on the twelve
projective parameters and seven adjusted carrier signs. Exhaustive symbolic
evaluation gives:

```text
all directions, full table       33,718 rows
all directions, parameter image   2,967 rows
physical V_2 full table           10,934 rows
physical V_2 parameter image       2,434 rows.
```

The physical full-table SHA-256 is

```text
441c25786c4a0bc56f9e86c84bf9c8c8252595a9f75298aad960c31320aeb6b4
```

and its parameter projection has SHA-256

```text
85972db2c71b3e1415705017b0f3f1e57aab3f7cba880104c8f60d83c687d2c0.
```

In particular lag 81 gives the universal clause

```text
beta or u7 or y1 or y7.
```

The exact model channels this compact table to the actual type, orientation,
and hole variables. It also exposes every coefficient pair at lags 64 through
83 directly: 800 Boolean products and twenty exact cardinalities.

The dependency-free verifier checks every table row by reconstructing actual
sequences and checks the closed boundary formula across all 48 quartets:

```sh
python3 verify_five_comb_high_lag_boundary.py
```

## 4. Exact correlation model

For each slot and carrier type, the scalar carrier has ten coefficients:
five teeth at its shift and five more at separation 42. The contribution of
two carriers factors exactly as

```text
projective inner product * scalar cross-correlation.
```

Carrier-hole terms use one projective row sign, and hole-hole terms are
literal sign products. This gives an exact compact model of all positive
lags. A second pure-Boolean model expands all 334 coefficients and retains
12,338 cross-carrier/hole XOR products; the 1,440 within-carrier products
cancel identically by quartet complementarity.

The factorized model also imposes the possible base-sequence row-sum
profiles. Any feasible assignment is reconstructed as four binary sequences,
checked against all 83 aperiodic correlations, converted to the special
quadruple, and used to build and verify the complete `668 x 668` matrix before
it can be written as a candidate.

Focused independent checks are:

```sh
.solver-venv/bin/python -m unittest -v \
  test_five_comb_unrestricted_projective_cp_sat.py \
  test_five_comb_spectral16_unrestricted.py
```

## 5. Exhaustive solver partition

The runner is resume-safe and stores one atomic record for each quartet/core
pair:

```sh
.solver-venv/bin/python run_five_comb_unrestricted_core_shards.py \
  --quartet-start 0 --quartet-end 47 \
  --time-limit 90 --workers 1 --max-memory-mb 3072 --in-process \
  --output-directory output/five_comb_unrestricted_core_cp_v2
```

The completed corpus contains exactly 1,536 distinct records:

```text
INFEASIBLE  1,536
UNKNOWN         0
candidates      0.
```

Its aggregate recorded solver statistics are:

```text
solver wall time     10,768.610061 seconds
conflicts             3,568,646
branches             71,107,207
zero-Boolean shards          58.
```

The canonical digests are:

```text
corpus
9c1534a77319dd1b8e0a90f8fb2a620ad09499c6948e1198087bc29c967ecb45

manifest
2012a82da3df8d60ec5549f888714c03b018bb6b8062632d1d80fed3a43aa3fe

source bundle
7ef1438adbe6b1f196f3de729c14d694279d077adc26ab7a185267b084757ca8.
```

The integrity verifier and manifest pin the retained source bundle, coverage,
record statistics, and canonical corpus digest. They do not record the
Python or OR-Tools dependency versions, and they do not turn the CP-SAT
statuses into proof certificates:

```sh
python3 verify_five_comb_unrestricted_full_corpus.py
```

The shard JSON records do not embed parent batch identifiers, limits, or
source hashes. The verifier can certify their contents and the retained
source bundle, but cannot reconstruct those missing invocation fields from
the records themselves.

## 6. Consequence

The diagonal/common-type hypothesis is too rigid. The correct continuation is
not a larger search over these 48 cases. The self-cancellation theorem in
`FIVE_COMB_PAIRED_LOBES.md` enlarges the carrier family while preserving the
rank-nine projective quotient, the 256-point hole fiber, the 32 cores, and the
physical high-lag table.

One of those 32 cores is now eliminated without a solver or a carrier-family
assumption. In structural core zero every label is `0` or `2`, so the four
carrier row sums have the form `(x,x,y,y)`. The physical hole fiber reduces
the necessary `z=1` row-square identity to

```text
X^2 + (Y+t)^2 = 165+t^2,  t in {-1,0,1}.
```

Neither 165 nor 166 is a sum of two integer squares. This removes all 128
normalized maps in core zero, including 8 of the 2,434 projected high-lag
rows and 288 of the 10,934 full rows. The dependency-free reconstruction is
`verify_five_comb_core0_obstruction.py`.
