# Exact full-LP order-three profile zero gate

## Status

The 22 profile tuples retained by the primitive-nine ideal audit should not
be lifted through their 54 placement trits.  Every one already fails a
stronger, exact necessary condition for a full `LP(333)`: its order-three
profile correlation must be zero on every column class.

The same gate excludes two closely related fixed profiles:

1. the original profile of the two labelled modular certificates;
2. ideal-witness 8, which lies in row 695's aggregate shard and whose
   phase-transfer intersection contains catalog row 695.

This closes 22 **fixed profile assignments**, not any of the 22 aggregate
row-sum shards.  A different profile tuple in any shard may still pass the
zero gate.  No `LP(333)` or `H(668)` is constructed or excluded.

The equation itself is the standard full Eisenstein/order-three Fourier
channel.  The new finite result here is its exact audit on the recently
constructed 22-witness corpus and on row 695.

## 1. Why a full Legendre pair forces zero

Let `X_A,X_B` be the plus supports of two length-333 sign sequences with
sum one.  Both supports have size 167.  At a nonzero lag, if `I` is their
combined plus-support intersection, then

```text
PAF(A)+PAF(B) = 4 I - 4(167+167) + 2*333
              = 4 I - 670.
```

The Legendre-pair target `-2` is therefore equivalent to

```text
I=167.                                                   (1)
```

At the zero lag the raw intersection is 334; subtracting the origin target
167 again leaves 167.  Consequently, in the `C_9 x C_37` coordinates, the
nine row-lag coefficients at every fixed column lag must be

```text
(167,167,167,167,167,167,167,167,167).                  (2)
```

If `omega` is a primitive cube root, the order-three Fourier coefficient of
(2) is zero.  The profile correlation `D_t` in
`LP333_ORDER3_PROFILE9_IDEAL.md` is exactly this coefficient, computed
before any within-residue placement:

```text
D_t =
  sum_c [a(c+t) conjugate(a(c))
        +b(c+t) conjugate(b(c))]
  -167 delta_(t,0).
```

Thus every full `LP(333)` necessarily satisfies

```text
D_t=0                         on all 13 column parts.    (3)
```

Equation (3) is only a necessary profile condition.  Passing it would not
by itself solve the placement or full-correlation problem.

## 2. Why the primitive-nine ideal was not enough

The earlier profile ideal requires

```text
D_t in 3(1-omega) Z[omega].                             (4)
```

Condition (4) says precisely that the three primitive-nine target values
reconstructed from the profile are integral.  Those values need not all
equal 167.  The full Legendre equation requires the special case

```text
D_t=0,
reconstructed target=(167,167,167).                     (5)
```

Hence (3) is strictly stronger than the successful ideal audit.  A
primitive-nine phase-frame search on a tuple that fails (3) cannot possibly
survive the final `LP(333)` gate, irrespective of its 54 placement phases.

## 3. Exact corpus result

All 22 ideal-compatible profile tuples were replayed with integer
Eisenstein arithmetic.  Their numbers of nonzero moments among the twelve
nonzero column classes are:

```text
nonzero classes    fixed profile tuples
10                 1
12                21
```

There are 262 nonzero class moments in total.  Every tuple has zero origin
moment and passes the earlier ideal test, so this is a strict strengthening
rather than a replay of an old failure.

The compact exact certificate hashes are:

```text
22 ideal-compatible profile tuples
d0e496d2a2b01ed5432e4ff89c2a306a778a52cac08cebd22aa60292588a9060

original row-695 profile
e22de237bf4a6e3b61d7bd31aff2bad9d7126fd8739b5ab503f75ca52c758621
```

For the original catalog-row-695 profile and its same-shard witness:

```text
aggregate shard target                 (1,-1,2,-2)
matching ideal-witness index            8
original profile nonzero classes       12
ideal-witness-8 nonzero classes         12
```

The verifier also reconstructs the full exact correlation table of the
original labelled row-695 certificate and checks that its order-three
moments agree entry-for-entry with the profile calculation.

## 4. Consequence for the search

Do not run a ternary phase lift on any of these 22 fixed tuples.  The next
finite problem is instead:

1. enumerate or solve for profile tuples satisfying the aggregate target,
   norm, opposite-class conditions, and exact `D_t=0`;
2. only for a zero-moment survivor, build the 54-trit phase-frame and
   cross-fiber lift;
3. replay all 333 correlations and the order-668 matrix before any success
   claim.

An exclusion of one fixed tuple is not an exclusion of its aggregate shard.

## Reproduction

```text
python3 verify_lp333_order3_profile_zero_gate.py
python3 -m unittest -v test_lp333_order3_profile_zero_gate.py
```

Both commands use exact arithmetic and the Python standard library only.
