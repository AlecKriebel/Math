# PR1064 bounded package repair 01

The two review01 P3 package findings have been repaired and falsification-tested. Assigned bounded repair completion: **100%**. The changed package is ready for a **new full whole02 review**; this repair is not a new whole review or root zero-issue clearance. `CURRENT_STATUS.json` is dated 14 October 2026, records one completed new whole review and at least two required, and keeps publication_ready=false and issues_updated=false. Publication/service action remains held after PR1032. Historical novelty and priority remain UNKNOWN.

## Scope, hypotheses and preserved evidence

Read the applicable AGENTS.md, complete `reviews/package_01/REPORT.md` and `VERDICT.json`, and `ROOT_WHOLE_PACKAGE_REVIEW_01.json`. The root adoption required both P3 repairs before zero-issue clearance. Treat the repaired claims as testable hypotheses: (1) no accepted build-PDF output can alias the canonical PDF through ordinary paths, directory/file symlinks or an existing hardlink; rejection must precede any output write or compiler call; (2) every allowlisted local path, including the self-hash-excluded manifest, must satisfy the existing regular-file, no-symlink and ancestry rules before its content is read. Guards must be effective with Python assertions disabled.

Before candidate mutation, froze all **294** immediate non-temporary audit inputs by size/SHA256 and preserved exact old bytes of **23** top-level mutable/admin code, documentation, pins and archive files under `before/preprint_v1_0/`. Large raw inputs were hashed without duplication. `INPUT_PINS.json` and `BEFORE_PINS.json` record this custody. Old temporary/render/extraction trees were neither modified nor copied. Only ten pre-existing package files changed; every other frozen immediate input (284 files) retains its exact bytes. `CHANGE_INVENTORY.json` gives before/after hashes and exact preserved-byte locations, and `PROTECTED_BYTE_RECEIPT.json` records all checks.

No TeX, canonical PDF, bibliographic metadata object or wrapper, mathematics/source claim, attribution/license, mathematical checker, nine originals, prior report/verdict, old 72 copy-map records/bytes, or dated original stage/seal was changed. All 170 original preparation input pins remain correct. All 103 old preparation output records validate through `resolve_preparation_stage.py`, using exact before bytes for records affected by the repaired stage. `OUTPUT_PINS.json`, `STATUS.json`, `PREPARATION_REPORT.md`, `FINAL_VERIFICATION.json` and the preparation research log remain immutable dated records; they do not acquire new meanings. The original package-review verdict retains its two P3 findings and original date/scope.

## Repairs and administrative changes

**P3-01:** `build_pdf.py` resolves the output directory and proposed `paper.pdf`, compares it with the resolved canonical PDF, and checks `samefile` when both files exist. A matching destination raises before `mkdir`, compiler discovery or subprocess invocation. This covers `.` and absolute/relative aliases, directory symlinks, file symlinks and existing hardlinks. The documented `tmp/recompiled` path still exports successfully. The no-canonical-mutation promise was preserved.

**P3-02:** `verify_package.py` adds an explicit raising `local_regular` preflight containing the existing file/no-symlink and full relative-ancestry checks plus an explicit regular-file-mode check. It first guards `SUPPORT_ALLOWLIST.json` before the necessary bootstrap read; after reading names it guards every member before reading the manifest or any other allowlisted content. `SUPPORT_MANIFEST.json` remains excluded from its own hash, while its path is guarded. No circular manifest was introduced. Existing hash, exact allowlist, archive, copy-map, selected-pin, metadata, original dated status, diagnostic and binding checks remain, and the separate current-stage gate requires pending whole02/count1/required>=2/false flags/PR1032 hold.

Appended exact UTF8 authored copies of all **17** review01 terminal outputs, their `OUTPUT_PINS.json` seal, and the root whole-review adoption to the selected history. All 72 preceding copy records retain their values/order and byte-identical package copies. Current `COPY_MAP.json`/`SAFE_INPUT_PINS.json` cover **91** source-equal copies, including all nine root originals. This history records completed review01 with its original findings; it does not certify the repaired bytes.

`CURRENT_STATUS.json` is the only new current-stage member. README identifies both the unchanged dated preparation snapshot and the current pending gate, explains alias rejection and separate current pins, and retains the original reproduction commands/scientific scope. `EXCLUSION_LEDGER.json` individually explains omitted third-party source bodies/raw searches/full Git trees; duplicate family snapshots; extracted/recompiled trees and duplicate binaries; render/source-page images; preserved-before/private custody trees; and environment/process/stdout/stderr scratch. None enters the safe payload. Only explicitly allowlisted authored UTF8 text/code and the one canonical authored PDF are distributed.

Regenerated the allowlist and self-excluding manifest, deterministic archive, and external delivery binding. `publication/DEPOSIT_BINDING.json` changes only the current archive hash/byte count; its canonical PDF record/schema/names are identical to the preserved descriptor. The descriptor remains outside the ZIP. `metadata.json`, `publication/release_metadata.json` and `publication/zenodo.json` are byte-identical and normalize to the same bibliographic object. `CURRENT_OUTPUT_PINS.json` separately seals all 124 other current non-temporary package files. Local repair `FINAL_CURRENT_PINS.json` pins all 125 current package files, including that current seal. These are noncircular integrity records.

## Actual verification and falsification

`validate_repair.py` ran **63 actual subprocess commands** with full argv, working directory, exit status, stdout and stderr captured in `REPRODUCTION_RECEIPTS.json`. A single new extraction was used and removed after receipts were captured; no pre-existing scratch was deleted. The actual clean README sequence succeeded:

```sh
python3 -I -B verify_package.py
python3 -I -B run_checks.py --out-dir tmp/recheck
python3 -I -B build_archive.py --output tmp/rebuilt.zip
python3 -I -B verify_package.py --archive tmp/rebuilt.zip
python3 -I -B build_pdf.py --out-dir tmp/recompiled
```

The last command ran actual Tectonic only in the disposable extraction to its safe temporary output. It produced a 74899-byte PDF with the disclosed underfull bibliography warning; no cross-build PDF byte-identity claim is made. The extraction's canonical PDF and actual candidate canonical PDF stayed byte-identical to their frozen inputs. There was no compiler run, render, new PDF marker, or layout validation on the actual candidate. Prior whole-review five-page visual QA applies to the unchanged canonical PDF bytes.

The unchanged mathematical reviewer checker reran in normal `-I -B` mode with assertions active, matching the baseline after the declared runtime-only projection. No optimized-mode validity claim is made for that original checker. The existing explicit-guard derivative reran normally and with `-O`, with matching complete mathematical output after the declared runtime projection. Seven semantic faults were rejected in both modes: scalar divergence deletion, wrong unit endpoint, zero-mass-term deletion, n1 pure-power misuse, matrix/sequential KL confusion, sequential KL deletion, and wrong Dong–Jain half coefficient. Scope remains 11 matrices, two arbitrary laws, 1573 positive histories, 201 scalar pairs and 120-digit Decimal logs; finite diagnostics are not a universal proof or interval/formal certificate. `CHECKER_REPLAY.json` preserves these receipts.

PDF controls used the actual repaired script in a disposable sentinel fixture with a guarded fake compiler. In both normal and optimized modes, six alias families (`.`, absolute root, nonexistent-parent/`..`, directory symlink, file symlink, existing hardlink) rejected: **12 rejections**, canonical sentinel bytes unchanged, no new alias directory and no compiler marker. A separate safe path succeeded in both modes and invoked the fake compiler. Deliberately deleting the guard only in the disposable script reproduced a compiler call and sentinel overwrite in both modes, establishing that the controls can expose the original bug.

Self-manifest controls used both coherent same-byte and malformed symlink targets. Both modes rejected with the path-safety message before JSON parsing; same-byte allowlist symlinks and regular files reached through symlink ancestry also rejected. Deliberately restoring the manifest omission only in the disposable verifier, with a coherently rehashed manifest, accepted the same-byte manifest symlink in both modes. `GUARD_CONTROL_RECEIPTS.json` records these observations. The immutable source was restored between controls.

Both modes also rejected required-absent bindings, malformed explicit/default-present bindings, unmanifested files, corrupted members, a traversal archive and a missing explicit archive. Present actual external binding with the rebuilt archive passed strictly. Coherently regenerated manifests could not bypass the original dated status gate, current readiness/count/hold gates, copy-map hash checks or selected-pin equality. Final actual-candidate strict verification passed normally and with `-O` after the scratch faults were removed.

Independently rebuilt the **closed** ZIP using a separate standard-library implementation without importing supplied builder/verifier code. It matched the actual candidate and supplied clean rebuild byte-for-byte. Inspected all **117** sorted member names, source bytes, fixed 14 October 2026 midnight timestamps, Unix regular mode 0644, deflate compression and lack of encryption. The self-excluded manifest covers exactly the other **116** members. Every non-PDF payload decodes as UTF8. Environment: Python 3.14.6 and zlib 1.2.12; cross-environment compressor identity remains qualified.

Final canonical PDF: **74898 bytes**, SHA256 `67f07f64a5b06c9a4372c285ed438e735fb780d8477b25652bea4f7f6c72e072`.

Final support ZIP: **308222 bytes**, SHA256 `245221160023953cbeac0fa0a253762b0a46ac9b56b6bf9e721669144cc93e13`, **117 members**.

Exact preserved prior ZIP: **263179 bytes**, SHA256 `46101b4ccb180bb99996e02ebceb1b23e616da23f54c291ddf1688f3976ceb63`, **97 members**.

Local final custody commands are `python3 -I -B resolve_preparation_stage.py` (captured in `PRESERVED_PREPARATION_RECEIPT.json`) and `python3 -B finalize_receipts.py` (imports only the adjacent resolver; creates protected/current-stage receipts). Terminal repair `OUTPUT_PINS.json` independently seals the repair's authored records and exact before copies, excluding itself. The parent must independently hash that seal, read the complete report/inventory/receipts, and obtain new whole02 review on the changed package.

## Disposition and exact remaining gap

Strongest verified repair result: the two bounded path-safety claims hold on the tested ordinary/alias/link cases, with controls that expose deliberately reintroduced failures, while mathematical/source/PDF/metadata/history bytes and original stage semantics are preserved. A concurrent hostile filesystem race is outside the original static local-package workflow and is not claimed to be prevented by path preflight. No full whole02 review, zero-issue clearance, release, deposit, publication, or novelty certification is claimed here.

Work stayed in the new `repairs/package01` folder and necessary package code/admin/history/binding paths. No Git/index/branch/remote/PR/issue/service operation, source fetch, outside communication, individual contact, other effort mutation, or external human peer review occurred. The next required action is independent root adoption and a fresh complete whole02 review. Both readiness flags remain false and the ascending service hold remains at PR1032.
