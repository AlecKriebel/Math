# LP(333) trivial-character phase transfer

## Status

The six Eisenstein phase sequences in
`LP333_ORDER3_PHASE_FACTOR.md` admit an exact low-dimensional transfer at
the trivial character of `C_37`.  For each channel, all of its placement
trits collapse to:

```text
one integer energy
+ one Eisenstein cross term.
```

The two channels join by one integer equality and one Eisenstein equality.
For a fixed profile tuple this replaces a scan of `3^54` phase assignments
by six small convolutions and a signature join.

This transfer is **not a new obstruction beyond the existing exact
1,756-word row-sum catalog**.  It is the primitive-nine Fourier form of
that row-direction gate.  A dependency-free replay proves, including
multiplicities, that its uncollapsed phase-sum survivors equal the
appropriate catalog intersection on all 22 stored profile tuples and on
the original row-695 profile.

There is also an important upstream scope restriction.  All 22 stored
profile-ideal witnesses, and the profile shared by the two labelled
row-695 fixtures, fail the stronger full-LP condition `D_t=0`.  Their
transfer censuses below are therefore diagnostic.  The architecture is
intended for a future exact-zero-moment profile tuple.

No `LP(333)` or `H(668)` is constructed.

## 1. Augmenting the six phase sequences

For channel `X` and residue fiber `s`, put

```text
S_(X,s) = sum_(c in C_37) U_(X,s)(c) in Z[omega].
```

The phase-frame equations are

```text
K_00+K_11+K_22 = 167 e,
K_10+K_21+omega^2 K_02 = 0.
```

Evaluation at the trivial column character gives, for one channel,

```text
E_X =
  |S_(X,0)|^2+|S_(X,1)|^2+|S_(X,2)|^2,

T_X =
  S_(X,1) conjugate(S_(X,0))
 +S_(X,2) conjugate(S_(X,1))
 +omega^2 S_(X,0) conjugate(S_(X,2)).
```

Every exact phase frame therefore satisfies

```text
E_A+E_B = 167,                 (1)
T_A+T_B = 0.                   (2)
```

Conversely, (1)--(2) are exactly the two phase-frame equations after
augmentation.  Thus `(E_X,T_X)` is a complete transfer signature for this
character, not a relaxation of it.

## 2. Why each one-sequence convolution is small

Every nonzero order-three column class has three physical columns.  If its
fixed fiber count is one or two, its contribution to the augmented sum is

```text
  3 omega^u       for count one,
 -3 omega^u       for count two,
```

with one free `u in C_3`.  Counts zero and three contribute zero.  The
fixed zero column contributes one known signed phase or zero.  Hence

```text
S_(X,s) =
  U_(X,s)(0) + 3 sum_j epsilon_j omega^(u_j),          (3)
```

where every `u_j` is independent and `epsilon_j` is fixed by the profile.
An exact dictionary convolution computes every possible value of (3) and
its assignment multiplicity.

For every norm-54 profile tuple in the audited corpus there are 54 active
fibers, so the raw phase space is

```text
3^54 = 58,149,737,003,040,059,690,390,169.
```

Energy truncation at 167 leaves fewer than 2,000 `(E_X,T_X)` states in
each channel in the replayed corpus.  Joining the two dictionaries by
(1)--(2) leaves only 22 to 87 compatible transfer signatures.

## 3. Exact relation to the row-sum catalog

Let `m_(X,r)` be the physical plus-count in CRT row `r`.  For a fixed
residue `s`, the profile fixes

```text
P_(X,s) = m_(X,s)+m_(X,s+3)+m_(X,s+6),
```

while the phase sum is

```text
S_(X,s) =
  m_(X,s)+m_(X,s+3) omega+m_(X,s+6) omega^2.           (4)
```

Writing `S=a+b omega`, (4) and the fixed total recover the three margins
uniquely:

```text
m_(X,s+6) = (P-a-b)/3,
m_(X,s)   = m_(X,s+6)+a,
m_(X,s+3) = m_(X,s+6)+b.                              (5)
```

Thus the six phase sums plus the profile totals are merely Fourier
coordinates for the 18 row margins.  The verifier loads the pinned
1,756-word row-sum catalog, reconstructs those same sums from every catalog
row, and compares the two finite objects.

For each of the 22 stored profile tuples it proves exact equality of:

```text
the uncollapsed phase-sum join from (1)--(3),
the compatible row-sum catalog intersection from (4)--(5),
the assignment multiplicity attached to every surviving six-sum word.
```

This proves the claimed comparison; a coincidental equality of total
counts would not suffice.

For a future profile satisfying the exact zero-moment condition, the
practical pipeline is therefore:

```text
exact D_t=0 profile
    -> six phase-sum convolutions
    -> (E,T) channel join
    -> retain only the corresponding catalog margins
    -> nontrivial column-character / mixed-lag equations.
```

## 4. Exact diagnostic corpus

The columns below are:

```text
aggregate shard target,
compatible (E_A,T_A) signatures,
compatible row-sum catalog words,
phase assignments satisfying the row-direction gate.
```

| target | signatures | catalog words | accepted phase assignments |
|---|---:|---:|---:|
| `(-3,-3,-4,-2)` | 69 | 77 | 299,476,370,398,383,830,889 |
| `(-3,-3,-2,2)` | 69 | 77 | 285,391,291,146,212,486,376 |
| `(-3,0,-3,-3)` | 46 | 93 | 338,269,656,430,021,779,738 |
| `(-3,0,0,3)` | 46 | 93 | 334,202,436,963,302,929,560 |
| `(-1,-2,-5,-1)` | 71 | 79 | 297,809,708,683,170,689,964 |
| `(-1,-2,-4,1)` | 71 | 79 | 325,887,533,715,811,099,305 |
| `(0,3,-4,-2)` | 69 | 77 | 286,095,435,102,253,502,460 |
| `(0,3,-2,2)` | 69 | 77 | 297,137,928,876,535,479,168 |
| `(1,-1,2,-2)` | 65 | 73 | 299,284,820,085,636,500,400 |
| `(1,-1,4,2)` | 65 | 73 | 282,896,931,033,697,012,200 |
| `(1,2,-5,-1)` | 75 | 82 | 361,897,672,694,646,844,620 |
| `(1,2,-4,1)` | 75 | 82 | 315,109,917,041,025,241,080 |
| `(2,-2,-4,-2)` | 64 | 72 | 270,488,436,031,587,303,072 |
| `(2,-2,-2,2)` | 64 | 72 | 277,384,846,079,729,614,824 |
| `(2,1,2,-2)` | 62 | 72 | 270,824,491,877,087,676,780 |
| `(2,1,4,2)` | 62 | 72 | 272,179,280,210,017,800,942 |
| `(3,0,0,-3)` | 47 | 98 | 348,610,104,286,486,308,288 |
| `(3,0,3,3)` | 47 | 98 | 350,009,864,417,078,476,128 |
| `(4,-1,0,0)` | 22 | 45 | 180,980,378,357,204,960,640 |
| `(4,2,-4,-2)` | 87 | 96 | 363,733,977,044,403,716,436 |
| `(4,2,-2,2)` | 87 | 96 | 361,319,476,281,225,792,516 |
| `(5,1,0,0)` | 37 | 73 | 266,128,504,156,683,310,464 |

Relative to `3^54`, the accepted fraction lies between
`3.1123e-6` and `6.2552e-6`: an exact reduction by factors between about
159,868 and 321,304 before any nontrivial column-character equation.

Again, this quantifies coordinate pruning on profile tuples already known
to fail `D_t=0`; it is not evidence that any of them can lift.

## 5. The two labelled fixtures

The original labelled row-695 certificate and its later trit-lift fixture
have the same six augmented phase sums.  Their channel signatures are

```text
(E_A,T_A) = (69, (32,15)),
(E_B,T_B) = (98, (-32,-15)).
```

They therefore satisfy (1)--(2), and the verifier locates their six-sum
word at catalog index 695.  The pinned profile has:

```text
compatible transfer signatures       65
compatible catalog rows               73
accepted phase assignments
  291,964,627,896,688,393,920.
```

Both labelled objects remain non-solutions because their shared profile
has twelve nonzero `D_t` classes.

## 6. Pinned hashes

```text
collapsed 22-tuple transfer corpus
af3bd3a306b7e23bd8c200acdd717d4c2b622bb17a08daf08a9ab5e2e2b6564d

exact catalog-intersection corpus
24b33f2fc55c8fe3580c1d35c1d24491e95b2ef0eafaa213b12e8030ae8378e7

two labelled fixture audits
87a5cf3f7be613a5fc77e285f9f0e55d2b6f67d07a88639aff8e66001e7f7c63
```

## Reproduction

```text
python3 verify_lp333_order3_phase_transfer.py
python3 -m unittest -v test_lp333_order3_phase_transfer.py
```

The replay uses exact integer and Eisenstein arithmetic and the Python
standard library only.
