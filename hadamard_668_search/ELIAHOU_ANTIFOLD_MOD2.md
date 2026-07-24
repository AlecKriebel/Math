# First binary lift of the distance-41 anti-fold

## Status

The orientation-free anti-fold admits a further exact reduction before SAT.
Pair the long rows and the short rows by

```text
P=(A+B)/2,  Q=(C+D)/2,  R=(A-B)/2,  S=(C-D)/2.
```

Then

```text
N(A)+N(B)+N(C)+N(D)
  = 2[N(P)+N(Q)+N(R)+N(S)].                       (1)
```

At special distance 41, `R` and `S` are fixed sparse boundary polynomials.
Writing the variable pair sums as

```text
P=P0+2p,  Q=Q0+2q
```

turns the first binary digit of (1) into an affine linear system on the
retained support cells.  Including retained-weight parity, its rank is
exactly 21 in every one of the 39 reciprocal-`q` cases.

This is a substantial exact sieve, but not an obstruction.  Exact
MacWilliams transforms give, for representative target-weight layers,

```text
long q index 0:  51,310,052,181,007,034
long q index 2:  25,953,942,447,362,002
short q index 2: 25,968,969,218,639,808
```

binary supports after the first lift.  The full integer anti-fold equations
therefore remain essential.  No distance-41 exclusion or Hadamard matrix is
claimed here.

## Derivation

After the reciprocal `q` pair is fixed, the two rows within each block agree
on every variable anti-fold cell.  Their differences `R,S` are supported
only on the `q` cells and the unavoidable long/short boundary cells.

Zero every variable cell to obtain fixed polynomials `P0,Q0`.  A retained
cell contributes twice a signed monomial, so

```text
N(P0+2p)+N(Q0+2q)+N(R)+N(S)
 = F0 + 2 C(p,q) + 4[N(p)+N(q)].                  (2)
```

The exact normalized target is `167`.  Dividing (2) by two and reducing
modulo two removes the quadratic term and leaves

```text
C(p,q) = (167-F0)/2              over F_2.        (3)
```

The checker constructs (3) directly in the 42-coefficient negacyclic group
ring, row-reduces it, and includes the parity forced by selecting exactly 39
support cells.  Its complete rank census is

```text
available cells 78: 38 cases, rank 21
available cells 79:  1 case, rank 21.
```

For the pinned representatives, the number of words of the required weight
in the affine code is computed independently from the dual code using the
exact Krawtchouk/MacWilliams formula.  This quantifies why the first bit is a
useful solver layer while also proving that it cannot close the boundary by
itself.

## Reproduction

From this directory:

```sh
python3 verify_eliahou_antifold_mod2.py
python3 -m unittest -v test_eliahou_antifold_mod2.py
```

Both commands use only the Python standard library.
