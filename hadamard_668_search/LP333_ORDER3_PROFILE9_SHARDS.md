# Primitive-nine profile ideal across all 22 LP(333) shards

## Status

The exact primitive-nine profile ideal is a strict obstruction on the 22
profile assignments retained by the characteristic-37 checkpoint: every one
of those assignments fails.  It does **not**, however, eliminate any of the
22 aggregate row-sum shards.

For each shard there is now an explicit alternative pair of twelve-profile
words satisfying simultaneously:

```text
the four-coordinate aggregate target,
total Eisenstein profile norm 54,
six opposite-class local mod-three conditions,
all twelve displayed primitive-nine profile ideal tests.
```

The 22 assignments are pinned in
`verify_lp333_order3_profile9_shards.py`.  A dependency-free replay checks
all constraints from their definitions and independently reconstructs the
exact periodic correlation target table for every assignment.

This is a complete profile-level survival result.  It is not a labelled
nine-row lift, an `LP(333)`, or a Hadamard matrix of order 668.

## 1. The finite layer

Each nonzero order-three column class has one of ten normalized residue
profiles

```text
(p_0,p_1,p_2),             p_0+p_1+p_2=3.
```

There are 24 profile variables: twelve for channel `A` and twelve for
channel `B`.  The earlier exact reductions impose:

1. one of the 22 aggregate targets from the pinned 1,756-row catalog;
2. total Eisenstein norm 54;
3. equality of the local mod-three signatures on each of the six
   opposite-class pairs.

For a profile tuple, let

```text
D_t =
  sum_c [a(c+t) conjugate(a(c))
        +b(c+t) conjugate(b(c))]
  -167 delta_(t,0)
```

be its order-three row Fourier correlation.  Exact primitive-nine
equidistribution requires, on every nonzero column class,

```text
D_t in 3(1-omega) Z[omega].
```

In coordinates `D_t=u+v omega`, this is the elementary exact test

```text
u = 0 mod 3,
v = 0 mod 3,
u/3+v/3 = 0 mod 3.
```

Reversal pairs the twelve displayed tests.  The verifier deliberately
checks all twelve rather than relying on a redundancy count.

## 2. Complete shard result

A finite-domain construction produced one profile assignment for every
aggregate target.  Every returned tuple was then detached from the search
solver and replayed using exact integer and Eisenstein arithmetic.

The resulting certificate inventory is:

```text
aggregate shards                         22
profile assignments                      22
aggregate and energy checks              22
opposite-class local checks              132
displayed profile ideal tests             264
reconstructed 13-row target tables        22
profile-level shard exclusions             0
labelled lifts asserted                     0
```

Thus the new ideal test removes all 22 *previously pinned assignments* but
each of their aggregate shards has at least one different profile
assignment that passes.

## 3. Certificate hashes

The compact SHA-256 hashes are:

```text
profile witness corpus
92fbf448260334f3e4a9b7d1cfb82046d3cb5043721bd5fcb09fbcb4aeaab43f

exact Eisenstein correlation tables
27a3fc0c11e745e05e3da8ca273cde3535419009e78cb2ce34ca83fc074b1a78

reconstructed periodic target tables
e7d395500053eeb4346260d545affbb1baea35f01a6793ef48d6b3a3ee9c8628
```

These hashes pin three logically distinct objects: the assignments, their
profile correlations, and the integer target tables that any later labelled
lift must realize.

## 4. Consequence for the next search

The profile ideal is useful pruning, but aggregate-level branching should
not treat it as an exclusion layer.  The next exact step must lift one or
more of these 22 profile assignments to actual nine-row class words and
enforce their reconstructed `12 by 3` correlation targets.

The existing trit parameterization is the natural representation for that
step: after profiles are fixed, the six-digit modular primitive-nine system
is affine over `F_3`, while exact row margins and the integral target table
remain as the finite realization constraints.

## Reproduction

```text
python3 verify_lp333_order3_profile9_shards.py
python3 -m unittest -v test_lp333_order3_profile9_shards.py
```

On the reference replay, the verifier used about `27 MB` peak RSS, recorded
zero swaps, and completed in under one second.
