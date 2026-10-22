# Independent PR206 publication-operations source audit

Verdict: **CLEAN SOURCE VERDICT within bounded offline scope** for the five exact final07 sources and contract. No mandatory source finding remains. The separately reviewed Root dispatcher **v2** also receives a clean bounded source verdict. These are source audit results only; no live stage, publish, DOI verification, Sheet update, source adoption, ready90 acceptance, lifecycle advancement or mathematical clearance occurred.

## Exact reviewed unit

| File | Bytes | SHA-256 |
|---|---:|---|
| ops_common206.py |17885|f2bf208c375220797971db2a4606c75164cd27a2e4884d3768c0d569ef1ed772|
| publisher206.py |12158|51809038d0811aba4d35584777a476f362ed032b51760059802c215ba6b7da3e|
| tracker206.py |12926|10975c5abf2b5cc87927bfd791395af76da9216f3e8f9a471d50b36baaf45e33|
| offline_guards.py |34651|9107c57a67a8dda7e0f20aea0dafb130dc6c9c32c7b7298774a03f2743116fa0|
| run_offline.py |4566|aae00bec48ae9a50b86dbf4ceda1073db7b6c44385ca6d8bb685e4cce1647c5a|
| CONTRACT.md |11125|6ea9b5aefef82c193109ff7b12b4e610cefd13a6319209bb5623b389c4b99794|

The final author SAFE_MANIFEST is 17314/SHA494524c185069006023076ce449c3cd6f6540a274f88a1b2f9bdc8807cb09747; its seal is 2351/SHA6950620bdfffdaed78ee2d05d4aa98b617102b6adca7e904ba4cdce5d2b73a1a. All 98 manifest payloads were authenticated only after my primary independent verdict was frozen. ADOPTION_SOURCE_MAP_ONLY.json and FINAL_SOURCE_PINS_07.json identify the current sources; historical FINAL_SOURCE_PINS.json must not be adopted. Absolute reviewed paths are in REVIEWED_SOURCE_PINS.json.

## Independence and evidence

FROZEN_ADVERSARIAL_PLAN.md was sealed before any proposed source exposure at 7049/SHA b9ba4d9c1cdcf863ddbafdc9f581d3e60b1697c00b74fc1ba05ac074c64b3e49. I fully read all 82186 source bytes and 11125 contract bytes, then froze a primary static assessment. Two later adverse hypotheses came from Root and are labeled as such; they were independently executed against the final source. No AUTHORING_REPORT or author result stream was used before the frozen primary dynamic verdict at 2806/SHA6c03ee3a2ee3b4a601c94d6b58405ce7376acd2c88196976c408ab8501e39999. Incidental claimed counts in the intake seal were not treated as evidence.

Independent exact-source tests: **95 cases / 668 checks in each normal and -O mode**. Initial 81/571 plus supplemental 14/97; all four child executions exited 0, had empty stderr, and recorded no prohibited network/process/write event. The harness compiled the authenticated common/publisher/tracker buffers and bound source hashes, result hashes, stdout JSON, exit evidence, interpreter path and Python binary hash. INDEPENDENT_RUNTIME_BINDINGS.json records the bindings. All five sources contain zero ast.Assert nodes. A secondary replay of the authored exact offline suite and runner was performed only after the primary verdict: 491 checks per mode, both exits0 and empty stderr, with exact code-before/after/source-snapshot/stdout/result bindings. Those 491 are **not counted as independent checks**.

## Safety properties checked

| Property | Source mechanism and independent evidence |
|---|---|
| Absent authority disables actions | common lines 70–89 authenticates externally supplied adoption, exact five sources, final gate and independently pinned actual ready pointer; actual case with no authority rejects before transport. Missing gate/ready/source, source/gate drift and substituted ready chains reject. |
| Exact scope/package/metadata | common lines 90–142 checks PR206 / problem 5100062 / HEAD 488e8f575a6c9bcc0bd097d2852c9a7fa19bf8a7, required truths/qualified false claims, distinct canonical whole-package events, reports/Root acceptances, all safe files, one PDF/TEX/ZIP and full metadata. Actual 17 package files and 14 ZIP member byte streams were independently hashed. Tamper, extra file, metadata, one/duplicate/noncanonical event and review corruption reject. |
| Actual custody/ready boundary | common lines 138–156 pins actual custody 1919/SHA b3f5a5e... and priority 5297/SHA f81e10f7..., requires open original draft HEAD and accepted ready90 input map chain. A full synthetic ready map retains the original 4416 actual custody identities. Replacing a self-consistent ready/map chain while adoption remains fixed rejects. |
| Phase and mutation bounds | publisher lines 72–111 separates stage/inspect/publish/inspect-doi; markers are O_EXCL, file+directory fsynced before adapter launch. Preexisting stage/marker/kit state, partial marker write and fsync failure prohibit mutation. Unknown stage and lost publish responses recover by reads with no duplicate mutation. |
| Public evidence | publisher lines 112–133 requires inspect-doi then three independently downloaded byte streams and a separate exact DOI resolver; wrong bytes/size/HTTPS/DOI/host/status/timeout refuse a receipt. The unchanged kit 25740/SHA a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca was hashed read-only; its verify lines 309–358 and fresh remote inspect/publish branches were inspected read-only to verify every manifest metadata field is checked and normalizations are rejected by the helper. The kit was never executed. |
| Tracker destination and row | tracker lines 8–41, 73–91 binds exact spreadsheet/gid 1254632077/tab/headers, searches actual DOI in every cell, derives the next one-row range from the second full baseline, and uses one RAW/INSERT_ROWS four-cell append. Wrong gid/type/tab, duplicates in every column, malformed/partial/count/range/value responses reject. |
| Retention and recovery | tracker lines 55–102 retains typed row multiplicities, original full baseline and marker range; own readback and two fresh full reads must locate the exact unique row at that range. Foreign loss, DOI loss, either late shift, corrupt own row, malformed/timeout second readback reject; lost append recovers read-only with exactly one append. Root's shift-after-own-readback hypothesis rejects at line 95, and second-read shift rejects at line 98. |
| Current truthful text | TRACKER_LIFECYCLE_TEXT_ALIGNMENT.json proves static equality of CLAIM/CREDIT/EFFORT with lifecycle support source, including date 10/20 (October2020), all integer r>=1 repetitions, exact Ferudun credit and qualified effort/AI/unrefereed wording. No lifecycle source was executed. |

## Separate dispatcher assessment

Final Root source: root_publication_ops_runner_01/run_operations206_v2.py, 5148 bytes, SHA3cce6202317f138d4c37f15dabf58f70492e170113a7cfae2f4a9c4918cecb63. All bytes read. **21 normal cases / 62 checks pass**, with empty stderr / exit 0. The exact optimized buffer rejects after importing sys alone, before dependency imports. Tests cover every isolation flag, fixed adoption basename, stale external adoption pin, source/self/gate/ready tamper, mode/symlink/bounds/normalized containment, buffer-only preflight, selection of common plus only the requested publisher/tracker module, fixed kit argument and argv/module-alias cleanup after compile/main/confirmation failures. Offline author modules are never compiled by dispatch.

A direct generic checked() probe in v1 accepted an A/../outside path because containment was lexical. No current CLI reachability was established because main constructs fixed normalized paths. Root conservatively replaced it with v2's strict resolution/equality/containment check. The original witness and exact v1 source/tests remain preserved. The v2 witness rejects, together with outside-A, relative, symlink and overbound paths. No remaining mandatory dispatcher finding was established. This review does not itself adopt either dispatcher.

## Limits and preserved diagnostics

The trusted future boundary is an independently authenticated Root adoption whose exact bytes approve the final whole-package gate and the actual ready90 pointer. The helper validates required inputs in that exact accepted native map; it does not reconstruct Git or independently re-prove all live foreign 4416 custody. That obligation remains with lifecycle acceptance and Root. Pure fakes cannot establish future actual API semantics, credentials, production account state, remote publication, mathematical correctness or scientific novelty.

No actual ready90, final publication gate or live Root operations adoption exists. All test authority/operation values are SYNTHETIC_NON_RECEIPT and remain inside this audit folder. No Git command, backend loader/cache, gws CLI, actual kit launch, HTTP/API, external service or external communication occurred. Internal messages were only to Root.

Every rejected probe is recorded with its exception and expected safety check. No harness test execution failed. The initial large source display was truncated by the tool; the missing offline_guards lines 247–286 range was explicitly reread before execution. The v1 path false acceptance was preserved rather than erased. Initial rough case-count commentary was corrected to actual 81; source/runtime binding metadata records the exact invoked interpreter symlink path and separately hashes its resolved binary. Raw synthetic fixture trees are preserved and separately indexed; the safe payload manifest excludes their bulk bodies and includes reproducible harnesses, results, byte pins and exact tree identities.

Source-audit completion best guess: **100% of this assigned bounded audit**, not mathematical truth, operational readiness or project completion.
