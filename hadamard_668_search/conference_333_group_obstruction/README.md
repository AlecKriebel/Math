# Cayley-core conference obstruction at order 334

## Result

There is no normalized conference matrix of order 334 whose `333 x 333`
core is developed over a group of order \(333=37\cdot9\).  Equivalently,
no group of order 333 contains a Paley-type partial difference set with
parameters

```text
(v,k,lambda,mu) = (333,166,82,83).
```

More explicitly, for no group \(G\) of order 333 is there an integral
group-ring element

```text
F = sum_(g in G) f_g g,
f_e = 0,
f_g in {+1,-1} for g != e,
```

such that

```text
F F^(-1) = 333 e - sum_(g in G) g.                    (1)
```

Equation (1) is the periodic correlation equation for the `333 x 333`
core of a group-developed conference matrix of order 334.  A symmetric
conference matrix of order 334 would give a Hadamard matrix of order 668
by the standard conference doubling construction.  The theorem excludes
this entire alternative `H(668)` family, over every abelian or nonabelian
group of order 333.

It does not exclude symmetric conference matrices without a regular group
of order 333, Legendre pairs, Eliahou repairs, or arbitrary Hadamard
matrices of order 668.

## One-character proof

The obstruction has a short proof.  The longer quotient classifications
below are retained as an independent exact certificate and because their
coset-shadow structure may be useful elsewhere.

Every group \(G\) of order 333 has a unique normal Sylow-37 subgroup
\(N\): the number of such subgroups divides 9 and is 1 modulo 37.  The
quotient \(G/N\), of order nine, has a quotient `C3`.  Inflate a
nonprincipal character

```text
chi : G -> C3 -> {1, omega, omega^2}.
```

The group-ring equation (1) and the forced inversion identity proved in
the next section give

```text
chi(F)^2 = 333.                                        (2)
```

On the other hand, `F=F^(-1)` makes `chi(F)` real, while an integral sum of
third roots of unity lies in `Z[omega]`.  Hence

```text
chi(F) in R intersect Z[omega] = Z.
```

No integer has square 333.  This contradiction proves the result.

In partial-difference-set language, the same calculation is the standard
linear-character condition

```text
chi(D) = (-1 +/- sqrt(333))/2,
```

which cannot be the value of an order-three character on an
inverse-closed integral group-ring subset.

The argument gives a general quotient obstruction.

> If a group of nonsquare order \(v\equiv1\pmod4\) has a quotient of
> prime order \(r\) and contains a Paley-type partial difference set,
> then the squarefree part of \(v\) is \(r\) and \(r\equiv1\pmod4\).

Indeed, the nonprincipal order-\(r\) character forces
`Q(sqrt(v))` to be the unique quadratic subfield of `Q(zeta_r)`.
Consequently, if \(p>q^2\) are distinct odd primes and
\(pq^2\equiv1\pmod4\), no group of order \(pq^2\) has a Paley-type
partial difference set: its normal Sylow-\(p\) subgroup supplies a
quotient `Cq`, but the required quadratic field is `Q(sqrt(p))`.

## Inversion is forced

No symmetry hypothesis is needed.  The augmentation of (1) forces exactly
166 negative coefficients.  If `D` is their subset, then

```text
F = G - e - 2D.
```

Expanding (1) gives

```text
D + D^(-1) + 2 D D^(-1) = 166(e+G).                   (2)
```

Modulo two this is

```text
D + D^(-1) = 0.
```

Each coefficient on the left is the sum of two zero-one indicators, so it
is even exactly when the indicators agree.  Hence

```text
D = D^(-1),  and therefore F = F^(-1).                 (3)
```

Thus every group-developed conference core in this odd-order setting is
automatically inversion-symmetric.

Substituting (3) back into (2) gives

```text
D D^(-1) = 83(e+G)-D,
```

which is exactly the group-ring equation for a regular
`(333,166,82,83)` Paley-type partial difference set.

## Independent cyclic-quotient certificate

Push (1) through `G -> C9`.  If

```text
S = (s_0,...,s_8)
```

is the vector of signed sums on the nine cosets of the kernel, then

```text
S S^(-1) = 333 e - 37 J_9.                            (4)
```

Consequently,

```text
sum_i s_i                    = 0,
sum_i s_i^2                  = 296,
sum_i s_i s_(i+k)            = -37,  1 <= k <= 8.     (5)
```

The identity coset contains the single zero coefficient and 36 signs, so
`s_0` is even.  Every other coset contains 37 signs, so
`s_1,...,s_8` are odd.  The energy in (3) bounds the even entry by 16 and
the odd entries by 17 in absolute value.

Push (4) once more through `C9 -> C3`.  Put

```text
A = s_0+s_3+s_6,
B = s_1+s_4+s_7,
C = s_2+s_5+s_8.
```

Then

```text
A+B+C = 0,
A^2+B^2+C^2 = 222,
AB+BC+CA = -111,
```

with `A` even and `B,C` odd.  These equations have exactly four ordered
solutions:

```text
(-10,-1,11), (-10,11,-1), (10,-11,1), (10,1,-11).
```

For each triple, exact bounded enumeration leaves 9,306 vectors satisfying
the parity, residue-class sums, and zero-lag energy.  None satisfies the
four independent nonzero cyclic correlations.  Thus all

```text
4 * 9,306 = 37,224
```

possible cyclic-quotient vectors are excluded.

## Independent elementary-abelian certificate

Now push (1) through `G -> C3 x C3`.  The signed coset-sum function `s`
must obey

```text
s s^(-1) = 333 e - 37 J_(C3 x C3).                    (6)
```

There are four quotient maps from `C3 x C3` onto `C3`, one for each
one-dimensional kernel.  Every one of their three-coordinate pushforwards
must be one of the four profiles displayed above.

Assign one of the four profiles to each of the four directions.  There are
only `4^4=256` assignments.  If `L_d(p)` is the assigned sum on the line
of direction `d` through a point `p`, the affine-plane incidence identity
gives the unique possible coefficient

```text
s(p) = (1/3) sum_(four lines through p) L_d(p).        (7)
```

Exactly 96 assignments make (7) integral.  All 96 reproduce their assigned
line sums, have the forced `even,odd,...,odd` parities, and satisfy (6).
They form one orbit under `GL(2,3)` together with global sign.

However, none satisfies

```text
s(p) = s(-p).                                          (8)
```

The forced inversion identity (3) necessarily pushes to (8).  Thus the
elementary-abelian quotient admits 96 formal nonsymmetric coset shadows,
but none can lift to a group-developed conference core.

## Verification

Run:

```text
python3 verify_conference_333_group_obstruction.py
```

The dependency-free verifier:

1. derives the parity-bounded coordinate domains;
2. solves the `C3` quotient equations by direct exact enumeration;
3. reconstructs all 37,224 energy-compatible `C9` vectors;
4. checks every independent cyclic correlation;
5. reconstructs all 256 affine-plane Radon assignments for `C3 x C3`;
6. checks the group-ring parity lemma forcing inversion, then proves that
   the 96 perfect profiles form one symmetry orbit and that zero are
   inversion-invariant; and
7. compares the complete count record with
   `CONFERENCE_333_GROUP_CERTIFICATE.json`.

The result is a delimited obstruction, not a construction of `H(668)`.

## Literature and priority boundary

The character-eigenvalue identity is prior and standard, not a local
discovery.  In particular, Nelson and Swartz explicitly state that
nonprincipal linear characters of a PDS in a nonabelian group must take
one of its two nonprincipal eigenvalues:

<https://arxiv.org/abs/2507.23039>

Wang completely classifies the *abelian* orders supporting Paley-type
partial difference sets.  Her theorem already excludes abelian groups of
order 333:

<https://arxiv.org/abs/1908.07055>

Davis, Polhill, Smith, and Swartz emphasize that nonabelian Paley-type
partial difference sets are a very recent and comparatively undeveloped
subject:

<https://doi.org/10.5802/alco.416>

No order-333 statement or the prime-quotient corollary above was located in
the checked sources.  Nevertheless, it is an immediate application of the
known linear-character identity plus Sylow theory.  It should be treated
as a clean, useful exclusion of one `H(668)` construction family, not as a
major standalone discovery without a broader literature review.  The
37,224-vector cyclic quotient census and the 96-profile affine-plane
classification are stronger computational anatomy of the same
obstruction, but are not needed for nonexistence.
