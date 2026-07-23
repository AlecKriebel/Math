# Sextic quotient for `LP(333)`

## Status

This is an exact order-six multiplier reduction of the Legendre-pair route.
It leaves 108 Boolean signs after symmetry normalization. An explicit quotient
table satisfies both coordinate axes but is not a Legendre pair because 20
of its 24 mixed quotient cells remain nonzero.

No `LP(333)` or `H(668)` is claimed.

## 1. Order-six multiplier

In `F_37^*`, let

```text
H = <2^6> = {1,27,26,36,10,11}
C_j = 2^j H,  j=0,...,5.
```

This is induced by the order-six multiplier

```text
<64> mod 333 = {1,64,100,73,10,307},
```

which fixes the `Z/9` CRT coordinate. Let `P_0={0}` and
`P_{j+1}=C_j`. The quotient is a `9 x 7` QPSK table `x_k(r)`.
Its fixed compression is

```text
sum_r x_0(r)     = 1
sum_r x_{j+1}(r) = -3 i (-1)^j.
```

For `b in C_s`, define

```text
M_s(k,l) = #{c in P_k : c+b in P_l}.
```

The quotient correlation equation is

```text
Re sum_{r,k,l} M_s(k,l) x_k(r) conjugate(x_l(r+a)) = -1.
```

Negation lies in `H`, so real-PAF reversal leaves 34 quotient-lag
representatives:

```text
a=0, b in C_0,...,C_5                  6
a=1,...,4, b=0 or b in C_0,...,C_5    28.
```

These are 34 reversal-inequivalent equations, not 34 linearly independent
equations. Fixed compression supplies seven affine relations, so at most 27
can be linearly independent.

## 2. Exact row-axis factorization

Put

```text
R_k(a) = Re PAF(x_k,a).
```

The zero-column equations give

```text
R_0(a) + 6 sum_{k=1}^6 R_k(a) = -1.
```

The sum of `x_0` is one, so formal possibilities for the four nonzero
real-PAF values are

```text
(-1,-1,-1,-1)
(-7,-1,-1,5)
(-7,-7,5,5).
```

Exact enumeration of all `4^9` QPSK words proves that only the first occurs.
There are exactly 972 such `LP(9)` cores.

For a nonzero quotient column with sum `-3i`, there are 7,056 words and 28
real-PAF signatures. Ordered signature sextuples summing to zero number
1,658,700. A three-plus-three meet in the middle has only 298 compatible
aggregate vectors, with individual triple tables of size at most 195.

The 5,832-element CRT symmetry group is transitive on the 972 zero-column
cores. Fixing

```text
x0 = (0,0,0,1,2,3,1,3,2)
```

as exponents of `i` removes 18 Boolean signs. Exactly 54 QPSK phases, or 108
binary `A/B` signs, remain.

Within the explicitly audited 5,832 class-rotation/normalization actions, the
residual symmetry compatible with both this canonical zero word and the
fixed alternating compression is `C3`, not `C6`. The unit

```text
d=226 mod 333
```

satisfies `d=1 mod 9`, `d=2^2 mod 37`, and `d^3=64 mod 333`. It fixes the
row coordinate and zero column and rotates classes by two. Exact enumeration
proves that the 972 zero words are precisely the free orbit of the canonical
word under independent `A/B` row shifts, common units modulo 9, and `A/B`
swap. Odd class rotations require a swap to preserve the alternating
compression, but that swap moves the canonical zero word; after
recanonicalization only rotations `0,2,4` survive.

On the signature fiber this `C3` action has 18 fixed sextuples. Burnside's
lemma therefore gives

```text
(1,658,700 + 2*18)/3 = 552,912
```

signature-sextuple orbits. This is not a count of full word or solution
orbits; for the 18 fixed signature patterns, any remaining word-level `C3`
symmetry is intentionally left unbroken.

## 3. Axis-complete skeleton

The repository checker contains an explicit `9 x 7` exponent table. It
satisfies:

```text
all fixed quotient sums
all 36 pure-column physical correlations
all 8 pure-row physical correlations.
```

Its mixed quotient residual matrix is

```text
( 6, 0,  2,-4,  6, -8)
( 0, 0, -8, 6,  4,  4)
( 2,-4, -4,-8,  0,  8)
(-8, 4, 10, 6,-10, -4).
```

Thus it is explicitly a non-candidate:

```text
mixed quotient cells bad      20/24
quotient residual energy        784
expanded mixed lags bad       120/144
physical residual energy       4,704
maximum residual                  10.
```

## 4. Exact Boolean model

Map a phase to two signs by

```text
x = (A+B + i(B-A))/2.
```

Then

```text
2 Re(x conjugate(y)) = A_x A_y + B_x B_y.
```

Each quotient equation becomes one weighted XOR cardinality of exactly 334
over the 108 free signs and the fixed zero column. There are at most
`C(108,2)=5,778` reusable pair-XOR literals. The base model needs only 2,862
of them:

```text
primary signs             108
cached XOR variables    2,862
compression constraints    12
quotient equations          34
```

The implemented default additionally channels six class words to the exact
28-signature catalog and 298 aggregate shards, then imposes a tie-safe
low-memory lex leader on the three adjacent class pairs:

```text
                                      variables  constraints
base model, no signature channel          2,970        2,908
signature channel, no C3                  2,977        2,916
signature channel plus C3 (default)       2,979        2,923
fixed signature shard plus C3             2,978        2,923.
```

The `C3` leader has two Boolean auxiliaries and seven constraints; exhaustive
replay proves it selects exactly the least cyclic signature rotation,
including every tie case. A feasible assignment is expanded and independently
checked at the quotient, CRT, all-333-lag Legendre-pair, bordered construction,
and full Hadamard layers before it can be written:

```sh
.solver-venv/bin/python search_lp333_sextic_cp_sat.py \
  --time-limit 3600 --workers 4 --max-memory-mb 8192 \
  --output output/lp333_sextic_candidate.json
```

A bounded base-model pilot with eight workers and a nominal 8 GiB solver cap
ended `UNKNOWN` after 300.070896 solver-seconds:

```text
conflicts          145,214
branches         3,155,570
maximum RSS        522.8 MB
swaps                    0
candidates               0.
```

The strengthened signature-plus-`C3` model then ran for 20.069041
solver-seconds with four workers:

```text
status                UNKNOWN
conflicts                 711
branches              149,953
solver booleans         79,251
maximum RSS      2,263,646,208 bytes
swaps                       0
candidates                  0.
```

Neither pilot proves anything negative. The strengthened model is now the
default, and the separate-shard continuation is resume-safe:

```sh
.solver-venv/bin/python run_lp333_sextic_signature_shards.py \
  --start 0 --end 297 --time-limit 3600 \
  --workers 1 --max-memory-mb 4096
```

The construction order is:

1. fix the canonical zero column;
2. impose the six nonzero-column compressions;
3. impose the row-axis signature condition in one of 298 shards and use the
   exact residual `C3` representative;
4. sieve with the six pure-column equations;
5. impose the 24 mixed equations;
6. expand every feasible quotient to two binary length-333 sequences;
7. verify every periodic correlation and then the complete `668 x 668`
   construction.

## 5. Closed smaller subfamilies

The quadratic-residue/order-18 quotient is already impossible from two
pure-column equations. Bounds leave only two cross terms, `J=-9` and `J=-8`,
and each contradicts the prescribed QPSK sums.

The natural logarithmically shifted template is also impossible: its bulk
nonzero-column correlation forces a real PAF value `-1` even at lag zero,
where it must be 9.

## 6. Verification

The standard-library checker reconstructs the subgroup, all transition
matrices, row catalogs, the full 333-cell skeleton, both residual energies,
and both negative lemmas. A second dependency-free verifier reconstructs the
972-word normalization orbit, physical `d=226` action, all 298 invariant
shards, and the complete Burnside/lex-leader count:

```sh
python3 check_lp333_sextic_quotient.py
python3 verify_lp333_sextic_c3.py
python3 -m unittest -v \
  test_lp333_sextic_quotient.py test_lp333_sextic_cp_sat.py
```

Pinned hashes include:

```text
classes
2dd47bcbd01b4d59c6b44fd60d4034eb247557017cabd6983d09aa03d6aca293

transition matrices
995968188a4d5ad6242891808a1ca15be500d9d3cc2ec267a8db802d01257c49

axis-complete skeleton
e00542e3fbe8da61888553c567462386740d948a92723ef8375b7060ce6cb9b1

mixed residual matrix
6fdcd7a7f1a659c5292e2970296e4f32288458fdaab35517dcd5cd6cb0b3b755

C3 verifier source
b6c80d63ca8c29cb15debc66b760046ab9db68069cc794ef59a552a254bbfef7

strengthened CP-SAT source
55d8bd65dc3ba2759addcf00084bfaf481b444e8b1df07aca410498f642e2413.
```
