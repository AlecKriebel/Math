# Half-turn placement algebra of the exact h=0 profile

## Result

The exact profile

```text
A = 1,1,2,4,4,5,1,1,2,4,4,5
B = 5,5,1,7,4,1,5,5,1,7,4,1
target = (2,-2,-4,-2)
```

repeats after six nonzero cyclotomic classes.  Its first physical placement
layer has 54 trits and affine dimension 36.  The class half-turn splits its
translation space exactly as

```text
V = V+ direct-sum V-,          dim(V+),dim(V-) = 21,15.
```

In coordinates adapted to this splitting, the 18 active second-placement
equations become:

```text
12 half-turn-even quadrics  F_i(x) + G_i(y) = 0,
 6 half-turn-odd equations  x^T B_i y + l_i(y) = 0,

x in F3^21, y in F3^15.
```

Every `21 x 15` block `B_i` has full column rank 15.  Of the 364
projective combinations of the six blocks, 361 have rank 15 and the three
exceptions have ranks 14, 12, and 11.  This gives an exact count

```text
205,901,492,005,503
```

for the common zero set of the six odd equations.  The count is close to
the generic `3^30` scale, so the decomposition explains the geometry but
does not by itself contract the complete second-digit search.

## Global fiber-permutation twists

For a permutation `pi` of the three quotient positions, impose on every
opposite class pair

```text
W_(j+6)(s,q) = W_j(s,pi(q)).
```

The permutation may be chosen independently in the two channels, giving
`6 x 6 = 36` structured families.  The action on every active placement
trit is affine, so the first layer can be classified exactly:

| first-layer outcome | families |
|---|---:|
| inconsistent | 17 |
| affine dimension 9 | 18 |
| affine dimension 21 | 1 |

Every one of the 18 dimension-nine families was then exhausted through all
`3^9 = 19,683` points.  None survives the complete second placement digit.
The only dimension-21 family is the identity/identity pairing.

The identity pairing fixes both full words under multiplication by 64
modulo 333.  Together with the existing order-three multiplier, this is the
order-six subgroup ID8.  That exact full-word family is independently
excluded by the recent public multiplier classification:

<https://arxiv.org/abs/2607.20765>

The public result is used only to interpret the remaining identity family;
the 35 nonidentity outcomes and all dimension-nine second-digit exclusions
are reconstructed locally.

## Scope

This is a complete exclusion of one natural collection of twisted
half-turn constructions for one exact order-three profile.  It is not an
exclusion of the profile, an unrestricted Legendre-pair search, or a
Hadamard matrix of order 668.  A viable lift must break the half-turn in a
less uniform way.

## Verification

From `hadamard_668_search/` run:

```text
python3 h0_halfturn_twists/verify_h0_halfturn_twists.py
```

The verifier reconstructs the first affine system, derives the quadratic
forms from the exact Eisenstein phase terms, checks the eigenspace action,
and performs the finite `18 * 3^9 = 354,294` point census.
