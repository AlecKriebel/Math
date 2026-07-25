# Affine-in-class half-turn obstruction for the exact `h=0` profile

## Result

For each binary channel independently, choose

```text
(epsilon,a,b) in F_3^* x F_3 x F_3.
```

On each opposite cyclotomic-class pair `j,j+6`, impose the labelled support
relation

```text
W_(j+6)(s,q) = W_j(s, epsilon*q + a*j + b),   j=0,...,5.
```

This is a finite family of `18^2=324` paired constructions.  When `a=0`,
the map is independent of `j`; because every permutation of `F_3` is
affine, those 36 cases are exactly the previously classified global
fiber-permutation twists.  The other 288 cases are new class-dependent row
shears.  They are not invariance under a single affine map of the CRT
coordinates: a global affine transport has the same row permutation in
every cyclotomic class, whereas a nonzero `a` changes it with `j`.

The exact census is:

| first placement layer | all families | new nonzero-slope families |
|---|---:|---:|
| inconsistent | 161 | 144 |
| affine dimension 9 | 162 | 144 |
| affine dimension 21 | 1 | 0 |

All `162*3^9 = 3,188,646` points in the dimension-nine families were
exhausted through the complete second placement digit.  None survives.
The sole dimension-21 case is the identity/identity relation, which is the
fixed order-six multiplier branch already separated in the half-turn
theorem.

Consequently every one of the 323 nonidentity affine-in-class twists is
excluded: 161 at the first digit and 162 at the second digit.  In
particular, all 288 genuinely class-dependent row shears are excluded
locally without invoking the recent external multiplier classification.

## Verification

From `hadamard_668_search/` run:

```text
python3 h0_affine_class_twists/verify_h0_affine_class_twists.py
```

The verifier reconstructs all 324 affine systems from the exact phase
equations, checks the old 36-family theorem as its zero-slope slice, and
directly evaluates every point in all 162 nine-dimensional second-digit
families.  There is no optimizer, randomized step, timeout, or negative
solver status in the certificate.

## Scope

This is a complete obstruction for one new structured lift family of one
exact order-three profile.  It does not exclude the profile, construct a
Legendre pair of length 333, or construct a Hadamard matrix of order 668.
A viable lift must use a more irregular class-dependent placement rule.

## Stronger quadratic-class extension

### Theorem

The companion verifier

```text
python3 h0_affine_class_twists/verify_h0_quadratic_class_twists.py
```

allows an arbitrary shift function `f(j mod 3)`:

```text
W_(j+6)(s,q) = W_j(s, epsilon*q + f(j mod 3)).
```

Write a channel parameter as `(epsilon;f_0,f_1,f_2)`.  Every function on
`F_3` is a quadratic polynomial, so there are 54 choices per channel and
`54^2=2,916` paired families.  Exactly 324 have both `f_A` and `f_B`
affine-linear, including the earlier affine-class theorem.  The other
**2,592 paired families are the genuinely new non-affine-class cases**.
Their exact outcomes are:

| failure stage | new non-affine-class families |
|---|---:|
| inconsistent at digit 1 | 1,293 |
| dimension 9, empty at digit 2 | 1,296 |
| exceptional dimension 15, empty at digit 2 | 1 |
| exceptional dimension 21, empty at digit 3 | 2 |

Thus every one of the 2,592 new cases is locally excluded.  Together with
the affine subfamily, all 2,915 nonidentity quadratic-class twists are
excluded no later than digit three.  The sole remaining local control is
the identity/identity order-six multiplier branch.  This is a theorem only
about the displayed finite family on the pinned `h=0` profile.

The exact census has 1,454 first-digit inconsistencies and 1,458
dimension-nine systems with no second-digit point.  One exceptional
dimension-15 system reduces through six hidden affine equations to
dimension nine and also has no second-digit point.  Two nonidentity
dimension-21 systems reduce to dimension 15 and have exactly 24
second-digit points apiece.  All 48 fail the next digit—each in at least
eight displayed equations—and none belongs to the exact row-margin
catalog.  In parameter notation, the exceptional families are:

```text
A=(1;0,0,1), B=(1;2,2,1):  24 digit-2 points,
A=(1;0,0,2), B=(1;1,1,2):  24 digit-2 points.
```

For each family, all `3^15=14,348,907` reduced points were enumerated.
The verifier then replayed every one of the 48 survivors in all 20 exact
displayed Eisenstein equations.  At digit three, each survivor fails in
between 8 and 16 displayed rows.  Separately, it reconstructed both
twelve-word binary channels, formed each complete 18-coordinate row
aggregate, and checked it against all 1,756 rows of the exact row-margin
catalog; none is a member.

Thus all 2,915 nonidentity quadratic-class twists are locally excluded no
later than digit three.  This stronger verifier is dependency-free and
exhausts `57,415,311` family-point incidences after the first-layer rank
census.
The two exception parameters, deterministic representative placements,
full replay scope, and corpus hashes are pinned in
`quadratic_class_twists_certificate.json`.  The exhaustive work count is
`57,415,311` **family-point incidences**; affine spaces belonging to
different control laws can overlap, so this is not asserted to be the
number of distinct placements.

### Scope boundary

The exact digit-three replay is only the next lambda-adic digit of the 20
displayed phase equations.  The row-margin replay is complete for the
1,756-word row-axis catalog.  These statements do not exclude any
placement outside the 2,916-family ansatz, the whole `h=0` profile, the
order-three ID3 lane, `LP(333)`, or `H(668)`.
