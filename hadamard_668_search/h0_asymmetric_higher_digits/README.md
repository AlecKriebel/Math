# Asymmetric higher-digit lift of the exact h=0 profile

## Result

This folder preserves the first mechanically replayable placement witness
for the exact h=0 profile that **breaks** its class half-turn.  The witness
vanishes through placement digit 2:

```text
digit                       0  1  2  3
nonzero displayed rows      0  0  0 13
```

It is therefore a genuine asymmetric second-digit witness, but not a
third-digit witness.

It also fails the physical row front.  Its 18-coordinate labelled
row-margin aggregate is not one of the complete 1,756 catalog rows, and
detached labelled replay fails the exact zero-column-lag equation.  Thus
this result is not a Legendre pair and does not construct `H(668)`.

## Canonical slice

The exact profile has identifiers

```text
A = 1,1,2,4,4,5,1,1,2,4,4,5
B = 5,5,1,7,4,1,5,5,1,7,4,1
```

and is stabilized at profile level by the class half-turn
`j -> j+6`.  On the rank-18 first placement layer, the induced involution
splits the 36-dimensional kernel as

```text
fixed dimension       21
anti-fixed dimension  15.
```

Fix the first canonical anti coordinate

```text
y = (1,0,...,0) in F_3^15.
```

The six half-turn-odd second-digit equations then become six independent
linear equations in the 21 fixed coordinates.  Their solution space has
dimension 15.  The verifier reconstructs this slice canonically from the
profile, solves those six rows, and checks that the stored 54-trit point is
the lift of the stored 15-trit affine coordinate.

This construction is intentionally separate from
`../h0_halfturn_twists/`, which contains the full eigenspace theorem and
global twist census.

## Exact digit-3 bounded search

After composition with the 15-dimensional slice, the exact compact
`(A,Q)` model has:

```text
affine trits                    15
distinct effective phase forms 411
model variables              1,286
model constraints              860
```

A 300-second, four-worker CP-SAT run returned `UNKNOWN` after 4,340,808
branches and 177,136 conflicts.  Peak resident memory was 175,112,192
bytes.  `UNKNOWN` is only a bounded hardness observation; it is not an
exclusion and supplies no evidence that the slice lacks a digit-3 point.

## Half-turn-fixed control

For comparison, the identity half-turn slice has dimension 21 and contains
an exact digit-2 witness.  Its next digit has 11 nonzero displayed rows.
An exact reduced-CNF digit-3 diagnostic was manually interrupted after
464.11 seconds without a solver conclusion.  This is recorded as
`INTERRUPTED_UNKNOWN`, not as a timed solver result.

That control remains fixed by multiplier 64 and is diagnostic only under
the project's current multiplier audit.  The asymmetric witness above is
not half-turn fixed.

## Replay

From `hadamard_668_search/`, run:

```bash
python3 h0_asymmetric_higher_digits/verify_h0_asymmetric_higher_digits.py
```

The replay is dependency-free beyond the repository's standard Python
modules.  It reconstructs the eigenspaces and affine slice, verifies both
placement digits by symbolic and direct exact Eisenstein arithmetic,
checks the row-margin failure, and independently derives the compact model
size.
