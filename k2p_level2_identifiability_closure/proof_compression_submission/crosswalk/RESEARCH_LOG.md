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
