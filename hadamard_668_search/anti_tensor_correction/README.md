# Algebraic second anti-tensor correction at the 18/20 near misses

## Outcome

The two profiles attaining `18/20` in the certified rank-one anti-tensor
audit have been tested by an exact, local rank-two correction calculation.
No correction reaches `19/20` or `20/20`.

This is a genuine low-rank elimination, not a census of the approximately
327 billion full rank-two chart incidences.  It decides the complete
fixed-background correction star at each of the three certified near-miss
points.

## Correction problem

The original family has

```text
u_X(j,s) = P_X(j mod 3,s) + h_j F_X(j mod 6) G_X(s).
```

At a pinned `18/20` point `u`, add a second separable component

```text
v_X(j,s) = h_j F'_X(j mod 6) G'_X(s).                 (1)
```

The quadratic background and the first tensor component are held fixed.
Each `G'_X` ranges over all 13 projective directions in `F_3^3`, including
the constant direction, and each `F'_X` is arbitrary.  Zero coefficients
include corrections in only one channel.  Consequently all possible
corrections in (1) are covered by `13^2=169` direction-pair charts.

Let `A u=b` be the twenty placement-digit-one equations and let `T_G` be
the `54 by 12` feature matrix for a fixed direction pair.  A correction
must satisfy

```text
A T_G f = 0.
```

The verifier eliminates `f`, takes the distinct image in the 54 trit
coordinates, and only then evaluates

```text
q_i(u+v)=0,  i=0,...,19
```

in the exact placement-digit-two quadratics.

The linear elimination is very strong:

| profile | chart image dimensions | chart incidences | distinct corrections |
|---|---|---:|---:|
| `h2-422220-2` | `0^114, 1^44, 2^10, 3^1` | 363 | 175 |
| `h2-422220-3` | `0^164, 1^5` | 179 | 11 |

Here `d^n` means that `n` charts have a `d`-dimensional correction image.

## Exact local obstruction

| profile | base hash prefix | missing rows | best after correction | exact `20/20` |
|---|---|---|---:|---:|
| `h2-422220-2` | `c9c276af…` | 8, 16 | 18 | 0 |
| `h2-422220-2` | `6f6a5948…` | 10, 14 | 18 | 0 |
| `h2-422220-3` | `740f4ac4…` | 1, 10 | 18 | 0 |

All 361 base-correction incidences were evaluated in all twenty
quadratics.  In particular, no correction solves the two missing rows
while preserving the other eighteen.

The two near misses for `h2-422220-2` have a revealing exact relation.
They both lie in the same unique original rank-one chart, whose row
directions are

```text
G_A=(1,2,2),  G_B=(1,1,2).
```

Their difference is one of the allowed corrections, with hash
`ccadbfcfdc253c481b8c854c59ec8e221baff621b14238423cdab290a2e87b0e`.
It maps either near miss to the other; the third point on that affine line
has only `9/20` zero rows.  Thus the only nonzero correction retaining
`18/20` does not introduce an independent second row direction at all—it
just moves between the two already known points in their rank-one chart.

For `h2-422220-3`, the zero correction is the unique correction retaining
`18/20`; every nonzero correction has at most `11/20` zero rows.

This is the rigorous result of this folder.

## Linearized diagnostics

For a correction-chart basis `v_1,...,v_d`, the verifier also solves the
inhomogeneous Newton system

```text
Dq_u(sum t_k v_k) = -q(u).
```

Every fixed-background chart has coefficient rank `d` and augmented rank
`d+1`.  Hence none of the 169 charts even has a linearized correction for
all twenty rows.  This agrees with, but is not used to infer, the exact
finite exclusion above: a quadratic self-term can invalidate a Newton
inference over `F_3`.

A broader diagnostic allows the background and first component to
rebalance inside each of the 16 full rank-two plane charts through the
unique rank-one chart:

| profile/base | linearized-solvable full charts | distinct Newton steps | best exact score of those steps |
|---|---:|---:|---:|
| `h2-422220-2`, base 0 | 2/16 | 1 | 7/20 |
| `h2-422220-2`, base 1 | 2/16 | 1 | 7/20 |
| `h2-422220-3`, base 0 | 7/16 | 11 | 11/20 |

This second table is only a heuristic prioritization of full rank-two
charts.  It neither constructs nor excludes a nonlinear solution in
those charts.  The verifier records the exact plane bases, ranks, Newton
step hashes, and exact scores so that a later targeted solver can start
from the surviving linearized charts without repeating this audit.

## Claim boundary

- **Witness:** none.
- **Exact local obstruction:** no separable correction (1), with the
  pinned background and original tensor component fixed, solves digit two.
- **Not excluded:** a full rank-at-most-two chart in which the background
  or original component is reoptimized.
- **`LP(333)`:** no Legendre pair is constructed or excluded.
- **`H(668)`:** no Hadamard matrix is constructed or excluded.

## Reproduction

Run from `hadamard_668_search`:

```sh
python3 anti_tensor_correction/verify_anti_tensor_correction.py
```

The reference run took 4.6 seconds and peaked below 40 MB resident memory
while the eight-core dense-shell census was also running.  The pinned
semantic certificate hash is

```text
ed254a1e0a884227b447d31910298ea09ef9d7080b244bce3934c459bed9c4b8
```
