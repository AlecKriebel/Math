# A signed-skeleton certificate for the four-high shell

## Status

This compressed certificate package gives a second, valuation-led exact exclusion of the
order-three `LP(333)` profile shell

```text
(n_9,n_3,n_0)=(4,6,14).
```

It does not enumerate the `27,468,720` fully phased medium frames used by
the production certificate.  Instead it reduces them to

```text
37,680 signed medium skeletons
 1,704 exact symmetry orbits,
```

restores all phases by a lossless six-trit meet-in-the-middle join modulo
nine, and replays one representative of every surviving full-assignment
orbit on all 37 physical lags in exact Eisenstein arithmetic.

The final census is

```text
modulo-nine full-assignment orbits        14,443
orbit-weighted raw modulo-nine survivors 345,984
exact profile-zero assignments                 0.
```

The orbit-weighted target counts and bad-class histogram agree
entry-for-entry with the independent production enumeration.  This is a
new compressed certificate for an exclusion already known in the project;
it is not a new excluded shell, an `LP(333)`, or an `H(668)`.

## 1. Signed uniformizer skeletons

Put

```text
lambda=1-omega.
```

The six norm-three profile values are uniquely

```text
sigma lambda omega^u,       sigma in {+1,-1}, u in F_3,
```

and the three norm-nine values are `3 omega^v`.  Modulo three a medium
letter retains only `sigma lambda`.  In an opposite-pair quartet

```text
(A_j,A_(j+6),B_j,B_(j+6)),
```

write its four signed residues as `(a_0,a_1,b_0,b_1)`.  The audited local
pair equation reduces to

```text
-a_0+a_1+b_0-b_1=0 in F_3.                         (1)
```

The exact local signed census by number of medium positions is

| medium positions | signed states |
|---:|---:|
| 0 | 1 |
| 1 | 0 |
| 2 | 12 |
| 3 | 8 |
| 4 | 6 |

Six medium letters therefore have only the partitions

```text
2+2+2,       3+3,       4+2.
```

Their complete signed counts are

```text
C(6,3) 12^3       = 34,560,
C(6,2)  8^2       =    960,
6*5*6*12          =  2,160,
total             = 37,680.
```

Restoring the omitted medium phases multiplies every skeleton by `3^6=729`
and exactly recovers `27,468,720`.

The exact profile symmetry group

```text
G=C_6 x C_(2,A) x C_(2,B)
```

acts by the shared even class rotation and independent channel star
operations.  Direct canonicalization gives exactly `1,704` skeleton
orbits.

## 2. The first lambda-adic flag

For a phase-zero skeleton baseline `m`, every local equation makes

```text
D_j(m) in 3 Z[omega].
```

Write

```text
q_j=D_j/3 mod 3,
ell(a+b omega)=a+b.
```

Changing one medium phase or inserting one high letter changes `ell(q_j)`
only in that position's opposite quartet.  At a nonempty-medium quartet,
one medium phase solves its flag equation, leaving `3^(m-1)` medium-phase
choices.  At an empty-medium quartet the high support must itself solve
the flag.

The complete support census over the 37,680 skeletons is:

| extendible four-high supports | skeletons |
|---:|---:|
| 16 | 528 |
| 28 | 1,200 |
| 53 | 1,104 |
| 60 | 10,576 |
| 65 | 240 |
| 109 | 15,192 |
| 116 | 48 |
| 171 | 7,440 |
| 246 | 1,352 |

Thus

```text
extendible skeleton/support pairs   4,017,048
primitive-ideal profile lifts   9,317,722,248.
```

Before this flag the full shell has

```text
37,680 * 3^6 * C(18,4) * 3^4
 = 6,808,396,939,200
```

profile assignments.  The six quartet phase equations supply a nominal
`3^6=729` reduction.  Empty-medium quartets impose additional, nonuniform
high-support gates, so the aggregate census reduction is slightly larger;
this flag layer remains a necessary filter, not an exclusion.

## 3. Why the remaining join has only six trits

Fix a signed skeleton and its phase-zero baseline.  Every remaining
one-slot correction is either

```text
sigma lambda(omega^u-1)
```

or `3 omega^v`.  Since

```text
lambda^2=-3 omega,
```

each correction is coefficientwise divisible by three.  Every product
between two corrections is consequently divisible by nine.  Hence, at
every lag,

```text
D(m+sum_i delta_i)
 =D(m)+sum_i(D(m+delta_i)-D(m))             (mod 9).       (2)
```

This is a lossless affine identity, not a relaxation.

After the six local flag equations are imposed, every `q_j` lies in
`ker(ell)`, which is one-dimensional over `F_3`.  Reversal conjugation
leaves six independent lag representatives.  The whole remaining modular
condition is therefore one signature in

```text
F_3^6,
```

together with the exact four-coordinate aggregate and the requirement of
exactly four high letters.

For each skeleton orbit, the verifier builds the six local lift tables,
splits the quartets into balanced groups of three, and hash-joins on

```text
(high count, six-trit signature, exact aggregate).
```

Across all 1,704 skeleton orbits it generates `21,499,626` right-half
records.  No one skeleton uses more than `41,337` right-half records or
`35,322` distinct right-half keys.

## 4. Exact symmetry recovery and detached replay

Every modular join is canonicalized again under the full exact group `G`.
There are

```text
14,443
```

full-assignment orbits.  Weighting each by `24/|Stab_G|` recovers exactly

```text
345,984
```

raw survivors.  Expanding the target around every orbit reproduces the
production target counts:

```text
15162, 15162, 13518, 13518, 14970, 14970,
15162, 15162, 19818, 19818, 14970, 14970,
15147, 15147, 19818, 19818, 14358, 14358,
14922, 15147, 15147, 14922.
```

For each full-assignment orbit representative, a detached routine expands
the two class words to all 37 physical coefficients and recomputes every
cyclic correlation directly with integer Eisenstein pairs.  It checks
origin energy, `H`-invariance, reversal conjugation, and the modulo-nine
join.  Weighting by exact orbit sizes gives:

| nonzero class correlations | raw survivors |
|---:|---:|
| 4 | 204 |
| 6 | 1,860 |
| 8 | 16,884 |
| 10 | 96,192 |
| 12 | 230,844 |

No survivor has zero bad classes.  This independently proves the shell
empty.

## 5. Reproduction and resources

Run the structural census:

```text
clang++ -std=c++20 -O3 -DNDEBUG \
  census_h4_skeleton.cpp -o /tmp/census_h4_skeleton
/tmp/census_h4_skeleton
```

Run the complete orbit/MITM certificate:

```text
clang++ -std=c++20 -O3 -DNDEBUG \
  verify_h4_skeleton_mitm.cpp -o /tmp/verify_h4_skeleton_mitm
/tmp/verify_h4_skeleton_mitm
```

Or run the pinned compile-and-replay regression:

```text
python3 -m unittest -v test_h4_skeleton_mitm.py
```

On the reference Apple Silicon run the complete verifier took `11.76 s`,
used `12,730,368` bytes maximum resident memory, and performed zero swaps.
This is far below the 16 GB project ceiling.

An additional complete `AddressSanitizer` plus
`UndefinedBehaviorSanitizer` replay produced the identical canonical
stdout hash, reported no sanitizer findings, took `39.07 s`, peaked at
`489,160,704` bytes RSS, and performed zero swaps.

Pinned SHA-256 values are:

```text
production table source included by the compressed verifier
b76c700e459cbe36318904b9c46ed40302ee50fdbf0eca71a2bbfd362b2d93ab

signed-skeleton census source
5735d18fba619590219654be788c5f5fd7d2832ae0dcf281d0ff833d35a0a918

MITM verifier source
734b3de505f313cb565cea77f6cb1ba390753bc8c030a2a9e56a1524336de26c

canonical MITM stdout
5b57f2187da536974436c1894fc1171c9e863a92d10cb3cf26770cf5cebdb97b
```

## Caveat

Shared-source caveat: this is a corroborating implementation, not a fully
source-independent certificate.  The compressed implementation includes
the audited production shell-four source to reuse its ten-letter alphabet,
target catalog, cyclotomic classes, and small exact one-slot tables.  Its
skeleton enumeration, symmetry quotient, meet-in-the-middle join,
full-assignment orbit recovery, and 37-lag replay are separate.  Agreement
of every target count and every bad-class bin is therefore a strong
implementation cross-check, but the package is not source-independent at
the alphabet/table initialization layer.
