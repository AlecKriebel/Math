# Complete pre-execution intake ledger

Before any candidate execution, the 26 paths below were authenticated against the separately supplied ORIGINAL_FILE_RECORDS.json digest `610351fbb778f78ce53cda03ea715f38615abb5710690987c214f8093bda13ae` and exact Git commit `b356dec5cb01e5f536b9cfeece56ad08844c03cb`. The initial authentication completed at the timestamp in receipts/original_before.json (2026-10-16T20:27:22.474028+00:00). Its 26 regular files total 147,731 bytes; every Git blob, disk byte string, Git mode 100644 and disk mode 0644 matched. Every text file below was then manually read in full. The archive was inspected with bounded reads of member byte strings and headers, without extraction, before replay began at 2026-10-16T20:28:27.510873+00:00.

Paths are relative to the original attempt root, `unsolved_math_prioritization/attempts/2616`. Full file hashes and sizes are in the before/after authentication receipts; the candidate REPORT.md digest is `ddde58f03f320c881b78e59b60a40f315e1811c7c88aaa25ce620c427afbb6ca`.

| Path | Inspection and scope assessment |
| --- | --- |
| ACCEPTANCE.md | Historical authored mathematical acceptance and software counts; not an independent trust anchor, novelty certificate, or present project acceptance. |
| BOOTSTRAP.py | Externally authenticated before execution. Requires -I -S -B, pins exact manifest and wrapper, rejects linked ancestors and nonregular bounded files; executes authenticated wrapper bytes. |
| PUBLICATION_MANIFEST.json | Exact 24-payload-record manifest; bootstrap independently binds its bytes. The manifest excludes itself and bootstrap to avoid a self-hash cycle. |
| README.md | Replay contract, genuine nonroot requirement, exact bounded software and source-free claims. Fresh source/corpus default NOT_RUN is explicit. |
| audit_1/INDEPENDENT_MATHEMATICAL_AUDIT.md | Historical complete logical review; earlier report hash and final report hash distinguished. Source scope and topology lineage are assertions not freshly recertified by this computational family. |
| audit_2/AUDIT_MANIFEST.json | Historical five-file audit allowlist and acceptance; no current acceptance inferred from its status string. |
| audit_2/AUTHOR_HARNESS_RERUN.json | Byte-identical to author external TEST_RESULTS.json, retaining historical UID1000 and Python3.12.14. |
| audit_2/AUTHOR_SNAPSHOT.json | Twelve author-file bindings plus original archive binding, all matched. |
| audit_2/INDEPENDENT_AUDIT.md | Historical separate infinite reconstruction, source assertions and bounded test report. Its claims about historical original-directory write denial are not reproduced by our immutable-original policy. |
| audit_2/INDEPENDENT_RESULTS.json | Counts 4096,65536,16,57344,65536 sum to192528. Historical runtime/UID and91 malformed input labels retained. |
| audit_2/independent_checks.py | Explicit finite-set reconstruction and original-public write probes. Only executed on owned read-only copies by authenticated replay. Uses explicit exceptions; requires nonroot. Does not model a free ultrafilter. |
| author/external/AUDIT_INSTRUCTIONS.md | Explicit requirement for external tool and manifest authentication and isolated execution. |
| author/external/MANIFEST.json | Six public-file names, exact byte counts and hashes; source strings match actual snapshot. |
| author/external/PINS.json | Five external-file records plus public-manifest pin; no circular authentication of itself claimed. |
| author/external/TEST_RESULTS.json | Historical bounded outcomes for normal/-O/-OO;43533 finite cases,18 malformed fixtures,10 tampering variants per mode. |
| author/external/bootstrap.py | Strict duplicate/nonfinite/shape/type checks; arbitrary nested path names excluded; exact directory entries checked. Authenticates checker and fixture then passes their snapshots to a local isolated child. Its file read is not prebounded by actual st_size; the outer publication wrapper supplies a bound and fixed accepted bytes. |
| author/external/test_harness.py | Actual nonroot/read-only and hostile-import controls on temporary copies,18 malformed variants,10 tampering variants across modes. Temporary mode restoration is limited to its own copies. |
| author/public/README.md | Explicit infinite-proof boundary and external authentication contract; candidate pending status is historically preserved. |
| author/public/REPORT.md | Complete infinite proof manually inspected and independently reconstructed in MATHEMATICAL_RECONSTRUCTION.md. No special-ultrafilter assumption found. No new source/priority conclusion drawn. |
| author/public/fixtures.json | Exactly ten pinned integer fields. Values constrain all checker loops before shifts/enumerations. |
| author/public/provenance.json | Metadata only; corpus hashes are historical metadata here. Fresh corpus rehash NOT_RUN. Pending status and finite-tests-not-proof flags retained. |
| author/public/sources.json | Public URL/hash/size metadata only. No primary bodies retrieved by this family; none of its source/status assertions recertified from those hashes alone. |
| author/public/verify.py | Bounded65537-byte read/65536-byte accepted limit; strict duplicate/nonfinite and exact-integer fixture validation. Finite bit-mask group/coset/size/fiber checks. No assert dependency. Deep JSON recursion is not caught; actual nonzero traceback retained as optional robustness issue. |
| expansive_group_2616_frozen.tar.gz |14 members:2 directories mode0555 and12 ordinary files mode0444, UID/GID0, no linknames/PAX extensions. All member bodies matched corresponding author files; compressed bytes13488. No extraction occurred. |
| mutation_tests.py | Externally authenticated source, actual selected-mode replay/relocated read-only and hostile-import controls plus53 negative controls. Tests malformed manifests, recursive inventory, archive names/types and accepted-evidence pinning. |
| verify_publication.py | Requires -I -S -B; exact recursive inventory; bounded ordinary reads, strict schemas and exact type equality; fixed accepted-evidence pins survive a mutable manifest rehash. Replays authenticated snapshots on actual read-only scratch, checks results/hashes. Does not claim raceproof sandboxing. |

## Execution and mutation boundaries

All candidate source was inspected before execution; it uses standard-library local file and subprocess operations. It contains no network access or external communication code. Our fresh fixtures and hostile modules also only write/read owned local paths. No Git/service mutation, queue/source-cache update, corpus access, publication or communication with other individuals occurred. Read-only Git blob lookup was used for authentication only.

Originals were never chmodded, opened for writing, imported as live modules, executed in place, or extracted. Executed source copies and fixtures are under this effort's fixtures/; disposable directories use this effort's tmp/ through TMPDIR,TMP,TEMP. Authenticated source bytes can execute ordinary local Python children; this is process execution, not a proof of sandbox security. Concurrent adversarial filesystem changes, compromised interpreter/OS, arbitrary remote state changes and whole-machine write monitoring are outside the audit.

The low-level archive helper accepts changed permission metadata and trailing compressed-stream bytes; the integrity wrapper still rejects their changed archive digests even after manifest repinning. The directory inventory allows hardlinks to regular files and does not bind disk permission bits. The exact original inventory/modes were independently checked here, and the replay tests prove denial on owned read-only copies. None of these observations establishes an outer external-pin bypass.

The authentication receipts summarize cat-file output using exact byte counts and digests rather than redistributing original file bodies or the binary archive. Every executed-checker command has raw stdout/stderr in the public receipts. The externally pinned original inventory remains the source of original bodies; fixture copies are deliberately outside the final public allowlist.
