# PR209 binding/publication/tracker repair implementation

Status: **implementation complete for the four assigned sources; new independent source review required**. This is internal implementation evidence, not independent review, finding clearance, final release authority, scientific rereview, or evidence of any live publication/tracker/PR/merge action. Case discovery estimate remains **55%**. Assigned implementation estimate is **100%**, subject to adversarial review.

## Scope and preserved inputs

Only `publication/release_binding.py`, `append_verified_tracker.py`, `publish_preprint.py`, and `verify_published_readonly.py` were changed by this shard. All newly authored records are within `publication/binding_repair_01/`. The root/native implementation owns the other two operative sources. Scientific snapshot B, including the 82,528-byte PDF SHA256 `8e28a1764160a7f7ef6e9bf4d1a1937062a003ab462ec93ce69c4643a5c36a55` and actual 683,157-byte ZIP SHA256 `0039aeee870804a149a5ae70f6893335387670e122f833e622d70b42584550f4`, is unchanged.

The sealed helper01 report, assessment, original probe sources, whole01 assessment/manifest/additive report correction, and root resolution were read before implementation. All six original reviewed helper copies remain unchanged in `release_helpers_adversary_01/`; their exact pins are rechecked in `FINAL_SOURCE_BINDINGS.json`. The actual original seals and every listed payload were also authenticated by the compatibility control. No original reviewer seal was rewritten.

All Python invocations used the existing standard runtime with `-B`. No live release, `gh`, GWS, Zenodo, network provider, Git/index/ref, database, queue, environment, cache, secret, or external communication action was performed. Provider behavior in every workflow control was supplied by an in-memory stub. Coordination was limited to the explicitly authorized root/native implementation agents.

## Implemented mechanisms

**RH209-M01:** `context()` now requires two structured sequential whole-package review records and two structured helper review records. It reads and hashes actual assessment, manifest, report, freeze, every manifest payload, and any explicitly supplied additive supplement. Each supplement must preserve the complete original seal. It checks unique review IDs, machine UTC freeze/completion order, and a later freeze after the prior review's completion or later resolution. Every actual mandatory and optional finding requires an actual pinned root resolution linked to that assessment/manifest and exact finding IDs; the next review must freeze the resulting repair bindings. The final clean scientific core and final six helper pins must exactly match current bytes. Counters must equal derived records, not declarations. The source manifest's current payload bytes are checked too. This authenticates retained local evidence and detects omissions/corruption; it does not claim protection if every trust anchor is maliciously rewritten together.

**RH209-M02:** pure `publication()` requires the durable stage intent, exact staged ID, prepublication inspection, publish intent, tool publication receipt, provider confirmation, and final verified receipt. An acyclic digest chain links each earlier record. It validates release binding, exact metadata/files, production environment, positive integer IDs, states and chronology. The verified receipt must agree with its retained actual provider readback and with the exact DOI/version/resolver URLs. Both public file downloads are retained as actual bytes and rehashed during pure receipt acceptance. Unknown publish outcomes recover by read-only inspection; an existing stage/publish intent prevents a repeated mutation. The immutable final receipt is written only after successful public-byte and DOI checks.

Pure `tracker()` requires the actual durable append intent, publication digest, exact destination/payload/DOI, canonical same-row `'Math Puzzles'!Arow:Drow`, integer invocation count 0 or 1, and matching reconciliation mode. It validates actual retained target/all-sheet response records and their request identities, rather than accepting booleans. One-write receipts require the exact saved append response; zero-write recovery receipts require the exact saved existing-row preflight. The provider tab/spreadsheet identity and every cell are checked.

**RH209-M03:** after the exact target readback, the append workflow reads the complete tracker again and requires exactly one problem row and one exact DOI row at the same target with all four expected cells. A duplicate appearing during append leaves timestamped pending evidence and no verified receipt. The retained append intent prevents a second append. Import-safe `verify_tracker_live()` repeats metadata/target/full-sheet read-only checks for native promotion while preserving accepted receipts.

**RH209-O03:** `expected_tracker_row(ctx,z)` derives title, version, and publication date from cleared metadata. Pure receipt acceptance compares the complete exact notes and all four fields. The notes retain the full-period theorem, precise contemporary Ferudun v1.1 credit, bounded priority/no firstness, original source v11, eight-suite qualification, and AI/unrefereed limitations. The version/date drift control uses metadata 1.1 / 2026-10-17 and verifies the resulting new text.

**Shared RH209-M04 support:** `public_exports(R,PUB,CTX)` returns only manifest-pinned case-relative bytes from the explicitly cleared `publication/PUBLIC_EXPORT_MANIFEST.json`. It rejects duplicate paths, traversal, symlinks, private/cache/environment names, self/clearance/mutable receipt references, and unexpected top-level scientific/publication files. Exact `.gitignore` is permitted for the required preserved originals. An explicit finite administrative name set permits stage records to exist without allowing them to enter the static export manifest. The native implementation must add its narrow explicit administrative payload independently; this report does not verify that implementation.

**Fresh public revalidation:** import-safe `verify_publication_live()` first validates the complete stored publication, then performs read-only provider inspection, DOI resolution and actual public PDF/ZIP hashing. It returns new retained evidence without replacing accepted receipts. The caller holds the shared stage lock. The corresponding tracker function has the same caller-lock/immutable-receipt contract.

## Checkable evidence

`SCHEMA_SPECIFICATION.json` defines structured review entries, local pins, export schema, acyclic publication lineage, append intent/readback/receipt contracts, chronology, counters, and callable interfaces. `FINAL_SOURCE_BINDINGS.json` pins the four final sources and unchanged scientific/reviewer bytes.

The three exact-source harnesses compile retained source bytes directly, without source text or AST rewriting. They import modules through controlled provider substitutions; actual local locks, durable first-writer intents, filesystem readbacks and source validation execute on owned synthetic fixture trees. The current four sources are exercised by the final baseline. Earlier snapshots preserve the exact inputs to earlier control runs, including the root/native sources as they existed then; this shard makes no claim that those two sources are their eventual final versions.

All **27 control groups passed**:

| Run | Groups | Evidence |
| --- | ---: | --- |
| 01 | 13 | `PROBE_RESULTS_01.json`, exact sources and input pins, complete stdout/stderr and `probe_runs_01/` |
| 02 | 8 | `PROBE_RESULTS_02.json`, exact sources and input pins, complete stdout/stderr and `probe_runs_02/` |
| 03 | 6 | `PROBE_RESULTS_03.json`, exact final sources and input pins, complete stdout/stderr and `probe_runs_03/` |

These cover a full synthetic publication/append/live-readback baseline; counter-only clearance; actual finding dispositions and chronology; stale science/helper bytes; absent publication ancestry; tracker count/range/notes/reconciliation corruption; duplicate races; unknown append recovery with zero further writes; unknown publish recovery with no repeated POST; bad public bytes retained before rejection; dynamic metadata; unreviewed/.env/traversal exports; optimized guards; altered saved target/uniqueness/intent records even after updating their pins; altered actual downloaded payloads; live duplicate and wrong DOI checks; missing readbacks; actual sealed whole01/helper01 parser compatibility; unknown stage outcomes; intent parent-fsync failure before provider mutation; boolean publication IDs; wrong spreadsheet identity; and a wrong returned append-data range.

No unexpected test run failed. Every deliberately failing workflow retains its fixture, raw streams, pending/exception record and trace. The corrupt public payload is retained losslessly. The implementation also encountered one rejected edit-tool patch (duplicate delete/add operations on the same target); it changed no file and executed no Python. Its error and correction are recorded in the log. Nothing from the original failed audit probes was altered or removed.

## Exact final source pins

| Source | Bytes | SHA256 |
| --- | ---: | --- |
| `release_binding.py` | 33180 | `759e11b99b0ba229edad62b487190d5983dd70fb025b358aec6167593d9570a5` |
| `append_verified_tracker.py` | 7715 | `8d1bb75a20567be282b7d3a38bc325efa9a2e36304b7aa8e788f3bf804604909` |
| `publish_preprint.py` | 5992 | `abd76471ed0d8b283a06ae70fa633214791cc7031bd4587e3155928994ce23d2` |
| `verify_published_readonly.py` | 7633 | `9b190d9e4903fbe2fae11dfe6f863f48e0b33c1e238b62e2bb6302062cadcdb0` |

## Remaining gap

The strongest result here is tested implementation of the assigned guards against exact source bytes, including compatibility with the actual existing first-review seals. The synthetic future clean review/resolution fixtures are explicitly labelled parser controls; they close no actual findings and grant no actual clearance. The root must independently inspect these changes, finish/review the native sources and progress accounting, obtain a **new independent adversarial review of all six final exact sources**, and resolve any resulting findings before constructing actual final clearance. Live provider behavior, permissions, final native tree/queue/accounting, and future release outcomes remain untested by this shard.
