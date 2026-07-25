# Hostile review: third edge-toggle mathematical audit

Date: 2026-07-25 16:20 PDT

## Verdict

**ACCEPTED for the stated finite scope.**

The installed certificate and checker rigorously establish

\[
  \gamma(G)<\gamma^\infty(G)
\]

for every one of the 19,136 distinct graph6 keys in the completed edge-toggle
ledger.  The separately bound coverage report accounts for all 25,641 labeled
toggle origins from the 391 accepted extension seeds.  Consequently none of
the graphs in this precisely delimited edge-toggle universe is a
\(\gamma=\gamma^\infty<\theta\) counterexample.

This is not an enumeration of all graphs of order 11 or 12 and is not a
resolution of the universal conjecture.

Severity census:

| Severity | Count | Disposition |
|---|---:|---|
| Critical | 0 | none |
| High | 0 | none |
| Medium | 0 | none |
| Low | 2 | non-mathematical metadata/portability notes below |

No critical, high, or medium defect was found.

## Frozen artifacts

| Artifact | SHA-256 |
|---|---|
| `results/edge_toggle_third_evaluation_certificates.ndjson` | `b31eee468a8a45e0534fece7b54cb142ff126fb1f9155db5bbea98acaa948435` |
| `results/edge_toggle_third_evaluation_audit.json` | `8877262c2ece90448106630b7e71909f3e39e4887f2455b5d1f089db1346b809` |
| `results/edge_toggle_coverage_audit.json` | `82c6918faec2105340205730a3e128d4be05b5c57190a58519e68b4cfe733679` |
| `results/checkpoints/edge_toggles.sqlite3` | `2a6349452906cf2904a5e9e6284806f603619ad28ec66fa63fc383f2b833b258` |
| `results/checkpoints/edge_toggles.json` | `f00b404fdfc09ac95f8b56325ef58a3399559b33eb1b659e304fdc81ed512ffc` |
| `results/edge_toggles_provenance.csv` | `378e867d5ec0d419f668f5169dbac6f2319cd2afc9ce3c5f63da2b9677dccba5` |
| `results/edge_toggles_unique.csv` | `a32505df6ba67479b5908a91711d21babb14fd8ac50cdfd0f0b92fc1001d4319` |
| reused strict graph6 parser | `cb60b10295aaa1e0a723e9fb3b1ecf497c461082bdcc8066044a664b4d76e731` |
| checker source set | `b2ba9d7a5e549e4da88542badf2d9948a54571dad925ad7f30ef89118574d76d` |
| certificate input/source binding | `b1a1fc061d973db9f90830427d0d7905b135f507abdb827afd7907abe52ea2de` |
| bound coverage binding | `e5d78a868397589e11cf87ed5e248d6ee03bde452c01b7fc3d260f2999b181d9` |
| bound origin chain | `d00dff4e6e0ad40b37e14da89c5deb2616ed10e39b08c81b1d5837723df1f5bb` |
| certificate row stream | `fc929585dd5b9096dc9dca262093d2fc4f02e5784fc66f0e8ab39ec5f23336a3` |
| hostile independent probe | `7f495b8c0f5abd726b2329a45936811f76cee5de854ce1b4204639f36b7a4cac` |
| hostile mutation probe | `2088ae73ebff6a56d9c6ef28a326e9687ac3e27b4fed6321065894dfc13fa920` |

The two hostile-probe hashes above are the hashes at the time this review was
written.

## Independent full mathematical replay

`reviews/edge_toggle_math_hostile_probe.py` imports no campaign module.  It
uses:

- a fresh strict graph6 decoder and encoder;
- adjacency as tuples of `frozenset` neighbors rather than bit rows;
- ordinary `frozenset` guard configurations rather than integer
  configurations;
- a fresh domination scan over Python combinations; and
- a fresh greatest-fixed-point computation using set subtraction and
  replacement of one set element.

It independently checked every ledger row, not a sample.  Its output was:

```text
status: accepted
rows: 19136
origins: 25641
wall_seconds: 19.81438425
certificate_sha256:
  b31eee468a8a45e0534fece7b54cb142ff126fb1f9155db5bbea98acaa948435
report_sha256:
  8877262c2ece90448106630b7e71909f3e39e4887f2455b5d1f089db1346b809
row_stream_sha256:
  fc929585dd5b9096dc9dca262093d2fc4f02e5784fc66f0e8ab39ec5f23336a3
```

Measured real time was 19.87 seconds and maximum resident set size was
35,848,192 bytes.

For every graph the hostile probe reproduced exactly:

- the independent value \(\gamma\);
- the explicit upper-bound dominating set;
- the exhaustive \((\gamma-1)\)-set blocker list;
- the complete initial family of dominating \(\gamma\)-sets;
- every simultaneous deletion round and first failing attack;
- the empty terminal fixed point; and
- the per-row, row-stream, footer, report, source, input, and coverage
  bindings.

The independently reproduced aggregate is:

| Quantity | Value |
|---|---:|
| rows | 19,136 |
| origins represented | 25,641 |
| rows with \(\gamma=2\) | 7,934 |
| rows with \(\gamma=3\) | 11,202 |
| initial dominating configurations | 1,235,981 |
| deletion records | 1,235,981 |
| simultaneous deletion rounds | 37,552 |
| maximum initial configurations for one graph | 156 |
| maximum deletion rounds for one graph | 7 |

Independent SQLite checks also found 19,136 distinct graph6 primary keys,
exactly 25,641 distinct `(seed_id,pair_index)` origin keys, 472 order-11 keys,
18,664 order-12 keys, and no category other than
`gamma_below_eternal`.

## Mathematical audit

### Domination

For a certified value \(k\in\{2,3\}\), the verifier checks an explicit
dominating \(k\)-set.  It then requires one record for every
\((k-1)\)-subset in exact lexicographic combination order.  Each record
contains a vertex outside that subset with no neighbor in it.  Thus no
\((k-1)\)-set dominates.  By monotonicity of domination, no smaller set
dominates either.  This proves \(\gamma(G)=k\), rather than merely
\(\gamma(G)\le k\).

The hostile probe reconstructed this proof from the graph on all 19,136 rows.
The independently obtained value was compared with both stored gamma fields.

### One-guard movement model

The audited transition is exactly

\[
  D'=(D-\{u\})\cup\{r\},
  \qquad u\in D\cap N(r),\quad r\notin D.
\]

The code explicitly skips occupied attacks.  Candidate moved guards are the
single bits in `configuration & graph.neighbors[attacked]`.  The successor
expression removes that one bit and adds the attacked bit.  Because the
attack is unoccupied, exactly one occupant changes.  Both generation and
replay require the successor to have \(k\) occupants, dominate the graph, and
belong to the current active family.

There is no all-guards move, distance move, occupied-vertex attack, total
domination condition, or complement graph in this computation.

### Greatest fixed point

The initial active family is recomputed as **all** dominating ordinary
\(k\)-subsets.  In each round the implementation freezes the current family
before testing any configuration.  A configuration is doomed exactly when
some unoccupied attacked vertex has no legal one-guard successor in that
frozen family.  Every doomed configuration, with its first failing attack, is
recorded.  Deletion occurs only after the complete round is constructed.

The replay implementation does not call the generator's response predicate.
It reconstructs the complete doomed set and requires exact ordered equality
with the supplied round.  It then requires an empty terminal family.  There
are exactly 1,235,981 deletion records for 1,235,981 initial configurations.

This is the descending iteration of the monotone defense operator on the
finite set of dominating \(k\)-configurations.  Its limit is the greatest
fixed point.  Any eternal family of size \(k\) would be a nonempty post-fixed
subset and hence would survive this iteration.  The empty limit therefore
proves \(\gamma^\infty(G)>k=\gamma(G)\).

### Ledger binding, order, and uniqueness

The SQLite database is opened read-only and immutable after rejection of
WAL, shared-memory, and rollback-journal companions.  Integrity and
foreign-key checks pass.  The actual schema has `graph6` as the primary key
of `canonical_graphs` and `(seed_id,pair_index)` as the primary key of
`origins`.

Rows are read in `(n,graph6)` order.  The unique CSV must match every typed
SQLite field literally and have no shorter or longer stream.  The certificate
row records its index, graph6 string, and SHA-256 of the canonical JSON
encoding of the complete typed database row.  The hostile probe additionally
required strict increase of `(n,graph6)` and independently counted distinct
keys.

The graph6 record is strict ASCII, must use the ordinary short order form,
must have exact payload length and zero padding, and must re-encode
byte-for-byte.  The reused parser is frozen by its explicit SHA-256.  The
hostile probe's unrelated decoder agreed on every graph, order, size,
connectedness, and re-encoding.

### Coverage and candidate logic

The mathematical certificate binds the exact coverage report by its full file
hash, binding digest, and origin-chain digest.  It also checks that the
coverage report binds the exact search database, checkpoint, provenance CSV,
and unique CSV.  The coverage report records 25,641 verified origins and
19,136 graph6 keys.

The mathematical conclusion does not trust the stored exact
\(\gamma^\infty\) value: the empty fixed point independently proves the
strict inequality.  It nevertheless requires both stored eternal values to
agree, to exceed the independently proved gamma, and the category to be
`gamma_below_eternal`.  Since strict inequality
\(\gamma<\gamma^\infty\) alone excludes
\(\gamma=\gamma^\infty<\theta\), no independent alpha or theta proof is
needed for this negative finite result.  The report correctly says that its
stored alpha, theta, and exact eternal values are reconciliation data only.

The search checkpoint is complete, represents all 25,641 expected origins,
has no pending candidate, and has a null candidate reference.

## Production replay and tests

The production replay command

```text
PYTHONPATH=src python3 -m edge_toggle_evaluation_checker --verify-only
```

completed successfully:

```text
status: complete
mode: verify-only
rows: 19136
replay_seconds: 11.445935458003078
certificate_sha256:
  b31eee468a8a45e0534fece7b54cb142ff126fb1f9155db5bbea98acaa948435
```

Measured real time was 11.58 seconds and maximum resident set size was
37,355,520 bytes.

All 17 targeted unit and differential tests passed in 0.927 seconds.  They
include exhaustive differential testing of every graph through order four,
random order-six differential tests, C5/C7 proof cases, a nonempty fixed
point rejection, parser/source pin checks, and certificate tampering.

## Adversarial mutations

`reviews/edge_toggle_math_hostile_mutations.py` made 13 mutations.  All 13
decisive mutations were rejected:

1. remove one deletion from a simultaneous round and repair the trace hash;
2. replace a failing attack by an occupied vertex and repair the trace hash;
3. move a deletion to a later round and repair the trace hash;
4. remove the terminal round and repair the trace hash;
5. replace a lower-bound blocker by an occupied witness;
6. replace the domination upper witness by the empty set;
7. label a proved strict-inequality row as an eternal candidate;
8. make the stored eternal value no larger than gamma;
9. duplicate a JSON key;
10. inject a non-finite JSON value;
11. present a semantic mutation in canonical NDJSON;
12. truncate the NDJSON stream after its first row; and
13. append a byte after an otherwise valid footer.

The repaired hashes in mutations 1--4 ensure that rejection came from the
mathematical replay, not merely from a stale trace digest.  The trailing-byte
test necessarily replayed the full certificate.  The mutation suite completed
in 11.664 seconds (11.72 seconds real) with maximum resident set size
36,798,464 bytes.

## Low-severity notes

### L1: runtime-only report metadata is not replay-validated

`_validate_existing_report` compares the decisive report core, binding,
certificate hash, model, limitations, and mathematical summary.  It does not
reject unknown extra keys and does not validate generation-only fields such
as `wall_seconds`, `started_unix`, or `resource_usage`.  A hostile test changed
`wall_seconds` to zero and added an unknown key; the private report validator
accepted those nondecisive changes.

This cannot alter any mathematical result, input/source binding, certificate
hash, or summary.  The full report hash above and the repository manifest can
anchor the operational metadata.  A future revision may use an exact report
key set and validate the types/ranges of generation metadata if those fields
are intended to be independently certified.

### L2: absolute-path binding is not relocation-friendly

The checkpoint and certificate binding contain checkout-specific absolute
paths, and the checker requires exact path equality.  This prevents a
byte-identical archived package from passing the same verify-only command
after arbitrary relocation without reconstructing the original directory.
It does not permit false acceptance in the current frozen checkout.

For a permanent public archive, add a second relocatable verifier that binds
normalized paths relative to the campaign root, or document a container path
that recreates the frozen absolute layout.  Do not alter the accepted frozen
artifacts merely to improve portability.

## Scope boundary

Accepted claim:

> Among the 25,641 labeled one-edge-toggle origins obtained from the 391
> specified extension seeds, represented by 19,136 distinct stored graph6
> keys, every graph has \(\gamma(G)<\gamma^\infty(G)\).  Hence this finite
> universe contains no counterexample to the gamma--theta conjecture.

Not established:

- nonexistence of a counterexample among all order-11 or order-12 graphs;
- correctness of stored exact alpha or theta values by this checker;
- a universal graph-class theorem; or
- resolution of the gamma--theta conjecture.
