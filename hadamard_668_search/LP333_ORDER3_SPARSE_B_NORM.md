# Relative norms in the energy-six sparse-\(B\) sector

## Status

For each of the two extreme aggregate targets

```text
(5,1,0,0),       (4,-1,0,0),
```

the normalized \(B\)-profile energy-six sector admits a finite, exact
relative-norm screen.  Of its 396 structural \(B\) words:

```text
312 are impossible by an inert-prime odd-valuation obstruction;
 84 pass the relative field-norm condition.
```

Under the certified lift-compatible group \(C_6\times C_{2,B}\), these are
respectively 26 and 8 orbits out of 34.  Therefore the relative-norm screen
is a substantial exact pruning theorem, but it does **not** close either
target or the full energy-six sector.  A field norm is only a necessary
condition for a physical \(A\)-profile.

All structural counts and local obstructions are replayed without external
dependencies by `verify_lp333_order3_sparse_b_norm.py`.  The four positive
relative-norm answers are independently replayed in the cyclic quadratic
extension by `verify_lp333_order3_sparse_b_norm.gp`.

## 1. Why energy six is sparse

Write the actual \(B\)-class coefficients as \(b_j\in\mathbf Z[\omega]\),
\(j\in\mathbf Z/12\mathbf Z\).  The physical profile alphabet has squared
norms

```text
0, 3, 9.
```

The two displayed targets both impose

```text
sum_j b_j=0.
```

If the normalized \(B\)-energy is six, no norm-nine letter can occur, and
exactly two norm-three letters occur.  Their sum is zero.  Thus every word
has the unique form

```text
B(X)=2+z(eta_i(X)-eta_j(X)),       i != j,       Norm(z)=3,       (1)
```

where

```text
eta_i(X)=sum_(h in H) X^(2^i h),       H={1,10,26}.
```

There are six norm-three Eisenstein integers.  Since

```text
(i,j,z) and (j,i,-z)
```

give the same word, (1) yields exactly

```text
binom(12,2)*6=396                                             (2)
```

distinct structural \(B\)'s.

The distinguished coefficient is \(b(0)=2\), so the physical \(B\)-energy
is

```text
4+3*6=22.
```

The complementary \(A\)-energy is \(145\).  The two \(A\)-aggregates are

```text
14+3 omega,       11-3 omega,
```

which are conjugate and both have norm \(163\).  Hence both target norm
pairs are \((163,4)\), and the same \(B\)-screen applies to both.

## 2. Exact symmetry counts

The certified symmetry that is safe for the labelled lift is

```text
C6 x C2_B.
```

Here \(C_6\) is common even rotation of the twelve classes and \(C_{2,B}\)
is \(B\)-star:

```text
(b_j) -> (conjugate(b_(j+6))).
```

Burnside enumeration on the finite set (2) gives

```text
34 lift-safe orbits = 32 of size 12 + 2 of size 6.           (3)
```

For the relative-norm calculation only, one may use the larger Galois
action

```text
C12 x Gal(Q(omega)/Q).
```

This is not asserted to be a labelled-lift symmetry.  It merely preserves
relative-norm solvability.  It gives

```text
17 norm types = 16 of size 24 + 1 of size 12.                (4)
```

Normalize the cyclic separation to \(1\le d\le6\).  For \(d<6\), three
coefficient representatives suffice:

```text
z1=-2-omega,       z2=-1-2 omega,       z3=1-omega.
```

For \(d=6\), sign reversal is also absorbed by a half-turn, leaving only
\(z_1,z_2\).  These are the \(5\cdot3+2=17\) rows in the table below.

## 3. Uniform total positivity

Let

```text
L=Q(omega,zeta_37)^H,
M=L^(star),
```

where star is complex conjugation.  Then \(M\) is totally real of degree
12, \(L/M\) is cyclic quadratic, and

```text
L=M(omega).
```

At every primitive embedding, each \(\eta_i\) is a sum of three roots of
unity.  Therefore

```text
|B_sigma| <= 2+|z|(|eta_i|+|eta_j|)
           <= 2+6 sqrt(3).
```

The comparison with 167 is exact:

```text
(2+6 sqrt(3))^2 = 112+24 sqrt(3) < 167,
24^2*3=1728 < 3025=55^2.                                  (5)
```

Consequently every

```text
gamma=167-B B^star                                          (6)
```

in this sector is totally positive.  No row is lost merely through a
floating-point positivity test.

## 4. The inert-prime obstruction

If exact complementarity holds, then at a primitive 37th root

```text
gamma=A A^star=N_(L/M)(A).                                  (7)
```

At an unramified prime \(\mathfrak p\) of \(M\) that is inert in \(L/M\),
every relative norm has even \(\mathfrak p\)-adic valuation.

The totally real field \(M\) is defined by

```text
y^12-y^11-35y^10-17y^9+394y^8+574y^7-1395y^6-3344y^5
 +131y^4+5219y^3+4501y^2+1298y+121.                        (8)
```

The rational primes 11 and 101 split completely in \(M\).  Since each is
2 modulo 3, \(T^2+T+1\) is irreducible over every degree-one residue
field, so all primes above 11 and 101 are inert in \(L=M(\omega)\).

The dependency-free verifier evaluates (6) modulo \(p^2\) in an
unramified degree-six ring containing a primitive 37th root.  The pinned
degree-six factors are

```text
p=11:
x^6+x^5+3x^4+5x^3+3x^2+x+1,

p=101:
x^6+4x^5+50x^4+90x^3+50x^2+4x+1.
```

For both primes, the order of \(p\) modulo 37 is six,
\(p^3=-1\pmod {37}\), and

```text
{1,p^2,p^4} mod 37 = H.
```

Thus the \(H\)-periods lie in the quadratic residue subfield and inversion
is its nontrivial automorphism.  A residue that is zero modulo \(p\) but
nonzero modulo \(p^2\) proves valuation exactly one, giving a completely
finite local certificate.

## 5. Complete norm-type table

The columns `simple 11` and `simple 101` count degree-one primes where
\(\gamma\) has valuation exactly one.

| \(d\) | \(z\) | field orbit | simple 11 | simple 101 | result |
|---:|---|---:|---:|---:|---|
| 1 | \(-2-\omega\) | 24 | 2 | 0 | obstructed at 11 |
| 1 | \(-1-2\omega\) | 24 | 0 | 0 | relative norm |
| 1 | \(1-\omega\) | 24 | 2 | 0 | obstructed at 11 |
| 2 | \(-2-\omega\) | 24 | 2 | 0 | obstructed at 11 |
| 2 | \(-1-2\omega\) | 24 | 1 | 0 | obstructed at 11 |
| 2 | \(1-\omega\) | 24 | 2 | 0 | obstructed at 11 |
| 3 | \(-2-\omega\) | 24 | 0 | 0 | relative norm |
| 3 | \(-1-2\omega\) | 24 | 1 | 0 | obstructed at 11 |
| 3 | \(1-\omega\) | 24 | 2 | 0 | obstructed at 11 |
| 4 | \(-2-\omega\) | 24 | 0 | 1 | obstructed at 101 |
| 4 | \(-1-2\omega\) | 24 | 2 | 0 | obstructed at 11 |
| 4 | \(1-\omega\) | 24 | 1 | 0 | obstructed at 11 |
| 5 | \(-2-\omega\) | 24 | 1 | 1 | obstructed at 11 (also 101) |
| 5 | \(-1-2\omega\) | 24 | 1 | 0 | obstructed at 11 |
| 5 | \(1-\omega\) | 24 | 2 | 0 | obstructed at 11 |
| 6 | \(-2-\omega\) | 24 | 0 | 0 | relative norm |
| 6 | \(-1-2\omega\) | 12 | 0 | 0 | relative norm |

Thus 13 of the 17 field types are impossible.  Their orbit sizes total

```text
13*24=312.
```

PARI/GP's exact `rnfisnorm` returns quotient \(q=1\) for precisely the four
displayed survivors:

```text
(d,z)=(1,-1-2 omega),
      (3,-2-omega),
      (6,-2-omega),
      (6,-1-2 omega).                                    (9)
```

Because \(L/M\) is Galois, this `rnfisnorm` answer is guaranteed rather
than conditional on GRH.  The orbit sizes in (9) are \(24,24,24,12\), so
they contain exactly

```text
84 raw B words.
```

They split into eight lift-safe orbits: six of size 12 and two of size 6.
The 312 excluded words form 26 lift-safe orbits, all of size 12.

## 6. Exact scope

The theorem proves:

```text
312/396 structural B words cannot occur in exact complementarity.
```

It does not prove:

- that any of the 84 surviving \(B\)'s has an \(A\)-profile;
- that the relative-norm witness returned by PARI has the physical
  coefficient alphabet, aggregate, or integrality required here;
- that either aggregate target is infeasible;
- that an LP(333) or an H(668) has been constructed.

The next theory-led step should work only on the four norm types (9), using
the fixed \(A\)-aggregate, normalized \(A\)-energy 48, and the ten-letter
profile alphabet.  No unrestricted 24-profile search is justified by this
result.

## Reproduction

From `hadamard_668_search`:

```text
python3 verify_lp333_order3_sparse_b_norm.py
python3 -m unittest -v test_lp333_order3_sparse_b_norm.py
gp -q verify_lp333_order3_sparse_b_norm.gp
```

The Python verifier uses only the standard library.  The GP replay pins
the real field (8), recomputes exact ideal valuations above 11 and 101,
and applies the guaranteed cyclic relative-norm test to the four residual
types.  Its PARI stack is capped at 1.5 GB.
