# LP(333) coupled order-three row-sum theorem

## Status

The two still-open coupled multiplier lanes have a common, finite outer
boundary:

```text
<121>: (r,c) -> (4r,10c)
<211>: (r,c) -> (4r,26c)
```

in `Z/9 x F_37`.  In either lane, the complete Gaussian row sum has exactly
`1,296` possibilities after imposing the fixed 37-column margins.  They form
`216` free orbits under the common row dihedral group and `108` free orbits
after one further fixed-compression equivalence.

An exact second-stage enumeration proves that all `1,296` possibilities can
also satisfy the two independent Legendre equations at zero column lag.
Thus neither multiplier lane is ruled out.  The first equations capable of
distinguishing or eliminating them have nonzero column lag.

This is an exact theorem about two restricted multiplier families.  It is
not a Legendre pair, a Hadamard matrix, or evidence that any of the `1,296`
outer states extends through the mixed equations.

The dependency-free verifier is `verify_lp333_twisted_order3.py`.

## 1. The common invariant row word

Combine the two binary sequences into a QPSK sequence

```text
q = (A+B + i(B-A))/2.
```

Its fixed column sums are

```text
1                     at c=0,
-3 i chi(c)           at c != 0,
```

where `chi` is the quadratic character of `F_37`.

Both multipliers have row component `4`, so the complete row sum

```text
s_r = sum_c q(r,c)
```

satisfies `s_(4r)=s_r`.  Write

```text
s = (a,d,e,b,d,e,c,d,e).
```

Summing the Legendre equations over all 37 column lags gives

```text
sum_r s_r = 1,
Re PAF_s(0) = 297,
Re PAF_s(k) = -37,       k=1,2,3,4.                 (1)
```

Let

```text
T = a+b+c,       P=d+e,
W = |d|^2+|e|^2.
```

The total-sum equation says `T=1-3P`.  The zero-lag and lag-three
equations are

```text
|a|^2+|b|^2+|c|^2 + 3W = 297,
Re(a conjugate(b)+b conjugate(c)+c conjugate(a)) + 3W = -37.
```

Taking `|T|^2` and eliminating the three fixed-row values gives the small
positive-definite equation

```text
3(|d|^2+|e|^2+Re(d conjugate(e))) - Re(d+e) = 37.  (2)
```

Conversely, (2), the total sum, and the energy equation imply all four
nonzero equations in (1): row invariance makes lags 1, 2, and 4 equal, and
their common value is

```text
Re(P) - 3(|d|^2+|e|^2+Re(d conjugate(e))) = -37.
```

## 2. Exact census: 36 to 12 to 6,048

Equation (2) has exactly `36` ordered Gaussian-integer pairs `(d,e)`.
Its quadratic form is at least half the squared Euclidean norm of the four
integer coordinates, so Cauchy--Schwarz gives a complete tiny search box.

A row contains 37 fourth roots.  Therefore a Gaussian integer `x+iy` is a
possible row sum exactly when

```text
|x|+|y| <= 37,       |x|+|y| is odd.               (3)
```

Applying (3) to both repeated row values leaves exactly `12` pairs:

```text
((-2,-3),( 1, 0))   ((-2,-1),( 4, 1))
((-2, 1),( 4,-1))   ((-2, 3),( 1, 0))
(( 0,-3),( 2, 3))   (( 0, 3),( 2,-3))
(( 1, 0),(-2,-3))   (( 1, 0),(-2, 3))
(( 2,-3),( 0, 3))   (( 2, 3),( 0,-3))
(( 4,-1),(-2, 1))   (( 4, 1),(-2,-1)).
```

For every pair, there are exactly `504` ordered triples `(a,b,c)` satisfying
their required sum, energy, and (3).  Hence the generic invariant row
projection contains

```text
12 * 504 = 6,048
```

words.  Their canonical integer serialization has SHA-256

```text
2a44ef09e87e6a364c105c1660e923076cc244c867b816722ec4791f4ba2fc28
```

## 3. The zero column and all fixed margins

The zero column is itself invariant under `r -> 4r`.  Each underlying binary
zero column has weight five.  Its values at rows `0,3,6` therefore contain
exactly two plus signs, and exactly one of the two moving row cycles is plus.
For the QPSK zero column `x`, this is equivalent to

```text
x_e = -x_d,
sum of the three fixed A signs = 1,
sum of the three fixed B signs = 1.
```

There are nine possible QPSK triples `(x_a,x_b,x_c)`.  Every nonzero
three-column multiplier orbit contributes `3q` at each fixed row, so a
candidate must satisfy

```text
(a,b,c) = (x_a,x_b,x_c)       coordinatewise modulo 3.   (4)
```

Condition (4) cuts each 504-word completion catalog to 108 words.  The exact
total is therefore

```text
12 * 108 = 1,296.
```

This congruence is also sufficient for lifting the row sums through all fixed
column margins.  For one binary sequence, a representative nonzero column
has weight three or six.  Its three-column orbit contributes

```text
(3u_0, 3u_3, 3u_6,
 u_1+u_4+u_7, u_2+u_5+u_8)
```

to the five invariant row values.  Each weight has only 20 distinct
signatures.  An exact 12-step set convolution (six columns of each weight)
gives 59,995 nonzero-column states and 186,576 row vectors after the six
possible zero columns are added.  Checking both binary sequences gives
exactly the same 1,296 QPSK words selected by (4), with no further loss.

The fixed-margin catalog SHA-256 is

```text
4c03c95355e161dca2bca94c635f377f73ec069baf36aa1be8143fd351ea2965
```

## 4. Exact symmetry quotient

Common translation by 111 cycles `(a,b,c)`, while inversion exchanges
`b,c` and `d,e`.  The resulting order-six action is free on the catalog:

```text
1,296 / 6 = 216
```

row-dihedral orbits.

There is one further valid fixed-compression equivalence.  Take the unit
`u=298`, for which

```text
u = 1 (mod 9),       u = 2 (mod 37),       chi(2)=-1.
```

Decimate both sequences by `u` and swap `A,B`.  This preserves the ordered
fixed compression and multiplier invariance, and it complex-conjugates every
row sum.  Conjugation acts freely on the 216 dihedral orbits, leaving exactly

```text
1,296 / 12 = 108
```

extended equivalence classes.

## 5. The pure row axis does not obstruct

At column lag zero, row invariance leaves only two independent LP equations:

```text
PAF_A(1,0)+PAF_B(1,0) = -2,
PAF_A(3,0)+PAF_B(3,0) = -2.                       (5)
```

For one representative binary column `u`, its three-column orbit contributes

```text
PAF_u(1)+PAF_u(4)+PAF_u(7),
3 PAF_u(3)
```

to these two coordinates.  Adding these coordinates to the 20 row
signatures and convolving six weight-three columns produces exactly 21,953
joint states over 3,430 row signatures.  Weight-six columns are complements:
their row contributions negate, while their PAF contributions do not change.

The 1,296 QPSK words contain 147 distinct binary row targets.  Every target
has between 25 and 34 attainable pure-axis PAF pairs, and every one of the
1,296 paired row words admits choices satisfying (5).  This is exhaustive,
not a bounded solver result.

## 6. Relation between the two coupled lanes

On each nonzero column orbit of `H=<10>={1,10,26}`, choose a representative
and reverse its exponent:

```text
pi(10^k c) = 10^(-k) c.
```

Then

```text
pi(10c) = 26 pi(c).
```

The column permutation `(r,c) -> (r,pi(c))` conjugates the `121` action to
the `211` action.  It stays inside each quadratic-character class, so it
preserves every fixed column margin.  Because it is the same column
permutation in every row, it also preserves complete row sums and every
correlation with column lag zero.

The permutation is not additive on `F_37`; consequently it does not preserve
general column or mixed lags.  This is a precise partial equivalence, not an
equivalence of the full LP problems.  It proves that only equations with
nonzero column lag can distinguish the two lanes.

## Reproduction

From this directory:

```sh
python3 verify_lp333_twisted_order3.py
python3 -m unittest -v test_lp333_twisted_order3.py
```

The verifier uses only the Python standard library and exact integer
arithmetic.
