# LP(333) primitive-nine profile ideal

## Status

Exact primitive-nine equidistribution has a new profile-level obstruction.
The 36 nonzero column-class/residue triples are not independent: their
order-three Fourier moments depend only on the 24 residue profiles, before
any within-residue row placement is chosen.

For each of six reversal-conjugate nonzero class pairs, a profile
correlation must lie in the Eisenstein ideal

```text
3(1-omega) Z[omega],          Norm(3(1-omega))=27.       (1)
```

If it does, the three exact correlation targets for that column class are
uniquely determined.  Thus the exact primitive-nine layer reduces first to
six displayed Eisenstein ideal tests and then to a labelled realization
problem with a fixed `12 by 3` target table.  The global moment identity
makes one of those six tests dependent, leaving five independent new trits.

All 22 profile assignments previously pinned for the characteristic-37
two-coefficient audit fail (1), in between four and twelve nonzero classes.
This eliminates those 22 assignments, not their 22 aggregate shards:
alternative profile assignments have not been exhausted.

The row-695 profiles used by the labelled-jet checkpoint pass (1), so they
remain viable for this ideal test even though both currently pinned
placements fail exact primitive-nine equidistribution.  The later full-LP
zero-moment gate is stronger and excludes this fixed profile tuple on all
twelve nonzero column classes.

## 1. Profile Fourier data

Let `omega` be a primitive cube root, and let a labelled class word have
actual plus counts

```text
(n_0,n_1,n_2)
```

in rows congruent to `0,1,2 mod 3`.  Its order-three Fourier value is

```text
n_0+n_1 omega+n_2 omega^2
  = (n_0-n_2)+(n_1-n_2) omega.                    (2)
```

This value depends only on the residue profile.  Put the 37 column values
for channel `A` into `a(c)` and those for `B` into `b(c)`, including the
fixed zero column.  At column lag `t`, define

```text
D_t =
  sum_c [a(c+t) conjugate(a(c))
        +b(c+t) conjugate(b(c))]
  -167 delta_(t,0).                               (3)
```

Equation (3) is the order-three row Fourier transform of the exact residual
correlation polynomial at column lag `t`.  It can be computed from 24
profiles alone.

## 2. The fixed mass 1503

The nonzero class weights are complementary:

```text
A: 6,3,6,3,...       B: 3,6,3,6,...
```

and both zero-column weights are five.  Direct cyclic convolution of these
weight sequences gives, at every one of the 37 column lags,

```text
sum_(a=0)^8 c_(t,a) = 1503 = 9*167.               (4)
```

The verifier checks all 37 instances of (4) exactly.  This identity is
placement-independent.

Suppose now that the exact primitive-nine criterion holds:

```text
c_(t,s)=c_(t,s+3)=c_(t,s+6)=q_(t,s),
                                      s=0,1,2.    (5)
```

Equation (4) then gives

```text
q_(t,0)+q_(t,1)+q_(t,2)=501.                     (6)
```

## 3. Eisenstein ideal obstruction

Evaluating (5) at `omega` and using `omega^3=1` gives

```text
D_t = 3(q_0+q_1 omega+q_2 omega^2)
    = 3(x+y omega),                               (7)

x=q_0-q_2,             y=q_1-q_2.
```

By (6),

```text
x+y = 501-3q_2 = 0 mod 3.                        (8)
```

In `Z[omega]`, an element `x+y omega` is divisible by
`lambda=1-omega` exactly when `x+y=0 mod 3`.  Equations (7)--(8) prove the
necessary ideal condition (1).

In canonical coordinates `D_t=u+v omega`, membership is the elementary
integer test

```text
u = 0 mod 3,
v = 0 mod 3,
u/3+v/3 = 0 mod 3.                               (9)
```

A scalar consequence is

```text
Norm(D_t) = 0 mod 27.
```

Conversely, if (9) holds, the only possible target triple is

```text
x = u/3,                    y = v/3,
q_2 = (501-x-y)/3,
q_0 = q_2+x,                q_1 = q_2+y.         (10)
```

Thus (1) is not merely a congruence filter: it reconstructs the exact
integer targets that a later labelled lift must realize.

## 4. Global coupling

Reversal sends class `C_j` to `C_(j+6)` and conjugates the Eisenstein
coefficient:

```text
D_(j+6)=conjugate(D_j).                           (11)
```

Therefore the twelve nonzero tests reduce to six displayed conjugate-pair
tests.
Their reconstructed targets satisfy

```text
q_(j+6,0)=q_(j,0),
q_(j+6,1)=q_(j,2),
q_(j+6,2)=q_(j,1).                               (12)
```

The aggregate order-three norm gives the further global moment identity

```text
D_0 + 3 sum_(j=0)^11 D_j = 0.
```

For a profile tuple with the exact origin energy, `D_0=0`; consequently the
nonzero coefficients sum to zero.  Equivalently, the reconstructed target
table has

```text
sum_(j=0)^11 q_(j,s)=12*167=2004,    s=0,1,2.    (13)
```

There is one further dependency at the finite-ideal level.  After the
earlier lower profile digits vanish, write

```text
D_j = t_j (1-omega)^2 mod (1-omega)^3,
                                     t_j in F_3.
```

Conjugate reversal gives the same `t_j` on `C_j` and `C_(j+6)`.  Reducing
`sum_j D_j=0` yields

```text
t_0+t_1+...+t_5=0 in F_3.                         (14)
```

Hence only five of the six displayed ideal trits are independent: if five
vanish, the sixth vanishes automatically.  Equations (10)--(14) replace 36
apparently free equality groups by five independent finite-ideal decisions
and a uniquely determined target table.

## 5. Pinned row-695 target table

The row-695 profiles pass all six ideal conditions.  Listing `q-167` for
the twelve nonzero classes gives

```text
C0   ( 3,  3, -6)       C6   ( 3, -6,  3)
C1   (-1,  2, -1)       C7   (-1, -1,  2)
C2   ( 7, -2, -5)       C8   ( 7, -5, -2)
C3   (-3,  6, -3)       C9   (-3, -3,  6)
C4   (-4,  3,  1)       C10  (-4,  1,  3)
C5   (-2, -2,  4)       C11  (-2,  4, -2).
```

Every row sums to zero, each right-hand entry is the conjugate reversal of
the corresponding left-hand entry, and each column sums to zero across the
twelve classes.

The complete target-table hash is

```text
75e7464c751de1dcc2405157d8769641c0b7407e9357a3546ab9c0df36392383.
```

The verifier independently computes the same profile moments from both
labelled row-695 certificates, despite their different within-residue
placements.

These nonconstant targets also make the scope transparent: a full
`LP(333)` requires the special target `(167,167,167)` in every class, hence
`D_t=0`.  Thus the table is an exact primitive-nine ideal witness, not a
full-LP profile survivor.

## 6. Audit of the 22 prior profile assignments

The earlier characteristic-37 checkpoint pins one partial profile witness
for each of the 22 aggregate shards.  Their numbers of nonzero classes
failing (1) are:

```text
failing classes    profile assignments
4                  4
6                  1
8                 10
10                 4
12                 3
```

Reversal forces every failure count to be even.  None of the 22 assignments
passes the new ideal layer.  The exact 22-table corpus hash is

```text
ee30efce6b0b64af57a54c15f94bc446444bd2a972e36713c271d7259d1c7b62.
```

This is a strict new obstruction on previously viable profile assignments.
It is not a shard exclusion because only one assignment per shard was
stored.

## Reproduction

```text
python3 verify_lp333_order3_profile9.py
python3 -m unittest -v test_lp333_order3_profile9.py
```

Both commands use only exact integer arithmetic and the Python standard
library.
