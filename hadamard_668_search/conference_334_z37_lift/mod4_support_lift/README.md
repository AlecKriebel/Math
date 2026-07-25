# The next 2-adic digit of the semiregular `C37` conference lift

## Status

No conference matrix or `H(668)` is constructed here.

Two exact characteristic-two support witnesses now realize the full block
margins and `6/3` diagonal trace law for the two surviving quotient parity
types.  They satisfy all 2,997 coefficients of

```text
D^2 + D = I*delta + J*U                 (mod 2).
```

Equivalently, their sign cores satisfy the conference equation modulo
eight.  The witnesses and their independent verifier are in
`../char2_support_realization/`.

Neither initial witness passes the next digit:

```text
type 1: 722 of 1,503 independent carry coefficients are nonzero;
type 2: 764 of 1,503 independent carry coefficients are nonzero.
```

A deterministic phase walk preserving the complete lower layer improves
type 1 to `672/1503` defects (72 diagonal and 600 off-diagonal), but that
optimized support also fails.  These outcomes reject only the three frozen
representatives.  They do not reject either quotient, either parity type,
or the general semiregular lane.

## Why adjacency modulo four is conference modulo 16

For a conference graph core of order 333, write

```text
S = J - I - 2D.
```

Using `D*1=166*1`, direct expansion gives the exact identity

```text
S^2 - (333I-J) = 4*(D^2+D-83*(I+J)).
```

Thus the adjacency equation modulo two is the sign-core equation modulo
eight, and the adjacency equation modulo four is the sign-core equation
modulo 16.  A zero carry in this folder would therefore be a genuine
consecutive higher-digit lift, though still not an integral conference
matrix.

## Exact 720-bit unitary chart

Let

```text
K = F_2[x]/Phi_37 = F_(2^36).
```

Group inversion is the unitary involution over the fixed field
`F_(2^18)`.  If `omega` is a primitive element of `F_4`, every
trace-oriented nontrivial Fourier solution has

```text
E = D + omega^2 I,
E^2 = E,
E* = E,
rank(E) = 4.
```

On the graph chart, choose `X` in `K^(5 x 4)` with
`G=I+X*X` nonsingular and put

```text
V = [I_4; X],
E = V G^-1 V*.
```

The chart has exactly `20*36=720` binary coordinates.  Combining its field
component with either trivial-factor parity quotient reconstructs a unique
37-bit word in every block.

There is a useful automatic physicality fact.  A diagonal field entry is
fixed by inversion.  Fourier inversion at displacement zero gives

```text
coefficient_0 = augmentation + Tr_(K/F2)(field entry).
```

The absolute trace of an element of the fixed subfield is twice its
relative trace and therefore vanishes in characteristic two.  Since both
parity quotients have zero diagonal, every reconstructed diagonal block
automatically has coefficient zero at displacement zero.  The C++ audit
checks this for every evaluated chart.

## Carry audit

For the coefficientwise binary representative, define

```text
R = (D^2+D-83*(I*delta+J*U))/2          (mod 2).
```

`R=0` is exactly the adjacency-modulo-four condition.  The audit evaluates
all 2,997 redundant ordered coefficients and the 1,503 independent
star-symmetric coefficients.

At eight deterministic random graph-chart points for each parity type, the
targeted syndrome consisting of carry plus margin/trace conditions has:

```text
rank of the 720 single-coordinate differences = 720;
rank after adjoining the base syndrome         = 721.
```

This is an exact finite-difference calculation at the sampled points, not a
global rank theorem.  It says the targeted next layer is locally maximally
sensitive and that the linearized single-coordinate model cannot repair
those sampled points.

A separate deterministic 3,000-point audit gives sampled targeted
affine-difference rank 1,493 for both parity types.  In each case zero lies
in the sampled affine hull.  Therefore no linear functional found at this
level excludes the targeted system globally.  Earlier exploratory output
also recorded a raw-carry rank, but the frozen verifier exposes only this
targeted statistic and no raw-rank claim is retained.

## Exact fixed-quotient model

`search_mod4_conference_lift.py` is a complete CP-SAT formulation for one
specified integral quotient.  It uses:

```text
1,494 physical block-membership bits;
418,293 reused Boolean products;
1,503 independent cyclic equations modulo four;
45 exact block margins;
36 nonzero-lag diagonal incidences;
redundant modulo-two XOR equations.
```

Relabeling the nine cyclic fibers permits eight independent shifts.  For
each root block `(0,j)`, the model selects the lexicographically least of
its 37 rotations.  Every root block has weight strictly between zero and
37, so its rotation orbit has size 37.  This removes the entire `37^8`
gauge, not merely a subgroup.

The model builds in about ten seconds and approximately 0.7 GB.  A
90-second, four-worker run for quotient type 1, seeded by the exact
characteristic-two witness, ended `UNKNOWN` with approximately 2.7 GB
maximum resident memory.  A 60-second lower-layer run also ended `UNKNOWN`
despite the independently known witness.  These bounded outcomes diagnose
the generic model as too weak; they are neither positive nor negative
mathematical evidence.

That proposed carry optimization has now been attempted: 200,000 exact
phase moves reduced `722` defects only to `672`.  Exact audits also found
no equation-preserving ordinary four-cycle switch and no margin-preserving
member of the smallest semiregular transvection family for either frozen
support.  A larger coupled construction would need a new global
margin-restoration principle; unstructured expansion of this search is not
justified by the present data.

## Reproduction

From this directory:

```text
clang++ -O3 -std=c++20 audit_mod4_carry_chart.cpp \
  -o /tmp/h668_mod4_carry_audit
/tmp/h668_mod4_carry_audit 8
/tmp/h668_mod4_carry_audit --affine 3000

python3 audit_char2_witness_mod4.py \
  ../char2_support_realization/TYPE1_SUPPORT_WITNESS_CARRY672.json \
  ../char2_support_realization/TYPE2_SUPPORT_WITNESS.json
```

The exact CP-SAT model uses the repository solver environment:

```text
/Users/alec/Documents/tmp/hadamard-env/bin/python \
  search_mod4_conference_lift.py \
  --quotient-type 1 --modulus 4 \
  --hint-json \
  ../char2_support_realization/TYPE1_SUPPORT_WITNESS_CARRY672.json \
  --time-limit 90 --workers 4 --max-memory-mb 4096
```
