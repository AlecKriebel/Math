# Exact integer degree-moment obstruction

## Statement

The exact pseudodistribution in
`centered_quarter_bv_pseudodistribution.json` is not the pair/triple marginal
of a centered 41-point code whose inner products lie in

```text
{-1, -3/4, -1/2, -1/4, 0, 1/4, 1/2}.
```

This statement is deliberately narrower than nonexistence of a 41-point
spherical code.

## Row identities

Fix a point `x`.  Let `d_i(x)` be the number of other points having inner
product `i/4` with `x`, for `i=-4,...,2`.  There are 40 other points, hence

```text
sum_i d_i(x) = 40.
```

Centering gives

```text
0 = <x, sum_y y> = 1 + sum_i (i/4)d_i(x),
```

or `sum_i i d_i(x)=-4`.  At most one point is antipodal to `x`, so
`0<=d_{-4}(x)<=1`.  All degrees are nonnegative integers.

The verifier solves these two linear identities explicitly and enumerates
exactly 27,041 possible rows.  Thus there is no discretization or rounding:
every row of every code under the hypotheses occurs in the finite list.

## Separating polynomial

Let `P(d)` be the 17-term integral quadratic polynomial stored in
`centered_quarter_integer_degree_obstruction.json`.  Direct integer
evaluation on the complete list gives

```text
P(d) >= 0
```

for all 27,041 rows.  Sixteen rows attain zero; the least positive value is
`555433528751984`.

The source pair distribution gives `E[d_i]=alpha_i`.  Its symmetrized triple
distribution gives

```text
E[d_i d_j]
  = delta_{ij} alpha_i
    + sum over ordered placements (i,j,k) of nu_{sort(i,j,k)}
      / |orbit(sort(i,j,k))|.
```

The verifier reconstructs this matrix using exact rational arithmetic.  On
substitution into `P`, it obtains

```text
E[P(d)]
  = -298897510609152269959977158772724413
    / 3198650000000000000
  < 0.
```

That contradicts pointwise nonnegativity, proving the statement.

## Computational boundary

The finite enumeration is a proof only because the hypotheses force every
row onto the exact quarter grid and the two displayed integer equations.
No claim is made about off-grid codes, noncentered codes, or even other
pair/triple distributions on the same grid.  The verifier uses no
floating-point arithmetic and does not trust solver status.

## Repair and barrier result

The displayed separator removes the original witness but not the underlying
relaxation.  Two further solve-separate rounds produce two more exact
quadratic inequalities, certified in

```text
centered_quarter_integer_degree_obstruction_2.json
centered_quarter_integer_degree_obstruction_3.json.
```

After imposing all three, exact rational reconstruction gives
`repaired_pair_triple_local_3.json`.  Its first two degree moments have the
positive 18-atom realization stored in
`centered_quarter_integer_degree_mixture.json`.  The independent verifier
checks

\[
 \sum_a w_a d^{(a)}_i=\alpha_i,\qquad
 \sum_a w_a d^{(a)}_i d^{(a)}_j=M_{ij}
\]

for all \(i,j\), where \(M\) is reconstructed from the pair/triple source.
Every stored \(d^{(a)}\) is a nonnegative integer vector satisfying the two
row identities and the antipode bound.

The same repaired source independently passes the exact all-harmonic
pair/BV verifier, every current sharp rank and cap row, and exact local
rank-five Gram consistency through six vertices.  Consequently the integer
degree-moment mechanism is a certified barrier, not an upper bound:
first/second finite-population row moments do not close the centered
quarter-grid relaxation.
