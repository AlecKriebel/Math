# Minimum half-turn breaking for the exact `h=0` profile

## Result

The exact dense-shell profile has a half-turn on its 27 opposite-class
placement pairs.  After the first placement digit, its antisymmetric
translation space is a ternary linear code

```text
C- <= F_3^27,       [length,dimension,minimum distance] = [27,15,4].
```

Its complete weight enumerator begins

```text
A_0=1, A_4=6, A_5=14, A_6=98, ...
```

and there are exactly six minimum words, or three projective minimum
directions.  These are the smallest possible **first-placement-digit**
antisymmetric departures from the publicly excluded full-word half-turn
family.

Fixing each of the six minimum words makes the six half-turn-odd
second-digit equations linear in the 21 symmetric coordinates.  Exact
enumeration of the resulting affine slices gives:

| minimum anti word | odd rank | remaining dimension | digit-two points |
|---:|---:|---:|---:|
| 0 | 6 | 15 | 22 |
| 1 | 5 | 16 | 87 |
| 2 | 6 | 15 | 22 |
| 3 | 5 | 16 | 87 |
| 4 | 6 | 15 | 24 |
| 5 | 6 | 15 | 24 |

All 266 points were replayed through the exact Eisenstein coefficients.
None belongs to any of the 72 exact row-margin fibers.  None survives the
third placement digit; the best points leave six nonzero digit-three rows.

The next anti-weight shell is also complete.  It contains 14 words, or
seven projective directions.  The seven representative slices contain 196
digit-two points, hence 392 across both signs.  Again, none belongs to an
exact row-margin fiber and none survives digit three; their best
digit-three defect is seven rows.

This is a complete exclusion of the **anti-weight four and five
construction families** for this one profile.  It is not an exclusion of
the profile, `LP(333)`, or `H(668)`.

## Exact row-margin precursor count

The symmetric anti-weight-zero fiber contains no exact physical row-margin
point.  At the minimum positive weight, exactly one of the three
projective directions reaches a row-margin fiber.  For each of its two
signs, precisely 7,346 first-digit placements reach target 34.  The
corresponding second-digit slice has 87 points, but the two sets are
disjoint.

This count is obtained by splitting the 27 natural pair coordinates into
six row-margin blocks of sizes

```text
3,4,6,4,4,6.
```

The symmetric eigenspace is a ternary `[27,21]` code with a six-row parity
check.  Each block is enumerated locally and the six syndrome
distributions are joined exactly in `Z[F_3^6]`.  A pinned labelled
placement independently replays target 34.

## Why the split is useful

For paired placement phases, write the symmetric and antisymmetric
coordinates as `x` and `y`.  The elementary identity

```text
omega^(x+y) + omega^(x-y)
  = 2 omega^x,  if y=0,
  =  -omega^x,  if y is nonzero
```

shows that the trivial-character/row-margin layer sees the support of the
antisymmetric word but not its sign.  The nontrivial second-digit layer
then restores the signs through six bilinear equations.  This is the
support-and-sign decomposition used by the finite census.

## Verification

The verifier requires NumPy and uses exact small integer arithmetic:

```text
../tmp/hadamard-env/bin/python \
  hadamard_668_search/h0_minimal_anti_code/verify_h0_minimal_anti_code.py
```

It reconstructs the profile and both half-turn eigenspaces, exhausts all
`3^15` antisymmetric codewords, exhausts the six minimum-word slices,
exhausts all seven projective weight-five slices, replays every digit-two
point directly, tests the exact row-margin corpus, and records every
digit-three residual histogram.  It also performs the exact
`F_3^6`-syndrome row-margin count.  Its semantic hash is

```text
2deaa893bb4e6e2f1afa218ae7a1ff8e6d06a036d89cbfd711fe3868bfbfaf11
```

Peak working memory is well below 1 GB on the 16 GB host.
