# Quotiented low-conflict closure and all-class second-barrier search

Date: 2026-07-23 (America/Los_Angeles)

## Outcome

No order-43 Ramsey graph was found. Two reproducible finite-corpus results
substantially sharpen the description of the retained constructive barrier:

1. The exact targeted closure contains 16,082 labeled states with objective
   \(E=3\) and 73,788 with \(E=4\), but these 89,870 graphs collapse to only
   **53 classes modulo graph isomorphism and complementation**: 9 at \(E=3\)
   and 44 at \(E=4\).
2. A frozen second-barrier run used every one of those 53 classes and every
   first edge outside the previously closed move type. It produced 1,670
   distinct labeled \(E=2\) endpoints, but independent recounting and
   dense/sparse canonicalization put all 1,670 back into exactly the two
   previously known complement-isomorphism classes.

This is a reproducible computational observation about finite exported
corpora and one frozen heuristic repair schedule. It is not a global
classification, construction, nonexistence proof, or Ramsey-bound change.

## Exact closure export replay

The previously accepted atomic scan was rerun with a graph6 export added
after every exact objective replay. All 28 substantive counters agreed with
the earlier result. In particular:

| quantity | count |
|---|---:|
| neutral \(E=2\) states | 1,892 |
| barrier-first ordered pair checks | 6,826,336 |
| targeted third-edge checks | 32,465,774 |
| unrestricted fourth-edge checks | 33,315,282 |
| targeted fifth-edge checks | 2,764,212 |
| targeted-closure checks | 2,764,212 |
| closure \(E=3\) states | 16,082 |
| closure \(E=4\) states | 73,788 |
| off-cycle \(E=2\) states | 0 |
| \(E=1\) or \(E=0\) states | 0 |

The closure completed below its 250,000-state cap. The exported streams are
unique as labeled graph6 strings:

```text
E=3 stream
results/constructive/e2_low_closure_v2/closure.e3.g6
16,082 lines
SHA-256 e592a201aa862c62ed98fdb7a3442665fe625f44da8b4586f6fd759580426c58

E=4 stream
results/constructive/e2_low_closure_v2/closure.e4.g6
73,788 lines
SHA-256 62baebe26a52f34b677ef6f6b1b07a21bc1e19a44a8f20ff9939d82c751a9f04
```

The replay result is
`results/constructive/e2_low_closure_v2/export_replay.result.json`,
SHA-256
`1315e444b3edf91e763b3739b96431c1305331d8c7746495ef339c0844d75864`.

## Isomorphism collapse

Every graph and its complement was canonicalized by nauty 2.9.3 `labelg`.
The operation was repeated using dense and sparse internal representations.
The induced ordinary and complement-isomorphism partitions agree exactly.
An independent recursive-bitset K5 implementation then recounted every
retained canonical representative in both colors.

The class census is:

| objective | labeled states | ordinary classes | classes modulo complement |
|---:|---:|---:|---:|
| 3 | 16,082 | 18 | 9 |
| 4 | 73,788 | 88 | 44 |
| total | 89,870 | 106 | 53 |

The class sizes reveal the same 86-step neutral-cycle symmetry seen earlier.
At \(E=3\), eight complement classes have size 1,892 and one has size 946.
At \(E=4\), 34 have size 1,892 and ten have size 946.

The 53 representative graphs are:

```text
results/constructive/e2_low_closure_v2/representatives.e3.g6
9 lines
SHA-256 0f9485a82ecb6dba9b19ea0759ba37ef7c9bc64d481cf8fd7a248480b348471d

results/constructive/e2_low_closure_v2/representatives.e4.g6
44 lines
SHA-256 2ea9964afed1205884e971fb50fce77d783925804ae9d1064460e7b89190bca4
```

The quotient audit is
`results/verification/e2_low_closure_isomorphism_audit_v1.json`,
SHA-256
`cd1f8a9e56e76b0c94df1c5705ca7090588e2eb12a2bd0009f3e53e115f47725`.

## Frozen all-class second-barrier run

For a low-conflict seed, let the conflict-edge union contain every edge of
every current forbidden five-set. The preceding closure already included
every move in this union that stayed at \(E\le4\). The next run therefore
forced:

- every edge outside the current conflict-edge union; and
- every conflict-union edge whose exact post-flip objective exceeded four.

A non-conflict edge cannot destroy a current forbidden set, and the second
case explicitly leaves the low closure. Every forced graph was exactly
recounted before its repair rollout.

The frozen schedule used all 53 representatives, no per-seed truncation, one
256-step tabu/noise repair per forced edge, tabu tenure 11, noise probability
0.09, objective ceiling 80, and seed 20261321. Results:

| quantity | count |
|---|---:|
| forced barriers | 47,675 |
| non-conflict barriers | 46,225 |
| high conflict-union barriers | 1,450 |
| exact forced-graph replays | 47,675 |
| repair steps | 2,080,964 |
| exact objective checks | 2,125,169 |
| retained distinct labeled \(E=2\) endpoints | 1,670 |
| \(E=1\) visits | 0 |
| \(E=0\) constructions | 0 |

The production source and binary hashes are:

```text
src/search43_e2_barrier_escape.cpp
SHA-256 cdddaef4c35dfb9ccdbcc7478029c15eb909247714ffc2bef9e8fa636fb0099c

ephemeral production binary
SHA-256 e145c90c00a6ba7058c58e0ee184ebb3bc8c6292f21c7231161422972cad4b69
```

The frozen plan is
`results/benchmark_plans/e2_low_closure_second_barrier_v1.json`,
SHA-256
`ebbe4ce7d5a6b9027651fe0e1d2ca70b729eda5545b6f84a44e3c5291ec8cac7`.
The result is
`results/constructive/e2_low_closure_v2/second_barrier.result.json`,
SHA-256
`ce9e17cae63f40dde390cc960fbd1865156cf923f2615f8f5c36d4fac3fba993`.

## Endpoint audit: no new basin

The 1,670-endpoint stream has SHA-256
`ba35df48ba6577605135fda1c893283b76420724bd9ff70b4c0641427ec96e97`.
An independent recursive-bitset enumeration verified objective two for every
endpoint. Every endpoint consists of two same-color forbidden five-sets
intersecting in four vertices.

Dense and sparse nauty runs agree on four ordinary isomorphism classes,
which pair into exactly two classes modulo complementation. Their labeled
sizes in this run are 819 and 851. Comparing their canonical labels with the
22 prior catalog-derived near misses finds:

```text
novel labeled endpoints                    0
novel complement-isomorphism classes       0
```

The deliberately retained novel-class file is empty and therefore has the
empty-stream SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

The endpoint-audit plan/result SHA-256 values are:

```text
72a26b4f57a5b57e3b6ee92e5824a4e41d9122d85d82835696d577632f0be387
fae8b82dd05df36cfc353848fb0c1ebd3f049c8975b3e02bf237d2a0ea06f2b1
```

## Decision

The frozen decision rule rejects a larger budget for the same one-barrier
repair operator when no novel \(E=2\) class appears. That condition occurred.
The next constructive experiment must change the move architecture—for
example, two explicitly non-repairing forced edges before any repair—rather
than repeat this funnel with more steps.

The production code counted but did not retain \(E=1\) states. This run had
zero such visits, so no evidence was lost here. Before any successor run,
the code must export and stop on \(E=1\), since such a graph would be the
strongest available near-construction.

## Claim boundary

The finite 53-class cover concerns only the exported targeted closure. The
47,675 first barriers are exhaustive only for the stated first-edge rule;
all subsequent repair paths are heuristic. The absence of \(E=0\), \(E=1\),
or a novel \(E=2\) class gives no global nonexistence conclusion and does
not change \(43\le R(5,5)\le46\).
