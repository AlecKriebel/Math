# Release engineering work log

## 2026-08-25T17:22:14Z — deterministic release layer

- Read and implemented frozen-program sections 12, 17, 18, and 21.
- Separated quick artifact binding, bounded full independent replay, and true
  all-producer regeneration.  The hour-scale probe producer appears only in
  the last path and has an explicit one-shot confirmation.
- Added canonical Git-`HEAD`-only TAR.GZ and ZIP construction, safe inspection
  and extraction, compact verifier dependency closure, nested LaTeX source
  archives, source-reproduction verification, final envelope/checksum binding,
  and human-action checklists.
- Added elapsed-time, peak-memory, clean-tree fingerprint, deterministic
  environment, and complete-transcript handling for all three suite entry
  points.
- Added 20 fail-closed release mutations covering stale hashes,
  self-reference, path traversal, timestamp nondeterminism, optimized Python,
  forbidden active evidence, missing active paths, unauthorized PDF engines,
  drift of the fixed PDF source timestamp/environment, PDF-equivalent non-HEAD
  TeX tampering, malformed fileset policies, ineffective timeouts, NOT_READY
  submission state, arbitrary journal files, and mislabeled journal archives.
  Added deterministic double-build, untracked-file exclusion, duplicate-path
  normalization, committed-policy isolation, and 42-command regeneration-plan
  controls.
- Independent audit found a duplicate active-path sort crash.  Replaced tuple
  sorting with path-keyed normalization; missing paths and conflicting hashes
  now fail explicitly.  The regression control and null-path mutation pass.
- Final pre-commit mutation replay: 20/20 rejected, payload
  `97668b0e790fafed7ea28c8bb2d05841c66645f206beca8694838810a03ea11c`.
- Final normal committed-source input gate: PASS, payload
  `8f9f88639316cfe753a8d927302f0c37d7fa5909acfe64c0071e9fbecf4783f3`.
- Compact verifier double-build at source commit `7e43d90c`: byte-identical,
  extracted replay PASS, development SHA-256
  `28609574f8eaf1f6ef912efbbf8cec37532f28a7704b1399e7e2979d178307e7`.

Best-guess completion: **100% of proof-release tooling implementation; 70% of
the full external-submission release goal**.  The audited PDFs and Tectonic
toolchain are present, while the submission validator is deliberately
NOT_READY with zero structural errors and 27 explicit blockers.
Remaining work is execution- and human-metadata-dependent: commit this layer,
run two source reproductions, perform clean quick/full/regeneration runs,
build final archives and journal ZIPs, complete adversarial release audit, and
create a human-approved tag/envelope.  DOI, license, GitHub/Zenodo release, and
journal uploads remain human-only.

## 2026-08-25T18:18:57Z — adversarial boundary hardening checkpoint

- Fast-forwarded the shared `main` branch to `a68321f3` without changing any
  K3P bytes; all 144 overlapping local K2P files were verified byte-identical
  to that remote commit before the recoverable fast-forward guard was removed.
- Pinned the exact arm64 Tectonic 0.16.9 executable, added NumPy 2.5.2 to the
  reproducibility lock, and bound source archives to exact HEAD TeX bytes,
  archive roots, outer commit epochs, fixed PDF epochs, and source-build
  schemas.
- Locked the canonical full and compact member path sets by count and SHA-256;
  proof-only builds now truly omit the two release PDFs.  Canonical builders
  require a clean project, generated readmes are reconstructed exactly, and
  TAR modes, archive metadata, roots, epochs, and both sidecars are verified.
- Suite reports now bind exact 2/4/42-command plans, runner/helper hashes,
  clean tracked fingerprints, complete log bytes, and transcript result rows.
  Timeouts launch a new process session and kill the entire process group; a
  descendant-survival mutation is rejected.
- Submission source-map inputs now require canonical in-project regular
  file/tree types with no symlinks.  The spurious JMB editable-source Boolean
  was removed: editable bytes are instead expanded exactly from the committed
  source map.  Journal packages must equal that expansion plus the six bound
  PDFs, with no unbound extra members.
- Current hostile result: 31/31 rejected, payload
  `fc5245fd67f543b2793524c97dc11bbbe13dea42673e38d0704bef814d197d6f`.
  Current release-input payload:
  `d865f3f4a024790a8886183e67c31175072acb7ca5786164e8b43138790c9ced`.
  Submission validation remains honestly NOT_READY with zero structural
  errors and 26 blockers; 12 submission mutations pass.

Best-guess completion: **96% of proof-release implementation and static
adversarial certification; 70% of the external-submission release goal**.
The exact remaining machine gate is the clean post-commit quick/full and
one-shot 42-command regeneration, followed by deterministic archive/source
replays.  Human metadata, license, DOI, tag/release approval, and portal actions
remain outside the machine gate.

## 2026-08-25T19:44:39Z — one-shot execution diagnosis and deterministic repair

- Clean quick/full, two source reproductions, and compact/full archive
  double-builds passed at `6dc41043a977aeb9ea97f33576bc40aa4b63cb4c`.
- The first all-producer attempt completed commands 1--27, including every
  long mathematical producer through the 2,789.020802-second probe replay.
  Command 28 then failed because its ignored report parent
  `release/work/regeneration_ephemeral/` did not exist.  This is an
  orchestration failure, not a 42-command PASS; no suite JSON was emitted.
  Tracked project bytes remained unchanged.
- `deterministic_environment()` now materializes that parent before the plan
  starts.  The 42-command-plan control checks it explicitly, and a separate
  suffix diagnostic passed commands 28--37 under the repair.  A static audit
  found no other ignored output parent at risk.
- Rejected-case diagnostics now replace random `TemporaryDirectory` nonces by
  a canonical token.  Two independent complete mutation-report writes were
  byte-identical (file SHA-256
  `54ff0c68e1fefae3b4cf1edd33248cff27c8c5dc7e67576099312532d3e03da7`);
  31/31 mutations were rejected with logical payload
  `631ce4b3a4152621466504950e7bf73d44142c2622b064af8cbcc38b049c24f4`.

Best-guess completion: **98% of the paper/certification/proof-archive goal and
70% of the external-submission release goal**.  The remaining machine action
is one unified exact-HEAD run plus commit-bound source/archive reconstruction.
Human metadata, license, DOI, tag/release approval, and portal actions remain
outside this machine checkpoint.

## 2026-08-26T03:42:13Z — clean 45-command fixed point and deterministic assets

- Exact pushed source commit:
  `7b4cdd3197e6d650abafc263cbc8a568d09ddf9f`.
- Clean quick/full/regeneration payloads:
  `63195e8437a90d7dc2a3a5c6b8d1b73d421609d97565a1f9184e0907c304a978`,
  `508843309677738fa04f05701f7e64d53db21b63518976bb49d44bb58c5a6277`,
  and
  `a73fe870142f8c56589ce1a2efd5fdd748d1b51a178b8043244a8c991fe009d7`.
  The unified regeneration completed all 45 commands in 4,301.285 seconds;
  the one-shot probe producer accounted for 2,937.148 seconds.
- Article/supplement source-reproduction logical payloads:
  `b6344bc345d7507663b84cd571702cecdaf1a279da185a9c8196e7469049d6c6`
  and
  `68a657ae62d3f60fa5b6fb68e0428846d00a193ced328d2be9ed24db42683b0e`.
  Each packaged source rebuilt twice and matched the committed PDF byte-for-byte.
- Compact/full archive SHA-256 values:
  `1e2be0e6d1657b763ba91ad3d20dedc7a3e8df58702df33896fb225ec6f08315`
  and
  `28916b14083d305fece3c71cdef1be4af3f6f68708fde3fa363ed03fc834635f`.
  Independent second builds were byte-identical; structural and extracted-gate
  checks passed.

Best-guess completion: **100% of the mathematical and proof-archive machine
goal; 70% of the external-submission goal**.  Submission metadata, license,
tag/release approval, DOI, and portal actions remain human-controlled.

## 2026-08-26T13:52:55Z — conditional-PASS minor-revision reseal

- Exact pushed source commit:
  `e5b0a9fc6cca79d6ab1d6cd96ceb5c4e8be5a2d5`.
- Clean quick/full payloads:
  `b684ca1a018e965271cfecd485cf3679b4d1e17bc93028b1e2328135a838d639`
  and
  `166912a36fb672f3f5ce93aef86f2f0f63fb90a9b7dd77f0fdf061a67cdfa217`.
  The full suite completed in 212.370 seconds and passed fresh theorem replay,
  18/18 integrated mutations, and 32/32 release mutations.
- Article/supplement source-reproduction logical payloads:
  `01a9d8d732c5b8ce16684acbd554fc860fb1604332a46507115926fdcb3e4af5`
  and
  `c224972b4885d47a6899878845283e85f6f3a639604fc0d41b2afc46f444571a`.
  Both packaged sources rebuilt twice and matched the committed PDFs
  byte-for-byte.
- Article/supplement source ZIP SHA-256 values:
  `26e5269503055d65cfb86c5517d52cd863be5878eef8f1fe3dacb2b02f0b0394`
  and
  `f98be392f84a40abe37f2526cf2f6a8901a4b9fcee2c01a689ad0a9ed1e66911`.
- Compact/full archive SHA-256 values:
  `42fc5e9e9d4d2797c6b196683a3e7b517ee8f7c8352b7182a07d143b0f8596cf`
  and
  `e9a6f9f44260df8001364325ac711fceac68a2ef35c9ee141d84cc5688a9f8f9`.
  Independent second builds were byte-identical; structural and extracted-gate
  checks passed.
- No active producer, verifier, or theorem certificate changed.  The prior
  successful 45-command one-shot regeneration remains the exact producer
  evidence; it was not rerun for source prose and PDF resealing.

Best-guess completion: **100% of the mathematical and proof-archive machine
goal; 70% of the external-submission goal**.  Submission metadata, license,
tag/release approval, DOI, and portal actions remain human-controlled.

## 2026-08-26T14:07:04Z — immutable-link source reseal

- Exact pushed source commit:
  `0ddf4a76f1c4cc37ac05dcb0915edcfdce65e057`.
- The article now links the exact certificate/replay snapshot at immutable
  commit `e5b0a9fc6cca79d6ab1d6cd96ceb5c4e8be5a2d5`; no tag was created.
- Clean quick/full payloads:
  `7c5f960aee698b9d027b64ae72ebe266e5a79890bf75f63af3a183091fe82a34`
  and
  `d65da00e795c4515cc390f337d83fe775c17c9a47cef68921c7b50780de827e3`.
  Full completed in 205.782 seconds and passed fresh theorem replay, 18/18
  integrated mutations, and 32/32 release mutations.
- Article/supplement source-reproduction logical payloads:
  `65256d4466cd527090b1a970550aac69c0a0957a3e007b62647805f55054a541`
  and
  `cf9110926d5219275960418d7e9b29093a9708dbc6b784e91481e90745a28523`.
  Both source packages rebuilt twice and matched the committed PDFs.
- Article/supplement source ZIP SHA-256 values:
  `84a2c4d447782c19bd59d99962f16ba7b71dfde15ef7d3ca2386c97a6fbd1b1d`
  and
  `aa364e0bda4edf4a8b6ad5d662c6076ab38792b02f93bd5314bbc8c7fd8797ef`.
- Compact/full archive SHA-256 values:
  `0b6a60c8e2f7ad065f019e10a4d255b3a6cf6af4a42b1e63cdb2533233990033`
  and
  `101ac4f72748013542cfa66587d3edfe3a6f49fb0e9f684f3ca7f68d13f8c8d4`.
  Independent second builds were byte-identical; structural and extracted-gate
  checks passed.
- No mathematical producer, verifier, theorem certificate, or release runner
  changed.  The successful one-shot 45-command execution remains the producer
  evidence and was not repeated for the link-only article rebuild.

Best-guess completion: **100% of the mathematical and proof-archive machine
goal; 70% of the external-submission goal**.  Submission metadata, license,
tag/release approval, DOI, and portal actions remain human-controlled.

## 2026-08-28T05:22:06Z — strengthened referee-repair proof execution

- Exact pushed proof snapshot:
  `203e114ace0ead3852f109a3713acda37bf74e65`.
- Clean quick payload:
  `0a2394d3cc9529c29c9e21a7b602f1793c9b13da0a437939639ece7ebb411cf0`.
- Clean full payload:
  `afdceb98352ff9d7446e8787b8508c07b0bf10e9cd497d74f282120b4b49736d`;
  elapsed time 2,991.443 seconds; fresh integrated replay, 27/27 integrated
  mutations, and 32/32 release mutations all passed.
- The single confirmed 55-command regeneration passed in 8,920.970 seconds
  with payload
  `74ab3e8830f4e0a8e8e1805c9aca591a4ec09d78a160126c183d496db3d6f019`.
  The hour-scale probe producer appeared exactly once and ran for 2,971.512
  seconds.  The runner reported no tracked canonical drift.
- The post-run fixed-epoch article and supplement builds now contain 38 and 14
  pages.  Every page was rendered and inspected; all fonts are embedded.  A
  TeX delimiter error and a one-word supplement orphan were found by the build
  and visual gates and corrected before this checkpoint.
- Source reproduction, proof archives, referee handoff, and Google Drive
  synchronization remain deliberately pending until these source/PDF bytes are
  committed and pushed.

Best-guess completion: **92% of the referee-repair release workstream; 70% of
the external-submission goal**.  Submission metadata, license, tag/release
approval, DOI, and portal actions remain human-controlled.

## 2026-08-28T05:33:18Z — final source, archive, and neutral-referee handoff

- Exact pushed paper/source snapshot:
  `5a6d64cb2a76e890d7baaef3ba5ac9861c1d029f`.
- The 38-page article and 14-page supplement have SHA-256 values
  `2a5c71feaadb0056cd738f6344eca2eb5ee09784ba542070238cc476b141b8db`
  and
  `a1b349bf2ffbdbd290ca2254159dc1304ef299bdbbf8792e7340526d60e985e8`.
  Each source package rebuilt twice and matched its delivered PDF exactly.
- Article/supplement source ZIP SHA-256 values:
  `98a23fac8fee67510ad53f435ed17ecaae983a122bb0d8baa2b6b48c236d81f5`
  and
  `0e26f9b3ae11fad49643776509db9e254c8cbfb16f1714d5c575d48711badec5`.
- Compact/full proof archive SHA-256 values:
  `3cdf9abb59dfdc86e1e95593e7d8aac02802c277b414c931229b57fc22957d0d`
  and
  `6fe6ed56e6c5252fdb269655ec508913c4bd5076448e598fd6141d1b913bc101`.
  Independent second builds are byte-identical, structurally valid, and pass
  extracted artifact-only binding/integrity replay.
- The neutral referee package binds the same source snapshot and full archive,
  seals 622 payload files / 160,506,893 bytes, passes integrity verification,
  and reconstructs the intended 54-command portable regeneration plan.  Its
  manifest SHA-256 is
  `090741f2cf6aa05ee5d9d65528e66980bb6eefd32c7cd25d49c8906fda83c1d0`.
- All 35 tracked TeX/Bib paths were copied to the requested Google Drive paper
  folder and verified with zero missing, extra, or mismatched files.  Their
  logical source-set SHA-256 is
  `cfb41635857a578bbea8c43c4726eccf4fe647f2db382364f5b843f5270e7e4e`.
- The post-typesetting quick suite passed with payload
  `0f6f9537884e8265ba80ae816acb2fe33118b1d8a3c984dc1a0c9fab4df85bd8`.
  The successful full and 55-command one-shot runs at `203e114a...` were not
  repeated for packaging-only work.
- A final read-only audit found two ignored source-reproduction reports from
  the superseded `98308677...` snapshot.  They and their transcripts were
  moved intact to
  `release/work/legacy_referee_source_reproduction_98308677/`; no delivered or
  tracked evidence was removed.

Best-guess completion: **100% of the referee-repair mathematical and local
release workstream; 70% of the external-submission goal**.  Submission remains
fail-closed at `NOT_READY` with zero structural errors and 26 human/release
blockers.  License, tag/release approval, DOI, and portal actions remain
human-controlled.

## 2026-08-29T08:36:00-07:00 — second-referee targeted reseal

- The self-contained K3P directed-cut-inclusion repair was pushed at proof
  snapshot `3710f2a24851bac2a4aee124fc2c5debb5b7c1c5`.  The article availability
  statement now links that immutable snapshot.
- The fixed-epoch linked article has 38 pages and SHA-256
  `5fd4fb902ee72c619c75846e2e5f561b018b4096a659b895063c0758dfc5d9df`;
  the unchanged 14-page revised supplement has SHA-256
  `e82d1afb01f937872ec06ee1b1529fe736362c3496721b99813d8849ff7327e6`.
- The release selection locks now cover 592 full and 383 compact paths.  At
  pushed paper snapshot `2563f8a80e48118eb1216364bb7b8ad2e3b29d38`, the
  release-engineering mutation suite rejects 32/32 cases with payload
  `5c6255a37bfcc094a1769f17b421d6534982384143ce7a65d357a8c351711b05`,
  and the development release-input gate passes.
- No multi-hour mathematical producer was rerun.  The exact atlas, probe,
  restoration, and Krawczyk inputs and implementations did not change; the
  targeted C1 dependency cone and every changed downstream verifier were the
  only mathematical checks replayed.

Best-guess completion: **97% of the second-referee local handoff workstream;
70% of the external-submission goal**.  The remaining local work is the final
archive/referee-package copy, Google Drive source synchronization, and a clean
post-package audit.

## 2026-08-29T08:42:00-07:00 — mode-aware extraction regression repair

- The first rebuilt referee package correctly failed its new inner mode check:
  canonical TAR/ZIP members declared scripts as `0755`, but the safe extraction
  helpers wrote every file with the host default mode.  Payload bytes were
  unaffected; the failure was confined to the new integrity interface.
- Both safe extractors now apply the already verified canonical archive mode
  after writing each regular file.  A focused release-engineering control
  confirms `0755` for extracted scripts and `0644` for extracted data in both
  TAR.GZ and ZIP paths.  The complete 32-mutation suite and the release-input
  gate pass after the fix.

Best-guess completion: **97% of the second-referee local handoff workstream;
70% of the external-submission goal**.

## 2026-08-29T19:24:00-07:00 — third-referee exact-once package replay

- Exact sealed proof/package snapshot:
  `10bd695cc7b7e0fd98a187026059b043589244f0`.
- Canonical full and compact archive SHA-256 values:
  `fecb2eda22bcb0558c02e14fdb7767b4229bde33471a4de2a764191f42d8d293`
  and
  `51e54e2d4eed0d7e980fccbd0319d79e83633a4fad9308c4ed79198112edc014`.
- Referee-package manifest SHA-256:
  `c67c1c524ef59217a2327e7dd4016cd82a9b8be1e8f188e6cc61a4fe1fd6c725`
  (635 files / 161,122,700 bytes).
- The portable `all` runner was launched exactly once under an external
  credential-free macOS sandbox.  It passed 4/4 verify commands in 3,016.565
  seconds and 55/55 regeneration commands in 8,584.394 seconds.  Total elapsed
  time was 11,608.930 seconds; the probe producer ran once in 2,886.752
  seconds.
- Runner summary SHA-256:
  `8aca186fe28786e61d7c25798fecf255b43dcaf9cfd0dc0035802757bc5f0db8`.
  External supervisor summary SHA-256:
  `afafe7d2504a0937028ec021030ad01dea059fcc932d5f6aa8db7941366c18be`.
- Pre/post inventories show an unchanged sealed package and virtual
  environment.  Both phases report zero undeclared workspace drift.  The
  focused file-mode control passes in both phases, including rejection of an
  unsafe `0644` to `0600` replacement.
- The final selective referee folder is
  `~/Documents/Math/k3p_level2_fourth_revision_referee_final_2026-08-29`.
  Runtime evidence is added only under the explicitly unsealed `review_runs/`
  root.  The remaining payload is byte-identical to the canonical package and
  passes the Git-independent package integrity checker.
- The monorepo's later `b49913a...` HEAD differs only in a sibling K2P
  workstream.  The K3P release remains intentionally bound to `10bd695c...`;
  no long command was repeated for unrelated repository movement.

Best-guess completion: **100% of the third-referee local repair/replay
workstream; 70% of the external-submission goal**.
