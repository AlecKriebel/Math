# The second placement digit and its collapsed six-form pencil

## Status

The five exact profile orbits in the two-high shell all survive the second
placement digit.  On each orbit, the first digit leaves an affine space

```text
x = x0 + N y,                    y in F_3^36.
```

The next exact Eisenstein digit is a system of twenty quadratic equations
over `F_3`.  Two norm-origin rows vanish identically and the other eighteen
polar forms are independent.  There is no nontrivial linear combination
whose quadratic part vanishes, so this digit gives no further linear
reduction and no profile-level contradiction.

There is nevertheless a useful new factorization.  Six three-row
combinations

```text
T_b = E0(b) + E1(b) + E1(27b),
              b in {1,2,4,8,16,32},                   (1)
```

have polar ranks only 15 through 21, even though the individual nonzero
displayed forms have ranks 34 through 36.  These six forms are exactly the
projective combinations supported on at most three displayed rows whose
polar rank is below 28.

An exact quadratic-Gauss calculation counts the joint zero fibers of (1)
without enumerating `3^36` points.  Every one of the `3^6=729` target
fibers is nonempty on every profile orbit.  Thus the collapsed pencil is a
strong compression, but it is not an obstruction.

This is a placement-layer theorem for five fixed profile orbits.  It does
not construct a labelled `LP(333)`, a Legendre pair, or a Hadamard matrix
of order 668.

## 1. Direct quadratic descent

Put `lambda=1-omega`.  On the first-digit affine space, one signed phase
term has the form

```text
sigma omega^L,                  L=d+b.y in F_3.
```

The exact expansion

```text
omega^L = (1-lambda)^L
        = 1 - L lambda + binom(L,2) lambda^2     modulo lambda^3
```

and the identity

```text
binom(L,2) = 2L^2+L                              in F_3
```

give a quadratic next digit.  If the lambda-zero integer constant of the
correlation row is `C`, then `3` contributes lambda-square digit `2`, and
the complete row is

```text
q(y) = 2(C/3) + sum_t sigma_t (2L_t(y)^2+L_t(y)).       (2)
```

Writing `q=c+l.y+(1/2)y^T B y`, formula (2) gives the coefficients directly:

```text
c = 2(C/3) + sum_t sigma_t (2d_t^2+d_t),
l =            sum_t sigma_t (d_t+1)b_t,
B =            sum_t sigma_t b_t b_t^T.                (3)
```

The verifier derives (3) symbolically and also reconstructs the same forms
by 667-point quadratic interpolation.  Eight additional affine points per
profile are replayed through the exact Eisenstein phase equations.

For all five profiles:

```text
placement variables before the first digit             54
first-digit rank                                        18
first-digit affine dimension                            36
displayed second-digit equations                        20
identically zero norm-origin equations                   2
dimension of the nonzero polar span                     18
dimension of zero-polar combinations                     2
rank contributed by those zero-polar combinations        0
common radical of all nonzero displayed forms            0
```

The two zero-polar combinations are exactly `E0(0)` and `E1(0)`, and both
their affine and constant parts vanish.  The individual polar-rank
histograms are:

| profile | rank 34 | rank 35 | rank 36 | zero rows |
|---|---:|---:|---:|---:|
| `h2-222222-0` | 1 | 6 | 11 | 2 |
| `h2-422220-0` | 1 | 9 | 8 | 2 |
| `h2-422220-1` | 0 | 5 | 13 | 2 |
| `h2-422220-2` | 2 | 6 | 10 | 2 |
| `h2-422220-3` | 1 | 5 | 12 | 2 |

## 2. Why the six low-rank combinations exist

Let

```text
K_st(b) = sum_(X,c) U_(X,s)(c+b) conjugate(U_(X,t)(c))
```

be the three-by-three phase-correlation matrix.  The displayed phase
components are

```text
E0(b) = K_00(b)+K_11(b)+K_22(b),
E1(b) = K_10(b)+K_21(b)+omega^2 K_02(b).                (4)
```

The order-three column classes are `C_j=2^j H`, with
`H={1,26,10}`.  Since

```text
-C_j = C_(j+6),             2^6 = 27 modulo 37,
```

the representative `27b` in (1) belongs to the opposite lag class.
Reversing a phase term negates its exponent, and the `omega^2` in (4)
adds a constant to it.  Neither operation changes the outer product
`b_t b_t^T` in (3).  Consequently the polar form of (1) is exactly

```text
B(T_b)
  = B(sum_(s,t) K_st(b))
  = B(sum_(X,c) V_X(c+b) conjugate(V_X(c))),            (5)

V_X(c)=U_(X,0)(c)+U_(X,1)(c)+U_(X,2)(c).
```

Thus (1) is the Hessian of the autocorrelation obtained by collapsing the
three row fibers.  The verifier constructs both sides of (5) independently
and checks equality coefficient by coefficient.

There is also an incidence factorization.  If `epsilon_v` is the signed
lambda-zero phase and `g_v` is its exponent gradient on `F_3^36`, then

```text
B(T_b)
 = sum_(X,c,s,t) epsilon_L epsilon_R
       (g_L-g_R)(g_L-g_R)^T
 = D_b^T W_b D_b.                                      (6)
```

Formula (6) explains the rank collapse: the complete forward and reverse
fiber cycles have recombined into a single signed correlation graph.

There is a sharper algebraic interpretation.  Let `alpha=zeta_9` and put
`epsilon=alpha-1`.  In characteristic three the row algebra is ramified:

```text
F_3[alpha]/(alpha^3-1) = F_3[epsilon]/(epsilon^3).       (7)
```

The invertible Hasse-coordinate change is

```text
E0+alpha E1+alpha^2 E2
 =
(E0+E1+E2)
+ epsilon (E1+2E2)
+ epsilon^2 E2.                                        (8)
```

The six forms `T_b` are exactly the residue layer `epsilon=0`; the other
twelve equations are the two nilpotent layers.  Independently, the six
column polar operators span

```text
C ~= F_27 x F_27.
```

Hence the complete eighteen-dimensional translation algebra has the form

```text
C tensor F_3[epsilon]/(epsilon^3)
 ~=
F_27[epsilon]/(epsilon^3)
 x
F_27[epsilon]/(epsilon^3),
```

and the collapsed pencil is its six-dimensional residue quotient.  The
independent verifier in
`structured_triples/verify_structured_triples.py` reconstructs this algebra
and proves the refined class-matrix plus fixed-zero-column boundary
factorization.

The six structured ranks are:

| profile | `b=1` | `2` | `4` | `8` | `16` | `32` | common-radical nullity |
|---|---:|---:|---:|---:|---:|---:|---:|
| `h2-222222-0` | 19 | 19 | 16 | 19 | 19 | 16 | 1 |
| `h2-422220-0` | 19 | 19 | 19 | 15 | 17 | 20 | 2 |
| `h2-422220-1` | 17 | 18 | 19 | 19 | 19 | 17 | 2 |
| `h2-422220-2` | 17 | 15 | 19 | 18 | 21 | 19 | 2 |
| `h2-422220-3` | 17 | 16 | 19 | 21 | 16 | 19 | 1 |

The six polar forms are independent on every profile.  For every one of
the thirty structured forms, its affine linear part is nonzero on its
polar radical:

```text
rank([B;l]) = rank(B)+1.                                (7)
```

It follows directly from (7) that each single equation `T_b=0` has exactly
`3^35` solutions: on every line in a suitable radical direction there is
one and only one solution.

## 3. Complete sparse-pencil audit

There are eighteen nonzero displayed polar forms.  Normalizing the first
nonzero coefficient to one, the number of projective combinations with
support at most three is

```text
C(18,1) + 2 C(18,2) + 4 C(18,3)
 = 18 + 306 + 3264
 = 3588.                                                (8)
```

All 3,588 combinations are checked on each profile.  Exactly six have rank
below 28, and they are precisely (1), each with coefficient pattern
`(1,1,1)`.  No search cutoff or sampled-rank inference is used.

## 4. Exact joint-fiber counts

For `a in F_3^6`, let

```text
q_a = sum_j a_j T_j.
```

If the linear part of `q_a` is nonzero on the radical of its polar matrix,
then its additive-character sum is zero.  Otherwise, translate away the
linear part and diagonalize the polar matrix by congruence:

```text
B_a ~ diag(d_1,...,d_r,0,...,0),       d_i in {1,2}.
```

The exact character sum is

```text
S(a)
 = 3^(36-r) omega^c'
   product_i (1+2 omega^(2d_i)).                        (9)
```

Fourier inversion over only `3^6=729` coefficient vectors gives every
joint fiber:

```text
N(z) = 3^-6 sum_a omega^(-a.z) S(a).                    (10)
```

All arithmetic in (9)--(10) is exact in `Z[omega]`.  The 729 counts sum to
`3^36`, and every count has the form

```text
N(z) = 3^30 + m_z 3^13.                                 (11)
```

The zero-fiber and full-distribution summaries are:

| profile | `N(0)` | zero correction `m_0` | min/max correction | distinct counts | all 729 nonempty |
|---|---:|---:|---:|---:|---|
| `h2-222222-0` | 205,891,130,500,326 | -1 | -8 / 8 | 17 | yes |
| `h2-422220-0` | 205,891,148,037,879 | 10 | -41 / 49 | 30 | yes |
| `h2-422220-1` | 205,891,197,461,892 | 41 | -121 / 107 | 64 | yes |
| `h2-422220-2` | 205,891,052,378,499 | -50 | -77 / 100 | 59 | yes |
| `h2-422220-3` | 205,891,125,717,357 | -4 | -7 / 7 | 14 | yes |

Here

```text
3^30 = 205,891,132,094,649,
3^13 =       1,594,323.
```

The six equations therefore cut the first-digit affine space almost
uniformly by the expected factor `3^6`, but they leave roughly `2.06e14`
points on every profile.  Their value is structural: they identify an
exactly countable collapsed subsystem that can be eliminated before
attacking the other twelve independent quadratic directions.

The algebra displayed above is an algebra of lag-coordinate operators, not
an action of the ramified ring on the 36-dimensional placement space.  The
companion exact audit in
`r_module_hypothesis/R_MODULE_HYPOTHESIS_FALSIFIED.md` proves that the common
self-adjoint centroid of all eighteen polar forms consists only of scalars.
In particular, the low-rank residue layer does not admit a hidden rank-two
module parametrization followed by two linear Hensel lifts.

## 5. Certificates

The semantic hashes of the generated certificates are

```text
complete second-digit forms
b8958ea3d3179aec2ae73c3e1bbb2ac76fd4f668a31422a3863f74c41bcafd60

collapsed sparse pencil and all 729 joint fibers
91cf19a2a9099d86908230df4d179cca877f1990be2a0c19a379235fcaa25615

ramified structured-triple algebra theorem
aa6dbb0c3272e8695e3c8beff8381702a9f7f5a2505716138086d8074aa20d5c
```

The SHA-256 of the compact stored certificate
`phase_second_digit_certificate.json` is

```text
c0e9d4670ba8065b8e8a6435eb7ee5daaf45f3418ff81462e0d2a01c8f684fcf.
```

## Reproduction

```text
python3 phase_second_digit/verify_phase_second_digit.py
python3 phase_second_digit/verify_phase_second_digit_pencil.py
python3 -m unittest -v \
  phase_second_digit/test_phase_second_digit.py
```

The first verifier takes about five seconds.  The complete sparse-pencil
and Gauss audit takes about 70 seconds and peaked below 30 MB resident
memory on the reference run.  Both use exact arithmetic and the Python
standard library only.
