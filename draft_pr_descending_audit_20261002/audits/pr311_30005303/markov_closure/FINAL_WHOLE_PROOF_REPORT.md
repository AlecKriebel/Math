# Final independent Markov/closure consistency report

**Verdict: PASS for both exact source questions.** In the authenticated finite
binary setting, Conjecture 1 is true and Conjecture 2 is false. The C4
counterexample also falsifies the source's stronger lattice-support Conjecture
3. This family found no remaining mathematical or checker-consistency gap in
the full two-turn author packet. Assigned family-audit completion: **100%**.

This verdict is independent of inherited review conclusions, sibling-family
results, the root's current reasoning, and priority searches. It certifies
the mathematics and its supplied exact checks, not historical novelty,
completeness of literature searches, remote state, or publication readiness.
No Git mutation, remote write, publication, or external contact occurred.

## Source and staged independence

The primary source was independently retrieved from
[EMS Press](https://ems.press/content/serial-article-files/46992), DOI
[10.4171/OWR/2022/55](https://doi.org/10.4171/OWR/2022/55), and visually inspected
on printed pp. 3125-3126 before any candidate text was released. Its exact
sample space is {0,1}^V for finite V; Markov means global graph separation;
factor potentials are finite real values; zeros are allowed; and the Ising
formula is literally edge-only. The original PDF hash is
`56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65`.

Source criteria were hash-frozen at actual UTC 2026-10-04 15:54:23, hash
`dab23a2c8f753dced42b7d93ed06564eecdf1bc36be3ae272ba4ec0611e42b9b`.
The criteria's earlier header records its source checkpoint, not the final
hash event. Root accepted those criteria before releasing four prose files.

The first candidate assessment was hash-frozen at actual UTC
2026-10-04 16:04:40, hash
`acf25a0a470b6a4c90d664ec3c16dc2f9983c58adb58c08854ee535ee98b3650`.
It already accepted both conclusions through independently reconstructed
proofs and self-authored exact controls, before any author checker was read.
Root read that assessment and log before releasing the author-code stage.

## Exact read scope and bindings

I read precisely the 18 author files listed in FINAL_PACKET_MANIFEST plus
that manifest itself, making **19 author packet files**. These include the
original source record, two proof texts, two source gates, two logs, two
ledgers, the first-turn manifest, readiness, final brief, three checkers, and
their three stored outputs. Their full absolute paths, actual byte counts,
SHA256 hashes, and modes at the binding read are recorded in
`INPUT_BINDINGS.json`. Every listed byte count/hash was checked against the
final manifest, the earlier manifest, and each overlapping publication entry.

PUBLICATION_MANIFEST was separately read for permitted input binding only.
Its entries exposed names, sizes, and hashes of inherited review files and
PUBLICATION_SUMMARY, but none of those semantic bodies was opened, read,
executed, or used. No sibling-family artifact or root conclusion was read.
All 20 authorized author/manifest input hashes remained unchanged through
reproduction. The primary report is separately bound in the same receipt.

`INPUT_BINDINGS.json` SHA256:
`8c7dce0bb2c794f642b660a48b458bf7bc0a4bc34ba2d505fed303a18f3b9b39`.

## Whole-proof verification

### Negative factorization answer

The candidate's support x1=x2 is a meet/join preserving copy of the
three-dimensional Boolean cube. The top-atom indicator abc is supermodular,
so weights 2^(abc), normalized by 9, satisfy every MTP2 inequality; outside
support the right-hand side vanishes. Exhaustive source separation analysis
gives exactly four ordered nontrivial C4 separations. Each required CI holds
because conditioning determines x1 or x2.

Every C4 clique has size at most two. The quotient cube's four even-parity
and four odd-parity atoms have identical projection multisets onto each
source edge, singleton, and empty clique. Substituting finite real clique
factors therefore forces equal products, without logarithms or division.
The candidate gives the unequal products 1/6561 and 2/6561. This polynomial
also persists in every pointwise factorizing limit, excluding M_E membership.
It supplies a complete counterexample to the stated C2 and its stronger C3,
while imposing none of the closures C1 actually assumes.

### Affirmative closure answer

I checked all central steps against the frozen source criteria:

- Exact pairwise factorization makes support the intersection of its unary
  and edge projections. MTP2 makes that nonempty support a sublattice.
  Fixed coordinates and active-edge implications describe it completely;
  collapsing implication cycles gives a poset and every upper set occurs.
- Log factors are used only on their positive projected supports. Comparable
  components contribute affine terms. Quadratic interactions between
  incomparable components are aggregated over all original connecting
  edges. The four upper sets built from their strict successors isolate
  each aggregate coefficient, and MTP2 makes it nonnegative.
- An aggregate is placed on one existing edge, unary coefficients on
  existing vertices, and implication violations receive attractive
  original-edge penalties. Their zero set is exactly the original support.
  Thus every zero-support MTP2 pairwise law is a limit of positive
  attractive laws, with no graph edges added.
- Every positive attractive energy is a nonnegative-capacity cut energy
  plus a constant. Maximum-flow existence follows from compactness; the
  absence of a residual augmenting path yields a zero-residual minimum cut.
  Conservation gives residual cut cost E(x)-min E for every configuration.
  Residual factors therefore lie in [0,1] and have product 1 at a minimum.
  Their normalization sums stay in [1,2^|V|]. Compactness cannot lose all
  unnormalized mass, so limiting factors give a finite actual factorization.
- Finite polynomial MTP2 and CI conditions pass to limits. Nonnegative
  graphical factors imply global Markov by product separation after a
  positive-mass conditioning assignment; null assignments require nothing.
- Literal uniform isolated vertices, nonempty edgeless empty-product or
  scalar-normalized conventions, and V=empty are explicitly covered. No
  arbitrary isolated unary law is substituted for the literal source class.

The result is equality of the MTP2 unary-and-edge factor class with the
closure of positive attractive models. The source's edge-only intersection
is a closed specialization. No unsupported assertion that an arbitrary
factor image is closed is used; the nondegenerate normalization bound is
the mechanism that resolves that potential failure.

The six-cycle auxiliary counterexample and its exhaustive source CI checker
are consistent with the same equality-block mechanism. The C4 proof alone
settles the negative source target; C6 remains corroborating finite evidence.

## Independent controls and code consistency

Before author-code exposure I authored `independent_controls.py` without
reading any checker. Its unchanged SHA256 is
`c7107a16077b2af89a7c094bb4c7f358321548f6e85f4f75bce65b5dab9c2e69`.
It exhaustively checks all sublattices and simple graphs through dimension
4: 731 nonempty four-cube sublattices and 18,067 total graph/support
representations across dimensions 0-4. It additionally checks 600 generated
integer attractive networks and 19,125 individual configurations through
dimension 7, including exact base-two factor products and normalization.

The source-first boundary controls pass: global versus pairwise Markov on
thin equality support, adjacent-square MTP2 false positives at zeros,
constant-addition smoothing failure, mixed-sign original edges with a
positive aggregate, and antiferromagnetic K3 nonclosure outside MTP2.
These controls have no universal-proof claim; the independently checked
arguments above supply the all-graph quantifiers.

After code release I inspected the three author scripts. C4 and C6 enumerate
all MTP2 pairs and all source global separations, evaluate CI as marginal
polynomial equalities, and check projection-multiset balance. The closure
checker tests support, SCC/equality correspondence, quotient squares,
aggregate signs, reconstruction, attractive lifted penalties, residual
capacities, no new edges, and normalization at energy minimizers. Its
generated samples are finite evidence; it states that limitation. All
asserted numerical identities use exact integers, with no floating-point
approximation used in the assertions.

## Reproduction: actual argv, UTC and full streams

All subprocesses used `/opt/homebrew/opt/python@3.14/bin/python3.14`, Python
3.14.6, with assertions enabled, and this family folder as their working
directory. Exact absolute argv, microsecond UTC times, exit status, code
hashes, full stdout, full stderr, and output hashes are recorded in
`REPRODUCTION_MANIFEST.json`; streams reside in `reproductions/`.

| Check | Actual UTC start / end | Exact assertions | stdout SHA256 |
|---|---|---:|---|
| Author C4 | 16:14:30.910442 / 16:14:30.939652 | 332 | `2a34abce573b98bd2ec1e8d76de22cd1a6094b686bde35379719ea3bac99ccaf` |
| Author C6 | 16:14:30.940430 / 16:14:31.018855 | 13,520 | `79b2f37c9daf023fb663597f18dabda887692ceddcc3ae78d44e163c01d40cd9` |
| Author closure | 16:14:31.019700 / 16:14:32.777494 | 550,337 | `37a008d55db19bfab9ac6b048fa94723227a87878cacdcca400db55b40cf0508` |
| Independent controls | 16:14:32.778233 / 16:14:38.640565 | Described above | `1f302ead79a4bde6f89fc48526d7b813ce796e700fd8d9f07c6d50137a1fd720` |

All times are 2026-10-04 UTC. Every process exited 0, every stderr was empty,
and every stdout matched the stored receipt byte-for-byte. The author total
is **564,189 exact assertions**. Independent output reproduced the pre-code
frozen result exactly. Input and code bytes remained unchanged.

Reproduction-manifest SHA256:
`864f14b8deb4dcc2927bac43cad44fc5931d326e83d842cc716c45c6dfc60bdb`.
Provenance-runner SHA256:
`5289168c58f8f96ef7b0b93a67875ca59bec538426f3d6fffd9ca10993fff7d6`.

## Freeze integrity and precise remaining scope

The source criteria, first assessment, independent code, and original
independent output were **observed as 0644**, then changed to 0444 at the
16:12:33 checkpoint, with all four bytes/hashes unchanged. This report
does not backdate the filesystem permission seal to either earlier hash
freeze. Final artifact modes, actual transitions, hashes, and output
bindings are recorded by the concluding audit seal.

There is no remaining proof or computation-consistency gap in this family's
assigned source target. Unperformed historical priority research and root
publication decisions are separate work, not gaps in either mathematical
answer. Third-party PDF and rendered source pages remain local verification
material and are not a publication deliverable. This completed report is
offered to the root for synthesis; no promotion or remote write is performed.
