# Hostile pre-production review: one-edge-toggle engine

## Verdict

**ACCEPT FOR PRODUCTION LAUNCH.**

The mathematical origin stream, toggle semantics, candidate predicate,
dual one-guard computations, complement direction, canonical deduplication,
transactional resume logic, and repaired path separation passed the checks
below.  The initially rejected engine omitted its derived per-seed checkpoint
namespace from path validation.  The repaired engine derives every per-seed
path through the same helpers used by the writer, rejects direct, nested, and
symlink-resolved collisions, and rejects the exact database-overwrite
assignment before creating any output.  No high- or medium-severity finding
remains in this review scope.

This is a pre-run review.  It neither launches nor reports the full
25,641-origin production search.

## Reviewed snapshot

Final re-review time: 2026-07-25 15:38 PDT.

| Artifact | SHA-256 |
|---|---|
| `src/search/edge_toggle_killtest.py` | `f1fdcb6f61426920e347aa81d64ea9e95dbae094956762cf42bbc637cb3f4336` |
| `tests/test_edge_toggle_killtest.py` | `710b4fc702a48a28cbc5c1a4cee8984fff05ea7e4d238877836d3e1555953db5` |
| `math/edge_toggle_search_scope.md` | `15b12a52563eac14b09f73f8fecdac9ff05ebc4ca060ff3324da1c0f2ce8e1c1` |
| `src/search/extension_killtest.py` | `44c6db503a41def3074099cfedd098ba3138cfc22b6cf12676c57c2081f1295d` |
| `src/verifier_a/core.py` | `f43860bb3048b39f6cb99aba75b60cdfe7c77e0dc1c0489c17851b061fd91af1` |
| `src/verifier_b/graph.py` | `12b77a569e16eb8d7aa94ecb0f37800944effb7e9d8b73814adc1ec9a1777237` |
| `src/verifier_b/invariants.py` | `6dc2ce5544bfa364a3381e06e91c15864aca6dfd693978e177f8921df432258e` |
| `src/verifier_b/eternal.py` | `cdb8b053416e74e8508d9c3b4e0a373c0b7c68ecbdac9a512b50803295c322d2` |
| immutable unique seed table | `e7f0ffa459d74a67a3a647e19ee5669652ff1679302b3b62daaef299ee02945e` |
| immutable extension coverage audit | `523b3a57ef9afac2b8c921564afcf3fcd8fdbe7719984014f3b0f8e80da8e7cb` |
| pinned `labelg` executable | `ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0` |

The engine, test, and scope files were untracked in the shared worktree at
re-review time.  A production checkpoint must bind exactly the post-repair
hashes in this table.

## Findings

### H1 — CLOSED: derived seed-checkpoint namespace omitted from validation

Original severity: **HIGH** for the general API and its artifact-integrity
claim.  Final status: **CLOSED**.

`_write_seed_checkpoint` writes

```text
<checkpoint parent>/<checkpoint stem>.seeds/<seed id>.json
```

The rejected snapshot checked only the explicit `checkpoint_path`.  Its
derived directory and 391 derived files were not compared with the database,
candidate directory, exported CSVs, trusted inputs, or runtime sources.

For example, the rejected validator accepted:

```text
checkpoint_path = /tmp/run.json
database_path   = /tmp/run.seeds/ET-0001.json
```

A bounded ET-0001 probe then returned `selected_seeds_complete` after 55
origins, while the file at `database_path` began with
`{\n  "canonical_s` rather than the SQLite header.  The atomic seed-checkpoint
write had replaced the on-disk database pathname with JSON while SQLite still
held the unlinked database open.  The validator also accepted the derived
directory as `candidate_directory`, and accepted a derived seed JSON path as
`provenance_output`.

The repair meets all five requested conditions:

1. `seed_checkpoint_directory` and `seed_checkpoint_path` are the sole
   derivation helpers, and `_write_seed_checkpoint` calls the latter;
2. validation resolves the derived directory and all 391 exact seed targets;
3. a shared `_paths_overlap` predicate rejects equality and both
   ancestor/descendant directions against every writable role, the candidate
   directory, trusted inputs, and runtime sources;
4. regression tests cover database, provenance, unique-output, candidate
   directory, nesting, whole-directory symlinks, and individual-seed
   symlinks;
5. the exact former overwrite assignment now raises before either the
   database or main checkpoint exists.

The hostile re-run additionally rejected nine direct, nested, and
symlink-resolved collision patterns.  The ordered rejection-matrix digest was
`637a6229d7a35fb58fa07988632f6df3c7b0cb809b1b0abe2c71ccbd8c54ef10`.
A safe completed ET-0001 run retained a valid SQLite header and wrote its seed
JSON at the helper-derived path with the expected stream digest
`d0f0110de48e5335c032f14f0886356d7be611a817d7d8f710363fbf77926f46`.

### L1 — formulate a finite result as a connected result

Severity: **LOW**, result-wording only.

The engine deliberately records a disconnected toggle as `disconnected` and
does not compute its parameters.  This is consistent with the campaign's
proved connected reduction and its instruction to search connected graphs.
It does not, by itself, establish that each disconnected toggled graph fails
the numerical counterexample predicate.  A post-run claim should therefore
say “no connected counterexample occurs among the toggles” unless it also
invokes the already established order-at-most-11 result componentwise or
independently evaluates the disconnected cases.

### I1 — independent seed-evaluation audit remains an external launch gate

Severity: **INFORMATIONAL**, not an engine defect.

The loader byte-binds the unique extension table and checks the stored
`gamma=alpha=3`, dual `eternal=0` fields.  The coverage audit bound by the
loader certifies origin/canonical coverage and stored-row consistency; it does
not independently recompute those mathematical values.  The campaign's
separately written evaluation checker should pass on all 391 selected rows
before this lane is promoted to a certificate-backed result.

## Checks that passed

### Exact universe and toggle semantics

An independent CSV reader and the separately implemented strict graph6 parser
found:

- 54,216 distinct canonical rows;
- 391 selected rows: 285
  `eternal_false_without_private_obstruction` and 106
  `private_obstruction_eternal_false`;
- 15 rows of order 11 and 376 rows of order 12;
- exactly
  \(15\binom{11}{2}+376\binom{12}{2}=25,641\) raw origins.

All 391 selected records round-tripped in strict graph6, matched stored order
and size, and were connected.  Their structural digest was
`55298c6ea7d8af57cfc3acd57c914efb1d5cec0054b6f2004491fcde659909fb`.

For every one of the 25,641 pairs, an independent edge-set implementation
agreed byte-for-byte with the engine's raw graph6.  Every result differed from
its seed in exactly the requested unordered pair.  There were 10,959 additions
and 14,682 deletions.  The ordered origin-semantics digest was
`bc91d5805a3d81dbc153cd063ab8df13e1f5272a4938750481ef6e05ca928b4c`.

### Canonicalization, deduplication, and multiplicity

Pinned `labelg` was checked at the expected executable and archive hashes.
For the first, middle, and last pair of every seed (1,173 origins), an
independent backtracking isomorphism checker verified each raw/canonical pair,
including the returned relabeling.  The sample produced 1,121 canonical keys;
the mapping-receipt digest was
`733f2a82ca12f7d6c2266ea33f4195b4e79838fce03313732c7ffba1d8020d03`.

A bounded two-seed ledger run produced 110 origins and 73 canonical keys.  It
had 17 collision keys, maximum multiplicity 5, total stored multiplicity 110,
and no row/count disagreement.  The ordered multiplicity digest was
`63c40b63351aec9b721d373415b73628724a1f8b326d8aa09beb8b5694846bb6`.

A separate completed ET-0001 ledger probe verified all 55 lexicographic pair
indices, actions, raw reconstructions, raw/canonical isomorphisms, A/B stored
equalities, parameter chains, and the seed stream hash
`d0f0110de48e5335c032f14f0886356d7be611a817d7d8f710363fbf77926f46`.

### Exact parameters and model

Source inspection confirmed in both independent stacks:

- attacks range only over vertices outside the current configuration;
- exactly one occupied guard is removed and the attacked adjacent vertex is
  inserted;
- only one-edge moves are generated;
- successor configurations must belong to the precomputed set of dominating
  configurations;
- the terminal object is the greatest family closed for every attack;
- generated winning families are checked again directly from the definition.

Verifier A computes clique partitions directly in \(G\).  Verifier B colors
the complement.  On all 728 connected labeled graphs of order 5, both stacks
agreed on `gamma`, `alpha`, `gamma_infinity`, and `theta`; an independent
clique-partition recursion also agreed on `theta`.  Every graph satisfied
`gamma <= alpha <= gamma_infinity <= theta`, and the stored category was
exactly the logical branch implied by those values.  The ordered result digest
was `dd5e5712cf5dddbf337027cbd735721ff14077bae1fda63166dc1776b97583b6`.

This validates the complement direction and the candidate condition
`gamma == gamma_infinity < theta`; it does not replace the larger campaign
regression record or the post-run independent evaluation checker.

### Transaction and candidate interruption audit

The authoritative progress tuple `(origins, next_pair_index, stream hash,
status)` is advanced inside the same SQLite transaction as canonical
evaluation and multiplicity.  Canonicalization occurs before that
transaction, so a failure there advances nothing.  Completion status and the
terminal stream hash commit together.  Atomic JSON checkpoints and CSV
exports are mirrors that can be regenerated from the ledger.

An initially suspected orphan-candidate defect was **retracted after an
explicit commit-point trace**.  The candidate JSON is written before the
batch transaction commits, but a failure after that write rolls back both its
origin and `next_pair_index`.  Resume therefore replays the same pair before
any later graph.  A fault-injection probe raised immediately after the
candidate file was written; the database remained at `(0 origins, next=0,
empty marker)`.  With the same deterministic evaluator on resume, the engine
reused the artifact, committed `(1 origin, next=1, marker path)`, and returned
`candidate_review_pending`.

If the transaction has committed, the redundant metadata marker, canonical
candidate category, and provenance candidate category each block resume.
The existing tests also verified marker-only and row-only interruption
states.  There is no continuation override.

### Limits, gates, and source binding

The CLI refuses to run without `--validation-gate-open`.  Batch size and
per-process limits reject Booleans, non-integers where applicable, NaN,
infinity, and nonpositive values before database creation.  Memory is checked
at each committed batch; wall time is checked at each batch and honored after
the current seed, whose maximum remaining raw work is 66 toggles.  The
production implementation is deterministic and single-process.

Configuration binding covers both immutable inputs, the pinned executable and
nauty archive, Python implementation/version/executable, all imported search
and evaluator sources, batch size, selected-seed tuple, limits, and schema
version.  Resume with a different configuration digest fails before progress.
Production should still be launched from a frozen commit with no concurrent
edits to those source files.

## Test record

The repaired unit module passed 15/15 tests under:

```text
PYTHONPATH=src PYTHONWARNINGS=error python3 -m unittest -v \
  tests.test_edge_toggle_killtest
```

The complete campaign suite also passed 140/140 tests under:

```text
PYTHONPATH=src PYTHONWARNINGS=error python3 -m unittest discover -s tests -v
```

Additional hostile probes performed:

1. independent exact seed/category/order/pair count;
2. independent reconstruction of all 25,641 raw toggles;
3. 1,173 independent raw/canonical isomorphism receipts;
4. complete two-seed dedup/multiplicity ledger audit;
5. all 728 connected labeled order-5 parameter/category comparisons;
6. candidate fault after frozen-file write followed by deterministic replay;
7. the original accepted path collisions and actual database-path replacement
   that demonstrated H1;
8. the exact former overwrite assignment rejected before output creation;
9. a nine-case direct/nested/symlink collision matrix, all rejected;
10. a safe completed-seed writer probe confirming the database remains SQLite
    and the writer uses the same helper-derived path;
11. post-repair reconstruction of all 25,641 origins, reproducing the exact
    pre-repair digest;
12. post-repair candidate fault/replay and all 728 connected labeled order-5
    parameter/category checks, reproducing their prior outcomes and digests.

No full production search was launched.
