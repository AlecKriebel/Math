# Exact Ramsey-anchor extension to the global degree-18 branch

Date: 2026-07-23 (America/Los_Angeles)

## Outcome and evidence boundary

**CERTIFIED EXACT COVER AND ENCODING, NOT A SOLVE.** The normalized global
degree-18 branch has an independently checked exact cover by the same 143
anchor-matrix orbits used for degrees 19 and 20. A compact selector-union CNF
represents that cover. Its materialized 90,757,889-byte formula was checked
clause-for-clause against the audited global CNF and an independent
reconstruction of every added clause.

No SAT solver was run on this formula. There is no SAT model, UNSAT
determination, DRAT proof, or LRAT proof. The degree-18 branch remains open,
no order-43 graph is excluded or constructed, and no Ramsey bound changes.

This is a standalone extension. It does not modify or import the degree-19/20
v1 cover generator or checker.

## The exact boundary argument

Start with a model in the normalized branch \(d=18\). Let the root be
\(v=0\), and put

\[
A=N(v),\qquad B=V\setminus(A\cup\{v\}).
\]

Then \(|A|=18\) and \(|B|=24\). The base formula already constrains every
degree to the interval 18--24, so fixing the 42 root-star literals fixes the
exact normalized degree-18 branch.

1. `G[A]` contains no \(K_4\), since such a \(K_4\) together with \(v\)
   would be a \(K_5\). The equality
   \[
   |A|=18=R(4,4)
   \]
   therefore forces an independent four-set in `A`. This is the
   zero-slack obligation that distinguishes degree 18 from the previously
   checked degree-19/20 cases.
2. `G[B]` contains no independent four-set, since the root is nonadjacent
   to every vertex of `B` and would extend it to an independent five-set.
   Since \(|B|=24\ge R(4,4)=18\), `G[B]` contains a four-clique.
3. Relabel one `A` independent four-set and one `B` four-clique to the first
   four labels on their respective sides.
4. The resulting \(4\times4\) cross-adjacency matrix has no all-one row:
   such a row vertex and the anchored `B` \(K_4\) would form a \(K_5\). It
   has no all-zero column: such a column vertex and the anchored `A`
   independent four-set would form an independent five-set.
5. Exactly 35,714 of all 65,536 binary matrices satisfy these conditions.
   Independent permutations of the two anchors give an
   \(S_4\times S_4\) action of order 576. Exact enumeration partitions the
   feasible matrices into 143 orbits.

Thus every graph in the original normalized degree-18 branch is isomorphic
to a model of at least one of the 143 cubes. Conversely, every cube only adds
units to that branch. The cover need not be disjoint.

The ordered canonical representative list has SHA-256
`7ac386a677a64b1bfe00226a73ffca27957cc2aa355b552b008e74b3d170d97e`,
identical to the degree-19/20 v1 list.

## Exhaustiveness of the secondary witness selectors

The compact encoding also uses two exact five-way witness unions.

- By \(R(3,5)=14\), `G[A]` contains a triangle: an alternative independent
  five-set is forbidden globally. A triangle meets the anchored independent
  four-set in at most one vertex.
- By \(R(5,3)=R(3,5)=14\), `G[B]` contains an independent triple: an
  alternative \(K_5\) is forbidden globally. An independent triple meets the
  anchored four-clique in at most one vertex.

For each side, the only possible anchor-intersection sizes are therefore zero
and one. Relabeling the non-anchor vertices gives exactly five location
patterns: one disjoint pattern and one for each of the four possible anchor
vertices. The independent checker reconstructed all ten patterns, verified
three edge literals per pattern, and checked that the location labels are
exactly `disjoint, 0, 1, 2, 3`.

After reserving three non-anchor labels per side, the remaining vertices are
freely permutable within each side. Their eight-bit incidence vectors to the
two anchors are sorted lexicographically. This uses 26 adjacent comparators
and 6,630 primary-only clauses. The checker exhaustively verified the direct
comparator template on every pair of binary vectors at widths one through
eight.

## Exact cover and formula checks

The production extension contributes:

| component | count |
|---|---:|
| root-star and anchor unit clauses | 54 |
| anchor-matrix selector variables | 143 |
| anchor-matrix selector clauses | 2,289 |
| witness selector variables | 10 |
| witness selector clauses | 32 |
| signature comparators | 26 |
| signature-sort clauses | 6,630 |
| total appended clauses | 9,005 |

Each cube has 54 common assumptions and 16 matrix assumptions, for 70
assumptions total. All 143 cube records passed the independent hash and
layout check with zero errors. The independent checker imports neither this
generator nor the degree-19/20 v1 cover; it separately reconstructs:

- all 903 primary edge variables and the 42 root-star units;
- the 12 anchor-structure units;
- every binary cross matrix and the exact \(S_4\times S_4\) orbit partition;
- all 143 cube assumption streams;
- both five-way witness unions;
- all signature-ordering clauses; and
- the materialized DIMACS stream and metadata.

The compact union has 65,556 variables and 2,061,137 clauses. Streaming
verification matched all 2,052,132 copied base clauses followed by exactly
9,005 expected additions. Every header, count, byte count, and digest check
passed.

```text
base CNF:
certificates/direct_ramsey43.cnf
SHA-256 141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1

degree-18 plan:
results/benchmark_plans/global_anchor_degree18_extension_v1.json
SHA-256 3c653a20a3d985921a3bf5b1b25b3744dbddb82fa43c278007e256ed5b161934

independent plan check:
results/verification/global_anchor_degree18_extension_v1.check.json
SHA-256 d368da3f32239487917559a3e2b0943d7bdf73200a4b018ed58ed51fa2f00c36

materialized formula metadata:
results/global_exact/global_anchor_d18_extension.metadata.json
SHA-256 d82bc58d6c8c45075d4afd1c52131e2a055568e1cacd657a06d211e3ce0ab301

materialized formula:
90,757,889 bytes
SHA-256 a14a4951041942c01d8787a381c36ca3d094633255a2d134c7879fbec0af78c7

independent materialized-formula check:
results/verification/global_anchor_d18_extension_union.check.json
SHA-256 be5c00086b5f32e046d25ef0aab24e9c8ab8faa2e6a5195d98388fa3dfaa09cf

appended clause stream:
SHA-256 782dd9bfe9d83d74ccf69939e6cbfff5b3060bed29904f0694a20f4bf223e904
```

Six implementation tests cover the orbit census, the exact Ramsey boundary,
common and cube layouts, witness-selector exhaustiveness, comparator
semantics, and independent clause-stream agreement.

## Preserved v1 checkpoint

The pre-existing degree-19/20 v1 artifacts remain byte-identical:

```text
results/benchmark_plans/global_anchor_cube_cover_v1.json
SHA-256 c4f7bc7e1e6191c81006530ca5204ef81e79ddb4403dbc790bedd77865cec28a

src/global_anchor_cube_cover.py
SHA-256 c4c7826e1a5fdde3abf9c6385ab651dd4984c29a91366e57464dba02c78ffcc7

verify/global_anchor_cube_cover_check.py
SHA-256 12da82e7b032ad2475abc3873f6010b3abb9dc13b37119d12801bc64117ffb69

tests/global_anchor_cube_cover_tests.py
SHA-256 5a67273de8f832bea010074115b263c7ce809ea51e9e8eb99029887cf0c6c1d2
```

## Derived local bounds not encoded

The root partition implies internal-degree intervals

\[
0\le d_A\le13,\qquad 10\le d_B\le17.
\]

For \(a\in A\), its `A`-neighbors contain neither a triangle nor an
independent five-set, giving the upper bound 13. The lower bound from the
complementary internal argument is zero. For \(b\in B\), its `B`-neighbors
contain neither a four-clique nor an independent four-set, giving the upper
bound 17. Its `B`-nonneighbors contain neither a five-clique nor an
independent triple, so there are at most 13; since `B` has 24 vertices this
gives the lower bound \(23-13=10\). These redundant constraints are recorded
in the plan but are not encoded in the lean union.

## Reproduction

Generate the plan:

```bash
PYTHONPATH=src python3 src/global_anchor_degree18_extension.py \
  --plan results/benchmark_plans/global_anchor_degree18_extension_v1.json
```

Independently check the plan:

```bash
python3 verify/global_anchor_degree18_extension_check.py \
  --plan results/benchmark_plans/global_anchor_degree18_extension_v1.json \
  --base-cnf certificates/direct_ramsey43.cnf \
  --base-metadata certificates/direct_ramsey43.metadata.json \
  --parent-v1-plan results/benchmark_plans/global_anchor_cube_cover_v1.json
```

Generate and check a working union formula:

```bash
PYTHONPATH=src python3 src/global_anchor_degree18_extension.py \
  --base-cnf certificates/direct_ramsey43.cnf \
  --output /tmp/ramsey55_global_anchor_d18_extension.cnf \
  --metadata results/global_exact/global_anchor_d18_extension.metadata.json

python3 verify/global_anchor_degree18_extension_check.py \
  --plan results/benchmark_plans/global_anchor_degree18_extension_v1.json \
  --base-cnf certificates/direct_ramsey43.cnf \
  --base-metadata certificates/direct_ramsey43.metadata.json \
  --parent-v1-plan results/benchmark_plans/global_anchor_cube_cover_v1.json \
  --union-cnf /tmp/ramsey55_global_anchor_d18_extension.cnf \
  --union-metadata results/global_exact/global_anchor_d18_extension.metadata.json
```

Run the focused tests:

```bash
PYTHONPATH=src python3 -m unittest -v \
  tests/global_anchor_degree18_extension_tests.py
```
