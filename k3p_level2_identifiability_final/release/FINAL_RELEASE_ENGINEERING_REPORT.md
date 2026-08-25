# Final release engineering report

Status: **proof-release tooling complete; final submission envelope blocked by human metadata**

The deterministic quick/full/regeneration orchestration, canonical TAR.GZ
and ZIP construction, compact verifier packaging, source-reproduction check,
pre-DOI envelope binding, safe archive inspection, and hostile release
mutations are implemented.  Ordinary full replay does not rerun the
hour-scale probe producer; full regeneration does, behind a deliberate
one-shot confirmation.

No DOI, license, Git tag, GitHub release, Zenodo record, or portal upload has
been created or claimed.

## Development validation checkpoint

The final pre-commit code-level check on 2026-08-25 used repository base
`a68321f3` (the K3P mathematical/submission corpus remains the one sealed at
`7e43d90c`) before these release files were committed.

- Release-engineering hostile mutations: **31/31 rejected**, payload
  `fc5245fd67f543b2793524c97dc11bbbe13dea42673e38d0704bef814d197d6f`.
  They cover a fake same-version PDF compiler, timestamp/environment drift,
  PDF-equivalent non-HEAD TeX tampering, noncanonical TAR modes, malformed
  fileset policy, direct-child and descendant timeouts, NOT_READY submission
  state, arbitrary/mislabeled journal files, and a well-formed package carrying
  an unbound DRAFT extra, forged suite/source-build reports, selection-lock
  drift, dirty final verification, unknown envelope claims, and tampered
  generated readmes/sidecars, in addition to archive/hash/path controls.
- Normal committed-source release-input gate: **PASS**, payload
  `d865f3f4a024790a8886183e67c31175072acb7ca5786164e8b43138790c9ced`.
- Development quick gate (dirty-tree override explicitly recorded): **PASS**;
  elapsed 0.234 seconds and peak child memory 31,096,832 bytes.  This is not a
  clean-clone Gate J result.
- Compact verifier: built twice byte-identically, extracted artifact replay
  **PASS**, development SHA-256
  `28609574f8eaf1f6ef912efbbf8cec37532f28a7704b1399e7e2979d178307e7`.
  It must be rebuilt after the release-layer commit because the canonical
  source-commit field will change.
- Full independent replay was not repeated: it would duplicate the freshly
  completed approximately three-minute integrated theorem replay.  The fast
  artifact/checksum/crosswalk gate was used instead.
- Full regeneration was deliberately not invoked.  It alone contains the
  hour-scale probe producer and requires the explicit one-shot confirmation.
- The canonical 29-page article and 10-page supplement PDFs are committed at
  the paths required by the fileset policy, with SHA-256 values
  `a50cfeedaeb0c38b484f4ac01e8cca861a87a746ad20d1e43766db3bc752efae`
  and
  `4e20fe62ad4261b2ece54b87a4770a3edf30fe8807851ad48973eaec6db1110c`.
- Source reproduction is bound to Tectonic 0.16.9 and the fixed PDF epoch
  `1787677101`.  It remains unexecuted in this pre-commit checkpoint because
  the source archives deliberately can be built only from a committed release
  layer.
- The 42-command all-producer plan passed static existence/order coverage.
  Its cut verifiers now retain ordinary/optimized mutation reports in the
  required order, all active cut and sharpness producers are included, the
  204-direction search is genuinely fresh, probe timing reports are written
  only to ignored work paths, and per-command timeouts are enforced.
- Submission validation is intentionally **NOT_READY** with zero structural
  errors and 26 explicit blockers (17 unresolved human/repository token
  classes, six absent upload artifacts, and three draft manifest states).
  Twelve targeted submission mutations pass.  The validator rejects external,
  traversing, symlinked, or wrong-type source-map inputs.  The final envelope
  expands an exact HEAD source-map member allowlist, binds every upload byte,
  and refuses arbitrary extras or mislabeled packages; it cannot be generated
  from the current draft sources.

Remaining release gates:

1. Commit the release layer and rebuild all derived assets from that exact
   commit.
2. Run byte-for-byte Tectonic source reproduction for both PDFs.
3. Run quick, full, and the one-shot full-regeneration suite from clean
   checkouts and retain their transcripts.
4. Build and verify the compact and full archives twice, confirming identical
   SHA-256 values.
5. Complete fresh adversarial release review.
6. After the unresolved author declarations, repository facts, and journal
   metadata are supplied,
   generate the journal-ready PDFs and packages.
7. Create a human-approved local exact-HEAD tag, generate the pre-DOI envelope,
   then separately confirm the pushed remote tag.
8. Choose licenses, mint a real DOI, rebuild DOI-bearing packages, and perform
   actual external uploads only through Alec's direct action.
