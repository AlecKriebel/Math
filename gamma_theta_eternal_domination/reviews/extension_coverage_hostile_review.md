# Hostile review: frozen extension-coverage checker and production audit

## Verdict

**ACCEPTED as a sound coverage and canonicalization certificate for the
precisely delimited 110,537-origin one-vertex-extension ledger, with one
low-severity operational qualification.**

No critical-, high-, or medium-severity correctness defect was found.  The
production report's `complete` status is supported by an independently
recomputed host-mask universe, exact reconstruction of every raw extension,
direct verification of every stored raw-to-canonical permutation, exact
multiplicities and first origins, a matching 110,537-step receipt chain, and
byte-for-byte export and hash checks.

This verdict certifies **coverage**, not the stored graph-parameter
evaluations.  It must be combined with the separate independent evaluation
audit before the empty extension run can support a finite negative theorem.
It does not resolve the universal \(\gamma\)--\(\theta\) conjecture.

Review date: 2026-07-25.

Reviewed frozen checker SHA-256 digests:

- `src/coverage_checker/__init__.py`:
  `6417882e5f766f82da521bf14b1eca2f0bcf5e22d886077ace980d07a1edcf28`;
- `src/coverage_checker/graph.py`:
  `cb60b10295aaa1e0a723e9fb3b1ecf497c461082bdcc8066044a664b4d76e731`;
- `src/coverage_checker/catalog.py`:
  `bf1baa96b74bb9ecec2b447ac307101a81700083d7fbfc595daa09f8772894ba`;
- `src/coverage_checker/audit.py`:
  `7515e9df658a3d63298242bfa4e6cfbdb167e088e47de5776ef6c01b7a4f9b64`;
- `src/coverage_checker/cli.py`:
  `520e889a2250305f5e0e7b3dc10f0386ccc5322f6f0018d5cdd3f5fb2dc32562`;
- `src/coverage_checker/__main__.py`:
  `3d2438ae92f4746e9ffaa1f837b1fe803f6281091d1f31f8c95643716f257d9a`;
- `src/coverage_checker/PROTOCOL.md`:
  `473b96e20606c04a33d8f81ac0e64052cc95913ed268d5916e4bd46b0ce9ca54`;
- `reviews/extension_coverage_hostile_probe.py`:
  `9fea13d8e31b864e27451c2f6cb48bbc27a9990bb04cf966b4b444db646c6c82`.

Reviewed production SHA-256 digests:

- search database:
  `06d294195dd46ac0e75f29f176f5f40240e016b33ac56c8890d638d3085ac4b7`;
- coverage-state database:
  `01687596bd6c46974432aa06cfd14068fb8c49ea3ac39050971eeb4879818859`;
- search checkpoint:
  `2b190ec2a60585e4485af80b5dc09bd1dad2df710d33e7d3869bc269570fe6da`;
- provenance CSV:
  `0a4dfb405c812a93ee60755110a60f380f7f565f608a461ad9df2833474bd782`;
- unique-graph CSV:
  `e7f0ffa459d74a67a3a647e19ee5669652ff1679302b3b62daaef299ee02945e`;
- coverage report:
  `523b3a57ef9afac2b8c921564afcf3fcd8fdbe7719984014f3b0f8e80da8e7cb`;
- catalog:
  `801f054853d07652c795fb16217425869f857d7f5d74e427165d554faf4eae1d`;
- parameter table:
  `ef74175dfd81542a167feed5a2d7f66be723846993642fb65344d08655b594c6`.

## 1. Independent production reconstruction

The hostile probe imports no code from `coverage_checker`, the search engine,
or either campaign evaluator.  It contains a separately written strict
ordinary-graph6 codec, extension constructor, and relabeling checker.  In a
7.4-second read-only run it established:

| item | independently checked value |
|---|---:|
| selected connected hosts | 55 |
| nonempty labeled extension masks | 110,537 |
| receipt rows | 110,537 |
| distinct stored canonical keys | 54,216 |
| independently summed multiplicity | 110,537 |
| final origin-chain SHA-256 | `453cbac4d39614c557a9f9a63563b41466c1632ba7123bf3c41390115e65fbad` |

The host selection was reconstructed from the separately byte-pinned catalog
and parameter table.  It recovered the distribution

\[
 (n,\gamma,\text{count})=(10,2,2),(11,1,2),(11,2,51)
\]

and hence

\[
 2(2^{10}-1)+53(2^{11}-1)=110{,}537.
\]

For every host and every integer mask \(1,\ldots,2^n-1\), the probe added a
new vertex adjacent to exactly the mask bits and required its independently
encoded raw graph6 string to equal the ledger row.  The row order was exactly
the lexicographic `(host_index, mask)` universe; there was no missing,
duplicated, zero, reordered, or out-of-range origin.

For each origin, the probe parsed the saved receipt permutation and directly
rebuilt the relabeled adjacency matrix.  All 110,537 permutations were valid
bijections carrying the reconstructed raw graph to the stored canonical-key
graph.  This check does not trust the checker's individualization/refinement
algorithm.  A separate 2,056-record differential against the pinned nauty
2.9.3 `showg` executable also confirmed that the independent codec and the
checker use standard graph6 vertex and bit order.

The probe recomputed the receipt chain from the domain separator and every
canonical JSON payload.  Every intermediate receipt digest and the final
state/report digest agreed.  It independently accumulated multiplicities and
first origins and matched all 54,216 `canonical_counts` rows and all 54,216
search-database evaluation keys.  The category distribution was:

| stored category | unique keys | origins |
|---|---:|---:|
| `gamma_below_3` | 52,447 | 107,135 |
| `alpha_above_3` | 1,378 | 2,604 |
| `private_obstruction_eternal_false` | 106 | 194 |
| `eternal_false_without_private_obstruction` | 285 | 604 |
| **total** | **54,216** | **110,537** |

No `candidate_eternal_3` key or origin occurs.  These labels are treated here
only as ledger values; their mathematical truth belongs to the independent
evaluation audit.

## 2. Binding, exports, and immutable-input checks

The hostile probe independently canonicalized and hashed the report's audit
binding.  It matched the current absolute paths and bytes of the database,
checkpoint, catalog, parameter table, both CSVs, and every listed checker
source file.  The checker-source aggregate digest was also recomputed from
the ordered manifest.

The search checkpoint binds the same database bytes and the same two export
hashes.  Every one of the 110,537 provenance CSV rows and every one of the
54,216 unique CSV rows matched the corresponding immutable-database query,
field for field and in the specified order.  Independently recomputed
per-host canonical-stream hashes matched the database, checkpoint, and final
report.

Both SQLite databases passed `PRAGMA integrity_check`.  No WAL, shared-memory,
or rollback-journal companion was present.  The search database, coverage
state, and report each had link count one.  Hashes taken before and after all
read-only hostile probes were identical.

The report's state hash is necessarily a point-in-time binding rather than a
self-authenticating signature.  The reviewed state bytes still have exactly
that hash, and replay from a copied state reproduced the same terminal chain
and counts.

## 3. Isomorphism implementation audit

The frozen `find_isomorphism` routine is exact for its bounded input domain.
It first rejects incompatible order, size, degree multiset, component orders,
and vertex invariants.  Joint color refinement is applied to both graphs with
one shared palette.  At every nonsingleton cell it individualizes one left
vertex against every right vertex in that cell, with no branch cutoff.
When all cells are singleton, `_mapping_is_valid` compares every mapped
adjacency row before returning a witness.

Consequently a false positive cannot pass merely through a refinement
collision: the final permutation is checked literally.  A false negative
would make a valid artifact fail to certify, not make an invalid artifact
pass.  In the actual production run all origins have concrete witnesses,
and the hostile probe independently checked every one.

The existing differential tests compare the routine with brute-force
permutation search for every graph pair through order four, random pairs
through order six, adversarial regular pairs, and an order-12 relabeling.
All passed.

## 4. Resume, tamper, and path tests

A completed production state was copied to a temporary directory.  Replaying
the frozen checker against that copy, while reading the production inputs
immutably, returned `complete` with the same 110,537 count, 54,216 keys, and
final chain.  It took 297.776 seconds and peaked at 38.703 MiB RSS.  The copied
state retained the production state hash.

The first saved mapping in that copy was then replaced by a non-permutation.
The next replay exited with the checker's failure status in one second:

```text
coverage audit failed closed: stored isomorphism receipt is invalid at MMV-001/1
```

It produced no success report.  Production hashes remained unchanged.

Exact and symbolic-link aliases from the report output to the immutable
search database were each rejected before any write.  The unit fixture
additionally rejected:

- a reconstructed raw graph inconsistent with its host and mask;
- a missing middle mask;
- a nonisomorphic raw/canonical pair;
- a corrupt canonical multiplicity;
- a purported full run carrying an active host shard;
- a CSV mutation even after rebinding its checkpoint hash;
- a live SQLite companion;
- a tampered saved mapping;
- zero, boolean, nonfinite, and otherwise invalid resource controls.

The complete focused suite passed 23 of 23 tests in 0.616 seconds.

## 5. Static state and crash-consistency audit

The search database is opened with `mode=ro&immutable=1` after companion-file
rejection.  Its schema version, exact table and column sets, integrity, foreign
keys, exact three metadata keys, complete host rows, origin total, and absence
of candidate rows are checked before reconstruction.

The independent state binds hashes of every immutable input and the ordered
checker-source manifest.  A batch transaction inserts the receipt, increments
the independent multiplicity, advances the exact position, and extends the
chain together.  A crash before commit rechecks that batch; a crash after
commit resumes at the exact successor.

Resume does not trust the position and count alone.  It verifies that receipt
counts equal the progress total, that reconstructed multiplicities equal the
state counts, then streams the entire saved prefix against the immutable
ledger.  Every stored permutation and every chain step is checked again.
First-origin provenance is also shown to have a matching receipt and no
earlier receipt for the same key.

After origin completion, the independently accumulated key set is streamed
against the whole canonical table.  Extra keys, missing keys, wrong
multiplicities, or altered first origins fail.  Only after stream hashes,
exports, checkpoint summaries, and a second all-input hash comparison pass is
the state promoted to `complete` and the report atomically replaced.

## 6. Nonblocking finding and deliberate limits

- **Low, replay/final-stage time control.**  `wall_limit_seconds`,
  `memory_limit_mib`, and `max_new_origins` are checked while discovering new
  origins, but not while replaying prior receipts or performing final
  multiplicity/export crosschecks.  The completed-state replay therefore ran
  for 297.776 seconds even though the mechanism is described broadly as
  wall-limited.  `EXPLAIN QUERY PLAN` shows that the first-origin audit uses a
  correlated earlier-receipt search without a canonical-key index, explaining
  most of this restart cost.  Peak memory was only 38.703 MiB, and the run was
  finite and deterministic, so this does not affect the production
  certificate's soundness.  The protocol should qualify the controls as
  origin-discovery gates, or a future version should index
  `origin_receipts(canonical_graph6, host_index, neighborhood_mask)` and add
  resource checks outside `_audit_origins`.
- **Canonical normal form not rederived.**  The checker proves that every raw
  origin is isomorphic to its stored key but does not independently prove that
  the key is nauty's unique normal form or compare all distinct keys for
  isomorphism.  An erroneous split of one isomorphism class would cause extra
  evaluations, not omit a raw origin or create a false negative.  An erroneous
  merge of nonisomorphic graphs is excluded by the per-origin witness checks.
- **Evaluation solvers not rerun.**  Category shape, nullability, deltas, and
  agreement fields are checked, but \(\gamma\), \(\alpha\), private
  obstructions, and one-guard fixed points are not recomputed here.  This is
  an explicit and appropriate separation of duties; the evaluation audit
  remains mandatory for a mathematical finite claim.
- **No execution-call trace.**  One database row per canonical key proves one
  stored evaluation result per key, not the number of times an evaluator
  function was invoked before that row was committed.  This cannot invalidate
  coverage or a correctly verified stored result.

## Final conclusion

The frozen coverage checker and the exact production report support the
claim that every connected one-vertex extension of each of the 55 pinned MMV
near-miss hosts was represented in the ledger and attached to an isomorphic
stored evaluation key, with no missing origin and exact multiplicity.

The accepted statement is precisely this finite coverage claim.  The
stronger statement that no such extension is a counterexample additionally
depends on the separately reviewed evaluation certificates; neither statement
settles the universal conjecture.
