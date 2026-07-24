# Isomorphism collapse of the 22 exact two-conflict near misses

Date: 2026-07-23 (America/Los_Angeles)

## Outcome and scope

**CERTIFIED FINITE-CORPUS CLASSIFICATION.** The 22 independently replayed
order-43 graphs with exactly two same-colour forbidden five-sets occupy only:

- three ordinary graph-isomorphism classes, of sizes 10, 11, and 1; and
- two classes after graph complementation is also identified, of sizes 10
  and 12.

Thus the 22 labeled neutral cycles previously proved pairwise disjoint are
not 22 structurally distinct basins. Up to relabeling and complementation,
the retained E=2 corpus contains exactly two near-miss graphs.

This classifies only the fixed 22-candidate corpus. It does not classify all
order-43 E=2 graphs and is not a nonexistence result.

## Candidate classes

The first complement class contains the ten independent-conflict candidates
from catalog source lines

```text
1, 3, 11, 14, 131, 144, 163, 177, 278, 326
```

The second complement class contains the eleven clique-conflict candidates
from lines

```text
2, 4, 18, 44, 152, 183, 253, 316, 325, 327, 328
```

together with the independent-conflict candidate from line 24, which is
isomorphic to the complement of the eleven-member class.

Before canonical labeling, every input was checked again to have order 43,
exactly two homogeneous five-sets of one colour, and an intersection of
exactly four vertices. Nauty 2.9.3 `labelg` then classified every graph and
its complement. Dense- and sparse-representation runs produced exactly the
same two equivalence partitions.

## Shared-core deletion closure

If the two forbidden five-sets are \(C\cup\{a\}\) and \(C\cup\{b\}\), where
\(|C|=4\), deleting any vertex of \(C\) destroys both conflicts. The 22
near misses therefore yield 88 order-42 graphs.

For all 88 deletions:

- direct enumeration inspected all ten pairs of every five-set and found no
  clique or independent five-set; and
- a separate recursive-bitset clique search found neither a five-clique in
  the graph nor in its complement.

Canonical labeling reduces the 88 labeled graphs to four ordinary
isomorphism classes and two classes modulo complement. Every complement
class is already represented by line 42 or line 256 of the supplied
328-line catalog. The two ordinary classes absent from the literal catalog
are precisely complements of those represented classes.

Consequently, this exact deletion transformation adds no new order-42 seed
class modulo complementation. It shows that all 22 near misses funnel back to
the same two catalog basins.

## Reproducibility and hashes

The production runs were frozen in advance:

```text
candidate-classification plan
34c6ba344e062891f72d40e836a1ab981987da416ce6460f74041230d878bf2e

shared-core-deletion plan
5111f755a3d16c1dc5085b1e8bd70cf40a453770efee4c327e46e84336d0aac6
```

Principal result hashes:

```text
candidate isomorphism audit
07969bcbbfb62fcd1e40ef3d2fb718816b1f5630c71db67c9e9a53322ed2be7b

shared-core deletion audit
7692195c4fc76d469de1ee204e5f2a0f64612f528af96d7ba0b2ddf4a6099c0e

22-candidate concatenated corpus
172fd8dca7e2a465bb483148036c7dd7a549796b191078742b80ef7df0ff34f0

328-line order-42 catalog
067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb

nauty 2.9.3 release archive
9fc4edae04f88a0f5883985be3b39cf7f898fd6cc96e96b9ee25452743cc1b5b

labelg executable
ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0
```

The empty file
`results/constructive/e2_core_deletion_novel42_v1.g6` is intentional: its
SHA-256 is the empty-stream hash because no complement-normalized class was
new.
