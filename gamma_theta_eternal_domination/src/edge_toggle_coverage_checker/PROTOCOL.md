# Independent edge-toggle post-run coverage audit

## Purpose and independence

This package audits a **completed** production run of the one-edge-toggle
kill test. It does not import or execute `src/search/edge_toggle_killtest.py`,
verifier A, verifier B, nauty, or the earlier extension checker. Its two write
targets are a separate resumable SQLite receipt ledger and an atomic JSON
report.

Run:

```text
PYTHONPATH=src PYTHONWARNINGS=error python3 -m edge_toggle_coverage_checker
```

The checker refuses an in-flight search database: `-journal`, `-wal`, or
`-shm` companions are fatal, and the production database is then opened with
SQLite's immutable read-only mode.

## Exact input binding and independent seed selection

The checker pins the exact bytes of:

```text
results/extensions_unique.csv
e7f0ffa459d74a67a3a647e19ee5669652ff1679302b3b62daaef299ee02945e

results/extension_coverage_audit.json
523b3a57ef9afac2b8c921564afcf3fcd8fdbe7719984014f3b0f8e80da8e7cb

results/extensions_evaluation_audit.json
75c999e19fb3e877083e4612dd2550079480ad610b67a5caefb0fbf6d303678e
```

Both extension audits must report a passed complete result and bind the
unique CSV. The evaluation audit must independently discharge exactly 391
rows with `gamma=alpha=3` and an empty one-guard greatest fixed point.

The edge-toggle checker parses all 54,216 unique rows itself. It selects, in
file order, exactly the 285
`eternal_false_without_private_obstruction` rows and 106
`private_obstruction_eternal_false` rows, assigns `ET-0001` through
`ET-0391`, and verifies every selected strict graph6 record is connected and
has its stored order, size, `gamma=alpha=3`, and both stored eternal decisions
zero. The independent order census is 15 order-11 and 376 order-12 seeds.

For each seed, the checker constructs the lexicographic unordered pairs
`(u,v)` with `0 <= u < v < n`. This yields exactly

```text
15*C(11,2) + 376*C(12,2) = 25,641
```

origins, each with an independently determined add/delete action.

## Search-artifact binding

The checker verifies SQLite integrity, foreign keys, user version, the exact
table schemas, and the three metadata keys. It parses configuration JSON with
duplicate-key and non-finite-number rejection and recomputes its canonical
SHA-256. The configuration must bind the exact seed input, passed extension
coverage audit, empty active-seed list, pinned `labelg` and nauty archive,
accepted engine SHA-256, all search/evaluator runtime source bytes, Python
runtime, and resource controls.

The final checkpoint must bind the immutable database bytes, both CSV export
hashes, all 391 completed seed summaries, 25,641 processed origins, and a
passed internal coverage audit. Database metadata, canonical rows, origin
rows, checkpoint fields, and the designated candidate-freeze directory must
all be candidate-free.

## Per-origin reconstruction and exact isomorphism

At each exact `(seed_id,pair_index)` position, the checker:

1. complements exactly the specified adjacency bit;
2. determines `add` or `delete` from the seed itself;
3. requires byte-for-byte equality with the stored raw graph6;
4. strictly parses the stored headerless canonical graph6;
5. runs a standalone deterministic color-refinement/backtracking
   isomorphism algorithm to obtain an explicit raw-to-canonical permutation;
6. verifies that permutation directly edge by edge;
7. records the origin, permutation, and a domain-separated receipt-chain
   digest in an independent transaction.

The graph code is bounded to order twelve and has no heuristic cutoff.

Every restart replays every earlier receipt from origin zero, reconstructs
the raw toggle, compares the immutable production row, verifies the saved
permutation directly, recomputes its receipt chain, and rebuilds canonical
multiplicities. It does not trust only a last-index counter.

## Completion checks

After all receipts exist, the checker requires exactly one canonical table
row for every used key and no unused row. It reconciles every multiplicity
and first origin, checks strict graph metadata, connectivity, A/B stored
equalities, parameter-chain and category logic, and absence of a candidate.
It recomputes every seed's ordered canonical-stream SHA-256 and compares
every field of both CSV exports with the immutable database.

Before marking its state complete, it recomputes the entire input/source
binding to detect concurrent mutation. The final report binds its own checker
source manifest, all input and output hashes, the independent state-database
hash, the receipt-chain hash, stream hashes, category census, resource use,
and limitations.

## Deliberate limitations

The checker exhibits an exact isomorphism from each raw graph to its stored
key, but it does not derive a canonical normal form independently. Distinct
stored keys that happened to be isomorphic would cause redundant evaluation,
not omission of a raw origin.

It checks stored mathematical parameter equalities and category logic for
consistency, but does not recompute `gamma`, `alpha`, one-guard eternal
domination, or `theta`; that is the separate mathematical evaluation audit.

The ledger proves one stored evaluation record per canonical key but contains
no evaluator call trace. The result is a certificate-backed finite search
around 391 seeds, not a proof of the universal conjecture.
