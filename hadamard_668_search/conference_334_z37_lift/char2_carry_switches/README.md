# Exact small-switch gate for the two `C37` support witnesses

## Status

This bounded audit finds no support-preserving carry contraction for either
frozen characteristic-two witness.  It constructs neither a conference
matrix nor `H(668)`.

It gives two exact negative results:

1. neither 333-vertex witness admits an equation-preserving combinatorial
   four-cycle switch;
2. neither witness admits a physically valid member of the smallest
   semiregular Hermitian-transvection family.

The second statement exhausts a named finite family, not all unitary
transvections.

## Carry transformation and invariant

Put

```text
F(D) = D^2 + D - 83*(I*delta + J*U)
R(D) = F(D)/2 mod 2.
```

If `D'` is another binary support and `Delta=D'-D` is its signed integer
difference, direct expansion gives

```text
R(D') + R(D)
 = (D*Delta + Delta*D + Delta^2 + Delta)/2 mod 2.       (1)
```

The numerator is even whenever `D` and `D'` satisfy the same
characteristic-two equation.  The verifier replays (1) on all 2,997
ordered cyclic coefficients between the two frozen witnesses.

Exact block margins give

```text
augmentation(F(D)) = Q^2 + Q - 83*(37*J+I) = 0.
```

Consequently every one of the 45 independent carry blocks has even
parity.  On a star-symmetric diagonal block, this forces its lag-zero
carry coefficient to vanish.  The two witnesses independently exhibit
these 45 parity constraints and nine forced diagonal zeros.  Their trace
carry also vanishes, but this audit does not promote that observation to
a universal theorem.

The combined invariant/carry audit has semantic SHA-256

```text
98a6a58e83ec0750c09dd03fbcd878a0c8babc649078b8c2b3e5416abcc28dcf
```

## No combinatorial four-cycle switch

Let `A` be either expanded 333 by 333 binary witness.  It obeys

```text
A^2 + A = I + J  over F_2.
```

A four-cycle switch has toggle matrix

```text
B = u*v^T + v*u^T,
```

where `u` and `v` are disjoint weight-two vectors.  Then `B^2=0`.

### Lemma

`A+B` satisfies the same equation if and only if
`W=span(u,v)` is `A`-invariant.

Indeed, the difference equation is

```text
A*B + B*A + B = 0.                                      (2)
```

If (2) holds, applying it to `ker(B)=W^perp` shows that `A` preserves
`W^perp`; symmetry then makes `W` invariant.  Conversely, on an invariant
`W`, the original equation restricts to

```text
(A|W)^2 + A|W + I = 0,
```

because `J` kills even-weight vectors.  The irreducible polynomial
`z^2+z+1` forces trace one on this two-plane, which is exactly (2).

In particular, for a pair-vector `u`, the vector `A*u` would have weight
two or four.  Exhausting all

```text
C(333,2) = 55,278
```

pair-vectors gives:

| witness | minimum `weight(A*u)` | pairs attaining it | invariant planes | valid switches |
|---|---:|---:|---:|---:|
| type 1 | 136 | 37 | 0 | 0 |
| type 2 | 138 | 74 | 0 | 0 |

Thus the four-cycle avenue fails by a gap of at least 132, before block
margins or the `6/3` trace law are imposed.

## No smallest semiregular orbit transvection

Work in

```text
K = F_2[x]/Phi_37
```

with involution `x -> x^-1`.  For every pair of fibers `a<b` and shift
`s`, put

```text
u = e_a + x^s*e_b.
```

Then `u^*u=0`.  For every fixed scalar `c=bar(c)`,

```text
U = I + c*u*u^*
```

is a Hermitian unitary involution.  Therefore

```text
E' = U*E*U
```

is automatically another exact rank-four Hermitian projection, and its
CRT reconstruction is an exact semiregular characteristic-two solution.

The audit exhausts all

```text
36*37 = 1,332
```

binomial isotropic directions and the 37 smallest fixed scalars

```text
1,
x^t+x^-t,
1+x^t+x^-t,       1 <= t <= 18.
```

That is 49,284 exact transvections per witness:

| witness | exact margins | exact `6/3` trace | loopless | fully physical |
|---|---:|---:|---:|---:|
| type 1 | 0 | 1,492 | 49,284 | 0 |
| type 2 | 0 | 1,604 | 49,284 | 0 |

For both witnesses the closest member is `c=1`, `s=0`.  It preserves the
trace law and looplessness but misses four block margins with total
absolute deviation eight.  In fact this case is simply a fiber
transposition; it cannot contract the carry because it only relabels the
graph.

The exact per-witness output hashes are:

```text
type 1
2a0ea7bab44375beb356b78f3dd4f3754ec116846e5d4cd80d04aca0e9faa73e

type 2
9cb4fbbc10955802b7d0815a16a6bfbd54243fee32d1aab6e81e0eae158378ae
```

These semantic payloads record only the stable witness basename, not the
caller-supplied path, so the hashes are unchanged by promotion or by the
working directory used for replay.

The optimized 672-defect type-1 seed was also checked as a secondary
replay: zero of its 49,284 family members has exact margins.  This is
consistent evidence only; the named result above concerns the two
original frozen representatives.

## Research gate

Small local switching is not a viable contraction mechanism for these
two witnesses:

- literal four-cycle switches cannot preserve the mod-two equation;
- the smallest `C37`-orbit unitary family cannot preserve block margins;
- its monomial boundary consists only of graph relabelings.

Any further unitary attack must use a larger transformation whose margin
restoration is built in globally—for example, a coupled product of
nonmonomial transvections.  This audit supplies no evidence that such a
larger family will reduce the carry, so it should not be pursued as an
unstructured search.

## Reproduction

From this directory:

```text
python3 audit_four_cycle_and_carry_invariants.py \
  ../char2_support_realization/TYPE1_SUPPORT_WITNESS.json \
  ../char2_support_realization/TYPE2_SUPPORT_WITNESS.json

python3 audit_sparse_unitary_transvections.py \
  ../char2_support_realization/TYPE1_SUPPORT_WITNESS.json

python3 audit_sparse_unitary_transvections.py \
  ../char2_support_realization/TYPE2_SUPPORT_WITNESS.json
```

The combined four-cycle/carry replay used about 25 MB and 0.6 seconds.
Each 49,284-member transvection census used about 25 MB and 35 seconds.
