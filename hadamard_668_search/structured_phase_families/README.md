# Exact structured phase-family audit on the five shell-two orbits

## Status

Eight named structured placement programs have been tested exactly on all
five certified `(n_9,n_3,n_0)=(2,12,10)` profile orbits:

- four low-period calibration families;
- three opposite-class-twisted families designed to escape fixed common
  multipliers;
- the complete family obtained by assigning the two channels independently
  to minimal modules of the certified `F_27 x F_27` class-operator algebra.

No placement outside the recently excluded fixed common-multiplier
supergroups passes the second placement digit.

One point in the `opposite_helical_c4` family passes the second digit, but
it is fixed by

```text
H_8=<10,64>,
```

and therefore lies in the order-six common-multiplier family excluded by
Ramos--Hulak--de Queiroz, arXiv:2607.20765.  Direct lambda-adic replay also
shows that this point fails the very next digit.  It is a useful positive
control for the digit-two equations, not a viable Legendre-pair lift.

These are exact exclusions only of the named families.  They do not exclude
any of the five profile orbits in general, do not exclude `LP(333)`, and do
not construct or exclude `H(668)`.

## 1. Coordinates and exact gates

Write an active placement trit as

```text
u_(X,j,s) in F_3,
```

where `X` is channel `A` or `B`, `j in Z/12` is the cyclotomic-class
index, and `s in F_3` is the row residue.  Put

```text
x = j mod 3,
p = (-1)^j,
h_j =  1 for 0 <= j < 6,
     = -1 for 6 <= j < 12.
```

For every linear feature family `u=M theta`, the verifier first substitutes
into the certified first placement digit:

```text
A M theta = b over F_3.
```

Coefficient/augmented ranks either give an explicit `0=1` certificate or
an affine parameter space.  Kernel images are reduced to an independent
basis, so each distinct structured placement is enumerated exactly once.
Every such point is evaluated in all twenty exact second-digit quadratics.
The canonical closest point in each nonempty intersection is replayed using
exact Eisenstein arithmetic.

There is no SAT solver, random sampling, floating-point arithmetic, or
timeout inference.

## 2. Fixed-common-multiplier audit

The recent multiplier classification leaves `<10>` open but excludes each
minimal proper fixed common-multiplier supergroup containing it.  In the
paper's stable IDs and generators these are:

| subgroup ID | extra generator |
|---:|---:|
| 8 | 64 |
| 11 | 112 |
| 12 | 46 |
| 13 | 7 |
| 14 | 16 |

The verifier derives the exact affine action of every generator on the 54
placement trits, including the canonical zero column.  Inclusion-exclusion
then counts the intersection with the five supergroups.

On profile orbits `h2-222222-0` and `h2-422220-3`, the fixed labelled
profile itself is incompatible with every one of the five proper
supergroups.  On each of the other three profiles, only ID 8 is compatible.

All first-digit survivors in the four low-period families below turn out to
be fixed by ID 8:

```text
quadratic_c3:
  u_X=P_X(j mod 3,s),                  total degree <=2

crt4_additive:
  u_X=F_X(j mod 4)+G_X(s)

antipodal_additive:
  u_X=F_X(j mod 6)+G_X(s)

cocyclic_multiaffine:
  u_X in span{1,x,p,xp,s,xs,ps,xps}.
```

Their second-digit exclusions are valid, but they add no coverage beyond
the July 2026 fixed-multiplier theorem.  They are retained as exact
calibration controls.

## 3. Opposite-class-twisted families

Multiplication by `h_j` makes the added component anti-invariant under
`j -> j+6`.  This deliberately breaks the only proper common multiplier
compatible with the three repeated profiles.

### 3.1 Ternary planar-quadratic envelope

```text
u_X(j,s)=P_X(x,s)+h_j Q_X(x,s),
```

where `P_X,Q_X` are arbitrary total-degree-at-most-two polynomials over
`F_3`.  A scalar quadratic `Q:F_3^2 -> F_3` has balanced nonzero
derivatives precisely when its polar matrix is nonsingular.  Hence this
envelope contains every quadratic perfect-nonlinear/balanced-derivative
choice for the opposite component, as well as a larger control family.

| profile | digit-one points | outside all five supergroups | digit-two points |
|---|---:|---:|---:|
| `h2-222222-0` | 729 | 729 | 0 |
| `h2-422220-0` | 729 | 0 | 0 |
| `h2-422220-1` | 2,187 | 1,458 | 0 |
| `h2-422220-2` | 729 | 0 | 0 |
| `h2-422220-3` | 729 | 729 | 0 |

### 3.2 Opposite-twisted six-class family

```text
u_X(j,s)
 =P_X(x,s)+h_j(F_X(j mod 6)+G_X(s)),
```

with `P_X` quadratic.

| profile | digit-one points | outside all five supergroups | digit-two points |
|---|---:|---:|---:|
| `h2-222222-0` | 59,049 | 59,049 | 0 |
| `h2-422220-0` | 19,683 | 18,954 | 0 |
| `h2-422220-1` | 19,683 | 18,954 | 0 |
| `h2-422220-2` | 19,683 | 18,954 | 0 |
| `h2-422220-3` | 59,049 | 59,049 | 0 |

### 3.3 Opposite helical `C4` family

The channels use opposite class-row helices:

```text
u_A=P_A(x,s)+h_j H_A(j+s mod 4,s),
u_B=P_B(x,s)+h_j H_B(j-s mod 4,s),
```

where each `H_X(y,s)=F_X(y)+G_X(s)`.

| profile | digit-one points | outside all five supergroups | digit-two points |
|---|---:|---:|---:|
| `h2-222222-0` | 729 | 729 | 0 |
| `h2-422220-0` | 59,049 | 0 | **1** |
| `h2-422220-1` | 59,049 | 0 | 0 |
| `h2-422220-2` | 59,049 | 0 | 0 |
| `h2-422220-3` | 729 | 729 | 0 |

The unique digit-two point has trit hash

```text
854a5af491580697ce9f91f3dbe93b06f5ec79a3dbe918a055aac9fb75377325.
```

It is ID-8 fixed.  Its displayed digit-three residual is

```text
(0,0,0,0,0,0,0,1,0,1,0,0,2,0,0,1,0,0,2,0),
```

so it fails six rows immediately at the next digit.

The three tables are per-family counts.  Their point sets can intersect;
the totals must not be added and described as a disjoint union.

## 4. The `F_27 x F_27` minimal-submodule family

The six exact class polar operators span

```text
F_27 x F_27
```

on `F_3^12`.  The two central idempotents have six-dimensional images.
Each image is two-dimensional over `F_27`, so its minimal nonzero invariant
submodules are the 28 points of

```text
P^1(F_27).
```

The verifier independently reconstructs all 28 submodules in each
component, for 56 total, and proves invariance under all six class
operators.

For one fixed channel and row residue, inactive profile classes are filled
with zero and the resulting supported class vector is intersected with a
chosen minimal submodule.  Channel `A` uses one submodule across its three
residues; channel `B` independently uses another.  Thus all

```text
56^2 = 3,136
```

channel-asymmetric submodule pairs are tested on every profile.

| profile | compatible submodule pairs | distinct digit-one points | outside all five supergroups | digit-two points |
|---|---:|---:|---:|---:|
| `h2-222222-0` | 0 | 0 | 0 | 0 |
| `h2-422220-0` | 4 | 108 | 0 | 0 |
| `h2-422220-1` | 58 | 221 | **6** | 0 |
| `h2-422220-2` | 58 | 107 | 0 | 0 |
| `h2-422220-3` | 0 | 0 | 0 | 0 |

This is the family most directly tied to the newly discovered class
algebra.  Its six genuinely non-multiplier points all fail digit two.

## 5. Certificates and reproduction

The semantic SHA-256 hashes are:

```text
feature-family certificate:
07ca938d874c702290eb5923d30d7e19c80c3947aa9c8d26ef8ace123c572784

F27-minimal-submodule certificate:
15978fe122ffaaba6a752ac6d5995aefabe5b0ba89fd200bb990408189aab61f

compact summary file:
f9b0b61ded5f1b9ca398442c6be5ed8e1363b668d10d4fb7a9d0ecb270fb465c

feature-family verifier source:
22822986c04a806d68ea58d173e6265ea9eeee3dd87a82dafcbe48b00a7ce740

F27-submodule verifier source:
8b408d2c0860b628935b971309f82c8c8613d99e77eee1c0649f6cc668b8ca3d
```

Run from `hadamard_668_search`:

```sh
python3 structured_phase_families/verify_structured_phase_families.py
python3 structured_phase_families/verify_f27_submodule_families.py
python3 -m unittest -v \
  structured_phase_families/test_structured_phase_families.py
```

The reference combined run takes under one minute and peaks below 32 MB
resident memory.
