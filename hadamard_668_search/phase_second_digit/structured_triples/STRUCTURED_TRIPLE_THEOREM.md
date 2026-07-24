# The ramified row-collapse subpencil in the second placement digit

## Status

For each of the six reversal-independent nonzero column-lag classes, put

```text
T_j = E0(b_j) + E1(b_j) + E1(27 b_j),
b_j = 1,2,4,8,16,32.                                  (1)
```

The unexpectedly low ranks of these six quadratic forms on the five exact
`h=2` profiles are systematic.  They are the row-residue image of an
eighteen-dimensional ramified translation algebra:

```text
F_27[epsilon]/(epsilon^3)
  x
F_27[epsilon]/(epsilon^3).                             (2)
```

The row-residue quotient of (2) is the six-dimensional algebra

```text
F_27 x F_27.                                           (3)
```

The polar form of (1) factors through (3), with a diagonal correction
supported only at the two nonzero classes adjacent to the fixed zero
column.  This explains the observed ranks between 15 and 21 after
restriction to the 36-dimensional first-digit affine space.

The affine terms do **not** turn these low ranks into an obstruction.
Instead, every individual `T_j` has an explicit radical translation on
which it changes by one.  Hence every scalar right-hand side occurs exactly

```text
3^35 = 50,031,545,098,999,707
```

times.  Moreover, exact Fourier inversion of only `3^6=729` quadratic
Gauss sums proves that the joint map

```text
(T_0,...,T_5): F_3^36 -> F_3^6
```

is surjective for all five profiles.  This checkpoint gives a strong
lossless parametrization, not an exclusion and not an `LP(333)`.

## 1. Why the three displayed coordinates occur

Let `alpha=zeta_9`, `omega=alpha^3`, and `lambda=1-omega`.  The exact
three-fiber factorization is

```text
sum_X W_X W_X^*
 = E0 + alpha E1 + alpha^2 E2,

E2 = omega^2 E1^*.                                    (4)
```

At a column lag `b`,

```text
E2(b) = omega^2 conjugate(E1(-b)).                     (5)
```

Since

```text
conjugate(lambda) = -omega^2 lambda,
omega^2 conjugate(lambda^2) = lambda^2,
```

the second `lambda` digit of the right-hand side of (5), once its two lower
digits vanish, is the second digit of `E1(-b)`.  Also

```text
27 belongs to -H in F_37^*,
```

so order-three invariance identifies `E1(27b)` with `E1(-b)`.  Therefore
(1) is exactly the second digit of

```text
E0(b)+E1(b)+E2(b).                                    (6)
```

Setting `alpha=1` in (4) gives (6).  Thus `T_j` is the norm equation after
collapsing the three row fibers.

This also identifies the complete row algebra at this digit.  In
characteristic three,

```text
F_3[alpha]/(alpha^3-1)
 = F_3[epsilon]/(epsilon^3),     epsilon=alpha-1.       (7)
```

The map `alpha -> 1` is its unique residue-field quotient.  Tensoring (7)
with the six-dimensional column-lag algebra (3) gives (2).  Consequently
the six low triples are the residue layer of the full eighteen-dimensional
pencil; they cannot be treated as six accidental sparse combinations.

There is a useful invertible Hasse-coordinate rewrite:

```text
E0+alpha E1+alpha^2 E2
 =
(E0+E1+E2)
+ epsilon (E1+2E2)
+ epsilon^2 E2.                                       (8)
```

The first six coordinates in (8) are precisely the `T_j`.  The remaining
twelve equations are the two nilpotent row layers.

## 2. Exact polar factorization

For an active phase at channel `X`, physical column `c`, and row fiber `s`,
write

```text
sigma_(X,c,s) omega^(L_(X,c,s)),
```

and let `a_(X,c,s)` be the linear slope vector of `L` in the 54 ambient
placement trits.  Define

```text
S_(X,c) = sum_s sigma_(X,c,s),

g_(X,c) = sum_s sigma_(X,c,s) a_(X,c,s),

H_(X,c) = sum_s sigma_(X,c,s)
                    a_(X,c,s) a_(X,c,s)^T.             (9)
```

The polar contribution of one left/right phase pair is

```text
sigma_left sigma_right
(a_left-a_right)(a_left-a_right)^T.
```

Summing all nine row-fiber pairs at lag `b` gives

```text
sum_c [
  S_(X,c) H_(X,c+b)
 +S_(X,c+b) H_(X,c)
 -g_(X,c+b) g_(X,c)^T
 -g_(X,c) g_(X,c+b)^T
].                                                     (10)
```

Every nonzero-column profile is a composition of weight three.  If `n_1`
and `n_2` count its entries equal to one and two, its signed active count
is, up to a common complement sign,

```text
n_1-n_2 = n_1+2n_2 = 0 in F_3.                        (11)
```

Thus `S_(X,c)=0` for every nonzero `c`.  The fixed zero column has

```text
S_(A,0)=S_(B,0)=-1.
```

Let `G_X` be the `12 x 54` matrix whose class row is `g_(X,c)`, and let
`M_j` be the symmetric order-three cyclotomic transition matrix at `b_j`.
Equation (10) collapses to the exact identity

```text
B(T_j)
 =
- sum_(X=A,B) [
    G_X^T M_j G_X
    + H_(X,b_j)
    + H_(X,-b_j)
  ].                                                   (12)
```

The first term in (12) has rank at most twelve per channel.  The boundary
term is diagonal and is confined to the active fibers of the two opposite
profiles at `b_j` and `-b_j`.  This proves the structural rank collapse.

Independently reconstructing the six `M_j` gives

```text
M_0+...+M_5 = 2 I_12,

span_F3(M_0,...,M_5) ~= F_27 x F_27,                   (13)
```

with projective rank census

```text
rank 6:   26,
rank 12: 338.
```

The verifier checks (12) first in all 54 ambient trits and then pulls it
back through the canonical 36-dimensional kernel basis of the first
placement digit.  It agrees exactly with the three-row combinations
derived directly from the Eisenstein phase terms on all thirty
profile/lag pairs.

## 3. The affine term gives a parametrization

On the first-digit affine space, write

```text
T_j(y)=c_j+l_j y+(1/2)y^T B_j y.                       (14)
```

For every one of the thirty forms, exact linear algebra produces a vector

```text
v_j in kernel(B_j),        l_j v_j=1.                  (15)
```

Therefore

```text
T_j(y+t v_j)=T_j(y)+t            for all t in F_3.     (16)
```

Every orbit of the translation generated by `v_j` contains exactly one
point satisfying any prescribed scalar equation `T_j=r`.  Equation (16)
is stronger than a positivity bound: it is a direct, lossless
35-parameter description of every scalar fiber.

The six forms do not share six such directions—their common polar radical
has dimension only one or two, depending on the profile—so (16) cannot
simply be applied six times independently.  Instead the complete joint
fiber count uses character orthogonality.

## 4. Exact character-sum audit

For a coefficient vector `a in F_3^6`, let

```text
T_a=sum_j a_j T_j.
```

The verifier evaluates the exact quadratic Gauss sum

```text
S(a)=sum_(y in F_3^36) omega^(T_a(y))                  (17)
```

by symmetric Gaussian elimination.  No phase point is enumerated.  For a
joint target `r in F_3^6`,

```text
# {y:T(y)=r}
 =
3^(-6) sum_(a in F_3^6) omega^(-a.r) S(a).             (18)
```

The Gauss-sum primitive is separately replayed against all 729 affine
quadratics in two variables.

The complete results are:

| profile | six ranks | balanced projective pencils / 364 | minimum scalar fiber over every pencil and RHS | joint zero fiber | joint fiber minimum | joint fiber maximum |
|---|---|---:|---:|---:|---:|---:|
| `h2-222222-0` | `19,19,16,19,19,16` | 356 | 50,031,543,936,738,240 | 205,891,130,500,326 | 205,891,119,340,065 | 205,891,144,849,233 |
| `h2-422220-0` | `19,19,19,15,17,20` | 348 | 50,031,541,612,215,306 | 205,891,148,037,879 | 205,891,066,727,406 | 205,891,210,216,476 |
| `h2-422220-1` | `17,18,19,19,19,17` | 350 | 50,031,534,638,646,504 | 205,891,197,461,892 | 205,890,939,181,566 | 205,891,302,687,210 |
| `h2-422220-2` | `17,15,19,18,21,19` | 345 | 50,031,534,638,646,504 | 205,891,052,378,499 | 205,891,009,331,778 | 205,891,291,526,949 |
| `h2-422220-3` | `17,16,19,21,16,19` | 355 | 50,031,544,711,579,218 | 205,891,125,717,357 | 205,891,120,934,388 | 205,891,143,254,910 |

All 364 projective combinations have positive fibers for all three scalar
right-hand sides.  More strongly, every one of the 729 joint targets is
represented for every profile.  The average joint fiber is

```text
3^30 = 205,891,132,094,649.
```

Every exact fiber count has the sharper form

```text
3^30 + m 3^13,                 m in Z.                 (19)
```

Across the five rows of the table, the respective minimum/maximum
deviation multipliers `m` are

```text
[-8,8], [-41,49], [-121,107], [-77,100], [-7,7].
```

Hence neither a single combination in the row-residue subpencil nor the
complete six-coordinate row-collapse layer can exclude an `h=2` profile.

## 5. Consequence for the next attack

The useful conclusion is organizational:

1. Replace the original eighteen coordinates by the ramified Hasse basis
   in (8).
2. Handle the six residue coordinates `T_j` by (16) or the exact
   729-character transform (18).
3. Study the two six-coordinate nilpotent layers conditionally on that
   fiber.

This respects the actual local algebra and avoids both unrestricted
`3^36` phase enumeration and blind search through arbitrary quadratic
combinations.  The residue layer alone removes essentially six trits but
leaves about `3^30` points, so it is a compression theorem rather than a
near construction.

## 6. Reproduction

From `hadamard_668_search`:

```text
python3 \
  phase_second_digit/structured_triples/verify_structured_triples.py
```

The reference verifier reconstructs the five exact profiles and the
canonical first-digit affine spaces, proves (12) independently of the
interpolated quadratics, audits (13), checks explicit radical-translation
witnesses, enumerates only the 364 projective pencils and 729 additive
characters, and performs no phase assignment search.
