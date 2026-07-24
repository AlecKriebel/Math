# Characteristic-37 transfer for the order-three LP(333) quotient

## Status

The viable order-three multiplier quotient has a second exact algebraic
description, independent of the Eisenstein prime above three.

Reduce its Eisenstein group-ring autocorrelation identity modulo 37. Because

```text
x^37-1 = (x-1)^37                 in characteristic 37,
```

the cyclic group ring becomes a truncated local ring. The logarithmic
coordinate `x=exp(u)` turns inversion into `u -> -u`. Order-three
`H={1,10,26}` invariance kills every moment whose degree is not divisible by
three, so putting `v=u^3` gives an invertible map

```text
13-dimensional H-invariant group ring
             <->
F_37[omega][v]/(v^13).
```

Under this map, the full mixed-column system is exactly one degree-twelve
truncated norm identity

```text
A(v) conjugate(A(-v)) + B(v) conjugate(B(-v)) = 19.       (1)
```

Thus the six complex mixed-lag equations become thirteen scalar
characteristic-37 transfer coefficients. The transfer matrix has rank 13 and
determinant 11 modulo 37.

This is a new exact necessary-condition layer, but its first two nonconstant
coefficients are not yet strong enough to remove a row-sum shard. Explicit
profile witnesses show that all 22 aggregate shards satisfy simultaneously:

- the aggregate target;
- total nonzero-class Eisenstein norm 54;
- the earlier local mod-three opposite-class sieve;
- characteristic-37 transfer coefficients one and two.

Every such witness fails later transfer coefficients. None is an `LP(333)`
candidate.

All statements are replayed by
`verify_lp333_order3_char37_transfer.py` with standard-library-only exact
arithmetic.

## 1. Starting group-ring identity

Let `omega^2+omega+1=0`, and let `a,b` be the two `H`-invariant Eisenstein
sequences on `F_37` obtained from the nontrivial row character. Their zero
coefficients are

```text
a(0)=-1,       b(0)=2.
```

For `c in C_j=2^j H`, write

```text
a(c)=-epsilon_j z(p_A,j),
b(c)= epsilon_j z(p_B,j),        epsilon_j=(-1)^j,
```

where

```text
z(p)=p0+p1 omega+p2 omega^2,
p0+p1+p2=3.
```

There are ten profiles `p`. Their norms are `0`, `3`, or `9`.

Define

```text
A(x)=sum_c a(c)x^c,
B(x)=sum_c b(c)x^c
```

in the cyclic group ring. The exact compressed correlation problem is

```text
A(x) A*(x) + B(x) B*(x) = 167,                   (2)
```

where `*` conjugates Eisenstein coefficients and sends `x` to `x^-1`.

## 2. Truncated logarithmic coordinate

Work in

```text
R_37 = (Z[omega]/37Z)[x]/(x^37-1).
```

Set `y=x-1`. In characteristic 37,

```text
x^37-1=y^37.
```

All integers `1,...,36` are invertible, so the truncated series

```text
u=log(1+y),
x=exp(u)
```

are mutually inverse modulo `u^37`. Inversion is now literal sign change:

```text
x -> x^-1       iff       u -> -u.               (3)
```

For any `H`-invariant sequence `f`,

```text
F(exp(u)) = sum_c f(c) exp(cu).
```

For `n>0`, its `n`th exponential moment over one class is

```text
sum_(h in H) (2^j h)^n
 = 2^(jn) sum_(h in H) h^n.
```

Since `H` is the group of cube roots of unity in `F_37`,

```text
sum_(h in H) h^n =
    3,  if 3 divides n,
    0,  otherwise.                               (4)
```

Consequently, every nonzero logarithmic coefficient occurs in degree `3k`.
Put

```text
v=u^3.
```

The `H`-invariant subring is thereby identified with truncated polynomials of
degree at most twelve in `v`.

## 3. Explicit transfer coefficients

Let `a_j` denote the common value of `a` on `C_j`. Write

```text
A(v)=A_0+A_1 v+...+A_12 v^12.
```

Equations (3)--(4) give

```text
A_0 = a(0) + 3 sum_(j=0)^11 a_j,                 (5)

A_k = 3/(3k)! sum_(j=0)^11 8^(jk) a_j,
                                      k=1,...,12. (6)
```

The same formulas define `B_k`. Here `8=2^3` has exact order twelve modulo
37. Therefore the nonconstant block in (6) is a twelve-point Fourier matrix.
All factorials through `36!` are nonzero modulo 37.

The complete `13 by 13` transfer matrix, including (5), has

```text
rank          13,
determinant   11 modulo 37.
```

Thus the transfer is invertible; it loses no `H`-invariant correlation
information modulo 37.

The first three scale factors `3/(3k)!` are

```text
k=0: 1,
k=1: 19,
k=2: 35                 modulo 37.
```

The compact hash of the classes, all thirteen scale factors, the full matrix,
rank, and determinant is

```text
6054140458c5995d454fe1ab58269faa1b6f293e2dc901e64c01b3ee3623d2a0
```

## 4. Thirteen norm coefficients

Conjugation and (3) send

```text
A(v) -> conjugate(A(-v)).
```

Reducing `167` modulo 37 gives `19`, so (2) becomes (1). The coefficient of
`v^n` is

```text
T_n =
 sum_(k=0)^n (-1)^(n-k)
   [ A_k conjugate(A_(n-k))
    +B_k conjugate(B_(n-k)) ].                   (7)
```

The exact targets are

```text
T_0=19,
T_n=0,              n=1,...,12.                 (8)
```

For even `n`, `T_n` is fixed by Eisenstein conjugation; for odd `n`, it is
negated by conjugation. Since

```text
Z[omega]/37Z = F_37 x F_37
```

with conjugation exchanging the factors, each `T_n` contributes one scalar
equation over `F_37`. Hence (8) has thirteen scalar conditions, matching the
dimension and the earlier count of independent real equations.

Because the transfer matrix is invertible, (8) is equivalent to all
cyclotomic mixed-lag correlations modulo 37, not merely a consequence of
them.

## 5. Direct mechanical audit

The verifier checks the theorem in three independent representations:

1. full length-37 sequences and cyclic group-ring multiplication;
2. twelve exact `13 by 13` cyclotomic transition matrices;
3. the thirteen logarithmic coefficients (5)--(7).

Its deterministic fixture corpus contains:

```text
one zero-class fixture,
240 exhaustive single-class/profile perturbations,
100 two-channel profile pairs,
32 dense deterministic fixtures,
--------------------------------
373 fixtures total.
```

For every fixture it:

- checks all non-multiple-of-three logarithmic moments vanish;
- computes the transform directly from all 37 physical coefficients;
- recomputes it from (5)--(6);
- multiplies the two transferred words by (7);
- independently transforms the physical group correlation;
- checks all twelve cyclotomic transition equations and their orientation.

This replays

```text
373 * 12 = 4,476
```

cyclotomic equations. The fixture-corpus hash is

```text
ade17851177daefcaefb416f9f52f7fbc417a4684499f2b648b4d5c0d37a103b
```

## 6. Paired-layer shard census

The smallest useful combined test joins:

```text
aggregate target,
total profile norm 54,
local mod-three opposite-class signature,
T_1=0,
T_2=0.
```

An explicit 24-profile witness is pinned for every one of the 22 aggregate
targets. Therefore

```text
22/22 shards survive.
```

This is an exact negative result about the strength of the first two transfer
coefficients: neither alone nor together with the earlier local sieve can
eliminate a row-sum shard.

The witnesses are deliberately audited against the remaining coefficients.
Their numbers of bad coefficients among `T_3,...,T_12` are:

```text
bad later coefficients   witnesses
6                         1
8                         7
9                        14
```

Thus no stored object satisfies the full characteristic-37 transfer, and no
candidate is implied. The paired-witness hash is

```text
8b5040dbec2d5089e926519e6006672629e3bb110d0a48221c771ac9eddad3a6
```

## 7. Scope and next use

What is established:

- an invertible characteristic-37 logarithmic transfer for the complete
  order-three mixed-lag system;
- thirteen explicit transfer coefficients with exact factorial/Fourier
  weights;
- direct equivalence to physical and cyclotomic correlations;
- exact survival of all 22 shards through the first two coefficients joined
  with the local mod-three and energy layers.

What is not established:

- later transfer coefficients have not been exhaustively joined;
- the characteristic-37 system has not been proved feasible or infeasible;
- no exact `3 by 37` compressed witness, `LP(333)`, or `H(668)` is claimed.

The useful next step is a staged transfer DP over `T_3,T_4,...`, retaining
the same 22 aggregate keys. Unlike a broad quotient search, each stage works
over a fixed 13-dimensional finite algebra with a mechanically checkable
frontier.

Run:

```sh
python3 verify_lp333_order3_char37_transfer.py
python3 -m unittest -v test_lp333_order3_char37_transfer.py
```
