# Independent decimations in the prime-83 Sidelnikov fold

## Status

This lane is now exactly exhausted, with no prime-fold object and therefore
no modulo-84 lift.

Starting from the `43` binary and `44` one-zero degree-at-most-two
Sidelnikov/product signatures in `PRIME83_SIDELNIKOV_FOLD.md`, this extension
allows an independent unit multiplier on every block.  A common multiplier
is quotiented exactly.  The resulting construction has:

```text
binary relative-decimation signatures             1,723
one-zero relative-decimation signatures           1,723
C/D unordered signature pairs                   1,485,226
normalized U/V phase-sign states               12,584,792
prime-fold objects                                       0.
```

The complete PAF join uses full `41`-coordinate integer signatures, not
probabilistic hashes.  More importantly, a new modulo-four prefilter explains
the zero result: every row-admissible `U,V` pair fails before the PAF join.

Reproduce the small independent certificate with:

```sh
python3 check_bs84_sidelnikov_fold.py
```

Reproduce the full signature catalog and exact join with:

```sh
c++ -O3 -std=c++20 -o search_bs84_sidelnikov_decimations \
    search_bs84_sidelnikov_decimations.cpp
./search_bs84_sidelnikov_decimations
```

A reference run used about `134 MB` peak RSS.  Both programs are
dependency-free.

## 1. Construction being exhausted

Write `n=83`.  The base libraries are:

```text
binary:
    B,
    B_i B_(i-t),                  t in Z_83;

one-zero:
    Z,
    Z^2,
    Z_i B_(i-t),                  t in Z_83.
```

After quotienting equal squared-row-sum/PAF signatures, these contain `43`
binary and `44` one-zero representatives.

For a unit `d in Z_83^*`, decimation acts by

```text
(D_d q)_i = q_(d i),
PAF_(D_d q)(k) = PAF_q(d k).                         (1)
```

Because PAF is unoriented, `d` and `-d` induce the same half-PAF
permutation.  It is therefore enough to use `d=1,...,41`.

The independently decimated endpoint family is:

```text
U = D_e(one-zero template), with its zero at 0;
v = a signed cyclic phase of D_f(binary template);
V[0]=2, V[i]=v[i] for i != 0;
C,D = independently decimated binary templates.       (2)
```

Signs and phases of the ordinary `C,D` blocks do not affect their PAFs or
squared row sums.

## 2. Exact common-decimation quotient

Applying the same `D_g` to all four folded blocks permutes the `82`
nonzero-lag equations and fixes the anomalous coordinate zero.  Given the
multiplier `e` of `U`, choose `g=e^(-1)`.  Thus `U` may be normalized to its
undecimated representative, while `V,C,D` retain arbitrary relative
multipliers.

Reversal accounts for the choice between `d` and `-d`.  The paired raw
templates with equal PAF are likewise related by reversal, phase, and an
irrelevant global sign.  Consequently the quotient loses no possible
prime-fold solution.

Decimating and canonicalizing the signatures gives:

```text
                               raw       distinct
binary                         43*41       1,723
one-zero                       44*41       1,723.
```

For `V`, the catalog retains an actual sequence representative as well as
its PAF, because raising coordinate zero depends on the entries at each
inverse pair.  The only duplicate binary decimations are the `40` redundant
decimations of the constant template, so this sequence quotient is exact.

## 3. A universal modulo-four orientation condition

Let `U` have its unique zero at coordinate zero.  Fill that zero with an
arbitrary sign `epsilon`, producing a binary sequence `F`.  Let `v` be the
binary sequence underlying `V`, and put `delta=2-v_0`, which is odd.  At a
nonzero lag `k`,

```text
PAF_U(k) = PAF_F(k) - epsilon (U_k+U_-k),
PAF_V(k) = PAF_v(k) + delta   (v_k+v_-k).              (3)
```

Every binary sequence of odd length `83` has

```text
PAF_q(k) = 3 mod 4,             k != 0,                (4)
```

because the Hamming distance from a cyclic shift is even.  In particular,
the two ordinary binary blocks contribute `2 mod 4`.  Reducing the
four-block complementarity equation modulo four therefore forces

```text
epsilon (U_k+U_-k)
    = delta (v_k+v_-k) mod 4.                           (5)
```

Both coefficients are odd and both parenthesized sums belong to
`{-2,0,2}`.  Equation (5) is equivalent to

```text
U_k U_-k = v_k v_-k,            k=1,...,41.            (6)
```

Define the inverse-pair orientation fingerprint

```text
Omega(q)_k = [q_k=q_-k] in {0,1}.                       (7)
```

Any endpoint-fold solution in this construction must satisfy

```text
Omega(U)=Omega(v).                                      (8)
```

This condition is independent of `C,D`, of all PAF magnitudes, and of the
sign chosen for `v`.

## 4. Exact fingerprint disjointness

The `44` normalized one-zero templates give `43` distinct `41`-bit
fingerprints.  The `1,723` relative-decimation binary states and their `83`
phases give `35,302` distinct fingerprints.

Their set intersection contains exactly one fingerprint: the all-symmetric
word

```text
(1,1,...,1).
```

On the `U` side it occurs only for `Z^2`, whose row sum is `82`.  On the
`V` side it occurs for `1,805` multiplier-template-phase states, or `3,610`
states after the two signs are restored.  But

```text
(sum U)^2 = 82^2 = 6,724 > 334.                         (9)
```

So every one of those `3,610` orientation survivors violates the required
row-square identity before the other three blocks are considered.

> **Independent-decimation exclusion.**
>
> No member of the independently decimated degree-at-most-two Sidelnikov
> product family satisfies the prime-83 endpoint fold.

This is stronger than the numerical PAF join: row norm plus the `41`-bit
modulo-four fingerprint already excludes all `12,584,792` normalized
`U/V` states.

## 5. Full exact PAF join

The C++ enumerator also performs the unreduced integer-signature join as an
independent check.

For each of the `1,723` binary states, retain its squared row sum and full
half-PAF.  Form every unordered `C,D` pair.  The exact counts are:

```text
all C/D pair states                              1,485,226
pair states with row norm at most 334            1,475,877
distinct exact (row norm,41-entry PAF) keys       1,475,877.
```

For `U,V`, the common-decimation quotient gives

```text
44 * 1,723 * 83 * 2 = 12,584,792                 (10)
```

template/multiplier/phase/sign states.  Exactly `863,337` have a remaining
row norm attained by some `C,D` pair.  Their distribution is:

```text
remaining C/D norm    U/V states
74                       64,575
90                      135,669
122                      72,324
170                     239,112
218                     351,657.
```

None of these states passes (8), none reaches an exact PAF key, and hence the
number of prime-fold objects is zero.

The enumerator stores the full integer vectors and compares them
lexicographically.  The count does not depend on a finite-width hash or a
collision assumption.

## 6. Modulo-84 lift status

No prime-fold object appeared, so there was nothing to submit to the
independent modulo-84 adjacent-fold portfolio.  Thus:

```text
prime-fold objects       0
modulo-84 lifts tested   0
BS(84,83) objects        0
Hadamard matrices        0.
```

This is a conditional absence, not an exclusion of `BS(84,83)` or
`H(668)`: only the displayed character-product construction has been
exhausted.

## 7. What this changes

Independent multiplier freedom was the most immediate untested enlargement
of the Sidelnikov construction.  It is now closed by a short structural
obstruction rather than merely by a large negative computation.

The next character lane must alter the inverse-pair orientation fingerprints.
Merely applying more multipliers, phases, signs, or PAF-preserving
equivalences to these degree-two templates cannot help.  Plausible next
extensions are:

1. mixed products using genuinely different character families on
   `Z_83`, retained only when their row squares fit the five admissible norm
   layers;
2. degree-three Sidelnikov products, filtered first by (8);
3. an algebraic construction that targets the oriented inverse-pair states
   directly rather than their PAFs.

The result was derived independently from local repository context.  No
external novelty claim is made, and no outside contact is to be prepared or
attempted.
