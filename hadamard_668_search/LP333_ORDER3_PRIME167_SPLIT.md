# Prime-167 exact split for the LP(333) order-three profile gate

## Status

On the exact energy-167 shell, reduction modulo 167 loses no nonzero-lag
correlation information: a pair of length-37 Eisenstein sequences is
complementary exactly when its combined correlation word vanishes modulo
167.

For the order-three-invariant profile algebra, this modular equation splits
over finite fields as

```text
F_167(omega)[C_37]^H
    = k x E x E,

k = F_(167^2),
E = F_(167^12),
H = {1,10,26}.
```

The verifier proves the displayed field split, checks the involution and an
explicit inverse CRT, and parameterizes all four branches of the resulting
finite-field solution cone.  The 22 stored profile-ideal witnesses are
negative controls: none passes the prime-167 equation.

This is a search reduction, not a new physical profile tuple, an `LP(333)`,
or a Hadamard matrix.  Most points of the finite-field cone do not have the
small integral coefficient alphabet required of a profile.

## 1. Why reduction modulo 167 is exact

Let `A,B` be length-37 sequences over `Z[omega]`, and write

```text
C_t = sum_j A_(j+t) conjugate(A_j)
    + sum_j B_(j+t) conjugate(B_j).
```

Assume the exact energy is

```text
C_0 = 167.
```

Cauchy's inequality gives `|C_t| <= 167`.  For `t!=0`, if `C_t` is divisible
by 167 in `Z[omega]`, then either `C_t=0` or

```text
C_t = 167 epsilon
```

for an Eisenstein unit `epsilon`: a nonzero Eisenstein integer has norm at
least one, with equality exactly at the six units.

In the nonzero case Cauchy's inequality is an equality.  Translation by
`t` therefore acts on the concatenated vector `(A,B)` by the scalar
`epsilon`.  For `t != 0`, translation has order 37, so

```text
epsilon in mu_6 intersect mu_37 = {1}.
```

Both sequences would then be constant, making their energy divisible by
37.  This contradicts `37` not dividing `167`.  Hence every nonzero
correlation divisible by 167 is exactly zero.  The origin coefficient is
already 167, so

```text
A A* + B B* = 167 e

if and only if

A A* + B B* = 0 modulo 167.                                (1)
```

This argument does not use the order-three symmetry; that symmetry is used
only to make the finite-field algebra small.  It also does not depend on
there being exactly two sequences: the same equality-case proof applies to
any finite Eisenstein family of total energy 167.  In particular it applies
to the six-sequence diagonal phase frame; the directed cross-frame equation
requires the separate twisted-translation argument recorded in the full
phase package.

## 2. The finite-field split

Because `167 = 2 mod 3`, `x^2+x+1` is irreducible over `F_167`, and

```text
k = F_167(omega) = F_(167^2).
```

Modulo 37,

```text
ord(167)   = 36,
ord(167^2) = 18.
```

Thus `Phi_37` has two irreducible degree-18 factors over `k`.  The verifier
pins one factor by its ascending coefficient pairs `a+b*omega`:

```text
f_+ =
((1,0),(62,123),(5,0),(121,79),(113,44),(15,35),(114,44),
 (119,79),(111,44),(121,79),(111,44),(119,79),(114,44),
 (15,35),(113,44),(121,79),(5,0),(62,123),(1,0)).
```

The second factor is the coefficient-conjugate reciprocal

```text
f_-(x)=conjugate(x^18 f_+(x^-1)).
```

The verifier multiplies these two factors to `Phi_37` exactly and applies
the finite-field irreducibility criterion to each.

The subgroup

```text
H = <167^12> = {1,10,26}
```

has order three.  Taking `H`-invariants fixes `F_(167^12)` inside each
degree-18 primitive factor.  Therefore

```text
k[C_37]^H = k x E x E,          E=F_(167^12),              (2)
```

with dimensions `1+6+6=13` over `k`, as required by the one origin orbit
and twelve nonzero `H`-orbits.  The verifier independently obtains rank six
from each of the two systems of Gaussian periods.

## 3. CRT and the involution

Let `zeta` be a root of `f_+`.  The CRT coordinates
of an invariant word `F` are

```text
(c,x,y) = (F(1), F(zeta), F(zeta^167)).
```

Coefficient conjugation is the 167th power, while group inversion sends
the exponent to its negative.  The congruences

```text
167^6  in -H,
167^7  in -167 H
```

give

```text
(c,x,y)* = (c^167, y^(167^5), x^(167^7)).                  (3)
```

The exponents five and seven add to twelve, so this operation squares to
the identity on `E`.  Six deterministic words are transformed and
round-tripped through an explicit 37-point inverse DFT.

## 4. Complete solution parameterization

For two invariant words, write their CRT coordinates as

```text
(c_A,x_A,y_A), (c_B,x_B,y_B).
```

By (3), equation (1) is equivalent to

```text
N(c_A)+N(c_B)=0                                      in F_167,   (4)

x_A y_A^(167^5) + x_B y_B^(167^5)=0                 in E.       (5)
```

The other primitive coordinate is the star image of (5), so it is
redundant.

### Trivial coordinate

There are two disjoint branches.

```text
zero:
    (c_A,c_B)=(0,0);

nonzero:
    c_A=s,
    c_B=s r,
    s in k^*,
    N(r)=-1.
```

The norm-minus-one fiber contains `167+1=168` elements.  Hence (4) has

```text
T = 1 + (167^2-1)(167+1)
  = 4,685,185
```

ordered solutions.  The verifier exhausts all `167^2` elements of `k`,
checks every norm fiber, and recovers the unique `(s,r)` from every tested
nonzero solution.

### Primitive coordinates

Put

```text
u_A = y_A^(167^5),
u_B = y_B^(167^5).
```

The fifth-power Frobenius is a bijection of `E`, with inverse the
seventh-power Frobenius.  Again there are two disjoint branches.

```text
degenerate:
    (x_A,x_B)=(0,0),
    y_A,y_B arbitrary in E;

nondegenerate:
    (x_A,x_B) != (0,0),
    u_A = -tau x_B,
    u_B =  tau x_A,
    tau arbitrary in E,
    y_A = u_A^(167^7),
    y_B = u_B^(167^7).
```

The parameter `tau` is unique on the nondegenerate branch.  If
`M=|E|=167^12`, the primitive equation has

```text
M^2 + (M^2-1)M
```

solutions.  Combining the two trivial and two primitive branches gives

```text
488112248150484454720739908681513468771243102038788308561487621641729425684669715267585
```

ordered pairs in the invariant finite-field algebra.  Four fixtures, one
from each branch combination, are sent through inverse CRT and checked
directly in the group ring.  Both one-axis subcases of the nondegenerate
primitive branch are also reconstructed explicitly.

## 5. Fixed profile corpus

For each of the 22 stored profile-ideal witnesses, the verifier:

1. reconstructs its two exact length-37 Eisenstein profile sequences;
2. checks exact energy 167;
3. computes all 37 exact correlations;
4. compares exact complementarity, coefficientwise reduction modulo 167,
   and the split predicates (4)--(5).

All three predicates agree, and all 22 fixed tuples fail.  The smallest
observed strict gap between `167^2` and the squared modulus of the largest
nonzero-lag correlation is 24,973.

This excludes 22 fixed profile assignments and zero aggregate shards.

## 6. Pinned certificates

```text
equality-case arithmetic
04435badfc26829c4b9bfdd51929c7ae6daa51868b138c335c383d99fa51cc3b

field split and period bases
445e8246071b8b84702e05d640cfbbf81ab7b09c7c82999d00d345d35afe6815

star action and CRT round trips
6cd8b72030b431111bdece3260526a211775c71191e63380a907fa8e65a08268

complete four-branch parameterization
1492ae5cf79738a1721c4f5eb9046e1333eb7ac99dd0f305cebafd20d5850d9e

22-profile split-signature corpus
6a4bd5cd494346cc1a0396e51936fb2fafb34ee53032f84fb79caeb95a890900
```

## Reproduction

```text
python3 verify_lp333_order3_prime167_split.py
python3 -m unittest -v test_lp333_order3_prime167_split.py
```

The replay uses exact integer and finite-field arithmetic from the Python
standard library.
