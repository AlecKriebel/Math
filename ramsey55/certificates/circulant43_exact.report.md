# Exact exclusion of circulant order-43 colorings

Evidence label: **CERTIFIED STRUCTURAL SUBCLASS EXCLUSION**

This certificate excludes every undirected circulant graph on
\(\mathbb Z_{43}\) as a \((5,5;43)\)-graph. It does **not** exclude arbitrary
order-43 graphs and does not change the bound \(43\leq R(5,5)\leq46\).

## Scope and encoding

An undirected circulant graph on \(\mathbb Z_{43}\) is determined by 21
variables. Variable \(x_d\), \(1\leq d\leq21\), specifies the common color of
all pairs at circular distance \(d\).

For each of the \(\binom{43}{5}=962{,}598\) vertex five-sets, the generator
forms the set of distinct circular distances among its ten pairs. A five-set
is a clique exactly when all variables in that signature are true; it is
independent exactly when they are all false. Hence each signature produces an
all-negative and an all-positive clause. Deduplicating identical signatures
is satisfiability-preserving.

There are 10,437 distinct signatures and 20,874 resulting clauses. Their size
distribution is:

| Signature size | Count |
|---:|---:|
| 4 | 21 |
| 5 | 42 |
| 6 | 462 |
| 7 | 819 |
| 8 | 2,877 |
| 9 | 3,486 |
| 10 | 2,730 |

## Preregistration and independent reconstruction

The immutable plan is
`results/benchmark_plans/circulant43_exact_v1.json`, SHA-256
`6e43423dfdf4e8e62332cabc250bc2bb55e46b0cd2a5b22cddffb8d98e2b18b8`.
All source pins and the storage gate passed before generation.

The generated CNF has SHA-256
`d688450b666ec8722820ba266a572f36ae69e8e0b90c171750b5a8112c01be9a`
and 597,624 bytes. A separately written checker reconstructed every
five-set, distance signature, clause, header field, histogram entry, and
metadata binding. It matched all 20,874 clauses exactly. The checker result
has SHA-256
`3aab579dd97851caf9b716536601620ea1d502c914c12140457c2372ff26e35e`.

## Proof result

Pinned Glucose3 reported UNSAT after 2,022 conflicts. Its 69,852-byte DRAT
proof has SHA-256
`1c4f5f6910163d0aa6e6b1b33d5dbb13d83b0170a24495290917b529de006feb`.
`drat-trim` returned `VERIFIED` and derived a 323,172-byte LRAT proof with
SHA-256
`1d800fbb5c318b58ec538818c4ad974a412ea61511a072efda3a134d172b4d42`.
`lrat-check` independently returned `VERIFIED` against the same matched CNF.
The pipeline result has SHA-256
`eeda889a6dc41c8c6b009b3a534c1719794b2d0b9719404948e09cefcc794d09`.

Therefore no undirected circulant graph on \(\mathbb Z_{43}\) avoids both a
5-clique and an independent 5-set.
