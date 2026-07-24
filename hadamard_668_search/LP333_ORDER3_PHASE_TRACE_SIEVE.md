# Factorwise trace and Parseval sieve for the prime-167 phase cone

## Status

The four blocks in the prime-167 ninth-root cone retain enough Galois
structure to recover the original six Eisenstein fiber words without an
inverse 37-point CRT.  After that three-by-three recovery, every physical
candidate must pass:

```text
12 ambient-independent F_167-linear equations fixing the normalized zero
column;

 6 ambient-independent F_167 Hermitian forms fixing the six fiber supports.
```

The cone already supplies the sum of the six support equations.  After
using that one displayed equation, a fixed profile leaves five further
profile-resolved scalar equations.  Together, the trace front end displays

```text
12 universal linear equations + 5 profile-specific support equations
    = 17 equations.
```

before reconstructing any of the twelve nonzero physical column classes.
This is an equation-count and redundancy statement, not a claim that the
five equations have codimension five on the locus already cut out by the
cone and zero-column equations.

Each reconstructed class coefficient then has a complete lookup-free
physicality test: the known weight and residue profile fill three ninth-root
Fourier channels, its six Frobenius conjugates fill the other six, and
nine inverse-DFT values must satisfy `b^2=b`.  This is an if-and-only-if
decoder for the actual weight-three and weight-six normalization branches.

An exhaustive classification of the 84 normalized weight-three row words
also gives a seven-value local norm alphabet.  Its two nonzero branches
satisfy explicit cubic polynomials, and the prime-field trace of the local
norm is exactly three times the number of active residue fibers.

These are necessary constraints and an exact search reduction.  They do
not produce an `LP(333)` or a Hadamard matrix.

## 1. Fields and the four cone blocks

Put

```text
p = 167,
k = F_(p^2) = F_p(omega),
K = F_(p^6) = F_p(alpha),       alpha^3=omega,
E = F_(p^12).
```

For one channel, let

```text
U_0,U_1,U_2 in k[C_37]^H,
W = U_0 + alpha U_1 + alpha^2 U_2.
```

The recombined prime-167 split records

```text
(c; w_0,w_1,w_2,w_3,w_4,w_5)
    in K x E^6,

c   = W(1),
w_r = W(zeta_37^(p^r)).
```

For two channels, the norm cone groups these coordinates into one trivial
quadratic cone and three paired primitive cones.  These are the four cone
blocks referred to below.

## 2. Exact row-Galois inversion

Write the original CRT coordinates as

```text
(c_s,x_s,y_s)
  = (U_s(1),U_s(zeta_37),U_s(zeta_37^p)),
                                    s=0,1,2.
```

The trivial coordinate has

```text
c = c_0 + alpha c_1 + alpha^2 c_2.
```

Since every `c_s` lies in `k`, applying the `p^2` and `p^4` Frobenius maps
gives the Vandermonde system

```text
[ c       ]   [1 alpha       alpha^2      ] [c_0]
[ c^(p^2) ] = [1 alpha^(p^2) alpha^(2p^2)] [c_1].
[ c^(p^4) ]   [1 alpha^(p^4) alpha^(2p^4)] [c_2]
```

The three conjugates of `alpha` over `k` are distinct, so this matrix has
rank three.

For the primitive coordinates, coefficientwise `p^2` Frobenius shifts the
column character by two.  Aligning the three even and three odd factors
gives

```text
X = (w_0, w_2^(p^10), w_4^(p^8)),
Y = (w_1, w_3^(p^10), w_5^(p^8)).
```

Both triples obey

```text
X = V (x_0,x_1,x_2)^T,
Y = V (y_0,y_1,y_2)^T,

V =
 [1 alpha       alpha^2      ]
 [1 alpha^(p^4) alpha^(2p^4)]
 [1 alpha^(p^2) alpha^(2p^2)].
```

Again `V` has rank three.  Thus the four cone blocks determine all six
original triples `(c_s,x_s,y_s)` exactly.  This is a small row-direction
transform, not a physical inverse CRT.

The verifier checks both matrix ranks and the inverse on all 39 members of
a `k`-basis: thirteen invariant column words placed independently in each
of the three row slots.  Linearity then proves the inversion on the full
space.

## 3. Factorwise recovery of every physical column

The four blocks also recover each of the thirteen physical column
coefficients by weighted field traces.  For a representative
`j in C_37`, put

```text
eta_(r,j) =
  sum_(h in H) zeta_37^(-j p^r h) in E,
                                      r=0,...,5.
```

Then ordinary Fourier inversion, grouped first into the `H`-orbits and
then into the quadratic `E/K` factors, gives

```text
37 W(j) =
    c + sum_(r=0)^5 Tr_(E/K)(w_r eta_(r,j)).          (A)
```

This is a factor-by-factor formula: each primitive cone coordinate appears
only inside its own quadratic trace.  It reconstructs a value in `K` and
does not enumerate phase assignments.  At `j=0`, every Gaussian period is
three, so (A) becomes the unweighted trace formula used below.

The verifier evaluates (A) for all thirteen physical representatives on
all thirteen invariant `K`-basis words:

```text
13 * 13 = 169
```

exact coefficient-recovery checks.  Since (A) is `K`-linear, this proves
the inverse on the full invariant algebra.

## 4. A lookup-free nine-bit physical decoder

Formula (A) supplies one proposed coefficient `v=W_X(j) in K`.  The
candidate profile supplies its actual row weight

```text
m in {3,6}
```

and its actual residue counts

```text
q=(q_0,q_1,q_2),       q_0+q_1+q_2=m.
```

The word may have weight six because the repository's alternating
normalization complements selected weight-three words.  Complementation
negates the primitive ninth-root value, but the decoder below treats both
weights uniformly.

Let `F(t)=sum_(r=0)^8 b_r t^r` be the unknown binary row polynomial.  One
value `v=F(alpha)` determines all six primitive ninth-character values:

```text
F(alpha^(p^a)) = v^(p^a),        a=0,...,5.            (B)
```

These are exactly the six unit exponents modulo nine because `p=5 mod 9`
has order six.  The weight and profile provide the remaining three values:

```text
F(1)       = m,
F(omega)   = q_0+q_1 omega+q_2 omega^2,
F(omega^2) = F(omega)^p.                              (C)
```

Equations (B)--(C) specify the complete nine-point DFT.  Define

```text
beta_r =
  9^(-1) sum_(a=0)^8 F(alpha^a) alpha^(-ar),
                                             r=0,...,8. (D)
```

Then the following criterion is exact:

```text
there is a physical binary word with value v, weight m, and profile q

if and only if

beta_r^2 = beta_r for every r=0,...,8.                 (E)
```

Indeed, a physical word makes (D) ordinary DFT inversion.  Conversely,
over a field the roots of `t^2-t` are exactly zero and one, so (E) makes
the nine `beta_r` binary.  The complete DFT then forces their weight,
profile, and primitive value to be exactly (B)--(C).  The word is unique.

Thus the sparse alphabet intersection needs no 84-entry lookup table.  For
the two channels and twelve nonzero classes it can be written as

```text
2 * 12 * 9 = 216
```

displayed quadratic idempotence equations after substituting the
factorwise trace formula (A).  This is a displayed equation count, not a
claim that all 216 equations are algebraically independent.

The verifier proves the full nine-dimensional DFT inverse on its nine
standard basis vectors.  It then exhausts both normalization branches:

```text
weight 3: 84 physical words, 82 primitive values;
weight 6: 84 physical words, 82 primitive values.
```

For each weight it crosses all 82 primitive values with all ten possible
profiles.  Among the resulting 820 pairs, (E) accepts exactly the 84
physical value/profile/word triples—no false positive and no false
negative.

## 5. The fixed-origin trace equations

Let

```text
Tr = Tr_(E/k).
```

For any `H`-invariant word `U` with CRT coordinates `(c,x,y)`, Fourier
inversion at column zero and the threefold repetition on every `H`-orbit
give

```text
37 U(0) = c + 3 Tr(x) + 3 Tr(y).                     (1)
```

This identity holds on the full invariant algebra.  The verifier checks it
on its thirteen-word `k`-basis.

Normalization fixes the six values universally, independently of the
candidate profile:

```text
(U_A0(0),U_A1(0),U_A2(0),
 U_B0(0),U_B1(0),U_B2(0))

    = (1, -omega, 1+omega, 0, 1, 1).                (2)
```

Each equality (1) lies in `k`, hence contributes two prime-field linear
equations.  The six evaluation maps are on disjoint word components and
are surjective, so (1)--(2) give exactly

```text
6 * [k:F_p] = 12
```

independent `F_167`-linear maps on the ambient coordinate space.

## 6. Profile-resolved Parseval equations

For two invariant Eisenstein words `U,V`, with coordinates
`(c_U,x_U,y_U)` and `(c_V,x_V,y_V)`, the certified involution

```text
(c,x,y)^* = (c^p, y^(p^5), x^(p^7))
```

and Fourier orthogonality give the bilinear identity

```text
37 sum_j U(j) conjugate(V(j))

 = c_U conjugate(c_V)
   + 3 Tr(
       x_U y_V^(p^5)
       + y_U x_V^(p^7)
     ).                                             (3)
```

The verifier checks (3) on all `13^2=169` ordered invariant basis pairs.
Because (3) is sesquilinear, this proves it throughout the invariant
algebra.

Every physical `U_Xs(j)` is zero or an Eisenstein unit.  Setting `V=U` in
(3) therefore yields

```text
37 n_Xs =
    c_Xs c_Xs^p
    + 3 Tr(
        x_Xs y_Xs^(p^5)
        + y_Xs x_Xs^(p^7)
      ),                                           (4)
```

where `n_Xs` is the exact support of that fiber sequence.

Let

```text
a_Xs =
  number of the twelve nonzero H-classes whose profile count
  in fiber (X,s) is one or two,

z = (1,1,1,0,1,1).
```

The vector `z` records which fixed zero-column fibers in (2) are active.
For a fixed candidate profile,

```text
n_Xs = z_Xs + 3 a_Xs.                               (5)
```

Thus the six right sides of (4) are profile-specific.  Only their sum is
universal on the norm-54 shell:

```text
sum_X,s a_Xs = 54,
sum_X,s n_Xs = 5 + 3*54 = 167 = 0 in F_167.         (6)
```

The diagonal origin equation of the full norm cone already supplies (6).
The six individual Hermitian support forms are independent in the ambient
polynomial space—on the six coordinate axes their evaluation matrix is the
identity.  Modulo the one-dimensional span of their known sum, five
support-difference forms remain.  Operationally these are five displayed
profile-resolved equations.  No codimension-five assertion is made after
also restricting to the cone and fixed-zero locus.

This distinction is important:

```text
universally fixed:
    the 12 zero-column scalar equations,
    the total support 167;

fixed only after choosing a profile:
    the six values n_Xs,
    equivalently five additional values after their total is used.
```

## 7. A nonzero cone counterexample

The individual support equations are not consequences of the full modular
norm cone.  Choose `R in K` with

```text
R R^(p^3) = -1
```

and take

```text
W_A = delta_0,
W_B = R delta_0.
```

Then

```text
W_A W_A^* + W_B W_B^* = 0
```

coefficientwise, so this is a nonzero point of all four norm-cone blocks.
After row-Galois inversion, its six support forms are

```text
(1,0,0,56,89,21),
```

whose sum is zero modulo 167.  The pinned physical profile fixture has

```text
(37,37,37,18,19,19).
```

All six individual target equations fail even though both totals are zero.
This explicitly proves that the profile-resolved vector is not implied by
the cone total; it does not by itself claim a codimension on the constrained
locus.

## 8. The seven-value local norm alphabet

At a nonzero physical column, a normalized channel word is a three-subset
`S` of the nine rows.  Put

```text
W(S)  = sum_(r in S) alpha^r,
nu(S) = W(S) W(S)^(p^3) in F_(p^3).
```

On a high-weight class the actual word is the six-element complement
`S^c`.  Since the sum of all ninth roots is zero,

```text
W(S^c)=-W(S),       nu(S^c)=nu(S).
```

Its actual profile is `(3-q_0,3-q_1,3-q_2)` and has the same number of
active fibers.  Hence the norm and trace classification below applies
unchanged to both physical weights.  The verifier explicitly checks all 84
weight-six complements as well as the 84 normalized weight-three words.

If the residue profile is `(q_0,q_1,q_2)`, then

```text
Tr_(F_(p^3)/F_p)(nu(S))
    = 9 - 3 sum_s binom(q_s,2)
    = 3 * #{s : q_s is 1 or 2}.                     (7)
```

The first equality follows by expanding the norm and pairing the two
orientations of every row difference.  A paired primitive ninth-root
difference has trace zero, while a paired nonzero difference divisible by
three has trace `-3`.  The three profile types are therefore:

```text
profile type       active fibers       trace(nu)
(3,0,0)                  0                  0
(2,1,0)                  2                  6
(1,1,1)                  3                  9
```

The 84 row words give 82 distinct `W(S)` values and only seven distinct
norms.  Besides zero, the two active branches are single cubic Frobenius
orbits with minimal polynomials

```text
active fibers 2:
    t^3 - 6t^2 + 9t - 3;

active fibers 3:
    t^3 - 9t^2 + 18t - 9.                            (8)
```

Consequently a reconstructed physical coefficient must lie on the branch
dictated by its profile, not merely anywhere in `K`.  The verifier exhausts
all `binom(9,3)=84` row words, checks (7), derives (8) from the elementary
symmetric functions/Newton data, and pins every multiplicity:

```text
inactive:
    one norm value, multiplicity 3;

two active fibers:
    three norm values, multiplicity 18 each;

three active fibers:
    three norm values, multiplicity 9 each.
```

## 9. Mechanical certificate

The verifier proves:

```text
row-Galois matrix ranks                    3, 3
full invariant basis words                  13
factorwise coefficient trace checks         169
origin trace basis checks                    13
bilinear Parseval basis-pair checks         169
row-Galois inversion basis checks            39
full ninth-root DFT basis checks               9
value/profile decoder pairs checked        1,640
idempotent physical pairs accepted           168
exhaustive normalized row words              84
exhaustive weight-six complements             84
fixed-zero prime-field equations              12
support equations remaining after total        5
```

Pinned hashes:

```text
local 84-word alphabet
111b47b011ff267769cb6af618baf048284fc6db8a5bc69e02c40be156a04277

full invariant-algebra proof
2978c247c1ac8ae68d876420d2521bfbaa1c7708a956d322e09af2b14204db26

lookup-free ninth-bit decoder
7bf5e08aca41bb4822472c4f8ed08fd7271429d823dff132589c7521c569169a

physical support-167 fixture
dbf9f30d023049d99d3fc3f038b7fc99124d535a83022fd3d825da9c581d6437

nonzero cone counterexample
98add67fffdbe386b2caabc1e679352e9d76f9f51a56e663ad8eb59cd830e6fe

composite
8253d73531cfbf4d5111c211b75da5abfdd8abeb11efc47973e49daedcc9b1e1
```

## Reproduction

```text
python3 verify_lp333_order3_phase_trace_sieve.py
python3 -m unittest -v test_lp333_order3_phase_trace_sieve.py
```

The verifier uses exact finite-field arithmetic and the Python standard
library only.
