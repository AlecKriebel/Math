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
