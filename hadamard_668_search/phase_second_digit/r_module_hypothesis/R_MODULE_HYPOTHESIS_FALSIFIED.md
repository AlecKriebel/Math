# The free rank-two ramified-module hypothesis is false

## Status

Let

```text
C = F_27 x F_27,
R = C[epsilon]/(epsilon^3).
```

The algebra `R` has dimension eighteen over `F_3`, so the
36-dimensional translation space `V` of each first-digit affine profile
has the same dimension as `R^2`.  Dimension alone, however, is not a
module theorem: any 36-dimensional vector space can be identified
noncanonically with `R^2`.

The mathematically useful hypothesis was stronger:

1. `V` has a compatible free rank-two `R` action;
2. the eighteen second-digit quadratics are the coordinates of an
   `R`-valued quadratic norm or conic;
3. in the Hasse basis, a regular residue solution lifts through the two
   nilpotent layers by linear equations.

Exact polar algebra falsifies this hypothesis for all five exact `h=2`
profiles.  Three independent invariants disagree:

```text
required common T0 radical dimension:      at least 24
actual common T0 radical dimension:        1 or 2

required compatible centroid dimension:   at least 18
actual compatible centroid dimension:      1

required unimodular scalar polar ranks:    multiples of 6
actual scalar polar ranks:                 include 15,17,19,21,35,...
```

Therefore the standard ramified Hensel parametrization does not exist.
This is a falsification of a proposed shortcut, not an exclusion of an
`h=2` profile and not a count of the complete second-digit solution set.

## 1. The proposed Hasse filtration

At one reversal-independent lag, use

```text
alpha=1+epsilon.
```

Then the three second-digit coordinates transform invertibly as

```text
E0+alpha E1+alpha^2 E2
 =
T0 + epsilon T1 + epsilon^2 T2,                        (1)

T0=E0+E1+E2,
T1=E1+2E2,
T2=E2.                                                 (2)
```

At this digit, the displayed opposite-lag coordinate `E1(27b)` supplies
`E2(b)`, so (2) is an exact transformation of the eighteen displayed
quadratics into three layers of six.

Suppose `V=R^2`.  Its canonical nilpotent flag would be

```text
V superset epsilon V superset epsilon^2 V superset 0

dimensions:       36,          24,              12, 0. (3)
```

For an `R`-valued quadratic `Q`, the residue coefficient `T0` depends only
on `V/epsilon V`, which has dimension twelve.  Consequently:

```text
epsilon V lies in the common polar radical of all six T0 coordinates,
rank B(T0_j) <= 12.                                    (4)
```

The first nilpotent coefficient `T1` is linear in the first lift layer
after the residue variables are fixed and is independent of the top lift
layer.  Homogeneously this requires

```text
epsilon^2 V lies in the common polar radical of all six T1 coordinates,
rank B(T1_j) <= 24.                                    (5)
```

Both necessary conditions are invariant under every change of the
36-dimensional `F_3` coordinate basis.

## 2. Exact Hasse-layer ranks

The reconstructed ranks and common radical nullities are:

| profile | `T0` ranks | common `T0` radical | `T1` ranks | common `T1` radical | `T2` ranks | common `T2` radical |
|---|---|---:|---|---:|---|---:|
| `h2-222222-0` | `19,19,16,19,19,16` | 1 | `35,35,35,35,35,33` | 0 | `35,36,36,36,35,36` | 0 |
| `h2-422220-0` | `19,19,19,15,17,20` | 2 | `28,30,30,30,30,30` | 0 | `35,36,35,36,36,35` | 0 |
| `h2-422220-1` | `17,18,19,19,19,17` | 2 | `30,30,30,30,30,30` | 0 | `36,36,36,36,36,35` | 0 |
| `h2-422220-2` | `17,15,19,18,21,19` | 2 | `28,30,28,30,30,30` | 0 | `36,35,36,36,36,36` | 0 |
| `h2-422220-3` | `17,16,19,21,16,19` | 1 | `33,35,35,35,35,35` | 0 | `36,36,36,36,36,35` | 0 |

Thus:

- every `T0` profile violates the rank bound in (4);
- the common `T0` radical is smaller than required by 22 or 23 dimensions;
- every `T1` profile violates (5);
- the six `T1` polars jointly have no radical at all.

The failure already occurs in the homogeneous quadratic terms.  Changing
the affine origin or completing squares cannot repair it.

This also explains why the low-rank `T0` discovery does not produce an
ordinary Hensel lift.  Its ranks 15 through 21 are low relative to 36, but
they are too high for a quadratic living on a twelve-dimensional residue
quotient.

## 3. The compatible-centroid obstruction

The filtration test uses the proposed identification of `T0,T1,T2`.
There is a stronger coordinate-free obstruction.

Let `B_1,...,B_18` be the symmetric polar matrices of the full
eighteen-dimensional second-digit pencil on `V`.  Define their common
self-adjoint centroid

```text
Cent(B)
 =
{A in End_F3(V):
 A^T B_i = B_i A for i=1,...,18}.                      (6)
```

If an `R` action and an `R`-balanced polar form `b:V x V -> R` existed,
then multiplication by every `s in R` would satisfy

```text
b(sx,y)=s b(x,y)=b(x,sy).
```

Applying any of the eighteen `F_3` coordinate functionals on `R` would put
the multiplication operator `L_s` in (6).  Since a free `R` action is
faithful,

```text
R embeds into Cent(B),
dim_F3 Cent(B) >= 18.                                  (7)
```

For each exact profile, the verifier writes (6) as an exact linear system
in the `36^2=1,296` entries of `A`.  Its rank is

```text
1,295,
```

so

```text
dim_F3 Cent(B)=1.                                      (8)
```

The identity endomorphism is checked directly, hence (8) says that the
centroid consists exactly of the three scalar maps.  There is no
compatible nontrivial algebra action, let alone a faithful
eighteen-dimensional copy of `R`.

This obstruction does not assume the Hasse ordering in (1).

## 4. The norm-rank obstruction

There is a third check if the proposed `R`-valued conic is assumed
unimodular.  One local component

```text
F_27[epsilon]/(epsilon^3)
```

has multiplication ranks over `F_3`

```text
9,6,3,0
```

according as an element has epsilon valuation `0,1,2,infinity`.  On the
two-component product `R`, multiplication ranks are therefore multiples
of three from zero through eighteen.

For a nondegenerate binary `R`-polar form and a scalar functional
represented by `a in R`, the induced `F_3` polar rank is

```text
2 rank_F3(multiplication by a).
```

The only possible ranks are

```text
0,6,12,18,24,30,36.                                   (9)
```

The actual coordinate forms include many odd ranks, including 35, and the
residue combinations include 15, 17, 19, and 21.  This independently
contradicts a unimodular binary `R` norm.

## 5. Consequence

There is no 12-variable residue conic followed by two linear
twelve-variable lift stages.  In particular, regularity of a `T0`
solution cannot imply automatic linear lifting through `T1` and `T2`:
the actual `T0` equations already involve almost every direction of the
36-dimensional space, and `T1` has no common unused lift direction.

The ramified Hasse basis remains useful as an organizational decomposition,
but the remaining layers must be handled by general quadratic methods—for
example conditional Schur complements or character sums—not by module
Hensel theory.

No assertion is made here about whether the full eighteen equations have a
solution.  The earlier exact 729-character audit proves that `T0` alone is
surjective with roughly `3^30` points in every joint fiber.

## 6. Reproduction

From `hadamard_668_search`:

```text
python3 \
  phase_second_digit/r_module_hypothesis/verify_r_module_hypothesis.py
```

The verifier:

- reconstructs the five exact profile affine spaces and all eighteen
  independent polar forms;
- checks the Hasse transform and the three rank tables above;
- verifies that the full polar span has dimension eighteen;
- solves all common-centroid equations by exact packed `F_3` elimination;
- cross-checks the packed rank primitive against the established dense
  eliminator on 36 deterministic fixtures.

The reference run used about 28 MB maximum resident memory and no phase
assignment enumeration.
