# Degree-three and degree-four prime-167 Sidelnikov product audit

Status: exact finite exclusion of the independently decimated
degree-at-most-three family and of the un-decimated degree-at-most-four
family.  No prime-fold object, `BS(84,83)`, or `H(668)` was found.

## Construction

Let

\[
B_i=\chi(2^i+1),\qquad Z_i=\chi(2^i-1),\qquad i\in\mathbb Z/83,
\]

where \(\chi\) is the quadratic character of \(\mathbb F_{167}\).  The
previous promoted audit exhausted products of at most two phases of these
words, including independent decimations, but explicitly left degree three
open.

This audit takes every binary product of at most three cyclic phases of
\(B\).  Because \(B^2=1\), it is indexed by a subset \(E\subseteq
\mathbb Z/83\) of size at most three:

\[
B_E(i)=\prod_{t\in E}B_{i-t}.
\]

Common translation does not change the PAF or squared row sum.  The exact
translation-orbit counts are

```text
factor count       0     1     2      3
orbits             1     1    41   1107
total                                1150.
```

For the one-zero endpoint block, all \(Z\) factors must share one phase;
otherwise the product has more than one zero.  Anchor that zero at the
origin.  Every product of total degree at most three is then uniquely in
one of the two forms

\[
ZB_E,\quad |E|\le2,\qquad\text{or}\qquad
Z^2B_E,\quad |E|\le1.
\]

They give respectively 3,487 and 84 distinct anchored words, hence 3,571
one-zero templates.

## Exact inverse-pair reduction

For an endpoint-fold solution, reduction modulo four gives the universal
condition

\[
U_kU_{-k}=v_kv_{-k},\qquad 1\le k\le41,
\]

where \(v\) is the binary word underlying the anomalous block \(V\).
Encoding these products as a 41-bit signature gives:

```text
U signatures                                  904
V template/phase signatures                11,522
common signatures                               42
U templates on a common signature               84
V phase states on a common signature          3,610.
```

All 84 surviving \(U\) templates are exactly the even-\(Z\) family
\(Z^2B_E\), \(|E|\le1\).  No one-zero word containing an odd power of \(Z\)
passes this necessary condition.  Thus the inverse-pair law reduces

```text
3,571 * 1,150 * 83 * 2 = 681,703,900
```

`U`-sign-quotiented labeled `U/V` states to 14,440 before any full PAF
comparison.  The row-norm
equation leaves 6,170 states, in five exact layers:

```text
remaining C/D norm       U/V states
10                              364
74                              657
234                           1,372
298                           1,724
314                           2,053.
```

## Complete PAF join

Signs and cyclic phases of the ordinary blocks \(C,D\) do not affect their
PAFs or squared row sums.  The 1,150 binary templates therefore give
661,825 unordered `C/D` pairs.  Of these, 572,893 have norm at most 334,
collapsing to 163,876 distinct full `(norm, 41-coordinate PAF)` keys.

Every one of the 6,170 row-compatible `U/V` states passes the expected
modulo-four residue test.  None has a required `C/D` key.  Consequently:

```text
exact prime-fold objects       0
modulo-84 lifts tested         0
Hadamard candidates            0.
```

This exhausts the displayed un-decimated degree-at-most-three product
family.

## Independent decimations through degree three

The C++ verifier allows an independent nonzero index multiplier modulo 83
on every block.  A common multiplier normalizes the multiplier of \(U\);
\(V,C,D\) retain every relative multiplier.  Cyclic phases and signs are
also complete:

- the phase of \(V\) is retained because raising coordinate zero depends on
  it;
- phases of \(C,D\) and all ordinary-block signs do not change PAF or
  squared row sum;
- the two signs of the binary word underlying \(V\) are tested explicitly.

The exact quotient contains:

```text
binary affine sign-orbit representatives      3,910,048
ordinary (absolute row sum, PAF) states          25,257
intersecting inverse-pair fingerprints                42
exact orientation/sum U/V states                  20,504
row-compatible exact U/V states                    5,434
exact C/D signature hits                               0.
```

The 5,434 row-compatible states lie in the five residual-norm layers

```text
10: 182,   74: 1,017,   234: 686,   298: 862,   314: 2,687.
```

The affine representatives are canonicalized under global sign only after
all relative decimations and phases have been formed.  This order matters
for reproducible state counts: choosing a global sign independently for
each base template before taking its affine closure gives a
representation-dependent larger count, although restoring the block sign
still covers the same family.

Thus the complete independently decimated degree-at-most-three family is
also excluded.

## Un-decimated products through degree four

One degree higher, the binary translation quotient has

```text
factor count       0     1     2      3       4
orbits             1     1    41   1107   22140
total                                      23290.
```

The anchored one-zero library becomes

\[
ZB_E,\quad |E|\le3,\qquad\text{or}\qquad
Z^2B_E,\quad |E|\le2,
\]

for 98,855 distinct words.  The complete un-decimated calculation has:

```text
binary phase states                          1,932,988
ordinary (absolute row sum, PAF) states         12,097
intersecting inverse-pair fingerprints              862
exact orientation/sum U/V states                642,560
row-compatible exact U/V states                 325,835
distinct required full PAF signatures           179,221
exact C/D signature hits                               0.
```

The required signatures split as follows:

```text
residual norm          10     74     90    122    170
required signatures  2257  16183  10823   9569  16260

residual norm         218    234    298    314
required signatures 21171  38023  20638  44297
```

For each required vector \(T\), the verifier tests the lossless
decomposition

\[
\operatorname{PAF}(C)+\operatorname{PAF}(D)=T
\]

by iterating one complete row-sum/PAF catalog and looking up the exact
coordinatewise complement in the other.  Full 41-entry integer arrays are
compared after the hash lookup, so finite-width hash collisions cannot
create either a false hit or a false exclusion.

This closes the un-decimated degree-at-most-four family.  It does **not**
close independently decimated degree-four products, degree five or higher,
arbitrary character products, `BS(84,83)`, or `H(668)`.

## Reproduction

From `hadamard_668_search`:

```sh
python3 prime83_sidelnikov_higher_products/verify_degree3_sidelnikov_fold.py

clang++ -O3 -std=c++20 \
  prime83_sidelnikov_higher_products/audit_independent_decimations.cpp \
  -o /tmp/audit_degree34
/tmp/audit_degree34
/tmp/audit_degree34 --degree4-undecimated
python3 prime83_sidelnikov_higher_products/verify_expected_outputs.py \
  --binary /tmp/audit_degree34
```

The verifier uses exact integer PAF vectors and compares complete Python
tuples, so hash collisions play no role.  A reference run used about
232 MB peak RSS and took under four seconds on the local M1 Pro.  The C++
degree-three run used about 133 MB RSS and three seconds; the degree-four
run used about 111 MB RSS and ten seconds.  AddressSanitizer and
UndefinedBehaviorSanitizer both pass in both modes.

`EXPECTED_INDEPENDENT_DEGREE3.txt` and
`EXPECTED_UNDECIMATED_DEGREE4.txt` freeze the complete C++ standard output
byte for byte.  `verify_expected_outputs.py` also checks the Python semantic
certificate

```text
272a898b43ace01056aa24a83f490c8ba2d6f25d0ed953d758d5e9a86bf9b0f5
```

before comparing both C++ replays with those frozen outputs.

These are internally derived finite exclusions.  No external novelty audit
has been performed, and no priority claim is made.

`ARTIFACT_SHA256.txt` freezes all seven source, certificate, and documentation
files in this directory.  `RESEARCH_LOG.md` records the exact theorem boundary
and the remaining construction scope.
