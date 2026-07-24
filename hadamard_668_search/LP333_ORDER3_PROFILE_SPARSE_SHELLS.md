# Exact exclusion of the two sparsest order-three profile sectors

## Status

The two highest-energy type sectors of the exact order-three `LP(333)`
profile equation are empty:

```text
(n_9,n_3,n_0)=(5,3,16),
(n_9,n_3,n_0)=(6,0,18).
```

Here `n_d` counts the 24 nonzero-class profile letters of Eisenstein norm
`d`.  The exclusion includes every one of the 22 established aggregate
targets, every opposite-class quartet satisfying the local condition, and
every phase of every nonzero profile letter.  It is a complete finite
theorem, not a bounded solver result.

The reduction is sparse and algebraic.  The opposite-pair condition confines
all three norm-3 letters in the first sector to one quartet.  Reduction of
the six exact correlations modulo 9 then makes the remaining norm-9 letters
linear, because every product of two such letters is divisible by 9.  Only
552 and 288 assignments, respectively, reach detached exact replay, and
none has all twelve nonzero correlation parts equal to zero.

This excludes two of the seven possible profile type sectors.  It does not
exclude the other five sectors and does not by itself construct or exclude
an `LP(333)` or an `H(668)`.

## 1. Alphabet and type sectors

For a composition `p=(p_0,p_1,p_2)` of three, its normalized profile value
is

```text
z(p)=p_0+p_1 omega+p_2 omega^2,
omega^2+omega+1=0.
```

The ten values consist of

```text
one value of norm 0,
six values of norm 3,
three values of norm 9.
```

The norm-9 values are exactly `3 mu_3`; the prescribed class-parity signs
may change them by a unit but leave every Eisenstein coordinate divisible
by 3.  Normalized profile energy 54 gives

```text
(n_0,n_3,n_9)=(6+2h,18-3h,h),       0 <= h <= 6.
```

The present theorem treats `h=5,6`.

The distinguished zero-column values are

```text
a(0)=-1,                 b(0)=2.
```

For a nonzero lag `t`, the required profile equation is

```text
D_t =
  sum_c [a(c+t) conjugate(a(c))
        +b(c+t) conjugate(b(c))]
  =0.                                                     (1)
```

Order-three invariance and reversal reduce (1) to six displayed Eisenstein
equations.  The verifier nevertheless reconstructs all 37 physical
correlations at the final replay.

## 2. Opposite-quartet sparse geometry

Group the 24 profile letters into the six opposite-class quartets

```text
Q_j=(A_j,A_(j+6),B_j,B_(j+6)),       j=0,...,5.
```

Direct evaluation of the exact local signature equality leaves 3,334 of the
`10^4` possible labelled quartets.  Their type census is:

| norm-9 letters | norm-3 letters | labelled quartets |
|---:|---:|---:|
| 0 | 0 | 1 |
| 0 | 2 | 108 |
| 0 | 3 | 216 |
| 0 | 4 | 486 |
| 1 | 0 | 12 |
| 1 | 2 | 648 |
| 1 | 3 | 648 |
| 2 | 0 | 54 |
| 2 | 2 | 972 |
| 3 | 0 | 108 |
| 4 | 0 | 81 |

In particular, a legal quartet never contains exactly one norm-3 letter.
Therefore a global word with exactly three norm-3 letters has one and only
one distinguished quartet containing all three.  There are

```text
216 distinguished frames with no norm-9 letter,
648 distinguished frames with one norm-9 letter,
864 frames in total
```

at each possible quartet position.  Every other quartet then uses the
four-letter alphabet consisting of zero and the three norm-9 values.

This confinement is the main reason the `h=5` sector is tractable without a
general constraint solver.

## 3. Modulo-9 linearization

For one quartet assignment `R`, let `S(R)` be its correlation contribution,
including its interactions with the two fixed zero-column coefficients.
For two distinct nonzero-class quartets, let `C(R,T)` denote their cross
contribution.  Exact bilinearity gives

```text
D = sum_i S(R_i) + sum_(i<j) C(R_i,R_j).                 (2)
```

If both `R_i` and `R_j` use only zero and norm-9 letters, then every nonzero
coefficient in the cross term is divisible by 3.  Hence

```text
C(R_i,R_j)=0 modulo 9.                                  (3)
```

### The `h=6` sector

All six nonzero letters have norm 9.  Modulo 9, each self term `S(R_j)` is
supported only on its own reversal pair of correlation classes.  Thus the
six conditions do not cancel across quartets: each quartet must pass its
own local test.

Of the 256 zero/high labelled assignments of a quartet, exactly 40 pass:

```text
norm-9 letters in quartet       0    2    4
passing assignments             1   12   27
```

Before this modulo-9 test, the aggregate and type conditions leave
1,653,840 assignments on four aggregate targets, 413,460 per target.
The local test leaves only 288:

| aggregate target | before modulo 9 | after modulo 9 |
|---|---:|---:|
| `(-3,0,-3,-3)` | 413,460 | 72 |
| `(-3,0,0,3)` | 413,460 | 72 |
| `(3,0,0,-3)` | 413,460 | 72 |
| `(3,0,3,3)` | 413,460 | 72 |

### The `h=5` sector

Fix the unique triple-medium frame `M`.  The other five quartets
`R_1,...,R_5` contain only zero and norm-9 letters.  Equations (2)--(3)
become the exact finite identity

```text
D =
  S(M) + sum_i [S(R_i)+C(M,R_i)]        modulo 9.         (4)
```

Thus every remaining quartet is independent after `M` is fixed.  The
verifier enumerates the five-block high-letter catalog once per possible
position of `M`.  Its exact sparse counts are

```text
four norm-9 letters       392,445,
five norm-9 letters     3,767,472.
```

Matching the established aggregate targets gives:

| aggregate target | before modulo 9 | after modulo 9 |
|---|---:|---:|
| `(-3,-3,-4,-2)` | 5,748,834 | 42 |
| `(-3,-3,-2,2)` | 5,748,834 | 42 |
| `(0,3,-4,-2)` | 5,748,834 | 42 |
| `(0,3,-2,2)` | 5,748,834 | 42 |
| `(4,-1,0,0)` | 5,819,400 | 192 |
| `(5,1,0,0)` | 5,819,400 | 192 |
| **total** | **34,634,136** | **552** |

No unrestricted `10^24` enumeration and no CP-SAT search occurs.  The large
pre-filter number is counted through a five-block sparse dynamic catalog;
only the 552 modulo-9 survivors enter physical correlation replay.

## 4. Detached exact replay

Every modulo-9 survivor is reconstructed as two physical
`H`-invariant length-37 Eisenstein words.  Independently of the block
decomposition, the verifier checks:

```text
the declared type sector,
the exact four-coordinate aggregate,
all six opposite-quartet signatures,
origin energy 167,
all 37 physical correlations,
constancy on every order-three cyclotomic class,
reversal/conjugation on the twelve nonzero parts,
the direct modulo-9 condition,
exact D_t=0 on every nonzero part.
```

The final failure histograms count all twelve nonzero parts:

| sector | 6 bad parts | 10 bad parts | 12 bad parts | exact survivors |
|---|---:|---:|---:|---:|
| `(5,3,16)` | 24 | 144 | 384 | 0 |
| `(6,0,18)` | 0 | 24 | 264 | 0 |

The replay certificates encode, in deterministic order, the sector,
aggregate-target index, all 24 profile IDs, and all twelve integer
coordinates of the six displayed exact residuals.  Their SHA-256 values
are:

```text
h=5
e917360e36cbf57b96e5f0a8d842017eaeab9a73c4cdff804bdad719d898090e

h=6
981f1a39c7858271e9588b7606dece1c6d408b31506381c71eecc9dbc85d410e
```

Both hashes and every displayed count are pinned inside the verifier.

## 5. Consequence

Any exact order-three profile survivor must lie in one of

```text
h=0,1,2,3,4.
```

Equivalently, it must contain at least ten nonzero profile letters and at
least six norm-3 letters.  The exact profile constructor can delete the two
sparse sectors before invoking any general search.

This conclusion concerns the necessary order-three profile gate only.
Passing one of the five remaining sectors would still require a labelled
phase lift, all 333 Legendre-pair correlations, and the final order-668
Hadamard replay.

## Reproduction

From the repository root:

```text
mkdir -p /tmp/h668_sparse_shells_build

clang++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror \
  hadamard_668_search/verify_lp333_order3_profile_sparse_shells.cpp \
  -o /tmp/h668_sparse_shells_build/verify_sparse_shells

/tmp/h668_sparse_shells_build/verify_sparse_shells

(cd hadamard_668_search && \
  python3 -m unittest -v \
  test_lp333_order3_profile_sparse_shells.py)
```

The reference run used about 78 MB peak RSS and completed in about 23
seconds.  The enumerator uses exact integer arithmetic and the C++ standard
library only.
