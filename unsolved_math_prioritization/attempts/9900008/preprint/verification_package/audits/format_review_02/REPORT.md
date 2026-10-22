# Independent format review 02 — CLEAR within the stated finite scope

Completed 2026-10-15 12:31:14 UTC. Completion estimate: 100% of this finite tools-format review. This review counts as neither of the two later whole-paper/whole-package reviews.

The repaired pinned format routines pass the independent finite checks. No issue remains from this review's frozen test plan. This conclusion concerns exact compressed-member consumption, tested format outcomes, byte preservation, deterministic construction, and ordinary/optimized consistency. It does not promote a mathematical claim, assess novelty or priority, approve publication, or audit a later assembled final package.

## Independence, inputs, and execution discipline

`PLAN.md` was frozen at 2026-10-15 12:18:44 UTC with SHA-256 `21850dd70fdc13af16231da10834e123ec451c6369018d8ce32b7fb7b2235491`, before any prior review report/verdict was read and before candidate execution. The parent had disclosed the earlier ignored-compressed-suffix failure category. No earlier review report or verdict was consulted. This review independently constructed the ZIP byte fixtures and expected decision table.

The parent's final executable seal was authenticated before use. All four scripts were read: the entire 285-line common prefix was read once and byte-compared across the other three files, then every distinct tail was read. Both archival executable bodies (`source/author/verify.py` and `source/check_publication.py`) were read in full before replay of authenticated private copies. Only standard-library imports occur in these scripts. The review fixture was fully read, and its final small delta was reviewed before rerunning.

| Candidate file | Bytes | SHA-256 |
| --- | ---: | --- |
| `check_originals.py` | 30482 | `e4fb73b16db72ed4387c08c38662a1ad9f836f9b0ecd2ff91778347deb74829b` |
| `verify_package.py` | 16013 | `e80ce30e89547c52d63c44237a554f0b3bf1ae1959783bbbba1f3f1703e9f7f8` |
| `build_verification.py` | 17641 | `2b0521d74a49360cbdd6d48427cb02763b586f3a5196766ec16f6ddc2fa41f2c` |
| `verify_current_publication.py` | 21129 | `3fc89372bae6cc3ed2f6a8d4f93d890e94e9fd635b712223853630d26f034672` |
| `TOOLING_MANIFEST.json` | 1006 | `86290fcc61e5a54a51a2108b55c408961938c45380a9a2bac156fdec8d264585` |
| `README.md` | 9874 | `c4b30b40eaa4afe087cce8b7cd4c985ae90d8587cb46b0110ddae5404a613350` |

The immutable `SOURCE_MANIFEST.json` SHA-256 is `53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab`. All 26 original files (211,771 bytes) were authenticated by length, SHA-256, and original Git blob identifier. `SOURCE_PINS.json` records complete before/after pins. All source/candidate pins were unchanged after both final runs.

All execution used `-I -S -B`; the optimized run additionally used `-O`. The environment was Python 3.14.6 with zlib 1.2.12. Generated packages, copied executable bodies, and nested replay temporary files were under review-owned temporary directories and removed afterward. No source-input write, chmod, truncate, corpus copy, network operation, Git mutation, publication, credential access, or outside contact occurred.

## Independent construction and raw-consumption result

`format_fixture.py` packs local headers, central records, and EOCD records directly with `struct`, using raw DEFLATE from standard-library zlib. It does not use candidate ZIP output or `zipfile` to construct the mutation fixtures. Each mutation reconciles the ZIP compressed sizes and offsets so the tested rejection reaches the compressed-stream layer. A table of compressed bytes, expected plaintext bytes, archive hashes, inflater state, and actual decisions is retained in each results JSON.

The repaired common routine independently decodes the entire declared compressed region with a bound of expected output length plus one byte. It requires exact expected output, inflater EOF, empty unused data, empty unconsumed tail, and full declared-region consumption. The independent fixtures establish that byte-correct first payloads alone do not suffice:

| Case family | Expected and observed result |
| --- | --- |
| Exact binary/CRLF payload; exact empty payload | Accept |
| One zero byte or five inert bytes after the stream | Reject at raw-consumption check, despite exact output and EOF |
| Second empty or nonempty complete raw-DEFLATE stream | Reject at raw-consumption check, despite exact first output and EOF |
| Empty member followed by a zero byte or second stream | Reject at raw-consumption check |
| Empty member with no stream or truncated empty stream | Reject for missing EOF, despite empty output |
| Nonempty stream truncated by 1, 2, or 3 bytes | Reject; the one-byte truncation still yields the entire expected output but lacks EOF |
| Invalid block type | Reject with zlib format error |
| One extra inflated output byte | Reject at bounded exact-output check |
| Incorrect CRC | Reject at CRC check |
| Incorrect declared uncompressed size | Reject at declared-size check |
| Generic valid stored-method representation | Reject at the documented DEFLATE-only metadata policy |

The 15 stream cases were tested through all four scripts in both `generated=False` and `generated=True` modes (120 decisions per interpreter mode). Three metadata/policy cases were tested through all four scripts (12 more decisions per mode). All 132 decisions per mode matched expectation; the complete 264-decision tables are identical between ordinary and optimized Python. A stored-method ZIP is outside the documented accepted format, so its rejection is a policy result rather than a malformed-stream result.

Both immutable historical ZIPs were also accepted by every repaired copy in each mode, with exact expected member bytes: the 18,611-byte author archive (8 members; SHA-256 `bd2a43c1d0de12ea87ba217b3b5316a00e008d1b547992d7bdd038ff695aed9b`) and the 15,301-byte review archive (7 members; SHA-256 `ac46400397200608b0b608908a29f8b3917347e32b0a77f5a14496c10cc197cc`).

## Portable, builder, and outer-wrapper checks

The review built a tiny complete package containing all 26 immutable source files, the three mandatory portable scripts, the exact source manifest, one binary/CRLF inert member, and an empty inert member. Its index SHA-256 is `2d4a6625af2a1a55ee407c0664b6a4911800935e0f587f3db973d7cb8a5d8a66`; the ZIP has 33 members including the index.

Each final interpreter-mode run performed nine CLI invocations, all with empty stderr and expected exit codes:

- Portable verification-only passed and reported zero direct/nested archival executions.
- Default portable verification passed with exactly 6 direct and 16 nested archival executions, including exact historical outputs. The unchanged archival publication body ran under the current isolation-injecting harness, as documented.
- Two default builder invocations passed. Each required the full 6-plus-16 replay before creating its ZIP.
- The current-root wrapper accepted the valid 61-file synthetic outer root, preserving all 26 portable originals and 24 required outer originals. Verification-only remained zero archival executions.
- The current-root wrapper rejected separately reconciled suffix, second-stream, and truncated-stream archives specifically at the raw-consumption check, with structured `REJECTED` and exit code 1.
- A malformed block-type archive produced a structured zlib-error `REJECTED`, exit code 1, in both modes. This exercises the added exception handling rather than merely inferring it from the source.

All four final builder outputs, two in each mode, were byte-identical: 114,777 bytes, SHA-256 `c1cc4d33a00de4070f0b36a3b11feaf89a16f3764c1d3bf1c90d8c0f1d2bcdcf`. Independent `zipfile` reads checked every member against the original input bytes; the binary bytes, CRLF/LF distinctions, empty file, and every original source byte were preserved. Members have fixed 2026-10-15 00:00:00 timestamps, Unix regular-file mode 0644, DEFLATE, and no member extra fields/comments. Reproducibility is established for the tested Python/zlib runtime, consistent with the documented scope.

The final ordinary and optimized runs both started at 12:30:49 UTC and completed at 12:30:55 UTC on 2026-10-15. `COMPARISON.json` verifies cross-mode decisions, original pins, deterministic outputs, and normalized CLI outcomes. Earlier pilot runs passed the same format table and builder checks; they prompted only the additional targeted structured-zlib-error wrapper case recorded in the research log.

## Reproduction and limits

After fully reading/authenticating all executable inputs, run from this review directory:

```text
python3 -I -S -B format_fixture.py .. NORMAL_RESULTS.json
python3 -I -S -B -O format_fixture.py .. OPTIMIZED_RESULTS.json
```

The fixture pins the source and candidate bytes before loading reviewed copies and verifies those pins again afterward. Test archives are regenerated and removed; their exact output hashes and receipts remain in the JSON artifacts. `OUTPUT_PINS.json` and `PUBLIC_MANIFEST.json` authenticate the delivery artifacts without a recursive self-hash claim.

This finite review establishes the listed falsifiable checks for the exact seal. It is not an exhaustive ZIP implementation proof, cross-runtime reproducibility proof, optional large-corpus authentication run, resource-limit stress test, or review of a final package that has not yet been assembled. The current-wrapper valid case used verification-only; full finite diagnostics were separately exercised by the portable verifier and every builder invocation. The two later full reviews remain required by the parent's workflow.

## Publication metadata amendment

2026-10-15T12:36:30Z — Four ephemeral absolute builder-output paths were found in the two public result JSON files. Their exact original files, together with the complete original delivery snapshot, were preserved in an ignored private directory. Only those four path values were normalized to stable `PRIVATE_TMP/built1/verification.zip` or `PRIVATE_TMP/built2/verification.zip`; the public results explicitly mark this transformation. `METADATA_REDACTION.json` records original byte counts/hashes and the changed JSON pointers without exposing the old directories.

The actual fixture stdout files are unchanged. Their `result_bytes` and `result_sha256` fields refer to the privately preserved original results. Every per-CLI `stdout_bytes` and `stdout_sha256` receipt also remains unchanged and describes the original raw subprocess output. Updated output pins authenticate the normalized public JSON. This is a publication-metadata correction: no format check was rerun, no candidate or fixture code changed, no test decision changed, and the finite-scope CLEAR verdict remains in force. Completion estimate: 100% of the amendment and the finite review.
