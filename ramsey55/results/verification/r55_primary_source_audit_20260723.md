# R(5,5) primary-source and public-data audit

Audit date: 2026-07-23 (America/Los_Angeles; some server timestamps are
2026-07-24 UTC).

## Bottom line

The current certified interval is

`43 <= R(5,5) <= 46`.

I found no published order-43, order-44, or order-45 Ramsey(5,5) graph and no
complete nonexistence computation at any of those three orders. The lower end
is still Exoo's order-42 construction. The upper end is the independently
implemented Angeltveit--McKay exclusion of order 46.

The most useful public inputs are real and machine-readable:

1. 328 known order-42 graphs (whose complements give the historical 656);
2. all 352,366 Ramsey(4,5,24) graphs; and
3. the edge-extremal Ramsey(4,5,n) slices used in the order-46 proof.

The graph data passed independent local checks described below. I did **not**
locate the two order-46 proof implementations, their complete run logs, or
proof certificates. Thus the published order-46 result is authoritative, but
the full computation is not presently replayable from public code.

## Exact status by order

| Order | Audited status | What is and is not proved |
|---:|---|---|
| 42 | Exists | [Exoo's 1989 paper](https://doi.org/10.1002/jgt.3190130113) gives a `K_42` two-colouring with no monochromatic `K_5`. McKay and Radziszowski later found 656 graphs, but explicitly presented completeness as a conjecture, not a theorem. |
| 43 | Open | [McKay--Radziszowski 1997](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf) checked that none of the known 656 order-42 graphs has a one-vertex extension. This excludes only that extension route. |
| 44 | Open | No construction or complete exclusion was located. |
| 45 | Open | No construction or complete exclusion was located. |
| 46 | Does not exist | [Angeltveit--McKay](https://arxiv.org/abs/2409.15709), subsequently [published in the Journal of Graph Theory](https://doi.org/10.1002/jgt.70029), proved `R(5,5) <= 46` by linear programming, catalog generation, and gluing computations independently implemented by both authors. |

Nonexistence at order 46 also excludes every larger order: an induced
46-vertex subgraph of any larger Ramsey(5,5) graph would itself be a
Ramsey(5,5,46) graph.

The maintained [Small Ramsey Numbers survey, revision
18](https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf) agrees with this interval,
but the primary papers above are the evidentiary basis.

## What the historical computations actually exclude

The strongest order-42/order-43 evidence is narrower than a proof of
`R(5,5)=43`:

- [McKay--Radziszowski 1997](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf)
  found the same 656 order-42 graphs by several routes. They generated 5,812
  heuristic hits, searched neighbourhoods of the known graphs for more than a
  decade of CPU time, and exhaustively extended 100 random 36-vertex
  subgraphs to more than 65 million order-42 outputs, all isomorphic to known
  graphs. They checked that none of the 656 extends to order 43. They still
  labelled both `R(5,5)=43` and completeness of the 656 as conjectures.
- [Angeltveit--McKay 2018](https://arxiv.org/abs/1703.08768) reports
  unpublished 2014 work of Lieby and McKay proving that an additional
  order-42 graph cannot share a 37-vertex subgraph with any of the 656. No
  public implementation, catalog of overlap cases, or certificate for this
  2014 computation was located.
- [Lehavi 2024](https://arxiv.org/abs/2411.04267) and its public
  [ROVEaC repository](https://github.com/aLehav/ramsey-ove-and-check) exclude
  an order-43 graph having at least six vertex-deleted subgraphs among the
  known 656. The paper itself warns that the 656 are not known to be
  exhaustive. This is a conditional/subclass result, not `R(5,5) <= 43`.

No source located in this audit establishes a comparable complete result for
orders 44 or 45.

## Degree and neighbourhood reductions

The formalized theorem `R(4,5)=25` implies that every vertex of a
Ramsey(5,5,n) graph satisfies

`n - 25 <= degree(v) <= 24`.

This gives the exact first-line search domains:

| Candidate order | Possible degrees before stronger constraints |
|---:|---|
| 43 | 18 through 24 |
| 44 | 19 through 24 |
| 45 | 20 through 24 |
| 46 | 21 through 24 |

For a vertex of degree `d`, its neighbourhood is a Ramsey(4,5,d) graph and
the complement of its dual neighbourhood is a Ramsey(4,5,n-1-d) graph. This
is the structural bridge to the public Ramsey(4,5) catalogs.

The order-46 proof uses the exact identity

`sum_v [ e(F_v^-) - e(F_v^+) - d(v)(n-2d(v))/2 ] = 0`

and reduces the computational input to:

- `R(4,5,24,e >= 127)`;
- `R(4,5,23,e >= 119)`;
- `R(4,5,22,e >= 113)`; and
- `R(4,5,21,e = 107)`.

It then glues selected pointed graphs. The first implementation used about 15
CPU-years to create catalogs and another 15 CPU-years for gluing. The second,
methodologically different replication used about 50 additional CPU-years.
The paper concludes that improving the upper bound by the same method would
require excessive computation and probably needs new theory.

For comparison, the 328 supplied order-42 representatives have degrees
19--22 and 423--430 edges. These are observed properties of the known
catalog, not necessary degree bounds for every hypothetical order-42 graph.

## Public graph data: independent checks

The authoritative source is Brendan McKay's [Ramsey graph data
page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html). The surrounding
[data collection](https://users.cecs.anu.edu.au/~bdm/data/) specifies graph6
format and CC BY 4.0 licensing for McKay's data unless otherwise noted.

All external downloads below were made into
`/private/tmp/r55-audit.h2oHwp`, checked there, and then deleted after this
report was written. Hashes pin the audited bytes.

### Known Ramsey(5,5,42) representatives

Audited workspace path:
`data/r55_42some.g6`

- SHA-256:
  `067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`
- 47,888 bytes; 328 nonempty, byte-distinct graph6 records.
- Two independent existing verifiers checked every record: exhaustive Python
  5-subset enumeration and recursive-bitset C++ clique search.
- Result: 328/328 are order 42, with zero 5-cliques and zero independent
  5-sets. Edge counts and sorted degree sequences agreed between verifiers.
- Edge histogram:
  `423:1, 424:7, 425:29, 426:66, 427:89, 428:77, 429:43, 430:16`.
  This exactly matches the 1997 paper.
- Temporary aggregate report SHA-256:
  `2e52bd4065b6b08eeef0e912530d3f8f97b054133da9604c1e56af065d2777fe`.
- Python verifier SHA-256:
  `fb8f5bee76f98a37a080970cd0548b88825f6f0f49f1144db20a3524ce5878b5`.
- C++ verifier SHA-256:
  `2ba9e189bc56b4d7c439b26317ade8eec60589c58e294bd26d7f35f4bd631f89`.

This verifies Ramsey validity and record uniqueness, not pairwise
non-isomorphism. The source and the 1997 paper supply the isomorphism-class
claim. The other 328 historical graphs are complements and are not separate
records in this file.

### Complete Ramsey(4,5,24) catalog

Downloaded URL:
`https://users.cecs.anu.edu.au/~bdm/data/r45_24.g6`

- SHA-256:
  `83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0`
- 16,913,568 bytes.
- A temporary streaming C++ graph6 parser checked all 352,366 records:
  correct order 24, no 4-clique, no independent 5-set, and no duplicate byte
  records.
- Full edge histogram:
  `116:9, 117:90, 118:806, 119:4358, 120:16346, 121:43457, 122:79678,`
  `123:92504, 124:67209, 125:31996, 126:11485, 127:3401, 128:843,`
  `129:147, 130:32, 131:3, 132:2`.
  It exactly matches the independently published 2018 table.
- Temporary verifier source SHA-256:
  `9428c85b44a78e05773898ff033d3d3f46a5595ac3084fe3637954b261dd2421`.

Again, this audit checked graph validity and byte uniqueness, not independent
canonical-isomorphism uniqueness.

### Edge-extremal Ramsey(4,5) archive

Downloaded URL:
`https://users.cecs.anu.edu.au/~bdm/data/r45extreme.tar.gz`

- SHA-256:
  `9cfac9dbd1c209cfa342e5d5424df2a7a3fbb008ca00bf0a992e5bbe72f925b6`
- 90,599,728 bytes; gzip and tar integrity checks passed.
- Every graph in the upper-proof-relevant classes below was parsed and
  checked for its stated order and edge count, absence of a 4-clique,
  absence of an independent 5-set, and byte uniqueness within its class.

| Class | Count | SHA-256 |
|---|---:|---|
| `R(4,5,21,e=106)` | 10,188 | `2be4df6ba89b1c55743624fb6e8141741aef82b06a922aa0a069923942389593` |
| `R(4,5,21,e=107)` | 31 | `6ef8619d5d6be9efa15cb9a5ccb6b0da7304cfbfd57fff29bb0dec2e46f81bef` |
| `R(4,5,22,e=113)` | 30,976 | `1e1a54b719dcdebb57581ee6f3cd4e1721e828680a72128010f1f888a4dda9db` |
| `R(4,5,22,e=114)` | 133 | `54dffec4ecab0f863b75620ccf8b228e5d6299c799e2d6b284fd51c51aa96ed7` |
| `R(4,5,23,e=119)` | 332,778 | `d41a20f92db7952fd0e2faf6776b4c696fcf23e6c700e0be890d8e9bad0dc8f1` |
| `R(4,5,23,e=120)` | 7,800 | `d7c9d88a02e5d3489bee994000419ac9f58f9e0bd0df778ba9149f694a5ff00c` |
| `R(4,5,23,e=121)` | 119 | `f68ea0279240dfaabcff5d94b6adb4f665672523aea0d04780d93bb052d9be94` |
| `R(4,5,23,e=122)` | 2 | `81a34501614786ed357dab36be0a0b6c04b4c6ce12668839cf4e9d127cf1e6fe` |

Temporary class-verifier source SHA-256:
`5b6a1b01b14d6ba0d74c750bf8359e07c02d46355390e03f247a8f9036464729`.

These exact counts match the order-46 paper. The archive therefore supplies
the published catalog inputs, but not the gluing program or its negative
certificates.

## Public code

### ROVEaC conditional extension search

Repository:
[`aLehav/ramsey-ove-and-check`](https://github.com/aLehav/ramsey-ove-and-check)

- Audited clean shallow clone at commit
  `cd8f94656d70cc5901ba54069e9f0e9f941b6389`
  (commit date 2025-01-14); `git fsck` passed.
- Python package using NetworkX and `tqdm`; no graph data or automated test
  suite is included.
- Its zero-output claim is conditional on the known catalog and covers graphs
  with enough known vertex-deleted subgraphs. It cannot establish global
  order-43 nonexistence unless the order-42 input is complete.
- The full published run was not replayed in this audit because the temporary
  environment lacked NetworkX and the task was stopped when disk became
  constrained.

### Formal proof of R(4,5)=25

Paper:
[`A Formal Proof of R(4,5)=25`](https://arxiv.org/abs/2404.01761)

Repository:
[`barakeel/ramsey`](https://github.com/barakeel/ramsey)

- Audited clean shallow clone at commit
  `065c07054483e3132f12909103e6d0e35e912c28`
  (commit date 2025-05-16); `git fsck` passed.
- The repository contains HOL4/SML sources and an order-24 witness.
- It is not a lightweight, self-contained replay: its instructions require
  HOL4, Poly/ML, a separately downloaded cover archive, very large memory, and
  gluing stages quoted at 18 and 16 days. No replay was attempted.
- This is valuable assurance for the degree bound, but it does not directly
  decide orders 43--45.

No public repository for either implementation of the
Angeltveit--McKay order-46 computation was located in the paper, arXiv
metadata, author publication page, or targeted repository searches.

## Correction to a published K43 near-miss

[Ge et al., arXiv:2212.12630v3](https://arxiv.org/abs/2212.12630) gives
explicit variants of Exoo's cyclic construction:

- Example 6.1: retain vertex 0 and apply the 16 Exoo recolourings; the paper
  claims 4 red and 9 blue monochromatic `K_5`s.
- Example 6.2: additionally recolour edge `(21,22)` from red to blue; the
  paper claims 1 red and 8 blue monochromatic `K_5`s.

The Example 6.2 blue count is impossible on monotonicity grounds: changing a
red edge to blue cannot destroy an existing blue clique. An independent
exhaustive enumeration of all `C(43,5)` vertex sets from the paper's exact
definition produced:

- Example 6.1: `(red, blue) = (4, 9)` — confirmed;
- Exoo(42), after deleting vertex 0: `(0, 0)` — confirmed;
- Example 6.2: `(1, 11)`, not `(1, 8)`.

Temporary audit script SHA-256:
`8bf7b402f7abaca131fc0f142defdb53bdc3d17756ac3396cf2cc68fbfe4c6a2`.

Therefore Example 6.2 is a 12-violation order-43 seed, not a 9-violation
seed. It should not be entered into benchmark data under the published
objective value without correction.

## Actionable integration and research priorities

1. **Finish trust promotion of the existing order-42 catalog.** The local
   `data/r55_42some.g6` bytes now have an all-record, dual-verifier PASS.
   Preserve the exact source URL, SHA-256, CC BY 4.0 attribution, and the
   distinction between “328 known representatives” and “a proven complete
   catalog.” Optionally add a canonical-isomorphism duplicate check before
   asserting 328 isomorphism classes locally.
2. **Use all 328 representatives plus complements as a controlled seed
   corpus.** This materially broadens search beyond one Exoo representative.
   Keep “one-vertex nonextendible” separate from “no nearby order-43 graph”:
   vertex deletion forces every genuine order-43 graph to yield 43
   order-42 graphs, but the known 656 may be incomplete.
3. **Import only the needed Ramsey(4,5) slices if implementing the published
   LP/gluing architecture.** The required high-edge files plus `r45_24.g6`
   are much smaller than maintaining every extreme class. Use the hashes in
   this report and a manifest rather than silently trusting filenames.
4. **Implement source-derived degree/neighbourhood presolve for orders
   43--45.** Enforce degree intervals, neighbourhood/dual-neighbourhood
   Ramsey types, handshake parity, and the exact excess identity before SAT
   or local search. The public extremal catalogs can provide canonical
   allowed high-edge neighbourhoods. This is a sound reduction; extrapolating
   the order-46 LP thresholds unchanged to smaller orders is not.
5. **Do not spend effort merely replaying ROVEaC as if it closed order 43.**
   Its useful contribution is overlap indexing by 41-vertex deletions and
   isomorphism invariants. A project implementation should emit an explicit
   coverage statement (“at least k known deletions”) for every negative
   result.
6. **Treat an upper-bound improvement as a new-theory project.** Public data
   make a partial reconstruction of the order-46 pipeline possible, but the
   missing implementations/certificates and published 80 CPU-years make a
   faithful replay substantial. Moving from 46 to 45 by the same method is
   not supported by the authors' cost assessment.

## Audit limitations

- Search was restricted to primary papers, author-maintained data, and
  author-linked repositories. The dynamic survey was used only as a
  current-status cross-check.
- No one was contacted.
- Public-data validation checked graph semantics, byte uniqueness, counts,
  and published histograms. It did not independently prove pairwise
  non-isomorphism of the large catalogs.
- The order-46 computational proof itself was not replayed because its
  implementations and certificates were not located.
- Temporary downloads and clones were intentionally removed after hashes and
  results were preserved here.
