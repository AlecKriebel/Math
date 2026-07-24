# Exact exclusion of the five-norm-nine profile shell

## Status

The order-three `LP(333)` profile energy equation is

```text
n_3+3 n_9=18.
```

The shell immediately below the norm-nine endpoint is therefore

```text
(n_9,n_3,n_0)=(5,3,16).
```

This shell is now excluded exactly.

The existing opposite-class equation first forces all three norm-three
letters into one quartet.  Fixing those letters makes every nonzero-lag
correlation modulo nine affine in the five norm-nine letters.  A complete
additive-signature join reduces

```text
34,634,136 aggregate/local assignments
```

to

```text
552 modulo-nine assignments.
```

Detached exact integer correlation rejects all 552.  Combined with the
separate exact exclusion of the `n_9=6` endpoint, this strengthens the
profile constructor to

```text
n_9 <= 4.
```

This is an exclusion of two energy shells, not an `LP(333)` construction or
an `H(668)`.

## 1. Profile alphabet and energy

For a composition `p=(p_0,p_1,p_2)` of three, write

```text
z(p)=p_0+p_1 omega+p_2 omega^2,
omega^2+omega+1=0.
```

The ten profile letters split as follows:

| norm | number of letters | description |
|---:|---:|---|
| `0` | 1 | the zero letter |
| `3` | 6 | Eisenstein associates of `1-omega` |
| `9` | 3 | three times a cube root of unity |

The normalized profile energy is 54, so

```text
3 n_3+9 n_9=54.
```

At `n_9=5`, exactly three letters have norm three and sixteen have norm
zero.

## 2. Universal quartet localization

For an opposite-class ordered pair, define

```text
f(p,q)=conjugate(z(p))+z(q) modulo 3.
```

The existing necessary condition on

```text
(A_j,A_(j+6),B_j,B_(j+6))
```

is

```text
f(A_j,A_(j+6))=f(B_j,B_(j+6)).                 (1)
```

There are 3,334 legal quartets among the `10^4` possible quartets.  Their
complete weight census is:

| norm-three letters | norm-nine letters | legal quartets |
|---:|---:|---:|
| 0 | 0 | 1 |
| 0 | 1 | 12 |
| 0 | 2 | 54 |
| 0 | 3 | 108 |
| 0 | 4 | 81 |
| 2 | 0 | 108 |
| 2 | 1 | 648 |
| 2 | 2 | 972 |
| 3 | 0 | 216 |
| 3 | 1 | 648 |
| 4 | 0 | 486 |

In particular, no legal quartet contains exactly one norm-three letter.
Since the shell contains three such letters in total, a `2+1` split is
impossible.  All three must occupy one opposite-class quartet.

Set every norm-nine letter temporarily to the zero letter.  The resulting
three-medium assignment is called its **medium frame**.  This projection is
unique.  It preserves (1), because both the zero letter and every norm-nine
letter are coefficientwise zero modulo three.

There are

```text
6 opposite-class positions x 216 local frames = 1,296 medium frames.
```

If `M` is the four-coordinate aggregate of a medium frame and `T` is one of
the 22 exact row-sum targets, the five remaining high coefficients are
multiples of three.  Hence

```text
T=M modulo 3.                                  (2)
```

Exactly 1,944 medium-frame/target pairs satisfy (2).  Only six targets
occur, each on 324 frames:

```text
(-3,-3,-4,-2), (-3,-3,-2, 2),
( 0, 3,-4,-2), ( 0, 3,-2, 2),
( 4,-1, 0, 0), ( 5, 1, 0, 0).
```

## 3. Frame symmetry and completeness

The exact profile group

```text
G=C6 x C2_A x C2_B
```

acts on medium-frame/target pairs.  The verifier replays the universal
2,200,368-monomial covariance proof for this action, checks that all 1,944
pairs are closed under it, and obtains

```text
90 frame/target orbits:
72 of size 24 and 18 of size 12.
```

The object being quotiented here is a **medium-frame/target pair**, not a
full profile assignment.  For each orbit representative, the additive join
enumerates its complete set of high-letter completions.  Only after that
complete set is known does the verifier apply all 24 group elements and
deduplicate full assignments.

This distinction matters for a size-12 frame orbit: its nontrivial
stabilizer need not fix an individual high-letter completion.  The
implementation makes no such assumption.

## 4. Affine correlation modulo nine

Fix a medium frame `m`.  A norm-nine letter changes a profile coefficient
by `3u`, where `u` is an Eisenstein unit after the fixed channel/parity sign
is included.  Let `h_1,...,h_5` be the five one-slot high corrections.

For either channel, every product

```text
h_i conjugate(h_k)
```

is divisible coefficientwise by nine.  Expanding the autocorrelation
therefore gives, at every nonzero lag,

```text
D(m+h_1+...+h_5)
 =
D(m)+sum_i (D(m+h_i)-D(m))             modulo 9.       (3)
```

Equation (3) includes every term:

- `D(m)` contains the zero/medium and medium/medium terms;
- `D(m+h_i)-D(m)` contains both orientations of every
  high/zero and high/medium term;
- all omitted high/high cross terms vanish modulo nine.

The local condition (1) says that every nonzero `D_j(m)` is divisible by
three.  Each one-high increment in (3) is also divisible by three.  Dividing
(3) by three produces twelve prime-field coordinates:

```text
sum_i delta_i
 =
-D_j(m)/3                              modulo 3,
j=0,...,5, in the basis 1,omega.                       (4)
```

Only six class representatives are needed because

```text
D_(j+6)=conjugate(D_j).
```

The aggregate equation is retained over the integers, not merely modulo
three:

```text
sum_i h_i/3=(T-M)/3 in Z^4.                         (5)
```

Finally, exactly five slots must be active.

## 5. Complete additive-signature join

For a fixed medium-frame/target representative, 21 slots remain.  Each slot
has four states:

```text
zero, or one of the three norm-nine letters.
```

The verifier divides them into blocks of 10 and 11.  Every partial
assignment of at most five active slots receives the exact signature

```text
(active count, integer aggregate in Z^4,
 twelve correlation coordinates in F_3).             (6)
```

Complementary signatures are joined to enforce:

```text
total active count = 5,
the exact aggregate (5),
all twelve congruences (4).
```

Before the correlation coordinates in (6) are used, the same enumeration
reproduces the complete aggregate/local census:

| target | assignments |
|---|---:|
| `(-3,-3,-4,-2)` | 5,748,834 |
| `(-3,-3,-2, 2)` | 5,748,834 |
| `( 0, 3,-4,-2)` | 5,748,834 |
| `( 0, 3,-2, 2)` | 5,748,834 |
| `( 4,-1, 0, 0)` | 5,819,400 |
| `( 5, 1, 0, 0)` | 5,819,400 |
| **total** | **34,634,136** |

Adding all six reversal-independent modulo-nine correlation equations
leaves:

| target | assignments |
|---|---:|
| `(-3,-3,-4,-2)` | 42 |
| `(-3,-3,-2, 2)` | 42 |
| `( 0, 3,-4,-2)` | 42 |
| `( 0, 3,-2, 2)` | 42 |
| `( 4,-1, 0, 0)` | 192 |
| `( 5, 1, 0, 0)` | 192 |
| **total** | **552** |

At the representative-frame level there are 30 completions, supported on
14 of the 90 frame/target orbits.  Explicit full-orbit expansion gives the
552 assignments in the table; the total is not inferred by multiplying one
representative by 24.

## 6. Detached exact closure

For each of the 552 assignments, the verifier independently reconstructs
the two 37-column Eisenstein words and evaluates every physical lag using
exact integer arithmetic.  It therefore replays

```text
552 x 37 = 20,424
```

physical correlations.  It verifies:

1. the exact aggregate target;
2. the shell counts `(5,3,16)`;
3. all six local quartet equations;
4. origin energy zero;
5. divisibility of every nonzero correlation by nine;
6. equality with the established invariant profile-correlation routine.

The exact failure census is:

| bad nonzero classes | assignments |
|---:|---:|
| 6 | 24 |
| 10 | 144 |
| 12 | 384 |

No assignment has zero bad classes.  Thus the complete shell

```text
(n_9,n_3,n_0)=(5,3,16)
```

is excluded.

The complete certificate SHA-256 is

```text
51c25095c92ba49c4c7c493373bb68f7d9c0c4671d65490413ae140c2b0aad69
```

## 7. Search consequence

Together with the independent endpoint exclusion `n_9 != 6`, every exact
order-three profile-zero constructor may impose

```text
n_9 <= 4.
```

The useful general mechanism is not the finite census by itself.  On an
energy shell with only a few letters outside a highly divisible alphabet,
project to the low-valuation letters first.  The remaining correlation
problem can become an exact fixed-cardinality additive join modulo a higher
ideal, while the row-sum aggregate remains integral.

## Reproduction

```text
python3 verify_lp333_order3_profile_penultimate_shell.py
python3 -m unittest -v test_lp333_order3_profile_penultimate_shell.py
```

The verifier uses exact integer arithmetic and the Python standard library
plus the repository's previously verified profile modules.  A full replay
uses well below 1 GB of memory.
