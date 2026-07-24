# Exact exclusion of the fourth order-three profile shell

## Status

The order-three `LP(333)` profile shell

```text
(n_9,n_3,n_0)=(4,6,14)
```

contains no exact profile-zero assignment.  A deterministic exhaustive
verifier reduces the shell modulo nine, replays every modular survivor in
exact integer Eisenstein arithmetic on all 37 physical lags, and finds

```text
exact profiles = 0.
```

This is an exact exclusion of one norm shell.  It is not an `LP(333)` or a
Hadamard matrix of order 668.  Together with the separately verified
`n_9=5` and `n_9=6` exclusions, it gives the constructor cut

```text
n_9 <= 3.
```

## 1. The shell and its local medium frames

The ten profile values are

```text
{0} union 3 mu_3 union (1-omega) mu_6.
```

Call the three norm-nine values high, the six norm-three values medium, and
the unique norm-zero value zero.  The energy equation in this shell gives
four high letters and six medium letters among the 24 profile positions.

Group the positions into the six opposite-pair quartets

```text
(A_j,A_(j+6),B_j,B_(j+6)),             0 <= j < 6.
```

The exact local pair-signature equation has the following medium-only
census:

| medium letters in a quartet | legal oriented states |
|---:|---:|
| 0 | 1 |
| 1 | 0 |
| 2 | 108 |
| 3 | 216 |
| 4 | 486 |

In particular, one medium letter in a quartet is impossible.  Six medium
letters can therefore occur only with quartet-size partitions

```text
2+2+2,       3+3,       4+2.
```

The legal support-mask and oriented-frame counts are consequently

```text
medium support masks = 4,740,
oriented medium frames = 27,468,720.
```

More explicitly,

```text
C(6,3) 6^3                         =  4,320 masks,
C(6,2) 4^2                         =    240 masks,
6*5*1*6                            =    180 masks,

C(6,3) 108^3                       = 25,194,240 frames,
C(6,2) 216^2                       =    699,840 frames,
6*5*486*108                        =  1,574,640 frames.
```

## 2. Why the four high letters are affine modulo nine

Fix a legal medium frame `m`.  If `h_i` is a one-slot high correction, then
every coefficient of `h_i` is divisible by three.  Hence every ordered
high-high correlation product is divisible by nine, including products
between distinct high slots.  Coefficientwise on every nonzero lag,

```text
D(m + sum_i h_i)
  = D(m) + sum_i (D(m+h_i)-D(m))              (mod 9).       (1)
```

The local pair signatures imply that `D(m)` is coefficientwise divisible by
three.  Divide (1) by three and reduce modulo three.  At each of the six
reversal-independent lags write the quotient as

```text
q_j=a_j+b_j omega in F_3[omega].
```

The linear functional

```text
ell(q_j)=a_j+b_j
```

splits the affine equation into a support flag and a phase coordinate:

1. a high letter changes `ell(q_j)` only at its own opposite-pair quartet;
2. that change is independent of which of the three high phases is used;
3. every high-medium cross term lies in `ker(ell)`;
4. changing a high phase affects only its own quartet and spans
   `ker(ell)`.

Therefore the six support flags are solved first by a weight-four layered
enumeration.  Once a support is fixed, an occupied quartet always solves its
remaining phase coordinate, with `3^(k-1)` solutions if it contains `k`
high letters.  An empty quartet must already have zero remaining
coordinate.  The exact four-coordinate aggregate target is imposed on the
resulting phase solutions.

This is a finite algebraic enumeration, not a search through the original
666 signs.

## 3. Complete census

The deterministic verifier obtains

```text
oriented medium frames                         27,468,720
phase-free high-support leaves                115,033,608
supports passing every empty-quartet gate       6,835,368
solutions of all modulo-nine phase equations   12,835,512
exact-aggregate modulo-nine survivors             345,984
exact profile-zero survivors                            0
```

The 345,984 survivors have the following numbers of bad nonzero class
correlations under exact replay:

| bad classes | survivors |
|---:|---:|
| 4 | 204 |
| 6 | 1,860 |
| 8 | 16,884 |
| 10 | 96,192 |
| 12 | 230,844 |

Thus every modular survivor fails the exact profile-zero equation.

The target-resolved survivor counts, in the canonical 22-target catalog
order, are

```text
15162, 15162, 13518, 13518, 14970, 14970,
15162, 15162, 19818, 19818, 14970, 14970,
15147, 15147, 19818, 19818, 14358, 14358,
14922, 15147, 15147, 14922.
```

## 4. Mechanical verification

Compile and run the standalone verifier:

```text
c++ -std=c++20 -O3 -DNDEBUG \
  verify_lp333_order3_profile_shell_four.cpp \
  -o /tmp/verify_lp333_order3_profile_shell_four
/tmp/verify_lp333_order3_profile_shell_four
```

Or run the focused wrapper, which compiles the source and checks every
pinned census:

```text
python3 -m unittest -v test_lp333_order3_profile_shell_four.py
```

On the first complete run, the exhaustive verifier took 75.24 seconds,
used 3,866,624 bytes of maximum resident memory, and performed no swaps.
The enumeration streams frames and survivors; it does not retain the
345,984-candidate corpus in memory.

The C++ verifier independently reconstructs the ten-value alphabet,
cyclotomic classes, signed coefficients, pair signatures, affine
high/medium tables, and all 37 physical correlations.  It checks
class-invariance, reversal-conjugation, modulo-nine survival, the complete
aggregate catalog, and exact zero for every enumerated survivor.

Pinned SHA-256 values are:

```text
verifier source
b76c700e459cbe36318904b9c46ed40302ee50fdbf0eca71a2bbfd362b2d93ab

canonical verifier stdout
a97dd5e6a5942f0b4e8deca5d2c563258cdc60df9ddf5ddb669bb614e6c5ffa9
```
