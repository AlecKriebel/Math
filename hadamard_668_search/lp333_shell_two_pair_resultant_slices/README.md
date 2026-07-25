# Pairwise resultant-norm gates for the shell-two physical phase lane

## Status

This package proves and operationalizes three exact necessary invariants for
the prime-167 physical phase problem.  It does **not** produce a Legendre
pair or H(668), and its finite slice census does not exclude a shell-two
profile.

The new result is stronger than equality of the total resultant norm.  Put

```text
E=F_(167^12),             F=F_(167^3),
```

and write the six primitive coordinates of channel `X` as `w_(X,r)`,
`r=0,...,5`.  For each star-paired factor define

```text
nu_(X,r)=Norm_(E/F)(w_(X,r) w_(X,r+3)),    r=0,1,2.     (1)
```

Every physical complementary solution must satisfy the three separate
equalities

```text
nu_(A,0)=nu_(B,0),
nu_(A,1)=nu_(B,1),
nu_(A,2)=nu_(B,2).                            (2)
```

The earlier total-product norm equality is only the product of (2).

## 1. Proof

The primitive-unit theorem permits

```text
R_r=w_(B,r)/w_(A,r).
```

The paired norm-cone equation is

```text
1+R_r R_(r+3)^(167^3)=0.                              (3)
```

Apply `Norm_(E/F)` to (3).  The extension degree is four, so

```text
Norm(-1)=(-1)^4=1.
```

Moreover the norm lies in `F`, where the `167^3` Frobenius is the identity.
Therefore

```text
Norm(R_r) Norm(R_(r+3))=1.
```

But the left side is exactly

```text
nu_(B,r)/nu_(A,r),
```

which proves (2), separately for all three `r`.

The three gates are independent on the ambient unit cone.  The norm map
`E^* -> F^*` is surjective, and the three star-pairs use disjoint
coordinates.  Thus one may prescribe the three `nu_(A,r)` independently
before choosing the corresponding ratio-torus coordinates.

## 2. Complete character factorization

The exact order is

```text
|F^*|=167^3-1=4,657,462=2*83*28,057.                  (4)
```

The factors are pairwise coprime.  For

```text
ell in {2,83,28057},
chi_ell(x)=x^((167^3-1)/ell),
```

equality in `F^*` is equivalent to equality under all three characters.
Consequently (2) is equivalent to nine scalar cyclic gates: three
star-pairs times the three factors in (4).

## 3. Exact physical nine-trit slices

The detached PARI program constructs the pinned repository field exactly:

1. `z` is the image of `X` in `F_167[X]/Phi_37`;
2. the promoted degree-18 `FACTOR_PLUS` selects the correct root `omega`;
3. the promoted deterministic `field_fixture(2)` reconstructs the pinned
   ninth root `alpha`;
4. the physical complement convention, normalized zero words, twelve
   multiplier classes, and all six primitive factors are rebuilt directly.

For each channel alphabet it varies the first three classes having three
active fibers and fixes every other class to local option zero.  Every
channel slice therefore contains exactly

```text
3^9=19,683
```

physical placements.  The audit covers fifteen alphabets:

```text
five canonical A,
five canonical B,
five A-star A.
```

It then joins the canonical A/B and A-star-A/B slices, ten ordered
Cartesian products of

```text
19,683^2=387,420,489
```

physical pairs.  These are exact finite subfamilies, not samples.

### Channel images

Across all fifteen exact slices:

| character | marginal image of each `nu_r` | joint triple support |
|---|---:|---:|
| order 2 | full `2/2` for every `r` | full `8/8` |
| order 83 | full `83/83` for every `r` | 18,969 to 19,387 |
| order 28,057 | 13,880 to 14,231 values for every `r` | 19,332 to 19,683 |

Thus the invariants are strongly nonconstant on the physical alphabets.

### Exact slice contractions

Among the ten exact A/B or A-star-A/B slice joins:

| character | one-pair equality count | contraction | three-pair equality count | contraction |
|---|---:|---:|---:|---:|
| order 2 | 193,693,992 to 193,733,392 | 1.9998 to 2.0002 | 48,417,524 to 48,434,696 | 7.9988 to 8.0017 |
| order 83 | 4,664,194 to 4,671,617 | 82.93 to 83.06 | 646 to 700 | 553,458 to 599,722 |
| order 28,057 | 13,609 to 14,059 | 27,557 to 28,468 | 0 | not applicable |

The first two joint contractions closely match `2^3=8` and
`83^3=571,787`.  Each order-28,057 scalar gate also closely matches the
random factor 28,057 and has positive witnesses for every seed and every
star-pair.

The zero simultaneous order-28,057 count has deliberately narrow scope.
Under uniform independent keys, the expected number in one such slice join
is only

```text
387,420,489 / 28,057^3 approximately 0.0000175.
```

Zero is therefore the ordinary expected slice result.  It is **not** a
profile exclusion and is not used as one.

## 4. Could nine-trit partitioning make the complete join feasible?

No, not on the current machine.  Nine-trit slices are useful audit units,
but they do not reduce the number of complete channel assignments.

For the 405 exact physical-margin targets, the conditioned channel-domain
sizes already computed by the promoted one-sequence tables are:

| domain | minimum | median | maximum |
|---|---:|---:|---:|
| A channel | 266,710,752 | 1,645,293,600 | 69,522,443,424 |
| B channel | 37,948,932 | 2,438,821,245 | 10,363,952,610 |
| A plus B per target | 3,129,845,130 | 6,033,337,266 | 69,610,870,944 |

Summed over the 405 targets, with target-wise duplication retained, a
complete channel-key pass requires

```text
5,091,993,547,996
```

invariant evaluations, or about 258.7 million nine-trit slice-equivalents.
The smallest target still needs 159,014 slices; the largest needs
3,536,600.

The three norm keys require at least 67 bits.  Adding the exact `T1,T2`
join residue requires at least 77 bits.  At a practical 16 bytes per stored
key:

```text
smallest target:  about 50.1 GB,
largest target:   about 1.11 TB,
all targets:      about 81.5 TB.
```

Even storing only the smaller channel is not an exact in-memory solution:
the largest smaller side has 2,238,465,240 assignments, about 35.8 GB at
16 bytes per exact entry.  A 10-bit Bloom filter would fit in about 2.8 GB,
but false positives would still need exact replay and the evaluation cost
would remain.

The frozen GP audit sustained roughly 1,570 assignments per second.  At
that rate a duplicated complete pass would take about 103 years.  Even
optimistic sustained rates give:

```text
1,000,000 evaluations/second:  about 59 days,
100,000,000 evaluations/second: about 14 hours,
```

before external sorting, bucket I/O, or exact collision replay.

The gate is mathematically promising: if the three `F^*` equalities behaved
independently of the existing `T1,T2` layer, the current
`1,123,966,766,238,638,605` survivors would have an expected residual near

```text
1.123966766e18 / 4,657,462^3 approximately 0.011.
```

That is a heuristic, not a proof.  Operationally, a complete join needs a
new algebraic compression of the resultant keys or a substantially faster
implicit character-sum method.  Merely batching the existing domains into
nine-trit slices is not feasible.

## 5. Reproduction

Run:

```sh
/usr/bin/time -l \
  /Users/alec/Documents/tmp/hadamard-env/bin/python \
  freeze_pair_norm_slices.py \
  --output pair_norm_nine_trit_slice_certificate.json
```

The frozen run completed all fifteen channels and ten pair joins in 193.71
seconds.  PARI reported 188.097 seconds for its exact core, and the peak
resident set was 100,466,688 bytes.

Pinned semantic SHA-256:

```text
3585ff30f2a2951bf071c03ea1a1c82c460c6ef46c729b12cd77e53bd74f7010
```
