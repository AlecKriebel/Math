# LP(333) labelled primitive-nine field split

## Status

This checkpoint gives an exact, dependency-free state reduction for the
fully labelled primitive-nine jet, together with one mechanically replayed
catalog survivor.

It does **not** construct an `LP(333)` or a Hadamard matrix of order 668, and
it does not exclude any of the 1,756 row-sum catalog entries.  The exact
catalog accounting at this checkpoint is:

```text
certified fully labelled jet survivors: at least 1
certified catalog exclusions:           0
```

The survivor statement includes all six primitive-nine digits at all 37
physical column lags and the four exact row-direction equations.

## 1. Exact invariant-algebra split

Let `H` be the order-three multiplier subgroup of `F_37^*`.  The algebra of
`H`-invariant functions on `C_37` has the zero class and twelve nonzero
classes, hence dimension 13 over `F_3`:

```text
A = F_3[C_37]^H.
```

If `E_0` is the first nonzero class sum, its thirteen powers span `A`.  Its
minimal polynomial factors as

```text
m(x) = x f_0(x) f_1(x),

f_0(x) = x^6 + x^5 + 2x^3 + x^2 + x + 1,
f_1(x) = x^6 + 2x^4 + x^2 + 2x + 2.
```

Both degree-six quotients are fields.  Therefore

```text
F_3[C_37]^H  ~=  F_3 x F_729 x F_729.            (1)
```

The verifier establishes (1) without a computer-algebra package:

- it reconstructs multiplication by physical convolution on `C_37`;
- it proves the 13 power vectors of `E_0` are independent;
- it checks that `m(E_0)=0` and that `m=x f_0 f_1`;
- it checks an inverse for each of the 728 nonzero elements in each
  degree-six quotient;
- it checks that the combined `1+6+6` coordinate map has rank 13;
- it checks all `2*13^2 = 338` basis products under the two field maps.

Column negation sends class `j` to class `j+6`.  In both field factors the
verifier independently confirms that this is the third Frobenius iterate,

```text
x |-> x^(3^3).                                   (2)
```

Thus each 13-component invariant column equation is replaced, without loss,
by augmentation and two six-coordinate field equations.  The augmentation
factor is already fixed by the row-sum catalog.

## 2. Why the upper three jet digits linearize

At a primitive ninth root, put `pi=1-zeta_9`.  The six-digit local ring is

```text
R = F_3[pi]/(pi^6).
```

The ideal

```text
I = pi^3 R
```

is square-zero.  Hence, after jet digits zero through two are fixed, every
contribution to digits three through five is linear in the remaining
within-residue placement data: a product of two upper corrections lies in
`I^2=0`.

Lucas' theorem makes the complementary lower statement precise.  For
`k=0,1,2`, `binom(r,k) mod 3` depends only on `r mod 3`, so the first three
digits of a normalized class triple depend only on its three residue
counts.  The exact state decomposition is therefore:

```text
ten possible residue profiles per class
        |
        +-- nonlinear digits 0,1,2 in F_729 x F_729
        |
        +-- linear placement lift for digits 3,4,5.
```

This is an exact finite reduction, not a relaxation or a timeout-based
inference.

## 3. Replayed labelled survivor

The pinned catalog is

```text
output/lp333_order3_row_sum_catalog.csv
SHA-256 e8631dc0ae2f65c475af1c2e13429778f666a0fa8a13c9f1153d07d7883a98ea
```

Data row 695 has aggregate word

```text
(-1,1, -3,-1, 2,0, 2,0, 1,1, -1,-1, 2,0, -1,-1, -1,1).
```

The following twelve masks in each channel encode normalized three-subsets
of the nine rows.  The verifier applies the prescribed complementation in
the weight-six classes.

```text
A = (49,296,42,41,208,208,385,37,97,208,261,69)
B = (416,67,100,168,25,385,328,296,73,35,49,112)
```

Exact replay checks:

```text
24 labelled class words
18 exact row margins
4 exact integer row-direction correlations
37 physical column lags x 6 jet digits = 222 equations over F_3
```

All checks pass.  This proves that digits two through five do not eliminate
every fully labelled lift, while leaving the global catalog audit open.

## Reproduction

From this directory:

```text
python3 verify_lp333_order3_labeled_jet.py
python3 -m unittest -v test_lp333_order3_labeled_jet.py
```

The verifier and tests import no SAT solver.  On the checkpoint machine the
focused test suite took under one second and peaked below 30 MB resident
memory.
