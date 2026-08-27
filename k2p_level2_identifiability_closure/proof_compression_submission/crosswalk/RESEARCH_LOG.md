# Crosswalk and bundle research log

## 2026-08-21 21:30 PDT — Exact crosswalk and draft bundle recipe

- Reconstructed the full 370-file, 434,661,763-byte frozen evidence ledger
  from the outer lock, two nested SHA manifests, and both direct-closure locks.
- Bound 13 theorem layers to exact authority, producer, replay, mutation,
  environment, schema, and file-hash fields.
- Preserved recorded component timings only where a locked JSON field exists;
  quick/full end-to-end runtimes remain explicitly unknown.
- Added the optional supplement compression table at its anticipated input
  point, with the restoration and probe residues labelled `PC-PARTIAL`.
- Built primary and independent manifest checkers, eight semantic mutations,
  optimized-mode rejection, and an explicit no-`assert` AST scan.
- Did not create the large ZIP archive.

Best-guess completion of the crosswalk/bundle subtask: **95%**.  The remaining
5% is the mandatory final reseal after concurrent article and integration
edits stop; the checker is intended to fail until that reseal is performed.

## 2026-08-22 14:55 PDT — Superseding final reseal

- Reconstructed the final 374-file, 434,698,345-byte frozen evidence ledger
  and 73 included submission artifacts, including the two final PDFs, build
  logs, clean full-replay report, and timing/memory telemetry.
- Bound the 35-layer detached full replay at 5,172.89 seconds and added
  fail-closed checks for its exact report hash, telemetry, PDF hashes, source
  hashes, logs, embedded-font/visual verdict, and human-only pending list.
- Expanded the bundle mutation suite from eight to eleven cases, adding false
  full-runtime, omitted-article-PDF, and false-supplement-PDF-hash mutations.
  All eleven are rejected, including after resealing the mutated manifest.
- The deterministic ZIP is built only after this final source seal; its SHA-256
  is kept in an external sidecar to avoid archive self-reference.

Crosswalk/bundle subtask completion: **100%**. Remaining submission decisions
are human metadata, licenses, immutable tag, and DOI timing.

## 2026-08-24 — final-metadata and semantic-evidence reseal machinery

- Replaced every hardcoded prior lock hash, content root, frozen file/byte
  census, 35-layer count, runtime, memory value, and commit with independent
  derivation from the current promotion-ready lock and detached clean-replay
  report/telemetry.
- Bound the approved corresponding address, sole-author contribution,
  funding, competing interests, CC BY 4.0 paper/data license, MIT code
  license, and tag `k2p-same-biorxiv-v1.0.0`. The manifest explicitly records
  that this package creates or claims no GitHub Release, Zenodo deposit, or
  DOI.
- Added exact crosswalk/checker coverage for corrected quartet semantics (six
  bodies, 288 transports), all 4,414,710 quartet terminals over 888 IDs,
  10,084 canonicalizer archetypes, 4,012 strict relations, and the 67,741 /
  71,022 / 5,540 graph-derived parameter-transport ledgers.
- Hardened the PDF checker for report schema v3 and the 24 August reproducible
  epoch. Expanded mutations to target omitted new evidence, false release
  claims, wrong tag/email, false layer count, and omission of the final static
  article audit.
- Deliberately did not regenerate the crosswalk or referee manifest before the
  final release lock and replay are rebuilt. The previously generated files
  are stale by design and must be replaced in the final sealing sequence.

Best-guess completion of the machinery subtask: **98%**. The remaining 2% is
the mechanical final generation/check/mutation pass after the parent workflow
produces the final lock, telemetry, PDFs, and source hash anchors.

## 2026-08-26 — v1.0.2 release-qualification closure

- Bound the final 41-layer clean replay and 25-gate outer mutation result, each
  with zero blockers or survivors, into the reader-facing crosswalk and
  deterministic referee package.
- Rebuilt the 489-member referee archive reproducibly at SHA-256
  `86a286be82ce3c211f556eaa24cf1120aa42e41f716b46cb8752c1d2546053ba`.
- Recorded annotated tag `k2p-same-biorxiv-v1.0.2`, tag object
  `ae537c7e2dacdc1026b30b65fe04daca57b4fd84`, and peeled commit
  `cb7559e0ba5fd72f94bce5941208be0838be878d` as the historical v1.0.2
  source binding.  No GitHub Release, Zenodo deposit, or DOI was created.

Crosswalk/bundle v1.0.2 qualification completion: **100%**.

## 2026-08-27 — round-3 editorial and diagnostic repair opened

- Accepted the referee's chronology correction and updated the companion JC
  citation from repository release v1.1.4 to the DOI-bearing v1.1.7 Zenodo
  preprint and its separate certificate-data DOI.
- Replaced the overstated phrase "immutable source tag" with "versioned
  annotated source tag" and designated `k2p-same-biorxiv-v1.0.3`.  The final
  tag-object and peeled-commit identifiers remain external release metadata;
  embedding the yet-to-be-created peeled commit in the tagged source would be
  self-referential.
- Added bounded, path-sanitized child-output diagnostics and explicit failure
  classes to unexpected parameter-transport mutation rejections without
  relaxing the strict rejection contract.

Best-guess completion of the round-3 editorial/diagnostic repair subtask:
**60%**.  The focused source and runner edits are complete; derived reports,
PDFs, replay bindings, manifest/archive construction, and the v1.0.3 tag remain
for the parent release workflow.

## 2026-08-27 — v1.0.3 release-qualification closure

- Bound a detached clean-checkout replay of the exact five-source set at
  source commit `1ef5dd2737a50fd33bc3b15d63e0ba70b050e03f`.  All 41/41 full layers
  passed with zero blockers in 5,880.83 seconds; report and telemetry hashes
  are `5a5f62104bea1e88d725aa3cee0441c369d53905f71fe30bc20de82f4eadb35e`
  and `200b8f18dcd01c2f9fc4f3013b6963b3b8e8083b1acb6a591e28c6e42f7695e3`.
- Rejected all 25/25 outer release mutations and all 33/33 independent
  package mutations with zero survivors.  The package suite includes
  legitimately resealed same-valued and conflicting-valued duplicate JSON
  name attacks through separately implemented producer and checker parsers.
- Rebuilt the 26-page article and 24-page supplement twice identically,
  inspected all 50 rendered pages, and closed the static source audit with
  zero findings and all 26 printed authority/hash rows bound.
- Built the deterministic referee archive twice byte-identically and checked
  two differently named fresh extractions.  Its SHA-256 is recorded only in
  the external sidecar and project-root status to avoid archive
  self-reference.  The five-source bioRxiv ZIP SHA-256 is
  `e9eec990d85d349109a1379b6d322da4e6a073891ba94886db385201d0f8e2e5`.
- The designated versioned annotated source tag is
  `k2p-same-biorxiv-v1.0.3`.  It is created and pushed only after the final
  source commit; its tag-object and peeled-commit IDs are therefore external
  non-self-referential release metadata.  No GitHub Release, Zenodo deposit,
  DOI, or submission action is part of this qualification.

Crosswalk/bundle v1.0.3 qualification completion: **100%**.
