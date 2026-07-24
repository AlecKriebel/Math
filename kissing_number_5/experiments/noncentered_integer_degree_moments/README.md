# Noncentered fixed-41 integer degree moments

This experiment applies universal integer row constraints to the exact
quarter-grid pair/triple pseudodistribution
`fixed41_bv_fullradial_k16_pseudodistribution.json`.  Unlike the centered
degree-moment experiment, no weighted row-sum identity is assumed.

For a row `d=(d_{-1},d_{-3/4},...,d_{1/2})`, every 41-point code satisfies:

```text
sum d_i = 40,
d_{-1} <= 1,
d_{-1}+d_{-3/4}+d_{-1/2}+d_{-1/4} >= 7,
d_{1/4}+d_{1/2} >= 6,
d_{1/2} <= 15,
d_{-3/4} <= 5.
```

The first two inequalities are immediate.  The two strict-tail bounds come
from the exact enlarged-cap theorem at `1/300`.  The contact-link projection
and the exact bound `A(4,1/3)<=15` give `d_{1/2}<=15`.

For the last bound, fix the row base `x` and project every neighbor `y` with
`<x,y>=-3/4` into `x` perpendicular.  The normalized projections are unit
vectors in `R^4`, and two distinct projections have inner product at most

```text
(1/2-9/16)/(1-9/16) = -1/7.
```

A set of pairwise strictly obtuse unit vectors in `R^4` has size at most
five.  One proof observes that a positive semidefinite Gram matrix with
strictly negative off-diagonal entries has nullity at most one
(Perron--Frobenius applied after subtracting it from a large scalar matrix);
rank at most four therefore gives `m<=5`.  Equality is included.

There are exactly 855,168 integer rows satisfying the displayed constraints.
The exact certificate stores a 22-term integral quadratic polynomial
nonnegative on all of them.  Its expectation under the named pair/triple
witness is

```text
-5965330868631874099279 / 1875000000000 < 0.
```

Hence that all-harmonic pseudodistribution is not even a valid first/second
integer row-moment shadow once the universal local bounds are imposed.  This
is still only a quarter-grid, fixed-witness obstruction; it is not an upper
bound for arbitrary spherical codes.

Run the standard-library verifier and tamper tests:

```bash
python3 verifiers/verify_fixed41_noncentered_integer_degree_obstruction.py
python3 -m unittest \
  tests.test_fixed41_noncentered_integer_degree_obstruction
```

Discovery used column generation over all 855,168 rows.  A floating
separator exposed 234 zero rows; the stored integral coefficients were then
reconstructed from the exact corank-one nullspace of those rows.  The
verifier trusts neither the LP nor the selected face and exhaustively
rechecks the exact polynomial.
