# Modulo-two affine-code search results

The search objective is the number of the twenty normalized residuals that
remain nonzero modulo three.  Every visited point has exact weight 39 and
passes the entire characteristic-two affine layer.

## Measured bounded runs

| case | runtime | restarts | iterations | best mod-3 defect |
|---|---:|---:|---:|---:|
| 26 | 180 s | 1 | 30,940 | 2 |
| 26, quotient restarts | 120 s | 55 | 20,943 | 2 |
| 0 | 90 s | 1 | 6,015 | 2 |

The pinned case-26 defect-two point is
`CASE26_MOD2_BEST_DEFECT2.json`.  Its only nonzero residues modulo three
occur at normalized lags 9 and 11:

```
lag 9:  -4 = 2 (mod 3)
lag 11: 16 = 1 (mod 3)
```

The verifier rebuilds its physical four anti-fold rows and confirms all
twenty residuals, weight 39, zero defect modulo two, and defect two modulo
three.

## Exact local exclusion

Using the joint mod-2/mod-3 SAT model, the entire Hamming ball of radius
eight around the pinned point is UNSAT.  Because both the center and every
feasible point have weight 39, this covers all replacements of at most four
selected cells by four unselected cells.  The exact run used 8,484 SAT
variables and 32,750 clauses and completed in 48.86 seconds.

A radius-ten run was deliberately stopped after three minutes without a
result.  It supplies no mathematical conclusion.

No joint modulo-six witness was found in these bounded runs.
