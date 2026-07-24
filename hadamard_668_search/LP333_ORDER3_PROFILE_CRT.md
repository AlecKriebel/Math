# Local-global CRT closure of the LP(333) profile zero gate

## Status

The exact 24-profile equation

```text
D_t=0
```

does not require an unbounded integer-correlation search.  On the
energy-167 order-three profile space it is exactly equivalent to the
combination of two finite modular layers already natural in the problem:

```text
D_t in 3(1-omega) Z[omega]       for every nonzero class,
D_t = 0 modulo 37                for every class.
```

The first line is the primitive-nine profile ideal.  The second is
equivalent, without loss, to vanishing of all thirteen coefficients of the
characteristic-37 logarithmic norm transfer.  Their Chinese-remainder
kernel has no nonzero point inside the Cauchy disk available to a profile
correlation, so the combined modular fingerprint detects exact zero.

This is a rigorous search reduction, not an `LP(333)` or an `H(668)`.
The 22 currently pinned ideal-compatible profile tuples all fail the
complete characteristic-37 transfer.  This excludes those fixed tuples,
not any of their 22 aggregate row-sum shards.

The later prime-167 theorem gives a simpler single-modulus zero detector and
applies more broadly to Eisenstein families of total energy 167 without
order-three invariance.  On the shared profile domain neither detector is
logically stronger: both are equivalent to exact zero.  The present CRT
remains useful computationally because it reuses the small lambda-adic and
characteristic-37 tables already native to the profile model; it is not a
second independent existence obstruction.

## 1. Exact energy and the origin coefficient

Let `a,b` be the two Eisenstein profile sequences on `F_37`.  Their fixed
zero-column values are

```text
a(0)=-1,             b(0)=2.
```

Every nonzero column class has three physical columns.  If its normalized
profile is `p`, its Eisenstein value has norm `0`, `3`, or `9`.  The viable
24-profile layer has total normalized profile norm `54`.  Consequently

```text
sum_c (Norm(a(c))+Norm(b(c)))
  = Norm(-1)+Norm(2)+3*54
  = 1+4+162
  = 167.                                                    (1)
```

For

```text
D_t =
  sum_c [a(c+t) conjugate(a(c))
        +b(c+t) conjugate(b(c))]
  -167 delta_(t,0),
```

equation (1) gives

```text
D_0=0                                                       (2)
```

identically.  Only the twelve nonzero `H`-classes remain.

## 2. The exact Cauchy disk

For `t!=0`, regard the two channels together as one vector in
`C^(2*37)`.  Translation is unitary, so Cauchy--Schwarz and (1) give

```text
|D_t| <= 167,
Norm(D_t)=|D_t|^2 <= 167^2=27,889.                         (3)
```

This bound uses no heuristic and no profile enumeration.

## 3. The two modular layers

Put

```text
lambda=1-omega.
```

Since

```text
3 lambda = -omega^2 lambda^3,
```

the primitive-nine ideal condition is exactly the first three
`lambda`-adic digits:

```text
D_t in lambda^3 Z[omega].                                  (4)
```

Independently, reduce the full `H`-invariant correlation word modulo 37.
The logarithmic substitution

```text
x=exp(u),              v=u^3
```

identifies the 13-dimensional invariant group ring with

```text
(Z[omega]/37)[v]/(v^13).
```

Its transfer matrix has rank 13 and determinant 11 modulo 37.  Therefore
vanishing of the complete transferred norm residual is equivalent to

```text
D_t in 37 Z[omega]              on all thirteen parts.     (5)
```

This equivalence uses all thirteen transfer coefficients.  A prefix such as
`T_1,T_2` is not enough.

## 4. Local-global closure

The ideals in (4) and (5) are coprime.  Hence their intersection is

```text
37 lambda^3 Z[omega]
 =37*3(1-omega) Z[omega].                                  (6)
```

The least norm of a nonzero element of (6) is

```text
37^2 * Norm(lambda)^3
 =37^2 * 3^3
 =36,963.                                                  (7)
```

But (3) bounds every possible nonzero-class profile correlation by
`27,889`.  Equations (3) and (7) are incompatible unless

```text
D_t=0.
```

Together with (2), this proves the exact equivalence:

> On the energy-167 `H`-invariant profile space, the full profile-zero
> equation is equivalent to the primitive-nine `lambda^3` ideal plus the
> complete characteristic-37 transfer.

The converse is immediate because exact zero satisfies both reductions.

In coordinates `D_t=r+s omega`, the verifier also performs the division in
(6) explicitly.  If `37` divides `r,s` and
`D_t in 3(1-omega)Z[omega]`, then

```text
D_t=37*3(1-omega)*(x+y omega)
```

with

```text
x=(2(r/37)-(s/37))/9,
y=((r/37)+(s/37))/9.
```

The ideal congruences guarantee both quotients are integers.

## 5. Why the third lambda digit is the threshold

This particular norm argument becomes sufficient for the first time at
`lambda^3`:

```text
37^2 * Norm(lambda)^2 = 12,321 <= 27,889,
37^2 * Norm(lambda)^3 = 36,963 >  27,889.                  (8)
```

Thus a modulo-`lambda^2` condition combined with modulo 37 cannot certify
exact zero from the universal Cauchy bound alone.  The third digit crosses
the threshold.  This is a sharp statement about the present bounding
method, not a claim that a nonzero profile correlation of norm `12,321`
actually occurs.

## 6. Exact pinned-corpus audit

The 22 profile assignments retained by the earlier primitive-nine ideal
audit have:

```text
energy 167                                      22/22,
lambda^3 ideal                                  22/22,
complete characteristic-37 transfer              0/22,
exact D_t=0                                       0/22.
```

Their numbers of nonzero transfer residual coefficients have histogram

```text
nonzero coefficients     fixed tuples
7                         1
8                         1
10                        4
11                       16
```

This is a negative control for the local-global theorem and shows why a
complete transfer, rather than a short prefix, is required.  It does not
exhaust the profile choices inside any aggregate shard.

The compact 22-tuple audit has SHA-256

```text
1b991b731a934c0c4361a93a1570c15fba69118fe1e15492ef5119385dcb7866
```

## 7. Search consequence

The next profile solver can remain finite throughout:

1. impose the aggregate target, profile energy, and opposite-class local
   constraints;
2. impose the primitive-nine `lambda^3` ideal;
3. impose all characteristic-37 transfer coefficients;
4. treat every survivor as an exact `D_t=0` profile tuple by the theorem;
5. only then enter the 54-placement-trit phase lift.

No exact integer-correlation state needs to be carried in that search.  The
two modular signatures form a zero-detecting CRT representation over the
entire feasible correlation disk.

## Reproduction

```text
python3 verify_lp333_order3_profile_crt.py
python3 -m unittest -v test_lp333_order3_profile_crt.py
```

The verifier uses exact arithmetic and the Python standard library only.
It independently checks the rank-13 transfer orientation, the explicit CRT
division, the Cauchy bound on all pinned physical correlations, the
lambda-power threshold, and every lattice point in the Cauchy disk.
