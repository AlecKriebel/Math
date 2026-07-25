# Full quadratic rank-two conic pilot on canonical `h=0` gauge 07

> **Scope correction, 2026-07-25.**  `orbit-07` below names the frozen
> canonical representative gauge, not the whole 12-image classification
> orbit.  The feature law is not known to be covariant under the
> 24-element action.  This certificate exhausts one gauge only and makes
> no outcome claim for its 11 other distinct action images.  See
> `../h0_witt_conic_rank_two_full_18/ACTION_NONINVARIANCE_CERTIFICATE.json`.

## Result

The complete independent-channel quadratic extension of the Witt-conic
center law has been exhausted for the exact dense-shell canonical gauge

```text
orbit-07 = 0x86b13a0388d98a5e.
```

Every center in the family has the form

```text
t_X(j,s) = P_X(x,s,p_X,j(s)) + h_j Q_X(x,s,p_X,j(s)),
x = j mod 3,
h_j = +1 for j<6 and -1 for j>=6,
u_X(j,s) = -p_X,j(s)t_X(j,s),
```

where all four polynomials

```text
P_A, P_B, Q_A, Q_B
```

are arbitrary total-degree-at-most-two polynomials in `(x,s,p)` over
`F_3`.  Thus the two opposite-correction coefficient rows `Q_A,Q_B` are
completely arbitrary: their `2 x 10` coefficient matrix has rank at most
two, and every rank-zero, rank-one, and rank-two correction in this
quadratic antipodal feature space occurs.

This is the lossless rank-two closure of the earlier shared-shape
rank-one law **within the stated quadratic antipodal feature space**.  It
does not include degree-three or more general non-antipodal center laws.

The exhaustive result is:

```text
distinct first-layer physical placements       4,782,969 = 3^14
maximum active second-digit equations                  17 / 18
exact second-digit survivors                                0
two-consecutive-digit survivors                             0
margin-compatible second-digit lifts                        0
```

There are exactly five `17/18` near misses.  They fail, respectively,
physical rows

```text
2, 3, 4, 10, 16,
```

one point per row.  None of the five has a row-margin word in the exact
1,756-word catalog.

This excludes the complete delimited family for the chosen `orbit-07`
canonical gauge.  It does not transfer to the other 11 action images and
is not an exclusion of the full 36-dimensional placement layer,
`LP(333)`, or `H(668)`.

## Why `orbit-07`

The completed 18-profile lift scan gives `orbit-07`:

- 96 compatible catalog rows, tied for the maximum;
- 405,962,790,888,377,068,200 accepted raw margin assignments, the
  second-largest transfer mass;
- the smallest structured six-zero fiber among the 18 profiles; and
- after the new rank-two linear reduction, a 14-dimensional physical
  family, the smallest dimension found among the 18 candidates.

This combination makes it a strong margin-aware profile and the only
candidate for which the full quadratic rank-two pilot is exceptionally
cheap.

## Exact reduction before enumeration

There are 40 raw polynomial coefficients.  Evaluation on the 54 active
local centers has rank 32.  The first-placement equations have rank 18 on
this image, so:

```text
first-layer coefficient solution dimension       40 - 18 = 22
coefficient evaluation kernel dimension          40 - 32 =  8
distinct physical first-layer dimension          22 -  8 = 14
```

Consequently the `3^22 = 31,381,059,609` valid coefficient descriptions
fall into uniform classes of `3^8 = 6,561`, leaving exactly
`3^14 = 4,782,969` physical placements.  No coefficient descriptions are
sampled and no duplicate physical points are enumerated.

Relative to the full 36-dimensional first-placement affine space, the
family covers the exact fraction

```text
3^14 / 3^36 = 1 / 31,381,059,609.
```

The half-turn sign separates the even base law `P_X` from the odd
correction `Q_X`.  Row reduction then quotients the eight-dimensional
evaluation kernel.  Finally, the 18 ambient quadrics are restricted
symbolically to the resulting 14-dimensional affine space before the
finite enumeration.

The upper tail of the exact score distribution is:

| satisfied equations | placements |
|---:|---:|
| 14 | 678 |
| 15 | 116 |
| 16 | 24 |
| 17 | 5 |
| 18 | 0 |

The complete histogram, stream hashes, all five near-miss replays, and one
direct physical replay at every attained score are pinned in
`rank_two_orbit07_certificate.json`.

## Verification

From this folder run:

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 \
PYTHONDONTWRITEBYTECODE=1 \
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  verify_witt_conic_rank_two.py
```

The verifier reconstructs the canonical-gauge profile from the frozen complete
classification, checks the selection data against the frozen 18-profile
scan, re-derives the conic identity and all finite-field ranks, restricts
the quadrics, exhausts all `3^14` physical placements, directly replays
the score representatives and near misses, and compares the result with
the pinned certificate.

The final verification run took 11.61 seconds, 10.75 user seconds, and
61,308,928 bytes maximum resident memory on the research machine.  It was
single-core under the displayed thread limits and stayed far below the
8 GB pilot ceiling.

The certificate semantic hash is

```text
cc272f74521b7cf58216b1971f8a2659b1eb1068a295b6c7552cb3c15c778dc8
```
