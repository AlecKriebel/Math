# Cubic character gate for the three-high profile shell

## Status

There is a one-scalar characteristic-\(37\) obstruction that is linear in
all remaining profile-letter choices once an exact aggregate target is
fixed.  It can therefore be appended to the shell-three additive
aggregate/modulo-nine join without introducing any cross terms.

This scalar is exactly the first logarithmic coordinate `T_1` from the
existing complete characteristic-\(37\) transfer theorem.  It is **not** an
independent obstruction from that transfer.  The new point here is its
target-fixed additive linearization, its integration into the shell-three
join, and the fact that this first coordinate alone rejects all six stored
shell-three controls.

For the six already-pinned primitive-nine witnesses in the
\((n_9,n_3,n_0)=(3,9,12)\) shell, this single scalar is nonzero:

```text
31, 6, 4, 14, 36, 11 modulo 37.
```

Thus all six fixed witnesses are excluded before the other twelve
characteristic-\(37\) coordinates are evaluated.  This does **not** exclude
the shell: other phase lifts of its signed skeletons may satisfy the cubic
gate.

## 1. The cubic moment

Let \(f:\mathbf F_{37}\to\mathbf Z[\omega]\) be one of the two
\(H\)-invariant profile words, where

```text
H={1,10,26},                C_j=2^j H.
```

Write \(f_j\) for its value on \(C_j\), and put

```text
M_0(f)=sum_x f(x)=f(0)+3 sum_j f_j,
P(f)=sum_(j=0)^11 8^j f_j       in Z[omega]/37.            (1)
```

The weight \(8=2^3\) has order twelve modulo \(37\), so \(P\) is the first
nontrivial multiplicative character coordinate of the twelve cyclotomic
classes.

For \(k=1,2,3\), let \(M_k(f)=\sum_x x^k f(x)\).  The subgroup power sums
give

```text
sum_(h in H) h   = 0,
sum_(h in H) h^2 = 0,
h^3              = 1                         modulo 37.
```

Consequently

```text
M_1(f)=M_2(f)=0,             M_3(f)=3P(f).                 (2)
```

## 2. Correlation proof

For

```text
D(t)=sum_x [
  a(x+t) conjugate(a(x)) + b(x+t) conjugate(b(x))
],
```

expand the cubic weighted sum:

```text
sum_t t^3 D(t)
 = sum_(x,y) (x-y)^3 [
     a(x) conjugate(a(y)) + b(x) conjugate(b(y))
   ].
```

Using (2), the middle two binomial terms vanish and the result is

```text
3 [
 P(a) conjugate(M_0(a)) - M_0(a) conjugate(P(a))
+P(b) conjugate(M_0(b)) - M_0(b) conjugate(P(b))
]                                                        (3)
```

in \(\mathbf Z[\omega]/37\).  An exact complementary profile has
\(D(t)=0\) for every \(t\ne0\), while the \(t=0\) summand in the weighted
sum is zero.  Since \(3\) is invertible modulo \(37\), (3) must vanish.

For Eisenstein coordinates \(z=z_0+z_1\omega\) define

```text
det(z,w)=z_0 w_1-z_1 w_0.
```

Because

```text
z conjugate(w)-w conjugate(z)
  =det(z,w)(omega^2-omega),
```

the exact necessary condition is the single scalar equation

```text
J =
 det(P(a),M_0(a)) + det(P(b),M_0(b))
 =0 modulo 37.                                            (4)
```

## 3. Why this belongs inside the additive join

For a fixed exact target, \(M_0(a)\) and \(M_0(b)\) are constants:

```text
M_0(a)=-1+3 alpha,             M_0(b)=2+3 beta,
```

where \(\alpha,\beta\) are the two class aggregates.  A choice
\(\delta=\delta_0+\delta_1\omega\) at channel \(X\), class \(j\), contributes

```text
8^j (delta_0 M_0(X)_1-delta_1 M_0(X)_0) modulo 37          (5)
```

to \(J\).  Hence every medium phase and every high state has an independent
one-slot signature.  If the existing meet-in-the-middle key is

```text
(exact aggregate, twelve modulo-nine correlation coordinates),
```

it can be replaced losslessly by

```text
(exact aggregate, twelve modulo-nine coordinates, J modulo 37).
```

No pairwise correction table is needed for the new coordinate.  The
verifier also checks that, for each of the 22 aggregate targets, the row
\(J\) has rank one beyond the four class-aggregate coordinate rows over
\(\mathbf F_{37}\); it is not a disguised aggregate equation.

## 4. Pinned shell-three negative controls

Six previously stored profile-ideal witnesses lie in this shell.  Each has:

- exactly three norm-nine, nine norm-three, and twelve zero letters;
- its declared exact aggregate;
- all six local opposite-quartet signatures;
- every nonzero correlation in \(3(1-\omega)\mathbf Z[\omega]\).

Their cubic values are:

| target | \(J\pmod {37}\) |
|---|---:|
| `(-3,-3,-4,-2)` | 31 |
| `(-3,0,-3,-3)` | 6 |
| `(0,3,-4,-2)` | 4 |
| `(2,1,2,-2)` | 14 |
| `(3,0,3,3)` | 36 |
| `(5,1,0,0)` | 11 |

Thus the cubic character alone rejects all six fixed controls.  Their
failure is evidence that (4) is useful, not a proof that all
92,968 skeleton/target orbits fail it.

## Reproduction

From this directory:

```text
python3 verify_lp333_order3_shell3_cubic_character.py
python3 -m unittest -v test_lp333_order3_shell3_cubic_character.py
```

The verifier is dependency-free and reconstructs the physical
length-\(37\) words, all correlations, the primitive-nine ideal membership,
the cubic weighted-correlation identity, and the rank calculation.  In
particular, it checks:

```text
676 ordered cross terms on the full 13-part invariant Eisenstein basis,
240 one-class states using both fixed channel origins,
625 determinant/wedge coordinate pairs,
22 target matrices of rank five rather than aggregate rank four,
6 detached shell-three primitive-nine controls.
```

The pinned hashes are:

```text
verifier source
87fe371b33c3a9f7d64261da1cb53d8683c228e6a0679ec0d0677b3b3fd37c79

test source
f73d70f1cd4260e4239fa5f1064858e3c6fd0c61c80ca1997e250c144c4f3cc0

verifier stdout
e1ebd7027bfc64b48aa380ad3e7a14706d105086df6748a05f569399f757da74

detached control replay
906eeeb7cf10895e381ff5963e229a30dfc2f8cc8de351af4c3ab4f790bdb932
```
