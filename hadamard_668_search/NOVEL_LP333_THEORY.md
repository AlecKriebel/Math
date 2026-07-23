# A theory-first `LP(333)` route

## Status

No Legendre pair of length `333`, and hence no Hadamard matrix of order
`668`, is claimed here.

The useful outcome is an exact cyclotomic reduction.  Inside one natural
order-nine multiplier subfamily, the `166` independent PAF equations become
`22` coupled equations on only `45` fourth roots of unity.  Those equations
split into six coordinate-axis equations and sixteen genuinely mixed
equations.  An explicit quotient array satisfies the fixed compression and
every equation on both axes, so the sixteen mixed equations are the sole
remaining obstruction in this subfamily.

The dependency-free checker is:

```sh
python3 check_lp333_quartic_quotient.py
```

It labels the displayed array a non-candidate and reports all remaining
defects.

## 1. Two exact reformulations

Let `A,B : Z_333 -> {+1,-1}` be normalized by

```text
sum A = sum B = 1.
```

They are a Legendre pair exactly when

```text
PAF_A(t) + PAF_B(t) = -2,       t != 0.
```

### 1.1 Difference-family form

Let `X,Y` be the negative supports of `A,B`.  Each has size `166`.  Direct
expansion gives the group-ring identity

```text
X X^(-1) + Y Y^(-1) = 167 e + 165 G                    (1)
```

in `Z[Z_333]`, where `G` is the sum of all group elements.  Equivalently,
every nonzero difference occurs `165` times across the two blocks.  Thus the
Legendre route is the cyclic supplementary difference family

```text
(333; 166,166; 165).
```

This is a proved equivalence, not an ansatz.

### 1.2 One QPSK sequence

Define

```text
u(x) = (A(x) + i B(x)) / (1+i).
```

Then `u(x)` is a fourth root of unity and

```text
Re sum_x u(x) conjugate(u(x+t))
  = (PAF_A(t) + PAF_B(t))/2.                            (2)
```

Consequently:

> **QPSK equivalence.** A normalized binary pair `A,B` is an `LP(333)` if
> and only if `u : Z_333 -> {1,i,-1,-i}` has `sum u=1` and
> `Re PAF_u(t)=-1` at every nonzero lag.

Only the real part is prescribed.  Requiring the full complex PAF to be `-1`
would be a strictly stronger circulant-core `BH(4,334)` construction.

Arrange `u` on the CRT product

```text
Z_333 = Z_9 x F_37.
```

The conjecturally motivated length-37 compression already used in this
repository becomes especially simple:

```text
sum_r u(r,0) = 1,
sum_r u(r,c) = -3 i chi(c),       c != 0,               (3)
```

where `chi` is the quadratic character of `F_37`.

Equations (2)--(3) are the starting point below.

## 2. General CRT/Fourier decomposition

Write `A_r(c)=A(r,c)`, and similarly for `B`.  For an additive character
`psi_s` of `F_37`, put

```text
a_s(r) = sum_c A_r(c) psi_s(-c),
b_s(r) = sum_c B_r(c) psi_s(-c).
```

Fourier transformation only in the `F_37` coordinate gives

```text
K_s(a) =
  sum_r [a_s(r) conjugate(a_s(r+a))
       + b_s(r) conjugate(b_s(r+a))].
```

The full Legendre equations are equivalent to the following exact table:

```text
                    s=0       s != 0
a=0                  594          668
a != 0               -74            0.                 (4)
```

Indeed, (4) is just the length-37 Fourier transform of the target
correlation array, whose value is `666` at `(0,0)` and `-2` elsewhere.

This does not by itself reduce the number of equations, but it identifies the
right construction object: nine row spectra must form vector-valued
complementary sequences at every nontrivial character of `F_37`.

## 3. The unexpected `37=4*9+1` design

Let

```text
H = <16>
  = {1,7,9,10,12,16,26,33,34} subset F_37^*.
```

This is the subgroup of quartic residues, of order `9`.  Direct difference
counting gives

```text
1_H 1_H^(-1) = 7 e + 2 F_37,                            (5)
```

so `H` is a cyclic `(37,9,2)` difference set.  The equality of its size with
the other CRT factor is the key arithmetic feature missed by the earlier
profile searches.

Let

```text
C_j = 2^j H,             j=0,1,2,3.
```

The quadratic character is `+1` on `C_0,C_2` and `-1` on `C_1,C_3`.

## 4. Exact quartic quotient: `166 -> 22`

Consider the motivated subfamily

```text
u(r,hc) = u(r,c)          for every h in H.              (6)
```

This is common multiplier invariance of `A` and `B`, not a necessary
condition for a general `LP(333)`.  It is stronger than the order-three
multiplier sublane already in the repository.

For each CRT row, (6) leaves five phases:

```text
x_0(r) = u(r,0),
x_(j+1)(r) = u(r,c),      c in C_j.
```

Thus the entire `333`-phase array is represented by `45` QPSK phases.  The
fixed compression is exactly

```text
sum x_0 = 1,
sum x_1 = sum x_3 = -3i,
sum x_2 = sum x_4 =  3i.                                (7)
```

For `b in C_s`, define the explicit cyclotomic transition matrix

```text
M_s(k,l) = #{c in P_k : c+b in P_l},
P_0={0}, P_(j+1)=C_j.                                   (8)
```

The four integer `5 x 5` matrices are pinned independently in
`check_lp333_quartic_quotient.py`.  If

```text
Q_s(a) =
  Re sum_(r,k,l) M_s(k,l) x_k(r) conjugate(x_l(r+a)),
```

then the nonzero-column equations are simply

```text
Q_s(a) = -1.                                             (9)
```

For column lag zero, replace `M_s` by

```text
D = diag(1,9,9,9,9).                                    (10)
```

Negating a lag identifies `C_0` with `C_2` and `C_1` with `C_3` when the row
lag is zero.  Therefore the independent quotient equations are:

```text
row lag 0:       2 nonzero-column equations;
row lags 1..4:  4 * (one zero-column + four nonzero-column)
               = 20 equations.
```

This proves:

> **Quartic quotient theorem.** Subject to (6) and (7), a QPSK array yields
> an `LP(333)` if and only if the `22` integer equations (9)--(10) hold.

This is an exact equivalence inside the stated subfamily.  It is not a
relaxation and does not sample compressed profiles.

## 5. The row-axis equations factor completely

Put `z=x_0`.  For a nonzero row lag `a`, the zero-column equation is

```text
R_a + 9 S_a = -1,                                       (11)
```

where

```text
R_a = Re PAF_z(a),
S_a = sum_(j=1)^4 Re PAF_(x_j)(a).
```

Every summand in `R_a` lies in `{-1,0,1}`, so `-9 <= R_a <= 9`.
Equation (11) implies

```text
R_a in {-1,8}.
```

But `sum z=1`, hence

```text
9 + 2 sum_(a=1)^4 R_a = |sum z|^2 = 1.
```

The four values must therefore all be `-1`.  Substitution in (11) gives
`S_a=0`.  We obtain another proved equivalence:

> **Axis factorization.** The four nontrivial row-axis equations hold if and
> only if
>
> ```text
> sum z=1,       Re PAF_z(a)=-1,
> sum_j Re PAF_(x_j)(a)=0,             a=1,2,3,4.
> ```

So the zero cell is a length-9 real-perfect QPSK sequence, while the four
quartic-class columns form a real periodic complementary family.
By the QPSK equivalence itself, `z` is exactly the encoding of a normalized
binary `LP(9)`.  The order-333 problem has therefore exposed a genuine
recursive Legendre core, not merely a numerical compression.

A complete `4^9` enumeration, reproduced by the checker, finds:

```text
972   length-9 z with sum 1 and Re PAF_z(a)=-1;
7056  length-9 w with sum -3i;
324   distinct complex PAF signatures among those 7056 w.
```

The checker also pins an explicit complex-complementary quadruple of the
`w` sequences.  Negation supplies the required `+3i` sums without changing
autocorrelation.

This changes the prospective construction from a `666`-bit search into a
finite assembly problem on short complementary objects.

## 6. An exact axis-complete skeleton

The following rows list phase exponents modulo four at

```text
(0,C_0,C_1,C_2,C_3),
```

with exponent `e` denoting `i^e`:

```text
(3,3,1,3,1)
(0,0,2,3,1)
(2,0,1,3,2)
(2,2,0,2,0)
(0,0,3,1,2)
(1,2,0,3,1)
(0,3,1,2,1)
(1,3,1,0,3)
(3,2,2,0,0)
```

Exact independent expansion verifies:

```text
the five compression equations (7);
all 36 nonzero pure-column correlations;
all 8 nonzero pure-row correlations.
```

Thus 44 of the 332 oriented nonzero CRT lags are already exact.  In the
independent half of the full problem, the remaining mixed region has:

```text
126 bad lags among 144 tested mixed lags;
sum (Re PAF_u + 1)^2 = 13824.
```

This skeleton is deliberately a non-candidate.  Its importance is logical:
there is no hidden incompatibility between the prescribed compression and
the two coordinate-axis systems.  All remaining difficulty is in the
sixteen mixed cyclotomic equations.

## 7. A natural construction that is genuinely impossible

There is a perfect QPSK Paley core of length `37`:

```text
g = i delta_0 + chi,
sum g = i,
PAF_g(t) = -1 for t != 0.
```

It is tempting to take the nine CRT rows to be phased translates of `g`.
This cannot even realize the fixed compression.

If the rows are `lambda_r g(c-t_r)`, let

```text
w = sum_r lambda_r delta_(t_r).
```

Their column sum is `w*g`, and (3) would require

```text
w*g = delta_0 - 3i chi.
```

Using

```text
chi*chi = 37 delta_0 - J,
J*g = iJ,
```

the unique solution in the group algebra is

```text
w = (-56i delta_0 - chi + iJ)/19.                       (12)
```

Its coefficients are nonintegral:

```text
w(0)              = -55i/19,
w(quadratic)      = (-1+i)/19,
w(nonquadratic)   = ( 1+i)/19.
```

On the other hand, a sum of phased point masses has Gaussian-integer
coefficients.  Equation (12) is therefore impossible.

This refutes the simplest Paley-row lift completely and explains why a
cyclotomic incidence construction, rather than translated perfect rows, is
needed.

## 8. Computational probes, carefully delimited

These are solver diagnostics, not proof certificates.

- For the common order-nine multiplier with column multiplier `16`, the two
  nontrivial homomorphisms to `U(9)` (row multipliers `4` and `7`) were
  reported infeasible by small CP-SAT models.  The trivial row multiplier is
  the quartic quotient above.
- A one-worker `300`-second run of that full `45`-phase quotient ended
  `UNKNOWN` after `14,343,971` branches and `3,816,619` conflicts.  It neither
  found a pair nor excluded the subfamily.
- Adding the exact `972`-row table forced by the axis factorization and using
  four workers still ended `UNKNOWN` after `300.085` seconds, `7,835,678`
  branches, and `382,823` conflicts.  This is evidence that the sixteen
  mixed equations, rather than the short `LP(9)` core, are the bottleneck.
- The axis-complete skeleton was found in a restricted quotient model and is
  then verified from scratch by the standard-library checker.

The negative local-search checkpoints in `LEGENDRE_LOCAL_NOTES.md` concern
different fixed row-profile fibers.  They neither imply nor contradict this
quartic construction.

## 9. Proved, conjectural, and refuted

### Proved here

- the difference-family identity (1);
- the QPSK equivalence (2) and compressed target (3);
- the CRT/Fourier table (4);
- the `(37,9,2)` quartic-residue identity (5);
- the exact `45`-phase, `22`-equation quotient;
- the row-axis factorization;
- the Paley-translate obstruction (12);
- the arithmetic properties of the displayed axis-complete skeleton.

### Open or conjectural

- Whether the sixteen mixed equations have a solution together with the six
  axis equations.
- Whether an `LP(333)` exists in the quartic-invariant subfamily.
- Whether the factor-9 compressed family contains any `LP(333)`.
- Whether any `LP(333)`, or any Hadamard matrix of order `668`, exists.

### Refuted

- The nine phased-translate Paley-row construction.
- Merely permuting the rows of either frozen pure-column multiset tested
  during this derivation; those finite failures do not refute the full
  quotient.

## 10. Best concrete next construction

`search_lp333_quartic_quotient.cpp` implements the first structured
constructor.  It never leaves the exact row-axis fiber:

- `z` is always one of the `972` real-perfect sequences;
- each `w` always has the required phase sum;
- the `7056` possible `w` sequences are grouped into only `28` real PAF
  signatures;
- single replacements stay inside a signature bucket, while paired
  replacements use a hash lookup for the complementary signature.

Thus every proposal satisfies the fixed compression and all four row-axis
equations.  Its objective contains only the two pure-column and sixteen
mixed quotient equations.  Compile and run it with:

```sh
clang++ -O3 -DNDEBUG -std=c++17 -Wall -Wextra -Wpedantic \
  search_lp333_quartic_quotient.cpp \
  -o ../tmp/search_lp333_quartic_quotient
../tmp/search_lp333_quartic_quotient \
  --seconds 60 --seed 1668 --epoch 150000 \
  --temperature-start 512 --temperature-end 0.25
```

The bounded pilot processed `37,492,829` exact axis-preserving proposals
across `252` restarts.  It retained quotient energy `112`, down from `1536`
for the axis-complete starting skeleton:

```text
14/18 remaining quotient equations bad;
126/162 remaining independent lags bad;
126/166 full independent lags bad;
2/2 pure-column quotient equations bad;
12/16 mixed quotient equations bad;
maximum absolute QPSK residual 6;
full independent-lag residual energy 1008.
```

The exact residual vector is

```text
pure column:  ( 2,-2)
mixed a=1:   ( 2, 2,-2, 0)
mixed a=2:   ( 2, 2, 2, 0)
mixed a=3:   (-4,-6,-2, 0)
mixed a=4:   (-2, 0, 2, 4).
```

The pilot used about `5.8 MB` peak RSS and no swap.  Its phase table is frozen
in the source as the next-run incumbent.  It is a non-candidate.  If the
objective reaches zero, the constructor expands the phases, inverts the QPSK
encoding, and checks all `332` oriented nonzero binary correlations before
returning success.

The exact completion strategy should continue to work entirely with the
short objects from the axis factorization:

1. enumerate the `972` admissible `z` sequences modulo dihedral symmetry and
   conjugation;
2. enumerate the `324` target-sum autocorrelation signatures for `w`;
3. form complementary quadruples by hashing two-signature sums against their
   negatives;
4. impose the two pure-column equations using the exact matrices `M_s`;
5. hash the resulting left/right mixed-correlation vectors for the sixteen
   remaining equations.

The finish line for this construction is one `9 x 5` exponent table passing
all `22` quotient equations.  Expansion is then deterministic: map each
quartic class to its phase, invert

```text
u=(A+iB)/(1+i),
```

and run `verify_legendre_333.py` to construct and check the full bordered
`668 x 668` Hadamard matrix.

If the exact quotient is eventually certified empty, the next relaxation
should break quartic invariance in one controlled `H`-orbit at a time while
retaining the QPSK compression and axis-factorization constraints.  That is
a mathematically organized lift, not an unrestricted restart.

## 11. Priority caution

The local literature audit records an exhaustive March 2026 computation of
millions of compatible factor-9 compressions.  Nothing in the locally
available notes states this QPSK/quartic quotient or the axis factorization,
but that is not enough to establish external novelty.  Treat the mathematics
above as an independent research lead until a full literature comparison is
possible.  Under the repository policy, no outside contact is to be prepared
or attempted.
