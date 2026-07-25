# Character compression of the second `h=0` orbit

This folder studies the eighteen second-digit quadrics for the exact
profile

```
A = (1,2,6,1,5,1,4,5,1,5,7,4)
B = (2,4,2,4,4,6,5,5,8,1,5,8)
target = (-3,0,0,3).
```

It is an algebraic compression result, not a placement witness, Legendre
pair, or Hadamard matrix.

## Six structured combinations

Write the active quadrics, in displayed-row order, as

```
(q_0,...,q_17) = (Q_1,...,Q_6,Q_8,...,Q_19)
```

and define

```
g_i = q_i + q_{i+6} + q_{i+12},       0 <= i < 6.
```

Thus the displayed row triples are

```
(1,8,14), (2,9,15), (3,10,16),
(4,11,17), (5,12,18), (6,13,19).
```

For a scalar combination `G_a = sum a_i g_i`, let `B_a` be its polar
matrix and `l_a` its linear coefficient.  Exhaustion of the 728 nonzero
vectors `a in F_3^6` gives:

* every `B_a` is singular, with rank between 19 and 34;
* for 722 vectors,
  `rank([B_a | l_a]) = rank(B_a) + 1`;
* the only exceptions are the three projective lines represented by

```
(1,1,2,2,1,2)
(1,2,0,2,1,2)
(1,2,2,1,2,1).
```

In the rank-increasing case there is a radical vector `v` with
`l_a(v) != 0`.  Consequently

```
G_a(x+t v) = G_a(x) + t l_a(v),
```

so every value of `G_a` occurs exactly `3^35` times.

All three exceptional lines have nonzero final coordinate.  It follows
that every nonzero scalar combination of `(g_0,...,g_4)` is balanced.
Additive-character orthogonality therefore proves the exact global
statement

```
# {x in F_3^36 : (g_0,...,g_4)(x) = y} = 3^31
```

for every `y in F_3^5`.

This is much stronger than a random or local-search observation: the
first five structured constraints define an exactly uniform quadratic
map on all `3^36` affine points.

## Exact six-coordinate fibers

Diagonalizing the three exceptional scalar quadrics and applying Fourier
inversion gives the complete fiber distribution of
`g=(g_0,...,g_5)`.  Its 729 fibers take only five sizes:

| fiber size | number of fibers |
|---:|---:|
| 205891120934388 | 27 |
| 205891125717357 | 135 |
| 205891130500326 | 243 |
| 205891135283295 | 216 |
| 205891140066264 | 108 |

In particular,

```
# g^{-1}(0) = 3^30 - 7*3^13
             = 205891120934388.
```

The six combined equations therefore leave exactly that many affine
points.  This count does not assert that any point satisfies the twelve
remaining independent quadrics.

The six polar matrices also have a two-dimensional common radical, and
the six linear terms have rank two on it.  Translation by that radical
maps bijectively onto a fixed two-dimensional output subspace.  This
explains directly why the full fiber sizes are constant on nine-element
output cosets (and why every multiplicity in the table is divisible by
nine).

## Exact prefix calibration

The same character method gives exact counts after adjoining the first
four original active quadrics to the six `g_i`:

| equations | exact zero fiber | `3^(36-m)` | ratio |
|---:|---:|---:|---:|
| 6 | 205891120934388 | 205891132094649 | 0.999999946 |
| 7 | 68630383210734 | 68630377364883 | 1.000000085 |
| 8 | 22876784306199 | 22876792454961 | 0.999999644 |
| 9 | 7625590635303 | 7625597484987 | 0.999999102 |
| 10 | 2541863158002 | 2541865828329 | 0.999998949 |

Here the ordered equation basis is

```
(g_0,...,g_5,q_0,q_1,q_2,q_3).
```

The counts are frozen in `EXACT_PREFIX_ZERO_FIBERS.json`.  They show that
the global population remains extremely close to the random-map
heuristic through ten constraints.  This is evidence against claiming
that the low-rank combinations alone make the complete eighteen-equation
lift unusually easy.

## Constructive four-equation parametrization

The common radical of the first four polar matrices has dimension seven.
Their four linear coefficients have rank four on that radical.  The
verifier constructs a `36 x 4` matrix `V` satisfying

```
B(g_i) V = 0,             0 <= i < 4,
(l(g_0),...,l(g_3)) V = I_4.
```

Choose the complement `Y` on which affine coordinates `0,2,5,9` vanish.
For `y in Y`, put

```
Phi(y) = y - V (g_0(y),...,g_3(y))^T.
```

Then `Phi` is a bijection from `F_3^32` onto the common zero set of the
first four `g_i`.  This is an explicit quadratic parametrization, and it
independently explains the exact count `3^32` for those four equations.

## Verification

Run:

```
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  verify_quadric_character_compression.py
```

The verifier re-derives the quadrics from the frozen profile, exhausts all
728 scalar combinations, diagonalizes the exceptional forms over `F_3`,
performs exact Fourier inversion, checks the parametrization directly,
and replays all 29,524 projective characters needed for the prefix table.

On the 2026-07-24 reference run it used one CPU for 16.74 seconds, with
maximum resident size 44,023,808 bytes.  Frozen artifact hashes are:

```
EXACT_PREFIX_ZERO_FIBERS.json
1576ca92f9ecf5cddd87d0c518ec1557bcf0fd15a1c33f1ef68e285913c9531d

verify_quadric_character_compression.py
7d9b1b33c6d769e351fcf6f9b3a33682dc30d5faea01a0e4be6d7abd41a0184f
```
