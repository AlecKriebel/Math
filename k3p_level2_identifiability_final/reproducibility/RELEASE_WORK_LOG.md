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
