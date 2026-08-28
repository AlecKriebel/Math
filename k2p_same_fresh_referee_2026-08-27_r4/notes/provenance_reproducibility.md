# Fresh provenance and reproducibility audit — 27 August 2026

## Status

**Provenance/integrity: PASS. Reproducibility engineering examined here: PASS, subject to integration with the root referee's fresh PDF rebuild, archive double-build, and quick/full replay. Human metadata and source-tag release: PASS for the claims actually made.**

I found no provenance or release-engineering blocker in the 20260827 package. This status is not mathematical validation: hash agreement proves identity and ancestry, not any theorem, census, or certificate semantics.

The source archive was read from
`/Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260827.zip`. All work was performed in the reviewer-owned r4 tree. No authoritative source file was edited.

## 1. Outer archive and recursive evidence closure

The independent checker in `independent_checks/provenance/audit_archive_ledgers.py` uses only the Python standard library and imports no submission code.

| Item | Independently observed result | Status |
|---|---:|---|
| distributed ZIP | 214,944,591 bytes; SHA-256 `51f502290434cd3415936ef69e3c5afe71438fa892d5b9e6998feecc47489278` | PASS |
| ZIP members | 491 files; 483,653,934 uncompressed bytes | PASS |
| member safety | zero unsafe paths, duplicate names, case-fold collisions, symlinks, special files, encrypted members, or CRC failures | PASS |
| deterministic metadata | lexicographic order; every member DEFLATE-compressed, mode `100644`, timestamp `2026-08-27 00:00:00` | PASS |
| revised manifest | 490 declared files plus the manifest itself; exact path/byte/hash equality to the ZIP | PASS |
| revised-manifest payload | `e7d40183edc8878ec91ea3a3fc00039225afbcd136a0c5d7af3a20e6b60caa10` | PASS |
| combined content root | `5b7aa44ef814c3ba08eb6b6be86d9a11cf6595b236c5d33e3d7ecd4597b1aaba` | PASS |
| frozen/submission split | 406 frozen files plus 84 submission/support files | PASS |
| release lock | 79,989 bytes; SHA-256 `30132af1b10f7aba6d49ababf14551f9f914a19dc6a0638517761b6b85cf4c8d`; payload `a32e7f04d5c979fc1f9e268ca8a791ae24ad99b296f3e3c72682a3beadadd653` | PASS |
| release-lock direct set | 230 files; ready; no blockers or missing files | PASS |
| recursive frozen closure | 406 files; 479,327,565 bytes; root `3e01609b924a4e884f58916e852fa4e63eaa8ab1a1af3c932de1ecc3498efcd0` | PASS |
| recursive partitions | rank manifest 94; cycle manifest 17; direct closure 60; direct input lock 15 | PASS |
| portable content ledger | exact equality to the independently reconstructed 406-file closure | PASS |

The supplied portable builder was inspected before use. It checks a byte-fixed release-lock hash and payload, promotion readiness, every outer and nested hash, count, byte total, and content root before producing a ledger or ZIP. It rejects symbolic evidence files and optimized Python. Its ZIP writer fixes prefix, order, timestamp, UNIX mode, compression method, and level. The separately implemented revised-bundle checker reconstructs both ledgers and rejects repeated JSON member names.

The source ZIP sidecar contains the same SHA-256 and is itself byte-identical to the sidecar stored at the annotated source tag.

## 2. Source commit, tag, and replay ancestry

The reviewer-owned `audit_tag_binding.py` compared each distributed byte directly with `git show` at the designated tag.

- All 491 distributed files are byte-identical to annotated tag `k2p-same-biorxiv-v1.0.3`.
- Annotated tag object: `83ffef7455ea2e43b887e12d9fb5ade5a867039f`.
- Peeled commit: `79e33706a5563d5c8620b988e27e98119da3487c`.
- A fresh read-only `git ls-remote` returned those same object IDs from `origin`.
- The tag commit is an ancestor of the current repository head. The K2P project tree has no tracked path change between the tag and current head; later commits are reviewer-workspace commits outside this project.
- The archive sidecar matches the ZIP and is byte-identical to the sidecar committed at the tag.

The stored detached replay predates the final packaging/tag commit, so I checked the exact dependency boundary rather than assuming ancestry was enough:

- replay commit `1ef5dd2737a50fd33bc3b15d63e0ba70b050e03f` is an ancestor of the tag;
- all 406 transitive frozen-evidence files at that replay commit are byte-identical to the distributed closure;
- all five article/supplement source files are byte-identical at the replay commit, tag, and distributed package;
- the telemetry's release-lock and source rows agree in path, bytes, and SHA-256;
- the telemetry binds report SHA-256 `5a5f62104bea1e88d725aa3cee0441c369d53905f71fe30bc20de82f4eadb35e` and its 41-layer summary exactly;
- wall time 5,880.83 s is not below internal elapsed time 5,880.415302 s;
- stored runtime is Python 3.14.6, NetworkX 3.5, SymPy 1.14.0.

This establishes provenance for the stored replay but does not substitute for the root referee's fresh full run.

## 3. Article, supplement, source archive, and build report

The independent document checker used `pdfinfo` and `pdffonts` and compared raw bytes, not report assertions.

| File | Bytes | SHA-256 |
|---|---:|---|
| `article/main.tex` | 85,978 | `d1344711d3d85ce5936574ccf54bcfbea1bf4164a0d2b6f5d25d5ecb483991bb` |
| `article/references.bib` | 6,960 | `781dd3503c00d9bbd9c1a7d551786fc4be393e883f7ac4c0b0fd712943a9e5c6` |
| `supplement/supplement.tex` | 46,305 | `e0fe9e08c923a2946c282a3b19aa66c4c6aaa52e762639977024f538295de455` |
| `supplement/compression_tables.tex` | 3,269 | `22ff0534b79cf226c9041703ab9d87ab123914bbb55ec1d44c84041a8616be81` |
| `supplement/certificate_appendix.tex` | 22,405 | `936e8d1879acd224affb053489a618dcfe8d7a7a2a5500bc8f0f85dd1b16794d` |
| article PDF | 194,574 | `a6b91bc5d8864d1ce1a6eb352d00ecdf83712449b41fa4ad041e43a4c06e4858` |
| supplement PDF | 160,272 | `654f9150a2a22be18c651d9bd38864be2a080828dbcdad847d2b344e407ebdb2` |

The PDFs have 26 and 24 pages, respectively; all 50 pages agree with the build report, and all 22 article and 28 supplement font rows are embedded. The submitted logs match their declared hashes and contain zero fatal errors, overfull boxes, undefined citations, undefined references, or hyperref PDF-string warnings. The article's bibliography command and the supplement's two generated `\input` commands are unconditional.

`PDF_BUILD_REPORT.json` is 2,102 bytes, SHA-256 `3e6b49cc14919ba582dc2b54d4222c16adc0bc333c5a6954c8a2f1aad3ddbee6`, and has verified payload `70394f0cb0a4b2947fb64c327431185c2fbd57df5f6c10fd1b5eecea221f0d89`. Its exact source list is the five files above; its engine declaration, Tectonic 0.16.9, matches the installed executable.

The external bioRxiv ZIP is 57,538 bytes, SHA-256 `e9eec990d85d349109a1379b6d322da4e6a073891ba94886db385201d0f8e2e5`. It contains exactly those five files, in the declared order and directory layout, with byte-identical contents, fixed timestamps, mode `100644`, no CRC error, and a matching sidecar.

## 4. Current versus historical authority

The independent authority-partition audit verified the duplicate-free registry payload `0dd650358fc50cdda38605e83a505d0252ed301e619befbbd5bba0b33081d431`.

- All eight scanned historical/revoked/superseded artifact paths are unique, present, and hash-correct.
- Every row has `promotion_authority: false` and at least one existing frozen replacement.
- The scanner scope equals the registry inventory and reports zero unclassified paths in that declared scope.
- No theorem-artifact crosswalk binding points to a release-lock layer labelled historical, legacy, or revoked.
- The frozen computational companion authority is `work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md`, SHA-256 `4acacb925f6aab2ee11baf1c08573b65636b7d867fb816142138ae9fe666a3d2`.
- The release README correctly distinguishes that machine-bound companion from the current article proof authority.

## 5. Round-3 regression closure and fail-closed packaging

The two previous release blockers are closed by mechanisms that were freshly inspected and executed:

1. The static source audit semantically binds exactly 8 path-labelled metadata rows plus 18 frozen-anchor rows. It rejects 9/9 stale, missing, duplicate, relabelled, and missing-target attacks for the intended diagnostic. The two formerly stale `composite_reseal_diff_audit.json` strings now equal the actual SHA-256 `96e30bae42939fa50dd585ba900bc5bd45e5eb122334de86c34654004212db4c`.
2. Both outer JSON readers now use repeated-name-rejecting hooks before interpretation. The 33-case package mutation suite passes with zero survivors, including same-valued and conflicting-valued duplicate-name documents after a valid outer reseal. It also rejects omission of the bibliography, both generated inputs, PDFs, portable content ledger, portable checker, README, source files, licenses, and telemetry bindings.

The portable builder, revised producer, and revised checker each rejected `python -O` with exit 1 and exact `optimized Python is forbidden` output.

## 6. Commands executed in this sub-audit

| Command or independent check | Exit | Wall time | Peak RSS | stdout or result SHA-256 |
|---|---:|---:|---:|---|
| `audit_archive_ledgers.py` | 0 | 3.2 s | 376,619,008 B on timed run | result `d0396f9a708294728f48f2c3d8ceb9e60d05a01af89880224157fbad900183e1` |
| `audit_tag_binding.py` | 0 | 9.5 s | 893,779,968 B on timed run | result `b68801bb5e1b1eba11bc5c7968c6952259eebff74c93c248805ae406ae52f69e` |
| `audit_replay_telemetry.py` | 0 | 7.08 s | 433,061,888 B | result `6e2f485219f32ee8f8b53077ff4d06dcd12e2e750a71cc6e7a210185723118a2` |
| `audit_submission_documents.py` | 0 | 0.3 s | 25,526,272 B on timed run | result `0cb501bf747c66bd035b601e67774e57c59306365894b17aff60041414375be9` |
| `audit_authority_partition.py` | 0 | 0.2 s | not sampled | result `bf5168e38a5f3e2ba184f0c668f6a656ba3ff9b45efb5428e003765920b43602` |
| `output/referee/build_referee_bundle.py --check-only` | 0 | 0.48 s | 229,736,448 B | stdout `734d2963a08ff58fa395001c1973c0153348a902e2c6a1f93085865563b8b217` |
| `build_release_lock.py --check --require-ready` | 0 | 10.03 s | 508,100,608 B | stdout `512b42175588bb9d4c686b57ae122cf28c35619b05a9b364603b996783afa1f0` |
| revised manifest producer `--check` | 0 | 0.99 s | 400,048,128 B | stdout `3fbfd3996b43d536140b597478dd21500cd6e7ae199cce1d34855db086723074` |
| independent revised-manifest checker | 0 | 1.17 s | 399,654,912 B | same summary hash `3fbfd399…` |
| static article audit `--check` after environment setup | 0 | 0.19 s | 41,500,672 B | stdout `a1bd85a53462390549681d5d025a99ea7fb415e2ca5c97d986d3c11ffad2c966` |
| printed-hash focused mutations | 0 | 0.05 s | 27,721,728 B | stdout `af7d96b25558d4a4bfeceea6e69967eba10ed8af612383576b4b508322b1f036` |
| 33 package/crosswalk mutations `--check` | 0 | 25.39 s | 624,295,936 B | stdout `7269bbb13d381069b8ccb235d12c482a674a88c555bac7216f30dabf96a66cea` |

One pre-setup invocation of the static audit exited 1 with `CROSSWALK_PATH_MISSING:.venv/bin/python`. This was the intended clean-copy dependency check, not a stale PASS: after the documented virtual environment was installed, the controlling rerun above passed. The execution environment was macOS 26.5.2 arm64, Python 3.14.6, NetworkX 3.5, SymPy 1.14.0, Tectonic 0.16.9, and Poppler 26.08.0.

## 7. Entry-point and release-boundary notes

The archive intentionally omits the legacy literal names `START_HERE.md`, `verify_handoff.py`, `test_handoff_mutations.py`, `setup_environment.sh`, `run_all_verifiers.py`, and `SUBMISSION_BINDING.json`. `output/referee/README.md` gives an explicit one-to-one mapping to the current portable builder, lock builder, quick/full harness, mutation runner, and ledgers. I therefore record the literal legacy commands as **not runnable by name**, while the current mapped gates are the applicable package protocol. This naming difference is not a mathematical or reproducibility blocker because the current commands and exact closure are included and checked; it must nevertheless remain visible in the final referee's unrun-gate disclosure.

The current revised-manifest architecture declares exactly three supplemental execution dependencies outside the frozen closure: `output/referee/README.md`, `output/referee/REFEREE_BUNDLE_CONTENTS.json`, and `output/referee/build_referee_bundle.py`. All three are included in the 84-file submission ledger, tag-bound, and protected by omission mutations. The older request's five-dependency `SUBMISSION_BINDING.json` vocabulary does not describe this release.

The package claims no GitHub Release, Zenodo deposit, or DOI. Those omissions are deliberate human-controlled release choices, not failed scientific gates. Metadata are mutually consistent: Alec Kriebel, ORCID `0009-0001-9320-500X`, corresponding email `me@aleckriebel.com`, sole-author contribution statement, no specific funding, no competing interests, CC BY 4.0 for article/supplement/data, and MIT for verifier code. The annotated v1.0.3 tag is present and matches the remote object and peeled commit.

## 8. Remaining integration gates

This sub-audit did not duplicate the root referee's long quick/full execution, two fresh archive writes, or PDF rebuild/render workflow. Those are explicitly assigned to the root execution ledger. If any of those fresh controlling runs fails, reproducibility must be downgraded despite the provenance PASS here. No other provenance or metadata action is required.
