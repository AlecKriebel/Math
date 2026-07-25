# LP333 shell-two physical-margin lift audit

## Status

This checkpoint materially narrows the five exact two-high (`n_9=2`)
profile charts, but it does **not** produce a Legendre pair of length 333 or a
Hadamard matrix of order 668.

The main exact result is that the physical row-margin gate has a previously
unused two-stage lambda-adic structure:

```text
first correlation lift                         dimension 36
six independent margin digit-3 affine rows    dimension 30
six margin digit-4 quadrics                    next physical gate
```

All `72+72+72+96+93=405` compatible catalog targets survive the affine
rank-six layer.  The following structured-retraction classification is
complete:

| profile | maximum retraction dimension after the margin cut | retracting four-spaces per target |
|---|---:|---:|
| `h2-222222-0` | 4 | 6 |
| `h2-422220-0` | 3 | 0 |
| `h2-422220-1` | 3 | 0 |
| `h2-422220-2` | 3 | 0 |
| `h2-422220-3` | 4 | 86 |

No five-dimensional subspace of the six structured correlation forms
retracts on any physical target chart.  The count above exhausts all

```text
[6 choose 4]_3 = 11,011
```

four-dimensional subspaces, not merely the fifteen coordinate subsets.
The maximum-three statements use the complete absence of a four-space plus
explicit coordinate three-space retractions on every target.

The next six margin equations are exact quadrics.  Their polar ranks are
target-independent:

| profile | six margin digit-4 polar ranks |
|---|---|
| `h2-222222-0` | `8,8,7,9,6,8` |
| `h2-422220-0` | `9,9,6,7,9,6` |
| `h2-422220-1` | `9,11,6,5,6,9` |
| `h2-422220-2` | `9,6,7,7,9,8` |
| `h2-422220-3` | `8,9,6,7,8,10` |

Despite those low individual ranks, their joint polar radical is zero on
all five profiles.  Exhausting all 364 projective five-hyperplanes finds no
five-form quadratic retraction for any of the 405 targets.

## 1. Why the first margin row occurs at digit 3

For one active residue fiber, augmentation contributes

```text
3 epsilon omega^u.
```

Because `3` is a unit times `lambda^2`, and because the signed augmentation
is fixed by the profile, digits zero through two of the difference between
any placement and a compatible target vanish automatically.  Using

```text
omega^u = 1-u lambda                    (mod lambda^2)
```

shows that digit 3 is affine in the placement trits.  Pulling it back to the
36-dimensional first-correlation chart gives six independent equations on
every profile.  All 405 augmented systems have rank `6/6`, hence every
target leaves a 30-dimensional parallel affine chart.

The next expansion term

```text
binom(u,2) lambda^2
```

makes margin digit 4 quadratic.  Direct quadratic interpolation is checked
against detached exact Eisenstein evaluations, and the polar matrices agree
across all parallel targets.

## 2. The directed origin is two digits late in a physical search

There is an exact group-ring identity

```text
E1(0) + 3 sum_(j=0)^11 E1(C_j)
    = E1 evaluated at the trivial column character.
```

The right side is zero for an exact compatible row-margin word.  Therefore,
if every nonzero class coefficient is divisible by `lambda^k`, then

```text
E1(0) is divisible by lambda^(k+2).
```

In particular, after all eighteen nonzero displayed rows pass correlation
digit 2, exact row-margin compatibility forces the delayed origin row
through digits 3 and 4 automatically.  The physical digit-3 and digit-4
systems have eighteen independent candidate rows, not nineteen.  The
nineteenth row in the phase-only chart remains genuine when the row margin
has not been imposed; the statements are consistent.

The audit checks this augmentation identity directly on 65 deterministic
placements per profile and checks exact augmentation on all 405 targets.

## 3. Retraction boundary

Before imposing a row margin, the six structured correlation forms have:

- one five-form retraction on `h2-222222-0`, omitting structured form 1;
- one on `h2-422220-3`, omitting structured form 3;
- none on the other three profiles.

All 364 five-hyperplanes are exhausted.  This is a useful new sampler for
the phase-only digit-two variety, but it is not physical.

After imposing the rank-six physical margin digit, no five-form retraction
survives.  The complete 11,011-space audit gives the maximum dimensions
`4,3,3,3,4` above.  Thus the physical cut removes exactly the most favorable
five-form shortcut.

## 4. Bounded physical-chart search

The strongest target on `h2-422220-3` by raw multiplicity is target 65:

```text
raw assignments       5,166,361,292,927,927,400
phase sums
  A: (1,3), (3,-1), (4,1)
  B: (-3,0), (1,-3), (4,12)
```

The pinned verifier below certifies one correlation digit-two point.
Separately, the archived 300-CPU-second manifold walk replayed five distinct
digit-two points but found no exact-margin point.  These are bounded
`UNKNOWN` observations, not evidence of convergence.

The best replayed seed has placement SHA-256

```text
941b2029c2d0df0935f91bb213bb53b3ee23117f21c7cee1f9fc245eaddb8abc.
```

It satisfies correlation digits zero through two, but:

```text
exact margin groups still wrong                 3 / 6
margin digit-4 residual                 (0,0,0,1,0,0)
active correlation digit-3 defect              12 / 18
active correlation digit-4 defect              11 / 18
```

Its correlation digit-two Jacobian has rank 18 and tangent dimension 12.
The margin digit-4 Jacobian has rank five on that tangent, and its
linearized correction is consistent with dimension seven.  Exhausting all
`3^7=2,187` corrections in that affine tangent sheet finds:

```text
minimum exact correlation digit-two defect       4
minimum margin digit-4 defect                     0
points satisfying both exactly                    0
```

A 120-CPU-second margin-digit-4-biased walk replayed four points and did not
improve the pinned defect one.  These are bounded `UNKNOWN` experiments,
not exclusions.  No consecutive correlation digit-3/digit-4 lift was
found.

Peak resident memory in these runs was below 55 MB.

## 5. Complete-search estimate and gate

The exact row-margin target count does not itself give its intersection
with the correlation quadrics.  Under the same explicitly neutral
independence model used by the existing search estimate:

```text
points in one rank-30 target chart                 3^30
after 18 correlation digit-two quadrics            3^12 = 531,441
after the six margin digit-4 quadrics               3^6  = 729
```

The exact raw target multiplicities give a separate heuristic.  Dividing
the accepted-assignment total by `3^36` predicts physical digit-two counts
per profile

```text
1817.51, 1814.11, 1926.57, 2454.51, 2238.90,
```

or `10,251.60` across all five.  The now-correct physical digit-3 count is
eighteen rows, so the same neutral model predicts

```text
10,251.60 / 3^18 = 2.6461e-5
```

physical digit-3 points across the entire five-profile shell.  None of
these decimal expectations is a theorem.  They are planning evidence.

**Gate recommendation:** stop spending headline search tokens on the five
two-high lifts.  The new rank-six reduction and exact retraction census are
worth preserving as a paper-strength extension of the five-orbit
classification, but they make the construction forecast worse, not better:
the physical gate destroys the five-form shortcut, and even a physical
digit-3 point is neutral-model exceptional at the `10^-5` program level.
Resume this lane only for an algebraic elimination theorem or a construction
that forces later digits, not for additional generic witness search.

This recommendation concerns the five `n_9=2` profiles only.  It neither
excludes the unclassified `h=1` shell nor any construction outside the
order-three multiplier chart.

## Reproduction

Standard-library exact audits:

```text
python3 audit_row_margin_retraction.py
python3 audit_four_subspaces.py
python3 audit_margin_digit4.py
```

Their pinned semantic SHA-256 values are respectively:

```text
7aed9978a72092c2146aff528734ac31afbc4c33fb1dd35c4bcd436015697c65
1a067c914ea5911136d2b4437d0ffb98fe80601ac545dff7e3dbd34c8216364d
83fe2380c978de46e1f919fd34d7715a9f0ae4ad3bb4a95f187aeb7437effe9e
```

The NumPy replay of the pinned seed and its complete tangent sheet is:

```text
/Users/alec/Documents/tmp/hadamard-env/bin/python \
  verify_pinned_physical_chart_seed.py
```
