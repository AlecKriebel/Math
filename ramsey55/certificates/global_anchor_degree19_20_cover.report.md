# Exact Ramsey-anchor cover of global degree branches 19 and 20

Date: 2026-07-23 (America/Los_Angeles)

## Outcome and evidence boundary

**CERTIFIED DECOMPOSITION, NOT A SOLVE.** The normalized global degree-19
and degree-20 branches now have an independently checked exact cover by 143
anchor-matrix cubes each. The same cover is represented compactly by one
selector-union CNF per degree. Both materialized union formulas were checked
clause-for-clause against the audited global CNF and the independently
reconstructed additions.

The bounded solver pilots exhausted every conflict budget. They produced no
SAT model, UNSAT determination, DRAT, or LRAT proof. Consequently neither
degree branch is excluded, no order-43 construction was found, and no Ramsey
bound changes.

## Exact cover argument

Start with a model in normalized branch \(d\in\{19,20\}\). Let the root be
\(v=0\), let

\[
A=N(v),\qquad B=V\setminus(A\cup\{v\}).
\]

Thus \(|A|=d\) and \(|B|=42-d\).

1. `G[A]` contains no \(K_4\), because such a \(K_4\) together with the root
   would form a \(K_5\). Since \(|A|\ge19>17\) and \(R(4,4)=18\), `G[A]`
   contains an independent four-set.
2. `G[B]` contains no independent four-set, because it would extend with the
   root to an independent five-set. Since \(|B|\ge22>17\), \(R(4,4)=18\)
   forces a four-clique in `G[B]`.
3. Relabel one independent four-set to the first four vertices of `A`, and
   one four-clique to the first four vertices of `B`.
4. Consider the \(4\times4\) cross-adjacency matrix between these anchors.
   It has no all-one row: such a row vertex together with the `B`-anchor
   \(K_4\) would form a \(K_5\). It has no all-zero column: such a column
   vertex together with the `A`-anchor \(I_4\) would form an \(I_5\).
5. Exactly 35,714 of the 65,536 binary matrices satisfy those two conditions.
   Independent row and column permutations form an \(S_4\times S_4\) action.
   Exact orbit enumeration gives 143 orbits. Relabel the two anchors so that
   their matrix is the minimum integer in its orbit.

This proves that every graph in either original branch is isomorphic to a
model of one of the 143 cubes. Conversely, every cube only adds units to the
original branch formula. The cover can overlap because a graph may have
multiple eligible anchors; disjointness is unnecessary.

The union encoding adds 143 selector variables. One clause requires at least
one selector, and each selector implies the 16 literals of its canonical
matrix. This is an exact compact representation of the 143-cube union.

## Secondary witness and ordering symmetries

Two further relabeling reductions are included in each union CNF.

- `G[A]` contains a triangle by \(R(3,5)=14\) and the absence of an
  independent five-set. A triangle meets the anchored \(I_4\) in zero or one
  vertex. Five selectors cover the disjoint case and the four possible
  one-vertex intersections.
- `G[B]` contains an independent triple by the complementary
  \(R(3,5)=14\) statement and the absence of a \(K_5\). Five analogous
  selectors cover its intersection with the anchored \(K_4\).

After reserving three non-anchor labels on each side for those witnesses, all
remaining vertices within each side are freely permutable. Their eight-bit
incidence vectors to the two four-vertex anchors are therefore sorted
lexicographically. The encoding uses 26 adjacent vector comparators and
6,630 primary-only clauses. The independent checker exhaustively verified
the comparator template for every pair of binary vectors at widths one
through eight.

## Independent cover and formula checks

The checker does not import the production cover generator. It independently
reconstructs:

- the 903 primary edge variables;
- the direct formula's 64,500 counter-variable layout and the 128 exact
  degree-branch assumptions;
- all 65,536 cross matrices, their feasibility test, and the
  \(S_4\times S_4\) action;
- all 286 cube assumption streams;
- the selector and witness clauses;
- the primary-only lexicographic comparator clauses; and
- the optional internal-degree counters described below.

It found exactly 35,714 feasible matrices, exactly 143 orbit representatives,
zero malformed cubes, and an exact orbit partition. The plan check is valid.

```text
plan:
results/benchmark_plans/global_anchor_cube_cover_v1.json
SHA-256 c4f7bc7e1e6191c81006530ca5204ef81e79ddb4403dbc790bedd77865cec28a

plan check:
results/verification/global_anchor_cube_cover_v1.check.json
SHA-256 ad3355a578e5688f07706e923d8265db801b96816506960edcddff6ea54eedab
```

For each materialized union formula, the streaming checker verified all
2,052,132 copied base clauses in order, followed by exactly the expected
9,091 additions.

| branch | variables | clauses | checked CNF SHA-256 | formula check |
|---:|---:|---:|---|---|
| 19 | 65,556 | 2,061,223 | `7540802b0e2b85256e85ed1a67ba6a9ca1736d703a025201ee8a2244c7c10ae8` | valid |
| 20 | 65,556 | 2,061,223 | `19f7d3a00ce8b491627cc063cb7b9584fce6619ca94416ada5926a19cf7ea7f6` | valid |

The materialized CNFs are deterministic working files rather than
certificates. Their metadata and checks preserve the exact expected hashes.

## Sound optional local-degree constraints

The root partition also gives the following internal-degree intervals:

| branch | vertices in `A` | \(d_A\) | vertices in `B` | \(d_B\) |
|---:|---:|---:|---:|---:|
| 19 | 19 | 1--13 | 23 | 9--17 |
| 20 | 20 | 2--13 | 22 | 8--17 |

For \(a\in A\), its neighbors inside `A` contain neither a triangle nor an
independent five-set, so there are at most 13 by \(R(3,5)=14\). Its
nonneighbors inside `A` contain neither a \(K_4\) nor an \(I_4\), so there
are at most 17 by \(R(4,4)=18\).

For \(b\in B\), its neighbors inside `B` contain neither a \(K_4\) nor an
\(I_4\), so there are at most 17. Its nonneighbors inside `B` contain neither
a \(K_5\) nor an \(I_3\), so there are at most 13 by
\(R(5,3)=R(3,5)=14\).

An optional 84-counter formula encodes these redundant exact consequences.
Both strengthened formulas passed the same independent clause-stream check.
They were slower in the matched 50,000-conflict pilot, so the lean formulas
remain the preferred proof targets.

## Matched bounded solver pilot

All jobs used MapleChrono from python-sat 1.9.dev7 with 50,000 conflicts and
no proof logging.

| branch | encoding | solver CPU s | wall s | propagations | status |
|---:|---|---:|---:|---:|---|
| 19 | exact branch baseline | 9.393 | 11.658 | 42,092,207 | budget exhausted |
| 19 | lean anchor union | 1.890 | 3.621 | 11,336,992 | budget exhausted |
| 19 | anchor union + local counters | 3.611 | 5.405 | 28,544,806 | budget exhausted |
| 20 | exact branch baseline | 8.958 | 11.466 | 42,576,449 | budget exhausted |
| 20 | lean anchor union | 2.291 | 4.017 | 17,279,825 | budget exhausted |
| 20 | anchor union + local counters | 7.809 | 12.900 | 33,483,908 | budget exhausted |

At equal conflict count, the lean union reduced solver CPU by factors 4.97
and 3.91 for branches 19 and 20 respectively. This is engineering evidence,
not evidence that either formula is UNSAT.

The aggregate pilot record is
`results/global_exact/global_anchor_union_pilot_v1.json`.

## Source-dependent side edge ranges

The public `r45extreme.tar.gz` archive was streamed and pinned at SHA-256
`9cfac9dbd1c209cfa342e5d5424df2a7a3fbb008ca00bf0a992e5bbe72f925b6`.
The source describes its low- and high-edge files as complete at the
smallest and largest few edge counts. This gives the following useful
source-dependent ranges:

| branch | \(e(G[A])\) | \(e(G[B])\) |
|---:|---:|---:|
| 19 | 57--92 | 131--152 |
| 20 | 68--100 | 117--143 |

The `B` ranges use complementation of Ramsey(4,5) graphs on 23 and 22
vertices. Local hashes, byte counts, record counts, and complement arithmetic
are recorded in
`results/verification/r45_extreme_root_side_source_audit_v1.json`.
The endpoint completeness claim was not independently re-enumerated here,
so these ranges are not built into the preferred certified formula.

## Certificate architecture

There are two exact routes to close these branches.

1. **Preferred:** generate and independently check one lean selector-union
   CNF for branch 19 and one for branch 20. A proof-producing solver must
   return UNSAT for each, `drat-trim` must accept each trace and emit LRAT,
   and `lrat-check` must accept each LRAT against its exact checked CNF.
2. **Cube bundle:** materialize all 143 cubes per branch from the plan's
   assumption hashes. Check every cube CNF and every proof, then validate a
   manifest covering all 143 representatives for each branch.

A SAT result on either route must be replayed as a 43-vertex graph and passed
through both independent Ramsey verifiers. UNSAT of these two branches alone
would still leave the separately handled degree-18 branch.

## Reproduction

Generate the plan:

```bash
PYTHONPATH=src python3 src/global_anchor_cube_cover.py \
  --plan results/benchmark_plans/global_anchor_cube_cover_v1.json
```

Generate the preferred branch-20 formula:

```bash
PYTHONPATH=src python3 src/global_anchor_cube_cover.py \
  --base-cnf certificates/direct_ramsey43.cnf \
  --degree 20 \
  --output /tmp/ramsey55_global_anchor_d20.cnf \
  --metadata results/global_exact/global_anchor_d20.metadata.json
```

Add `--local-degree-counters` only to reproduce the optional strengthened
variant.

Independently check the plan and materialized formula:

```bash
python3 verify/global_anchor_cube_cover_check.py \
  --plan results/benchmark_plans/global_anchor_cube_cover_v1.json \
  --base-cnf certificates/direct_ramsey43.cnf \
  --base-metadata certificates/direct_ramsey43.metadata.json \
  --union-degree 20 \
  --union-cnf /tmp/ramsey55_global_anchor_d20.cnf \
  --union-metadata results/global_exact/global_anchor_d20.metadata.json
```

Run the implementation tests:

```bash
PYTHONPATH=src python3 -m unittest -v \
  tests/global_anchor_cube_cover_tests.py
```

Six tests pass.
