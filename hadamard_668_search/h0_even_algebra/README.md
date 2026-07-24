# Irreducibility of the h=0 half-turn even pencils

## Scope

This directory records an exact negative structural result for the pinned
`h=0` order-three profile.  It is a contraction obstruction, not a
Legendre pair of length 333 and not a Hadamard matrix of order 668.

The first placement affine space has half-turn eigencoordinates

```text
x in F_3^21,     y in F_3^15.
```

At the second placement digit, the active equations split into

```text
12 even rows:  F_i(x) + G_i(y) = 0,
 6 odd rows:   x^T B_i y + l_i(y) = 0.
```

The verifier reconstructs these forms from the audited primary lifting
code rather than storing copied matrices.

## Certified obstruction

There is no common affine translation that makes either the `F_i` family
or the six odd equations homogeneous.  In both cases the relevant stacked
linear system has coefficient/augmented ranks

```text
21 / 22.
```

More strongly, choose any nonsingular polar form `P_0` in a pencil and
form the relative operators `P_0^{-1} P_i`.  Exact closure under
multiplication gives

```text
X pencil:  dim algebra = 441 = dim End(F_3^21),
Y pencil:  dim algebra = 225 = dim End(F_3^15).
```

Thus neither even pencil has a nonzero proper common invariant subspace.
In particular, neither admits simultaneous block diagonalization by
congruence.  A single-field trace-square or coordinatewise norm model
would give a proper commutative relative-operator algebra, so those
standard norm contractions are also excluded.

The canonical asymmetric slice `y=e_0` makes the six odd equations rank
six and leaves a 15-dimensional kernel in `X`.  After restriction to that
kernel, the twelve polar ranks are

```text
15, 15, 15, 14, 13, 15, 15, 14, 14, 15, 14, 14,
```

and their relative operators again generate all of
`End(F_3^15)`, of dimension 225.  Consequently the slice that produced
the known asymmetric second-digit witness does not uncover a hidden
simultaneous block decomposition either.

This does not rule out a nonlinear parametrization or a more global
elimination involving both even and odd equations.  It does rigorously
rule out the most direct simultaneous-diagonalization, invariant-code
block, and field-trace norm reductions.

## Verification

From `hadamard_668_search` run:

```bash
python3 h0_even_algebra/verify_h0_even_algebra.py
```

The calculation is exact over `F_3`, dependency-free, and normally takes
under ten seconds.
