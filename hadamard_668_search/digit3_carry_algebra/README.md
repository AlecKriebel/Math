# Compact carry algebra for the third and fourth placement digits

## Status

This scratch package gives an exact reduction of every displayed phase
coefficient to two signed-cardinality statistics.  It also exposes a
previously hidden nineteenth equation at the third digit and supplies two
smaller CP-SAT models.  It has not yet produced a digit-3 witness, a
digit-4 witness, an exact `LP(333)`, or `H(668)`.

The principal verifier is:

```text
python3 audit_digit3_carry.py
```

The exact delayed-origin count is:

```text
python3 verify_e1_origin_exact_dp.py
```

The dependency-free regression suite is:

```text
python3 -m unittest -v test_digit3_algebra.py
```

The solver scripts require the local Python environment containing OR-Tools.
Every solver result is bounded: `UNKNOWN` is not an exclusion.

## 1. Two exact integer statistics

For one displayed row, let `n_j` be the signed number of phase terms whose
canonical exponent is `j in {0,1,2}`, and let `T` be the row target.  Thus

```text
F = n_0 + n_1 omega + n_2 omega^2 - T.
```

Put

```text
C = n_0+n_1+n_2-T,
A = C - sum_t sigma_t L_t
  = n_0-n_2-T,
Q = C/3 - sum_t sigma_t 1[L_t=2]
  = (n_0+n_1-2n_2-T)/3.
```

The shell hypotheses make `C/3` integral.  Using
`omega^2=-1-omega` gives the exact identity

```text
F = A + (3Q-A) omega.                                  (1)
```

In particular, exact vanishing is the signed-histogram condition

```text
n_0-T = n_1 = n_2,
```

equivalently `A=Q=0`.  No lambda-adic truncation is involved in this
equivalence.

For `m>=1`, (1) gives the complete prefix lattice:

```text
digits 0,...,2m-1 vanish  iff  A=0 mod 3^m,
                                  Q=0 mod 3^(m-1);

digits 0,...,2m vanish    iff  A=0 mod 3^m,
                                  Q=0 mod 3^m.
```

Thus the new layers are:

```text
through digit 2:   A=0 mod 3,   Q=0 mod 3;
through digit 3:   A=0 mod 9,   Q=0 mod 3;
through digit 4:   A=0 mod 9,   Q=0 mod 9;
through digit 8:   A=0 mod 81,  Q=0 mod 81.
```

The audit reconstructs all twenty exact Eisenstein coefficients from
`(A,Q)` and independently matches every prefix condition through digit 8.

## 2. Carry degrees and the hidden nineteenth equation

On the first-digit affine space write each phase exponent as

```text
L = (d+s.y) mod 3,          y in F_3^36.
```

The second-digit equation is `Q mod 3`; since

```text
1[L=2] = 2L^2+L
```

over `F_3`, the eighteen nonzero second-digit equations are quadratic.

The next equation is `A/3 mod 3`.  Writing

```text
L = d+s.y - 3 floor((d+s.y)/3)
```

shows that it is an affine term plus first ternary carries.  The reduced
carry is cubic over `F_3`.  Therefore the generic third-digit system is
eighteen quadratics plus cubic carry equations.

There is one crucial exception.  The displayed `E1(origin)` row (row 7)
has 42 sparse forms, with every multiplicity equal to `+3` or `-3`.
Its second digit is identically zero, but division by the common factor
three reveals a **linear third-digit equation**.  It is independent of the
rank-18 first-digit system:

```text
first-digit rank                         18
rank after delayed E1(origin) row        19
remaining affine dimension              35
```

Consequently a full digit-3 witness must solve eighteen quadratic and
nineteen third-digit equations in 36 variables.  At the pinned full
second-digit witness, the quadratic residual is zero, 17 of the 19
third-digit rows are nonzero, and the `37 x 36` combined Jacobian has full
column rank 36.  Its linearized correction system is inconsistent.  This
is a negative local finding, not a global obstruction.

The next `E1(origin)` layer is quadratic.  Its polar rank is 16 on the
36-space and 14 after restriction to the delayed linear hyperplane.

## 3. Exact local theorem for E1(origin)

The 42 row-7 forms are all supported on two original placement trits and
split into 22 disjoint `(channel,class)` blocks:

```text
12 singleton blocks,
10 three-cycle blocks.
```

After dividing the exact coefficient by 3, each singleton contributes
`-omega^a`, while each three-cycle contributes
`(1-omega)omega^b`.  Hence the exact row is

```text
-sum_(i=1)^12 omega^a_i
 +(1-omega) sum_(j=1)^10 omega^b_j = 0.                (2)
```

There are only `91*66=6006` pairs of orientation-count triples in (2).
Exactly 30 pairs work.  Their multinomial weights sum to

```text
596,095,200 of 3^22 = 31,381,059,609 orientations,
fraction 0.01899538152717576.
```

`verify_e1_origin_exact_dp.py` obtains this number both from the 6,006
count-pair enumeration and from an independent Eisenstein-coordinate
dynamic program.  It also derives the singleton and three-cycle catalogs
directly from the pinned phase forms.

This exact row is about 17.55 times more selective than its third-digit
linear condition alone.  The sparse solver therefore has an optional
`digit3_exact_row7` mode: it requires (2) exactly while requiring only the
digit-3 prefix on the other displayed rows.

## 4. Smaller exact solver models

`solve_carry_cp_sat.py` works on the 36 affine coordinates.  For profile
`h2-422220-0` its digit-3 model has:

```text
3,044 variables,
2,018 constraints,
990 distinct effective phase forms.
```

`solve_sparse_histogram_cp_sat.py` instead works on the original 54 trits.
Every phase form depends on at most two trits and is encoded by a table of
at most nine rows.  The profile has:

```text
993 distinct sparse phase forms:
  1 constant, 118 one-variable, 874 two-variable;
8,221 total allowed table rows;
2,099 variables and 1,052 constraints
  after explicitly exposing the rank-18 first layer
  and delayed nineteenth linear row.
```

The exact mode asserts `A=Q=0`, i.e. equality of the three signed histogram
cardinalities, rather than asking a solver to rediscover exactness through
nine modular digits.

The sparse solver also has a `digit2` mode and an optional exact
`--row-margins` join.  The join exposes the twelve integer coordinates of
the six phase sums and requires their tuple to belong to the profile's
complete compatible row-margin corpus.  `--row-margin-target INDEX` fixes
one corpus member for shardable searches.  On candidate 0, a 300-second
four-worker union run and eight sampled 30-second one-worker target shards
were all `UNKNOWN`; these are bounded hardness observations, not
exclusions.

`search_row_margin_permutation_tabu.py` supplies a solver-independent
stochastic control inside one selected target: every pair move preserves
the exact six phase sums, while the objective repairs the first layer
lexicographically before digit 2.  Its initial 60-second target-0 run
reached `(2,9)` nonzero first-/second-digit rows and remained `UNKNOWN`.

An initial 180-second run of the version before the explicit 19 linear
rows, on candidate 1 with four workers, ended `UNKNOWN` after 1,341,326
branches and 18,835 conflicts.  Peak resident memory was approximately
517 MB.  This is a negative bounded result only.

## 5. Degree-3 XL closes no additional equation

`audit_digit3_xl.py` eliminates the delayed linear row exactly, leaving
35 variables.  It derives the other eighteen digit-3 polynomials with the
Lucas/Vandermonde carry identity

```text
floor(S/3) = binom(S,3) mod 3.
```

It then forms:

```text
18 digit-3 cubics;
18*(1+35) affine multiples of the 18 digit-2 quadrics;
666 rows total;
8,401 reduced monomials through degree 3.
```

Exact bit-packed elimination over `F_3` gives:

```text
full XL rank                              666
cubic-projection rank                    648
degree <= 2 intersection dimension        18
original quadric span dimension           18
degree <= 1 intersection dimension         0
constant-only intersection dimension       0
```

Thus this degree-3 XL system has no refutation and yields no new quadratic
or linear consequence beyond the original eighteen quadrics.  All 666
generators are independent, while the only combinations cancelling their
cubic parts recover the known quadric span.  This is an exact negative
result against a low-degree algebraic closure, not evidence that a
digit-3 witness exists.

## 6. Pinned semantic hashes

```text
carry and delayed-row audit
  a862b985fac4fe153465e03fdda51b82deccdb9020c82aff5600d9c96b68d427

exact E1-origin orientation DP
  0f5d0a8dc5364cd1c9d440d14b08a9c9bc40ad698c5dd207f841b828cd1dce83

degree-3 XL audit
  a92083fcb42ba0d9745bc7907b26e523804a7ee49f05e5f272bbc009db637bd6
```
