# Targeted helper02 binding/publication/tracker repair

Status: four-source implementation and targeted controls complete; **coordinated six-source freeze received, new independent review required**. This is internal repair evidence, not finding clearance or release authority. Case estimate remains **65%**. Scientific B and all historical review/repair evidence remain unchanged.

## Scope and intake

This iteration read the full sealed `release_helpers_adversary_02/REPORT.md`, `ASSESSMENT.json`, M01/M02 exact probe/edge sources and results, and root's actual read-only Sheets response contract before changes. It owns only `release_binding.py`, `append_verified_tracker.py`, `publish_preprint.py`, and `verify_published_readonly.py`. The native implementer owns M03 and the other two sources.

The actual root observation shows the full-column A:D request returning `'Math Puzzles'!A1:D1114`, `majorDimension: ROWS`, with 118 returned values; omitted trailing blank rows do not mean truncated grid coverage. A later root read-only metadata observation has rowCount1115/columnCount43, demonstrating legitimate growth. This shard performed no live provider/network/Git/index/ref/QUEUE/database/install/environment/cache/secret/external communication action. All Python used the existing standard runtime with `-B`. Real child processes were controlled local Python children only.

## RH209-02-M01 implementation

`tracker_properties()` authenticates spreadsheet identity, the unique exact sheet ID/title, grid sheet type when supplied, and integer row/column dimensions with at least four columns. `tracker_readback(record,target,properties)` now validates both retained request and returned response: explicit `ROWS`, exact quoted Math Puzzles tab and A:D columns, finite row coordinates, matrix bounds, and coverage against that authenticated grid metadata.

An exact target requires the same requested row within the grid. A full A:D scan requires the finite response A1:DgridRowCount; returning 118 values over a1114-row grid is valid because trailing blanks are omitted. Missing/wrong/truncated range identity, COLUMNS, wrong tab/columns/start, absent grid dimensions and overlong matrices fail closed.

Every append GET and fresh read-only target/full scan uses this validator. The append workflow retains initial `properties_before` and `before_scan`, then obtains new `properties` after the attempted INSERT_ROWS and validates the target/final full scan against the new grid. This accepts legitimate growth1114→1115 and rejects a stale1114 scan after growth. Pure `tracker()` checks all retained before/target/after responses, with matching metadata, including zero-write reconciliation. It validates the complete initial preflight for count1 and requires reconciliation_before to equal before_scan for count0.

Publication's tracker duplicate preflight also obtains grid metadata and uses the same returned-identity validator. The durable stage intent pins its retained `PUBLICATION_PREFLIGHT.json`, which pins actual metadata and full-scan response bytes. Pure `publication_lineage()` revalidates those retained responses and the no-problem/header condition. Thus the earlier publication-stage GET is covered as well as the append/live GETs.

Fresh grid changes during the interval between metadata and a values GET may cause a legitimate response to fail closed. Retained once-intents remain in place; recovery is read-only, and no second append is authorized. This does not claim an atomic snapshot across Sheets calls.

## RH209-02-M02 implementation

All three process readers now use binary `subprocess.run` capture (`text=False`). The shared `save_process_streams()` writes both exact stdout and stderr before UTF-8/JSON parsing. Exception stdout/output and stderr are also saved before the error record and rethrow. Decode failures cannot discard invalid UTF-8 or NUL bytes. Existing timeout/nonzero/pending and once-intent behavior remains.

Public downloads now open a retained payload before reading, then stream finite chunks directly to it while hashing. On an exception, available `exception.partial` bytes are appended after earlier chunks, flushed and described by a retained READ_FAILURE record with exact size/hash and exception type. The original error is rethrown. Generic read failures preserve earlier chunks too. Hash/size failures retain their payloads. An oversize stream fails after retaining the bytes already returned, preventing an endlessly repeating adapter from growing storage without bound.

No exception or decode failure authorizes another stage, publication or append. Successful recovery of a known publication continues through read-only inspection/DOI/public-byte checks only. Existing accepted publication/tracker receipts remain immutable.

## Exact-source controls and honest failures

The programs compile exact source snapshots without source text/AST rewriting. New provider adapters return binary process output, finite cursor-based HTTP reads, authenticated grid properties and canonical finite ValueRanges. Historical sealed programs and their stubs were not edited.

The first program completed eight groups: six passed, two failed because the **new fixture adapter** captured urlopen at module import rather than dispatching the subsequently scripted HTTP response. Its program, raw streams, result tracebacks and every fixture remain preserved. No operative defect is inferred from those two adapter failures. `retry_probes_01.py` supplies a corrected new dispatch adapter and preserves the first program unchanged.

The latest **eleven groups passed** (eight corrected groups plus three final controls), all with actual exit0 and empty stderr:

- Canonical1114-row grid/118-value preflight, INSERT_ROWS growth to1115, exact target row119, pure receipt acceptance and fresh publication/tracker readbacks.
- Missing/wrong tab/range/columns/start, truncated finite coverage, missing/COLUMNS dimension, literal unbounded response range, wrong target row and missing grid dimensions.
- Corrupt retained before/target/after responses even after refreshing their pins, plus live response rejection with accepted receipts unchanged.
- Stale post-append grid coverage leaves pending; recovery appends zero more rows.
- **Six real local binary child runs:** each of the three readers receives invalid UTF-8/NUL stdout and stderr, once as a completed process and once through an actual TimeoutExpired. All twelve saved streams match expected bytes exactly.
- Real `http.client.IncompleteRead` on the first read and after two earlier chunks; exact partial concatenations and failure records retained.
- Published HTTP failure, blocked repeated publish, and successful read-only recovery with one stage/one publish total.
- Wrong publication-preflight returned identity stops before stage.
- Unknown append outcome recovers with append_count0 and exactly one original append.
- Corrupt retained publication preflight rejects through the pure lineage validator.
- Generic HTTP OSError after earlier binary bytes preserves those bytes.

`probes.py`, `retry_probes_01.py`, `final_controls.py`, their stdout/stderr/results, and exact source inputs specify the actual outcomes. This is tested guard behavior with controlled providers, not actual publication or scientific validation.

## Storage and preservation

The first attempt to create this evidence folder failed with ENOSPC; the following patch failed creating its parent before reaching any operative edit. The failure was reported immediately and is recorded in the log. After the root recovered only its own verified duplicates, this shard proceeded. No test execution later suffered a storage interruption.

Every generated fixture group was consolidated only after its ZIP's **exact member set, CRC and every body** matched the owned originals. Each archive has an accompanying member manifest. Only that verified owned generated tree was then removed. All passing and failing fixture groups, binary child streams, malformed responses, pending records and partial HTTP payloads remain in those archives. No historical sealed source/evidence, foreign fixture or scientific byte was removed.

## Interfaces and remaining work

Public native-stage interfaces remain `verify_tracker_live(R,PUB,CTX,z)` and `verify_publication_live(R,PUB,CTX)`. `tracker_readback` now requires authenticated properties as its third argument. The tracker evidence object adds `properties_before` and `before_scan`; stage intents add a retained `preflight` pin. `SCHEMA_SPECIFICATION.json` describes these internal record changes. `CANDIDATE_SOURCE_PINS.json` identifies the four tested candidates.

The root and native implementer received the new adapter/record contracts and candidate hashes. Root froze all six at `2026-10-16T07:12:37.851830+00:00` in `ROOT_RELEASE_HELPER_REPAIR02_SOURCE_FREEZE.json`; this shard subsequently checked exact current six-source equality. The final tested four hashes match that freeze. Native M03 changed only its separately owned source; this report does not claim its targeted tests as this shard's work. `FINAL_VALIDATION.json` records the coordinated bindings, unchanged scientific/historical inputs and reverified fixture archives. Another new independent adversarial source review remains required. Case65% and no actual release authority.

For reproduction, copy only the three program files (`probes.py`, `retry_probes_01.py`, `final_controls.py`) into a fresh owned sibling directory under publication, leaving the sealed original untouched. Run the latter two with the existing standard Python runtime and `-B` for the latest eleven groups; their new finite binary/HTTP adapters load the first program's fixture code. The first program is the preserved historical six-pass/two-adapter-failure run. Each program creates new owned evidence and checks each ZIP before its own raw-tree consolidation. Source hashes and the root freeze must be checked first. No live provider is needed.
