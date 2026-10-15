# Independent receipt crosscheck

Checkpoint: 2026-10-15 10:02 UTC. Completion estimate: 100% of this receipt-crosscheck subtask. The mathematical discovery goal and final whole-package review remain outside this estimate.

An adversarial subagent independently read the threat model, harness, receipts, relevant candidate guards, and historical regression reproduction. This crosscheck did not execute candidate tools, rerun fixtures, read corpus/PDF contents, contact anyone, or change candidate/source files. Its only authored output is this report.

No blocking inconsistency was found within this scope. The evidence supports a tooling-only pass for the recorded five candidate bodies and synthetic fixtures. It does not establish a final paper/package, mathematical correctness, priority, or whole-package CLEAR.

## Final artifact identity

| Artifact | SHA-256 |
| --- | --- |
| `guard_review.py` | `2e6f922d97d02f118dfab0b0019d08611f46de7e1aabc40b467813b55f20ac43` |
| `RECEIPTS_SOURCE_FREE.json` | `c457d76affce9acbff0364a90d4b38c3fd4fd9e9d7438c3ba7cabd4398a42379` |
| `RECEIPTS_WITH_PROVENANCE.json` | `779c92cd98547fc9dc25ef98054117a33be916c6d2b937c0b81dd51d6ceec95c` |

Both receipts bind the current harness and the same five candidate byte counts/hashes; all matched independently read current bytes. AST inspection found no `assert` statements in any candidate. The current outer verifier is 19,000 bytes with SHA-256 `465f9f4875740f282db18a13d1ea57137bb71708d3e87c1c6d8cf881d191abc6`. The other four candidate hashes remain those in `INITIAL_CANDIDATE_PINS.json`. That intentionally historical file retains the pre-ZIP-fix outer hash and is not the final candidate inventory.

## Receipt meaning and reachability

- Source-free: 335 distinct receipts; provenance: 347 distinct receipts. Stored counts, success flags, and candidate-unchanged flags agree. The source-free total is 10 static + 220 common + 1 original identity + 17 assembly + 54 portable/builder + 25 outer + 7 original-archive + 1 scope receipts. Provenance replaces the one scope receipt with thirteen checks.
- All 224 helper rejections per run are `ValueError` with relevant guard reasons; none pass through the harness's broader `KeyError`/`TypeError` exception allowance. All CLI result objects reconstruct to their recorded stdout byte counts and SHA-256 digests, with zero mismatches.
- Twenty malformed-index CLI cases cover duplicate keys, overflow, NaN, boolean byte counts, and unsafe paths in verifier/builder under ordinary and optimized Python. The harness supplies each malformed index's actual external digest, so the receipts reach the parser or typed/path guard rather than failing the external hash first.
- Four generated-index exact/descendant collision cases now use valid JSON where applicable, check the exact collision reason, and record absent output. The same-size ZIP payload mutation reaches `verification ZIP member differs: README.md`; it no longer stops at the declared-size guard.
- Direct and outer source-free full positives contain eight distinct normal/optimized historical executions with exact-output matches. Provenance full positives contain ten, including the source checker. Verify-only truthfully has zero replay receipts and `NOT_RUN`; source-free full execution keeps source replay `NOT_RUN`. Restrictive-umask, startup-marker nonexecution, allowlist exclusion, and ordinary/optimized reconstruction controls pass.

## ZIP boundary and remaining gap

Final receipts reject all three formerly accepted representations: trailing bytes, prefix bytes, and a local-header timestamp differing from the central directory. Their reasons identify the relevant end, central/end, and local/central guards. The revised harness fails if these observations accept. Inspection confirms contiguous local headers from byte zero, checked local/central names and metadata, and the final central/end boundary.

This supports the tested structural ZIP boundary. It does not show a unique DEFLATE bitstream or fully canonical ZIP representation. Reproducibility is limited to identical inputs and the same Python ZIP implementation/zlib. The probes are finite evidence, not an exhaustive security proof. Final authored paper, final index/ZIP assembly, mathematical/priority review, and mandatory final whole-package review remain unperformed here.

## Historical regression and privacy

`REGRESSION_REPRODUCTION.json` has eight successful observations. Its reproduction-script and shared-harness hashes match current files. Independent in-memory reconstruction, without executing the reconstructed code, yields the exact recorded old verifier and assembler hashes. The record shows old verifier success at umask 022, rejection at 077 in both modes, and old assembler descendant collisions leaving 50 portable / 5 outer files after failure. Current final receipts show the corresponding corrected positive and pre-materialization rejection behavior.

Round-one receipt hashes/counts remain the previously crosschecked 311/323 records. Their historical harness hash was verified before later harness edits; they are remediation evidence rather than final candidate evidence. The naive `872` substring setup issue was corrected to a `PR872` token check before successful round-one receipts and is not a candidate failure.

Inspected public review artifacts contain authored code/prose, synthetic markers, hashes, pin sizes, finite diagnostics, and receipt metadata; no raw corpus/PDF content was found. Provenance records equal before/after input size, permission mode, and SHA-256 for three corpora and two PDFs, and reject the wrong 2012 mapping and leaf alias. Final CLI children inherit a review-private `TMPDIR`; both final run directories were removed. The initial code snapshot was subsequently removed with the remaining private tree, as checked in the addendum below. No repeated PDF marker or final publication action is represented by these records.

## Final docstring-only bridge and cleanup addendum

Checkpoint: 2026-10-15 10:07 UTC. Completion estimate: 100% of this receipt-crosscheck subtask, with the same final-package and scientific exclusions above.

The outer verifier and assembler subsequently received leading module-docstring corrections. The 335/347 behavioral receipts above remain evidence for the pre-docstring bodies; they are not relabeled as full provenance reruns of the final bytes. The final outer verifier is 19,010 bytes / SHA-256 `b8279f4945b2f05b3755bfec20ae6c78dbbb00d053abdb04f87d8068f2ff62a7`; the final assembler is 10,086 bytes / `939fea38779e6df5e81f7930a6a39153a082bcea046ad2879dabc4e0b8115055`. The other three candidates are unchanged.

Independently read current bytes match all five entries in `FINAL_CANDIDATE_PINS.json`, `DOCSTRING_BRIDGE.json`, and `CLEANUP_RECEIPT.json`. Without executing either candidate or rerunning fixtures, reconstructing the old leading prefix gives the exact preceding outer `465f9f4875740f282db18a13d1ea57137bb71708d3e87c1c6d8cf881d191abc6` and assembler `4523285345f0d9df2d8024db419769915494406e4446c27b882d005a62a8a893` hashes. Independent AST comparison removes only the checked leading string-expression node; all remaining AST nodes agree, and the resulting AST hashes match the bridge record. ArgumentParser description text can change through the docstring; the behavioral code is unchanged.

`DOCSTRING_BRIDGE.json` SHA-256 is `6016c3b93cdf65c8257f4686befe237c3ff2eed2f12436d7c84b61c83926e25e`. It binds the current bridge script and shared harness, contains 53 unique all-passed checks, and records unchanged candidate bytes. Its fresh final-byte checks cover synthetic assembly positives/negatives and outer ordinary/optimized inventory/full paths, including eight finite source-free replays and rejection of the three ZIP representation mutants. All recorded CLI result objects reconstruct to their stdout byte counts and hashes. This bridge is explicitly source-free: it is not a new full corpus/PDF provenance run.

The updated regression script matches its recorded digest `fb0150d07e6a4865123e3249d55e242afe3292303295e7803f90b7db2e41df0e`; its new receipt digest is `ec0204b2ee29bf191434865714e98430719d4f11c72e63eb47672a92a7b64c5e`, with eight unique successful observations of the same historical defects. This record remains historical, not a final-candidate failure.

`CLEANUP_RECEIPT.json` records `private_tree_removed: true`, removal of the five remaining snapshot files, and 40 original files / 276,581 bytes unchanged at cleanup. The private directory is independently confirmed absent. The cleanup's final candidate inventory equals both final pins and the bridge inventory. The addendum found no new blocking inconsistency and preserves the tooling-only scope.
