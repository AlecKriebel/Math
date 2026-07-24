# LP(333) order-three trit lift

## Status

The upper half of the primitive-nine labelled lift has an exact trit
linearization.  For the pinned catalog-row-695 profiles, 54 placement trits
are cut by a rank-18 affine system over `F_3`, leaving affine nullity 36
before the exact row-margin and correlation equations are imposed.

A smaller CP model using this reduction found a second fully labelled
certificate for the same profiles.  The assignment was independently
replayed against all 222 primitive-nine equations and the four exact
row-direction equations.

This is a state reduction and one certified profile lift.  It excludes no
catalog row and is not an `LP(333)` or a Hadamard matrix of order 668.

## 1. One trit per active residue

Write a row as

```text
r = s + 3q,              s,q in {0,1,2}.
```

For a fixed normalized class profile, let `p_s` be the number of selected
rows in residue `s`.  If `p_s` is zero or three, its placement is fixed.  If
`p_s` is one or two, define

```text
u_s = 1_{q=2} - 1_{q=1}  in F_3.
```

This is a bijective encoding:

```text
p_s=1:  u=0 -> {0},    u=1 -> {2},    u=2 -> {1}
p_s=2:  u=0 -> {1,2},  u=1 -> {0,2},  u=2 -> {0,1}.
```

Thus a class profile has exactly one independent trit for every entry equal
to one or two.  Exhausting all ten compositions of three verifies that the
trit encoding produces every one of the

```text
binom(3,p_0) binom(3,p_1) binom(3,p_2)
```

placements exactly once.

## 2. Exact upper linearity

In `R=F_3[pi]/(pi^6)`, with `pi=1-zeta_9`, Frobenius gives

```text
(1-pi)^(s+3q) = (1-pi)^s (1-pi^3)^q.             (1)
```

Modulo `pi^6`, the three values of the second factor differ by

```text
0, -pi^3, +pi^3
```

from the `q=0` value.  Therefore jet digits zero through two depend only on
the fixed profile, while digits three through five are affine-linear in the
placement trits.

All placement differences lie in `I=pi^3 R`, and `I^2=0`.  Hence their
pairwise products disappear from the autocorrelation identity.  After a
lower profile passes digits zero through two, the complete upper
autocorrelation condition is an affine system over `F_3`; no relaxation is
being made.

The dependency-free verifier checks this locally rather than assuming it:

```text
352 complete local class assignments
54 upper placement differences
54^2 = 2,916 square-zero products.
```

## 3. Exact rank for the pinned profiles

The row-695 profile tuple has 54 active placement trits.  Evaluating the
three upper digits on the 13 physical invariant classes gives 39 displayed
coordinates.  Exact row reduction over `F_3` gives

```text
affine rank    = 18
affine nullity = 36.
```

The original row-695 certificate satisfies this system.  These rank and
nullity values are claims about this pinned profile tuple only; they are not
asserted for every catalog lift.

## 4. Reduced model and replayed certificate

The trit model retains exact row margins and the four integer
row-direction correlations.  For the pinned profiles its exact size is

```text
placement trits       54
actual word bits     216
lag signatures        96
affine quotients       18
total variables       384
total constraints      64.
```

A bounded one-worker run returned:

```text
A = (7,261,448,41,131,131,273,100,41,145,37,76)
B = (388,74,352,161,88,140,41,289,73,35,7,322).
```

These are normalized three-subset masks.  Dependency-free replay verifies:

```text
24 labelled class words
18 exact row margins
4 exact integer row-direction correlations
37 physical column lags x 6 jet digits = 222 equations over F_3.
```

On the checkpoint machine, the bounded solver run took about 3.4 solver
seconds and stayed below 100 MB resident memory.  A timeout or `UNKNOWN`
status is never interpreted as mathematical evidence.

## Reproduction

Dependency-free theorem and certificate replay:

```text
python3 verify_lp333_order3_trit_lift.py
python3 -m unittest -v test_lp333_order3_trit_lift.py
```

Optional bounded reconstruction with the repository solver environment:

```text
../.venv/bin/python search_lp333_order3_trit_lift.py \
  --time-limit 10 --workers 1
```
