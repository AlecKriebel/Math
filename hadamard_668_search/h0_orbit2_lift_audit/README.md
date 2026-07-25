# Independent lift audit for the second `h=0` profile orbit

This audit concerns

```
A = (1,2,6,1,5,1,4,5,1,5,7,4)
B = (2,4,2,4,4,6,5,5,8,1,5,8)
target = (-3,0,0,3).
```

The profile has trivial stabilizer.  No halfturn or other profile symmetry
is imposed anywhere in this folder.

## Exact algebra

The first placement digit has rank 18 on 54 active trits, hence nullity 36.
After composition with a canonical affine parameterization, displayed rows
0 and 7 vanish identically.  The remaining rows

```
1,2,3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19
```

give eighteen quadrics over `F_3`.

The polar matrices are dense: eleven have rank 36 and seven have rank 35.
Their coefficient vectors have rank 18.  Thus there is no constant or
linear combination eliminating a quadratic equation, and no low-rank
individual equation.  The exact ordered quadratic hashes are checked by
`verify_orbit2_quadrics.py`, which also compares 64 random affine points
against the independent symbolic phase evaluator.

## Bounded search result

Ternary tabu search evaluated 2,841,815 updates in 120 seconds and reached
defect one.  The pinned point in `DEFECT1_CERTIFICATE.json` satisfies every
second-digit row except displayed row 10:

```
(0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0).
```

At this point the full 18-row Jacobian has rank 18, while the Jacobian of
the seventeen satisfied rows has rank 17.

An exact sparse quadratic enumerator then exhausted the complete ternary
Hamming ball of radius six around this point:

```
radius 0:           1
radius 1:          72
radius 2:       2,520
radius 3:      57,120
radius 4:     942,480
radius 5:  12,063,744
radius 6: 124,658,688
total:    137,724,625
```

No digit-2 point occurs in that ball.  The run took 116.14 seconds and
peaked at 539 MB.  This is a rigorous local exclusion, not a global
obstruction.

The independent one-hot CNF has 27,264 Boolean variables and 117,694
clauses.  A bounded CaDiCaL run was stopped after ten minutes without a
result; an independent Kissat run was stopped after 2.3 minutes with the
same status.  Neither run makes a claim.

## Status

No exact digit-2 witness was found.  Therefore there is no digit-3 or
row-margin witness to replay for this orbit yet.  The substantive outputs
are the independently derived 18 quadrics, the defect-one point, and its
certified radius-six exclusion.

Run the fast verifier with:

```
/Users/alec/Documents/tmp/hadamard-env/bin/python \
  verify_orbit2_quadrics.py
```
