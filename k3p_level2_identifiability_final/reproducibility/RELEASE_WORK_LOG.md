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
