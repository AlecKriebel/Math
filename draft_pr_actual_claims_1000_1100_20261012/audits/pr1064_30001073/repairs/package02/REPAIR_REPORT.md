# PR1064 bounded archive-output repair02

**The sole whole02 P3 archive-output alias finding is repaired and falsification-tested. Bounded repair completion: 100%.** The changed package is prepared for root adoption and a **new complete whole03 review**. This is neither a new whole review nor zero-issue clearance. Current stage is `PENDING_NEW_WHOLE_03`, dated 14 October 2026, with two whole reviews completed, at least two required, publication_ready=false and issues_updated=false. Service/publication action remains held after PR1032.

## Scope and custody before mutation

Read the complete whole02 report/verdict and `ROOT_WHOLE_PACKAGE_REVIEW_02.json`, including the root's independently reproduced normal/-O exit-zero descriptor overwrite. The exact hypothesis under repair is that the archive builder must reject, before any directory creation or writer opening, an output whose resolved pathname or existing filesystem identity aliases **any protected current package input**. This includes allowlisted members and excluded external binding, metadata/admin/report/seal files. The designated generated `support.zip` and temporary outputs remain mutable; an ordinary independent archive output must still work. The claim concerns a static local filesystem, not a concurrent hostile-filesystem race.

Before editing, froze **402** immediate non-temporary audit inputs by bytes/SHA256 and preserved exact bytes of **25** old current top-level code/admin/docs/seals and the external descriptor/archive under `before/preprint_v1_0/`. Raw source/tree bodies were hashed without duplication; old tmp/render/extracted trees were not touched or copied. `INPUT_PINS.json` and `BEFORE_PINS.json` record this custody. Disk pressure briefly prevented a helper-file write and shell heredoc creation before archive regeneration or scratch creation; the failed helper was absent, and the small writes succeeded after availability recovered. No unrelated files were removed.

Exactly **ten** pre-existing package files changed: `build_archive.py`, `verify_package.py`, README, COPY_MAP, SAFE_INPUT_PINS, EXCLUSION_LEDGER, SUPPORT_ALLOWLIST, SUPPORT_MANIFEST, support.zip and external DEPOSIT_BINDING. All other **392** frozen inputs retain exact bytes. `CHANGE_INVENTORY.json` supplies every before/after hash and exact preserved-byte path. `PROTECTED_BYTE_RECEIPT.json` checks the full boundary.

Canonical paper source/PDF, all source and mathematical claims, bibliography/attribution/license, unchanged mathematical checkers, the original nine, all old 91 copy-map records/bytes, both whole-review verdicts/reports, original103-stage OUTPUT/STATUS/FINAL_VERIFICATION/preparation report/log, and repair01 current124/all125 and 37 terminal outputs remain unchanged. The dated `CURRENT_STATUS.json` and `CURRENT_OUTPUT_PINS.json` from repair01 also remain unchanged. No prior stage is silently rebound to repaired bytes.

`resolve_prior_stages.py` checks all original103 preparation outputs, repair01 current124 output records, repair01 all125 file records, 37 repair01 terminal outputs, 294 repair01 initial inputs, and the 17 whole01/28 whole02 terminal outputs. For package-stage records it selects only a current/before02/before01 file whose size and SHA256 exactly match the original dated pin; otherwise it raises. `PRIOR_STAGE_RECEIPTS.json` records every stage resolution. All 170 original preparation inputs are still unchanged. Historical Git/source authentication retains its review's original scope and date; this repair performed no new authentication or source retrieval.

## Code and current-stage changes

`CODE_DIFF.patch` gives the complete two-program diff. `build_archive.py` keeps the existing verifier and archive checks, then iterates over every current package file. It excludes only root `support.zip` and paths below root `tmp/`, compares the resolved output against each resolved protected input, and checks `samefile` for an existing output. An explicit raising guard rejects an alias before suffix/location validation, `mkdir`, ZipFile writer construction or content writes. This protects the external descriptor and excluded stage/admin files as well as ZIP members. It uses the same resolved-path plus existing-file-identity mechanism as the unchanged PDF builder guard. Python bytecode writing is explicitly disabled before dynamic verifier import, so even ordinary invocation does not create an incidental cache while rejecting an alias.

`verify_package.py` adds the latest stage's strict pending/count/false-flags/PR1032 checks while preserving the original and repair01 gates and every old hash/allowlist/path/copy/status/metadata/diagnostic/archive/binding check. The PDF builder, mathematical programs and source claims have no code/content changes.

Added `CURRENT_STATUS_WHOLE03.json` rather than editing old status records. Appended **31** exact UTF8 authored history copies: all 28 whole02 terminal outputs, its OUTPUT_PINS, its distinct SEAL, and root whole02 adoption. Existing 91 copy records retain both order and values; current COPY_MAP/SAFE_INPUT_PINS cover **122** exact source-equal copies, including all nine originals. Reports and seals still describe their original dated candidates and findings.

README now identifies the separate latest pending stage, archive alias protection and prior-stage resolver. EXCLUSION_LEDGER retains all previous boundaries and individually adds whole02 private source extracts/renders/evidence binaries and repair02 preserved-before/private-custody/disposable fixture/process trees. Full third-party bodies, raw search captures, full Git trees, duplicate archives/PDFs, source-page renders, environment/process trees and old scratch remain excluded. Terminal authored receipts, derivations, locators, programs and reports are included; private-evidence pins contain hashes/locators rather than source bodies.

Regenerated the allowlist, self-excluding manifest, archive and external binding. The latter changes only archive hash/byte count; PDF record/schema/names remain identical to its preserved value and the descriptor remains outside the ZIP. Bare metadata and both publication wrappers retain byte-identical bibliographic objects and normalize exactly. The latest `CURRENT_OUTPUT_PINS_WHOLE03.json` separately seals 157 other current non-temporary package files; `FINAL_CURRENT_PINS.json` pins all **158**, including that latest seal. Old stage seals remain immutable and resolve through preserved bytes. These pins and the external descriptor avoid self/archive hash cycles.

## Actual controls and independent reproduction

`validate_repair.py` ran **411 actual subprocess commands** and incrementally persisted every result—argv, cwd, expected success, exit code, stdout and stderr—in `EXECUTIONS.jsonl`, before any subsequent assertion could fail. Full terminal reproduction and guard receipts are in `REPRODUCTION_RECEIPTS.json` and `GUARD_CONTROL_RECEIPTS.json`. One small new disposable extraction was used and removed only after receipts were captured; no prior scratch or other effort was deleted.

The four actual standard-library README commands passed from a clean extraction:

```sh
python3 -I -B verify_package.py
python3 -I -B run_checks.py --out-dir tmp/recheck
python3 -I -B build_archive.py --output tmp/rebuilt.zip
python3 -I -B verify_package.py --archive tmp/rebuilt.zip
```

The unchanged fifth CLI, `python3 -I -B build_pdf.py --out-dir tmp/recompiled`, passed **only with a disposable fake compiler**. This is an explicitly scoped CLI check, not actual standalone paper compilation or PDF/layout verification. No actual paper compiler/render/new PDF marker ran on the candidate. The next full whole03 reviewer will run real standalone compilation. Prior five-page QA applies to the byte-identical canonical PDF.

The unchanged entropy reviewer checker replayed only in normal -I -B mode with assertions active, matching its root baseline after the declared runtime-only projection. No optimized-mode validity claim is made for that assertion-based original. The existing explicit-guard derivative's normal/-O mathematical outputs agree after the declared runtime projection, and its seven semantic faulty variants reject in both modes. `CHECKER_REPLAY.json` preserves the 11 matrices/two laws/1573 positive histories/201 scalar pairs/120-digit Decimal scope. This remains finite corroboration rather than a universal, interval or formal proof.

After the clean commands, every exact excluded current input was also supplied to the extraction. The resulting **157 protected inputs** match the candidate's complete current non-generated input set, including every metadata, status, seal, report, program, selected history record and external descriptor. In both normal and optimized Python, an existing `tmp/hardlinked.zip` hardlink to **each** protected file rejected at the new explicit guard: **314 hardlink rejections**. Every alias retained its sentinel bytes, and every protected fixture byte was compared with the full baseline after each rejection.

Sixteen representative protected inputs—TeX, PDF, all three bibliographic objects, descriptor, original/current/latest seals, original/current/latest status, preparation report, final verification, builder and verifier—also rejected direct lexical and file-symlink aliases in both modes. Directory-symlink descriptor aliases rejected, as did a nonexistent-parent/`..` alias without creating that parent. Four instrumented actual-builder controls against descriptor/latest-seal hardlinks showed that ZipFile's writer constructor never opened. The source bytes were unmodified for these probes.

Both modes permit ordinary `support.zip` regeneration and a separate tmp archive, with byte-identical output and every protected byte preserved. Present binding verification passes strictly; a required explicitly absent binding rejects. Coherently rehashed manifests cannot bypass latest readiness/count/hold checks or the prior dated status/count gates. Final actual-candidate strict verification passed normally and with -O after current pins were issued.

To prove the falsification controls expose the original mechanism, each mode then deleted only the new alias assertion in a disposable builder and coherently rehashed its manifest. An existing hardlink to the excluded descriptor allowed the writer to open, overwrote that descriptor and **exited zero**, exactly reproducing the actionable finding. The receipts preserve before/after hashes and writer-open observations. Builder, manifest and descriptor were restored byte-for-byte, the alias/marker were removed, and all protected baseline bytes matched again before scratch deletion.

A separate standard-library builder, without importing supplied code, produced a **closed ZIP** identical to the canonical archive and documented supplied rebuild. All **149** sorted members have identical source bytes, fixed 14 October 2026 midnight timestamps, Unix regular mode0644, deflate compression and no encryption. The self-excluded manifest covers the other **148** members, and every non-PDF payload decodes as UTF8. Environment: Python3.14.6/zlib1.2.12. Cross-environment compressor identity remains qualified.

Final canonical PDF: **74898 bytes**, SHA256 `67f07f64a5b06c9a4372c285ed438e735fb780d8477b25652bea4f7f6c72e072`.

Final support ZIP: **392854 bytes**, **149 members**, SHA256 `38167c28024e0d726e8bcc4a82649c5a7f1640548e26ff88a183c832e068940f`.

Exact preserved repair01 ZIP: **308222 bytes**, **117 members**, SHA256 `245221160023953cbeac0fa0a253762b0a46ac9b56b6bf9e721669144cc93e13`.

## Terminal disposition

The strongest verified bounded result is pre-write rejection of lexical/symlink/existing-hardlink aliases to all current protected inputs, including excluded descriptor/admin/stage records, with valid independent generated outputs and effective normal/-O guards. All prior mathematical/source/PDF/metadata/history and dated stage semantics remain checkable through exact bytes. No speculative concurrent-filesystem security guarantee is made.

`python3 -I -B resolve_prior_stages.py` produces the full old-stage receipt. `python3 -B finalize_receipts.py` imports only the adjacent resolver and regenerates final protected/current pins and code diff. Repair02 OUTPUT_PINS seals the authored terminal records and exact before files, excluding itself; the parent must independently hash it and read the full report/inventory/receipts before adoption. A fresh complete whole03 review remains the exact outstanding gate.

No Git/index/branch/remote, PR/issue/service, publication/deposit/DOI, source fetch, external individual communication, other effort/shard mutation, new human peer review, formal certification or readiness promotion occurred. Historical novelty/priority remain UNKNOWN, both readiness flags remain false, and the service hold remains after PR1032.
