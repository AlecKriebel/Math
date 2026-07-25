# Independent post-run coverage and canonicalization audit

## Scope

This package checks a **completed** run of
`src/search/extension_killtest.py`. It never launches or resumes the search.
It imports neither that engine nor either eternal-domination evaluator.
Its purpose is to turn a completed SQLite ledger and its two CSV exports into
an independently reconstructed coverage artifact.

The production command is:

```text
PYTHONPATH=src python3 -m coverage_checker
```

The audit is resumable. Its only write targets are a separate audit-state
SQLite file and an atomic JSON report. `--max-new-origins`, the wall limit,
and the resident-memory limit produce a clean `in_progress` checkpoint.
Re-running the same command resumes. A changed input, search database,
checkpoint, export, search source file, or checker source file invalidates
the audit binding and fails closed.

## Immutable inputs and configuration binding

The production checker requires the exact catalog and parameter-table
SHA-256 values:

```text
instances/mmv2022_table9.csv
801f054853d07652c795fb16217425869f857d7f5d74e427165d554faf4eae1d

results/mmv2022_parameters.csv
ef74175dfd81542a167feed5a2d7f66be723846993642fb65344d08655b594c6
```

It independently parses and joins those files, obtains exactly 55 distinct
connected hosts, checks their stored order and size, verifies the
\((n,\gamma)\) distribution, and derives

\[
 2(2^{10}-1)+53(2^{11}-1)=110\,537
\]

nonempty extension masks.

The search database is opened read-only with SQLite's immutable flag. Any
WAL, shared-memory, or journal companion makes the audit refuse to start.
SQLite integrity, foreign keys, schema version, exact table columns, and the
three exact metadata keys are checked.

The stored configuration JSON is parsed with duplicate-key and non-finite
number rejection. Its canonical SHA-256 must equal the metadata digest. The
checker then verifies:

- the supplied catalog and parameter paths and byte hashes;
- an empty active-host list, so the run is not a shard;
- target guard count three and schema version one;
- the exact pinned `labelg` executable and nauty source-archive hashes;
- the ordered runtime-source manifest, its aggregate hash, and the engine
  hash against current local bytes;
- positive finite resource controls and a positive integer batch size.

The final human-readable checkpoint must bind the same configuration and
database bytes, have status `complete`, contain no candidate state, report
55 completed hosts and 110,537 processed origins, and bind both output CSV
hashes.

## Streaming origin proof

Origins are read in `(host_index, neighborhood_mask)` order. Starting from
the previous independent checkpoint, the checker requires the exact next
pair. Thus a missing, duplicated, reordered, zero, or out-of-range mask
fails at its first position. For every one of the 110,537 origins it:

1. independently reconstructs the host graph from strict graph6;
2. adds vertex \(n\) adjacent to exactly the nonempty mask;
3. requires exact equality with the recorded raw graph6;
4. parses the recorded canonical graph6 independently;
5. uses a standalone exact individualization/refinement backtracker to
   exhibit a raw-to-canonical graph isomorphism;
6. checks neighborhood size, category inheritance, and
   \((\Delta\gamma,\Delta\alpha)\);
7. increments an independent canonical-key multiplicity and extends a
   deterministic origin-chain SHA-256.

The graph implementation accepts only ordinary, headerless graph6 in ledger
records and is deliberately bounded to order 12. It has no heuristic
isomorphism cutoff: rejection is exhaustive in that bounded universe.

Each audit-state batch is one SQLite transaction containing canonical
multiplicities, first-origin provenance, the last verified mask, total
count, chain digest, and a receipt for every origin containing its exact
raw/canonical records and isomorphism mapping. A crash before commit rechecks
that batch; a crash after commit resumes at its exact successor.

Before every resume, all earlier receipts are streamed from the beginning.
The checker reconstructs their raw graphs again, compares them to the
immutable search rows, directly verifies each stored permutation as an
isomorphism, and recomputes the full receipt chain. Thus resume does not
merely trust a mutable count and last-mask pointer; it cheaply replays the
already discovered mapping witnesses without repeating the backtracking
search.

## Canonical rows, multiplicities, and exports

After all origins are reconstructed, the checker streams the canonical table
against the independently accumulated key table. It requires:

- exactly one stored evaluation row for every distinct canonical graph6 key
  used by an origin, and no unused row;
- exact stored and independently counted origin multiplicities summing to
  110,537;
- first-evaluation host, mask, and raw graph equal to the first origin in
  search order;
- graph order and size equal to the strict graph6 record;
- category-specific nullability and parameter consistency;
- no `candidate_eternal_3` record in a claimed completed negative run.

It independently recomputes every host's ordered canonical-stream SHA-256.
Finally it streams both CSV files and compares every field and row, in the
documented order, to the immutable database. Their byte hashes must already
match the final checkpoint.

## Deliberate limitations

The final database can show one **stored evaluation record** per canonical
key, but it contains no call trace and therefore cannot prove how many times
an evaluator routine was invoked during execution.

The exact backtracker verifies every raw-to-canonical isomorphism, which
rules out a nonisomorphic collision under a key. It does not independently
derive a canonical normal form or compare every pair of distinct keys.
Redundant isomorphic keys would cause duplicate work, not omission of a raw
origin or an unsound negative conclusion.

The checker validates evaluation-record consistency; it does not recompute
\(\gamma\), \(\alpha\), or the eternal-family fixed point. Those are covered
by the two separately audited evaluator implementations and, for any
decisive claim, their own certificates.

`complete` certifies only the finite one-vertex-extension universe. It is not
a proof of the universal \(\gamma\)–\(\theta\) conjecture.
