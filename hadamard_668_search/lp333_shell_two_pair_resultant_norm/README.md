# Pair-resultant norm gate for shell-two `LP(333)`

## Status

This package does **not** construct a Legendre pair or a Hadamard matrix of
order 668, and it does not exclude any of the five shell-two profile
orbits.

It proves an exact multiplicative consequence of the three primitive
prime-167 norm equations:

> Every physical shell-two solution has the same three pair-resultant
> norms in its A and B channels.

The three keys lie in

```text
F_(167^3)^*,
```

whose order is

```text
167^3-1 = 4,657,462 = 2 * 83 * 28,057.
```

Thus the abstract key space has

```text
(167^3-1)^3 = 101,029,443,456,638,735,128
```

points.  This is a potentially strong exact join key for separately
generated A- and B-channel catalogs.  It is a consequence of the full
primitive equations, not an additional equation, so the package does not
claim a factor of this size on the actual physical candidate count.

## 1. The pair-resultant theorem

Let

```text
E = F_(167^12)
```

and write the six primitive coordinates of the two recombined channels as

```text
W_(X,r),  X in {A,B}, r=0,...,5.
```

The promoted primitive-unit theorem proves that every one of these
coordinates is nonzero on all 84 formal shell-two images.  The ratio

```text
R_r = W_(B,r) / W_(A,r)
```

is therefore defined.  The three paired norm equations are equivalent to

```text
R_(r+3) = -R_r^(-167^9),       r=0,1,2.              (1)
```

Multiplying within one pair gives

```text
R_r R_(r+3) = -R_r^(1-167^9).                        (2)
```

Put

```text
N = Norm_(E/F_(167^3)),
N(x) = x^(1+167^3+167^6+167^9).
```

The extension degree is four, so `N(-1)=1`.  Moreover,

```text
(1-167^9)(1+167^3+167^6+167^9)
    = 0 mod 167^12-1.
```

Applying `N` to (2) gives

```text
N(R_r R_(r+3)) = 1.                                  (3)
```

Define the intrinsic pair-resultant keys

```text
nu_(X,r) =
  N(W_(X,r) W_(X,r+3)) in F_(167^3)^*.               (4)
```

Then every physical solution must satisfy

```text
nu_(A,r) = nu_(B,r),          r=0,1,2.               (5)
```

The product of the three equalities is the weaker total-resultant norm
identity.  Keeping the three pair keys separately is essential.

Equivalently, `nu_(X,r)` is the determinant over `F_(167^3)` of
multiplication by the pair coordinate
`W_(X,r)W_(X,r+3)` in `E`.  This makes (5) independent of a choice of
power basis.

## 2. Exact character form

The three factors `2`, `83`, and `28,057` are distinct primes.  Equality
in `F_(167^3)^*` is therefore equivalent to equality of all three
multiplicative-character projections.  For

```text
d in {2,83,28057},
```

the order-`d` projection of (4) can be computed without first materializing
the relative norm:

```text
chi_d(nu_(X,r))
  = (W_(X,r) W_(X,r+3))^((167^12-1)/d).              (6)
```

Hence (5) is exactly the following nine small-root equalities:

```text
chi_d(W_(A,r)) chi_d(W_(A,r+3))
  = chi_d(W_(B,r)) chi_d(W_(B,r+3)),

r=0,1,2,  d=2,83,28057.                              (7)
```

This form is suitable for staged hash joins: first a three-bit quadratic
key, then three order-83 labels, then three order-28,057 labels.

## 3. Exact audit on every physical shell-two orbit

The 84 formal shell-two images split into ten physical lift orbits.  As in
the promoted primitive-unit package, they are represented by:

```text
five canonical A seeds,
five canonical B seeds,
five A-star A seeds.
```

Thus 15 seed/channel alphabets suffice.  The exporter reconstructs every
local physical class alphabet directly from the promoted exact
certificates.  It then derives a degree-12 power basis of `E` from the
repository's 36-coordinate ambient field.  Every exported element is
reconstructed in the ambient field before it is accepted.

The compiled verifier searches only for finite witness sets.  Once a
character value is first seen, it retains the twelve local class choices;
after the image audit, every retained witness is evaluated again exactly.
The search order is deterministic.  Completeness claims come from explicit
witnesses for every value, not from a timeout or sampling probability.

### Complete marginal images

For every one of the 15 cases, every pair `r=0,1,2`, and every character
order `d=2,83,28057`, the physical alphabet attains **all** `d` possible
values.  Per case, the exact witness targets are:

```text
d=2:          3*2     =      6 /      6
d=83:         3*83    =    249 /    249
d=28057:      3*28057 = 84,171 / 84,171.
```

The largest audit used 4,843,905 deterministic trial assignments across
all 15 cases, 547.03 seconds, and about 4.05 MB maximum resident memory.

### Full affine dimension of each triple image

For each of the three prime character orders and every one of the 15
cases, exact witnesses show that the three pair-character coordinates
have affine rank three over `F_d`.  Thus no nonzero affine-linear
character relation collapses the three keys on a physical shell-two
alphabet.

This does **not** prove that the complete triple image is all of
`F_d^3` for `d=83` or `28,057`.

### Negative small-character audit

The complete joint six-factor character image is:

```text
2^6 = 64 / 64   for d=2,
3^6 = 729 / 729 for d=3
```

in every seed/channel case.  Single-factor quadratic and cubic characters
therefore yield no restriction.  The useful information is the A/B
coupling (7), not a one-channel local obstruction.

The six-factor product character also attains every value for each
`d=2,83,28057` in every case.  This independently confirms that the
weaker total-resultant norm is nonconstant, but the three pair keys retain
strictly more information.

## 4. What the result does and does not buy

The positive search consequence is exact: any separately generated A and
B channel candidates can be joined on the triple

```text
(nu_0,nu_1,nu_2).
```

At the unrestricted unit-spectrum level, each of the three relative norm
maps is surjective, so the aggregate gate has exact index
`(167^3-1)^3`.  On the sparse physical alphabets, however, key
distributions and correlations can be highly nonuniform.  The audit proves
full marginals and full affine rank, not uniformity and not a
`10^20` physical reduction.

No profile orbit is excluded by any individual character-coordinate
projection.  The next operational question is whether exact
margin-conditioned or 12-trit slice catalogs contract enough that the
triple key can be materialized and joined.  A useful next experiment must
measure complete slice distributions or exact A/B intersections; finding
more isolated character witnesses would add no information.

## 5. Independent arithmetic checks

The pure-Python theorem verifier checks:

1. the pair formula (1) and all three original primitive residuals;
2. the norm-exponent identity;
3. all three pair-resultant equalities on four exact torus fixtures;
4. the character decomposition for `2`, `83`, and `28,057`;
5. a negative control showing the norm equality is not an identity on
   arbitrary unit spectra.

The compiled field bridge independently compares 45 deterministic product
and character probes against the repository's original 36-coordinate
field implementation.  All 45 agree exactly.

## 6. Honest conclusion

The pair-resultant norm gate is a genuine new structural lemma and a
potentially high-value search architecture.  It compresses each of the
three large paired field equations into a small exact catalog key.

It is not yet evidence of convergence to a Legendre pair: all marginal
character images are full, no shell-two orbit is removed, and the
margin-conditioned triple-key distributions have not yet been enumerated.
The next gate is operational rather than algebraic—show a strong exact
contraction on complete structured slices, or stop treating this lane as a
headline search.
