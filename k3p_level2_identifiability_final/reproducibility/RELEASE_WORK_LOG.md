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
- Current hostile result: 24/24 rejected, payload
  `32c1cead12dc49f6b211b958d86813499f6468d95df72cd90f4f364058062141`.
  Current release-input payload:
  `60140806939c6e11912ba41d240cc863108c0bcfe9ff97bd99c2cfe9a7bda25e`.
  Submission validation remains honestly NOT_READY with zero structural
  errors and 26 blockers; 12 submission mutations pass.

Best-guess completion: **96% of proof-release implementation and static
adversarial certification; 70% of the external-submission release goal**.
The exact remaining machine gate is the clean post-commit quick/full and
one-shot 42-command regeneration, followed by deterministic archive/source
replays.  Human metadata, license, DOI, tag/release approval, and portal actions
remain outside the machine gate.
