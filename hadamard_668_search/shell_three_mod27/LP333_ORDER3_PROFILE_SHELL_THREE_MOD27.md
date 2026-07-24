# Exact exclusion of the three-high order-three profile shell

## Status

The order-three `LP(333)` profile type sector

```text
(n_9,n_3,n_0)=(3,9,12)
```

has no exact profile-zero assignment.  The complete, symmetry-reduced
calculation has:

```text
exactly 479,850 modulo-nine/exact-aggregate survivors,
exactly two modulo-27 survivors,
zero survivors of modulo 27 plus the cubic characteristic-37 moment,
zero survivors under detached exact correlation replay.
```

This is an exact exclusion of one of the seven global profile type sectors.
It is not an `LP(333)` construction and is not a Hadamard matrix of order
668.

## 1. Uniformizer alphabet

Put

```text
lambda=1-omega,             omega^2+omega+1=0.
```

The ten residue-profile values split without overlap as

```text
0,
sigma lambda omega^u          (sigma in {+1,-1}, u in F_3),
3 omega^v                     (v in F_3).
```

The nine norm-three letters are called medium and the three norm-nine
letters high.  After the fixed channel/parity sign is absorbed into
`sigma`, reduction modulo three remembers only the medium sign.  A signed
skeleton therefore has nine nonzero entries in 24 ternary positions.

For each opposite quartet

```text
(A_j,A_(j+6),B_j,B_(j+6)),
```

the local pair-signature equation is

```text
-s_A,j+s_A,j+6+s_B,j-s_B,j+6=0 in F_3.          (1)
```

The legal local counts by number of medium entries are

```text
m=0,1,2,3,4:       1,0,12,8,6.
```

Since the shell has nine medium letters, only the quartet patterns
`333000`, `432000`, and `322200` occur.  Their exact total is

```text
908,800 signed skeletons.
```

## 2. Lossless affine modulo-nine lift

Fix a signed skeleton and let `w` be its phase-zero medium word.  Every
remaining one-slot correction is divisible by three:

```text
delta_i =
  sigma lambda(omega^u-1)       for a medium phase change,
  3 omega^v                     for a high insertion,
```

including the fixed channel/parity sign.  Therefore products of two
distinct corrections are divisible by nine.  For every nonzero lag,

```text
D(w+sum_i delta_i)
 =
D(w)+sum_i (D(w+delta_i)-D(w))             (mod 9).         (2)
```

This identity is exact in the quotient.  It turns the remaining search into
a fixed-cardinality additive signature join on:

```text
12 correlation coordinates modulo 9,
4 exact integer aggregate coordinates,
exactly 3 high-support positions.
```

The first quotient digit is the primitive flag

```text
ell(D_j/3),            ell(a+b omega)=a+b mod 3.
```

For a fixed skeleton and high support it is one nonzero affine equation in
the medium phases of each nonempty quartet.  An `m`-medium quartet has
exactly `3^(m-1)` solutions.  An empty-medium quartet instead gives a
support gate.  Consequently each support produces only `3^6=729` or
`3^5=243` medium records, and only 27 high-phase records.

### The two quotient coordinates

The locality can be made explicit.  Write

```text
D_j/3 = ell_j+k_j lambda                    modulo 3,
```

so `ell_j=a+b` and `k_j=-b` when `D_j/3=a+b omega`.
For the origin-medium contribution at one opposite quartet, write

```text
T=sum_i c_i omega^(r_i),
C_0=sum_i c_i=3m,
C_1=sum_i c_i r_i,
C_2=sum_i c_i binom(r_i,2).
```

The local skeleton equation is exactly what makes `C_0` divisible by
three.  Since the contribution is `lambda T`,

```text
(lambda T)/3
 = C_1+(m-C_1-C_2)lambda                    modulo 3.       (3)
```

Thus its `ell` coordinate is linear in the local medium phases, while its
`k` coordinate is local quadratic.  The other contribution types have the
following exact dual-number structure:

| contribution to `D/3 mod 3` | `ell` coordinate | `k` coordinate |
|---|---|---|
| origin-medium | local linear in `u` | local quadratic in `u` |
| origin-high | support only | local linear in `v` |
| medium-medium | signed skeleton only | global linear in phase differences |
| medium-high | zero | signed support only |
| high-high | zero | zero |

For example,

```text
(lambda sigma_y omega^u_y)
 conjugate(lambda sigma_x omega^u_x)/3
 =
sigma_y sigma_x
 [1-(u_y-u_x)lambda]                         modulo 3,
```

and a medium-high product divided by three is `lambda` times a unit, whose
unit phase disappears modulo `lambda^2`.

These formulas give two useful ranks.

1. If `r` opposite quartets contain medium letters, the six `ell`
   equations have rank `r`.  Adding the two next aggregate digits raises
   the rank to `r+1`: every nine-medium shell skeleton has a quartet
   containing media in both channels.  Hence the medium-phase rank is four
   for the `333000` and `432000` patterns and five for `322200`.
2. Once the medium phases are fixed, a quartet containing `h>0` high
   letters has one rank-one equation in their high phases and therefore
   `3^(h-1)` solutions.  A high-empty quartet instead contributes a
   medium-only gate.

The exact aggregate statement behind the first rank is also transparent.
If a channel target is `t=lambda tau`, then

```text
(S-t)/lambda
 =
[sum sigma-ell(tau)]
+lambda[-sum sigma u-sum kappa-k(tau)]          modulo 3,   (4)
```

where `kappa` is the fixed sign of a high support position.  The high phase
`v` does not yet occur.

## 3. The next digit and the high-high terms

Write every correction as `delta_i=3 eta_i`.  Expanding the Hermitian
correlation one digit farther gives the lossless quadratic identity

```text
D(w+sum_i delta_i)
 =
D(w)+sum_i Delta_i
 +9 sum_(i<k) (eta_i eta_k^*+eta_k eta_i^*)       (mod 27), (5)
```

where

```text
Delta_i=D(w+delta_i)-D(w)
```

is the precomputed unary response, with the group-ring shifts understood.
The final term is a quadratic form over `F_3`.  This is the first layer in
which high-high interactions survive.  Equation (5), evaluated after the
additive join, leaves exactly two assignments.

Their displayed correlations on `C_0,...,C_5` are:

```text
near witness 1:
(-27,-27), (0,27), (0,0), (0,0), (27,0), (0,0)

near witness 2:
(-27,0), (0,-27), (0,0), (0,0), (0,0), (0,-27).
```

Both are genuinely zero modulo 27 and visibly nonzero over the integers.
The other six classes are their conjugate reversals.

## 4. Independent cubic characteristic-37 moment

For one channel let `f_j` be its actual signed Eisenstein coefficient on
`C_j=2^jH`, and define

```text
P_F=sum_(j=0)^11 8^j f_j                  modulo 37,
M_0=sum_(c in F_37) F(c).
```

For `z=(z_0,z_1)` and `w=(w_0,w_1)` in the basis `(1,omega)`, put

```text
det(z,w)=z_0 w_1-z_1 w_0.
```

The scalar

```text
J=det(P_A,M_(0,A))+det(P_B,M_(0,B))        modulo 37           (6)
```

is necessary for exact profile zero.  Indeed, for

```text
D(t)=sum_X sum_c F_X(c+t) conjugate(F_X(c)),
```

expanding `(d-c)^3` and using the order-three invariance kills the first
and second power moments, while

```text
sum_(x in C_j) x^3=3*8^j.
```

Hence

```text
sum_t t^3 D(t)
 =3J(omega^2-omega)
 =(-3J,-6J)                              modulo 37.            (7)
```

Exact correlation zero forces `J=0`.  The verifier independently evaluates
both sides of (7) for every joined assignment.

The two modulo-27 near witnesses have

```text
J=33,        J=23
```

respectively, so neither survives the independent moment.  Conversely,
`13,004` of the modulo-nine assignments pass `J`; none is among the two
modulo-27 assignments.

## 5. Symmetry coverage and the target count

The exact skeleton group is

```text
G=C_6 x C_(2,A) x C_(2,B),             |G|=24.
```

The verifier chooses the lexicographically least skeleton in every orbit,
leaving

```text
38,296 canonical skeletons.
```

It deliberately canonicalizes only the skeleton, not the
skeleton/target pair.  For every canonical skeleton it processes every one
of the 22 exact aggregate targets whose first uniformizer residues match.
This gives

```text
93,564 canonical-skeleton/target loops.
```

The earlier simultaneous Burnside quotient has 92,968
skeleton/target-pair orbits.  The difference

```text
93,564-92,968=596
```

is safe duplicate work from canonical-skeleton stabilizers, not an omitted
orbit.

Coverage is lossless.  Given any shell assignment, choose `g in G` sending
its skeleton to the canonical representative.  The transformed target is
still one of the 22 targets: channel star conjugates that channel's
Eisenstein target and the target set is closed under both channel stars.
Its residue necessarily matches the canonical skeleton, so the verifier
includes it.  The transformed high support and all medium/high phases are
then restored by the local tables.

## 6. Complete census

The deterministic counts are:

| gate | count |
|---|---:|
| signed skeletons | 908,800 |
| canonical skeletons | 38,296 |
| canonical-skeleton/target loops | 93,564 |
| three-high support trials | 17,424,680 |
| first-flag extendible supports | 1,817,356 |
| medium records | 470,489,796 |
| high records | 49,068,612 |
| modulo-nine plus exact-aggregate survivors | 479,850 |
| modulo-27 survivors | 2 |
| cubic-37 survivors | 13,004 |
| modulo-27 and cubic-37 survivors | 0 |
| detached exact replays | 479,850 |
| exact profile-zero survivors | 0 |

The exact replay is intentionally applied to every modulo-nine survivor,
not only to points passing the cubic moment.  Thus the final zero does not
depend on the characteristic-37 lemma.

## 7. Reproduction and checkpoints

Compile and run the complete verifier:

```text
clang++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic \
  verify_lp333_order3_profile_shell_three_mod27.cpp \
  -o /tmp/verify_lp333_order3_profile_shell_three_mod27

/tmp/verify_lp333_order3_profile_shell_three_mod27
```

The full run asserts every count in the table.  It can be resumed in
canonical-skeleton chunks:

```text
/tmp/verify_lp333_order3_profile_shell_three_mod27 \
  --skip 10000 --limit 5000
```

Eight chunks starting at `0,5000,...,35000` cover the complete canonical
set; the last contains 3,296 skeletons.  Independent complete runs produced
the same census.  The checkpoint run took about 168 seconds total and used
under 2 MB resident memory for the verifier itself.

The focused Python test checks the source and certificate hashes, replays
both near witnesses through an independent profile-correlation
implementation, verifies the cubic identity, checks target-set closure, and
compiles a deterministic one-skeleton fixture.

Pinned C++ source SHA-256:

```text
a6aac0af88e9ba1045da137ce71815c6a41341c981d9f6af5c757ec63958e091
```
