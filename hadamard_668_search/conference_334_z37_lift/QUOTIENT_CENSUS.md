# Exact census of the semiregular `C37` orbit-sum quotients

## Result

The system

```text
T = T^T
T 1 = 0
T^2 = 333 I_9 - 37 J_9
T_ii even
T_ij odd for i != j
```

with the block-degree bounds has exactly

```text
196,560,000 labeled matrices,
625 classes under T ~ P T P^T,
314 classes under T ~ +/- P T P^T.
```

Exactly three permutation classes are equivalent to their negatives.
The permutation-automorphism orders are distributed as follows:

```text
|Aut(T)|       1    2   3  4   6  24
class count  480  100  24  5  14   2
```

The already certified `1+4+4` quotient and its negative are the two
classes of automorphism order 24.  Thus they form the unique maximally
symmetric class when global sign is identified.

There are 111 realized diagonal multisets, and **none is all zero**.
Consequently, the `(0,9)` branch of the diagonal quadratic-character
trace law is impossible for every semiregular `C37` quotient.  Up to
interchanging residues and nonresidues, every lift of every quotient in
this census must have diagonal incidence counts `(6,3)`.

Further exact distributions are:

```text
rank over F_3          2: 39 classes; 4: 586 classes
maximum |entry|        9: 3; 11: 52; 12: 231;
                      13: 231; 15: 28; 16: 80
```

The rank over `F_37` is always four.  Indeed, `T^2=0 (mod 37)` makes
the image a totally isotropic subspace of the 9-dimensional standard
quadratic space, so its rank is at most four.  The restriction to
`1^perp` has determinant `333^4`, whose 37-adic valuation is four.
Because 9 is a unit modulo 37,
`F_37^9 = <1> direct-sum 1^perp`; hence the nullity of the restriction
is at most four and the rank is at least four.

The raw binary block-membership count varies surprisingly little among
the 625 quotient classes:

```text
minimum log2 count       1340.52392808143
maximum log2 count       1340.83193919044
certified quotient       1340.72177608771
```

Here the count is

```text
prod_i C(18, (36-T_ii)/4)
  * prod_{i<j} C(37, (37-T_ij)/2),
```

before the universal `(6,3)` trace law and nonzero Fourier equations.
Thus selecting a different quotient changes the raw exponent by less
than 0.31 bit.  The certified quotient ranks 106th of 625 by this raw
count (with sign-paired ties).

Imposing the universal `(6,3)` diagonal trace law and summing over one
canonical representative of each of the 625 permutation classes gives:

```text
minimum per-class trace-law log2 ambient   1297.60492221007667
maximum per-class trace-law log2 ambient   1297.90621474626255
625-class union log2 ambient               1307.10873431446430
625-class union bit length                 1308
625-class union decimal digits             394
```

The exact first-moment map has rank 16 over `F_37` for the rank-four
square-zero quotient, and fixed-size subset moments are uniform under
translation.  Dividing the canonical union by `37^16` therefore gives

```text
post-first-moment 625-class union log2     1223.75748046440094
```

These are ambient binary membership counts, not counts of conference
graphs.  All higher Fourier equations remain to be imposed.

## The unique quotient sign-class surviving the rank-two diagonal code

The constant symmetric rank-two formal-conjugator over-code permits
diagonal adjacency degrees only in `{16,18,20}`.  Exactly two of the 625
permutation classes meet that condition.  They have the same diagonal
multiset

```text
(-4,-4,0,0,0,0,0,4,4)
```

for `T`, are negatives of one another up to permutation, and therefore
form exactly one class modulo global sign.  Both have automorphism order
two, rank four over `F_3`, rank four over `F_37`, and maximum absolute
entry 11.  Thus the diagonal over-code excludes the other 623
permutation classes but does not exclude this one sign-class.

A canonical representative is

```text
 -4 -11  -7   1   1   3   5   5   7
-11   0  11   1   1  -5   3   3  -3
 -7  11  -4  -3  -3   5  -3  -3   7
  1   1  -3   4   1   5  -9   9  -9
  1   1  -3   1   4   5   9  -9  -9
  3  -5   5   5   5   0  -9  -9   5
  5   3  -3  -9   9  -9   0   3   1
  5   3  -3   9  -9  -9   3   0   1
  7  -3   7  -9  -9   5   1   1   0
```

Its adjacency quotient `B=(37J-I-T)/2` is

```text
20 24 22 18 18 17 16 16 15
24 18 13 18 18 21 17 17 20
22 13 20 20 20 16 20 20 15
18 18 20 16 18 16 23 14 23
18 18 20 18 16 16 14 23 23
17 21 16 16 16 18 23 23 16
16 17 20 23 14 23 18 17 18
16 17 20 14 23 23 17 18 18
15 20 15 23 23 16 18 18 18
```

The nonidentity automorphism is `(4 5)(7 8)` in one-based indexing.

The later fixed-coefficient affine refinement closes this apparent
exception: the two remaining Jordan types have no binary diagonal word at
either genuine trace orientation.  Combined with the other similarity
types, no constant symmetric rank-two generator works for any of the 625
quotients.  See `RANK_TWO_JORDAN_OBSTRUCTION.md`.

## Only three binary adjacency quotients

Reducing the adjacency quotients modulo two collapses all 625 integral
classes to only three permutation classes.  Their integral-class
preimage counts are `206, 213, 206`, and their automorphism orders are
`24, 20, 24`.  Consequently the number of distinct fully labeled
binary quotients is

```text
9!/24 + 9!/20 + 9!/24 = 48,384.
```

The first and third binary classes are off-diagonal complements.  The
middle one is self-complementary up to permutation, so only two classes
remain when global sign/complement is identified.  Literal complement
acts freely on the labeled matrices, leaving 24,192 labeled pairs.

All three parity graphs are loopless because every `T_ii` is divisible
by four.  One order-24 graph has the following transparent description:
take a `K4` on `{5,6,7,8}`, an independent set `{1,2,3,4}`, join vertex
9 to the independent set, and add the matching

```text
(1,8), (2,7), (3,6), (4,5).
```

It has degree sequence `2^4,4^5`; its complement has `4^5,6^4`.  The
self-complementary order-20 class has degree sequence
`2,2,4,4,4,4,4,6,6`.  `audit_z37_quotient_parity.cpp` emits canonical
edge lists for all three.

Let `N4` be the trace-oriented rank-four unitary-projection count for
one fixed binary quotient.  The independent characteristic-two census
gives

```text
2^719 < N4 < 2^720.
```

Because only two binary quotient types remain up to fiber permutation
and global complement, the full all-quotient characteristic-two
relaxation in that normalization is bounded by `2*N4`, hence

```text
2^720 < 2*N4 < 2^721.
```

This is an upper bound modulo fiber permutation/complement on integral
binary lifts, not an exact count of integral candidates and not a
factor to multiply by the characteristic-37 moment count.

## Local rigidity

For one row, write the diagonal entry as `d` and the eight odd
off-diagonal entries as `x_j`.  The row equations are

```text
d + sum_j x_j = 0,
d^2 + sum_j x_j^2 = 296.
```

Since every odd square is `1 (mod 8)`, the second equation forces
`d^2 = 0 (mod 8)`, hence `4 | d`.  The norm bound gives

```text
d in {-16,-12,-8,-4,0,4,8,12,16}.
```

An off-diagonal entry of magnitude 17 would leave norm seven for the
other seven odd entries and zero for `d`; those seven entries would all
be `+/-1` and could not cancel `+/-17`.  Therefore `|T_ij| <= 15`.

There are exactly 411 unordered row multisets satisfying these two
equations, expanding to 2,109,524 ordered row vectors.

## Census method

`census_z37_quotients.cpp` first generates the complete list of 2,109,524
ordered valid rows.  It then fills the symmetric matrix one row at a
time.  A candidate row must agree with the previously filled upper
triangle and have dot product `-37` with every earlier row.

The root row is sorted because its other eight vertices are
interchangeable.  At every later depth, unprocessed vertices with
identical columns against all earlier rows are interchangeable, so the
new entries within each such cell are required to be nondecreasing.
This is a complete orderly augmentation: any solution can be relabeled
to meet these conditions.  At a terminal node, all diagonal row norms
are 296 and all distinct row inner products are -37, which is exactly
the required square equation.

All terminal matrices are finally canonicalized under all `9!`
permutations.  Direct stabilizer enumeration gives the automorphism
distribution above; orbit-stabilizer then gives the labeled total

```text
sum_classes 9! / |Aut(T)| = 196,560,000.
```

The complete run takes about 45 seconds and under 60 MB RSS on the
project machine.  The solver directly rechecks symmetry, parity, block
bounds, every entry of the square equation, and rank four modulo 37 for
every one of its 7,016 orderly terminal matrices.  It also contains
fail-fast assertions for every reported total and distribution.

## Reproduction

From the repository root:

```text
clang++ -O3 -std=c++20 \
  hadamard_668_search/conference_334_z37_lift/census_z37_quotients.cpp \
  -o /tmp/census_z37_quotients
/tmp/census_z37_quotients
```

For a parseable list of all canonical upper triangles, add
`--dump-canonical`.  The independently audited final dump has 625 lines
of 45 entries:

```text
SHA256(/tmp/z37_625_canonical_final.txt)
c5d8765da49deb39c2ff3407b9d0f265e3ca56c1015d5b0075355c53ca60fb5b
```

The binary quotient audit is reproduced by

```text
clang++ -O3 -std=c++20 \
  hadamard_668_search/conference_334_z37_lift/audit_z37_quotient_parity.cpp \
  -o /tmp/audit_z37_quotient_parity
/tmp/audit_z37_quotient_parity /tmp/z37_625_canonical_final.txt
```

The exact all-quotient trace-law and first-moment ambient audit is
reproduced by

```text
python3 \
  hadamard_668_search/conference_334_z37_lift/audit_z37_all_quotient_ambient.py \
  /tmp/z37_625_canonical_final.txt
```

On the project machine the asserted quotient enumeration takes about
42--44 seconds and 59 MB RSS; the exact all-profile trace audit takes about
165 seconds and under 20 MB RSS.

At the time of this finalized report:

```text
SHA256(census_z37_quotients.cpp)
759c0701ecc82ec0f74778848f4de20fcb15dc089e4b3e9cd2c35dd5007b57d3

SHA256(audit_z37_quotient_parity.cpp)
fc78d1be289d598c136e2d744e3b572d7a965db0cf7b72ad59328881e56b484c

SHA256(audit_z37_all_quotient_ambient.py)
bd4ab55b745ac5b20c7fc52e8b11a355a32629c59ba342c7415885319bdb6a2d
```
