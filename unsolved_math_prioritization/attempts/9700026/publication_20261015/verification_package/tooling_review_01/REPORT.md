# Independent PR880 publication-tooling adversarial review

**Disposition: PASS for the reviewed tooling, within the limits below. This is not final whole-package clearance or permission to publish or seal a package.**

This engineering review concerns PR 880, problem 9700026, original head `fba74a301786f9648e48722e76f440097b0746c2`. The external original-source manifest pin is `b0b0cdc72798cfcffc5fefeec1de30ff422f54bde83d0f8a91fd2e6a87311d8b`. The independent threat model was recorded at 2026-10-15 09:49 UTC before candidate-code or engineering-verdict inspection. All five complete candidate bodies and their execution boundaries were subsequently read. The earlier artifact-family report was first read after the independent tests had completed.

No real final paper, final index, final verification ZIP, final outer package, or publication metadata is certified here. Synthetic paper/PDF/README bytes were conspicuously labeled `SYNTHETIC TOOLING FIXTURE -- NOT THE REAL PAPER OR PUBLICATION`. They existed only in ignored disposable fixtures and have been removed. Final real-package review remains mandatory.

## Exact final candidate

| Path relative to the parent audit | Bytes | SHA-256 |
|---|---:|---|
| `preprint/check_originals.py` | 22093 | `e78f97d36210f29e466636861767124a338c9ad0fe48e050eeec2a5355c3771f` |
| `preprint/verify_package.py` | 9852 | `73faad1cfa4ab2e9c7e6cfa214e58fadb361ccf4de3199ed87e96883ae6a351a` |
| `preprint/build_verification.py` | 10648 | `a1d76f65b2438236f2251c0f4dc850140fd1495a6e7ed418bfbf10fc86e23cca` |
| `local_tools/pr880_verify_current_publication.py` | 19010 | `b8279f4945b2f05b3755bfec20ae6c78dbbb00d053abdb04f87d8068f2ff62a7` |
| `local_tools/pr880_assemble.py` | 10086 | `939fea38779e6df5e81f7930a6a39153a082bcea046ad2879dabc4e0b8115055` |

The comprehensive behavioral runs preceded a final description-only correction to the outer and assembler module docstrings. They bind outer hash `465f9f4875740f282db18a13d1ea57137bb71708d3e87c1c6d8cf881d191abc6` / 19000 bytes and assembler hash `4523285345f0d9df2d8024db419769915494406e4446c27b882d005a62a8a893` / 10094 bytes. `docstring_bridge.py` reconstructs those exact preceding source hashes from the final bytes, proves equality of their ASTs after removing only the leading module-docstring node, and runs fresh final-byte assembly and outer-entry-point controls. `DOCSTRING_BRIDGE.json` binds the five final hashes above. No full corpus replay is represented as having used the new docstring bytes. Each run and bridge verified that its live candidate bytes were unchanged during testing. No security-critical `assert` occurs in any candidate; no stale `PR872`/`pr872` or old problem identifier was found. Incidental digest digits `872` are not treated as a stale identifier.

## Findings and remediation

1. **Restrictive-umask replay defect, fixed.** The earlier verifier put `target.chmod(0o644)` outside its relocation loop. Under umask 077, most copied originals therefore became mode 0600 and the original checker correctly refused them. The engineer moved the operation inside the loop. Independent final normal/optimized controls both pass under umask 077. `reproduce_fixed_defects.py` reconstructs the earlier verifier byte-for-byte at hash `3d4baafaa90d17746685a481a74d0267479888ade3c4f8fb9d09df8c1c4288ba`: normal umask 022 passes, while umask 077 fails in both modes.
2. **Generated-index directory collision, fixed.** The engineer identified that a selected `package_index.json/x` or `PUBLICATION_MANIFEST.json/x` could cause failure only after materialization. The assembler now rejects exact and ancestor/descendant generated-index collisions before creating output. Independent portable/outer tests use valid JSON for exact collisions, check the exact intended rejection reason, and confirm no output path exists. An exact-hash reconstruction of the earlier assembler (`608a5a6bb613bb52525cd07ff4db31fed785fd235e2e8c02d50df21971023286`) independently reproduces partial materialization for both descendant cases.
3. **ZIP representation boundary, strengthened.** The first outer wrapper accepted a ZIP prefix, a ZIP trailer, and a local-header DOS time inconsistent with the fixed central timestamp. Logical member payloads and checked central fields were still correct; this was not a bypass of an unchanged externally fixed outer-manifest pin. These accepted boundaries are retained in the two `ROUND1_` receipts. At the root's authorization, the engineer added terminal end-record/central-directory boundary checks, contiguous local headers starting at byte zero, and local/central field and name agreement. The revised wrapper rejects all three exact mutations; normal/optimized valid outer controls pass. No runtime-dependent recompression was added.

## Independent final checks

The comprehensive guard is `guard_review.py`, SHA-256 `2e6f922d97d02f118dfab0b0019d08611f46de7e1aabc40b467813b55f20ac43`. Its final source-free behavioral receipt has SHA-256 `c457d76affce9acbff0364a90d4b38c3fd4fd9e9d7438c3ba7cabd4398a42379`; the authentic-provenance behavioral receipt has SHA-256 `779c92cd98547fc9dc25ef98054117a33be916c6d2b937c0b81dd51d6ceec95c`. Both are bridged to the final description-only changes as just described.

| Category | Source-free run | Provenance run |
|---|---:|---:|
| Total distinct check records | 335 | 347 |
| Positive top-level tool processes | 16 | 22 |
| Rejecting top-level tool processes | 47 | 49 |
| Helper rejection evaluations | 224 | 224 |
| Checked revised ZIP boundary mutations | 3 rejected | 3 rejected |

Counts are check records, not claims of that many independent mathematical tests. Nested finite-checker processes are not added again to the top-level process counts.

The successful controls cover both explicit-allowlist assembly kinds, absence of an unallowlisted sentinel from output, portable inventory-only and full modes, deterministic builder output in normal/optimized Python, outer inventory-only and full modes, and the real original archives. The builder's two ZIP outputs are byte-identical to each other and to the independent same-runtime construction. The implementation's reproducibility claim is limited to the same input bytes, Python ZIP implementation and zlib runtime.

The rejection matrix covers symlink leaves and internal directories, a symlink root, FIFOs, Unix-domain sockets, unlisted files and empty directories, missing files, unsafe/absolute/parent/dot/backslash/colon/control-character paths, file/directory collisions, duplicate inventory rows, bounded reads, negative/boolean/noninteger/oversized counts, duplicate JSON keys, NaN/Infinity and overflow `1e999`. Five malformed index families additionally reach the actual verifier and builder entry points in both normal and optimized Python. Special-file rejection occurs before open, preventing FIFO hangs. No device node was created; ordinary-mode predicates were inspected and a Unix socket supplied the additional special-file test.

ZIP checks include symlink/mode/platform metadata, fixed timestamp, compression method, extras and member/archive comments, duplicate members, a same-length payload alteration, and declared byte-count disagreement. Original nested ZIP and readable-duplicate mutations reject against the externally frozen source inventory. Positive original authentication traverses the author eight-member ZIP, audit nineteen-member ZIP, nested author ZIP, all inner inventories and readable duplicates. These branches cannot be made to accept changed original bytes merely by resealing a current package index because the original source manifest remains hard pinned.

Startup-marker tests change the verifier's bytes while retaining the external index/verifier pins; a second test reseals the index but retains the external verifier pin. Both reject, neither marker executes, and no output is created. The tested caller already trusts the inspected builder body. The original historical publication wrapper is authenticated as a frozen file and is never on the new tools' execution call graph.

## Replay and provenance truthfulness

Each source-free finite replay actually runs eight distinct original checks: author witness/self-test and audit witness/self-test, each under normal and optimized Python. Outputs match the authenticated historical expected outputs exactly, not merely the word PASS. Source-free results explicitly report `source_replay: NOT_RUN`; inventory-only portable results report `full_replay: NOT_RUN`. Original `--verify-only` runs authenticate without launching finite diagnostics and report an empty execution receipt list.

The optional run authenticates all three complete original corpus files and both complete PDFs, including the 2012 PDF at its separately supplied path. It then performs two further original source-checker replays, giving ten checks per full provenance replay. The full corpus is not replaced with a target-row excerpt. Normal/optimized verify-only authenticates the inputs but truthfully retains both replay statuses as NOT_RUN. Wrong 2012-PDF mapping and a 2012-PDF leaf symlink reject. All-or-none source arguments, a lone PDF override and source arguments without `--full` reject at their intended guards.

The five authentic input files' byte counts, SHA-256 digests and permission modes match before and after optional replay. After reading the code, this review allowed only read-only hardlinks with legacy basenames; no input was written, truncated or chmodded. The PDF marker mentioned in the parent task was not repeated: these provenance runs only read and hash PDFs. No raw corpus, canonical-pair content, PDF, extracted third-party text or third-party image is in the public deliverables.

## Independent receipt adversary and operational limits

A separate internal adversarial agent reviewed the harness and receipts without rerunning fixtures. It independently verified counts, hashes, meaningful rejection reasons, distinct actual replay receipts and privacy scope. It caught two weaknesses in the initial guard fixtures: an exact reserved-index name carried invalid JSON, and a changed-size ZIP payload tested the size guard first. Both fixtures were corrected before final runs; exact collision reason and same-length member-difference checks now demonstrate the intended branches. Its final evidence is `CROSSCHECK.md`.

An initial harness setup check used an overly broad substring search for `872` and failed on incidental digest digits. It was corrected before the first successful run. This was a harness issue, not a candidate defect. Final test processes set TMPDIR inside their own ignored review-private run directories. Those runs, optional hardlinks, synthetic packages, startup markers and initial candidate snapshots were removed. `CLEANUP_RECEIPT.json` records cleanup and final original-source/candidate identities. No candidate, original source, corpus/PDF, Git state, PR, release, DOI, spreadsheet, external researcher chat or other external application was changed by this review.

The tools must themselves be independently authenticated before initial Python execution. An index self-reference or a program comparing its own bytes after startup does not establish that trust. External pins are caller trust anchors, not signatures, provenance of human approval, or mathematical certificates. This review assumes a trusted interpreter/standard library and no hostile concurrent filesystem race; it is not a general sandbox. Normal exception cleanup is verified, not cleanup after SIGKILL or hardware failure.

The ZIP checks authenticate the tested structure, boundaries, selected metadata and decompressed payloads; they do not prove a unique DEFLATE compressed bitstream or cross-runtime compressed-byte identity. Finite replays do not prove a universal theorem, novelty, priority, source interpretation or historical execution. The earlier 106 adversarial-rejection claim is not reconstructed or promoted here. Final real paper/metadata/README consistency, final outer/index/ZIP pins and final independent whole-package reviews remain outside this review's completed engineering scope.

Assigned independent tooling-review completion estimate: **100%** after final receipt crosscheck and cleanup. Research-wide discovery/publication completion is the root audit's separate assessment.
