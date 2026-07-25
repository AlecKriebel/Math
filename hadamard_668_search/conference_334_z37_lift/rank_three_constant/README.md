# Constant symmetric rank-three conjugators are impossible

## Result

Work over

\[
R=\mathbf F_{37}[y]/(y^{37}),\qquad z=\log(1+y),
\]

in the trace-corrected semiregular \(C_{37}\) family

\[
N_A=e^{-zA}
\left(N_0+\eta z^{18}J+19y^{36}J\right)e^{zA},
\qquad \eta\in\{1,-1\}.
\]

The exact census proves:

> No constant symmetric \(9\times9\) matrix \(A\) of rank three can make
> this formal family the group-ring form of a binary semiregular
> \(C_{37}\) conference core for any of the 625 integral orbit quotients.

This extends the promoted constant rank-two obstruction.  It does not
exclude rank at least four, a nonconstant \(y\)-adic conjugator, or a
general semiregular lift.

## Complete rational-type list

Write the rank contribution of the zero-primary nilpotent part as
\(r_0\), and the dimension of the invertible primary part as \(d\).
Then

\[
r_0+d=3.
\]

The census deliberately includes every rational similarity type of an
arbitrary rank-three matrix, whether or not that type is realizable by a
symmetric matrix.  This makes the list an over-list and preserves the
direction of the obstruction.

Up to nonzero scalar multiplication, the list contains:

| primary shape | projective types |
|---|---:|
| invertible dimension three, cyclic | 1,371 |
| invertible dimension three, noncyclic | 37 |
| \(J_2(0)\) plus invertible dimension two | 39 |
| zero-primary rank two plus one nonzero line | 2 |
| pure nilpotent rank three | 3 |
| **total** | **1,452** |

The 1,371 cyclic types are the scalar orbits of monic cubics with
nonzero constant term.  The noncyclic additions are the repeated
semisimple, scalar, and \(J_2(\lambda)\oplus[\lambda]\) cases.  The
remaining zero-primary partitions are

```text
r0=1: J2
r0=2: J3 or J2+J2
r0=3: J4, J3+J2, or J2+J2+J2.
```

Scaling \(A\) is cyclic decimation \(z\mapsto qz\).  It may reverse the
quadratic-character trace orientation because \(q^{18}=\pm1\), so the
final test explicitly includes both \(\eta=+1\) and \(\eta=-1\).

## Symmetry-reduced diagonal overcode

Let the minimal polynomial of \(A\) have degree \(m\le4\), and expand

\[
e^{\pm zA}=\sum_{r=0}^{m-1} f_r^\pm(z)A^r.
\]

For symmetric \(A\) and symmetric \(M\),

\[
\operatorname{diag}(A^rMA^s)
=\operatorname{diag}(A^sMA^r).
\]

Thus every diagonal entry of \(e^{-zA}Me^{zA}\) lies in the span \(F_A\)
of

\[
\phi_{rr}=f_r^-f_r^+,
\qquad
\phi_{rs}=f_r^-f_s^+ + f_s^-f_r^+
\quad(r<s).
\]

Allowing the associated matrix coefficients to vary independently gives
the safe temporal overcode

\[
W_A=F_A+z^{18}F_A.
\]

The verifier computes \(W_A\) exactly in the cyclic coefficient basis
\(1,x,\ldots,x^{36}\), then intersects it with

\[
\{0\}\times\{18,19\}^{36}.
\]

Across all 1,452 types:

```text
code dimensions
4:2 6:4 8:38 10:41 12:97 14:1270

binary-word counts
2:492 4:673 8:8 16:82 32:19 64:56 128:114 256:8
```

The intersection is small: no type has more than 256 formal binary
diagonal words.  Comparing their weights with the frozen 625-class
quotient census removes 492 types and leaves 960.

## Restoring the fixed \(J\) term

The remaining overcode had allowed the coefficients of the
\(z^{18}F_A\) term to vary independently.  For the actual fixed matrix
\(J=\mathbf1\mathbf1^T\), put at coordinate \(i\)

\[
v_r=(A^r\mathbf1)_i,\qquad v_0=1.
\]

The coefficient of \(z^{18}\phi_{rs}\) is forced to

\[
v_rv_s.
\]

The verifier reduces every candidate binary word modulo the ordinary
space \(F_A\).  It then exhausts

\[
(v_1,\ldots,v_{m-1})\in\mathbf F_{37}^{m-1}
\]

and both signs of \(\eta\).  Since \(m\le4\), this is at most
\(37^3=50,653\) local tuples per rational type.

This is still a relaxation: the local powers are allowed to vary freely,
and all relations between coordinates, \(N_0\), and the quotient are
discarded.  Therefore a zero local intersection is a valid obstruction.

All 960 residual rational types have zero surviving binary words.  The
complete conclusion is

```text
constant_symmetric_rank3=IMPOSSIBLE
certificate=PASS
```

## Independent checks

The implementation also supports the looser all-entry-product code.
Representative sanity tests established:

- direct reconstruction of \(e^{\pm zA}\) from the computed minimal
  polynomial for cyclic, repeated, mixed, and nilpotent types;
- containment of the symmetry-reduced code in the universal
  entry-product code;
- equality between the meet-in-the-middle intersection and independent
  brute information-set enumeration for every observed word-count shape
  \(2,4,8,16,32,64,128,256\);
- a direct 37-coordinate fixed-\(J\) replay for the generic cubic
  \(X^3+1\), independently reproducing zero intersection against its 128
  binary candidates.

## Reproduction

After placing this folder at
`conference_334_z37_lift/rank_three_constant`, first regenerate the
promoted canonical quotient dump:

```text
clang++ -O3 -std=c++17 \
  ../census_z37_quotients.cpp \
  -o /tmp/census_z37_quotients

/tmp/census_z37_quotients --dump-canonical \
  > /tmp/z37_quotients_canonical.txt
```

Then run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 audit_rank_three_constant.py \
  --quotients /tmp/z37_quotients_canonical.txt \
  --code symmetric --fixed-j
```

On the M1 Pro project machine, the final assertion-bearing fixed-\(J\)
run took 323.06 seconds and used 61.1 MB peak RSS.  The preliminary 1,452-type
word census without fixed \(J\) took 9.91 seconds and used 29.0 MB.

## Why the three-plane nonconstant pair is deferred

The analogous common-support family

\[
K=zA_0+z^2A_1
\]

on a nondegenerate three-plane does not have the two-plane closure used
in the adjacent first-nonconstant certificate.  Here a self-adjoint
\(A_0\) has six parameters and a skew-adjoint \(A_1\) has three; a
generic pair generates the full nine-dimensional matrix algebra.
Orthogonal conjugacy removes only three dimensions, and decimation is a
finite action.  Consequently the raw pair space has on the order of
\(37^6\) orbit-scale possibilities before support constraints, rather
than the 1,408 scalar types of the two-plane pencil.

There is presently no comparably small invariant temporal code that is
complete for those pairs.  Enumerating them would be a generic
multi-billion-type search and was not attempted.  A future attack should
first stratify pairs by the dimension and radical of the algebra they
generate; low-algebra-dimension strata may again admit finite function
codes.
